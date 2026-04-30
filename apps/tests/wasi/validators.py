from __future__ import annotations

from dateutil.relativedelta import relativedelta

from .config import WASI_MAX_AGE, WASI_MIN_AGE, WASI_SUBTESTS
from .schemas import WASIRawInput


def validate_wasi_input(data: WASIRawInput) -> list[str]:
    errors: list[str] = []

    age = relativedelta(data.applied_on, data.birth_date)
    if age.years < WASI_MIN_AGE or age.years > WASI_MAX_AGE:
        errors.append("O WASI pode ser aplicado apenas entre 6 e 89 anos.")

    if data.confidence_level not in {"90", "95"}:
        errors.append("O nivel de confianca do WASI deve ser 90 ou 95.")

    for key, config in WASI_SUBTESTS.items():
        value = getattr(data, key)
        if value < 0:
            errors.append(f"{config['name']}: escore bruto nao pode ser negativo.")

    return errors
