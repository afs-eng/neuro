"use client";

import React from "react";
import Link from "next/link";
import { PageContainer, PageHeader, SectionCard, StatCard, InfoCard } from "@/components/ui/page";
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
  Activity,
  Calendar,
  Search,
  MessageSquare,
  Sparkles
} from "lucide-react";

const STATS = [
  { 
    title: "Total de Pacientes", 
    value: "248", 
    trend: { value: 23, label: "este mês" },
    icon: Users
  },
  { 
    title: "Avaliações Ativas", 
    value: "23", 
    trend: { value: 8, label: "esta semana" },
    icon: ClipboardList
  },
  { 
    title: "Laudos Pendentes", 
    value: "8", 
    trend: { value: -5, label: "vs mês ant." },
    icon: FileText
  },
  { 
    title: "Testes Aplicados", 
    value: "156", 
    trend: { value: 15, label: "total hoje" },
    icon: FlaskConical
  },
];

const RECENT_EVALUATIONS = [
  { id: "AV-2201", patient: "Marina Carvalho", stage: "Coleta de dados", start: "Hoje, 10:30", tests: 4 },
  { id: "AV-2202", patient: "João Pedro Silva", stage: "Redação do laudo", start: "Ontem, 16:45", tests: 3 },
  { id: "AV-2203", patient: "Renato Vitulli", stage: "Finalizado", start: "11/03/2026", tests: 5 },
  { id: "AV-2204", patient: "Ana Clara Santos", stage: "Documentação", start: "10/03/2026", tests: 2 },
];

const QUICK_ACTIONS = [
  { title: "Novo Paciente", icon: Users, href: "/dashboard/patients/new", color: "text-blue-600", bg: "bg-blue-50" },
  { title: "Aplicar Teste", icon: Stethoscope, href: "/dashboard/tests", color: "text-primary", bg: "bg-primary/10" },
  { title: "Gerar Laudo", icon: FileText, href: "/dashboard/reports", color: "text-amber-600", bg: "bg-amber-50" },
  { title: "IA Clínica", icon: Sparkles, href: "/dashboard/ai", color: "text-purple-600", bg: "bg-purple-50" },
];

function StatusBadge({ children }: { children: string }) {
  const map: Record<string, string> = {
    "Coleta de dados": "text-amber-600 bg-amber-50 border-amber-100",
    "Redação do laudo": "text-primary bg-primary/10 border-primary/20",
    "Finalizado": "text-emerald-600 bg-emerald-50 border-emerald-100",
    "Documentação": "text-slate-500 bg-slate-50 border-slate-100",
  };
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${map[children] || "bg-slate-50 text-slate-500 border-slate-100"}`}>
      {children}
    </span>
  );
}

export default function DashboardPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Dashboard"
        subtitle="Bem-vindo de volta, Dr. André. Aqui está o resumo da sua clínica hoje."
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
        {STATS.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Recent Evaluations */}
        <div className="lg:col-span-2 space-y-8">
          <SectionCard 
            title="Avaliações Recentes" 
            description="Acompanhamento em tempo real dos processos ativos."
            actions={
              <Link href="/dashboard/evaluations">
                <Button variant="ghost" size="sm" className="font-bold text-primary hover:bg-primary/5">
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
                    <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">CÓDIGO</th>
                    <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">PACIENTE</th>
                    <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">STATUS</th>
                    <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">TESTES</th>
                    <th className="pb-4 text-left text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">ÚLTIMA ATUALIZAÇÃO</th>
                    <th className="pb-4"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                  {RECENT_EVALUATIONS.map((eval_) => (
                    <tr key={eval_.id} className="group hover:bg-slate-50/50 transition-colors">
                      <td className="py-4 text-sm font-bold text-slate-900">{eval_.id}</td>
                      <td className="py-4">
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary/5 text-primary text-[10px] font-black">
                            {eval_.patient.charAt(0)}
                          </div>
                          <span className="text-sm font-bold text-slate-700">{eval_.patient}</span>
                        </div>
                      </td>
                      <td className="py-4">
                        <StatusBadge>{eval_.stage}</StatusBadge>
                      </td>
                      <td className="py-4 text-sm font-bold text-slate-600">{eval_.tests}</td>
                      <td className="py-4 text-xs font-medium text-slate-400">{eval_.start}</td>
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
          </SectionCard>

          <div className="grid gap-6 md:grid-cols-2">
            <SectionCard title="Atividade da IA" description="Insights gerados recentemente.">
              <div className="space-y-4">
                <div className="flex gap-3 p-3 rounded-xl bg-primary/5 border border-primary/10">
                  <Sparkles className="h-5 w-5 text-primary shrink-0" />
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-slate-900">Análise de WISC-IV Concluída</p>
                    <p className="text-[11px] text-slate-500 font-medium">Padrão de discrepância identificado para Marina Carvalho.</p>
                  </div>
                </div>
                <div className="flex gap-3 p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <Brain className="h-5 w-5 text-slate-400 shrink-0" />
                  <div className="space-y-1">
                    <p className="text-xs font-bold text-slate-900">Sugestão de Teste Adicional</p>
                    <p className="text-[11px] text-slate-500 font-medium">Considere Raven para avaliar inteligência fluida em João Silva.</p>
                  </div>
                </div>
              </div>
            </SectionCard>
            
            <SectionCard title="Próximas Sessões" description="Agenda de hoje.">
              <div className="space-y-3">
                <div className="flex items-center justify-between p-2">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-primary" />
                    <span className="text-sm font-bold text-slate-700">14:00 - Marina C.</span>
                  </div>
                  <span className="text-[10px] font-black text-slate-400">EM 15 MIN</span>
                </div>
                <div className="flex items-center justify-between p-2">
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-slate-200" />
                    <span className="text-sm font-bold text-slate-500">16:30 - Pedro L.</span>
                  </div>
                  <span className="text-[10px] font-black text-slate-400 underline cursor-pointer hover:text-primary">ABRIR</span>
                </div>
              </div>
            </SectionCard>
          </div>
        </div>

        {/* Sidebar Actions & Info */}
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

          <SectionCard title="Recursos do Sistema">
            <div className="space-y-4">
              <InfoCard label="Pacientes Novos" value="12 esta semana" icon={Users} />
              <InfoCard label="Laudos Finalizados" value="45 no mês" icon={FileText} />
              <InfoCard label="Uso de IA" value="85% das avaliações" icon={Sparkles} />
            </div>
          </SectionCard>

          <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 text-white shadow-xl relative overflow-hidden group">
            <Brain className="absolute -right-4 -bottom-4 h-32 w-32 text-white/5 rotate-12 group-hover:rotate-0 transition-transform duration-700" />
            <p className="text-xs font-black uppercase tracking-[0.2em] text-white/40 mb-2">Suporte Premium</p>
            <h5 className="text-lg font-black leading-tight mb-4">Gerencie sua clínica com precisão cirúrgica.</h5>
            <Button variant="secondary" className="w-full font-black text-xs uppercase tracking-widest bg-white text-slate-900 hover:bg-slate-100">
              Falar com Suporte
            </Button>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
