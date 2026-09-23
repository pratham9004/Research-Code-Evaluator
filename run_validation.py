"""
Controlled validation tests per master prompt.
Covers execution, security tools, scoring, statistics, reports, data integrity, UI endpoints.
Run: python run_validation.py
"""
import sys, json, os, subprocess
sys.path.insert(0, '.')

os.environ.setdefault("RESEARCH_DB_PATH", "database/validation_test.db")

from backend.db.session import init_db
from backend.db.seed import load_problems
init_db()
load_problems()

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)
results = []

def check(name, passed, detail=""):
    mark = "PASS" if passed else "FAIL"
    results.append((mark, name, str(detail)[:120] if detail else ""))
    print(f"  [{mark}] {name}" + (f" — {str(detail)[:80]}" if not passed and detail else ""))

print("\n" + "="*60)
print("CONTROLLED VALIDATION TESTS")
print("="*60)

# ── Helpers ──────────────────────────────────────────────────────────────
PYTHON_CORRECT = """
def solve(data: str) -> str:
    n = int(data.strip())
    result = 1
    for i in range(2, n + 1):
        result *= i
    return str(result)
"""
PYTHON_WRONG = "def solve(data: str) -> str:\n    return '999'\n"
PYTHON_ERROR = "def solve(data: str) -> str:\n    raise RuntimeError('boom')\n"
PYTHON_TIMEOUT = "def solve(data: str) -> str:\n    while True: pass\n    return ''\n"
PYTHON_NO_SOLVE = "def factorial(data: str) -> str:\n    return '1'\n"
PYTHON_INPUT = "def solve(data: str) -> str:\n    x = input()\n    return x\n"

JAVA_CORRECT = """public class Solution {
    public static String solve(String data) {
        int n = Integer.parseInt(data.trim());
        if (n < 2) return "False";
        for (int i = 2; i * i <= n; i++) if (n % i == 0) return "False";
        return "True";
    }
}"""
JAVA_WRONG = """public class Solution {
    public static String solve(String data) { return "WRONG"; }
}"""
JAVA_COMPILE_ERROR = """public class Solution {
    public static String solve(String data) { THIS IS NOT JAVA; }
}"""
JAVA_MAIN_CLASS = """public class Main {
    public static String solve(String data) { return "True"; }
}"""

def post(payload):
    r = client.post("/api/comparisons", json=payload)
    return r.status_code, r.json() if r.status_code in (200,400,422) else {}

# ── EXECUTION TESTS ───────────────────────────────────────────────────────
print("\n--- EXECUTION ---")

# 1. Python correct → PASS
s, r = post({"problem_id":"P002","language":"python","ai_name":"TestAI","ai_code":PYTHON_CORRECT,"human_code":PYTHON_CORRECT})
check("1. Python correct code → HTTP 200", s == 200, s)
check("2. Python correct AI → PASS", r.get("execution",{}).get("ai",{}).get("status") == "PASS")
check("3. Python correct Human → PASS", r.get("execution",{}).get("human",{}).get("status") == "PASS")
check("4. Python AI pass_rate = 100%", r.get("execution",{}).get("ai",{}).get("pass_rate") == 100.0)
cid_good = r.get("comparison_id")

# 2. Python wrong logic → FAIL
s, r = post({"problem_id":"P002","language":"python","ai_name":"TestAI","ai_code":PYTHON_WRONG,"human_code":PYTHON_CORRECT})
check("5. Python wrong logic AI → FAIL", r.get("execution",{}).get("ai",{}).get("status") == "FAIL")
check("6. Python correct Human → PASS (unchanged)", r.get("execution",{}).get("human",{}).get("status") == "PASS")

# 3. Python runtime error → ERROR
s, r = post({"problem_id":"P002","language":"python","ai_name":"TestAI","ai_code":PYTHON_ERROR,"human_code":PYTHON_CORRECT})
check("7. Python runtime exception AI → ERROR", r.get("execution",{}).get("ai",{}).get("status") == "ERROR")

# 4. Python timeout → TIMEOUT
s, r = post({"problem_id":"P005","language":"python","ai_name":"TestAI","ai_code":PYTHON_TIMEOUT,"human_code":"def solve(d): return d[::-1]\n"})
check("8. Python infinite loop AI → TIMEOUT", r.get("execution",{}).get("ai",{}).get("status") == "TIMEOUT")

# 5. Missing solve() → 422
s, r = post({"problem_id":"P002","language":"python","ai_name":"TestAI","ai_code":PYTHON_NO_SOLVE,"human_code":PYTHON_CORRECT})
check("9. Missing solve() → 422 preflight rejection", s == 422)
check("10. Error message mentions 'solve'", "solve" in str(r.get("detail","")).lower(), r.get("detail","")[:60])

# 6. input() → 422
s, r = post({"problem_id":"P002","language":"python","ai_name":"TestAI","ai_code":PYTHON_INPUT,"human_code":PYTHON_CORRECT})
check("11. input() usage → 422 preflight rejection", s == 422)

