from __future__ import annotations

from typing import Any

from .loaders import WAIS3NormLoader

# Domains used by some unit tests / helpers
WAIS3_DOMAINS = {
    "verbal": [
        "vocabulario",
        "semelhancas",
        "aritmetica",
        "digitos",
        "informacao",
    ],
    "ivp": [
        "codigos",
        "procurar_simbolos",
    ],
}


def sum_scaled_scores(scaled_scores: dict, subtests: list[str]) -> int:
    """Sum safe: only include tests that are present, not parenthetical and allowed.

    Raises ValueError if any required subtest is missing a value.
    """
    total = 0
    missing: list[str] = []

    for subtest in subtests:
        item = scaled_scores.get(subtest)

        if item is None:
            missing.append(subtest)
            continue

        if item.get("parenthetical") is True:
            # explicitly excluded
            continue

        if item.get("included_in_primary_sum") is False:
            continue

        value = item.get("value")
        if value is None:
            missing.append(subtest)
            continue

        total += int(value)

    if missing:
        raise ValueError(f"Subtestes obrigatorios ausentes: {missing}")

    return total


def convert_wais3_raw_to_scaled(*, age_years: int, age_months: int = 0, subtest_key: str, raw_score: int, loader: WAIS3NormLoader | None = None) -> int:
    """Convert a raw subtest score to scaled score using WAIS3NormLoader.

    This is a thin helper used by unit tests and scripts. It raises
    ValueError if conversion is not found, mirroring loader behaviour.
    """
    loader = loader or WAIS3NormLoader()
    age_range = loader.base_path  # just to keep type
    # use the norm util in loader indirectly by resolving age range via loader's manifest usage
    # WAIS3NormLoader doesn't expose resolve_age_range, but the loader files' keys follow the project's naming
    # We'll compute a matching key by checking available raw_to_scaled files and choosing the one that contains the age
    # The simple path: determine the age range by iterating loader.base_path / 'raw_to_scaled' folders and filenames.
    # However the project already provides a norm_utils.resolve_age_range; to avoid circular imports we call loader._read_csv_rows indirectly
    from .norm_utils import resolve_age_range

    age_key = resolve_age_range(age_years, age_months)
    # delegate to loader.get_scaled_score which implements the lookup and fallbacks
    return loader.get_scaled_score(subtest_key, int(raw_score), age_key)


def _map_composite_alias(key: str) -> str:
    mapping = {
        "qiv": "qi_verbal",
        "qie": "qi_execucao",
        "qit": "qi_total",
        "icv": "compreensao_verbal",
        "iop": "organizacao_perceptual",
        "imo": "memoria_operacional",
        "ivp": "velocidade_processamento",
    }
    return mapping.get(key, key)


def convert_wais3_sum_to_composite(*, composite_key: str, sum_score: int, loader: WAIS3NormLoader | None = None) -> dict[str, Any]:
    """Convert a summed scaled-score into a composite standard score (QI / index).

    composite_key may be an alias like 'qiv' or the internal key used in WAIS3_COMPOSITE_TABLES.
    """
    loader = loader or WAIS3NormLoader()
    key = _map_composite_alias(composite_key)
    # loader expects the index_key names used in constants (e.g. 'qi_verbal')
    return loader.get_composite_score(key, int(sum_score))


def compute_wais3_composites(sums: dict, conversion_tables: dict) -> dict:
    """Compatibility wrapper mirroring the skill's expected behaviour.

    This function is kept for compatibility with skill tests but in the
    actual code the loader.get_composite_score is the preferred path.
    """
    # The project already has an implementation in the skill description; here we keep a thin wrapper
    from .constants import WAIS3_COMPOSITE_TABLES

    # mapping from composite table key to expected sum key in the 'sums' dict
    sum_key_map = {
        "qi_verbal": "verbal",
        "qi_execucao": "execucao",
        "qi_total": "escala_total",
        "compreensao_verbal": "icv",
        "organizacao_perceptual": "iop",
        "memoria_operacional": "imo",
        "velocidade_processamento": "ivp",
    }

    composites: dict[str, Any] = {}
    for composite_key, config in WAIS3_COMPOSITE_TABLES.items():
        sum_key = sum_key_map.get(composite_key, composite_key)
        table_name = config.get("path") or config.get("table")

        # If the caller didn't provide the conversion table for this composite,
        # skip it. This allows tests to validate a single composite table
        # without having to pass all tables.
        if table_name not in conversion_tables:
            continue

        if sum_key not in sums:
            # skip if sums do not include this composite's sum
            continue
        if sum_key not in sums:
            raise ValueError(f"Soma ausente para {composite_key}: {sum_key}")

        # Expect conversion_tables to be a mapping table_name -> pandas-like frame/dict rows
        conversion_df = conversion_tables.get(table_name)
        if conversion_df is None:
            raise ValueError(f"Tabela de conversao ausente: {table_name}")

        # conversion_df is expected to be an iterable of dict rows (as returned by loader._read_csv_rows)
        found = None
        for row in conversion_df:
            val = row.get("soma_escores_ponderados") or row.get("soma_ponderada")
            try:
                if val is not None and int(float(str(val).replace(",", "."))) == int(sums[sum_key]):
                    found = row
                    break
            except Exception:
                continue

        if not found:
            raise ValueError(f"Soma de escores ponderados {sums[sum_key]} nao encontrada na tabela de conversao {table_name}.")

        standard = found.get("score_padronizado") or found.get("pontuacao_composta")
        percentile = found.get("percentil")

        # ic_95 fields in CSVs often use a range with a dash (e.g. '101–109').
        # Extract integers safely for min/max when possible.
        def _extract_first_int(text):
            if text is None:
                return None
            s = str(text)
            import re
            m = re.search(r"(\d+)", s)
            return int(m.group(1)) if m else None

        ic95_min = _extract_first_int(found.get("ic_95_min") or found.get("ic_95") or found.get("ic95"))
        ic95_max = _extract_first_int(found.get("ic_95_max") or found.get("ic_95_max") or found.get("ic95_max") or found.get("ic_95"))

        composites[composite_key] = {
            "label": config.get("label"),
            "sum_score": int(sums[sum_key]),
            "standard_score": int(float(standard)) if standard is not None else None,
            "percentile": float(str(percentile).replace(",", ".")) if percentile is not None else None,
            "confidence_interval_95": {"min": ic95_min, "max": ic95_max},
            "conversion_table": table_name,
        }

    return composites
