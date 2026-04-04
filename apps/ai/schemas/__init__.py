from ninja import Schema
from typing import Optional, Literal
from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    input_data: dict = Field(..., description="Dados estruturados recebidos do backend")
    context: Optional[dict] = Field(
        default=None, description="Contexto adicional para a IA"
    )
    task_type: Literal[
        "summarize", "suggest", "draft", "translate", "explain", "review"
    ] = Field(..., description="Tipo de tarefa")


class AIResponse(BaseModel):
    output: str = Field(..., description="Resposta gerada pela IA")
    confidence: Optional[float] = Field(
        default=None, description="Confiança da resposta (0-1)"
    )
    metadata: Optional[dict] = Field(default=None, description="Metadados adicionais")
    warnings: Optional[list[str]] = Field(
        default=None, description="Avisos sobre a resposta"
    )


class AIProviderConfig(BaseModel):
    provider: str = Field(
        default="openai", description="Provider: openai, anthropic, local"
    )
    model: str = Field(default="gpt-4", description="Modelo a ser usado")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2048, ge=1)
