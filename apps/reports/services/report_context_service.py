from apps.reports.builders.snapshot_builder import build_report_snapshot


class ReportContextService:
    @staticmethod
    def build_context(evaluation) -> dict:
        return build_report_snapshot(evaluation)

    @classmethod
    def sync_report_context(cls, report, persist: bool = True) -> dict:
        latest_context = cls.build_context(report.evaluation)
        if latest_context != (report.context_payload or {}):
            report.context_payload = latest_context
            if persist:
                report.save(update_fields=["context_payload", "updated_at"])
        return latest_context
