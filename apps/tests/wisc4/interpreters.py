TITLE = "Interpretação e Observações Clínicas"

INDEX_DEFINITIONS = {
    "qit": "O Coeficiente de Inteligência Total representa a estimativa mais abrangente do funcionamento intelectual global, derivada da combinação dos principais subtestes do WISC-IV.",
    "icv": "O Índice de Compreensão Verbal avalia raciocínio verbal, abstração mediada pela linguagem, formação de conceitos, compreensão verbal e utilização de conhecimentos previamente adquiridos.",
    "iop": "O Índice de Organização Perceptual avalia raciocínio não verbal, percepção e organização visual, análise visuoespacial, integração visuoconstrutiva e resolução de problemas a partir de estímulos perceptuais.",
    "imt": "O Índice de Memória Operacional avalia a capacidade de sustentar a atenção, reter informações temporariamente, manipulá-las mentalmente e exercer controle cognitivo durante a execução de tarefas.",
    "ivp": "O Índice de Velocidade de Processamento avalia a rapidez e a eficiência com que estímulos visuais simples são processados sob exigência de precisão, envolvendo atenção visual sustentada, rastreamento perceptivo e coordenação visuomotora.",
    "gai": "O Índice de Habilidade Geral representa uma estimativa do potencial global de raciocínio, com menor influência da memória operacional e da velocidade de processamento.",
    "cpi": "O Índice de Proficiência Cognitiva avalia a eficiência cognitiva operacional, especialmente nos mecanismos relacionados à memória de trabalho e à velocidade de processamento.",
}

QIT_TEMPLATES = {
    "Muito Superior": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Muito Superior, indicando funcionamento intelectual global substancialmente acima da média esperada para a faixa etária.",
    "Superior": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Superior, indicando funcionamento intelectual global acima da média esperada para a faixa etária.",
    "Média Superior": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Média Superior, indicando funcionamento intelectual global discretamente acima da média esperada para a faixa etária.",
    "Média": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Média, indicando funcionamento intelectual global dentro dos limites esperados para a faixa etária.",
    "Média Inferior": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa de Média Inferior, indicando funcionamento intelectual global abaixo da média esperada para a faixa etária.",
    "Limítrofe": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Limítrofe, indicando rebaixamento importante do funcionamento intelectual global em comparação ao esperado para a faixa etária.",
    "Inferior": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Inferior, indicando comprometimento relevante do funcionamento intelectual global.",
    "Extremamente Baixo": "O Coeficiente de Inteligência Total (QIT = {score}) foi classificado na faixa Extremamente Baixa, indicando comprometimento expressivo do funcionamento intelectual global, muito abaixo do esperado para a faixa etária.",
}

