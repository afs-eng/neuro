from .config import WISC4_SUBTESTS
from .schemas import WISC4RawInput


def validate_wisc4_input(data: WISC4RawInput) -> list[str]:
    errors = []
    raw_dict = data.model_dump()

    for code, config in WISC4_SUBTESTS.items():
        subtest_data = raw_dict.get(code)
        if not subtest_data:
            errors.append(f"Subteste '{code}' não informado")
            continue

        eb = subtest_data["escore_bruto"]
        if eb > config.max_raw_score:
            errors.append(
                f"{code}: escore bruto ({eb}) maior que o máximo ({config.max_raw_score})"
            )
        if eb < 0:
            errors.append(f"{code}: escore bruto não pode ser negativo")

    return errors
