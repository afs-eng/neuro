from typing import Optional

from django.db.models import QuerySet

from .models import Report, ReportSection


def get_reports_by_evaluation(evaluation_id: int) -> QuerySet[Report]:
    return (
        Report.objects.with_details()
        .filter(evaluation_id=evaluation_id)
        .order_by("-updated_at")
    )


def get_report_by_id(report_id: int) -> Optional[Report]:
    return Report.objects.with_details().filter(id=report_id).first()


def get_report_section_by_id(section_id: int) -> Optional[ReportSection]:
    return ReportSection.objects.select_related("report").filter(id=section_id).first()
