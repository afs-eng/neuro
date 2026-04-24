def interpret_result(fator: str, classificacao: str) -> str:
    return _factor_inference(fator, classificacao)


def get_synthesis(resultado: dict) -> str:
    parts = []
    for fator in ["P", "E", "N", "S"]:
        if fator in resultado:
            r = resultado[fator]
            parts.append(f"{fator}: {r['classificacao']} (P{r['percentil']})")
    return " | ".join(parts)


def get_report_interpretation(result: dict, patient_name: str = "") -> str:
    if not result:
        return "Sem resultados suficientes para interpretação do EPQ-J."

    name = _first_name(patient_name)
    paragraphs = [
        "Interpretação e Observações Clínicas: O EPQ-J (Inventário de Personalidade de Eysenck para Jovens) avalia os traços de personalidade a partir de quatro dimensões fundamentais: Psicoticismo (P), Extroversão (E), Neuroticismo (N) e Sinceridade (S) (Eysenck & Eysenck, 1992). O instrumento permite compreender o padrão predominante de funcionamento emocional e comportamental do indivíduo, bem como o estilo de resposta frente às demandas sociais e cognitivas.",
        _psychoticism_text(result, name),
        _extroversion_text(result, name),
        _neuroticism_text(result),
        _sincerity_text(result),
        _clinical_integration_text(result, name),
        _final_analysis_text(result, name),
        _diagnostic_hypothesis_text(result, name),
    ]
    return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)


def _first_name(patient_name: str) -> str:
    return (patient_name or "Paciente").strip().split(" ", 1)[0] or "Paciente"


def _classification_value(classificacao: str) -> int:
    return {
        "MUITO BAIXO": -2,
        "BAIXO": -1,
        "MEDIO": 0,
        "ALTO": 1,
        "MUITO ALTO": 2,
    }.get((classificacao or "").strip().upper(), 0)


def _is_high(classificacao: str) -> bool:
    return _classification_value(classificacao) >= 1


def _is_low(classificacao: str) -> bool:
    return _classification_value(classificacao) <= -1


def _factor_inference(fator: str, classificacao: str) -> str:
    level = (classificacao or "").strip().upper()
    texts = {
        "P": {
            "MUITO BAIXO": "maior sensibilidade social, menor tendência à impulsividade e melhor modulação interpessoal",
            "BAIXO": "boa consideração pelas normas e funcionamento interpessoal mais ajustado",
            "MEDIO": "equilíbrio relativo nesse domínio, sem indicadores marcantes de endurecimento interpessoal ou impulsividade",
            "ALTO": "maior impulsividade, menor empatia e possível rigidez ou oposição diante de frustrações",
            "MUITO ALTO": "importante impulsividade, menor sensibilidade interpessoal e necessidade de análise cuidadosa do controle comportamental",
        },
        "E": {
            "MUITO BAIXO": "perfil bastante introspectivo, reservado e com menor busca por estimulação social",
            "BAIXO": "maior introspecção, reserva afetiva e preferência por contextos menos expansivos",
            "MEDIO": "equilíbrio entre abertura social e momentos de maior reserva",
            "ALTO": "sociabilidade, comunicabilidade e maior busca por interação interpessoal",
            "MUITO ALTO": "perfil bastante expansivo, ativo e voltado ao contato social",
        },
        "N": {
            "MUITO BAIXO": "boa estabilidade emocional e baixa reatividade a tensões do cotidiano",
            "BAIXO": "estabilidade emocional e recursos adequados para lidar com estresse e frustração",
            "MEDIO": "reações emocionais dentro de limites esperados, sem indícios expressivos de instabilidade persistente",
            "ALTO": "instabilidade emocional, sensibilidade ao estresse e vulnerabilidade ansiosa",
            "MUITO ALTO": "acentuada instabilidade emocional, ansiedade e maior suscetibilidade a oscilações afetivas",
        },
        "S": {
            "MUITO BAIXO": "respostas mais espontâneas, com menor tendência à desejabilidade social",
            "BAIXO": "autoapresentação relativamente espontânea, sem preocupação excessiva em parecer socialmente ideal",
            "MEDIO": "protocolo com validade global preservada, sem indícios marcantes de distorção da autoapresentação",
            "ALTO": "tendência à desejabilidade social e maior preocupação em responder de forma socialmente aceita",
            "MUITO ALTO": "forte desejabilidade social, exigindo cautela adicional na leitura dos demais fatores",
        },
    }
    return texts.get(fator, {}).get(level, "")


