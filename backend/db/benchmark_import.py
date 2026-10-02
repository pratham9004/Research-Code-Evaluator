"""Import saved benchmark execution JSON files into the SQLite research dataset."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from sqlalchemy import or_

from backend.config import PROJECT_ROOT
from backend.db import models
from backend.db.seed import load_problems
from backend.db.session import SessionLocal

BENCHMARK_RESULTS_DIR = PROJECT_ROOT / "AI VS HUMAN CODE" / "benchmark_execution_results"


def _to_int(value: Any, default: int | None = None) -> int | None:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None


def _status_for_result(result: dict[str, Any], default: str = "MISSING") -> str:
    status = str(result.get("status") or result.get("execution_status") or default).upper()
    if status not in {"PASS", "FAIL", "ERROR", "TIMEOUT", "MISSING"}:
        return default
    return status


def _safe_case_list(result: dict[str, Any]) -> list[dict[str, Any]]:
    cases = result.get("cases") or []
    return cases if isinstance(cases, list) else []


def _human_entry(problem_id: str, human_reference: dict[str, Any]) -> dict[str, Any]:
    entry = human_reference.get(problem_id, {}) if isinstance(human_reference, dict) else {}
    if not isinstance(entry, dict):
        entry = {}
    status = str(entry.get("status") or "MISSING").upper()
    if status not in {"PASS", "FAIL", "ERROR", "TIMEOUT", "MISSING"}:
        status = "MISSING"
    return {
        "status": status,
        "function": entry.get("function") or problem_id,
        "error": entry.get("error"),
        "source_code": entry.get("source_code"),
        "cases": _safe_case_list(entry),
        "cases_total": _to_int(entry.get("cases_total"), default=len(_safe_case_list(entry))),
        "cases_passed": _to_int(entry.get("cases_passed")),
        "cases_failed": _to_int(entry.get("cases_failed")),
        "cases_error": _to_int(entry.get("cases_error")),
        "timeout_count": _to_int(entry.get("timeout_count")),
        "pass_rate": _to_float(entry.get("pass_rate")),
        "execution_time_ms": _to_float(entry.get("execution_time_ms")),
        "stdout": entry.get("stdout"),
        "stderr": entry.get("stderr"),
        "exit_code": _to_int(entry.get("exit_code")),
    }


def _ensure_comparison_row(session, problem_id: str, language: str, ai_name: str, problem_version: int, test_case_version: int, result: dict[str, Any], human_result: dict[str, Any], generated_at: datetime | None) -> models.Comparison:
    ai_source_code = str(result.get("source_code") or "")
    human_source_code = str(human_result.get("source_code") or "")
    existing = (
        session.query(models.Comparison)
        .filter(models.Comparison.problem_id == problem_id)
        .filter(models.Comparison.language == language)
        .filter(models.Comparison.ai_name == ai_name)
        .filter(models.Comparison.is_pilot == 0)
        .filter(or_(models.Comparison.ai_source_code == ai_source_code,
                    models.Comparison.ai_source_code.like("Imported benchmark result for %")))
        .filter(or_(models.Comparison.human_source_code == human_source_code,
                    models.Comparison.human_source_code.like("Imported human reference status:%")))
        .order_by(models.Comparison.comparison_id.desc())
        .first()
    )

    if existing is None:
        comparison = models.Comparison(
            problem_id=problem_id,
            language=language,
            ai_name=ai_name,
            ai_source_code=str(result.get("source_code") or ""),
            human_source_code=str(human_result.get("source_code") or ""),
            status="incomplete",
            created_at=generated_at or datetime.now(timezone.utc),
            completed_at=generated_at or datetime.now(timezone.utc),
            is_pilot=0,
            experiment_type="RESEARCH",
            problem_version=problem_version,
            test_case_version=test_case_version,
        )
        session.add(comparison)
        session.flush()
        return comparison

    existing.ai_source_code = str(result.get("source_code") or "")
    existing.human_source_code = str(human_result.get("source_code") or "")
    existing.status = "incomplete"
    existing.completed_at = generated_at or existing.completed_at or datetime.now(timezone.utc)
    existing.is_pilot = 0
    existing.experiment_type = "RESEARCH"
    existing.problem_version = problem_version
    existing.test_case_version = test_case_version
    return existing


def _persist_execution(session, comparison_id: int, code_variant: str, result: dict[str, Any], test_case_ids: list[int] | None = None) -> None:
    cases = _safe_case_list(result)
    total = _to_int(result.get("cases_total"), default=len(cases))
    passed = _to_int(result.get("cases_passed"), default=sum(1 for c in cases if (c.get("status") or "").upper() == "PASS"))
    failed = _to_int(result.get("cases_failed"), default=sum(1 for c in cases if (c.get("status") or "").upper() == "FAIL"))
    error = _to_int(result.get("cases_error"), default=sum(1 for c in cases if (c.get("status") or "").upper() == "ERROR"))
    timeout = _to_int(result.get("timeout_count"), default=sum(1 for c in cases if (c.get("status") or "").upper() == "TIMEOUT"))
    pass_rate = _to_float(result.get("pass_rate"), default=(passed / total * 100.0 if total else None))
    execution_time_ms = _to_float(result.get("execution_time_ms"))
    status = _status_for_result(result)

    existing = (
        session.query(models.ExecutionResult)
        .filter(models.ExecutionResult.comparison_id == comparison_id)
        .filter(models.ExecutionResult.code_variant == code_variant)
        .first()
    )
    if existing is None:
        session.add(
            models.ExecutionResult(
                comparison_id=comparison_id,
                code_variant=code_variant,
                total_test_cases=total,
                passed_count=passed,
                failed_count=failed,
                error_count=error,
                timeout_count=timeout,
                pass_rate=pass_rate,
                execution_time_ms=execution_time_ms,
                execution_status=status,
                stdout=result.get("stdout"),
                stderr=result.get("stderr"),
                exit_code=result.get("exit_code"),
            )
        )
    else:
        existing.total_test_cases = total
        existing.passed_count = passed
        existing.failed_count = failed
        existing.error_count = error
        existing.timeout_count = timeout
        existing.pass_rate = pass_rate
        existing.execution_time_ms = execution_time_ms
        existing.execution_status = status
        existing.stdout = result.get("stdout")
        existing.stderr = result.get("stderr")
        existing.exit_code = result.get("exit_code")

    session.query(models.TestCaseResult).filter(models.TestCaseResult.comparison_id == comparison_id).filter(models.TestCaseResult.code_variant == code_variant).delete()
    for case in cases:
        case_index = _to_int(case.get("index"), default=None)
        mapped_test_case_id = (
            test_case_ids[case_index]
            if test_case_ids is not None and case_index is not None and 0 <= case_index < len(test_case_ids)
            else case_index
        )
        if mapped_test_case_id is None:
            continue
        session.add(
            models.TestCaseResult(
                comparison_id=comparison_id,
                code_variant=code_variant,
                test_case_id=mapped_test_case_id,
                status=str(case.get("status") or "UNKNOWN").upper(),
                actual_output=case.get("actual"),
                expected_output=case.get("expected"),
                error=case.get("error"),
                execution_time_ms=_to_float(case.get("execution_time_ms")),
                exit_code=_to_int(case.get("exit_code")),
                stdout=case.get("stdout"),
                stderr=case.get("stderr"),
            )
        )


def _persist_summary_metrics(session, comparison_id: int, ai_result: dict[str, Any], human_result: dict[str, Any]) -> None:
    session.query(models.ComparisonResult).filter(models.ComparisonResult.comparison_id == comparison_id).delete()
    session.query(models.Score).filter(models.Score.comparison_id == comparison_id).delete()

    def observed(result: dict[str, Any], field: str) -> float | None:
        value = _to_float(result.get(field))
        if value is not None:
            return value
        cases = _safe_case_list(result)
        if field == "pass_rate" and cases:
            return round(sum(1 for c in cases if str(c.get("status", "")).upper() == "PASS") / len(cases) * 100.0, 3)
        return None

    ai_pass, human_pass = observed(ai_result, "pass_rate"), observed(human_result, "pass_rate")
    ai_time, human_time = observed(ai_result, "execution_time_ms"), observed(human_result, "execution_time_ms")
    metric_rows = [("reliability", ai_pass, human_pass), ("performance", ai_time, human_time)]
    for metric, ai_value, human_value in metric_rows:
        diff = ai_value - human_value if ai_value is not None and human_value is not None else None
        if diff is None:
            direction = None
        elif metric == "performance":
            direction = "AI" if ai_value < human_value else "HUMAN" if ai_value > human_value else "COMPARABLE"
        else:
            direction = "AI" if ai_value > human_value else "HUMAN" if ai_value < human_value else "COMPARABLE"
        pct = round(diff / abs(human_value) * 100.0, 3) if diff is not None and human_value not in (0.0, 0) else None
        session.add(
            models.ComparisonResult(
                comparison_id=comparison_id,
                metric=metric,
                ai_value=ai_value,
                human_value=human_value,
                difference=diff,
                direction=direction,
                percentage_difference=pct,
                statistical_status="aggregate_only" if diff is not None else "incomplete_pair",
            )
        )

    dims = [(variant, dimension, value) for variant, values in (("AI", (ai_pass, ai_time)), ("HUMAN", (human_pass, human_time)))
            for dimension, value in zip(("reliability", "performance"), values)]
    for variant, dimension, value in dims:
        session.add(
            models.Score(
                comparison_id=comparison_id,
                code_variant=variant,
                dimension=dimension,
                raw_value=value,
                normalized_value=None,
                weighted_value=None,
                dimension_score=None,
                overall_score=None,
                scoring_config_version=1,
                normalization_population_min=None,
                normalization_population_max=None,
                normalization_population_n=None,
            )
        )


def import_all_benchmark_results(result_files: list[Path] | None = None) -> int:
    """Import the active raw Python collection by default.

    Pass explicit result files to import an archived dataset. Imports are
    idempotent for the same source/model/problem identity.
    """
    load_problems()
    imported = 0
    if result_files is not None:
        files = sorted(result_files)
    else:
        active_file = BENCHMARK_RESULTS_DIR / "python_chatgpt_human_p001_p050_execution_results.json"
        files = [active_file] if active_file.is_file() else []
    for result_file in files:
        payload = json.loads(result_file.read_text(encoding="utf-8"))
        language = str(payload.get("language") or result_file.name.split("_")[0]).lower()
        generated_at = _parse_ts(payload.get("generated_at_utc"))
        human_reference = payload.get("human_reference") or {}
        model_results = payload.get("models") or {}
        execution_only = payload.get("collection_mode") == "raw_execution"

        for ai_name, problem_map in model_results.items():
            if not isinstance(problem_map, dict):
                continue
            for problem_id, result in problem_map.items():
                if not isinstance(result, dict):
                    continue
                human_result = _human_entry(problem_id, human_reference)
                with SessionLocal() as session:
                    comparison = _ensure_comparison_row(
                        session,
                        problem_id=problem_id,
                        language=language,
                        ai_name=ai_name,
                        problem_version=1,
                        test_case_version=1,
                        result=result,
                        human_result=human_result,
                        generated_at=generated_at,
                    )
                    test_case_ids = [tc.test_case_id for tc in session.query(models.TestCase).filter_by(problem_id=problem_id).order_by(models.TestCase.test_case_id).all()]
                    ai_exec = dict(result)
                    ai_cases = _safe_case_list(result)
                    ai_total = _to_int(result.get("cases_total"), default=len(ai_cases)) or 0
                    human_valid = human_result.get("status") in {"PASS", "FAIL", "ERROR", "TIMEOUT"} and bool(human_result.get("cases")) and bool(human_result.get("source_code"))
                    ai_valid = _status_for_result(result) in {"PASS", "FAIL", "ERROR", "TIMEOUT"} and bool(ai_cases) and ai_total == len(ai_cases)
                    comparison.status = ("execution_only" if execution_only else "completed") if ai_valid and human_valid else "incomplete"
                    _persist_execution(session, comparison.comparison_id, "AI", ai_exec, test_case_ids)
                    human_exec = {
                        "status": human_result["status"],
                        "pass_rate": None,
                        "execution_time_ms": None,
                        "cases_total": 0,
                        "cases_passed": 0,
                        "cases_failed": 0,
                        "cases_error": 0,
                        "timeout_count": 0,
                        "cases": [],
                        "stderr": human_result.get("error"),
                    }
                    if human_result.get("cases"):
                        human_exec.update(human_result)
                    _persist_execution(session, comparison.comparison_id, "HUMAN", human_exec, test_case_ids)
                    if execution_only:
                        # Raw collection records intentionally have no comparative
                        # score rows or winner direction.
                        session.query(models.ComparisonResult).filter_by(comparison_id=comparison.comparison_id).delete()
                        session.query(models.Score).filter_by(comparison_id=comparison.comparison_id).delete()
                    else:
                        _persist_summary_metrics(session, comparison.comparison_id, result, human_exec)
                    session.commit()
                    imported += 1
    return imported


if __name__ == "__main__":
    count = import_all_benchmark_results()
    print(f"Imported {count} benchmark records.")
