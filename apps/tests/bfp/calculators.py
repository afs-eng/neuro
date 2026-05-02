from __future__ import annotations

import math

from .config import (
    BFP_CLASSIFICATION_MEANING,
    FACTOR_DEFINITIONS,
    FACET_DEFINITIONS,
    NORMS,
    RESPONSE_OPTIONS,
    SAMPLE_LABELS,
)


CLASSIFICATION_ORDER = [
    "Muito Baixo",
    "Baixo",
    "Média Inferior",
    "Média",
    "Média Superior",
    "Superior",
    "Muito Superior",
]


def normalize_sample(sample: str | None) -> str:
    value = (sample or "geral").strip().lower()
    aliases = {
        "geral": "geral",
        "general": "geral",
        "masculino": "masculino",
        "masc": "masculino",
        "m": "masculino",
        "feminino": "feminino",
        "fem": "feminino",
        "f": "feminino",
    }
    return aliases.get(value, value)


def response_value(raw_scores: dict, item: int) -> int | None:
    responses = raw_scores.get("responses") if isinstance(raw_scores.get("responses"), dict) else None
    keys = [
        str(item),
        f"{item:02d}",
        f"{item:03d}",
        f"item_{item}",
        f"item_{item:02d}",
        f"item_{item:03d}",
    ]
    for source in (responses, raw_scores):
        if not isinstance(source, dict):
            continue
        for key in keys:
            if key in source:
                return int(source[key])
    return None


def extract_bfp_responses(raw_scores: dict) -> dict[int, int]:
    return {
        item: response_value(raw_scores, item)
        for item in range(1, 127)
        if response_value(raw_scores, item) is not None
    }


def invert_score(score: int) -> int:
    return 8 - score


def normal_cdf(z_score: float) -> float:
    return 0.5 * (1 + math.erf(z_score / math.sqrt(2)))


def percentile_from_z(z_score: float) -> float:
    return normal_cdf(z_score) * 100


def weighted_score_from_z(z_score: float) -> float:
    return 10 + (z_score * 3)


def classify_percentile(percentile: float) -> str:
    if percentile >= 97.5:
        return "Muito Superior"
    if percentile >= 85:
        return "Superior"
    if percentile >= 70:
        return "Média Superior"
    if percentile >= 30:
        return "Média"
    if percentile >= 15:
        return "Média Inferior"
    if percentile >= 2.5:
        return "Baixo"
    return "Muito Baixo"


def classify_bfp_domain(classification: str) -> str:
    if classification in {"Média Superior", "Superior", "Muito Superior"}:
        return "elevado"
    if classification in {"Média Inferior", "Baixo", "Muito Baixo"}:
        return "reduzido"
    return "medio"


def _build_scale_result(code: str, name: str, raw_score: float, sample: str) -> dict:
    norm = NORMS[sample][code]
    z_score = (raw_score - norm["mean"]) / norm["sd"]
    percentile = percentile_from_z(z_score)
    classification = classify_percentile(percentile)
    return {
        "code": code,
        "name": name,
        "raw_score": round(raw_score, 4),
        "mean": norm["mean"],
        "sd": norm["sd"],
        "z_score": round(z_score, 4),
        "weighted_score": round(weighted_score_from_z(z_score), 2),
        "percentile": round(percentile, 1),
        "classification": classification,
        "classification_meaning": BFP_CLASSIFICATION_MEANING[classification],
        "domain_level": classify_bfp_domain(classification),
    }


def compute_bfp_scores(raw_scores: dict) -> dict:
    sample = normalize_sample(
        raw_scores.get("sample") or raw_scores.get("amostra") or raw_scores.get("norm_group")
    )
    responses = extract_bfp_responses(raw_scores)

    facets = {}
    for code, definition in FACET_DEFINITIONS.items():
        values = []
        for item in definition["items"]:
            score = responses[item]
            if item in definition["reversed"]:
                score = invert_score(score)
            values.append(score)
        raw_score = sum(values) / len(values)
        facets[code] = {
            **_build_scale_result(code, definition["name"], raw_score, sample),
            "factor_code": definition["factor"],
            "item_count": len(definition["items"]),
            "reversed_items": definition["reversed"],
        }

    factors = {}
    for code, definition in FACTOR_DEFINITIONS.items():
        facet_scores = [facets[facet_code]["raw_score"] for facet_code in definition["facets"]]
        raw_score = sum(facet_scores) / len(facet_scores)
        factors[code] = {
            **_build_scale_result(code, definition["name"], raw_score, sample),
            "facet_codes": definition["facets"],
        }

    return {
        "sample": sample,
        "sample_label": SAMPLE_LABELS[sample],
        "response_scale": RESPONSE_OPTIONS,
        "responses": {str(item): score for item, score in sorted(responses.items())},
        "factors": factors,
        "facets": facets,
        "factor_order": list(FACTOR_DEFINITIONS.keys()),
        "facet_order": list(FACET_DEFINITIONS.keys()),
    }
