from __future__ import annotations

from django.utils import timezone

from apps.reports.builders.snapshot_builder import build_report_snapshot
from apps.reports.models import Report
from apps.reports.services.report_pipeline_service import ReportPipelineService
from apps.reports.services.report_section_service import ReportSectionService
from apps.reports.services.report_version_service import ReportVersionService
from .section_workflow_service import SectionWorkflowService


class SectionRegenerationService:
    @classmethod
    def regenerate_section(cls, report: Report, section_key: str, context: dict | None = None, user=None):
        section = report.sections.filter(key=section_key).first()
        if not section or section.is_locked:
            return None

        context = context or build_report_snapshot(report.evaluation)
        report.context_payload = context
        report.save(update_fields=["context_payload", "updated_at"])

        result = ReportPipelineService._generate_single_section(report, section_key, context)
        ReportPipelineService._save_section_result(
            report,
            section_key,
            section.title,
            section.order,
            result,
        )

        cls.mark_dependents_stale(report, section_key)
        regenerated = report.sections.filter(key=section_key).first()
        generation_metadata = regenerated.generation_metadata or {}
        generation_metadata = {
            **generation_metadata,
            "generated_at": timezone.now().isoformat(),
            "stale": False,
            "stale_dependencies": [],
        }
        regenerated.generation_metadata = generation_metadata
        regenerated.save(update_fields=["generation_metadata", "updated_at"])

        report.ai_metadata = {
            **(report.ai_metadata or {}),
            "last_generation": generation_metadata,
            "stale_sections": [
                item.key
                for item in report.sections.all()
                if (item.generation_metadata or {}).get("stale")
            ],
        }
        report.save(update_fields=["ai_metadata", "updated_at"])
        ReportSectionService._rebuild_report_text(report)
        ReportVersionService.create_version(report, user=user)
        return regenerated

    @classmethod
    def mark_dependents_stale(cls, report: Report, section_key: str) -> list[str]:
        stale_keys: list[str] = []
        queue: list[tuple[str, str]] = [
            (dependent_key, section_key)
            for dependent_key in SectionWorkflowService.get_dependents(section_key)
        ]
        visited: set[str] = set()

        while queue:
            dependent_key, stale_source = queue.pop(0)
            if dependent_key in visited:
                continue
            visited.add(dependent_key)
            section = report.sections.filter(key=dependent_key).first()
            if not section or section.is_locked:
                continue
            metadata = section.generation_metadata or {}
            stale_dependencies = sorted(
                set((metadata.get("stale_dependencies") or []) + [stale_source])
            )
            section.generation_metadata = {
                **metadata,
                "stale": True,
                "stale_dependencies": stale_dependencies,
                "stale_marked_at": timezone.now().isoformat(),
            }
            section.save(update_fields=["generation_metadata", "updated_at"])
            stale_keys.append(dependent_key)
            queue.extend(
                (child_key, dependent_key)
                for child_key in SectionWorkflowService.get_dependents(dependent_key)
            )
        return stale_keys

    @classmethod
    def regenerate_with_dependents(
        cls, report: Report, section_key: str, context: dict | None = None, user=None
    ) -> dict:
        context = context or build_report_snapshot(report.evaluation)
        report.context_payload = context
        regeneration_order = [section_key, *cls._collect_dependents(section_key)]
        existing_keys = {item.key for item in report.sections.all()}
        generated_set = existing_keys - set(regeneration_order)
        regenerated_keys: list[str] = []
        failed_sections: list[dict] = []

        for item_key in regeneration_order:
            section = report.sections.filter(key=item_key).first()
            if not section or section.is_locked:
                failed_sections.append(
                    {
                        "section_key": item_key,
                        "reason": "Seção inexistente ou bloqueada.",
                    }
                )
                continue
            if not SectionWorkflowService.can_generate(item_key, generated_set):
                failed_sections.append(
                    {
                        "section_key": item_key,
                        "reason": "Dependências não disponíveis para regeneração.",
                    }
                )
                continue

            result = ReportPipelineService._generate_single_section(report, item_key, context)
            ReportPipelineService._save_section_result(
                report,
                item_key,
                section.title,
                section.order,
                result,
            )
            current = report.sections.filter(key=item_key).first()
            metadata = current.generation_metadata or {}
            current.generation_metadata = {
                **metadata,
                "generated_at": timezone.now().isoformat(),
                "stale": False,
                "stale_dependencies": [],
            }
            current.save(update_fields=["generation_metadata", "updated_at"])
            regenerated_keys.append(item_key)
            generated_set.add(item_key)

        report.ai_metadata = {
            **(report.ai_metadata or {}),
            "last_regeneration": {
                "section_key": section_key,
                "regenerated_sections": regenerated_keys,
                "failed_sections": failed_sections,
                "regenerated_at": timezone.now().isoformat(),
            },
            "stale_sections": [
                item.key
                for item in report.sections.all()
                if (item.generation_metadata or {}).get("stale")
            ],
        }
        report.save(update_fields=["context_payload", "ai_metadata", "updated_at"])
        ReportSectionService._rebuild_report_text(report)
        ReportVersionService.create_version(report, user=user)
        return {
            "regenerated_sections": regenerated_keys,
            "failed_sections": failed_sections,
        }

    @classmethod
    def _collect_dependents(cls, section_key: str) -> list[str]:
        queue = list(SectionWorkflowService.get_dependents(section_key))
        visited: list[str] = []
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.append(current)
            queue.extend(SectionWorkflowService.get_dependents(current))
        return visited
