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
    item_01: int
    item_02: int
    item_03: int
    item_04: int
    item_05: int
    item_06: int
    item_07: int
    item_08: int
    item_09: int
    item_10: int
    item_11: int
    item_12: int
    item_13: int
    item_14: int
    item_15: int
    item_16: int
    item_17: int
    item_18: int
    item_19: int
    item_20: int
    item_21: int
    item_22: int
    item_23: int
    item_24: int
    item_25: int
    item_26: int
    item_27: int
    item_28: int
    item_29: int
    item_30: int
    item_31: int
    item_32: int
    item_33: int
    item_34: int
    item_35: int
    item_36: int
    item_37: int
    item_38: int
    item_39: int
    item_40: int
    item_41: int
    item_42: int
    item_43: int
    item_44: int
    item_45: int


# --- EBADEP-IJ ---


class EBADEPIJSubmitIn(Schema):
    evaluation_id: int
    applied_on: Optional[date] = None
    item_01: int
    item_02: int
    item_03: int
    item_04: int
    item_05: int
    item_06: int
    item_07: int
    item_08: int
    item_09: int
    item_10: int
    item_11: int
    item_12: int
    item_13: int
    item_14: int
    item_15: int
    item_16: int
    item_17: int
    item_18: int
    item_19: int
    item_20: int
    item_21: int
    item_22: int
    item_23: int
    item_24: int
    item_25: int
    item_26: int
    item_27: int


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
