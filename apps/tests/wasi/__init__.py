from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module

from .calculators import compute_wasi_payload
from .config import WASI_CODE, WASI_NAME
from .interpreters import build_wasi_interpretation
from .schemas import WASIRawInput
from .validators import validate_wasi_input


class WASIModule(BaseTestModule):
    code = WASI_CODE
    name = WASI_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            data = WASIRawInput(**(context.raw_scores or {}))
        except Exception as exc:
            return [f"Erro na validação: {exc}"]
        return validate_wasi_input(data)

    def compute(self, context: TestContext) -> dict:
        return compute_wasi_payload(context.raw_scores or {})

    def classify(self, computed_data: dict, **kwargs) -> dict:
        composites = computed_data.get("composites", {})
        return {
            "summary": {
                key: {
                    "qi": value.get("qi"),
                    "classification": value.get("classification"),
                    "interpretability": value.get("interpretability", {}),
                }
                for key, value in composites.items()
            }
        }

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return build_wasi_interpretation(merged_data, patient_name=context.patient_name)


register_test_module(WASI_CODE, WASIModule())
