from .config import FATORES, FATORES_TOTAL


def compute_scared_scores(raw_payload: dict, patient_age: int | None = None) -> dict:
    responses = raw_payload.get("responses", {})
    form = raw_payload.get("form", "child")

    resp_int = {int(k): int(v) for k, v in responses.items()}

    brutos = {}
    for fator, itens in FATORES.items():
        brutos[fator] = sum(resp_int.get(i, 0) for i in itens)

    brutos["total"] = sum(resp_int.get(i, 0) for i in FATORES_TOTAL)

    return {
        "form": form,
        "brutos": brutos,
        "gender": raw_payload.get("gender", "M"),
        "age": raw_payload.get("age", patient_age),
    }
