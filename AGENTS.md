## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

## Session: Correção de Exportação DOCX — Gráficos, Tabelas e Consistência de Dados

### Problema
Laudo de Leticia Bolonha Lucati apresentava inconsistência: gráfico WASI mostrava QIV=115, QIE=123, mas texto da interpretação usava QIV=118, QIE=120. Isso acontecia porque:
1. **`clinical_interpretation`** e **`summary`** do teste WASI eram gerados por IA com dados de uma avaliação anterior (stale)
2. O gráfico era populado corretamente via `computed_payload` → `_wasi_chart_payload`
3. A interpretação textual vinha da `_resolve_interpretation_text` que usava o texto salvo (stale)

### Correções Aplicadas em `apps/reports/services/report_export_service.py`

**1. `_wasi_payload` (linha 4385):** Removeu busca pela chave intermediária `"composites"` como source separado, que causava sobreposição de dados. Agora usa apenas `structured_results` e `computed_payload`.

**2. `_wasi_candidate_has_stale_qi` (novo, linha 5117):** Detecta se um texto de interpretação contém valores de QI diferentes dos computados no `computed_payload`. Usa regex `/\b(\d{2,3})\b/` para encontrar números entre 60-160, compara com os valores reais dos composites.

**3. `_resolve_interpretation_text` candidates (linha 5157):** Reordenou candidatos para:
   - `clinical_interpretation` (primeiro, pode ser stale)
   - `_fallback_test_interpretation` (sempre consistente, usa computed_payload)
   - `summary`
   - `primary_section` / `fallback_section`

**4. `_fallback_test_interpretation` (linha 5238):** Adicionou handler específico para `instrument_code == "wasi"` que usa `build_wasi_interpretation` com dados de `computed_payload`.

**5. `_remove_empty_paragraphs` (linha 2432):** Adicionou `if cls._paragraph_contains_chart(paragraph): continue` — parágrafos que contêm charts embedding (vazios em texto mas com `<w:drawing>`) não eram mais removidos. Antes o `_remove_empty_paragraphs` destruía todos os charts.

**6. `@classmethod` duplicado (linhas 4246 e 4361):** Removida duplicação de `@classmethod` nos métodos `_populate_wasi_tables` e `_fmt_fdt_num`.

### Fluxo de Dados WASI

```
TestApplication.computed_payload
  └── composites{ qi_verbal{qi:115}, qi_execucao{qi:123}, qit_4{qi:122} }
  └── subtests{ vc, sm, cb, rm }
  └── age

TestApplication.classified_payload
  └── summary{ qi_verbal, qi_execucao, qit_4 }  ← só QI + classificação

build_validated_tests_snapshot
  └── structured_results = classified_payload (summary)
  └── classified_payload = classified_payload
  └── computed_payload = computed_payload

_report_export_service
  └── _wasi_payload() → merge structured_results + computed_payload → composites{subtests, etc}
  └── _wasi_chart_payload() → usa _wasi_payload().composites → gráfico correto
  └── _wasi_intro_text() → usa _wasi_payload() → QIT correto
  └── _wasi_global_bullet_parts() → usa _wasi_payload() → bullets corretos
  └── _resolve_interpretation_text() → pula candidatos stale → usa _fallback → consistente

_template WASI (Modelo-WASI.docx)
  └── 7 charts nativos (wasi, bpa2, ravlt, fdt_auto, fdt_control, etdah_ad, srs2)
  └── 7 tabelas (WASI verbal, WASI execução, BPA-2, RAVLT, FDT, E-TDAH-AD, SRS-2)
  └── Body text com placeholders
```

### Validação: `_validate_patient_identity` (linha 2526)
Após `_sanitize_generated_document`, roda `_validate_patient_identity` que verifica se há nomes de pacientes divergentes no texto. Se encontrar, lança `ValueError` e bloqueia a exportação.

### Key Files
- `apps/reports/services/report_export_service.py` — todas as correções
- `apps/tests/wasi/interpreters.py` — `build_wasi_interpretation()` usa `merged_data.composites`
- `apps/tests/wasi/loaders.py` — lê tabela Excel (CORRECAO.xlsm) para normas
- `apps/tests/wasi/calculators.py` — `compute_wasi_payload()` populates `computed_payload`
- `apps/reports/builders/tests_builder.py` — `build_validated_tests_snapshot()` monta contexto