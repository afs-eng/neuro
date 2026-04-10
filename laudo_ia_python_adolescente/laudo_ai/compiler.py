from __future__ import annotations

from .schemas import ReportDraft


class ReportCompiler:
    def compile_markdown(self, draft: ReportDraft) -> str:
        return draft.compile_text()

    def compile_plaintext(self, draft: ReportDraft) -> str:
        return "\n\n".join(section.text for section in draft.sections)
