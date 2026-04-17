import json

from apps.ai.services.text_generation_service import TextGenerationService

from .section_context_service import SectionContextService
from .section_registry import get_ai_section_config, list_section_configs
from .section_validation_service import SectionValidationService


class ReportAIService:
    SUPPORTED_SECTIONS = {
        key for key, config in list_section_configs() if config.get("supports_ai")
    }

    @classmethod
    def supports_section(cls, section_key: str) -> bool:
        return section_key in cls.SUPPORTED_SECTIONS

    @classmethod
    def generate_section(cls, report, section_key: str, context: dict) -> dict:
        if not cls.supports_section(section_key):
            raise ValueError(f"Secao nao suportada por IA nesta fase: {section_key}")

        return cls._generate_with_prompt(report, section_key, context)

    @classmethod
    def _generate_with_prompt(cls, report, section_key: str, context: dict) -> dict:
        warnings = SectionValidationService.validate_raw_context(section_key, context)
        if warnings:
            raise ValueError(warnings[0])

        filtered_context = SectionContextService.build_for_section(
            report, section_key, context
        )
        warnings = SectionValidationService.validate_filtered_context(
            section_key, filtered_context
        )
        if warnings:
            raise ValueError(warnings[0])
        config = cls._generator_config(section_key)
        result = TextGenerationService.generate_from_prompt(
            prompt_name=cls._prompt_name(section_key),
            user_prompt=cls._build_user_prompt(filtered_context),
            timeout=config["timeout"],
        )

        content = (result.get("content") or "").strip()
        if not content:
            raise ValueError(
                "A IA retornou uma resposta vazia para a secao solicitada."
            )

        return {
            "content": content,
            "warnings": result.get("warnings") or [],
            "metadata": {
                "provider": result.get("provider"),
                "model": result.get("model"),
                "requested_model": result.get("requested_model") or config.get("model"),
                "used_model_fallback": bool(result.get("used_model_fallback")),
                "fallback_model": result.get("fallback_model"),
                "attempted_models": result.get("attempted_models") or [],
                "finish_reason": result.get("finish_reason"),
                "usage": result.get("usage") or {},
                "section": section_key,
                "prompt_name": config["prompt_name"],
                "generation_path": "ai",
            },
        }

    @classmethod
    def _prompt_name(cls, section_key: str) -> str:
        config = cls._generator_config(section_key)
        return config["prompt_name"]

    @classmethod
    def _build_user_prompt(cls, filtered_context: dict) -> str:
        return (
            "Baseie a redacao prioritariamente nas interpretacoes tecnicas ja geradas "
            "pelos interpreters.py do sistema e persistidas em 'clinical_interpretation' ou 'technical_basis'. "
            "Use os resultados estruturados apenas para sustentar e organizar essa redacao, "
            "sem recalcular classificacoes.\n\n"
            "Dados clinicos estruturados para a secao solicitada:\n"
            f"{json.dumps(filtered_context, ensure_ascii=False, indent=2)}"
        )

    @classmethod
    def _generator_config(cls, section_key: str) -> dict:
        return get_ai_section_config(section_key)
