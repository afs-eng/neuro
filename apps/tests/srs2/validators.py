from typing import Optional


def validate_srs2_input(data: "SRS2RawInput", age: Optional[int] = None) -> list[str]:
    errors = []

    if not data.responses:
        errors.append("Respostas não informadas")
        return errors

    valid_responses = [1, 2, 3, 4]

    for key, value in data.responses.items():
        if value is not None and value not in valid_responses:
            errors.append(f"Item {key}: resposta deve ser 1, 2, 3 ou 4")

    return errors


def calculate_raw_score(responses: dict, items: list[int]) -> int:
    return sum(responses.get(i, 0) for i in items)


def apply_reversed_items(responses: dict, reversed_items: list[int]) -> dict:
    converted = {}
    for key, value in responses.items():
        if key in reversed_items and value is not None:
            converted[key] = 4 - value
        else:
            converted[key] = value
    return converted


def classify_by_percentile(percentile: float) -> str:
    if percentile >= 70:
        return "Acima da média"
    if percentile >= 30:
        return "Média"
    if percentile >= 16:
        return "Abaixo da média"
    return "Muito abaixo da média"
