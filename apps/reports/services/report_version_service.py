from apps.reports.models import Report, ReportVersion


class ReportVersionService:
    @staticmethod
    def create_version(report: Report, user=None):
        base_content = report.final_text or report.edited_text or report.generated_text
        next_version = (
            (report.versions.first().version_number + 1)
            if report.versions.exists()
            else 1
        )
        return ReportVersion.objects.create(
            report=report,
            version_number=next_version,
            content=base_content,
            created_by=user,
        )
