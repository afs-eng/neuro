from typing import Dict, Any, Union

from .config import FACTOR_NAMES, NORMS, MEANS, FACTOR_ORDER
from .calculators import formatar_percentil_e_classificacao


CLINICAL_DIFFICULTY = {"Média Superior", "Superior"}
NON_CLINICAL = {"Inferior", "Média Inferior", "Média"}

FACTOR_LABELS = {
    "D": "Fator 1 - Desatenção",
    "I": "Fator 2 - Impulsividade",
    "AE": "Fator 3 - Aspectos Emocionais",
    "AAMA": "Fator 4 - Autorregulação da Atenção, da Motivação e da Ação",
    "H": "Fator 5 - Hiperatividade",
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


def _factor_paragraph(factor_key: str, result: dict) -> str:
    classification = result.get("classification", "Média")
    header = FACTOR_LABELS[factor_key]

    if factor_key == "D":
        if classification in NON_CLINICAL:
            body = (
                f"O resultado foi classificado como {classification}, não configurando prejuízo clínico nesse domínio. "
                "Esse padrão sugere funcionamento atencional globalmente compatível com o esperado, sem evidências consistentes de distraibilidade excessiva, perda frequente do foco, falhas marcantes de organização ou dificuldade relevante de sustentação atencional no autorrelato."
            )
        else:
            body = (
                f"O resultado situou-se na classificação {classification}, configurando indicativo de dificuldade clínica nesse domínio. "
                "Esse achado sugere presença de comportamentos associados à desatenção, como dificuldade de manter o foco, sustentar o esforço mental, organizar tarefas, acompanhar demandas sequenciais e conservar informações relevantes em mente durante a execução de atividades."
            )
    elif factor_key == "I":
        if classification in NON_CLINICAL:
            body = (
                f"O desempenho apresentou classificação {classification}, não indicando prejuízo clínico nesse domínio. "
                "Esse resultado sugere controle globalmente adequado das respostas impulsivas, sem sinais consistentes de precipitação comportamental, dificuldade significativa de inibição ou comprometimento relevante no seguimento de regras segundo o autorrelato."
            )
        else:
            body = (
                f"O desempenho situou-se na classificação {classification}, configurando indicativo de dificuldade clínica relevante nesse domínio. "
                "Esse perfil sugere tendência a responder de forma precipitada, dificuldade em inibir impulsos imediatos, menor tolerância à espera e possíveis repercussões no convívio interpessoal, na tomada de decisão e na autorregulação comportamental."
            )
    elif factor_key == "AE":
        if classification in NON_CLINICAL:
            body = (
                f"O escore foi classificado como {classification}, o que não indica prejuízo clínico relevante nesse domínio. "
                "Esse padrão sugere estabilidade emocional globalmente preservada no autorrelato, sem evidências consistentes de sofrimento afetivo acentuado, autopercepção cronicamente negativa, retraimento importante ou dificuldade emocional clinicamente significativa associada ao quadro investigado."
            )
        else:
            body = (
                f"O escore apresentou classificação {classification}, indicando dificuldade clínica nesse domínio. "
                "Esse achado sugere maior presença de sofrimento subjetivo, oscilação emocional, sensação de fracasso, dificuldade no manejo de frustrações e possível repercussão afetiva secundária às dificuldades atencionais e comportamentais referidas."
            )
    elif factor_key == "AAMA":
        if classification in NON_CLINICAL:
            body = (
                f"O resultado apresentou classificação {classification}, não indicando prejuízo clínico nesse domínio. "
                "Esse padrão sugere capacidade globalmente preservada de organizar metas, regular o próprio comportamento, sustentar motivação e conduzir ações de forma coerente com os objetivos propostos."
            )
        else:
            body = (
                f"O resultado apresentou classificação {classification}, configurando indicativo de dificuldade clínica significativa nesse domínio. "
                "Esse achado sugere prejuízos na capacidade de estabelecer prioridades, manter motivação ao longo do tempo, organizar etapas de ação, persistir diante de obstáculos e ajustar estratégias de forma eficiente para alcançar objetivos."
            )
    else:
        if classification in NON_CLINICAL:
            body = (
                f"O resultado foi classificado como {classification}, não configurando prejuízo clínico nesse domínio. "
                "Esse perfil sugere ausência de indicadores consistentes de inquietação motora excessiva, agitação persistente ou aceleração comportamental com repercussão funcional importante no cotidiano."
            )
        else:
            body = (
                f"O resultado foi classificado como {classification}, indicando dificuldade clínica nesse domínio. "
                "Esse achado sugere presença de inquietação, agitação comportamental, aceleração do ritmo de ação e instabilidade na condução das atividades, com potencial impacto sobre a qualidade do desempenho cotidiano e a manutenção da organização comportamental."
            )

    return f"{header}\n{body}"


def _general_summary(results: Dict[str, Any]) -> str:
    elevated = [FACTOR_LABELS[key].replace("Fator 1 - ", "").replace("Fator 2 - ", "").replace("Fator 3 - ", "").replace("Fator 4 - ", "").replace("Fator 5 - ", "") for key in FACTOR_ORDER if _is_clinical(results[key].get("classification", ""))]

    if not elevated:
        body = (
            "A distribuição dos fatores não evidencia um padrão global de comprometimento clínico no autorrelato. Ainda assim, a interpretação final deve considerar a articulação com a anamnese, a observação clínica e os demais instrumentos, uma vez que manifestações situacionais ou subjetivas podem não se expressar de forma homogênea em todos os domínios."
        )
    elif len(elevated) <= 2:
        body = (
            f"Embora a versão normativa atualmente utilizada no sistema não disponibilize uma classificação padronizada de escore geral para o ETDAH-AD, a distribuição interna dos fatores sugere um perfil mais focal, com elevação significativa em {', '.join(elevated)} e repercussões funcionais mais localizadas."
        )
    else:
        body = (
            "Embora a versão normativa atualmente utilizada no sistema não disponibilize uma classificação padronizada de escore geral para o ETDAH-AD, a elevação observada em múltiplos fatores sugere um padrão mais disseminado de dificuldades autorreferidas, com impacto mais amplo sobre atenção, autorregulação, estabilidade emocional e organização comportamental."
        )

    return f"Escore Geral\n{body}"


def _integrated_analysis(results: Dict[str, Any]) -> str:
    elevated = []
    impact_map = {
        "D": "atenção e organização",
        "I": "controle da resposta e manejo interpessoal",
        "AE": "estabilidade emocional e sofrimento subjetivo",
        "AAMA": "autorregulação executiva e persistência",
        "H": "ritmo comportamental e inquietação",
    }
    for key in FACTOR_ORDER:
        if _is_clinical(results[key].get("classification", "")):
            elevated.append(impact_map[key])

    if not elevated:
        return (
            "Análise Integrada\n"
            "O autorrelato obtido no ETDAH-AD não apontou elevações clinicamente significativas nos domínios investigados, sugerindo percepção subjetiva globalmente preservada. Ainda assim, a compreensão clínica final deve integrar esses dados com desempenho em testes objetivos, observação durante a avaliação e história de desenvolvimento."
        )

    if len(elevated) <= 2:
        return (
            "Análise Integrada\n"
            f"A integração dos resultados do ETDAH-AD com os demais instrumentos pode revelar um perfil parcialmente dissociado entre sintomas autorreferidos e desempenho psicométrico. No presente protocolo, as elevações concentram-se sobretudo em {', '.join(elevated)}, sugerindo que parte do sofrimento funcional pode manifestar-se de forma mais subjetiva, ecológica ou situacional, nem sempre captada integralmente por medidas estruturadas de desempenho."
        )

    return (
        "Análise Integrada\n"
        f"A distribuição das elevações no ETDAH-AD sugere convergência interna entre dificuldades autorreferidas em {', '.join(elevated)}. Esse padrão favorece a compreensão de um conjunto mais amplo de repercussões sobre atenção, autorregulação, controle da resposta e organização do comportamento, devendo ser integrado aos achados observacionais e instrumentais do restante da avaliação."
    )


def _final_paragraph(patient_name: str, results: Dict[str, Any]) -> str:
    domain_map = {
        "D": "desatenção",
        "I": "impulsividade",
        "AE": "aspectos emocionais",
        "AAMA": "autorregulação da atenção, da motivação e da ação",
        "H": "hiperatividade",
    }
    elevated = [domain_map[key] for key in FACTOR_ORDER if _is_clinical(results[key].get("classification", ""))]

    if not elevated:
        return (
            f"Em análise clínica, o autorrelato de {patient_name} no ETDAH-AD não sugere comprometimento clinicamente significativo nos domínios investigados, permanecendo fundamental a integração desses achados com a observação clínica, a anamnese e os demais instrumentos para uma conclusão diagnóstica abrangente."
        )

    if len(elevated) == 1:
        joined = elevated[0]
    elif len(elevated) == 2:
        joined = f"{elevated[0]} e {elevated[1]}"
    else:
        joined = f"{', '.join(elevated[:-1])} e {elevated[-1]}"

    return (
        f"Em análise clínica, a integração entre o autorrelato do ETDAH-AD e os demais dados da avaliação sugere que {patient_name} apresenta dificuldades predominantes nos domínios de {joined}, com repercussão funcional sobre atenção, organização do comportamento e autorregulação. Esses achados não devem ser interpretados isoladamente e precisam ser articulados à observação clínica, à anamnese e aos demais instrumentos antes de qualquer definição diagnóstica final."
    )


def generate_report(raw_scores: Dict[str, int], schooling: Union[int, str], patient_name: str | None = None) -> str:
    results = interpret_results(raw_scores, schooling)
    first_name = _first_name(patient_name)

    paragraphs = [
        "Interpretação e Observações Clínicas: A Escala ETDAH-AD é um instrumento de autorrelato destinado à identificação de sintomas associados ao Transtorno do Déficit de Atenção e Hiperatividade em adolescentes e adultos, avaliando domínios relacionados à desatenção, impulsividade, aspectos emocionais, autorregulação da atenção, da motivação e da ação, além de hiperatividade. O instrumento permite quantificar a intensidade das manifestações referidas pelo próprio avaliado, contribuindo para a compreensão do impacto funcional desses sintomas em diferentes contextos da vida cotidiana."
    ]

    for factor in FACTOR_ORDER:
        paragraphs.append(_factor_paragraph(factor, results[factor]))

    paragraphs.append(_general_summary(results))
    paragraphs.append(_integrated_analysis(results))
    paragraphs.append(_final_paragraph(first_name, results))

    return "\n\n".join(paragraphs)
