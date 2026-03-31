from .models import Evaluation, EvaluationProgressEntry


def create_evaluation(**data) -> Evaluation:
    return Evaluation.objects.create(**data)


def update_evaluation(evaluation: Evaluation, **data) -> Evaluation:
    for field, value in data.items():
        setattr(evaluation, field, value)
    evaluation.save()
    return evaluation


def create_progress_entry(**data) -> EvaluationProgressEntry:
    return EvaluationProgressEntry.objects.create(**data)


def update_progress_entry(
    progress_entry: EvaluationProgressEntry, **data
) -> EvaluationProgressEntry:
    for field, value in data.items():
        setattr(progress_entry, field, value)
    progress_entry.save()
    return progress_entry


def delete_progress_entry(progress_entry: EvaluationProgressEntry) -> None:
    progress_entry.delete()
