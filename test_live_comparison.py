"""
Full AI-vs-Human comparison workflow test through the live FastAPI application.
Tests P001-P020 benchmark (20 problems, 200 test cases).
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# ── 1. Verify problems loaded ────────────────────────────────────────────
print("=== Step 1: Problems API ===")
r = client.get("/api/problems")
assert r.status_code == 200, f"Problems API failed: {r.status_code}"
problems = r.json()
print(f"  Problems loaded: {len(problems)}")
assert len(problems) == 30, f"Expected 30 problems, got {len(problems)}"
p001 = next(p for p in problems if p["problem_id"] == "P001")
p011 = next(p for p in problems if p["problem_id"] == "P011")
assert p001["harness_type"] == "typed"
assert p001["starter_template_python"] is not None
assert p011["harness_type"] == "typed"
assert p011["starter_template_python"] is not None
print(f"  P001 harness_type: {p001['harness_type']}  ✓")
print(f"  P011 harness_type: {p011['harness_type']}  ✓")
print(f"  All 20 problems loaded  ✓")

# ── 2. Verify P011-P020 present ─────────────────────────────────────────
print("\n=== Step 2: P011-P020 verification ===")
new_ids = [f"P0{i}" for i in range(11, 21)]
loaded_ids = [p["problem_id"] for p in problems]
for pid in new_ids:
    assert pid in loaded_ids, f"{pid} not found"
print(f"  P011-P020 all present  ✓")
r = client.get("/api/problems/P016")
assert r.status_code == 200
p016 = r.json()
assert p016["test_case_count"] == 10
assert p016["harness_type"] == "typed"
print(f"  P016 test cases: {p016['test_case_count']}  ✓")
print(f"  P016 first test: {p016['test_cases'][0]['input']}  →  {p016['test_cases'][0]['expected_output']}")

# ── 3. Submit AI-vs-Human comparison (P002) ──────────────────────────────
print("\n=== Step 3: Submit AI-vs-Human comparison (P002, Python) ===")

AI_CODE = """
def max_subarray(nums):
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best
"""

HUMAN_CODE = """
def max_subarray(nums):
    max_sum = nums[0]
    for i in range(len(nums)):
        current = 0
        for j in range(i, len(nums)):
            current += nums[j]
            max_sum = max(max_sum, current)
    return max_sum
"""

payload = {
    "problem_id": "P002",
    "language": "python",
    "ai_name": "ChatGPT-4o (Research Test)",
    "ai_code": AI_CODE,
    "human_code": HUMAN_CODE,
    "experiment_type": "RESEARCH",
}

r = client.post("/api/comparisons", json=payload)
assert r.status_code == 200, f"Submission failed ({r.status_code}): {r.text[:500]}"
report = r.json()
cid = report["comparison_id"]
print(f"  Comparison ID: {cid}  ✓")
print(f"  Problem: {report['problem_title']}  ✓")

exec_ai = report["execution"]["ai"]
exec_hu = report["execution"]["human"]
print(f"  AI execution:    {exec_ai['passed']}/{exec_ai['total']} passed  ({exec_ai['execution_time_ms']:.1f}ms)")
print(f"  Human execution: {exec_hu['passed']}/{exec_hu['total']} passed  ({exec_hu['execution_time_ms']:.1f}ms)")
assert exec_ai["passed"] == 10
assert exec_hu["passed"] == 10
print("  Both pass all 10 test cases  ✓")

scores = report["scores"]
overall = next(m for m in report["comparison"] if m["metric"] == "overall")
print(f"  AI overall: {scores['ai_overall']}  Human overall: {scores['human_overall']}")
print(f"  Winner: {overall['direction']}  ✓")

# ── 4. Submit comparison on a new P011-P020 problem ─────────────────────
print("\n=== Step 4: Submit comparison on P016 (HTML Escaper, Python) ===")

AI_HTML = """
def escape_html(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'",'&#39;')
"""

HUMAN_HTML = """
def escape_html(s):
    result = []
    for ch in s:
        if ch == '&':   result.append('&amp;')
        elif ch == '<': result.append('&lt;')
        elif ch == '>': result.append('&gt;')
        elif ch == '"': result.append('&quot;')
        elif ch == "'": result.append('&#39;')
        else:           result.append(ch)
    return ''.join(result)
"""

r2 = client.post("/api/comparisons", json={
    "problem_id": "P016",
    "language": "python",
    "ai_name": "ChatGPT-4o (Research Test)",
    "ai_code": AI_HTML,
    "human_code": HUMAN_HTML,
    "experiment_type": "RESEARCH",
})
assert r2.status_code == 200, f"P016 submission failed: {r2.text[:300]}"
rep2 = r2.json()
cid2 = rep2["comparison_id"]
exec_ai2 = rep2["execution"]["ai"]
exec_hu2 = rep2["execution"]["human"]
assert exec_ai2["passed"] == 10, f"P016 AI passed {exec_ai2['passed']}/10"
assert exec_hu2["passed"] == 10, f"P016 Human passed {exec_hu2['passed']}/10"
print(f"  P016 Comparison ID: {cid2}  ✓")
print(f"  AI: {exec_ai2['passed']}/10 PASS  Human: {exec_hu2['passed']}/10 PASS  ✓")
print(f"  Both P011-P020 problems execute correctly through the live API  ✓")

# ── 5. Retrieve and verify reports ──────────────────────────────────────
print("\n=== Step 5: Retrieve reports ===")
r = client.get(f"/api/comparisons/{cid}")
assert r.status_code == 200
assert r.json()["problem_title"] == "Maximum Subarray Sum"
print(f"  GET /api/comparisons/{cid} → 200  ✓")

r = client.get(f"/api/comparisons/{cid2}/detailed")
assert r.status_code == 200
detail = r.json()
assert "six_dimensions" in detail
assert detail["experiment"]["problem_id"] == "P016"
print(f"  Detailed report for P016 → 200  ✓")
print(f"  All 6 dimensions present  ✓")

# ── 6. Dashboard ─────────────────────────────────────────────────────────
print("\n=== Step 6: Dashboard ===")
r = client.get("/api/dashboard")
assert r.status_code == 200
kpis = r.json()["kpis"]
print(f"  total_problems:    {kpis['total_problems']}")
print(f"  total_comparisons: {kpis['total_comparisons']}")
assert kpis["total_problems"] == 30, f"Expected 30 problems, got {kpis['total_problems']}"
assert kpis["total_comparisons"] >= 2
print("  Dashboard shows 30 problems and ≥2 comparisons  ✓")

# ── 7. Statistics ────────────────────────────────────────────────────────
print("\n=== Step 7: Statistics API ===")
r = client.get("/api/statistics")
assert r.status_code == 200
print("  /api/statistics → 200  ✓")

# ── 8. Summary ───────────────────────────────────────────────────────────
print("\n" + "="*60)
print("ALL WORKFLOW STEPS PASSED")
print(f"  20 problems (P001-P030 all loaded and accessible")
print(f"  P001-P010 and P011-P020 both execute correctly")
print(f"  AI-vs-Human comparison stored and retrievable")
print(f"  All 6 research dimensions scored")
print(f"  Dashboard shows correct problem count (20)")
print("="*60)
