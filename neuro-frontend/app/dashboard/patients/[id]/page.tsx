"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { PageContainer, PageHeader, SectionCard, InfoCard, EmptyState } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Calendar,
  MapPin,
  Phone,
  Mail,
  GraduationCap,
  User,
  Edit,
  Plus,
  ChevronRight,
  FileText,
  FlaskConical,
  ClipboardList,
  Stethoscope,
  Sparkles,
  ArrowLeft,
  School
} from "lucide-react";

export const dynamic = "force-dynamic";

interface Patient {
  id: number;
  full_name: string;
  birth_date: string;
  sex: string;
  schooling: string;
  school_name: string;
  grade_year?: string;
  city?: string;
  state?: string;
  phone?: string;
  email?: string;
  mother_name?: string;
  father_name?: string;
  responsible_name?: string;
  responsible_phone?: string;
}

function calculateAge(birthDate: string | undefined | null): string {
  if (!birthDate) return "—";
  const birth = new Date(birthDate);
  const today = new Date();
  if (isNaN(birth.getTime())) return "—";

  let years = today.getFullYear() - birth.getFullYear();
  let months = today.getMonth() - birth.getMonth();

  if (today.getDate() < birth.getDate()) months--;
  if (months < 0) { years--; months += 12; }

  if (years <= 0) return `${months} ${months === 1 ? "mês" : "meses"}`;
  return `${years} ${years === 1 ? "ano" : "anos"}`;
}

function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return "—";
  try {
    return new Date(dateStr).toLocaleDateString("pt-BR");
  } catch {
    return "—";
  }
}

