import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.tests.models.applications import TestApplication
from apps.tests.registry import get_test_module
from apps.tests.base.types import TestContext

def update_all_results():
    # Instrumentos que precisam de atualização
    target_codes = ['etdah_ad', 'etdah_pais', 'fdt', 'epq_j', 'ravlt']
    
    apps = TestApplication.objects.filter(
        instrument__code__in=target_codes,
        is_validated=True
    )
    
    updated_count = 0
    print(f"Iniciando atualização de {apps.count()} registros para: {target_codes}")

    for app in apps:
        try:
            module = get_test_module(app.instrument.code)
            if not module:
                continue

            # Contexto
            ctx = TestContext(
                patient_name=app.evaluation.patient.full_name,
                evaluation_id=app.evaluation_id,
                instrument_code=app.instrument.code,
                raw_scores=app.raw_payload or {},
                reviewed_scores=app.reviewed_payload or {}
            )

            # Re-processar
            computed = module.compute(ctx)
            classified = module.classify(computed)
            
            # Alguns módulos podem não ter interpret() implementado se for apenas via classificar_payload
            try:
                interpretation = module.interpret(ctx, {**computed, **classified})
            except Exception:
                interpretation = app.interpretation_text

            # Atualizar e salvar
            app.computed_payload = computed
            app.classified_payload = classified
            app.interpretation_text = interpretation
            app.save(update_fields=['computed_payload', 'classified_payload', 'interpretation_text', 'updated_at'])
            
            updated_count += 1
            if updated_count % 20 == 0:
                print(f"Processados {updated_count} registros...")

        except Exception as e:
            print(f"Erro ao processar {app.instrument.code} ID {app.id}: {str(e)}")

    print(f"Sucesso! {updated_count} registros sincronizados com as novas lógicas de precisão e classificação.")

if __name__ == "__main__":
    update_all_results()
