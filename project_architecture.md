# NeuroAvalia — Report Export Architecture

## Overview

The report export system generates DOCX files from neuropsychological evaluation reports. Each report contains multiple test instruments (WASI, WAIS3, WISC4, BPA-2, RAVLT, FDT, E-TDAH-AD, SRS-2, SCARED, etc.) with embedded charts and tables.

## Key Pipeline: `ReportExportService.generate_docx_bytes`

```
ReportExportService.generate_docx_bytes(report)
  ├── ReportContextService.sync_report_context(report) → context dict
  ├── sections = { key: _sanitize_section_text(text) } for all sections
  ├── _select_template_path(report, context) → template path
  ├── Document(template) OR _build_fallback_document()
  ├── _replace_simple_sections(document, report, sections, context)
  ├── _rebuild_qualitative_section(document, sections, context)
  ├── _populate_wasi_tables(document, context)
  ├── _sanitize_generated_document(document, report, context)
  ├── _validate_patient_identity(document, report, context) → raises if contamination
  └── _populate_wasi_excel_charts(docx_bytes, context) → byte-level chart update
```

## Data Flow per Test Instrument

### WASI (Wechsler Abbreviated Scale of Intelligence)

```
Raw Scores → compute_wasi_payload() → computed_payload
                                         └── composites{ qi_verbal{qi,classification}, qi_execucao, qit_4 }
                                         └── subtests{ vc, sm, cb, rm }
                                         └── age{ years, months }

compute_wasi_payload() → classify() → classified_payload
                                         └── summary{ qi_verbal, qi_execucao, qit_4 }

classify() → interpret() → interpretation_text (AI-generated or fallback)

build_validated_tests_snapshot(evaluation) → validated_tests[]
                                         └── structured_results = classified_payload.summary
                                         └── classified_payload
                                         └── computed_payload
                                         └── clinical_interpretation

_report_export_service
  ├── _wasi_payload(test) → merge(structured_results, computed_payload)
  ├── _wasi_chart_payload(test) → [QIE, QIV, QI TOTAL] + [123.0, 115.0, 122.0]
  ├── _wasi_intro_text(test, context) → "QIT = 122, classificação Superior"
  ├── _wasi_global_bullet_parts(test) → "QIV — Média Superior"
  ├── _resolve_interpretation_text() → skips stale candidates → uses _fallback_test_interpretation
  └── _populate_wasi_excel_charts(bytes, context) → updates chart1.xml (WASI chart)
```

## Consistency Problem: Gráfico vs. Texto

### Root Cause
`clinical_interpretation` (saved AI text) could contain QI values from a previous scoring run, while `computed_payload` has the current calculated values. When `_resolve_interpretation_text` picks `clinical_interpretation` as first candidate, it returns stale text.

### Solution: Stale Detection + Candidate Reordering

1. **`_wasi_candidate_has_stale_qi(text, test_payload)`** (line 5117):
   - Extracts all 2-3 digit numbers (60-160 range) from text
   - Compares against `computed_payload.composites.{qi_verbal, qi_execucao, qit_4}.qi`
   - Returns `True` if stale QI count >= valid QI count

2. **Candidate reordering in `_resolve_interpretation_text`** (line 5157):
   ```
   clinical_interpretation (stale) → skipped
   → _fallback_test_interpretation (always fresh) → returned
   ```

3. **`_fallback_test_interpretation`** (line 5225): Added WASI handler that uses `build_wasi_interpretation(merged_data, patient_name)` with data from `computed_payload`.

## Chart Population (Byte-Level)

`_populate_wasi_excel_charts` operates on the saved DOCX bytes:

1. `_document_chart_targets(docx_bytes)` → finds all `<c:chart>` in document.xml + their rel IDs → `["word/charts/chart1.xml", ...]`
2. Iterates through chart targets, loading each chart XML, updating series data with `_update_chart_series(root, idx, categories, values)`
3. Re-zips the DOCX with modified chart XMLs
4. Sanitizes charts: removes external data references, inlines cached values

**Charts in Modelo-WASI.docx template:**
- chart1.xml → WASI QIs (QIE, QIV, QI TOTAL)
- chart2.xml → BPA-2 attention scores
- chart3.xml → RAVLT learning curve
- chart4.xml → FDT automatic process
- chart5.xml → FDT controlled process
- chart6.xml → E-TDAH-AD factors
- chart7.xml → SRS-2 scales

## Chart Preservation Bug

`_remove_empty_paragraphs` was removing paragraphs that contained chart embedding elements (`<w:drawing>`), even though the paragraph text was empty. This destroyed all 7 charts.

**Fix:** Added `if cls._paragraph_contains_chart(paragraph): continue` guard.

## Patient Identity Validation

`_validate_patient_identity` runs after `_sanitize_generated_document` and checks if any foreign patient names remain in the document body text. If found, raises `ValueError` and blocks export.

## Key Files

| File | Purpose |
|------|---------|
| `apps/reports/services/report_export_service.py` | DOCX generation, chart population, sanitization |
| `apps/reports/builders/tests_builder.py` | `build_validated_tests_snapshot()` — assembles context |
| `apps/tests/wasi/calculators.py` | `compute_wasi_payload()` — computes QI from raw scores |
| `apps/tests/wasi/interpreters.py` | `build_wasi_interpretation()` — generates fallback text |
| `apps/tests/wasi/loaders.py` | Reads CORRECAO.xlsm norms table |
| `apps/tests/services/scoring_service.py` | `process()` — compute → classify → interpret pipeline |
| `apps/reports/services/section_context_service.py` | `build_for_section()` — filters context for AI prompts |
| `apps/reports/services/report_pipeline_service.py` | Orchestrates full report generation |

## Template Files

- `apps/reports/templates_assets/laudo-modelo/Modelo-WASI.docx` — 7 native charts + 7 tables
- `apps/reports/templates_assets/laudo-modelo/Modelo-WAIS3.docx` — WAIS3 template (missing)
- `apps/reports/templates_assets/laudo-modelo/Modelo-WISC4.docx` — WISC4 template (missing)
- `apps/reports/templates_assets/laudo-modelo/PAPEL-TIMBRADO-MODELO.docx` — header/footer