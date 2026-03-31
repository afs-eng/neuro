"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, User, Calendar, FileText, ClipboardList, FolderOpen, StickyNote, Plus, X } from "lucide-react";
import { api } from "@/lib/api";

interface Instrument {
  id: number;
  code: string;
  name: string;
  category: string;
  version: string;
  is_active: boolean;
}

interface Evaluation {
  id: number;
  code: string;
  title: string;
  patient_id: number;
  patient_name: string;
  patient_birth_date: string | null;
  patient_sex: string | null;
  examiner_name: string | null;
  referral_reason: string;
  evaluation_purpose: string;
  clinical_hypothesis: string;
  start_date: string | null;
  end_date: string | null;
  status: string;
  status_display: string;
  priority: string;
  priority_display: string;
  is_archived: boolean;
  general_notes: string;
  tests: TestApp[];
  documents: any[];
  created_at: string;
}

interface TestApp {
  id: number;
  instrument_name: string;
  instrument_code: string;
  applied_on: string | null;
  is_validated: boolean;
  status: string;
}

const STATUS_COLORS: Record<string, string> = {
  draft: "bg-slate-100 text-slate-700",
  collecting_data: "bg-amber-50 text-amber-700 border-amber-200",
  tests_in_progress: "bg-blue-50 text-blue-700 border-blue-200",
  scoring: "bg-purple-50 text-purple-700 border-purple-200",
  writing_report: "bg-orange-50 text-orange-700 border-orange-200",
  in_review: "bg-indigo-50 text-indigo-700 border-indigo-200",
  approved: "bg-emerald-50 text-emerald-700 border-emerald-200",
  archived: "bg-slate-100 text-slate-500",
};

type TabType = "overview" | "tests" | "documents" | "evolution" | "report";

