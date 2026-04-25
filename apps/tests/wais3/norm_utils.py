from __future__ import annotations

from .constants import WAIS3_AGE_RANGES


def resolve_age_range(anos: int, meses: int = 0) -> str:
    for item in WAIS3_AGE_RANGES:
        if item["min_years"] <= anos <= item["max_years"]:
            return item["key"]
    raise ValueError("Idade fora da faixa normativa do WAIS-III (16 a 89 anos).")


def raw_score_matches_interval(raw_score: int, interval: str) -> bool:
    if interval is None:
        return False
    text = str(interval).strip().replace("–", "-").replace("—", "-")
    if not text or text.lower() == "nan" or text in {"-", "—"}:
        return False
    if "-" in text:
        start, end = text.split("-", 1)
        return int(start.strip()) <= raw_score <= int(end.strip())
    return raw_score == int(text)


def normalize_csv_value(value: str | None):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        numeric = float(text.replace(",", "."))
    except ValueError:
        return text
    return int(numeric) if numeric.is_integer() else numeric


def has_meaningful_value(value: str | None) -> bool:
    normalized = normalize_csv_value(value)
    return normalized not in (None, "")
