"""Problem bank API."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.db import models
from backend.db.session import SessionLocal

router = APIRouter(prefix="/api/problems", tags=["problems"])


@router.get("")
def list_problems():
    with SessionLocal() as session:
        problems = session.query(models.Problem).order_by(models.Problem.problem_id).all()
        compared = {pid for (pid,) in session.query(models.Comparison.problem_id).distinct()}
        out = []
        for p in problems:
            out.append({
                "problem_id": p.problem_id,
                "title": p.title,
                "description": p.description,
                "category": p.category,
                "difficulty": p.difficulty,
                "supported_languages": p.supported_languages,
                "signature_python": p.signature_python,
                "signature_java": p.signature_java,
                "signature_cpp": p.signature_cpp,
                "signature_javascript": p.signature_javascript,
                "entry_function": p.entry_function,
                "compared": p.problem_id in compared,
                "test_case_count": session.query(models.TestCase).filter_by(problem_id=p.problem_id).count(),
                "version": p.version,
                "input_spec": p.input_spec,
                "output_spec": p.output_spec,
                "constraints": p.constraints,
                "starter_template": p.starter_template,
                "active": p.active,
                "research_focus": p.research_focus,
                "security_relevance": p.security_relevance,
                "harness_type": getattr(p, "harness_type", "legacy") or "legacy",
                "starter_template_python": getattr(p, "starter_template_python", None),
                "starter_template_java": getattr(p, "starter_template_java", None),
                "starter_template_cpp": getattr(p, "starter_template_cpp", None),
                "starter_template_javascript": getattr(p, "starter_template_javascript", None),
            })
        return out


@router.get("/{problem_id}")
def get_problem(problem_id: str):
    with SessionLocal() as session:
        p = session.get(models.Problem, problem_id)
        if not p:
            raise HTTPException(status_code=404, detail="Problem not found.")
        # Expected outputs are exposed on the Solve Problem page so the
        # researcher can see the controlled test cases before submitting.
        test_cases = session.query(models.TestCase).filter_by(problem_id=p.problem_id).order_by(models.TestCase.test_case_id).all()
        return {
            "problem_id": p.problem_id,
            "title": p.title,
            "description": p.description,
            "category": p.category,
            "difficulty": p.difficulty,
            "supported_languages": p.supported_languages,
            "signature_python": p.signature_python,
            "signature_java": p.signature_java,
            "signature_cpp": p.signature_cpp,
            "signature_javascript": p.signature_javascript,
            "entry_function": p.entry_function,
            "test_case_count": len(test_cases),
            "version": p.version,
            "input_spec": p.input_spec,
            "output_spec": p.output_spec,
            "constraints": p.constraints,
            "starter_template": p.starter_template,
            "active": p.active,
            "research_focus": p.research_focus,
            "security_relevance": p.security_relevance,
            "harness_type": getattr(p, "harness_type", "legacy") or "legacy",
            "starter_template_python": getattr(p, "starter_template_python", None),
            "starter_template_java": getattr(p, "starter_template_java", None),
            "starter_template_cpp": getattr(p, "starter_template_cpp", None),
            "starter_template_javascript": getattr(p, "starter_template_javascript", None),
            "test_cases": [
                {"test_case_id": tc.test_case_id, "input": tc.input,
                 "expected_output": tc.expected_output, "case_type": tc.case_type}
                for tc in test_cases
            ],
        }
