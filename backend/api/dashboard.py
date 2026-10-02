"""Dashboard aggregation API (computed from stored research records)."""
from __future__ import annotations

from fastapi import APIRouter

from backend.db import models
from backend.db.session import SessionLocal

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

METRIC_LABELS = {
    "reliability": "Reliability (%)",
    "performance": "Execution Time (ms)",
    "maintainability": "Maintainability",
    "security": "Security Findings",
    "complexity": "Cyclomatic Complexity",
    "code_quality": "Quality Findings",
}


@router.get("")
def dashboard():
    with SessionLocal() as session:
        total_problems = session.query(models.Problem).count()
        valid_research = session.query(models.Comparison).filter(
            models.Comparison.is_pilot == 0,
            models.Comparison.status == "completed",
        ).join(models.ComparisonResult, models.ComparisonResult.comparison_id == models.Comparison.comparison_id).filter(
            models.ComparisonResult.metric == "overall",
            models.ComparisonResult.ai_value.is_not(None),
            models.ComparisonResult.human_value.is_not(None),
        )
        compared = {pid for (pid,) in valid_research.with_entities(models.Comparison.problem_id).distinct()}
        problems_compared = len(compared)
        total_comparisons = valid_research.count()
        research_record_count = session.query(models.Comparison).filter(models.Comparison.is_pilot == 0).count()
        raw_execution_count = session.query(models.Comparison).filter(
            models.Comparison.is_pilot == 0, models.Comparison.status == "execution_only"
        ).count()
        incomplete_comparisons = max(0, research_record_count - total_comparisons - raw_execution_count)
        pilot_comparisons = session.query(models.Comparison).filter(models.Comparison.is_pilot == 1).count()

        ai_systems = {}
        for (name,) in valid_research.with_entities(models.Comparison.ai_name).distinct():
            cnt = valid_research.filter(models.Comparison.ai_name == name).count()
            ai_systems[name] = cnt

        outcomes = {"AI": 0, "HUMAN": 0, "COMPARABLE": 0}
        for (direction,) in session.query(models.ComparisonResult.direction).join(models.Comparison).filter(
            models.ComparisonResult.metric == "overall", models.Comparison.is_pilot == 0,
            models.Comparison.status == "completed", models.ComparisonResult.direction.is_not(None)
        ).all():
            if direction in outcomes:
                outcomes[direction] += 1

        metric_averages = {}
        for metric in METRIC_LABELS:
            rows = session.query(models.ComparisonResult).join(models.Comparison).filter(
                models.ComparisonResult.metric == metric, models.Comparison.is_pilot == 0,
                models.Comparison.status == "completed").all()
            ai_vals = [r.ai_value for r in rows if r.ai_value is not None]
            hu_vals = [r.human_value for r in rows if r.human_value is not None]
            metric_averages[metric] = {
                "label": METRIC_LABELS[metric],
                "ai": round(sum(ai_vals) / len(ai_vals), 3) if ai_vals else None,
                "human": round(sum(hu_vals) / len(hu_vals), 3) if hu_vals else None,
            }

        has_data = total_comparisons > 0

        # Recent research comparisons (last 5)
        recent = session.query(models.Comparison).filter(
            models.Comparison.is_pilot == 0, models.Comparison.status == "completed"
        ).order_by(models.Comparison.comparison_id.desc()).limit(5).all()
        recent_list = []
        for c in recent:
            problem = session.get(models.Problem, c.problem_id)
            overall = session.query(models.ComparisonResult).filter_by(
                comparison_id=c.comparison_id, metric="overall").first()
            recent_list.append({
                "comparison_id": c.comparison_id,
                "problem_title": problem.title if problem else c.problem_id,
                "language": c.language,
                "ai_name": c.ai_name,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "overall_winner": overall.direction if overall else "N/A",
                "ai_overall": overall.ai_value if overall else None,
                "human_overall": overall.human_value if overall else None,
            })

        # Execution-facing view for the dedicated ChatGPT/Human Python collection.
        python_comparisons = session.query(models.Comparison).filter(
            models.Comparison.language == "python",
            models.Comparison.ai_name == "ChatGPT",
            models.Comparison.is_pilot == 0,
        ).order_by(models.Comparison.comparison_id.desc()).all()
        by_problem = {}
        for comparison in python_comparisons:
            by_problem.setdefault(comparison.problem_id, comparison)
        python_results = []
        for problem in session.query(models.Problem).order_by(models.Problem.problem_id).all():
            comparison = by_problem.get(problem.problem_id)
            # Problem definitions alone are not execution results.
            if comparison is None:
                continue
            variants = {}
            for variant in ("AI", "HUMAN"):
                execution = session.query(models.ExecutionResult).filter_by(
                    comparison_id=comparison.comparison_id, code_variant=variant
                ).first()
                variants[variant.lower()] = {
                    "status": execution.execution_status if execution else "MISSING",
                    "total": execution.total_test_cases if execution else 0,
                    "passed": execution.passed_count if execution else 0,
                    "failed": execution.failed_count if execution else 0,
                    "errors": execution.error_count if execution else 0,
                    "timeouts": execution.timeout_count if execution else 0,
                    "execution_time_ms": execution.execution_time_ms if execution else None,
                    "error_message": execution.stderr if execution and execution.execution_status in {"ERROR", "TIMEOUT"} else None,
                }
            python_results.append({
                "problem_id": problem.problem_id,
                "problem_name": problem.title,
                "comparison_id": comparison.comparison_id,
                "ai": variants["ai"],
                "human": variants["human"],
            })

        return {
            "has_data": has_data,
            "kpis": {
                "total_problems": total_problems,
                "problems_compared": problems_compared,
                "problems_remaining": max(0, total_problems - problems_compared),
                "completion_percentage": round(problems_compared / total_problems * 100, 1) if total_problems else 0.0,
                "total_comparisons": total_comparisons,
                "raw_execution_datasets": raw_execution_count,
                "incomplete_comparisons": incomplete_comparisons,
                "pilot_comparisons": pilot_comparisons,
                "ai_systems_count": len(ai_systems),
            },
            "ai_systems": ai_systems,
            "outcomes": {
                "ai_better": outcomes["AI"],
                "human_better": outcomes["HUMAN"],
                "comparable": outcomes["COMPARABLE"],
            },
            "metric_averages": metric_averages,
            "recent_comparisons": recent_list,
            "python_benchmark_results": python_results,
        }
