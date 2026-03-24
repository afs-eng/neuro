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