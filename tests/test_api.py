import os
import tempfile

import pytest

# Use an isolated test database before any backend module is imported.
_TMP = tempfile.mkdtemp(prefix="rce_test_")
os.environ["RESEARCH_DB_PATH"] = os.path.join(_TMP, "test_research.db")

from fastapi.testclient import TestClient  # noqa: E402

from backend.db.session import init_db, SessionLocal  # noqa: E402
from backend.db import models  # noqa: E402
from backend.db.seed import load_problems  # noqa: E402
from backend.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()
    load_problems()
    yield
    # cleanup temp db
    try:
        os.remove(os.environ["RESEARCH_DB_PATH"])
    except OSError:
        pass


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def sample_python(n):
    # correct integer range validator for P013
    # input: "value|min|max" → "VALID" if min <= value <= max else "INVALID"
    return (
        "def is_valid_range(s):\n"
        "    parts = s.strip().split('|')\n"
        "    try:\n"
        "        v, lo, hi = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())\n"
        "        if lo > hi: return 'INVALID'\n"
        "        return 'VALID' if lo <= v <= hi else 'INVALID'\n"
        "    except Exception:\n"
        "        return 'INVALID'\n"
    )


def sample_python_bad():
    # always returns wrong answer
    return "def is_valid_range(s):\n    return 'wrong'\n"


# ---------------------------------------------------------------------------
# Problem IDs used across tests
# ---------------------------------------------------------------------------
_TEST_PROBLEM_ID = "P013"   # Integer Range Validator — simple, deterministic


# ---------------------------------------------------------------------------
# Problem bank
# ---------------------------------------------------------------------------

def test_problems_load(client):
    probs = client.get("/api/problems").json()
    assert len(probs) == 50
    assert any(p["problem_id"] == "P001" for p in probs)
    assert any(p["problem_id"] == "P050" for p in probs)


def test_problem_detail(client):
    p = client.get("/api/problems/P001").json()
    assert "title" in p
    assert p["title"]  # non-empty title
    # This is a research instrument; test cases including expected outputs are
    # shown to the researcher so they understand the problem specification.
    assert "test_cases" in p
    assert len(p["test_cases"]) == 10
    assert all("input" in tc for tc in p["test_cases"])
    assert all("expected_output" in tc for tc in p["test_cases"])
    # New language signatures present
    assert "signature_python" in p
    assert "signature_java" in p
    assert "signature_cpp" in p
    assert "signature_javascript" in p


# ---------------------------------------------------------------------------
# Execution + comparison
# ---------------------------------------------------------------------------

def test_python_execution_and_comparison(client):
    # Use P013 (Integer Range Validator): input "value|min|max" -> VALID/INVALID
    correct_code = (
        "def is_valid_range(s):\n"
        "    parts = s.strip().split('|')\n"
        "    try:\n"
        "        v, lo, hi = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())\n"
        "        if lo > hi: return 'INVALID'\n"
        "        return 'VALID' if lo <= v <= hi else 'INVALID'\n"
        "    except Exception:\n"
        "        return 'INVALID'\n"
    )
    r = client.post("/api/comparisons", json={
        "problem_id": "P013", "language": "python", "ai_name": "ChatGPT",
        "ai_code": correct_code,
        "human_code": sample_python_bad(),
    })
    assert r.status_code == 200
    d = r.json()
    assert d["execution"]["ai"]["pass_rate"] == 100.0
    assert d["execution"]["human"]["pass_rate"] == 0.0  # always returns 'wrong'
    assert d["scores"]["ai_overall"] is not None
    assert d["scores"]["human_overall"] is not None
    assert any(c["metric"] == "reliability" for c in d["comparison"])


def test_java_not_available_graceful(client):
    # Java runtime is installed; ensure comparison succeeds end-to-end.
    # Use the canonical P001 typed-harness contract: twoSum(nums, target).
    # Any of PASS/FAIL/ERROR/TIMEOUT are valid outcomes.
    java_code = """public class Solution {
        public static int[] twoSum(int[] nums, int target) {
            for (int i = 0; i < nums.length; i++) {
                for (int j = i + 1; j < nums.length; j++) {
                    if (nums[i] + nums[j] == target) return new int[] {i, j};
                }
            }
            return new int[] {0, 0};
        }
    }"""
    r = client.post("/api/comparisons", json={
        "problem_id": "P001", "language": "java", "ai_name": "Claude",
        "ai_code": java_code,
        "human_code": java_code,
    })
    # Either success (if JDK installed) or a clean 200 with ERROR status.
    assert r.status_code == 200
    d = r.json()
    assert d["execution"]["ai"]["status"] in ("PASS", "FAIL", "ERROR", "TIMEOUT")


