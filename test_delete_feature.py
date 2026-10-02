"""
Deletion feature tests — per task requirements.
Tests: delete one, delete multiple, delete by date range, delete all,
verify problems intact, verify test cases intact, verify new submissions = RESEARCH.
"""
import os, sys, tempfile
os.environ["RESEARCH_DB_PATH"] = os.path.join(tempfile.mkdtemp(prefix="rce_del_"), "test.db")

sys.path.insert(0, '.')
from fastapi.testclient import TestClient
from backend.db.session import init_db, SessionLocal
from backend.db import models
from backend.db.seed import load_problems
from backend.main import app

init_db()
load_problems()

client = TestClient(app)
results = []

def check(name, cond, detail=""):
    mark = "PASS" if cond else "FAIL"
    results.append((mark, name, str(detail)[:100]))
    symbol = "  [PASS]" if cond else "  [FAIL]"
    print(f"{symbol} {name}" + (f"  — {str(detail)[:80]}" if not cond and detail else ""))

GOOD_CODE = "def max_subarray(nums):\n    best = current = nums[0]\n    for value in nums[1:]:\n        current = max(value, current + value)\n        best = max(best, current)\n    return best\n"
HUMAN_CODE = "def max_subarray(nums):\n    return max(sum(nums[i:j]) for i in range(len(nums)) for j in range(i + 1, len(nums) + 1))\n"

def submit(ai_name="TestAI"):
    r = client.post("/api/comparisons", json={
        "problem_id": "P002", "language": "python",
        "ai_name": ai_name, "ai_code": GOOD_CODE, "human_code": HUMAN_CODE,
    })
    assert r.status_code == 200, f"Submit failed: {r.text}"
    return r.json()["comparison_id"]

def count_table(session, model):
    return session.query(model).count()

print("\n" + "="*60)
print("DELETE FEATURE TESTS")
print("="*60)

print("\n--- Setup: create 6 comparisons ---")
ids = [submit(f"AI-{i}") for i in range(1, 7)]
print(f"  Created comparison IDs: {ids}")

with SessionLocal() as s:
    initial_probs = count_table(s, models.Problem)
    initial_tcs = count_table(s, models.TestCase)
    initial_comps = count_table(s, models.Comparison)

check("Setup: 6 comparisons created", initial_comps == 6, initial_comps)
check("Setup: 50 problems exist", initial_probs == 50, initial_probs)
check("Setup: 500 test cases exist", initial_tcs == 500, initial_tcs)

# ── Verify new submissions default to RESEARCH ──────────────────────────
print("\n--- Test: new Submit & Compare = RESEARCH DATA ---")
new_id = submit("RESEARCH_CHECK")
with SessionLocal() as s:
    c = s.get(models.Comparison, new_id)
    check("New comparison is_pilot = 0 (RESEARCH)", c.is_pilot == 0, c.is_pilot)
    check("New comparison experiment_type = RESEARCH", c.experiment_type == "RESEARCH", c.experiment_type)
# Delete this one right away to keep count clean
client.delete(f"/api/data-management/comparisons/{new_id}")
with SessionLocal() as s:
    check("After delete, comparison gone", s.get(models.Comparison, new_id) is None)

# ── Test 1: Delete one comparison ───────────────────────────────────────
print("\n--- Test 1: Delete one comparison ---")
target_id = ids[0]
with SessionLocal() as s:
    dep_scores_before = count_table(s, models.Score)

r = client.delete(f"/api/data-management/comparisons/{target_id}")
check("DELETE /comparisons/{id} → 200", r.status_code == 200, r.text[:60])
check("Response success=True", r.json().get("success") is True)
check("Response deleted_comparisons=1", r.json().get("deleted_comparisons") == 1)

with SessionLocal() as s:
    check("Comparison deleted from DB", s.get(models.Comparison, target_id) is None)
    check("execution_results deleted", s.query(models.ExecutionResult).filter_by(comparison_id=target_id).count() == 0)
    check("test_case_results deleted", s.query(models.TestCaseResult).filter_by(comparison_id=target_id).count() == 0)
    check("scores deleted", s.query(models.Score).filter_by(comparison_id=target_id).count() == 0)
    check("comparison_results deleted", s.query(models.ComparisonResult).filter_by(comparison_id=target_id).count() == 0)
    check("statistical_results deleted", s.query(models.StatisticalResult).filter_by(comparison_id=target_id).count() == 0)
    check("preflight_results deleted", s.query(models.PreflightResult).filter_by(comparison_id=target_id).count() == 0)
    check("Problems still intact", count_table(s, models.Problem) == initial_probs)
    check("Test cases still intact", count_table(s, models.TestCase) == initial_tcs)

# 404 for non-existent
r404 = client.delete(f"/api/data-management/comparisons/{target_id}")
check("Second delete → 404", r404.status_code == 404)

# ── Test 2: Delete multiple comparisons ─────────────────────────────────
print("\n--- Test 2: Delete multiple comparisons ---")
multi_ids = ids[1:3]
r = client.request("DELETE", "/api/data-management/comparisons",
    json={"comparison_ids": multi_ids})
check("DELETE /comparisons (multiple) → 200", r.status_code == 200, r.text[:60])
check("deleted_comparisons = 2", r.json().get("deleted_comparisons") == 2, r.json())

with SessionLocal() as s:
    for mid in multi_ids:
        check(f"Comparison {mid} deleted", s.get(models.Comparison, mid) is None)
    check("Problems still intact after multi-delete", count_table(s, models.Problem) == initial_probs)
    check("Test cases still intact after multi-delete", count_table(s, models.TestCase) == initial_tcs)

