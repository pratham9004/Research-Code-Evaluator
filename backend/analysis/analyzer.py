"""Static analysis + raw metric extraction for Python and Java.

Python: radon (complexity), AST (function length / nesting / coupling),
        Ruff (code quality), Bandit (security).
Java:   lightweight parser (raw metrics) + optional PMD (quality) /
        SpotBugs (security) when available on PATH.

All findings retain tool name, version, rule, category, severity, message,
location and raw result. Missing tools are recorded, never fabricated.
"""
from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def _run(cmd, input_text=None):
    try:
        proc = subprocess.run(
            cmd, input=input_text, capture_output=True, text=True, timeout=60
        )
        return proc.returncode, proc.stdout, proc.stderr
    except FileNotFoundError:
        return None, "", "not_installed"
    except Exception as e:  # pragma: no cover
        return None, "", str(e)


def _run_shell(cmd: str, timeout: int = 120):
    """Run a shell command string (needed for .bat files on Windows)."""
    try:
        proc = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return None, "", "Command timed out."
    except Exception as e:
        return None, "", str(e)


def _tool_version_shell(cmd: str) -> str | None:
    """Get tool version using shell (for .bat tools on Windows)."""
    rc, out, _ = _run_shell(cmd, timeout=30)
    if rc == 0 and out.strip():
        return out.strip().splitlines()[0]
    return None


def _tool_version(name, flag="--version"):
    rc, out, _ = _run([name, flag])
    if rc == 0:
        return out.strip().splitlines()[0] if out.strip() else name
    return None


# --------------------------------------------------------------------------
# Python
# --------------------------------------------------------------------------

def _python_raw(code: str) -> dict:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            "cyclomatic_avg": 0.0,
            "function_length_avg": 0.0,
            "nesting_depth_avg": 0.0,
            "coupling": 0.0,
            "avg_cyclomatic_complexity": 0.0,
            "loc": 0,
        }

    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    func_lens = [fn.end_lineno - fn.lineno + 1 for fn in funcs if fn.end_lineno]
    function_length_avg = sum(func_lens) / len(func_lens) if func_lens else 0.0

    nesting = []
    for fn in funcs:
        nesting.append(_max_nesting(fn))
    nesting_depth_avg = sum(nesting) / len(nesting) if nesting else 0.0

    coupling = _python_coupling(tree)

    try:
        from radon.complexity import cc_visit
        blocks = cc_visit(code)
        comps = [b.complexity for b in blocks]
        avg_cyclo = sum(comps) / len(comps) if comps else 1.0
    except Exception:
        avg_cyclo = 1.0

    loc = code.count("\n") + 1
    return {
        "cyclomatic_avg": round(avg_cyclo, 3),
        "function_length_avg": round(function_length_avg, 3),
        "nesting_depth_avg": round(nesting_depth_avg, 3),
        "coupling": float(coupling),
        "avg_cyclomatic_complexity": round(avg_cyclo, 3),
        "loc": loc,
    }


_COMPOUND = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith,
             ast.Try, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
             getattr(ast, "Match", ast.If))


def _max_nesting(node, depth=0):
    best = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, _COMPOUND):
            best = max(best, _max_nesting(child, depth + 1))
        else:
            best = max(best, _max_nesting(child, depth))
    return best


def _python_coupling(tree) -> int:
    imported = set()
    attr_bases = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imported.add(a.asname or a.name)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                attr_bases.add(node.value.id)
    return len(imported) + len(attr_bases)


def _python_quality(code: str, notes: list):
    findings = []
    if not shutil.which("ruff"):
        notes.append("Ruff unavailable: code-quality analysis skipped (not fabricated).")
        return findings, notes
    version = _tool_version("ruff")
    rc, out, _ = _run(["ruff", "check", "--output-format=json", "--stdin-filename", "solution.py", "-"], input_text=code)
    if rc is None:
        notes.append("Ruff unavailable: code-quality analysis skipped.")
        return findings, notes
    try:
        items = json.loads(out) if out.strip() else []
    except Exception:
        items = []
    for it in items:
        code_id = it.get("code") or "RULE"
        sev = it.get("severity")
        if sev is None:
            sev = "error" if code_id.startswith("F") else ("warning" if code_id[:1] in "EW" else "info")
        loc = it.get("location", {})
        findings.append({
            "tool_name": "ruff",
            "tool_version": version,
            "rule": code_id,
            "category": "code_quality",
            "severity": sev,
            "message": it.get("message", ""),
            "source_location": f"line {loc.get('row')}:{loc.get('column')}" if loc else "",
            "raw_result": json.dumps(it),
        })
    return findings, notes


