from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from apps.patients.models import Patient
from apps.evaluations.models import Evaluation
from apps.tests.models.instruments import Instrument
from apps.tests.models.applications import TestApplication
from apps.tests.registry import get_test_module
from apps.tests.base.types import TestContext
from apps.tests.bpa2.interpreters import get_report_interpretation, get_synthesis


def _get_application(application_id):
    return get_object_or_404(
        TestApplication.objects.select_related(
            "evaluation", "evaluation__patient", "instrument"
        ),
        pk=application_id,
    )


def _get_existing_application(patient, instrument_code):
    existing_eval = Evaluation.objects.filter(
        patient=patient,
        test_applications__instrument__code=instrument_code,
        test_applications__is_validated=True,
    ).first()
    if existing_eval:
        return existing_eval.test_applications.filter(
            instrument__code=instrument_code, is_validated=True
        ).first(), existing_eval
    return None, None


def _process_and_save_test(
    patient,
    evaluation,
    instrument_code,
    raw_scores,
    evaluation_date,
    extra_classify_kwargs=None,
):
    module = get_test_module(instrument_code)
    reviewed_scores = {}
    if hasattr(patient, "birth_date") and patient.birth_date:
        reviewed_scores["birth_date"] = str(patient.birth_date)
    if evaluation_date:
        reviewed_scores["evaluation_date"] = str(evaluation_date)
    ctx = TestContext(
        patient_name=patient.full_name,
        evaluation_id=evaluation.pk if evaluation else 0,
        instrument_code=instrument_code,
        raw_scores=raw_scores,
        reviewed_scores=reviewed_scores,
    )

    errors = module.validate(ctx)
    if errors:
        return None, errors

    computed = module.compute(ctx)
    if extra_classify_kwargs:
        classified = module.classify(computed, **extra_classify_kwargs)
    else:
        classified = module.classify(computed)
    interpretation = module.interpret(ctx, {**computed, **classified})

    if not evaluation:
        evaluation, _ = Evaluation.objects.get_or_create(
            patient=patient,
            status="collecting_data",
            defaults={"referral_reason": "Avaliação neuropsicológica"},
        )

    instrument = Instrument.objects.get(code=instrument_code)
    application, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": evaluation_date or date.today()},
    )

    application.raw_payload = raw_scores
    application.computed_payload = computed
    application.classified_payload = classified
    application.interpretation_text = interpretation
    application.is_validated = True
    application.applied_on = evaluation_date or date.today()
    application.save()

    return application, classified, interpretation


def test_list_view(request):
    return render(request, "tests/list.html")


def apply_test_for_patient(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    return render(request, "tests/apply_for_patient.html", {"patient": patient})


def add_test_to_evaluation(request, evaluation_id, instrument_code):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    instrument = get_object_or_404(Instrument, code=instrument_code, is_active=True)

    app, _ = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": date.today()},
    )

    return redirect(f"tests:{instrument_code}", application_id=app.pk)


def test_result_view(request, application_id):
    application = _get_application(application_id)
    classified = application.classified_payload or {}
    context = {
        "patient": application.evaluation.patient,
        "evaluation": application.evaluation,
        "application": application,
        "evaluation_date": application.applied_on,
        "classified": classified,
        "interpretation": application.interpretation_text or "",
        "raw_scores": application.raw_payload or {},
    }
    return render(request, f"tests/{application.instrument.code}_result.html", context)


def _item_form_view(
    request, application_id, instrument_code, item_count, form_template
):
    patients = Patient.objects.all()
    application = None
    evaluation = None

    if application_id:
        application = _get_application(application_id)
        evaluation = application.evaluation
        patients = Patient.objects.filter(pk=evaluation.patient.pk)

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        evaluation_date = request.POST.get("evaluation_date")
        patient = get_object_or_404(Patient, pk=patient_id)

        existing_app, existing_eval = _get_existing_application(
            patient, instrument_code
        )
        if existing_app and not application:
            return render(
                request,
                form_template,
                {
                    "patients": patients,
                    "errors": [
                        f"Paciente já possui teste aplicado em {existing_app.applied_on.strftime('%d/%m/%Y')}."
                    ],
                    "evaluation": evaluation,
                    "application": application,
                    "existing_app": existing_app,
                },
            )

        raw_scores = {}
        for i in range(1, item_count + 1):
            key = f"item_{i:02d}"
            raw_value = request.POST.get(key)
            raw_scores[key] = (
                int(raw_value) if raw_value is not None and raw_value != "" else 0
            )

        result = _process_and_save_test(
            patient, evaluation, instrument_code, raw_scores, evaluation_date
        )
        if isinstance(result[1], list):
            return render(
                request,
                form_template,
                {
                    "patients": patients,
                    "errors": result[1],
                    "evaluation": evaluation,
                    "application": application,
                },
            )

        app_result, classified, interpretation = result
        return render(
            request,
            f"tests/{instrument_code}_result.html",
            {
                "patient": patient,
                "evaluation": evaluation,
                "application": app_result,
                "evaluation_date": evaluation_date,
                "classified": classified,
                "interpretation": interpretation,
                "raw_scores": raw_scores,
            },
        )

    existing_data = (
        application.raw_payload if application and application.raw_payload else None
    )
    return render(
        request,
        form_template,
        {
            "patients": patients,
            "evaluation": evaluation,
            "application": application,
            "existing_data": existing_data,
        },
    )


