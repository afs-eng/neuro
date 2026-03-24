from .schemas import BPA2RawInput


def validate_bpa2_input(data: BPA2RawInput) -> list[str]:
    errors = []
    raw_dict = data.model_dump()

    for code in ["ac", "ad", "aa"]:
        subtest = raw_dict.get(code)
        if not subtest:
            errors.append(f"Subteste '{code}' não informado")
            continue

        if subtest["brutos"] < 0:
            errors.append(f"{code}: pontos brutos não podem ser negativos")
        if subtest["erros"] < 0:
            errors.append(f"{code}: erros não podem ser negativos")
        if subtest["omissoes"] < 0:
            errors.append(f"{code}: omissões não podem ser negativas")

        total = subtest["brutos"] - subtest["erros"] - subtest["omissoes"]
        if total < 0:
            errors.append(
                f"{code}: total ({total}) ficou negativo. Verifique os valores."
            )

    return errors
