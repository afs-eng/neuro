from collections.abc import Iterable

from apps.tests.base.types import TestContext
from apps.tests.registry import get_test_module
from apps.tests.selectors import get_validated_test_applications_by_evaluation


SECTION_MAP = {
    "wisc4": "eficiencia_intelectual",
    "bpa2": "atencao",
    "fdt": "funcoes_executivas",
    "ravlt": "memoria_aprendizagem",
    "epq_j": "escalas_complementares",
    "scared": "escalas_complementares",
    "srs2": "escalas_complementares",
    "ebadep_a": "escalas_complementares",
    "ebaped_ij": "escalas_complementares",
    "etdah_ad": "atencao",
    "etdah_pais": "atencao",
}


def _clean_text(value) -> str:
    if value is None:
        return ""
    return str(value).replace("_", " ").strip()


def _format_number(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


def _format_result_line(label: str, *parts) -> str:
    details = [str(part).strip() for part in parts if part not in (None, "", [], {})]
    suffix = " | ".join(details)
    return f"- {label}: {suffix}" if suffix else f"- {label}"


def _extract_generic_rows(data, depth: int = 0) -> list[str]:
    if depth > 2:
        return []

    rows: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            label = _clean_text(key).title()
            if isinstance(value, dict):
                simple_parts = []
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, (dict, list)):
                        continue
                    simple_parts.append(
                        f"{_clean_text(sub_key)} {_format_number(sub_value)}"
                    )
                if simple_parts:
                    rows.append(_format_result_line(label, *simple_parts[:4]))
                else:
                    rows.extend(_extract_generic_rows(value, depth + 1))
            elif isinstance(value, list):
                if value and all(isinstance(item, dict) for item in value):
                    for item in value[:6]:
                        item_label = _clean_text(
                            item.get("nome")
                            or item.get("subteste")
                            or item.get("name")
                            or item.get("indice")
                            or key
                        ).title()
                        details = []
                        for field in (
                            "escore_composto",
                            "escore_padrao",
                            "raw_score",
                            "valor",
                            "total",
                            "percentil",
                            "percentil_num",
                            "classificacao",
                            "classification",
                        ):
                            if field in item and item[field] not in (None, ""):
                                details.append(
                                    f"{_clean_text(field)} {_format_number(item[field])}"
                                )
                        rows.append(_format_result_line(item_label, *details[:4]))
                elif value and all(
                    not isinstance(item, (dict, list)) for item in value
                ):
                    rows.append(
                        _format_result_line(
                            label, ", ".join(_format_number(item) for item in value[:8])
                        )
                    )
            else:
                rows.append(_format_result_line(label, _format_number(value)))
    return rows[:12]


def _build_wisc4_rows(payload: dict) -> list[str]:
    rows = []
    qit = payload.get("qit_data") or {}
    if qit:
        rows.append(
            _format_result_line(
                "QI Total",
                f"escore composto {_format_number(qit.get('escore_composto'))}",
                f"percentil {_format_number(qit.get('percentil'))}",
            )
        )
    for item in (payload.get("indices") or [])[:6]:
        rows.append(
            _format_result_line(
                item.get("nome") or item.get("indice") or "Indice",
                f"escore composto {_format_number(item.get('escore_composto'))}",
                f"percentil {_format_number(item.get('percentil'))}",
            )
        )
    strengths = payload.get("pontos_fortes") or []
    if strengths:
        rows.append(_format_result_line("Pontos fortes", ", ".join(strengths)))
    weaknesses = payload.get("pontos_fragilizados") or []
    if weaknesses:
        rows.append(_format_result_line("Pontos fragilizados", ", ".join(weaknesses)))
    return rows


def _build_bpa2_rows(payload: dict) -> list[str]:
    rows = []
    for item in payload.get("subtestes") or []:
        rows.append(
            _format_result_line(
                item.get("subteste") or item.get("codigo") or "Subteste",
                f"total {_format_number(item.get('total'))}",
                f"percentil {_format_number(item.get('percentil'))}",
                item.get("classificacao"),
            )
        )
    return rows


def _build_fdt_rows(payload: dict) -> list[str]:
    rows = []
    for item in payload.get("metric_results") or []:
        rows.append(
            _format_result_line(
                item.get("nome") or item.get("codigo") or "Metrica",
                f"valor {_format_number(item.get('valor'))}",
                f"percentil {_format_number(item.get('percentil_num'))}",
                item.get("classificacao"),
            )
        )
    derived = payload.get("derived_scores") or {}
    if derived:
        rows.append(
            _format_result_line(
                "Indices derivados",
                f"inibicao {_format_number(derived.get('inibicao'))}",
                f"flexibilidade {_format_number(derived.get('flexibilidade'))}",
                f"erros totais {_format_number(derived.get('total_erros'))}",
            )
        )
    return rows


