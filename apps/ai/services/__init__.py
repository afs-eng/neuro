import os
from typing import Optional
from functools import lru_cache


class AIProvider:
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        self.provider = provider
        self.model = model
        self._client = None

    def _get_client(self):
        if self._client is None:
            if self.provider == "openai":
                from openai import OpenAI

                self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            elif self.provider == "anthropic":
                from anthropic import Anthropic

                self._client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        return self._client

    def generate(self, prompt: str, **kwargs) -> str:
        client = self._get_client()
        if self.provider == "openai":
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs,
            )
            return response.choices[0].message.content
        elif self.provider == "anthropic":
            response = client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 2048),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        raise ValueError(f"Provider {self.provider} não suportado")


class AIService:
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.provider = AIProvider(
            provider=self.config.get("provider", "openai"),
            model=self.config.get("model", "gpt-4"),
        )

    def generate(self, prompt: str, **kwargs) -> str:
        return self.provider.generate(prompt, **kwargs)

    def summarize(self, data: dict, context: Optional[dict] = None) -> str:
        prompt = self._build_summarize_prompt(data, context)
        return self.generate(prompt)

    def suggest(self, data: dict, context: Optional[dict] = None) -> str:
        prompt = self._build_suggest_prompt(data, context)
        return self.generate(prompt)

    def draft(self, data: dict, context: Optional[dict] = None) -> str:
        prompt = self._build_draft_prompt(data, context)
        return self.generate(prompt)

    def _build_summarize_prompt(self, data: dict, context: Optional[dict]) -> str:
        return f"""Resuma de forma clara e profissional as seguintes informações:
{data}

Contexto adicional: {context or "N/A"}"""

    def _build_suggest_prompt(self, data: dict, context: Optional[dict]) -> str:
        return f"""Com base nos dados fornecidos, sugira recomendações clínicas:
{data}

Contexto: {context or "N/A"}

Importante: Esta é apenas uma sugestão assistiva. A decisão final deve ser sempre do profissional."""

    def _build_draft_prompt(self, data: dict, context: Optional[dict]) -> str:
        return f"""Elabore um rascunho profissional baseado nos dados:
{data}

Contexto: {context or "N/A"}

Este é apenas um rascunho inicial que deve ser revisado por um profissional."""


@lru_cache()
def get_ai_service() -> AIService:
    from django.conf import settings

    ai_config = getattr(settings, "AI_CONFIG", {})
    return AIService(config=ai_config)
