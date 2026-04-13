"use client";

import React from "react";
import Link from "next/link";
import { PageContainer, PageHeader, SectionCard, StatCard } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { 
  Users, 
  ClipboardList, 
  FlaskConical, 
  FileText, 
  Plus, 
  ChevronRight, 
  Brain,
  Stethoscope,
  Sparkles,
  Loader2,
  Inbox
} from "lucide-react";

const QUICK_ACTIONS = [
  { title: "Novo Paciente", icon: Users, href: "/dashboard/patients/new", color: "text-blue-600", bg: "bg-blue-50" },
  { title: "Aplicar Teste", icon: Stethoscope, href: "/dashboard/tests", color: "text-primary", bg: "bg-primary/10" },
  { title: "Gerar Laudo", icon: FileText, href: "/dashboard/reports", color: "text-amber-600", bg: "bg-amber-50" },
  { title: "IA Clínica", icon: Sparkles, href: "/dashboard/ai", color: "text-purple-600", bg: "bg-purple-50" },
];

function StatusBadge({ children }: { children: string }) {
  const map: Record<string, string> = {
    "init": "text-amber-600 bg-amber-50 border-amber-100",
    "in_progress": "text-primary bg-primary/10 border-primary/20",
    "completed": "text-emerald-600 bg-emerald-50 border-emerald-100",
    "report": "text-indigo-600 bg-indigo-50 border-indigo-100",
  };
  
  const labels: Record<string, string> = {
    "init": "Triagem",
    "in_progress": "Avaliação",
    "completed": "Finalizado",
    "report": "Laudo",
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${map[children] || "bg-slate-50 text-slate-500 border-slate-100"}`}>
      {labels[children] || children}
    </span>
  );
}

export default function DashboardPage() {
  const [user, setUser] = React.useState<any>(null);
  const [evaluations, setEvaluations] = React.useState<any[]>([]);
  const [stats, setStats] = React.useState<any>(null);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const initDashboard = async () => {
      if (typeof window !== "undefined") {
        const savedUser = localStorage.getItem("user");
        if (savedUser) {
          setUser(JSON.parse(savedUser));
        }
      }

      try {
        const { api } = await import("@/lib/api");
        // Busca estatisticas e avaliações recentes em paralelo
        const [evalsRes] = await Promise.all([
          api.get<any[]>("/api/evaluations/"),
          // api.get("/api/dashboard/stats") // Exemplo de endpoint futuro
        ]);
        
        setEvaluations(evalsRes.slice(0, 5)); // Pega as 5 mais recentes
      } catch (e) {
        console.error("Erro ao carregar dashboard:", e);
      } finally {
        setLoading(false);
      }
    };

    initDashboard();
  }, []);

  const getGreeting = () => {
    if (!user) return "Bem-vindo(a) de volta.";
    const rawName = user.full_name || user.username || "Profissional";
    const cleanName = rawName.replace(/^(Dr\.|Dra\.|Dr|Dra)\s+/i, "").trim();
    const firstName = cleanName.split(/\s+/)[0];
    const isFemale = user.sex === "F" || (firstName.toLowerCase().endsWith("a") && !["luca", "joshua"].includes(firstName.toLowerCase()));
    return `Bem-vindo(a) de volta, ${isFemale ? "Dra. " : "Dr. "}${firstName}.`;
  };

  const dashboardStats = [
    { title: "Total de Pacientes", value: evaluations.length.toString(), trend: { value: 0, label: "total" }, icon: Users },
    { title: "Avaliações Ativas", value: evaluations.filter(e => e.status !== 'completed').length.toString(), trend: { value: 0, label: "em curso" }, icon: ClipboardList },
    { title: "Laudos Pendentes", value: evaluations.filter(e => e.status === 'report').length.toString(), trend: { value: 0, label: "p/ fazer" }, icon: FileText },
    { title: "Testes Aplicados", value: "...", trend: { value: 0, label: "total" }, icon: FlaskConical },
  ];

  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        subtitle={`${getGreeting()} Aqui está o resumo da sua clínica hoje.`}
        actions={
          <div className="flex items-center gap-3">
            <Link href="/dashboard/evaluations/new">
              <Button className="gap-2 shadow-spike font-bold">
                <Plus className="h-4 w-4" />
                Nova Avaliação
              </Button>
            </Link>
          </div>
        }
      />

      {/* Stats Grid */}
      <div className="mb-10 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {dashboardStats.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-8">
          <SectionCard title="Avaliações Recentes" description="Acompanhamento em tempo real dos seus processos ativos.">
            {loading ? (
              <div className="flex flex-col items-center justify-center py-20 text-slate-400">
                <Loader2 className="h-8 w-8 animate-spin mb-4" />
                <p className="text-sm font-medium">Carregando seus dados clínicos...</p>
              </div>
            ) : evaluations.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-slate-100">
                      <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">CÓDIGO</th>
                      <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">PACIENTE</th>
                      <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">STATUS</th>
                      <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">DATA INÍCIO</th>
                      <th className="pb-4"></th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-50">
                    {evaluations.map((eval_) => (
                      <tr key={eval_.id} className="group hover:bg-slate-50/50 transition-colors">
                        <td className="py-4 text-sm font-bold text-slate-900">#{eval_.id.toString().padStart(4, '0')}</td>
                        <td className="py-4">
                          <div className="flex items-center gap-3">
                            <Link
                              href={`/dashboard/patients/${eval_.patient_id}`}
                              className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/5 text-primary text-[10px] font-black transition-colors hover:bg-primary/10"
                            >
                              {eval_.patient_name?.charAt(0) || 'P'}
                            </Link>
                            <Link
                              href={`/dashboard/patients/${eval_.patient_id}`}
                              className="text-sm font-bold text-slate-700 transition-colors hover:text-primary"
                            >
                              {eval_.patient_name}
                            </Link>
                          </div>
                        </td>
                        <td className="py-4"><StatusBadge>{eval_.status}</StatusBadge></td>
                        <td className="py-4 text-xs font-medium text-slate-400">
                          {new Date(eval_.created_at).toLocaleDateString('pt-BR')}
                        </td>
                        <td className="py-4 text-right">
                          <Link href={`/dashboard/evaluations/${eval_.id}`}>
                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 opacity-0 group-hover:opacity-100 transition-opacity">
                              <ChevronRight className="h-4 w-4 text-primary" />
                            </Button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-20 text-slate-400">
                <div className="h-16 w-16 rounded-full bg-slate-50 flex items-center justify-center mb-4">
                   <Inbox className="h-8 w-8 text-slate-200" />
                </div>
                <p className="text-sm font-bold text-slate-900 mb-1">Nenhuma avaliação encontrada</p>
                <p className="text-xs font-medium text-slate-500 mb-6">Você ainda não possui processos clínicos registrados.</p>
                <Link href="/dashboard/evaluations/new">
                   <Button variant="outline" size="sm" className="font-bold gap-2">
                      <Plus className="h-4 w-4" />
                      Começar Avaliação
                   </Button>
                </Link>
              </div>
            )}
          </SectionCard>
        </div>

        <div className="space-y-8">
          <SectionCard title="Ações Rápidas">
            <div className="grid grid-cols-2 gap-4">
              {QUICK_ACTIONS.map((action) => (
                <Link key={action.title} href={action.href}>
                  <button className="flex h-24 w-full flex-col items-center justify-center gap-2 rounded-xl border border-slate-100 bg-white shadow-sm transition-all hover:border-primary/20 hover:shadow-spike group">
                    <div className={`p-2 rounded-lg ${action.bg} ${action.color} group-hover:scale-110 transition-transform`}>
                      <action.icon className="h-5 w-5" />
                    </div>
                    <span className="text-[11px] font-bold text-slate-600 uppercase tracking-wider">{action.title}</span>
                  </button>
                </Link>
              ))}
            </div>
          </SectionCard>
        </div>
      </div>
    </PageContainer>
  );
}
