from pydantic import BaseModel, Field


class EBADEPARawInput(BaseModel):
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
    item_22: int = Field(ge=0, le=3)
    item_23: int = Field(ge=0, le=3)
    item_24: int = Field(ge=0, le=3)
    item_25: int = Field(ge=0, le=3)
    item_26: int = Field(ge=0, le=3)
    item_27: int = Field(ge=0, le=3)
    item_28: int = Field(ge=0, le=3)
    item_29: int = Field(ge=0, le=3)
    item_30: int = Field(ge=0, le=3)
    item_31: int = Field(ge=0, le=3)
    item_32: int = Field(ge=0, le=3)
    item_33: int = Field(ge=0, le=3)
    item_34: int = Field(ge=0, le=3)
    item_35: int = Field(ge=0, le=3)
    item_36: int = Field(ge=0, le=3)
    item_37: int = Field(ge=0, le=3)
    item_38: int = Field(ge=0, le=3)
    item_39: int = Field(ge=0, le=3)
    item_40: int = Field(ge=0, le=3)
    item_41: int = Field(ge=0, le=3)
    item_42: int = Field(ge=0, le=3)
    item_43: int = Field(ge=0, le=3)
    item_44: int = Field(ge=0, le=3)
    item_45: int = Field(ge=0, le=3)


class ItemDetail(BaseModel):
    item: int
    resposta: int


class EBADEPANorms(BaseModel):
    percentil: int


class EBADEPAResult(BaseModel):
    escore_total: int
    classificacao: str
    percentil: int
    detalhe_itens: list[ItemDetail] = []
