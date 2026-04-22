from .config import SCARED_FORMS


def validate_scared_input(raw_payload: dict) -> list[str]:
    errors = []
    responses = raw_payload.get("responses", {})
    form = raw_payload.get("form", "child")

    if form not in SCARED_FORMS:
        errors.append("Formulário SCARED inválido.")

    if not responses:
        errors.append("Nenhuma resposta informada.")

    for i in range(1, 42):
        val = responses.get(str(i))
        if val is None:
            errors.append(f"Item {i} não respondido.")
        elif val not in [0, 1, 2]:
            errors.append(f"Item {i} possui valor inválido ({val}).")

    return errors
