from .schemas import FDTRawInput


def validate_fdt_input(data: FDTRawInput, age: int | None = None) -> list[str]:
    errors: list[str] = []

    if age is None:
        errors.append("Paciente sem idade valida para aplicar as normas do FDT")
    elif age < 6:
        errors.append("A idade minima normativa disponivel para o FDT e 6 anos")

    for stage_name, stage in data.model_dump().items():
        if stage["tempo"] <= 0:
            errors.append(f"O tempo da etapa '{stage_name}' deve ser maior que zero")

    return errors
