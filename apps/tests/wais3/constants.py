WAIS3_CODE = "wais3"
WAIS3_NAME = "WAIS-III - Escala de Inteligência Wechsler para Adultos"
WAIS3_MIN_AGE = 16
WAIS3_MAX_AGE = 89

WAIS3_VERBAL_SUBTESTS = {
    "vocabulario": "Vocabulário",
    "semelhancas": "Semelhanças",
    "aritmetica": "Aritmética",
    "digitos": "Dígitos",
    "informacao": "Informação",
    "compreensao": "Compreensão",
    "sequencia_numeros_letras": "Sequência de Números e Letras",
}

WAIS3_EXECUTION_SUBTESTS = {
    "completar_figuras": "Completar Figuras",
    "codigos": "Códigos",
    "cubos": "Cubos",
    "raciocinio_matricial": "Raciocínio Matricial",
    "arranjo_figuras": "Arranjo de Figuras",
    "procurar_simbolos": "Procurar Símbolos",
    "armar_objetos": "Armar Objetos",
}

WAIS3_ALL_SUBTESTS = {
    **WAIS3_VERBAL_SUBTESTS,
    **WAIS3_EXECUTION_SUBTESTS,
}

WAIS3_INDEXES = {
    "qi_verbal": {
        "label": "QI Verbal",
        "subtests": ["vocabulario", "semelhancas", "aritmetica", "digitos", "informacao", "compreensao"],
    },
    "qi_execucao": {
        "label": "QI de Execução",
        "subtests": ["completar_figuras", "codigos", "cubos", "raciocinio_matricial", "arranjo_figuras"],
    },
    "qi_total": {
        "label": "QI Total",
        "subtests": [
            "vocabulario", "semelhancas", "aritmetica", "digitos", "informacao", "compreensao",
            "completar_figuras", "codigos", "cubos", "raciocinio_matricial", "arranjo_figuras",
        ],
    },
    "compreensao_verbal": {
        "label": "Índice de Compreensão Verbal",
        "subtests": ["vocabulario", "semelhancas", "informacao"],
    },
    "organizacao_perceptual": {
        "label": "Índice de Organização Perceptual",
        "subtests": ["completar_figuras", "cubos", "raciocinio_matricial"],
    },
    "memoria_operacional": {
        "label": "Índice de Memória Operacional",
        "subtests": ["aritmetica", "digitos", "sequencia_numeros_letras"],
    },
    "velocidade_processamento": {
        "label": "Índice de Velocidade de Processamento",
        "subtests": ["codigos", "procurar_simbolos"],
    },
}

WAIS3_COMPOSITE_TABLES = {
    "qi_verbal": {
        "path": "QI Equivalente à Soma dos Escores Ponderados/tabela_a3_qi_verbal.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "qi_verbal",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "qi_execucao": {
        "path": "QI Equivalente à Soma dos Escores Ponderados/tabela_a4_qi_execucao.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "qi_execucao",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "qi_total": {
        "path": "QI Equivalente à Soma dos Escores Ponderados/tabela_a5_qi_total.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "qi_total",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "compreensao_verbal": {
        "path": "QI-Equivalente-Soma-dos-Escores-Ponderados/tabela_a6_indice_compreensao_verbal.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "indice_compreensao_verbal",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "organizacao_perceptual": {
        "path": "QI-Equivalente-Soma-dos-Escores-Ponderados/tabela_a7_indice_organizacao_perceptual.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "indice_organizacao_perceptual",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "memoria_operacional": {
        "path": "QI-Equivalente-Soma-dos-Escores-Ponderados/tabela_a8_indice_memoria_operacional.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "indice_memoria_operacional",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
    "velocidade_processamento": {
        "path": "QI-Equivalente-Soma-dos-Escores-Ponderados/tabela_a9_indice_velocidade_processamento.csv",
        "sum_column": "soma_escores_ponderados",
        "score_column": "indice_velocidade_processamento",
        "percentile_column": "percentil",
        "ic90_column": "intervalo_confianca_90",
        "ic95_column": "intervalo_confianca_95",
    },
}

WAIS3_SUPPLEMENTARY_TABLES = {
    "b1": "Diferenças Consideradas Estatisticamente Significantes entre os Escores em QI e entre os Índices Fatoriais, Segundo a Faixa Etária e para Todas as Idades/wais3_tabela_b1_csv/tabela_b1_diferencas_qi_indices_significancia.csv",
    "b2": "tabela_b2_csv/tabela_b2_frequencias_diferencas_qi_indices.csv",
    "b3": "tabela_b3/tabela_b3_completa_diferencas_subteste_media_ponderada.csv",
    "b4": "tabela_b4/wais3_tabela_b4_csv/tabela_b4_diferencas_entre_subtestes_significancia_long.csv",
    "b5": "tabela_b5/wais3_tabela_b5_csv/tabela_b5_porcentagens_cumulativas_dispersoes_subtestes.csv",
    "b6": "tabela_b6/wais3_tabela_b6_csv/tabela_b6_porcentagens_cumulativas_digitos_direta_inversa_long.csv",
    "b7": "tabela_b7/wais3_tabela_b7_csv/tabela_b7_porcentagens_cumulativas_diferencas_digitos_long.csv",
}

WAIS3_PSYCHOMETRICS_TABLES = {
    "consistencia_interna": "tabela_5_7/wais3_tabela_5_7_csv/tabela_5_7_consistencia_interna_alfa_cronbach_long.csv",
    "estabilidade_teste_reteste": "tabela_5_8a/wais3_tabela_5_8a_csv/tabela_5_8a_coeficientes_estabilidade_teste_reteste_long.csv",
    "amostra_reteste": "tabela_5_8b/wais3_tabela_5_8b_csv/tabela_5_8b_distribuicao_amostra_reteste.csv",
    "erro_padrao_medida": "tabela_5_9/wais3_tabela_5_9_csv/tabela_5_9_erros_padrao_medida_long.csv",
}

WAIS3_AGE_RANGES = [
    {"key": "idade_16-17", "min_years": 16, "max_years": 17},
    {"key": "idade_18-19", "min_years": 18, "max_years": 19},
    {"key": "idade_20-29", "min_years": 20, "max_years": 29},
    {"key": "idade_30-39", "min_years": 30, "max_years": 39},
    {"key": "idade_40-49", "min_years": 40, "max_years": 49},
    {"key": "idade_50-59", "min_years": 50, "max_years": 59},
    {"key": "idade_60-64", "min_years": 60, "max_years": 64},
    {"key": "idade_65-89", "min_years": 65, "max_years": 89},
]


def classify_composite_score(score: int | None) -> str | None:
    if score is None:
        return None
    if score >= 130:
        return "Muito Superior"
    if score >= 120:
        return "Superior"
    if score >= 110:
        return "Média Superior"
    if score >= 90:
        return "Média"
    if score >= 80:
        return "Média Inferior"
    if score >= 70:
        return "Limítrofe"
    return "Extremamente Baixo"


def classify_scaled_score(score: int | None) -> str | None:
    if score is None:
        return None
    if score >= 16:
        return "Muito Superior"
    if score >= 14:
        return "Superior"
    if score >= 12:
        return "Média Superior"
    if score >= 8:
        return "Média"
    if score >= 6:
        return "Média Inferior"
    if score >= 4:
        return "Limítrofe"
    return "Extremamente Baixo"
