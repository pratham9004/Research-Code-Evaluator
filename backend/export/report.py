"""Research report generation (Excel workbook)."""
from __future__ import annotations

import io
import re
from datetime import datetime, timezone
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

from backend.config import SCORING_YAML
from backend.db import models
from backend.db.session import SessionLocal
from backend.scoring.scoring import load_config
from backend.statistics.statistics import compute_statistics

_ILLEGAL_XML_CHARACTERS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _autosize(ws) -> None:
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                val = str(cell.value) if cell.value is not None else ""
                max_length = max(max_length, len(val))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = min(max_length + 2, 80)


def _header(ws, row: int, headers: list[str]) -> None:
    fill = PatternFill(start_color="1e3a8a", end_color="1e3a8a", fill_type="solid")
    font = Font(color="ffffff", bold=True)
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=h)
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def _write_sheet(ws, headers: list[str], rows: list[dict], start_row: int = 1) -> None:
    _header(ws, start_row, headers)
    for r_idx, row in enumerate(rows, start_row + 1):
        for c_idx, h in enumerate(headers, 1):
            val = row.get(h)
            # Excel worksheet strings cannot contain XML 1.0 control characters.
            if isinstance(val, str):
                val = _ILLEGAL_XML_CHARACTERS.sub("", val)
            ws.cell(row=r_idx, column=c_idx, value=val)
    _autosize(ws)


def _problem_sheet(wb: Workbook, session) -> None:
    problems = session.query(models.Problem).order_by(models.Problem.problem_id).all()
    test_cases = session.query(models.TestCase).order_by(models.TestCase.test_case_id).all()
    tc_map: dict[str, list] = {}
    for tc in test_cases:
        tc_map.setdefault(tc.problem_id, []).append(tc)

    headers = [
        "problem_id", "title", "description", "category", "difficulty",
        "supported_languages", "version", "active", "input_spec", "output_spec",
        "constraints", "starter_template", "signature_python", "signature_java",
        "entry_function", "test_case_id", "input", "expected_output", "case_type",
    ]
    rows = []
    for p in problems:
        p_tcs = tc_map.get(p.problem_id, [])
        if not p_tcs:
            rows.append({
                "problem_id": p.problem_id,
                "title": p.title,
                "description": p.description,
                "category": p.category,
                "difficulty": p.difficulty,
                "supported_languages": str(p.supported_languages),
                "version": p.version,
                "active": p.active,
                "input_spec": p.input_spec,
                "output_spec": p.output_spec,
                "constraints": p.constraints,
                "starter_template": p.starter_template,
                "signature_python": p.signature_python,
                "signature_java": p.signature_java,
                "entry_function": p.entry_function,
                "test_case_id": None,
                "input": None,
                "expected_output": None,
                "case_type": None,
            })
        else:
            for tc in p_tcs:
                rows.append({
                    "problem_id": p.problem_id,
                    "title": p.title,
                    "description": p.description,
                    "category": p.category,
                    "difficulty": p.difficulty,
                    "supported_languages": str(p.supported_languages),
                    "version": p.version,
                    "active": p.active,
                    "input_spec": p.input_spec,
                    "output_spec": p.output_spec,
                    "constraints": p.constraints,
                    "starter_template": p.starter_template,
                    "signature_python": p.signature_python,
                    "signature_java": p.signature_java,
                    "entry_function": p.entry_function,
                    "test_case_id": tc.test_case_id,
                    "input": tc.input,
                    "expected_output": tc.expected_output,
                    "case_type": tc.case_type,
                })

    ws = wb.create_sheet("Problems & Test Cases")
    _write_sheet(ws, headers, rows)


