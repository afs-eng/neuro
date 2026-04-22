from typing import Dict, Any


CLINICAL_DIFFICULTY = {"Média Superior", "Superior"}
NON_CLINICAL = {"Inferior", "Média Inferior", "Média"}

FACTOR_ORDER = ["fator_1", "fator_2", "fator_3", "fator_4", "escore_geral"]

FACTOR_LABELS = {
    "fator_1": "Fator 1 - Regulação Emocional",
    "fator_2": "Fator 2 - Hiperatividade / Impulsividade",
    "fator_3": "Fator 3 - Comportamento Adaptativo",
    "fator_4": "Fator 4 - Atenção",
    "escore_geral": "Escore Geral",
}


def get_faixa_etaria(idade: int) -> str:
    if 2 <= idade <= 5:
        return "2_5"
    if 6 <= idade <= 9:
        return "6_9"
    if 10 <= idade <= 13:
        return "10_13"
    if 14 <= idade <= 17:
        return "14_17"
    raise ValueError("Idade fora da faixa normativa do E-TDAH-PAIS (2 a 17 anos).")


def interpret_results(raw_scores: Dict[str, int], age: int, sex: str) -> Dict[str, Any]:
    from .config import NORMS, FACTOR_NAMES
    from .calculators import (
        manual_percentile_from_raw,
        classificar_percentil,
        classify_guilmette,
        percentile_guilmette,
        points_scaled,
    )

    faixa = get_faixa_etaria(age)
    sex_key = "feminino" if sex.upper() == "F" else "masculino"
    norms = NORMS[sex_key][faixa]

    results = {}
    metric_keys = ["fator_1", "fator_2", "fator_3", "fator_4", "escore_geral"]

    for metric_key in metric_keys:
        raw_score = raw_scores.get(metric_key, 0)

        pct_manual_num, pct_manual_text = manual_percentile_from_raw(
            raw_score, norms["scores"][metric_key]
        )
        class_manual = classificar_percentil(pct_manual_num)

        mean = norms["stats"][metric_key]["media"]
        std = norms["stats"][metric_key]["dp"]
        z = 0.0 if std == 0 else (raw_score - mean) / std
        pp = points_scaled(z)
        pct_g = percentile_guilmette(z)
        class_g = classify_guilmette(pct_g)

        results[metric_key] = {
            "name": FACTOR_NAMES.get(metric_key, metric_key),
            "raw_score": raw_score,
            "mean": mean,
            "std": std,
            "z_score": z,
            "points_scaled": pp,
            "percentile_text": pct_manual_text,
            "percentile_guilmette": pct_g,
            "classification": class_manual,
            "classification_guilmette": class_g,
        }

    return results


def _first_name(patient_name: str | None) -> str:
    if not patient_name:
        return "a criança"
    return patient_name.strip().split()[0] or "a criança"


def _is_clinical(classification: str) -> bool:
    return classification in CLINICAL_DIFFICULTY


def _factor_paragraph(factor_key: str, result: dict) -> str:
    classification = result.get("classification", "Média")
    header = FACTOR_LABELS[factor_key]

    if factor_key == "fator_1":
        if classification in NON_CLINICAL:
            body = (
                f"O resultado foi classificado como {classification}, o que, conforme os critérios interpretativos do instrumento, não indica prejuízo clínico nesse domínio. "
                "Esse padrão sugere estabilidade emocional globalmente compatível com a faixa etária, sem evidências consistentes de labilidade afetiva acentuada, irritabilidade persistente ou dificuldade significativa de modulação emocional na percepção dos responsáveis."
            )
        else:
            body = (
                f"O resultado situou-se na classificação {classification}, configurando indicativo de dificuldade clínica nesse domínio. "
                "Esse achado sugere maior frequência de manifestações como irritabilidade, oscilação afetiva, reatividade emocional aumentada e dificuldade de autorregulação, com possível repercussão no convívio familiar e na adaptação às frustrações cotidianas."
            )
    elif factor_key == "fator_2":
        if classification in NON_CLINICAL:
            body = (
                f"O desempenho apresentou classificação {classification}, não configurando prejuízo clínico nesse domínio. "
                "Esse resultado sugere ausência de indicadores consistentes de agitação motora excessiva, impulsividade comportamental ou dificuldade relevante de inibição de respostas na percepção parental."
            )
        else:
            body = (
                f"O desempenho situou-se na classificação {classification}, configurando indicativo de dificuldade clínica relevante nesse domínio. "
                "Esse achado aponta para comportamentos frequentes de inquietação, agitação psicomotora, impulsividade e dificuldade em postergar respostas imediatas, com impacto funcional percebido no ambiente familiar e potencial repercussão em outros contextos de exigência comportamental."
            )
    elif factor_key == "fator_3":
        if classification in NON_CLINICAL:
            body = (
                f"O escore foi classificado como {classification}, sendo interpretado como sem indicativo de prejuízo clínico. "
                "Esse padrão sugere repertório funcional adequado para responder a rotinas, regras e demandas cotidianas compatíveis com a etapa do desenvolvimento."
            )
        else:
            body = (
                f"O escore apresentou classificação {classification}, indicando dificuldade clínica nesse domínio. "
                "Esse resultado sugere prejuízos na organização do comportamento frente às exigências do cotidiano, com possíveis dificuldades para seguir rotinas, adaptar-se a regras, sustentar comportamentos adequados ao contexto e responder de forma funcional às demandas ambientais."
            )
    elif factor_key == "fator_4":
        if classification in NON_CLINICAL:
            body = (
                f"O resultado apresentou classificação {classification}, não indicando prejuízo clínico nesse domínio segundo a percepção dos responsáveis. "
                "Esse perfil sugere funcionamento atencional globalmente compatível com a faixa etária, sem sinais consistentes de distraibilidade excessiva, dificuldade de sustentação do foco ou comprometimento importante na conclusão de tarefas."
            )
        else:
            body = (
                f"O resultado apresentou classificação {classification}, indicando dificuldade clínica significativa nesse domínio. "
                "Esse achado sugere presença de comportamentos associados à desatenção, como dificuldade em manter o foco, concluir tarefas, acompanhar instruções e sustentar a atenção em atividades estruturadas."
            )
    else:
        if classification in NON_CLINICAL:
            body = (
                f"O escore global situou-se na classificação {classification}, o que não configura comprometimento clínico amplo segundo os parâmetros do instrumento. "
                "Ainda assim, a interpretação deve considerar a distribuição interna dos fatores, uma vez que alterações específicas podem coexistir com um escore global dentro dos limites esperados."
            )
        else:
            body = (
                f"O escore global situou-se na classificação {classification}, indicando comprometimento clínico global na percepção dos responsáveis. "
                "Esse resultado sugere que as manifestações comportamentais relacionadas ao TDAH se apresentam de forma mais abrangente e funcionalmente relevante no cotidiano da criança."
            )

    return f"{header}\n{body}"


