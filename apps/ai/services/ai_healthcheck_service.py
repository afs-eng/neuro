from __future__ import annotations

from django.conf import settings

from .provider_factory import ProviderFactory


class AIHealthcheckService:
    HEALTHCHECK_SYSTEM_PROMPT = (
        "Voce esta executando uma verificacao tecnica de disponibilidade. "
        "Responda apenas com OK."
    )
    HEALTHCHECK_USER_PROMPT = "Responda apenas OK."

    @classmethod
    def check(cls, provider: str | None = None, timeout: int = 20) -> dict:
        provider_name = provider or settings.AI_PROVIDER
        client = ProviderFactory.create(provider_name)
        result = client.generate(
            system_prompt=cls.HEALTHCHECK_SYSTEM_PROMPT,
            user_prompt=cls.HEALTHCHECK_USER_PROMPT,
            temperature=0,
            timeout=timeout,
            max_tokens=8,
        )
        return {
            "ok": True,
            "provider": result.get("provider") or provider_name,
            "model": result.get("model") or getattr(client, "model", None),
            "finish_reason": result.get("finish_reason") or "unknown",
        }

    @classmethod
    def ensure_available(cls, provider: str | None = None, timeout: int = 20) -> dict:
        try:
            return cls.check(provider=provider, timeout=timeout)
        except Exception as exc:
            provider_name = provider or settings.AI_PROVIDER
            raise ValueError(
                "A IA configurada nao esta disponivel no momento "
                f"(provider: {provider_name}). Detalhes: {exc}"
            ) from exc
