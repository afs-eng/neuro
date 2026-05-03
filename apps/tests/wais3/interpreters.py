from __future__ import annotations


def _first_name(patient_name: str | None) -> str:
    if not patient_name:
        return "Paciente"
    return patient_name.strip().split()[0] or "Paciente"


def classify_composite_score(value: int | None) -> str:
    if value is None:
        return "-"
    if value <= 69:
        return "Extremamente Baixo"
    if 70 <= value <= 79:
        return "Limítrofe"
    if 80 <= value <= 89:
        return "Média Inferior"
    if 90 <= value <= 109:
        return "Média"
    if 110 <= value <= 119:
        return "Média Superior"
    if 120 <= value <= 129:
        return "Superior"
    return "Muito Superior"


def _get_score_value(score_dict: dict) -> int | None:
    if score_dict is None:
        return None
    value = score_dict.get("pontuacao_composta")
    if value is None:
        value = score_dict.get("valor")
    if isinstance(value, (int, float)):
        return int(value)
    return None


def _describe_profile_variability(scores: dict) -> str:
    values = [
        _get_score_value(v)
        for v in scores.values()
        if v is not None and _get_score_value(v) is not None
    ]
    if not values:
        return "com variações não especificadas"
    spread = max(values) - min(values)
    if spread <= 9:
        return "relativamente homogêneo"
    if spread <= 14:
        return "com variações discretas"
    if spread <= 22:
        return "heterogêneo"
    return "acentuadamente heterogêneo"


def _get_classification_description(classification: str) -> str:
    classification = (classification or "").lower().strip()
    descriptions = {
        "muito superior": "desempenho significativamente acima da média esperada, indicando recursos cognitivos amplamente desenvolvidos nesse domínio",
        "superior": "desempenho acima da média esperada, sugerindo recursos cognitivos bem desenvolvidos nesse domínio",
        "média superior": "desempenho situado acima da média, indicando bom nível de eficiência nesse domínio",
        "média": "desempenho compatível com o esperado para a faixa etária, indicando funcionamento preservado nesse domínio",
        "média inferior": "desempenho abaixo da média esperada, sugerindo menor eficiência relativa nesse domínio",
        "limítrofe": "desempenho situado em faixa limítrofe, indicando vulnerabilidade importante nesse domínio e maior probabilidade de repercussões funcionais em tarefas de maior exigência",
        "extremamente baixo": "desempenho significativamente rebaixado, indicando prejuízo importante nesse domínio e necessidade de análise integrada com dados adaptativos, escolares, ocupacionais e clínicos",
    }
    return descriptions.get(classification, "desempenho compatível com o esperado")


def _format_score(score_dict: dict) -> str:
    value = _get_score_value(score_dict)
    if value is None:
        return "-"
    return str(value)


