from pydantic import BaseModel, Field


class SubtestInput(BaseModel):
    brutos: int = Field(ge=0, description="Pontos brutos")
    erros: int = Field(ge=0, description="Erros")
    omissoes: int = Field(ge=0, description="Omissões")


class BPA2RawInput(BaseModel):
    ac: SubtestInput
    ad: SubtestInput
    aa: SubtestInput


class SubtestResult(BaseModel):
    subteste: str
    codigo: str
    brutos: int
    erros: int
    omissoes: int
    total: int
    classificacao: str
    percentil: int


class BPA2Result(BaseModel):
    subtestes: list[SubtestResult]
    pontos_fortes: list[str]
    pontos_fragilizados: list[str]
