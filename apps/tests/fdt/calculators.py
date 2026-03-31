import math

from .config import FDT_NORMS, FDT_PROCESS_GROUPS, FDT_STAGE_LABELS


def select_norm_by_age(age: int) -> dict:
    for group in FDT_NORMS:
        if group["idade_min"] <= age <= group["idade_max"]:
            return group
    raise ValueError("Idade fora das faixas normativas disponiveis.")


def normal_cdf(z: float) -> float:
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def percentile_from_z(z: float) -> float:
    return normal_cdf(z) * 100


def weighted_points_from_z(z: float) -> float:
    return 10 + (z * 3)


def classify_percentile(percentile: float) -> str:
    if percentile < 2:
        return "Muito Inferior"
    if percentile < 9:
        return "Inferior"
    if percentile < 25:
        return "Media Inferior"
    if percentile <= 75:
        return "Media"
    if percentile <= 91:
        return "Media Superior"
    if percentile <= 98:
        return "Superior"
    return "Muito Superior"


def percentile_range_text(percentile: float) -> str:
    if percentile < 5:
        return "< 5"
    if percentile < 25:
        return "> 5 < 25"
    if percentile < 50:
        return "> 25 < 50"
    if percentile == 50:
        return "50"
    if percentile < 75:
        return "> 50 < 75"
    if percentile < 95:
        return "> 75 < 95"
    return ">= 95"


def calculate_metric_result(
    code: str, value: float, mean: float, std_dev: float
) -> dict:
    if std_dev == 0:
        raise ValueError(f"Desvio padrao invalido para {code}.")

    z_raw = (value - mean) / std_dev
    z_score = -z_raw
    percentile = percentile_from_z(z_score)

    return {
        "codigo": code,
        "nome": FDT_STAGE_LABELS[code],
        "categoria": FDT_PROCESS_GROUPS[code],
        "valor": round(value, 2),
        "media": mean,
        "dp": std_dev,
        "z_score": round(z_score, 3),
        "pontos_ponderados": round(weighted_points_from_z(z_score), 1),
        "percentil_num": round(percentile, 1),
        "percentil_texto": percentile_range_text(round(percentile, 1)),
        "classificacao": classify_percentile(percentile),
    }


def classify_error_percentile(percentile: float) -> str:
    return "Deficitario" if percentile < 25 else "Media"


def manual_percentile_from_table(value: float, norms: dict) -> str:
    pc95 = norms["pc95"]
    pc75 = norms["pc75"]
    pc50 = norms["pc50"]
    pc25 = norms["pc25"]
    pc5 = norms["pc5"]

    if value <= pc95:
        return "95" if value == pc95 else ">= 95"
    if value < pc75:
        return "> 75 < 95"
    if value == pc75:
        return "75"
    if value < pc50:
        return "> 50 < 75"
    if value == pc50:
        return "50"
    if value < pc25:
        return "> 25 < 50"
    if value == pc25:
        return "25"
    if value < pc5:
        return "> 5 < 25"
    return "< 5"


def calculate_error_result(
    code: str, errors: int, mean: float, std_dev: float, norms: dict
) -> dict:
    z_raw = 0.0 if std_dev == 0 else (errors - mean) / std_dev
    z_score = -z_raw
    percentile = percentile_from_z(z_score)

    return {
        "categoria": FDT_PROCESS_GROUPS[code],
        "qtde_erros": errors,
        "percentil_manual": manual_percentile_from_table(errors, norms),
        "media": mean,
        "desvio_padrao": std_dev,
        "z_score": round(z_score, 3),
        "pontos_ponderados": round(weighted_points_from_z(z_score), 1),
        "percentil": round(percentile, 1),
        "classificacao_guilmette": classify_error_percentile(percentile),
    }


def calculate_stage_totals(raw_scores: dict) -> dict:
    return {
        stage: {
            "tempo": float(raw_scores[stage]["tempo"]),
            "erros": int(raw_scores[stage].get("erros", 0)),
        }
        for stage in ("leitura", "contagem", "escolha", "alternancia")
    }


def calculate_derived_scores(stage_totals: dict) -> dict:
    leitura = stage_totals["leitura"]["tempo"]
    contagem = stage_totals["contagem"]["tempo"]
    escolha = stage_totals["escolha"]["tempo"]
    alternancia = stage_totals["alternancia"]["tempo"]

    return {
        "inibicao": round(escolha - leitura, 2),
        "flexibilidade": round(alternancia - leitura, 2),
        "total_erros": sum(stage["erros"] for stage in stage_totals.values()),
    }


def calculate_fdt_results(stage_totals: dict, age: int) -> dict:
    norm_group = select_norm_by_age(age)
    time_norms = norm_group["tempos"]
    error_norms = norm_group["erros"]
    derived_scores = calculate_derived_scores(stage_totals)

    metric_values = {
        "leitura": stage_totals["leitura"]["tempo"],
        "contagem": stage_totals["contagem"]["tempo"],
        "escolha": stage_totals["escolha"]["tempo"],
        "alternancia": stage_totals["alternancia"]["tempo"],
        "inibicao": derived_scores["inibicao"],
        "flexibilidade": derived_scores["flexibilidade"],
    }

    metrics = [
        calculate_metric_result(
            code=code,
            value=value,
            mean=time_norms[code]["media"],
            std_dev=time_norms[code]["dp"],
        )
        for code, value in metric_values.items()
    ]

    error_results = {
        code: calculate_error_result(
            code=code,
            errors=stage_totals[code]["erros"],
            mean=error_norms[code]["media"],
            std_dev=error_norms[code]["dp"],
            norms=error_norms[code],
        )
        for code in ("leitura", "contagem", "escolha", "alternancia")
    }

    return {
        "faixa": norm_group["faixa"],
        "titulo": norm_group.get("titulo", ""),
        "n": norm_group.get("n", 0),
        "idade": age,
        "stage_totals": stage_totals,
        "derived_scores": derived_scores,
        "metric_results": metrics,
        "erros": error_results,
    }
