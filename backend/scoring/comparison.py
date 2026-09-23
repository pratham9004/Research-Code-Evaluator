"""AI-vs-Human metric comparison (docs/03 section 10, docs/04 section 13)."""
from __future__ import annotations

from backend.config import SCORING_YAML


def _load_direction(cfg, name):
    for d in cfg["overall_score"]["dimensions"]:
        if d["name"] == name:
            return d["direction"]
    return "higher_is_better"


def compute_comparison_results(ai_dims: dict, human_dims: dict, cfg: dict) -> list:
    epsilon = cfg["comparison"]["comparable_epsilon"]
    metrics = [
        ("reliability", "reliability_pass_rate"),
        ("performance", "execution_time_ms"),
        ("maintainability", "maintainability_index"),
        ("security", "security_findings_count"),
        ("complexity", "avg_cyclomatic_complexity"),
        ("code_quality", "quality_findings_count"),
    ]
    results = []
    for metric, field in metrics:
        ai = ai_dims.get(field)
        human = human_dims.get(field)
        if ai is None or human is None:
            continue
        direction = _load_direction(cfg, metric)
        results.append(_build(metric, ai, human, direction, None))

    # Overall uses epsilon-based comparability.
    ai_o = ai_dims.get("overall_score")
    human_o = human_dims.get("overall_score")
    if ai_o is not None and human_o is not None:
        results.append(_build("overall", ai_o, human_o, "higher_is_better", epsilon))
    return results


def _build(metric, ai, human, direction, epsilon):
    diff = round(ai - human, 4)
    if direction == "higher_is_better":
        ai_better = ai > human
    else:
        ai_better = ai < human

    if epsilon is not None:
        comparable = abs(diff) <= epsilon
    else:
        comparable = ai == human

    if comparable:
        direction_label = "COMPARABLE"
    else:
        direction_label = "AI" if ai_better else "HUMAN"

    pct = round(diff / abs(human) * 100, 3) if human not in (0, 0.0) else None
    return {
        "metric": metric,
        "ai_value": ai,
        "human_value": human,
        "difference": diff,
        "direction": direction_label,
        "percentage_difference": pct,
        "statistical_status": "aggregate_only",
    }
