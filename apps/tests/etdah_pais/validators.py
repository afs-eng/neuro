from typing import Dict, List


def validate_etdah_pais_input(data: dict) -> list[str]:
    errors = []

    age = data.get("age")
    if age is not None and age > 0 and (age < 2 or age > 17):
        errors.append("ETDAH-PAIS é indicado para pacientes de 2 a 17 anos")

    sex = data.get("sex", "").upper()
    if sex not in ("M", "F"):
        errors.append("Sexo deve ser 'M' ou 'F'")

    return errors


def validate_responses(responses: Dict[int, int]) -> List[str]:
    errors = []
    for item in range(1, 59):
        value = responses.get(item)
        if value is None:
            errors.append(f"Item {item} não respondido")
        elif not (1 <= value <= 6):
            errors.append(f"Item {item} deve estar entre 1 e 6, got {value}")
    return errors
