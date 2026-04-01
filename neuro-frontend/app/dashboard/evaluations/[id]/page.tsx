"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, User, Calendar, FileText, ClipboardList, FolderOpen, StickyNote, Plus, X, Send, Mail, MessageCircle, Copy, CheckCircle2 } from "lucide-react";
import { api } from "@/lib/api";

interface Instrument {
  id: number;
  code: string;
  name: string;
  category: string;
  version: string;
  is_active: boolean;
  min_age?: number | null;
  max_age?: number | null;
  age_message?: string;
}

interface Evaluation {
  id: number;
  code: string;
  title: string;
  patient_id: number;
  patient_name: string;
  patient_birth_date: string | null;
  patient_sex: string | null;
  patient_responsible_name: string | null;
  examiner_name: string | null;
  referral_reason: string;
  evaluation_purpose: string;
  clinical_hypothesis: string;
  start_date: string | null;
  end_date: string | null;
  status: string;
  status_display: string;
  priority: string;
  priority_display: string;
  is_archived: boolean;
  general_notes: string;
  tests: TestApp[];
  documents: any[];
  progress_entries: ProgressEntry[];
  current_anamnesis?: CurrentAnamnesisSummary | null;
  clinical_checklist: ClinicalChecklist;
  created_at: string;
}

interface TestApp {
  id: number;
  instrument_name: string;
  instrument_code: string;
  applied_on: string | null;
  is_validated: boolean;
  status: string;
}

interface EvaluationDocument {
  id: number;
  evaluation_id: number;
  patient_id: number;
  title: string;
  file_name: string;
  file_url: string;
  document_type: string;
  document_type_display: string;
  source: string;
  document_date: string | null;
  notes: string;
  is_relevant_for_report: boolean;
  created_at: string;
}

interface ProgressEntry {
  id: number;
  evaluation_id: number;
  patient_id: number;
  professional_id: number;
  professional_name: string;
  entry_type: string;
  entry_type_display: string;
  entry_date: string;
  start_time: string | null;
  end_time: string | null;
  objective: string;
  tests_applied: string;
  observed_behavior: string;
  clinical_notes: string;
  next_steps: string;
  include_in_report: boolean;
  created_at: string;
}

interface CurrentAnamnesisSummary {
  response_id: number;
  status: string;
  source: string;
  response_type: string;
  template_name: string;
  submitted_by_name: string;
  submitted_by_relation: string;
  submitted_at: string | null;
  reviewed_at: string | null;
  summary_payload: Record<string, any>;
}

interface ClinicalChecklist {
  anamnesis_completed: boolean;
  anamnesis_reviewed: boolean;
  has_relevant_documents: boolean;
  has_progress_entries_for_report: boolean;
  has_validated_tests: boolean;
  ready_for_report: boolean;
}

interface ReportSection {
  id: number;
  key: string;
  title: string;
  order: number;
  source_payload: Record<string, unknown>;
  generated_text: string;
  edited_text: string;
  is_locked: boolean;
}

interface ReportItem {
  id: number;
  evaluation_id: number;
  patient_id: number;
  author_id: number;
  author_name: string;
  title: string;
  interested_party: string;
  purpose: string;
  status: string;
  snapshot_payload: Record<string, unknown>;
  final_text: string;
  created_at: string;
  updated_at: string;
  sections?: ReportSection[];
}

interface AnamnesisTemplate {
  id: number;
  code: string;
  name: string;
  target_type: string;
  version: string;
  schema_payload: Record<string, any>;
  is_active: boolean;
}

interface AnamnesisInvite {
  id: number;
  evaluation_id: number;
  patient_id: number;
  template_id: number;
  template_name: string;
  template_target_type: string;
  recipient_name: string;
  recipient_email: string;
  recipient_phone: string;
  channel: string;
  token: string;
  public_url: string;
  status: string;
  sent_at: string | null;
  opened_at: string | null;
  last_activity_at: string | null;
  completed_at: string | null;
  expires_at: string | null;
  created_by_name: string;
  created_at: string;
  message: string;
  delivery_payload: Record<string, any>;
}

interface AnamnesisResponse {
  id: number;
  invite_id: number;
  evaluation_id: number;
  patient_id: number;
  template_id: number;
  template_name: string;
  answers_payload: Record<string, any>;
  status: string;
  submitted_by_name: string;
  submitted_by_relation: string;
  submitted_at: string | null;
  reviewed_by_name: string | null;
  reviewed_at: string | null;
  created_at: string;
  updated_at: string;
}

const STATUS_COLORS: Record<string, string> = {
  draft: "bg-slate-100 text-slate-700",
  collecting_data: "bg-amber-50 text-amber-700 border-amber-200",
  tests_in_progress: "bg-blue-50 text-blue-700 border-blue-200",
  scoring: "bg-purple-50 text-purple-700 border-purple-200",
  writing_report: "bg-orange-50 text-orange-700 border-orange-200",
  in_review: "bg-indigo-50 text-indigo-700 border-indigo-200",
  approved: "bg-emerald-50 text-emerald-700 border-emerald-200",
  archived: "bg-slate-100 text-slate-500",
};

type TabType = "overview" | "tests" | "anamnesis" | "documents" | "evolution" | "report";

