from pydantic import BaseModel, ConfigDict, Field


class WAIS3AgeInput(BaseModel):
    anos: int = Field(ge=0)
    meses: int = Field(default=0, ge=0, le=11)


class WAIS3SubtestInput(BaseModel):
    pontos_brutos: int = Field(ge=0)


class WAIS3RawInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    idade: WAIS3AgeInput
    subtestes: dict[str, WAIS3SubtestInput]