def _build_ravlt_rows(payload: dict) -> list[str]:
    rows = []
    for key in ("a1", "a2", "a3", "a4", "a5", "b", "a6", "a7"):
        if key in payload:
            rows.append(
                _format_result_line(key.upper(), _format_number(payload.get(key)))
            )
    for key in ("alt", "ret", "ip", "ir", "r"):
        if key in payload:
            rows.append(
                _format_result_line(key.upper(), _format_number(payload.get(key)))
            )
    if not rows:
        rows.extend(_extract_generic_rows(payload))
    return rows


def _build_scale_rows(payload: dict) -> list[str]:
    if payload.get("results") and isinstance(payload["results"], dict):
        rows = []
        for _, item in payload["results"].items():
            rows.append(
                _format_result_line(
                    item.get("name") or "Fator",
                    f"escore {_format_number(item.get('raw_score'))}",
                    f"percentil {_format_number(item.get('percentile_text') or item.get('percentil'))}",
                    item.get("classification") or item.get("classificacao"),
                )
            )
        return rows

    if payload.get("result") and isinstance(payload["result"], dict):
        base = payload.get("result") or {}
        return [
            _format_result_line(
                "Resultado principal",
                f"escore {_format_number(base.get('escore_total') or base.get('pontuacao_total'))}",
                f"percentil {_format_number(base.get('percentil') or (base.get('normas') or {}).get('percentil'))}",
                base.get("classificacao"),
            )
        ]

    return _extract_generic_rows(payload)


def build_result_rows(instrument_code: str, payload: dict) -> list[str]:
    if not payload:
        return []
    if instrument_code == "wisc4":
        return _build_wisc4_rows(payload)
    if instrument_code == "bpa2":
        return _build_bpa2_rows(payload)
    if instrument_code == "fdt":
        return _build_fdt_rows(payload)
    if instrument_code == "ravlt":
        return _build_ravlt_rows(payload)
    if instrument_code in {
        "etdah_ad",
        "etdah_pais",
        "ebadep_a",
        "ebaped_ij",
        "epq_j",
        "scared",
        "srs2",
    }:
        return _build_scale_rows(payload)
    return _extract_generic_rows(payload)


def build_validated_tests_snapshot(evaluation) -> list[dict]:
    tests = get_validated_test_applications_by_evaluation(evaluation.id)
    snapshots: list[dict] = []

    for item in tests:
        warnings = []
        structured_results = item.classified_payload or item.computed_payload or {}
        clinical_interpretation = (item.interpretation_text or "").strip()

        module = get_test_module(item.instrument.code)
        if module:
            try:
                context = TestContext(
                    patient_name=item.evaluation.patient.full_name,
                    evaluation_id=item.evaluation_id,
                    instrument_code=item.instrument.code,
                    raw_scores=item.raw_payload or {},
                )
                merged_data = {
                    **(item.computed_payload or {}),
                    **(item.classified_payload or {}),
                }
                recalculated = (module.interpret(context, merged_data) or "").strip()
                if recalculated:
                    clinical_interpretation = recalculated
            except Exception:
                warnings.append(
                    "Nao foi possivel recalcular a interpretacao tecnica atual; usando texto persistido."
                )

        summary = (
            clinical_interpretation.split(". ")[0].strip()
            if clinical_interpretation
            else ""
        )
        if not clinical_interpretation:
            warnings.append(
                "Interpretacao clinica ausente; usando apenas payload estruturado."
            )

        result_rows = build_result_rows(item.instrument.code, structured_results)

        snapshots.append(
            {
                "id": item.id,
                "instrument": item.instrument.name,
                "instrument_code": item.instrument.code,
                "instrument_name": item.instrument.name,
                "domain": item.instrument.category or "geral",
                "report_section": SECTION_MAP.get(
                    item.instrument.code, "escalas_complementares"
                ),
                "applied_on": item.applied_on.isoformat() if item.applied_on else None,
                "is_validated": item.is_validated,
                "summary": summary,
                "structured_results": structured_results,
                "classified_payload": item.classified_payload or {},
                "computed_payload": item.computed_payload or {},
                "clinical_interpretation": clinical_interpretation,
                "interpretation_text": clinical_interpretation,
                "result_rows": result_rows,
                "warnings": warnings,
            }
        )

    return snapshots
