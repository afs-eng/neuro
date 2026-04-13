import { Patient } from './patient'
export type { Patient }

// ============================================================
// Evaluation
// ============================================================

export interface ClinicalChecklist {
  anamnesis_completed: boolean
  anamnesis_reviewed: boolean
  has_relevant_documents: boolean
  has_progress_entries_for_report: boolean
  has_validated_tests: boolean
  ready_for_report: boolean
}

export interface Evaluation {
  id: number
  code: string
  title: string
  patient_id: number
  patient_name: string
  patient_birth_date: string | null
  patient_sex: string | null
  patient_responsible_name: string | null
  examiner_name: string | null
  referral_reason: string
  evaluation_purpose: string
  clinical_hypothesis: string
  start_date: string | null
  end_date: string | null
  status: string
  status_display: string
  priority: string
  priority_display: string
  is_archived: boolean
  general_notes: string
  clinical_checklist: ClinicalChecklist
  created_at: string
}

// ============================================================
// Instruments
// ============================================================

export interface Instrument {
  id: number
  code: string
  name: string
  category: string
  version: string
  is_active: boolean
  min_age?: number | null
  max_age?: number | null
  age_message?: string
}

// ============================================================
// Test Application
// ============================================================

export interface TestApplication {
  id: number
  evaluation_id: number
  instrument_id: number
  instrument_name: string
  instrument_code: string
  applied_on: string | null
  is_validated: boolean
  status: string
  raw_payload: Record<string, unknown>
  computed_payload: Record<string, unknown>
  classified_payload: Record<string, unknown>
  reviewed_payload: Record<string, unknown> | null
  interpretation_text: string
}

// ============================================================
// Documents
// ============================================================

export interface EvaluationDocument {
  id: number
  evaluation_id: number
  patient_id: number
  title: string
  file_name: string
  file_url: string
  document_type: string
  document_type_display: string
  source: string
  document_date: string | null
  notes: string
  is_relevant_for_report: boolean
  created_at: string
}

// ============================================================
// Progress Entries
// ============================================================

export interface ProgressEntry {
  id: number
  evaluation_id: number
  patient_id: number
  professional_id: number
  professional_name: string
  entry_type: string
  entry_type_display: string
  entry_date: string
  start_time: string | null
  end_time: string | null
  objective: string
  tests_applied: string
  observed_behavior: string
  clinical_notes: string
  next_steps: string
  include_in_report: boolean
  created_at: string
}

// ============================================================
// Reports
// ============================================================

export interface ReportSection {
  id: number
  key: string
  title: string
  order: number
  source_payload: Record<string, unknown>
  generated_text: string
  edited_text: string
  is_locked: boolean
}

export interface Report {
  id: number
  evaluation_id: number
  patient_id: number
  author_id: number
  author_name: string
  title: string
  interested_party: string
  purpose: string
  status: string
  snapshot_payload: Record<string, unknown>
  final_text: string
  created_at: string
  updated_at: string
  sections?: ReportSection[]
}

// ============================================================
// Anamnesis
// ============================================================

export interface AnamnesisTemplate {
  id: number
  code: string
  name: string
  target_type: string
  version: string
  schema_payload: Record<string, any>
  is_active: boolean
}

export interface AnamnesisInvite {
  id: number
  evaluation_id: number
  patient_id: number
  template_id: number
  template_name: string
  template_target_type: string
  recipient_name: string
  recipient_email: string
  recipient_phone: string
  channel: string
  token: string
  public_url: string
  status: string
  sent_at: string | null
  opened_at: string | null
  last_activity_at: string | null
  completed_at: string | null
  expires_at: string | null
  created_by_name: string
  created_at: string
  message: string
  delivery_payload: Record<string, any>
}

export interface AnamnesisResponse {
  id: number
  invite_id: number | null
  evaluation_id: number
  patient_id: number
  template_id: number
  template_name: string
  response_type: string
  source: string
  status: string
  answers_payload: Record<string, any>
  summary_payload: Record<string, any>
  submitted_by_name: string
  submitted_by_relation: string
  submitted_at: string | null
  reviewed_at: string | null
  reviewed_by: string | null
  created_at: string
}

export interface CurrentAnamnesisSummary {
  response_id: number
  status: string
  source: string
  response_type: string
  template_name: string
  submitted_by_name: string
  submitted_by_relation: string
  submitted_at: string | null
  reviewed_at: string | null
  summary_payload: Record<string, any>
}

// ============================================================
// User
// ============================================================

export interface User {
  id: number
  username: string
  email: string
  full_name: string
  specialty?: string
  role?: string
  sex?: string
  is_active: boolean
  created_at: string
}