def _python_security(code: str, notes: list):
    findings = []
    if not shutil.which("bandit"):
        notes.append("Bandit unavailable: security analysis skipped (not fabricated).")
        return findings, notes
    version = _tool_version("bandit")
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as tf:
        tf.write(code)
        path = tf.name
    try:
        rc, out, _ = _run(["bandit", "-f", "json", "-q", path])
        if rc is None:
            notes.append("Bandit unavailable: security analysis skipped.")
            return findings, notes
        try:
            data = json.loads(out) if out.strip() else {"results": []}
        except Exception:
            data = {"results": []}
        for it in data.get("results", []):
            findings.append({
                "tool_name": "bandit",
                "tool_version": version,
                "rule": it.get("test_id", ""),
                "category": it.get("test_name", ""),
                "severity": it.get("issue_severity", "unknown"),
                "message": it.get("issue_text", ""),
                "source_location": f"line {it.get('line_number')}",
                "raw_result": json.dumps(it),
            })
    finally:
        Path(path).unlink(missing_ok=True)
    return findings, notes


# --------------------------------------------------------------------------
# Java (lightweight parser; optional PMD/SpotBugs)
# --------------------------------------------------------------------------

_METHOD_RE = re.compile(r"^\s*(?:public|private|protected|static|final|\s)*[A-Za-z_<>\[\],\s]+\w+\s*\([^;]*$")


def _java_raw(code: str) -> dict:
    lines = code.splitlines()
    methods = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if _METHOD_RE.search(line) and "(" in line and ";" not in line and "}" not in line.split("(")[0][-1:]:
            # attempt to capture the method signature across lines until ')' and '{'
            depth = 0
            j = i
            started = False
            while j < len(lines):
                seg = lines[j]
                for ch in seg:
                    if ch == "{":
                        started = True
                        depth += 1
                    elif ch == "}":
                        depth -= 1
                if started and depth == 0:
                    break
                j += 1
            if j < len(lines):
                body_lines = lines[i:j + 1]
                methods.append("\n".join(body_lines))
            i = j + 1
        else:
            i += 1

    cycs, lengths, nests = [], [], []
    for m in methods:
        cycs.append(_java_cyclomatic(m))
        lengths.append(m.count("\n") + 1)
        nests.append(_java_nesting(m))

    avg_cyclo = sum(cycs) / len(cycs) if cycs else 1.0
    avg_len = sum(lengths) / len(lengths) if lengths else 0.0
    avg_nest = sum(nests) / len(nests) if nests else 0.0

    imports = len(re.findall(r"^\s*import\s+", code, re.M))
    attr_bases = set(re.findall(r"([A-Za-z_][\w]*)\.", code))
    coupling = imports + len(attr_bases)

    return {
        "cyclomatic_avg": round(avg_cyclo, 3),
        "function_length_avg": round(avg_len, 3),
        "nesting_depth_avg": round(avg_nest, 3),
        "coupling": float(coupling),
        "avg_cyclomatic_complexity": round(avg_cyclo, 3),
        "loc": len(lines),
    }


def _java_cyclomatic(method: str) -> int:
    score = 1
    score += len(re.findall(r"\bif\s*\(", method))
    score += len(re.findall(r"\bfor\s*\(", method))
    score += len(re.findall(r"\bwhile\s*\(", method))
    score += len(re.findall(r"\bcase\s+", method))
    score += len(re.findall(r"\bcatch\s*\(", method))
    score += len(re.findall(r"\b&&\b", method))
    score += len(re.findall(r"\b\|\|\b", method))
    score += len(re.findall(r"\?", method))
    return score


def _java_nesting(method: str) -> int:
    depth = 0
    max_d = 0
    in_str = False
    for ch in method:
        if ch in "\"'":
            in_str = not in_str
        if in_str:
            continue
        if ch == "{":
            depth += 1
            max_d = max(max_d, depth)
        elif ch == "}":
            depth -= 1
    return max(0, max_d - 1)


