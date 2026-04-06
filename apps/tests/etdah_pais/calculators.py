import math
from typing import Dict, Tuple, Any, List


def inverter_pontuacao(valor: int) -> int:
    return 7 - valor


def calculate_raw_scores(responses: Dict[int, int]) -> Dict[str, int]:
    from .config import FACTOR_ITEMS, REVERSE_FACTORS, REVERSE_ITEMS

    raw_scores = {}
    for factor, items in FACTOR_ITEMS.items():
        total = 0
        for item in items:
            value = responses.get(item, 0)
            is_reversed = factor in REVERSE_FACTORS or (
                factor in REVERSE_ITEMS and item in REVERSE_ITEMS[factor]
            )
            if is_reversed:
                value = inverter_pontuacao(value)
            total += value
        raw_scores[factor] = total

    raw_scores["escore_geral"] = sum(raw_scores.get(f, 0) for f in FACTOR_ITEMS.keys())
    return raw_scores


def classificar_percentil(percentil: float) -> str:
    if percentil < 25:
        return "Inferior"
    if percentil < 45:
        return "Média Inferior"
    if percentil < 65:
        return "Média"
    if percentil < 85:
        return "Média Superior"
    return "Superior"


def classify_guilmette(percentile: float) -> str:
    if percentile < 2:
        return "Deficitário"
    if percentile < 9:
        return "Inferior"
    if percentile < 25:
        return "Média Inferior"
    if percentile < 75:
        return "Média"
    if percentile < 91:
        return "Média Superior"
    if percentile < 98:
        return "Superior"
    return "Muito Superior"


def manual_percentile_from_raw(
    raw_score: float, percentile_score_pairs: List[Tuple[int, float]]
) -> Tuple[float, str]:
    pairs = sorted(percentile_score_pairs, key=lambda x: x[1])

    if raw_score < pairs[0][1]:
        return float(pairs[0][0]), f"< {pairs[0][0]}"

    if raw_score > pairs[-1][1]:
        last_p = pairs[-1][0]
        if last_p >= 99:
            return 99.0, "> 99"
        return float(last_p), f"> {last_p}"

    for p, s in pairs:
        if abs(raw_score - s) < 1e-9:
            return float(p), str(p)

    for idx in range(len(pairs) - 1):
        p1, s1 = pairs[idx]
        p2, s2 = pairs[idx + 1]
        if s1 <= raw_score <= s2:
            if s2 == s1:
                p_est = float(p1)
            else:
                ratio = (raw_score - s1) / (s2 - s1)
                p_est = p1 + ratio * (p2 - p1)
            
            # Formata para uma casa decimal, mas remove se for .0
            p_str = f"{p_est:.1f}".rstrip('0').rstrip('.')
            return p_est, p_str

    return float(pairs[-1][0]), str(pairs[-1][0])


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def percentile_guilmette(z: float) -> float:
    return normal_cdf(z) * 100


def points_scaled(z: float) -> float:
    return 10 + (3 * z)