def _integrated_analysis(results: Dict[str, Any]) -> str:
    elevated_factors = [
        FACTOR_LABELS[key].replace("Fator 1 - ", "").replace("Fator 2 - ", "").replace("Fator 3 - ", "").replace("Fator 4 - ", "")
        for key in ["fator_1", "fator_2", "fator_3", "fator_4"]
        if _is_clinical(results[key].get("classification", ""))
    ]
    global_elevated = _is_clinical(results["escore_geral"].get("classification", ""))

    if not elevated_factors:
        return (
            "Análise Integrada\n"
            "O conjunto dos resultados não evidenciou elevações clinicamente significativas nos fatores avaliados, sugerindo perfil comportamental globalmente compatível com os limites esperados segundo a percepção dos responsáveis. Ainda assim, a interpretação final deve ser articulada com a anamnese, a observação clínica e os demais instrumentos aplicados."
        )

    if not global_elevated:
        return (
            "Análise Integrada\n"
            f"Embora o escore global não indique comprometimento clínico amplo, a presença de elevação significativa em {', '.join(elevated_factors)} demonstra que as dificuldades se concentram de maneira específica nesses domínios, com repercussões funcionais mais localizadas. Esse perfil sugere um padrão focal de dificuldades comportamentais, cuja relevância clínica deve ser analisada em conjunto com a observação direta, a anamnese e os demais instrumentos da avaliação."
        )

    return (
        "Análise Integrada\n"
        f"A elevação observada no escore geral, associada ao aumento em múltiplos fatores, sugere um padrão mais disseminado de dificuldades comportamentais, com impacto mais amplo sobre o funcionamento cotidiano. As elevações em {', '.join(elevated_factors)} reforçam a necessidade de integrar a percepção parental com os achados objetivos e o comportamento observado durante a avaliação para delimitar a extensão funcional dessas manifestações."
    )


def _final_paragraph(patient_name: str, results: Dict[str, Any]) -> str:
    elevated_domains = []
    mapping = {
        "fator_1": "regulação emocional",
        "fator_2": "hiperatividade/impulsividade",
        "fator_3": "comportamento adaptativo",
        "fator_4": "atenção",
    }
    for key, label in mapping.items():
        if _is_clinical(results[key].get("classification", "")):
            elevated_domains.append(label)

    if not elevated_domains:
        return (
            f"Em análise clínica, a percepção dos responsáveis no E-TDAH-PAIS não sugere comprometimento comportamental clinicamente significativo nos domínios investigados, mantendo-se a recomendação de articulação com os demais dados da avaliação para conclusão diagnóstica global."
        )

    joined = ", ".join(elevated_domains[:-1]) + (" e " + elevated_domains[-1] if len(elevated_domains) > 1 else elevated_domains[0])
    return (
        f"Em análise clínica, a percepção parental descrita no E-TDAH-PAIS sugere que {patient_name} apresenta dificuldades predominantes nos domínios de {joined}, com repercussão funcional sobre a autorregulação e o manejo das demandas cotidianas. Esses achados devem ser integrados à observação clínica, à anamnese e aos demais instrumentos antes de qualquer conclusão diagnóstica definitiva."
    )


def generate_report(raw_scores: Dict[str, int], age: int, sex: str, patient_name: str | None = None) -> str:
    results = interpret_results(raw_scores, age, sex)
    first_name = _first_name(patient_name)

    paragraphs = [
        "Interpretação e Observações Clínicas: A Escala E-TDAH-PAIS tem como objetivo identificar manifestações comportamentais e emocionais associadas ao Transtorno do Déficit de Atenção e Hiperatividade (TDAH) a partir da percepção dos responsáveis, avaliando domínios relacionados à regulação emocional, hiperatividade/impulsividade, comportamento adaptativo e atenção. O instrumento fornece indicadores quantitativos sobre a intensidade e o impacto funcional desses comportamentos no cotidiano da criança, contribuindo para a compreensão clínica do quadro comportamental em diferentes contextos de desenvolvimento (Benczik, 2005).",
    ]

    for key in FACTOR_ORDER:
        paragraphs.append(_factor_paragraph(key, results[key]))

    paragraphs.append(_integrated_analysis(results))
    paragraphs.append(_final_paragraph(first_name, results))

    return "\n\n".join(paragraphs)
