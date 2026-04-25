from apps.tests.wisc4 import WISC4Module
from apps.tests.base.types import TestContext
from apps.tests.wisc4.calculators import WISC4_SUBTESTS


def _map_subtests_to_wais_shape(subtests_dict: dict) -> dict:
    """Map the WISC4 subtest results to a WAIS-like dict keyed by subtest code.

    This keeps field names similar to the WAIS payload so downstream code
    that expects the WAIS model can consume it for comparison/analysis.
    """
    mapped = {}
    for code, data in subtests_dict.items():
        mapped[code] = {
            "nome": data.get("subteste"),
            "pontos_brutos": data.get("escore_bruto"),
            "escore_ponderado": data.get("escore_padrao"),
            "classificacao": data.get("classificacao"),
        }
    return mapped


def _map_indices_list_to_dict(indices_list: list[dict]) -> dict:
    result = {}
    for entry in indices_list:
        code = entry.get("indice")
        if code is None:
            continue
        result[code] = {
            "nome": entry.get("nome"),
            "soma_ponderada": entry.get("soma_ponderados"),
            "pontuacao_composta": entry.get("escore_composto"),
            "percentil": entry.get("percentil"),
            "ic": entry.get("intervalo_confianca"),
            "classificacao": entry.get("classificacao"),
        }
    return result


def test_wisc4_model_compatibility_shape_and_consistency():
    """Verifies we can produce a WAIS3-style payload from WISC4 outputs.

    The goal is structural compatibility (same top-level keys and predictable
    mapping of values) and internal consistency between the classification
    results returned by WISC4Module.classify and the transformed payload.
    """
    module = WISC4Module()

    # Build a TestContext with reasonable mid-range raw scores for all core
    # subtests so the module can compute and classify without validation errors.
    raw_scores = {code: max(1, cfg["max"] // 2) for code, cfg in WISC4_SUBTESTS.items()}
    context = TestContext(
        patient_name="Teste Exemplo",
        evaluation_id=1,
        instrument_code="wisc4",
        raw_scores=raw_scores,
        reviewed_scores={},
    )

    # Compute per-subtest results
    computed = module.compute(context)
    assert isinstance(computed, dict)

    # Classify indices and compose higher-level results
    classification = module.classify(computed)
    assert isinstance(classification, dict)

    # Build WAIS-like payload
    payload = {
        "instrument_code": "wisc4",
        "instrument_name": module.name,
        "idade": context.reviewed_scores.get("idade", {}),
        "subtestes": _map_subtests_to_wais_shape(computed),
        "indices": _map_indices_list_to_dict(classification.get("indices", [])),
        "qit_data": classification.get("qit_data"),
        "gai_data": classification.get("gai_data"),
        "cpi_data": classification.get("cpi_data"),
    }

    # Basic shape assertions
    assert payload["instrument_code"] == "wisc4"
    assert isinstance(payload["subtestes"], dict)
    assert isinstance(payload["indices"], dict)

    # Consistency checks: values in payload must reflect classification output
    for idx_entry in classification.get("indices", []):
        code = idx_entry.get("indice")
        if not code:
            continue
        mapped = payload["indices"].get(code)
        assert mapped is not None
        assert mapped["soma_ponderada"] == idx_entry.get("soma_ponderados")
        assert mapped["pontuacao_composta"] == idx_entry.get("escore_composto")

    # QIT consistency
    qit_from_classify = classification.get("qi_total")
    qit_data = payload.get("qit_data") or {}
    assert qit_data.get("escore_composto") == (classification.get("qit_data") or {}).get(
        "escore_composto"
    )
