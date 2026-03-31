from pydantic import BaseModel, Field


class EPQJRawInput(BaseModel):
    item_01: int = Field(ge=0, le=1)
    item_02: int = Field(ge=0, le=1)
    item_03: int = Field(ge=0, le=1)
    item_04: int = Field(ge=0, le=1)
    item_05: int = Field(ge=0, le=1)
    item_06: int = Field(ge=0, le=1)
    item_07: int = Field(ge=0, le=1)
    item_08: int = Field(ge=0, le=1)
    item_09: int = Field(ge=0, le=1)
    item_10: int = Field(ge=0, le=1)
    item_11: int = Field(ge=0, le=1)
    item_12: int = Field(ge=0, le=1)
    item_13: int = Field(ge=0, le=1)
    item_14: int = Field(ge=0, le=1)
    item_15: int = Field(ge=0, le=1)
    item_16: int = Field(ge=0, le=1)
    item_17: int = Field(ge=0, le=1)
    item_18: int = Field(ge=0, le=1)
    item_19: int = Field(ge=0, le=1)
    item_20: int = Field(ge=0, le=1)
    item_21: int = Field(ge=0, le=1)
    item_22: int = Field(ge=0, le=1)
    item_23: int = Field(ge=0, le=1)
    item_24: int = Field(ge=0, le=1)
    item_25: int = Field(ge=0, le=1)
    item_26: int = Field(ge=0, le=1)
    item_27: int = Field(ge=0, le=1)
    item_28: int = Field(ge=0, le=1)
    item_29: int = Field(ge=0, le=1)
    item_30: int = Field(ge=0, le=1)
    item_31: int = Field(ge=0, le=1)
    item_32: int = Field(ge=0, le=1)
    item_33: int = Field(ge=0, le=1)
    item_34: int = Field(ge=0, le=1)
    item_35: int = Field(ge=0, le=1)
    item_36: int = Field(ge=0, le=1)
    item_37: int = Field(ge=0, le=1)
    item_38: int = Field(ge=0, le=1)
    item_39: int = Field(ge=0, le=1)
    item_40: int = Field(ge=0, le=1)
    item_41: int = Field(ge=0, le=1)
    item_42: int = Field(ge=0, le=1)
    item_43: int = Field(ge=0, le=1)
    item_44: int = Field(ge=0, le=1)
    item_45: int = Field(ge=0, le=1)
    item_46: int = Field(ge=0, le=1)
    item_47: int = Field(ge=0, le=1)
    item_48: int = Field(ge=0, le=1)
    item_49: int = Field(ge=0, le=1)
    item_50: int = Field(ge=0, le=1)
    item_51: int = Field(ge=0, le=1)
    item_52: int = Field(ge=0, le=1)
    item_53: int = Field(ge=0, le=1)
    item_54: int = Field(ge=0, le=1)
    item_55: int = Field(ge=0, le=1)
    item_56: int = Field(ge=0, le=1)
    item_57: int = Field(ge=0, le=1)
    item_58: int = Field(ge=0, le=1)
    item_59: int = Field(ge=0, le=1)
    item_60: int = Field(ge=0, le=1)
    sexo: str = Field(pattern="^[MF]$")


class EPQJFactorResult(BaseModel):
    escore: int
    percentil: int | str
    classificacao: str


class EPQJResult(BaseModel):
    fatores: dict[str, EPQJFactorResult]
    sexo: str