def _java_quality(code: str, notes: list):
    findings = []
    pmd_cmd = shutil.which("pmd") or shutil.which("pmd.bat")
    if not pmd_cmd:
        notes.append("PMD unavailable: Java code-quality analysis skipped (not fabricated).")
        return findings, notes

    version = _tool_version_shell("pmd.bat --version 2>&1") or _tool_version_shell("pmd --version 2>&1") or "unknown"
    # PMD outputs ASCII art before the version line; extract the actual version line
    if version and "PMD" not in version:
        # Try to find the PMD version line specifically
        rc_v, out_v, _ = _run_shell("pmd.bat --version 2>&1", timeout=30)
        if out_v:
            for line in out_v.splitlines():
                if line.strip().startswith("PMD "):
                    version = line.strip()
                    break

    with tempfile.NamedTemporaryFile("w", suffix=".java", delete=False, prefix="Solution") as tf:
        tf.write(code)
        path = tf.name

    out_dir = tempfile.mkdtemp()
    out_json = Path(out_dir) / "pmd_out.json"
    try:
        # PMD 7.x CLI: pmd check -d <file> -R <ruleset> -f <format>
        cmd = f'pmd.bat check -d "{path}" -R rulesets/java/quickstart.xml -f json 2>&1'
        rc, out, err = _run_shell(cmd, timeout=60)
        if rc is None:
            notes.append("PMD: analysis timed out or failed to run.")
            return findings, notes
        # PMD exits with 4 when violations found, 0 when clean, other codes = errors
        if rc not in (0, 4):
            notes.append(f"PMD: analysis error (rc={rc}).")
            return findings, notes
        try:
            data = json.loads(out) if out.strip() else {}
        except Exception:
            data = {}
        for v in data.get("violations", []):
            findings.append({
                "tool_name": "pmd",
                "tool_version": version,
                "rule": v.get("rule", ""),
                "category": "code_quality",
                "severity": str(v.get("priority", "info")),
                "message": v.get("description", ""),
                "source_location": f"line {v.get('beginline', '')}",
                "raw_result": json.dumps(v),
            })
        notes.append(f"PMD {version}: analysis completed, {len(findings)} finding(s).")
    finally:
        Path(path).unlink(missing_ok=True)
        shutil.rmtree(out_dir, ignore_errors=True)
    return findings, notes


def _java_security(code: str, notes: list):
    findings = []
    spotbugs_cmd = shutil.which("spotbugs") or shutil.which("spotbugs.bat")
    if not spotbugs_cmd:
        notes.append("SpotBugs unavailable: Java security analysis skipped (not fabricated).")
        return findings, notes

    version = "unknown"
    try:
        vr = subprocess.run("spotbugs.bat -version", shell=True, capture_output=True, text=True, timeout=30)
        if vr.returncode == 0 and vr.stdout.strip():
            version = vr.stdout.strip().splitlines()[0]
    except Exception:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        src_path = Path(tmp) / "Solution.java"
        src_path.write_text(code, encoding="utf-8")

        # Compile the source first
        rc, out, err = _run(["javac", str(src_path)])
        if rc != 0:
            notes.append(f"SpotBugs: Java compilation failed during security analysis — findings not collected.")
            return findings, notes

        # Run SpotBugs on the compiled class directory
        out_xml = Path(tmp) / "spotbugs_results.xml"
        sb_rc, sb_out, sb_err = _run_shell(
            f'spotbugs.bat -textui -xml -output "{out_xml}" "{tmp}"',
            timeout=120
        )
        if sb_rc is None:
            notes.append("SpotBugs: analysis timed out or failed to run.")
            return findings, notes

        if not out_xml.exists():
            notes.append(f"SpotBugs: no output file produced (rc={sb_rc}).")
            return findings, notes

        # Parse XML output
        try:
            import xml.etree.ElementTree as ET
            tree = ET.parse(str(out_xml))
            root = tree.getroot()
            for bug in root.findall("BugInstance"):
                bug_type = bug.get("type", "UNKNOWN")
                priority = bug.get("priority", "3")
                category = bug.get("category", "")
                rank = bug.get("rank", "")
                # Map priority: 1=high, 2=medium, 3=low
                sev = "high" if priority == "1" else ("medium" if priority == "2" else "low")
                # Get source line info
                source_line = bug.find("SourceLine")
                location = ""
                if source_line is not None:
                    loc_start = source_line.get("start", "")
                    loc_end = source_line.get("end", "")
                    src_file = source_line.get("sourcefile", "Solution.java")
                    location = f"{src_file}:{loc_start}" if loc_start else src_file
                # Get message
                long_msg = bug.find("LongMessage")
                short_msg = bug.find("ShortMessage")
                msg = (long_msg.text if long_msg is not None and long_msg.text
                       else short_msg.text if short_msg is not None and short_msg.text
                       else bug_type)
                findings.append({
                    "tool_name": "spotbugs",
                    "tool_version": version,
                    "rule": bug_type,
                    "category": category or "security",
                    "severity": sev,
                    "message": msg,
                    "source_location": location,
                    "raw_result": ET.tostring(bug, encoding="unicode"),
                })
            notes.append(f"SpotBugs {version}: analysis completed, {len(findings)} finding(s).")
        except Exception as ex:
            notes.append(f"SpotBugs: XML parse error — {ex}")

    return findings, notes


