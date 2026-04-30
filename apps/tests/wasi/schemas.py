from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class WASIRawInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    vc: int = Field(ge=0)
    sm: int = Field(ge=0)
    cb: int = Field(ge=0)
    rm: int = Field(ge=0)
    birth_date: date
    applied_on: date
    confidence_level: str = Field(default="95")
