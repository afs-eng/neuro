# Graph Report - neuro  (2026-04-28)

## Corpus Check
- 572 files · ~414,881 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2630 nodes · 5257 edges · 67 communities detected
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 1456 edges (avg confidence: 0.73)
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
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 95|Community 95]]
- [[_COMMUNITY_Community 99|Community 99]]
- [[_COMMUNITY_Community 100|Community 100]]
- [[_COMMUNITY_Community 101|Community 101]]
- [[_COMMUNITY_Community 103|Community 103]]
- [[_COMMUNITY_Community 104|Community 104]]
- [[_COMMUNITY_Community 105|Community 105]]
- [[_COMMUNITY_Community 106|Community 106]]
- [[_COMMUNITY_Community 107|Community 107]]
- [[_COMMUNITY_Community 108|Community 108]]
- [[_COMMUNITY_Community 109|Community 109]]
- [[_COMMUNITY_Community 110|Community 110]]
- [[_COMMUNITY_Community 111|Community 111]]
- [[_COMMUNITY_Community 112|Community 112]]
- [[_COMMUNITY_Community 115|Community 115]]
- [[_COMMUNITY_Community 116|Community 116]]
- [[_COMMUNITY_Community 117|Community 117]]
- [[_COMMUNITY_Community 164|Community 164]]
- [[_COMMUNITY_Community 172|Community 172]]

## God Nodes (most connected - your core abstractions)
1. `_build_adolescent_document()` - 64 edges
2. `split()` - 58 edges
3. `_rebuild_qualitative_section()` - 47 edges
4. `find()` - 39 edges
5. `testContext()` - 38 edges
6. `TestContext` - 34 edges
7. `Pt()` - 34 edges
8. `Patient` - 30 edges
9. `Preview WAIS-III results without saving to database.          This endpoint is u` - 29 edges
10. `WAIS3NormLoader` - 29 edges

## Surprising Connections (you probably didn't know these)
- `handleRegenerateWiscSubscales()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/reports/[id]/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js
- `handleRegenerateTests()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/reports/[id]/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js
- `formatDisplayDate()` --calls--> `split()`  [INFERRED]
  neuro-frontend/app/dashboard/evaluations/[id]/overview/page.tsx → apps/common/templatetags/form_helpers.py
