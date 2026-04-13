from ninja import Router, Query
from ninja.errors import HttpError

from apps.api.auth import bearer_auth
from apps.accounts.models import UserRole
from apps.evaluations.models import Evaluation
from apps.tests.models import Instrument
from apps.tests.age_rules import get_instrument_age_rule
from apps.tests.api.schemas import (
    EPQJSubmitIn,
    RAVLTSubmitIn,
    SRS2SubmitIn,
    SCAREDSubmitIn,
)
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
from datetime import date as date_cls
from dateutil.relativedelta import relativedelta


def get_reference_date(evaluation, applied_on=None):
    return (
        applied_on or evaluation.start_date or evaluation.end_date or date_cls.today()
    )


def calcAge(birth_date, reference_date=None):
    base_date = reference_date or date_cls.today()
    return relativedelta(base_date, birth_date).years


def get_faixa_wisc(age):
    if 6 <= age <= 7:
        return "6-7 anos"
    elif 8 <= age <= 9:
        return "8-9 anos"
    elif 10 <= age <= 11:
        return "10-11 anos"
    elif 12 <= age <= 13:
        return "12-13 anos"
    elif 14 <= age <= 15:
        return "14-15 anos"
    elif age == 16:
        return "16 anos"
    return "6-7 anos"


def validate_instrument_age(evaluation, instrument):
    patient = evaluation.patient
    if not patient or not patient.birth_date:
        return None

    rules = get_instrument_age_rule(instrument.code)
    if not rules:
        return None

    age = calcAge(patient.birth_date, get_reference_date(evaluation))
    min_age = rules.get("min_age")
    max_age = rules.get("max_age")

    if min_age is not None and age < min_age:
        return rules["message"]
    if max_age is not None and age > max_age:
        return rules["message"]
    return None


