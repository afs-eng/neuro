from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from apps.patients.models import Patient
from apps.evaluations.models import Evaluation
from apps.tests.models.instruments import Instrument
from apps.tests.models.applications import TestApplication
from apps.tests.registry import get_test_module
from apps.tests.base.types import TestContext
from apps.tests.bpa2.interpreters import get_report_interpretation, get_synthesis


def test_list_view(request):
    return render(request, "tests/list.html")


def add_test_to_evaluation(request, evaluation_id, instrument_code):
    evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
    instrument = get_object_or_404(Instrument, code=instrument_code, is_active=True)

    app, created = TestApplication.objects.get_or_create(
        evaluation=evaluation,
        instrument=instrument,
        defaults={"applied_on": date.today()},
    )

    if instrument_code == "bpa2":
        return redirect("tests:bpa2", application_id=app.pk)

    return redirect("evaluations:detail", pk=evaluation_id)


def bpa2_form_view(request, application_id=None):
    patients = Patient.objects.all()
    application = None
    evaluation = None

    if application_id:
        application = get_object_or_404(
            TestApplication.objects.select_related(
                "evaluation", "evaluation__patient", "instrument"
            ),
            pk=application_id,
        )
        evaluation = application.evaluation
        patients = Patient.objects.filter(pk=evaluation.patient.pk)

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        evaluation_date = request.POST.get("evaluation_date")
        norm_type = request.POST.get("norm_type", "idade")

        patient = get_object_or_404(Patient, pk=patient_id)

        existing_eval = Evaluation.objects.filter(
            patient=patient,
            test_applications__instrument__code="bpa2",
            test_applications__is_validated=True,
        ).first()

        if existing_eval and not application:
            existing_app = existing_eval.test_applications.filter(
                instrument__code="bpa2", is_validated=True
            ).first()
            return render(
                request,
                "tests/bpa2_form.html",
                {
                    "patients": patients,
                    "errors": [
                        f"Paciente já possui BPA-2 aplicado em {existing_app.applied_on.strftime('%d/%m/%Y')}. Avaliação #{existing_eval.pk}."
                    ],
                    "evaluation": evaluation,
                    "application": application,
                    "existing_app": existing_app,
                },
            )

        raw_scores = {
            "ac": {
                "brutos": int(request.POST.get("ac_brutos", 0)),
                "erros": int(request.POST.get("ac_erros", 0)),
                "omissoes": int(request.POST.get("ac_omissoes", 0)),
            },
            "ad": {
                "brutos": int(request.POST.get("ad_brutos", 0)),
                "erros": int(request.POST.get("ad_erros", 0)),
                "omissoes": int(request.POST.get("ad_omissoes", 0)),
            },
            "aa": {
                "brutos": int(request.POST.get("aa_brutos", 0)),
                "erros": int(request.POST.get("aa_erros", 0)),
                "omissoes": int(request.POST.get("aa_omissoes", 0)),
            },
        }

        ctx = TestContext(
            patient_name=patient.full_name,
            evaluation_id=evaluation.pk if evaluation else 0,
            instrument_code="bpa2",
            raw_scores=raw_scores,
        )

        module = get_test_module("bpa2")
        errors = module.validate(ctx)

        if errors:
            return render(
                request,
                "tests/bpa2_form.html",
                {
                    "patients": patients,
                    "errors": errors,
                    "evaluation": evaluation,
                    "application": application,
                },
            )

        computed = module.compute(ctx)
        faixa = _get_age_group(patient, evaluation_date, norm_type)
        classified = module.classify(computed, faixa=faixa)
        classified["faixa"] = faixa
        classified["norm_type"] = norm_type
        interpretation = module.interpret(ctx, classified)

        if not evaluation:
            evaluation, _ = Evaluation.objects.get_or_create(
                patient=patient,
                status="collecting_data",
                defaults={
                    "referral_reason": "Avaliação neuropsicológica",
                },
            )

        instrument = Instrument.objects.get(code="bpa2")
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

        context = {
            "patient": patient,
            "evaluation": evaluation,
            "application": application,
            "evaluation_date": evaluation_date,
            "norm_type": norm_type,
            "faixa": faixa,
            "classified": classified,
            "interpretation": interpretation,
            "raw_scores": raw_scores,
        }
        return render(request, "tests/bpa2_result.html", context)

    context = {
        "patients": patients,
        "evaluation": evaluation,
        "application": application,
    }
    return render(request, "tests/bpa2_form.html", context)


def test_result_view(request, application_id):
    application = get_object_or_404(
        TestApplication.objects.select_related(
            "evaluation", "evaluation__patient", "instrument"
        ),
        pk=application_id,
    )

    classified = application.classified_payload or {}
    raw_scores = application.raw_payload or {}

    context = {
        "patient": application.evaluation.patient,
        "evaluation": application.evaluation,
        "application": application,
        "evaluation_date": application.applied_on,
        "classified": classified,
        "interpretation": application.interpretation_text or "",
        "raw_scores": raw_scores,
    }

    if application.instrument.code == "bpa2":
        return render(request, "tests/bpa2_result.html", context)

    return render(request, "tests/generic_result.html", context)


def wisc4_form_view(request, application_id=None):
    patients = Patient.objects.all()
    if request.method == "POST":
        return redirect("tests:wisc4")
    return render(request, "tests/wisc4_form.html", {"patients": patients})


def bpa2_report_view(request, application_id):
    application = get_object_or_404(
        TestApplication.objects.select_related(
            "evaluation", "evaluation__patient", "instrument", "evaluation__examiner"
        ),
        pk=application_id,
    )

    patient = application.evaluation.patient
    classified = application.classified_payload or {}
    raw_scores = application.raw_payload or {}

    subtestes = []
    for st in classified.get("subtestes", []):
        code = st.get("codigo", "")
        classificacao = st.get("classificacao", "")

        badge_class = "badge-media"
        if "Superior" in classificacao and "Média" not in classificacao:
            badge_class = "badge-superior"
        elif "Média Superior" in classificacao:
            badge_class = "badge-media-sup"
        elif classificacao == "Média":
            badge_class = "badge-media"
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
    ag_classificacao = ag_st.get("classificacao", "Média")

    examiner = application.evaluation.examiner
    examiner_name = examiner.get_full_name() if examiner else "-"

    faixa = classified.get("faixa", "-")
    norm_type = classified.get("norm_type", "idade")

    if norm_type == "escolaridade":
        referencia_normativa = f"Percentis - 2022 - {faixa} de escolaridade - Brasil"
    else:
        referencia_normativa = f"Percentis - 2022 - {faixa} - Brasil"

    context = {
        "patient": patient,
        "evaluation": application.evaluation,
        "application": application,
        "evaluation_date": application.applied_on,
        "faixa": faixa,
        "referencia_normativa": referencia_normativa,
        "subtestes": subtestes,
        "ag_classificacao": ag_classificacao,
        "sintese_atencional": get_synthesis(ag_classificacao),
        "examiner_name": examiner_name,
        "raw_scores": raw_scores,
    }

    return render(request, "tests/bpa2_report.html", context)


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
