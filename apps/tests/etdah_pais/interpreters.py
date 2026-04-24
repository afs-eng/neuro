from typing import Any, Dict


CLINICAL_DIFFICULTY = {"Média Superior", "Superior"}
NON_CLINICAL = {"Inferior", "Média Inferior", "Média"}

FACTOR_ORDER = ["fator_1", "fator_2", "fator_3", "fator_4", "escore_geral"]

FACTOR_LABELS = {
    "fator_1": "Fator 1 — Regulação Emocional",
    "fator_2": "Fator 2 — Hiperatividade/Impulsividade",
    "fator_3": "Fator 3 — Comportamento Adaptativo",
    "fator_4": "Fator 4 — Atenção",
    "escore_geral": "Escore Geral",
}

DOMAIN_NAMES = {
    "fator_1": "regulação emocional",
    "fator_2": "hiperatividade/impulsividade",
    "fator_3": "comportamento adaptativo",
    "fator_4": "atenção",
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
    from .config import FACTOR_NAMES, NORMS
    from .calculators import (
        classificar_percentil,
        classify_guilmette,
        manual_percentile_from_raw,
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


def _classification_text(result: dict) -> str:
    return str(result.get("classification") or "Média")


def _percentile_text(result: dict) -> str:
    text = str(result.get("percentile_text") or "")
    return text.replace("Percentil ", "").replace("percentil ", "") or "-"


def _severity_text(classification: str) -> str:
    if classification == "Superior":
        return "prejuízo clínico grave"
    if classification == "Média Superior":
        return "prejuízo clínico moderado"
    return "ausência de prejuízo clínico significativo"


def _factor_paragraph(factor_key: str, result: dict) -> str:
    classification = _classification_text(result)
    percentile = _percentile_text(result)

    if factor_key == "fator_1":
        if classification == "Superior":
            body = (
                "indica presença significativa de dificuldades na modulação das emoções, com maior reatividade emocional, baixa tolerância à frustração e dificuldade em manejar respostas emocionais de forma adaptativa. "
                "Esse resultado sugere prejuízo clínico grave nesse domínio, com impacto na autorregulação, no comportamento cotidiano e na adaptação às demandas do ambiente."
            )
        elif classification == "Média Superior":
            body = (
                "sugere dificuldades moderadas na modulação emocional, com tendência à maior sensibilidade a frustrações, oscilação afetiva e dificuldade em regular respostas emocionais diante de demandas ambientais. "
                "Esse padrão indica prejuízo clínico moderado, devendo ser compreendido em conjunto com a observação clínica e os demais dados da avaliação."
            )
        else:
            body = (
                f"indica funcionamento dentro dos limites esperados, sem evidências de prejuízo clínico significativo nesse domínio segundo a percepção dos responsáveis. "
                f"Esse resultado sugere {_severity_text(classification)} em regulação emocional."
            )
    elif factor_key == "fator_2":
        if classification == "Superior":
            body = (
                "indica presença significativa de sintomas relacionados à agitação motora, impulsividade e dificuldade de inibir respostas comportamentais. "
                "Esse padrão sugere prejuízo clínico grave, com possível impacto na convivência familiar, no cumprimento de regras, na permanência em atividades e na adaptação a contextos que exigem autocontrole."
            )
        elif classification == "Média Superior":
            body = (
                "sugere presença moderada de comportamentos associados à impulsividade e à inquietação motora, podendo envolver dificuldade de aguardar, tendência a agir antes de pensar e necessidade aumentada de movimento. "
                "Esse resultado indica prejuízo clínico moderado nesse domínio."
            )
        else:
            body = (
                "indica ausência de prejuízos significativos relacionados à agitação motora excessiva ou impulsividade comportamental, sugerindo que esses sintomas não se apresentam de forma clinicamente relevante no contexto avaliado."
            )
    elif factor_key == "fator_3":
        if classification == "Superior":
            body = (
                "indica prejuízo grave na adaptação comportamental, com dificuldades importantes no cumprimento de regras, organização das condutas, adequação às demandas ambientais e manutenção de comportamentos funcionais no cotidiano. "
                "Esse resultado sugere impacto clínico relevante na autonomia, na convivência familiar e na adaptação social."
            )
        elif classification == "Média Superior":
            body = (
                "aponta dificuldades importantes na adaptação comportamental, incluindo desafios no cumprimento de regras, organização do comportamento e adequação às exigências do ambiente, configurando prejuízo clínico moderado nesse domínio."
            )
        else:
            body = (
                f"sugere funcionamento adaptativo dentro dos limites esperados, sem evidências de prejuízo clínico significativo nesse domínio segundo a percepção dos responsáveis."
            )
    elif factor_key == "fator_4":
        if classification == "Superior":
            body = (
                "indica presença significativa de dificuldades atencionais, com prejuízo grave na manutenção do foco, na persistência em tarefas, na organização das atividades e na resistência à distração. "
                "Esse resultado sugere impacto funcional relevante no cotidiano e deve ser integrado aos achados objetivos das testagens neuropsicológicas."
            )
        elif classification == "Média Superior":
            body = (
                "sugere dificuldades moderadas relacionadas à manutenção do foco, organização atencional e persistência em tarefas. "
                "Esse padrão indica prejuízo clínico moderado, especialmente em atividades que exigem continuidade, autonomia e controle voluntário da atenção."
            )
        else:
            body = (
                "indica funcionamento dentro da normalidade, sem evidências de prejuízo clínico significativo segundo a percepção dos responsáveis, embora esse resultado deva ser analisado em conjunto com os achados objetivos das testagens neuropsicológicas."
            )
    else:
        if classification == "Superior":
            body = (
                "sugere prejuízo comportamental global grave, com impacto clinicamente significativo em múltiplos domínios avaliados. "
                "Esse padrão indica necessidade de análise integrada quanto à presença de sintomas compatíveis com TDAH, dificuldades de autorregulação emocional, prejuízos adaptativos e repercussões funcionais no cotidiano."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo comportamental global moderado, com presença de dificuldades clinicamente relevantes em parte dos domínios avaliados. "
                "Esse resultado indica necessidade de investigação integrada, especialmente quando houver convergência com queixas da anamnese, observação clínica e testes de atenção ou funções executivas."
            )
        else:
            body = (
                f"sugere funcionamento comportamental global dentro dos limites esperados, podendo coexistir com prejuízos específicos em fatores isolados. "
                f"Nesses casos, a interpretação deve destacar os domínios clinicamente elevados, quando houver, e evitar concluir que há prejuízo global quando o escore total não estiver elevado."
            )

    prefix = FACTOR_LABELS[factor_key]
    if factor_key == "escore_geral":
        return f"{prefix}: classificado como {classification} (percentil {percentile}), {body}"
    return f"No {prefix}, o desempenho classificado como {classification} (percentil {percentile}) {body}"


def _elevated_domains(results: Dict[str, Any]) -> list[str]:
    return [
        DOMAIN_NAMES[key]
        for key in ["fator_1", "fator_2", "fator_3", "fator_4"]
        if _is_clinical(results[key].get("classification", ""))
    ]


def _joined(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " e " + items[-1]


def _analysis_text(name: str, results: Dict[str, Any]) -> str:
    elevated = _elevated_domains(results)
    global_elevated = _is_clinical(results["escore_geral"].get("classification", ""))

    if not elevated:
        return (
            f"Em análise clínica, os resultados do E-TDAH-PAIS indicam que {name} apresenta funcionamento comportamental globalmente dentro dos limites esperados nos domínios avaliados, sem evidências de prejuízo clinicamente relevante em regulação emocional, hiperatividade/impulsividade, comportamento adaptativo ou atenção. O perfil sugere preservação funcional segundo a percepção dos responsáveis, devendo ser compreendido de forma integrada aos dados cognitivos, atencionais, executivos, emocionais e comportamentais obtidos ao longo da avaliação neuropsicológica."
        )

    joined = _joined(elevated)
    if global_elevated:
        synthesis = f"prejuízos comportamentais clinicamente relevantes, com maior comprometimento em {joined}"
        profile = "um padrão mais disseminado de dificuldades, com impacto funcional mais amplo no cotidiano"
    else:
        synthesis = f"prejuízos específicos, com maior comprometimento em {joined}, sem configuração de comprometimento global amplo"
        profile = "um padrão focal de dificuldades, com repercussões mais localizadas e dependentes do contexto"

    return (
        f"Em análise clínica, os resultados do E-TDAH-PAIS indicam que {name} apresenta {synthesis}. O perfil sugere {profile}, devendo ser compreendido de forma integrada aos dados cognitivos, atencionais, executivos, emocionais e comportamentais obtidos ao longo da avaliação neuropsicológica."
    )


def _hypothesis_text(results: Dict[str, Any]) -> str:
    attention = _is_clinical(results["fator_4"].get("classification", ""))
    hyperactivity = _is_clinical(results["fator_2"].get("classification", ""))
    emotion = _is_clinical(results["fator_1"].get("classification", ""))
    adaptive = _is_clinical(results["fator_3"].get("classification", ""))

    if attention and hyperactivity:
        return (
            "Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade, apresentação combinada, conforme critérios do DSM-5-TR, desde que os achados sejam convergentes com a anamnese, observação clínica, prejuízo funcional e demais instrumentos aplicados."
        )

    if attention:
        return (
            "Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade, apresentação predominantemente desatenta, conforme critérios do DSM-5-TR, desde que haja convergência com os demais dados clínicos e funcionais da avaliação."
        )

    if hyperactivity:
        return (
            "Há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade, apresentação predominantemente hiperativa/impulsiva, conforme critérios do DSM-5-TR, desde que os sintomas estejam presentes em diferentes contextos e com prejuízo funcional clinicamente significativo."
        )

    if emotion and adaptive and not attention and not hyperactivity:
        return (
            "Os resultados indicam prejuízos emocionais e adaptativos relevantes, sem configuração suficiente, pelo E-TDAH-PAIS isoladamente, de perfil típico de TDAH. Recomenda-se análise integrada com os demais instrumentos, especialmente medidas de ansiedade, humor, responsividade social, funções executivas e dados da anamnese."
        )

    return ""


def generate_report(raw_scores: Dict[str, int], age: int, sex: str, patient_name: str | None = None) -> str:
    results = interpret_results(raw_scores, age, sex)
    first_name = _first_name(patient_name)

    paragraphs = [
        f"Interpretação e Observações Clínicas: A avaliação comportamental de {first_name} por meio da Escala E-TDAH-PAIS permitiu investigar aspectos relacionados à regulação emocional, hiperatividade/impulsividade, comportamento adaptativo e atenção, a partir da percepção dos responsáveis, fornecendo subsídios para a compreensão do funcionamento comportamental no contexto familiar e cotidiano.",
    ]

    for key in FACTOR_ORDER:
        paragraphs.append(_factor_paragraph(key, results[key]))

    paragraphs.append(_analysis_text(first_name, results))
    hypothesis = _hypothesis_text(results)
    if hypothesis:
        paragraphs.append(hypothesis)

    return "\n\n".join(paragraphs)
