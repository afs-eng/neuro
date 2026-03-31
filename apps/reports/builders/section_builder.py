DEFAULT_REPORT_SECTIONS = [
    ("identificacao", "Identificacao"),
    ("descricao_demanda", "Descricao da demanda"),
    ("procedimentos", "Procedimentos"),
    ("historia_pessoal_anamnese", "Historia pessoal / anamnese"),
    ("eficiencia_cognitiva", "Eficiencia cognitiva"),
    ("funcoes_executivas", "Funcoes executivas"),
    ("linguagem", "Linguagem"),
    ("gnosias_praxias", "Gnosias e praxias"),
    ("memoria_aprendizagem", "Memoria e aprendizagem"),
    ("bpa2", "BPA-2"),
    ("fdt", "FDT"),
    ("ravlt", "RAVLT"),
    ("epqj", "EPQ-J"),
    ("ebadep", "EBADEP"),
    ("etdah", "ETDAH"),
    ("conclusao", "Conclusao"),
    ("encaminhamentos", "Encaminhamentos"),
]


def build_section_source_payload(section_key: str, snapshot_payload: dict) -> dict:
    tests = snapshot_payload.get("validated_tests", [])
    anamnesis = snapshot_payload.get("anamnesis", {})
    if section_key in {"bpa2", "fdt", "epqj", "etdah"}:
        return {
            "tests": [item for item in tests if item["instrument_code"] == section_key]
        }
    if section_key == "ebadep":
        return {
            "tests": [
                item
                for item in tests
                if item["instrument_code"] in {"ebadep_a", "ebadep_ij"}
            ]
        }
    if section_key == "procedimentos":
        return {
            "validated_tests": tests,
            "documents": snapshot_payload.get("documents", []),
            "progress_entries": snapshot_payload.get("progress_entries", []),
        }
    if section_key == "historia_pessoal_anamnese":
        return {
            "anamnesis": anamnesis,
            "progress_entries": snapshot_payload.get("progress_entries", []),
        }
    return snapshot_payload


def build_section_text(
    section_key: str, snapshot_payload: dict, source_payload: dict
) -> str:
    patient = snapshot_payload.get("patient", {})
    evaluation = snapshot_payload.get("evaluation", {})

    if section_key == "identificacao":
        return (
            f"Paciente: {patient.get('full_name', '')}. "
            f"Avaliacao: {evaluation.get('code', '')}. "
            f"Titulo do caso: {evaluation.get('title', '')}."
        )
    if section_key == "descricao_demanda":
        return evaluation.get("referral_reason", "") or "Demanda nao registrada."
    if section_key == "procedimentos":
        test_names = [
            item["instrument_name"]
            for item in source_payload.get("validated_tests", [])
        ]
        document_names = [item["title"] for item in source_payload.get("documents", [])]
        parts = []
        if test_names:
            parts.append("Testes validados: " + ", ".join(test_names))
        if document_names:
            parts.append("Documentos relevantes: " + ", ".join(document_names))
        if not parts:
            return "Sem procedimentos estruturados suficientes no momento."
        return ". ".join(parts) + "."
    if section_key == "historia_pessoal_anamnese":
        anamnesis = source_payload.get("anamnesis", {})
        current = anamnesis.get("current_response") or {}
        summary = current.get("summary_payload") or {}
        relevant_points = summary.get("clinically_relevant_points") or []
        labeled_parts = [
            ("Queixa principal", summary.get("chief_complaint", "")),
            ("Contexto familiar", summary.get("family_context_summary", "")),
            ("Desenvolvimento", summary.get("development_summary", "")),
            ("Histórico clínico", summary.get("medical_history_summary", "")),
            ("Histórico escolar", summary.get("school_history_summary", "")),
            ("Sono e alimentação", summary.get("sleep_eating_summary", "")),
            ("Rotina", summary.get("routine_summary", "")),
        ]
        text = "\n\n".join(
            f"{label}: {value}" for label, value in labeled_parts if value
        )
        if current.get("submitted_by_name") or current.get("submitted_by_relation"):
            informer = f"Informante: {current.get('submitted_by_name', '')}"
            if current.get("submitted_by_relation"):
                informer += f" ({current.get('submitted_by_relation')})"
            text = informer + ("\n\n" + text if text else "")
        if relevant_points:
            text += "\n\nPontos clinicamente relevantes: " + "; ".join(relevant_points)
        risk_flags = summary.get("risk_flags") or []
        if risk_flags:
            text += "\n\nAlertas clínicos: " + ", ".join(risk_flags)
        return text or "Sem anamnese estruturada revisada para compor esta secao."
    if section_key in {"bpa2", "fdt", "epqj", "etdah", "ebadep"}:
        items = source_payload.get("tests", [])
        if not items:
            return "Teste nao aplicado ou ainda nao validado."
        return (
            "\n\n".join(
                item.get("interpretation_text", "")
                for item in items
                if item.get("interpretation_text")
            )
            or "Sem interpretacao persistida."
        )
    if section_key == "conclusao":
        return "Secao pronta para conclusao clinica integrada pelo profissional responsavel."
    if section_key == "encaminhamentos":
        return "Secao pronta para orientacoes e encaminhamentos finais."
    return "Secao preparada para preenchimento estruturado."
