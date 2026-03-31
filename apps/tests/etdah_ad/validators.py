from typing import Dict, List


def validate_etdah_ad_input(data: dict) -> list[str]:
    errors = []

    age = data.get("age")
    if age is not None and age > 0 and age < 12:
        errors.append("ETDAH-AD é indicado para pacientes a partir de 12 anos")

    return errors


def validate_responses(responses: Dict[int, int]) -> List[str]:
    errors = []
    for item in range(1, 70):
        value = responses.get(item)
        if value is None:
            errors.append(f"Item {item} não respondido")
        elif not (0 <= value <= 5):
            errors.append(f"Item {item} deve estar entre 0 e 5, got {value}")
    return errors