def ebadep_a_form_view(request, application_id=None):
    return _item_form_view(
        request, application_id, "ebadep_a", 45, "tests/ebadep_a_form.html"
    )


def ebaped_ij_form_view(request, application_id=None):
    return _item_form_view(
        request, application_id, "ebadep_ij", 27, "tests/ebaped_ij_form.html"
    )


def bpa2_form_view(request, application_id=None):
    patients = Patient.objects.all()
    application = None
    evaluation = None

    if application_id:
        application = _get_application(application_id)
        evaluation = application.evaluation
        patients = Patient.objects.filter(pk=evaluation.patient.pk)

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        evaluation_date = request.POST.get("evaluation_date")
        norm_type = request.POST.get("norm_type", "idade")
        patient = get_object_or_404(Patient, pk=patient_id)

        existing_app, existing_eval = _get_existing_application(patient, "bpa2")
        if existing_app and not application:
            return render(
                request,
                "tests/bpa2_form.html",
                {
                    "patients": patients,
                    "errors": [
                        f"Paciente já possui BPA-2 aplicado em {existing_app.applied_on.strftime('%d/%m/%Y')}."
                    ],
                    "evaluation": evaluation,
                    "application": application,
                    "existing_app": existing_app,
                },
            )

        raw_scores = {}
        for code in ["ac", "ad", "aa"]:
            raw_scores[code] = {
                "brutos": int(request.POST.get(f"{code}_brutos", 0)),
                "erros": int(request.POST.get(f"{code}_erros", 0)),
                "omissoes": int(request.POST.get(f"{code}_omissoes", 0)),
            }

        faixa = _get_age_group(patient, evaluation_date, norm_type)
        result = _process_and_save_test(
            patient,
            evaluation,
            "bpa2",
            raw_scores,
            evaluation_date,
            extra_classify_kwargs={"faixa": faixa},
        )
        if isinstance(result[1], list):
            return render(
                request,
                "tests/bpa2_form.html",
                {
                    "patients": patients,
                    "errors": result[1],
                    "evaluation": evaluation,
                    "application": application,
                },
            )

        app_result, classified, interpretation = result
        classified["faixa"] = faixa
        classified["norm_type"] = norm_type
        return render(
            request,
            "tests/bpa2_result.html",
            {
                "patient": patient,
                "evaluation": evaluation,
                "application": app_result,
                "evaluation_date": evaluation_date,
                "norm_type": norm_type,
                "faixa": faixa,
                "classified": classified,
                "interpretation": interpretation,
                "raw_scores": raw_scores,
            },
        )

    existing_data = (
        application.raw_payload if application and application.raw_payload else None
    )
    return render(
        request,
        "tests/bpa2_form.html",
        {
            "patients": patients,
            "evaluation": evaluation,
            "application": application,
            "existing_data": existing_data,
        },
    )


def wisc4_form_view(request, application_id=None):
    patients = Patient.objects.all()
    application = None
    evaluation = None

    if application_id:
        application = _get_application(application_id)
        evaluation = application.evaluation
        patients = Patient.objects.filter(pk=evaluation.patient.pk)

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        evaluation_date = request.POST.get("evaluation_date")
        patient = get_object_or_404(Patient, pk=patient_id)

        existing_app, existing_eval = _get_existing_application(patient, "wisc4")
        if existing_app and not application:
            return render(
                request,
                "tests/wisc4_form.html",
                {
                    "patients": patients,
                    "errors": [
                        f"Paciente já possui WISC-IV aplicado em {existing_app.applied_on.strftime('%d/%m/%Y')}."
                    ],
                    "evaluation": evaluation,
                    "application": application,
                    "existing_app": existing_app,
                },
            )

        raw_scores = {}
        subtest_codes = [
            "cubos",
            "semelhancas",
            "digitos",
            "conceitos",
            "codigos",
            "vocabulario",
            "sequencias",
            "matricial",
            "compreensao",
            "procura_simbolos",
        ]
        for code in subtest_codes:
            raw_value = request.POST.get(code)
            raw_scores[code] = (
                int(raw_value) if raw_value is not None and raw_value != "" else 0
            )

        from datetime import date as date_cls

        confidence_level = request.POST.get("confidence_level", "95")

        reviewed_scores = {
            "birth_date": str(patient.birth_date) if patient.birth_date else None,
            "evaluation_date": str(evaluation_date or date_cls.today()),
            "confidence_level": confidence_level,
        }

        result = _process_and_save_test(
            patient,
            evaluation,
            "wisc4",
            raw_scores,
            evaluation_date,
            extra_classify_kwargs={"faixa": confidence_level},
        )
        if isinstance(result[1], list):
            return render(
                request,
                "tests/wisc4_form.html",
                {
                    "patients": patients,
                    "errors": result[1],
                    "evaluation": evaluation,
                    "application": application,
                },
            )

        app_result, classified, interpretation = result
        return render(
            request,
            "tests/wisc4_result.html",
            {
                "patient": patient,
                "evaluation": evaluation,
                "application": app_result,
                "evaluation_date": evaluation_date,
                "classified": classified,
                "interpretation": interpretation,
                "raw_scores": raw_scores,
            },
        )

    existing_data = (
        application.raw_payload if application and application.raw_payload else None
    )
    return render(
        request,
        "tests/wisc4_form.html",
        {
            "patients": patients,
            "evaluation": evaluation,
            "application": application,
            "existing_data": existing_data,
        },
    )


