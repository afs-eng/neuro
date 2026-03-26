def validate_ebadep_a_input(data) -> list[str]:
    errors = []
    raw_dict = data.model_dump()

    for i in range(1, 46):
        key = f"item_{i:02d}"
        valor = raw_dict.get(key)
        if valor is None:
            errors.append(f"Item {i:02d} não informado")
            continue
        if valor not in (0, 1, 2, 3):
            errors.append(f"Item {i:02d}: valor inválido ({valor}). Use 0, 1, 2 ou 3.")

    return errors
