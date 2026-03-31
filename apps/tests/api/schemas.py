from datetime import date
from typing import Any, Optional

from ninja import Schema


class InstrumentOut(Schema):
    id: int
    code: str
    name: str
    category: str
    version: str
    is_active: bool
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    age_message: Optional[str] = ""


class InstrumentCreateIn(Schema):
    code: str
    name: str
    category: Optional[str] = ""
    version: Optional[str] = ""
    is_active: bool = True


class InstrumentUpdateIn(Schema):
    code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    version: Optional[str] = None
    is_active: Optional[bool] = None


class TestApplicationOut(Schema):
    id: int
    evaluation_id: int
    patient_name: str
    instrument_id: int
    instrument_code: str
    instrument_name: str
    applied_on: Optional[date] = None
    raw_payload: dict[str, Any]
    computed_payload: dict[str, Any]
    classified_payload: dict[str, Any]
    reviewed_payload: dict[str, Any]
    interpretation_text: str
    is_validated: bool


class TestApplicationCreateIn(Schema):
    evaluation_id: int
    instrument_id: int
    applied_on: Optional[date] = None
    raw_payload: dict[str, Any] = {}
    reviewed_payload: dict[str, Any] = {}
    interpretation_text: Optional[str] = ""
    is_validated: bool = False


class TestApplicationUpdateIn(Schema):
    evaluation_id: Optional[int] = None
    instrument_id: Optional[int] = None
    applied_on: Optional[date] = None
    raw_payload: Optional[dict[str, Any]] = None
    computed_payload: Optional[dict[str, Any]] = None
    classified_payload: Optional[dict[str, Any]] = None
    reviewed_payload: Optional[dict[str, Any]] = None
    interpretation_text: Optional[str] = None
    is_validated: Optional[bool] = None


class MessageOut(Schema):
    message: str


# --- EBADEP-A ---


class EBADEPASubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    item_01: int = 0
    item_02: int = 0
    item_03: int = 0
    item_04: int = 0
    item_05: int = 0
    item_06: int = 0
    item_07: int = 0
    item_08: int = 0
    item_09: int = 0
    item_10: int = 0
    item_11: int = 0
    item_12: int = 0
    item_13: int = 0
    item_14: int = 0
    item_15: int = 0
    item_16: int = 0
    item_17: int = 0
    item_18: int = 0
    item_19: int = 0
    item_20: int = 0
    item_21: int = 0
    item_22: int = 0
    item_23: int = 0
    item_24: int = 0
    item_25: int = 0
    item_26: int = 0
    item_27: int = 0
    item_28: int = 0
    item_29: int = 0
    item_30: int = 0
    item_31: int = 0
    item_32: int = 0
    item_33: int = 0
    item_34: int = 0
    item_35: int = 0
    item_36: int = 0
    item_37: int = 0
    item_38: int = 0
    item_39: int = 0
    item_40: int = 0
    item_41: int = 0
    item_42: int = 0
    item_43: int = 0
    item_44: int = 0
    item_45: int = 0


# --- EBADEP-IJ ---


class EBADEPIJSubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    item_01: int = 0
    item_02: int = 0
    item_03: int = 0
    item_04: int = 0
    item_05: int = 0
    item_06: int = 0
    item_07: int = 0
    item_08: int = 0
    item_09: int = 0
    item_10: int = 0
    item_11: int = 0
    item_12: int = 0
    item_13: int = 0
    item_14: int = 0
    item_15: int = 0
    item_16: int = 0
    item_17: int = 0
    item_18: int = 0
    item_19: int = 0
    item_20: int = 0
    item_21: int = 0
    item_22: int = 0
    item_23: int = 0
    item_24: int = 0
    item_25: int = 0
    item_26: int = 0
    item_27: int = 0


# --- FDT ---


class FDTStageIn(Schema):
    tempo: float = 0
    erros: int = 0


class FDTSubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    leitura: FDTStageIn
    contagem: FDTStageIn
    escolha: FDTStageIn
    alternancia: FDTStageIn


# --- BPA-2 ---


class BPA2SubtestIn(Schema):
    brutos: int = 0
    erros: int = 0
    omissoes: int = 0


class BPA2SubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    norm_type: Optional[str] = "idade"
    ac: BPA2SubtestIn
    ad: BPA2SubtestIn
    aa: BPA2SubtestIn


# --- WISC-IV ---


