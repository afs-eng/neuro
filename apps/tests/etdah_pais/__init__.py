from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .config import ETDAHPAIS_CODE, ETDAHPAIS_NAME
from .schemas import ETDAHPAISInput, ETDAHPAISResponse
from .validators import validate_etdah_pais_input, validate_responses
from .calculators import calculate_raw_scores
from .interpreters import interpret_results, generate_report


class ETDAHPAISModule(BaseTestModule):
    code = ETDAHPAIS_CODE
    name = ETDAHPAIS_NAME

    def validate(self, context: TestContext) -> list[str]:
        errors = []

        errors.extend(validate_etdah_pais_input(context.raw_scores))

        responses = context.raw_scores.get("responses", {})
        errors.extend(validate_responses(responses))

        return errors

    def compute(self, context: TestContext) -> dict:
        responses = context.raw_scores.get("responses", {})
        raw_scores = calculate_raw_scores(responses)
        age = context.raw_scores.get("age", 10)
        sex = context.raw_scores.get("sex", "M")

        return {
            "raw_scores": raw_scores,
            "age": age,
            "sex": sex,
            "responses": responses,
        }

    def classify(self, computed_data: dict, faixa: str = "") -> dict:
        raw_scores = computed_data.get("raw_scores", {})
        age = computed_data.get("age", 10)
        sex = computed_data.get("sex", "M")

        results = interpret_results(raw_scores, age, sex)

        return {
            "raw_scores": raw_scores,
            "results": results,
            "age": age,
            "sex": sex,
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        raw_scores = merged_data.get("raw_scores", {})
        age = merged_data.get("age", context.raw_scores.get("age", 10))
        sex = merged_data.get("sex", context.raw_scores.get("sex", "M"))

        return generate_report(raw_scores, age, sex, patient_name=context.patient_name)


register_test_module(ETDAHPAIS_CODE, ETDAHPAISModule())
