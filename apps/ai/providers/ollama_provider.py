import requests

from .base import BaseAIProvider


class OllamaProvider(BaseAIProvider):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        timeout = kwargs.get("timeout", 180)
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": kwargs.get("model", self.model),
                "system": system_prompt,
                "prompt": user_prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.2),
                },
            },
            timeout=timeout,
        )
        response.raise_for_status()
        data = response.json()
        return {
            "content": (data.get("response") or "").strip(),
            "provider": "ollama",
            "model": data.get("model") or self.model,
            "finish_reason": "stop" if data.get("done") else "unknown",
            "usage": {
                "prompt_eval_count": data.get("prompt_eval_count"),
                "eval_count": data.get("eval_count"),
            },
            "warnings": [],
        }
