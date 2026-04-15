from __future__ import annotations

from pathlib import Path

from .calculators import BAICalculator
from .schemas import BAIItemResponse, BAIRawPayload


class BAIModule:
    key = "BAI"
    label = "Inventário de Ansiedade de Beck"

    def __init__(self, chart_output_dir: str | Path | None = None):
        self.calculator = BAICalculator(chart_output_dir=chart_output_dir)

    def run(self, raw_payload: dict) -> dict:
        payload = BAIRawPayload(
            respondent_name=raw_payload.get("respondent_name"),
            application_mode=raw_payload.get("application_mode", "paper"),
            responses=[
                BAIItemResponse(item_number=item["item_number"], score=item["score"])
                for item in raw_payload.get("responses", [])
            ],
        )
        return self.calculator.score(payload)
