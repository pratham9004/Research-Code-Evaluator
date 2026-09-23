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
        compared = {pid for (pid,) in session.query(models.Comparison.problem_id).filter(models.Comparison.is_pilot == 0).distinct()}
        problems_compared = len(compared)
        total_comparisons = session.query(models.Comparison).filter(models.Comparison.is_pilot == 0).count()
        pilot_comparisons = session.query(models.Comparison).filter(models.Comparison.is_pilot == 1).count()

        ai_systems = {}
        for (name,) in session.query(models.Comparison.ai_name).filter(models.Comparison.is_pilot == 0).distinct():
            cnt = session.query(models.Comparison).filter_by(ai_name=name, is_pilot=0).count()
            ai_systems[name] = cnt

        outcomes = {"AI": 0, "HUMAN": 0, "COMPARABLE": 0}
        for (direction,) in session.query(models.ComparisonResult.direction).join(models.Comparison).filter(
            models.ComparisonResult.metric == "overall", models.Comparison.is_pilot == 0
        ).all():
            key = direction if direction in outcomes else "COMPARABLE"
            outcomes[key] += 1

        metric_averages = {}
        for metric in METRIC_LABELS:
            rows = session.query(models.ComparisonResult).join(models.Comparison).filter(
                models.ComparisonResult.metric == metric, models.Comparison.is_pilot == 0).all()
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
            models.Comparison.is_pilot == 0
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

        return {
            "has_data": has_data,
            "kpis": {
                "total_problems": total_problems,
                "problems_compared": problems_compared,
                "problems_remaining": max(0, total_problems - problems_compared),
                "completion_percentage": round(problems_compared / total_problems * 100, 1) if total_problems else 0.0,
                "total_comparisons": total_comparisons,
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
        }
