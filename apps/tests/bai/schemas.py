from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


# Pydantic schemas para API
class BAIRawInput(BaseModel):
    item_01: int = Field(ge=0, le=3)
    item_02: int = Field(ge=0, le=3)
    item_03: int = Field(ge=0, le=3)
    item_04: int = Field(ge=0, le=3)
    item_05: int = Field(ge=0, le=3)
    item_06: int = Field(ge=0, le=3)
    item_07: int = Field(ge=0, le=3)
    item_08: int = Field(ge=0, le=3)
    item_09: int = Field(ge=0, le=3)
    item_10: int = Field(ge=0, le=3)
    item_11: int = Field(ge=0, le=3)
    item_12: int = Field(ge=0, le=3)
    item_13: int = Field(ge=0, le=3)
    item_14: int = Field(ge=0, le=3)
    item_15: int = Field(ge=0, le=3)
    item_16: int = Field(ge=0, le=3)
    item_17: int = Field(ge=0, le=3)
    item_18: int = Field(ge=0, le=3)
    item_19: int = Field(ge=0, le=3)
    item_20: int = Field(ge=0, le=3)
    item_21: int = Field(ge=0, le=3)


class BAIFactorResult(BaseModel):
    escore: int
    classificacao: str


class BAIResult(BaseModel):
    escore_total: int
    classificacao: dict
    t_score: Optional[float] = None
    percentile: Optional[float] = None
    fatores: dict[str, BAIFactorResult] = {}


# Dataclasses para uso interno do módulo
@dataclass(slots=True)
class BAIItemResponse:
    item_number: int
    score: int


@dataclass(slots=True)
class BAIRawPayload:
    respondent_name: Optional[str] = None
    application_mode: str = "paper"
    responses: List[BAIItemResponse] = field(default_factory=list)


@dataclass(slots=True)
class BAIComputedPayload:
    total_raw_score: int
    t_score: Optional[float]
    percentile: Optional[float]
    confidence_interval: Optional[List[float]]
    missing_count: int
    faixa_normativa: str
    interpretacao_faixa: str
    response_distribution: Dict[int, int]
    tables: Dict[str, list]
    chart_payload: Dict[str, object]
