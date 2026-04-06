import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.tests.models.applications import TestApplication
from apps.tests.registry import get_test_module
from apps.tests.base.types import TestContext

def update_etdah_results():
    # Buscar aplicações de ETDAH (AD e Pais)
    etdah_apps = TestApplication.objects.filter(
        instrument__code__in=['etdah_ad', 'etdah_pais'],
        is_validated=True
    )
    
    updated_count = 0
    print(f"Iniciando atualização de {etdah_apps.count()} registros...")

    for app in etdah_apps:
        try:
            module = get_test_module(app.instrument.code)
            if not module:
                print(f"Módulo não encontrado para {app.instrument.code}")
                continue

            # Criar contexto com os dados brutos já salvos
            ctx = TestContext(
                patient_name=app.evaluation.patient.full_name,
                evaluation_id=app.evaluation_id,
                instrument_code=app.instrument.code,
                raw_scores=app.raw_payload or {},
                reviewed_scores=app.reviewed_payload or {}
            )

            # Re-processar cálculos e interpretação
            computed = module.compute(ctx)
            classified = module.classify(computed)
            interpretation = module.interpret(ctx, {**computed, **classified})

            # Atualizar e salvar
            app.computed_payload = computed
            app.classified_payload = classified
            app.interpretation_text = interpretation
            app.save(update_fields=['computed_payload', 'classified_payload', 'interpretation_text', 'updated_at'])
            
            updated_count += 1
            if updated_count % 10 == 0:
                print(f"Processados {updated_count} registros...")

        except Exception as e:
            print(f"Erro ao processar App ID {app.id}: {str(e)}")

    print(f"Sucesso! {updated_count} registros atualizados com a nova lógica de percentis.")

if __name__ == "__main__":
    update_etdah_results()
