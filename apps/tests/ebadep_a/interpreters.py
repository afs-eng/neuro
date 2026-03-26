INTERPRETATIONS = {
    "Sintomatologia Depressiva Mínima (sem sintomatologia)": {
        "geral": "O resultado sugere ausência de sintomatologia depressiva clinicamente relevante neste rastreio, devendo a interpretação ser integrada aos demais dados clínicos.",
        "nivel": "mínimo",
        "descricao": "ausência de sintomatologia depressiva clinicamente relevante",
        "cor": "positivo",
    },
    "Sintomatologia Depressiva Leve": {
        "geral": "Esse resultado sugere que o avaliado se encontra na categoria de sintomas depressivos leves. Nessa faixa, as pessoas podem apresentar sofrimento psicológico leve, porém não comprometem significativamente o funcionamento cotidiano.",
        "nivel": "leve",
        "descricao": "sintomatologia depressiva leve",
        "cor": "leve",
    },
    "Sintomatologia Depressiva Moderada": {
        "geral": "Esse resultado sugere que o avaliado se encontra na categoria sintomas depressivos moderados. Nessa faixa, as pessoas já podem apresentar sofrimento psicológico significativo e/ou limitações importantes para o desempenho de atividades laborais, escolares, entre outras.",
        "nivel": "moderado",
        "descricao": "sintomatologia depressiva moderada",
        "cor": "moderado",
    },
    "Sintomatologia Depressiva Severa": {
        "geral": "Esse resultado sugere que o avaliado se encontra na categoria de sintomas depressivos severos. Nessa faixa, o sofrimento psicológico é intenso e as limitações funcionais são significativas, sendo indicada avaliação clínica prioritária.",
        "nivel": "severo",
        "descricao": "sintomatologia depressiva severa",
        "cor": "grave",
    },
}

SYNTHESIS_LEVELS = {
    "Sintomatologia Depressiva Mínima (sem sintomatologia)": "sem indicadores significativos de depressão",
    "Sintomatologia Depressiva Leve": "com indicadores leves de sintomatologia depressiva",
    "Sintomatologia Depressiva Moderada": "com indicadores moderados de sintomatologia depressiva",
    "Sintomatologia Depressiva Severa": "com indicadores severos de sintomatologia depressiva",
}


def interpret_result(classificacao: str) -> dict:
    return INTERPRETATIONS.get(
        classificacao,
        {
            "geral": "Classificação não disponível.",
            "nivel": "indefinido",
            "descricao": "não classificado",
            "cor": "neutro",
        },
    )


def get_synthesis(classificacao: str) -> str:
    return SYNTHESIS_LEVELS.get(classificacao, "não classificado")


def get_report_interpretation(classificacao: str, nome: str) -> str:
    interp = INTERPRETATIONS.get(classificacao, {})
    return interp.get("geral", "Interpretação não disponível.")
