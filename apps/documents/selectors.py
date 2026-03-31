from typing import Optional

from django.db.models import QuerySet

from .models import EvaluationDocument


def get_document_by_id(document_id: int) -> Optional[EvaluationDocument]:
    return EvaluationDocument.objects.with_details().filter(id=document_id).first()


def get_documents_by_evaluation(evaluation_id: int) -> QuerySet[EvaluationDocument]:
    return (
        EvaluationDocument.objects.with_details()
        .filter(evaluation_id=evaluation_id)
        .order_by("-created_at")
    )


def get_relevant_documents_by_evaluation(
    evaluation_id: int,
) -> QuerySet[EvaluationDocument]:
    return (
        EvaluationDocument.objects.with_details()
        .filter(evaluation_id=evaluation_id, is_relevant_for_report=True)
        .order_by("document_date", "created_at")
    )
