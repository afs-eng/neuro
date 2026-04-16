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
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip("/")
        self.referer = referer
        self.title = title

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        payload = {
            "model": kwargs.get("model", self.model),
            "temperature": kwargs.get("temperature", 0.2),
            "max_tokens": kwargs.get("max_tokens", 2048),
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.referer:
            headers["HTTP-Referer"] = self.referer
        if self.title:
            headers["X-OpenRouter-Title"] = self.title

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", 180),
        )
        if not response.ok:
            try:
                error_payload = response.json()
                message = error_payload.get("error", {}).get(
                    "message"
                ) or error_payload.get("message")
            except Exception:
                message = response.text
            raise ValueError(
                message or f"OpenAI/OpenRouter retornou HTTP {response.status_code}"
            )

        data = response.json()
        choice = (data.get("choices") or [{}])[0]
        message = choice.get("message") or {}
        usage = data.get("usage") or {}
        return {
            "content": str(message.get("content") or "").strip(),
            "provider": "openai",
            "model": data.get("model") or self.model,
            "finish_reason": choice.get("finish_reason") or "unknown",
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "total_tokens": usage.get("total_tokens"),
            },
            "warnings": [],
        }
