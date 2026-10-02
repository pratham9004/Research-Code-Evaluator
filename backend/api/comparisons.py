"""Comparison orchestration API.

POST /api/comparisons runs the full research workflow:
validate -> execute both -> same test cases -> static analysis -> metrics ->
compare -> persist -> return report.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from backend.db import models
from backend.db.session import SessionLocal
from backend.engine.executor import execute, VARIANT_AI, VARIANT_HUMAN
from backend.analysis.analyzer import analyze
from backend.scoring.scoring import load_config, maintainability_index, compute_scores
from backend.scoring.comparison import compute_comparison_results
from backend.statistics import statistics as stats_module
from backend.schemas import CompareRequest

router = APIRouter(prefix="/api/comparisons", tags=["comparisons"])


def _utcnow():
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# TYPED-PROBLEM preflight signatures
# Maps problem_id -> {language: required_function_name}
# ---------------------------------------------------------------------------
_TYPED_SIGNATURES = {
    "P001": {"python": "two_sum",            "java": "twoSum",            "cpp": "twoSum",            "javascript": "twoSum"},
    "P002": {"python": "max_subarray",        "java": "maxSubarray",       "cpp": "maxSubarray",       "javascript": "maxSubarray"},
    "P003": {"python": "binary_search",       "java": "binarySearch",      "cpp": "binarySearch",      "javascript": "binarySearch"},
    "P004": {"python": "merge_sorted_arrays", "java": "mergeSortedArrays", "cpp": "mergeSortedArrays", "javascript": "mergeSortedArrays"},
    "P005": {"python": "is_balanced",         "java": "isBalanced",        "cpp": "isBalanced",        "javascript": "isBalanced"},
    "P006": {"python": "csv_field_count",     "java": "csvFieldCount",     "cpp": "csvFieldCount",     "javascript": "csvFieldCount"},
    "P007": {"python": "count_log_levels",    "java": "countLogLevels",    "cpp": "countLogLevels",    "javascript": "countLogLevels"},
    "P008": {"python": "parse_key_value",     "java": "parseKeyValue",     "cpp": "parseKeyValue",     "javascript": "parseKeyValue"},
    "P009": {"python": "normalize_date",      "java": "normalizeDate",     "cpp": "normalizeDate",     "javascript": "normalizeDate"},
    "P010": {"python": "word_frequency",      "java": "wordFrequency",     "cpp": "wordFrequency",     "javascript": "wordFrequency"},
    "P011": {"python": "is_valid_email",      "java": "isValidEmail",      "cpp": "isValidEmail",      "javascript": "isValidEmail"},
    "P012": {"python": "is_valid_password",   "java": "isValidPassword",   "cpp": "isValidPassword",   "javascript": "isValidPassword"},
    "P013": {"python": "is_valid_range",      "java": "isValidRange",      "cpp": "isValidRange",      "javascript": "isValidRange"},
    "P014": {"python": "is_valid_ipv4",       "java": "isValidIPv4",       "cpp": "isValidIPv4",       "javascript": "isValidIPv4"},
    "P015": {"python": "is_valid_username",   "java": "isValidUsername",   "cpp": "isValidUsername",   "javascript": "isValidUsername"},
    "P016": {"python": "escape_html",         "java": "escapeHtml",        "cpp": "escapeHtml",        "javascript": "escapeHtml"},
    "P017": {"python": "escape_csv_cell",     "java": "escapeCsvCell",     "cpp": "escapeCsvCell",     "javascript": "escapeCsvCell"},
    "P018": {"python": "escape_json_string",  "java": "escapeJsonString",  "cpp": "escapeJsonString",  "javascript": "escapeJsonString"},
    "P019": {"python": "encode_url_component","java": "encodeUrlComponent","cpp": "encodeUrlComponent","javascript": "encodeUrlComponent"},
    "P020": {"python": "sanitize_template",   "java": "sanitizeTemplate",  "cpp": "sanitizeTemplate",  "javascript": "sanitizeTemplate"},
    "P021": {"python": "safe_path_normalize",  "java": "safePathNormalize", "cpp": "safePathNormalize", "javascript": "safePathNormalize"},
    "P022": {"python": "is_allowed_extension", "java": "isAllowedExtension","cpp": "isAllowedExtension","javascript": "isAllowedExtension"},
    "P023": {"python": "sanitize_filename",    "java": "sanitizeFilename",  "cpp": "sanitizeFilename",  "javascript": "sanitizeFilename"},
    "P024": {"python": "check_archive_entry",  "java": "checkArchiveEntry", "cpp": "checkArchiveEntry", "javascript": "checkArchiveEntry"},
    "P025": {"python": "is_allowed_filetype",  "java": "isAllowedFiletype", "cpp": "isAllowedFiletype", "javascript": "isAllowedFiletype"},
    "P026": {"python": "is_valid_sql_identifier","java":"isValidSqlIdentifier","cpp":"isValidSqlIdentifier","javascript":"isValidSqlIdentifier"},
    "P027": {"python": "escape_sql_string",    "java": "escapeSqlString",   "cpp": "escapeSqlString",   "javascript": "escapeSqlString"},
    "P028": {"python": "build_param_query",    "java": "buildParamQuery",   "cpp": "buildParamQuery",   "javascript": "buildParamQuery"},
    "P029": {"python": "validate_sort_direction","java":"validateSortDirection","cpp":"validateSortDirection","javascript":"validateSortDirection"},
    "P030": {"python": "is_allowed_column",    "java": "isAllowedColumn",   "cpp": "isAllowedColumn",   "javascript": "isAllowedColumn"},
    "P031": {"python": "quote_shell_arg",       "java": "quoteShellArg",     "cpp": "quoteShellArg",     "javascript": "quoteShellArg"},
    "P032": {"python": "is_allowed_command",    "java": "isAllowedCommand",  "cpp": "isAllowedCommand",  "javascript": "isAllowedCommand"},
    "P033": {"python": "detect_shell_meta",     "java": "detectShellMeta",   "cpp": "detectShellMeta",   "javascript": "detectShellMeta"},
    "P034": {"python": "is_valid_env_var",      "java": "isValidEnvVar",     "cpp": "isValidEnvVar",     "javascript": "isValidEnvVar"},
    "P035": {"python": "split_args",            "java": "splitArgs",         "cpp": "splitArgs",         "javascript": "splitArgs"},
    "P036": {"python": "parse_safe_literal",    "java": "parseSafeLiteral",  "cpp": "parseSafeLiteral",  "javascript": "parseSafeLiteral"},
    "P037": {"python": "parse_config_bool",     "java": "parseConfigBool",   "cpp": "parseConfigBool",   "javascript": "parseConfigBool"},
    "P038": {"python": "is_allowed_config_key", "java": "isAllowedConfigKey","cpp": "isAllowedConfigKey","javascript": "isAllowedConfigKey"},
    "P039": {"python": "validate_token",        "java": "validateToken",     "cpp": "validateToken",     "javascript": "validateToken"},
    "P040": {"python": "validate_numeric_expr", "java": "validateNumericExpr","cpp":"validateNumericExpr","javascript":"validateNumericExpr"},
    "P041": {"python": "frequency_counter",    "java": "frequencyCounter",   "cpp": "frequencyCounter",   "javascript": "frequencyCounter"},
    "P042": {"python": "has_duplicate",        "java": "hasDuplicate",       "cpp": "hasDuplicate",       "javascript": "hasDuplicate"},
    "P043": {"python": "streaming_sum",        "java": "streamingSum",       "cpp": "streamingSum",       "javascript": "streamingSum"},
    "P044": {"python": "bounded_log_processor","java": "boundedLogProcessor","cpp": "boundedLogProcessor","javascript": "boundedLogProcessor"},
    "P045": {"python": "top_k_frequent",       "java": "topKFrequent",       "cpp": "topKFrequent",       "javascript": "topKFrequent"},
    "P046": {"python": "validate_token_format","java": "validateTokenFormat","cpp": "validateTokenFormat","javascript": "validateTokenFormat"},
    "P047": {"python": "evaluate_permission",  "java": "evaluatePermission", "cpp": "evaluatePermission", "javascript": "evaluatePermission"},
    "P048": {"python": "role_has_permission",  "java": "roleHasPermission",  "cpp": "roleHasPermission",  "javascript": "roleHasPermission"},
    "P049": {"python": "check_session",        "java": "checkSession",       "cpp": "checkSession",       "javascript": "checkSession"},
    "P050": {"python": "validate_scope",       "java": "validateScope",      "cpp": "validateScope",      "javascript": "validateScope"},
}


def _preflight_typed(language: str, ai_code: str, human_code: str, problem) -> str | None:
    """Lightweight preflight for typed (LeetCode-style) problems.
    Checks only that the required function/method name is present.
    Does NOT enforce exact parameter counts — that's the harness's job.
    """
    pid = problem.problem_id
    sig_map = _TYPED_SIGNATURES.get(pid, {})
    fn_name = sig_map.get(language)
    if not fn_name:
        return None  # no check defined for this combo

    for label, code in [("AI", ai_code), ("Human", human_code)]:
        if language == "python":
            try:
                import ast as _ast
                _ast.parse(code)
            except SyntaxError as e:
                return f"{label} code has a Python syntax error: {e.msg} (line {e.lineno})"
            if "input(" in code:
                return f"{label} code must not use input(). The harness supplies inputs directly."
            # Check function defined
            try:
                import ast as _ast
                tree = _ast.parse(code)
                names = [n.name for n in _ast.walk(tree)
                         if isinstance(n, (_ast.FunctionDef, _ast.AsyncFunctionDef))]
                if fn_name not in names:
                    return (f"{label} code must define the function '{fn_name}'. "
                            f"See the starter template for the required signature.")
            except Exception:
                pass

        elif language == "java":
            if "public class " in code:
                m = re.search(r"public\s+class\s+(\w+)", code)
                if m and m.group(1) != "Solution":
                    return (f"{label} Java code must use 'public class Solution'. "
                            f"Found 'public class {m.group(1)}'.")
            if fn_name not in code:
                return (f"{label} Java code must define the method '{fn_name}'. "
                        f"See the starter template.")

        elif language == "cpp":
            if fn_name not in code:
                return (f"{label} C++ code must define the function '{fn_name}'. "
                        f"See the starter template.")

        elif language == "javascript":
            has_func = bool(
                re.search(r"\bfunction\s+" + re.escape(fn_name) + r"\s*\(", code)
                or re.search(r"\b" + re.escape(fn_name) + r"\s*=\s*(?:async\s*)?\(", code)
                or re.search(r"\b" + re.escape(fn_name) + r"\s*=\s*(?:async\s*)?function", code)
            )
            has_export = bool(
                re.search(r"module\.exports\s*=\s*\{[^}]*" + re.escape(fn_name), code)
                or re.search(r"module\.exports\." + re.escape(fn_name) + r"\s*=", code)
                or re.search(r"module\.exports\s*=\s*" + re.escape(fn_name), code)
            )
            if not has_func:
                return f"{label} JavaScript code must define 'function {fn_name}(...)'."
            if not has_export:
                return (f"{label} JavaScript code must export '{fn_name}' via "
                        f"module.exports = {{ {fn_name} }} or module.exports.{fn_name} = ...")
    return None


def _preflight_validate(language: str, ai_code: str, human_code: str, problem) -> str | None:
    if not ai_code.strip() or not human_code.strip():
        return "Both AI and Human code are required."
    if language not in problem.supported_languages:
        return f"Language '{language}' is not supported for problem {problem.problem_id}."

    # Route to typed or legacy preflight
    harness_type = getattr(problem, "harness_type", "legacy") or "legacy"
    if harness_type == "typed":
        return _preflight_typed(language, ai_code, human_code, problem)

    # ── Legacy preflight (original string-in/string-out) ──────────────
    entry = (problem.entry_function or "solve").strip()
    if language == "python":
        if "input(" in ai_code or "input(" in human_code:
            return "Interactive input() is not supported. The entry function must accept a string parameter and return a string."
        try:
            import ast
            ast.parse(ai_code)
            ast.parse(human_code)
        except SyntaxError as e:
            return f"Python syntax error: {e.msg} (line {e.lineno})"
        for label, code in [("AI", ai_code), ("Human", human_code)]:
            try:
                import ast
                tree = ast.parse(code)
                func_names = [n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                if entry not in func_names:
                    return f"{label} code does not define the required function '{entry}(data: str) -> str'."
                fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == entry)
                if len(fn.args.args) != 1:
                    return f"{label} code must define '{entry}' with exactly one parameter (data: str)."
            except Exception:
                pass
    elif language == "java":
        for label, code in [("AI", ai_code), ("Human", human_code)]:
            if "public class " in code:
                match = re.search(r"public\s+class\s+(\w+)", code)
                if match:
                    class_name = match.group(1)
                    if class_name != "Solution":
                        return f"{label} code declares 'public class {class_name}'. The harness expects 'public class Solution' in a file named Solution.java."
            if not re.search(r"public\s+static\s+String\s+" + re.escape(entry) + r"\s*\(\s*String\s+\w+\s*\)", code):
                return f"{label} code must define 'public static String {entry}(String data)'."
    elif language == "cpp":
        for label, code in [("AI", ai_code), ("Human", human_code)]:
            if not re.search(
                r"(?:std::)?string\s+" + re.escape(entry) + r"\s*\(\s*const\s+(?:std::)?string\s*&",
                code,
            ):
                return (
                    f"{label} C++ code must define "
                    f"'string {entry}(const string& data)' (or std::string / const std::string&)."
                )
    elif language == "javascript":
        for label, code in [("AI", ai_code), ("Human", human_code)]:
            has_func = bool(
                re.search(r"\bfunction\s+" + re.escape(entry) + r"\s*\(", code)
                or re.search(r"\b" + re.escape(entry) + r"\s*=\s*(?:async\s*)?\(", code)
                or re.search(r"\b" + re.escape(entry) + r"\s*=\s*(?:async\s*)?function", code)
            )
            has_export = bool(
                re.search(r"module\.exports\s*=\s*\{[^}]*" + re.escape(entry), code)
                or re.search(r"module\.exports\." + re.escape(entry) + r"\s*=", code)
                or re.search(r"module\.exports\s*=\s*" + re.escape(entry), code)
            )
            if not has_func:
                return f"{label} JavaScript code must define a function named '{entry}'."
            if not has_export:
                return (
                    f"{label} JavaScript code must export '{entry}' via "
                    f"module.exports = {{ {entry} }} or module.exports.{entry} = ..."
                )
    return None


def _mark_existing_as_pilot():
    with SessionLocal() as session:
        session.query(models.Comparison).filter(models.Comparison.is_pilot == 0).update({"is_pilot": 1}, synchronize_session=False)
        session.query(models.Comparison).filter(models.Comparison.is_pilot.is_(None)).update({"is_pilot": 1}, synchronize_session=False)
        session.commit()


def _summarize_exec(exec_result):
    cases = exec_result.get("cases", [])
    total = len(cases)
    passed = sum(1 for c in cases if c["status"] == "PASS")
    failed = sum(1 for c in cases if c["status"] == "FAIL")
    errored = sum(1 for c in cases if c["status"] == "ERROR")
    timeout = sum(1 for c in cases if c["status"] == "TIMEOUT")
    pass_rate = round(passed / total * 100, 2) if total else 0.0
    return {
        "status": exec_result.get("status"),
        "execution_time_ms": exec_result.get("execution_time_ms", 0.0),
        "pass_rate": pass_rate,
        "total": total,
        "passed": passed,
        "failed": failed,
        "error": errored,
        "timeout": timeout,
        "cases": cases,
        "error_message": exec_result.get("error"),
    }


def _run_variant(language, code, test_cases, entry_function,
                 harness_type="legacy", problem_id=""):
    exec_result = execute(language, code, test_cases, entry_function,
                          harness_type=harness_type, problem_id=problem_id)
    analysis = analyze(language, code)
    return exec_result, analysis


def _persist(session, comparison, problem, test_cases, ai_exec, ai_analysis,
             human_exec, human_analysis, ai_dims, human_dims, ai_scores,
             human_scores, ai_overall, human_overall, comparison_rows, cfg,
             ai_preflight="PASS", human_preflight="PASS"):
    cid = comparison.comparison_id

    session.add(models.PreflightResult(
        comparison_id=cid, code_variant=VARIANT_AI,
        status=ai_preflight, message="Contract validation passed."))
    session.add(models.PreflightResult(
        comparison_id=cid, code_variant=VARIANT_HUMAN,
        status=human_preflight, message="Contract validation passed."))

    for variant, exec_r, analysis in (
        (VARIANT_AI, ai_exec, ai_analysis),
        (VARIANT_HUMAN, human_exec, human_analysis),
    ):
        summary = _summarize_exec(exec_r)
        session.add(models.ExecutionResult(
            comparison_id=cid, code_variant=variant,
            total_test_cases=summary["total"], passed_count=summary["passed"],
            failed_count=summary["failed"], error_count=summary["error"],
            timeout_count=summary["timeout"], pass_rate=summary["pass_rate"],
            execution_time_ms=summary["execution_time_ms"],
            execution_status=summary["status"],
        ))
        for c in summary["cases"]:
            tc = test_cases[c["index"]]
            session.add(models.TestCaseResult(
                comparison_id=cid, code_variant=variant,
                test_case_id=tc.test_case_id, status=c["status"],
                actual_output=c.get("actual"), expected_output=c.get("expected"),
                error=c.get("error"), execution_time_ms=c.get("execution_time_ms"),
                exit_code=c.get("exit_code"), stdout=c.get("stdout"), stderr=c.get("stderr"),
            ))

        rm = analysis["raw_metrics"]
        for metric_name, value in (
            ("cyclomatic_avg", rm.get("cyclomatic_avg")),
            ("function_length_avg", rm.get("function_length_avg")),
            ("nesting_depth_avg", rm.get("nesting_depth_avg")),
            ("coupling", rm.get("coupling")),
        ):
            session.add(models.ComplexityData(
                comparison_id=cid, code_variant=variant,
                metric_name=metric_name, raw_value=float(value or 0.0),
            ))

        for f in analysis["quality_findings"] + analysis["security_findings"]:
            session.add(models.StaticAnalysisResult(
                comparison_id=cid, code_variant=variant,
                tool_name=f.get("tool_name"), tool_version=f.get("tool_version"),
                rule=f.get("rule"), category=f.get("category"),
                severity=f.get("severity"), message=f.get("message"),
                source_location=f.get("source_location"), raw_result=f.get("raw_result"),
            ))
        for f in analysis["security_findings"]:
            session.add(models.SecurityFinding(
                comparison_id=cid, code_variant=variant,
                tool=f.get("tool_name"), tool_version=f.get("tool_version"),
                severity=f.get("severity"), rule=f.get("rule"),
                category=f.get("category"), message=f.get("message"),
                location=f.get("source_location"),
            ))
        for note in analysis["tool_notes"]:
            session.add(models.StaticAnalysisResult(
                comparison_id=cid, code_variant=variant, tool_name="engine",
                tool_version="", rule="TOOL_UNAVAILABLE", category="tool_status",
                severity="info", message=note, source_location="", raw_result="",
            ))

    for variant, scores in ((VARIANT_AI, ai_scores), (VARIANT_HUMAN, human_scores)):
        for s in scores:
            session.add(models.Score(
                comparison_id=cid, code_variant=variant, dimension=s["dimension"],
                raw_value=s["raw_value"], normalized_value=s["normalized_value"],
                weighted_value=s["weighted_value"], dimension_score=s["dimension_score"],
                overall_score=ai_overall if variant == VARIANT_AI else human_overall,
                scoring_config_version=1,
                normalization_population_min=s.get("normalization_population_min"),
                normalization_population_max=s.get("normalization_population_max"),
                normalization_population_n=s.get("normalization_population_n"),
            ))

    for r in comparison_rows:
        session.add(models.ComparisonResult(
            comparison_id=cid, metric=r["metric"], ai_value=r["ai_value"],
            human_value=r["human_value"], difference=r["difference"],
            direction=r["direction"], percentage_difference=r["percentage_difference"],
            statistical_status=r["statistical_status"],
        ))

    # Persist statistical results for this comparison
    try:
        stats = stats_module.compute_statistics(session, cfg)
        for metric, data in stats.get("per_metric", {}).items():
            session.add(models.StatisticalResult(
                comparison_id=cid, metric=metric,
                test=cfg.get("statistics", {}).get("test", "wilcoxon_signed_rank"),
                n_paired=data.get("n_paired"),
                statistic=data.get("statistic"),
                p_value=data.get("p_value"),
                significant=1 if data.get("significant") else 0,
                effect_size=data.get("effect_size"),
                status=data.get("status", "insufficient_data"),
                alpha=cfg.get("statistics", {}).get("alpha"),
                dataset_used="research_dataset",
            ))
    except Exception:
        pass


def build_report(session, comparison_id: int) -> dict:
    comparison = session.get(models.Comparison, comparison_id)
    problem = session.get(models.Problem, comparison.problem_id)

    def variant_exec(variant):
        er = session.query(models.ExecutionResult).filter_by(
            comparison_id=comparison_id, code_variant=variant).first()
        cases = session.query(models.TestCaseResult).filter_by(
            comparison_id=comparison_id, code_variant=variant).all()
        return er, cases

    def variant_scores(variant):
        return session.query(models.Score).filter_by(
            comparison_id=comparison_id, code_variant=variant).all()

    ai_er, ai_cases = variant_exec(VARIANT_AI)
    hu_er, hu_cases = variant_exec(VARIANT_HUMAN)
    comp_rows = session.query(models.ComparisonResult).filter_by(
        comparison_id=comparison_id).all()

    def exec_block(er, cases):
        return {
            "status": er.execution_status,
            "execution_time_ms": er.execution_time_ms,
            "pass_rate": er.pass_rate,
            "total": er.total_test_cases,
            "passed": er.passed_count,
            "failed": er.failed_count,
            "error": er.error_count,
            "timeout": er.timeout_count,
        "cases": [
            {"index": c.test_case_id, "status": c.status,
             "actual": c.actual_output, "expected": c.expected_output,
             "error": c.error, "execution_time_ms": c.execution_time_ms,
             "exit_code": c.exit_code, "stdout": c.stdout, "stderr": c.stderr} for c in cases
        ],
        }

    def score_block(scores):
        return [{"dimension": s.dimension, "raw_value": s.raw_value,
                 "normalized_value": s.normalized_value,
                 "weighted_value": s.weighted_value,
                 "dimension_score": s.dimension_score,
                 "normalization_population_min": s.normalization_population_min,
                 "normalization_population_max": s.normalization_population_max,
                 "normalization_population_n": s.normalization_population_n} for s in scores]

    ai_overall = (session.query(models.Score.overall_score)
                 .filter_by(comparison_id=comparison_id, code_variant=VARIANT_AI).first())
    hu_overall = (session.query(models.Score.overall_score)
                 .filter_by(comparison_id=comparison_id, code_variant=VARIANT_HUMAN).first())

    preflight = session.query(models.PreflightResult).filter_by(
        comparison_id=comparison_id).all()

    return {
        "comparison_id": comparison_id,
        "problem_id": comparison.problem_id,
        "problem_title": problem.title if problem else comparison.problem_id,
        "language": comparison.language,
        "ai_name": comparison.ai_name,
        "status": comparison.status,
        "experiment_type": comparison.experiment_type,
        "is_pilot": bool(comparison.is_pilot),
        "problem_version": comparison.problem_version,
        "test_case_version": comparison.test_case_version,
        "created_at": comparison.created_at.isoformat() if comparison.created_at else None,
        "completed_at": comparison.completed_at.isoformat() if comparison.completed_at else None,
        "data_classification": "PILOT / TEST DATA" if comparison.is_pilot else "RESEARCH DATA",
        "execution": {"ai": exec_block(ai_er, ai_cases), "human": exec_block(hu_er, hu_cases)},
        "preflight": {
            "ai": [{"status": p.status, "message": p.message} for p in preflight if p.code_variant == VARIANT_AI],
            "human": [{"status": p.status, "message": p.message} for p in preflight if p.code_variant == VARIANT_HUMAN],
        },
        "scores": {
            "ai": score_block(variant_scores(VARIANT_AI)),
            "human": score_block(variant_scores(VARIANT_HUMAN)),
            "ai_overall": ai_overall[0] if ai_overall else None,
            "human_overall": hu_overall[0] if hu_overall else None,
        },
        "comparison": [
            {"metric": r.metric, "ai_value": r.ai_value, "human_value": r.human_value,
             "difference": r.difference, "direction": r.direction,
             "percentage_difference": r.percentage_difference,
             "statistical_status": r.statistical_status}
            for r in comp_rows
        ],
    }


def _get_complexity_map(session, comparison_id: int, variant: str) -> dict:
    rows = session.query(models.ComplexityData).filter_by(
        comparison_id=comparison_id, code_variant=variant).all()
    return {r.metric_name: r.raw_value for r in rows}


def _maintainability_components(raw_metrics: dict, cfg: dict) -> dict:
    mcfg = cfg["maintainability"]
    weights = mcfg["weights"]
    ref = mcfg["reference"]
    mapping = {
        "cyclomatic": "cyclomatic_avg",
        "function_length": "function_length_avg",
        "nesting": "nesting_depth_avg",
        "coupling": "coupling",
    }
    components = {}
    for key, field in mapping.items():
        x = float(raw_metrics.get(field, 0.0))
        r = ref[key]
        lo, hi = float(r["min"]), float(r["max"])
        if hi == lo:
            comp = 100.0 if x <= lo else 0.0
        else:
            comp = (hi - x) / (hi - lo) * 100.0
        components[key] = {
            "raw_value": x,
            "reference_min": lo,
            "reference_max": hi,
            "normalized_score": round(max(0.0, min(100.0, comp)), 3),
            "weight": weights[key],
            "weighted_contribution": round(max(0.0, min(100.0, comp)) * weights[key], 3),
        }
    return components


def build_detailed_report(session, comparison_id: int) -> dict:
    comparison = session.get(models.Comparison, comparison_id)
    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found.")
    problem = session.get(models.Problem, comparison.problem_id)
    cfg = load_config()

    ai_er = session.query(models.ExecutionResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_AI).first()
    hu_er = session.query(models.ExecutionResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_HUMAN).first()
    ai_cases = session.query(models.TestCaseResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_AI).all()
    hu_cases = session.query(models.TestCaseResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_HUMAN).all()
    preflight = session.query(models.PreflightResult).filter_by(
        comparison_id=comparison_id).all()
    comp_rows = session.query(models.ComparisonResult).filter_by(
        comparison_id=comparison_id).all()
    ai_scores = session.query(models.Score).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_AI).all()
    hu_scores = session.query(models.Score).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_HUMAN).all()
    ai_complexity = _get_complexity_map(session, comparison_id, VARIANT_AI)
    hu_complexity = _get_complexity_map(session, comparison_id, VARIANT_HUMAN)

    ai_sec = session.query(models.SecurityFinding).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_AI).all()
    hu_sec = session.query(models.SecurityFinding).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_HUMAN).all()
    ai_static = session.query(models.StaticAnalysisResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_AI).all()
    hu_static = session.query(models.StaticAnalysisResult).filter_by(
        comparison_id=comparison_id, code_variant=VARIANT_HUMAN).all()

    ai_quality = [f for f in ai_static if f.category == "code_quality"]
    hu_quality = [f for f in hu_static if f.category == "code_quality"]

    ai_mi_components = _maintainability_components(ai_complexity, cfg) if ai_complexity else {}
    hu_mi_components = _maintainability_components(hu_complexity, cfg) if hu_complexity else {}
    ai_mi = round(sum(v["weighted_contribution"] for v in ai_mi_components.values()), 3) if ai_mi_components else None
    hu_mi = round(sum(v["weighted_contribution"] for v in hu_mi_components.values()), 3) if hu_mi_components else None

    ai_overall = next((s.overall_score for s in ai_scores if s.overall_score is not None), None)
    hu_overall = next((s.overall_score for s in hu_scores if s.overall_score is not None), None)

    def score_dimension(scores, name):
        for s in scores:
            if s.dimension == name:
                return {
                    "raw_value": s.raw_value,
                    "normalized_value": s.normalized_value,
                    "weighted_value": s.weighted_value,
                    "dimension_score": s.dimension_score,
                    "normalization_population_min": s.normalization_population_min,
                    "normalization_population_max": s.normalization_population_max,
                    "normalization_population_n": s.normalization_population_n,
                }
        return None

    dims = ["reliability", "performance", "maintainability", "security", "complexity", "code_quality"]
    ai_dim_scores = {d: score_dimension(ai_scores, d) for d in dims}
    hu_dim_scores = {d: score_dimension(hu_scores, d) for d in dims}
    weights = {d["name"]: d["weight"] for d in cfg["overall_score"]["dimensions"]}

    def exec_summary(er):
        if not er:
            return None
        return {
            "execution_status": er.execution_status,
            "execution_time_ms": er.execution_time_ms,
            "pass_rate": er.pass_rate,
            "total_test_cases": er.total_test_cases,
            "passed_count": er.passed_count,
            "failed_count": er.failed_count,
            "error_count": er.error_count,
            "timeout_count": er.timeout_count,
        }

    def findings_to_list(findings):
        return [{
            "tool": f.tool,
            "tool_version": f.tool_version,
            "severity": f.severity,
            "rule": f.rule,
            "category": f.category,
            "message": f.message,
            "location": f.location,
        } for f in findings]

    def static_to_list(findings):
        return [{
            "tool_name": f.tool_name,
            "tool_version": f.tool_version,
            "rule": f.rule,
            "category": f.category,
            "severity": f.severity,
            "message": f.message,
            "source_location": f.source_location,
            "raw_result": f.raw_result,
        } for f in findings]

    def tc_to_list(cases):
        return [{
            "test_case_id": c.test_case_id,
            "input": (session.get(models.TestCase, c.test_case_id).input
                      if session.get(models.TestCase, c.test_case_id) else None),
            "status": c.status,
            "actual_output": c.actual_output,
            "expected_output": c.expected_output,
            "error": c.error,
            "execution_time_ms": c.execution_time_ms,
        } for c in cases]

    stats = stats_module.compute_statistics(session, cfg)

    return {
        "experiment": {
            "comparison_id": comparison_id,
            "problem_id": comparison.problem_id,
            "problem_title": problem.title if problem else None,
            "category": problem.category if problem else None,
            "difficulty": problem.difficulty if problem else None,
            "language": comparison.language,
            "ai_name": comparison.ai_name,
            "status": comparison.status,
            "created_at": comparison.created_at.isoformat() if comparison.created_at else None,
            "completed_at": comparison.completed_at.isoformat() if comparison.completed_at else None,
            "execution_timeout_seconds": cfg.get("execution", {}).get("timeout_seconds", 10),
            "test_case_count": len(ai_cases),
            "ai_code_available": bool(comparison.ai_source_code),
            "human_code_available": bool(comparison.human_source_code),
            "experiment_type": comparison.experiment_type,
            "is_pilot": bool(comparison.is_pilot),
            "problem_version": comparison.problem_version,
            "test_case_version": comparison.test_case_version,
            "data_classification": "PILOT / TEST DATA" if comparison.is_pilot else "RESEARCH DATA",
        },
        "executive_result": {
            "ai_overall": ai_overall,
            "human_overall": hu_overall,
            "difference": round(ai_overall - hu_overall, 3) if ai_overall is not None and hu_overall is not None else None,
            "percentage_difference": round((ai_overall - hu_overall) / abs(hu_overall) * 100, 3) if ai_overall is not None and hu_overall not in (None, 0) else None,
            "direction": next((r.direction for r in comp_rows if r.metric == "overall"), None),
            "neutral_statement": "This result applies only to this comparison and does not establish a universal superiority of AI-generated code.",
        },
        "six_dimensions": [
            {
                "dimension": r.metric,
                "ai_value": r.ai_value,
                "human_value": r.human_value,
                "difference": r.difference,
                "direction": r.direction,
                "percentage_difference": r.percentage_difference,
            }
            for r in comp_rows if r.metric != "overall"
        ] + [
            {
                "dimension": "overall",
                "ai_value": ai_overall,
                "human_value": hu_overall,
                "difference": round(ai_overall - hu_overall, 3) if ai_overall is not None and hu_overall is not None else None,
                "direction": next((r.direction for r in comp_rows if r.metric == "overall"), None),
                "percentage_difference": round((ai_overall - hu_overall) / abs(hu_overall) * 100, 3) if ai_overall is not None and hu_overall not in (None, 0) else None,
            }
        ],
        "preflight": {
            "ai": [{"status": p.status, "message": p.message} for p in preflight if p.code_variant == VARIANT_AI],
            "human": [{"status": p.status, "message": p.message} for p in preflight if p.code_variant == VARIANT_HUMAN],
        },
        "reliability": {
            "ai": {
                **(exec_summary(ai_er) or {}),
                "cases": tc_to_list(ai_cases),
            },
            "human": {
                **(exec_summary(hu_er) or {}),
                "cases": tc_to_list(hu_cases),
            },
            "formula": "Pass Rate = (Passed Test Cases / Total Test Cases) × 100",
        },
        "performance": {
            "ai": {
                "execution_time_ms": ai_er.execution_time_ms if ai_er else None,
                "execution_status": ai_er.execution_status if ai_er else None,
                "normalized_value": ai_dim_scores["performance"]["normalized_value"] if ai_dim_scores["performance"] else None,
            },
            "human": {
                "execution_time_ms": hu_er.execution_time_ms if hu_er else None,
                "execution_status": hu_er.execution_status if hu_er else None,
                "normalized_value": hu_dim_scores["performance"]["normalized_value"] if hu_dim_scores["performance"] else None,
            },
            "direction": "lower_is_better",
            "note": "Lower execution time represents better observed performance.",
        },
        "maintainability": {
            "ai": {
                "components": ai_mi_components,
                "final_score": ai_mi,
            },
            "human": {
                "components": hu_mi_components,
                "final_score": hu_mi,
            },
            "formula": "0.30 × Cyclomatic Component + 0.20 × Function Length Component + 0.20 × Nesting Component + 0.30 × Coupling Component",
            "reference_bounds": cfg["maintainability"]["reference"],
            "weights": cfg["maintainability"]["weights"],
        },
        "security": {
            "ai": {
                "findings": findings_to_list(ai_sec),
                "count": len(ai_sec),
                "tool_status": next((f.message for f in ai_static if f.rule == "TOOL_UNAVAILABLE"), None),
            },
            "human": {
                "findings": findings_to_list(hu_sec),
                "count": len(hu_sec),
                "tool_status": next((f.message for f in hu_static if f.rule == "TOOL_UNAVAILABLE"), None),
            },
            "direction": "lower_is_better",
            "note": "Fewer security findings represent better observed security posture.",
        },
        "complexity": {
            "ai": ai_complexity,
            "human": hu_complexity,
            "normalized_ai": ai_dim_scores["complexity"]["normalized_value"] if ai_dim_scores["complexity"] else None,
            "normalized_human": hu_dim_scores["complexity"]["normalized_value"] if hu_dim_scores["complexity"] else None,
            "direction": "lower_is_better",
            "note": "Lower complexity represents better observed maintainability.",
        },
        "code_quality": {
            "ai": {
                "findings": static_to_list(ai_quality),
                "count": len(ai_quality),
                "tool_status": next((f.message for f in ai_static if f.rule == "TOOL_UNAVAILABLE" and f.category == "tool_status"), None),
            },
            "human": {
                "findings": static_to_list(hu_quality),
                "count": len(hu_quality),
                "tool_status": next((f.message for f in hu_static if f.rule == "TOOL_UNAVAILABLE" and f.category == "tool_status"), None),
            },
            "normalized_ai": ai_dim_scores["code_quality"]["normalized_value"] if ai_dim_scores["code_quality"] else None,
            "normalized_human": hu_dim_scores["code_quality"]["normalized_value"] if hu_dim_scores["code_quality"] else None,
            "direction": "lower_is_better",
            "note": "Fewer code-quality findings represent better observed code quality.",
        },
        "scoring_calculation": {
            "weights": weights,
            "ai": {
                "dimensions": [
                    {
                        "dimension": d,
                        "raw_value": ai_dim_scores[d]["raw_value"] if ai_dim_scores[d] else None,
                        "normalized_value": ai_dim_scores[d]["normalized_value"] if ai_dim_scores[d] else None,
                        "normalization_population_min": ai_dim_scores[d].get("normalization_population_min") if ai_dim_scores[d] else None,
                        "normalization_population_max": ai_dim_scores[d].get("normalization_population_max") if ai_dim_scores[d] else None,
                        "normalization_population_n": ai_dim_scores[d].get("normalization_population_n") if ai_dim_scores[d] else None,
                        "weight": weights.get(d),
                        "weighted_contribution": round((ai_dim_scores[d]["normalized_value"] or 0) * weights.get(d, 0), 3) if ai_dim_scores[d] else None,
                    }
                    for d in dims
                ],
                "overall_score": ai_overall,
            },
            "human": {
                "dimensions": [
                    {
                        "dimension": d,
                        "raw_value": hu_dim_scores[d]["raw_value"] if hu_dim_scores[d] else None,
                        "normalized_value": hu_dim_scores[d]["normalized_value"] if hu_dim_scores[d] else None,
                        "normalization_population_min": hu_dim_scores[d].get("normalization_population_min") if hu_dim_scores[d] else None,
                        "normalization_population_max": hu_dim_scores[d].get("normalization_population_max") if hu_dim_scores[d] else None,
                        "normalization_population_n": hu_dim_scores[d].get("normalization_population_n") if hu_dim_scores[d] else None,
                        "weight": weights.get(d),
                        "weighted_contribution": round((hu_dim_scores[d]["normalized_value"] or 0) * weights.get(d, 0), 3) if hu_dim_scores[d] else None,
                    }
                    for d in dims
                ],
                "overall_score": hu_overall,
            },
            "formula": "Overall Score = Σ (Normalized Dimension Score × Dimension Weight)",
        },
        "normalization": {
            "methodology": "Dataset min/max normalization",
            "neutral_value": cfg["normalization"]["neutral_value"],
            "higher_is_better_formula": "(x - min) / (max - min) × 100",
            "lower_is_better_formula": "(max - x) / (max - min) × 100",
            "note": "Normalized scores are relative to the accumulated research dataset, not absolute quality percentages.",
        },
        "ai_vs_human": [
            {
                "metric": r.metric,
                "ai_value": r.ai_value,
                "human_value": r.human_value,
                "difference": r.difference,
                "percentage_difference": r.percentage_difference,
                "direction": r.direction,
                "statistical_status": r.statistical_status,
            }
            for r in comp_rows
        ],
        "statistical_analysis": {
            "alpha": stats.get("alpha"),
            "per_metric": stats.get("per_metric", {}),
            "has_sufficient_data": any(
                m.get("status") == "ok" for m in stats.get("per_metric", {}).values()
            ),
        },
        "test_cases": {
            "ai": tc_to_list(ai_cases),
            "human": tc_to_list(hu_cases),
        },
        "raw_analysis": {
            "ai_security_findings": findings_to_list(ai_sec),
            "human_security_findings": findings_to_list(hu_sec),
            "ai_static_analysis": static_to_list(ai_static),
            "human_static_analysis": static_to_list(hu_static),
            "ai_complexity": ai_complexity,
            "human_complexity": hu_complexity,
        },
        "interpretation": {
            "statement": (f"This comparison shows that {'AI' if ai_overall > hu_overall else 'Human' if hu_overall > ai_overall else 'both implementations'} achieved a higher overall composite score." if ai_overall is not None and hu_overall is not None else "An overall conclusion is unavailable because one or more required measurements are missing."),
            "disclaimer": "This result applies only to this comparison and does not imply a universal conclusion.",
        },
    }


@router.post("")
def submit_comparison(req: CompareRequest):
    cfg = load_config()
    with SessionLocal() as session:
        problem = session.get(models.Problem, req.problem_id)
        if not problem:
            raise HTTPException(status_code=404, detail="Problem not found.")
        if req.language not in problem.supported_languages:
            raise HTTPException(status_code=400, detail="Language not supported for this problem.")
        if not req.ai_name.strip():
            raise HTTPException(status_code=400, detail="AI name is required.")
        if not req.ai_code.strip() or not req.human_code.strip():
            raise HTTPException(status_code=400, detail="Both code inputs are required.")

        test_cases = session.query(models.TestCase).filter_by(
            problem_id=req.problem_id).order_by(models.TestCase.test_case_id).all()
        tc_list = [{"input": tc.input, "expected": tc.expected_output} for tc in test_cases]

        entry = problem.entry_function or "solve"

        preflight_error = _preflight_validate(req.language, req.ai_code, req.human_code, problem)
        if preflight_error:
            raise HTTPException(status_code=422, detail=preflight_error)

        ht = getattr(problem, "harness_type", "legacy") or "legacy"
        pid = problem.problem_id

        ai_exec, ai_analysis = _run_variant(req.language, req.ai_code, tc_list, entry,
                                            harness_type=ht, problem_id=pid)
        hu_exec, hu_analysis = _run_variant(req.language, req.human_code, tc_list, entry,
                                            harness_type=ht, problem_id=pid)

        ai_pass = sum(1 for c in ai_exec["cases"] if c["status"] == "PASS")
        hu_pass = sum(1 for c in hu_exec["cases"] if c["status"] == "PASS")
        total = len(tc_list)
        ai_pass_rate = round(ai_pass / total * 100, 2) if total else 0.0
        hu_pass_rate = round(hu_pass / total * 100, 2) if total else 0.0

        ai_mi = maintainability_index(ai_analysis["raw_metrics"], cfg)
        hu_mi = maintainability_index(hu_analysis["raw_metrics"], cfg)

        ai_dims = {
            "reliability_pass_rate": ai_pass_rate,
            "execution_time_ms": ai_exec["execution_time_ms"],
            "maintainability_index": ai_mi,
            "security_findings_count": ai_analysis["security_findings_count"],
            "avg_cyclomatic_complexity": ai_analysis["raw_metrics"]["avg_cyclomatic_complexity"],
            "quality_findings_count": ai_analysis["quality_findings_count"],
        }
        human_dims = {
            "reliability_pass_rate": hu_pass_rate,
            "execution_time_ms": hu_exec["execution_time_ms"],
            "maintainability_index": hu_mi,
            "security_findings_count": hu_analysis["security_findings_count"],
            "avg_cyclomatic_complexity": hu_analysis["raw_metrics"]["avg_cyclomatic_complexity"],
            "quality_findings_count": hu_analysis["quality_findings_count"],
        }

        ai_scores, human_scores, ai_overall, human_overall = compute_scores(
            session, ai_dims, human_dims, cfg)
        ai_dims["overall_score"] = ai_overall
        human_dims["overall_score"] = human_overall

        comparison_rows = compute_comparison_results(ai_dims, human_dims, cfg)

        comparison = models.Comparison(
            problem_id=req.problem_id, language=req.language, ai_name=req.ai_name.strip(),
            ai_source_code=req.ai_code, human_source_code=req.human_code,
            status="completed", created_at=_utcnow(), completed_at=_utcnow(),
            is_pilot=1 if req.experiment_type.upper() == "PILOT" else 0,
            experiment_type=req.experiment_type.upper() if req.experiment_type.upper() in ("PILOT", "RESEARCH") else "RESEARCH",
            problem_version=problem.version,
            test_case_version=min((tc.version for tc in test_cases), default=problem.version),
        )
        session.add(comparison)
        session.flush()

        _persist(session, comparison, problem, test_cases, ai_exec, ai_analysis,
                 hu_exec, hu_analysis, ai_dims, human_dims, ai_scores,
                 human_scores, ai_overall, human_overall, comparison_rows, cfg)
        session.commit()

        return build_report(session, comparison.comparison_id)


@router.get("")
def list_comparisons():
    with SessionLocal() as session:
        rows = (session.query(models.Comparison)
                .order_by(models.Comparison.comparison_id.desc()).all())
        out = []
        for c in rows:
            problem = session.get(models.Problem, c.problem_id)
            overall = session.query(models.ComparisonResult).filter_by(
                comparison_id=c.comparison_id, metric="overall").first()
            out.append({
                "comparison_id": c.comparison_id,
                "problem_id": c.problem_id,
                "problem_title": problem.title if problem else c.problem_id,
                "language": c.language,
                "ai_name": c.ai_name,
                "status": c.status,
                "experiment_type": c.experiment_type,
                "is_pilot": bool(c.is_pilot),
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "overall_winner": overall.direction if overall else None,
                "ai_overall": overall.ai_value if overall else None,
                "human_overall": overall.human_value if overall else None,
            })
        return out


@router.get("/{comparison_id}")
def get_comparison(comparison_id: int):
    with SessionLocal() as session:
        if not session.get(models.Comparison, comparison_id):
            raise HTTPException(status_code=404, detail="Comparison not found.")
        return build_report(session, comparison_id)


@router.get("/{comparison_id}/detailed")
def get_detailed_comparison(comparison_id: int):
    with SessionLocal() as session:
        if not session.get(models.Comparison, comparison_id):
            raise HTTPException(status_code=404, detail="Comparison not found.")
        return build_detailed_report(session, comparison_id)
