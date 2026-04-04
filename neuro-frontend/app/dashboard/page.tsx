"use client";

import React from "react";
import Link from "next/link";
import { PageContainer, PageHeader, SectionCard, SummaryCard } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import {
  Users,
  ClipboardList,
  FlaskConical,
  FileText,
  Brain,
  Plus,
  ChevronRight,
  Search,
  TrendingUp,
  TrendingDown,
  Calendar,
  Activity,
  Stethoscope,
  ClipboardCheck,
} from "lucide-react";

const STATS = [
  { 
    title: "Total de Pacientes", 
    value: "248", 
    trend: "+23%",
    trendUp: true,
    icon: <Users className="h-6 w-6" />,
    color: "bg-indigo-500"
  },
  { 
    title: "Avaliações em Andamento", 
    value: "23", 
    trend: "+8%",
    trendUp: true,
    icon: <ClipboardList className="h-6 w-6" />,
    color: "bg-cyan-500"
  },
  { 
    title: "Laudos Pendentes", 
    value: "8", 
    trend: "-5%",
    trendUp: false,
    icon: <FileText className="h-6 w-6" />,
    color: "bg-amber-500"
  },
  { 
    title: "Testes Aplicados", 
    value: "156", 
    trend: "+15%",
    trendUp: true,
    icon: <FlaskConical className="h-6 w-6" />,
    color: "bg-emerald-500"
  },
];

const RECENT_EVALUATIONS = [
  { id: "AV-2201", patient: "Marina Carvalho", examiner: "Dr. André", stage: "Coleta de dados", start: "19/03/2026", tests: 4 },
  { id: "AV-2202", patient: "João Pedro Silva", examiner: "Dr. André", stage: "Redação do laudo", start: "18/03/2026", tests: 3 },
  { id: "AV-2203", patient: "Renato Vitulli", examiner: "Dr. André", stage: "Aprovado", start: "11/03/2026", tests: 5 },
  { id: "AV-2204", patient: "Ana Clara Santos", examiner: "Dr. André", stage: "Aguardando documentos", start: "10/03/2026", tests: 2 },
];

const RECENT_PATIENTS = [
  { id: 1, name: "Marina Carvalho", age: 8, evaluation: "AV-2201", status: "Em avaliação" },
  { id: 2, name: "João Pedro Silva", age: 12, evaluation: "AV-2202", status: "Laudo" },
  { id: 3, name: "Renato Vitulli", age: 45, evaluation: "AV-2203", status: "Finalizado" },
];

