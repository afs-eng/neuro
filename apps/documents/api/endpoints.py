from datetime import date

from ninja import File, Form, Router, UploadedFile
from ninja.errors import HttpError

from apps.accounts.models import UserRole
from apps.api.auth import bearer_auth
from apps.evaluations.models import Evaluation
from apps.patients.models import Patient

from apps.documents.models import DocumentType
from apps.documents.selectors import get_document_by_id, get_documents_by_evaluation
from apps.documents.services import create_document, delete_document, update_document

from .schemas import DocumentOut, DocumentUpdateIn, MessageOut


router = Router(tags=["documents"])


def can_view_documents(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
        UserRole.REVIEWER,
        UserRole.READONLY,
    }


def can_edit_documents(user) -> bool:
    return bool(user) and user.role in {
        UserRole.ADMIN,
        UserRole.NEUROPSYCHOLOGIST,
        UserRole.ASSISTANT,
    }


def serialize_document(document) -> dict:
    return {
        "id": document.id,
        "evaluation_id": document.evaluation_id,
        "patient_id": document.patient_id,
        "title": document.title,
        "file_name": document.file.name.split("/")[-1] if document.file else "",
        "file_url": document.file.url if document.file else "",
        "document_type": document.document_type,
        "document_type_display": document.get_document_type_display(),
        "source": document.source or "",
        "document_date": document.document_date,
        "notes": document.notes or "",
        "is_relevant_for_report": document.is_relevant_for_report,
        "created_at": document.created_at.isoformat() if document.created_at else None,
    }


@router.get("/", response=list[DocumentOut], auth=bearer_auth)
def list_documents(request, evaluation_id: int) -> list[dict]:
    if not can_view_documents(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar documentos.")
    return [
        serialize_document(item) for item in get_documents_by_evaluation(evaluation_id)
    ]


@router.get(
    "/{document_id}", response={200: DocumentOut, 404: MessageOut}, auth=bearer_auth
)
def get_document_endpoint(request, document_id: int) -> tuple[int, dict]:
    if not can_view_documents(request.auth):
        raise HttpError(403, "Você não tem permissão para visualizar documentos.")

    document = get_document_by_id(document_id)
    if not document:
        return 404, {"message": "Documento não encontrado."}
    return 200, serialize_document(document)


@router.post(
    "/upload",
    response={201: DocumentOut, 400: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def upload_document_endpoint(
    request,
    evaluation_id: int = Form(...),
    patient_id: int = Form(...),
    title: str = Form(...),
    document_type: str = Form(DocumentType.OTHER),
    source: str = Form(""),
    document_date: date | None = Form(None),
    notes: str = Form(""),
    is_relevant_for_report: bool = Form(True),
    file: UploadedFile = File(...),
) -> tuple[int, dict]:
    if not can_edit_documents(request.auth):
        return 403, {"message": "Você não tem permissão para enviar documentos."}

    evaluation = (
        Evaluation.objects.filter(id=evaluation_id).select_related("patient").first()
    )
    if not evaluation:
        return 404, {"message": "Avaliação não encontrada."}

    patient = Patient.objects.filter(id=patient_id).first()
    if not patient:
        return 404, {"message": "Paciente não encontrado."}

    if evaluation.patient_id != patient.id:
        return 400, {"message": "Paciente não corresponde à avaliação informada."}

    document = create_document(
        evaluation=evaluation,
        patient=patient,
        title=title,
        file=file,
        document_type=document_type,
        source=source,
        document_date=document_date,
        notes=notes,
        is_relevant_for_report=is_relevant_for_report,
    )
    return 201, serialize_document(document)


@router.patch(
    "/{document_id}",
    response={200: DocumentOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def update_document_endpoint(
    request, document_id: int, payload: DocumentUpdateIn
) -> tuple[int, dict]:
    if not can_edit_documents(request.auth):
        return 403, {"message": "Você não tem permissão para editar documentos."}

    document = get_document_by_id(document_id)
    if not document:
        return 404, {"message": "Documento não encontrado."}

    updated = update_document(document, **payload.dict(exclude_unset=True))
    return 200, serialize_document(updated)


@router.delete(
    "/{document_id}",
    response={200: MessageOut, 403: MessageOut, 404: MessageOut},
    auth=bearer_auth,
)
def delete_document_endpoint(request, document_id: int) -> tuple[int, dict]:
    if not can_edit_documents(request.auth):
        return 403, {"message": "Você não tem permissão para excluir documentos."}

    document = get_document_by_id(document_id)
    if not document:
        return 404, {"message": "Documento não encontrado."}

    delete_document(document)
    return 200, {"message": "Documento excluído com sucesso."}
