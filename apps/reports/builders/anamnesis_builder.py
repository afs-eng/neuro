from apps.anamnesis.selectors import get_current_anamnesis_response_by_evaluation


def build_anamnesis_snapshot(evaluation) -> dict:
    response = get_current_anamnesis_response_by_evaluation(evaluation.id)
    if not response:
        return {
            "current_response": None,
            "available": False,
        }

    return {
        "available": True,
        "current_response": {
            "id": response.id,
            "template_code": response.template.code,
            "template_name": response.template.name,
            "response_type": response.response_type,
            "source": response.source,
            "status": response.status,
            "submitted_by_name": response.submitted_by_name or "",
            "submitted_by_relation": response.submitted_by_relation or "",
            "submitted_at": response.submitted_at.isoformat()
            if response.submitted_at
            else None,
            "reviewed_at": response.reviewed_at.isoformat()
            if response.reviewed_at
            else None,
            "answers_payload": response.answers_payload or {},
            "summary_payload": response.summary_payload or {},
        },
    }
