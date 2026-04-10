from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .schemas import EvaluationContext, ReportDraft


@dataclass
class ConsistencyIssue:
    level: str
    message: str


@dataclass
class ConsistencyReport:
    issues: List[ConsistencyIssue] = field(default_factory=list)

    def add(self, level: str, message: str) -> None:
        self.issues.append(ConsistencyIssue(level=level, message=message))

    @property
    def is_valid(self) -> bool:
        return not any(issue.level == "error" for issue in self.issues)


class ConsistencyChecker:
    def validate(self, context: EvaluationContext, draft: ReportDraft) -> ConsistencyReport:
        report = ConsistencyReport()

        if not context.tests:
            report.add("warning", "Nenhum teste foi informado no contexto.")

        conclusao = next((s for s in draft.sections if s.key.value == "conclusao"), None)
        if conclusao and "diagnóstico confirmado" in conclusao.text.lower():
            report.add("warning", "Evite fechar diagnóstico como definitivo no rascunho automático.")

        return report
