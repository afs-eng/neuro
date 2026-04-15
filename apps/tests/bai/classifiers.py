from __future__ import annotations

from .constants import RAW_SCORE_BANDS, T_SCORE_BANDS


class BAIClassifier:
    @staticmethod
    def classify_raw_score(raw_score: int) -> dict:
        """Classifica o escore bruto do BAI conforme faixas normativas."""
        for band in RAW_SCORE_BANDS:
            if band["min"] <= raw_score <= band["max"]:
                return band
        return RAW_SCORE_BANDS[-1]

    @staticmethod
    def classify_t_score(t_score: float | None) -> dict | None:
        """Classifica o escore T do BAI conforme faixas normativas."""
        if t_score is None:
            return None
        for band in T_SCORE_BANDS:
            if band["min"] <= t_score <= band["max"]:
                return band
        if t_score < T_SCORE_BANDS[0]["min"]:
            return T_SCORE_BANDS[0]
        return T_SCORE_BANDS[-1]
