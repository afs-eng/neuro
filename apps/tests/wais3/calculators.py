from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any

from .constants import (
    WAIS3_ALL_SUBTESTS,
    WAIS3_INDEXES,
    WAIS3_NAME,
    WAIS3_SUBTEST_ORDER,
    classify_composite_score,
    classify_scaled_score,
)
from .loaders import WAIS3NormLoader
from .norm_utils import resolve_age_range


# ------------------------------------------------------------------
# Análise complementar (Tabelas B.1 a B.7)
# ------------------------------------------------------------------

def _load_b1(loader: WAIS3NormLoader) -> dict[str, Any]:
    """Carrega Tabela B.1: valores críticos para discrepâncias entre índices."""
    rows = loader.get_supplementary_tables().get("b1") or []
    if not rows:
        return {}
    result = {}
    for row in rows:
        age = str(row.get("col_0") or "").strip()
        if not age or not age[0].isdigit():
            continue
        nivel = str(row.get("col_1") or "").strip()
        result[f"{age}_{nivel}"] = {
            "age": age,
            "nivel": nivel,
            "qiv_qie": _norm_float(row.get("col_2")),
            "icv_iop": _norm_float(row.get("col_3")),
            "icv_imo": _norm_float(row.get("col_4")),
            "iop_ivp": _norm_float(row.get("col_5")),
            "icv_ivp": _norm_float(row.get("col_6")),
            "iop_imo": _norm_float(row.get("col_7")),
            "imo_ivp": _norm_float(row.get("col_8")),
        }
    return result


def _load_b3(loader: WAIS3NormLoader) -> dict[str, Any]:
    """Carrega Tabela B.3: diferenças entre subteste e média."""
    rows = loader.get_supplementary_tables().get("b3") or []
    if not rows:
        return {}
    result = {}
    for row in rows:
        subtest = str(row.get("col_0") or "").strip()
        if not subtest or subtest in ("Subtestes", "", "Tabela"):
            continue
        result[subtest.lower()] = {
            "verbal_n15": _norm_float(row.get("col_1")),
            "verbal_n05": _norm_float(row.get("col_2")),
            "exec_n15": _norm_float(row.get("col_9")),
            "exec_n05": _norm_float(row.get("col_10")),
        }
    return result


def _load_b6(loader: WAIS3NormLoader) -> dict[str, Any]:
    """Carrega Tabela B.6: Dígitos Ordem Direta e Inversa."""
    rows = loader.get_supplementary_tables().get("b6") or []
    if not rows:
        return {}
    result = {}
    for row in rows:
        maximo = str(row.get("col_0") or "").strip()
        if not maximo or not maximo.isdigit():
            continue
        result[int(maximo)] = {
            "direta": {age: _norm_float(row.get(f"col_{i}")) for i, age in enumerate([16, 18, 20, 30, 40, 50, 60, 65, "todas"], start=1)},
            "inversa": {age: _norm_float(row.get(f"col_{i}")) for i, age in enumerate([16, 18, 20, 30, 40, 50, 60, 65, "todas"], start=2)},
        }
    return result


