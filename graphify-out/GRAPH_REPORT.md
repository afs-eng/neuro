# Graph Report - neuro  (2026-04-29)

## Corpus Check
- 572 files · ~431,008 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2665 nodes · 5367 edges · 72 communities detected
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 1492 edges (avg confidence: 0.73)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 96|Community 96]]
- [[_COMMUNITY_Community 97|Community 97]]
- [[_COMMUNITY_Community 98|Community 98]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 113|Community 113]]
- [[_COMMUNITY_Community 114|Community 114]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 116|Community 116]]
- [[_COMMUNITY_Community 119|Community 119]]
- [[_COMMUNITY_Community 120|Community 120]]
- [[_COMMUNITY_Community 121|Community 121]]
- [[_COMMUNITY_Community 168|Community 168]]
- [[_COMMUNITY_Community 176|Community 176]]

## God Nodes (most connected - your core abstractions)
1. `_build_adolescent_document()` - 64 edges
2. `split()` - 60 edges
3. `_rebuild_qualitative_section()` - 53 edges
4. `find()` - 39 edges
5. `testContext()` - 38 edges
6. `ReportExportChartSanitizationTests` - 36 edges
7. `Pt()` - 35 edges
8. `TestContext` - 34 edges
9. `Patient` - 32 edges
10. `Preview WAIS-III results without saving to database.          This endpoint is u` - 29 edges

## Surprising Connections (you probably didn't know these)
- `getGreeting()` --calls--> `split()`  [INFERRED]
  neuro-frontend/app/dashboard/page.tsx → apps/common/templatetags/form_helpers.py
- `formatClassification()` --calls--> `normalize()`  [INFERRED]
  neuro-frontend/app/dashboard/tests/fdt/[id]/result/page.tsx → config/staticfiles/admin/js/vendor/xregexp/xregexp.js
- `toDomainKey()` --calls--> `normalize()`  [INFERRED]
  neuro-frontend/app/dashboard/tests/fdt/[id]/result/page.tsx → config/staticfiles/admin/js/vendor/xregexp/xregexp.js
