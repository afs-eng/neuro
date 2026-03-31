"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { api } from "@/lib/api"

interface Patient {
  id: number
  full_name: string
  birth_date: string
  sex: string
}

export default function NewEvaluationPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const patientId = searchParams.get("patient_id")
  
  const [patient, setPatient] = useState<Patient | null>(null)
  const [title, setTitle] = useState("")
  const [clinicalHypothesis, setClinicalHypothesis] = useState("")
  const [priority, setPriority] = useState("medium")
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    async function fetchPatient() {
      if (!patientId) {
        setLoading(false)
        return
      }
      try {
        const data = await api.get<Patient>(`/api/patients/${patientId}`)
        setPatient(data)
        setTitle(`Avaliação Neuropsicológica - ${data.full_name}`)
      } catch (err) {
        console.error("Erro ao buscar paciente:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchPatient()
  }, [patientId])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!patient) return
    
    setSaving(true)
    try {
      const evaluation = await api.post<{ id: number }>("/api/evaluations/", {
        patient_id: patient.id,
        title: title || `Avaliação Neuropsicológica - ${patient.full_name}`,
        clinical_hypothesis: clinicalHypothesis,
        priority: priority,
      })
      router.push(`/dashboard/evaluations/${evaluation.id}`)
    } catch (err) {
      console.error("Erro ao criar avaliação:", err)
      alert("Erro ao criar avaliação")
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
        <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
          <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
            <div className="text-center py-12 text-zinc-600">Carregando...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          {/* Header */}
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <Link href={patient ? `/dashboard/patients/${patient.id}` : "/dashboard/patients"} className="rounded-full bg-white/70 p-2 text-zinc-700 hover:bg-white">
                ←
              </Link>
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/patients" className="rounded-full px-4 py-2 hover:bg-black/5">Pacientes</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
            </nav>
          </header>

          {/* Title */}
          <div className="mb-6">
            <h1 className="text-2xl font-medium text-zinc-900">Nova Avaliação</h1>
            {patient && (
              <p className="text-sm text-zinc-500">Paciente: {patient.full_name}</p>
            )}
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-zinc-700 mb-1">Título</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Avaliação Neuropsicológica"
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-zinc-700 mb-1">Hipótese Clínica</label>
                <textarea
                  value={clinicalHypothesis}
                  onChange={(e) => setClinicalHypothesis(e.target.value)}
                  placeholder="Descreva a hipótese clínica..."
                  rows={3}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-zinc-700 mb-1">Prioridade</label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                >
                  <option value="low">Baixa</option>
                  <option value="medium">Média</option>
                  <option value="high">Alta</option>
                  <option value="urgent">Urgente</option>
                </select>
              </div>
            </div>
            <div className="mt-6 flex gap-2">
              <button
                type="submit"
                disabled={saving}
                className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white disabled:opacity-50"
              >
                {saving ? "Criando..." : "Criar Avaliação"}
              </button>
              <Link
                href={patient ? `/dashboard/patients/${patient.id}` : "/dashboard/patients"}
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
