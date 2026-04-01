"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { api } from "@/lib/api"

interface Evaluation {
  id: number
  code: string
  title: string
  patient_id: number
  patient_name: string
  referral_reason: string
  evaluation_purpose: string
  clinical_hypothesis: string
  start_date: string | null
  end_date: string | null
  priority: string
  status: string
  general_notes: string
}

export default function EditEvaluationPage() {
  const params = useParams()
  const router = useRouter()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formData, setFormData] = useState({
    title: "",
    referral_reason: "",
    evaluation_purpose: "",
    clinical_hypothesis: "",
    start_date: "",
    end_date: "",
    priority: "medium",
    status: "draft",
    general_notes: "",
  })
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null)

  useEffect(() => {
    async function fetchEvaluation() {
      try {
        const data = await api.get<Evaluation>(`/api/evaluations/${params.id}`)
        setEvaluation(data)
        setFormData({
          title: data.title || "",
          referral_reason: data.referral_reason || "",
          evaluation_purpose: data.evaluation_purpose || "",
          clinical_hypothesis: data.clinical_hypothesis || "",
          start_date: data.start_date || "",
          end_date: data.end_date || "",
          priority: data.priority || "medium",
          status: data.status || "draft",
          general_notes: data.general_notes || "",
        })
      } catch (err) {
        console.error("Erro ao buscar avaliação:", err)
        alert("Erro ao carregar avaliação")
      } finally {
        setLoading(false)
      }
    }

    if (params.id) {
      fetchEvaluation()
    }
  }, [params.id])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setSaving(true)

    try {
      await api.patch(`/api/evaluations/${params.id}`, {
        title: formData.title,
        referral_reason: formData.referral_reason,
        evaluation_purpose: formData.evaluation_purpose,
        clinical_hypothesis: formData.clinical_hypothesis,
        start_date: formData.start_date || null,
        end_date: formData.end_date || null,
        priority: formData.priority,
        status: formData.status,
        general_notes: formData.general_notes,
      })

      router.push(`/dashboard/evaluations/${params.id}?tab=overview`)
    } catch (err) {
      console.error("Erro ao atualizar avaliação:", err)
      alert("Erro ao atualizar avaliação")
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
        <div className="mx-auto max-w-5xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
          <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
            <div className="py-12 text-center text-zinc-600">Carregando...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-5xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <Link href={`/dashboard/evaluations/${params.id}?tab=overview`} className="rounded-full bg-white/70 p-2 text-zinc-700 hover:bg-white">
                ←
              </Link>
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
            <h1 className="text-2xl font-medium text-zinc-900">Editar Avaliação</h1>
            <p className="text-sm text-zinc-500">Paciente: {evaluation?.patient_name || "—"}</p>
          </div>

          <form onSubmit={handleSubmit} className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium text-zinc-700">Titulo do caso</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-zinc-700">Data de inicio</label>
                <input
                  type="date"
                  value={formData.start_date}
                  onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-zinc-700">Data da conclusao</label>
                <input
                  type="date"
                  value={formData.end_date}
                  onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-zinc-700">Prioridade</label>
                <select
                  value={formData.priority}
                  onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                >
                  <option value="low">Baixa</option>
                  <option value="medium">Media</option>
                  <option value="high">Alta</option>
                  <option value="urgent">Urgente</option>
                </select>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-zinc-700">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                >
                  <option value="draft">Rascunho</option>
                  <option value="collecting_data">Coletando dados</option>
                  <option value="tests_in_progress">Testes em andamento</option>
                  <option value="scoring">Correcao</option>
                  <option value="writing_report">Escrevendo laudo</option>
                  <option value="in_review">Em revisao</option>
                  <option value="approved">Aprovado</option>
                  <option value="archived">Arquivado</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium text-zinc-700">Motivo do encaminhamento</label>
                <textarea
                  value={formData.referral_reason}
                  onChange={(e) => setFormData({ ...formData, referral_reason: e.target.value })}
                  rows={3}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium text-zinc-700">Finalidade da avaliacao</label>
                <textarea
                  value={formData.evaluation_purpose}
                  onChange={(e) => setFormData({ ...formData, evaluation_purpose: e.target.value })}
                  rows={3}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium text-zinc-700">Hipotese clinica</label>
                <textarea
                  value={formData.clinical_hypothesis}
                  onChange={(e) => setFormData({ ...formData, clinical_hypothesis: e.target.value })}
                  rows={3}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>

              <div className="md:col-span-2">
                <label className="mb-1 block text-sm font-medium text-zinc-700">Observacoes gerais</label>
                <textarea
                  value={formData.general_notes}
                  onChange={(e) => setFormData({ ...formData, general_notes: e.target.value })}
                  rows={4}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>
            </div>

            <div className="mt-6 flex gap-2">
              <button
                type="submit"
                disabled={saving}
                className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white disabled:opacity-50"
              >
                {saving ? "Salvando..." : "Salvar alteracoes"}
              </button>
              <Link
                href={`/dashboard/evaluations/${params.id}?tab=overview`}
                className="rounded-full border border-black/10 bg-white px-6 py-2 text-sm font-medium text-zinc-700"
              >
                Cancelar
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
