from .base import BaseAIProvider


class AnthropicProvider(BaseAIProvider):
    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, **kwargs) -> dict:
        try:
            from anthropic import Anthropic
        except ImportError as exc:
            raise ValueError(
                "Dependencia opcional anthropic nao esta instalada."
            ) from exc

        client = Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=kwargs.get("model", self.model),
            max_tokens=kwargs.get("max_tokens", 2048),
            temperature=kwargs.get("temperature", 0.2),
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        content = "".join(
            block.text for block in response.content if getattr(block, "text", None)
        )
        return {
            "content": content.strip(),
            "provider": "anthropic",
            "model": response.model or self.model,
            "finish_reason": getattr(response, "stop_reason", None) or "unknown",
            "usage": {
                "input_tokens": getattr(response.usage, "input_tokens", None),
                "output_tokens": getattr(response.usage, "output_tokens", None),
            },
            "warnings": [],
        }
