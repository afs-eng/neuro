from __future__ import annotations

from datetime import date
import math

from dateutil.relativedelta import relativedelta

from .config import WASI_COMPOSITES, WASI_SUBTESTS, classify_composite_score, classify_subtest_z_score
from .loaders import lookup_composite, lookup_t_score, lookup_weighted_score


def _to_date(value) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _normal_cdf(z_score: float) -> float:
    return 0.5 * (1 + math.erf(z_score / math.sqrt(2)))


def _age_metric(birth_date: date, applied_on: date) -> tuple[int, dict]:
    age = relativedelta(applied_on, birth_date)
    metric = (age.years * 365) + (age.months * 30) + age.days
    return metric, {"years": age.years, "months": age.months, "days": age.days}


def _subtest_result(code: str, raw_score: int, age_metric: int) -> dict:
    t_score, age_band = lookup_t_score(code, raw_score, age_metric)
    z_score = (t_score - 50) / 10
    weighted_score = lookup_weighted_score(t_score)
    percentile = _normal_cdf(z_score) * 100
    return {
        "code": WASI_SUBTESTS[code]["code"],
        "name": WASI_SUBTESTS[code]["name"],
        "raw_score": raw_score,
        "t_score": t_score,
        "z_score": round(z_score, 3),
        "weighted_score": weighted_score,
        "percentile": round(percentile, 1),
        "classification": classify_subtest_z_score(z_score),
        "age_band": age_band,
    }


def _composite_result(key: str, subtests: dict[str, dict], confidence_level: str, *, is_child: bool) -> dict:
    config = WASI_COMPOSITES[key]
    sum_t_scores = sum(subtests[subtest]["t_score"] for subtest in config["subtests"])
    composite_lookup = lookup_composite(config["table"], sum_t_scores, is_child=is_child, confidence_level=confidence_level)
    weighted_scores = [subtests[subtest]["weighted_score"] for subtest in config["subtests"]]

    interpretability_ok = True
    warning = ""
    if key == "qi_verbal":
        interpretability_ok = abs(weighted_scores[0] - weighted_scores[1]) < config["interpretability_gap"]
    elif key == "qi_execucao":
        interpretability_ok = abs(weighted_scores[0] - weighted_scores[1]) < config["interpretability_gap"]
    elif key == "qit_2":
        interpretability_ok = abs(weighted_scores[0] - weighted_scores[1]) < config["interpretability_gap"]

    if not interpretability_ok:
        warning = config["interpretability_message"]

    return {
        "code": key,
        "name": config["name"],
        "sum_t_scores": sum_t_scores,
        "scaled_sum": round((((sum_t_scores - 50) / 10) * 3) + 10, 1),
        "qi": composite_lookup["qi"],
        "percentile": composite_lookup["percentile"],
        "percentile_display": composite_lookup["percentile_display"],
        "confidence_interval": composite_lookup["confidence_interval"],
        "classification": classify_composite_score(composite_lookup["qi"]),
        "interpretability": {
            "ok": interpretability_ok,
            "warning": warning,
        },
        "subtests": [WASI_SUBTESTS[subtest]["code"] for subtest in config["subtests"]],
    }


def compute_wasi_payload(raw_scores: dict) -> dict:
    birth_date = _to_date(raw_scores["birth_date"])
    applied_on = _to_date(raw_scores["applied_on"])
    confidence_level = str(raw_scores.get("confidence_level") or "95")
    age_metric, age = _age_metric(birth_date, applied_on)

    subtests = {
        code: _subtest_result(code, int(raw_scores[code]), age_metric)
        for code in WASI_SUBTESTS
    }

    composites = {
        key: _composite_result(key, subtests, confidence_level, is_child=age["years"] < 17)
        for key in WASI_COMPOSITES
    }

    qit4_warning = ""
    qit4_ok = abs(composites["qi_verbal"]["qi"] - composites["qi_execucao"]["qi"]) < WASI_COMPOSITES["qit_4"]["interpretability_gap"]
    if not qit4_ok:
        qit4_warning = WASI_COMPOSITES["qit_4"]["interpretability_message"]
    composites["qit_4"]["interpretability"] = {"ok": qit4_ok, "warning": qit4_warning}

    weighted_average = round(sum(item["weighted_score"] for item in subtests.values()) / len(subtests), 2)
    ipsative = {}
    for code, result in subtests.items():
        difference = round(result["weighted_score"] - weighted_average, 2)
        ipsative[code] = {
            "name": result["name"],
            "weighted_score": result["weighted_score"],
            "difference_from_mean": difference,
            "trend": "Positivo" if difference >= 1 else "Negativo" if difference <= -1 else "Neutro",
        }

    return {
        "birth_date": birth_date.isoformat(),
        "applied_on": applied_on.isoformat(),
        "age": age,
        "age_metric": age_metric,
        "confidence_level": confidence_level,
        "subtests": subtests,
        "composites": composites,
        "ipsative": {
            "weighted_mean": weighted_average,
            "subtests": ipsative,
            "highest_positive": max(ipsative.items(), key=lambda item: item[1]["difference_from_mean"]),
            "highest_negative": min(ipsative.items(), key=lambda item: item[1]["difference_from_mean"]),
        },
    }
