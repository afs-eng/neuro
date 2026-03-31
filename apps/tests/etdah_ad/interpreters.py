from typing import Dict, Any, Union
from .config import FACTOR_NAMES, NORMS, MEANS, FACTOR_ORDER
from .calculators import formatar_percentil_e_classificacao


def get_schooling_level(schooling: Union[int, str]) -> str:
    if isinstance(schooling, str):
        if schooling in ("preschool", "elementary"):
            return "fundamental"
        elif schooling in ("middle",):
            return "medio"
        elif schooling in ("higher", "higher_incomplete"):
            return "superior"
    if isinstance(schooling, (int, float)):
        if schooling <= 9:
            return "fundamental"
        elif schooling <= 12:
            return "medio"
        return "superior"
    return "fundamental"


def interpret_results(
    raw_scores: Dict[str, int], schooling: Union[int, str]
) -> Dict[str, Any]:
    schooling_level = get_schooling_level(schooling)

    results = {}
    for factor in FACTOR_ORDER:
        score = raw_scores.get(factor, 0)
        mean = MEANS[schooling_level][factor]
        percentil_txt, classificacao = formatar_percentil_e_classificacao(
            score, NORMS[schooling_level][factor]
        )

        results[factor] = {
            "name": FACTOR_NAMES[factor],
            "raw_score": score,
            "mean": mean,
            "percentile_text": percentil_txt,
            "classification": classificacao,
        }

    return results


def generate_report(raw_scores: Dict[str, int], schooling: int) -> str:
    results = interpret_results(raw_scores, schooling)

    schooling_labels = {
        "fundamental": "Ensino Fundamental",
        "medio": "Ensino Médio",
        "superior": "Ensino Superior",
    }
    schooling_level = get_schooling_level(schooling)

    lines = []
    lines.append("=" * 80)
    lines.append(
        "ETDAH-AD - ESCALA DE TRANSTORNO DE DÉFICIT DE ATENÇÃO E HIPERATIVIDADE"
    )
    lines.append("=" * 80)
    lines.append("")
    lines.append(
        f"Escolaridade: {schooling_labels.get(schooling_level, 'Não informada')} ({schooling} anos)"
    )
    lines.append("")

    for factor in FACTOR_ORDER:
        r = results[factor]
        lines.append(f"▸ {r['name']}")
        lines.append(f"  Escore Bruto: {r['raw_score']}")
        lines.append(f"  Média: {r['mean']:.2f}")
        lines.append(f"  Percentil: {r['percentile_text']}")
        lines.append(f"  Classificação: {r['classification']}")
        lines.append("")

    lines.append("=" * 80)

    return "\n".join(lines)