def _norm_float(val: Any) -> float | None:
    """Converte string '2,4' → 2.4 ou None."""
    if val is None:
        return None
    s = str(val).strip().replace(",", ".")
    if s in ("", "–", "-", "nan", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _map_faixa_b(faixa: str) -> str:
    """Mapeia 'idade_30-39' → chave B.1 '30-39'."""
    return faixa.replace("idade_", "")


def _map_faixa_b6(faixa: str) -> int:
    """Mapeia faixa etaria para coluna B.6: retorna índice da coluna."""
    mapping = {
        "idade_16-17": 1,
        "idade_18-19": 3,
        "idade_20-29": 5,
        "idade_30-39": 7,
        "idade_40-49": 9,
        "idade_50-59": 11,
        "idade_60-64": 13,
        "idade_65-89": 15,
    }
    return mapping.get(faixa, 7)  # default 30-39


def _b6_columns_for_age(age_range_key: str) -> tuple[str, str]:
    mapping = {
        "idade_16-17": ("col_1", "col_2"),
        "idade_18-19": ("col_3", "col_4"),
        "idade_20-29": ("col_5", "col_6"),
        "idade_30-39": ("col_7", "col_8"),
        "idade_40-49": ("col_9", "col_10"),
        "idade_50-59": ("col_11", "col_12"),
        "idade_60-64": ("col_13", "col_14"),
        "idade_65-89": ("col_15", "col_16"),
    }
    return mapping.get(age_range_key, ("col_7", "col_8"))


def _b7_column_for_age(age_range_key: str) -> str:
    mapping = {
        "idade_16-17": "col_1",
        "idade_18-19": "col_2",
        "idade_20-29": "col_3",
        "idade_30-39": "col_4",
        "idade_40-49": "col_5",
        "idade_50-59": "col_6",
        "idade_60-64": "col_7",
        "idade_65-89": "col_8",
    }
    return mapping.get(age_range_key, "col_4")


def _lookup_percentile_from_csv_rows(rows: list[dict[str, str]], raw_value: int, value_column: str) -> float | None:
    for row in rows:
        key = str(row.get("col_0") or "").strip()
        if not key or key in {"Média", "DP", "Mediana"}:
            continue
        try:
            row_value = int(float(key))
        except ValueError:
            continue
        if row_value == raw_value:
            return _norm_float(row.get(value_column))
    return None


def _row_value(rows: list[dict[str, str]], row_key: str, value_column: str) -> float | None:
    for row in rows:
        key = str(row.get("col_0") or "").strip()
        if key == row_key:
            return _norm_float(row.get(value_column))
    return None


def _build_process_result(raw_value: int, mean: float | None, sd: float | None, percentile: float | None, *, reverse_z: bool = False) -> dict:
    z_score = None
    if mean is not None and sd not in (None, 0):
        z_score = ((mean - raw_value) / sd) if reverse_z else ((raw_value - mean) / sd)

    return {
        "raw_score": raw_value,
        "cumulative_frequency": percentile,
        "mean": mean,
        "sd": sd,
        "z_score": round(z_score, 3) if z_score is not None else None,
        "scaled_score": round((z_score * 3) + 10, 1) if z_score is not None else None,
        "percentile": round(_xlfn_norm_s_dist(z_score) * 100, 1) if z_score is not None else None,
        "classification": _classify_z_score(z_score),
    }


def _xlfn_norm_s_dist(z_score: float | None) -> float:
    if z_score is None:
        return float("nan")
    return 0.5 * (1 + math.erf(z_score / math.sqrt(2)))


def _classify_z_score(z_score: float | None) -> str | None:
    if z_score is None:
        return None
    if z_score >= 2:
        return "Muito Superior"
    if z_score >= 1.333:
        return "Superior"
    if z_score >= 0.666:
        return "Média Superior"
    if z_score >= -0.667:
        return "Média"
    if z_score >= -1.333:
        return "Média Inferior"
    if z_score >= -2:
        return "Limítrofe"
    return "Deficitário"


def analyze_supplementary(loader: WAIS3NormLoader, age_range_key: str, computed_subtests: dict, indices: dict, raw_scores: dict | None = None) -> dict:
    """Executa análises complementares B.1, B.3, B.6, B.7."""
    result = {
        "facilidades_dificuldades": [],
        "discrepancias": [],
        "digitos": {},
    }

    b1_data = _load_b1(loader)
    b3_data = _load_b3(loader)

    # ----- B.3: facilidades e dificuldades -----
    faixa = _map_faixa_b(age_range_key)
    verbal_subtests = ["vocabulario", "semelhancas", "aritmetica", "digitos", "informacao", "compreensao"]
    exec_subtests = ["completar_figuras", "codigos", "cubos", "raciocinio_matricial", "arranjo_figuras"]

    # Calcular médias
    verbal_scores = [computed_subtests[k]["escore_ponderado"] for k in verbal_subtests if computed_subtests.get(k) and computed_subtests[k]["escore_ponderado"] is not None]
    exec_scores = [computed_subtests[k]["escore_ponderado"] for k in exec_subtests if computed_subtests.get(k) and computed_subtests[k]["escore_ponderado"] is not None]
    media_verbal = sum(verbal_scores) / len(verbal_scores) if verbal_scores else 0
    media_exec = sum(exec_scores) / len(exec_scores) if exec_scores else 0

    def _b3_key_for(subtest: str) -> str:
        m = {
            "vocabulario": "vocabulário", "semelhanças": "semelhanças",
            "aritmética": "aritmética", "dígitos": "dígitos",
            "informação": "informação", "compreensão": "compreensão",
            "seq. n. e letras": "seq. n. e letras",
            "comp. figuras": "comp. figuras", "códigos": "códigos",
            "cubos": "cubos", "rac. matricial": "rac. matricial",
            "ar. de figuras": "ar. de figuras", "proc. símbolos": "proc. símbolos",
            "armar objetos": "armar objetos",
        }
        return m.get(subtest, subtest)

    for key in list(verbal_subtests) + list(exec_subtests):
        data = computed_subtests.get(key)
        if not data or data["escore_ponderado"] is None:
            continue
        score = data["escore_ponderado"]
        media = media_verbal if key in verbal_subtests else media_exec
        diff = score - media
        b3_label = WAIS3_ALL_SUBTESTS[key]
        b3_key = b3_label.lower()
        is_verbal = key in verbal_subtests
        critical_15 = b3_data.get(b3_key, {}).get("verbal_n15" if is_verbal else "exec_n15")
        critical_05 = b3_data.get(b3_key, {}).get("verbal_n05" if is_verbal else "exec_n05")

        if critical_05 and abs(diff) >= critical_05:
            tipo = "facilidade" if diff > 0 else "dificuldade"
            result["facilidades_dificuldades"].append({
                "subteste": b3_label,
                "escore": score,
                "media": round(media, 2),
                "diferenca": round(diff, 2),
                "tipo": tipo,
                "significancia": "α=0,05" if abs(diff) >= critical_05 else "α=0,15",
            })

    # ----- B.1: discrepâncias entre índices -----
    age_key_b1 = _map_faixa_b(age_range_key)
    for nivel in ["0,15", "0,05"]:
        key_b1 = f"{age_key_b1}_{nivel}"
        if key_b1 not in b1_data:
            continue
        row = b1_data[key_b1]
        discrepantes = []

        def _diff(i1: str, i2: str) -> float | None:
            v1 = (indices.get(i1) or {}).get("pontuacao_composta")
            v2 = (indices.get(i2) or {}).get("pontuacao_composta")
            if v1 is None or v2 is None:
                return None
            return abs(v1 - v2)

        pairs = [
            ("qi_verbal", "qi_execucao", "qiv_qie"),
            ("compreensao_verbal", "organizacao_perceptual", "icv_iop"),
            ("compreensao_verbal", "memoria_operacional", "icv_imo"),
            ("organizacao_perceptual", "velocidade_processamento", "iop_ivp"),
            ("compreensao_verbal", "velocidade_processamento", "icv_ivp"),
            ("organizacao_perceptual", "memoria_operacional", "iop_imo"),
            ("memoria_operacional", "velocidade_processamento", "imo_ivp"),
        ]

        for i1, i2, col in pairs:
            diff = _diff(i1, i2)
            critical = row.get(col)
            if diff is not None and critical is not None and diff >= critical:
                n1 = (indices.get(i1) or {}).get("nome") or i1
                n2 = (indices.get(i2) or {}).get("nome") or i2
                discrepantes.append({
                    "par": f"{n1} × {n2}",
                    "diferenca": diff,
                    "critico": critical,
                    "nivel": nivel,
                })

        if discrepantes:
            result["discrepancias"].append({
                "nivel": nivel,
                "pares": discrepantes,
            })

    # ----- B.6 e B.7: análise de Dígitos -----
    digitos_data = computed_subtests.get("digitos")
    if digitos_data and digitos_data.get("escore_ponderado") is not None:
        raw_digitos = digitos_data.get("pontos_brutos", 0) or 0
        col_direta = _map_faixa_b6(age_range_key)
        col_inversa = col_direta + 1

        # Tentar ler B.6 do CSV raw para frequência cumulativa
        b6_path = Path(loader.base_path) / "supplementary" / "b6_digitos_ordem_direta_inversa.csv"
        freq_direta = None
        freq_inversa = None
        if b6_path.exists():
            try:
                with b6_path.open(encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for r in reader:
                        if r.get("col_0") and str(r.get("col_0")).strip().isdigit():
                            maximo = int(str(r.get("col_0")).strip())
                            if maximo == raw_digitos:
                                freq_direta = _norm_float(r.get(f"col_{col_direta}"))
                                freq_inversa = _norm_float(r.get(f"col_{col_inversa}"))
                                break
            except Exception:
                pass

        result["digitos"] = {
            "maximo_ordem_direta": raw_digitos,
            "maximo_ordem_inversa": None,  # raw não distingue; calculado via B.7 se necessário
            "diferenca_direta_inversa": None,
            "frequencia_b6_direta": freq_direta,
            "frequencia_b6_inversa": freq_inversa,
        }

    process_scores = (raw_scores or {}).get("process_scores") or {}
    b6_rows = loader.get_supplementary_tables().get("b6") or []
    b7_rows = loader.get_supplementary_tables().get("b7") or []
    direct_col, inverse_col = _b6_columns_for_age(age_range_key)
    b7_col = _b7_column_for_age(age_range_key)

    digits_forward = process_scores.get("digitos_ordem_direta")
    digits_backward = process_scores.get("digitos_ordem_inversa")
    forward_span = process_scores.get("maior_sequencia_digitos_direta")
    backward_span = process_scores.get("maior_sequencia_digitos_inversa")

    if digits_forward is not None:
        result["digitos"]["ordem_direta"] = _build_process_result(
            raw_value=int(digits_forward),
            mean=_row_value(b6_rows, "Média", direct_col),
            sd=_row_value(b6_rows, "DP", direct_col),
            percentile=_lookup_percentile_from_csv_rows(b6_rows, int(digits_forward), direct_col),
        )

    if digits_backward is not None:
        result["digitos"]["ordem_inversa"] = _build_process_result(
            raw_value=int(digits_backward),
            mean=_row_value(b6_rows, "Média", inverse_col),
            sd=_row_value(b6_rows, "DP", inverse_col),
            percentile=_lookup_percentile_from_csv_rows(b6_rows, int(digits_backward), inverse_col),
        )

    if forward_span is not None:
        result["digitos"]["maior_sequencia_direta"] = _build_process_result(
            raw_value=int(forward_span),
            mean=_row_value(b6_rows, "Média", direct_col),
            sd=_row_value(b6_rows, "DP", direct_col),
            percentile=_lookup_percentile_from_csv_rows(b6_rows, int(forward_span), direct_col),
        )

    if backward_span is not None:
        result["digitos"]["maior_sequencia_inversa"] = _build_process_result(
            raw_value=int(backward_span),
            mean=_row_value(b6_rows, "Média", inverse_col),
            sd=_row_value(b6_rows, "DP", inverse_col),
            percentile=_lookup_percentile_from_csv_rows(b6_rows, int(backward_span), inverse_col),
        )

    if forward_span is not None and backward_span is not None:
        difference = int(forward_span) - int(backward_span)
        result["digitos"]["diferenca_maior_sequencia"] = _build_process_result(
            raw_value=difference,
            mean=_row_value(b7_rows, "Média", b7_col),
            sd=_row_value(b7_rows, "DP", b7_col),
            percentile=_lookup_percentile_from_csv_rows(b7_rows, difference, b7_col),
            reverse_z=True,
        )
        result["digitos"]["diferenca_maior_sequencia"]["difference"] = difference

    return result


# ------------------------------------------------------------------
# Cálculo principal
# ------------------------------------------------------------------

def compute_wais3_payload(raw_scores: dict, loader: WAIS3NormLoader | None = None) -> dict:
    loader = loader or WAIS3NormLoader()
    idade = raw_scores.get("idade") or {}
    anos = int(idade.get("anos", 0) or 0)
    meses = int(idade.get("meses", 0) or 0)
    age_range_key = resolve_age_range(anos, meses)

    computed_subtests: dict[str, dict] = {}
    warnings: list[str] = []
    supplementary_tables = loader.get_supplementary_tables()
    psychometrics_tables = loader.get_psychometrics_tables()

    for key, label in WAIS3_ALL_SUBTESTS.items():
        payload = (raw_scores.get("subtestes") or {}).get(key)
        if not payload:
            continue
        raw_value = int(payload.get("pontos_brutos", 0) or 0)
        scaled_score = None
        warning = None
        try:
            scaled_score = loader.get_scaled_score(key, raw_value, age_range_key)
        except Exception as exc:
            try:
                scaled_score = loader.get_scaled_score(key, raw_value, "grupo_referencia_20-34")
                warning = f"fallback: used grupo_referencia_20-34 for {age_range_key}"
            except Exception as exc2:
                warning = str(exc2)
                warnings.append(f"{label}: {warning}")
        computed_subtests[key] = {
            "nome": label,
            "pontos_brutos": raw_value,
            "escore_ponderado": scaled_score,
            "classificacao": classify_scaled_score(scaled_score),
            "dominio": "verbal" if key in {"vocabulario", "semelhancas", "aritmetica", "digitos", "informacao", "compreensao", "sequencia_numeros_letras"} else "execucao",
            "warning": warning,
        }

    # Subtestes ordenados
    subtestes_ordenados = [
        computed_subtests[key]
        for key in WAIS3_SUBTEST_ORDER
        if key in computed_subtests
    ]

    computed_indexes: dict[str, dict] = {}
    for index_key, index_cfg in WAIS3_INDEXES.items():
        missing_subtests = [
            code
            for code in index_cfg["subtests"]
            if not computed_subtests.get(code) or computed_subtests[code].get("escore_ponderado") is None
        ]
        scaled_sum = None
        composite_data = None
        warning = None
        if not missing_subtests:
            scaled_sum = sum(computed_subtests[code]["escore_ponderado"] for code in index_cfg["subtests"])
            try:
                composite_data = loader.get_composite_score(index_key, scaled_sum)
            except Exception as exc:
                warning = str(exc)
                warnings.append(f"{index_cfg['label']}: {warning}")
        composite_score = composite_data.get("pontuacao_composta") if composite_data else None
        computed_indexes[index_key] = {
            "nome": index_cfg["label"],
            "subtestes": index_cfg["subtests"],
            "soma_ponderada": scaled_sum,
            "pontuacao_composta": composite_score,
            "percentil": composite_data.get("percentil") if composite_data else None,
            "ic_90": composite_data.get("ic_90") if composite_data else None,
            "ic_95": composite_data.get("ic_95") if composite_data else None,
            "classificacao": composite_data.get("classificacao") if composite_data and composite_data.get("classificacao") else classify_composite_score(composite_score),
            "fonte_tabela": composite_data.get("source") if composite_data else None,
            "subtestes_ausentes": missing_subtests,
            "warning": warning,
        }

    # Análises complementares
    supplementary = analyze_supplementary(loader, age_range_key, computed_subtests, computed_indexes, raw_scores=raw_scores)

    return {
        "instrument_code": "wais3",
        "instrument_name": WAIS3_NAME,
        "idade": {"anos": anos, "meses": meses},
        "idade_normativa": age_range_key,
        "subtestes": computed_subtests,
        "subtestes_ordenados": subtestes_ordenados,
        "indices": computed_indexes,
        "supplementary_tables": supplementary_tables,
        "psychometrics_tables": psychometrics_tables,
        "supplementary_tables_available": sorted(supplementary_tables.keys()),
        "psychometrics_available": sorted(psychometrics_tables.keys()),
        "has_scaled_score_data": loader.has_scaled_score_data(),
        "has_composite_data": loader.has_composite_data(),
        "norm_tables_ready": loader.has_normative_data(),
        "warnings": warnings,
        "manifest": loader.load_manifest(),
        # Análises complementares
        "facilidades_dificuldades": supplementary["facilidades_dificuldades"],
        "discrepancias": supplementary["discrepancias"],
        "digitos": supplementary["digitos"],
    }
