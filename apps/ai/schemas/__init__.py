from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, Field


@dataclass(slots=True)
class GenerationRequest:
    prompt_name: str
    user_prompt: str
    provider: str | None = None
    model: str | None = None
    temperature: float = 0.2
    timeout: int = 180
    max_tokens: int = 2048
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GenerationResponse:
    content: str
    provider: str
    model: str
    finish_reason: str
    usage: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "provider": self.provider,
            "model": self.model,
            "finish_reason": self.finish_reason,
            "usage": self.usage,
            "warnings": self.warnings,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "GenerationResponse":
        return cls(
            content=str(payload.get("content") or ""),
            provider=str(payload.get("provider") or "unknown"),
            model=str(payload.get("model") or "unknown"),
            finish_reason=str(payload.get("finish_reason") or "unknown"),
            usage=dict(payload.get("usage") or {}),
            warnings=list(payload.get("warnings") or []),
        )


@dataclass(slots=True)
class ProviderConfig:
    provider: str = "ollama"
    model: str = "qwen2.5:14b"
    base_url: str | None = None
    api_key: str | None = None


class AIRequest(BaseModel):
    input_data: dict = Field(..., description="Dados estruturados recebidos do backend")
    context: dict | None = Field(
        default=None, description="Contexto adicional para a IA"
    )
    task_type: Literal[
        "summarize", "suggest", "draft", "translate", "explain", "review"
    ] = Field(..., description="Tipo de tarefa")


class AIResponse(BaseModel):
    output: str = Field(..., description="Resposta gerada pela IA")
    confidence: float | None = Field(
        default=None, description="Confiança da resposta (0-1)"
    )
    metadata: dict | None = Field(default=None, description="Metadados adicionais")
    warnings: list[str] | None = Field(
        default=None, description="Avisos sobre a resposta"
    )


class AIProviderConfig(BaseModel):
    provider: str = Field(
        default="ollama", description="Provider: ollama, openai, anthropic"
    )
    model: str = Field(default="qwen2.5:14b", description="Modelo a ser usado")
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)


__all__ = [
    "GenerationRequest",
    "GenerationResponse",
    "ProviderConfig",
    "AIRequest",
    "AIResponse",
    "AIProviderConfig",
]
