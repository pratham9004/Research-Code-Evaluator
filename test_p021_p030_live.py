"""Live API test for P021-P030."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# ── Verify all 30 problems present ────────────────────────────────────
r = client.get("/api/problems")
assert r.status_code == 200
problems = r.json()
assert len(problems) == 30, f"Expected 30, got {len(problems)}"
new_ids = [f"P0{i}" for i in range(21,31)]
loaded_ids = {p["problem_id"] for p in problems}
for pid in new_ids:
    assert pid in loaded_ids, f"{pid} missing"
print(f"  All 30 problems present ✓  (P021-P030 confirmed)")

# ── Verify P021 detail ─────────────────────────────────────────────────
r = client.get("/api/problems/P021")
assert r.status_code == 200
p = r.json()
assert p["harness_type"] == "typed"
assert p["test_case_count"] == 10
print(f"  P021: '{p['title']}' — {p['test_case_count']} test cases ✓")

# ── Submit comparison on P029 (Sort Direction Validator) ───────────────
AI = """
def validate_sort_direction(s):
    n = s.strip().upper()
    return n if n in ('ASC','DESC') else 'INVALID'
"""
HUMAN = """
def validate_sort_direction(s):
    cleaned = s.strip().upper()
    if cleaned == 'ASC': return 'ASC'
    if cleaned == 'DESC': return 'DESC'
    return 'INVALID'
"""
r = client.post("/api/comparisons", json={
    "problem_id": "P029",
    "language": "python",
    "ai_name": "TestAI-P029",
    "ai_code": AI,
    "human_code": HUMAN,
    "experiment_type": "RESEARCH"
})
assert r.status_code == 200, f"P029 submission failed: {r.text[:200]}"
rep = r.json()
assert rep["execution"]["ai"]["passed"] == 10
assert rep["execution"]["human"]["passed"] == 10
print(f"  P029 comparison: AI 10/10 PASS, Human 10/10 PASS ✓")

# ── Submit on P026 (SQL Identifier Validator) ──────────────────────────
AI2 = """
import re
def is_valid_sql_identifier(name):
    if not name or len(name) > 64: return False
    return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))
"""
HUMAN2 = """
def is_valid_sql_identifier(name):
    if not name or len(name) > 64: return False
    if not (name[0].isalpha() or name[0] == '_'): return False
    return all(c.isalnum() or c == '_' for c in name)
"""
r2 = client.post("/api/comparisons", json={
    "problem_id": "P026",
    "language": "python",
    "ai_name": "TestAI-P026",
    "ai_code": AI2,
    "human_code": HUMAN2,
    "experiment_type": "RESEARCH"
})
assert r2.status_code == 200, f"P026 failed: {r2.text[:200]}"
rep2 = r2.json()
assert rep2["execution"]["ai"]["passed"] == 10
assert rep2["execution"]["human"]["passed"] == 10
print(f"  P026 comparison: AI 10/10 PASS, Human 10/10 PASS ✓")

# ── Check dashboard ────────────────────────────────────────────────────
r = client.get("/api/dashboard")
kpis = r.json()["kpis"]
assert kpis["total_problems"] == 30
assert kpis["total_comparisons"] >= 3
print(f"  Dashboard: {kpis['total_problems']} problems, {kpis['total_comparisons']} comparisons ✓")

print("\nALL P021-P030 LIVE TESTS PASSED ✓")
