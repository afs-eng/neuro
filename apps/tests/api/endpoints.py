from ninja import Router, Query
from ninja.errors import HttpError

from apps.api.auth import bearer_auth
from apps.accounts.models import UserRole
from apps.evaluations.models import Evaluation
from apps.tests.models import Instrument
from apps.tests.selectors import (
    get_instrument_by_id,
    get_instruments,
    get_test_application_by_id,
    get_test_applications,
    get_test_applications_by_evaluation,
)
from apps.tests.services import (
    create_test_application,
    update_test_application,
    TestScoringService,
)

from .schemas import (
    InstrumentOut,
    InstrumentCreateIn,
    InstrumentUpdateIn,
    TestApplicationOut,
    TestApplicationCreateIn,
    TestApplicationUpdateIn,
    MessageOut,
)


router = Router(tags=["tests"])


def can_view_tests(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
        UserRole.READONLY,
    }


def can_edit_tests(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
    }


def serialize_instrument(instrument):
    return {
        "id": instrument.id,
        "code": instrument.code,
        "name": instrument.name,
        "category": instrument.category,
        "version": instrument.version,
        "is_active": instrument.is_active,
    }


def serialize_test_application(application):
    return {
        "id": application.id,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "instrument_id": application.instrument_id,
        "instrument_code": application.instrument.code,
        "instrument_name": application.instrument.name,
        "applied_on": application.applied_on,
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
        "reviewed_payload": application.reviewed_payload or {},
        "interpretation_text": application.interpretation_text or "",
        "is_validated": application.is_validated,
    }


@router.get("/instruments/", response=list[InstrumentOut], auth=bearer_auth)
def list_instruments(request) -> list[dict]:
    if not can_view_tests(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar instrumentos.")
    return [serialize_instrument(item) for item in get_instruments()]


@router.post("/instruments/", response={201: InstrumentOut, 403: MessageOut}, auth=bearer_auth)
def create_instrument_endpoint(request, payload: InstrumentCreateIn) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para criar instrumentos."}

    instrument = Instrument.objects.create(**payload.dict())
    return 201, serialize_instrument(instrument)


@router.patch("/instruments/{instrument_id}", response={200: InstrumentOut, 403: MessageOut, 404: MessageOut}, auth=bearer_auth)
def update_instrument_endpoint(request, instrument_id: int, payload: InstrumentUpdateIn) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para editar instrumentos."}

    instrument = get_instrument_by_id(instrument_id)
    if not instrument:
        return 404, {"message": "Instrumento não encontrado."}

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(instrument, field, value)
    instrument.save()

    return 200, serialize_instrument(instrument)


@router.get("/applications/", response=list[TestApplicationOut], auth=bearer_auth)
def list_test_applications(request, evaluation_id: int | None = Query(default=None)) -> list[dict]:
    if not can_view_tests(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar aplicações de teste.")

    applications = (
        get_test_applications_by_evaluation(evaluation_id)
        if evaluation_id
        else get_test_applications()
    )
    return [serialize_test_application(item) for item in applications]


@router.get("/applications/{application_id}", response={200: TestApplicationOut, 404: MessageOut}, auth=bearer_auth)
def get_test_application_endpoint(request, application_id: int) -> tuple[int, dict]:
    if not can_view_tests(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar aplicações de teste.")

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    return 200, serialize_test_application(application)


@router.post("/applications/", response={201: TestApplicationOut, 403: MessageOut, 404: MessageOut}, auth=bearer_auth)
def create_test_application_endpoint(request, payload: TestApplicationCreateIn) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para criar aplicações de teste."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    instrument = Instrument.objects.filter(id=payload.instrument_id, is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento não encontrado."}

    application = create_test_application(
        evaluation=evaluation,
        instrument=instrument,
        applied_on=payload.applied_on,
        raw_payload=payload.raw_payload or {},
        reviewed_payload=payload.reviewed_payload or {},
        interpretation_text=payload.interpretation_text or "",
        is_validated=payload.is_validated,
    )
    return 201, serialize_test_application(application)


@router.patch("/applications/{application_id}", response={200: TestApplicationOut, 403: MessageOut, 404: MessageOut}, auth=bearer_auth)
def update_test_application_endpoint(request, application_id: int, payload: TestApplicationUpdateIn) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para editar aplicações de teste."}

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    data = payload.dict(exclude_unset=True)

    if "evaluation_id" in data:
        evaluation = Evaluation.objects.filter(id=data["evaluation_id"]).first()
        if not evaluation:
            return 404, {"message": "Avaliação não encontrada."}
        data["evaluation"] = evaluation
        del data["evaluation_id"]

    if "instrument_id" in data:
        instrument = Instrument.objects.filter(id=data["instrument_id"], is_active=True).first()
        if not instrument:
            return 404, {"message": "Instrumento não encontrado."}
        data["instrument"] = instrument
        del data["instrument_id"]

    application = update_test_application(application, **data)
    return 200, serialize_test_application(application)


@router.post("/applications/{application_id}/process", response={200: TestApplicationOut, 400: MessageOut, 403: MessageOut, 404: MessageOut}, auth=bearer_auth)
def process_test_application_endpoint(request, application_id: int) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para processar aplicações de teste."}

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    result = TestScoringService.process(application)
    if not result["ok"]:
        return 400, {"message": "; ".join(result["errors"])}

    application.refresh_from_db()
    return 200, serialize_test_application(application)