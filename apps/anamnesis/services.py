from datetime import timedelta

from django.utils import timezone

from apps.messaging.services import (
    send_anamnesis_invite_via_email,
    send_anamnesis_invite_via_whatsapp,
)

from .constants import (
    ANAMNESIS_DEFAULT_EXPIRATION_DAYS,
    ANAMNESIS_MESSAGE_TEMPLATE,
    get_default_templates,
)
from .selectors import (
    get_active_invites_by_evaluation,
    get_current_anamnesis_response_by_evaluation,
)
from .models import (
    AnamnesisInvite,
    AnamnesisInviteStatus,
    AnamnesisResponse,
    AnamnesisResponseSource,
    AnamnesisResponseStatus,
    AnamnesisTemplate,
)


INVITE_ALLOWED_TRANSITIONS = {
    AnamnesisInviteStatus.PENDING: {
        AnamnesisInviteStatus.SENT,
        AnamnesisInviteStatus.CANCELED,
        AnamnesisInviteStatus.EXPIRED,
    },
    AnamnesisInviteStatus.SENT: {
        AnamnesisInviteStatus.OPENED,
        AnamnesisInviteStatus.CANCELED,
        AnamnesisInviteStatus.EXPIRED,
    },
    AnamnesisInviteStatus.OPENED: {
        AnamnesisInviteStatus.IN_PROGRESS,
        AnamnesisInviteStatus.COMPLETED,
        AnamnesisInviteStatus.CANCELED,
        AnamnesisInviteStatus.EXPIRED,
    },
    AnamnesisInviteStatus.IN_PROGRESS: {
        AnamnesisInviteStatus.COMPLETED,
        AnamnesisInviteStatus.CANCELED,
        AnamnesisInviteStatus.EXPIRED,
    },
    AnamnesisInviteStatus.COMPLETED: set(),
    AnamnesisInviteStatus.EXPIRED: set(),
    AnamnesisInviteStatus.CANCELED: set(),
}

RESPONSE_ALLOWED_TRANSITIONS = {
    AnamnesisResponseStatus.DRAFT: {
        AnamnesisResponseStatus.SUBMITTED,
        AnamnesisResponseStatus.REVIEWED,
    },
    AnamnesisResponseStatus.SUBMITTED: {
        AnamnesisResponseStatus.DRAFT,
        AnamnesisResponseStatus.REVIEWED,
    },
    AnamnesisResponseStatus.REVIEWED: {AnamnesisResponseStatus.DRAFT},
}


def ensure_invite_transition(invite: AnamnesisInvite, next_status: str) -> None:
    allowed = INVITE_ALLOWED_TRANSITIONS.get(invite.status, set())
    if next_status not in allowed:
        raise ValueError(
            f"Transição inválida do convite: {invite.status} -> {next_status}"
        )


def ensure_response_transition(response: AnamnesisResponse, next_status: str) -> None:
    if response.status == next_status:
        return
    allowed = RESPONSE_ALLOWED_TRANSITIONS.get(response.status, set())
    if next_status not in allowed:
        raise ValueError(
            f"Transição inválida da resposta: {response.status} -> {next_status}"
        )


def build_public_url(token: str, frontend_base_url: str) -> str:
    return f"{frontend_base_url.rstrip('/')}/public/anamnesis/{token}"


def build_default_message(invite: AnamnesisInvite, public_url: str) -> str:
    return ANAMNESIS_MESSAGE_TEMPLATE.format(
        recipient_name=invite.recipient_name,
        patient_name=invite.patient.full_name,
        public_url=public_url,
    )


def create_invite(
    *,
    evaluation,
    patient,
    template,
    created_by,
    recipient_name,
    recipient_email="",
    recipient_phone="",
    channel="email",
    message="",
    expires_at=None,
):
    if expires_at is None:
        expires_at = timezone.now() + timedelta(days=ANAMNESIS_DEFAULT_EXPIRATION_DAYS)

    for active_invite in get_active_invites_by_evaluation(evaluation.id):
        active_invite.status = AnamnesisInviteStatus.CANCELED
        active_invite.save(update_fields=["status", "updated_at"])

    invite = AnamnesisInvite.objects.create(
        evaluation=evaluation,
        patient=patient,
        template=template,
        created_by=created_by,
        recipient_name=recipient_name,
        recipient_email=recipient_email,
        recipient_phone=recipient_phone,
        channel=channel,
        message=message,
        expires_at=expires_at,
    )
    return invite


def send_invite(invite: AnamnesisInvite, frontend_base_url: str) -> dict:
    public_url = build_public_url(invite.token, frontend_base_url)
    message = invite.message or build_default_message(invite, public_url)

    if invite.channel == "email":
        payload = send_anamnesis_invite_via_email(
            invite=invite, public_url=public_url, message=message
        )
    else:
        payload = send_anamnesis_invite_via_whatsapp(
            invite=invite, public_url=public_url, message=message
        )

    invite.message = message
    invite.delivery_payload = payload
    ensure_invite_transition(invite, AnamnesisInviteStatus.SENT)
    invite.status = AnamnesisInviteStatus.SENT
    invite.sent_at = timezone.now()
    invite.last_activity_at = timezone.now()
    invite.save()
    return payload


