from datetime import date as date_cls
from ninja import Router, Query
from ninja.errors import HttpError

from apps.api.auth import bearer_auth
from apps.accounts.models import User, UserRole
from apps.patients.models import Patient
from apps.evaluations.models import EvaluationStatus, EvaluationPriority
from apps.evaluations.selectors import (
    get_evaluation_by_id,
    get_evaluations,
    get_evaluations_by_patient,
)
from apps.evaluations.services import create_evaluation, update_evaluation

from .schemas import (
    EvaluationOut,
    EvaluationCreateIn,
    EvaluationUpdateIn,
    EvaluationDetailOut,
    TestApplicationOut,
    DocumentOut,
    MessageOut,
)


router = Router(tags=["evaluations"])


def can_view_evaluations(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
        UserRole.READONLY,
    }


def can_edit_evaluations(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
    }


def serialize_evaluation(evaluation, include_details=False):
    patient = evaluation.patient
    examiner = evaluation.examiner

    data = {
        "id": evaluation.id,
        "code": f"AV-{evaluation.id:04d}",
        "title": evaluation.title or "",
        "patient_id": patient.id,
        "patient_name": patient.full_name,
        "patient_birth_date": patient.birth_date,
        "patient_sex": patient.sex,
        "examiner_id": examiner.id if examiner else None,
        "examiner_name": examiner.display_name if examiner else None,
        "referral_reason": evaluation.referral_reason or "",
        "evaluation_purpose": evaluation.evaluation_purpose or "",
        "clinical_hypothesis": evaluation.clinical_hypothesis or "",
        "start_date": evaluation.start_date,
        "end_date": evaluation.end_date,
        "status": evaluation.status,
        "status_display": evaluation.get_status_display(),
        "priority": evaluation.priority,
        "priority_display": evaluation.get_priority_display(),
        "is_archived": evaluation.is_archived,
        "general_notes": evaluation.general_notes or "",
        "created_at": evaluation.created_at.isoformat()
        if evaluation.created_at
        else None,
        "updated_at": evaluation.updated_at.isoformat()
        if evaluation.updated_at
        else None,
    }

    if include_details:
        from apps.tests.models import TestApplication

        tests = TestApplication.objects.filter(evaluation=evaluation).select_related(
            "instrument"
        )
        data["tests"] = [
            {
                "id": t.id,
                "instrument_name": t.instrument.name,
                "instrument_code": t.instrument.code,
                "applied_on": t.applied_on,
                "is_validated": t.is_validated,
                "status": "Concluído" if t.is_validated else "Pendente",
            }
            for t in tests
        ]
        data["documents"] = []

    return data


@router.get("/", response=list[EvaluationOut], auth=bearer_auth)
def list_evaluations(
    request, patient_id: int | None = Query(default=None)
) -> list[dict]:
    user = request.auth

    if not can_view_evaluations(user):
        raise HttpError(403, "Você não tem permissão para visualizar avaliações.")

    evaluations = (
        get_evaluations_by_patient(patient_id) if patient_id else get_evaluations()
    )
    return [serialize_evaluation(evaluation) for evaluation in evaluations]


@router.get(
    "/{evaluation_id}",
    response={200: EvaluationDetailOut, 404: MessageOut},
    auth=bearer_auth,
)
def get_evaluation_endpoint(request, evaluation_id: int) -> tuple[int, dict]:
    user = request.auth

    if not can_view_evaluations(user):
        raise HttpError(403, "Você não tem permissão para visualizar avaliações.")

    evaluation = get_evaluation_by_id(evaluation_id)
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    return 200, serialize_evaluation(evaluation, include_details=True)


@router.post(
    "/",
    response={201: EvaluationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def create_evaluation_endpoint(
    request, payload: EvaluationCreateIn
) -> tuple[int, dict]:
    user = request.auth

    if not can_edit_evaluations(user):
        return 403, {"message": "Você não tem permissão para criar avaliações."}

    patient = Patient.objects.filter(id=payload.patient_id).first()
    if not patient:
        return 404, {"message": "Paciente não encontrado."}

    examiner = None
    if payload.examiner_id:
        examiner = User.objects.filter(id=payload.examiner_id, is_active=True).first()

    evaluation = create_evaluation(
        patient=patient,
        examiner=examiner,
        title=payload.title or "",
        referral_reason=payload.referral_reason or "",
        evaluation_purpose=payload.evaluation_purpose or "",
        clinical_hypothesis=payload.clinical_hypothesis or "",
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=payload.status or EvaluationStatus.DRAFT,
        priority=payload.priority or EvaluationPriority.MEDIUM,
        general_notes=payload.general_notes or "",
    )

    return 201, serialize_evaluation(evaluation)


@router.patch(
    "/{evaluation_id}",
    response={200: EvaluationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_evaluation_endpoint(
    request, evaluation_id: int, payload: EvaluationUpdateIn
) -> tuple[int, dict]:
    user = request.auth

    if not can_edit_evaluations(user):
        return 403, {"message": "Você não tem permissão para editar avaliações."}

    evaluation = get_evaluation_by_id(evaluation_id)
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    data = payload.dict(exclude_unset=True)

    if "patient_id" in data:
        patient = Patient.objects.filter(id=data["patient_id"]).first()
        if not patient:
            return 404, {"message": "Paciente não encontrado."}
        data["patient"] = patient
        del data["patient_id"]

    if "examiner_id" in data:
        examiner = None
        if data["examiner_id"]:
            examiner = User.objects.filter(
                id=data["examiner_id"], is_active=True
            ).first()
        data["examiner"] = examiner
        del data["examiner_id"]

    evaluation = update_evaluation(evaluation, **data)
    return 200, serialize_evaluation(evaluation)
