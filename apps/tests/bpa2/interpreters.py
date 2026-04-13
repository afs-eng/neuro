INTRO_TEMPLATE = (
    "Interpretação e Observações Clínicas: A avaliação da atenção de {name} foi "
    "realizada por meio da Bateria Psicológica para Avaliação da Atenção – BPA-2, "
    "instrumento destinado à investigação dos principais componentes do "
    "funcionamento atencional, incluindo atenção concentrada, dividida, alternada e "
    "atenção geral, domínios associados à sustentação do foco, à distribuição dos "
    "recursos atencionais e ao controle executivo."
)

NOMES_SUBTESTES = {
    "ac": "Atenção Concentrada",
    "ad": "Atenção Dividida",
    "aa": "Atenção Alternada",
    "ag": "Atenção Geral",
}

SECTION_TITLES = {
    "ac": "Atenção Concentrada (AC)",
    "ad": "Atenção Dividida (AD)",
    "aa": "Atenção Alternada (AA)",
    "ag": "Atenção Geral (AG)",
}

SUBTEST_OPENINGS = {
    "ac": {
        "opening": "Avalia a capacidade de selecionar estímulos relevantes e manter o foco atencional diante de estímulos distratores.",
        "Muito Inferior": "{name} apresentou desempenho classificado como muito inferior (percentil {percentil}), indicando comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse resultado sugere dificuldade importante para sustentar a atenção, manter constância do foco e inibir interferências distratoras durante tarefas contínuas.",
        "Inferior": "{name} apresentou desempenho classificado como inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse resultado sugere dificuldade importante para sustentar a atenção, manter constância do foco e inibir interferências distratoras durante tarefas contínuas.",
        "Média Inferior": "{name} apresentou desempenho classificado como média inferior (percentil {percentil}), indicando rebaixamento leve nesse domínio, com sinais de menor eficiência atencional quando comparado ao esperado para a faixa etária. Esse resultado sugere maior suscetibilidade a oscilações do foco atencional em tarefas que exigem concentração prolongada.",
        "Média": "{name} apresentou desempenho classificado como médio (percentil {percentil}), indicando funcionamento atencional dentro dos limites esperados para sua faixa etária, sem evidências de prejuízo significativo nesse domínio. Esse resultado sugere capacidade adequada de concentração sustentada e manutenção do foco diante de demandas contínuas.",
        "Média Superior": "{name} apresentou desempenho classificado como média superior (percentil {percentil}), sugerindo funcionamento atencional acima do esperado, com boa eficiência nesse domínio. Esse resultado sugere boa sustentação do foco e adequada resistência à interferência de estímulos distratores.",
        "Superior": "{name} apresentou desempenho classificado como superior (percentil {percentil}), indicando habilidade muito desenvolvida nesse domínio, com eficiência acima do esperado para sua faixa etária. Esse resultado sugere excelente capacidade de sustentação do foco, elevada resistência à distração e boa constância atencional em tarefas prolongadas.",
        "Muito Superior": "{name} apresentou desempenho classificado como muito superior (percentil {percentil}), indicando desempenho excepcional na capacidade de sustentar a atenção de forma contínua e direcionada, com elevada estabilidade do foco mesmo em contextos de alta exigência.",
    },
    "ad": {
        "opening": "Refere-se à habilidade de distribuir os recursos atencionais entre múltiplos estímulos ou demandas simultâneas.",
        "Muito Inferior": "O desempenho de {name} foi classificado como muito inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse desempenho sugere prejuízo importante na habilidade de processar simultaneamente mais de uma demanda, com possível impacto em situações que exigem monitoramento concorrente de informações.",
        "Inferior": "O desempenho de {name} foi classificado como inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse desempenho sugere prejuízo importante na habilidade de processar simultaneamente mais de uma demanda, com possível impacto em situações que exigem monitoramento concorrente de informações.",
        "Média Inferior": "O desempenho de {name} foi classificado como média inferior (percentil {percentil}), indicando rebaixamento leve nesse domínio, com sinais de menor eficiência atencional quando comparado ao esperado para a faixa etária. Esse desempenho sugere dificuldade discreta a moderada na distribuição dos recursos atencionais entre múltiplas demandas, podendo reduzir a eficiência em situações complexas.",
        "Média": "O desempenho de {name} foi classificado como médio (percentil {percentil}), indicando funcionamento atencional dentro dos limites esperados para sua faixa etária, sem evidências de prejuízo significativo nesse domínio. Esse desempenho indica capacidade preservada para dividir a atenção entre diferentes estímulos ou tarefas simultâneas.",
        "Média Superior": "O desempenho de {name} foi classificado como média superior (percentil {percentil}), sugerindo funcionamento atencional acima do esperado, com boa eficiência nesse domínio. Esse desempenho sugere boa distribuição dos recursos atencionais entre estímulos múltiplos, sem prejuízos relevantes.",
        "Superior": "O desempenho de {name} foi classificado como superior (percentil {percentil}), indicando habilidade muito desenvolvida nesse domínio, com eficiência acima do esperado para sua faixa etária. Esse desempenho evidencia notável capacidade de acompanhar simultaneamente diferentes estímulos e lidar com múltiplas demandas cognitivas com eficiência.",
        "Muito Superior": "O desempenho de {name} foi classificado como muito superior (percentil {percentil}), sugerindo capacidade excepcional para distribuir os recursos atencionais entre estímulos múltiplos, com funcionamento diferenciado em situações de alta complexidade.",
    },
    "aa": {
        "opening": "Mede a capacidade de alternar o foco atencional entre tarefas ou estímulos distintos, exigindo flexibilidade cognitiva e monitoramento contínuo.",
        "Muito Inferior": "{name} apresentou desempenho na faixa muito inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse resultado indica comprometimento importante da alternância atencional, com dificuldade para ajustar o foco mental diante de mudanças de tarefa, regra ou estímulo.",
        "Inferior": "{name} apresentou desempenho na faixa inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. Esse resultado indica comprometimento importante da alternância atencional, com dificuldade para ajustar o foco mental diante de mudanças de tarefa, regra ou estímulo.",
        "Média Inferior": "{name} apresentou desempenho na faixa média inferior (percentil {percentil}), indicando rebaixamento leve nesse domínio, com sinais de menor eficiência atencional quando comparado ao esperado para a faixa etária. Esse resultado indica redução na flexibilidade atencional e menor eficiência para mudar o foco entre diferentes demandas cognitivas.",
        "Média": "{name} apresentou desempenho na faixa média (percentil {percentil}), indicando funcionamento atencional dentro dos limites esperados para sua faixa etária, sem evidências de prejuízo significativo nesse domínio. Esse resultado indica capacidade preservada para alternar o foco atencional entre diferentes demandas, sem prejuízos significativos.",
        "Média Superior": "{name} apresentou desempenho na faixa média superior (percentil {percentil}), sugerindo funcionamento atencional acima do esperado, com boa eficiência nesse domínio. Esse resultado sugere boa flexibilidade cognitiva e eficiência na alternância do foco entre tarefas ou estímulos distintos.",
        "Superior": "{name} apresentou desempenho na faixa superior (percentil {percentil}), indicando habilidade muito desenvolvida nesse domínio, com eficiência acima do esperado para sua faixa etária. Esse resultado evidencia elevada flexibilidade atencional, com boa capacidade de ajustar-se rapidamente a mudanças de regras, estímulos ou exigências da tarefa.",
        "Muito Superior": "{name} apresentou desempenho na faixa muito superior (percentil {percentil}), indicando flexibilidade atencional excepcional e elevada eficiência para mudar rapidamente o foco entre diferentes demandas cognitivas.",
    },
    "ag": {
        "opening": "Representa a integração global dos componentes atencionais avaliados, sintetizando o funcionamento geral da atenção.",
        "Muito Inferior": "O desempenho foi classificado como muito inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. De forma global, observa-se comprometimento do funcionamento atencional, com impacto conjunto sobre a sustentação, distribuição e alternância do foco atencional.",
        "Inferior": "O desempenho foi classificado como inferior (percentil {percentil}), sugerindo comprometimento relevante nesse domínio, com prejuízo atencional clinicamente significativo. De forma global, observa-se comprometimento do funcionamento atencional, com impacto conjunto sobre a sustentação, distribuição e alternância do foco atencional.",
        "Média Inferior": "O desempenho foi classificado como média inferior (percentil {percentil}), indicando rebaixamento leve nesse domínio, com sinais de menor eficiência atencional quando comparado ao esperado para a faixa etária. De forma global, observa-se funcionamento atencional discretamente rebaixado, sugerindo fragilidade na integração entre os diferentes componentes da atenção.",
        "Média": "O desempenho foi classificado como médio (percentil {percentil}), indicando funcionamento atencional dentro dos limites esperados para sua faixa etária, sem evidências de prejuízo significativo nesse domínio. De forma global, o funcionamento atencional encontra-se preservado, com integração adequada entre os diferentes componentes avaliados.",
        "Média Superior": "O desempenho foi classificado como média superior (percentil {percentil}), sugerindo funcionamento atencional acima do esperado, com boa eficiência nesse domínio. De forma global, o funcionamento atencional mostra-se acima do esperado, com boa integração entre os diferentes componentes da atenção.",
        "Superior": "O desempenho foi classificado como superior (percentil {percentil}), indicando habilidade muito desenvolvida nesse domínio, com eficiência acima do esperado para sua faixa etária. De forma global, o funcionamento atencional mostra-se muito bem desenvolvido, com integração eficiente entre os diferentes componentes avaliados.",
        "Muito Superior": "O desempenho foi classificado como muito superior (percentil {percentil}), sugerindo funcionamento atencional global excepcional, com integração diferenciada entre os diversos componentes avaliados.",
    },
}


