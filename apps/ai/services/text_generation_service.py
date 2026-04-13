import logging
from pathlib import Path

from django.conf import settings

from .provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


class TextGenerationService:
    PROMPTS_DIR = Path(settings.BASE_DIR) / "apps" / "ai" / "prompts"

    @classmethod
    def _read_prompt(cls, relative_path: str) -> str:
        prompt_path = cls.PROMPTS_DIR / relative_path
        try:
            return prompt_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise ValueError(f"Prompt nao encontrado: {relative_path}") from exc

    @classmethod
    def generate_from_prompt(cls, prompt_name: str, user_prompt: str, **kwargs) -> dict:
        provider_name = kwargs.get("provider") or settings.AI_PROVIDER
        provider = ProviderFactory.create(provider_name)
        system_prompt = cls._read_prompt("base_system_prompt.txt")
        section_prompt = cls._read_prompt(prompt_name)
        full_user_prompt = f"{section_prompt}\n\n{user_prompt}".strip()
        try:
            result = provider.generate(
                system_prompt=system_prompt,
                user_prompt=full_user_prompt,
                **kwargs,
            )
        except ValueError:
            raise
        except Exception as exc:
            logger.exception("AI generation failed")
            raise ValueError(f"Falha ao gerar texto com IA: {exc}") from exc
        logger.info(
            "AI generation completed",
            extra={
                "provider": result.get("provider"),
                "model": result.get("model"),
                "prompt_name": prompt_name,
            },
        )
        return result
