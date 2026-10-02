"""Loads the predefined research problem bank from config/problems.yaml into SQLite."""
from __future__ import annotations

import yaml

from backend.config import PROBLEMS_YAML
from backend.db import models
from backend.db.session import SessionLocal, init_db


def _problem_from_dict(p: dict) -> models.Problem:
    return models.Problem(
        problem_id=p["id"],
        title=p["title"],
        description=p["description"].strip(),
        category=p["category"],
        difficulty=p["difficulty"],
        supported_languages=p["supported_languages"],
        version=p.get("version", 1),
        input_spec=p.get("input_spec"),
        output_spec=p.get("output_spec"),
        constraints=p.get("constraints"),
        # legacy single starter_template (kept for backwards compat)
        starter_template=p.get("starter_template") or p.get("starter_template_python"),
        active=p.get("active", True),
        signature_python=p.get("signature_python"),
        signature_java=p.get("signature_java"),
        signature_cpp=p.get("signature_cpp"),
        signature_javascript=p.get("signature_javascript"),
        entry_function=p.get("entry_function", "solve"),
        research_focus=p.get("research_focus"),
        security_relevance=p.get("security_relevance"),
        harness_type=p.get("harness_type", "legacy"),
        starter_template_python=p.get("starter_template_python"),
        starter_template_java=p.get("starter_template_java"),
        starter_template_cpp=p.get("starter_template_cpp"),
        starter_template_javascript=p.get("starter_template_javascript"),
    )


def _update_problem(existing: models.Problem, p: dict) -> None:
    existing.title = p["title"]
    existing.description = p["description"].strip()
    existing.category = p["category"]
    existing.difficulty = p["difficulty"]
    existing.supported_languages = p["supported_languages"]
    existing.version = p.get("version", 1)
    existing.input_spec = p.get("input_spec")
    existing.output_spec = p.get("output_spec")
    existing.constraints = p.get("constraints")
    existing.starter_template = p.get("starter_template") or p.get("starter_template_python")
    existing.active = p.get("active", True)
    existing.signature_python = p.get("signature_python")
    existing.signature_java = p.get("signature_java")
    existing.signature_cpp = p.get("signature_cpp")
    existing.signature_javascript = p.get("signature_javascript")
    existing.entry_function = p.get("entry_function", "solve")
    existing.research_focus = p.get("research_focus")
    existing.security_relevance = p.get("security_relevance")
    existing.harness_type = p.get("harness_type", "legacy")
    existing.starter_template_python = p.get("starter_template_python")
    existing.starter_template_java = p.get("starter_template_java")
    existing.starter_template_cpp = p.get("starter_template_cpp")
    existing.starter_template_javascript = p.get("starter_template_javascript")


def load_problems() -> int:
    with open(PROBLEMS_YAML, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    problems = data.get("problems", [])
    if not problems:
        return 0

    with SessionLocal() as session:
        existing_count = session.query(models.Problem).count()
        if existing_count == 0:
            # Fresh seed — insert all problems and test cases
            for p in problems:
                problem = _problem_from_dict(p)
                session.add(problem)
                for tc in p.get("test_cases", []):
                    session.add(
                        models.TestCase(
                            problem_id=p["id"],
                            input=str(tc["input"]),
                            expected_output=str(tc["expected"]),
                            case_type=tc.get("case_type", "functional"),
                            version=p.get("version", 1),
                        )
                    )
            session.commit()
        else:
            # Update existing problems; add new ones; never delete old ones
            for p in problems:
                existing = session.get(models.Problem, p["id"])
                if existing:
                    _update_problem(existing, p)
                    # Keep the database's ordinal test-case mapping aligned with
                    # the official YAML, while preserving existing test_case_ids
                    # (and therefore any stored research-result foreign keys).
                    stored_cases = (session.query(models.TestCase)
                                    .filter_by(problem_id=p["id"])
                                    .order_by(models.TestCase.test_case_id).all())
                    official_cases = p.get("test_cases", [])
                    for index, tc in enumerate(official_cases):
                        if index < len(stored_cases):
                            stored = stored_cases[index]
                            stored.input = str(tc["input"])
                            stored.expected_output = str(tc["expected"])
                            stored.case_type = tc.get("case_type", "functional")
                            stored.version = p.get("version", 1)
                        else:
                            session.add(models.TestCase(
                                problem_id=p["id"],
                                input=str(tc["input"]),
                                expected_output=str(tc["expected"]),
                                case_type=tc.get("case_type", "functional"),
                                version=p.get("version", 1),
                            ))
                else:
                    problem = _problem_from_dict(p)
                    session.add(problem)
                    for tc in p.get("test_cases", []):
                        session.add(
                            models.TestCase(
                                problem_id=p["id"],
                                input=str(tc["input"]),
                                expected_output=str(tc["expected"]),
                                case_type=tc.get("case_type", "functional"),
                                version=p.get("version", 1),
                            )
                        )
            session.commit()
    return len(problems)


if __name__ == "__main__":
    init_db()
    count = load_problems()
    print(f"Seeded {count} problems.")
