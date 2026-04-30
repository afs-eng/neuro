from apps.tests.wais3.calculators import compute_wais3_payload


def test_wais3_sample_result_case():
    """Case reproduzindo os dados do WAIS-III 2020 para um adulto de 30 anos.

    Os valores brutos fornecidos correspondem a escores ponderados e QIs
    compatíveis com o perfil cognitivo de um adulto de 30 anos (faixa 30-39).

    A verificação é feita contra os valores extraídos das tabelas normativas
    brasileiras WAIS-III 2020 (Tabelas A.1 a A.9).
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

    # Assertions de estrutura
    assert payload["instrument_code"] == "wais3"
    assert payload["idade_normativa"] == "idade_30-39"

    indices = payload.get("indices") or {}
    subtests = payload.get("subtestes") or {}

    # --- Subtestes: escores ponderados (Tabela A.1, faixa 30-39) ---
    assert subtests["vocabulario"]["escore_ponderado"] == 11
    assert subtests["semelhancas"]["escore_ponderado"] == 10
    assert subtests["aritmetica"]["escore_ponderado"] == 8
    assert subtests["digitos"]["escore_ponderado"] == 9
    assert subtests["informacao"]["escore_ponderado"] == 11
    assert subtests["compreensao"]["escore_ponderado"] == 13
    assert subtests["sequencia_numeros_letras"]["escore_ponderado"] == 12
    assert subtests["completar_figuras"]["escore_ponderado"] == 10
    assert subtests["codigos"]["escore_ponderado"] == 10
    assert subtests["cubos"]["escore_ponderado"] == 8
    assert subtests["raciocinio_matricial"]["escore_ponderado"] == 11
    assert subtests["arranjo_figuras"]["escore_ponderado"] == 13
    assert subtests["procurar_simbolos"]["escore_ponderado"] == 10
    assert subtests["armar_objetos"]["escore_ponderado"] == 1

    # --- Classificações qualitativas (escore ponderado) ---
    assert subtests["vocabulario"]["classificacao"] == "Média"
    assert subtests["compreensao"]["classificacao"] == "Média Superior"
    assert subtests["arranjo_figuras"]["classificacao"] == "Média Superior"
    assert subtests["sequencia_numeros_letras"]["classificacao"] == "Média Superior"
    assert subtests["armar_objetos"]["classificacao"] == "Extremamente Baixo"

    # --- QI Total (Tabela A.5, soma=114) ---
    qi_total = indices.get("qi_total") or {}
    assert qi_total["soma_ponderada"] == 114
    assert qi_total["pontuacao_composta"] == 102
    assert qi_total["percentil"] == 55

    # --- QI Verbal (Tabela A.3, soma=62) ---
    qi_verbal = indices.get("qi_verbal") or {}
    assert qi_verbal["soma_ponderada"] == 62
    assert qi_verbal["pontuacao_composta"] == 102
    assert qi_verbal["percentil"] == 55

    # --- QI Execução (Tabela A.4, soma=52) ---
    qi_exec = indices.get("qi_execucao") or {}
    assert qi_exec["soma_ponderada"] == 52
    assert qi_exec["pontuacao_composta"] == 102
    assert qi_exec["percentil"] == 55

    # --- ICV (Tabela A.6, soma=32: Vocab(11)+Semelh(10)+Info(11)) ---
    icv = indices.get("compreensao_verbal") or {}
    assert icv["soma_ponderada"] == 32
    assert icv["pontuacao_composta"] == 104
    assert icv["percentil"] == 61

    # --- IOP (Tabela A.7, soma=29: CF(10)+Cubos(8)+RM(11)) ---
    iop = indices.get("organizacao_perceptual") or {}
    assert iop["soma_ponderada"] == 29
    assert iop["pontuacao_composta"] == 98
    assert iop["percentil"] == 45

    # --- IMO (Tabela A.8, soma=29: Arit(8)+Dig(9)+SeqNL(12)) ---
    imo = indices.get("memoria_operacional") or {}
    assert imo["soma_ponderada"] == 29
    assert imo["pontuacao_composta"] == 98

    # --- IVP (Tabela A.9, soma=20: Cod(10)+PS(10)) ---
    ivp = indices.get("velocidade_processamento") or {}
    assert ivp["soma_ponderada"] == 20
    assert ivp["pontuacao_composta"] == 100
    assert ivp["percentil"] == 50

    # --- Sem warnings, todas as tabelas carregadas ---
    assert not payload.get("warnings"), f"Há warnings: {payload['warnings']}"
    assert payload["has_scaled_score_data"] is True
    assert payload["has_composite_data"] is True
    assert payload["norm_tables_ready"] is True


def test_wais3_digit_process_scores_are_computed_when_provided():
    raw_scores = {
        "idade": {"anos": 30, "meses": 0},
        "subtestes": {
            "digitos": {"pontos_brutos": 13},
        },
        "process_scores": {
            "digitos_ordem_direta": 6,
            "digitos_ordem_inversa": 4,
            "maior_sequencia_digitos_direta": 6,
            "maior_sequencia_digitos_inversa": 4,
        },
    }

    payload = compute_wais3_payload(raw_scores)
    digitos = payload["digitos"]

    assert digitos["ordem_direta"]["cumulative_frequency"] == 61.8
    assert digitos["ordem_direta"]["scaled_score"] == 10.0
    assert digitos["ordem_direta"]["classification"] == "Média"

    assert digitos["ordem_inversa"]["cumulative_frequency"] == 70.7
    assert digitos["ordem_inversa"]["classification"] == "Média"

    assert digitos["diferenca_maior_sequencia"]["difference"] == 2
    assert digitos["diferenca_maior_sequencia"]["cumulative_frequency"] == 58.7
    assert digitos["diferenca_maior_sequencia"]["classification"] == "Média"
