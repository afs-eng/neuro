"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { PageContainer, SectionCard, SummaryCard, InfoCard } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
        <div className="flex items-center justify-center py-20">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-100 border-t-indigo-600"></div>
        </div>
      </PageContainer>
    );
  }

  if (!patient) {
    return (
      <PageContainer>
        <div className="text-center py-20">
          <p className="text-slate-500">Paciente não encontrado</p>
          <Link href="/dashboard/patients">
            <Button className="mt-4">Voltar para lista</Button>
          </Link>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      {/* Header */}
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-indigo-600 text-xl font-semibold text-white">
            {patient.full_name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-slate-900">{patient.full_name}</h1>
            <p className="text-sm text-slate-500">Paciente #{patient.id} • {age}</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2 border-slate-200">
            <Edit className="h-4 w-4" />
            Editar
          </Button>
          <Link href={`/dashboard/evaluations/new?patient=${patient.id}`}>
            <Button className="gap-2 bg-indigo-600 hover:bg-indigo-700">
              <Plus className="h-4 w-4" />
              Nova Avaliação
            </Button>
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Left Column - Tabs */}
        <div className="lg:col-span-2">
          <Tabs defaultValue="dados" className="w-full">
            <TabsList className="mb-4 grid w-full grid-cols-4 bg-slate-100 p-1">
              <TabsTrigger value="dados" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Dados</TabsTrigger>
              <TabsTrigger value="avaliacoes" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Avaliações</TabsTrigger>
              <TabsTrigger value="testes" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Testes</TabsTrigger>
              <TabsTrigger value="laudos" className="data-[state=active]:bg-white data-[state=active]:shadow-sm">Laudos</TabsTrigger>
            </TabsList>

            <TabsContent value="dados">
              <SectionCard title="Informações Pessoais" className="mb-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoCard label="Sexo" value={patient.sex === "M" ? "Masculino" : patient.sex === "F" ? "Feminino" : "—"} icon={<User className="h-4 w-4" />} />
                  <InfoCard label="Data de Nascimento" value={formatDate(patient.birth_date)} icon={<Calendar className="h-4 w-4" />} />
                  <InfoCard label="Cidade" value={patient.city || "—"} icon={<MapPin className="h-4 w-4" />} />
                  <InfoCard label="Estado" value={patient.state || "—"} icon={<MapPin className="h-4 w-4" />} />
                </div>
              </SectionCard>

              <SectionCard title="Contato" className="mb-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoCard label="Telefone" value={patient.phone || "—"} icon={<Phone className="h-4 w-4" />} />
                  <InfoCard label="Email" value={patient.email || "—"} icon={<Mail className="h-4 w-4" />} />
                </div>
              </SectionCard>

              <SectionCard title="Responsáveis">
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoCard label="Nome da Mãe" value={patient.mother_name || "—"} icon={<User className="h-4 w-4" />} />
                  <InfoCard label="Nome do Pai" value={patient.father_name || "—"} icon={<User className="h-4 w-4" />} />
                  <InfoCard label="Responsável" value={patient.responsible_name || "—"} icon={<User className="h-4 w-4" />} />
                  <InfoCard label="Telefone do Responsável" value={patient.responsible_phone || "—"} icon={<Phone className="h-4 w-4" />} />
                </div>
              </SectionCard>
            </TabsContent>

            <TabsContent value="avaliacoes">
              <SectionCard title="Histórico de Avaliações">
                <div className="text-center py-12 text-slate-500">
                  <ClipboardList className="mx-auto h-10 w-10 mb-3 text-slate-300" />
                  <p className="mb-4">Nenhuma avaliação encontrada</p>
                  <Link href={`/dashboard/evaluations/new?patient=${patient.id}`}>
                    <Button className="bg-indigo-600 hover:bg-indigo-700">Criar primeira avaliação</Button>
                  </Link>
                </div>
              </SectionCard>
            </TabsContent>

            <TabsContent value="testes">
              <SectionCard title="Testes Aplicados">
                <div className="text-center py-12 text-slate-500">
                  <FlaskConical className="mx-auto h-10 w-10 mb-3 text-slate-300" />
                  <p>Nenhum teste aplicado</p>
                </div>
              </SectionCard>
            </TabsContent>

            <TabsContent value="laudos">
              <SectionCard title="Laudos">
                <div className="text-center py-12 text-slate-500">
                  <FileText className="mx-auto h-10 w-10 mb-3 text-slate-300" />
                  <p>Nenhum laudo encontrado</p>
                </div>
              </SectionCard>
            </TabsContent>
          </Tabs>
        </div>

        {/* Right Column - Summary */}
        <div className="space-y-4">
          <SectionCard title="Informações Clínicas">
            <div className="space-y-3">
              <InfoCard label="Escolaridade" value={patient.schooling || "—"} icon={<GraduationCap className="h-4 w-4" />} />
              <InfoCard label="Escola" value={patient.school_name || "—"} icon={<GraduationCap className="h-4 w-4" />} />
              <InfoCard label="Série/Ano" value={patient.grade_year || "—"} icon={<GraduationCap className="h-4 w-4" />} />
            </div>
          </SectionCard>

          <SectionCard title="Ações Rápidas">
            <div className="space-y-2">
              <Button variant="outline" className="w-full justify-start gap-2 border-slate-200">
                <Calendar className="h-4 w-4 text-indigo-500" />
                Agendar
              </Button>
              <Button variant="outline" className="w-full justify-start gap-2 border-slate-200">
                <FileText className="h-4 w-4 text-emerald-500" />
                Gerar Laudo
              </Button>
              <Button variant="outline" className="w-full justify-start gap-2 border-slate-200">
                <Stethoscope className="h-4 w-4 text-cyan-500" />
                Aplicar Teste
              </Button>
            </div>
          </SectionCard>
        </div>
      </div>
    </PageContainer>
  );
}
