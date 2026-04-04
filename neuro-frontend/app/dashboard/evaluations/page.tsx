"use client";

"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { Plus, Search, User, Calendar } from "lucide-react";
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

function formatDisplayDate(value: string | null | undefined) {
  if (!value) return "—";
  if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    const [year, month, day] = value.split("-");
    return `${day}/${month}/${year}`;
  }
  const date = new Date(value);
  if (isNaN(date.getTime())) return "—";
  return date.toLocaleDateString("pt-BR");
}

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
    start_date: "",
    end_date: "",
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
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
      });
      alert("Avaliação criada com sucesso!");
      setShowForm(false);
      setFormData({
        patient_id: "",
        title: "",
        referral_reason: "",
        evaluation_purpose: "",
        priority: "medium",
        start_date: "",
        end_date: "",
      });
      fetchEvaluations();
    } catch (err: any) {
      console.error("Erro:", err);
      alert("Erro ao criar avaliação: " + (err?.message || "Erro desconhecido"));
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-zinc-600">Carregando...</div>
      </div>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        title="Avaliações"
        subtitle="Gerencie as avaliações neuropsicológicas"
        actions={
          <Button onClick={() => setShowForm(!showForm)} className="gap-2">
            <Plus className="h-4 w-4" />
            Nova Avaliação
          </Button>
        }
      />

          {showForm && (
            <Card className="mb-6 rounded-xl border border-slate-200 bg-white shadow-sm">
              <CardHeader>
                <CardTitle>Nova Avaliação</CardTitle>
                <CardDescription>Crie uma nova avaliação neuropsicológica. Campos com * são obrigatórios.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-600">
                  Obrigatório para salvar: selecionar um paciente.
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Paciente *</label>
                    <select
                      className={`w-full rounded-lg border bg-white px-3 py-2 ${formTouched.patient_id && !formData.patient_id ? "border-red-500" : "border-slate-200"}`}
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
                    <Input
                      type="date"
                      value={formData.start_date}
                      onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Data da conclusão</label>
                    <Input
                      type="date"
                      value={formData.end_date}
                      onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                    />
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
            <EmptyState
              title="Nenhuma avaliação encontrada"
              description="Comece criando sua primeira avaliação."
              action={
                <Button onClick={() => setShowForm(true)}>
                  + Nova Avaliação
                </Button>
              }
            />
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {filteredEvaluations.map((evaluation) => (
                <Link key={evaluation.id} href={`/dashboard/evaluations/${evaluation.id}`}>
                  <Card className="rounded-xl border border-slate-200 bg-white shadow-sm hover:shadow-md transition cursor-pointer h-full">
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
                            {formatDisplayDate(evaluation.start_date)}
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
        </PageContainer>
  );
}
