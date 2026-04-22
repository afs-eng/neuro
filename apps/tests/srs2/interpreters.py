DOMAIN_DESCRIPTIONS = {
    "percepcao_social": "perceber pistas interpessoais e captar elementos relevantes do contexto social",
    "cognicao_social": "compreender situacoes sociais e inferir adequadamente intencoes e estados mentais de outras pessoas",
    "comunicacao_social": "sustentar trocas comunicativas reciprocas e ajustar a comunicacao ao contexto",
    "motivacao_social": "manter interesse e iniciativa para o engajamento social",
    "padroes_restritos": "maior rigidez comportamental, repetitividade e menor flexibilidade diante de mudancas",
    "cis": "os componentes centrais de reciprocidade social e comunicacao interpessoal",
}

CORE_SOCIAL_KEYS = [
    "percepcao_social",
    "cognicao_social",
    "comunicacao_social",
    "motivacao_social",
]


def _normalize_classification(value: str) -> str:
    normalized = (value or "").strip().lower()
    if "normal" in normalized:
        return "normal"
    if "leve" in normalized:
        return "leve"
    if "moder" in normalized:
        return "moderado"
    if "grave" in normalized or "sever" in normalized:
        return "grave"
    return normalized or "indefinido"


def _join_names(names: list[str]) -> str:
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} e {names[1]}"
    return f"{', '.join(names[:-1])} e {names[-1]}"


def _profile_paragraph(total_level: str, altered_count: int) -> str:
    if total_level == "normal" and altered_count == 0:
        return (
            "O perfil obtido no SRS-2 revelou funcionamento social globalmente dentro dos limites esperados nos dominios investigados, "
            "sem indicativos de comprometimento clinicamente relevante da responsividade social segundo este instrumento."
        )
    if total_level == "normal":
        return (
            "O perfil obtido no SRS-2 revelou funcionamento social globalmente dentro dos limites esperados na maior parte dos dominios investigados, "
            "com elevacao discreta em areas especificas."
        )
    if total_level == "leve":
        return (
            "O perfil obtido no SRS-2 evidenciou alteracoes leves na responsividade social, sugerindo dificuldades sutis, porem clinicamente relevantes, "
            "na qualidade das interacoes interpessoais e/ou na flexibilidade comportamental."
        )
    if total_level == "moderado":
        return (
            "O perfil obtido no SRS-2 evidenciou alteracoes clinicamente relevantes em multiplos dominios da responsividade social, sugerindo prejuizos "
            "na qualidade das interacoes interpessoais, no processamento de pistas sociais e na flexibilidade comportamental."
        )
    return (
        "O perfil obtido no SRS-2 evidenciou alteracoes intensas e abrangentes na responsividade social, sugerindo comprometimento expressivo na reciprocidade "
        "social, na comunicacao interpessoal e na modulacao comportamental."
    )


def interpret_srs2_results(merged_data: dict) -> str:
    results = merged_data.get("resultados", [])
    if not results:
        return "Sem resultados para interpretação."

    by_key = {item.get("variavel"): item for item in results}
    total = by_key.get("total")
    cis = by_key.get("cis")

    total_level = _normalize_classification((total or {}).get("classificacao", ""))
    altered_domains = [
        item
        for item in results
        if item.get("variavel") != "total"
        and _normalize_classification(item.get("classificacao", "")) != "normal"
    ]

    paragraphs = [
        "A Escala de Responsividade Social - Segunda Edicao (SRS-2) foi aplicada com o objetivo de investigar possiveis dificuldades na comunicacao social, cognicao social, motivacao social, percepcao social e na presenca de padroes de comportamento restritos e repetitivos, a fim de rastrear indicadores associados ao Transtorno do Espectro Autista (TEA).",
        _profile_paragraph(total_level, len(altered_domains)),
    ]

    core_preserved = []
    core_altered = []
    for key in CORE_SOCIAL_KEYS:
        row = by_key.get(key)
        if not row:
            continue
        if _normalize_classification(row.get("classificacao", "")) == "normal":
            core_preserved.append(row.get("nome", key))
        else:
            core_altered.append(row)

    factor_sentences = []
    if core_preserved:
        factor_sentences.append(
            f"Os dominios de {_join_names(core_preserved)} permaneceram dentro dos limites normais, sugerindo recursos preservados para {_join_names([DOMAIN_DESCRIPTIONS[key] for key in CORE_SOCIAL_KEYS if by_key.get(key) and _normalize_classification(by_key[key].get('classificacao', '')) == 'normal'])}."
        )

    for row in core_altered:
        key = row.get("variavel")
        level = _normalize_classification(row.get("classificacao", ""))
        factor_sentences.append(
            f"O dominio de {row.get('nome')} apresentou elevacao em nivel {level}, indicando dificuldades em {DOMAIN_DESCRIPTIONS.get(key, 'aspectos centrais da responsividade social')}."
        )

    if cis:
        cis_level = _normalize_classification(cis.get("classificacao", ""))
        if cis_level == "normal":
            factor_sentences.append(
                "A escala de Comunicacao e Interacao Social permaneceu dentro dos limites normais, indicando ausencia de comprometimento global expressivo nos componentes centrais de reciprocidade social."
            )
        else:
            factor_sentences.append(
                f"A escala de Comunicacao e Interacao Social situou-se em nivel {cis_level}, funcionando como sintese de alteracoes nos componentes centrais de reciprocidade social e comunicacao interpessoal."
            )

    repetitive = by_key.get("padroes_restritos")
    if repetitive:
        repetitive_level = _normalize_classification(repetitive.get("classificacao", ""))
        if repetitive_level == "normal":
            factor_sentences.append(
                "O dominio de Padroes Restritos e Repetitivos manteve-se dentro da faixa de normalidade, sem indicativos expressivos de rigidez ou repetitividade comportamental neste instrumento."
            )
        else:
            factor_sentences.append(
                f"Em contraste, o dominio de Padroes Restritos e Repetitivos apresentou elevacao em nivel {repetitive_level}, indicando {DOMAIN_DESCRIPTIONS['padroes_restritos']}."
            )

    if total:
        total_sentence = {
            "normal": "A Pontuacao Total do SRS-2 tambem permaneceu dentro da faixa de normalidade, nao sugerindo comprometimento clinico relevante da responsividade social segundo este instrumento.",
            "leve": "A Pontuacao Total do SRS-2 situou-se em nivel leve, sugerindo dificuldades sutis, porem clinicamente relevantes, na responsividade social global.",
            "moderado": "A Pontuacao Total do SRS-2 situou-se em nivel moderado, sugerindo comprometimento global clinicamente relevante da responsividade social.",
            "grave": "A Pontuacao Total do SRS-2 situou-se em nivel grave, apontando comprometimento global importante da responsividade social e maior probabilidade de prejuizos funcionais associados.",
        }.get(total_level, "A Pontuacao Total do SRS-2 deve ser interpretada como estimativa global do grau de comprometimento da responsividade social.")
        factor_sentences.append(total_sentence)

    paragraphs.append(" ".join(factor_sentences))
    paragraphs.append(
        "Em analise clinica, os resultados do SRS-2 fornecem uma estimativa padronizada do funcionamento sociointeracional, mas nao sao suficientes, de forma isolada, para sustentar conclusao diagnostica de TEA, devendo ser interpretados em conjunto com a historia do desenvolvimento, a observacao comportamental e os demais instrumentos da avaliacao neuropsicologica."
    )

    return "\n\n".join(paragraphs)
