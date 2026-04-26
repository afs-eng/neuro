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
        "path": "composite_scores/qi_verbal.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "qi_execucao": {
        "path": "composite_scores/qi_execucao.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "qi_total": {
        "path": "composite_scores/qi_total.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "compreensao_verbal": {
        "path": "composite_scores/compreensao_verbal.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "organizacao_perceptual": {
        "path": "composite_scores/organizacao_perceptual.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "memoria_operacional": {
        "path": "composite_scores/memoria_operacional.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
    "velocidade_processamento": {
        "path": "composite_scores/velocidade_processamento.csv",
        "sum_column": "soma_ponderada",
        "score_column": "pontuacao_composta",
        "percentile_column": "percentil",
        "ic90_column": "ic_90",
        "ic95_column": "ic_95",
    },
}

WAIS3_SUPPLEMENTARY_TABLES = {
    "b1": "supplementary/b1_diferencas_qi_indices_significancia.csv",
    "b2": "supplementary/b2_frequencia_diferencas_qi_indices.csv",
    "b3": "supplementary/b3_diferencas_subteste_media.csv",
    "b4": "supplementary/b4_diferencas_entre_subtestes.csv",
    "b5": "supplementary/b5_dispersao_subtestes.csv",
    "b6": "supplementary/b6_digitos_ordem_direta_inversa.csv",
    "b7": "supplementary/b7_diferenca_digitos_direta_inversa.csv",
}

WAIS3_PSYCHOMETRICS_TABLES = {
    "consistencia_interna": "psychometrics/consistencia_interna.csv",
    "estabilidade_teste_reteste": "psychometrics/estabilidade_teste_reteste.csv",
    "amostra_reteste": "psychometrics/amostra_reteste.csv",
    "erro_padrao_medida": "psychometrics/erro_padrao_medida.csv",
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
