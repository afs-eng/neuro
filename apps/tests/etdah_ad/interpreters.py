from typing import Any, Dict, Union

from .calculators import formatar_percentil_e_classificacao
from .config import FACTOR_NAMES, FACTOR_ORDER, MEANS, NORMS


CLINICAL_DIFFICULTY = {"Média Superior", "Superior"}

FACTOR_LABELS = {
    "D": "Fator 1 — Desatenção",
    "I": "Fator 2 — Impulsividade",
    "AE": "Fator 3 — Aspectos Emocionais",
    "AAMA": "Fator 4 — Autorregulação da Atenção, Motivação e Ação",
    "H": "Fator 5 — Hiperatividade",
}

DOMAIN_NAMES = {
    "D": "desatenção",
    "I": "impulsividade",
    "AE": "aspectos emocionais",
    "AAMA": "autorregulação da atenção, motivação e ação",
    "H": "hiperatividade",
}


def get_schooling_level(schooling: Union[int, str]) -> str:
    if isinstance(schooling, str):
        if schooling in ("preschool", "elementary"):
            return "fundamental"
        if schooling in ("middle",):
            return "medio"
        if schooling in ("higher", "higher_incomplete"):
            return "superior"
    if isinstance(schooling, (int, float)):
        if schooling <= 9:
            return "fundamental"
        if schooling <= 12:
            return "medio"
        return "superior"
    return "fundamental"


def interpret_results(raw_scores: Dict[str, int], schooling: Union[int, str]) -> Dict[str, Any]:
    schooling_level = get_schooling_level(schooling)

    results = {}
    for factor in FACTOR_ORDER:
        score = raw_scores.get(factor, 0)
        mean = MEANS[schooling_level][factor]
        percentil_txt, classificacao = formatar_percentil_e_classificacao(
            score, NORMS[schooling_level][factor]
        )

        results[factor] = {
            "name": FACTOR_NAMES[factor],
            "raw_score": score,
            "mean": mean,
            "percentile_text": percentil_txt,
            "classification": classificacao,
        }

    return results


def _first_name(patient_name: str | None) -> str:
    if not patient_name:
        return "o avaliado"
    return patient_name.strip().split()[0] or "o avaliado"


def _is_clinical(classification: str) -> bool:
    return classification in CLINICAL_DIFFICULTY


def _classification_text(result: dict) -> str:
    return str(result.get("classification") or "Média")


def _percentile_text(result: dict) -> str:
    return str(result.get("percentile_text") or "-")