- `getInstrumentAgeRangeLabel()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/evaluations/[id]/overview/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js
- `split()` --calls--> `env_list()`  [INFERRED]
  apps/common/templatetags/form_helpers.py → config/settings/base.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (198): getDisplayName(), getUserInitials(), _calcular_idade(), split(), find(), Pt(), formatClassification(), getGreeting() (+190 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (125): check(), ensure_available(), _timeout(), AILogService, log_generation_end(), log_generation_error(), log_generation_start(), generate() (+117 more)

### Community 2 - "Community 2"
Cohesion: 0.04
Nodes (91): get_instrument_age_rule(), create_test_application(), update_test_application(), BaseTestModule, compute_scared_scores(), classify_scared_scores(), MCHATModule, bai_result() (+83 more)

### Community 3 - "Community 3"
Cohesion: 0.03
Nodes (106): gerar_grafico_bpa(), gerar_grafico_bpa_bytes(), _render_bpa_chart(), analyze_supplementary(), compute_wais3_payload(), _load_b1(), _load_b3(), _load_b6() (+98 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (89): A(), Ae(), B(), Be(), c(), $e(), ee(), F() (+81 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (75): EvaluationAdmin, EvaluationDocumentAdmin, PatientAdmin, AIHealthcheckService, Meta, TestApplication, TestApplicationQuerySet, can_edit_documents() (+67 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (78): checker(), clearAcross(), hide(), ready(), reset(), show(), showClear(), showQuestion() (+70 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (94): Migration, seed_templates_v2(), build_anamnesis_snapshot(), get_default_templates(), create_admin(), build_documents_snapshot(), can_access_evaluation(), can_edit() (+86 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (68): calculate_raw_scores(), classificar_percentil(), classify_guilmette(), formatar_percentil_e_classificacao(), inverter_pontuacao(), manual_percentile_from_raw(), normal_cdf(), percentile_guilmette() (+60 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (78): Preview WAIS-III results without saving to database.          This endpoint is u, Schema, AIHealthErrorOut, AIHealthOut, AnamnesisInviteCreateIn, AnamnesisInviteOut, AnamnesisResponseCreateIn, AnamnesisResponseOut (+70 more)

### Community 10 - "Community 10"
Cohesion: 0.03
Nodes (31): fetchAPI(), resolveApiUrl(), stringifyApiError(), Boolean(), DateField(), FieldRenderer(), formatDateForDisplay(), normalizeOptions() (+23 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (52): BaseModel, _build_chart_series_item(), build_fdt_charts(), calcular_escore(), calcular_pontuacoes(), calculate_derived_scores(), calculate_error_result(), calculate_fdt_results() (+44 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (44): BAICalculator, calculate_percentile_from_t(), estimate_confidence_interval(), estimate_percentile(), estimate_t_score(), Calcula a partir de um dicionário simples (uso via TestContext)., Calcula percentil a partir do escore T usando distribuição normal padrão., Intervalo de confiança estimado (±5 pontos T). (+36 more)

### Community 13 - "Community 13"
Cohesion: 0.03
Nodes (29): Data(), leverageNative(), $(), He(), addPopupIndex(), dismissAddRelatedObjectPopup(), dismissChangeRelatedObjectPopup(), dismissDeleteRelatedObjectPopup() (+21 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (52): AbstractUser, UserAdmin, BearerAuth, BaseUserAdmin, create_user_endpoint(), forgot_password(), list_users(), login() (+44 more)

### Community 15 - "Community 15"
Cohesion: 0.05
Nodes (25): build_computed_payload(), calculate_factor_score(), calculate_raw_total(), compute_srs2_scores(), convert_raw_to_norms(), convert_response(), get_factor_name(), get_highest_domains() (+17 more)

### Community 16 - "Community 16"
Cohesion: 0.06
Nodes (32): calculateAge(), fetchPatientData(), formatDisplayDate(), getInstrumentAgeRangeLabel(), getInstrumentAgeRestriction(), getPatientAgeNumber(), handleBuildReport(), handleCancelAnamnesis() (+24 more)

### Community 17 - "Community 17"
Cohesion: 0.06
Nodes (33): classify_srs2_scores(), _acquisition_phrase(), _build_ravlt_chart_payload(), _clinical_summary(), _consolidation_phrase(), _efficiency_phrase(), _expected_phrase(), _first_name() (+25 more)

### Community 18 - "Community 18"
Cohesion: 0.08
Nodes (33): calculate_total(), classify_score(), get_age_group(), get_norms_dir(), load_table(), find_strengths_weaknesses(), SubtestCode, SubtestConfig (+25 more)

### Community 19 - "Community 19"
Cohesion: 0.07
Nodes (23): ABC, AnthropicProvider, BaseAIProvider, BaseAIProvider, ICalculator, IClassifier, IInterpreter, IValidator (+15 more)

### Community 20 - "Community 20"
Cohesion: 0.08
Nodes (23): build_references(), build_references_text(), build_section_source_payload(), build_section_text(), normalize_section_key(), build_report_sections(), create_report(), ReferencesBuilderTests (+15 more)

### Community 21 - "Community 21"
Cohesion: 0.1
Nodes (24): buscar_ponderado(), calculate_confidence_interval(), calculate_index_score(), calculate_qi_total(), _carregar_tabela_equivalente(), _carregar_tabela_ncp(), get_classification_composto(), get_classification_padrao() (+16 more)

### Community 22 - "Community 22"
Cohesion: 0.06
Nodes (15): AppConfig, AccountsConfig, AiConfig, AnamnesisConfig, ApiConfig, AuditConfig, CommonConfig, DocumentsConfig (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.14
Nodes (27): _adolescent_history_sections(), _age_years(), _anamnesis_summary(), _answers_payload(), _build_conclusion_text(), _build_filiation(), _clean_clinical_interpretation(), _domain_clause() (+19 more)

### Community 24 - "Community 24"
Cohesion: 0.13
Nodes (8): fetchResult(), formatAppliedOn(), formatNumber(), getClassificationColor(), getClassificationStyle(), getClinicalBadgeStyle(), getFormLabel(), getScoreLabel()

### Community 25 - "Community 25"
Cohesion: 0.21
Nodes (15): can_access_patient(), can_edit_patients(), can_view_patients(), create_patient_endpoint(), delete_patient_endpoint(), get_patient_endpoint(), list_patients(), serialize_patient() (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.21
Nodes (9): CalculationError, ClassificationError, InstrumentNotFoundError, InterpretationError, InvalidAgeRangeError, InvalidEducationRangeError, NormTableNotFoundError, RawDataValidationError (+1 more)

### Community 27 - "Community 27"
Cohesion: 0.22
Nodes (3): AIProvider, AIService, get_ai_service()

### Community 28 - "Community 28"
Cohesion: 0.27
Nodes (10): send_anamnesis_invite_email(), _send_via_django_mail(), _send_via_resend(), send_anamnesis_invite_via_email(), send_anamnesis_invite_via_whatsapp(), _build_whatsapp_link(), _normalize_phone(), Send WhatsApp message via Evolution API if configured, otherwise return wa.me li (+2 more)

### Community 29 - "Community 29"
Cohesion: 0.2
Nodes (1): TestEditPage()

### Community 30 - "Community 30"
Cohesion: 0.2
Nodes (1): Migration

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (4): handleSave(), handleScoreChange(), loadApplication(), normalizeScore()

### Community 32 - "Community 32"
Cohesion: 0.25
Nodes (2): env_list(), Base Django settings shared across environments.

### Community 33 - "Community 33"
Cohesion: 0.57
Nodes (6): compareEvaluationsByDeadline(), formatDate(), getDaysUntil(), getEvaluationDeadlineMeta(), getToday(), parseDateValue()

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (1): AIGuard

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (2): saveDraft(), submitResponse()

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (3): InstrumentAdmin, TestApplicationAdmin, TestInterpretationTemplateAdmin

### Community 41 - "Community 41"
Cohesion: 0.5
Nodes (1): Migration

### Community 43 - "Community 43"
Cohesion: 0.5
Nodes (1): Migration

### Community 44 - "Community 44"
Cohesion: 0.83
Nodes (3): cycleTheme(), initTheme(), setTheme()

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 46 - "Community 46"
Cohesion: 1.0
Nodes (2): convert_one(), main()

### Community 49 - "Community 49"
Cohesion: 0.67
Nodes (1): Page()

### Community 53 - "Community 53"
Cohesion: 0.67
Nodes (1): Migration

### Community 54 - "Community 54"
Cohesion: 0.67
Nodes (2): get_param(), Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp

### Community 92 - "Community 92"
Cohesion: 1.0
Nodes (1): Migration

### Community 93 - "Community 93"
Cohesion: 1.0
Nodes (1): Migration

### Community 94 - "Community 94"
Cohesion: 1.0
Nodes (1): Migration

### Community 95 - "Community 95"
Cohesion: 1.0
Nodes (1): Migration

### Community 99 - "Community 99"
Cohesion: 1.0
Nodes (1): Migration

### Community 100 - "Community 100"
Cohesion: 1.0
Nodes (1): Migration

### Community 101 - "Community 101"
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

### Community 106 - "Community 106"
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

### Community 115 - "Community 115"
Cohesion: 1.0
Nodes (1): Migration

### Community 116 - "Community 116"
Cohesion: 1.0
Nodes (1): WSGI config for config project.  It exposes the WSGI callable as a module-level

### Community 117 - "Community 117"
Cohesion: 1.0
Nodes (1): ASGI config for config project.  It exposes the ASGI callable as a module-level

### Community 164 - "Community 164"
Cohesion: 1.0
Nodes (1): Classifica o escore T do BAI conforme faixas normativas.

### Community 172 - "Community 172"
Cohesion: 1.0
Nodes (1): Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent

## Knowledge Gaps
- **79 isolated node(s):** `Run administrative tasks.`, `Merge user data over defaults recursively for top-level keys.`, `Retorna o código Node.js completo que gera o .docx.`, `Management command to create an admin user from environment variables.`, `Migration` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (10 nodes): `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `TestEditPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (10 nodes): `Migration`, `seed_templates()`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (9 nodes): `env_bool()`, `env_list()`, `Base Django settings shared across environments.`, `base.py`, `__init__.py`, `local.py`, `production.py`, `_append_unique()`, `_hostname_from_url()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 34`** (6 nodes): `__init__.py`, `AIGuard`, `check_output_length()`, `sanitize_output()`, `validate_data_safety()`, `validate_no_clinical_decision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 39`** (4 nodes): `saveDraft()`, `submitResponse()`, `updateField()`, `InternalAnamnesisEditor.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (4 nodes): `add_wais3_instrument()`, `Migration`, `remove_wais3_instrument()`, `0003_add_wais3_instrument.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 43`** (4 nodes): `deactivate_v1_templates()`, `Migration`, `reactivate_v1_templates()`, `0003_deactivate_v1_templates.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 46`** (3 nodes): `convert_one()`, `main()`, `convert_csvs_to_xlsm.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 49`** (3 nodes): `page.tsx`, `page.tsx`, `Page()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 53`** (3 nodes): `Migration`, `seed_default_instruments()`, `0002_seed_default_instruments.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 54`** (3 nodes): `utils.py`, `get_param()`, `Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 92`** (2 nodes): `Migration`, `0007_user_two_factor_fields.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 93`** (2 nodes): `Migration`, `0003_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 94`** (2 nodes): `Migration`, `0004_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 95`** (2 nodes): `Migration`, `0005_user_sex.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 99`** (2 nodes): `Migration`, `0004_report_ai_metadata_reportsection_generation_metadata_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 100`** (2 nodes): `Migration`, `0003_report_interested_party_report_purpose.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 101`** (2 nodes): `Migration`, `0002_alter_reportsection_options_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 103`** (2 nodes): `Migration`, `0007_remove_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 104`** (2 nodes): `Migration`, `0005_remove_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 105`** (2 nodes): `Migration`, `0010_alter_patient_responsible_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 106`** (2 nodes): `Migration`, `0006_alter_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 107`** (2 nodes): `Migration`, `0008_patient_responsible_name_patient_responsible_phone.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 108`** (2 nodes): `Migration`, `0003_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 109`** (2 nodes): `Migration`, `0011_patient_created_by.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 110`** (2 nodes): `Migration`, `0009_alter_patient_notes_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 111`** (2 nodes): `Migration`, `0002_patient_grade_year_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 112`** (2 nodes): `Migration`, `0004_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 115`** (2 nodes): `Migration`, `0002_evaluationprogressentry.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 116`** (2 nodes): `wsgi.py`, `WSGI config for config project.  It exposes the WSGI callable as a module-level`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 117`** (2 nodes): `ASGI config for config project.  It exposes the ASGI callable as a module-level`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 164`** (1 nodes): `Classifica o escore T do BAI conforme faixas normativas.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 172`** (1 nodes): `Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `split()` connect `Community 0` to `Community 32`, `Community 33`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 13`, `Community 14`, `Community 16`, `Community 17`, `Community 20`, `Community 21`, `Community 23`?**
  _High betweenness centrality (0.167) - this node is a cross-community bridge._
- **Why does `testContext()` connect `Community 2` to `Community 0`, `Community 18`, `Community 3`, `Community 6`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `find()` connect `Community 0` to `Community 2`, `Community 6`, `Community 10`, `Community 13`, `Community 16`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 110 inferred relationships involving `str` (e.g. with `build_js()` and `_totp_code()`) actually correct?**
  _`str` has 110 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `_build_adolescent_document()` (e.g. with `str` and `split()`) actually correct?**
  _`_build_adolescent_document()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 57 inferred relationships involving `split()` (e.g. with `getUserInitials()` and `getDisplayName()`) actually correct?**
  _`split()` has 57 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `_rebuild_qualitative_section()` (e.g. with `.test_rebuild_qualitative_section_preserves_template_chart_for_wais3()` and `.test_rebuild_qualitative_section_uses_wais3_model_titles_and_order()`) actually correct?**
  _`_rebuild_qualitative_section()` has 3 INFERRED edges - model-reasoned connections that need verification._