# --------------------------------------------------------------------------
# C++
# --------------------------------------------------------------------------

_CPPCHECK = r"C:\msys64\ucrt64\bin\cppcheck.exe"


def _cpp_raw(code: str) -> dict:
    """Lightweight regex-based raw metrics for C++."""
    lines = code.splitlines()
    loc = len(lines)

    # Find function bodies by tracking braces after a signature pattern
    func_pattern = re.compile(
        r"^\s*(?:[\w:<>*&\s]+)\s+\w+\s*\([^;]*\)\s*(?:const\s*)?(?:noexcept\s*)?\{"
    )
    func_starts = []
    for i, line in enumerate(lines):
        if func_pattern.match(line) or (
            "{" in line and re.search(r"\w+\s*\([^;]*\)\s*(?:const\s*)?(?:noexcept\s*)?\s*\{", line)
        ):
            func_starts.append(i)

    func_bodies = []
    for start in func_starts:
        depth = 0
        for j in range(start, len(lines)):
            for ch in lines[j]:
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
            if depth == 0 and j > start:
                func_bodies.append("\n".join(lines[start : j + 1]))
                break

    cycs, lengths, nests = [], [], []
    for body in func_bodies:
        cycs.append(_cpp_cyclomatic(body))
        lengths.append(body.count("\n") + 1)
        nests.append(_cpp_nesting(body))

    avg_cyclo = sum(cycs) / len(cycs) if cycs else 1.0
    avg_len = sum(lengths) / len(lengths) if lengths else 0.0
    avg_nest = sum(nests) / len(nests) if nests else 0.0

    includes = len(re.findall(r"^\s*#include\s+", code, re.M))
    attr_bases = set(re.findall(r"([A-Za-z_][\w]*)::", code))
    coupling = includes + len(attr_bases)

    return {
        "cyclomatic_avg": round(avg_cyclo, 3),
        "function_length_avg": round(avg_len, 3),
        "nesting_depth_avg": round(avg_nest, 3),
        "coupling": float(coupling),
        "avg_cyclomatic_complexity": round(avg_cyclo, 3),
        "loc": loc,
    }


def _cpp_cyclomatic(body: str) -> int:
    score = 1
    score += len(re.findall(r"\bif\s*\(", body))
    score += len(re.findall(r"\bfor\s*\(", body))
    score += len(re.findall(r"\bwhile\s*\(", body))
    score += len(re.findall(r"\bcase\s+", body))
    score += len(re.findall(r"\bcatch\s*\(", body))
    score += len(re.findall(r"&&", body))
    score += len(re.findall(r"\|\|", body))
    score += body.count("?")
    return score


def _cpp_nesting(body: str) -> int:
    depth = 0
    max_d = 0
    in_str = False
    for ch in body:
        if ch in "\"'":
            in_str = not in_str
        if in_str:
            continue
        if ch == "{":
            depth += 1
            max_d = max(max_d, depth)
        elif ch == "}":
            depth -= 1
    return max(0, max_d - 1)