def _factor_paragraph(factor_key: str, result: dict, name: str) -> str:
    classification = _classification_text(result)
    percentile = _percentile_text(result)

    if factor_key == "D":
        if classification == "Superior":
            body = (
                f"indica prejuízo grave na atenção sustentada. {name} apresenta dificuldade significativa para manter o foco em atividades prolongadas, com oscilação atencional frequente, maior distraibilidade, lentificação no início ou na conclusão de tarefas e necessidade aumentada de redirecionamento externo, sobretudo em demandas com baixo interesse, alta exigência cognitiva ou maior necessidade de organização autônoma."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo moderado nos mecanismos atencionais, com dificuldade para sustentar o foco, manter continuidade em tarefas prolongadas e resistir a distrações. Esse padrão pode repercutir na organização acadêmica/profissional, no cumprimento de prazos e na eficiência em atividades que exigem persistência mental."
            )
        else:
            body = (
                "indica funcionamento dentro dos limites esperados, sem evidências de prejuízo clínico significativo na atenção sustentada segundo o autorrelato. Esse achado deve ser interpretado em conjunto com os testes objetivos de atenção e as observações clínicas."
            )
    elif factor_key == "I":
        if classification == "Superior":
            body = (
                f"indica prejuízo grave no controle inibitório comportamental. {name} pode apresentar tendência a agir de forma precipitada, responder antes de avaliar adequadamente a situação, ter dificuldade de aguardar, interromper atividades ou interações e demonstrar menor controle sobre respostas imediatas, especialmente em contextos emocionalmente ativadores ou com alta demanda de autocontrole."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo moderado no controle inibitório, com tendência a respostas precipitadas, dificuldade de espera e menor planejamento antes da ação. Esse padrão pode interferir na qualidade das interações sociais, no cumprimento de regras e na organização do comportamento."
            )
        else:
            body = (
                f"é interpretado como dentro da normalidade, sem indicativos de prejuízo clínico relevante no controle inibitório segundo o autorrelato. Esse resultado sugere que {name} tende a manter respostas relativamente controladas, sem padrão consistente de impulsividade comportamental."
            )
    elif factor_key == "AE":
        if classification == "Superior":
            body = (
                "indica prejuízo grave na regulação emocional, com maior reatividade afetiva, baixa tolerância à frustração, oscilação emocional e dificuldade de manejar respostas emocionais de forma adaptativa. Esse padrão pode intensificar dificuldades atencionais e comportamentais, especialmente em situações de cobrança, frustração, conflito ou sobrecarga."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo moderado na regulação emocional, com tendência a maior sensibilidade a frustrações, irritabilidade, instabilidade afetiva e dificuldade em recuperar o equilíbrio emocional após situações adversas."
            )
        else:
            body = (
                "indica funcionamento dentro dos limites esperados, sem evidências de prejuízo clínico significativo na regulação emocional segundo este instrumento."
            )
    elif factor_key == "AAMA":
        if classification == "Superior":
            body = (
                f"indica prejuízo grave nos mecanismos de planejamento, persistência e manutenção do esforço mental. {name} pode apresentar dificuldade significativa para iniciar tarefas, manter constância, organizar etapas, monitorar o próprio desempenho e concluir atividades sem apoio externo, especialmente em demandas longas, repetitivas ou pouco estimulantes."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo moderado na organização da ação, persistência e sustentação motivacional. Esse padrão pode repercutir na autonomia, na produtividade e na capacidade de manter desempenho consistente ao longo do tempo."
            )
        else:
            body = (
                "é interpretado como dentro da normalidade, sem indicativos de prejuízo clínico relevante nos mecanismos de planejamento, persistência e manutenção do esforço mental segundo este instrumento."
            )
    elif factor_key == "H":
        if classification == "Superior":
            body = (
                "indica prejuízo grave relacionado à agitação motora e inquietação. Observa-se tendência a aumento da ativação psicomotora, dificuldade em permanecer em repouso, necessidade elevada de movimentação e maior inquietação interna, especialmente em contextos estruturados ou que exigem permanência atencional prolongada."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo moderado relacionado à inquietação motora, necessidade aumentada de movimento e dificuldade em permanecer em atividades que exigem controle corporal e permanência prolongada."
            )
        else:
            body = (
                "indica ausência de prejuízo clínico significativo relacionado à agitação motora ou inquietação psicomotora segundo o autorrelato."
            )
    else:
        if classification == "Superior":
            body = (
                "indica prejuízo clínico global grave, com presença significativa de manifestações comportamentais e autorregulatórias compatíveis com sintomas de TDAH. Esse resultado deve ser interpretado em conjunto com a distribuição dos fatores, o prejuízo funcional, a anamnese, a observação clínica e os demais instrumentos aplicados."
            )
        elif classification == "Média Superior":
            body = (
                "sugere prejuízo clínico global moderado, com indicadores relevantes de dificuldade atencional, comportamental ou autorregulatória. A interpretação deve considerar quais fatores sustentam a elevação global e se há impacto funcional consistente."
            )
        else:
            body = (
                "sugere funcionamento autorregulatório global dentro dos limites esperados, podendo coexistir com elevações específicas em fatores isolados. Nesses casos, a análise deve destacar os domínios clinicamente elevados e evitar concluir prejuízo global quando o escore total não estiver elevado."
            )

    if factor_key == "escore_geral":
        return f"Escore Geral: classificado como {classification} (percentil {percentile}), {body}"
    return f"No {FACTOR_LABELS[factor_key]}, o resultado classificado como {classification} (percentil {percentile}) {body}"


