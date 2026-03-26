INTERPRETATIONS = {
    "Comportamento positivo 1": {
        "geral": "Os resultados indicam um perfil comportamental positivo, com escores muito baixos em indicadores de sintomatologia. O avaliado apresenta padrões de comportamento adequados, sem evidências significativas de dificuldades emocionais, comportamentais ou sociais. Este perfil sugere um bom ajuste psicológico e desenvolvimento socioemocional dentro dos parâmetros esperados.",
        "nivel": "muito baixo",
        "descricao": "ausência de sintomatologia significativa",
    },
    "Comportamento positivo 2": {
        "geral": "Os resultados indicam um perfil comportamental positivo, com escores baixos em indicadores de sintomatologia. O avaliado apresenta padrões de comportamento predominantemente adequados, com possíveis indicadores leves que não configuram prejuízo funcional significativo. Este perfil sugere um bom ajuste psicológico geral.",
        "nivel": "baixo",
        "descricao": "indicadores mínimos de sintomatologia",
    },
    "Com sintomatologia leve": {
        "geral": "Os resultados indicam a presença de sintomatologia em nível leve. O avaliado apresenta alguns indicadores comportamentais que podem requerer atenção, embora não configurem comprometimento funcional significativo. Recomenda-se monitoramento e, se necessário, intervenções preventivas para evitar agravamento.",
        "nivel": "leve",
        "descricao": "presença leve de sintomatologia",
    },
    "Com sintomatologia moderada": {
        "geral": "Os resultados indicam a presença de sintomatologia em nível moderado. O avaliado apresenta indicadores comportamentais que sugerem necessidade de acompanhamento e intervenção. Os escores obtidos apontam para dificuldades que podem estar impactando o funcionamento em diferentes contextos, requerendo atenção profissional.",
        "nivel": "moderado",
        "descricao": "presença moderada de sintomatologia",
    },
    "Com sintomatologia grave ou severa": {
        "geral": "Os resultados indicam a presença de sintomatologia em nível grave ou severo. O avaliado apresenta indicadores comportamentais significativos que requerem atenção profissional prioritária. Os escores obtidos sugerem comprometimento funcional que necessita de intervenção imediata e acompanhamento especializado.",
        "nivel": "grave/severo",
        "descricao": "presença significativa de sintomatologia",
    },
}

SYNTHESIS_LEVELS = {
    "Comportamento positivo 1": "muito positivo",
    "Comportamento positivo 2": "positivo",
    "Com sintomatologia leve": "com indicadores leves de sintomatologia",
    "Com sintomatologia moderada": "com indicadores moderados de sintomatologia",
    "Com sintomatologia grave ou severa": "com indicadores significativos de sintomatologia",
}


def interpret_result(classificacao: str) -> dict:
    return INTERPRETATIONS.get(
        classificacao,
        {
            "geral": "Classificação não disponível.",
            "nivel": "indefinido",
            "descricao": "não classificado",
        },
    )


def get_synthesis(classificacao: str) -> str:
    return SYNTHESIS_LEVELS.get(classificacao, "não classificado")


def get_report_interpretation(classificacao: str, nome: str) -> str:
    interp = INTERPRETATIONS.get(classificacao, {})
    nivel = interp.get("nivel", "não classificado")
    descricao = interp.get("descricao", "")

    return (
        f'{nome} obteve pontuação total classificada como "{classificacao}", '
        f"indicando um nível {nivel} de sintomatologia comportamental. "
        f"Os resultados sugerem {descricao}, "
        f"sendo recomendada a integração com demais dados obtidos no processo avaliativo "
        f"para uma compreensão abrangente do perfil do avaliado."
    )