INDEX_TEMPLATES = {
    "icv": {
        "Muito Superior": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho situou-se na faixa Muito Superior, sugerindo repertório verbal amplamente desenvolvido e elevada eficiência em tarefas de abstração verbal, formação de conceitos e raciocínio mediado pela linguagem.",
        "Superior": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho situou-se na faixa Superior, sugerindo repertório verbal bem desenvolvido e bom desempenho em tarefas de abstração verbal, formação de conceitos e raciocínio mediado pela linguagem.",
        "Média Superior": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho situou-se na faixa Média Superior, sugerindo repertório verbal acima da média, com recursos adequados para compreensão de conceitos, abstração verbal e raciocínio mediado pela linguagem.",
        "Média": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho situou-se na faixa Média, sugerindo repertório verbal preservado, com recursos adequados para compreensão de conceitos, abstração verbal, formação de categorias e raciocínio mediado pela linguagem.",
        "Média Inferior": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho situou-se na faixa de Média Inferior, sugerindo fragilidade leve no repertório verbal e menor eficiência em tarefas que exigem abstração verbal, compreensão conceitual e raciocínio mediado pela linguagem.",
        "Limítrofe": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho foi classificado na faixa Limítrofe, sugerindo rebaixamento importante nas habilidades verbais, com impacto sobre a compreensão de conceitos, a abstração verbal e o raciocínio mediado pela linguagem.",
        "Inferior": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho foi classificado na faixa Inferior, evidenciando comprometimento relevante nas habilidades de raciocínio verbal, formação de conceitos e compreensão mediada pela linguagem.",
        "Extremamente Baixo": "No Índice de Compreensão Verbal (ICV = {score}), o desempenho foi classificado na faixa Extremamente Baixa, indicando comprometimento expressivo do repertório verbal, com fragilidade acentuada na compreensão conceitual e no raciocínio mediado pela linguagem.",
    },
    "iop": {
        "Muito Superior": "No Índice de Organização Perceptual (IOP = {score}), o desempenho situou-se na faixa Muito Superior, indicando recursos muito desenvolvidos em raciocínio não verbal, análise visuoespacial e resolução de problemas a partir de estímulos perceptuais.",
        "Superior": "No Índice de Organização Perceptual (IOP = {score}), o desempenho situou-se na faixa Superior, indicando bom desenvolvimento em raciocínio não verbal, análise visuoespacial e resolução de problemas a partir de estímulos perceptuais.",
        "Média Superior": "No Índice de Organização Perceptual (IOP = {score}), o desempenho situou-se na faixa Média Superior, indicando recursos acima da média em raciocínio não verbal, análise visuoespacial e organização perceptual.",
        "Média": "No Índice de Organização Perceptual (IOP = {score}), o desempenho situou-se na faixa Média, indicando funcionamento adequado no raciocínio não verbal, na análise visuoespacial e na resolução de problemas a partir de estímulos perceptuais.",
        "Média Inferior": "No Índice de Organização Perceptual (IOP = {score}), o desempenho foi classificado na faixa de Média Inferior, sugerindo fragilidade no raciocínio não verbal, na análise visuoespacial e na resolução de problemas baseados em estímulos perceptuais.",
        "Limítrofe": "No Índice de Organização Perceptual (IOP = {score}), o desempenho foi classificado na faixa Limítrofe, evidenciando fragilidade importante no raciocínio não verbal, na análise visuoespacial e na integração visuoconstrutiva.",
        "Inferior": "No Índice de Organização Perceptual (IOP = {score}), o desempenho foi classificado na faixa Inferior, evidenciando fragilidade importante no raciocínio não verbal, na análise visuoespacial e na resolução de problemas a partir de estímulos perceptuais.",
        "Extremamente Baixo": "No Índice de Organização Perceptual (IOP = {score}), o desempenho foi classificado na faixa Extremamente Baixa, indicando comprometimento expressivo nas habilidades de organização perceptual, raciocínio não verbal e integração visuoespacial.",
    },
    "imt": {
        "Muito Superior": "No Índice de Memória Operacional (IMO = {score}), o desempenho situou-se na faixa Muito Superior, indicando excelente capacidade de retenção, manipulação mental de informações e controle cognitivo em curto prazo.",
        "Superior": "No Índice de Memória Operacional (IMO = {score}), o desempenho situou-se na faixa Superior, indicando boa capacidade de retenção, manipulação mental de informações e controle cognitivo em curto prazo.",
        "Média Superior": "No Índice de Memória Operacional (IMO = {score}), o desempenho situou-se na faixa Média Superior, sugerindo recursos acima da média para retenção, manipulação e reorganização mental de informações em curto prazo.",
        "Média": "No Índice de Memória Operacional (IMO = {score}), o desempenho situou-se na faixa Média, indicando funcionamento adequado em tarefas que exigem retenção, manipulação e reorganização mental de informações em curto prazo.",
        "Média Inferior": "No Índice de Memória Operacional (IMO = {score}), o desempenho foi classificado na faixa de Média Inferior, indicando vulnerabilidade em tarefas que exigem retenção, manipulação e reorganização mental de informações em curto prazo.",
        "Limítrofe": "No Índice de Memória Operacional (IMO = {score}), o desempenho foi classificado na faixa Limítrofe, sugerindo rebaixamento importante nos mecanismos de memória de trabalho, controle mental e sustentação atencional.",
        "Inferior": "No Índice de Memória Operacional (IMO = {score}), o desempenho foi classificado na faixa Inferior, indicando comprometimento relevante em tarefas que exigem memória de trabalho, controle mental e manutenção ativa da atenção.",
        "Extremamente Baixo": "No Índice de Memória Operacional (IMO = {score}), o desempenho foi classificado na faixa Extremamente Baixa, evidenciando comprometimento expressivo na retenção e manipulação mental de informações em curto prazo.",
    },
    "ivp": {
        "Muito Superior": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho situou-se na faixa Muito Superior, indicando elevada rapidez e eficiência no processamento de estímulos visuais simples sob exigência de precisão.",
        "Superior": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho situou-se na faixa Superior, indicando boa rapidez e eficiência no processamento de estímulos visuais simples sob exigência de precisão.",
        "Média Superior": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho situou-se na faixa Média Superior, sugerindo eficiência acima da média no processamento de estímulos visuais simples sob exigência de rapidez e precisão.",
        "Média": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho situou-se na faixa Média, indicando eficiência adequada no processamento de estímulos visuais simples sob exigência de rapidez e precisão.",
        "Média Inferior": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho foi classificado na faixa de Média Inferior, indicando lentificação relativa no processamento de estímulos visuais simples sob exigência de rapidez e precisão.",
        "Limítrofe": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho foi classificado na faixa Limítrofe, sugerindo rebaixamento importante na velocidade de execução e na eficiência do processamento visual sob pressão de tempo.",
        "Inferior": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho foi classificado na faixa Inferior, indicando comprometimento relevante na rapidez de processamento visual e na execução eficiente de tarefas simples sob limite de tempo.",
        "Extremamente Baixo": "Em relação ao Índice de Velocidade de Processamento (IVP = {score}), o desempenho foi classificado na faixa Extremamente Baixa, indicando comprometimento expressivo na velocidade de processamento e na resposta eficiente a estímulos visuais simples.",
    },
}

