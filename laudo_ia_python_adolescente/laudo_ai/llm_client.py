from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str = "mock-model"


class BaseLLMClient:
    def generate(self, prompt: str) -> LLMResponse:
        raise NotImplementedError


class MockLLMClient(BaseLLMClient):
    """
    Cliente fake para desenvolvimento local. Troque depois por OpenAI, Azure, Anthropic etc.
    """

    def generate(self, prompt: str) -> LLMResponse:
        return LLMResponse(
            text="Texto gerado em modo mock. Substitua este cliente por uma integração real com LLM.",
            model="mock-model",
        )