def _joined(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " e " + items[-1]


def _elevated_domains(results: Dict[str, Any]) -> list[str]:
    return [
        DOMAIN_NAMES[key]
        for key in FACTOR_ORDER
        if key != "escore_geral" and _is_clinical(results[key].get("classification", ""))
    ]


def _preserved_domains(results: Dict[str, Any]) -> list[str]:
    return [
        DOMAIN_NAMES[key]
        for key in FACTOR_ORDER
        if key != "escore_geral" and not _is_clinical(results[key].get("classification", ""))
    ]


def _integrated_analysis(results: Dict[str, Any]) -> str:
    elevated = _elevated_domains(results)
    preserved = _preserved_domains(results)

    if not elevated:
        return (
            "Em análise integrada, os resultados da E-TDAH-AD indicam um padrão sem elevações clinicamente significativas nos domínios investigados, associado a preservação de desatenção, impulsividade, aspectos emocionais, autorregulação e hiperatividade. Esse perfil sugere funcionamento autorreferido globalmente preservado, devendo ser compreendido à luz dos achados cognitivos, atencionais, executivos, comportamentais e observacionais obtidos ao longo da avaliação neuropsicológica."
        )

    synthesis = _joined(elevated)
    preserved_text = _joined(preserved) if preserved else "ausência de domínios claramente preservados"

    if len(elevated) <= 2:
        clinical = "um perfil mais focal, com dificuldades concentradas em domínios específicos"
    else:
        clinical = "um perfil mais disseminado de dificuldades autorreferidas, com repercussão ampliada sobre o funcionamento cotidiano"

    return (
        f"Em análise integrada, os resultados da E-TDAH-AD indicam um padrão caracterizado por elevação em {synthesis}, associado a preservação relativa de {preserved_text}. Esse perfil sugere {clinical}, devendo ser compreendido à luz dos achados cognitivos, atencionais, executivos, comportamentais e observacionais obtidos ao longo da avaliação neuropsicológica."
    )


def _hypothesis_text(results: Dict[str, Any]) -> str:
    attention = _is_clinical(results["D"].get("classification", ""))
    impulsivity = _is_clinical(results["I"].get("classification", ""))
    hyperactivity = _is_clinical(results["H"].get("classification", ""))
    emotional = _is_clinical(results["AE"].get("classification", ""))

    if attention and hyperactivity:
        return (
            "Dessa forma, há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade (TDAH), apresentação combinada, conforme critérios do DSM-5-TR, desde que os achados sejam convergentes com a anamnese, observação clínica, prejuízo funcional e demais instrumentos aplicados."
        )
    if attention and not hyperactivity and not impulsivity:
        return (
            "Dessa forma, há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade (TDAH), apresentação predominantemente desatenta, conforme critérios do DSM-5-TR, desde que haja convergência clínica e funcional com os demais dados da avaliação."
        )
    if (hyperactivity or impulsivity) and not attention:
        return (
            "Dessa forma, há hipótese diagnóstica de Transtorno do Déficit de Atenção e Hiperatividade (TDAH), apresentação predominantemente hiperativa/impulsiva, conforme critérios do DSM-5-TR, desde que os sintomas estejam presentes em diferentes contextos e associados a prejuízo funcional clinicamente significativo."
        )
    if emotional and not attention and not hyperactivity and not impulsivity:
        return (
            "Dessa forma, os achados indicam prejuízo emocional relevante, sem configuração suficiente, pela E-TDAH-AD isoladamente, de perfil típico de TDAH. Recomenda-se análise integrada com instrumentos de ansiedade, humor, observação clínica e dados da anamnese."
        )
    return (
        "Dessa forma, os resultados da E-TDAH-AD não sustentam, isoladamente, hipótese diagnóstica de TDAH no momento da avaliação, devendo a interpretação ser integrada aos demais achados clínicos e neuropsicológicos."
    )


def generate_report(raw_scores: Dict[str, int], schooling: Union[int, str], patient_name: str | None = None) -> str:
    results = interpret_results(raw_scores, schooling)
    first_name = _first_name(patient_name)

    paragraphs = [
        "Interpretação e Observações Clínicas: A Escala E-TDAH-AD tem como finalidade identificar manifestações comportamentais e emocionais relacionadas à atenção, impulsividade, regulação emocional, motivação e hiperatividade, fornecendo indicadores quantitativos do funcionamento autorregulatório e atencional (Benczik, 2005).",
    ]

    for factor in FACTOR_ORDER:
        paragraphs.append(_factor_paragraph(factor, results[factor], first_name))

    paragraphs.append(_integrated_analysis(results))
    paragraphs.append(_hypothesis_text(results))

    return "\n\n".join(paragraphs)
