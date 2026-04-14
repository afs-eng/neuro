"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";

import { FormStepRenderer, isVisible } from "@/components/anamnesis/FormStepRenderer";
import { ProgressHeader } from "@/components/anamnesis/ProgressHeader";
import { ReviewSummary } from "@/components/anamnesis/ReviewSummary";
import { AnamnesisStep } from "@/components/anamnesis/types";
import { api } from "@/lib/api";

type PublicAnamnesisData = {
  invite_id: number;
  status: string;
  patient_name: string;
  template_name: string;
  target_type: string;
  schema_payload: { intro?: string; steps?: AnamnesisStep[]; title?: string; description?: string };
  answers_payload: Record<string, any>;
  submitted_by_name: string;
  submitted_by_relation: string;
  expires_at: string | null;
  access_state: string;
  message: string;
};

export default function PublicAnamnesisPage() {
  const params = useParams();
  const token = String(params.token || "");
  const [data, setData] = useState<PublicAnamnesisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [currentSection, setCurrentSection] = useState(0);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [notice, setNotice] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [invalidFieldIds, setInvalidFieldIds] = useState<string[]>([]);
  const [pendingFocusFieldId, setPendingFocusFieldId] = useState<string | null>(null);

  const sections = useMemo(() => data?.schema_payload?.steps || [], [data]);

  useEffect(() => {
    async function load() {
      try {
        const response = await api.get<PublicAnamnesisData>(`/api/public/anamnesis/${token}`);
        setData(response);
        setAnswers(response.answers_payload || {});
      } catch (err: any) {
        setNotice({ type: "error", text: err?.message || "Não foi possível carregar a anamnese." });
      } finally {
        setLoading(false);
      }
    }
    if (token) load();
  }, [token]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [currentSection]);

  useEffect(() => {
    if (!pendingFocusFieldId) return;

    const frame = window.requestAnimationFrame(() => {
      const fieldElement = document.getElementById(`anamnesis-field-${pendingFocusFieldId}`);
      const inputElement = document.getElementById(`anamnesis-input-${pendingFocusFieldId}`) as HTMLElement | null;

      fieldElement?.scrollIntoView({ behavior: "smooth", block: "center" });
      inputElement?.focus();
    });

    setPendingFocusFieldId(null);
    return () => window.cancelAnimationFrame(frame);
  }, [currentSection, pendingFocusFieldId]);

  const current = sections[currentSection];

  function isEmptyValue(value: any) {
    return value === undefined || value === null || value === "" || (Array.isArray(value) && value.length === 0);
  }

  function setFieldValue(key: string, value: any) {
    setAnswers((prev) => ({ ...prev, [key]: value }));
    if (!isEmptyValue(value)) {
      setInvalidFieldIds((prev) => prev.filter((fieldId) => fieldId !== key));
    }
  }

  function validateRequiredFields() {
    const missing: Array<{ fieldId: string; label: string; sectionIndex: number }> = [];
    for (const [sectionIndex, section] of sections.entries()) {
      for (const field of section.fields || []) {
        if (!isVisible(field, answers)) continue;
        const value = answers[field.id];
        if (field.required && isEmptyValue(value)) {
          missing.push({ fieldId: field.id, label: field.label, sectionIndex });
        }
      }
    }
    return missing;
  }

  function validateCurrentSection() {
    const section = sections[currentSection];
    if (!section) return [] as Array<{ fieldId: string; label: string; sectionIndex: number }>;

    const missing: Array<{ fieldId: string; label: string; sectionIndex: number }> = [];

    for (const field of section.fields || []) {
      if (!isVisible(field, answers)) continue;
      const value = answers[field.id];
      if (field.required && isEmptyValue(value)) {
        missing.push({ fieldId: field.id, label: field.label, sectionIndex: currentSection });
      }
    }

    return missing;
  }

  function goToField(fieldId: string, sectionIndex: number) {
    setCurrentSection(sectionIndex);
    setPendingFocusFieldId(fieldId);
  }

  function goToNextSection() {
    const missing = validateCurrentSection();

    if (missing.length > 0) {
      setInvalidFieldIds((prev) => Array.from(new Set([...prev, ...missing.map((field) => field.fieldId)])));
      setNotice({ type: "error", text: `Preencha os campos obrigatórios desta etapa: ${missing.map((field) => field.label).join(", ")}` });
      goToField(missing[0].fieldId, missing[0].sectionIndex);
      return;
    }

    setNotice(null);
    setCurrentSection((prev) => Math.min(prev + 1, sections.length));
  }

  async function saveDraft() {
    if (!data) return;
    setSaving(true);
    try {
      const response = await api.post<PublicAnamnesisData>(`/api/public/anamnesis/${token}/save-draft`, {
        answers_payload: answers,
        submitted_by_name: answers.submitted_by_name || "",
        submitted_by_relation: answers.submitted_by_relation || "",
      });
      setData(response);
      setNotice({ type: "success", text: "Rascunho salvo com sucesso." });
    } catch (err: any) {
      setNotice({ type: "error", text: err?.message || "Erro ao salvar rascunho." });
    } finally {
      setSaving(false);
    }
  }

  async function submitFinal() {
    if (!data) return;
    const missing = validateRequiredFields();
    if (missing.length > 0) {
      setInvalidFieldIds(missing.map((field) => field.fieldId));
      setNotice({ type: "error", text: `Preencha os campos obrigatórios: ${missing.map((field) => field.label).join(", ")}` });
      goToField(missing[0].fieldId, missing[0].sectionIndex);
      return;
    }

    setInvalidFieldIds([]);
    setSubmitting(true);
    try {
      const response = await api.post<PublicAnamnesisData>(`/api/public/anamnesis/${token}/submit`, {
        answers_payload: answers,
        submitted_by_name: answers.submitted_by_name || "",
        submitted_by_relation: answers.submitted_by_relation || "",
      });
      setData(response);
      setNotice({ type: "success", text: "Anamnese enviada com sucesso." });
    } catch (err: any) {
      setNotice({ type: "error", text: err?.message || "Erro ao enviar anamnese." });
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <div className="min-h-screen bg-[#f4efe3] p-6 text-center text-slate-600">Carregando anamnese...</div>;
  }

  if (!data) {
    return <div className="min-h-screen bg-[#f4efe3] p-6 text-center text-rose-700">{notice?.text || "Convite inválido."}</div>;
  }

  if (data.access_state === "expired" || data.access_state === "canceled") {
    return <div className="min-h-screen bg-[#f4efe3] p-6 text-center text-slate-700">Este convite está {data.access_state === "expired" ? "expirado" : "cancelado"}.</div>;
  }

  if (data.access_state === "completed") {
    return <div className="min-h-screen bg-[#f4efe3] p-6 text-center text-slate-700">Esta anamnese já foi enviada. Obrigado pelo preenchimento.</div>;
  }

  return (
    <div className="min-h-screen bg-[#f4efe3] p-4 md:p-8">
      <div className="mx-auto max-w-4xl rounded-[32px] bg-white p-6 shadow-xl ring-1 ring-black/5 md:p-8">
        <div className="mb-6 rounded-2xl bg-slate-50 p-5">
          <h1 className="text-2xl font-semibold text-slate-900">{data.schema_payload?.title || data.template_name}</h1>
          <p className="mt-2 text-sm text-slate-600">Paciente: {data.patient_name}</p>
          <p className="mt-2 text-sm text-slate-500">{data.schema_payload?.description || data.schema_payload?.intro || "Preencha com calma. Você pode salvar o rascunho antes do envio final."}</p>
          <p className="mt-3 text-xs text-slate-500">Confidencialidade: suas respostas serão utilizadas exclusivamente no contexto da avaliação clínica.</p>
        </div>

        {notice && (
          <div className={`mb-6 rounded-2xl px-4 py-3 text-sm ${notice.type === "success" ? "border border-emerald-200 bg-emerald-50 text-emerald-800" : "border border-rose-200 bg-rose-50 text-rose-800"}`}>
            {notice.text}
          </div>
        )}

        <ProgressHeader steps={sections} currentStep={Math.min(currentSection, sections.length)} />

        {current && currentSection < sections.length && (
          <div className="space-y-5">
            <FormStepRenderer step={current} answers={answers} onChange={setFieldValue} invalidFieldIds={invalidFieldIds} />
          </div>
        )}

        {currentSection >= sections.length && <ReviewSummary steps={sections} answers={answers} />}

        <div className="mt-8 flex flex-col gap-3 border-t border-slate-200 pt-6 md:flex-row md:items-center md:justify-between">
          <div className="flex gap-2">
            <button onClick={() => setCurrentSection((prev) => Math.max(prev - 1, 0))} disabled={currentSection === 0} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm disabled:opacity-50">Anterior</button>
            <button onClick={goToNextSection} disabled={currentSection === sections.length} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm disabled:opacity-50">Próxima</button>
          </div>
          <div className="flex gap-2">
            <button onClick={saveDraft} disabled={saving} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm">{saving ? "Salvando..." : "Salvar rascunho"}</button>
            <button onClick={submitFinal} disabled={submitting} className="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white">{submitting ? "Enviando..." : "Enviar anamnese"}</button>
          </div>
        </div>
      </div>
    </div>
  );
}
