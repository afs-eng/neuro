from pydantic import BaseModel, Field


class EBADEPIJRawInput(BaseModel):
    item_01: int = Field(ge=0, le=2)
    item_02: int = Field(ge=0, le=2)
    item_03: int = Field(ge=0, le=2)
    item_04: int = Field(ge=0, le=2)
    item_05: int = Field(ge=0, le=2)
    item_06: int = Field(ge=0, le=2)
    item_07: int = Field(ge=0, le=2)
    item_08: int = Field(ge=0, le=2)
    item_09: int = Field(ge=0, le=2)
    item_10: int = Field(ge=0, le=2)
    item_11: int = Field(ge=0, le=2)
    item_12: int = Field(ge=0, le=2)
    item_13: int = Field(ge=0, le=2)
    item_14: int = Field(ge=0, le=2)
    item_15: int = Field(ge=0, le=2)
    item_16: int = Field(ge=0, le=2)
    item_17: int = Field(ge=0, le=2)
    item_18: int = Field(ge=0, le=2)
    item_19: int = Field(ge=0, le=2)
    item_20: int = Field(ge=0, le=2)
    item_21: int = Field(ge=0, le=2)
    item_22: int = Field(ge=0, le=2)
    item_23: int = Field(ge=0, le=2)
    item_24: int = Field(ge=0, le=2)
    item_25: int = Field(ge=0, le=2)
    item_26: int = Field(ge=0, le=2)
    item_27: int = Field(ge=0, le=2)


class ItemDetail(BaseModel):
    item: int
    resposta: int
    invertido: bool
    corrigido: int


class EBADEPIJNorms(BaseModel):
    percentil: str | int
    T: int
    estanino: int


class EBADEPIJResult(BaseModel):
    soma_itens_negativos: int
    soma_itens_positivos: int
    pontuacao_total: int
    classificacao: str
    normas: EBADEPIJNorms | None = None
    detalhe_itens: list[ItemDetail] = []