def cancel_invite(invite: AnamnesisInvite) -> AnamnesisInvite:
    ensure_invite_transition(invite, AnamnesisInviteStatus.CANCELED)
    invite.status = AnamnesisInviteStatus.CANCELED
    invite.save(update_fields=["status", "updated_at"])
    return invite


def touch_invite_open(invite: AnamnesisInvite) -> AnamnesisInvite:
    now = timezone.now()
    if not invite.opened_at:
        invite.opened_at = now
    if invite.status in {AnamnesisInviteStatus.PENDING, AnamnesisInviteStatus.SENT}:
        ensure_invite_transition(invite, AnamnesisInviteStatus.OPENED)
        invite.status = AnamnesisInviteStatus.OPENED
    invite.last_activity_at = now
    invite.save(update_fields=["opened_at", "status", "last_activity_at", "updated_at"])
    return invite


def get_or_create_response(invite: AnamnesisInvite) -> AnamnesisResponse:
    response, _ = AnamnesisResponse.objects.get_or_create(
        invite=invite,
        defaults={
            "evaluation": invite.evaluation,
            "patient": invite.patient,
            "template": invite.template,
            "response_type": invite.template.target_type,
            "source": AnamnesisResponseSource.EXTERNAL,
            "created_by": invite.created_by,
        },
    )
    return response


def save_draft_response(
    invite: AnamnesisInvite,
    *,
    answers_payload: dict,
    submitted_by_name="",
    submitted_by_relation="",
) -> AnamnesisResponse:
    response = get_or_create_response(invite)
    response.answers_payload = answers_payload
    response.submitted_by_name = submitted_by_name
    response.submitted_by_relation = submitted_by_relation
    ensure_response_transition(response, AnamnesisResponseStatus.DRAFT)
    response.status = AnamnesisResponseStatus.DRAFT
    response.save()

    invite.status = AnamnesisInviteStatus.IN_PROGRESS
    invite.last_activity_at = timezone.now()
    invite.save(update_fields=["status", "last_activity_at", "updated_at"])
    return response


def submit_response(
    invite: AnamnesisInvite,
    *,
    answers_payload: dict,
    submitted_by_name: str,
    submitted_by_relation: str,
) -> AnamnesisResponse:
    response = get_or_create_response(invite)
    now = timezone.now()
    response.answers_payload = answers_payload
    response.submitted_by_name = submitted_by_name
    response.submitted_by_relation = submitted_by_relation
    ensure_response_transition(response, AnamnesisResponseStatus.SUBMITTED)
    response.status = AnamnesisResponseStatus.SUBMITTED
    response.submitted_at = now
    response.save()

    invite.status = AnamnesisInviteStatus.COMPLETED
    invite.completed_at = now
    invite.last_activity_at = now
    invite.save(
        update_fields=["status", "completed_at", "last_activity_at", "updated_at"]
    )
    return response


def review_response(
    response: AnamnesisResponse,
    *,
    reviewed_by,
    answers_payload: dict | None = None,
    summary_payload: dict | None = None,
    status: str = AnamnesisResponseStatus.REVIEWED,
) -> AnamnesisResponse:
    if answers_payload is not None:
        response.answers_payload = answers_payload
    if summary_payload is not None:
        response.summary_payload = summary_payload
    elif response.answers_payload:
        response.summary_payload = generate_summary_payload(
            response.answers_payload, response.response_type
        )
    ensure_response_transition(response, status)
    response.status = status
    response.reviewed_by = reviewed_by
    response.reviewed_at = timezone.now()
    response.save()
    return response


def generate_summary_payload(answers_payload: dict, response_type: str) -> dict:
    def text(*keys: str) -> str:
        values = []
        for key in keys:
            value = answers_payload.get(key)
            if value:
                if isinstance(value, list):
                    values.append(", ".join(str(item) for item in value if item))
                elif isinstance(value, dict):
                    values.append(str(value))
                else:
                    values.append(str(value))
        return " ".join(item.strip() for item in values if item).strip()

    risk_flags = []
    if answers_payload.get("development_regression") is True:
        risk_flags.append("historico_de_regressao")
    if answers_payload.get("hospitalizations"):
        risk_flags.append("historico_de_internacao")
    if answers_payload.get("previous_diagnostic_hypotheses"):
        risk_flags.append("historico_de_hipotese_diagnostica")
    if answers_payload.get("current_medications") or answers_payload.get(
        "medication_details"
    ):
        risk_flags.append("uso_de_medicacao")

    clinically_relevant_points = [
        item
        for item in [
            text("main_complaint"),
            text("evaluation_reason", "reason_for_assessment", "referral_reason"),
            text("medical_notes", "clinical_notes"),
            text(
                "school_difficulties_by_year",
                "academic_difficulties",
                "general_school_performance",
            ),
        ]
        if item
    ]

    return {
        "response_type": response_type,
        "chief_complaint": text("main_complaint"),
        "development_summary": text(
            "development_notes",
            "motor_comparison",
            "speech_description",
            "development_delays",
        ),
        "medical_history_summary": text(
            "medical_notes",
            "current_medical_treatment",
            "current_medications",
            "medication_details",
            "neurological_psychiatric_history",
        ),
        "school_history_summary": text(
            "school_difficulties_by_year",
            "general_school_performance",
            "academic_difficulties",
            "teacher_reports_difficulties",
        ),
        "family_context_summary": text(
            "family_notes",
            "support_network",
            "family_relationships",
            "lives_with",
            "current_residence",
        ),
        "sleep_eating_summary": text(
            "current_sleep",
            "feeding_notes",
            "sleep_pattern",
            "food_notes",
            "sleep_food",
        ),
        "routine_summary": text(
            "weekday_routine",
            "weekend_routine",
            "routine_notes",
            "functional_notes",
        ),
        "risk_flags": risk_flags,
        "clinically_relevant_points": clinically_relevant_points,
    }