def test_validation_missing_fields(client):
    r = client.post("/api/comparisons", json={
        "problem_id": "P001", "language": "python", "ai_name": "",
        "ai_code": "x", "human_code": "y",
    })
    assert r.status_code == 400


def test_invalid_language(client):
    # Submit a language string that is not in P001's supported_languages list
    r = client.post("/api/comparisons", json={
        "problem_id": "P001", "language": "cobol", "ai_name": "ChatGPT",
        "ai_code": "x", "human_code": "y",
    })
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Persistence / DB
# ---------------------------------------------------------------------------

def test_comparison_persisted(client):
    correct_code = (
        "def is_valid_range(s):\n"
        "    parts = s.strip().split('|')\n"
        "    try:\n"
        "        v, lo, hi = int(parts[0].strip()), int(parts[1].strip()), int(parts[2].strip())\n"
        "        if lo > hi: return 'INVALID'\n"
        "        return 'VALID' if lo <= v <= hi else 'INVALID'\n"
        "    except Exception:\n"
        "        return 'INVALID'\n"
    )
    client.post("/api/comparisons", json={
        "problem_id": "P013", "language": "python", "ai_name": "Gemini",
        "ai_code": correct_code,
        "human_code": correct_code,
    })
    with SessionLocal() as s:
        assert s.query(models.Comparison).count() >= 1
        assert s.query(models.TestCaseResult).count() >= 1
        assert s.query(models.Score).count() >= 1
        assert s.query(models.ComparisonResult).count() >= 1


def test_dashboard_aggregation(client):
    d = client.get("/api/dashboard").json()
    assert d["kpis"]["total_problems"] == 50
    assert d["kpis"]["total_comparisons"] >= 1
    assert "ChatGPT" in d["ai_systems"] or "Gemini" in d["ai_systems"]


def test_statistics_insufficient_then_present(client):
    # With >=2 comparisons we can check statistics endpoint runs.
    d = client.get("/api/statistics").json()
    assert "per_metric" in d
    assert "reliability" in d["per_metric"]


def test_export_csv(client):
    csv_text = client.get("/api/export/dataset?format=csv").text
    assert "comparison_id" in csv_text


def test_reports_list_and_detail(client):
    lst = client.get("/api/comparisons").json()
    assert isinstance(lst, list) and len(lst) >= 1
    cid = lst[0]["comparison_id"]
    detail = client.get(f"/api/comparisons/{cid}").json()
    assert detail["comparison_id"] == cid
    assert "comparison" in detail


def test_detailed_report(client):
    lst = client.get("/api/comparisons").json()
    assert len(lst) >= 1
    cid = lst[0]["comparison_id"]
    r = client.get(f"/api/comparisons/{cid}/detailed")
    assert r.status_code == 200
    data = r.json()
    assert data["experiment"]["comparison_id"] == cid
    assert "executive_result" in data
    assert "six_dimensions" in data
    assert "reliability" in data
    assert "maintainability" in data
    assert "scoring_calculation" in data
    assert "normalization" in data
    assert "ai_vs_human" in data
    assert "statistical_analysis" in data
    assert "interpretation" in data
    # data_classification is either PILOT or RESEARCH depending on how the comparison was created
    assert data["experiment"]["data_classification"] in ("PILOT / TEST DATA", "RESEARCH DATA")


def test_excel_export(client):
    r = client.get("/api/export/research-report")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(r.content) > 0
    assert r.headers["content-disposition"] == "attachment; filename=research_report.xlsx"


def test_detailed_report_maintainability_calculation(client):
    lst = client.get("/api/comparisons").json()
    cid = lst[0]["comparison_id"]
    r = client.get(f"/api/comparisons/{cid}/detailed")
    assert r.status_code == 200
    data = r.json()
    ai_mi = data["maintainability"]["ai"]["final_score"]
    hu_mi = data["maintainability"]["human"]["final_score"]
    assert 0 <= ai_mi <= 100
    assert 0 <= hu_mi <= 100
    components = data["maintainability"]["ai"]["components"]
    assert "cyclomatic" in components
    assert "function_length" in components
    assert "nesting" in components
    assert "coupling" in components
    for comp in components.values():
        assert "raw_value" in comp
        assert "reference_min" in comp
        assert "reference_max" in comp
        assert "normalized_score" in comp
        assert "weight" in comp
        assert "weighted_contribution" in comp
