from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .calculators import compute_srs2_scores
from .classifiers import classify_srs2_scores
from .config import SRS2_CODE, SRS2_NAME
from .interpreters import interpret_srs2_results
from .validators import validate_srs2_input


class SRS2Module(BaseTestModule):
    code = SRS2_CODE
    name = SRS2_NAME

    def validate(self, context: TestContext) -> list[str]:
        responses = context.raw_scores.get("responses", {})
        errors = validate_srs2_input(responses, expected_count=65)
        if not responses:
            return ["Nenhuma resposta recebida"]
        return errors

    def compute(self, context: TestContext) -> dict:
        raw_responses = context.raw_scores.get("responses", {})
        form = context.raw_scores.get("form", "idade_escolar")
        return compute_srs2_scores(raw_responses, form)

    def classify(self, computed_data: dict, **kwargs) -> dict:
        gender = kwargs.get("gender", "M")
        age = kwargs.get("age", 10)
        return classify_srs2_scores(computed_data, gender=gender, age=age)

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return interpret_srs2_results(merged_data)


register_test_module(SRS2_CODE, SRS2Module())
