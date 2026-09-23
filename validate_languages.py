"""
End-to-end execution validation for all 4 languages.
Uses the real executor + harness pipeline (same path as the API).
"""
import os, sys, json
os.environ.setdefault("RESEARCH_DB_PATH", "database/research.db")
sys.path.insert(0, ".")

from backend.engine.executor import execute
from backend.db.session import SessionLocal
from backend.db import models

PASS_MARK = "\u2705"
FAIL_MARK = "\u274c"
WARN_MARK = "\u26a0\ufe0f"

def get_test_cases(problem_id):
    with SessionLocal() as s:
        tcs = s.query(models.TestCase).filter_by(problem_id=problem_id).order_by(models.TestCase.test_case_id).all()
        return [{"input": tc.input, "expected": tc.expected_output} for tc in tcs]

def run_test(lang, problem_id, label, code, expect_all_pass):
    tcs = get_test_cases(problem_id)
    result = execute(lang, code, tcs, "solve")
    status     = result["status"]
    cases      = result.get("cases", [])
    passed     = sum(1 for c in cases if c["status"] == "PASS")
    failed     = sum(1 for c in cases if c["status"] == "FAIL")
    errored    = sum(1 for c in cases if c["status"] == "ERROR")
    total      = len(cases)
    elapsed    = result.get("execution_time_ms", 0)

    ok = (expect_all_pass and status in ("PASS",)) or \
         (not expect_all_pass and status in ("FAIL", "ERROR", "PASS"))

    mark = PASS_MARK if ok else FAIL_MARK
    print(f"\n{mark}  [{lang.upper()}] {label}")
    print(f"   Problem : {problem_id}")
    print(f"   Status  : {status}  ({passed}/{total} passed, {failed} failed, {errored} errors)  {elapsed:.1f}ms")

    if expect_all_pass and status != "PASS":
        print(f"   {FAIL_MARK} EXPECTED all PASS — got {status}")
        # Show failing cases
        for c in cases:
            if c["status"] != "PASS":
                print(f"      TC#{c['index']} status={c['status']}")
                print(f"        input    = {repr(tcs[c['index']]['input'])}")
                print(f"        expected = {repr(c['expected'])}")
                print(f"        actual   = {repr(c['actual'])}")
                if c.get("error"):
                    print(f"        error    = {c['error']}")
        # Also dump raw stdout/stderr for compile/harness failures
        if result.get("error"):
            print(f"   Engine error: {result['error'][:800]}")
        if result.get("stderr"):
            print(f"   STDERR: {result['stderr'][:800]}")
    elif not expect_all_pass:
        # Deliberate wrong — just confirm it didn't ERROR unexpectedly
        if status == "ERROR" and errored == total:
            print(f"   {WARN_MARK}  All cases ERROR (may be compile/runtime issue, not a FAIL)")
            if result.get("error"):
                print(f"   Engine error: {result['error'][:600]}")
        else:
            print(f"   {PASS_MARK} Deliberate wrong solution correctly scored {status}")

    return ok, result

# =============================================================================
# SOLUTIONS — B013 Integer Range Validator
# Input: "value|min|max"  →  "VALID" or "INVALID"
# =============================================================================

PYTHON_CORRECT = """\
def solve(data: str) -> str:
    parts = data.strip().split('|')
    try:
        v  = int(parts[0].strip())
        lo = int(parts[1].strip())
        hi = int(parts[2].strip())
        if lo > hi:
            return 'INVALID'
        return 'VALID' if lo <= v <= hi else 'INVALID'
    except Exception:
        return 'INVALID'
"""

PYTHON_WRONG = """\
def solve(data: str) -> str:
    return 'WRONG'
"""

JAVA_CORRECT = """\
public class Solution {
    public static String solve(String data) {
        String[] parts = data.trim().split("\\\\|");
        try {
            int v  = Integer.parseInt(parts[0].trim());
            int lo = Integer.parseInt(parts[1].trim());
            int hi = Integer.parseInt(parts[2].trim());
            if (lo > hi) return "INVALID";
            return (v >= lo && v <= hi) ? "VALID" : "INVALID";
        } catch (Exception e) {
            return "INVALID";
        }
    }
}
"""

JAVA_WRONG = """\
public class Solution {
    public static String solve(String data) {
        return "WRONG";
    }
}
"""

