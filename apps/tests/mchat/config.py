from apps.tests.base.types import BaseTestModule, TestContext

from .calculators import build_computed_payload
from .classifiers import classify_mchat
from .interpreters import build_mchat_interpretation
from .validators import validate_mchat_payload


class MCHATModule(BaseTestModule):
    code = "MCHAT"
    name = "M-CHAT"

    def validate(self, context: TestContext) -> list[str]:
        try:
            validate_mchat_payload(context.raw_scores)
            return []
        except Exception as exc:
            return [f"Erro na validacao: {exc}"]

    def compute(self, context: TestContext) -> dict:
        return build_computed_payload(context.raw_scores)

    def classify(self, computed_data: dict) -> dict:
        return classify_mchat(computed_data)

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return build_mchat_interpretation(merged_data, merged_data)
