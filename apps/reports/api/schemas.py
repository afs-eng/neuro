from typing import Optional, List
from ninja import Schema


class MessageOut(Schema):
    message: str


class HtmlOut(Schema):
    html: str


class FileOut(Schema):
    file_url: str


class ReportSectionOut(Schema):
    id: int
    key: str
    title: str
    order: int
    source_payload: dict = {}
    generated_text: str
    edited_text: str
    generation_metadata: dict = {}
    warnings_payload: List[str] = []
    is_locked: bool
    updated_at: Optional[str] = None


class ReportVersionOut(Schema):
    id: int
    version_number: int
    content: str
    created_by: str
    created_at: Optional[str] = None


class ReportSectionUpdateIn(Schema):
    edited_text: Optional[str] = None
    is_locked: Optional[bool] = None


class ReportOut(Schema):
    id: int
    evaluation_id: int
    evaluation_code: str = ""
    evaluation_title: str = ""
    patient_id: int
    patient_name: str = ""
    author_id: Optional[int]
    author_name: str
    title: str
    interested_party: str = ""
    purpose: str = ""
    status: str
    snapshot_payload: dict = {}
    context_payload: dict = {}
    generated_text: str
    edited_text: str
    final_text: str
    ai_metadata: dict = {}
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    generated_at: Optional[str] = None


class ReportDetailOut(ReportOut):
    sections: List[ReportSectionOut] = []
    versions: List[ReportVersionOut] = []


class ReportCreateIn(Schema):
    evaluation_id: int
    title: Optional[str] = "Laudo Neuropsicológico"
    patient_id: Optional[int] = None
    interested_party: Optional[str] = ""
    purpose: Optional[str] = ""


class ReportUpdateIn(Schema):
    title: Optional[str] = None
    interested_party: Optional[str] = None
    purpose: Optional[str] = None
    status: Optional[str] = None
    final_text: Optional[str] = None
