from .anamnesis_builder import build_anamnesis_snapshot
from .documents_builder import build_documents_snapshot
from .progress_builder import build_progress_snapshot
from .tests_builder import build_validated_tests_snapshot


def build_report_snapshot(evaluation) -> dict:
    patient = evaluation.patient
    validated_tests = build_validated_tests_snapshot(evaluation)

    return {
        "evaluation": {
            "id": evaluation.id,
            "code": evaluation.code,
            "title": evaluation.title or "",
            "referral_reason": evaluation.referral_reason or "",
            "evaluation_purpose": evaluation.evaluation_purpose or "",
            "clinical_hypothesis": evaluation.clinical_hypothesis or "",
            "start_date": evaluation.start_date.isoformat()
            if evaluation.start_date
            else None,
            "end_date": evaluation.end_date.isoformat()
            if evaluation.end_date
            else None,
            "general_notes": evaluation.general_notes or "",
        },
        "patient": {
            "id": patient.id,
            "full_name": patient.full_name,
            "birth_date": patient.birth_date.isoformat()
            if patient.birth_date
            else None,
            "sex": patient.sex,
            "schooling": patient.schooling,
            "school_name": patient.school_name,
            "grade_year": patient.grade_year,
        },
        "anamnesis": build_anamnesis_snapshot(evaluation),
        "documents": build_documents_snapshot(evaluation),
        "progress_entries": build_progress_snapshot(evaluation),
        "validated_tests": validated_tests,
        "tests": validated_tests,
    }