export default function EvaluationDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [showAddTestModal, setShowAddTestModal] = useState(false);
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [loadingInstruments, setLoadingInstruments] = useState(false);
  const [addingTest, setAddingTest] = useState(false);

  useEffect(() => {
    async function fetchEvaluation() {
      try {
        const data = await api.get<Evaluation>(`/api/evaluations/${params.id}`);
        setEvaluation(data);
      } catch (err) {
        console.error("Erro ao buscar avaliação:", err);
      } finally {
        setLoading(false);
      }
    }
    if (params.id) {
      fetchEvaluation();
    }
  }, [params.id]);

  async function loadInstruments() {
    setLoadingInstruments(true);
    try {
      const data = await api.get<Instrument[]>("/api/tests/instruments/");
      setInstruments(data);
    } catch (err: any) {
      console.error("Erro ao carregar instrumentos:", err);
      alert("Erro ao carregar instrumentos: " + (err?.message || "Ver console"));
    } finally {
      setLoadingInstruments(false);
    }
  }

  async function addTest(instrumentId: number) {
    if (!evaluation) return;
    setAddingTest(true);
    try {
      const newTest = await api.post<any>("/api/tests/applications/", {
        evaluation_id: evaluation.id,
        instrument_id: instrumentId,
      });
      setEvaluation({
        ...evaluation,
        tests: [...evaluation.tests, {
          id: newTest.id,
          instrument_name: newTest.instrument_name,
          instrument_code: newTest.instrument_code,
          applied_on: newTest.applied_on,
          is_validated: newTest.is_validated,
          status: newTest.is_validated ? "Concluído" : "Pendente"
        }]
      });
      setShowAddTestModal(false);
    } catch (err) {
      console.error("Erro ao adicionar teste:", err);
      alert("Erro ao adicionar teste");
    } finally {
      setAddingTest(false);
    }
  }

  function openAddTestModal() {
    setShowAddTestModal(true);
    if (instruments.length === 0) {
      loadInstruments();
    }
  }

  function getTestUrl(instrumentCode: string, testId: number): string {
    const baseUrls: Record<string, string> = {
      "wisc4": "/dashboard/tests/wisc4",
      "bpa2": "/dashboard/tests/bpa2",
      "ebadep_a": "/dashboard/tests/ebadep-a",
      "ebadep_ij": "/dashboard/tests/ebadep-ij",
      "ebaped_ij": "/dashboard/tests/ebaped-ij",
      "epq_j": "/dashboard/tests/epq-j",
      "etdah_ad": "/dashboard/tests/etdah-ad",
    };
    return `${baseUrls[instrumentCode] || "/dashboard/tests"}?evaluation_id=${evaluation?.id}&application_id=${testId}`;
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Carregando...</div>
      </div>
    );
  }

  if (!evaluation) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Avaliação não encontrada</div>
      </div>
    );
  }

  const tabs = [
    { id: "overview" as TabType, label: "Visão Geral", icon: User },
    { id: "tests" as TabType, label: "Testes", icon: ClipboardList },
    { id: "documents" as TabType, label: "Documentos", icon: FolderOpen },
    { id: "evolution" as TabType, label: "Evolução", icon: StickyNote },
    { id: "report" as TabType, label: "Laudo", icon: FileText },
  ];

  const getTestesDisponiveis = () => {
    const codes = evaluation.tests.map(t => t.instrument_code);
    const disponiveis = instruments.map(i => ({ code: i.code, name: i.name, id: i.id }));
    return disponiveis.filter(t => !codes.includes(t.code));
  };

  if (showAddTestModal) {
    const availableTests = getTestesDisponiveis();
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10">
        <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
          <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-medium">Adicionar Teste</h1>
              <Button variant="ghost" size="icon" onClick={() => setShowAddTestModal(false)}>
                <X className="h-5 w-5" />
              </Button>
            </div>
            
            <p className="text-zinc-600 mb-4">Selecione um teste para adicionar a esta avaliação:</p>
            
            {loadingInstruments || instruments.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-zinc-500">Carregando instrumentos...</p>
              </div>
            ) : availableTests.length === 0 ? (
              <div className="text-center py-8 text-zinc-500">
                <p>Todos os testes disponíveis já foram adicionados.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {availableTests.map((test) => (
                  <button
                    key={test.id}
                    onClick={() => addTest(test.id)}
                    disabled={addingTest}
                    className="p-4 text-left rounded-xl border border-slate-200 bg-white hover:bg-slate-50 hover:border-slate-300 transition disabled:opacity-50"
                  >
                    <p className="font-medium">{test.name}</p>
                    <p className="text-sm text-zinc-500">{test.code}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
            </nav>
          </header>

          <div className="mb-6">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-3">
                  <h1 className="text-3xl font-medium tracking-tight text-zinc-900">{evaluation.code}</h1>
                  <Badge className={`${STATUS_COLORS[evaluation.status]} rounded-full`}>
                    {evaluation.status_display}
                  </Badge>
                </div>
                <p className="mt-1 text-lg text-zinc-600">{evaluation.patient_name}</p>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" className="rounded-full">Editar</Button>
                <Button className="rounded-full">Abrir Laudo</Button>
              </div>
            </div>
          </div>

          <div className="mb-6 flex flex-wrap gap-2 border-b border-slate-200">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition ${
                  activeTab === tab.id
                    ? "border-zinc-900 text-zinc-900"
                    : "border-transparent text-zinc-500 hover:text-zinc-700"
                }`}
              >
                <tab.icon className="h-4 w-4" />
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === "overview" && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <Card className="lg:col-span-2 rounded-2xl border-slate-200 shadow-sm">
                <CardHeader>
                  <CardTitle>Dados Principais</CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-zinc-500">Paciente</p>
                      <p className="font-medium">{evaluation.patient_name}</p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500">Responsável</p>
                      <p className="font-medium">{evaluation.examiner_name || "—"}</p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500">Data de início</p>
                      <p className="font-medium">
                        {evaluation.start_date ? new Date(evaluation.start_date).toLocaleDateString("pt-BR") : "—"}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-zinc-500">Data de término</p>
                      <p className="font-medium">
                        {evaluation.end_date ? new Date(evaluation.end_date).toLocaleDateString("pt-BR") : "—"}
                      </p>
                    </div>
                  </div>

                  {evaluation.title && (
                    <div>
                      <p className="text-sm text-zinc-500">Título do caso</p>
                      <p className="font-medium">{evaluation.title}</p>
                    </div>
                  )}

                  {evaluation.referral_reason && (
                    <div>
                      <p className="text-sm text-zinc-500">Motivo do encaminhamento</p>
                      <p className="text-sm">{evaluation.referral_reason}</p>
                    </div>
                  )}

                  {evaluation.evaluation_purpose && (
                    <div>
                      <p className="text-sm text-zinc-500">Finalidade da avaliação</p>
                      <p className="text-sm">{evaluation.evaluation_purpose}</p>
                    </div>
                  )}

                  {evaluation.clinical_hypothesis && (
                    <div>
                      <p className="text-sm text-zinc-500">Hipótese clínica</p>
                      <p className="text-sm">{evaluation.clinical_hypothesis}</p>
                    </div>
                  )}

                  {evaluation.general_notes && (
                    <div>
                      <p className="text-sm text-zinc-500">Observações clínicas</p>
                      <p className="text-sm">{evaluation.general_notes}</p>
                    </div>
                  )}
                </CardContent>
              </Card>

              <div className="space-y-4">
                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Testes Aplicados</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {evaluation.tests.length === 0 ? (
                      <p className="text-sm text-zinc-500">Nenhum teste aplicado</p>
                    ) : (
                      <div className="space-y-2">
                        {evaluation.tests.map((test) => (
                          <div key={test.id} className="flex items-center justify-between text-sm">
                            <span>{test.instrument_name}</span>
                            <Badge variant="outline" className={test.is_validated ? "bg-emerald-50" : "bg-amber-50"}>
                              {test.status}
                            </Badge>
                          </div>
                        ))}
                      </div>
                    )}
                    <Button variant="outline" className="w-full mt-4 rounded-xl" onClick={openAddTestModal}>
                      <Plus className="h-4 w-4 mr-2" />
                      Adicionar Teste
                    </Button>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Documentos</CardTitle>
                  </CardHeader>
                  <CardContent>
                    {evaluation.documents.length === 0 ? (
                      <p className="text-sm text-zinc-500">Nenhum documento</p>
                    ) : (
                      <div className="space-y-2">
                        {evaluation.documents.map((doc: any) => (
                          <div key={doc.id} className="text-sm">
                            {doc.name}
                          </div>
                        ))}
                      </div>
                    )}
                    <Button variant="outline" className="w-full mt-4 rounded-xl">
                      <Plus className="h-4 w-4 mr-2" />
                      Anexar Documento
                    </Button>
                  </CardContent>
                </Card>

                <Card className="rounded-2xl border-slate-200 shadow-sm">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">Status do Laudo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Badge className="bg-slate-100 text-slate-700 rounded-full">
                      {evaluation.status === "approved" ? "Aprovado" : "Em andamento"}
                    </Badge>
                    <Button className="w-full mt-4 rounded-xl">
                      Abrir Editor
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          {activeTab === "tests" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Testes Aplicados</CardTitle>
                <Button className="rounded-xl" onClick={openAddTestModal}>
                  <Plus className="h-4 w-4 mr-2" />
                  Adicionar Teste
                </Button>
              </CardHeader>
              <CardContent>
                {evaluation.tests.length === 0 ? (
                  <div className="text-center py-8 text-zinc-500">
                    <ClipboardList className="h-12 w-12 mx-auto mb-4 opacity-50" />
                    <p>Nenhum teste aplicado ainda</p>
                    <p className="text-sm">Adicione um teste para começar a avaliação</p>
                  </div>
                ) : (
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-slate-200">
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Teste</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Data</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Status</th>
                        <th className="pb-3 text-left text-sm font-medium text-zinc-500">Ações</th>
                      </tr>
                    </thead>
                    <tbody>
                      {evaluation.tests.map((test) => (
                        <tr key={test.id} className="border-b border-slate-100 hover:bg-slate-50 cursor-pointer" onClick={() => router.push(getTestUrl(test.instrument_code, test.id))}>
                          <td className="py-3 font-medium">{test.instrument_name}</td>
                          <td className="py-3">
                            {test.applied_on ? new Date(test.applied_on).toLocaleDateString("pt-BR") : "—"}
                          </td>
                          <td className="py-3">
                            <Badge variant="outline" className={test.is_validated ? "bg-emerald-50" : "bg-amber-50"}>
                              {test.status}
                            </Badge>
                          </td>
                          <td className="py-3" onClick={(e) => e.stopPropagation()}>
                            <Button variant="ghost" size="sm" onClick={() => router.push(getTestUrl(test.instrument_code, test.id))}>Abrir</Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </CardContent>
            </Card>
          )}

          {activeTab === "documents" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Documentos</CardTitle>
                <Button className="rounded-xl">
                  <Plus className="h-4 w-4 mr-2" />
                  Enviar Documento
                </Button>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8 text-zinc-500">
                  <FolderOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Nenhum documento anexado</p>
                  <p className="text-sm">Envie documentos para esta avaliação</p>
                </div>
              </CardContent>
            </Card>
          )}

          {activeTab === "evolution" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Evolução / Sessões</CardTitle>
                <Button className="rounded-xl">
                  <Plus className="h-4 w-4 mr-2" />
                  Nova Anotação
                </Button>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8 text-zinc-500">
                  <StickyNote className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Nenhum registro de evolução</p>
                  <p className="text-sm">Adicione notas de evolução ou sessões</p>
                </div>
              </CardContent>
            </Card>
          )}

          {activeTab === "report" && (
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Laudo</CardTitle>
                <div className="flex gap-2">
                  <Button variant="outline" className="rounded-xl">Pré-visualizar</Button>
                  <Button className="rounded-xl">Exportar PDF</Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8 text-zinc-500">
                  <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p>Laudo em redação</p>
                  <p className="text-sm">Clique em &quot;Abrir Editor&quot; para começar a redigir o laudo</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
