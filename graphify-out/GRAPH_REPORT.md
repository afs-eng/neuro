# Graph Report - neuro  (2026-05-05)

## Corpus Check
- 598 files · ~446,267 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2885 nodes · 6178 edges · 71 communities detected
- Extraction: 69% EXTRACTED · 31% INFERRED · 0% AMBIGUOUS · INFERRED: 1928 edges (avg confidence: 0.73)
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
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 120|Community 120]]
- [[_COMMUNITY_Community 121|Community 121]]
- [[_COMMUNITY_Community 146|Community 146]]
- [[_COMMUNITY_Community 173|Community 173]]
- [[_COMMUNITY_Community 268|Community 268]]

## God Nodes (most connected - your core abstractions)
1. `_rebuild_qualitative_section()` - 72 edges
2. `_build_adolescent_document()` - 70 edges
3. `split()` - 62 edges
4. `WAIS3NormLoader` - 51 edges
5. `ReportExportChartSanitizationTests` - 51 edges
6. `testContext()` - 49 edges
7. `TestContext` - 41 edges
8. `find()` - 40 edges
9. `Pt()` - 36 edges
10. `Patient` - 32 edges

## Surprising Connections (you probably didn't know these)
- `split()` --calls--> `getUserInitials()`  [INFERRED]
  apps/common/templatetags/form_helpers.py → neuro-frontend/components/layout/AppHeader.tsx
- `split()` --calls--> `getGreeting()`  [INFERRED]
  apps/common/templatetags/form_helpers.py → neuro-frontend/app/dashboard/page.tsx
- `split()` --calls--> `formatDisplayDate()`  [INFERRED]
  apps/common/templatetags/form_helpers.py → neuro-frontend/app/dashboard/evaluations/[id]/overview/page.tsx
- `split()` --calls--> `env_list()`  [INFERRED]
  apps/common/templatetags/form_helpers.py → config/settings/base.py
- `getInstrumentAgeRangeLabel()` --calls--> `find()`  [INFERRED]
  neuro-frontend/app/dashboard/evaluations/[id]/overview/page.tsx → config/staticfiles/admin/js/vendor/jquery/jquery.js

## Communities

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (233): getDisplayName(), getUserInitials(), _calcular_idade(), split(), find(), Pt(), remove(), formatClassification() (+225 more)

### Community 1 - "Community 1"
Cohesion: 0.03
Nodes (139): gerar_grafico_bpa(), gerar_grafico_bpa_bytes(), _render_bpa_chart(), analyze_supplementary(), _b6_columns_for_age(), _b7_column_for_age(), _build_below_threshold_reason(), _build_discrepancy_interpretation() (+131 more)

