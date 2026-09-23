"""Statistical analysis across the accumulated research dataset.

Primary test: Wilcoxon Signed-Rank (docs/03 section 11). Reported only when
sufficient paired observations exist; otherwise clearly marked insufficient.
"""
from __future__ import annotations

import math

from scipy import stats

from backend.db import models


def compute_statistics(session, cfg: dict) -> dict:
    alpha = cfg["statistics"]["alpha"]
    min_obs = cfg["statistics"]["min_paired_observations"]
    metrics = ["reliability", "performance", "maintainability",
               "security", "complexity", "code_quality", "overall"]

    out = {"alpha": alpha, "per_metric": {}}
    for metric in metrics:
        rows = session.query(models.ComparisonResult).join(models.Comparison).filter(
            models.ComparisonResult.metric == metric, models.Comparison.is_pilot == 0
        ).all()
        pairs = [(r.ai_value, r.human_value) for r in rows
                 if r.ai_value is not None and r.human_value is not None]
        n = len(pairs)
        if n < min_obs:
            out["per_metric"][metric] = {
                "n_paired": n,
                "statistic": None,
                "p_value": None,
                "significant": False,
                "effect_size": None,
                "status": "insufficient_data",
            }
            continue

        ai = [p[0] for p in pairs]
        human = [p[1] for p in pairs]
        diffs = [a - h for a, h in pairs]
        if all(d == 0 for d in diffs):
            out["per_metric"][metric] = {
                "n_paired": n,
                "statistic": None,
                "p_value": None,
                "significant": False,
                "effect_size": 0.0,
                "status": "no_variation",
            }
            continue

        try:
            stat, pval = stats.wilcoxon(ai, human)
        except ValueError as e:
            out["per_metric"][metric] = {
                "n_paired": n,
                "statistic": None,
                "p_value": None,
                "significant": False,
                "effect_size": None,
                "status": f"error: {e}",
            }
            continue

        denom = n * (n + 1) / 2.0
        effect = (2.0 * stat) / denom - 1.0 if denom else 0.0
        out["per_metric"][metric] = {
            "n_paired": n,
            "statistic": round(float(stat), 4),
            "p_value": round(float(pval), 6),
            "significant": bool(pval < alpha),
            "effect_size": round(float(effect), 4),
            "status": "ok",
        }
    return out