def bpa2_report_view(request, application_id):
    application = _get_application(application_id)
    patient = application.evaluation.patient
    classified = application.classified_payload or {}

    subtestes = []
    for st in classified.get("subtestes", []):
        code = st.get("codigo", "")
        classificacao = st.get("classificacao", "")
        badge_class = "badge-media"
        if "Superior" in classificacao and "Média" not in classificacao:
            badge_class = "badge-superior"
        elif "Média Superior" in classificacao:
            badge_class = "badge-media-sup"
        elif "Média Inferior" in classificacao:
            badge_class = "badge-media-inf"
        elif "Inferior" in classificacao and "Muito" not in classificacao:
            badge_class = "badge-inferior"
        elif "Muito Inferior" in classificacao:
            badge_class = "badge-muito-inf"

        subtestes.append(
            {
                **st,
                "badge_class": badge_class,
                "interpretacao_completa": get_report_interpretation(
                    code, classificacao, patient.full_name
                ),
            }
        )

    ag_st = next(
        (s for s in classified.get("subtestes", []) if s.get("codigo") == "ag"), {}
    )
    examiner = application.evaluation.examiner
    faixa = classified.get("faixa", "-")
    norm_type = classified.get("norm_type", "idade")

    return render(
        request,
        "tests/bpa2_report.html",
        {
            "patient": patient,
            "evaluation": application.evaluation,
            "application": application,
            "evaluation_date": application.applied_on,
            "faixa": faixa,
            "referencia_normativa": f"Percentis - 2022 - {faixa}{' de escolaridade' if norm_type == 'escolaridade' else ''} - Brasil",
            "subtestes": subtestes,
            "ag_classificacao": ag_st.get("classificacao", "Média"),
            "sintese_atencional": get_synthesis(ag_st.get("classificacao", "Média")),
            "examiner_name": examiner.get_full_name() if examiner else "-",
            "raw_scores": application.raw_payload or {},
        },
    )


def ebaped_ij_report_view(request, application_id):
    application = _get_application(application_id)
    examiner = application.evaluation.examiner
    return render(
        request,
        "tests/ebaped_ij_report.html",
        {
            "patient": application.evaluation.patient,
            "evaluation": application.evaluation,
            "application": application,
            "evaluation_date": application.applied_on,
            "classified": application.classified_payload or {},
            "interpretation": application.interpretation_text or "",
            "examiner_name": examiner.get_full_name() if examiner else "-",
            "raw_scores": application.raw_payload or {},
        },
    )


def ebadep_a_report_view(request, application_id):
    application = _get_application(application_id)
    examiner = application.evaluation.examiner
    return render(
        request,
        "tests/ebadep_a_report.html",
        {
            "patient": application.evaluation.patient,
            "evaluation": application.evaluation,
            "application": application,
            "evaluation_date": application.applied_on,
            "classified": application.classified_payload or {},
            "interpretation_text": application.interpretation_text or "",
            "examiner_name": examiner.get_full_name() if examiner else "-",
            "raw_scores": application.raw_payload or {},
        },
    )


def _get_age_group(patient, evaluation_date_str, norm_type):
    from apps.tests.bpa2.calculators import get_age_group

    if norm_type == "escolaridade":
        return patient.schooling or "5 anos"

    if not patient.birth_date:
        return "15-17 anos"

    try:
        eval_date = date.fromisoformat(evaluation_date_str)
    except ValueError, TypeError:
        eval_date = date.today()

    age = eval_date.year - patient.birth_date.year
    if (eval_date.month, eval_date.day) < (
        patient.birth_date.month,
        patient.birth_date.day,
    ):
        age -= 1

    return get_age_group(age)