def build_wais3_interpretation(merged_data: dict, patient_name: str) -> str:
    indices = merged_data.get("indices") or {}
    gai = merged_data.get("gai_data") or {}
    
    qit = indices.get("qi_total") or {}
    qiv = indices.get("qi_verbal") or {}
    qie = indices.get("qi_execucao") or {}
    icv = indices.get("compreensao_verbal") or {}
    iop = indices.get("organizacao_perceptual") or {}
    imo = indices.get("memoria_operacional") or {}
    ivp = indices.get("velocidade_processamento") or {}
    
    qit_val = _get_score_value(qit)
    qiv_val = _get_score_value(qiv)
    qie_val = _get_score_value(qie)
    icv_val = _get_score_value(icv)
    iop_val = _get_score_value(iop)
    imo_val = _get_score_value(imo)
    ivp_val = _get_score_value(ivp)
    gai_val = _get_score_value(gai) if gai else None
    
    if qit_val is None:
        first_name = _first_name(patient_name)
        return (
            f"Interpretação e Observações Clínicas: A avaliação da eficiência intelectual de {first_name} por meio da Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III) foi registrada no sistema, porém as tabelas normativas ainda não estão preenchidas de forma suficiente para cálculo automatizado dos escores compostos, percentis e intervalos de confiança. Em análise clínica, o módulo está estruturado para receber os dados do teste, mas a interpretação quantitativa completa depende do preenchimento autorizado das tabelas normativas."
        )
    
    qit_class = classify_composite_score(qit_val)
    qiv_class = classify_composite_score(qiv_val)
    qie_class = classify_composite_score(qie_val)
    icv_class = classify_composite_score(icv_val)
    iop_class = classify_composite_score(iop_val)
    imo_class = classify_composite_score(imo_val)
    ivp_class = classify_composite_score(ivp_val)
    gai_class = classify_composite_score(gai_val) if gai_val else None
    
    profile_scores = {
        "QIV": qiv_val,
        "QIE": qie_val,
        "ICV": icv_val,
        "IOP": iop_val,
        "IMO": imo_val,
        "IVP": ivp_val,
    }
    profile_desc = _describe_profile_variability(profile_scores)
    
    parts = []
    
    parts.append(
        f"Os resultados obtidos na Escala Wechsler de Inteligência para Adultos – Terceira Edição (WAIS-III) indicam funcionamento intelectual global situado na faixa {qit_class.lower()}, com {profile_desc} entre os domínios avaliados. O Quociente de Inteligência Total (QIT = {qit_val}) encontra-se na classificação {qit_class.lower()}, refletindo funcionamento intelectual global {'compatível com o esperado para a faixa etária' if qit_class == 'Média' else 'abaixo da média esperada para a faixa etária' if qit_class in ['Média Inferior', 'Limítrofe', 'Extremamente Baixo'] else 'acima da média esperada para a faixa etária' if qit_class in ['Média Superior', 'Superior', 'Muito Superior'] else 'abaixo da média esperada'}, sem que esse achado, isoladamente, seja suficiente para caracterizar diagnóstico clínico específico."
    )
    
    parts.append(
        f"O Quociente de Inteligência Verbal (QIV = {qiv_val}) foi classificado como {qiv_class.lower()}, sugerindo {_get_classification_description(qiv_class)}. Esse índice envolve recursos de compreensão verbal, expressão conceitual, raciocínio mediado pela linguagem, aquisição de conhecimentos e uso funcional de informações verbais."
    )
    
    parts.append(
        f"O Quociente de Inteligência de Execução (QIE = {qie_val}) situou-se na faixa {qie_class.lower()}, indicando {_get_classification_description(qie_class)}. Esse resultado expressa o funcionamento em tarefas que demandam organização visuoespacial, raciocínio perceptivo, análise de estímulos visuais, solução prática de problemas e eficiência diante de demandas não verbais."
    )
    
    parts.append(
        f"Entre os índices fatoriais, a Compreensão Verbal (ICV = {icv_val}) apresentou desempenho {icv_class.lower()}, evidenciando {_get_classification_description(icv_class)}. Esse domínio está associado à formação de conceitos verbais, raciocínio abstrato mediado pela linguagem, compreensão de informações verbais e repertório de conhecimentos adquiridos."
    )
    
    parts.append(
        f"O Índice de Organização Perceptual (IOP = {iop_val}) também se situou na faixa {iop_class.lower()}, demonstrando {_get_classification_description(iop_class)}. Esse índice envolve análise, síntese e organização de estímulos visuais, raciocínio não verbal, percepção de relações espaciais e solução de problemas com menor dependência da linguagem."
    )
    
    parts.append(
        f"O Índice de Memória Operacional (IMO = {imo_val}) foi classificado como {imo_class.lower()}, indicando {_get_classification_description(imo_class)}. Esse domínio refere-se à capacidade de reter, manipular e reorganizar informações temporárias, especialmente em tarefas auditivo-verbais e de controle mental imediato."
    )
    
    parts.append(
        f"O Índice de Velocidade de Processamento (IVP = {ivp_val}) permaneceu na faixa {ivp_class.lower()}, sugerindo {_get_classification_description(ivp_class)}. Esse índice reflete a eficiência em tarefas simples, rápidas e automatizadas, envolvendo rastreamento visual, coordenação visuomotora, precisão gráfica e rapidez na execução."
    )
    
    if gai_val and gai_class:
        if gai_val >= 8 or qit_val - gai_val >= 8 or gai_val - qit_val >= 8:
            parts.append(
                f"Quando analisado o Índice de Habilidade Geral (GAI = {gai_val}), observa-se classificação {gai_class.lower()}, indicando {_get_classification_description(gai_class)}. A diferença entre o QIT e o GAI sugere que os componentes de memória operacional e/ou velocidade de processamento influenciaram o desempenho intelectual global, tornando o GAI uma estimativa complementar relevante das habilidades de raciocínio verbal e perceptual."
            )
        else:
            parts.append(
                f"Quando analisado o Índice de Habilidade Geral (GAI = {gai_val}), observa-se classificação {gai_class.lower()}, indicando {_get_classification_description(gai_class)}. O GAI fornece uma estimativa das habilidades intelectuais gerais com menor influência relativa da memória operacional e da velocidade de processamento, sendo útil para compreender os recursos de raciocínio verbal e perceptual de base."
            )
    
    more_preserved = []
    more_vulnerable = []
    
    score_map = {
        "Compreensão Verbal": icv_val,
        "Organização Perceptual": iop_val,
        "Memória Operacional": imo_val,
        "Velocidade de Processamento": ivp_val,
    }
    
    valid_scores = [(k, v) for k, v in score_map.items() if v is not None]
    if valid_scores:
        sorted_scores = sorted(valid_scores, key=lambda x: x[1], reverse=True)
        if sorted_scores:
            more_preserved.append(sorted_scores[0][0].lower())
            more_vulnerable.append(sorted_scores[-1][0].lower())
    
    vulnerable_text = f"maior vulnerabilidade nas demandas de {more_vulnerable[0]}" if more_vulnerable else "alguns domínios"
    preserved_text = f"recursos relativamente mais preservados em {more_preserved[0]}" if more_preserved else "recursos preservados"
    
    if profile_desc == "relativamente homogêneo":
        synthesis = f"O conjunto dos resultados revela um perfil cognitivo relativamente homogêneo, com funcionamento compatível entre os domínios avaliados. Esse padrão sugere que o desempenho cognitivo é consistente, sem grandes variações entre as diferentes áreas avaliadas."
    elif profile_desc == "com variações discretas":
        synthesis = f"O conjunto dos resultados revela um perfil cognitivo com variações discretas entre os domínios, com {preserved_text} e {vulnerable_text}. Esse padrão sugere {'boa integração entre as habilidades cognitivas' if not more_vulnerable else 'variabilidade que pode requerer atenção em situações que exijam demanda específica do domínio mais vulnerável'}."
    else:
        synthesis = f"O conjunto dos resultados revela um perfil cognitivo {profile_desc}, com {preserved_text} e {vulnerable_text}. Esse padrão sugere possíveis repercussões em situações que exijam {more_vulnerable[0] if more_vulnerable else 'demandas específicas'}, apesar da presença de {more_preserved[0] if more_preserved else 'recursos cognitivos'} relativamente preservados."
    
    parts.append(synthesis)
    
    return "Interpretação e Observações Clínicas: " + " ".join(parts)