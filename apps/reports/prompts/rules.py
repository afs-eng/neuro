# apps/reports/prompts/rules.py

CLINICAL_REPORT_RULES = """
# REGRAS ÉTICAS E TÉCNICAS (OBRIGATÓRIO):
1. **Linguagem Profissional**: Use terminologia clínica (ex: 'função executiva', 'desempenho mnemônico', 'limiar atencional').
2. **Coerência Baseada em Evidências**: Use APENAS os dados fornecidos no contexto. NUNCA invente resultados de testes ou diagnósticos.
3. **Sinalização de Ausência**: Se faltarem dados para uma conclusão, escreva: 'No momento, os dados são insuficientes para uma análise definitiva acerca de...'
4. **Nomenclatura**: Siga o DSM-V ou CID-11.
5. **Estilo**: Texto rico em análise clínica, evitando descrições mecanizadas de números. Converta 'Percentil 10' em 'Desempenho Inferior' ou 'Z-Score -1.5' em 'Déficit Clínico Significativo'.
6. **Ortografia e Norma-Padrão**: Escreva sempre em português do Brasil, com acentuação correta, ortografia atual e redação formal compatível com a norma-padrão e com o estilo técnico de laudo psicológico/neuropsicológico.
"""

# apps/reports/prompts/sections.py
PROMPTS_BY_SECTION = {
    "identificacao": "Dados demográficos do paciente.",
    "descricao_demanda": "Motivo do encaminhamento e descrição da queixa principal.",
    "historia_pessoal": "Resumo sintético da história pessoal, desenvolvimento e contexto familiar relevante.",
    "capacidade_cognitiva_global": "Análise do QI (se disponível), raciocínio lógico e funcionamento cognitivo global.",
    "memoria_aprendizagem": "Interpretação detalhada dos testes de memória e aprendizagem disponíveis.",
    "conclusao": "Síntese dos achados. Relacionar dados observados com os resultados dos testes.",
    "sugestoes_conduta": "Recomendações terapêuticas, adaptações escolares e encaminhamentos médicos.",
}