export default function PatientDetailPage() {
  const params = useParams();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPatient();
  }, [params.id]);

  async function fetchPatient() {
    try {
      setLoading(true);
      const data = await api.get<Patient>(`/api/patients/${params.id}`);
      setPatient(data);
    } catch (err) {
      console.error("Erro ao buscar paciente:", err);
    } finally {
      setLoading(false);
    }
  }

  const age = useMemo(() => calculateAge(patient?.birth_date), [patient?.birth_date]);

  if (loading) {
    return (
      <PageContainer>
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-100 border-t-primary"></div>
          <p className="text-sm font-bold text-slate-400 uppercase tracking-widest animate-pulse">Carregando Prontuário...</p>
        </div>
      </PageContainer>
    );
  }

  if (!patient) {
    return (
      <PageContainer>
        <EmptyState 
          title="Paciente não encontrado" 
          description="O prontuário solicitado não existe ou foi removido."
          icon={<User className="h-12 w-12 text-slate-200" />}
          action={
            <Link href="/dashboard/patients">
              <Button variant="outline" className="gap-2 font-bold">
                <ArrowLeft className="h-4 w-4" />
                Voltar para Lista
              </Button>
            </Link>
          }
        />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title={patient.full_name}
        breadcrumbs={
          <Link href="/dashboard/patients" className="inline-flex items-center text-xs font-bold text-primary uppercase tracking-widest hover:underline gap-1">
            <ArrowLeft className="h-3 w-3" />
            Base de Pacientes
          </Link>
        }
        subtitle={`ID #${String(patient.id).padStart(4, '0')} • ${age} • Prontuário Ativo`}
        actions={
          <div className="flex gap-3">
            <Button variant="outline" className="gap-2 border-slate-100 font-bold hover:bg-slate-50 transition-all">
              <Edit className="h-4 w-4 text-slate-400" />
              Editar Prontuário
            </Button>
            <Link href={`/dashboard/evaluations/new?patient=${patient.id}`}>
              <Button className="gap-2 shadow-spike font-bold">
                <Plus className="h-4 w-4" />
                Nova Avaliação
              </Button>
            </Link>
          </div>
        }
      />

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Left Column - Detailed Tabs */}
        <div className="lg:col-span-2 space-y-8">
          <div className="flex h-[350px] w-full items-center justify-center rounded-3xl bg-gradient-to-br from-primary/10 via-primary/5 to-white border border-primary/10 overflow-hidden relative group">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(0,128,128,0.05),transparent)] pointer-events-none" />
            <div className="flex flex-col items-center gap-4 text-center z-10">
              <div className="flex h-24 w-24 items-center justify-center rounded-3xl bg-white border border-primary/20 text-primary text-4xl font-black shadow-xl group-hover:scale-105 transition-transform duration-500">
                {patient.full_name?.charAt(0).toUpperCase()}
              </div>
              <div className="space-y-1">
                <h2 className="text-2xl font-black text-slate-900">{patient.full_name}</h2>
                <div className="flex items-center justify-center gap-2">
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black tracking-[0.1em] uppercase border ${
                    patient.sex === "M" ? "bg-blue-50 text-blue-600 border-blue-100" : "bg-pink-50 text-pink-600 border-pink-100"
                  }`}>
                    {patient.sex === "M" ? "Masculino" : "Feminino"}
                  </span>
                  <span className="h-1 w-1 rounded-full bg-slate-300" />
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{formatDate(patient.birth_date)}</span>
                </div>
              </div>
            </div>
          </div>

          <Tabs defaultValue="dados" className="w-full">
            <TabsList className="mb-0 grid w-full grid-cols-4 bg-slate-100/50 p-1 rounded-t-xl border-x border-t border-slate-100">
              <TabsTrigger value="dados" className="rounded-lg font-bold text-xs uppercase tracking-widest data-[state=active]:bg-white data-[state=active]:text-primary data-[state=active]:shadow-sm transition-all py-3">Dados Cadastrais</TabsTrigger>
              <TabsTrigger value="avaliacoes" className="rounded-lg font-bold text-xs uppercase tracking-widest data-[state=active]:bg-white data-[state=active]:text-primary data-[state=active]:shadow-sm transition-all py-3">Avaliações</TabsTrigger>
              <TabsTrigger value="testes" className="rounded-lg font-bold text-xs uppercase tracking-widest data-[state=active]:bg-white data-[state=active]:text-primary data-[state=active]:shadow-sm transition-all py-3">Testes</TabsTrigger>
              <TabsTrigger value="laudos" className="rounded-lg font-bold text-xs uppercase tracking-widest data-[state=active]:bg-white data-[state=active]:text-primary data-[state=active]:shadow-sm transition-all py-3">Laudos</TabsTrigger>
            </TabsList>

            <div className="bg-white border border-slate-100 rounded-b-xl p-8">
              <TabsContent value="dados" className="mt-0 space-y-8 animate-in fade-in duration-500">
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-4">
                    <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-4">Informações de Contato</h4>
                    <InfoCard label="Celular/WhatsApp" value={patient.phone || "Não informado"} icon={Phone} />
                    <InfoCard label="E-mail" value={patient.email || "Não informado"} icon={Mail} />
                    <InfoCard label="Cidade Atual" value={patient.city || "Não informado"} icon={MapPin} />
                  </div>
                  <div className="space-y-4">
                    <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em] mb-4">Núcleo Familiar</h4>
                    <InfoCard label="Mãe" value={patient.mother_name || "Não informado"} icon={User} />
                    <InfoCard label="Pai" value={patient.father_name || "Não informado"} icon={User} />
                    <InfoCard label="Responsável Legal" value={patient.responsible_name || "Mesmo acima"} icon={User} />
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="avaliacoes" className="mt-0 animate-in fade-in duration-500">
                <EmptyState
                  title="Nenhuma avaliação registrada"
                  description="Ainda não foram iniciados processos clínicos para este paciente."
                  icon={<ClipboardList className="h-10 w-10 text-slate-200" />}
                  action={
                    <Link href={`/dashboard/evaluations/new?patient=${patient.id}`}>
                      <Button className="font-bold shadow-sm">Iniciar Primeira Avaliação</Button>
                    </Link>
                  }
                />
              </TabsContent>

              <TabsContent value="testes" className="mt-0 animate-in fade-in duration-500">
                <EmptyState
                  title="Histórico de testes vazio"
                  description="Os testes aparecerão aqui após a aplicação em uma avaliação."
                  icon={<FlaskConical className="h-10 w-10 text-slate-200" />}
                />
              </TabsContent>

              <TabsContent value="laudos" className="mt-0 animate-in fade-in duration-500">
                <EmptyState
                  title="Nenhum laudo emitido"
                  description="Os laudos finalizados serão listados aqui para download."
                  icon={<FileText className="h-10 w-10 text-slate-200" />}
                />
              </TabsContent>
            </div>
          </Tabs>
        </div>

        {/* Right Column - Clinical Summary */}
        <div className="space-y-8">
          <SectionCard title="Contexto Clínico" description="Informações acadêmicas e triagem.">
            <div className="space-y-4">
              <InfoCard label="Nível Escolar" value={patient.schooling || "Não informado"} icon={GraduationCap} />
              <InfoCard label="Instituição" value={patient.school_name || "Não informado"} icon={School} />
              <InfoCard label="Série/Ano" value={patient.grade_year || "Não informado"} icon={Calendar} />
            </div>
          </SectionCard>

          <SectionCard title="Ações Rápidas">
            <div className="space-y-3">
              <Button variant="outline" className="w-full justify-between gap-3 border-slate-100 font-bold hover:bg-slate-50 group">
                <div className="flex items-center gap-3">
                  <Calendar className="h-4 w-4 text-primary" />
                  <span>Agendar Consulta</span>
                </div>
                <ChevronRight className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
              </Button>
              <Button variant="outline" className="w-full justify-between gap-3 border-slate-100 font-bold hover:bg-slate-50 group">
                <div className="flex items-center gap-3">
                  <Stethoscope className="h-4 w-4 text-emerald-500" />
                  <span>Aplicar Novo Teste</span>
                </div>
                <ChevronRight className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
              </Button>
              <Button variant="outline" className="w-full justify-between gap-3 border-slate-100 font-bold hover:bg-slate-50 group">
                <div className="flex items-center gap-3">
                  <FileText className="h-4 w-4 text-amber-500" />
                  <span>Solicitar Documentos</span>
                </div>
                <ChevronRight className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
              </Button>
            </div>
          </SectionCard>

          <div className="p-6 rounded-2xl bg-slate-50 border border-slate-100 relative overflow-hidden group">
            <Sparkles className="absolute -right-4 -bottom-4 h-24 w-24 text-primary/5 transition-transform group-hover:scale-110" />
            <h5 className="text-xs font-black uppercase tracking-widest text-primary mb-2">IA Assistiva</h5>
            <p className="text-sm font-bold text-slate-900 leading-tight">Gere um rascunho de anamnese baseado nos dados cadastrais.</p>
            <Button size="sm" className="mt-4 w-full font-black text-[10px] uppercase tracking-widest">Gerar Resumo IA</Button>
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
