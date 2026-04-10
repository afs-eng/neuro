from apps.reports.builders.snapshot_builder import build_report_snapshot


class ReportContextService:
    @staticmethod
    def build_context(evaluation) -> dict:
        return build_report_snapshot(evaluation)