def build_report_intro(name: str) -> str:
    return INTRO_TEMPLATE.format(name=name)


def get_report_interpretation(code: str, classificacao: str, nome: str) -> str:
    return build_subtest_paragraph(code, classificacao, 0, nome.split(" ", 1)[0])


def get_synthesis(classificacao: str) -> str:
    if classificacao in {"Muito Inferior", "Inferior", "Média Inferior"}:
        return (
            "Perfil atencional global rebaixado, com prejuízo clinicamente relevante."
        )
    if classificacao == "Média":
        return "Perfil atencional global compatível com o esperado para a faixa etária."
    return "Perfil atencional global acima do esperado, com recursos atencionais preservados."


def build_subtest_paragraph(
    code: str, classificacao: str, percentil: int | float, name: str
) -> str:
    descriptions = SUBTEST_OPENINGS.get(code, {})
    opening = descriptions.get("opening")
    description = descriptions.get(classificacao)
    title = SECTION_TITLES.get(code)
    if not title or not opening or not description:
        return "Interpretação não disponível."
    return f"{title}\n{opening} {description.format(name=name, percentil=percentil)}"


def build_clinical_summary(subtests: list[dict], name: str) -> str:
    by_code = {item.get("codigo"): item for item in subtests}
    ag_classificacao = (by_code.get("ag") or {}).get("classificacao", "")
    ac = (by_code.get("ac") or {}).get("classificacao", "")
    ad = (by_code.get("ad") or {}).get("classificacao", "")
    aa = (by_code.get("aa") or {}).get("classificacao", "")

    preserved = {"Média", "Média Superior", "Superior"}
    lowered = {"Média Inferior", "Inferior", "Muito Inferior"}
    specific = [ac, ad, aa]
    lowered_count = sum(1 for item in specific if item in lowered)
    preserved_count = sum(1 for item in specific if item in preserved)

    if ag_classificacao in preserved and preserved_count == 3:
        return (
            f"Em análise clínica, o perfil atencional de {name} revela funcionamento global dentro ou acima do esperado para a faixa etária, "
            "com adequada integração entre sustentação do foco, divisão dos recursos atencionais e alternância entre estímulos. "
            "Os achados não indicam prejuízo atencional clinicamente relevante no momento da avaliação."
        )

    if ag_classificacao in {"Média", "Média Superior"} and lowered_count >= 1:
        return (
            f"Em análise clínica, o perfil atencional de {name} revela funcionamento global preservado, embora com fragilidades pontuais em componentes específicos da atenção. "
            "Esse padrão sugere que, apesar da integração global mostrar-se adequada, determinadas exigências cognitivas podem ser realizadas com maior esforço, especialmente em contextos de maior complexidade ou sobrecarga ambiental."
        )

    if ag_classificacao in {"Média Inferior", "Inferior"} and preserved_count >= 1:
        return (
            f"Em análise clínica, o perfil atencional de {name} revela que, embora alguns componentes específicos tenham se mantido dentro da faixa esperada, a integração global desses recursos mostrou-se menos eficiente. "
            "Esse padrão sugere fragilidade no funcionamento atencional como um todo, com possível oscilação no desempenho diante de tarefas prolongadas, múltiplas demandas ou necessidade de adaptação rápida."
        )

    if ag_classificacao == "Média Inferior" and lowered_count >= 2:
        return (
            f"Em análise clínica, o perfil atencional de {name} revela funcionamento global discretamente rebaixado, com fragilidades mais abrangentes nos mecanismos de sustentação, distribuição e alternância do foco atencional. "
            "Os achados sugerem menor eficiência para lidar com tarefas contínuas, múltiplos estímulos e situações que exigem ajuste mental frequente."
        )

    if ag_classificacao == "Inferior" and lowered_count >= 2:
        return (
            f"Em análise clínica, o perfil atencional de {name} revela funcionamento global rebaixado, com prejuízo clinicamente relevante nos mecanismos de sustentação do foco, distribuição dos recursos atencionais e alternância entre estímulos. "
            "Em contexto funcional, esse padrão pode se associar a dificuldades para manter a concentração em tarefas prolongadas, acompanhar comandos com múltiplas etapas, alternar entre atividades e sustentar desempenho consistente diante de demandas cognitivas contínuas."
        )

    if (
        ag_classificacao in {"Superior", "Média Superior"}
        and sum(1 for item in specific if item in {"Superior", "Média Superior"}) >= 2
    ):
        return (
            f"Em análise clínica, o perfil atencional de {name} revela funcionamento global eficiente, com bom controle do foco atencional, adequada distribuição dos recursos cognitivos e flexibilidade para alternar entre diferentes demandas. "
            "Os achados sugerem recursos atencionais bem desenvolvidos e funcionalmente adaptativos."
        )

    return (
        f"Em análise clínica, o perfil atencional de {name} deve ser interpretado de forma integrada, considerando o peso maior da atenção geral e a variação observada nos componentes específicos. "
        "Os achados sugerem que o funcionamento atencional pode oscilar conforme a complexidade da tarefa, a necessidade de sustentar o foco e a exigência de adaptação entre diferentes demandas cognitivas."
    )
