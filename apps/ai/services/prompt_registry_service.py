from pathlib import Path

from django.conf import settings


class PromptRegistryService:
    PROMPTS_DIR = Path(settings.BASE_DIR) / "apps" / "ai" / "prompts"

    @classmethod
    def resolve(cls, relative_path: str) -> Path:
        prompt_path = cls.PROMPTS_DIR / relative_path
        if not prompt_path.exists():
            raise ValueError(f"Prompt nao encontrado: {relative_path}")
        return prompt_path

    @classmethod
    def read(cls, relative_path: str) -> str:
        return cls.resolve(relative_path).read_text(encoding="utf-8").strip()
