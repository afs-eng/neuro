"use client";

import React, { useState, useEffect, useMemo } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { getEvaluationDeadlineMeta } from "@/lib/evaluation-deadline";
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
  School,
  Trash2,
  AlertTriangle
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

interface Evaluation {
  id: number;
  code: string;
  title: string;
  status_display: string;
  priority_display: string;
  start_date: string | null;
  end_date: string | null;
  status: string;
}

interface TestApplication {
  id: number;
  instrument_name: string;
  instrument_code: string;
  applied_on: string | null;
  is_validated: boolean;
  status: string;
}

interface Report {
  id: number;
  evaluation_id?: number;
  evaluation_code: string;
  evaluation_title: string;
  author_name: string;
  status: string;
  created_at: string;
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

function formatDateTime(dateStr: string | null | undefined): string {
  if (!dateStr) return "—";
  try {
    return new Date(dateStr).toLocaleDateString("pt-BR");
  } catch {
    return "—";
  }
}

export default function PatientDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [tests, setTests] = useState<TestApplication[]>([]);
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleteEvaluationId, setDeleteEvaluationId] = useState<number | null>(null);
  const [deleteConfirmationOpen, setDeleteConfirmationOpen] = useState(false);
  const [deletingEvaluation, setDeletingEvaluation] = useState(false);
  const [deleteReportId, setDeleteReportId] = useState<number | null>(null);
  const [deleteReportConfirmationOpen, setDeleteReportConfirmationOpen] = useState(false);
  const [deletingReport, setDeletingReport] = useState(false);

  useEffect(() => {
    fetchPatientData();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params.id]);

  async function fetchPatientData() {
    try {
      setLoading(true);

      // Fetch patient
      const patientData = await api.get<Patient>(`/api/patients/${params.id}`);
      setPatient(patientData);

      // Fetch evaluations for this patient
      const evaluationsData = await api.get<Evaluation[]>(`/api/evaluations/?patient_id=${params.id}`);
      setEvaluations(evaluationsData);

      // Collect all tests and reports from evaluations
      const allTests: TestApplication[] = [];
      const allReports: Report[] = [];

      for (const evaluation of evaluationsData) {
        // Fetch evaluation details (includes tests)
        try {
          const detailData = await api.get<any>(`/api/evaluations/${evaluation.id}`);
          if (detailData.tests && detailData.tests.length > 0) {
            allTests.push(...detailData.tests.map((t: any) => ({
              ...t,
              evaluation_code: evaluation.code,
              evaluation_title: evaluation.title,
            })));
          }
        } catch (err) {
          console.error(`Erro ao buscar detalhes da avaliação ${evaluation.id}:`, err);
        }

        // Fetch reports for this evaluation
        try {
          const reportsData = await api.get<Report[]>(`/api/reports/?evaluation_id=${evaluation.id}`);
          if (reportsData && reportsData.length > 0) {
            allReports.push(...reportsData);
          }
        } catch (err) {
          console.error(`Erro ao buscar laudos da avaliação ${evaluation.id}:`, err);
        }
      }

      setTests(allTests);
      setReports(allReports);
    } catch (err) {
      console.error("Erro ao buscar dados do paciente:", err);
    } finally {
      setLoading(false);
    }
  }

  function handleOpenDeleteDialog(evaluationId: number) {
    setDeleteEvaluationId(evaluationId);
    setDeleteConfirmationOpen(true);
  }

  function handleCloseDeleteDialog() {
    setDeleteEvaluationId(null);
    setDeleteConfirmationOpen(false);
  }

  function handleOpenDeleteReportDialog(reportId: number) {
    setDeleteReportId(reportId);
    setDeleteReportConfirmationOpen(true);
  }

  function handleCloseDeleteReportDialog() {
    setDeleteReportId(null);
    setDeleteReportConfirmationOpen(false);
  }

  async function handleDeleteEvaluation() {
    if (!deleteEvaluationId) return;

    try {
      setDeletingEvaluation(true);
      await api.delete(`/api/evaluations/${deleteEvaluationId}`);

      // Remove from local state
      setEvaluations(prev => prev.filter(e => e.id !== deleteEvaluationId));
      setTests(prev => prev.filter(t => !("evaluation_code" in t) || t.evaluation_code !== evaluations.find(e => e.id === deleteEvaluationId)?.code));

      handleCloseDeleteDialog();

      // Refresh data
      fetchPatientData();
    } catch (err) {
      console.error("Erro ao excluir avaliação:", err);
      alert("Não foi possível excluir a avaliação. Tente novamente.");
    } finally {
      setDeletingEvaluation(false);
    }
  }

  async function handleDeleteReport() {
    if (!deleteReportId) return;

    try {
      setDeletingReport(true);
      await api.delete(`/api/reports/${deleteReportId}`);
      setReports((prev) => prev.filter((report) => report.id !== deleteReportId));
      handleCloseDeleteReportDialog();
      fetchPatientData();
    } catch (err) {
      console.error("Erro ao excluir laudo:", err);
      alert("Não foi possível excluir o laudo. Tente novamente.");
    } finally {
      setDeletingReport(false);
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
            <Link href={`/dashboard/evaluations/new?patient_id=${patient.id}`}>
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
                {evaluations.length === 0 ? (
                  <EmptyState
                    title="Nenhuma avaliação registrada"
                    description="Ainda não foram iniciados processos clínicos para este paciente."
                    icon={<ClipboardList className="h-10 w-10 text-slate-200" />}
                    action={
                      <Link href={`/dashboard/evaluations/new?patient_id=${patient.id}`}>
                        <Button className="font-bold shadow-sm">Iniciar Primeira Avaliação</Button>
                      </Link>
                    }
                  />
                ) : (
                  <div className="space-y-4">
                    {evaluations.map((evaluation) => (
                      (() => {
                        const deadlineMeta = getEvaluationDeadlineMeta(evaluation.end_date, evaluation.status);

                        return (
                          <div
                            key={evaluation.id}
                            className="group flex items-start justify-between gap-4 rounded-xl border border-slate-100 p-4 transition-all hover:border-primary/30 hover:bg-slate-50"
                          >
                           <Link
                              href={`/dashboard/evaluations/${evaluation.id}/overview`}
                              className="flex flex-1 items-start gap-4"
                            >
                              <div className="space-y-1 flex-1">
                                <div className="flex items-center gap-2">
                                  <span className="text-xs font-black text-primary">{evaluation.code}</span>
                                  <span className="h-1 w-1 rounded-full bg-slate-300" />
                                  <span className="text-sm font-bold text-slate-900">{evaluation.title || "Sem título"}</span>
                                </div>
                                <div className="flex items-center gap-3 text-xs text-slate-500">
                                  <span className="font-semibold">{evaluation.status_display}</span>
                                  <span className="h-1 w-1 rounded-full bg-slate-300" />
                                  <span>{evaluation.priority_display}</span>
                                  {evaluation.start_date && (
                                    <>
                                      <span className="h-1 w-1 rounded-full bg-slate-300" />
                                     <span>Início: {formatDate(evaluation.start_date)}</span>
                                    </>
                                  )}
                                </div>
                                <div className="mt-2 flex flex-wrap items-center gap-2">
                                  <span className={`rounded-full border px-2.5 py-1 text-[10px] font-black uppercase tracking-widest ${deadlineMeta.badgeClassName}`}>
                                    {deadlineMeta.label}
                                </span>
                                <span className="text-xs text-slate-400">{deadlineMeta.helperText}</span>
                                </div>
                              </div>
                            </Link>
                            <div className="flex items-center gap-2">
                              <Link
                                href={`/dashboard/evaluations/${evaluation.id}/overview`}
                                className="shrink-0"
                              >
                                <Button variant="ghost" size="sm" className="h-9 w-9 p-0 text-primary opacity-0 transition-opacity group-hover:opacity-100 hover:bg-primary/5">
                                  <ChevronRight className="h-5 w-5" />
                                </Button>
                              </Link>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-9 w-9 p-0 text-red-400 opacity-0 transition-opacity group-hover:opacity-100 hover:bg-red-50 hover:text-red-600"
                                onClick={() => handleOpenDeleteDialog(evaluation.id)}
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                        );
                      })()
                    ))}
                  </div>
                )}
              </TabsContent>

              <TabsContent value="testes" className="mt-0 animate-in fade-in duration-500">
                {tests.length === 0 ? (
                  <EmptyState
                    title="Histórico de testes vazio"
                    description="Os testes aparecerão aqui após a aplicação em uma avaliação."
                    icon={<FlaskConical className="h-10 w-10 text-slate-200" />}
                  />
                ) : (
                  <div className="space-y-4">
                    {tests.map((test) => {
                      // Montar a URL do resultado do teste
                      const testCodeNormalized = test.instrument_code.replace(/-/g, '_').toLowerCase();
                      const resultUrl = `/dashboard/tests/${testCodeNormalized}/${test.id}/result`;

                      return (
                        <div
                          key={test.id}
                          className="group p-4 rounded-xl border border-slate-100 hover:border-primary/30 hover:bg-slate-50 transition-all"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="space-y-1 flex-1">
                              <div className="flex items-center gap-2">
                                <Link
                                  href={resultUrl}
                                  className="text-sm font-bold text-slate-900 transition-colors hover:text-primary"
                                >
                                  {test.instrument_name}
                                </Link>
                                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black tracking-[0.1em] uppercase border ${
                                  test.is_validated
                                    ? "bg-emerald-50 text-emerald-600 border-emerald-100"
                                    : "bg-amber-50 text-amber-600 border-amber-100"
                                }`}>
                                  {test.is_validated ? "Validado" : "Pendente"}
                                </span>
                              </div>
                              <div className="flex items-center gap-3 text-xs text-slate-500">
                                <span>Código: {test.instrument_code}</span>
                                {test.applied_on && (
                                  <>
                                    <span className="h-1 w-1 rounded-full bg-slate-300" />
                                    <span>Aplicado em: {formatDate(test.applied_on)}</span>
                                  </>
                                )}
                                {(test as any).evaluation_code && (
                                  <>
                                    <span className="h-1 w-1 rounded-full bg-slate-300" />
                                    <span className="text-primary font-semibold">{(test as any).evaluation_code}</span>
                                  </>
                                )}
                              </div>
                            </div>
                            <Link href={resultUrl}>
                              <ChevronRight className="h-5 w-5 text-slate-300 group-hover:text-primary transition-colors" />
                            </Link>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </TabsContent>

              <TabsContent value="laudos" className="mt-0 animate-in fade-in duration-500">
                {reports.length === 0 ? (
                  <EmptyState
                    title="Nenhum laudo emitido"
                    description="Os laudos finalizados serão listados aqui para download."
                    icon={<FileText className="h-10 w-10 text-slate-200" />}
                  />
                ) : (
                  <div className="space-y-4">
                    {reports.map((report) => (
                      <div
                        key={report.id}
                        className="p-4 rounded-xl border border-slate-100 hover:border-primary/30 hover:bg-slate-50 transition-all group"
                      >
                        <div className="flex items-center justify-between gap-4">
                          <Link href={`/dashboard/evaluations/${report.evaluation_id}/report`} className="flex min-w-0 flex-1 items-center justify-between gap-4">
                            <div className="space-y-1 flex-1 min-w-0">
                              <div className="flex items-center gap-2">
                                <FileText className="h-4 w-4 text-primary" />
                                <span className="text-sm font-bold text-slate-900">{report.evaluation_title || report.evaluation_code}</span>
                              </div>
                              <div className="flex items-center gap-3 text-xs text-slate-500 flex-wrap">
                                <span>Autor: {report.author_name}</span>
                                <span className="h-1 w-1 rounded-full bg-slate-300" />
                                <span>Criado em: {formatDateTime(report.created_at)}</span>
                                <span className="h-1 w-1 rounded-full bg-slate-300" />
                                <span className={`font-semibold ${
                                  report.status === "finalized" ? "text-emerald-600" : "text-amber-600"
                                }`}>
                                  {report.status === "finalized" ? "Finalizado" : "Em andamento"}
                                </span>
                              </div>
                            </div>
                            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-300 transition-colors group-hover:border-primary/20 group-hover:text-primary">
                              <ChevronRight className="h-5 w-5" />
                            </div>
                          </Link>
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="h-9 w-9 shrink-0 rounded-full text-slate-400 hover:bg-red-50 hover:text-red-600"
                            onClick={() => handleOpenDeleteReportDialog(report.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
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

          <SectionCard title="Resumo Clínico">
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Avaliações</span>
                <span className="text-lg font-black text-primary">{evaluations.length}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Testes Aplicados</span>
                <span className="text-lg font-black text-primary">{tests.length}</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50">
                <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Laudos</span>
                <span className="text-lg font-black text-primary">{reports.length}</span>
              </div>
            </div>
          </SectionCard>

          <SectionCard title="Ações Rápidas">
            <div className="space-y-3">
              <Link href={`/dashboard/evaluations/new?patient_id=${patient.id}`} className="block">
                <Button variant="outline" className="w-full justify-between gap-3 border-slate-100 font-bold hover:bg-slate-50 group">
                  <div className="flex items-center gap-3">
                    <ClipboardList className="h-4 w-4 text-primary" />
                    <span>Nova Avaliação</span>
                  </div>
                  <ChevronRight className="h-4 w-4 text-slate-300 group-hover:text-primary transition-colors" />
                </Button>
              </Link>
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

      {/* Delete Evaluation Confirmation Dialog */}
      {deleteConfirmationOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-red-50">
                <AlertTriangle className="h-6 w-6 text-red-500" />
              </div>
              <div className="flex-1 space-y-2">
                <h3 className="text-lg font-bold text-slate-900">Excluir Avaliação?</h3>
                <p className="text-sm text-slate-600">
                  Esta ação irá remover permanentemente a avaliação e todos os dados vinculados:
                </p>
                <ul className="ml-4 list-disc space-y-1 text-xs text-slate-500">
                  <li>Testes aplicados e resultados</li>
                  <li>Evoluções clínicas</li>
                  <li>Documentos anexados</li>
                  <li>Anamneses vinculadas</li>
                  <li>Laudos gerados</li>
                </ul>
                <p className="text-sm font-bold text-red-600">Esta ação não pode ser desfeita.</p>
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-3">
              <Button
                variant="outline"
                className="font-bold"
                onClick={handleCloseDeleteDialog}
                disabled={deletingEvaluation}
              >
                Cancelar
              </Button>
              <Button
                variant="destructive"
                className="font-bold"
                onClick={handleDeleteEvaluation}
                disabled={deletingEvaluation}
              >
                {deletingEvaluation ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    Excluindo...
                  </>
                ) : (
                  <>
                    <Trash2 className="mr-2 h-4 w-4" />
                    Sim, Excluir
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}

      {deleteReportConfirmationOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-red-50">
                <AlertTriangle className="h-6 w-6 text-red-500" />
              </div>
              <div className="flex-1 space-y-2">
                <h3 className="text-lg font-bold text-slate-900">Excluir Laudo?</h3>
                <p className="text-sm text-slate-600">
                  Esta ação irá remover permanentemente o laudo selecionado.
                </p>
                <p className="text-sm font-bold text-red-600">Esta ação não pode ser desfeita.</p>
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-3">
              <Button
                variant="outline"
                className="font-bold"
                onClick={handleCloseDeleteReportDialog}
                disabled={deletingReport}
              >
                Cancelar
              </Button>
              <Button
                variant="destructive"
                className="font-bold"
                onClick={handleDeleteReport}
                disabled={deletingReport}
              >
                {deletingReport ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    Excluindo...
                  </>
                ) : (
                  <>
                    <Trash2 className="mr-2 h-4 w-4" />
                    Sim, Excluir
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