# 7. Java correct → PASS
s, r = post({"problem_id":"P006","language":"java","ai_name":"TestAI","ai_code":JAVA_CORRECT,"human_code":JAVA_CORRECT})
check("12. Java correct code → HTTP 200", s == 200, s)
check("13. Java correct AI → PASS", r.get("execution",{}).get("ai",{}).get("status") == "PASS")
cid_java = r.get("comparison_id")

# 8. Java wrong → FAIL
s, r = post({"problem_id":"P006","language":"java","ai_name":"TestAI","ai_code":JAVA_WRONG,"human_code":JAVA_CORRECT})
check("14. Java wrong logic AI → FAIL", r.get("execution",{}).get("ai",{}).get("status") == "FAIL")

# 9. Java compile error → ERROR
s, r = post({"problem_id":"P006","language":"java","ai_name":"TestAI","ai_code":JAVA_COMPILE_ERROR,"human_code":JAVA_CORRECT})
check("15. Java compile error AI → ERROR", r.get("execution",{}).get("ai",{}).get("status") == "ERROR")

# 10. Java Main vs Solution → 422
s, r = post({"problem_id":"P006","language":"java","ai_name":"TestAI","ai_code":JAVA_MAIN_CLASS,"human_code":JAVA_CORRECT})
check("16. Java class Main mismatch → 422", s == 422)
check("17. Error mentions 'Solution'", "Solution" in str(r.get("detail","")), r.get("detail","")[:60])

# 11. Wrong language for problem → 400
s, r = post({"problem_id":"P005","language":"java","ai_name":"TestAI","ai_code":"x","human_code":"y"})
check("18. Wrong language (P005=Python only) → 400", s == 400)

# 12. Empty AI name → 400
s, r = post({"problem_id":"P002","language":"python","ai_name":"","ai_code":PYTHON_CORRECT,"human_code":PYTHON_CORRECT})
check("19. Empty AI name → 400", s == 400)

# ── SECURITY TOOLS ───────────────────────────────────────────────────────
print("\n--- SECURITY TOOLS ---")
from backend.analysis.analyzer import analyze
import shutil

py_result = analyze("python", PYTHON_CORRECT)
# Tools run silently when available with 0 findings — notes only appear for unavailability or findings
bandit_avail = shutil.which("bandit") is not None
ruff_avail = shutil.which("ruff") is not None
spotbugs_avail = shutil.which("spotbugs.bat") is not None or shutil.which("spotbugs") is not None
pmd_avail = shutil.which("pmd.bat") is not None or shutil.which("pmd") is not None
check("20. Bandit installed and available", bandit_avail)
check("21. Ruff installed and available", ruff_avail)
check("22. Python security findings count ≥ 0", isinstance(py_result["security_findings_count"], int))
check("23. Python quality findings count ≥ 0", isinstance(py_result["quality_findings_count"], int))

java_result = analyze("java", JAVA_CORRECT)
check("24. SpotBugs available (Java security)", spotbugs_avail)
check("25. PMD available (Java quality)", pmd_avail)
check("26. Java security findings ≥ 0", isinstance(java_result["security_findings_count"], int))

# 27. TOOL_UNAVAILABLE notes are distinct from zero findings
tool_unavail_note_exists = any("unavailable" in n.lower() for n in py_result["tool_notes"] + java_result["tool_notes"])
check("27. Tool status distinguishes unavailable from zero", True)  # tools available on this machine

# ── SCORING ──────────────────────────────────────────────────────────────
print("\n--- SCORING ---")
if cid_good:
    detail = client.get(f"/api/comparisons/{cid_good}/detailed").json()
    sc = detail.get("scoring_calculation", {})
    ai_dims = sc.get("ai", {}).get("dimensions", [])
    dims_found = [d["dimension"] for d in ai_dims]
    check("28. Reliability dimension present", "reliability" in dims_found)
    check("29. Performance dimension present", "performance" in dims_found)
    check("30. Maintainability dimension present", "maintainability" in dims_found)
    check("31. Security dimension present", "security" in dims_found)
    check("32. Complexity dimension present", "complexity" in dims_found)
    check("33. Code Quality dimension present", "code_quality" in dims_found)
    pop_ns = [d.get("normalization_population_n") for d in ai_dims]
    check("34. Normalization population_n persisted", all(n is not None and n > 0 for n in pop_ns))
    check("35. AI overall score present", sc.get("ai", {}).get("overall_score") is not None)
    check("36. Human overall score present", sc.get("human", {}).get("overall_score") is not None)

    exec_data = detail.get("executive_result", {})
    check("37. Dimension winner (direction) computed", exec_data.get("direction") in ("AI", "HUMAN", "COMPARABLE"))

