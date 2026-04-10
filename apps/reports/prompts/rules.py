# apps/reports/prompts/rules.py

CLINICAL_REPORT_RULES = """
# REGRAS ÉTICAS E TÉCNICAS (OBRIGATÓRIO):
1. **Linguagem Profissional**: Use terminologia clínica (ex: 'função executiva', 'desempenho mnemônico', 'limiar atencional').
2. **Coerência Baseada em Evidências**: Use APENAS os dados fornecidos no contexto. NUNCA invente resultados de testes ou diagnósticos.
3. **Sinalização de Ausência**: Se faltarem dados para uma conclusão, escreva: 'No momento, os dados são insuficientes para uma análise definitiva acerca de...'
4. **Nomenclatura**: Siga o DSM-V ou CID-11.
5. **Estilo**: Texto rico em análise clínica, evitando descrições mecanizadas de números. Converta 'Percentil 10' em 'Desempenho Inferior' ou 'Z-Score -1.5' em 'Déficit Clínico Significativo'.
"""

# apps/reports/prompts/sections.py
PROMPTS_BY_SECTION = {
    "identificacao": "Dados demográficos do paciente.",
    "demanda": "Motivo do encaminhamento e descrição da queixa principal.",
    "anamnese": "Resumo sintético da história pessoal, desenvolvimento e contexto familiar relevante.",
    "eficiencia_cognitiva": "Análise do QI (se disponível), raciocínio lógico e funcionamento cognitivo global.",
    "atencao_memoria": "Interpretação detalhada dos testes de atenção (BPA, etc) e memória (RAVLT, etc).",
    "conclusao_clinica": "Síntese dos achados. Relacionar dados observados com os resultados dos testes.",
    "conduta_sugestoes": "Recomendações terapêuticas, adaptações escolares e encaminhamentos médicos.",
}
