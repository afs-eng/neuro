"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { PageContainer, PageHeader, EmptyState, SectionCard } from "@/components/ui/page";
import { FileText, Plus, Loader2, ArrowRight, Calendar, User } from "lucide-react";
import { reportService } from "@/services/reportService";

function statusLabel(status: string) {
  switch (status) {
    case "draft":
      return "Rascunho";
    case "generating":
      return "Gerando";
    case "in_review":
      return "Em revisao";
    case "finalized":
      return "Finalizado";
    case "sent":
      return "Enviado";
    default:
      return status;
  }
}

export default function ReportsPage() {
  const router = useRouter();
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadReports() {
      try {
        setError("");
        const data = await reportService.list();
        setReports(Array.isArray(data) ? data : []);
      } catch (err: any) {
        setError(err?.message || "Nao foi possivel carregar os laudos.");
      } finally {
        setLoading(false);
      }
    }

    loadReports();
  }, []);

  return (
    <PageContainer>
      <PageHeader
        title="Laudos"
        subtitle="Rascunhos gerados a partir das avaliacoes, prontos para revisao, finalizacao e exportacao."
        actions={
          <Button className="gap-2" onClick={() => router.push("/dashboard/evaluations")}> 
            <Plus className="h-4 w-4" />
            Novo laudo
          </Button>
        }
      />

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          <Loader2 className="h-8 w-8 animate-spin text-slate-400" />
        </div>
      ) : reports.length === 0 ? (
        <SectionCard title="Fila de laudos" description="Assim que um laudo for criado a partir de uma avaliacao, ele aparecera aqui.">
          <EmptyState
            icon={<FileText className="h-12 w-12" />}
            title="Nenhum laudo em producao"
            description={error || "Gere um laudo pela tela da avaliacao para iniciar a revisao clinica."}
          />
        </SectionCard>
      ) : (
        <div className="grid grid-cols-1 gap-4 xl:grid-cols-2">
          {reports.map((report) => (
            <div key={report.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="text-lg font-semibold text-slate-900">{report.title}</h3>
                  <p className="mt-1 text-sm text-slate-500">{report.evaluation_title || "Laudo vinculado a avaliacao"}</p>
                </div>
                <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700">
                  {statusLabel(report.status)}
                </span>
              </div>

              <div className="mt-5 grid grid-cols-1 gap-3 text-sm text-slate-600 sm:grid-cols-2">
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4 text-slate-400" />
                  <span>{report.patient_name || "Paciente nao informado"}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-slate-400" />
                  <span>{report.updated_at ? new Date(report.updated_at).toLocaleDateString("pt-BR") : "Sem data"}</span>
                </div>
              </div>

              <div className="mt-6 flex justify-end">
                <Button className="gap-2" onClick={() => router.push(`/dashboard/reports/${report.id}`)}>
                  Abrir laudo
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
