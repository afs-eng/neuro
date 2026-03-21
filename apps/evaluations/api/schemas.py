from datetime import date
from typing import Optional

from ninja import Schema


class EvaluationOut(Schema):
    id: int
    patient_id: int
    patient_name: str
    examiner_id: int
    examiner_name: str
    referral_reason: str
    evaluation_purpose: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    general_notes: str


class EvaluationCreateIn(Schema):
    patient_id: int
    examiner_id: int
    referral_reason: Optional[str] = ""
    evaluation_purpose: Optional[str] = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = "draft"
    general_notes: Optional[str] = ""


class EvaluationUpdateIn(Schema):
    patient_id: Optional[int] = None
    examiner_id: Optional[int] = None
    referral_reason: Optional[str] = None
    evaluation_purpose: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    general_notes: Optional[str] = None


class MessageOut(Schema):
    message: str