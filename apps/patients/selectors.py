from django.db.models import Q

from .models import Patient


def get_patients():
    return Patient.objects.all().order_by("full_name")


def get_patient_by_id(patient_id: int):
    return Patient.objects.filter(id=patient_id).first()


def search_patients(query: str):
    return (
        Patient.objects.filter(
            Q(full_name__icontains=query)
            | Q(mother_name__icontains=query)
            | Q(father_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
        )
        .order_by("full_name")
    )