from .schemas import (
    FDTSubmitIn,
    BPA2SubmitIn,
    EBADEPIJSubmitIn,
    EBADEPASubmitIn,
    ETDAHADSubmitIn,
    ETDAHPAISSubmitIn,
    InstrumentOut,
    InstrumentCreateIn,
    InstrumentUpdateIn,
    TestApplicationOut,
    TestApplicationCreateIn,
    TestApplicationUpdateIn,
    MessageOut,
    WISC4SubmitIn,
    SCAREDSubmitIn,
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
    age_rule = get_instrument_age_rule(instrument.code) or {}
    return {
        "id": instrument.id,
        "code": instrument.code,
        "name": instrument.name,
        "category": instrument.category,
        "version": instrument.version,
        "is_active": instrument.is_active,
        "min_age": age_rule.get("min_age"),
        "max_age": age_rule.get("max_age"),
        "age_message": age_rule.get("message", ""),
    }


def serialize_test_application(application):
    patient = application.evaluation.patient if application.evaluation else None
    return {
        "id": application.id,
        "evaluation_id": application.evaluation_id,
        "patient_name": patient.full_name if patient else None,
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


@router.get("/instruments", response=list[InstrumentOut], auth=bearer_auth)
def list_instruments(request) -> list[dict]:
    # Auto-seed essencial após reset de banco
    required = [
        {
            "code": "scared",
            "name": "SCARED - Screen for Child Anxiety",
            "category": "Ansiedade",
        },
        {"code": "ravlt", "name": "RAVLT - Memória Auditiva", "category": "Memoria"},
        {
            "code": "srs2",
            "name": "SRS-2 - Escala de Responsividade Social",
            "category": "Social / Autismo",
        },
    ]
    for item in required:
        Instrument.objects.get_or_create(
            code=item["code"],
            defaults={
                "name": item["name"],
                "category": item["category"],
                "is_active": True,
            },
        )

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


@router.get("/applications", response=list[TestApplicationOut], auth=bearer_auth)
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
    "/applications",
    response={
        201: TestApplicationOut,
        400: MessageOut,
        403: MessageOut,
        404: MessageOut,
    },
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

    age_error = validate_instrument_age(evaluation, instrument)
    if age_error:
        return 400, {"message": age_error}

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
        age_error = validate_instrument_age(application.evaluation, instrument)
        if age_error:
            return 400, {"message": age_error}
        data["instrument"] = instrument
        del data["instrument_id"]

    application = update_test_application(application, **data)
    return 200, serialize_test_application(application)


@router.delete(
    "/applications/{application_id}",
    response={200: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def delete_test_application_endpoint(request, application_id: int) -> tuple[int, dict]:
    if not can_edit_tests(request.auth):
        return 403, {
            "message": "Você não tem permissão para remover aplicações de teste."
        }

    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    application.delete()
    return 200, {"message": "Teste removido com sucesso."}


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

    reference_date = get_reference_date(
        evaluation, getattr(payload, "applied_on", None)
    )

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
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
    "/ebadep-ij/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
@router.post(
    "/ebaped-ij/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_ij_submit(request, payload: EBADEPIJSubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.ebaped_ij import EBADEPIJModule
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
    for i in range(1, 28):
        key = f"item_{i:02d}"
        raw_scores[key] = getattr(payload, key, 0)

    module = EBADEPIJModule()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="ebadep_ij",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(
        code__in=["ebadep_ij", "ebaped_ij"], is_active=True
    ).first()
    if not instrument:
        return 404, {"message": "Instrumento EBADEP-IJ não encontrado."}

    reference_date = get_reference_date(evaluation, payload.applied_on)

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
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
    "/ebadep-ij/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
@router.get(
    "/ebaped-ij/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def ebadep_ij_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}
    if application.instrument.code not in {"ebadep_ij", "ebaped_ij"}:
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


# --- FDT ---


@router.post(
    "/fdt/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def fdt_submit(request, payload: FDTSubmitIn) -> tuple[int, dict]:
    from apps.tests.base.types import TestContext
    from apps.tests.fdt import FDTModule
    from apps.tests.models.applications import TestApplication
    from apps.tests.models.instruments import Instrument

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = evaluation.patient
    if not patient.birth_date:
        return 400, {"message": "Paciente não tem data de nascimento."}

    reference_date = get_reference_date(evaluation, payload.applied_on)
    age = calcAge(patient.birth_date, reference_date)
    raw_scores = {
        "leitura": {"tempo": payload.leitura.tempo, "erros": payload.leitura.erros},
        "contagem": {"tempo": payload.contagem.tempo, "erros": payload.contagem.erros},
        "escolha": {"tempo": payload.escolha.tempo, "erros": payload.escolha.erros},
        "alternancia": {
            "tempo": payload.alternancia.tempo,
            "erros": payload.alternancia.erros,
        },
    }

    module = FDTModule()
    ctx = TestContext(
        patient_name=patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="fdt",
        raw_scores=raw_scores,
        reviewed_scores={"age": age},
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, classified)

    instrument = Instrument.objects.filter(code="fdt", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento FDT não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.pk,
        "faixa": classified.get("faixa", ""),
        "idade": classified.get("idade", age),
        "metric_results": classified.get("metric_results", []),
        "derived_scores": classified.get("derived_scores", {}),
        "interpretation": interpretation,
    }


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
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication

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
            eval_date = get_reference_date(evaluation, payload.applied_on)
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

    reference_date = get_reference_date(evaluation, payload.applied_on)

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
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


# --- WISC-IV ---


@router.post(
    "/wisc4/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def wisc4_submit(request, payload: WISC4SubmitIn) -> tuple[int, dict]:
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from datetime import timedelta

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = evaluation.patient
    if not patient.birth_date:
        return 400, {"message": "Paciente não tem data de nascimento."}

    reference_date = get_reference_date(evaluation, payload.applied_on)
    age = calcAge(patient.birth_date, reference_date)

    # WISC-IV é indicado para pacientes de 6 anos até 16 anos e 11 meses
    today = reference_date
    max_age_date = patient.birth_date + timedelta(
        days=16 * 365 + 364
    )  # 16 anos e 364 dias
    min_age_date = patient.birth_date + timedelta(days=6 * 365)  # 6 anos

    if today < min_age_date:
        return 400, {"message": "WISC-IV é indicado para pacientes a partir de 6 anos."}
    if today > max_age_date:
        return 400, {
            "message": "WISC-IV é indicado para pacientes de até 16 anos e 11 meses."
        }
    raw_scores = {
        "cubos": int(payload.cb) if payload.cb else 0,
        "semelhancas": int(payload.sm) if payload.sm else 0,
        "digitos": int(payload.dg) if payload.dg else 0,
        "conceitos": int(payload.cn) if payload.cn else 0,
        "codigos": int(payload.cd) if payload.cd else 0,
        "vocabulario": int(payload.vc) if payload.vc else 0,
        "sequencias": int(payload.snl) if payload.snl else 0,
        "matricial": int(payload.rm) if payload.rm else 0,
        "compreensao": int(payload.co) if payload.co else 0,
        "procura_simbolos": int(payload.ps) if payload.ps else 0,
        "cf": int(payload.cf) if payload.cf else 0,
        "ca": int(payload.ca) if payload.ca else 0,
        "in": int(payload.in_) if payload.in_ else 0,
        "rp": int(payload.rp) if payload.rp else 0,
    }

    faixa = get_faixa_wisc(age)

    from apps.tests.wisc4 import WISC4Module
    from apps.tests.base.types import TestContext

    reviewed_scores = {
        "birth_date": str(patient.birth_date),
        "evaluation_date": str(reference_date),
        "confidence_level": "95",
    }

    ctx = TestContext(
        patient_name=patient.full_name,
        evaluation_id=evaluation.id,
        instrument_code="wisc4",
        raw_scores=raw_scores,
        reviewed_scores=reviewed_scores,
    )

    wisc_module = WISC4Module()
    computed = wisc_module.compute(ctx)
    classified = wisc_module.classify(computed, faixa="95")
    interpretation = wisc_module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="wisc4", is_active=True).first()
    if not instrument:
        instrument = Instrument.objects.filter(code="WISC-IV", is_active=True).first()
    if not instrument:
        instrument = Instrument.objects.filter(code="WISC-4", is_active=True).first()
    if not instrument:
        instrument = Instrument.objects.filter(
            code__icontains="wisc", is_active=True
        ).first()

    if not instrument:
        return 404, {"message": "Instrumento WISC-IV não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.id,
        "age": age,
        "faixa": faixa,
        "scores": raw_scores,
        "classified": classified,
    }


# --- Generic Application Result ---


@router.get(
    "/applications/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def get_application_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "patient_birth_date": application.evaluation.patient.birth_date,
        "instrument_code": application.instrument.code,
        "instrument_name": application.instrument.name,
        "applied_on": application.applied_on,
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
        "interpretation_text": application.interpretation_text or "",
        "is_validated": application.is_validated,
    }


# --- EPQ-J ---


@router.post(
    "/epq-j/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def epq_j_submit(request, payload: EPQJSubmitIn) -> tuple[int, dict]:
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from apps.tests.epq_j.calculators import (
        calcular_escore,
        obter_percentil_e_classificacao,
    )
    from datetime import date as date_cls

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    instrument = Instrument.objects.filter(code="epq_j", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento EPQ-J não encontrado."}

    raw_scores = {}
    for i in range(1, 61):
        key = f"item_{i:02d}"
        raw_scores[key] = getattr(payload, key, 0) or 0

    escores = calcular_escore(raw_scores)
    resultados = obter_percentil_e_classificacao(
        escores["P"], escores["E"], escores["N"], escores["S"], payload.sexo
    )

    reference_date = get_reference_date(evaluation, payload.applied_on)

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = {
        "escore_bruto": escores,
        "resultados": resultados,
        "sexo": payload.sexo,
    }
    application.classified_payload = {
        "fatores": resultados,
        "sexo": payload.sexo,
    }
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.pk,
        "escore_bruto": escores,
        "resultados": resultados,
    }


# --- ETDAH-AD ---


@router.post(
    "/etdah-ad/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def etdah_ad_submit(request, payload: ETDAHADSubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.etdah_ad import ETDAHADModule
    from apps.tests.base.types import TestContext
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from apps.evaluations.models import Evaluation

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = evaluation.patient
    examiner = evaluation.examiner
    reference_date = get_reference_date(evaluation, payload.applied_on)

    responses = {}
    for i in range(1, 70):
        key = f"item_{i:02d}"
        responses[i] = getattr(payload, key, 0)

    raw_scores = {
        "patient_id": patient.pk,
        "examiner_id": examiner.pk if examiner else None,
        "age": calcAge(patient.birth_date, reference_date) if patient.birth_date else 0,
        "schooling": patient.schooling or "elementary",
        "responses": responses,
    }

    module = ETDAHADModule()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="etdah_ad",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="etdah_ad", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento ETDAH-AD não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    results = classified.get("results", {})

    return 200, {
        "application_id": application.pk,
        "raw_scores": classified.get("raw_scores", {}),
        "results": results,
        "interpretation": interpretation,
    }


@router.get(
    "/etdah-ad/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def etdah_ad_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "etdah_ad":
        return 404, {"message": "Aplicação não é do tipo ETDAH-AD."}

    classified = application.classified_payload or {}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "raw_scores": classified.get("raw_scores", {}),
        "results": classified.get("results", {}),
        "interpretation": application.interpretation_text or "",
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
    }


# --- ETDAH-PAIS ---


@router.post(
    "/etdah-pais/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def etdah_pais_submit(request, payload: ETDAHPAISSubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.etdah_pais import ETDAHPAISModule
    from apps.tests.base.types import TestContext
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from apps.evaluations.models import Evaluation

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = evaluation.patient
    examiner = evaluation.examiner
    reference_date = get_reference_date(evaluation, payload.applied_on)

    responses = {}
    for i in range(1, 59):
        key = f"item_{i:02d}"
        responses[i] = getattr(payload, key, 0)

    raw_scores = {
        "patient_id": patient.pk,
        "examiner_id": examiner.pk if examiner else None,
        "age": calcAge(patient.birth_date, reference_date) if patient.birth_date else 0,
        "sex": payload.sex,
        "schooling": patient.schooling or "elementary",
        "responses": responses,
    }

    module = ETDAHPAISModule()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="etdah_pais",
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="etdah_pais", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento ETDAH-PAIS não encontrado."}

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    results = classified.get("results", {})

    return 200, {
        "application_id": application.pk,
        "raw_scores": classified.get("raw_scores", {}),
        "results": results,
        "interpretation": interpretation,
    }


@router.get(
    "/etdah-pais/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def etdah_pais_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "etdah_pais":
        return 404, {"message": "Aplicação não é do tipo ETDAH-PAIS."}

    classified = application.classified_payload or {}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "raw_scores": classified.get("raw_scores", {}),
        "results": classified.get("results", {}),
        "interpretation": application.interpretation_text or "",
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
    }


# --- RAVLT ---


@router.post(
    "/ravlt/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def ravlt_submit(request, payload: RAVLTSubmitIn) -> tuple[int, dict]:
    from datetime import date as date_cls
    from apps.tests.ravlt import RAVLTModule
    from apps.tests.base.types import TestContext
    from apps.tests.models.instruments import Instrument
    from apps.tests.models.applications import TestApplication
    from apps.evaluations.models import Evaluation

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = evaluation.patient
    examiner = evaluation.examiner
    reference_date = get_reference_date(evaluation, payload.applied_on)

    raw_scores = {
        "a1": int(payload.a1 or 0),
        "a2": int(payload.a2 or 0),
        "a3": int(payload.a3 or 0),
        "a4": int(payload.a4 or 0),
        "a5": int(payload.a5 or 0),
        "b": int(payload.b or 0),
        "a6": int(payload.a6 or 0),
        "a7": int(payload.a7 or 0),
        "reconhecimento": int(payload.reconhecimento or 0),
    }

    idade = 25
    try:
        if patient.birth_date and reference_date:
            anos = reference_date.year - patient.birth_date.year
            if (reference_date.month, reference_date.day) < (
                patient.birth_date.month,
                patient.birth_date.day,
            ):
                anos -= 1
            if anos > 0:
                idade = anos
    except Exception:
        idade = 25

    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="ravlt",
        raw_scores=raw_scores,
        patient_age=idade,
    )

    module = RAVLTModule()
    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed, idade=idade)
    interpretation = module.interpret(ctx, {**computed, **classified})

    instrument = Instrument.objects.filter(code="ravlt", is_active=True).first()
    if not instrument:
        instrument = Instrument.objects.create(
            name="RAVLT",
            code="ravlt",
            is_active=True,
        )

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.id,
        "computed": computed,
        "classified": classified,
        "interpretation": interpretation,
    }


@router.get(
    "/ravlt/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def ravlt_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "ravlt":
        return 404, {"message": "Aplicação não é do tipo RAVLT."}

    classified = application.classified_payload or {}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "results": classified,
        "interpretation": application.interpretation_text or "",
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
    }


@router.get(
    "/srs2/items",
    response={200: dict},
    # auth=bearer_auth,  # Temporarily disabled for testing
)
def srs2_get_items(request) -> tuple[int, dict]:
    import json
    import os

    items_file = os.path.join(os.path.dirname(__file__), "..", "srs2", "items.json")
    with open(items_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    forms = [
        "pre_escola",
        "idade_escolar",
        "adulto_autorrelato",
        "adulto_heterorrelato",
    ]
    result = {}
    for form in forms:
        items = data.get(form, [])
        result[form] = [
            {"item": i["item"], "fator": i["fator"], "pergunta": i.get("pergunta", "")}
            for i in items
        ]

    return 200, result


@router.post(
    "/srs2/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def srs2_submit(request, payload: SRS2SubmitIn) -> tuple[int, dict]:
    from apps.tests.srs2 import SRS2Module
    from apps.tests.base.types import TestContext
    from apps.tests.models.applications import TestApplication

    if not can_edit_tests(request.auth):
        return 403, {"message": "Você não tem permissão para submeter testes."}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    raw_scores = {
        "form": payload.form,
        "gender": payload.gender,
        "age": payload.age,
        "respondent_name": payload.respondent_name,
        "responses": payload.responses or {},
    }

    patient = evaluation.patient
    age = payload.age
    if not age and patient.birth_date:
        eval_date = get_reference_date(evaluation, payload.applied_on)
        age = eval_date.year - patient.birth_date.year
        if (eval_date.month, eval_date.day) < (
            patient.birth_date.month,
            patient.birth_date.day,
        ):
            age -= 1

    module = SRS2Module()
    ctx = TestContext(
        patient_name=evaluation.patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="srs2",
        patient_age=age or 10,
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed, age=age or 10, gender=payload.gender or "M")
    interpretation = module.interpret(ctx, classified)

    instrument = Instrument.objects.filter(code="srs2", is_active=True).first()
    if not instrument:
        return 404, {"message": "Instrumento SRS-2 não encontrado."}

    reference_date = get_reference_date(evaluation, payload.applied_on)

    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.pk,
        "computed": computed,
        "classified": classified,
        "interpretation": interpretation,
    }


@router.get(
    "/srs2/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def srs2_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "srs2":
        return 404, {"message": "Aplicação não é do tipo SRS-2."}

    classified = application.classified_payload or {}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "results": classified,
        "interpretation": application.interpretation_text or "",
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
    }


# --- SCARED ---


@router.post(
    "/scared/submit",
    response={200: dict, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def scared_submit(request, payload: SCAREDSubmitIn) -> tuple[int, dict]:
    from apps.tests.scared import SCAREDModule
    from apps.tests.base.types import TestContext
    from apps.tests.models.applications import TestApplication

    if not can_view_tests(request.auth):
        return 403, {"message": "User not authorized"}

    evaluation = Evaluation.objects.filter(id=payload.evaluation_id).first()
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    raw_scores = {
        "form": payload.form,
        "gender": payload.gender,
        "age": payload.age,
        "responses": payload.responses or {},
    }

    patient = evaluation.patient
    idade = payload.age
    if not idade and patient.birth_date:
        reference_date = get_reference_date(evaluation, payload.applied_on)
        idade = calcAge(patient.birth_date, reference_date)

    module = SCAREDModule()
    ctx = TestContext(
        patient_name=patient.full_name,
        evaluation_id=evaluation.pk,
        instrument_code="scared",
        patient_age=idade or 10,
        raw_scores=raw_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return 400, {"message": "; ".join(errors)}

    computed = module.compute(ctx)
    classified = module.classify(computed, idade=idade or 10)
    interpretation = module.interpret(ctx, classified)

    instrument = Instrument.objects.filter(code="scared", is_active=True).first()
    if not instrument:
        instrument = Instrument.objects.create(
            name="SCARED",
            code="scared",
            is_active=True,
        )

    reference_date = get_reference_date(evaluation, payload.applied_on)
    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": reference_date},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = reference_date
    application.save()

    return 200, {
        "application_id": application.pk,
        "computed": computed,
        "classified": classified,
        "interpretation": interpretation,
    }


@router.get(
    "/scared/result/{application_id}",
    response={200: dict, 404: MessageOut},
    auth=bearer_auth,
)
def scared_result(request, application_id: int) -> tuple[int, dict]:
    application = get_test_application_by_id(application_id)
    if not application:
        return 404, {"message": "Aplicação de teste não encontrada."}

    if application.instrument.code != "scared":
        return 404, {"message": "Aplicação não é do tipo SCARED."}

    classified = application.classified_payload or {}

    return 200, {
        "application_id": application.pk,
        "evaluation_id": application.evaluation_id,
        "patient_name": application.evaluation.patient.full_name,
        "applied_on": application.applied_on,
        "results": classified,
        "interpretation": application.interpretation_text or "",
        "raw_payload": application.raw_payload or {},
        "computed_payload": application.computed_payload or {},
        "classified_payload": application.classified_payload or {},
    }
