from datetime import date
from typing import Optional

from ninja import Schema


class DocumentOut(Schema):
    id: int
    evaluation_id: int
    patient_id: int
    title: str
    file_name: str
    file_url: str
    document_type: str
    document_type_display: str
    source: str
    document_date: Optional[date] = None
    notes: str
    is_relevant_for_report: bool
    created_at: str


class DocumentUpdateIn(Schema):
    title: Optional[str] = None
    document_type: Optional[str] = None
    source: Optional[str] = None
    document_date: Optional[date] = None
    notes: Optional[str] = None
    is_relevant_for_report: Optional[bool] = None


class MessageOut(Schema):
    message: str
