from .builders import (
    DEFAULT_REPORT_SECTIONS,
    build_report_snapshot,
    build_section_source_payload,
    build_section_text,
)
from .models import Report, ReportSection


def create_report(**data) -> Report:
    return Report.objects.create(**data)


def update_report(report: Report, **data) -> Report:
    for field, value in data.items():
        setattr(report, field, value)
    report.save()
    return report


def update_report_section(section: ReportSection, **data) -> ReportSection:
    for field, value in data.items():
        setattr(section, field, value)
    section.save()
    return section


def build_report_sections(report: Report) -> list[ReportSection]:
    report.status = "generating"
    report.save(update_fields=["status", "updated_at"])

    snapshot = build_report_snapshot(report.evaluation)
    report.snapshot_payload = snapshot
    report.status = "in_review"
    report.save(update_fields=["snapshot_payload", "status", "updated_at"])

    sections = []
    for order, (key, title) in enumerate(DEFAULT_REPORT_SECTIONS, start=1):
        source_payload = build_section_source_payload(key, snapshot)
        generated_text = build_section_text(key, snapshot, source_payload)
        section, _ = ReportSection.objects.update_or_create(
            report=report,
            key=key,
            defaults={
                "title": title,
                "order": order,
                "source_payload": source_payload,
                "generated_text": generated_text,
            },
        )
        sections.append(section)
    return sections
