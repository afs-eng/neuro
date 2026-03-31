from .models import EvaluationDocument


def create_document(**data) -> EvaluationDocument:
    return EvaluationDocument.objects.create(**data)


def update_document(document: EvaluationDocument, **data) -> EvaluationDocument:
    for field, value in data.items():
        setattr(document, field, value)
    document.save()
    return document


def delete_document(document: EvaluationDocument) -> None:
    storage = document.file.storage if document.file else None
    file_name = document.file.name if document.file else None
    document.delete()
    if storage and file_name:
        storage.delete(file_name)
