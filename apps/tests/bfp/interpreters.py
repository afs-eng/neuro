from __future__ import annotations

from .calculators import classify_bfp_domain
from .config import (
    BFP_CLOSING_TEXT,
    FACTOR_DEFINITIONS,
    FACTOR_INTERPRETATION_TEMPLATES,
    FACTOR_INTERPRETIVE_NAMES,
    FACET_DEFINITIONS,
    FACET_TEMPLATES,
    SAMPLE_LABELS,
)


def _first_name(patient_name: str) -> str:
    return (patient_name or "Paciente").strip().split(" ", 1)[0] or "Paciente"


def _factor_key(factor_code: str) -> str:
    return FACTOR_INTERPRETIVE_NAMES[factor_code]


def _factor_result(factors: dict, code: str) -> dict:
    return factors.get(code) or {}


def _facet_direction(classification: str) -> str:
    level = classify_bfp_domain(classification)
    if level == "elevado":
        return "a maior"
    if level == "reduzido":
        return "a menor"
    return "a moderada"


def _interpret_factor(factor_result: dict) -> str:
    factor_name = _factor_key(factor_result["code"])
    level = factor_result.get("domain_level") or classify_bfp_domain(factor_result["classification"])
    template_key = "medio" if level == "medio" else level
    return FACTOR_INTERPRETATION_TEMPLATES[factor_name][template_key].format(
        classification=factor_result["classification"]
    )


def _interpret_facet(facet_result: dict) -> str:
    template = FACET_TEMPLATES.get(facet_result["code"])
    if not template:
        return ""
    return template.format(
        classification=facet_result["classification"],
        direction=_facet_direction(facet_result["classification"]),
    )


def _relevant_factors(factors: dict) -> list[dict]:
    return [
        result
        for code in FACTOR_DEFINITIONS
        if (result := factors.get(code)) and result.get("domain_level") != "medio"
    ]


def _relevant_facets(facets: dict) -> list[dict]:
    return [
        result
        for code in FACET_DEFINITIONS
        if (result := facets.get(code)) and result.get("domain_level") != "medio"
    ]


def _build_summary(name: str, relevant_factors: list[dict]) -> str:
    if not relevant_factors:
        return (
            f"{name} apresentou resultados globalmente situados em faixas médias nos fatores principais do BFP, "
            "sem elevações ou reduções clinicamente salientes na estrutura geral da personalidade."
        )

    parts = []
    for factor in relevant_factors:
        level = factor.get("domain_level")
        direction = "elevação" if level == "elevado" else "redução"
        parts.append(f"{direction} em {factor['name']}")

    if len(parts) == 1:
        joined = parts[0]
    else:
        joined = ", ".join(parts[:-1]) + f" e {parts[-1]}"

    return f"{name} apresentou {joined} entre os fatores principais do BFP, configurando um perfil de personalidade com aspectos clinicamente relevantes a serem integrados ao restante da avaliação."


