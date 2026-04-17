from __future__ import annotations

import requests

from .base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str | None = None,
        referer: str | None = None,
        title: str | None = None,
        fallback_models: list[str] | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self.referer = referer
        self.title = title
        self.fallback_models = [item for item in (fallback_models or []) if item]

    @staticmethod
    def _extract_error(response: requests.Response) -> tuple[int, str]:
        try:
            error_payload = response.json()
            message = error_payload.get("error", {}).get(
                "message"
            ) or error_payload.get("message")
        except Exception:
            message = response.text
        return response.status_code, str(message or "").strip()

    @staticmethod
    def _should_try_fallback(status_code: int, message: str) -> bool:
        normalized = message.lower()
        return status_code in {429, 502, 503, 504} or any(
            token in normalized
            for token in {
                "provider returned error",
                "no providers",
                "temporarily unavailable",
                "rate limit",
                "capacity",
            }
        )

    def _model_candidates(self, requested_model: str | None) -> list[str]:
        candidates = [requested_model or self.model, *self.fallback_models]
        unique: list[str] = []
        for candidate in candidates:
            if candidate and candidate not in unique:
                unique.append(candidate)
        return unique

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.title:
            headers["X-OpenRouter-Title"] = self.title
        warnings: list[str] = []
        last_error: tuple[int, str] | None = None

        for index, candidate_model in enumerate(
            self._model_candidates(kwargs.get("model"))
        ):
            payload = {
                "model": candidate_model,
                "temperature": kwargs.get("temperature", 0.2),
                "max_tokens": kwargs.get("max_tokens", 2048),
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
            }
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=kwargs.get("timeout", 180),
            )
            if response.ok:
                data = response.json()
                choice = (data.get("choices") or [{}])[0]
                message = choice.get("message") or {}
                usage = data.get("usage") or {}
                if index > 0:
                    warnings.append(
                        f"Modelo principal indisponivel; resposta gerada com fallback '{candidate_model}'."
                    )
                return {
                    "content": str(message.get("content") or "").strip(),
                    "provider": "openai",
                    "model": data.get("model") or candidate_model,
                    "finish_reason": choice.get("finish_reason") or "unknown",
                    "usage": {
                        "prompt_tokens": usage.get("prompt_tokens"),
                        "completion_tokens": usage.get("completion_tokens"),
                        "total_tokens": usage.get("total_tokens"),
                    },
                    "warnings": warnings,
                }

            status_code, message = self._extract_error(response)
            last_error = (status_code, message)
            if index < len(
                self._model_candidates(kwargs.get("model"))
            ) - 1 and self._should_try_fallback(status_code, message):
                warnings.append(
                    f"Falha no modelo '{candidate_model}' (HTTP {status_code}); tentando fallback."
                )
                continue
            raise ValueError(
                message or f"OpenAI/OpenRouter retornou HTTP {status_code}"
            )

        status_code, message = last_error or (
            0,
            "Falha desconhecida no provider OpenAI/OpenRouter.",
        )
        raise ValueError(message or f"OpenAI/OpenRouter retornou HTTP {status_code}")
