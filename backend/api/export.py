"""Research dataset export API (CSV / JSON / Excel / PDF)."""
from __future__ import annotations

import csv
import io
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse, StreamingResponse

from backend.db import models
from backend.db.session import SessionLocal
from backend.export.report import generate_research_report
from backend.export.pdf_report import generate_pdf_report

router = APIRouter(prefix="/api/export", tags=["export"])


def _gather_rows(session):
    comparisons = session.query(models.Comparison).order_by(models.Comparison.comparison_id).all()
    rows = []
    for c in comparisons:
        scores = session.query(models.Score).filter_by(comparison_id=c.comparison_id).all()
        comp = {r.metric: r for r in session.query(models.ComparisonResult).filter_by(
            comparison_id=c.comparison_id).all()}

        def val(metric, variant, field):
            for s in scores:
                if s.dimension == metric and s.code_variant == variant:
                    return getattr(s, field)
            return None

        def comp_val(metric, variant):
            r = comp.get(metric)
            return getattr(r, f"{'ai' if variant == 'AI' else 'human'}_value") if r else None

        rows.append({
            "comparison_id": c.comparison_id,
            "problem_id": c.problem_id,
            "language": c.language,
            "ai_name": c.ai_name,
            "experiment_type": c.experiment_type,
            "is_pilot": bool(c.is_pilot),
            "ai_pass_rate": comp_val("reliability", "AI"),
            "human_pass_rate": comp_val("reliability", "HUMAN"),
            "ai_execution_time_ms": comp_val("performance", "AI"),
            "human_execution_time_ms": comp_val("performance", "HUMAN"),
            "ai_maintainability": comp_val("maintainability", "AI"),
            "human_maintainability": comp_val("maintainability", "HUMAN"),
            "ai_security_findings": comp_val("security", "AI"),
            "human_security_findings": comp_val("security", "HUMAN"),
            "ai_complexity": comp_val("complexity", "AI"),
            "human_complexity": comp_val("complexity", "HUMAN"),
            "ai_quality_findings": comp_val("code_quality", "AI"),
            "human_quality_findings": comp_val("code_quality", "HUMAN"),
            "ai_overall_score": comp_val("overall", "AI"),
            "human_overall_score": comp_val("overall", "HUMAN"),
            "overall_direction": comp.get("overall").direction if comp.get("overall") else None,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        })
    return rows


@router.get("/dataset")
def export_dataset(format: str = "csv"):
    with SessionLocal() as session:
        rows = _gather_rows(session)
    if format == "json":
        return JSONResponse(content={"comparisons": rows})
    if format == "csv":
        if not rows:
            return PlainTextResponse("comparison_id\n", media_type="text/csv")
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        return PlainTextResponse(buf.getvalue(), media_type="text/csv")
    raise HTTPException(status_code=400, detail="format must be csv or json")


@router.get("/research-report")
def export_research_report():
    buf = generate_research_report()
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=research_report.xlsx"},
    )


@router.get("/research-report/pdf/{comparison_id}")
def export_research_report_pdf(comparison_id: int):
    try:
        data = generate_pdf_report(comparison_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Comparison not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")
    content_type = "application/pdf" if data[:4] == b"%PDF" else "text/html"
    return StreamingResponse(
        io.BytesIO(data),
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename=research_report_{comparison_id}.pdf"},
    )

