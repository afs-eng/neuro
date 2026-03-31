"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Plus, Search, FileText, ClipboardList, Calendar, User } from "lucide-react";
import { api } from "@/lib/api";

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
  tests: any[];
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

const PRIORITY_COLORS: Record<string, string> = {
  low: "bg-slate-100 text-slate-600",
  medium: "bg-blue-50 text-blue-700",
  high: "bg-orange-50 text-orange-700",
  urgent: "bg-red-50 text-red-700",
};

export default function EvaluationsPage() {
  const router = useRouter();
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [showForm, setShowForm] = useState(false);
  const [formTouched, setFormTouched] = useState<Record<string, boolean>>({});
  const [formData, setFormData] = useState({
    patient_id: "",
    title: "",
    referral_reason: "",
    evaluation_purpose: "",
    priority: "medium",
  });
  const [patients, setPatients] = useState<any[]>([]);

  useEffect(() => {
    fetchEvaluations();
    fetchPatients();
  }, []);

  async function fetchEvaluations() {
    try {
      const data = await api.get<Evaluation[]>("/api/evaluations/");
      setEvaluations(data);
    } catch (err: any) {
      console.error("Erro ao buscar avaliações:", err);
    } finally {
      setLoading(false);
    }
  }

  async function fetchPatients() {
    try {
      const data = await api.get<any[]>("/api/patients/");
      setPatients(data);
    } catch (err: any) {
      console.error("Erro ao buscar pacientes:", err);
    }
  }

  const filteredEvaluations = evaluations.filter(
    (e) =>
      e.patient_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      e.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSave = async () => {
    setFormTouched({ patient_id: true });
    if (!formData.patient_id) {
      alert("Selecione um paciente");
      return;
    }
    try {
      await api.post("/api/evaluations/", {
        patient_id: Number(formData.patient_id),
        title: formData.title,
        referral_reason: formData.referral_reason,
        evaluation_purpose: formData.evaluation_purpose,
        priority: formData.priority,
      });
      alert("Avaliação criada com sucesso!");
      setShowForm(false);
      setFormData({
        patient_id: "",
        title: "",
        referral_reason: "",
        evaluation_purpose: "",
        priority: "medium",
      });
      fetchEvaluations();
    } catch (err: any) {
      console.error("Erro:", err);
      alert("Erro ao criar avaliação: " + (err?.message || "Erro desconhecido"));
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Carregando...</div>
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
              <Link href="/dashboard/patients" className="rounded-full px-4 py-2 hover:bg-black/5">Pacientes</Link>
              <Link href="/dashboard/evaluations" className="rounded-full bg-zinc-900 px-4 py-2 text-white">Avaliações</Link>
              <Link href="/dashboard/tests" className="rounded-full px-4 py-2 hover:bg-black/5">Testes</Link>
            </nav>
          </header>

          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">Avaliações</h1>
              <p className="mt-1 text-sm text-zinc-600">Gerencie as avaliações neuropsicológicas</p>
            </div>
            <Button onClick={() => setShowForm(!showForm)} className="rounded-full gap-2">
              <Plus className="h-4 w-4" />
              Nova Avaliação
            </Button>
          </div>

          {showForm && (
            <Card className="mb-6 rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Nova Avaliação</CardTitle>
                <CardDescription>Crie uma nova avaliação neuropsicológica. Campos com * são obrigatórios.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
                  Obrigatório para salvar: selecionar um paciente.
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Paciente *</label>
                    <select
                      className={`w-full rounded-xl border bg-white px-3 py-2 ${formTouched.patient_id && !formData.patient_id ? "border-red-500" : "border-slate-200"}`}
                      value={formData.patient_id}
                      onChange={(e) => setFormData({ ...formData, patient_id: e.target.value })}
                      onBlur={() => setFormTouched((prev) => ({ ...prev, patient_id: true }))}
                    >
                      <option value="">Selecione...</option>
                      {patients.map((p) => (
                        <option key={p.id} value={p.id}>{p.full_name}</option>
                      ))}
                    </select>
                    {formTouched.patient_id && !formData.patient_id && (
                      <p className="text-xs text-red-500">Campo obrigatório</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Título do caso</label>
                    <Input
                      placeholder="Ex: Avaliação de atenção"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Prioridade</label>
                    <select
                      className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2"
                      value={formData.priority}
                      onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                    >
                      <option value="low">Baixa</option>
                      <option value="medium">Média</option>
                      <option value="high">Alta</option>
                      <option value="urgent">Urgente</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Data de início</label>
                    <Input type="date" />
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Motivo do encaminhamento</label>
                  <textarea
                    className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[80px]"
                    placeholder="Descreva o motivo do encaminhamento..."
                    value={formData.referral_reason}
                    onChange={(e) => setFormData({ ...formData, referral_reason: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Finalidade da avaliação</label>
                  <textarea
                    className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 min-h-[80px]"
                    placeholder="Descreva o objetivo da avaliação..."
                    value={formData.evaluation_purpose}
                    onChange={(e) => setFormData({ ...formData, evaluation_purpose: e.target.value })}
                  />
                </div>
                <div className="flex gap-2">
                  <Button onClick={handleSave}>Criar Avaliação</Button>
                  <Button variant="outline" onClick={() => setShowForm(false)}>Cancelar</Button>
                </div>
              </CardContent>
            </Card>
          )}

          <div className="mb-6 flex gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <Input
                placeholder="Buscar avaliações..."
                className="pl-10 rounded-xl"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          {filteredEvaluations.length === 0 ? (
            <div className="rounded-[28px] bg-white/70 p-12 text-center shadow-lg ring-1 ring-black/5">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-zinc-100 text-3xl">📋</div>
              <h3 className="text-xl font-medium text-zinc-900">Nenhuma avaliação encontrada</h3>
              <p className="mt-2 text-sm text-zinc-500">Comece criando sua primeira avaliação.</p>
              <Button onClick={() => setShowForm(true)} className="mt-6 rounded-full">
                + Nova Avaliação
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
              {filteredEvaluations.map((evaluation) => (
                <Link key={evaluation.id} href={`/dashboard/evaluations/${evaluation.id}`}>
                  <Card className="rounded-2xl border-slate-200 shadow-sm hover:shadow-md transition cursor-pointer h-full">
                    <CardHeader className="pb-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="text-xs text-slate-500">{evaluation.code}</p>
                          <CardTitle className="text-lg">{evaluation.patient_name}</CardTitle>
                        </div>
                        <Badge className={`${STATUS_COLORS[evaluation.status] || "bg-slate-100"} rounded-full`}>
                          {evaluation.status_display}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      {evaluation.title && (
                        <p className="text-sm text-slate-600 line-clamp-2">{evaluation.title}</p>
                      )}
                      <div className="flex flex-wrap gap-2 text-xs text-slate-500">
                        {evaluation.examiner_name && (
                          <span className="flex items-center gap-1">
                            <User className="h-3 w-3" />
                            {evaluation.examiner_name}
                          </span>
                        )}
                        {evaluation.start_date && (
                          <span className="flex items-center gap-1">
                            <Calendar className="h-3 w-3" />
                            {new Date(evaluation.start_date).toLocaleDateString("pt-BR")}
                          </span>
                        )}
                      </div>
                      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                        <Badge variant="outline" className={`${PRIORITY_COLORS[evaluation.priority]} rounded-full text-xs`}>
                          {evaluation.priority_display}
                        </Badge>
                        <span className="text-xs text-slate-400">
                          {evaluation.tests?.length || 0} testes
                        </span>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