- `handleRegenerateWiscSubscales()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/reports/[id]/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js
- `handleRegenerateTests()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/reports/[id]/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (212): getDisplayName(), getUserInitials(), split(), find(), Pt(), remove(), raw_score_matches_interval(), handleExportDocx() (+204 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (123): build_anamnesis_snapshot(), audit_report(), _build_audit_payload(), _call_ai(), ClinicalConsistencyAuditService, _normalize_audit_result(), _parse_json(), DataPresenceGuard (+115 more)

### Community 2 - "Community 2"
Cohesion: 0.03
Nodes (89): A(), Ae(), B(), Be(), c(), $e(), ee(), F() (+81 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (109): Migration, seed_templates_v2(), AbstractUser, UserAdmin, BearerAuth, BaseUserAdmin, get_default_templates(), create_admin() (+101 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (89): get_instrument_age_rule(), create_test_application(), update_test_application(), BaseTestModule, MCHATModule, bai_result(), bai_submit(), bpa2_result() (+81 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (69): EvaluationAdmin, EvaluationDocumentAdmin, PatientAdmin, AIHealthcheckService, AnamnesisChannel, AnamnesisInvite, AnamnesisInviteQuerySet, AnamnesisInviteStatus (+61 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (66): BaseModel, _build_chart_series_item(), build_fdt_charts(), calcular_escore(), calcular_pontuacoes(), calculate_derived_scores(), calculate_error_result(), calculate_fdt_results() (+58 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (69): calculate_raw_scores(), classificar_percentil(), classify_guilmette(), compute_scared_scores(), formatar_percentil_e_classificacao(), inverter_pontuacao(), manual_percentile_from_raw(), normal_cdf() (+61 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (85): Meta, TestApplication, TestApplicationQuerySet, Preview WAIS-III results without saving to database.          This endpoint is u, Instrument, Meta, Schema, AIHealthErrorOut (+77 more)

### Community 9 - "Community 9"
Cohesion: 0.03
Nodes (63): BaseCommand, Command, Management command to create an admin user from environment variables., Command, build_js(), main(), merge(), Merge user data over defaults recursively for top-level keys. (+55 more)

### Community 10 - "Community 10"
Cohesion: 0.03
Nodes (40): checker(), clearAcross(), hide(), ready(), reset(), show(), showClear(), showQuestion() (+32 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (45): check(), ensure_available(), _timeout(), AILogService, log_generation_end(), log_generation_error(), log_generation_start(), AnthropicProvider (+37 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (46): BAICalculator, calculate_percentile_from_t(), estimate_confidence_interval(), estimate_percentile(), estimate_t_score(), Calcula a partir de um dicionário simples (uso via TestContext)., Calcula percentil a partir do escore T usando distribuição normal padrão., Intervalo de confiança estimado (±5 pontos T). (+38 more)

### Community 13 - "Community 13"
Cohesion: 0.05
Nodes (60): buscar_ponderado(), _calcular_idade(), calculate_confidence_interval(), calculate_index_score(), calculate_qi_total(), _carregar_tabela_equivalente(), _carregar_tabela_ncp(), get_classification_composto() (+52 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (55): analyze_supplementary(), compute_wais3_payload(), _load_b1(), _load_b3(), _load_b6(), _map_faixa_b(), _map_faixa_b6(), _norm_float() (+47 more)

### Community 15 - "Community 15"
Cohesion: 0.04
Nodes (27): Boolean(), DateField(), FieldRenderer(), formatDateForDisplay(), normalizeOptions(), calcularEscores(), clearForm(), fetchData() (+19 more)

### Community 16 - "Community 16"
Cohesion: 0.05
Nodes (25): build_computed_payload(), calculate_factor_score(), calculate_raw_total(), compute_srs2_scores(), convert_raw_to_norms(), convert_response(), get_factor_name(), get_highest_domains() (+17 more)

### Community 17 - "Community 17"
Cohesion: 0.06
Nodes (32): calculateAge(), fetchPatientData(), formatDisplayDate(), getInstrumentAgeRangeLabel(), getInstrumentAgeRestriction(), getPatientAgeNumber(), handleBuildReport(), handleCancelAnamnesis() (+24 more)

### Community 18 - "Community 18"
Cohesion: 0.06
Nodes (33): classify_srs2_scores(), _acquisition_phrase(), _build_ravlt_chart_payload(), _clinical_summary(), _consolidation_phrase(), _efficiency_phrase(), _expected_phrase(), _first_name() (+25 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (10): fetchResult(), formatAppliedOn(), formatClassification(), formatNumber(), getClassificationColor(), getClassificationStyle(), getClinicalBadgeStyle(), getFormLabel() (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.06
Nodes (15): AppConfig, AccountsConfig, AiConfig, AnamnesisConfig, ApiConfig, AuditConfig, CommonConfig, DocumentsConfig (+7 more)

### Community 21 - "Community 21"
Cohesion: 0.15
Nodes (25): can_access_evaluation(), can_edit_evaluations(), can_view_evaluations(), create_evaluation_endpoint(), create_progress_entry_endpoint(), delete_evaluation_endpoint(), delete_progress_entry_endpoint(), get_evaluation_endpoint() (+17 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (16): ABC, ICalculator, IClassifier, IInterpreter, IValidator, Protocol, AgeGroup, ClassificationResult (+8 more)

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (18): get_test_module(), add_test_to_evaluation(), bpa2_form_view(), bpa2_report_view(), _calculate_age(), ebadep_a_form_view(), ebadep_a_report_view(), ebaped_ij_form_view() (+10 more)

### Community 24 - "Community 24"
Cohesion: 0.21
Nodes (15): can_access_patient(), can_edit_patients(), can_view_patients(), create_patient_endpoint(), delete_patient_endpoint(), get_patient_endpoint(), list_patients(), serialize_patient() (+7 more)

### Community 25 - "Community 25"
Cohesion: 0.21
Nodes (9): CalculationError, ClassificationError, InstrumentNotFoundError, InterpretationError, InvalidAgeRangeError, InvalidEducationRangeError, NormTableNotFoundError, RawDataValidationError (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (17): convert_a1_to_csv(), convert_composite_scores(), convert_psychometrics(), convert_supplementary(), expand_range_to_raw_scores(), main(), parse_range(), Conversor de tabelas XLSM/XLSX do WAIS-III para CSV.  Converte as tabelas normat (+9 more)

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (13): can_edit_documents(), can_view_documents(), delete_document_endpoint(), get_document_endpoint(), list_documents(), serialize_document(), update_document_endpoint(), upload_document_endpoint() (+5 more)

### Community 28 - "Community 28"
Cohesion: 0.27
Nodes (10): build(), _build_domain_text(), _build_global_text(), _first_name(), _get_wais3_test(), _has_test(), _patient_label(), _payload() (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.27
Nodes (10): send_anamnesis_invite_email(), _send_via_django_mail(), _send_via_resend(), send_anamnesis_invite_via_email(), send_anamnesis_invite_via_whatsapp(), _build_whatsapp_link(), _normalize_phone(), Send WhatsApp message via Evolution API if configured, otherwise return wa.me li (+2 more)

### Community 30 - "Community 30"
Cohesion: 0.2
Nodes (1): TestEditPage()

### Community 31 - "Community 31"
Cohesion: 0.2
Nodes (1): Migration

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (4): handleSave(), handleScoreChange(), loadApplication(), normalizeScore()

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (2): env_list(), Base Django settings shared across environments.

### Community 34 - "Community 34"
Cohesion: 0.29
Nodes (3): fetchAPI(), resolveApiUrl(), stringifyApiError()

### Community 35 - "Community 35"
Cohesion: 0.57
Nodes (6): compareEvaluationsByDeadline(), formatDate(), getDaysUntil(), getEvaluationDeadlineMeta(), getToday(), parseDateValue()

### Community 36 - "Community 36"
Cohesion: 0.33
Nodes (1): AIGuard

### Community 38 - "Community 38"
Cohesion: 0.6
Nodes (3): gerar_grafico_bpa(), gerar_grafico_bpa_bytes(), _render_bpa_chart()

### Community 41 - "Community 41"
Cohesion: 0.67
Nodes (2): saveDraft(), submitResponse()

### Community 42 - "Community 42"
Cohesion: 0.5
Nodes (1): getGreeting()

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (3): InstrumentAdmin, TestApplicationAdmin, TestInterpretationTemplateAdmin

### Community 44 - "Community 44"
Cohesion: 0.5
Nodes (1): Migration

### Community 46 - "Community 46"
Cohesion: 0.5
Nodes (1): Migration

### Community 47 - "Community 47"
Cohesion: 0.83
Nodes (3): cycleTheme(), initTheme(), setTheme()

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 49 - "Community 49"
Cohesion: 1.0
Nodes (2): convert_one(), main()

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (1): Page()

### Community 55 - "Community 55"
Cohesion: 1.0
Nodes (2): _curva_suave_fluida(), gerar_grafico_pontos_compostos()

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (1): Migration

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (2): get_param(), Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp

### Community 96 - "Community 96"
Cohesion: 1.0
Nodes (1): Migration

### Community 97 - "Community 97"
Cohesion: 1.0
Nodes (1): Migration

### Community 98 - "Community 98"
Cohesion: 1.0
Nodes (1): Migration

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (1): Migration

### Community 103 - "Community 103"
Cohesion: 1.0
Nodes (1): Migration

### Community 104 - "Community 104"
Cohesion: 1.0
Nodes (1): Migration

### Community 105 - "Community 105"
Cohesion: 1.0
Nodes (1): Migration

### Community 107 - "Community 107"
Cohesion: 1.0
Nodes (1): Migration

### Community 108 - "Community 108"
Cohesion: 1.0
Nodes (1): Migration

### Community 109 - "Community 109"
Cohesion: 1.0
Nodes (1): Migration

### Community 110 - "Community 110"
Cohesion: 1.0
Nodes (1): Migration

### Community 111 - "Community 111"
Cohesion: 1.0
Nodes (1): Migration

### Community 112 - "Community 112"
Cohesion: 1.0
Nodes (1): Migration

### Community 113 - "Community 113"
Cohesion: 1.0
Nodes (1): Migration

### Community 114 - "Community 114"
Cohesion: 1.0
Nodes (1): Migration

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (1): Migration

### Community 116 - "Community 116"
Cohesion: 1.0
Nodes (1): Migration

### Community 119 - "Community 119"
Cohesion: 1.0
Nodes (1): Migration

### Community 120 - "Community 120"
Cohesion: 1.0
Nodes (1): WSGI config for config project.  It exposes the WSGI callable as a module-level

### Community 121 - "Community 121"
Cohesion: 1.0
Nodes (1): ASGI config for config project.  It exposes the ASGI callable as a module-level

### Community 168 - "Community 168"
Cohesion: 1.0
Nodes (1): Classifica o escore T do BAI conforme faixas normativas.

### Community 176 - "Community 176"
Cohesion: 1.0
Nodes (1): Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent

## Knowledge Gaps
- **79 isolated node(s):** `Run administrative tasks.`, `Merge user data over defaults recursively for top-level keys.`, `Retorna o código Node.js completo que gera o .docx.`, `Management command to create an admin user from environment variables.`, `Migration` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 30`** (10 nodes): `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `TestEditPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 31`** (10 nodes): `Migration`, `seed_templates()`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 33`** (9 nodes): `env_bool()`, `env_list()`, `Base Django settings shared across environments.`, `base.py`, `__init__.py`, `local.py`, `production.py`, `_append_unique()`, `_hostname_from_url()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (6 nodes): `__init__.py`, `AIGuard`, `check_output_length()`, `sanitize_output()`, `validate_data_safety()`, `validate_no_clinical_decision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (4 nodes): `saveDraft()`, `submitResponse()`, `updateField()`, `InternalAnamnesisEditor.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 42`** (4 nodes): `page.tsx`, `getGreeting()`, `initDashboard()`, `StatusBadge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (4 nodes): `add_wais3_instrument()`, `Migration`, `remove_wais3_instrument()`, `0003_add_wais3_instrument.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (4 nodes): `deactivate_v1_templates()`, `Migration`, `reactivate_v1_templates()`, `0003_deactivate_v1_templates.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (3 nodes): `convert_one()`, `main()`, `convert_csvs_to_xlsm.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (3 nodes): `page.tsx`, `page.tsx`, `Page()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (3 nodes): `wisc4_pontos_compostos_linha_fluida.py`, `_curva_suave_fluida()`, `gerar_grafico_pontos_compostos()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 57`** (3 nodes): `Migration`, `seed_default_instruments()`, `0002_seed_default_instruments.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 58`** (3 nodes): `utils.py`, `get_param()`, `Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 96`** (2 nodes): `Migration`, `0007_user_two_factor_fields.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 97`** (2 nodes): `Migration`, `0003_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 98`** (2 nodes): `Migration`, `0004_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (2 nodes): `Migration`, `0005_user_sex.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (2 nodes): `Migration`, `0004_report_ai_metadata_reportsection_generation_metadata_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (2 nodes): `Migration`, `0003_report_interested_party_report_purpose.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (2 nodes): `Migration`, `0002_alter_reportsection_options_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (2 nodes): `Migration`, `0007_remove_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (2 nodes): `Migration`, `0005_remove_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (2 nodes): `Migration`, `0010_alter_patient_responsible_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (2 nodes): `Migration`, `0006_alter_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (2 nodes): `Migration`, `0008_patient_responsible_name_patient_responsible_phone.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (2 nodes): `Migration`, `0003_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 113`** (2 nodes): `Migration`, `0011_patient_created_by.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 114`** (2 nodes): `Migration`, `0009_alter_patient_notes_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (2 nodes): `Migration`, `0002_patient_grade_year_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (2 nodes): `Migration`, `0004_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 119`** (2 nodes): `Migration`, `0002_evaluationprogressentry.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 120`** (2 nodes): `wsgi.py`, `WSGI config for config project.  It exposes the WSGI callable as a module-level`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 121`** (2 nodes): `ASGI config for config project.  It exposes the ASGI callable as a module-level`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 168`** (1 nodes): `Classifica o escore T do BAI conforme faixas normativas.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 176`** (1 nodes): `Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `split()` connect `Community 0` to `Community 1`, `Community 33`, `Community 3`, `Community 35`, `Community 5`, `Community 2`, `Community 7`, `Community 9`, `Community 42`, `Community 10`, `Community 13`, `Community 15`, `Community 17`, `Community 18`, `Community 26`, `Community 27`, `Community 28`?**
  _High betweenness centrality (0.183) - this node is a cross-community bridge._
- **Why does `find()` connect `Community 0` to `Community 4`, `Community 9`, `Community 10`, `Community 15`, `Community 17`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `testContext()` connect `Community 4` to `Community 0`, `Community 9`, `Community 13`, `Community 23`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 113 inferred relationships involving `str` (e.g. with `build_js()` and `_totp_code()`) actually correct?**
  _`str` has 113 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `_build_adolescent_document()` (e.g. with `.test_build_adolescent_document_renumbers_wisc4_sections_when_optional_tests_are_missing()` and `str`) actually correct?**
  _`_build_adolescent_document()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 59 inferred relationships involving `split()` (e.g. with `getUserInitials()` and `getDisplayName()`) actually correct?**
  _`split()` has 59 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `_rebuild_qualitative_section()` (e.g. with `.test_rebuild_qualitative_section_preserves_template_chart_for_wais3()` and `.test_rebuild_qualitative_section_uses_wais3_model_titles_and_order()`) actually correct?**
  _`_rebuild_qualitative_section()` has 5 INFERRED edges - model-reasoned connections that need verification._