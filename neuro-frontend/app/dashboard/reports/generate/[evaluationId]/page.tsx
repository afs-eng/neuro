"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { PageContainer, PageHeader, SectionCard } from "@/components/ui/page";
import { reportService } from "@/services/reportService";
import { ArrowLeft, FileText, Loader2, Sparkles } from "lucide-react";

export default function GenerateReportPage() {
  const params = useParams<{ evaluationId: string }>();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [existingReport, setExistingReport] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadExistingReport() {
      try {
        const reports = await reportService.getByEvaluation(params.evaluationId);
        setExistingReport(Array.isArray(reports) && reports.length > 0 ? reports[0] : null);
      } catch (err: any) {
        setError(err?.message || "Nao foi possivel verificar laudos existentes.");
      } finally {
        setLoading(false);
      }
    }

    loadExistingReport();
  }, [params.evaluationId]);

  async function handleGenerate() {
    setGenerating(true);
    setError("");
    try {
      const report = await reportService.generateFromEvaluation(params.evaluationId);
      router.push(`/dashboard/reports/${report.id}`);
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel gerar o laudo.");
    } finally {
      setGenerating(false);
    }
  }

  if (loading) {
    return (
      <div className="flex h-[420px] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
      </div>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title="Gerar laudo"
        subtitle={`Avaliacao ${params.evaluationId}`}
        actions={
          <Link href={`/dashboard/evaluations/${params.evaluationId}/overview?tab=report`}>
            <Button variant="outline" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Voltar
            </Button>
          </Link>
        }
      />

      {error && <div className="mb-4 rounded-xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}

      <SectionCard title="Laudo com IA" description="O sistema usa o contexto estruturado da avaliacao para gerar um rascunho revisavel.">
        <div className="mx-auto max-w-2xl py-10 text-center">
          <div className="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
            <FileText className="h-10 w-10" />
          </div>

          {existingReport ? (
            <>
              <h2 className="text-2xl font-semibold text-slate-900">Ja existe um laudo para esta avaliacao</h2>
              <p className="mt-3 text-sm text-slate-500">Abra o laudo existente para continuar a revisao ou gere um novo rascunho se precisar reiniciar o processo.</p>
              <div className="mt-8 flex justify-center gap-3">
                <Button variant="outline" onClick={() => router.push(`/dashboard/reports/${existingReport.id}`)}>
                  Abrir laudo existente
                </Button>
                <Button className="gap-2" disabled={generating} onClick={handleGenerate}>
                  {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                  Gerar novo rascunho
                </Button>
              </div>
            </>
          ) : (
            <>
              <h2 className="text-2xl font-semibold text-slate-900">Preparado para gerar o rascunho</h2>
              <p className="mt-3 text-sm text-slate-500">Testes validados, anamnese, documentos relevantes e observacoes clinicas serao consolidados antes da geracao.</p>
              <div className="mt-8 flex justify-center">
                <Button className="gap-2" disabled={generating} onClick={handleGenerate}>
                  {generating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                  Gerar laudo com IA
                </Button>
              </div>
            </>
          )}
        </div>
      </SectionCard>
    </PageContainer>
  );
}
