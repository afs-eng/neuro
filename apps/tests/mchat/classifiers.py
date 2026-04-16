def classify_mchat(computed_payload: dict) -> dict:
    total_failures = computed_payload["total_failures"]
    critical_failures = computed_payload["critical_failures"]

    if total_failures >= 3 or critical_failures >= 2:
        return {
            "screen_result": "Triagem positiva para risco de sinais compatíveis com TEA",
            "screen_code": "positive",
        }

    return {
        "screen_result": "Triagem negativa no M-CHAT",
        "screen_code": "negative",
    }
