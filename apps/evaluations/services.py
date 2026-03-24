from .models import Evaluation


def create_evaluation(**data) -> Evaluation:
    return Evaluation.objects.create(**data)


def update_evaluation(evaluation: Evaluation, **data) -> Evaluation:
    for field, value in data.items():
        setattr(evaluation, field, value)
    evaluation.save()
    return evaluation