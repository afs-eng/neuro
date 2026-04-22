PRESERVED_CLASSIFICATIONS = {"Media", "Media Superior", "Superior", "Muito Superior"}
def _first_name(patient_name: str | None) -> str:
    if not patient_name:
        return "o paciente"
    return patient_name.strip().split()[0] or "o paciente"


def _metrics_by_code(merged_data: dict) -> dict:
    return {
        item.get("codigo"): item for item in merged_data.get("metric_results", []) if item.get("codigo")
    }


def _is_preserved(item: dict | None) -> bool:
    return (item or {}).get("classificacao") in PRESERVED_CLASSIFICATIONS
def _join_labels(labels: list[str]) -> str:
    if not labels:
        return ""
    if len(labels) == 1:
        return labels[0]
    if len(labels) == 2:
        return f"{labels[0]} e {labels[1]}"
    return f"{', '.join(labels[:-1])} e {labels[-1]}"


def _classification_phrase(item: dict | None) -> str:
    classification = (item or {}).get("classificacao", "")
    if classification in {"Muito Inferior", "Inferior", "Media Inferior"}:
        return "indicativo de déficit"
    if classification in {"Media Superior", "Superior", "Muito Superior"}:
        return "desempenho acima da média"
    return "desempenho dentro da média"


def _automatic_paragraph(patient_name: str, metrics: dict, errors: dict) -> str:
    leitura = metrics.get("leitura")
    contagem = metrics.get("contagem")
    leitura_ok = _is_preserved(leitura)
    contagem_ok = _is_preserved(contagem)
    automatic_errors = (errors.get("leitura", {}).get("qtde_erros", 0) + errors.get("contagem", {}).get("qtde_erros", 0))
    error_text = "sem erros" if automatic_errors == 0 else "com baixa ocorrência de erros" if automatic_errors <= 2 else "com presença de erros"

    if leitura_ok and contagem_ok:
        precision_text = "precisa" if automatic_errors == 0 else "adequada"
        return (
            f"Nos processos automáticos, os desempenhos em Leitura e Contagem foram classificados como sem indicativo de déficit, "
            f"com execução {precision_text} e {error_text}, sugerindo automatização preservada e velocidade de processamento adequada em tarefas de baixa demanda executiva."
        )

    changed = []
    preserved = []
    for code, label in (("leitura", "Leitura"), ("contagem", "Contagem")):
        item = metrics.get(code)
        if _is_preserved(item):
            preserved.append(label)
        else:
            changed.append(label)

    if preserved and changed:
        changed_labels = []
        for code, label in (("leitura", "Leitura"), ("contagem", "Contagem")):
            item = metrics.get(code)
            if code in {"leitura", "contagem"} and not _is_preserved(item):
                changed_labels.append(f"{label} com {_classification_phrase(item)}")
        return (
            f"Nos processos automáticos, {patient_name} apresentou desempenho preservado em {_join_labels(preserved)}, enquanto "
            f"{_join_labels(changed_labels)} sugeriu oscilação na eficiência do processamento automático. Esse perfil indica que a automatização não se encontra homogênea entre as tarefas de leitura e contagem."
        )

    return (
        f"Nos processos automáticos, observaram-se dificuldades em {_join_labels(changed or ['Leitura e Contagem'])}, indicando lentificação no processamento de estímulos altamente automatizados e possível redução da eficiência em tarefas de baixa complexidade executiva. "
        f"Esse padrão sugere comprometimento na rapidez de resposta e menor fluidez no processamento automático."
    )


def _controlled_paragraph(patient_name: str, metrics: dict, errors: dict) -> str:
    controlled_codes = [
        ("escolha", "Escolha"),
        ("alternancia", "Alternância"),
        ("inibicao", "Inibição"),
        ("flexibilidade", "Flexibilidade"),
    ]
    controlled_errors = errors.get("escolha", {}).get("qtde_erros", 0) + errors.get("alternancia", {}).get("qtde_erros", 0)
    precision_text = "ausência de erros" if controlled_errors == 0 else "boa precisão" if controlled_errors <= 2 else "presença de erros"

    if all(_is_preserved(metrics.get(code)) for code, _ in controlled_codes):
        return (
            f"Nos processos controlados, {patient_name} apresentou desempenho sem indicativo de déficit em Escolha, Alternância, Inibição e Flexibilidade, com {precision_text} e tempos compatíveis ou mais eficientes que a média esperada. "
            f"Esse padrão indica preservação da capacidade de seleção de respostas, alternância entre regras, supressão de respostas automáticas inadequadas e adaptação cognitiva diante de mudanças de demanda."
        )

    return (
        "Nos processos controlados, observaram-se dificuldades em Escolha, Alternância, Inibição e/ou Flexibilidade, sugerindo rebaixamento na capacidade de selecionar respostas relevantes, alternar critérios mentais, inibir respostas automáticas inadequadas e adaptar-se com eficiência a mudanças de regra. "
        "Esse padrão é compatível com fragilidades no controle executivo e na autorregulação cognitiva."
    )


def _controlled_mixed_paragraph(patient_name: str, metrics: dict) -> str:
    controlled_codes = {
        "escolha": "Escolha",
        "alternancia": "Alternância",
        "inibicao": "Inibição",
        "flexibilidade": "Flexibilidade",
    }
    preserved = [label for code, label in controlled_codes.items() if _is_preserved(metrics.get(code))]
    changed = [label for code, label in controlled_codes.items() if not _is_preserved(metrics.get(code))]
    fragility_map = {
        "Escolha": "seleção de respostas",
        "Alternância": "alternância",
        "Inibição": "controle inibitório",
        "Flexibilidade": "flexibilidade",
    }
    fragilities = [fragility_map[label] for label in changed if label in fragility_map]
    return (
        f"Nos processos controlados, {patient_name} demonstrou desempenho preservado em {_join_labels(preserved)}, porém apresentou indicativo de déficit em {_join_labels(changed)}. "
        f"Esse perfil sugere funcionamento executivo parcial, com preservação de alguns componentes do controle cognitivo, mas com fragilidades em {_join_labels(fragilities)}."
    )


