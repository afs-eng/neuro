class AIGuard:
    @staticmethod
    def validate_no_clinical_decision(output: str) -> tuple[bool, list[str]]:
        warnings = []
        forbidden_terms = [
            "diagnóstico",
            "diagnóstico final",
            "prescrição",
            "tratamento definitivo",
            "classificação clínica definitiva",
            "resultado final",
            "decisão clínica",
        ]
        output_lower = output.lower()
        for term in forbidden_terms:
            if term in output_lower:
                warnings.append(f"Conteúdo sensível detectado: {term}")

        return len(warnings) == 0, warnings

    @staticmethod
    def validate_data_safety(data: dict) -> tuple[bool, list[str]]:
        warnings = []
        sensitive_fields = ["cpf", "rg", "endereço", "telefone", "email"]

        for field in sensitive_fields:
            if field in data and data[field]:
                warnings.append(f"Campo sensível encontrado: {field}")

        return len(warnings) == 0, warnings

    @staticmethod
    def check_output_length(output: str, max_chars: int = 10000) -> tuple[bool, str]:
        if len(output) > max_chars:
            return False, f"Output excede {max_chars} caracteres"
        return True, ""

    @staticmethod
    def sanitize_output(output: str) -> str:
        output = output.strip()
        return output