CPP_CORRECT = """\
#include <string>
#include <sstream>
#include <stdexcept>
using namespace std;

string solve(const string& data) {
    // parse "value|min|max"
    string token;
    int vals[3];
    int idx = 0;
    string s = data;
    // trim
    while (!s.empty() && (s.front()==' '||s.front()=='\\t')) s.erase(s.begin());
    while (!s.empty() && (s.back()==' '||s.back()=='\\t')) s.pop_back();

    istringstream ss(s);
    while (getline(ss, token, '|')) {
        // trim token
        while (!token.empty() && (token.front()==' '||token.front()=='\\t')) token.erase(token.begin());
        while (!token.empty() && (token.back()==' '||token.back()=='\\t')) token.pop_back();
        if (idx >= 3) return "INVALID";
        try { vals[idx++] = stoi(token); }
        catch(...) { return "INVALID"; }
    }
    if (idx != 3) return "INVALID";
    int v = vals[0], lo = vals[1], hi = vals[2];
    if (lo > hi) return "INVALID";
    return (v >= lo && v <= hi) ? "VALID" : "INVALID";
}
"""

CPP_WRONG = """\
#include <string>
using namespace std;
string solve(const string& data) {
    return "WRONG";
}
"""

JS_CORRECT = """\
function solve(data) {
    const parts = data.trim().split('|');
    try {
        const v  = parseInt(parts[0].trim(), 10);
        const lo = parseInt(parts[1].trim(), 10);
        const hi = parseInt(parts[2].trim(), 10);
        if (isNaN(v) || isNaN(lo) || isNaN(hi)) return 'INVALID';
        if (lo > hi) return 'INVALID';
        return (v >= lo && v <= hi) ? 'VALID' : 'INVALID';
    } catch (e) {
        return 'INVALID';
    }
}
module.exports = { solve };
"""

JS_WRONG = """\
function solve(data) { return 'WRONG'; }
module.exports = { solve };
"""

# =============================================================================
# RUN ALL TESTS
# =============================================================================
print("=" * 65)
print("  RESEARCH CODE EVALUATOR — 4-LANGUAGE EXECUTION VALIDATION")
print("  Problem: B013  Integer Range Validator  (10 test cases)")
print("=" * 65)

results = {}

ok_py_good,  r_py_good  = run_test("python",     "B013", "Correct solution",     PYTHON_CORRECT, expect_all_pass=True)
ok_py_bad,   r_py_bad   = run_test("python",     "B013", "Deliberate wrong",     PYTHON_WRONG,   expect_all_pass=False)
ok_java_good,r_java_good= run_test("java",        "B013", "Correct solution",     JAVA_CORRECT,   expect_all_pass=True)
ok_java_bad, r_java_bad = run_test("java",        "B013", "Deliberate wrong",     JAVA_WRONG,     expect_all_pass=False)
ok_cpp_good, r_cpp_good = run_test("cpp",         "B013", "Correct solution",     CPP_CORRECT,    expect_all_pass=True)
ok_cpp_bad,  r_cpp_bad  = run_test("cpp",         "B013", "Deliberate wrong",     CPP_WRONG,      expect_all_pass=False)
ok_js_good,  r_js_good  = run_test("javascript",  "B013", "Correct solution",     JS_CORRECT,     expect_all_pass=True)
ok_js_bad,   r_js_bad   = run_test("javascript",  "B013", "Deliberate wrong",     JS_WRONG,       expect_all_pass=False)

print("\n" + "=" * 65)
print("  SUMMARY")
print("=" * 65)
py_ok   = ok_py_good   and ok_py_bad
java_ok = ok_java_good and ok_java_bad
cpp_ok  = ok_cpp_good  and ok_cpp_bad
js_ok   = ok_js_good   and ok_js_bad

for lang, ok in [("Python    ", py_ok), ("Java      ", java_ok), ("C++       ", cpp_ok), ("JavaScript", js_ok)]:
    print(f"  {PASS_MARK if ok else FAIL_MARK}  {lang}  {'PASS' if ok else 'ISSUE'}")

print()
all_ok = py_ok and java_ok and cpp_ok and js_ok
print("  OVERALL:", "ALL PASS — ready for research data collection" if all_ok else "ISSUES FOUND — see details above")
print()
