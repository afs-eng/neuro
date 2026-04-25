from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module

from .calculators import compute_wais3_payload
from .classifiers import classify_wais3_payload
from .config import WAIS3_CODE, WAIS3_NAME
from .interpreters import build_wais3_interpretation
from .schemas import WAIS3RawInput
from .validators import validate_wais3_input


class WAIS3Module(BaseTestModule):
    code = WAIS3_CODE
    name = WAIS3_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            data = WAIS3RawInput(**(context.raw_scores or {}))
        except Exception as exc:
            return [f"Erro na validação: {exc}"]
        return validate_wais3_input(data)

    def compute(self, context: TestContext) -> dict:
        return compute_wais3_payload(context.raw_scores or {})

    def classify(self, computed_data: dict) -> dict:
        return classify_wais3_payload(computed_data)

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return build_wais3_interpretation(merged_data or {}, context.patient_name)


register_test_module(WAIS3_CODE, WAIS3Module())
