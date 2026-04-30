from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class BFPRawInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    sample: str = Field(default="geral")
    responses: dict[str, int] = Field(default_factory=dict)


class BFPScaleResult(BaseModel):
    code: str
    name: str
    raw_score: float
    mean: float
    sd: float
    z_score: float
    weighted_score: float
    percentile: float
    classification: str


class BFPResult(BaseModel):
    sample: str
    factors: dict[str, BFPScaleResult]
    facets: dict[str, BFPScaleResult]