FUNCTIONAL_COMPLEMENTS = {
    "icv": {
        "high": "Esse resultado indica boa capacidade para compreender instruções, expressar-se verbalmente e utilizar conhecimentos previamente adquiridos na resolução de problemas, constituindo área de melhor recurso intelectual relativo.",
        "average": "Esse resultado indica capacidade satisfatória para compreender instruções, expressar-se verbalmente e utilizar conhecimentos previamente adquiridos na resolução de problemas.",
        "low": "Esse resultado sugere que tarefas dependentes de compreensão verbal, abstração conceitual e elaboração de respostas mediadas pela linguagem podem exigir maior esforço cognitivo.",
    },
    "iop": {
        "high": "Esse resultado sugere boa eficiência em tarefas que demandam análise visuoespacial, raciocínio prático e organização perceptual.",
        "average": "Esse resultado sugere desempenho funcional adequado em tarefas que envolvem percepção visual, organização espacial e solução prática de problemas.",
        "low": "Esse achado pode repercutir negativamente em situações acadêmicas que demandem interpretação visual, matemática, organização espacial e solução prática de problemas.",
    },
    "imt": {
        "high": "Esse resultado sugere boa capacidade para lidar com instruções sequenciais, cálculo mental, controle atencional e manipulação ativa de informações.",
        "average": "Esse resultado sugere funcionamento adequado nas demandas que envolvem memória de trabalho, controle mental e sustentação da atenção.",
        "low": "Esse resultado sugere que atividades que dependem de controle mental, acompanhamento de instruções sequenciais, cálculo mental, resistência à distração e manutenção ativa da atenção tendem a exigir maior esforço cognitivo.",
    },
    "ivp": {
        "high": "Esse desempenho sugere boa eficiência em tarefas automatizadas que dependem de atenção visual, rastreamento perceptivo rápido e resposta gráfica sob limite de tempo.",
        "average": "Esse desempenho sugere eficiência adequada em tarefas automatizadas que dependem de atenção visual sustentada, rastreamento perceptivo e rapidez de execução.",
        "low": "Esse resultado sugere menor eficiência em tarefas automatizadas que dependem de atenção visual sustentada, rastreamento perceptivo rápido e resposta gráfica sob pressão de tempo, podendo contribuir para lentidão na execução de atividades escolares e em contextos que exigem agilidade de resposta.",
    },
}

GAI_TEMPLATES = {
    "Muito Superior": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Muito Superior, sugere potencial global de raciocínio amplamente desenvolvido.",
    "Superior": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Superior, sugere potencial global de raciocínio acima da média esperada.",
    "Média Superior": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Média Superior, sugere potencial global de raciocínio discretamente acima da média esperada.",
    "Média": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Média, sugere potencial global de raciocínio dentro da faixa esperada.",
    "Média Inferior": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa de Média Inferior, sugere potencial de raciocínio global discretamente rebaixado.",
    "Limítrofe": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Limítrofe, sugere rebaixamento importante do potencial global de raciocínio.",
    "Inferior": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Inferior, sugere comprometimento relevante do potencial global de raciocínio.",
    "Extremamente Baixo": "O Índice de Habilidade Geral (GAI = {score}), classificado na faixa Extremamente Baixa, indica comprometimento expressivo do potencial global de raciocínio.",
}

