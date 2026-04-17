from apps.ai.guards.data_presence_guard import DataPresenceGuard

from .section_registry import get_ai_section_config, get_section_validation


class SectionValidationService:
    @classmethod
    def validate_raw_context(cls, section_key: str, context: dict) -> list[str]:
        validation = get_section_validation(section_key)
        if not validation:
            return DataPresenceGuard.validate_section_context(section_key, context)

        tests = context.get("validated_tests") or []
        required_any_codes = validation.get("required_any_codes") or set()
        if required_any_codes and not any(
            item.get("instrument_code") in required_any_codes for item in tests
        ):
            return [validation["message"]]
        return []

    @classmethod
    def validate_filtered_context(
        cls, section_key: str, filtered_context: dict
    ) -> list[str]:
        config = get_ai_section_config(section_key)
        validation = get_section_validation(section_key)
        tests = filtered_context.get("validated_tests") or []
        if config.get("kind") in {"test", "section"} and not tests:
            message = (
                validation.get("message")
                or "Nao ha dados suficientes para gerar esta secao com IA."
            )
            return [message]

        for test in tests:
            has_content = bool(
                (test.get("clinical_interpretation") or "").strip()
                or test.get("technical_basis")
                or test.get("structured_results")
                or test.get("result_rows")
                or (test.get("summary") or "").strip()
            )
            if not has_content:
                instrument_name = (
                    test.get("instrument_name")
                    or test.get("instrument_code")
                    or "instrumento"
                )
                return [
                    f"Os dados filtrados de {instrument_name} sao insuficientes para gerar esta secao com IA."
                ]
        return []
