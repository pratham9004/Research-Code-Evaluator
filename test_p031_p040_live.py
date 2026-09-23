"""Live API verification for P031-P040."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# ── 1. DB counts ─────────────────────────────────────────────────────
r = client.get("/api/problems")
assert r.status_code == 200
problems = r.json()
assert len(problems) == 40, f"Expected 40, got {len(problems)}"
print(f"  Problems: {len(problems)} ✓")

new_ids = [f"P0{i}" for i in range(31,41)]
loaded  = {p["problem_id"] for p in problems}
for pid in new_ids:
    assert pid in loaded, f"{pid} missing"
print(f"  P031-P040 all present ✓")

# P001 and P030 still exist (boundary check)
assert "P001" in loaded and "P030" in loaded, "P001 or P030 missing!"
print(f"  P001 and P030 still intact ✓")

# ── 2. Problem detail ─────────────────────────────────────────────────
for pid in ["P031","P037","P040"]:
    r2 = client.get(f"/api/problems/{pid}")
    assert r2.status_code == 200
    p = r2.json()
    assert p["harness_type"] == "typed"
    assert p["test_case_count"] == 10
    assert p["starter_template_python"] is not None
    print(f"  {pid}: '{p['title']}' — 10 TCs — typed ✓")

# ── 3. Submit comparison on P033 (Shell Meta Detector, Python) ───────
AI = """
def detect_shell_meta(s):
    dangerous = set(';|&$`><(){}"' + "'\\\\" + '\\n\\r')
    for ch in s:
        if ch in dangerous: return "unsafe"
    return "safe"
"""
HUMAN = """
def detect_shell_meta(s):
    for ch in s:
        if ch in (';','|','&','$','`','>','<','(',')','{'  ,'}','"',"'",'\\\\','\\n','\\r'):
            return "unsafe"
    return "safe"
"""
r3 = client.post("/api/comparisons", json={
    "problem_id": "P033", "language": "python",
    "ai_name": "TestAI-P033", "ai_code": AI, "human_code": HUMAN,
    "experiment_type": "RESEARCH"
})
assert r3.status_code == 200, f"P033 submission failed: {r3.text[:200]}"
rep = r3.json()
assert rep["execution"]["ai"]["passed"] == 10, f"AI passed {rep['execution']['ai']['passed']}/10"
assert rep["execution"]["human"]["passed"] == 10
print(f"  P033 comparison: AI 10/10, Human 10/10 ✓")

# ── 4. Submit comparison on P040 (Numeric Expr Validator, Python) ────
AI2 = """
import re
def validate_numeric_expr(s):
    s = s.strip()
    if not s: return 'invalid'
    pattern = r'^-?(?:0|[1-9][0-9]*)(?:\\s*[+\\-*/]\\s*-?(?:0|[1-9][0-9]*))*$'
    return 'valid' if re.match(pattern, s) else 'invalid'
"""
HUMAN2 = """
import re
def validate_numeric_expr(s):
    s = s.strip()
    if not s: return 'invalid'
    num = r'-?(?:0|[1-9]\\d*)'
    op  = r'\\s*[+\\-*/]\\s*'
    if re.fullmatch(f'{num}(?:{op}{num})*', s):
        return 'valid'
    return 'invalid'
"""
r4 = client.post("/api/comparisons", json={
    "problem_id": "P040", "language": "python",
    "ai_name": "TestAI-P040", "ai_code": AI2, "human_code": HUMAN2,
    "experiment_type": "RESEARCH"
})
assert r4.status_code == 200, f"P040 failed: {r4.text[:200]}"
rep4 = r4.json()
assert rep4["execution"]["ai"]["passed"] == 10
assert rep4["execution"]["human"]["passed"] == 10
print(f"  P040 comparison: AI 10/10, Human 10/10 ✓")

# ── 5. Dashboard ─────────────────────────────────────────────────────
r5 = client.get("/api/dashboard")
kpis = r5.json()["kpis"]
assert kpis["total_problems"] == 40, f"Expected 40 problems, got {kpis['total_problems']}"
assert kpis["total_comparisons"] >= 2
print(f"  Dashboard: {kpis['total_problems']} problems, {kpis['total_comparisons']} comparisons ✓")

# ── 6. Statistics ─────────────────────────────────────────────────────
r6 = client.get("/api/statistics")
assert r6.status_code == 200
print(f"  Statistics API: 200 ✓")

print("\nALL P031-P040 LIVE TESTS PASSED ✓")
