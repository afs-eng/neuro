from __future__ import annotations

from .section_registry import (
    get_section_dependencies,
    list_section_configs,
)


class SectionWorkflowService:
    @classmethod
    def get_generation_order(cls, context: dict) -> list[str]:
        available = {
            item.get("instrument_code") for item in (context.get("validated_tests") or [])
        }
        is_adolescent = cls._is_adolescent_case(context)
        eligible = []

        for section_key, config in list_section_configs():
            required_any_codes = set(config.get("required_any_codes") or ())
            enabled = True
            if required_any_codes:
                enabled = bool(available & required_any_codes)
            if not enabled and config.get("enable_when_adolescent"):
                enabled = is_adolescent
            if enabled:
                eligible.append(section_key)

        return eligible

    @classmethod
    def get_dependencies(cls, section_key: str) -> list[str]:
        return get_section_dependencies(section_key)

    @classmethod
    def can_generate(cls, section_key: str, generated: set[str]) -> bool:
        return all(dep in generated for dep in cls.get_dependencies(section_key))

    @classmethod
    def get_dependents(cls, section_key: str) -> list[str]:
        dependents = []
        for key, config in list_section_configs():
            if section_key in (config.get("depends_on") or []):
                dependents.append(key)
        return dependents

    @staticmethod
    def _is_adolescent_case(context: dict) -> bool:
        tests = context.get("validated_tests") or []
        return any(item.get("instrument_code") == "etdah_pais" for item in tests)
