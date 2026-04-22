def validate_srs2_input(responses: dict, expected_count: int = 65) -> list[str]:
    errors = []

    if not responses:
        errors.append("Respostas não informadas")
        return errors

    valid_responses = [1, 2, 3, 4]

    for key, value in responses.items():
        if value is not None and value not in valid_responses:
            errors.append(f"Item {key}: resposta deve ser 1, 2, 3 ou 4")

    if len(responses) < expected_count:
        errors.append(f"Esperado {expected_count} respostas, recebidas {len(responses)}")

    return errors
