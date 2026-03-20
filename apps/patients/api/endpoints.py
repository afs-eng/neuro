from ninja import Router, Query
from ninja.errors import HttpError

from apps.api.auth import bearer_auth
from apps.accounts.models import UserRole
from apps.patients.selectors import (
    get_patient_by_id,
    get_patients,
    search_patients,
)
from apps.patients.services import create_patient, update_patient

from .schemas import PatientOut, PatientCreateIn, PatientUpdateIn, MessageOut


router = Router(tags=["patients"])


def can_view_patients(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
        UserRole.READONLY,
    }


def can_edit_patients(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
    }


def serialize_patient(patient):
    return {
        "id": patient.id,
        "full_name": patient.full_name,
        "birth_date": patient.birth_date,
        "sex": patient.sex,
        "schooling": patient.schooling,
        "school_name": patient.school_name,
        "occupation": patient.occupation,
        "mother_name": patient.mother_name,
        "father_name": patient.father_name,
        "phone": patient.phone,
        "email": patient.email,
        "city": patient.city,
        "state": patient.state,
        "notes": patient.notes,
    }


@router.get("/", response=list[PatientOut], auth=bearer_auth)
def list_patients(request, q: str | None = Query(default=None)):
    user = request.auth

    if not can_view_patients(user):
        raise HttpError(403, "Você não tem permissão para visualizar pacientes.")

    patients = search_patients(q) if q else get_patients()
    return [serialize_patient(patient) for patient in patients]


@router.get(
    "/{patient_id}",
    response={200: PatientOut, 404: MessageOut},
    auth=bearer_auth,
)
def get_patient_endpoint(request, patient_id: int):
    user = request.auth

    if not can_view_patients(user):
        raise HttpError(403, "Você não tem permissão para visualizar pacientes.")

    patient = get_patient_by_id(patient_id)
    if not patient:
        return 404, {"message": "Paciente não encontrado."}

    return 200, serialize_patient(patient)


@router.post(
    "/",
    response={201: PatientOut, 403: MessageOut},
    auth=bearer_auth,
)
def create_patient_endpoint(request, payload: PatientCreateIn):
    user = request.auth

    if not can_edit_patients(user):
        return 403, {"message": "Você não tem permissão para criar pacientes."}

    patient = create_patient(**payload.dict())
    return 201, serialize_patient(patient)


@router.patch(
    "/{patient_id}",
    response={200: PatientOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_patient_endpoint(request, patient_id: int, payload: PatientUpdateIn):
    user = request.auth

    if not can_edit_patients(user):
        return 403, {"message": "Você não tem permissão para editar pacientes."}

    patient = get_patient_by_id(patient_id)
    if not patient:
        return 404, {"message": "Paciente não encontrado."}

    patient = update_patient(patient, **payload.dict(exclude_unset=True))
    return 200, serialize_patient(patient)