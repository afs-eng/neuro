from apps.evaluations.selectors import get_progress_entries_by_evaluation


def build_progress_snapshot(evaluation) -> list[dict]:
    progress_entries = get_progress_entries_by_evaluation(evaluation.id)
    return [
        {
            "id": item.id,
            "entry_type": item.entry_type,
            "entry_type_display": item.get_entry_type_display(),
            "entry_date": item.entry_date.isoformat(),
            "objective": item.objective,
            "tests_applied": item.tests_applied,
            "observed_behavior": item.observed_behavior,
            "clinical_notes": item.clinical_notes,
            "next_steps": item.next_steps,
            "include_in_report": item.include_in_report,
        }
        for item in progress_entries
        if item.include_in_report
    ]
