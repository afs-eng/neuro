from typing import Optional

from ninja import Schema


class ReportSectionOut(Schema):
    id: int
    key: str
    title: str
    order: int
    source_payload: dict
    generated_text: str
    edited_text: str
    is_locked: bool


class ReportOut(Schema):
    id: int
    evaluation_id: int
    patient_id: int
    author_id: int
    author_name: str
    title: str
    interested_party: str
    purpose: str
    status: str
    snapshot_payload: dict
    final_text: str
    created_at: str
    updated_at: str


class ReportDetailOut(ReportOut):
    sections: list[ReportSectionOut] = []


class ReportCreateIn(Schema):
    evaluation_id: int
    patient_id: int
    author_id: Optional[int] = None
    title: str
    interested_party: Optional[str] = ""
    purpose: Optional[str] = ""
    status: Optional[str] = "draft"


class ReportUpdateIn(Schema):
    title: Optional[str] = None
    interested_party: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[str] = None
    final_text: Optional[str] = None


class ReportSectionUpdateIn(Schema):
    edited_text: Optional[str] = None
    is_locked: Optional[bool] = None


class MessageOut(Schema):
    message: str
