from django.shortcuts import render, redirect, get_object_or_404
from apps.patients.models import Patient
from apps.evaluations.models import Evaluation
from apps.tests.models.instruments import Instrument
from apps.tests.models.applications import TestApplication


def evaluation_list_view(request):
    evaluations = Evaluation.objects.select_related("patient", "examiner").order_by(
        "-created_at"
    )
    return render(request, "evaluations/list.html", {"evaluations": evaluations})


def evaluation_create_view(request):
    patients = Patient.objects.all()

    if request.method == "POST":
        patient_id = request.POST.get("patient")
        referral_reason = request.POST.get("referral_reason", "")
        evaluation_purpose = request.POST.get("evaluation_purpose", "")

        patient = get_object_or_404(Patient, pk=patient_id)

        evaluation = Evaluation.objects.create(
            patient=patient,
            referral_reason=referral_reason,
            evaluation_purpose=evaluation_purpose,
            status="collecting_data",
        )

        return redirect("evaluations:detail", pk=evaluation.pk)

    return render(request, "evaluations/form.html", {"patients": patients})


def evaluation_detail_view(request, pk):
    evaluation = get_object_or_404(Evaluation.objects.select_related("patient"), pk=pk)
    applications = TestApplication.objects.filter(evaluation=evaluation).select_related(
        "instrument"
    )

    instruments = Instrument.objects.filter(is_active=True)

    applied_codes = applications.values_list("instrument__code", flat=True)
    available_instruments = instruments.exclude(code__in=applied_codes)

    context = {
        "evaluation": evaluation,
        "applications": applications,
        "available_instruments": available_instruments,
    }
    return render(request, "evaluations/detail.html", context)
