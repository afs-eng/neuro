def validate_epq_j_input(data) -> list[str]:
    erros = []
    for i in range(1, 61):
        key = f"item_{i:02d}"
        if not hasattr(data, key):
            erros.append(f"Item {i} ausente")
        elif getattr(data, key) not in [0, 1]:
            erros.append(f"Item {i} deve ser 0 ou 1")
    return erros
