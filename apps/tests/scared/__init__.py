from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module
from .calculators import compute_scared_scores
from .classifiers import classify_scared_scores
from .config import SCARED_CODE, SCARED_NAME
from .interpreters import interpret_scared_results
from .validators import validate_scared_input


class SCAREDModule(BaseTestModule):
    code = SCARED_CODE
    name = SCARED_NAME

    def validate(self, context: TestContext) -> list[str]:
        return validate_scared_input(context.raw_scores)

    def compute(self, context: TestContext) -> dict:
        return compute_scared_scores(context.raw_scores, patient_age=context.patient_age)

    def classify(self, computed_data: dict, idade: int = 0) -> dict:
        return classify_scared_scores(computed_data, idade=idade)

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return interpret_scared_results(merged_data, context.patient_name)


register_test_module(SCARED_CODE, SCAREDModule())
