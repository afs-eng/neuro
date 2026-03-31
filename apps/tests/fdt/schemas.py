from pydantic import BaseModel, Field


class FDTStageInput(BaseModel):
    tempo: float = Field(ge=0)
    erros: int = Field(ge=0, default=0)


class FDTRawInput(BaseModel):
    leitura: FDTStageInput
    contagem: FDTStageInput
    escolha: FDTStageInput
    alternancia: FDTStageInput


class FDTMetricResult(BaseModel):
    codigo: str
    nome: str
    categoria: str
    valor: float
    media: float
    dp: float
    z_score: float
    pontos_ponderados: float
    percentil_num: float
    percentil_texto: str
    classificacao: str
