from apps.tests.base.types import BaseTestModule, TestContext
from apps.tests.registry import register_test_module

from .calculators import calculate_fdt_results, calculate_stage_totals
from .config import FDT_CODE, FDT_NAME
from .interpreters import interpret_fdt_result
from .schemas import FDTRawInput
from .validators import validate_fdt_input


class FDTModule(BaseTestModule):
    code = FDT_CODE
    name = FDT_NAME

    def validate(self, context: TestContext) -> list[str]:
        try:
            data = FDTRawInput(**context.raw_scores)
            age = context.reviewed_scores.get("age")
            return validate_fdt_input(data, age=age)
        except Exception as e:
            return [f"Erro na validacao: {e}"]

    def compute(self, context: TestContext) -> dict:
        data = FDTRawInput(**context.raw_scores)
        age = context.reviewed_scores.get("age")
        stage_totals = calculate_stage_totals(data.model_dump())
        return calculate_fdt_results(stage_totals, age)

    def classify(self, computed_data: dict) -> dict:
        return computed_data

    def interpret(self, context: TestContext, merged_data: dict) -> str:
        return interpret_fdt_result(merged_data, patient_name=context.patient_name)


register_test_module(FDT_CODE, FDTModule())
