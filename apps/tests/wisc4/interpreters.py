INDEX_INTERPRETATIONS = {
    "icv": {
        "Muito Baixo": "Habilidades verbais significativamente abaixo do esperado, indicando possíveis dificuldades na compreensão e expressão de conceitos verbais.",
        "Baixo": "Habilidades verbais abaixo do esperado, com dificuldades em raciocínio verbal e formação de conceitos.",
        "Médio": "Habilidades verbais dentro do esperado para a faixa etária.",
        "Médio-Alto": "Boas habilidades verbais, com raciocínio verbal acima da média.",
        "Superior": "Excelentes habilidades verbais, demonstrando forte capacidade de raciocínio verbal e formação de conceitos.",
    },
    "iop": {
        "Muito Baixo": "Habilidades de organização perceptual significativamente comprometidas.",
        "Baixo": "Dificuldades em tarefas que exigem integração perceptual e raciocínio não-verbal.",
        "Médio": "Capacidade de organização perceptual adequada para a faixa etária.",
        "Médio-Alto": "Boas habilidades de organização perceptual e raciocínio não-verbal.",
        "Superior": "Excelentes habilidades de integração perceptual e raciocínio não-verbal.",
    },
    "imt": {
        "Muito Baixo": "Memória de trabalho significativamente comprometida, podendo impactar aprendizagem.",
        "Baixo": "Dificuldades na retenção e manipulação de informações na memória de curto prazo.",
        "Médio": "Memória de trabalho dentro dos parâmetros esperados.",
        "Médio-Alto": "Boa capacidade de memória de trabalho.",
        "Superior": "Excelente capacidade de retenção e manipulação de informações.",
    },
    "ivp": {
        "Muito Baixo": "Velocidade de processamento significativamente reduzida.",
        "Baixo": "Dificuldades na rapidez de processamento de informações visuais simples.",
        "Médio": "Velocidade de processamento adequada para a faixa etária.",
        "Médio-Alto": "Boa velocidade de processamento de informações.",
        "Superior": "Excelente rapidez no processamento de informações visuais.",
    },
}


def get_classification_group(classificacao: str) -> str:
    if "Muito Superior" in classificacao:
        return "Superior"
    elif "Média Superior" in classificacao:
        return "Médio-Alto"
    elif "Superior" in classificacao or "Médio-Alto" in classificacao:
        return "Médio-Alto"
    elif "Médio" in classificacao or "Média" in classificacao:
        return "Médio"
    elif "Limítrofe" in classificacao:
        return "Baixo"
    else:
        # Extremamente Baixo, Dificuldade Grave, Dificuldade Moderada, Dificuldade Leve
        return "Muito Baixo"


def interpret_index(indice: str, classificacao: str) -> str:
    group = get_classification_group(classificacao)
    interpretations = INDEX_INTERPRETATIONS.get(indice, {})
    return interpretations.get(group, "Interpretação não disponível.")


def interpret_qi(classificacao: str) -> str:
    group = get_classification_group(classificacao)
    if group == "Superior":
        return "O funcionamento intelectual global está significativamente acima da média, indicando capacidades cognitivas elevadas."
    elif group == "Médio-Alto":
        return "O funcionamento intelectual global está acima da média."
    elif group == "Médio":
        return "O funcionamento intelectual global encontra-se dentro dos parâmetros esperados para a faixa etária."
    elif group == "Baixo":
        return "O funcionamento intelectual global está abaixo do esperado, podendo indicar dificuldades cognitivas que necessitam acompanhamento."
    else:
        return "O funcionamento intelectual global está significativamente abaixo do esperado, indicando necessidade de intervenção e acompanhamento especializado."
