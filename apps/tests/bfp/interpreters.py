from __future__ import annotations

from .config import FACTOR_DEFINITIONS, FACET_DEFINITIONS, MIDDLE_TEXT, SAMPLE_LABELS


def _first_name(patient_name: str) -> str:
    return (patient_name or "Paciente").strip().split(" ", 1)[0] or "Paciente"


def _facet_text(facet_result: dict) -> str:
    definition = FACET_DEFINITIONS[facet_result["code"]]
    percentile = facet_result["percentile"]
    if percentile > 70.5:
        return definition["high_text"]
    if percentile < 30:
        return definition["low_text"]
    return MIDDLE_TEXT


def build_bfp_interpretation(merged_data: dict, patient_name: str | None = None) -> str:
    name = _first_name(patient_name or "Paciente")
    sample = merged_data.get("sample", "geral")
    sample_label = SAMPLE_LABELS.get(sample, sample.title())
    factors = merged_data.get("factors", {})
    facets = merged_data.get("facets", {})

    if not factors or not facets:
        return "Sem resultados suficientes para interpretação do BFP."

    paragraphs = [
        f"{name} respondeu à Bateria Fatorial de Personalidade (BFP), com correção pela amostra {sample_label.lower()}. O instrumento descreve o funcionamento predominante nos fatores Neuroticismo, Extroversão, Socialização, Realização e Abertura, e seus resultados devem ser interpretados em conjunto com entrevista clínica, observação comportamental e demais dados do processo avaliativo.",
    ]

    for factor_code, factor_definition in FACTOR_DEFINITIONS.items():
        factor_result = factors[factor_code]
        factor_name = factor_result["name"]
        facet_sentences = []
        for facet_code in factor_definition["facets"]:
            facet_result = facets[facet_code]
            facet_definition = FACET_DEFINITIONS[facet_code]
            facet_sentences.append(
                f"Na faceta {facet_definition['name']}, percentil {facet_result['percentile']:.1f} ({facet_result['classification'].lower()}), {_facet_text(facet_result)}"
            )

        paragraphs.append(
            f"No fator {factor_name}, {name} apresentou percentil {factor_result['percentile']:.1f}, classificado como {factor_result['classification'].lower()}, com escore médio bruto de {factor_result['raw_score']:.2f}. "
            + " ".join(facet_sentences)
        )

    return "\n\n".join(paragraphs)


def get_report_interpretation(merged_data: dict, patient_name: str | None = None) -> str:
    return build_bfp_interpretation(merged_data, patient_name=patient_name)