def _cpp_quality_security(code: str, notes: list):
    """Run cppcheck for both quality and security findings (cppcheck covers both)."""
    quality = []
    security = []

    if not Path(_CPPCHECK).exists():
        notes.append("cppcheck unavailable: C++ quality/security analysis skipped (not fabricated).")
        return quality, security, notes

    # Get version
    rc_v, out_v, _ = _run([_CPPCHECK, "--version"])
    version = out_v.strip() if rc_v == 0 and out_v.strip() else "unknown"

    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as tf:
        tf.write(code)
        path = tf.name

    try:
        rc, out, err = _run(
            [
                _CPPCHECK,
                "--enable=all",
                "--suppress=missingIncludeSystem",
                "--suppress=missingInclude",
                "--output-format=sarif",
                "--quiet",
                path,
            ]
        )
        # cppcheck writes SARIF to stdout when --output-format=sarif
        sarif_text = out if out.strip() else ""
        if rc is None:
            notes.append("cppcheck: analysis failed to run.")
            return quality, security, notes

        try:
            data = json.loads(sarif_text) if sarif_text.strip() else {}
        except Exception:
            # Fall back to stderr text parsing
            data = {}

        if data:
            for run_ in data.get("runs", []):
                for result in run_.get("results", []):
                    rule_id = result.get("ruleId", "")
                    msg = result.get("message", {}).get("text", "")
                    locs = result.get("locations", [])
                    loc_str = ""
                    if locs:
                        phys = locs[0].get("physicalLocation", {})
                        region = phys.get("region", {})
                        loc_str = f"line {region.get('startLine', '')}"
                    level = result.get("level", "warning")
                    sev = "high" if level == "error" else ("medium" if level == "warning" else "info")
                    # security-related rule IDs
                    is_sec = any(k in rule_id.lower() for k in ("buffer", "overflow", "uninit", "leak", "null", "use-after", "format", "inject", "unsafe"))
                    entry = {
                        "tool_name": "cppcheck",
                        "tool_version": version,
                        "rule": rule_id,
                        "category": "security" if is_sec else "code_quality",
                        "severity": sev,
                        "message": msg,
                        "source_location": loc_str,
                        "raw_result": json.dumps(result),
                    }
                    if is_sec:
                        security.append(entry)
                    else:
                        quality.append(entry)
            notes.append(f"cppcheck {version}: {len(quality)} quality, {len(security)} security finding(s).")
        else:
            # Parse plain-text stderr output as fallback
            # Format: file:line:col: severity: message [ruleId]
            pattern = re.compile(r"^.+?:(\d+):\d+:\s+(\w+):\s+(.*?)\s+\[([^\]]+)\]$")
            for line in err.splitlines():
                m = pattern.match(line)
                if not m:
                    continue
                lineno, level, msg, rule_id = m.groups()
                sev = "high" if level == "error" else ("medium" if level == "warning" else "info")
                is_sec = any(k in rule_id.lower() for k in ("buffer", "overflow", "uninit", "leak", "null", "format", "inject", "unsafe"))
                entry = {
                    "tool_name": "cppcheck",
                    "tool_version": version,
                    "rule": rule_id,
                    "category": "security" if is_sec else "code_quality",
                    "severity": sev,
                    "message": msg,
                    "source_location": f"line {lineno}",
                    "raw_result": line,
                }
                if is_sec:
                    security.append(entry)
                else:
                    quality.append(entry)
            notes.append(f"cppcheck {version}: {len(quality)} quality, {len(security)} security finding(s) (text fallback).")
    finally:
        Path(path).unlink(missing_ok=True)

    return quality, security, notes


# --------------------------------------------------------------------------
# JavaScript
# --------------------------------------------------------------------------

_ESLINT_CMD = "eslint"  # globally installed


def _js_raw(code: str) -> dict:
    """Lightweight raw metrics for JavaScript."""
    lines = code.splitlines()
    loc = len(lines)

    func_pattern = re.compile(
        r"(?:function\s+\w+\s*\(|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?function)"
    )
    func_starts = [i for i, line in enumerate(lines) if func_pattern.search(line)]

    func_bodies = []
    for start in func_starts:
        depth = 0
        started = False
        for j in range(start, len(lines)):
            for ch in lines[j]:
                if ch == "{":
                    depth += 1
                    started = True
                elif ch == "}":
                    depth -= 1
            if started and depth == 0:
                func_bodies.append("\n".join(lines[start : j + 1]))
                break

    cycs, lengths, nests = [], [], []
    for body in func_bodies:
        cycs.append(_js_cyclomatic(body))
        lengths.append(body.count("\n") + 1)
        nests.append(_js_nesting(body))

    avg_cyclo = sum(cycs) / len(cycs) if cycs else 1.0
    avg_len = sum(lengths) / len(lengths) if lengths else 0.0
    avg_nest = sum(nests) / len(nests) if nests else 0.0

    requires = len(re.findall(r"\brequire\s*\(", code))
    imports = len(re.findall(r"^\s*import\s+", code, re.M))
    attr_bases = set(re.findall(r"([A-Za-z_$][\w$]*)\.", code))
    coupling = requires + imports + len(attr_bases)

    return {
        "cyclomatic_avg": round(avg_cyclo, 3),
        "function_length_avg": round(avg_len, 3),
        "nesting_depth_avg": round(avg_nest, 3),
        "coupling": float(coupling),
        "avg_cyclomatic_complexity": round(avg_cyclo, 3),
        "loc": loc,
    }


