from apps.tests.wais3.calculators import compute_wais3_payload


def test_wais3_sample_result_case():
    """Case reproducing the screenshots provided by the user.

    We provide raw subtest scores and age so the existing loaders/tables
    produce the same scaled/subtotal/composite values shown in the images.
    This is a regression-style test that asserts specific output fields.
    """
    raw_scores = {
        "idade": {"anos": 30, "meses": 0},
        "subtestes": {
            "completar_figuras": {"pontos_brutos": 18},
            "vocabulario": {"pontos_brutos": 36},
            "codigos": {"pontos_brutos": 59},
            "semelhancas": {"pontos_brutos": 22},
            "cubos": {"pontos_brutos": 22},
            "aritmetica": {"pontos_brutos": 8},
            "raciocinio_matricial": {"pontos_brutos": 16},
            "digitos": {"pontos_brutos": 13},
            "informacao": {"pontos_brutos": 13},
            "arranjo_figuras": {"pontos_brutos": 17},
            "compreensao": {"pontos_brutos": 27},
            "procurar_simbolos": {"pontos_brutos": 26},
            "sequencia_numeros_letras": {"pontos_brutos": 10},
            "armar_objetos": {"pontos_brutos": 0},
        },
    }

    payload = compute_wais3_payload(raw_scores)

    # Basic top-level assertions
    assert payload["instrument_code"] == "wais3"
    assert payload["idade"] == {"anos": 30, "meses": 0}

    indices = payload.get("indices") or {}

    # Assert the total composite QI and composite points shown on the screenshot
    qi_total = indices.get("qi_total") or {}
    assert qi_total.get("soma_ponderada") == 114
    assert qi_total.get("pontuacao_composta") == 102
    assert qi_total.get("percentil") == 55

    # Check some factor indices from the screenshot
    icv = indices.get("compreensao_verbal") or {}
    iop = indices.get("organizacao_perceptual") or {}
    imo = indices.get("memoria_operacional") or {}
    ivp = indices.get("velocidade_processamento") or {}

    assert icv.get("soma_ponderada") == 32
    assert icv.get("pontuacao_composta") == 104

    assert iop.get("soma_ponderada") == 28
    assert iop.get("pontuacao_composta") == 96

    assert imo.get("soma_ponderada") == 30
    assert imo.get("pontuacao_composta") == 100

    assert ivp.get("soma_ponderada") == 19
    assert ivp.get("pontuacao_composta") == 98

    # Ensure subtest scaled scores exist for a few subtests
    subtests = payload.get("subtestes") or {}
    assert subtests["vocabulario"]["escore_ponderado"] == 11
    assert subtests["codigos"]["escore_ponderado"] == 10
    assert subtests["completar_figuras"]["escore_ponderado"] == 11
