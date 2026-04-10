
# Laudo IA Python - Modelo Adolescente

Estrutura Python adaptada para o modelo de laudo neuropsicológico adolescente.

## O que foi ajustado

- estrutura de seções alinhada ao modelo adolescente
- inclusão de `E-TDAH-PAIS`
- inclusão de `E-TDAH-AD`
- inclusão de `EPQ-J`
- remoção de `SNAP-IV`
- remoção de `HTP`
- texto base de identificação ajustado para "Identificação da paciente"
- exemplo de uso específico para adolescente

## Estrutura principal

- `laudo_ai/schemas.py`: contexto estruturado da avaliação
- `laudo_ai/section_generators.py`: geração do rascunho por seções
- `laudo_ai/section_catalog.py`: catálogo de títulos das seções
- `laudo_ai/templates.py`: partes fixas do documento
- `laudo_ai/example_usage_adolescente.py`: exemplo de uso com contexto adolescente

## Fluxo recomendado

1. Monte o contexto estruturado da avaliação.
2. Gere o rascunho por seções.
3. Permita revisão clínica no sistema.
4. Compile o texto final.
5. Exporte para `.docx`.

## Observação

Esse pacote mantém a mesma ideia da versão anterior: usar partes fixas para seções estáveis e IA para seções interpretativas, como capacidade cognitiva global, atenção, memória, SRS-2 e conclusão.
