from dataclasses import dataclass, field
from typing import Any


@dataclass
class TestContext:
    patient_name: str
    evaluation_id: int
    instrument_code: str
    raw_scores: dict[str, Any] = field(default_factory=dict)
    reviewed_scores: dict[str, Any] = field(default_factory=dict)


class BaseTestModule:
    code: str = ""
    name: str = ""

    def validate(self, context: TestContext) -> list[str]:
        return []

    def compute(self, context: TestContext) -> dict[str, Any]:
        return {}

    def classify(self, computed_data: dict[str, Any]) -> dict[str, Any]:
        return {}

    def interpret(self, context: TestContext, merged_data: dict[str, Any]) -> str:
        return ""