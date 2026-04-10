INTERPRETATIONS = {
    "Sintomatologia mínima": {
        "geral": "Os resultados sugerem um perfil comportamental muito positivo, com ausência de sintomas clinicamente relevantes. O desenvolvimento socioemocional encontra-se dentro dos parâmetros de normalidade esperados para a faixa etária.",
        "nivel": "muito baixo",
        "descricao": "Essa categoria expressa a ausência de sintomatologia depressiva significativa, sugerindo um bom ajuste emocional e funcional no momento atual.",
    },
    "Sintomatologia mínima (presença de indicadores isolados)": {
        "geral": "Os resultados sugerem um perfil comportamental positivo, com indicadores mínimos de sintomatologia que não configuram prejuízo funcional.",
        "nivel": "baixo",
        "descricao": "Essa categoria expressa um ajuste emocional adequado, embora possam existir flutuações de humor ocasionais comuns ao desenvolvimento infantil e juvenil.",
    },
    "Sintomatologia Leve (ou sem sintomas clinicamente relevantes)": {
        "geral": "Os resultados sugerem que o avaliado se encontra em um nível de sintomatologia leve.",
        "nivel": "leve",
        "descricao": "Essa categoria pode expressar a presença de alguns sintomas que podem causar sofrimento psicológico, mas que, na maioria das vezes, não necessariamente limitam a execução de tarefas do cotidiano, considerando que é relativamente esperado que crianças e adolescentes apresentem alguns sintomas avaliados pela EBADEP-IJ, mesmo sem hipótese diagnóstica de transtornos depressivos.",
    },
    "Sintomatologia Moderada": {
        "geral": "Os resultados indicam a presença de sintomatologia em nível moderado.",
        "nivel": "moderado",
        "descricao": "Essa categoria expressa a presença de diversos sintomas que podem estar impactando o cotidiano do avaliado, sugerindo sofrimento psíquico que requer atenção clínica e possivelmente intervenção terapêutica.",
    },
    "Sintomatologia Grave ou Severa": {
        "geral": "Os resultados indicam a presença de sintomatologia em nível grave ou severo.",
        "nivel": "grave/severo",
        "descricao": "Essa categoria expressa um quadro clínico com sofrimento psíquico intenso e prejuízo funcional significativo, exigindo intervenção profissional imediata e acompanhamento especializado prioritário.",
    },
}

SYNTHESIS_LEVELS = {
    "Sintomatologia mínima": "muito positivo",
    "Sintomatologia mínima (presença de indicadores isolados)": "positivo",
    "Sintomatologia Leve (ou sem sintomas clinicamente relevantes)": "com indicadores leves de sintomatologia",
    "Sintomatologia Moderada": "com indicadores moderados de sintomatologia",
    "Sintomatologia Grave ou Severa": "com indicadores significativos de sintomatologia",
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
