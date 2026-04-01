"use client"

import { useState, useEffect, useMemo } from "react"
import Link from "next/link"
import { useParams, useRouter } from "next/navigation"
import { api } from "@/lib/api"

interface Patient {
  id: number
  full_name: string
  birth_date: string
  sex: string
  schooling: string
  school_name: string
  grade_year?: string
  city?: string
  state?: string
  phone?: string
  email?: string
  mother_name?: string
  father_name?: string
  responsible_name?: string
  responsible_phone?: string
}

function calculateAge(birthDate: string | undefined | null): string {
  if (!birthDate) return "—"
  const birth = new Date(birthDate)
  const today = new Date()
  if (isNaN(birth.getTime())) return "—"
  let years = today.getFullYear() - birth.getFullYear()
  let months = today.getMonth() - birth.getMonth()

  if (today.getDate() < birth.getDate()) {
    months--
  }

  if (months < 0) {
    years--
    months += 12
  }

  if (years <= 0) {
    return `${months} ${months === 1 ? "mês" : "meses"}`
  }

  if (months === 0) {
    return `${years} ${years === 1 ? "ano" : "anos"}`
  }

  return `${years} ${years === 1 ? "ano" : "anos"} e ${months} ${months === 1 ? "mês" : "meses"}`
}

function getSchoolingLabel(value: string | number | undefined): string {
  if (!value) return "—"
  const labels: Record<string, string> = {
    preschool: "Ensino Pré-escolar",
    elementary: "Ensino Fundamental",
    middle: "Ensino Médio",
    higher: "Ensino Superior",
    higher_incomplete: "Ensino Superior Incompleto",
  }
  return labels[String(value)] || "—"
}

function getGradeYearDisplay(gradeYear: string | undefined, schooling: string | undefined): string {
  if (!gradeYear) return "—"
  let suffix = "º ano"
  if (schooling === "elementary" && parseInt(gradeYear) <= 5) {
    suffix = "º ano"
  } else if (schooling === "middle" || (schooling === "elementary" && parseInt(gradeYear) > 5)) {
    suffix = "ª série"
  }
  return `${gradeYear}${suffix}`
}