# ── Test 3: Preview by date range ───────────────────────────────────────
print("\n--- Test 3: Delete by date range ---")
r_prev = client.post("/api/data-management/preview/date-range",
    json={"date_from": "2020-01-01", "date_to": "2099-12-31"})
check("Preview date range → 200", r_prev.status_code == 200)
prev_data = r_prev.json()
remaining_before = prev_data["count"]
check("Preview shows remaining comparisons", remaining_before > 0, remaining_before)

r_del = client.request("DELETE", "/api/data-management/by-date-range",
    json={"date_from": "2020-01-01", "date_to": "2099-12-31"})
check("DELETE /by-date-range → 200", r_del.status_code == 200, r_del.text[:60])
check("All remaining deleted", r_del.json().get("deleted_comparisons") == remaining_before, r_del.json())

with SessionLocal() as s:
    check("No comparisons remain after date range delete", count_table(s, models.Comparison) == 0)
    check("Problems still intact after date range delete", count_table(s, models.Problem) == initial_probs)
    check("Test cases still intact after date range delete", count_table(s, models.TestCase) == initial_tcs)

# ── Test 4: Delete all ───────────────────────────────────────────────────
print("\n--- Test 4: Delete all ---")
# Recreate 2 comparisons first
a = submit("Fresh1")
b = submit("Fresh2")
with SessionLocal() as s:
    check("Recreated 2 comparisons", count_table(s, models.Comparison) == 2)

# Delete without confirmed → error
r_no_conf = client.delete("/api/data-management/all")
check("DELETE /all without confirmed → 400", r_no_conf.status_code == 400)

# Delete with confirmed=true
r_all = client.delete("/api/data-management/all?confirmed=true")
check("DELETE /all?confirmed=true → 200", r_all.status_code == 200, r_all.text[:60])
check("deleted_comparisons = 2", r_all.json().get("deleted_comparisons") == 2, r_all.json())

with SessionLocal() as s:
    check("No comparisons remain", count_table(s, models.Comparison) == 0)
    check("No execution_results remain", count_table(s, models.ExecutionResult) == 0)
    check("No scores remain", count_table(s, models.Score) == 0)
    check("No comparison_results remain", count_table(s, models.ComparisonResult) == 0)
    check("Problems STILL INTACT after delete all", count_table(s, models.Problem) == initial_probs)
    check("Test cases STILL INTACT after delete all", count_table(s, models.TestCase) == initial_tcs)

# ── Test 5: Submit after delete-all → still RESEARCH ────────────────────
print("\n--- Test 5: Submit after delete-all still RESEARCH ---")
new_id2 = submit("POST_DELETE_AI")
with SessionLocal() as s:
    c2 = s.get(models.Comparison, new_id2)
    check("Post-delete new comparison is_pilot=0", c2.is_pilot == 0)
    check("Post-delete new comparison experiment_type=RESEARCH", c2.experiment_type == "RESEARCH")

# ── Test 6: API summary endpoint ────────────────────────────────────────
print("\n--- Test 6: Summary endpoint ---")
r_sum = client.get("/api/data-management/summary")
check("GET /summary → 200", r_sum.status_code == 200)
s_data = r_sum.json()
check("Summary has deletable section", "deletable" in s_data)
check("Summary has protected section", "protected" in s_data)
check("Protected problems = 50", s_data["protected"]["problems"] == initial_probs)
check("Protected test_cases = 500", s_data["protected"]["predefined_test_cases"] == initial_tcs)

# ── Test 7: Dashboard updates after deletion ─────────────────────────────
print("\n--- Test 7: Dashboard updates correctly ---")
dash = client.get("/api/dashboard").json()
check("Dashboard returns 200", "kpis" in dash)

# ── Test 8: No orphaned records ──────────────────────────────────────────
print("\n--- Test 8: No orphaned records ---")
# Delete the post-delete comparison and verify clean state
client.delete(f"/api/data-management/comparisons/{new_id2}")
with SessionLocal() as s:
    check("execution_results: 0 (no orphans)", count_table(s, models.ExecutionResult) == 0)
    check("test_case_results: 0 (no orphans)", count_table(s, models.TestCaseResult) == 0)
    check("complexity_data: 0 (no orphans)", count_table(s, models.ComplexityData) == 0)
    check("security_findings: 0 (no orphans)", count_table(s, models.SecurityFinding) == 0)
    check("static_analysis_results: 0 (no orphans)", count_table(s, models.StaticAnalysisResult) == 0)
    check("scores: 0 (no orphans)", count_table(s, models.Score) == 0)
    check("comparison_results: 0 (no orphans)", count_table(s, models.ComparisonResult) == 0)
    check("statistical_results: 0 (no orphans)", count_table(s, models.StatisticalResult) == 0)
    check("preflight_results: 0 (no orphans)", count_table(s, models.PreflightResult) == 0)
    check("FINAL: Problems intact = 50", count_table(s, models.Problem) == initial_probs)
    check("FINAL: Test cases intact = 500", count_table(s, models.TestCase) == initial_tcs)

# ── Summary ──────────────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
print(f"DELETION TESTS: {passed}/{len(results)} PASSED")
if failed:
    print("\nFAILED:")
    for r in results:
        if r[0] == "FAIL":
            print(f"  ✗ {r[1]}" + (f" — {r[2]}" if r[2] else ""))
print("="*60)

# cleanup
try:
    os.remove(os.environ["RESEARCH_DB_PATH"])
except Exception:
    pass

sys.exit(0 if failed == 0 else 1)
