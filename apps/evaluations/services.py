from .models import Evaluation


def create_evaluation(**data):
    return Evaluation.objects.create(**data)


def update_evaluation(evaluation: Evaluation, **data):
    for field, value in data.items():
        setattr(evaluation, field, value)
    evaluation.save()
    return evaluation