def generate_research_report() -> io.BytesIO:
    buf = io.BytesIO()
    wb = Workbook()
    wb.remove(wb.active)

    with SessionLocal() as session:
        cfg = load_config()

        comparisons = session.query(models.Comparison).order_by(models.Comparison.comparison_id).all()
        exec_results = (
            session.query(models.ExecutionResult)
            .order_by(models.ExecutionResult.comparison_id, models.ExecutionResult.code_variant)
            .all()
        )
        tc_results = (
            session.query(models.TestCaseResult)
            .order_by(models.TestCaseResult.comparison_id, models.TestCaseResult.code_variant, models.TestCaseResult.test_case_id)
            .all()
        )
        complexity = (
            session.query(models.ComplexityData)
            .order_by(models.ComplexityData.comparison_id, models.ComplexityData.code_variant, models.ComplexityData.metric_name)
            .all()
        )
        security = (
            session.query(models.SecurityFinding)
            .order_by(models.SecurityFinding.comparison_id, models.SecurityFinding.code_variant)
            .all()
        )
        static_results = (
            session.query(models.StaticAnalysisResult)
            .order_by(models.StaticAnalysisResult.comparison_id, models.StaticAnalysisResult.code_variant)
            .all()
        )
        scores = (
            session.query(models.Score)
            .order_by(models.Score.comparison_id, models.Score.code_variant, models.Score.dimension)
            .all()
        )
        comparisons_data = (
            session.query(models.ComparisonResult)
            .order_by(models.ComparisonResult.comparison_id, models.ComparisonResult.metric)
            .all()
        )

        exec_map: dict[int, dict] = {}
        for e in exec_results:
            exec_map.setdefault(e.comparison_id, {})[e.code_variant] = e
        comp_map: dict[int, dict] = {}
        for r in comparisons_data:
            comp_map.setdefault(r.comparison_id, {})[r.metric] = r

        score_map: dict[int, dict] = {}
        for s in scores:
            score_map.setdefault(s.comparison_id, {})[(s.code_variant, s.dimension)] = s

        complexity_map: dict[int, dict] = {}
        for c in complexity:
            complexity_map.setdefault(c.comparison_id, {})[(c.code_variant, c.metric_name)] = c

        tc_map: dict[int, dict] = {}
        for r in tc_results:
            tc_map.setdefault(r.comparison_id, {})[r.test_case_id] = r

        # Sheet 1: Executive Summary
        summary_rows = []
        for c in comparisons:
            problem = session.get(models.Problem, c.problem_id)
            summary_rows.append({
                "comparison_id": c.comparison_id,
                "problem_id": c.problem_id,
                "problem_title": problem.title if problem else None,
                "category": problem.category if problem else None,
                "difficulty": problem.difficulty if problem else None,
                "language": c.language,
                "ai_name": c.ai_name,
                "experiment_type": c.experiment_type,
                "is_pilot": bool(c.is_pilot),
                "problem_version": c.problem_version,
                "test_case_version": c.test_case_version,
                "status": c.status,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "completed_at": c.completed_at.isoformat() if c.completed_at else None,
                "ai_source_code": c.ai_source_code,
                "human_source_code": c.human_source_code,
            })
        ws = wb.create_sheet("Executive Summary")
        _write_sheet(ws, [
            "comparison_id", "problem_id", "problem_title", "category", "difficulty",
            "language", "ai_name", "experiment_type", "is_pilot", "problem_version",
            "test_case_version", "status", "created_at", "completed_at",
            "ai_source_code", "human_source_code",
        ], summary_rows)

        # Sheet 2: Executive Result
        exec_summary_rows = []
        for c in comparisons:
            cid = c.comparison_id
            ai_exec = exec_map.get(cid, {}).get("AI")
            hu_exec = exec_map.get(cid, {}).get("HUMAN")
            overall = comp_map.get(cid, {}).get("overall")
            exec_summary_rows.append({
                "comparison_id": cid,
                "ai_overall_score": overall.ai_value if overall else None,
                "human_overall_score": overall.human_value if overall else None,
                "difference": overall.difference if overall else None,
                "percentage_difference": overall.percentage_difference if overall else None,
                "direction": overall.direction if overall else None,
                "ai_execution_status": ai_exec.execution_status if ai_exec else None,
                "human_execution_status": hu_exec.execution_status if hu_exec else None,
                "ai_pass_rate": ai_exec.pass_rate if ai_exec else None,
                "human_pass_rate": hu_exec.pass_rate if hu_exec else None,
                "ai_execution_time_ms": ai_exec.execution_time_ms if ai_exec else None,
                "human_execution_time_ms": hu_exec.execution_time_ms if hu_exec else None,
                "neutral_statement": "This result applies only to this comparison and does not establish a universal superiority of AI-generated code.",
            })
        ws = wb.create_sheet("Experiment Details")
        _write_sheet(ws, [
            "comparison_id", "ai_overall_score", "human_overall_score", "difference",
            "percentage_difference", "direction", "ai_execution_status", "human_execution_status",
            "ai_pass_rate", "human_pass_rate", "ai_execution_time_ms", "human_execution_time_ms",
            "neutral_statement",
        ], exec_summary_rows)

        # Sheet 3: Reliability
        reliability_rows = []
        for c in comparisons:
            cid = c.comparison_id
            ai_exec = exec_map.get(cid, {}).get("AI")
            hu_exec = exec_map.get(cid, {}).get("HUMAN")
            reliability_rows.append({
                "comparison_id": cid,
                "ai_total": ai_exec.total_test_cases if ai_exec else None,
                "ai_passed": ai_exec.passed_count if ai_exec else None,
                "ai_failed": ai_exec.failed_count if ai_exec else None,
                "ai_errors": ai_exec.error_count if ai_exec else None,
                "ai_timeouts": ai_exec.timeout_count if ai_exec else None,
                "ai_pass_rate": ai_exec.pass_rate if ai_exec else None,
                "human_total": hu_exec.total_test_cases if hu_exec else None,
                "human_passed": hu_exec.passed_count if hu_exec else None,
                "human_failed": hu_exec.failed_count if hu_exec else None,
                "human_errors": hu_exec.error_count if hu_exec else None,
                "human_timeouts": hu_exec.timeout_count if hu_exec else None,
                "human_pass_rate": hu_exec.pass_rate if hu_exec else None,
                "formula": "Pass Rate = (Passed / Total) × 100",
            })
        ws = wb.create_sheet("Reliability")
        _write_sheet(ws, [
            "comparison_id",
            "ai_total", "ai_passed", "ai_failed", "ai_errors", "ai_timeouts", "ai_pass_rate",
            "human_total", "human_passed", "human_failed", "human_errors", "human_timeouts", "human_pass_rate",
            "formula",
        ], reliability_rows)
        ws.freeze_panes = "A2"

        # Sheet 4: Test Case Results
        # Build test-case lookup: test_case_id → case_type + problem_id
        all_tcs = session.query(models.TestCase).all()
        tc_meta = {tc.test_case_id: tc for tc in all_tcs}
        # comparison → problem_id lookup
        cmp_problem = {c.comparison_id: c.problem_id for c in comparisons}

        tc_rows = [{
            "comparison_id": r.comparison_id,
            "problem_id": cmp_problem.get(r.comparison_id, ""),
            "code_variant": r.code_variant,
            "test_case_id": r.test_case_id,
            "case_type": tc_meta[r.test_case_id].case_type if r.test_case_id in tc_meta else "functional",
            "status": r.status,
            "actual_output": r.actual_output,
            "expected_output": r.expected_output,
            "error": r.error,
            "execution_time_ms": r.execution_time_ms,
        } for r in tc_results]
        ws = wb.create_sheet("Test Case Results")
        _write_sheet(ws, [
            "comparison_id", "problem_id", "code_variant", "test_case_id", "case_type",
            "status", "actual_output", "expected_output", "error", "execution_time_ms",
        ], tc_rows)

        ws.freeze_panes = "A2"

        # Sheet: Preflight Results
        preflight_rows = [{
            "comparison_id": p.comparison_id,
            "code_variant": p.code_variant,
            "status": p.status,
            "message": p.message,
            "checked_at": p.checked_at.isoformat() if p.checked_at else None,
        } for p in session.query(models.PreflightResult).order_by(
            models.PreflightResult.comparison_id, models.PreflightResult.code_variant).all()]
        ws = wb.create_sheet("Preflight Results")
        _write_sheet(ws, [
            "comparison_id", "code_variant", "status", "message", "checked_at",
        ], preflight_rows)
        ws.freeze_panes = "A2"

        # Sheet 5: Performance
        performance_rows = []
        for c in comparisons:
            cid = c.comparison_id
            ai_exec = exec_map.get(cid, {}).get("AI")
            hu_exec = exec_map.get(cid, {}).get("HUMAN")
            ai_norm = score_map.get(cid, {}).get(("AI", "performance"))
            hu_norm = score_map.get(cid, {}).get(("HUMAN", "performance"))
            ai_time = ai_exec.execution_time_ms if ai_exec else None
            hu_time = hu_exec.execution_time_ms if hu_exec else None
            performance_rows.append({
                "comparison_id": cid,
                "ai_execution_time_ms": ai_time,
                "human_execution_time_ms": hu_time,
                "difference": round((ai_time or 0) - (hu_time or 0), 3) if ai_time and hu_time else None,
                "percentage_difference": round((ai_time - hu_time) / abs(hu_time) * 100, 3) if hu_time and ai_time and hu_time != 0 else None,
                "ai_normalized_score": ai_norm.normalized_value if ai_norm else None,
                "human_normalized_score": hu_norm.normalized_value if hu_norm else None,
                "direction": "lower_is_better",
                "note": "Lower execution time represents better observed performance.",
            })
        ws = wb.create_sheet("Performance")
        _write_sheet(ws, [
            "comparison_id", "ai_execution_time_ms", "human_execution_time_ms",
            "difference", "percentage_difference", "ai_normalized_score", "human_normalized_score",
            "direction", "note",
        ], performance_rows)
        ws.freeze_panes = "A2"


        # Sheet 5: Complexity & Maintainability
        comp_rows = [{
            "comparison_id": c.comparison_id,
            "code_variant": c.code_variant,
            "metric_name": c.metric_name,
            "raw_value": c.raw_value,
        } for c in complexity]
        ws = wb.create_sheet("Maintainability")
        _write_sheet(ws, [
            "comparison_id", "code_variant", "metric_name", "raw_value",
        ], comp_rows)

        # Sheet 6: Security Findings
        sec_rows = [{
            "comparison_id": s.comparison_id,
            "code_variant": s.code_variant,
            "tool": s.tool,
            "tool_version": s.tool_version,
            "severity": s.severity,
            "rule": s.rule,
            "category": s.category,
            "message": s.message,
            "location": s.location,
        } for s in security]
        ws = wb.create_sheet("Security")
        _write_sheet(ws, [
            "comparison_id", "code_variant", "tool", "tool_version", "severity",
            "rule", "category", "message", "location",
        ], sec_rows)
        ws.freeze_panes = "A2"

        # Security Evidence sheet — per-comparison security summary with tool status
        sec_evidence_rows = []
        for c in comparisons:
            cid = c.comparison_id
            problem = session.get(models.Problem, c.problem_id)
            sec_relevance = problem.security_relevance if problem else "unknown"
            for variant in ("AI", "HUMAN"):
                variant_static = [f for f in static_results if f.comparison_id == cid and f.code_variant == variant]
                variant_sec = [f for f in security if f.comparison_id == cid and f.code_variant == variant]

                # Determine security tool name and status
                def _sec_tool_name(lang):
                    return "Bandit" if lang == "python" else "SpotBugs"

                def _sec_status(static_list, lang):
                    tool_kw = "bandit" if lang == "python" else "spotbugs"
                    for f in static_list:
                        msg = (f.message or "").lower()
                        if f.rule == "TOOL_UNAVAILABLE" and tool_kw in msg:
                            return "TOOL_UNAVAILABLE"
                        if tool_kw in msg and "analysis completed" in msg:
                            return "COMPLETED"
                    return "COMPLETED"

                tool_name = _sec_tool_name(c.language)
                tool_status = _sec_status(variant_static, c.language)
                tool_ver = next((f.tool_version for f in variant_sec if f.tool_version), "N/A")
                findings_count = len(variant_sec)

                # Severity breakdown
                high = sum(1 for f in variant_sec if (f.severity or "").lower() == "high")
                medium = sum(1 for f in variant_sec if (f.severity or "").lower() in ("medium", "moderate"))
                low = sum(1 for f in variant_sec if (f.severity or "").lower() == "low")

                sec_evidence_rows.append({
                    "comparison_id": cid,
                    "problem_id": c.problem_id,
                    "problem_title": problem.title if problem else c.problem_id,
                    "language": c.language,
                    "experiment_type": c.experiment_type,
                    "is_pilot": bool(c.is_pilot),
                    "code_variant": variant,
                    "security_tool": tool_name,
                    "tool_version": tool_ver,
                    "tool_status": tool_status,
                    "findings_count": findings_count,
                    "high_severity": high,
                    "medium_severity": medium,
                    "low_severity": low,
                    "security_relevance": sec_relevance,
                    "note": (
                        "Tool unavailable — no security analysis performed. Score uses zero findings."
                        if tool_status == "TOOL_UNAVAILABLE"
                        else f"Analysis completed — {findings_count} finding(s)."
                    ),
                })

        ws = wb.create_sheet("Security Evidence")
        _write_sheet(ws, [
            "comparison_id", "problem_id", "problem_title", "language",
            "experiment_type", "is_pilot", "code_variant",
            "security_tool", "tool_version", "tool_status",
            "findings_count", "high_severity", "medium_severity", "low_severity",
            "security_relevance", "note",
        ], sec_evidence_rows)
        ws.freeze_panes = "A2"

        # Sheet 8: Complexity
        complexity_rows = []
        for c in comparisons:
            cid = c.comparison_id
            ai_norm = score_map.get(cid, {}).get(("AI", "complexity"))
            hu_norm = score_map.get(cid, {}).get(("HUMAN", "complexity"))
            ai_vals = {k: v.raw_value for (v2, k), v in complexity_map.get(cid, {}).items() if v2 == "AI"}
            hu_vals = {k: v.raw_value for (v2, k), v in complexity_map.get(cid, {}).items() if v2 == "HUMAN"}
            row = {
                "comparison_id": cid,
                "ai_cyclomatic": ai_vals.get("cyclomatic_avg"),
                "ai_function_length": ai_vals.get("function_length_avg"),
                "ai_nesting": ai_vals.get("nesting_depth_avg"),
                "ai_coupling": ai_vals.get("coupling"),
                "human_cyclomatic": hu_vals.get("cyclomatic_avg"),
                "human_function_length": hu_vals.get("function_length_avg"),
                "human_nesting": hu_vals.get("nesting_depth_avg"),
                "human_coupling": hu_vals.get("coupling"),
                "ai_normalized_score": ai_norm.normalized_value if ai_norm else None,
                "human_normalized_score": hu_norm.normalized_value if hu_norm else None,
                "difference": round((ai_norm.normalized_value or 0) - (hu_norm.normalized_value or 0), 3) if ai_norm and hu_norm else None,
                "direction": "lower_is_better",
                "note": "Lower complexity represents better observed maintainability.",
            }
            complexity_rows.append(row)
        ws = wb.create_sheet("Complexity")
        _write_sheet(ws, [
            "comparison_id", "ai_cyclomatic", "ai_function_length", "ai_nesting", "ai_coupling",
            "human_cyclomatic", "human_function_length", "human_nesting", "human_coupling",
            "ai_normalized_score", "human_normalized_score", "difference", "direction", "note",
        ], complexity_rows)
        ws.freeze_panes = "A2"

        # Sheet 9: Code Quality
        quality_rows = []
        for c in comparisons:
            cid = c.comparison_id
            ai_findings = [s for s in static_results if s.comparison_id == cid and s.code_variant == "AI" and s.category == "code_quality"]
            hu_findings = [s for s in static_results if s.comparison_id == cid and s.code_variant == "HUMAN" and s.category == "code_quality"]
            ai_norm = score_map.get(cid, {}).get(("AI", "code_quality"))
            hu_norm = score_map.get(cid, {}).get(("HUMAN", "code_quality"))
            quality_rows.append({
                "comparison_id": cid,
                "ai_findings_count": len(ai_findings),
                "human_findings_count": len(hu_findings),
                "ai_normalized_score": ai_norm.normalized_value if ai_norm else None,
                "human_normalized_score": hu_norm.normalized_value if hu_norm else None,
                "direction": "lower_is_better",
                "note": "Fewer code-quality findings represent better observed code quality.",
            })
        ws = wb.create_sheet("Code Quality")
        _write_sheet(ws, [
            "comparison_id", "ai_findings_count", "human_findings_count",
            "ai_normalized_score", "human_normalized_score", "direction", "note",
        ], quality_rows)
        ws.freeze_panes = "A2"

        # Sheet 7: Static Analysis Findings
        static_rows = [{
            "comparison_id": s.comparison_id,
            "code_variant": s.code_variant,
            "tool_name": s.tool_name,
            "tool_version": s.tool_version,
            "rule": s.rule,
            "category": s.category,
            "severity": s.severity,
            "message": s.message,
            "source_location": s.source_location,
            "raw_result": s.raw_result,
        } for s in static_results]
        ws = wb.create_sheet("Raw Static Analysis")
        _write_sheet(ws, [
            "comparison_id", "code_variant", "tool_name", "tool_version", "rule",
            "category", "severity", "message", "source_location", "raw_result",
        ], static_rows)

        # Sheet 8: Scores & Calculations
        score_rows = []
        for s in scores:
            score_rows.append({
                "comparison_id": s.comparison_id,
                "code_variant": s.code_variant,
                "dimension": s.dimension,
                "raw_value": s.raw_value,
                "normalized_value": s.normalized_value,
                "normalization_population_min": s.normalization_population_min,
                "normalization_population_max": s.normalization_population_max,
                "normalization_population_n": s.normalization_population_n,
                "weighted_value": s.weighted_value,
                "dimension_score": s.dimension_score,
                "overall_score": s.overall_score,
                "scoring_config_version": s.scoring_config_version,
            })
        ws = wb.create_sheet("Scores & Calculations")
        _write_sheet(ws, [
            "comparison_id", "code_variant", "dimension", "raw_value",
            "normalized_value", "normalization_population_min", "normalization_population_max",
            "normalization_population_n", "weighted_value", "dimension_score",
            "overall_score", "scoring_config_version",
        ], score_rows)

        # Sheet 9: AI vs Human Comparison
        comp_out_rows = [{
            "comparison_id": r.comparison_id,
            "metric": r.metric,
            "ai_value": r.ai_value,
            "human_value": r.human_value,
            "difference": r.difference,
            "direction": r.direction,
            "percentage_difference": r.percentage_difference,
            "statistical_status": r.statistical_status,
        } for r in comparisons_data]
        ws = wb.create_sheet("AI vs Human Comparison")
        _write_sheet(ws, [
            "comparison_id", "metric", "ai_value", "human_value", "difference",
            "direction", "percentage_difference", "statistical_status",
        ], comp_out_rows)

        # Sheet 10: AI vs Human Summary
        summary_rows = []
        for c in comparisons:
            cid = c.comparison_id
            overall = comp_map.get(cid, {}).get("overall")
            if not overall:
                continue
            summary_rows.append({
                "comparison_id": cid,
                "problem_id": c.problem_id,
                "problem_title": session.get(models.Problem, c.problem_id).title if session.get(models.Problem, c.problem_id) else c.problem_id,
                "language": c.language,
                "ai_name": c.ai_name,
                "ai_overall": overall.ai_value,
                "human_overall": overall.human_value,
                "difference": overall.difference,
                "direction": overall.direction,
                "percentage_difference": overall.percentage_difference,
            })
        ws = wb.create_sheet("AI vs Human Summary")
        _write_sheet(ws, [
            "comparison_id", "problem_id", "problem_title", "language", "ai_name",
            "ai_overall", "human_overall", "difference", "direction", "percentage_difference",
        ], summary_rows)

        # Sheet 11: Statistical Results
        persisted_stats = session.query(models.StatisticalResult).order_by(models.StatisticalResult.comparison_id, models.StatisticalResult.metric).all()
        stat_rows = []
        for s in persisted_stats:
            stat_rows.append({
                "comparison_id": s.comparison_id,
                "metric": s.metric,
                "test": s.test,
                "n_paired": s.n_paired,
                "statistic": s.statistic,
                "p_value": s.p_value,
                "significant": s.significant,
                "effect_size": s.effect_size,
                "status": s.status,
                "alpha": s.alpha,
                "dataset_used": s.dataset_used,
                "computed_at": s.computed_at.isoformat() if s.computed_at else None,
            })
        if not stat_rows:
            ws = wb.create_sheet("Statistical Results")
            ws.cell(row=1, column=1, value="No statistical data available yet.")
            ws.cell(row=2, column=1, value="Statistical analysis requires multiple paired comparisons.")
        else:
            ws = wb.create_sheet("Statistical Results")
            _write_sheet(ws, [
                "comparison_id", "metric", "test", "n_paired", "statistic", "p_value",
                "significant", "effect_size", "status", "alpha", "dataset_used", "computed_at",
            ], stat_rows)

        # Sheet 11: Problems & Test Cases
        # Sheet 14: Source Code
        source_rows = []
        for c in comparisons:
            source_rows.append({
                "comparison_id": c.comparison_id,
                "ai_source_code": c.ai_source_code,
                "human_source_code": c.human_source_code,
            })
        ws = wb.create_sheet("Source Code")
        _write_sheet(ws, ["comparison_id", "ai_source_code", "human_source_code"], source_rows)
        ws.freeze_panes = "A2"
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical="top")

        _problem_sheet(wb, session)

        # Sheet 12: Methodology / Scoring Reference
        ws = wb.create_sheet("Methodology & Scoring Reference")
        ws.cell(row=1, column=1, value="Research Title")
        ws.cell(row=1, column=2, value="An Empirical Study on the Reliability, Security, and Maintainability of AI-Generated Code in Software Development.")
        ws.cell(row=3, column=1, value="Overall Score Formula")
        ws.cell(row=3, column=2, value="Overall Score = Σ (Normalized Dimension Score × Dimension Weight)")
        ws.cell(row=5, column=1, value="Dimension")
        ws.cell(row=5, column=2, value="Weight")
        ws.cell(row=5, column=3, value="Direction")
        ws.cell(row=6, column=1, value="Reliability")
        ws.cell(row=6, column=2, value=cfg["overall_score"]["dimensions"][0]["weight"])
        ws.cell(row=6, column=3, value=cfg["overall_score"]["dimensions"][0]["direction"])
        ws.cell(row=7, column=1, value="Performance")
        ws.cell(row=7, column=2, value=cfg["overall_score"]["dimensions"][1]["weight"])
        ws.cell(row=7, column=3, value=cfg["overall_score"]["dimensions"][1]["direction"])
        ws.cell(row=8, column=1, value="Maintainability")
        ws.cell(row=8, column=2, value=cfg["overall_score"]["dimensions"][2]["weight"])
        ws.cell(row=8, column=3, value=cfg["overall_score"]["dimensions"][2]["direction"])
        ws.cell(row=9, column=1, value="Security")
        ws.cell(row=9, column=2, value=cfg["overall_score"]["dimensions"][3]["weight"])
        ws.cell(row=9, column=3, value=cfg["overall_score"]["dimensions"][3]["direction"])
        ws.cell(row=10, column=1, value="Complexity")
        ws.cell(row=10, column=2, value=cfg["overall_score"]["dimensions"][4]["weight"])
        ws.cell(row=10, column=3, value=cfg["overall_score"]["dimensions"][4]["direction"])
        ws.cell(row=11, column=1, value="Code Quality")
        ws.cell(row=11, column=2, value=cfg["overall_score"]["dimensions"][5]["weight"])
        ws.cell(row=11, column=3, value=cfg["overall_score"]["dimensions"][5]["direction"])
        ws.cell(row=13, column=1, value="Maintainability Formula")
        ws.cell(row=13, column=2, value="0.30 × Cyclomatic Component + 0.20 × Function Length Component + 0.20 × Nesting Component + 0.30 × Coupling Component")
        ws.cell(row=15, column=1, value="Component")
        ws.cell(row=15, column=2, value="Weight")
        ws.cell(row=15, column=3, value="Min")
        ws.cell(row=15, column=4, value="Max")
        row = 16
        for key, ref in cfg["maintainability"]["reference"].items():
            ws.cell(row=row, column=1, value=key)
            ws.cell(row=row, column=2, value=cfg["maintainability"]["weights"][key])
            ws.cell(row=row, column=3, value=ref["min"])
            ws.cell(row=row, column=4, value=ref["max"])
            row += 1
        ws.cell(row=row + 1, column=1, value="Normalization Higher-is-Better")
        ws.cell(row=row + 1, column=2, value="(x - min) / (max - min) × 100")
        ws.cell(row=row + 2, column=1, value="Normalization Lower-is-Better")
        ws.cell(row=row + 2, column=2, value="(max - x) / (max - min) × 100")
        ws.cell(row=row + 3, column=1, value="Neutral Value")
        ws.cell(row=row + 3, column=2, value=cfg["normalization"]["neutral_value"])
        ws.cell(row=row + 4, column=1, value="Statistics Test")
        ws.cell(row=row + 4, column=2, value="Wilcoxon Signed-Rank")
        ws.cell(row=row + 5, column=1, value="Alpha")
        ws.cell(row=row + 5, column=2, value=cfg["statistics"]["alpha"])
        _autosize(ws)

        # ── RESEARCH SCORECARD ──────────────────────────────────────────────
        # One row per comparison: AI score, Human score, winner, per-dimension
        scorecard_rows = []
        for c in comparisons:
            cid = c.comparison_id
            problem = session.get(models.Problem, c.problem_id)
            comp_dim = comp_map.get(cid, {})

            def _winner(metric_name):
                r = comp_dim.get(metric_name)
                return r.direction if r else "N/A"

            def _ai_val(metric_name):
                r = comp_dim.get(metric_name)
                return r.ai_value if r else None

            def _hu_val(metric_name):
                r = comp_dim.get(metric_name)
                return r.human_value if r else None

            overall_r = comp_dim.get("overall")
            scorecard_rows.append({
                "comparison_id": cid,
                "problem_id": c.problem_id,
                "problem_title": problem.title if problem else c.problem_id,
                "category": problem.category if problem else "N/A",
                "language": c.language,
                "experiment_type": c.experiment_type,
                "is_pilot": bool(c.is_pilot),
                "ai_system": c.ai_name,
                "ai_overall": overall_r.ai_value if overall_r else None,
                "human_overall": overall_r.human_value if overall_r else None,
                "overall_difference": overall_r.difference if overall_r else None,
                "overall_winner": overall_r.direction if overall_r else "N/A",
                "reliability_ai": _ai_val("reliability"),
                "reliability_human": _hu_val("reliability"),
                "reliability_winner": _winner("reliability"),
                "performance_ai": _ai_val("performance"),
                "performance_human": _hu_val("performance"),
                "performance_winner": _winner("performance"),
                "maintainability_ai": _ai_val("maintainability"),
                "maintainability_human": _hu_val("maintainability"),
                "maintainability_winner": _winner("maintainability"),
                "security_ai": _ai_val("security"),
                "security_human": _hu_val("security"),
                "security_winner": _winner("security"),
                "complexity_ai": _ai_val("complexity"),
                "complexity_human": _hu_val("complexity"),
                "complexity_winner": _winner("complexity"),
                "code_quality_ai": _ai_val("code_quality"),
                "code_quality_human": _hu_val("code_quality"),
                "code_quality_winner": _winner("code_quality"),
            })

        ws = wb.create_sheet("Research Scorecard")
        scorecard_headers = [
            "comparison_id", "problem_id", "problem_title", "category",
            "language", "experiment_type", "is_pilot", "ai_system",
            "ai_overall", "human_overall", "overall_difference", "overall_winner",
            "reliability_ai", "reliability_human", "reliability_winner",
            "performance_ai", "performance_human", "performance_winner",
            "maintainability_ai", "maintainability_human", "maintainability_winner",
            "security_ai", "security_human", "security_winner",
            "complexity_ai", "complexity_human", "complexity_winner",
            "code_quality_ai", "code_quality_human", "code_quality_winner",
        ]
        _write_sheet(ws, scorecard_headers, scorecard_rows)
        ws.freeze_panes = "A2"
        # Colour-code winner cells: AI=blue, HUMAN=teal, COMPARABLE=grey
        winner_cols = {
            "overall_winner": 12,
            "reliability_winner": 15,
            "performance_winner": 18,
            "maintainability_winner": 21,
            "security_winner": 24,
            "complexity_winner": 27,
            "code_quality_winner": 30,
        }
        from openpyxl.styles import PatternFill as PF
        ai_fill = PF(start_color="dbeafe", end_color="dbeafe", fill_type="solid")
        hu_fill = PF(start_color="ccfbf1", end_color="ccfbf1", fill_type="solid")
        cmp_fill = PF(start_color="f1f5f9", end_color="f1f5f9", fill_type="solid")
        for row_idx, row_data in enumerate(scorecard_rows, 2):
            for field, col_idx in winner_cols.items():
                val = row_data.get(field, "")
                cell = ws.cell(row=row_idx, column=col_idx)
                if val == "AI":
                    cell.fill = ai_fill
                elif val == "HUMAN":
                    cell.fill = hu_fill
                elif val in ("COMPARABLE", "N/A"):
                    cell.fill = cmp_fill

        # ── RESEARCH OVERVIEW (summary across research comparisons) ─────────
        research_comps = [
            c for c in comparisons
            if not c.is_pilot
            and c.status == "completed"
            and comp_map.get(c.comparison_id, {}).get("overall") is not None
            and comp_map[c.comparison_id]["overall"].ai_value is not None
            and comp_map[c.comparison_id]["overall"].human_value is not None
        ]
        raw_execution_count = sum(1 for c in comparisons if not c.is_pilot and c.status == "execution_only")
        incomplete_research_count = sum(1 for c in comparisons if not c.is_pilot) - len(research_comps) - raw_execution_count
        ws_ov = wb.create_sheet("Research Overview")
        ws_ov.cell(row=1, column=1, value="Research Code Evaluator — Dataset Overview")
        ws_ov.cell(row=1, column=1).font = Font(bold=True, size=14, color="1e3a8a")
        ws_ov.cell(row=3, column=1, value="Total Comparisons (all)")
        ws_ov.cell(row=3, column=2, value=len(comparisons))
        ws_ov.cell(row=4, column=1, value="Research Comparisons")
        ws_ov.cell(row=4, column=2, value=len(research_comps))
        ws_ov.cell(row=5, column=1, value="Pilot Comparisons")
        ws_ov.cell(row=5, column=2, value=sum(1 for c in comparisons if c.is_pilot))
        ws_ov.cell(row=6, column=1, value="Incomplete Research Records (excluded from scores)")
        ws_ov.cell(row=6, column=2, value=incomplete_research_count)
        problems_set = {c.problem_id for c in research_comps}
        ws_ov.cell(row=7, column=1, value="Problems Evaluated (valid research pairs)")
        ws_ov.cell(row=7, column=2, value=len(problems_set))
        langs = {c.language for c in research_comps}
        ws_ov.cell(row=8, column=1, value="Languages Used (valid research pairs)")
        ws_ov.cell(row=8, column=2, value=", ".join(sorted(langs)))
        ai_systems = {c.ai_name for c in research_comps}
        ws_ov.cell(row=9, column=1, value="AI Systems (valid research pairs)")
        ws_ov.cell(row=9, column=2, value=", ".join(sorted(ai_systems)))
        ws_ov.cell(row=10, column=1, value="Raw Execution Datasets (scores/winners not calculated)")
        ws_ov.cell(row=10, column=2, value=raw_execution_count)

        # Average AI vs Human overall scores (research only)
        res_overall = [comp_map.get(c.comparison_id, {}).get("overall") for c in research_comps]
        ai_ovals = [r.ai_value for r in res_overall if r and r.ai_value is not None]
        hu_ovals = [r.human_value for r in res_overall if r and r.human_value is not None]
        avg_ai = round(sum(ai_ovals) / len(ai_ovals), 3) if ai_ovals else None
        avg_hu = round(sum(hu_ovals) / len(hu_ovals), 3) if hu_ovals else None
        diff = round(avg_ai - avg_hu, 3) if avg_ai is not None and avg_hu is not None else None
        ws_ov.cell(row=11, column=1, value="Average AI Overall Score")
        ws_ov.cell(row=11, column=2, value=avg_ai)
        ws_ov.cell(row=12, column=1, value="Average Human Overall Score")
        ws_ov.cell(row=12, column=2, value=avg_hu)
        ws_ov.cell(row=13, column=1, value="Average Difference (AI - Human)")
        ws_ov.cell(row=13, column=2, value=diff)

        ai_wins = sum(1 for r in res_overall if r and r.direction == "AI")
        hu_wins = sum(1 for r in res_overall if r and r.direction == "HUMAN")
        comp_count = sum(1 for r in res_overall if r and r.direction == "COMPARABLE")
        ws_ov.cell(row=15, column=1, value="Overall AI Wins")
        ws_ov.cell(row=15, column=2, value=ai_wins)
        ws_ov.cell(row=16, column=1, value="Overall Human Wins")
        ws_ov.cell(row=16, column=2, value=hu_wins)
        ws_ov.cell(row=17, column=1, value="Comparable")
        ws_ov.cell(row=17, column=2, value=comp_count)
        ws_ov.cell(row=19, column=1, value="Note")
        ws_ov.cell(row=19, column=2, value=(
            "Single-comparison results do not establish universal superiority. "
            "Statistical conclusions require sufficient paired observations."
        ))
        _autosize(ws_ov)

        # ── DIMENSION DETAIL SHEET ───────────────────────────────────────────
        # One row per comparison × dimension (like the PDF score table).
        # Shows: problem, language, AI system, dimension, direction, weight,
        #         AI raw → normalized → weighted, Human raw → normalized → weighted,
        #         difference, winner.
        # This mirrors the PDF score calculation section for every comparison.
        dim_detail_rows = []
        dim_meta = {d["name"]: d for d in cfg["overall_score"]["dimensions"]}

        for c in comparisons:
            cid = c.comparison_id
            problem = session.get(models.Problem, c.problem_id)
            comp_dim = comp_map.get(cid, {})
            # Maintainability components from complexity data
            ai_cx = {k: v.raw_value for (v2, k), v in complexity_map.get(cid, {}).items() if v2 == "AI"}
            hu_cx = {k: v.raw_value for (v2, k), v in complexity_map.get(cid, {}).items() if v2 == "HUMAN"}

            dims_order = ["reliability", "performance", "maintainability", "security", "complexity", "code_quality"]
            for dim_name in dims_order:
                ai_s = score_map.get(cid, {}).get(("AI", dim_name))
                hu_s = score_map.get(cid, {}).get(("HUMAN", dim_name))
                cr = comp_dim.get(dim_name)
                meta = dim_meta.get(dim_name, {})
                weight = meta.get("weight", 0)
                direction = meta.get("direction", "")

                # Maintainability components (extra detail)
                if dim_name == "maintainability":
                    maint_cfg = cfg["maintainability"]
                    mw = maint_cfg["weights"]
                    mr = maint_cfg["reference"]
                    mapping = {
                        "cyclomatic": "cyclomatic_avg",
                        "function_length": "function_length_avg",
                        "nesting": "nesting_depth_avg",
                        "coupling": "coupling",
                    }
                    def comp_score(raw_metrics, key):
                        x = float(raw_metrics.get(mapping[key], 0.0))
                        lo, hi = float(mr[key]["min"]), float(mr[key]["max"])
                        if hi == lo:
                            return round(100.0 if x <= lo else 0.0, 3)
                        return round(max(0.0, min(100.0, (hi - x) / (hi - lo) * 100.0)), 3)
                    required_raw = set(mapping.values())
                    ai_maint_detail = " | ".join(
                        f"{k}={comp_score(ai_cx, k):.1f}×{mw[k]}" for k in mw
                    ) if required_raw.issubset(ai_cx) else "N/A"
                    hu_maint_detail = " | ".join(
                        f"{k}={comp_score(hu_cx, k):.1f}×{mw[k]}" for k in mw
                    ) if required_raw.issubset(hu_cx) else "N/A"
                else:
                    ai_maint_detail = ""
                    hu_maint_detail = ""

                row = {
                    "comparison_id": cid,
                    "problem_id": c.problem_id,
                    "problem_title": problem.title if problem else c.problem_id,
                    "language": c.language,
                    "experiment_type": c.experiment_type,
                    "is_pilot": bool(c.is_pilot),
                    "ai_system": c.ai_name,
                    "dimension": dim_name,
                    "direction": direction,
                    "weight": weight,
                    # AI
                    "ai_raw_value": ai_s.raw_value if ai_s else None,
                    "ai_normalized": round(ai_s.normalized_value, 4) if ai_s and ai_s.normalized_value is not None else None,
                    "ai_weighted_contribution": round(ai_s.weighted_value, 4) if ai_s and ai_s.weighted_value is not None else None,
                    "ai_norm_pop_min": ai_s.normalization_population_min if ai_s else None,
                    "ai_norm_pop_max": ai_s.normalization_population_max if ai_s else None,
                    "ai_norm_pop_n": ai_s.normalization_population_n if ai_s else None,
                    "ai_maint_components": ai_maint_detail,
                    # Human
                    "human_raw_value": hu_s.raw_value if hu_s else None,
                    "human_normalized": round(hu_s.normalized_value, 4) if hu_s and hu_s.normalized_value is not None else None,
                    "human_weighted_contribution": round(hu_s.weighted_value, 4) if hu_s and hu_s.weighted_value is not None else None,
                    "human_norm_pop_min": hu_s.normalization_population_min if hu_s else None,
                    "human_norm_pop_max": hu_s.normalization_population_max if hu_s else None,
                    "human_norm_pop_n": hu_s.normalization_population_n if hu_s else None,
                    "human_maint_components": hu_maint_detail,
                    # Comparison
                    "difference": cr.difference if cr else None,
                    "percentage_difference": cr.percentage_difference if cr else None,
                    "winner": cr.direction if cr else "N/A",
                }
                dim_detail_rows.append(row)

            # Overall score row
            ai_ov = score_map.get(cid, {}).get(("AI", "reliability"))  # any score row has overall_score
            overall_r = comp_dim.get("overall")
            ai_overall_val = ai_ov.overall_score if ai_ov else None
            hu_ov = score_map.get(cid, {}).get(("HUMAN", "reliability"))
            hu_overall_val = hu_ov.overall_score if hu_ov else None
            dim_detail_rows.append({
                "comparison_id": cid,
                "problem_id": c.problem_id,
                "problem_title": problem.title if problem else c.problem_id,
                "language": c.language,
                "experiment_type": c.experiment_type,
                "is_pilot": bool(c.is_pilot),
                "ai_system": c.ai_name,
                "dimension": "OVERALL",
                "direction": "higher_is_better",
                "weight": 1.0,
                "ai_raw_value": ai_overall_val,
                "ai_normalized": ai_overall_val,
                "ai_weighted_contribution": ai_overall_val,
                "ai_norm_pop_min": None, "ai_norm_pop_max": None, "ai_norm_pop_n": None,
                "ai_maint_components": "",
                "human_raw_value": hu_overall_val,
                "human_normalized": hu_overall_val,
                "human_weighted_contribution": hu_overall_val,
                "human_norm_pop_min": None, "human_norm_pop_max": None, "human_norm_pop_n": None,
                "human_maint_components": "",
                "difference": overall_r.difference if overall_r else None,
                "percentage_difference": overall_r.percentage_difference if overall_r else None,
                "winner": overall_r.direction if overall_r else "N/A",
            })

        dim_detail_headers = [
            "comparison_id", "problem_id", "problem_title", "language",
            "experiment_type", "is_pilot", "ai_system",
            "dimension", "direction", "weight",
            "ai_raw_value", "ai_normalized", "ai_weighted_contribution",
            "ai_norm_pop_min", "ai_norm_pop_max", "ai_norm_pop_n", "ai_maint_components",
            "human_raw_value", "human_normalized", "human_weighted_contribution",
            "human_norm_pop_min", "human_norm_pop_max", "human_norm_pop_n", "human_maint_components",
            "difference", "percentage_difference", "winner",
        ]
        ws = wb.create_sheet("Dimension Detail")
        _write_sheet(ws, dim_detail_headers, dim_detail_rows)
        ws.freeze_panes = "A2"
        # Colour-code winner column (col 27)
        ai_fill2  = PatternFill(start_color="dbeafe", end_color="dbeafe", fill_type="solid")
        hu_fill2  = PatternFill(start_color="ccfbf1", end_color="ccfbf1", fill_type="solid")
        cmp_fill2 = PatternFill(start_color="f1f5f9", end_color="f1f5f9", fill_type="solid")
        overall_fill = PatternFill(start_color="fef9c3", end_color="fef9c3", fill_type="solid")
        winner_col_idx = len(dim_detail_headers)  # last column
        dim_col_idx = dim_detail_headers.index("dimension") + 1
        for row_idx, row_data in enumerate(dim_detail_rows, 2):
            winner = row_data.get("winner", "")
            dim    = row_data.get("dimension", "")
            w_cell = ws.cell(row=row_idx, column=winner_col_idx)
            if winner == "AI":
                w_cell.fill = ai_fill2
            elif winner == "HUMAN":
                w_cell.fill = hu_fill2
            elif winner in ("COMPARABLE", "N/A"):
                w_cell.fill = cmp_fill2
            if dim == "OVERALL":
                for col in range(1, len(dim_detail_headers) + 1):
                    ws.cell(row=row_idx, column=col).fill = overall_fill

    wb.save(buf)
    buf.seek(0)
    return buf
