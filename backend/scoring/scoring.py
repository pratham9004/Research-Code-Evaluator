"""Scoring engine (source of truth: docs/03_METRICS_AND_SCORING.md).

- Maintainability composite = weighted sum of four inverted (0-100) components.
- Per-dimension normalization for the overall score uses the research
  dataset min/max (docs/03 section 8), with safe divide-by-zero handling.
"""
from __future__ import annotations

import yaml

from backend.config import SCORING_YAML
from backend.db import models


def load_config() -> dict:
    with open(SCORING_YAML, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _clamp(v: float, lo=0.0, hi=100.0) -> float:
    return max(lo, min(hi, v))


def maintainability_index(raw_metrics: dict, cfg: dict) -> float:
    mcfg = cfg["maintainability"]
    weights = mcfg["weights"]
    ref = mcfg["reference"]
    mapping = {
        "cyclomatic": "cyclomatic_avg",
        "function_length": "function_length_avg",
        "nesting": "nesting_depth_avg",
        "coupling": "coupling",
    }
    components = {}
    for key, field in mapping.items():
        x = float(raw_metrics.get(field, 0.0))
        r = ref[key]
        lo, hi = float(r["min"]), float(r["max"])
        if hi == lo:
            comp = 100.0 if x <= lo else 0.0
        else:
            comp = (hi - x) / (hi - lo) * 100.0
        components[key] = _clamp(comp)
    index = (
        weights["cyclomatic"] * components["cyclomatic"]
        + weights["function_length"] * components["function_length"]
        + weights["nesting"] * components["nesting"]
        + weights["coupling"] * components["coupling"]
    )
    return round(index, 3)


def _normalize_dataset(raw: float, population: list, direction: str, neutral: float) -> dict:
    values = [v for v in population if v is not None]
    if not values:
        return {
            "value": neutral,
            "population_min": None,
            "population_max": None,
            "population_n": 0,
        }
    lo, hi = min(values), max(values)
    if hi == lo:
        result = neutral
    elif direction == "higher_is_better":
        result = _clamp((raw - lo) / (hi - lo) * 100.0)
    else:
        result = _clamp((hi - raw) / (hi - lo) * 100.0)
    return {
        "value": result,
        "population_min": lo,
        "population_max": hi,
        "population_n": len(values),
    }


def compute_scores(session, ai_dims: dict, human_dims: dict, cfg: dict):
    dims = cfg["overall_score"]["dimensions"]
    neutral = cfg["normalization"]["neutral_value"]
    ai_scores, human_scores = [], []

    for d in dims:
        name = d["name"]
        field = d["raw_field"]
        direction = d["direction"]
        weight = d["weight"]
        ai_raw = ai_dims.get(field)
        human_raw = human_dims.get(field)

        population = [r[0] for r in session.query(models.Score.raw_value)
                      .filter(models.Score.dimension == name).all()]
        population += [ai_raw, human_raw]

        ai_norm = _normalize_dataset(ai_raw, population, direction, neutral) if ai_raw is not None else {"value": None, "population_min": None, "population_max": None, "population_n": 0}
        human_norm = _normalize_dataset(human_raw, population, direction, neutral) if human_raw is not None else {"value": None, "population_min": None, "population_max": None, "population_n": 0}

        ai_scores.append(_score_row(name, ai_raw, ai_norm, weight))
        human_scores.append(_score_row(name, human_raw, human_norm, weight))

    ai_overall = round(sum(s["weighted_value"] for s in ai_scores if s["weighted_value"] is not None), 3)
    human_overall = round(sum(s["weighted_value"] for s in human_scores if s["weighted_value"] is not None), 3)
    return ai_scores, human_scores, ai_overall, human_overall


def _score_row(dimension, raw, normalized, weight):
    norm_val = normalized.get("value") if isinstance(normalized, dict) else normalized
    pop_min = normalized.get("population_min") if isinstance(normalized, dict) else None
    pop_max = normalized.get("population_max") if isinstance(normalized, dict) else None
    pop_n = normalized.get("population_n") if isinstance(normalized, dict) else None
    weighted = round(norm_val * weight, 4) if norm_val is not None else None
    return {
        "dimension": dimension,
        "raw_value": raw,
        "normalized_value": round(norm_val, 4) if norm_val is not None else None,
        "weighted_value": weighted,
        "dimension_score": round(norm_val, 4) if norm_val is not None else None,
        "normalization_population_min": pop_min,
        "normalization_population_max": pop_max,
        "normalization_population_n": pop_n,
    }
