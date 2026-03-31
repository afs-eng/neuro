from typing import Dict, Tuple
from .config import FACTOR_ITEMS, REVERSE_FACTORS


def inverter_pontuacao(valor: int) -> int:
    return 5 - valor


def calculate_raw_scores(responses: Dict[int, int]) -> Dict[str, int]:
    raw_scores = {}
    for factor, items in FACTOR_ITEMS.items():
        total = 0
        for item in items:
            value = responses.get(item, 0)
            if factor in REVERSE_FACTORS:
                value = inverter_pontuacao(value)
            total += value
        raw_scores[factor] = total
    return raw_scores


def classificar_percentil(percentil: int) -> str:
    if percentil <= 20:
        return "Inferior"
    elif percentil <= 40:
        return "Média Inferior"
    elif percentil <= 60:
        return "Média"
    elif percentil <= 80:
        return "Média Superior"
    return "Superior"


def formatar_percentil_e_classificacao(
    score: int, anchors: Dict[int, int]
) -> Tuple[str, str]:
    ordenado = sorted((raw, pct) for pct, raw in anchors.items())

    for raw, pct in ordenado:
        if score == raw:
            return str(pct), classificar_percentil(pct)

    menor_raw, menor_pct = ordenado[0]
    if score < menor_raw:
        return f"< {menor_pct}", "Inferior"

    for i in range(len(ordenado) - 1):
        raw1, pct1 = ordenado[i]
        raw2, pct2 = ordenado[i + 1]
        if raw1 < score < raw2:
            return f"> {pct1} e < {pct2}", classificar_percentil(pct1)

    maior_raw, maior_pct = ordenado[-1]
    if score > maior_raw:
        if maior_pct < 99:
            return f"> {maior_pct} e < 99", "Superior"
        return "> 99", "Superior"

    return "Não encontrado", "Não classificado"
