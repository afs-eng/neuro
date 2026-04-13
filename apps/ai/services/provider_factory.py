from django.conf import settings

from apps.ai.providers import OllamaProvider


class ProviderFactory:
    @staticmethod
    def create(provider_name: str | None = None):
        provider = (provider_name or settings.AI_PROVIDER or "ollama").lower()
        if provider == "ollama":
            return OllamaProvider(
                base_url=settings.OLLAMA_BASE_URL,
                model=settings.OLLAMA_MODEL,
            )
        if provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY nao configurada.")
            from apps.ai.providers.openai_provider import OpenAIProvider

            return OpenAIProvider(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL_TEXT,
            )
        raise ValueError(f"Provider de IA nao suportado: {provider}")