def _factor_result(result: dict, factor: str) -> dict:
    return result.get(factor, {}) or {}


def _classification_text(item: dict) -> str:
    return str(item.get("classificacao") or "MEDIO").lower().replace("medio", "médio")


def _percentile_text(item: dict) -> str:
    return str(item.get("percentil") or "-")


def _psychoticism_text(result: dict, name: str) -> str:
    item = _factor_result(result, "P")
    classification = _classification_text(item)
    percentile = _percentile_text(item)
    inference = _factor_inference("P", item.get("classificacao", ""))
    expansion = (
        "maior necessidade de acompanhamento do controle inibitório e da qualidade das trocas interpessoais"
        if _is_high(item.get("classificacao", ""))
        else "recursos mais favoráveis de sensibilidade social e adaptação às normas de convivência"
    )
    return (
        f"O resultado de {name} nesse fator foi classificado como {classification} (percentil {percentile}), sugerindo {inference}. "
        f"Esse padrão não implica, por si só, quadro psiquiátrico específico ou traço patológico isolado, mas pode indicar {expansion}."
    )


def _extroversion_text(result: dict, name: str) -> str:
    item = _factor_result(result, "E")
    classification = _classification_text(item)
    percentile = _percentile_text(item)
    inference = _factor_inference("E", item.get("classificacao", ""))

    if _is_high(item.get("classificacao", "")):
        behavior = f"{name} tende a buscar mais contato com o ambiente, com maior iniciativa relacional e expressão social"
        integration = "maior abertura à interação, responsividade interpessoal e busca por estimulação externa"
    elif _is_low(item.get("classificacao", "")):
        behavior = f"{name} tende a funcionar de modo mais introspectivo, reservado e seletivo nas interações"
        integration = "maior contenção interpessoal, observação do ambiente antes do engajamento e preferência por contextos menos expansivos"
    else:
        behavior = f"{name} tende a oscilar de forma adaptativa entre momentos de sociabilidade e de reserva"
        integration = "equilíbrio entre abertura social e preservação de espaço subjetivo"

    return (
        f"O fator Extroversão apresentou classificação {classification} (percentil {percentile}), indicando {inference}. "
        f"{behavior}. Esse perfil está frequentemente associado a {integration}."
    )


def _neuroticism_text(result: dict) -> str:
    item = _factor_result(result, "N")
    classification = _classification_text(item)
    percentile = _percentile_text(item)
    inference = _factor_inference("N", item.get("classificacao", ""))

    if _is_high(item.get("classificacao", "")):
        impact = "maior impacto das tensões emocionais sobre a autorregulação, a tolerância à frustração e a adaptação diante de demandas cotidianas"
    elif _is_low(item.get("classificacao", "")):
        impact = "preservação relativa dos recursos de estabilidade emocional e menor tendência a reações intensas diante de estressores"
    else:
        impact = "funcionamento emocional sem sinais expressivos de instabilidade persistente"

    return (
        f"O escore {classification} em Neuroticismo (percentil {percentile}) indica {inference}. "
        f"Esse fator sugere {impact}."
    )


def _sincerity_text(result: dict) -> str:
    item = _factor_result(result, "S")
    classification = _classification_text(item)
    percentile = _percentile_text(item)
    inference = _factor_inference("S", item.get("classificacao", ""))

    if _is_high(item.get("classificacao", "")):
        reliability = "menor grau de confiabilidade plena"
    elif _is_low(item.get("classificacao", "")):
        reliability = "boa confiabilidade interpretativa"
    else:
        reliability = "adequado nível de confiabilidade"

    return (
        f"O fator Sinceridade apresentou classificação {classification} (percentil {percentile}), indicando {inference}. "
        f"Esse resultado confere {reliability} aos demais fatores avaliados."
    )


