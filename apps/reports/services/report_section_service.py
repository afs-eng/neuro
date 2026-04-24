from apps.reports.models import Report, ReportSection


class ReportSectionService:
    AI_FALLBACK_WARNING = "A IA nao esta disponivel no momento; a secao foi regenerada pelo fallback deterministico."

    @staticmethod
    def _rebuild_report_text(report: Report):
        report.edited_text = "\n\n".join(
            f"## {item.title}\n{item.content_edited or item.content_generated}"
            for item in report.sections.all()
        )
        report.save(update_fields=["edited_text", "updated_at"])

    @staticmethod
    def regenerate_section(report: Report, section_key: str, user=None):
        """
        Regenera o texto de uma única seção baseando-se no snapshot de contexto original do laudo.
        Cria uma nova entrada de histórico no ReportVersion se houver mudanças significativas.
        """
        from apps.reports.services.section_regeneration_service import (
            SectionRegenerationService,
        )

        return SectionRegenerationService.regenerate_section(
            report, section_key, user=user
        )

    @staticmethod
    def update_manual_content(section: ReportSection, new_content: str):
        """Atualiza o conteúdo editado pelo profissional"""
        section.content_edited = new_content
        section.save()
        report = section.report
        ReportSectionService._rebuild_report_text(report)
        return section
