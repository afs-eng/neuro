from __future__ import annotations

from .constants import WAIS3_ALL_SUBTESTS, WAIS3_INDEXES, WAIS3_NAME, classify_composite_score, classify_scaled_score
from .loaders import WAIS3NormLoader
from .norm_utils import resolve_age_range


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
            # fallback: some normative files are empty for specific ages,
            # try the group-reference template 'grupo_referencia_20-34' if available
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

    return {
        "instrument_code": "wais3",
        "instrument_name": WAIS3_NAME,
        "idade": {"anos": anos, "meses": meses},
        "idade_normativa": age_range_key,
        "subtestes": computed_subtests,
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
    }