def _build_integration(factors: dict) -> str:
    notes: list[str] = []
    nn = _factor_result(factors, "NN")
    ee = _factor_result(factors, "EE")
    ss = _factor_result(factors, "SS")
    rr = _factor_result(factors, "RR")
    aa = _factor_result(factors, "AA")

    if nn.get("domain_level") == "elevado" and rr.get("domain_level") == "reduzido":
        notes.append(
            "A combinação entre elevação em Neuroticismo e redução em Realização pode sugerir maior vulnerabilidade emocional associada a dificuldades de organização, persistência e autorregulação comportamental."
        )
    if nn.get("domain_level") == "elevado" and ee.get("domain_level") == "reduzido":
        notes.append(
            "A elevação em Neuroticismo associada à redução em Extroversão pode indicar maior tendência à vivência interna de sofrimento emocional, com menor busca espontânea por apoio social ou maior reserva interpessoal."
        )
    if ss.get("domain_level") == "reduzido" and nn.get("domain_level") == "elevado":
        notes.append(
            "A combinação entre menor Socialização e maior Neuroticismo pode sugerir maior vulnerabilidade a conflitos interpessoais, sensibilidade a críticas e dificuldade de regulação emocional em contextos relacionais."
        )
    if rr.get("domain_level") == "reduzido":
        notes.append(
            "A redução em Realização pode reforçar a hipótese de dificuldades funcionais em planejamento, organização, persistência e gerenciamento de tarefas, especialmente quando articulada a queixas atencionais ou executivas."
        )
    if aa.get("domain_level") == "reduzido":
        notes.append(
            "A redução em Abertura à Experiência pode sugerir maior preferência por previsibilidade, rotinas conhecidas e menor tolerância a mudanças, quando compatível com os dados clínicos e observacionais."
        )

    if not notes:
        return (
            "Em análise clínica, o perfil de personalidade sugere tendências globalmente compatíveis com a amostra normativa, "
            "sem combinações fatoriais que indiquem, isoladamente, risco interpretativo elevado."
        )

    return "Em análise clínica, " + " ".join(notes)


def build_bfp_interpretation_payload(merged_data: dict, patient_name: str | None = None) -> dict:
    name = _first_name(patient_name or "Paciente")
    sample = merged_data.get("sample", "geral")
    factors = merged_data.get("factors", {})
    facets = merged_data.get("facets", {})

    if not factors or not facets:
        return {
            "summary": "Sem resultados suficientes para interpretação do BFP.",
            "factors": {},
            "facets": {},
            "clinical_integration": BFP_CLOSING_TEXT,
        }

    relevant_factors = _relevant_factors(factors)
    relevant_facets = _relevant_facets(facets)

    factor_texts = {
        code: _interpret_factor(factors[code])
        for code in FACTOR_DEFINITIONS
        if code in factors
    }
    facet_texts = {
        facet["code"]: _interpret_facet(facet)
        for facet in relevant_facets
        if _interpret_facet(facet)
    }

    return {
        "summary": _build_summary(name, relevant_factors),
        "sample_label": SAMPLE_LABELS.get(sample, sample.title()),
        "factors": factor_texts,
        "facets": facet_texts,
        "clinical_integration": _build_integration(factors),
        "closing": BFP_CLOSING_TEXT,
    }


def build_bfp_interpretation(merged_data: dict, patient_name: str | None = None) -> str:
    payload = build_bfp_interpretation_payload(merged_data, patient_name=patient_name)
    sample_label = payload.get("sample_label", "Geral")
    paragraphs = [
        f"A Bateria Fatorial de Personalidade (BFP) foi utilizada para investigar traços de personalidade com base no modelo dos Cinco Grandes Fatores, permitindo compreender tendências emocionais, interpessoais, motivacionais e comportamentais. A correção foi realizada com base na amostra {sample_label.lower()}.",
        payload["summary"],
    ]

    factor_texts = payload.get("factors", {})
    relevant_factor_codes = [
        code
        for code in FACTOR_DEFINITIONS
        if code in factor_texts and classify_bfp_domain((merged_data.get("factors", {}).get(code) or {}).get("classification", "Média")) != "medio"
    ]
    if not relevant_factor_codes:
        relevant_factor_codes = [code for code in FACTOR_DEFINITIONS if code in factor_texts]
    paragraphs.extend(factor_texts[code] for code in relevant_factor_codes)

    facet_texts = payload.get("facets", {})
    if facet_texts:
        paragraphs.append("Nas facetas clinicamente relevantes, observaram-se os seguintes destaques:")
        paragraphs.extend(facet_texts[code] for code in FACET_DEFINITIONS if code in facet_texts)

    paragraphs.append(payload["clinical_integration"])
    paragraphs.append(payload["closing"])
    return "\n\n".join(paragraphs)


def get_report_interpretation(merged_data: dict, patient_name: str | None = None) -> str:
    return build_bfp_interpretation(merged_data, patient_name=patient_name)
