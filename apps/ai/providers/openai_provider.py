from openai import OpenAI

from .base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", self.model),
            temperature=kwargs.get("temperature", 0.2),
            max_tokens=kwargs.get("max_tokens", 2048),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        choice = response.choices[0]
        usage = response.usage
        return {
            "content": (choice.message.content or "").strip(),
            "provider": "openai",
            "model": response.model or self.model,
            "finish_reason": choice.finish_reason or "unknown",
            "usage": {
                "prompt_tokens": getattr(usage, "prompt_tokens", None),
                "completion_tokens": getattr(usage, "completion_tokens", None),
                "total_tokens": getattr(usage, "total_tokens", None),
            },
            "warnings": [],
        }
