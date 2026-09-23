"""Research data management API — safe deletion of experiment/comparison data.

PROTECTED (never deleted):
  - problems table
  - test_cases table (predefined test cases, expected outputs, problem definitions)

DELETABLE (experiment/result data only):
  - comparisons
  - execution_results
  - test_case_results
  - static_analysis_results
  - complexity_data
  - security_findings
  - scores
  - comparison_results
  - statistical_results
  - preflight_results

All deletions use an atomic transaction with rollback on any failure.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.db import models
from backend.db.session import SessionLocal

router = APIRouter(prefix="/api/data-management", tags=["data-management"])


# ---------------------------------------------------------------------------
# The ordered list of all tables that reference comparison_id.
# Delete children before parent (comparisons) to respect FK constraints.
# ---------------------------------------------------------------------------
DEPENDENT_TABLES = [
    models.ExecutionResult,
    models.TestCaseResult,       # FK on comparison_id AND test_case_id — only rows deleted, not test_cases
    models.StaticAnalysisResult,
    models.ComplexityData,
    models.SecurityFinding,
    models.Score,
    models.ComparisonResult,
    models.StatisticalResult,
    models.PreflightResult,
]


def _delete_comparison_ids(session, ids: list[int]) -> dict:
    """Atomically delete all experiment data for the given comparison IDs.

    Never touches problems or test_cases tables.
    Returns counts of deleted rows per table.
    """
    if not ids:
        return {"deleted_comparisons": 0, "tables": {}}

    counts: dict[str, int] = {}

    # Delete dependent rows first
    for model_cls in DEPENDENT_TABLES:
        table_name = model_cls.__tablename__
        deleted = session.query(model_cls).filter(
            model_cls.comparison_id.in_(ids)
        ).delete(synchronize_session=False)
        counts[table_name] = deleted

    # Delete the comparisons themselves
    deleted_comps = session.query(models.Comparison).filter(
        models.Comparison.comparison_id.in_(ids)
    ).delete(synchronize_session=False)
    counts["comparisons"] = deleted_comps

    return {"deleted_comparisons": deleted_comps, "tables": counts}


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------

class DeleteByIdsRequest(BaseModel):
    comparison_ids: List[int]


class DeleteByDateRangeRequest(BaseModel):
    date_from: str   # ISO date string e.g. "2026-01-01"
    date_to: str     # ISO date string e.g. "2026-12-31"


class DeletionPreview(BaseModel):
    comparison_ids: List[int]
    count: int
    earliest: Optional[str]
    latest: Optional[str]
    problems_affected: List[str]
    protected_note: str = "Problems and predefined test cases will NOT be deleted."


# ---------------------------------------------------------------------------
# Helper: preview what would be deleted
# ---------------------------------------------------------------------------

def _build_preview(session, ids: list[int]) -> dict:
    comps = session.query(models.Comparison).filter(
        models.Comparison.comparison_id.in_(ids)
    ).all()
    if not comps:
        return {
            "comparison_ids": [],
            "count": 0,
            "earliest": None,
            "latest": None,
            "problems_affected": [],
            "protected_note": "Problems and predefined test cases will NOT be deleted.",
        }
    dates = [c.created_at for c in comps if c.created_at]
    problems_affected = sorted({c.problem_id for c in comps})
    return {
        "comparison_ids": sorted(ids),
        "count": len(comps),
        "earliest": min(dates).isoformat() if dates else None,
        "latest": max(dates).isoformat() if dates else None,
        "problems_affected": problems_affected,
        "protected_note": "Problems and predefined test cases will NOT be deleted.",
    }


# ---------------------------------------------------------------------------
# GET /api/data-management/summary
# Returns counts of deletable experiment data vs protected data.
# ---------------------------------------------------------------------------

@router.get("/summary")
def data_summary():
    with SessionLocal() as session:
        total_comparisons = session.query(models.Comparison).count()
        research_comparisons = session.query(models.Comparison).filter(
            models.Comparison.is_pilot == 0).count()
        pilot_comparisons = session.query(models.Comparison).filter(
            models.Comparison.is_pilot == 1).count()
        total_problems = session.query(models.Problem).count()
        total_test_cases = session.query(models.TestCase).count()
        return {
            "deletable": {
                "total_comparisons": total_comparisons,
                "research_comparisons": research_comparisons,
                "pilot_comparisons": pilot_comparisons,
            },
            "protected": {
                "problems": total_problems,
                "predefined_test_cases": total_test_cases,
                "note": "Problems and predefined test cases are NEVER deleted.",
            },
        }


# ---------------------------------------------------------------------------
# POST /api/data-management/preview/ids
# Preview what would be deleted for a list of IDs (no deletion performed).
# ---------------------------------------------------------------------------

@router.post("/preview/ids")
def preview_delete_by_ids(req: DeleteByIdsRequest):
    with SessionLocal() as session:
        return _build_preview(session, req.comparison_ids)


# ---------------------------------------------------------------------------
# POST /api/data-management/preview/date-range
# Preview deletions by date range.
# ---------------------------------------------------------------------------

@router.post("/preview/date-range")
def preview_delete_by_date_range(req: DeleteByDateRangeRequest):
    try:
        dt_from = datetime.fromisoformat(req.date_from)
        dt_to = datetime.fromisoformat(req.date_to + "T23:59:59")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")

    with SessionLocal() as session:
        comps = session.query(models.Comparison).filter(
            models.Comparison.created_at >= dt_from,
            models.Comparison.created_at <= dt_to,
        ).all()
        ids = [c.comparison_id for c in comps]
        return _build_preview(session, ids)


# ---------------------------------------------------------------------------
# POST /api/data-management/preview/all
# Preview deleting ALL comparison data.
# ---------------------------------------------------------------------------

@router.post("/preview/all")
def preview_delete_all():
    with SessionLocal() as session:
        ids = [c.comparison_id for c in session.query(models.Comparison).all()]
        return _build_preview(session, ids)


# ---------------------------------------------------------------------------
# DELETE /api/data-management/comparisons/{id}
# Delete a single comparison and all its dependent experiment data.
# ---------------------------------------------------------------------------

@router.delete("/comparisons/{comparison_id}")
def delete_one_comparison(comparison_id: int):
    with SessionLocal() as session:
        comp = session.get(models.Comparison, comparison_id)
        if not comp:
            raise HTTPException(status_code=404, detail=f"Comparison {comparison_id} not found.")
        try:
            result = _delete_comparison_ids(session, [comparison_id])
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed and was rolled back: {e}")

    # Verify problems and test_cases untouched
    _verify_protected_data_intact()
    return {
        "success": True,
        "deleted_comparisons": result["deleted_comparisons"],
        "tables": result["tables"],
        "protected_note": "Problems and predefined test cases were NOT deleted.",
    }


# ---------------------------------------------------------------------------
# DELETE /api/data-management/comparisons
# Delete multiple comparisons by IDs.
# ---------------------------------------------------------------------------

@router.delete("/comparisons")
def delete_comparisons_by_ids(req: DeleteByIdsRequest):
    if not req.comparison_ids:
        raise HTTPException(status_code=400, detail="No comparison IDs provided.")

    with SessionLocal() as session:
        # Verify all IDs exist
        existing = {c.comparison_id for c in session.query(models.Comparison.comparison_id).filter(
            models.Comparison.comparison_id.in_(req.comparison_ids)).all()}
        missing = set(req.comparison_ids) - existing
        if missing:
            raise HTTPException(status_code=404,
                                detail=f"Comparison IDs not found: {sorted(missing)}")
        try:
            result = _delete_comparison_ids(session, req.comparison_ids)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed and was rolled back: {e}")

    _verify_protected_data_intact()
    return {
        "success": True,
        "deleted_comparisons": result["deleted_comparisons"],
        "tables": result["tables"],
        "protected_note": "Problems and predefined test cases were NOT deleted.",
    }


# ---------------------------------------------------------------------------
# DELETE /api/data-management/by-date-range
# Delete all comparisons created within a date range.
# ---------------------------------------------------------------------------

@router.delete("/by-date-range")
def delete_by_date_range(req: DeleteByDateRangeRequest):
    try:
        dt_from = datetime.fromisoformat(req.date_from)
        dt_to = datetime.fromisoformat(req.date_to + "T23:59:59")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")

    with SessionLocal() as session:
        comps = session.query(models.Comparison).filter(
            models.Comparison.created_at >= dt_from,
            models.Comparison.created_at <= dt_to,
        ).all()
        ids = [c.comparison_id for c in comps]
        if not ids:
            return {"success": True, "deleted_comparisons": 0, "tables": {},
                    "protected_note": "Problems and predefined test cases were NOT deleted."}
        try:
            result = _delete_comparison_ids(session, ids)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed and was rolled back: {e}")

    _verify_protected_data_intact()
    return {
        "success": True,
        "deleted_comparisons": result["deleted_comparisons"],
        "tables": result["tables"],
        "protected_note": "Problems and predefined test cases were NOT deleted.",
    }


# ---------------------------------------------------------------------------
# DELETE /api/data-management/all
# Delete ALL comparison/experiment data. Requires confirmed=true query param.
# ---------------------------------------------------------------------------

@router.delete("/all")
def delete_all_comparisons(confirmed: bool = False):
    if not confirmed:
        raise HTTPException(
            status_code=400,
            detail="Deletion of all data requires confirmed=true query parameter."
        )

    with SessionLocal() as session:
        ids = [c.comparison_id for c in session.query(models.Comparison).all()]
        if not ids:
            return {"success": True, "deleted_comparisons": 0, "tables": {},
                    "protected_note": "No comparisons existed. Problems and predefined test cases were NOT deleted."}
        try:
            result = _delete_comparison_ids(session, ids)
            session.commit()
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Deletion failed and was rolled back: {e}")

    _verify_protected_data_intact()
    return {
        "success": True,
        "deleted_comparisons": result["deleted_comparisons"],
        "tables": result["tables"],
        "protected_note": "Problems and predefined test cases were NOT deleted.",
    }


# ---------------------------------------------------------------------------
# Internal integrity check — always verify protected data after any deletion
# ---------------------------------------------------------------------------

def _verify_protected_data_intact():
    """Raise an error if problems or test_cases were accidentally deleted."""
    with SessionLocal() as session:
        prob_count = session.query(models.Problem).count()
        tc_count = session.query(models.TestCase).count()
        if prob_count == 0:
            raise RuntimeError("CRITICAL: Problems table is empty after deletion — rollback required!")
        if tc_count == 0:
            raise RuntimeError("CRITICAL: Test cases table is empty after deletion — rollback required!")
