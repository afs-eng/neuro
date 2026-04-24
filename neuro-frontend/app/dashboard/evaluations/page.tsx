"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { Plus, Search, User, Calendar, ClipboardList, Filter, MoreHorizontal, ArrowRight, Clock, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";
import { compareEvaluationsByDeadline, getEvaluationDeadlineMeta } from "@/lib/evaluation-deadline";

interface Evaluation {
  id: number;
  code: string;
  title: string;
  patient_id: number;
  patient_name: string;
  examiner_name: string | null;
  status: string;
  status_display: string;
  priority: string;
  priority_display: string;
  start_date: string | null;
  end_date: string | null;
  created_at: string;
  tests_count?: number;
}

const STATUS_COLORS: Record<string, string> = {
  draft: "bg-slate-100 text-slate-600 border-slate-200",
  collecting_data: "bg-amber-50 text-amber-600 border-amber-100",
  tests_in_progress: "bg-blue-50 text-blue-600 border-blue-100",
  scoring: "bg-purple-50 text-purple-600 border-purple-100",
  writing_report: "bg-orange-50 text-orange-600 border-orange-100",
  in_review: "bg-indigo-50 text-indigo-600 border-indigo-100",
  approved: "bg-emerald-50 text-emerald-600 border-emerald-100",
  archived: "bg-slate-100 text-slate-400 border-slate-200",
};

const PRIORITY_ICONS: Record<string, React.ReactNode> = {
  low: <Clock className="h-3 w-3" />,
  medium: <Clock className="h-3 w-3" />,
  high: <AlertCircle className="h-3 w-3" />,
  urgent: <AlertCircle className="h-3 w-3" />,
};

const PRIORITY_COLORS: Record<string, string> = {
  low: "text-slate-400",
  medium: "text-blue-500",
  high: "text-orange-500",
  urgent: "text-rose-500",
};

export default function EvaluationsPage() {
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchEvaluations();
  }, []);

  async function fetchEvaluations() {
    try {
      const data = await api.get<Evaluation[]>("/api/evaluations/");
      setEvaluations(Array.isArray(data) ? data : []);
    } catch (err: any) {
      console.error("Erro ao buscar avaliações:", err);
      setEvaluations([]);
    } finally {
      setLoading(false);
    }
  }

  const filteredEvaluations = Array.isArray(evaluations)
    ? evaluations
        .filter(
          (e) =>
            (e.patient_name?.toLowerCase() || "").includes(searchTerm.toLowerCase()) ||
            (e.code?.toLowerCase() || "").includes(searchTerm.toLowerCase()) ||
            (e.title?.toLowerCase() || "").includes(searchTerm.toLowerCase())
        )
        .sort(compareEvaluationsByDeadline)
    : [];

  if (loading) {
    return (
      <PageContainer>
        <div className="py-20 text-center animate-pulse text-slate-300 font-bold uppercase tracking-widest text-xs">Sincronizando processos clínicos...</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title="Painel de Avaliações"
        subtitle="Monitore o progresso clínico e a aplicação de instrumentos."
        actions={
          <div className="flex gap-2">
             <div className="relative group">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400 group-focus-within:text-primary transition-colors" />
                <input 
                  type="text" 
                  placeholder="Buscar processo..." 
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 h-11 w-64 rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-primary/20 transition-all"
                />
             </div>
             <Button variant="outline" className="h-11 rounded-xl border-slate-200 text-slate-500 font-bold gap-2">
               <Filter className="h-4 w-4" /> Filtros
             </Button>
             <Link href="/dashboard/evaluations/new">
                <Button className="h-11 rounded-xl font-bold gap-2 shadow-sm border-none">
                  <Plus className="h-4 w-4" /> Nova Avaliação
                </Button>
             </Link>
          </div>
        }
      />

      {filteredEvaluations.length === 0 ? (
        <EmptyState
          title="Sem avaliações ativas"
          description="Inicie um novo processo clínico a partir do perfil de um paciente."
          icon={<ClipboardList className="h-12 w-12 text-slate-200" />}
          action={
            <Link href="/dashboard/patients">
              <Button className="rounded-xl font-bold">Ver Pacientes</Button>
            </Link>
          }
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
          {filteredEvaluations.map((evaluation) => {
            const deadlineMeta = getEvaluationDeadlineMeta(evaluation.end_date, evaluation.status);

            return (
              <Link key={evaluation.id} href={`/dashboard/evaluations/${evaluation.id}`}>
                <div className="group relative flex flex-col rounded-[40px] border border-slate-100 bg-white p-8 transition-all hover:border-primary/20 hover:shadow-spike">
                  <div className="mb-8 flex items-start justify-between">
                    <div className="space-y-1">
                      <span className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-300 transition-colors group-hover:text-primary/40">{evaluation.code}</span>
                      <h3 className="text-xl font-black tracking-tight text-slate-900 transition-colors group-hover:text-primary">{evaluation.patient_name}</h3>
                    </div>
                    <button className="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-50 text-slate-400 opacity-0 transition-all group-hover:opacity-100">
                      <MoreHorizontal className="h-5 w-5" />
                    </button>
                  </div>

                  <div className="flex-1 space-y-6">
                    {evaluation.title && (
                      <p className="line-clamp-2 text-sm font-bold leading-relaxed text-slate-500">
                        {evaluation.title}
                      </p>
                    )}

                    <div className="flex flex-wrap gap-3">
                      <Badge className={`${STATUS_COLORS[evaluation.status] || "bg-slate-100"} rounded-full border px-3 py-1 text-[9px] font-black uppercase tracking-widest shadow-none`}>
                        {evaluation.status_display}
                      </Badge>
                      <div className={`flex items-center gap-1.5 rounded-full border border-slate-100 bg-slate-50 px-3 py-1 text-[9px] font-black uppercase tracking-widest ${PRIORITY_COLORS[evaluation.priority]}`}>
                        {PRIORITY_ICONS[evaluation.priority]}
                        {evaluation.priority_display}
                      </div>
                      <div className={`rounded-full border px-3 py-1 text-[9px] font-black uppercase tracking-widest ${deadlineMeta.badgeClassName}`}>
                        {deadlineMeta.label}
                      </div>
                    </div>

                    <div className="flex items-center gap-2 text-[11px] font-bold text-slate-400">
                      <Calendar className="h-3.5 w-3.5" />
                      <span>{deadlineMeta.helperText}</span>
                    </div>
                  </div>

                  <div className="mt-10 flex items-center justify-between border-t border-slate-50 pt-6">
                    <div className="flex items-center gap-2">
                      <div className="-ml-1 flex h-8 w-8 items-center justify-center rounded-full border-2 border-white bg-slate-100 first:ml-0">
                        <User className="h-4 w-4 text-slate-400" />
                      </div>
                      <span className="text-[10px] font-bold uppercase tracking-widest text-slate-400">
                        {evaluation.examiner_name?.split(" ")[0] || "Sistema"}
                      </span>
                    </div>
                    <div className="flex items-center gap-2 text-primary">
                      <span className="text-[10px] font-black uppercase tracking-widest">Ver Processo</span>
                      <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </PageContainer>
  );
}
