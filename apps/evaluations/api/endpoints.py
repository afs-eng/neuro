from ninja import Router, Query
from ninja.errors import HttpError

from apps.api.auth import bearer_auth
from apps.accounts.models import User, UserRole
from apps.patients.models import Patient
from apps.evaluations.models import EvaluationStatus
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


def serialize_evaluation(evaluation):
    return {
        "id": evaluation.id,
        "patient_id": evaluation.patient_id,
        "patient_name": evaluation.patient.full_name,
        "examiner_id": evaluation.examiner_id,
        "examiner_name": evaluation.examiner.display_name,
        "referral_reason": evaluation.referral_reason,
        "evaluation_purpose": evaluation.evaluation_purpose,
        "start_date": evaluation.start_date,
        "end_date": evaluation.end_date,
        "status": evaluation.status,
        "general_notes": evaluation.general_notes,
    }


@router.get("/", response=list[EvaluationOut], auth=bearer_auth)
def list_evaluations(request, patient_id: int | None = Query(default=None)):
    user = request.auth

    if not can_view_evaluations(user):
        raise HttpError(403, "Você não tem permissão para visualizar avaliações.")

    evaluations = (
        get_evaluations_by_patient(patient_id)
        if patient_id
        else get_evaluations()
    )
    return [serialize_evaluation(evaluation) for evaluation in evaluations]


@router.get(
    "/{evaluation_id}",
    response={200: EvaluationOut, 404: MessageOut},
    auth=bearer_auth,
)
def get_evaluation_endpoint(request, evaluation_id: int):
    user = request.auth

    if not can_view_evaluations(user):
        raise HttpError(403, "Você não tem permissão para visualizar avaliações.")

    evaluation = get_evaluation_by_id(evaluation_id)
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    return 200, serialize_evaluation(evaluation)


@router.post(
    "/",
    response={201: EvaluationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def create_evaluation_endpoint(request, payload: EvaluationCreateIn):
    user = request.auth

    if not can_edit_evaluations(user):
        return 403, {"message": "Você não tem permissão para criar avaliações."}

    patient = Patient.objects.filter(id=payload.patient_id).first()
    if not patient:
        return 404, {"message": "Paciente não encontrado."}

    examiner = User.objects.filter(id=payload.examiner_id, is_active=True).first()
    if not examiner:
        return 404, {"message": "Profissional responsável não encontrado."}

    evaluation = create_evaluation(
        patient=patient,
        examiner=examiner,
        referral_reason=payload.referral_reason or "",
        evaluation_purpose=payload.evaluation_purpose or "",
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=payload.status or EvaluationStatus.DRAFT,
        general_notes=payload.general_notes or "",
    )

    return 201, serialize_evaluation(evaluation)


@router.patch(
    "/{evaluation_id}",
    response={200: EvaluationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_evaluation_endpoint(request, evaluation_id: int, payload: EvaluationUpdateIn):
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
        examiner = User.objects.filter(id=data["examiner_id"], is_active=True).first()
        if not examiner:
            return 404, {"message": "Profissional responsável não encontrado."}
        data["examiner"] = examiner
        del data["examiner_id"]

    evaluation = update_evaluation(evaluation, **data)
    return 200, serialize_evaluation(evaluation)