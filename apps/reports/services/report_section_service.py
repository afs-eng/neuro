from django.utils import timezone

from apps.reports.models import Report, ReportSection, ReportVersion
from apps.reports.builders.snapshot_builder import build_report_snapshot
from apps.reports.services.report_ai_service import ReportAIService
from apps.reports.services.report_generation_service import ReportGenerationService
from apps.reports.services.report_version_service import ReportVersionService


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
        section = report.sections.filter(key=section_key).first()
        if not section or section.is_locked:
            return None

        context = build_report_snapshot(report.evaluation)
        report.context_payload = context

        warnings = []
        generation_metadata = {}
        if ReportAIService.supports_section(section_key):
            try:
                generation_result = ReportAIService.generate_section(
                    report, section_key, context
                )
                new_text = generation_result["content"]
                warnings = generation_result.get("warnings") or []
                generation_metadata = generation_result.get("metadata") or {}
            except Exception as exc:
                # Se a IA falhar, mantém a regeneração disponível com fallback determinístico.
                new_text = ReportGenerationService._generate_section_text(
                    report, section_key, context
                )
                generation_metadata = {
                    "provider": "deterministic",
                    "model": "rules-based",
                    "section": section_key,
                    "fallback_reason": str(exc),
                    "used_fallback": True,
                    "generation_path": "deterministic_fallback",
                }
                warnings = [ReportSectionService.AI_FALLBACK_WARNING]
        else:
            new_text = ReportGenerationService._generate_section_text(
                report, section_key, context
            )
            generation_metadata = {
                "provider": "deterministic",
                "model": "rules-based",
                "section": section_key,
                "used_fallback": False,
                "generation_path": "deterministic_only",
            }

        generation_metadata = {
            **generation_metadata,
            "used_fallback": bool(generation_metadata.get("used_fallback")),
            "generated_at": timezone.now().isoformat(),
        }

        previous_generated = section.content_generated
        previous_edited = section.content_edited

        section.content_generated = new_text
        section.generation_metadata = generation_metadata
        section.warnings_payload = warnings
        if previous_edited == previous_generated:
            section.content_edited = new_text

        section.save(
            update_fields=[
                "content_generated",
                "content_edited",
                "generation_metadata",
                "warnings_payload",
                "updated_at",
            ]
        )
        report.ai_metadata = {
            **(report.ai_metadata or {}),
            "last_generation": generation_metadata,
        }
        report.save(update_fields=["context_payload", "ai_metadata", "updated_at"])
        ReportSectionService._rebuild_report_text(report)
        ReportVersionService.create_version(report, user=user)
        return section

    @staticmethod
    def update_manual_content(section: ReportSection, new_content: str):
        """Atualiza o conteúdo editado pelo profissional"""
        section.content_edited = new_content
        section.save()
        report = section.report
        ReportSectionService._rebuild_report_text(report)
        return section