def sync_default_templates() -> list[AnamnesisTemplate]:
    current_codes = [item["code"] for item in get_default_templates()]
    # Deactivate templates that are not in the current defaults to avoid duplicates (e.g., v1)
    AnamnesisTemplate.objects.filter(is_active=True).exclude(
        code__in=current_codes
    ).update(is_active=False)

    templates = []
    for item in get_default_templates():
        template, _ = AnamnesisTemplate.objects.update_or_create(
            code=item["code"],
            defaults={
                "name": item["name"],
                "target_type": item["target_type"],
                "version": item["version"],
                "schema_payload": item["schema_payload"],
                "is_active": True,
            },
        )
        templates.append(template)
    return templates


def create_internal_response(
    *, evaluation, patient, template, created_by
) -> AnamnesisResponse:
    return AnamnesisResponse.objects.create(
        evaluation=evaluation,
        patient=patient,
        template=template,
        response_type=template.target_type,
        source=AnamnesisResponseSource.INTERNAL,
        created_by=created_by,
        submitted_by_name=patient.full_name,
        submitted_by_relation="proprio paciente"
        if template.target_type == "adult"
        else "informante interno",
    )


def update_response_draft(
    response: AnamnesisResponse,
    *,
    answers_payload: dict,
    submitted_by_name: str = "",
    submitted_by_relation: str = "",
    summary_payload: dict | None = None,
) -> AnamnesisResponse:
    response.answers_payload = answers_payload
    if submitted_by_name:
        response.submitted_by_name = submitted_by_name
    if submitted_by_relation:
        response.submitted_by_relation = submitted_by_relation
    if summary_payload is not None:
        response.summary_payload = summary_payload
    elif answers_payload:
        response.summary_payload = generate_summary_payload(
            answers_payload, response.response_type
        )
    if response.status == AnamnesisResponseStatus.REVIEWED:
        ensure_response_transition(response, AnamnesisResponseStatus.DRAFT)
        response.status = AnamnesisResponseStatus.DRAFT
    response.save()
    return response


def submit_internal_response(
    response: AnamnesisResponse,
    *,
    answers_payload: dict | None = None,
    submitted_by_name: str = "",
    submitted_by_relation: str = "",
    summary_payload: dict | None = None,
) -> AnamnesisResponse:
    if answers_payload is not None:
        response.answers_payload = answers_payload
    if submitted_by_name:
        response.submitted_by_name = submitted_by_name
    if submitted_by_relation:
        response.submitted_by_relation = submitted_by_relation
    if summary_payload is not None:
        response.summary_payload = summary_payload
    elif response.answers_payload:
        response.summary_payload = generate_summary_payload(
            response.answers_payload, response.response_type
        )
    ensure_response_transition(response, AnamnesisResponseStatus.SUBMITTED)
    response.status = AnamnesisResponseStatus.SUBMITTED
    response.submitted_at = timezone.now()
    response.save()
    return response


def invite_access_state(invite: AnamnesisInvite) -> str:
    if invite.status == AnamnesisInviteStatus.CANCELED:
        return "canceled"
    if invite.is_expired:
        if invite.status != AnamnesisInviteStatus.EXPIRED:
            invite.status = AnamnesisInviteStatus.EXPIRED
            invite.save(update_fields=["status", "updated_at"])
        return "expired"
    if invite.status == AnamnesisInviteStatus.COMPLETED:
        return "completed"
    return "active"


def get_current_response_summary(evaluation_id: int) -> dict | None:
    response = get_current_anamnesis_response_by_evaluation(evaluation_id)
    if not response:
        return None
    return {
        "response_id": response.id,
        "status": response.status,
        "source": response.source,
        "response_type": response.response_type,
        "template_name": response.template.name,
        "submitted_by_name": response.submitted_by_name or "",
        "submitted_by_relation": response.submitted_by_relation or "",
        "submitted_at": response.submitted_at.isoformat()
        if response.submitted_at
        else None,
        "reviewed_at": response.reviewed_at.isoformat()
        if response.reviewed_at
        else None,
        "summary_payload": response.summary_payload or {},
    }