function StatusBadge({ children }: { children: string }) {
  const map: Record<string, string> = {
    "Coleta de dados": "bg-amber-100 text-amber-700",
    "Redação do laudo": "bg-blue-100 text-blue-700",
    "Aprovado": "bg-emerald-100 text-emerald-700",
    "Aguardando documentos": "bg-slate-100 text-slate-600",
    "Em avaliação": "bg-amber-100 text-amber-700",
    "Laudo": "bg-blue-100 text-blue-700",
    "Finalizado": "bg-emerald-100 text-emerald-700",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${map[children] || "bg-slate-100 text-slate-600"}`}>
      {children}
    </span>
  );
}

function StatCard({ title, value, trend, trendUp, icon, color }: { 
  title: string; 
  value: string; 
  trend: string;
  trendUp: boolean;
  icon: React.ReactNode;
  color: string;
}) {
  return (
    <div className="bg-white rounded-xl p-5 border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p className="mt-2 text-3xl font-bold text-slate-900">{value}</p>
          <div className="mt-3 flex items-center gap-1.5">
            {trendUp ? (
              <TrendingUp className="h-4 w-4 text-emerald-500" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-500" />
            )}
            <span className={`text-sm font-medium ${trendUp ? "text-emerald-500" : "text-red-500"}`}>
              {trend}
            </span>
            <span className="text-sm text-slate-400">desde o mês passado</span>
          </div>
        </div>
        <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${color} text-white`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        subtitle="Visão geral das suas avaliações neuropsicológicas"
        actions={
          <Link href="/dashboard/evaluations/new">
            <Button className="gap-2 bg-indigo-600 hover:bg-indigo-700">
              <Plus className="h-4 w-4" />
              Nova Avaliação
            </Button>
          </Link>
        }
      />

      {/* Stats Grid */}
      <div className="mb-6 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        {STATS.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Recent Evaluations */}
        <SectionCard 
          title="Avaliações Recentes" 
          className="lg:col-span-2"
          actions={
            <Link href="/dashboard/evaluations">
              <Button variant="ghost" size="sm" className="text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50">
                Ver todas
                <ChevronRight className="ml-1 h-4 w-4" />
              </Button>
            </Link>
          }
        >
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-100">
                  <th className="pb-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Código</th>
                  <th className="pb-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Paciente</th>
                  <th className="pb-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Status</th>
                  <th className="pb-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Testes</th>
                  <th className="pb-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Início</th>
                  <th className="pb-3"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50">
                {RECENT_EVALUATIONS.map((eval_) => (
                  <tr key={eval_.id} className="hover:bg-slate-50/50">
                    <td className="py-3 text-sm font-medium text-slate-900">{eval_.id}</td>
                    <td className="py-3 text-sm text-slate-700">{eval_.patient}</td>
                    <td className="py-3">
                      <StatusBadge>{eval_.stage}</StatusBadge>
                    </td>
                    <td className="py-3 text-sm text-slate-600">{eval_.tests}</td>
                    <td className="py-3 text-sm text-slate-500">{eval_.start}</td>
                    <td className="py-3 text-right">
                      <Link href={`/dashboard/evaluations/${eval_.id}`}>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <ChevronRight className="h-4 w-4 text-slate-400" />
                        </Button>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </SectionCard>

        {/* Quick Actions & Activity */}
        <div className="space-y-6">
          {/* Recent Patients */}
          <SectionCard title="Pacientes Recentes">
            <div className="space-y-4">
              {RECENT_PATIENTS.map((patient) => (
                <div key={patient.id} className="flex items-center gap-3 p-2 rounded-lg hover:bg-slate-50 -mx-2 cursor-pointer">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 text-indigo-600 font-semibold text-sm">
                    {patient.name.charAt(0)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900 truncate">{patient.name}</p>
                    <p className="text-xs text-slate-500">#{patient.evaluation} • {patient.age} anos</p>
                  </div>
                  <StatusBadge>{patient.status}</StatusBadge>
                </div>
              ))}
            </div>
            <Link href="/dashboard/patients">
              <Button variant="ghost" className="w-full mt-4 text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50">
                Ver todos os pacientes
                <ChevronRight className="ml-1 h-4 w-4" />
              </Button>
            </Link>
          </SectionCard>

          {/* Quick Actions */}
          <SectionCard title="Ações Rápidas">
            <div className="grid grid-cols-2 gap-3">
              <Link href="/dashboard/patients/new">
                <Button variant="outline" className="w-full h-20 flex-col gap-2 border-slate-200 hover:border-indigo-300 hover:bg-indigo-50">
                  <Users className="h-5 w-5 text-indigo-500" />
                  <span className="text-xs">Novo Paciente</span>
                </Button>
              </Link>
              <Link href="/dashboard/tests">
                <Button variant="outline" className="w-full h-20 flex-col gap-2 border-slate-200 hover:border-cyan-300 hover:bg-cyan-50">
                  <Stethoscope className="h-5 w-5 text-cyan-500" />
                  <span className="text-xs">Aplicar Teste</span>
                </Button>
              </Link>
              <Link href="/dashboard/reports">
                <Button variant="outline" className="w-full h-20 flex-col gap-2 border-slate-200 hover:border-emerald-300 hover:bg-emerald-50">
                  <FileText className="h-5 w-5 text-emerald-500" />
                  <span className="text-xs">Gerar Laudo</span>
                </Button>
              </Link>
              <Link href="/dashboard/ai">
                <Button variant="outline" className="w-full h-20 flex-col gap-2 border-slate-200 hover:border-violet-300 hover:bg-violet-50">
                  <Brain className="h-5 w-5 text-violet-500" />
                  <span className="text-xs">IA Assistiva</span>
                </Button>
              </Link>
            </div>
          </SectionCard>
        </div>
      </div>
    </PageContainer>
  );
}
