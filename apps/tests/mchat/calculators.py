from .constants import CRITICAL_ITEMS, ITEMS, FAILURE_RULES
from .loaders import load_scoring_rules
from .validators import normalize_answer


def is_failure(item_number: int, answer: str) -> bool:
    rules = load_scoring_rules().get("failure_rules", {})
    expected = normalize_answer(rules.get(str(item_number), FAILURE_RULES[item_number]))
    return expected == normalize_answer(answer)


def build_computed_payload(payload: dict) -> dict:
    item_results = {}
    total_failures = 0
    critical_failures = 0
    failed_items: list[int] = []
    failed_critical_items: list[int] = []

    for item_number, slug in ITEMS:
        answer = payload["items"][slug]["answer"]
        failed = is_failure(item_number, answer)

        item_results[slug] = {
            "item_number": item_number,
            "answer": answer,
            "result": "Falha" if failed else "Passa",
            "is_critical": item_number in CRITICAL_ITEMS,
        }

        if failed:
            total_failures += 1
            failed_items.append(item_number)
            if item_number in CRITICAL_ITEMS:
                critical_failures += 1
                failed_critical_items.append(item_number)

    return {
        "total_failures": total_failures,
        "critical_failures": critical_failures,
        "failed_items": failed_items,
        "failed_critical_items": failed_critical_items,
        "item_results": item_results,
    }
