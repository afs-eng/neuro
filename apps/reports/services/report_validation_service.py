from apps.reports.builders.tests_builder import build_validated_tests_snapshot
from django.core.exceptions import ValidationError

class ReportValidationService:
    @staticmethod
    def validate_for_generation(evaluation):
        """
        Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerente.
        """
        errors = []
        
        # 1. Verifica Paciente
        if not evaluation.patient:
            errors.append("Avaliação sem paciente vinculado.")
            
        # 2. Verifica Testes Validados
        validated_tests = build_validated_tests_snapshot(evaluation)
        if not validated_tests:
            errors.append("Não há testes validados nesta avaliação. Valide ao menos um teste antes de gerar o laudo.")
            
        # 3. Verifica Anamnese (Apenas um warning, não bloqueia)
        # Note: A skill diz "há pelo menos um teste concluído".
        
        if errors:
            raise ValidationError(errors)
            
        return True
