from django.conf import settings

from apps.ai.providers import AnthropicProvider, OllamaProvider
from apps.ai.schemas import ProviderConfig


class ProviderFactory:
    @staticmethod
    def create(provider_name: str | None = None):
        provider = (provider_name or settings.AI_PROVIDER or "ollama").lower()
        config = ProviderConfig(
            provider=provider,
            model=getattr(settings, "OLLAMA_MODEL", "qwen2.5:14b"),
            base_url=getattr(settings, "OLLAMA_BASE_URL", None),
        )
        if provider == "ollama":
            return OllamaProvider(
                base_url=config.base_url or "http://localhost:11434", model=config.model
            )
        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY nao configurada.")
            from apps.ai.providers.openai_provider import OpenAIProvider

            return OpenAIProvider(
                api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL_TEXT
            )
        if provider == "anthropic":
            if not getattr(settings, "ANTHROPIC_API_KEY", ""):
                raise ValueError("ANTHROPIC_API_KEY nao configurada.")
            return AnthropicProvider(
                api_key=settings.ANTHROPIC_API_KEY, model=settings.ANTHROPIC_MODEL_TEXT
            )
        raise ValueError(f"Provider de IA nao suportado: {provider}")