class WISC4SubmitIn(Schema):
    evaluation_id: int
    cb: Optional[str] = ""
    sm: Optional[str] = ""
    dg: Optional[str] = ""
    cn: Optional[str] = ""
    cd: Optional[str] = ""
    vc: Optional[str] = ""
    snl: Optional[str] = ""
    rm: Optional[str] = ""
    co: Optional[str] = ""
    ps: Optional[str] = ""
    cf: Optional[str] = ""
    ca: Optional[str] = ""
    in_: Optional[str] = ""
    rp: Optional[str] = ""


# --- EPQ-J ---


class EPQJSubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    sexo: str = "M"
    item_01: Optional[int] = 0
    item_02: Optional[int] = 0
    item_03: Optional[int] = 0
    item_04: Optional[int] = 0
    item_05: Optional[int] = 0
    item_06: Optional[int] = 0
    item_07: Optional[int] = 0
    item_08: Optional[int] = 0
    item_09: Optional[int] = 0
    item_10: Optional[int] = 0
    item_11: Optional[int] = 0
    item_12: Optional[int] = 0
    item_13: Optional[int] = 0
    item_14: Optional[int] = 0
    item_15: Optional[int] = 0
    item_16: Optional[int] = 0
    item_17: Optional[int] = 0
    item_18: Optional[int] = 0
    item_19: Optional[int] = 0
    item_20: Optional[int] = 0
    item_21: Optional[int] = 0
    item_22: Optional[int] = 0
    item_23: Optional[int] = 0
    item_24: Optional[int] = 0
    item_25: Optional[int] = 0
    item_26: Optional[int] = 0
    item_27: Optional[int] = 0
    item_28: Optional[int] = 0
    item_29: Optional[int] = 0
    item_30: Optional[int] = 0
    item_31: Optional[int] = 0
    item_32: Optional[int] = 0
    item_33: Optional[int] = 0
    item_34: Optional[int] = 0
    item_35: Optional[int] = 0
    item_36: Optional[int] = 0
    item_37: Optional[int] = 0
    item_38: Optional[int] = 0
    item_39: Optional[int] = 0
    item_40: Optional[int] = 0
    item_41: Optional[int] = 0
    item_42: Optional[int] = 0
    item_43: Optional[int] = 0
    item_44: Optional[int] = 0
    item_45: Optional[int] = 0
    item_46: Optional[int] = 0
    item_47: Optional[int] = 0
    item_48: Optional[int] = 0
    item_49: Optional[int] = 0
    item_50: Optional[int] = 0
    item_51: Optional[int] = 0
    item_52: Optional[int] = 0
    item_53: Optional[int] = 0
    item_54: Optional[int] = 0
    item_55: Optional[int] = 0
    item_56: Optional[int] = 0
    item_57: Optional[int] = 0
    item_58: Optional[int] = 0
    item_59: Optional[int] = 0
    item_60: Optional[int] = 0


# --- ETDAH-AD ---


class ETDAHADSubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    item_01: int = 0
    item_02: int = 0
    item_03: int = 0
    item_04: int = 0
    item_05: int = 0
    item_06: int = 0
    item_07: int = 0
    item_08: int = 0
    item_09: int = 0
    item_10: int = 0
    item_11: int = 0
    item_12: int = 0
    item_13: int = 0
    item_14: int = 0
    item_15: int = 0
    item_16: int = 0
    item_17: int = 0
    item_18: int = 0
    item_19: int = 0
    item_20: int = 0
    item_21: int = 0
    item_22: int = 0
    item_23: int = 0
    item_24: int = 0
    item_25: int = 0
    item_26: int = 0
    item_27: int = 0
    item_28: int = 0
    item_29: int = 0
    item_30: int = 0
    item_31: int = 0
    item_32: int = 0
    item_33: int = 0
    item_34: int = 0
    item_35: int = 0
    item_36: int = 0
    item_37: int = 0
    item_38: int = 0
    item_39: int = 0
    item_40: int = 0
    item_41: int = 0
    item_42: int = 0
    item_43: int = 0
    item_44: int = 0
    item_45: int = 0
    item_46: int = 0
    item_47: int = 0
    item_48: int = 0
    item_49: int = 0
    item_50: int = 0
    item_51: int = 0
    item_52: int = 0
    item_53: int = 0
    item_54: int = 0
    item_55: int = 0
    item_56: int = 0
    item_57: int = 0
    item_58: int = 0
    item_59: int = 0
    item_60: int = 0
    item_61: int = 0
    item_62: int = 0
    item_63: int = 0
    item_64: int = 0
    item_65: int = 0
    item_66: int = 0
    item_67: int = 0
    item_68: int = 0
    item_69: int = 0
