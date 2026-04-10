"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { PageContainer, PageHeader } from "@/components/ui/page";
import { resolveApiUrl } from "@/lib/api";
import { reportService } from "@/services/reportService";
import { ArrowLeft, Calendar, CheckCircle2, Download, FileText, Loader2, RotateCcw, Save, User } from "lucide-react";

export default function ReportDetailPage() {
  const params = useParams<{ id: string }>();
  const reportId = params.id;
  const [report, setReport] = useState<any>(null);
  const [activeSectionId, setActiveSectionId] = useState<number | null>(null);
  const [editedText, setEditedText] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  const activeSection = useMemo(
    () => report?.sections?.find((section: any) => section.id === activeSectionId) || null,
    [activeSectionId, report]
  );

  const loadReport = useCallback(async () => {
    try {
      setError("");
      const data = await reportService.get(reportId);
      setReport(data);
      if (data.sections?.length) {
        const firstSection = data.sections[0];
        setActiveSectionId((current) => current ?? firstSection.id);
        if (!activeSectionId) {
          setEditedText(firstSection.edited_text || firstSection.generated_text || "");
        }
      }
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel carregar o laudo.");
    } finally {
      setLoading(false);
    }
  }, [activeSectionId, reportId]);

  useEffect(() => {
    loadReport();
  }, [loadReport]);

  useEffect(() => {
    if (activeSection) {
      setEditedText(activeSection.edited_text || activeSection.generated_text || "");
    }
  }, [activeSectionId, activeSection]);

  async function handleSave() {
    if (!activeSection) return;
    setSaving(true);
    setNotice("");
    try {
      const updated = await reportService.saveSection(activeSection.id, editedText);
      setReport((current: any) => ({
        ...current,
        sections: current.sections.map((section: any) =>
          section.id === activeSection.id ? { ...section, ...updated } : section
        ),
      }));
      setNotice("Secao salva com sucesso.");
      await loadReport();
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel salvar a secao.");
    } finally {
      setSaving(false);
    }
  }

  async function handleRegenerate() {
    if (!activeSection || !report) return;
    setSaving(true);
    setNotice("");
    try {
      const updated = await reportService.regenerateSection(report.id, activeSection.key);
      setReport((current: any) => ({
        ...current,
        sections: current.sections.map((section: any) =>
          section.id === activeSection.id ? { ...section, ...updated } : section
        ),
      }));
      setEditedText(updated.edited_text || updated.generated_text || "");
      setNotice("Secao regenerada com sucesso.");
      await loadReport();
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel regenerar a secao.");
    } finally {
      setSaving(false);
    }
  }

  async function handleFinalize() {
    if (!report) return;
    setSaving(true);
    setNotice("");
    try {
      const updated = await reportService.finalize(report.id);
      setReport(updated);
      setNotice("Laudo finalizado com sucesso.");
      await loadReport();
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel finalizar o laudo.");
    } finally {
      setSaving(false);
    }
  }

  async function handleExportHtml() {
    if (!report) return;
    try {
      const data = await reportService.exportHtml(report.id);
      const popup = window.open("", "_blank");
      if (popup) {
        popup.document.open();
        popup.document.write(data.html);
        popup.document.close();
      }
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel exportar o laudo.");
    }
  }

  async function handleExportDocx() {
    if (!report) return;
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(resolveApiUrl(`/api/reports/${report.id}/export-docx`), {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });

      if (!response.ok) {
        let message = "Nao foi possivel exportar o laudo em DOCX.";
        try {
          const payload = await response.json();
          message = payload?.message || message;
        } catch {}
        throw new Error(message);
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      const patientName = (report.patient_name || "paciente")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-zA-Z0-9]+/g, "-")
        .replace(/^-+|-+$/g, "");
      link.download = `Laudo-${patientName || report.id}.docx`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel exportar o laudo em DOCX.");
    }
  }

  if (loading) {
    return (
      <div className="flex h-[420px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
      </div>
    );
  }

  if (!report) {
    return (
      <PageContainer>
        <PageHeader title="Laudo" subtitle={error || "Laudo nao encontrado."} />
      </PageContainer>
    );
  }

  const isFinalized = report.status === "finalized";

  return (
    <PageContainer>
      <PageHeader
        title={report.title}
        subtitle={`${report.patient_name || "Paciente"} · ${report.evaluation_title || "Avaliacao"}${report.purpose ? ` · ${report.purpose}` : ""}`}
        actions={
          <div className="flex gap-2">
            <Link href="/dashboard/reports">
              <Button variant="outline" className="gap-2">
                <ArrowLeft className="h-4 w-4" />
                Voltar
              </Button>
            </Link>
            <Button variant="outline" className="gap-2" onClick={handleExportHtml}>
              <Download className="h-4 w-4" />
              Exportar HTML
            </Button>
            <Button variant="outline" className="gap-2" onClick={handleExportDocx}>
              <FileText className="h-4 w-4" />
              Exportar DOCX
            </Button>
          </div>
        }
      />

      {error && <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}
      {notice && <div className="mb-4 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">{notice}</div>}

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[280px_minmax(0,1fr)]">
        <aside className="space-y-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="space-y-2">
            {report.sections?.map((section: any) => (
              <button
                key={section.id}
                type="button"
                onClick={() => setActiveSectionId(section.id)}
                className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition ${
                  activeSectionId === section.id
                    ? "border-indigo-600 bg-indigo-600 text-white"
                    : "border-slate-200 bg-slate-50 text-slate-700 hover:bg-white"
                }`}
              >
                <div className="font-medium">{section.title}</div>
                <div className={`mt-1 text-xs ${activeSectionId === section.id ? "text-indigo-100" : "text-slate-400"}`}>
                  {section.key}
                </div>
              </button>
            ))}
          </div>

          <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-600">
            <div className="flex items-center gap-2"><User className="h-4 w-4 text-slate-400" />{report.author_name}</div>
            <div className="mt-2 flex items-center gap-2"><Calendar className="h-4 w-4 text-slate-400" />{report.updated_at ? new Date(report.updated_at).toLocaleString("pt-BR") : "Sem atualizacao"}</div>
            <div className="mt-2 flex items-center gap-2"><CheckCircle2 className="h-4 w-4 text-slate-400" />Status: {report.status}</div>
            <div className="mt-2 text-xs text-slate-500">Interessado: {report.interested_party || report.patient_name}</div>
          </div>

          <div>
            <h3 className="mb-2 text-sm font-semibold text-slate-900">Historico</h3>
            <div className="space-y-2">
              {(report.versions || []).slice(0, 5).map((version: any) => (
                <div key={version.id} className="rounded-xl border border-slate-100 bg-slate-50 px-3 py-2 text-xs text-slate-600">
                  <div className="font-medium text-slate-800">Versao {version.version_number}</div>
                  <div>{version.created_by}</div>
                </div>
              ))}
            </div>
          </div>
        </aside>

        <main className="rounded-2xl border border-slate-200 bg-white shadow-sm">
          <div className="flex items-center justify-between border-b border-slate-200 px-6 py-4">
            <div>
              <h2 className="text-lg font-semibold text-slate-900">{activeSection?.title || "Selecione uma secao"}</h2>
              <p className="text-sm text-slate-500">Edite o rascunho gerado e regenere a secao quando necessario.</p>
            </div>
            <div className="flex gap-2">
              {!isFinalized && (
                <>
                  <Button variant="outline" className="gap-2" disabled={saving || !activeSection} onClick={handleRegenerate}>
                    <RotateCcw className="h-4 w-4" />
                    Regenerar secao
                  </Button>
                  <Button className="gap-2" disabled={saving || !activeSection} onClick={handleSave}>
                    {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
                    Salvar
                  </Button>
                </>
              )}
              <Button variant="outline" disabled={saving || isFinalized} onClick={handleFinalize}>
                Finalizar
              </Button>
            </div>
          </div>

          <textarea
            value={editedText}
            onChange={(event) => setEditedText(event.target.value)}
            disabled={isFinalized || !activeSection}
            className="min-h-[620px] w-full resize-none border-0 p-6 text-sm leading-7 text-slate-700 focus:ring-0"
            placeholder="Selecione uma secao para revisar o conteudo..."
          />
        </main>
      </div>
    </PageContainer>
  );
}
