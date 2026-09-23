"""Execution engine for submitted AI/Human code.

Runs pasted code in an isolated temp directory via subprocess with a strict
timeout. Never uses eval()/exec() in the API process.

Two harness generations:
  harness_type="legacy"  — original string-in/string-out contract
  harness_type="typed"   — LeetCode-style per-problem typed function contract
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
import os

from backend.config import TEMP_BASE_DIR, EXECUTION_TIMEOUT_SECONDS
from backend.engine import harness

# Paths to non-PATH tools
_GPP = r"C:\msys64\ucrt64\bin\g++.exe"
_MSYS2_BIN = r"C:\msys64\ucrt64\bin"

VARIANT_AI = "AI"
VARIANT_HUMAN = "HUMAN"

# Problem-ID -> C preprocessor flag for typed C++ harness
_CPP_PROBLEM_FLAGS = {
    "P001": "P001", "P002": "P002", "P003": "P003", "P004": "P004",
    "P005": "P005", "P006": "P006", "P007": "P007", "P008": "P008",
    "P009": "P009", "P010": "P010",
    "P011": "P011", "P012": "P012", "P013": "P013", "P014": "P014",
    "P015": "P015", "P016": "P016", "P017": "P017", "P018": "P018",
    "P019": "P019", "P020": "P020",
    "P021": "P021", "P022": "P022", "P023": "P023", "P024": "P024",
    "P025": "P025", "P026": "P026", "P027": "P027", "P028": "P028",
    "P029": "P029", "P030": "P030",
    "P031": "P031", "P032": "P032", "P033": "P033", "P034": "P034",
    "P035": "P035", "P036": "P036", "P037": "P037", "P038": "P038",
    "P039": "P039", "P040": "P040",
    "P041": "P041", "P042": "P042", "P043": "P043", "P044": "P044",
    "P045": "P045", "P046": "P046", "P047": "P047", "P048": "P048",
    "P049": "P049", "P050": "P050",
}


def _write(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def _cpp_env() -> dict:
    env = os.environ.copy()
    env["PATH"] = _MSYS2_BIN + os.pathsep + env.get("PATH", "")
    return env


def _run_subprocess(cmd, cwd, timeout, env=None):
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return None, "", "Execution timed out."
    except FileNotFoundError as e:
        return None, "", f"Required runtime not found: {e}"


def execute(language: str, code: str, test_cases, entry_function: str,
            harness_type: str = "legacy", problem_id: str = "") -> dict:
    """Execute `code` against `test_cases`.

    test_cases: list of dicts {input, expected}.
    harness_type: "legacy" or "typed"
    problem_id: required when harness_type=="typed"
    """
    TEMP_BASE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="rce_", dir=str(TEMP_BASE_DIR)))
    try:
        if harness_type == "typed":
            return _execute_typed(language, code, test_cases, entry_function,
                                  problem_id, tmp)
        else:
            return _execute_in_tmp(language, code, test_cases, entry_function, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _all_error(test_cases, error: str) -> list:
    return [
        {
            "index": i,
            "status": "ERROR",
            "actual": None,
            "expected": str(tc.get("expected", "")),
            "error": error,
            "execution_time_ms": None,
            "exit_code": None,
            "stdout": None,
            "stderr": None,
        }
        for i, tc in enumerate(test_cases)
    ]


# ─────────────────────────────────────────────────────────────────────────────
# TYPED execution (LeetCode-style per-problem)
# ─────────────────────────────────────────────────────────────────────────────

def _execute_typed(language, code, test_cases, entry_function, problem_id, tmp):
    start = time.perf_counter()
    cases_json = json.dumps({
        "cases": [{"input": str(t["input"]), "expected": str(t["expected"])}
                  for t in test_cases]
    })
    _write(tmp / "testcases.json", cases_json)

    if language == "python":
        harness_src = (
            harness.PYTHON_TYPED_HARNESS
            .replace("__PROBLEM_ID__", problem_id)
        )
        _write(tmp / "solution.py", code)
        _write(tmp / "harness.py", harness_src)
        rc, out, err = _run_subprocess(
            [sys.executable, "harness.py", "testcases.json"],
            tmp, EXECUTION_TIMEOUT_SECONDS,
        )

    elif language == "java":
        harness_src = (
            harness.JAVA_TYPED_HARNESS
            .replace("__PROBLEM_ID__", problem_id)
        )
        _write(tmp / "Solution.java", code)
        _write(tmp / "Runner.java", harness_src)
        rc, out, err = _run_subprocess(
            ["javac", "Solution.java", "Runner.java"],
            tmp, EXECUTION_TIMEOUT_SECONDS,
        )
        if rc != 0:
            elapsed = (time.perf_counter() - start) * 1000
            return {
                "status": "ERROR",
                "execution_time_ms": round(elapsed, 3),
                "error": "Java compilation failed:\n" + err,
                "cases": _all_error(test_cases, "Compilation failed: " + err.strip()),
                "stdout": out, "stderr": err, "exit_code": rc,
            }
        rc, out, err = _run_subprocess(
            ["java", "Runner", "testcases.json"],
            tmp, EXECUTION_TIMEOUT_SECONDS,
        )

    elif language == "cpp":
        flag = _CPP_PROBLEM_FLAGS.get(problem_id, "UNKNOWN")
        harness_src = (
            harness.CPP_TYPED_HARNESS
            .replace("__PROBLEM_ID__", problem_id)
        )
        _write(tmp / "solution.cpp", code)
        _write(tmp / "runner.cpp", harness_src)
        cpp_env = _cpp_env()
        compile_cmd = [
            _GPP, "-std=c++17", "-O2",
            f"-D{flag}",          # activates the correct #if branch
            "solution.cpp", "runner.cpp", "-o", "runner.exe",
        ]
        rc, out, err = _run_subprocess(compile_cmd, tmp, EXECUTION_TIMEOUT_SECONDS, env=cpp_env)
        if rc != 0:
            elapsed = (time.perf_counter() - start) * 1000
            return {
                "status": "ERROR",
                "execution_time_ms": round(elapsed, 3),
                "error": "C++ compilation failed:\n" + err,
                "cases": _all_error(test_cases, "Compilation failed: " + err.strip()),
                "stdout": out, "stderr": err, "exit_code": rc,
            }
        rc, out, err = _run_subprocess(
            [str(tmp / "runner.exe"), "testcases.json"],
            tmp, EXECUTION_TIMEOUT_SECONDS, env=cpp_env,
        )

    elif language == "javascript":
        harness_src = (
            harness.JS_TYPED_HARNESS
            .replace("__PROBLEM_ID__", problem_id)
        )
        _write(tmp / "solution.js", code)
        _write(tmp / "runner.js", harness_src)
        rc, out, err = _run_subprocess(
            ["node", "runner.js", "testcases.json"],
            tmp, EXECUTION_TIMEOUT_SECONDS,
        )

    else:
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "status": "ERROR",
            "execution_time_ms": round(elapsed, 3),
            "error": f"Unsupported language: {language}",
            "cases": _all_error(test_cases, f"Unsupported language: {language}"),
            "stdout": "", "stderr": "", "exit_code": None,
        }

    return _parse_result(rc, out, err, test_cases, start)


# ─────────────────────────────────────────────────────────────────────────────
# LEGACY execution (string-in / string-out)
# ─────────────────────────────────────────────────────────────────────────────

def _execute_in_tmp(language, code, test_cases, entry_function, tmp):
    start = time.perf_counter()
    rc = None
    out = ""
    err = ""
    if language == "python":
        _write(tmp / "solution.py", code)
        _write(tmp / "harness.py", harness.PYTHON_HARNESS.replace("__ENTRY__", entry_function))
        _write(
            tmp / "testcases.json",
            json.dumps({"cases": [{"input": str(t["input"]), "expected": str(t["expected"])}
                                  for t in test_cases]}),
        )
        rc, out, err = _run_subprocess(
            [sys.executable, "harness.py", "testcases.json"],
            tmp, EXECUTION_TIMEOUT_SECONDS,
        )
    elif language == "java":
        _write(tmp / "Solution.java", code)
        _write(tmp / "Runner.java", harness.JAVA_HARNESS.replace("__ENTRY__", entry_function))
        lines = [f"{t['input']}|||{t['expected']}" for t in test_cases]
        _write(tmp / "testcases.txt", "\n".join(lines))
        rc, out, err = _run_subprocess(
            ["javac", "Solution.java", "Runner.java"], tmp, EXECUTION_TIMEOUT_SECONDS
        )
        if rc != 0:
            elapsed = (time.perf_counter() - start) * 1000
            return {
                "status": "ERROR",
                "execution_time_ms": round(elapsed, 3),
                "error": "Java compilation failed:\n" + err,
                "cases": _all_error(test_cases, "Compilation failed: " + err.strip()),
                "stdout": out, "stderr": err, "exit_code": rc,
            }
        rc, out, err = _run_subprocess(
            ["java", "Runner", "testcases.txt"], tmp, EXECUTION_TIMEOUT_SECONDS
        )
    elif language == "cpp":
        _write(tmp / "solution.cpp", code)
        _write(tmp / "runner.cpp", harness.CPP_HARNESS)
        _write(
            tmp / "testcases.json",
            json.dumps({"cases": [{"input": str(t["input"]), "expected": str(t["expected"])}
                                  for t in test_cases]}),
        )
        cpp_env = _cpp_env()
        compile_cmd = [_GPP, "-std=c++17", "-O2", "solution.cpp", "runner.cpp", "-o", "runner.exe"]
        rc, out, err = _run_subprocess(compile_cmd, tmp, EXECUTION_TIMEOUT_SECONDS, env=cpp_env)
        if rc != 0:
            elapsed = (time.perf_counter() - start) * 1000
            return {
                "status": "ERROR",
                "execution_time_ms": round(elapsed, 3),
                "error": "C++ compilation failed:\n" + err,
                "cases": _all_error(test_cases, "Compilation failed: " + err.strip()),
                "stdout": out, "stderr": err, "exit_code": rc,
            }
        rc, out, err = _run_subprocess(
            [str(tmp / "runner.exe"), "testcases.json"], tmp, EXECUTION_TIMEOUT_SECONDS, env=cpp_env
        )
    elif language == "javascript":
        _write(tmp / "solution.js", code)
        _write(tmp / "runner.js", harness.JS_HARNESS)
        _write(
            tmp / "testcases.json",
            json.dumps({"cases": [{"input": str(t["input"]), "expected": str(t["expected"])}
                                  for t in test_cases]}),
        )
        rc, out, err = _run_subprocess(
            ["node", "runner.js", "testcases.json"], tmp, EXECUTION_TIMEOUT_SECONDS,
        )
    else:
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "status": "ERROR",
            "execution_time_ms": round(elapsed, 3),
            "error": f"Unsupported language: {language}",
            "cases": _all_error(test_cases, f"Unsupported language: {language}"),
            "stdout": out, "stderr": err, "exit_code": rc,
        }

    return _parse_result(rc, out, err, test_cases, start)


def _parse_result(rc, out, err, test_cases, start):
    elapsed = (time.perf_counter() - start) * 1000
    if rc is None:
        timed_out = "timed out" in err.lower()
        return {
            "status": "TIMEOUT" if timed_out else "ERROR",
            "execution_time_ms": round(elapsed, 3),
            "error": err,
            "cases": [
                {
                    "index": i,
                    "status": "TIMEOUT" if timed_out else "ERROR",
                    "actual": None,
                    "expected": str(t.get("expected", "")),
                    "error": err,
                    "execution_time_ms": None,
                    "exit_code": None,
                    "stdout": None,
                    "stderr": None,
                }
                for i, t in enumerate(test_cases)
            ],
            "stdout": out, "stderr": err, "exit_code": None,
        }

    try:
        parsed = json.loads(out)
        cases = parsed.get("cases", [])
    except Exception:
        return {
            "status": "ERROR",
            "execution_time_ms": round(elapsed, 3),
            "error": "Could not parse execution output.\nSTDOUT:\n" + out + "\nSTDERR:\n" + err,
            "cases": _all_error(test_cases, "Execution output parse failure."),
            "stdout": out, "stderr": err, "exit_code": rc,
        }

    status = "PASS"
    if any(c["status"] in ("ERROR", "TIMEOUT") for c in cases):
        status = "ERROR" if any(c["status"] == "ERROR" for c in cases) else "TIMEOUT"
    elif any(c["status"] == "FAIL" for c in cases):
        status = "FAIL"
    return {
        "status": status,
        "execution_time_ms": round(elapsed, 3),
        "error": err if rc != 0 else None,
        "cases": cases,
        "stdout": out,
        "stderr": err,
        "exit_code": rc,
    }
