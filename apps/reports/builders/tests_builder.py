from apps.tests.selectors import get_validated_test_applications_by_evaluation


def build_validated_tests_snapshot(evaluation) -> list[dict]:
    tests = get_validated_test_applications_by_evaluation(evaluation.id)
    return [
        {
            "id": item.id,
            "instrument_code": item.instrument.code,
            "instrument_name": item.instrument.name,
            "applied_on": item.applied_on.isoformat() if item.applied_on else None,
            "is_validated": item.is_validated,
            "classified_payload": item.classified_payload or {},
            "interpretation_text": item.interpretation_text or "",
        }
        for item in tests
    ]
