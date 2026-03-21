from .models import Evaluation


def get_evaluations():
    return (
        Evaluation.objects.select_related("patient", "examiner")
        .all()
        .order_by("-created_at")
    )


def get_evaluation_by_id(evaluation_id: int):
    return (
        Evaluation.objects.select_related("patient", "examiner")
        .filter(id=evaluation_id)
        .first()
    )


def get_evaluations_by_patient(patient_id: int):
    return (
        Evaluation.objects.select_related("patient", "examiner")
        .filter(patient_id=patient_id)
        .order_by("-created_at")
    )