export default function PatientDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [patient, setPatient] = useState<Patient | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [isEditing, setIsEditing] = useState(false)
  const [editForm, setEditForm] = useState<Partial<Patient>>({})

  const age = useMemo(() => {
    return patient?.birth_date ? calculateAge(patient.birth_date) : "—"
  }, [patient?.birth_date])

  function handleEdit() {
    if (patient) {
      setEditForm({ 
        ...patient, 
        schooling: String(patient.schooling || "") 
      })
      setIsEditing(true)
    }
  }

  async function handleSaveEdit() {
    try {
      const payload: Record<string, unknown> = {}
      const fields = ['full_name', 'birth_date', 'sex', 'schooling', 'school_name', 'grade_year', 
                       'mother_name', 'father_name', 'phone', 'email', 'city', 'state', 'notes', 
                       'responsible_name', 'responsible_phone']
      for (const field of fields) {
        const value = editForm[field as keyof Patient]
        if (value !== undefined && value !== '') {
          payload[field] = value
        }
      }
      if (editForm.schooling) {
        payload.schooling = String(editForm.schooling)
      }
      const updated = await api.patch<Patient>(`/api/patients/${params.id}`, payload)
      setPatient({ ...updated, schooling: String(updated.schooling || "") })
      setIsEditing(false)
      alert("Paciente atualizado com sucesso!")
    } catch (err: any) {
      console.error("Erro ao salvar:", err)
      alert("Erro ao atualizar paciente")
    }
  }

  function handleNewEvaluation() {
    router.push(`/dashboard/evaluations/new?patient_id=${params.id}`)
  }

  useEffect(() => {
    async function fetchPatient() {
      try {
        const data = await api.get<Patient>(`/api/patients/${params.id}`)
        setPatient(data)
      } catch (err: any) {
        console.error("Erro ao buscar paciente:", err)
        setError(err?.message || "Erro ao carregar paciente")
      } finally {
        setLoading(false)
      }
    }
    if (params.id) {
      fetchPatient()
    }
  }, [params.id])

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

  if (error || !patient) {
    return (
      <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
        <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
          <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
            <div className="rounded-[28px] bg-white/70 p-12 text-center shadow-lg">
              <h2 className="text-xl font-medium text-zinc-900">Paciente não encontrado</h2>
              <p className="mt-2 text-sm text-zinc-500">{error}</p>
              <Link href="/dashboard/patients" className="mt-4 inline-block text-sm text-zinc-600 hover:underline">
                ← Voltar para pacientes
              </Link>
            </div>
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
              <Link href="/dashboard/patients" className="rounded-full bg-white/70 p-2 text-zinc-700 hover:bg-white">
                ←
              </Link>
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/patients" className="rounded-full px-4 py-2 bg-zinc-900 text-white shadow">Pacientes</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
              <Link href="/dashboard/tests" className="rounded-full px-4 py-2 hover:bg-black/5">Testes</Link>
              <Link href="/dashboard/reports" className="rounded-full px-4 py-2 hover:bg-black/5">Laudos</Link>
            </nav>
          </header>

          {/* Edit Form */}
          {isEditing && (
            <div className="mb-6 rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="text-lg font-medium text-zinc-900 mb-4">Editar Paciente</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Nome completo</label>
                  <input
                    type="text"
                    value={editForm.full_name || ""}
                    onChange={(e) => setEditForm({ ...editForm, full_name: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Data de nascimento</label>
                  <input
                    type="date"
                    value={editForm.birth_date || ""}
                    onChange={(e) => setEditForm({ ...editForm, birth_date: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Sexo</label>
                  <select
                    value={editForm.sex || ""}
                    onChange={(e) => setEditForm({ ...editForm, sex: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  >
                    <option value="">Selecione...</option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Telefone</label>
                  <input
                    type="text"
                    value={editForm.phone || ""}
                    onChange={(e) => setEditForm({ ...editForm, phone: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={editForm.email || ""}
                    onChange={(e) => setEditForm({ ...editForm, email: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Cidade</label>
                  <input
                    type="text"
                    value={editForm.city || ""}
                    onChange={(e) => setEditForm({ ...editForm, city: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Escolaridade</label>
                  <select
                    value={editForm.schooling as string || ""}
                    onChange={(e) => setEditForm({ ...editForm, schooling: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  >
                    <option value="">Selecione...</option>
                    <option value="preschool">Ensino Pré-escolar</option>
                    <option value="elementary">Ensino Fundamental</option>
                    <option value="middle">Ensino Médio</option>
                    <option value="higher">Ensino Superior</option>
                    <option value="higher_incomplete">Ensino Superior Incompleto</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Nome da escola</label>
                  <input
                    type="text"
                    value={editForm.school_name || ""}
                    onChange={(e) => setEditForm({ ...editForm, school_name: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Série/Ano</label>
                  <input
                    type="number"
                    min="1"
                    max="12"
                    value={editForm.grade_year || ""}
                    onChange={(e) => setEditForm({ ...editForm, grade_year: e.target.value })}
                    placeholder="Ex: 5"
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Nome da Mãe</label>
                  <input
                    type="text"
                    value={editForm.mother_name || ""}
                    onChange={(e) => setEditForm({ ...editForm, mother_name: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-zinc-700 mb-1">Nome do Pai</label>
                  <input
                    type="text"
                    value={editForm.father_name || ""}
                    onChange={(e) => setEditForm({ ...editForm, father_name: e.target.value })}
                    className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm"
                  />
                </div>
              </div>
              <div className="mt-4 flex gap-2">
                <button
                  onClick={handleSaveEdit}
                  className="rounded-full bg-zinc-900 px-4 py-2 text-sm font-medium text-white"
                >
                  Salvar
                </button>
                <button
                  onClick={() => setIsEditing(false)}
                  className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700"
                >
                  Cancelar
                </button>
              </div>
            </div>
          )}

          {/* Patient Info */}
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-zinc-800 text-2xl font-medium text-white">
                {patient.full_name?.charAt(0) || "?"}
              </div>
              <div>
                <h1 className="text-2xl font-medium text-zinc-900">{patient.full_name}</h1>
                <p className="text-sm text-zinc-500">Paciente ID: {patient.id}</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button onClick={handleEdit} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm">
                Editar
              </button>
              <button onClick={handleNewEvaluation} className="rounded-full bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-lg">
                Nova Avaliação
              </button>
            </div>
          </div>

          {/* Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="text-sm font-medium text-zinc-500 mb-2">Dados Pessoais</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-zinc-500">Sexo:</span> {patient.sex || "—"}</p>
                <p><span className="text-zinc-500">Nascimento:</span> {patient.birth_date || "—"}</p>
                <p><span className="text-zinc-500">Idade:</span> {age}</p>
                <p><span className="text-zinc-500">Cidade:</span> {patient.city || "—"}</p>
                <p><span className="text-zinc-500">Estado:</span> {patient.state || "—"}</p>
              </div>
            </div>
            <div className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="text-sm font-medium text-zinc-500 mb-2">Contato</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-zinc-500">Telefone:</span> {patient.phone || "—"}</p>
                <p><span className="text-zinc-500">Email:</span> {patient.email || "—"}</p>
              </div>
            </div>
            <div className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="text-sm font-medium text-zinc-500 mb-2">Escolaridade</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-zinc-500">Nível:</span> {getSchoolingLabel(patient.schooling)}</p>
                <p><span className="text-zinc-500">Série/Ano:</span> {getGradeYearDisplay(patient.grade_year, patient.schooling)}</p>
                <p><span className="text-zinc-500">Escola:</span> {patient.school_name || "—"}</p>
              </div>
            </div>
            <div className="rounded-2xl bg-white/70 p-5 shadow-lg ring-1 ring-black/5 md:col-span-2">
              <h3 className="text-sm font-medium text-zinc-500 mb-2">Filiação</h3>
              <div className="space-y-2 text-sm">
                <p><span className="text-zinc-500">Mãe:</span> {patient.mother_name || "—"}</p>
                <p><span className="text-zinc-500">Pai:</span> {patient.father_name || "—"}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
