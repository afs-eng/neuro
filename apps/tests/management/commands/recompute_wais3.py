from django.core.management.base import BaseCommand

from apps.tests.base.types import TestContext
from apps.tests.models.applications import TestApplication
from apps.tests.wais3 import WAIS3Module


class Command(BaseCommand):
    help = "Recalcula aplicações WAIS-III salvas"

    def add_arguments(self, parser):
        parser.add_argument("--application-id", type=int, help="Recalcula apenas uma aplicação")
        parser.add_argument("--evaluation-id", type=int, help="Filtra por avaliação")

    def handle(self, *args, **options):
        module = WAIS3Module()
        queryset = TestApplication.objects.with_details().filter(instrument__code="wais3")

        application_id = options.get("application_id")
        evaluation_id = options.get("evaluation_id")

        if application_id:
            queryset = queryset.filter(pk=application_id)
        if evaluation_id:
            queryset = queryset.filter(evaluation_id=evaluation_id)

        applications = list(queryset)
        if not applications:
            self.stdout.write(self.style.WARNING("Nenhuma aplicação WAIS-III encontrada para recalcular."))
            return

        updated = 0
        for application in applications:
            age = int(((application.raw_payload or {}).get("idade") or {}).get("anos") or 0)
            context = TestContext(
                patient_name=application.evaluation.patient.full_name,
                evaluation_id=application.evaluation_id,
                instrument_code="wais3",
                patient_age=age,
                raw_scores=application.raw_payload or {},
            )

            computed = module.compute(context)
            classified = module.classify(computed)
            interpretation = module.interpret(context, {**computed, **classified})

            application.computed_payload = computed
            application.classified_payload = classified
            application.interpretation_text = interpretation
            application.save(update_fields=["computed_payload", "classified_payload", "interpretation_text", "updated_at"])
            updated += 1

        self.stdout.write(self.style.SUCCESS(f"{updated} aplicação(ões) WAIS-III recalculada(s)."))
