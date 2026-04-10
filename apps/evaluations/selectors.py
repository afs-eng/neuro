from typing import Optional

from django.db.models import QuerySet

from .models import Evaluation, EvaluationProgressEntry


def get_evaluations(user=None) -> QuerySet[Evaluation]:
    queryset = Evaluation.objects.with_details().all().order_by("-created_at")
    if user and not (user.is_superuser or user.role in ["admin", "reviewer"]):
        queryset = queryset.filter(examiner=user)
    return queryset



def get_evaluation_by_id(evaluation_id: int) -> Optional[Evaluation]:
    return Evaluation.objects.with_details().filter(id=evaluation_id).first()


def get_evaluations_by_patient(patient_id: int, user=None) -> QuerySet[Evaluation]:
    queryset = (
        Evaluation.objects.with_details()
        .filter(patient_id=patient_id)
        .order_by("-created_at")
    )
    if user and not (user.is_superuser or user.role in ["admin", "reviewer"]):
        queryset = queryset.filter(examiner=user)
    return queryset



def get_progress_entry_by_id(entry_id: int) -> Optional[EvaluationProgressEntry]:
    return EvaluationProgressEntry.objects.with_details().filter(id=entry_id).first()


def get_progress_entries_by_evaluation(
    evaluation_id: int,
) -> QuerySet[EvaluationProgressEntry]:
    return (
        EvaluationProgressEntry.objects.with_details()
        .filter(evaluation_id=evaluation_id)
        .order_by("-entry_date", "-created_at")
    )
