from ninja import Router
from ninja.errors import HttpError

from apps.accounts.models import User, UserRole
from apps.api.auth import bearer_auth
from apps.evaluations.models import Evaluation
from apps.patients.models import Patient
from apps.reports.models import Report
from apps.reports.selectors import (
    get_report_by_id,
    get_report_section_by_id,
    get_reports_by_evaluation,
)
from apps.reports.services import (
    build_report_sections,
    create_report,
    update_report,
    update_report_section,
)

from .schemas import (
    MessageOut,
    ReportCreateIn,
    ReportDetailOut,
    ReportOut,
    ReportSectionOut,
    ReportSectionUpdateIn,
    ReportUpdateIn,
)


router = Router(tags=["reports"])


def can_view_reports(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
        UserRole.READONLY,
    }


def can_edit_reports(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
    }


def serialize_section(section) -> dict:
    return {
        "id": section.id,
        "key": section.key,
        "title": section.title,
        "order": section.order,
        "source_payload": section.source_payload or {},
        "generated_text": section.generated_text or "",
        "edited_text": section.edited_text or "",
        "is_locked": section.is_locked,
    }


def serialize_report(report, include_sections=False) -> dict:
    data = {
        "id": report.id,
        "evaluation_id": report.evaluation_id,
        "patient_id": report.patient_id,
        "author_id": report.author_id,
        "author_name": report.author.display_name,
        "title": report.title,
        "interested_party": report.interested_party or "",
        "purpose": report.purpose or "",
        "status": report.status,
        "snapshot_payload": report.snapshot_payload or {},
        "final_text": report.final_text or "",
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "updated_at": report.updated_at.isoformat() if report.updated_at else None,
    }
    if include_sections:
        data["sections"] = [serialize_section(item) for item in report.sections.all()]
    return data


@router.get("/", response=list[ReportOut], auth=bearer_auth)
def list_reports(request, evaluation_id: int) -> list[dict]:
    if not can_view_reports(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar laudos.")
    return [serialize_report(item) for item in get_reports_by_evaluation(evaluation_id)]


@router.get(
    "/{report_id}", response={200: ReportDetailOut, 404: MessageOut}, auth=bearer_auth
)
def get_report_endpoint(request, report_id: int) -> tuple[int, dict]:
    if not can_view_reports(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar laudos.")
    report = get_report_by_id(report_id)
    if not report:
        return 404, {"message": "Laudo não encontrado."}
    return 200, serialize_report(report, include_sections=True)


@router.post(
    "/",
    response={201: ReportOut, 403: MessageOut, 404: MessageOut, 400: MessageOut},
    auth=bearer_auth,
)
def create_report_endpoint(request, payload: ReportCreateIn) -> tuple[int, dict]:
    if not can_edit_reports(request.auth):
        return 403, {"message": "Você não tem permissão para criar laudos."}

    evaluation = (
        Evaluation.objects.filter(id=payload.evaluation_id)
        .select_related("patient")
        .first()
    )
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = Patient.objects.filter(id=payload.patient_id).first()
    if not patient or patient.id != evaluation.patient_id:
        return 400, {"message": "Paciente inválido para a avaliação informada."}

    author = request.auth
    if payload.author_id:
        author = User.objects.filter(id=payload.author_id, is_active=True).first()
        if not author:
            return 404, {"message": "Autor não encontrado."}

    report = create_report(
        evaluation=evaluation,
        patient=patient,
        author=author,
        title=payload.title,
        interested_party=payload.interested_party or "",
        purpose=payload.purpose or "",
        status=payload.status or "draft",
    )
    build_report_sections(report)
    return 201, serialize_report(report)


@router.patch(
    "/{report_id}",
    response={200: ReportOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_report_endpoint(
    request, report_id: int, payload: ReportUpdateIn
) -> tuple[int, dict]:
    if not can_edit_reports(request.auth):
        return 403, {"message": "Você não tem permissão para editar laudos."}
    report = get_report_by_id(report_id)
    if not report:
        return 404, {"message": "Laudo não encontrado."}
    updated = update_report(report, **payload.dict(exclude_unset=True))
    return 200, serialize_report(updated)


@router.post(
    "/{report_id}/build",
    response={200: ReportDetailOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def build_report_endpoint(request, report_id: int) -> tuple[int, dict]:
    if not can_edit_reports(request.auth):
        return 403, {"message": "Você não tem permissão para gerar laudos."}
    report = get_report_by_id(report_id)
    if not report:
        return 404, {"message": "Laudo não encontrado."}
    build_report_sections(report)
    report.refresh_from_db()
    return 200, serialize_report(report, include_sections=True)


@router.patch(
    "/sections/{section_id}",
    response={200: ReportSectionOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_report_section_endpoint(
    request, section_id: int, payload: ReportSectionUpdateIn
) -> tuple[int, dict]:
    if not can_edit_reports(request.auth):
        return 403, {"message": "Você não tem permissão para editar seções do laudo."}
    section = get_report_section_by_id(section_id)
    if not section:
        return 404, {"message": "Seção não encontrada."}
    updated = update_report_section(section, **payload.dict(exclude_unset=True))
    return 200, serialize_section(updated)
