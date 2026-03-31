from apps.documents.selectors import get_relevant_documents_by_evaluation


def build_documents_snapshot(evaluation) -> list[dict]:
    documents = get_relevant_documents_by_evaluation(evaluation.id)
    return [
        {
            "id": item.id,
            "title": item.title,
            "document_type": item.document_type,
            "document_type_display": item.get_document_type_display(),
            "source": item.source,
            "document_date": item.document_date.isoformat()
            if item.document_date
            else None,
            "notes": item.notes,
            "file_name": item.file.name.split("/")[-1] if item.file else "",
            "is_relevant_for_report": item.is_relevant_for_report,
        }
        for item in documents
    ]
