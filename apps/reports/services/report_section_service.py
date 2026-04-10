from apps.reports.models import Report, ReportSection, ReportVersion
from apps.reports.builders.snapshot_builder import build_report_snapshot
from apps.reports.services.report_version_service import ReportVersionService


class ReportSectionService:
    @staticmethod
    def regenerate_section(report: Report, section_key: str, user=None):
        """
        Regenera o texto de uma única seção baseando-se no snapshot de contexto original do laudo.
        Cria uma nova entrada de histórico no ReportVersion se houver mudanças significativas.
        """
        section = report.sections.filter(key=section_key).first()
        if not section or section.is_locked:
            return None

        # Puxa o snapshot (Dados do momento em que o laudo foi gerado)
        context = report.context_payload or build_report_snapshot(report.evaluation)

        # Simulação de nova chamada ao Provedor de IA com o prompt da seção específica
        # TODO: Integrar com LLM usando context + section_key + prompt_especifico
        new_text = f"🔄 Texto regenerado para a seção: {section.title}."
        previous_generated = section.content_generated
        previous_edited = section.content_edited

        # Salva a alteração
        section.content_generated = new_text
        # Se o texto editado for igual ao gerado anterior, atualizamos o editado também
        if previous_edited == previous_generated:
            section.content_edited = new_text

        section.save()
        report.edited_text = "\n\n".join(
            f"## {item.title}\n{item.content_edited or item.content_generated}"
            for item in report.sections.all()
        )
        report.save(update_fields=["edited_text", "updated_at"])
        ReportVersionService.create_version(report, user=user)
        return section

    @staticmethod
    def update_manual_content(section: ReportSection, new_content: str):
        """Atualiza o conteúdo editado pelo profissional"""
        section.content_edited = new_content
        section.save()
        report = section.report
        report.edited_text = "\n\n".join(
            f"## {item.title}\n{item.content_edited or item.content_generated}"
            for item in report.sections.all()
        )
        report.save(update_fields=["edited_text", "updated_at"])
        return section
