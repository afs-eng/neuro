class TestException(Exception):
    pass


class InvalidAgeRangeError(TestException):
    def __init__(self, instrument_code: str, age: int, min_age: int, max_age: int):
        self.instrument_code = instrument_code
        self.age = age
        self.min_age = min_age
        self.max_age = max_age
        super().__init__(
            f"Idade {age} fora do range do instrumento {instrument_code} ({min_age}-{max_age})"
        )


class InvalidEducationRangeError(TestException):
    def __init__(self, instrument_code: str, education: int):
        self.instrument_code = instrument_code
        self.education = education
        super().__init__(
            f"Anos de educação {education} inválidos para {instrument_code}"
        )


class InstrumentNotFoundError(TestException):
    def __init__(self, code: str):
        self.code = code
        super().__init__(f"Instrumento com código '{code}' não encontrado")


class CalculationError(TestException):
    def __init__(self, instrument_code: str, reason: str):
        self.instrument_code = instrument_code
        self.reason = reason
        super().__init__(f"Erro no cálculo {instrument_code}: {reason}")


class ClassificationError(TestException):
    def __init__(self, instrument_code: str, reason: str):
        self.instrument_code = instrument_code
        self.reason = reason
        super().__init__(f"Erro na classificação {instrument_code}: {reason}")


class InterpretationError(TestException):
    def __init__(self, instrument_code: str, reason: str):
        self.instrument_code = instrument_code
        self.reason = reason
        super().__init__(f"Erro na interpretação {instrument_code}: {reason}")


class NormTableNotFoundError(TestException):
    def __init__(
        self, instrument_code: str, age_group: str, education_group: str = None
    ):
        self.instrument_code = instrument_code
        self.age_group = age_group
        self.education_group = education_group
        super().__init__(
            f"Tabela normativa não encontrada para {instrument_code}, "
            f"idade={age_group}, educação={education_group or 'N/A'}"
        )


class RawDataValidationError(TestException):
    def __init__(self, field: str, reason: str):
        self.field = field
        self.reason = reason
        super().__init__(f"Erro na validação do campo '{field}': {reason}")