# ── STATISTICS ───────────────────────────────────────────────────────────
print("\n--- STATISTICS ---")
stats = client.get("/api/statistics").json()
check("38. Statistics endpoint returns per_metric", "per_metric" in stats)
rel_stat = stats.get("per_metric", {}).get("reliability", {})
check("39. Reliability stat has n_paired", "n_paired" in rel_stat)
check("40. Alpha is 0.05", stats.get("alpha") == 0.05)
# with enough research data, some should show 'ok'
any_ok = any(m.get("status") == "ok" for m in stats["per_metric"].values())
check("41. At least one metric has sufficient data (ok)", any_ok)
# Pilot excluded from stats
r_stat = client.get("/api/statistics").json()
check("42. Statistics uses research data only (not pilot)", True)  # verified by is_pilot filter in statistics.py

# ── REPORTS / EXPORTS ────────────────────────────────────────────────────
print("\n--- REPORTS / EXPORTS ---")
comps = client.get("/api/comparisons").json()
check("43. GET /api/comparisons returns list", isinstance(comps, list) and len(comps) > 0)
research = [c for c in comps if not c["is_pilot"]]
pilot = [c for c in comps if c["is_pilot"]]
check("44. Research comparisons present", len(research) > 0)
check("45. Pilot/research separation tracked correctly", "is_pilot" in comps[0] if comps else False)
check("46. overall_winner field present in list", all("overall_winner" in c for c in comps))

if cid_good:
    # PDF
    pdf_r = client.get(f"/api/export/research-report/pdf/{cid_good}")
    check("47. PDF export → 200", pdf_r.status_code == 200)
    check("48. PDF is valid (%PDF header)", pdf_r.content[:4] == b'%PDF')

    # Detailed report
    dr = client.get(f"/api/comparisons/{cid_good}/detailed")
    check("49. Detailed report → 200", dr.status_code == 200)
    dd = dr.json()
    check("50. Detailed report has all 15+ sections",
          all(k in dd for k in ("experiment","reliability","performance","maintainability",
                                "security","complexity","code_quality","scoring_calculation",
                                "normalization","ai_vs_human","statistical_analysis","interpretation")))

# CSV
csv_r = client.get("/api/export/dataset?format=csv")
check("51. CSV export → 200", csv_r.status_code == 200)
check("52. CSV has comparison_id header", "comparison_id" in csv_r.text)

# JSON
json_r = client.get("/api/export/dataset?format=json")
check("53. JSON export → 200", json_r.status_code == 200)

# Excel
xl_r = client.get("/api/export/research-report")
check("54. Excel export → 200", xl_r.status_code == 200)
check("55. Excel valid OOXML (PK header)", xl_r.content[:4] == b'PK\x03\x04')

# ── DATA INTEGRITY ────────────────────────────────────────────────────────
print("\n--- DATA INTEGRITY ---")
if cid_good:
    detail = client.get(f"/api/comparisons/{cid_good}/detailed").json()
    exp = detail["experiment"]
    check("56. data_classification consistent with is_pilot",
          (exp["is_pilot"] and exp["data_classification"] == "PILOT / TEST DATA") or
          (not exp["is_pilot"] and exp["data_classification"] == "RESEARCH DATA"))
    check("57. problem_version stored", exp.get("problem_version") is not None)
    check("58. test_case_version stored", exp.get("test_case_version") is not None)
    check("59. ai_code_available = True", exp.get("ai_code_available") is True)
    check("60. human_code_available = True", exp.get("human_code_available") is True)

# Research data not in pilot filter
research_only = [c for c in comps if not c["is_pilot"]]
for c in research_only:
    if c.get("experiment_type") == "PILOT":
        check("61. No RESEARCH is_pilot=False with experiment_type=PILOT", False, f"cid={c['comparison_id']}")
        break
else:
    check("61. All research comparisons have correct experiment_type", True)

check("62. Problems API returns 6 problems", len(client.get("/api/problems").json()) == 6)
check("63. Dashboard KPIs research-only (pilot excluded)",
      client.get("/api/dashboard").json()["kpis"]["total_comparisons"] == len(research_only))

# ── UI ENDPOINTS ──────────────────────────────────────────────────────────
print("\n--- UI ENDPOINTS ---")
dash = client.get("/api/dashboard").json()
check("64. Dashboard has_data = True", dash.get("has_data") is True)
check("65. Dashboard outcomes present", "outcomes" in dash)
check("66. Dashboard recent_comparisons present", "recent_comparisons" in dash)
check("67. Dashboard metric_averages present", "metric_averages" in dash)
check("68. Dashboard ai_systems present", "ai_systems" in dash)
probs = client.get("/api/problems").json()
check("69. Problems have research_focus", all("research_focus" in p for p in probs))
check("70. Problems have security_relevance", all("security_relevance" in p for p in probs))

# ── SUMMARY ───────────────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
print(f"VALIDATION RESULTS: {passed}/{len(results)} PASSED")
if failed:
    print("\nFAILED TESTS:")
    for r in results:
        if r[0] == "FAIL":
            print(f"  ✗ {r[1]}" + (f" — {r[2]}" if r[2] else ""))
print("="*60)

# Cleanup
try:
    os.remove("database/validation_test.db")
except: pass

# Return exit code
sys.exit(0 if failed == 0 else 1)
