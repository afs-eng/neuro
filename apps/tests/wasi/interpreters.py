from __future__ import annotations


def _first_name(patient_name: str) -> str:
    return (patient_name or "Paciente").strip().split(" ", 1)[0] or "Paciente"


def build_wasi_interpretation(merged_data: dict, patient_name: str | None = None) -> str:
    name = _first_name(patient_name or "Paciente")
    composites = merged_data.get("composites", {})
    verbal = composites.get("qi_verbal", {})
    execution = composites.get("qi_execucao", {})
    qit4 = composites.get("qit_4", {})
    qit2 = composites.get("qit_2", {})
    age = merged_data.get("age", {})

    paragraphs = [
        f"{name} foi avaliado(a) pelo WASI, com idade de {age.get('years', 0)} anos e {age.get('months', 0)} meses na data da aplicacao. O instrumento resume o desempenho em Vocabulário, Semelhanças, Cubos e Raciocínio Matricial, permitindo estimativas abreviadas de funcionamento intelectual verbal, de execucao e global.",
        f"No QI Verbal, obteve escore composto {verbal.get('qi', '-')}, classificado como {str(verbal.get('classification', '-')).lower()}, com percentil {verbal.get('percentile_display', '-')} e intervalo de confianca {verbal.get('confidence_interval', '-')}. No QI Execucao, obteve escore composto {execution.get('qi', '-')}, classificado como {str(execution.get('classification', '-')).lower()}, com percentil {execution.get('percentile_display', '-')} e intervalo de confianca {execution.get('confidence_interval', '-')}.",
        f"O QIT-4 foi {qit4.get('qi', '-')}, classificado como {str(qit4.get('classification', '-')).lower()}, com intervalo de confianca {qit4.get('confidence_interval', '-')}. O QIT-2 foi {qit2.get('qi', '-')}, classificado como {str(qit2.get('classification', '-')).lower()}, com intervalo de confianca {qit2.get('confidence_interval', '-')}.",
    ]

    warnings = [
        item.get("interpretability", {}).get("warning", "")
        for item in (verbal, execution, qit4, qit2)
        if item.get("interpretability", {}).get("warning")
    ]
    if warnings:
        paragraphs.append("Aspectos de interpretabilidade: " + " ".join(warnings))

    paragraphs.append(
        "Os resultados do WASI devem ser integrados a anamnese, observacao clinica e demais instrumentos da avaliacao, especialmente quando houver discrepancias relevantes entre os domínios verbal e nao verbal."
    )
    return "\n\n".join(paragraphs)
