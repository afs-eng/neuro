from typing import Optional

from django.db.models import QuerySet

from .models import Evaluation

def get_evaluations() -> QuerySet[Evaluation]:
    return (
        Evaluation.objects.with_details()
        .all()
        .order_by("-created_at")
    )


def get_evaluation_by_id(evaluation_id: int) -> Optional[Evaluation]:
    return (
        Evaluation.objects.with_details()
        .filter(id=evaluation_id)
        .first()
    )


def get_evaluations_by_patient(patient_id: int) -> QuerySet[Evaluation]:
    return (
        Evaluation.objects.with_details()
        .filter(patient_id=patient_id)
        .order_by("-created_at")
    )