CPI_TEMPLATES = {
    "Muito Superior": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Muito Superior, indicando elevada eficiência cognitiva operacional.",
    "Superior": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Superior, indicando boa eficiência cognitiva operacional.",
    "Média Superior": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Média Superior, indicando eficiência cognitiva operacional acima da média.",
    "Média": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Média, indicando eficiência cognitiva operacional dentro do esperado.",
    "Média Inferior": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa de Média Inferior, indicando menor eficiência cognitiva operacional.",
    "Limítrofe": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Limítrofe, indicando comprometimento mais acentuado nos mecanismos relacionados à eficiência cognitiva, especialmente na memória de trabalho e na rapidez para processar informações.",
    "Inferior": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Inferior, indicando comprometimento relevante da eficiência cognitiva operacional.",
    "Extremamente Baixo": "Já o Índice de Proficiência Cognitiva (CPI = {score}) situou-se na faixa Extremamente Baixa, indicando comprometimento expressivo da eficiência cognitiva operacional.",
}


def _first_name(name: str) -> str:
    return (name or "Paciente").split(" ", 1)[0]


def _classification_bucket(classificacao: str) -> str:
    if classificacao in {"Muito Superior", "Superior", "Média Superior"}:
        return "high"
    if classificacao == "Média":
        return "average"
    return "low"


def _index_map(merged_data: dict) -> dict:
    return {item.get("indice"): item for item in merged_data.get("indices", [])}


def _max_difference(indices: dict) -> int:
    scores = [
        item.get("escore_composto")
        for key, item in indices.items()
        if key in {"icv", "iop", "imt", "ivp"} and item.get("escore_composto")
    ]
    if len(scores) < 2:
        return 0
    return max(scores) - min(scores)


def _profile_analysis(indices: dict) -> str:
    difference = _max_difference(indices)
    parts = []
    if difference >= 15:
        parts.append(
            "A análise dos índices revela um perfil cognitivo heterogêneo, com discrepâncias clinicamente relevantes entre os domínios avaliados."
        )
    else:
        parts.append(
            "A análise dos índices revela um perfil cognitivo relativamente homogêneo, sem discrepâncias clinicamente relevantes entre os domínios avaliados."
        )

    ordered = sorted(
        (
            (key, item.get("escore_composto", 0))
            for key, item in indices.items()
            if key in {"icv", "iop", "imt", "ivp"}
        ),
        key=lambda entry: entry[1],
        reverse=True,
    )
    if len(ordered) >= 2 and ordered[0][1] - ordered[-1][1] >= 15:
        highest, lowest = ordered[0][0], ordered[-1][0]
        if highest == "icv":
            parts.append(
                "Observa-se melhor desempenho relativo nas habilidades verbais, que se mostraram mais preservadas em comparação aos demais domínios cognitivos."
            )
        if lowest == "iop":
            parts.append(
                "Em contrapartida, os recursos de raciocínio perceptual e organização visuoespacial configuram área de maior fragilidade relativa dentro do perfil avaliado."
            )
        if lowest == "imt":
            parts.append(
                "Destaca-se, ainda, fragilidade relativa nos mecanismos de memória operacional e controle mental, sugerindo maior vulnerabilidade em tarefas de retenção e manipulação ativa de informações."
            )
        if lowest == "ivp":
            parts.append(
                "Também se observa fragilidade relativa na velocidade de processamento, indicando menor eficiência em tarefas simples realizadas sob exigência de rapidez e precisão."
            )

    return " ".join(parts)


def _index_paragraph(index_code: str, index_data: dict) -> str:
    classificacao = index_data.get("classificacao", "Média")
    score = index_data.get("escore_composto", 0)
    template = INDEX_TEMPLATES[index_code][classificacao]
    complement = FUNCTIONAL_COMPLEMENTS[index_code][
        _classification_bucket(classificacao)
    ]
    return f"{template.format(score=score)} {complement}"


def _gai_cpi_paragraph(merged_data: dict) -> str:
    gai_data = merged_data.get("gai_data") or {}
    cpi_data = merged_data.get("cpi_data") or {}
    if not gai_data.get("escore_composto") or not cpi_data.get("escore_composto"):
        return ""

    parts = [
        GAI_TEMPLATES[gai_data.get("classificacao", "Média")].format(
            score=gai_data.get("escore_composto", 0)
        ),
        CPI_TEMPLATES[cpi_data.get("classificacao", "Média")].format(
            score=cpi_data.get("escore_composto", 0)
        ),
    ]

    difference = gai_data.get("escore_composto", 0) - cpi_data.get("escore_composto", 0)
    if difference >= 8:
        parts.append(
            "Essa diferença entre GAI e CPI sugere um perfil em que o raciocínio global, embora possa apresentar fragilidades, mostra-se relativamente mais preservado do que a eficiência operacional necessária para sustentar o desempenho em tarefas com maior exigência atencional, rapidez e gerenciamento simultâneo de informações."
        )
    elif difference <= -8:
        parts.append(
            "Essa configuração sugere que a eficiência cognitiva operacional encontra-se relativamente mais preservada do que o potencial global de raciocínio."
        )
    else:
        parts.append(
            "A proximidade entre GAI e CPI sugere equilíbrio relativo entre o potencial de raciocínio e a eficiência cognitiva operacional."
        )

    return " ".join(parts)