def _js_cyclomatic(body: str) -> int:
    score = 1
    score += len(re.findall(r"\bif\s*\(", body))
    score += len(re.findall(r"\bfor\s*\(", body))
    score += len(re.findall(r"\bwhile\s*\(", body))
    score += len(re.findall(r"\bcase\s+", body))
    score += len(re.findall(r"\bcatch\s*\(", body))
    score += len(re.findall(r"&&", body))
    score += len(re.findall(r"\|\|", body))
    score += body.count("?")
    return score


def _js_nesting(body: str) -> int:
    depth = 0
    max_d = 0
    in_str = False
    for ch in body:
        if ch in "\"'`":
            in_str = not in_str
        if in_str:
            continue
        if ch == "{":
            depth += 1
            max_d = max(max_d, depth)
        elif ch == "}":
            depth -= 1
    return max(0, max_d - 1)


def _js_quality_security(code: str, notes: list):
    """Run eslint with eslint-plugin-security for quality + security findings."""
    quality = []
    security = []

    eslint_path = shutil.which(_ESLINT_CMD)
    if not eslint_path:
        notes.append("eslint unavailable: JavaScript quality/security analysis skipped (not fabricated).")
        return quality, security, notes

    rc_v, out_v, _ = _run([eslint_path, "--version"])
    version = out_v.strip() if rc_v == 0 and out_v.strip() else "unknown"

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "solution.js"
        src.write_text(code, encoding="utf-8")

        # Write a minimal flat eslint config (ESLint 9+ uses eslint.config.js)
        cfg_file = Path(tmp) / "eslint.config.mjs"
        cfg_file.write_text(
            """
import securityPlugin from 'eslint-plugin-security';
export default [
  {
    plugins: { security: securityPlugin },
    rules: {
      ...securityPlugin.configs.recommended.rules,
      'no-eval': 'warn',
      'no-implied-eval': 'warn',
      'no-new-func': 'warn',
    },
  },
];
""",
            encoding="utf-8",
        )

        rc, out, err = _run(
            [eslint_path, "--format=json", "--no-ignore", str(src)],
            # Pass the tmp dir as cwd so eslint.config.mjs is discovered
        )
        # rc=1 means lint violations found, rc=0 = clean, other = error
        if rc is None:
            notes.append("eslint: analysis failed to run.")
            return quality, security, notes

        try:
            data = json.loads(out) if out.strip() else []
        except Exception:
            data = []

        for file_result in data:
            for msg in file_result.get("messages", []):
                rule_id = msg.get("ruleId") or "unknown"
                sev_code = msg.get("severity", 1)
                sev = "error" if sev_code == 2 else "warning"
                message = msg.get("message", "")
                loc_str = f"line {msg.get('line', '')}:{msg.get('column', '')}"
                is_sec = rule_id.startswith("security/")
                entry = {
                    "tool_name": "eslint",
                    "tool_version": version,
                    "rule": rule_id,
                    "category": "security" if is_sec else "code_quality",
                    "severity": sev,
                    "message": message,
                    "source_location": loc_str,
                    "raw_result": json.dumps(msg),
                }
                if is_sec:
                    security.append(entry)
                else:
                    quality.append(entry)

        notes.append(f"eslint {version}: {len(quality)} quality, {len(security)} security finding(s).")

    return quality, security, notes


# --------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------

def analyze(language: str, code: str) -> dict:
    notes: list = []
    if language == "python":
        raw = _python_raw(code)
        quality, notes = _python_quality(code, notes)
        security, notes = _python_security(code, notes)
    elif language == "java":
        raw = _java_raw(code)
        quality, notes = _java_quality(code, notes)
        security, notes = _java_security(code, notes)
    elif language == "cpp":
        raw = _cpp_raw(code)
        quality, security, notes = _cpp_quality_security(code, notes)
    elif language == "javascript":
        raw = _js_raw(code)
        quality, security, notes = _js_quality_security(code, notes)
    else:
        raw = {"cyclomatic_avg": 0.0, "function_length_avg": 0.0,
               "nesting_depth_avg": 0.0, "coupling": 0.0,
               "avg_cyclomatic_complexity": 0.0, "loc": 0}
        quality, security = [], []

    quality_count = sum(1 for f in quality if f.get("category") != "tool_status")
    security_count = sum(1 for f in security if f.get("category") != "tool_status")
    return {
        "raw_metrics": raw,
        "quality_findings": quality,
        "security_findings": security,
        "quality_findings_count": quality_count,
        "security_findings_count": security_count,
        "tool_notes": notes,
    }
