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
    BPA2SubmitIn,
    EBADEPIJSubmitIn,
    EBADEPASubmitIn,
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


@router.post(
    "/instruments/", response={201: InstrumentOut, 403: MessageOut}, auth=bearer_auth
)
def create_instrument_endpoint(
    request, payload: InstrumentCreateIn
) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para criar instrumentos."}

    instrument = Instrument.objects.create(**payload.dict())
    return 201, serialize_instrument(instrument)


@router.patch(
    "/instruments/{instrument_id}",
    response={200: InstrumentOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_instrument_endpoint(
    request, instrument_id: int, payload: InstrumentUpdateIn
) -> tuple[int, dict]:
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
def list_test_applications(
    request, evaluation_id: int | None = Query(default=None)
) -> list[dict]:
    if not can_view_tests(request.auth):
        raise HttpError(
            403, "Você não tem permissão para visualizar aplicações de teste."
        )

    applications = (
        get_test_applications_by_evaluation(evaluation_id)
        if evaluation_id
        else get_test_applications()
    )
    return [serialize_test_application(item) for item in applications]


@router.get(
    "/applications/{application_id}",
    response={200: TestApplicationOut, 404: MessageOut},
    auth=bearer_auth,
)
def get_test_application_endpoint(request, application_id: int) -> tuple[int, dict]:
    if not can_view_tests(request.auth):
        raise HttpError(
            403, "Você não tem permissão para visualizar aplicações de teste."
        )

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    return 200, serialize_test_application(application)


@router.post(
    "/applications/",
    response={201: TestApplicationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def create_test_application_endpoint(
    request, payload: TestApplicationCreateIn
) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {
            "message": "Você não tem permissão para criar aplicações de teste."
        }

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    instrument = Instrument.objects.filter(
        id=payload.instrument_id, is_active=True
    ).first()
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


@router.patch(
    "/applications/{application_id}",
    response={200: TestApplicationOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_test_application_endpoint(
    request, application_id: int, payload: TestApplicationUpdateIn
) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {
            "message": "Você não tem permissão para editar aplicações de teste."
        }

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
        instrument = Instrument.objects.filter(
            id=data["instrument_id"], is_active=True
        ).first()
        if not instrument:
            return 404, {"message": "Instrumento não encontrado."}
        data["instrument"] = instrument
        del data["instrument_id"]

    application = update_test_application(application, **data)
    return 200, serialize_test_application(application)


@router.post(
    "/applications/{application_id}/process",
    response={
        200: TestApplicationOut,
        400: MessageOut,
        403: MessageOut,
        404: MessageOut,
    },
    auth=bearer_auth,
)
def process_test_application_endpoint(request, application_id: int) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {
            "message": "Você não tem permissão para processar aplicações de teste."
        }

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    result = TestScoringService.process(application)
    if not result["ok"]:
        return 400, {"message": "; ".join(result["errors"])}

    application.refresh_from_db()
    return 200, serialize_test_application(application)


@router.post(
    "/ebadep-a/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_a_submit(request, payload: EBADEPASubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.ebadep_a import EBADEPAModule
    from apps.tests.base.types import TestContext
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from apps.evaluations.models import Evaluation

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    raw_scores = {}
    for i in range(1, 46):
        key = f"item_{i:02d}"
        raw_scores[key] = getattr(payload, key, 0)

    module = EBADEPAModule()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="ebadep_a",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="ebadep_a", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento EBADEP-A não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": payload.applied_on or date_cls.today()},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = payload.applied_on or date_cls.today()
    application.save()

    items_criticos = classified.get("items_criticos", [])

    return 200, {
        "application_id": application.pk,
        "escore_total": classified.get("escore_total", 0),
        "percentil": classified.get("percentil", 0),
        "classificacao": classified.get("classificacao", ""),
        "sintese": classified.get("sintese", ""),
        "items_criticos": [d.get("item") for d in items_criticos],
        "interpretation": interpretation,
    }


@router.get(
    "/ebadep-a/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_a_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "ebadep_a":
        return 404, {"message": "Aplicação não é do tipo EBADEP-A."}

    classified = application.classified_payload or {}
    items_criticos = classified.get("items_criticos", [])

    return 200, {
        "application_id": application.pk,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "escore_total": classified.get("escore_total", 0),
        "percentil": classified.get("percentil", 0),
        "classificacao": classified.get("classificacao", ""),
        "sintese": classified.get("sintese", ""),
        "items_criticos": [d.get("item") for d in items_criticos],
        "detalhe_itens": classified.get("result", {}).get("detalhe_itens", []),
        "interpretation": application.interpretation_text or "",
    }


# --- EBADEP-IJ ---


@router.post(
    "/ebaped-ij/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_ij_submit(request, payload: EBADEPIJSubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.ebaped_ij import EBADEPIJModule
    from apps.tests.base.types import TestContext

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    raw_scores = {}
    for i in range(1, 28):
        key = f"item_{i:02d}"
        raw_scores[key] = getattr(payload, key, 0)

    module = EBADEPIJModule()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="ebaped_ij",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="ebaped_ij", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento EBADEP-IJ não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": payload.applied_on or date_cls.today()},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = payload.applied_on or date_cls.today()
    application.save()

    return 200, {
        "application_id": application.pk,
        "pontuacao_total": classified.get("pontuacao_total", 0),
        "classificacao": classified.get("classificacao", ""),
        "sintese": classified.get("sintese", ""),
        "normas": classified.get("normas"),
        "interpretation": interpretation,
    }


@router.get(
    "/ebaped-ij/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_ij_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}
    if application.instrument.code != "ebaped_ij":
        return 404, {"message": "Aplicação não é do tipo EBADEP-IJ."}

    classified = application.classified_payload or {}
    return 200, {
        "application_id": application.pk,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "pontuacao_total": classified.get("pontuacao_total", 0),
        "classificacao": classified.get("classificacao", ""),
        "sintese": classified.get("sintese", ""),
        "normas": classified.get("normas"),
        "items_criticos": [d.get("item") for d in classified.get("items_criticos", [])],
        "detalhe_itens": classified.get("result", {}).get("detalhe_itens", []),
        "interpretation": application.interpretation_text or "",
    }


# --- BPA-2 ---


@router.post(
    "/bpa2/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def bpa2_submit(request, payload: BPA2SubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.bpa2 import BPA2Module
    from apps.tests.base.types import TestContext
    from apps.tests.bpa2.calculators import get_age_group

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    raw_scores = {
        "ac": {
            "brutos": payload.ac.brutos,
            "erros": payload.ac.erros,
            "omissoes": payload.ac.omissoes,
        },
        "ad": {
            "brutos": payload.ad.brutos,
            "erros": payload.ad.erros,
            "omissoes": payload.ad.omissoes,
        },
        "aa": {
            "brutos": payload.aa.brutos,
            "erros": payload.aa.erros,
            "omissoes": payload.aa.omissoes,
        },
    }

    module = BPA2Module()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="bpa2",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    patient = evaluation.patient
    norm_type = payload.norm_type or "idade"

    if norm_type == "escolaridade":
        faixa = patient.schooling or "5 anos"
    else:
        if not patient.birth_date:
            faixa = "15-17 anos"
        else:
            eval_date = payload.applied_on or date_cls.today()
            age = eval_date.year - patient.birth_date.year
            if (eval_date.month, eval_date.day) < (
                patient.birth_date.month,
                patient.birth_date.day,
            ):
                age -= 1
            faixa = get_age_group(age)

    computed = module.compute(ctx)
    classified = module.classify(computed, faixa=faixa)
    classified["faixa"] = faixa
    classified["norm_type"] = norm_type
    interpretation = module.interpret(ctx, classified)

    instrument = Instrument.objects.filter(code="bpa2", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento BPA-2 não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": payload.applied_on or date_cls.today()},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = payload.applied_on or date_cls.today()
    application.save()

    ag = next(
        (s for s in classified.get("subtestes", []) if s.get("codigo") == "ag"), {}
    )

    return 200, {
        "application_id": application.pk,
        "subtestes": classified.get("subtestes", []),
        "pontos_fortes": classified.get("pontos_fortes", []),
        "pontos_fragilizados": classified.get("pontos_fragilizados", []),
        "faixa": faixa,
        "norm_type": norm_type,
        "ag_classificacao": ag.get("classificacao", ""),
        "interpretation": interpretation,
    }


@router.get(
    "/bpa2/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def bpa2_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}
    if application.instrument.code != "bpa2":
        return 404, {"message": "Aplicação não é do tipo BPA-2."}

    classified = application.classified_payload or {}
    ag = next(
        (s for s in classified.get("subtestes", []) if s.get("codigo") == "ag"), {}
    )

    return 200, {
        "application_id": application.pk,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "subtestes": classified.get("subtestes", []),
        "pontos_fortes": classified.get("pontos_fortes", []),
        "pontos_fragilizados": classified.get("pontos_fragilizados", []),
        "faixa": classified.get("faixa", ""),
        "norm_type": classified.get("norm_type", ""),
        "ag_classificacao": ag.get("classificacao", ""),
        "interpretation": application.interpretation_text or "",
    }
