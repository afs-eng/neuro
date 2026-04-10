from django.db.models import Q

from .models import Patient


def get_patients(user=None):
    queryset = Patient.objects.all().order_by("full_name")
    if user and not (user.is_superuser or user.role in ["admin", "reviewer"]):
        queryset = queryset.filter(created_by=user)
    return queryset



def get_patient_by_id(patient_id: int):
    return Patient.objects.filter(id=patient_id).first()


def search_patients(query: str, user=None):
    queryset = Patient.objects.filter(
        Q(full_name__icontains=query)
        | Q(mother_name__icontains=query)
        | Q(father_name__icontains=query)
        | Q(email__icontains=query)
        | Q(phone__icontains=query)
    )
    if user and not (user.is_superuser or user.role in ["admin", "reviewer"]):
        queryset = queryset.filter(created_by=user)
    return queryset.order_by("full_name")