### Community 2 - "Community 2"
Cohesion: 0.02
Nodes (116): check(), ensure_available(), _timeout(), AILogService, log_generation_end(), log_generation_error(), log_generation_start(), build_anamnesis_snapshot() (+108 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (93): get_instrument_age_rule(), create_test_application(), update_test_application(), BaseTestModule, classify_cars2_hf(), CARS2HFModule, MCHATModule, bai_result() (+85 more)

### Community 4 - "Community 4"
Cohesion: 0.03
Nodes (93): BaseModel, _build_chart_series_item(), build_fdt_charts(), _build_scale_result(), calcular_escore(), calcular_pontuacoes(), calculate_derived_scores(), calculate_error_result() (+85 more)

### Community 5 - "Community 5"
Cohesion: 0.03
Nodes (92): A(), Ae(), B(), Be(), c(), $e(), ee(), F() (+84 more)

### Community 6 - "Community 6"
Cohesion: 0.03
Nodes (85): EvaluationAdmin, EvaluationDocumentAdmin, AIHealthcheckService, AnamnesisChannel, AnamnesisInvite, AnamnesisInviteQuerySet, AnamnesisInviteStatus, AnamnesisResponse (+77 more)

### Community 7 - "Community 7"
Cohesion: 0.04
Nodes (103): Migration, seed_templates_v2(), get_default_templates(), create_admin(), can_access_evaluation(), can_edit(), can_edit_documents(), can_edit_evaluations() (+95 more)

### Community 8 - "Community 8"
Cohesion: 0.04
Nodes (79): calculate_raw_scores(), classificar_percentil(), classify_guilmette(), compute_scared_scores(), formatar_percentil_e_classificacao(), inverter_pontuacao(), manual_percentile_from_raw(), percentile_guilmette() (+71 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (91): Meta, TestApplication, TestApplicationQuerySet, Preview WAIS-III results without saving to database.          This endpoint is u, Preview WAIS-III results without saving to database.          This endpoint is u, Preview WAIS-III results without saving to database.          This endpoint is u, Instrument, Meta (+83 more)

### Community 10 - "Community 10"
Cohesion: 0.03
Nodes (64): BaseCommand, Command, Management command to create an admin user from environment variables., Command, build_js(), main(), merge(), Merge user data over defaults recursively for top-level keys. (+56 more)

### Community 11 - "Community 11"
Cohesion: 0.04
Nodes (72): _age_metric(), buscar_ponderado(), calculate_confidence_interval(), calculate_index_score(), calculate_qi_total(), _carregar_tabela_equivalente(), _carregar_tabela_ncp(), _composite_result() (+64 more)

### Community 12 - "Community 12"
Cohesion: 0.03
Nodes (41): checker(), clearAcross(), hide(), ready(), reset(), show(), showClear(), showQuestion() (+33 more)

### Community 13 - "Community 13"
Cohesion: 0.04
Nodes (26): buildStatusSummary(), calcularEscores(), clearForm(), fetchData(), fetchEvaluation(), fetchResult(), formatAppliedOn(), formatNumber() (+18 more)

### Community 14 - "Community 14"
Cohesion: 0.05
Nodes (50): AbstractUser, UserAdmin, BearerAuth, BaseUserAdmin, create_user_endpoint(), forgot_password(), list_users(), login() (+42 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (37): BAICalculator, calculate_percentile_from_t(), estimate_confidence_interval(), estimate_percentile(), estimate_t_score(), Calcula a partir de um dicionário simples (uso via TestContext)., Calcula percentil a partir do escore T usando distribuição normal padrão., Intervalo de confiança estimado (±5 pontos T). (+29 more)

### Community 16 - "Community 16"
Cohesion: 0.06
Nodes (34): classify_srs2_scores(), _acquisition_phrase(), _build_ravlt_chart_payload(), _clinical_summary(), _consolidation_phrase(), _efficiency_phrase(), _expected_phrase(), _first_name() (+26 more)

### Community 17 - "Community 17"
Cohesion: 0.05
Nodes (23): build_computed_payload(), calculate_factor_score(), calculate_raw_total(), compute_srs2_scores(), convert_raw_to_norms(), convert_response(), get_factor_name(), get_highest_domains() (+15 more)

### Community 18 - "Community 18"
Cohesion: 0.06
Nodes (32): calculateAge(), fetchPatientData(), formatDisplayDate(), getInstrumentAgeRangeLabel(), getInstrumentAgeRestriction(), getPatientAgeNumber(), handleBuildReport(), handleCancelAnamnesis() (+24 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (30): _adolescent_history_sections(), _age_years(), _anamnesis_summary(), _answers_payload(), _build_conclusion_text(), _build_filiation(), _build_wisc4_adolescent_conclusion(), _clean_clinical_interpretation() (+22 more)

### Community 20 - "Community 20"
Cohesion: 0.06
Nodes (15): AppConfig, AccountsConfig, AiConfig, AnamnesisConfig, ApiConfig, AuditConfig, CommonConfig, DocumentsConfig (+7 more)

### Community 21 - "Community 21"
Cohesion: 0.09
Nodes (22): _calculate_clusters(), classify_wais3_payload(), _classify_wechsler(), _estimate_cpi(), _load_cluster_table(), _load_gai_table(), Load GAI table from CSV., Load cluster table from CSV. (+14 more)

### Community 22 - "Community 22"
Cohesion: 0.11
Nodes (18): calculate_total(), classify_score(), get_age_group(), get_norms_dir(), load_table(), find_strengths_weaknesses(), SubtestCode, SubtestConfig (+10 more)

### Community 23 - "Community 23"
Cohesion: 0.08
Nodes (11): Boolean(), DateField(), FieldRenderer(), formatDateForDisplay(), normalizeOptions(), getGenerationDetails(), getPercentileWidth(), handleLogin() (+3 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (16): ABC, ICalculator, IClassifier, IInterpreter, IValidator, Protocol, AgeGroup, ClassificationResult (+8 more)

### Community 25 - "Community 25"
Cohesion: 0.15
Nodes (17): PatientAdmin, can_access_patient(), can_edit_patients(), can_view_patients(), create_patient_endpoint(), delete_patient_endpoint(), get_patient_endpoint(), list_patients() (+9 more)

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
Cohesion: 0.17
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
Cohesion: 0.29
Nodes (3): fetchAPI(), resolveApiUrl(), stringifyApiError()

### Community 34 - "Community 34"
Cohesion: 0.57
Nodes (6): compareEvaluationsByDeadline(), formatDate(), getDaysUntil(), getEvaluationDeadlineMeta(), getToday(), parseDateValue()

### Community 35 - "Community 35"
Cohesion: 0.33
Nodes (1): AIGuard

### Community 36 - "Community 36"
Cohesion: 0.4
Nodes (1): getUserInitials()

### Community 39 - "Community 39"
Cohesion: 0.5
Nodes (3): InstrumentAdmin, TestApplicationAdmin, TestInterpretationTemplateAdmin

### Community 40 - "Community 40"
Cohesion: 0.5
Nodes (1): Migration

### Community 41 - "Community 41"
Cohesion: 0.5
Nodes (1): Migration

### Community 44 - "Community 44"
Cohesion: 0.67
Nodes (2): saveDraft(), submitResponse()

### Community 45 - "Community 45"
Cohesion: 0.5
Nodes (1): getGreeting()

### Community 46 - "Community 46"
Cohesion: 0.83
Nodes (3): cycleTheme(), initTheme(), setTheme()

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (2): main(), Run administrative tasks.

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (1): Migration

### Community 51 - "Community 51"
Cohesion: 0.67
Nodes (2): get_param(), Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp

### Community 52 - "Community 52"
Cohesion: 1.0
Nodes (2): convert_one(), main()

### Community 55 - "Community 55"
Cohesion: 0.67
Nodes (1): Page()

### Community 62 - "Community 62"
Cohesion: 1.0
Nodes (1): Migration

### Community 63 - "Community 63"
Cohesion: 1.0
Nodes (1): Migration

### Community 64 - "Community 64"
Cohesion: 1.0
Nodes (1): Migration

### Community 65 - "Community 65"
Cohesion: 1.0
Nodes (1): Migration

### Community 66 - "Community 66"
Cohesion: 1.0
Nodes (1): Migration

### Community 67 - "Community 67"
Cohesion: 1.0
Nodes (1): Migration

### Community 68 - "Community 68"
Cohesion: 1.0
Nodes (1): Migration

### Community 69 - "Community 69"
Cohesion: 1.0
Nodes (1): Migration

### Community 70 - "Community 70"
Cohesion: 1.0
Nodes (1): Migration

### Community 71 - "Community 71"
Cohesion: 1.0
Nodes (1): Migration

### Community 73 - "Community 73"
Cohesion: 1.0
Nodes (1): Migration

### Community 74 - "Community 74"
Cohesion: 1.0
Nodes (1): Migration

### Community 75 - "Community 75"
Cohesion: 1.0
Nodes (1): Migration

### Community 76 - "Community 76"
Cohesion: 1.0
Nodes (1): Migration

### Community 79 - "Community 79"
Cohesion: 1.0
Nodes (1): Migration

### Community 83 - "Community 83"
Cohesion: 1.0
Nodes (1): Migration

### Community 84 - "Community 84"
Cohesion: 1.0
Nodes (1): Migration

### Community 85 - "Community 85"
Cohesion: 1.0
Nodes (1): Migration

### Community 120 - "Community 120"
Cohesion: 1.0
Nodes (1): ASGI config for config project.  It exposes the ASGI callable as a module-level

### Community 121 - "Community 121"
Cohesion: 1.0
Nodes (1): WSGI config for config project.  It exposes the WSGI callable as a module-level

### Community 146 - "Community 146"
Cohesion: 1.0
Nodes (1): Classifica o escore T do BAI conforme faixas normativas.

### Community 173 - "Community 173"
Cohesion: 1.0
Nodes (1): Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent

### Community 268 - "Community 268"
Cohesion: 1.0
Nodes (1): Case reproduzindo os dados do WAIS-III 2020 para um adulto de 30 anos.      Os v

## Knowledge Gaps
- **101 isolated node(s):** `Run administrative tasks.`, `SchoolingLevel`, `Migration`, `Migration`, `Migration` (+96 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 29`** (12 nodes): `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `page.tsx`, `TestEditPage()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 30`** (10 nodes): `Migration`, `seed_templates()`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`, `0001_initial.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 32`** (9 nodes): `env_bool()`, `env_list()`, `Base Django settings shared across environments.`, `base.py`, `__init__.py`, `local.py`, `production.py`, `_append_unique()`, `_hostname_from_url()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 35`** (6 nodes): `__init__.py`, `AIGuard`, `check_output_length()`, `sanitize_output()`, `validate_data_safety()`, `validate_no_clinical_decision()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 36`** (5 nodes): `getDisplayName()`, `getRole()`, `getUserInitials()`, `handleLogout()`, `AppHeader.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 40`** (4 nodes): `add_wais3_instrument()`, `Migration`, `remove_wais3_instrument()`, `0003_add_wais3_instrument.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 41`** (4 nodes): `deactivate_v1_templates()`, `Migration`, `reactivate_v1_templates()`, `0003_deactivate_v1_templates.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 44`** (4 nodes): `saveDraft()`, `submitResponse()`, `updateField()`, `InternalAnamnesisEditor.tsx`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 45`** (4 nodes): `page.tsx`, `getGreeting()`, `initDashboard()`, `StatusBadge()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 47`** (3 nodes): `main()`, `manage.py`, `Run administrative tasks.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 48`** (3 nodes): `Migration`, `seed_default_instruments()`, `0002_seed_default_instruments.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 51`** (3 nodes): `utils.py`, `get_param()`, `Get a parameter from JSON body (if sent) or from form POST data.      Keeps endp`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 52`** (3 nodes): `convert_one()`, `main()`, `convert_csvs_to_xlsm.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 55`** (3 nodes): `page.tsx`, `page.tsx`, `Page()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 62`** (2 nodes): `Migration`, `0008_patient_responsible_name_patient_responsible_phone.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 63`** (2 nodes): `Migration`, `0004_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 64`** (2 nodes): `Migration`, `0005_remove_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 65`** (2 nodes): `Migration`, `0011_patient_created_by.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 66`** (2 nodes): `Migration`, `0003_alter_patient_schooling.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 67`** (2 nodes): `Migration`, `0010_alter_patient_responsible_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 68`** (2 nodes): `Migration`, `0007_remove_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 69`** (2 nodes): `Migration`, `0009_alter_patient_notes_null.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 70`** (2 nodes): `Migration`, `0002_patient_grade_year_patient_institution.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 71`** (2 nodes): `Migration`, `0006_alter_patient_occupation.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 73`** (2 nodes): `Migration`, `0007_user_two_factor_fields.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 74`** (2 nodes): `Migration`, `0005_user_sex.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 75`** (2 nodes): `Migration`, `0003_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 76`** (2 nodes): `Migration`, `0004_alter_user_crp_alter_user_email.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 79`** (2 nodes): `Migration`, `0002_evaluationprogressentry.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 83`** (2 nodes): `Migration`, `0003_report_interested_party_report_purpose.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 84`** (2 nodes): `Migration`, `0002_alter_reportsection_options_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 85`** (2 nodes): `Migration`, `0004_report_ai_metadata_reportsection_generation_metadata_and_more.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 120`** (2 nodes): `ASGI config for config project.  It exposes the ASGI callable as a module-level`, `asgi.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 121`** (2 nodes): `wsgi.py`, `WSGI config for config project.  It exposes the WSGI callable as a module-level`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 146`** (1 nodes): `Classifica o escore T do BAI conforme faixas normativas.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 173`** (1 nodes): `Verifica se a avaliação possui dados mínimos para gerar um laudo clínico coerent`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 268`** (1 nodes): `Case reproduzindo os dados do WAIS-III 2020 para um adulto de 30 anos.      Os v`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `split()` connect `Community 0` to `Community 1`, `Community 2`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 10`, `Community 11`, `Community 12`, `Community 13`, `Community 14`, `Community 16`, `Community 18`, `Community 19`, `Community 22`, `Community 23`, `Community 32`, `Community 34`, `Community 36`, `Community 45`?**
  _High betweenness centrality (0.135) - this node is a cross-community bridge._
- **Why does `testContext()` connect `Community 3` to `Community 0`, `Community 1`, `Community 10`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `TestContext` connect `Community 3` to `Community 4`, `Community 9`, `Community 10`, `Community 15`, `Community 22`, `Community 24`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 133 inferred relationships involving `str` (e.g. with `_totp_code()` and `login()`) actually correct?**
  _`str` has 133 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `_rebuild_qualitative_section()` (e.g. with `.test_rebuild_qualitative_section_for_wasi_omits_missing_sections()` and `.test_rebuild_qualitative_section_for_wasi_preserves_native_template_charts()`) actually correct?**
  _`_rebuild_qualitative_section()` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `_build_adolescent_document()` (e.g. with `.test_build_adolescent_document_uses_model_wisc4_titles_when_optional_tests_are_missing()` and `str`) actually correct?**
  _`_build_adolescent_document()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `split()` (e.g. with `display_name()` and `initials()`) actually correct?**
  _`split()` has 61 INFERRED edges - model-reasoned connections that need verification._