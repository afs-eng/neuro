from typing import Dict, Any, Union


def get_faixa_etaria(idade: int) -> str:
    if 2 <= idade <= 5:
        return "2_5"
    if 6 <= idade <= 9:
        return "6_9"
    if 10 <= idade <= 13:
        return "10_13"
    if 14 <= idade <= 17:
        return "14_17"
    raise ValueError("Idade fora da faixa normativa do E-TDAH-PAIS (2 a 17 anos).")


def interpret_results(raw_scores: Dict[str, int], age: int, sex: str) -> Dict[str, Any]:
    from .config import NORMS, FACTOR_NAMES, FACTOR_ORDER
    from .calculators import (
        manual_percentile_from_raw,
        classificar_percentil,
        classify_guilmette,
        percentile_guilmette,
        points_scaled,
    )

    faixa = get_faixa_etaria(age)
    sex_key = "feminino" if sex.upper() == "F" else "masculino"
    norms = NORMS[sex_key][faixa]

    results = {}
    metric_keys = ["fator_1", "fator_2", "fator_3", "fator_4", "escore_geral"]

    for metric_key in metric_keys:
        raw_score = raw_scores.get(metric_key, 0)

        pct_manual_num, pct_manual_text = manual_percentile_from_raw(
            raw_score, norms["scores"][metric_key]
        )
        class_manual = classificar_percentil(pct_manual_num)

        mean = norms["stats"][metric_key]["media"]
        std = norms["stats"][metric_key]["dp"]
        z = 0.0 if std == 0 else (raw_score - mean) / std
        pp = points_scaled(z)
        pct_g = percentile_guilmette(z)
        class_g = classify_guilmette(pct_g)

        results[metric_key] = {
            "name": FACTOR_NAMES.get(metric_key, metric_key),
            "raw_score": raw_score,
            "mean": mean,
            "std": std,
            "z_score": z,
            "points_scaled": pp,
            "percentile_text": pct_manual_text,
            "percentile_guilmette": pct_g,
            "classification": class_manual,
            "classification_guilmette": class_g,
        }

    return results


def generate_report(raw_scores: Dict[str, int], age: int, sex: str) -> str:
    results = interpret_results(raw_scores, age, sex)

    faixa = get_faixa_etaria(age)
    sex_labels = {"feminino": "Feminino", "masculino": "Masculino"}
    sex_key = "feminino" if sex.upper() == "F" else "masculino"

    lines = []
    lines.append("=" * 132)
    lines.append(
        "ETDAH-PAIS - ESCALA DE TRANSTORNO DE DÉFICIT DE ATENÇÃO E HIPERATIVIDADE - VERSÃO PARA PAIS"
    )
    lines.append("=" * 132)
    lines.append("")
    lines.append(f"Sexo: {sex_labels.get(sex_key, 'Não informado')}")
    lines.append(f"Faixa etária: {faixa.replace('_', ' a ')} anos")
    lines.append("")

    metric_keys = ["fator_1", "fator_2", "fator_3", "fator_4", "escore_geral"]

    for metric_key in metric_keys:
        r = results[metric_key]
        lines.append(f"▸ {r['name']}")
        lines.append(f"  Pontos Brutos: {r['raw_score']}")
        lines.append(f"  Percentil (Manual): {r['percentile_text']}")
        lines.append(f"  Classificação (Manual): {r['classification']}")
        lines.append(f"  Média: {r['mean']:.2f}")
        lines.append(f"  Dp: {r['std']:.2f}")
        lines.append(f"  Z-Score: {r['z_score']:.3f}")
        lines.append(f"  Pontos Ponderados: {r['points_scaled']:.1f}")
        lines.append(f"  Percentil (Guilmette): {r['percentile_guilmette']:.1f}")
        lines.append(f"  Classificação (Guilmette): {r['classification_guilmette']}")
        lines.append("")

    lines.append("=" * 132)

    return "\n".join(lines)
