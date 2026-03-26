from .schemas import EBADEPIJRawInput
from .config import ITENS_POSITIVOS, ITENS_NEGATIVOS


def validate_ebadep_ij_input(data: EBADEPIJRawInput) -> list[str]:
    errors = []
    raw_dict = data.model_dump()

    for i in range(1, 28):
        key = f"item_{i:02d}"
        valor = raw_dict.get(key)
        if valor is None:
            errors.append(f"Item {i:02d} não informado")
            continue
        if valor not in (0, 1, 2):
            errors.append(f"Item {i:02d}: valor inválido ({valor}). Use 0, 1 ou 2.")

    return errors