def _errors_paragraph(errors: dict) -> str:
    automatic_errors = errors.get("leitura", {}).get("qtde_erros", 0) + errors.get("contagem", {}).get("qtde_erros", 0)
    controlled_errors = errors.get("escolha", {}).get("qtde_erros", 0) + errors.get("alternancia", {}).get("qtde_erros", 0)
    total_errors = automatic_errors + controlled_errors

    if total_errors == 0:
        return "A ausência de erros em todas as etapas reforça boa precisão, controle da resposta e monitoramento executivo, sem marcadores de impulsividade, desorganização ou instabilidade cognitiva durante a execução."
    if total_errors >= 8:
        return "A frequência elevada de erros reforça a presença de prejuízos no monitoramento executivo, na precisão da resposta e na capacidade de autorregulação cognitiva, apontando para execução pouco consistente, com sinais de impulsividade e dificuldade de manutenção do controle atencional ao longo da tarefa."
    if automatic_errors > 0 and controlled_errors == 0:
        return "Os erros observados nos processos automáticos sugerem redução da precisão em tarefas de resposta mais imediata, podendo indicar instabilidade atencional basal, lentificação associada a perda de rastreio visual ou menor consistência na automatização de respostas simples."
    if controlled_errors > 0 and automatic_errors == 0:
        return "Os erros observados nas etapas de maior demanda executiva sugerem dificuldade de monitoramento, controle inibitório e regulação da resposta sob condição de maior complexidade cognitiva. Esse padrão pode estar associado a impulsividade, falhas de autocontrole e menor estabilidade na condução de tarefas que exigem flexibilidade mental."
    if total_errors <= 3:
        return "A presença de erros discretos e pontuais não compromete de forma global o desempenho, mas sugere oscilações leves de monitoramento e controle da resposta ao longo da execução. Ainda assim, o conjunto do protocolo indica funcionamento globalmente organizado, com pequenas falhas situacionais de precisão."
    return "A ocorrência de erros em diferentes etapas do teste sugere comprometimento mais amplo da precisão, com impacto tanto em componentes automáticos quanto em processos controlados. Esse padrão pode indicar instabilidade atencional, falhas de monitoramento contínuo e menor eficiência no controle global da resposta."


def _summary_paragraph(patient_name: str, metrics: dict) -> str:
    all_codes = ["leitura", "contagem", "escolha", "alternancia", "inibicao", "flexibilidade"]
    preserved_count = sum(1 for code in all_codes if _is_preserved(metrics.get(code)))
    changed_domains = []
    label_map = {
        "leitura": "velocidade de processamento",
        "contagem": "automatização",
        "escolha": "seleção de respostas",
        "alternancia": "alternância atencional",
        "inibicao": "controle inibitório",
        "flexibilidade": "flexibilidade cognitiva",
    }
    for code in all_codes:
        if not _is_preserved(metrics.get(code)):
            changed_domains.append(label_map[code])

    if preserved_count == len(all_codes):
        return (
            f"Em análise clínica, o desempenho de {patient_name} no FDT revela funcionamento executivo preservado e eficiente, tanto nos componentes automáticos quanto nos controlados, sem evidências de prejuízo em velocidade de processamento, controle inibitório, alternância atencional ou flexibilidade cognitiva."
        )
    if preserved_count >= 3:
        return (
            f"Em análise clínica, o desempenho de {patient_name} no FDT sugere funcionamento executivo parcialmente preservado, com sinais de fragilidade em {_join_labels(changed_domains)}, o que indica oscilação na eficiência do controle cognitivo e da regulação da resposta diante de demandas de maior complexidade."
        )
    return (
        f"Em análise clínica, o desempenho de {patient_name} no FDT evidencia prejuízos em componentes relevantes das funções executivas, com impacto sobre a velocidade de processamento, o controle inibitório, a alternância atencional e a flexibilidade cognitiva, sugerindo comprometimento do controle executivo global."
    )


def interpret_fdt_result(merged_data: dict, patient_name: str | None = None) -> str:
    name = _first_name(patient_name)
    metrics = _metrics_by_code(merged_data)
    errors = merged_data.get("erros", {})

    paragraphs = [
        f"A avaliação das funções executivas de {name} incluiu a aplicação do Teste dos Cinco Dígitos (FDT), instrumento destinado à investigação da velocidade de processamento, controle inibitório, alternância atencional e flexibilidade cognitiva, contemplando processos automáticos e controlados.",
        _automatic_paragraph(name, metrics, errors),
    ]

    controlled_codes = ["escolha", "alternancia", "inibicao", "flexibilidade"]
    if all(_is_preserved(metrics.get(code)) for code in controlled_codes):
        paragraphs.append(_controlled_paragraph(name, metrics, errors))
    elif any(_is_preserved(metrics.get(code)) for code in controlled_codes):
        paragraphs.append(_controlled_mixed_paragraph(name, metrics))
    else:
        paragraphs.append(_controlled_paragraph(name, metrics, errors))

    paragraphs.append(_errors_paragraph(errors))
    paragraphs.append(_summary_paragraph(name, metrics))

    return "\n\n".join(paragraphs)
