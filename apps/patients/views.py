from django.shortcuts import render, get_object_or_404, redirect
from apps.patients.models import Patient
from apps.evaluations.models import Evaluation


def dashboard_view(request):
    patients = Patient.objects.all()[:5]
    evaluations = Evaluation.objects.select_related("patient").order_by("-created_at")[
        :5
    ]

    context = {
        "total_patients": Patient.objects.count(),
        "active_evaluations": Evaluation.objects.filter(
            status__in=["draft", "collecting_data"]
        ).count(),
        "tests_applied": 0,
        "pending_reports": 0,
        "recent_patients": patients,
        "recent_evaluations": evaluations,
    }
    return render(request, "dashboard/index.html", context)


def patient_list_view(request):
    patients = Patient.objects.all()
    return render(request, "patients/list.html", {"patients": patients})


def patient_detail_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    from apps.tests.models.applications import TestApplication

    test_applications = (
        TestApplication.objects.filter(evaluation__patient=patient)
        .select_related("instrument", "evaluation")
        .order_by("-applied_on", "-created_at")
    )
    return render(
        request,
        "patients/detail.html",
        {
            "patient": patient,
            "test_applications": test_applications,
        },
    )


def patient_create_view(request):
    if request.method == "POST":
        Patient.objects.create(
            full_name=request.POST.get("full_name"),
            birth_date=request.POST.get("birth_date") or None,
            sex=request.POST.get("sex", ""),
            schooling=request.POST.get("schooling", ""),
            school_name=request.POST.get("school_name", ""),
            phone=request.POST.get("phone", ""),
            email=request.POST.get("email", ""),
            mother_name=request.POST.get("mother_name", ""),
            father_name=request.POST.get("father_name", ""),
            city=request.POST.get("city", ""),
            state=request.POST.get("state", ""),
            notes=request.POST.get("notes", ""),
        )
        return redirect("patients:list")
    return render(request, "patients/form.html")


def patient_edit_view(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == "POST":
        patient.full_name = request.POST.get("full_name", patient.full_name)
        patient.birth_date = request.POST.get("birth_date") or None
        patient.sex = request.POST.get("sex", "")
        patient.schooling = request.POST.get("schooling", "")
        patient.school_name = request.POST.get("school_name", "")
        patient.phone = request.POST.get("phone", "")
        patient.email = request.POST.get("email", "")
        patient.mother_name = request.POST.get("mother_name", "")
        patient.father_name = request.POST.get("father_name", "")
        patient.city = request.POST.get("city", "")
        patient.state = request.POST.get("state", "")
        patient.notes = request.POST.get("notes", "")
        patient.save()
        return redirect("patients:detail", pk=pk)
    return render(request, "patients/form.html", {"patient": patient})
