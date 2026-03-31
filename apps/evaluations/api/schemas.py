from datetime import date
from typing import Optional

from ninja import Schema


class EvaluationOut(Schema):
    id: int
    code: str
    title: str
    patient_id: int
    patient_name: str
    patient_birth_date: Optional[date] = None
    patient_sex: Optional[str] = None
    examiner_id: Optional[int] = None
    examiner_name: Optional[str] = None
    referral_reason: str
    evaluation_purpose: str
    clinical_hypothesis: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    status_display: str
    priority: str
    priority_display: str
    is_archived: bool
    general_notes: str
    created_at: str
    updated_at: str


class EvaluationCreateIn(Schema):
    patient_id: int
    title: Optional[str] = ""
    examiner_id: Optional[int] = None
    referral_reason: Optional[str] = ""
    evaluation_purpose: Optional[str] = ""
    clinical_hypothesis: Optional[str] = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = "draft"
    priority: Optional[str] = "medium"
    general_notes: Optional[str] = ""


class EvaluationUpdateIn(Schema):
    title: Optional[str] = None
    patient_id: Optional[int] = None
    examiner_id: Optional[int] = None
    referral_reason: Optional[str] = None
    evaluation_purpose: Optional[str] = None
    clinical_hypothesis: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    is_archived: Optional[bool] = None
    general_notes: Optional[str] = None


class TestApplicationOut(Schema):
    id: int
    instrument_name: str
    instrument_code: str
    applied_on: Optional[date] = None
    is_validated: bool
    status: str


class DocumentOut(Schema):
    id: int
    name: str
    file_type: str
    uploaded_at: str


class EvaluationDetailOut(EvaluationOut):
    tests: list[TestApplicationOut] = []
    documents: list[DocumentOut] = []


class MessageOut(Schema):
    message: str