def _integrated_closing(merged_data: dict) -> str:
    qit = (merged_data.get("qit_data") or {}).get("classificacao", "Média")
    difference = _max_difference(_index_map(merged_data))

    if qit in {"Muito Superior", "Superior", "Média Superior"} and difference < 15:
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global preservado ou acima da média, com recursos intelectuais consistentes e boa capacidade para responder às demandas de raciocínio verbal, não verbal e eficiência cognitiva, sem discrepâncias internas relevantes."
    if qit in {"Muito Superior", "Superior", "Média Superior"}:
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global preservado ou acima da média, porém com oscilações internas significativas entre os domínios avaliados, indicando que determinadas áreas se mostram mais desenvolvidas do que outras dentro do perfil intelectual."
    if qit == "Média" and difference < 15:
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global dentro da faixa esperada para a idade, com perfil intelectual relativamente homogêneo e funcionalmente preservado."
    if qit == "Média":
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global dentro da faixa média, porém com discrepâncias internas clinicamente relevantes, indicando preservação relativa de alguns domínios e maior vulnerabilidade em outros."
    if qit == "Média Inferior" and difference < 15:
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global abaixo da média normativa, com fragilidades distribuídas de forma relativamente homogênea entre os domínios avaliados. Clinicamente, esse padrão pode estar associado a maior esforço para lidar com demandas acadêmicas e cognitivas mais complexas."
    if qit == "Média Inferior":
        return "Em análise clínica, os resultados do WISC-IV sugerem funcionamento cognitivo global abaixo da média normativa, com melhor desempenho relativo em alguns domínios e fragilidades mais expressivas em outros. Clinicamente, esse padrão pode estar associado a dificuldades em situações que exigem raciocínio não verbal, retenção ativa de informações, organização perceptual, execução sequencial de comandos e rapidez na realização de tarefas."
    if difference < 15:
        return "Em análise clínica, os resultados do WISC-IV sugerem rebaixamento importante do funcionamento cognitivo global, com impacto potencial abrangente sobre a aprendizagem, a adaptação acadêmica e o desempenho em tarefas que exigem integração entre raciocínio, memória operacional, atenção e velocidade de processamento."
    return "Em análise clínica, os resultados do WISC-IV sugerem rebaixamento importante do funcionamento cognitivo global, associado a oscilações internas clinicamente relevantes entre os domínios avaliados. Esse padrão indica coexistência de recursos relativamente mais preservados e áreas de maior vulnerabilidade, com potencial repercussão significativa sobre o desempenho acadêmico e funcional."


def interpret_index(indice: str, classificacao: str) -> str:
    template = INDEX_TEMPLATES.get(indice, {}).get(classificacao)
    if not template:
        return "Interpretação não disponível."
    return template.format(score=0)


def interpret_qi(classificacao: str) -> str:
    template = QIT_TEMPLATES.get(classificacao)
    if not template:
        return "Interpretação não disponível."
    return template.format(score=0)


def interpret_wisc4_profile(merged_data: dict, patient_name: str) -> str:
    name = _first_name(patient_name)
    indices = _index_map(merged_data)
    qit_data = merged_data.get("qit_data") or {}
    qit_classificacao = qit_data.get("classificacao", "Média")
    qit_score = qit_data.get("escore_composto", merged_data.get("qi_total", 0))

    parts = [TITLE]
    parts.append(
        f"{INDEX_DEFINITIONS['qit']} {QIT_TEMPLATES[qit_classificacao].format(score=qit_score)} {_profile_analysis(indices)}"
    )
    parts.append(_index_paragraph("icv", indices.get("icv") or {}))
    parts.append(_index_paragraph("iop", indices.get("iop") or {}))
    parts.append(_index_paragraph("imt", indices.get("imt") or {}))
    parts.append(_index_paragraph("ivp", indices.get("ivp") or {}))

    gai_cpi = _gai_cpi_paragraph(merged_data)
    if gai_cpi:
        parts.append(gai_cpi)

    parts.append(_integrated_closing(merged_data))
    return "\n\n".join(parts)