def _clinical_integration_text(result: dict, name: str) -> str:
    p = _factor_result(result, "P").get("classificacao", "")
    e = _factor_result(result, "E").get("classificacao", "")
    n = _factor_result(result, "N").get("classificacao", "")
    s = _factor_result(result, "S").get("classificacao", "")

    traits = []
    if _is_high(n):
        traits.append("maior vulnerabilidade emocional")
    elif _is_low(n):
        traits.append("estabilidade afetiva relativamente preservada")

    if _is_high(e):
        traits.append("busca ativa por contato interpessoal")
    elif _is_low(e):
        traits.append("funcionamento mais introspectivo")

    if _is_high(p):
        traits.append("maior impulsividade e menor modulação interpessoal")
    elif _is_low(p):
        traits.append("sensibilidade social mais preservada")

    if _is_high(s):
        traits.append("possível influência de desejabilidade social nas respostas")

    if not traits:
        traits.append("traços de personalidade sem desvios expressivos nos fatores investigados")

    joined_traits = ", ".join(traits[:-1]) + (" e " + traits[-1] if len(traits) > 1 else traits[0])
    return (
        f"Em análise clínica, o perfil de {name} no EPQ-J revela uma combinação de {joined_traits}, configurando um padrão de funcionamento emocional e relacional que deve ser compreendido de forma integrada à observação clínica e aos demais instrumentos aplicados."
    )


def _final_analysis_text(result: dict, name: str) -> str:
    p = _factor_result(result, "P").get("classificacao", "")
    e = _factor_result(result, "E").get("classificacao", "")
    n = _factor_result(result, "N").get("classificacao", "")

    if _is_high(n) and _is_low(e):
        synthesis = "maior internalização afetiva, sensibilidade ao estresse e tendência à introspecção"
    elif _is_high(n) and _is_high(e):
        synthesis = "reatividade emocional relevante associada a maior busca de contato, validação e intensidade nas trocas interpessoais"
    elif _is_high(p):
        synthesis = "impulsividade e modulação interpessoal mais vulnerável, especialmente em contextos de tensão ou frustração"
    elif _is_low(n) and _is_low(p):
        synthesis = "estabilidade emocional relativa, sensibilidade social e bom potencial adaptativo nas relações"
    else:
        synthesis = "características de personalidade que ajudam a compreender o estilo emocional e comportamental observado ao longo da avaliação"

    return (
        f"Análise Clínica: Os resultados do EPQ-J indicam que {name} apresenta traços de personalidade caracterizados por {synthesis}. Esses achados devem ser lidos como dado complementar do exame, sempre articulados à anamnese, ao contexto desenvolvimental e ao funcionamento escolar, social e emocional." 
    )


def _diagnostic_hypothesis_text(result: dict, name: str) -> str:
    p = _factor_result(result, "P").get("classificacao", "")
    n = _factor_result(result, "N").get("classificacao", "")
    s = _factor_result(result, "S").get("classificacao", "")

    if _is_high(s):
        return (
            f"Considerando a integração dos dados do EPQ-J com as observações clínicas, não há elementos suficientes para sustentar hipótese diagnóstica específica a partir deste instrumento, especialmente diante de possível influência de desejabilidade social no protocolo de {name}."
        )

    if _is_high(n) and _is_high(p):
        return (
            f"Considerando a integração dos dados do EPQ-J com as observações clínicas, há hipótese diagnóstica de sofrimento emocional com prejuízo de autorregulação afetiva e comportamental, devendo essa formulação ser confirmada a partir da articulação com anamnese e demais instrumentos da avaliação."
        )

    if _is_high(n):
        return (
            f"Considerando a integração dos dados do EPQ-J com as observações clínicas, há hipótese diagnóstica de vulnerabilidade emocional e sintomatologia ansiosa ou internalizante, a ser confirmada pela articulação com a história clínica e os demais achados do exame."
        )

    return (
        f"Considerando a integração dos dados do EPQ-J com as observações clínicas, não há elementos suficientes para sustentar hipótese diagnóstica específica a partir dos traços de personalidade identificados, embora o instrumento contribua para a compreensão do estilo de funcionamento de {name}."
    )