export default function EvaluationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [showAddTestModal, setShowAddTestModal] = useState(false);
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [loadingInstruments, setLoadingInstruments] = useState(false);
  const [addingTest, setAddingTest] = useState(false);
  const [instrumentFilterError, setInstrumentFilterError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<EvaluationDocument[]>([]);
  const [anamnesisTemplates, setAnamnesisTemplates] = useState<AnamnesisTemplate[]>([]);
  const [anamnesisInvites, setAnamnesisInvites] = useState<AnamnesisInvite[]>([]);
  const [anamnesisResponses, setAnamnesisResponses] = useState<AnamnesisResponse[]>([]);
  const [selectedAnamnesisResponse, setSelectedAnamnesisResponse] = useState<AnamnesisResponse | null>(null);
  const [progressEntries, setProgressEntries] = useState<ProgressEntry[]>([]);
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportItem | null>(null);
  const [tabLoading, setTabLoading] = useState(false);
  const [pageNotice, setPageNotice] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [showDocumentForm, setShowDocumentForm] = useState(false);
  const [showAnamnesisInviteForm, setShowAnamnesisInviteForm] = useState(false);
  const [showProgressForm, setShowProgressForm] = useState(false);
  const [showReportForm, setShowReportForm] = useState(false);
  const [savingDocument, setSavingDocument] = useState(false);
  const [savingAnamnesisInvite, setSavingAnamnesisInvite] = useState(false);
  const [savingProgress, setSavingProgress] = useState(false);
  const [savingReport, setSavingReport] = useState(false);
  const [documentForm, setDocumentForm] = useState({
    title: "",
    document_type: "other",
    source: "",
    document_date: "",
    notes: "",
    is_relevant_for_report: true,
    file: null as File | null,
  });
  const [anamnesisForm, setAnamnesisForm] = useState({
    template_id: "",
    recipient_name: "",
    recipient_email: "",
    recipient_phone: "",
    channel: "email",
    expires_at: "",
    message: "",
  });
  const [progressForm, setProgressForm] = useState({
    entry_type: "anamnesis",
    entry_date: new Date().toISOString().slice(0, 10),
    start_time: "",
    end_time: "",
    objective: "",
    tests_applied: "",
    observed_behavior: "",
    clinical_notes: "",
    next_steps: "",
    include_in_report: true,
  });
  const [reportForm, setReportForm] = useState({
    title: "",
    interested_party: "",
    purpose: "",
  });

  const documentRequiredMissing = !documentForm.title || !documentForm.file;
  const anamnesisRequiredMissing = !anamnesisForm.template_id || !anamnesisForm.recipient_name || (anamnesisForm.channel === "email" ? !anamnesisForm.recipient_email : !anamnesisForm.recipient_phone);
  const progressRequiredMissing = !progressForm.entry_type || !progressForm.entry_date;
  const reportRequiredMissing = !reportForm.title;

  function isValidTab(value: string | null): value is TabType {
    return value === "overview" || value === "tests" || value === "anamnesis" || value === "documents" || value === "evolution" || value === "report";
  }

  function navigateToTab(tab: TabType) {
    setActiveTab(tab);
    router.push(`/dashboard/evaluations/${params.id}?tab=${tab}`);
  }

  useEffect(() => {
    if (typeof window === "undefined") return;
    const search = new URLSearchParams(window.location.search);
    const tab = search.get("tab");
    if (isValidTab(tab)) {
      setActiveTab(tab);
    }
  }, []);

  useEffect(() => {
    async function fetchEvaluation() {
      try {
        setErrorMessage(null);
        const data = await api.get<Evaluation>(`/api/evaluations/${params.id}`);
        setEvaluation(data);
      } catch (err: any) {
        console.error("Erro ao buscar avaliação:", err);
        if (err?.status === 401 || err?.status === 403) {
          setErrorMessage("Sua sessão não tem permissão para acessar esta avaliação. Faça login novamente.");
        } else {
          setErrorMessage(err?.message || "Não foi possível carregar a avaliação.");
        }
      } finally {
        setLoading(false);
      }
    }
    if (params.id) {
      fetchEvaluation();
    }
  }, [params.id]);

  useEffect(() => {
    if (!evaluation) return;
    if (activeTab === "anamnesis") loadAnamnesisData();
    if (activeTab === "documents") loadDocuments();
    if (activeTab === "evolution") loadProgressEntries();
    if (activeTab === "report") loadReports();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, evaluation]);

  async function loadInstruments() {
    setLoadingInstruments(true);
    try {
      const data = await api.get<Instrument[]>("/api/tests/instruments/");
      setInstruments(data);
    } catch (err: any) {
      console.error("Erro ao carregar instrumentos:", err);
      alert("Erro ao carregar instrumentos: " + (err?.message || "Ver console"));
    } finally {
      setLoadingInstruments(false);
    }
  }

  async function addTest(instrumentId: number) {
    if (!evaluation) return;
    setAddingTest(true);
    try {
      setInstrumentFilterError(null);
      const newTest = await api.post<any>("/api/tests/applications/", {
        evaluation_id: evaluation.id,
        instrument_id: instrumentId,
      });
      setEvaluation({
        ...evaluation,
        tests: [...evaluation.tests, {
          id: newTest.id,
          instrument_name: newTest.instrument_name,
          instrument_code: newTest.instrument_code,
          applied_on: newTest.applied_on,
          is_validated: newTest.is_validated,
          status: newTest.is_validated ? "Concluído" : "Pendente"
        }]
      });
      setShowAddTestModal(false);
    } catch (err: any) {
      console.error("Erro ao adicionar teste:", err);
      setInstrumentFilterError(err?.message || "Erro ao adicionar teste.");
    } finally {
      setAddingTest(false);
    }
  }

  async function loadDocuments() {
    if (!evaluation) return;
    setTabLoading(true);
    try {
      const data = await api.get<EvaluationDocument[]>(`/api/documents/?evaluation_id=${evaluation.id}`);
      setDocuments(data);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao carregar documentos." });
    } finally {
      setTabLoading(false);
    }
  }

  async function loadAnamnesisData() {
    if (!evaluation) return;
    setTabLoading(true);
    try {
      const [templates, invites, responses] = await Promise.all([
        api.get<AnamnesisTemplate[]>("/api/anamnesis/templates/"),
        api.get<AnamnesisInvite[]>(`/api/anamnesis/invites/?evaluation_id=${evaluation.id}`),
        api.get<AnamnesisResponse[]>(`/api/anamnesis/responses/?evaluation_id=${evaluation.id}`),
      ]);
      setAnamnesisTemplates(templates);
      setAnamnesisInvites(invites);
      setAnamnesisResponses(responses);
      setSelectedAnamnesisResponse((current) => current ? responses.find((item) => item.id === current.id) || null : responses[0] || null);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao carregar anamneses." });
    } finally {
      setTabLoading(false);
    }
  }

  async function handleCreateAnamnesisInvite() {
    if (!evaluation || anamnesisRequiredMissing) return;
    setSavingAnamnesisInvite(true);
    try {
      const invite = await api.post<AnamnesisInvite>("/api/anamnesis/invites/", {
        evaluation_id: evaluation.id,
        patient_id: evaluation.patient_id,
        template_id: Number(anamnesisForm.template_id),
        recipient_name: anamnesisForm.recipient_name,
        recipient_email: anamnesisForm.recipient_email,
        recipient_phone: anamnesisForm.recipient_phone,
        channel: anamnesisForm.channel,
        message: anamnesisForm.message,
        expires_at: anamnesisForm.expires_at ? new Date(anamnesisForm.expires_at).toISOString() : null,
      });
      setPageNotice({ type: "success", text: "Convite de anamnese criado com sucesso." });
      setShowAnamnesisInviteForm(false);
      setAnamnesisForm({ template_id: "", recipient_name: "", recipient_email: "", recipient_phone: "", channel: "email", expires_at: "", message: "" });
      await loadAnamnesisData();
      if (invite.channel === "email") {
        await handleSendAnamnesis(invite.id, "email");
      }
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao criar convite de anamnese." });
    } finally {
      setSavingAnamnesisInvite(false);
    }
  }

  async function handleSendAnamnesis(inviteId: number, channel: "email" | "whatsapp") {
    try {
      const endpoint = channel === "email" ? `/api/anamnesis/invites/${inviteId}/send-email` : `/api/anamnesis/invites/${inviteId}/send-whatsapp`;
      const invite = await api.post<AnamnesisInvite>(endpoint, {});
      setPageNotice({ type: "success", text: channel === "email" ? "Convite enviado por e-mail." : "Link de WhatsApp gerado e registrado." });
      await loadAnamnesisData();
      if (channel === "whatsapp" && invite.delivery_payload?.whatsapp_link) {
        window.open(String(invite.delivery_payload.whatsapp_link), "_blank");
      }
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao enviar convite." });
    }
  }

  async function handleResendAnamnesis(inviteId: number) {
    try {
      await api.post(`/api/anamnesis/invites/${inviteId}/resend`, {});
      setPageNotice({ type: "success", text: "Convite reenviado com sucesso." });
      await loadAnamnesisData();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao reenviar convite." });
    }
  }

  async function handleCancelAnamnesis(inviteId: number) {
    try {
      await api.post(`/api/anamnesis/invites/${inviteId}/cancel`, {});
      setPageNotice({ type: "success", text: "Convite cancelado com sucesso." });
      await loadAnamnesisData();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao cancelar convite." });
    }
  }

  async function handleReviewAnamnesis(responseId: number) {
    try {
      const response = await api.patch<AnamnesisResponse>(`/api/anamnesis/responses/${responseId}/review`, { status: "reviewed" });
      setPageNotice({ type: "success", text: "Resposta marcada como revisada." });
      await loadAnamnesisData();
      setSelectedAnamnesisResponse(response);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao revisar resposta." });
    }
  }

  async function copyToClipboard(text: string, successMessage: string) {
    try {
      await navigator.clipboard.writeText(text);
      setPageNotice({ type: "success", text: successMessage });
    } catch {
      setPageNotice({ type: "error", text: "Não foi possível copiar o link." });
    }
  }

  async function loadProgressEntries() {
    if (!evaluation) return;
    setTabLoading(true);
    try {
      const data = await api.get<ProgressEntry[]>(`/api/evaluations/${evaluation.id}/progress-entries`);
      setProgressEntries(data);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao carregar evolução." });
    } finally {
      setTabLoading(false);
    }
  }

  async function loadReports(selectFirst = false) {
    if (!evaluation) return;
    setTabLoading(true);
    try {
      const data = await api.get<ReportItem[]>(`/api/reports/?evaluation_id=${evaluation.id}`);
      setReports(data);
      if (selectFirst && data[0]) {
        await openReport(data[0].id);
      }
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao carregar laudos." });
    } finally {
      setTabLoading(false);
    }
  }

  async function openReport(reportId: number) {
    try {
      const data = await api.get<ReportItem>(`/api/reports/${reportId}`);
      setSelectedReport(data);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao abrir laudo." });
    }
  }

  async function handleDocumentUpload() {
    if (!evaluation || documentRequiredMissing) return;
    setSavingDocument(true);
    try {
      const formData = new FormData();
      formData.append("evaluation_id", String(evaluation.id));
      formData.append("patient_id", String(evaluation.patient_id));
      formData.append("title", documentForm.title);
      formData.append("document_type", documentForm.document_type);
      formData.append("source", documentForm.source);
      formData.append("document_date", documentForm.document_date);
      formData.append("notes", documentForm.notes);
      formData.append("is_relevant_for_report", String(documentForm.is_relevant_for_report));
      formData.append("file", documentForm.file as File);
      await api.post("/api/documents/upload", formData);
      setPageNotice({ type: "success", text: "Documento enviado com sucesso." });
      setDocumentForm({ title: "", document_type: "other", source: "", document_date: "", notes: "", is_relevant_for_report: true, file: null });
      setShowDocumentForm(false);
      loadDocuments();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao enviar documento." });
    } finally {
      setSavingDocument(false);
    }
  }

  async function handleDeleteDocument(documentId: number) {
    try {
      await api.delete(`/api/documents/${documentId}`);
      setPageNotice({ type: "success", text: "Documento excluído com sucesso." });
      loadDocuments();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao excluir documento." });
    }
  }

  async function handleCreateProgress() {
    if (!evaluation || progressRequiredMissing) return;
    setSavingProgress(true);
    try {
      await api.post("/api/evaluations/progress-entries", {
        evaluation_id: evaluation.id,
        patient_id: evaluation.patient_id,
        entry_type: progressForm.entry_type,
        entry_date: progressForm.entry_date,
        start_time: progressForm.start_time || null,
        end_time: progressForm.end_time || null,
        objective: progressForm.objective,
        tests_applied: progressForm.tests_applied,
        observed_behavior: progressForm.observed_behavior,
        clinical_notes: progressForm.clinical_notes,
        next_steps: progressForm.next_steps,
        include_in_report: progressForm.include_in_report,
      });
      setPageNotice({ type: "success", text: "Registro de evolução salvo com sucesso." });
      setProgressForm({ entry_type: "anamnesis", entry_date: new Date().toISOString().slice(0, 10), start_time: "", end_time: "", objective: "", tests_applied: "", observed_behavior: "", clinical_notes: "", next_steps: "", include_in_report: true });
      setShowProgressForm(false);
      loadProgressEntries();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao salvar evolução." });
    } finally {
      setSavingProgress(false);
    }
  }

  async function handleDeleteProgress(entryId: number) {
    try {
      await api.delete(`/api/evaluations/progress-entries/${entryId}`);
      setPageNotice({ type: "success", text: "Registro de evolução excluído com sucesso." });
      loadProgressEntries();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao excluir evolução." });
    }
  }

  async function handleCreateReport() {
    if (!evaluation || reportRequiredMissing) return;
    setSavingReport(true);
    try {
      const report = await api.post<ReportItem>("/api/reports/", {
        evaluation_id: evaluation.id,
        patient_id: evaluation.patient_id,
        title: reportForm.title,
        interested_party: reportForm.interested_party,
        purpose: reportForm.purpose,
      });
      setPageNotice({ type: "success", text: "Laudo criado com sucesso." });
      setReportForm({ title: "", interested_party: "", purpose: "" });
      setShowReportForm(false);
      await loadReports();
      await openReport(report.id);
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao criar laudo." });
    } finally {
      setSavingReport(false);
    }
  }

  async function handleBuildReport(reportId: number) {
    try {
      const report = await api.post<ReportItem>(`/api/reports/${reportId}/build`, {});
      setSelectedReport(report);
      setPageNotice({ type: "success", text: "Seções do laudo regeneradas com sucesso." });
      loadReports();
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao gerar laudo." });
    }
  }

  async function handleSaveSection(sectionId: number, editedText: string) {
    try {
      const updated = await api.patch<ReportSection>(`/api/reports/sections/${sectionId}`, { edited_text: editedText });
      if (selectedReport?.sections) {
        setSelectedReport({
          ...selectedReport,
          sections: selectedReport.sections.map((section) => section.id === sectionId ? { ...section, ...updated } : section),
        });
      }
      setPageNotice({ type: "success", text: "Seção salva com sucesso." });
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao salvar seção." });
    }
  }

  function openAddTestModal() {
    setShowAddTestModal(true);
    if (instruments.length === 0) {
      loadInstruments();
    }
  }

  function getTestUrl(instrumentCode: string, testId: number): string {
    const baseUrls: Record<string, string> = {
      "fdt": "/dashboard/tests/fdt",
      "wisc4": "/dashboard/tests/wisc4",
      "bpa2": "/dashboard/tests/bpa2",
      "ebadep_a": "/dashboard/tests/ebadep-a",
      "ebadep_ij": "/dashboard/tests/ebadep-ij",
      "ebaped_ij": "/dashboard/tests/ebadep-ij",
      "epq_j": "/dashboard/tests/epq-j",
      "etdah_ad": "/dashboard/tests/etdah-ad",
    };
    return `${baseUrls[instrumentCode] || "/dashboard/tests"}?evaluation_id=${evaluation?.id}&application_id=${testId}`;
  }

  async function removeTest(applicationId: number) {
    if (!evaluation) return;
    try {
      await api.delete(`/api/tests/applications/${applicationId}`);
      setEvaluation({
        ...evaluation,
        tests: evaluation.tests.filter((test) => test.id !== applicationId),
      });
      setPageNotice({ type: "success", text: "Teste removido com sucesso." });
    } catch (err: any) {
      setPageNotice({ type: "error", text: err?.message || "Erro ao remover teste." });
    }
  }

  function resolveReferenceDate() {
    return evaluation?.start_date || evaluation?.end_date || null;
  }

  function getPatientAge(birthDate: string | null, referenceDate?: string | null) {
    if (!birthDate) return "—";
    const birth = new Date(birthDate);
    const baseDate = referenceDate ? new Date(referenceDate) : new Date();
    if (isNaN(birth.getTime())) return "—";
    if (isNaN(baseDate.getTime())) return "—";

    let years = baseDate.getFullYear() - birth.getFullYear();
    let months = baseDate.getMonth() - birth.getMonth();

    if (baseDate.getDate() < birth.getDate()) {
      months -= 1;
    }

    if (months < 0) {
      years -= 1;
      months += 12;
    }

    if (years <= 0) {
      return `${months} ${months === 1 ? "mês" : "meses"}`;
    }

    if (months === 0) {
      return `${years} ${years === 1 ? "ano" : "anos"}`;
    }

    return `${years} ${years === 1 ? "ano" : "anos"} e ${months} ${months === 1 ? "mês" : "meses"}`;
  }

  function getPatientAgeNumber(birthDate: string | null, referenceDate?: string | null) {
    if (!birthDate) return null;
    const birth = new Date(birthDate);
    const baseDate = referenceDate ? new Date(referenceDate) : new Date();
    if (isNaN(birth.getTime()) || isNaN(baseDate.getTime())) return null;
    let age = baseDate.getFullYear() - birth.getFullYear();
    const monthDiff = baseDate.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && baseDate.getDate() < birth.getDate())) {
      age -= 1;
    }
    return age;
  }

  function formatDisplayDate(value: string | null | undefined) {
    if (!value) return "—";
    if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
      const [year, month, day] = value.split("-");
      return `${day}/${month}/${year}`;
    }
    const date = new Date(value);
    if (isNaN(date.getTime())) return "—";
    return date.toLocaleDateString("pt-BR");
  }

  function getInstrumentAgeRestriction(instrumentCode: string) {
    const age = getPatientAgeNumber(evaluation?.patient_birth_date || null, resolveReferenceDate());
    if (age === null) return null;
    const rule = instruments.find((instrument) => instrument.code === instrumentCode);
    if (!rule) return null;
    if (rule.min_age !== undefined && rule.min_age !== null && age < rule.min_age) return rule.age_message || null;
    if (rule.max_age !== undefined && rule.max_age !== null && age > rule.max_age) return rule.age_message || null;
    return null;
  }

  function getInstrumentAgeRangeLabel(instrumentCode: string) {
    const rule = instruments.find((instrument) => instrument.code === instrumentCode);
    if (!rule || (rule.min_age == null && rule.max_age == null)) return "Faixa etária não definida";
    if (rule.min_age != null && rule.max_age != null) return `${rule.min_age} a ${rule.max_age} anos`;
    if (rule.min_age != null) return `${rule.min_age}+ anos`;
    if (rule.max_age != null) return `Até ${rule.max_age} anos`;
    return "Faixa etária não definida";
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Carregando...</div>
      </div>
    );
  }

  if (!evaluation) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="max-w-lg text-center">
          <div className="text-zinc-800 font-medium">Avaliação não carregada</div>
          <div className="mt-2 text-sm text-zinc-600">{errorMessage || "Avaliação não encontrada."}</div>
          <Button className="mt-4 rounded-xl" onClick={() => router.push('/dashboard/evaluations')}>
            Voltar para avaliações
          </Button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: "overview" as TabType, label: "Visão Geral", icon: User },
    { id: "tests" as TabType, label: "Testes", icon: ClipboardList },
    { id: "anamnesis" as TabType, label: "Anamnese", icon: Send },
    { id: "documents" as TabType, label: "Documentos", icon: FolderOpen },
    { id: "evolution" as TabType, label: "Evolução", icon: StickyNote },
    { id: "report" as TabType, label: "Laudo", icon: FileText },
  ];

  const getTestesDisponiveis = () => {
    const codes = evaluation.tests.map(t => t.instrument_code);
    const disponiveis = instruments
      .map(i => ({
        code: i.code,
        name: i.name,
        id: i.id,
        ageRestriction: getInstrumentAgeRestriction(i.code),
      }))
      .filter(t => !codes.includes(t.code));

    return disponiveis.sort((a, b) => {
      const aBlocked = !!a.ageRestriction;
      const bBlocked = !!b.ageRestriction;
      if (aBlocked !== bBlocked) return aBlocked ? 1 : -1;
      return a.name.localeCompare(b.name);
    });
  };

  if (showAddTestModal) {
    const availableTests = getTestesDisponiveis();
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10">
        <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
          <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-medium">Adicionar Teste</h1>
              <Button variant="ghost" size="icon" onClick={() => setShowAddTestModal(false)}>
                <X className="h-5 w-5" />
              </Button>
            </div>
            
            <p className="text-zinc-600 mb-4">Selecione um teste para adicionar a esta avaliação:</p>
            <div className="mb-4 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
              Idade do paciente: <span className="font-semibold text-slate-900">{getPatientAge(evaluation.patient_birth_date, resolveReferenceDate())}</span>
            </div>
            {instrumentFilterError && (
              <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">
                {instrumentFilterError}
              </div>
            )}
            
            {loadingInstruments ? (
              <div className="text-center py-8">
                <p className="text-zinc-500">Carregando instrumentos...</p>
              </div>
            ) : instruments.length === 0 ? (
              <div className="text-center py-8 text-zinc-500">
                <p>Nenhum instrumento foi cadastrado no sistema.</p>
              </div>
            ) : availableTests.length === 0 ? (
              <div className="text-center py-8 text-zinc-500">
                <p>Todos os testes disponíveis já foram adicionados.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {availableTests.map((test) => {
                  const ageRestriction = test.ageRestriction
                  return (
                    <button
                      key={test.id}
                      onClick={() => addTest(test.id)}
                      disabled={addingTest || !!ageRestriction}
                      className={`p-4 text-left rounded-xl border transition disabled:opacity-60 ${ageRestriction ? "border-rose-200 bg-rose-50" : "border-slate-200 bg-white hover:bg-slate-50 hover:border-slate-300"}`}
                    >
                      <p className="font-medium">{test.name}</p>
                      <p className="text-sm text-zinc-500">{test.code}</p>
                      <p className="mt-2 text-xs text-slate-500">Faixa etária: {getInstrumentAgeRangeLabel(test.code)}</p>
                      {ageRestriction && <p className="mt-2 text-xs text-rose-700">{ageRestriction}</p>}
                    </button>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
            </nav>
          </header>

          <div className="mb-6">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-3xl font-medium tracking-tight text-zinc-900">{evaluation.code}</h1>
                  <Badge className={`${STATUS_COLORS[evaluation.status]} rounded-full`}>
                    {evaluation.status_display}
                  </Badge>
                </div>
                <p className="mt-1 text-lg text-zinc-600">{evaluation.patient_name}</p>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" className="rounded-full" onClick={() => router.push(`/dashboard/evaluations/${evaluation.id}/edit`)}>Editar</Button>
                <Button className="rounded-full" onClick={() => navigateToTab("report")}>Abrir Laudo</Button>
              </div>
            </div>
          </div>

          <div className="mb-6 flex flex-wrap gap-2 border-b border-slate-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => navigateToTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition ${
                  activeTab === tab.id
                    ? "border-zinc-900 text-zinc-900"
                    : "border-transparent text-zinc-500 hover:text-zinc-700"
                }`}
              >
                <tab.icon className="h-4 w-4" />
                {tab.label}
              </button>
            ))}
          </div>

          {pageNotice && (
            <div className={`mb-6 rounded-2xl px-4 py-3 text-sm ${pageNotice.type === "success" ? "border border-emerald-200 bg-emerald-50 text-emerald-800" : "border border-rose-200 bg-rose-50 text-rose-800"}`}>
              <div className="flex items-center justify-between gap-4">
                <span>{pageNotice.text}</span>
                <button onClick={() => setPageNotice(null)} className="text-xs font-medium opacity-80 hover:opacity-100">Fechar</button>
              </div>
            </div>
          )}

          {activeTab === "overview" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2 rounded-2xl border-slate-200 shadow-sm">
                <CardHeader>
                  <CardTitle>Dados Principais</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Nome do paciente</p>
                      <p className="mt-1 font-medium text-zinc-900">{evaluation.patient_name || "—"}</p>
                    </div>
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Idade</p>
                      <p className="mt-1 font-medium text-zinc-900">{getPatientAge(evaluation.patient_birth_date, resolveReferenceDate())}</p>
                    </div>
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Responsável</p>
                      <p className="mt-1 font-medium text-zinc-900">{evaluation.patient_responsible_name || evaluation.examiner_name || "—"}</p>
                    </div>
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Data de início</p>
                      <p className="mt-1 font-medium text-zinc-900">{formatDisplayDate(evaluation.start_date)}</p>
                    </div>
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Data da conclusão</p>
                      <p className="mt-1 font-medium text-zinc-900">{formatDisplayDate(evaluation.end_date)}</p>
                    </div>
                    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <p className="text-sm text-zinc-500">Status</p>
                      <div className="mt-2">
                        <Badge className={`${STATUS_COLORS[evaluation.status]} rounded-full`}>
                          {evaluation.status_display}
                        </Badge>
                      </div>
                    </div>
                  </div>

                  {evaluation.title && (
                    <div>
                      <p className="text-sm text-zinc-500">Título do caso</p>
                      <p className="font-medium">{evaluation.title}</p>
                    </div>
                  )}

                  {evaluation.referral_reason && (
                    <div>
                      <p className="text-sm text-zinc-500">Motivo do encaminhamento</p>
                      <p className="text-sm">{evaluation.referral_reason}</p>
                    </div>
                  )}

                  {evaluation.evaluation_purpose && (
                    <div>
                      <p className="text-sm text-zinc-500">Finalidade da avaliação</p>
                      <p className="text-sm">{evaluation.evaluation_purpose}</p>
                    </div>
                  )}

                  {evaluation.clinical_hypothesis && (
                    <div>
                      <p className="text-sm text-zinc-500">Hipótese clínica</p>
                      <p className="text-sm">{evaluation.clinical_hypothesis}</p>
                    </div>
                  )}

                  {evaluation.general_notes && (
                    <div>
                      <p className="text-sm text-zinc-500">Observações clínicas</p>
                      <p className="text-sm">{evaluation.general_notes}</p>
                    </div>
                  )}

                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="flex items-center justify-between gap-4">
                      <div>
                        <p className="text-sm text-zinc-500">Anamnese vigente</p>
                        <p className="mt-1 font-medium text-zinc-900">{evaluation.current_anamnesis?.template_name || "Nenhuma anamnese vigente"}</p>
                      </div>
                      {evaluation.current_anamnesis ? (
                        <Badge variant="outline" className={evaluation.current_anamnesis.status === "reviewed" ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"}>
                          {evaluation.current_anamnesis.status}
                        </Badge>
                      ) : null}
                    </div>
                    {evaluation.current_anamnesis?.summary_payload?.chief_complaint && (
                      <p className="mt-3 text-sm text-slate-600">{evaluation.current_anamnesis.summary_payload.chief_complaint}</p>
                    )}
                    <Button variant="outline" className="mt-4 rounded-xl" onClick={() => navigateToTab("anamnesis")}>Abrir anamnese</Button>
                  </div>
                </CardContent>
              </Card>

              <div className="space-y-4">
                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Testes Aplicados</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {evaluation.tests.length === 0 ? (
                      <p className="text-sm text-zinc-500">Nenhum teste aplicado</p>
                    ) : (
                      <div className="space-y-2">
                        {evaluation.tests.map((test) => (
                          <div key={test.id} className="flex items-center justify-between text-sm">
                            <span>{test.instrument_name}</span>
                            <Badge variant="outline" className={test.is_validated ? "bg-emerald-50" : "bg-amber-50"}>
                              {test.status}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    )}
                    <Button variant="outline" className="w-full mt-4 rounded-xl" onClick={openAddTestModal}>
                      <Plus className="h-4 w-4 mr-2" />
                      Adicionar Teste
                    </Button>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between gap-3">
                    <CardTitle className="text-base">Documentos</CardTitle>
                    <Button variant="ghost" size="sm" onClick={() => navigateToTab("anamnesis")}>Anamnese</Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    {evaluation.documents.length === 0 ? (
                      <p className="text-sm text-zinc-500">Nenhum documento</p>
                    ) : (
                      <div className="space-y-2">
                        {evaluation.documents.map((doc: any) => (
                          <div key={doc.id} className="text-sm">
                            {doc.name}
                          </div>
                        ))}
                      </div>
                    )}
                    <Button variant="outline" className="w-full mt-4 rounded-xl">
                      <Plus className="h-4 w-4 mr-2" />
                      Anexar Documento
                    </Button>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Status do Laudo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="mb-4 space-y-2 rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm">
                      <div className="flex items-center justify-between"><span>Anamnese concluída</span><span>{evaluation.clinical_checklist?.anamnesis_completed ? "Sim" : "Não"}</span></div>
                      <div className="flex items-center justify-between"><span>Anamnese revisada</span><span>{evaluation.clinical_checklist?.anamnesis_reviewed ? "Sim" : "Não"}</span></div>
                      <div className="flex items-center justify-between"><span>Documentos relevantes</span><span>{evaluation.clinical_checklist?.has_relevant_documents ? "Sim" : "Não"}</span></div>
                      <div className="flex items-center justify-between"><span>Evolução registrada</span><span>{evaluation.clinical_checklist?.has_progress_entries_for_report ? "Sim" : "Não"}</span></div>
                      <div className="flex items-center justify-between"><span>Testes validados</span><span>{evaluation.clinical_checklist?.has_validated_tests ? "Sim" : "Não"}</span></div>
                    </div>
                    <Badge className="bg-slate-100 text-slate-700 rounded-full">
                      {evaluation.clinical_checklist?.ready_for_report ? "Pronto para gerar laudo" : "Dados clínicos incompletos"}
                    </Badge>
                    <Button className="w-full mt-4 rounded-xl">
                      Abrir Editor
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {activeTab === "tests" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Testes Aplicados</CardTitle>
                <Button className="rounded-xl" onClick={openAddTestModal}>
                  <Plus className="h-4 w-4 mr-2" />
                  Adicionar Teste
                </Button>
              </CardHeader>
              <CardContent>
                {evaluation.tests.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500">
                    <ClipboardList className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Nenhum teste aplicado ainda</p>
                    <p className="text-sm">Adicione um teste para começar a avaliação</p>
                  </div>
                ) : (
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Teste</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Data</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Status</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Ações</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evaluation.tests.map((test) => (
                        <tr key={test.id} className="border-b border-slate-100 hover:bg-slate-50 cursor-pointer" onClick={() => router.push(getTestUrl(test.instrument_code, test.id))}>
                          <td className="py-3 font-medium">{test.instrument_name}</td>
                          <td className="py-3">
                            {test.applied_on ? new Date(test.applied_on).toLocaleDateString("pt-BR") : "—"}
                          </td>
                          <td className="py-3">
                            <Badge variant="outline" className={test.is_validated ? "bg-emerald-50" : "bg-amber-50"}>
                              {test.status}
                            </Badge>
                          </td>
                          <td className="py-3" onClick={(e) => e.stopPropagation()}>
                            <div className="flex gap-2">
                              <Button variant="ghost" size="sm" onClick={() => router.push(getTestUrl(test.instrument_code, test.id))}>Abrir</Button>
                              <Button variant="ghost" size="sm" className="text-rose-700 hover:text-rose-800" onClick={() => removeTest(test.id)}>Remover</Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </CardContent>
            </Card>
          )}

          {activeTab === "anamnesis" && (
            <div className="space-y-6">
              <Card className="rounded-2xl border-slate-200 shadow-sm">
                <CardHeader className="flex flex-row items-center justify-between">
                  <div>
                    <CardTitle>Enviar Anamnese</CardTitle>
                    <p className="mt-1 text-sm text-slate-500">Convites por link seguro para preenchimento externo por e-mail ou WhatsApp.</p>
                  </div>
                  <Button className="rounded-xl" onClick={() => setShowAnamnesisInviteForm((prev) => !prev)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Novo convite
                  </Button>
                </CardHeader>
                <CardContent>
                  {showAnamnesisInviteForm && (
                    <div className="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                      <div className="mb-4 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
                        Obrigatórios: template, nome do destinatário e o contato correspondente ao canal escolhido.
                      </div>
                      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Template *</label>
                          <select value={anamnesisForm.template_id} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, template_id: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!anamnesisForm.template_id ? "border-rose-300" : "border-slate-200"}`}>
                            <option value="">Selecione...</option>
                            {anamnesisTemplates.map((template) => (
                              <option key={template.id} value={template.id}>{template.name}</option>
                            ))}
                          </select>
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Canal *</label>
                          <select value={anamnesisForm.channel} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, channel: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2">
                            <option value="email">E-mail</option>
                            <option value="whatsapp">WhatsApp</option>
                          </select>
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Nome do destinatário *</label>
                          <input value={anamnesisForm.recipient_name} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, recipient_name: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!anamnesisForm.recipient_name ? "border-rose-300" : "border-slate-200"}`} placeholder="Nome do responsável ou paciente" />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">Validade</label>
                          <input type="datetime-local" value={anamnesisForm.expires_at} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, expires_at: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">E-mail {anamnesisForm.channel === "email" ? "*" : ""}</label>
                          <input type="email" value={anamnesisForm.recipient_email} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, recipient_email: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${anamnesisForm.channel === "email" && !anamnesisForm.recipient_email ? "border-rose-300" : "border-slate-200"}`} placeholder="responsavel@email.com" />
                        </div>
                        <div className="space-y-2">
                          <label className="text-sm font-medium">WhatsApp {anamnesisForm.channel === "whatsapp" ? "*" : ""}</label>
                          <input value={anamnesisForm.recipient_phone} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, recipient_phone: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${anamnesisForm.channel === "whatsapp" && !anamnesisForm.recipient_phone ? "border-rose-300" : "border-slate-200"}`} placeholder="(62) 99999-9999" />
                        </div>
                        <div className="space-y-2 md:col-span-2">
                          <label className="text-sm font-medium">Mensagem opcional</label>
                          <textarea value={anamnesisForm.message} onChange={(e) => setAnamnesisForm({ ...anamnesisForm, message: e.target.value })} className="min-h-[110px] w-full rounded-xl border border-slate-200 bg-white px-3 py-2" placeholder="Se vazio, o sistema usa a mensagem padrão." />
                        </div>
                      </div>
                      <div className="mt-4 flex gap-2">
                        <Button className="rounded-xl" onClick={handleCreateAnamnesisInvite} disabled={anamnesisRequiredMissing || savingAnamnesisInvite}>{savingAnamnesisInvite ? "Criando..." : "Criar convite"}</Button>
                        <Button variant="outline" className="rounded-xl" onClick={() => setShowAnamnesisInviteForm(false)}>Cancelar</Button>
                      </div>
                    </div>
                  )}

                  {tabLoading ? (
                    <div className="py-8 text-center text-zinc-500">Carregando anamnese...</div>
                  ) : (
                    <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1.2fr_0.8fr]">
                      <div className="space-y-4">
                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Convites</h3>
                          {anamnesisInvites.length === 0 ? (
                            <div className="mt-3 text-sm text-slate-600">Nenhum convite criado para esta avaliação.</div>
                          ) : (
                            <div className="mt-3 space-y-3">
                              {anamnesisInvites.map((invite) => (
                                <div key={invite.id} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                                  <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                                    <div>
                                      <p className="font-medium text-slate-900">{invite.template_name}</p>
                                      <p className="text-sm text-slate-500">{invite.recipient_name} • {invite.channel === "email" ? invite.recipient_email : invite.recipient_phone}</p>
                                      <p className="mt-1 text-xs text-slate-500">Status: {invite.status} • Validade: {invite.expires_at ? new Date(invite.expires_at).toLocaleString("pt-BR") : "padrão"}</p>
                                    </div>
                                    <Badge variant="outline" className={invite.status === "completed" ? "bg-emerald-50 text-emerald-700" : invite.status === "in_progress" || invite.status === "opened" ? "bg-blue-50 text-blue-700" : invite.status === "canceled" ? "bg-slate-100 text-slate-600" : "bg-amber-50 text-amber-700"}>{invite.status}</Badge>
                                  </div>
                                  <div className="mt-4 flex flex-wrap gap-2">
                                    <Button variant="outline" className="rounded-xl" onClick={() => copyToClipboard(invite.public_url, "Link copiado com sucesso.")}><Copy className="mr-2 h-4 w-4" />Copiar link</Button>
                                    <Button variant="outline" className="rounded-xl" onClick={() => window.open(invite.public_url, "_blank")}><Send className="mr-2 h-4 w-4" />Abrir link</Button>
                                    <Button variant="outline" className="rounded-xl" onClick={() => handleSendAnamnesis(invite.id, "email")} disabled={!invite.recipient_email}><Mail className="mr-2 h-4 w-4" />E-mail</Button>
                                    <Button variant="outline" className="rounded-xl" onClick={() => handleSendAnamnesis(invite.id, "whatsapp")} disabled={!invite.recipient_phone}><MessageCircle className="mr-2 h-4 w-4" />WhatsApp</Button>
                                    <Button variant="outline" className="rounded-xl" onClick={() => handleResendAnamnesis(invite.id)}>Reenviar</Button>
                                    <Button variant="outline" className="rounded-xl" onClick={() => handleCancelAnamnesis(invite.id)}>Cancelar</Button>
                                  </div>
                                </div>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="space-y-4">
                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Respostas recebidas</h3>
                          {anamnesisResponses.length === 0 ? (
                            <div className="mt-3 text-sm text-slate-600">Nenhuma resposta enviada ainda.</div>
                          ) : (
                            <div className="mt-3 space-y-3">
                              {anamnesisResponses.map((response) => (
                                <button key={response.id} onClick={() => setSelectedAnamnesisResponse(response)} className={`w-full rounded-2xl border p-4 text-left shadow-sm transition ${selectedAnamnesisResponse?.id === response.id ? "border-zinc-900 bg-white" : "border-slate-200 bg-white hover:bg-slate-50"}`}>
                                  <p className="font-medium text-slate-900">{response.template_name}</p>
                                  <p className="text-sm text-slate-500">{response.submitted_by_name || "Sem nome"} • {response.submitted_by_relation || "Sem vínculo"}</p>
                                  <p className="mt-1 text-xs text-slate-500">Status: {response.status}</p>
                                </button>
                              ))}
                            </div>
                          )}
                        </div>

                        <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                          {!selectedAnamnesisResponse ? (
                            <div className="text-sm text-slate-600">Selecione uma resposta para revisar.</div>
                          ) : (
                            <div className="space-y-4">
                              <div className="flex items-center justify-between gap-4">
                                <div>
                                  <h3 className="font-semibold text-slate-900">{selectedAnamnesisResponse.template_name}</h3>
                                  <p className="text-sm text-slate-500">Respondido por {selectedAnamnesisResponse.submitted_by_name || "—"}</p>
                                </div>
                                <Button className="rounded-xl" onClick={() => handleReviewAnamnesis(selectedAnamnesisResponse.id)} disabled={selectedAnamnesisResponse.status === "reviewed"}><CheckCircle2 className="mr-2 h-4 w-4" />Marcar revisada</Button>
                              </div>
                              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4">
                                <pre className="whitespace-pre-wrap break-words text-sm text-slate-700">{JSON.stringify(selectedAnamnesisResponse.answers_payload, null, 2)}</pre>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {activeTab === "documents" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Documentos</CardTitle>
                  <p className="mt-1 text-sm text-slate-500">Obrigatórios para upload: título e arquivo.</p>
                </div>
                <Button className="rounded-xl" onClick={() => setShowDocumentForm((prev) => !prev)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Enviar Documento
                </Button>
              </CardHeader>
              <CardContent>
                {showDocumentForm && (
                  <div className="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="mb-4 text-sm text-slate-600">Tipos aceitos clinicamente: encaminhamento, relatorios, exames, formularios e anexos relevantes.</div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Título *</label>
                        <input value={documentForm.title} onChange={(e) => setDocumentForm({ ...documentForm, title: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!documentForm.title ? "border-rose-300" : "border-slate-200"}`} placeholder="Ex: Relatório escolar 2026" />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Tipo</label>
                        <select value={documentForm.document_type} onChange={(e) => setDocumentForm({ ...documentForm, document_type: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2">
                          <option value="referral">Encaminhamento</option>
                          <option value="school_report">Relatório escolar</option>
                          <option value="medical_report">Relatório médico</option>
                          <option value="therapeutic_report">Relatório terapêutico</option>
                          <option value="family_attachment">Ficha/anexo da família</option>
                          <option value="school_activity">Atividade escolar</option>
                          <option value="exam">Exame</option>
                          <option value="form">Formulário</option>
                          <option value="exported_report">Laudo exportado</option>
                          <option value="other">Outro</option>
                        </select>
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Origem</label>
                        <input value={documentForm.source} onChange={(e) => setDocumentForm({ ...documentForm, source: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" placeholder="Escola, médico, família..." />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Data do documento</label>
                        <input type="date" value={documentForm.document_date} onChange={(e) => setDocumentForm({ ...documentForm, document_date: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Arquivo *</label>
                        <input type="file" onChange={(e) => setDocumentForm({ ...documentForm, file: e.target.files?.[0] || null })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!documentForm.file ? "border-rose-300" : "border-slate-200"}`} />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Observações</label>
                        <textarea value={documentForm.notes} onChange={(e) => setDocumentForm({ ...documentForm, notes: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[90px]" />
                      </div>
                    </div>
                    <label className="mt-4 flex items-center gap-2 text-sm text-slate-600">
                      <input type="checkbox" checked={documentForm.is_relevant_for_report} onChange={(e) => setDocumentForm({ ...documentForm, is_relevant_for_report: e.target.checked })} />
                      Marcar como relevante para o laudo
                    </label>
                    <div className="mt-4 flex gap-2">
                      <Button className="rounded-xl" onClick={handleDocumentUpload} disabled={documentRequiredMissing || savingDocument}>{savingDocument ? "Enviando..." : "Salvar documento"}</Button>
                      <Button variant="outline" className="rounded-xl" onClick={() => setShowDocumentForm(false)}>Cancelar</Button>
                    </div>
                  </div>
                )}

                {tabLoading ? (
                  <div className="text-center py-8 text-zinc-500">Carregando documentos...</div>
                ) : documents.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500">
                    <FolderOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Nenhum documento anexado</p>
                    <p className="text-sm">Envie documentos para esta avaliação</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {documents.map((doc) => (
                      <div key={doc.id} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                          <div>
                            <p className="font-medium text-slate-900">{doc.title}</p>
                            <p className="text-sm text-slate-500">{doc.document_type_display} • {doc.file_name}</p>
                            <p className="mt-1 text-sm text-slate-600">{doc.source || "Sem origem informada"}</p>
                          </div>
                          <div className="flex gap-2">
                            <a href={doc.file_url} target="_blank" className="rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm">Abrir</a>
                            <Button variant="outline" className="rounded-xl" onClick={() => handleDeleteDocument(doc.id)}>Excluir</Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {activeTab === "evolution" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Evolução / Sessões</CardTitle>
                  <p className="mt-1 text-sm text-slate-500">Obrigatórios: tipo de registro e data.</p>
                </div>
                <Button className="rounded-xl" onClick={() => setShowProgressForm((prev) => !prev)}>
                  <Plus className="h-4 w-4 mr-2" />
                  Nova Anotação
                </Button>
              </CardHeader>
              <CardContent>
                {showProgressForm && (
                  <div className="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Tipo de evolução *</label>
                        <select value={progressForm.entry_type} onChange={(e) => setProgressForm({ ...progressForm, entry_type: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2">
                          <option value="anamnesis">Anamnese</option>
                          <option value="testing_session">Sessão de testagem</option>
                          <option value="scoring">Correção</option>
                          <option value="feedback">Devolutiva</option>
                          <option value="family_contact">Contato com família</option>
                          <option value="school_contact">Contato com escola</option>
                          <option value="clinical_meeting">Reunião clínica</option>
                          <option value="other">Outro</option>
                        </select>
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Data *</label>
                        <input type="date" value={progressForm.entry_date} onChange={(e) => setProgressForm({ ...progressForm, entry_date: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!progressForm.entry_date ? "border-rose-300" : "border-slate-200"}`} />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Hora inicial</label>
                        <input type="time" value={progressForm.start_time} onChange={(e) => setProgressForm({ ...progressForm, start_time: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Hora final</label>
                        <input type="time" value={progressForm.end_time} onChange={(e) => setProgressForm({ ...progressForm, end_time: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Objetivo</label>
                        <input value={progressForm.objective} onChange={(e) => setProgressForm({ ...progressForm, objective: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Testes aplicados</label>
                        <input value={progressForm.tests_applied} onChange={(e) => setProgressForm({ ...progressForm, tests_applied: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" placeholder="Ex: BPA-2, FDT" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Comportamento observado</label>
                        <textarea value={progressForm.observed_behavior} onChange={(e) => setProgressForm({ ...progressForm, observed_behavior: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[90px]" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Notas clínicas</label>
                        <textarea value={progressForm.clinical_notes} onChange={(e) => setProgressForm({ ...progressForm, clinical_notes: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[110px]" />
                      </div>
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Próximos passos</label>
                        <textarea value={progressForm.next_steps} onChange={(e) => setProgressForm({ ...progressForm, next_steps: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[90px]" />
                      </div>
                    </div>
                    <label className="mt-4 flex items-center gap-2 text-sm text-slate-600">
                      <input type="checkbox" checked={progressForm.include_in_report} onChange={(e) => setProgressForm({ ...progressForm, include_in_report: e.target.checked })} />
                      Incluir este registro no laudo
                    </label>
                    <div className="mt-4 flex gap-2">
                      <Button className="rounded-xl" onClick={handleCreateProgress} disabled={progressRequiredMissing || savingProgress}>{savingProgress ? "Salvando..." : "Salvar evolução"}</Button>
                      <Button variant="outline" className="rounded-xl" onClick={() => setShowProgressForm(false)}>Cancelar</Button>
                    </div>
                  </div>
                )}

                {tabLoading ? (
                  <div className="text-center py-8 text-zinc-500">Carregando evolução...</div>
                ) : progressEntries.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500">
                    <StickyNote className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Nenhum registro de evolução</p>
                    <p className="text-sm">Adicione notas de evolução ou sessões</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {progressEntries.map((entry) => (
                      <div key={entry.id} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                        <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                          <div>
                            <p className="font-medium text-slate-900">{entry.entry_type_display}</p>
                            <p className="text-sm text-slate-500">{new Date(entry.entry_date).toLocaleDateString("pt-BR")} • {entry.professional_name}</p>
                            {entry.objective && <p className="mt-2 text-sm text-slate-700"><span className="font-medium">Objetivo:</span> {entry.objective}</p>}
                            {entry.clinical_notes && <p className="mt-2 text-sm text-slate-600 whitespace-pre-wrap">{entry.clinical_notes}</p>}
                          </div>
                          <div className="flex flex-col gap-2">
                            <Badge variant="outline" className={entry.include_in_report ? "bg-emerald-50 text-emerald-700" : "bg-slate-100 text-slate-600"}>
                              {entry.include_in_report ? "Vai para o laudo" : "Uso interno"}
                            </Badge>
                            <Button variant="outline" className="rounded-xl" onClick={() => handleDeleteProgress(entry.id)}>Excluir</Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {activeTab === "report" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <div>
                  <CardTitle>Laudo</CardTitle>
                  <p className="mt-1 text-sm text-slate-500">Obrigatório para criar: título do laudo. O laudo consome testes, documentos e evolução já persistidos.</p>
                </div>
                <div className="flex gap-2">
                  {selectedReport && <Button variant="outline" className="rounded-xl" onClick={() => handleBuildReport(selectedReport.id)}>Regenerar seções</Button>}
                  <Button className="rounded-xl" onClick={() => setShowReportForm((prev) => !prev)}>Novo laudo</Button>
                </div>
              </CardHeader>
              <CardContent>
                {showReportForm && (
                  <div className="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="space-y-2 md:col-span-2">
                        <label className="text-sm font-medium">Título do laudo *</label>
                        <input value={reportForm.title} onChange={(e) => setReportForm({ ...reportForm, title: e.target.value })} className={`w-full rounded-xl border bg-white px-3 py-2 ${!reportForm.title ? "border-rose-300" : "border-slate-200"}`} placeholder="Ex: Laudo Neuropsicológico - Maria Cecilia" />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Interessado</label>
                        <input value={reportForm.interested_party} onChange={(e) => setReportForm({ ...reportForm, interested_party: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" placeholder="Família, escola, médico..." />
                      </div>
                      <div className="space-y-2">
                        <label className="text-sm font-medium">Finalidade</label>
                        <input value={reportForm.purpose} onChange={(e) => setReportForm({ ...reportForm, purpose: e.target.value })} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2" placeholder="Avaliação diagnóstica, acompanhamento..." />
                      </div>
                    </div>
                    <div className="mt-4 flex gap-2">
                      <Button className="rounded-xl" onClick={handleCreateReport} disabled={reportRequiredMissing || savingReport}>{savingReport ? "Criando..." : "Criar laudo"}</Button>
                      <Button variant="outline" className="rounded-xl" onClick={() => setShowReportForm(false)}>Cancelar</Button>
                    </div>
                  </div>
                )}

                {tabLoading ? (
                  <div className="text-center py-8 text-zinc-500">Carregando laudos...</div>
                ) : reports.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500">
                    <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Nenhum laudo criado</p>
                    <p className="text-sm">Crie um laudo estruturado para esta avaliação</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 gap-6 xl:grid-cols-[320px_1fr]">
                    <div className="space-y-3">
                      {reports.map((report) => (
                        <button key={report.id} onClick={() => openReport(report.id)} className={`w-full rounded-2xl border p-4 text-left shadow-sm transition ${selectedReport?.id === report.id ? "border-zinc-900 bg-zinc-50" : "border-slate-200 bg-white hover:bg-slate-50"}`}>
                          <p className="font-medium text-slate-900">{report.title}</p>
                          <p className="mt-1 text-sm text-slate-500">{report.author_name}</p>
                          <p className="mt-2 text-xs text-slate-500">Atualizado em {new Date(report.updated_at).toLocaleDateString("pt-BR")}</p>
                        </button>
                      ))}
                    </div>

                    <div>
                      {!selectedReport ? (
                        <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 text-sm text-slate-600">Selecione um laudo para revisar as seções.</div>
                      ) : (
                        <div className="space-y-4">
                          <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                            <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
                              <div>
                                <h3 className="text-lg font-semibold text-slate-900">{selectedReport.title}</h3>
                                <p className="text-sm text-slate-500">Interessado: {selectedReport.interested_party || "—"} • Finalidade: {selectedReport.purpose || "—"}</p>
                              </div>
                              <Button className="rounded-xl" onClick={() => handleBuildReport(selectedReport.id)}>Atualizar snapshot</Button>
                            </div>
                          </div>
                          {(selectedReport.sections || []).map((section) => (
                            <div key={section.id} className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                              <div className="mb-3 flex items-center justify-between gap-4">
                                <div>
                                  <p className="font-medium text-slate-900">{section.title}</p>
                                  <p className="text-xs text-slate-500">{section.key}</p>
                                </div>
                                <Badge variant="outline" className={section.is_locked ? "bg-amber-50 text-amber-700" : "bg-slate-100 text-slate-600"}>{section.is_locked ? "Bloqueada" : "Editável"}</Badge>
                              </div>
                              <textarea
                                defaultValue={section.edited_text || section.generated_text}
                                className="min-h-[160px] w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700"
                                onBlur={(e) => handleSaveSection(section.id, e.target.value)}
                              />
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
