from datetime import datetime
from typing import Any, Optional

from ninja import Schema


class AnamnesisTemplateOut(Schema):
    id: int
    code: str
    name: str
    target_type: str
    version: str
    schema_payload: dict[str, Any]
    is_active: bool


class AnamnesisInviteCreateIn(Schema):
    evaluation_id: int
    patient_id: int
    template_id: int
    recipient_name: str
    recipient_email: Optional[str] = ""
    recipient_phone: Optional[str] = ""
    channel: str
    message: Optional[str] = ""
    expires_at: Optional[datetime] = None


class AnamnesisInviteOut(Schema):
    id: int
    evaluation_id: int
    patient_id: int
    template_id: int
    template_name: str
    template_target_type: str
    recipient_name: str
    recipient_email: str
    recipient_phone: str
    channel: str
    token: str
    public_url: str
    status: str
    sent_at: Optional[str] = None
    opened_at: Optional[str] = None
    last_activity_at: Optional[str] = None
    completed_at: Optional[str] = None
    expires_at: Optional[str] = None
    created_by_name: str
    created_at: str
    message: str
    delivery_payload: dict[str, Any]


class AnamnesisResponseCreateIn(Schema):
    evaluation_id: int
    patient_id: int
    template_id: int
    submitted_by_name: Optional[str] = ""
    submitted_by_relation: Optional[str] = ""
    answers_payload: dict[str, Any] = {}
    summary_payload: dict[str, Any] = {}


class AnamnesisResponseUpdateIn(Schema):
    submitted_by_name: Optional[str] = None
    submitted_by_relation: Optional[str] = None
    answers_payload: Optional[dict[str, Any]] = None
    summary_payload: Optional[dict[str, Any]] = None


class AnamnesisResponseSubmitIn(Schema):
    submitted_by_name: Optional[str] = None
    submitted_by_relation: Optional[str] = None
    answers_payload: Optional[dict[str, Any]] = None
    summary_payload: Optional[dict[str, Any]] = None


class AnamnesisResponseReviewIn(Schema):
    answers_payload: Optional[dict[str, Any]] = None
    summary_payload: Optional[dict[str, Any]] = None
    status: Optional[str] = "reviewed"


class AnamnesisResponseOut(Schema):
    id: int
    invite_id: Optional[int] = None
    evaluation_id: int
    patient_id: int
    template_id: int
    template_name: str
    response_type: str
    source: str
    answers_payload: dict[str, Any]
    summary_payload: dict[str, Any]
    status: str
    submitted_by_name: str
    submitted_by_relation: str
    submitted_at: Optional[str] = None
    created_by_name: Optional[str] = None
    reviewed_by_name: Optional[str] = None
    reviewed_at: Optional[str] = None
    created_at: str
    updated_at: str


class PublicAnamnesisOut(Schema):
    invite_id: int
    status: str
    patient_name: str
    template_name: str
    target_type: str
    schema_payload: dict[str, Any]
    answers_payload: dict[str, Any]
    submitted_by_name: str
    submitted_by_relation: str
    expires_at: Optional[str] = None
    access_state: str
    message: str


class PublicAnamnesisDraftIn(Schema):
    answers_payload: dict[str, Any]
    submitted_by_name: Optional[str] = ""
    submitted_by_relation: Optional[str] = ""


class PublicAnamnesisSubmitIn(Schema):
    answers_payload: dict[str, Any]
    submitted_by_name: str
    submitted_by_relation: str


class MessageOut(Schema):
    message: str
