"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { api } from "@/lib/api"

export const dynamic = 'force-dynamic'

interface Patient {
  id: number
  full_name: string
  birth_date: string | null
  sex: string | null
  schooling: string | null
  city: string | null
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [formData, setFormData] = useState({
    full_name: "",
    birth_date: "",
    sex: "",
    schooling: "",
    school_name: "",
    grade_year: "",
    mother_name: "",
    father_name: "",
    phone: "",
    email: "",
    city: "",
    state: "",
    notes: "",
    responsible_name: "",
    responsible_phone: "",
  })

  const requiredFields = ["full_name", "birth_date", "sex", "schooling", "school_name"]
  const [viewMode, setViewMode] = useState<"cards" | "list">("cards")
  const [searchTerm, setSearchTerm] = useState("")
  const [ageFilter, setAgeFilter] = useState("")
  const [sortBy, setSortBy] = useState("")

  const filteredPatients = patients
    .filter((patient) => {
      if (searchTerm) {
        const term = searchTerm.toLowerCase()
        if (!patient.full_name?.toLowerCase().includes(term) && 
            !patient.city?.toLowerCase().includes(term)) {
          return false
        }
      }
      
      if (ageFilter && patient.birth_date) {
        const birthDate = new Date(patient.birth_date)
        const today = new Date()
        let age = today.getFullYear() - birthDate.getFullYear()
        const monthDiff = today.getMonth() - birthDate.getMonth()
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--
        }
        
        if (ageFilter === "0-5" && (age < 0 || age > 5)) return false
        if (ageFilter === "6-10" && (age < 6 || age > 10)) return false
        if (ageFilter === "11-15" && (age < 11 || age > 15)) return false
        if (ageFilter === "16+" && age < 16) return false
      }
      
      return true
    })
    .sort((a, b) => {
      if (sortBy === "name") {
        return (a.full_name || "").localeCompare(b.full_name || "")
      }
      return 0
    })

  const getFieldError = (field: string) => {
    if (!touched[field]) return null
    if (!formData[field as keyof typeof formData]) {
      return "Campo obrigatório"
    }
    return null
  }

  const handleBlur = (field: string) => {
    setTouched(prev => ({ ...prev, [field]: true }))
  }

  useEffect(() => {
    fetchPatients()
  }, [])

  async function fetchPatients() {
    try {
      setLoading(true)
      const data = await api.get<Patient[]>("/api/patients/")
      setPatients(data)
    } catch (err: any) {
      console.error("Erro ao buscar pacientes:", err)
      setError(err?.message || "Erro ao carregar pacientes")
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSave = async () => {
    // Marca todos os campos obrigatórios como touched
    const allTouched: Record<string, boolean> = {}
    requiredFields.forEach(field => {
      allTouched[field] = true
    })
    setTouched(prev => ({ ...prev, ...allTouched }))

    // Valida campos obrigatórios
    const hasErrors = requiredFields.some(field => !formData[field as keyof typeof formData])
    
    if (hasErrors) {
      return
    }
    try {
      const payload = {
        full_name: formData.full_name,
        birth_date: formData.birth_date,
        sex: formData.sex,
        schooling: formData.schooling,
        school_name: formData.school_name,
        grade_year: formData.grade_year || null,
        mother_name: formData.mother_name || null,
        father_name: formData.father_name || null,
        phone: formData.phone || null,
        email: formData.email || null,
        city: formData.city || null,
        state: formData.state || null,
        notes: formData.notes || null,
        responsible_name: formData.responsible_name || null,
        responsible_phone: formData.responsible_phone || null,
      }
      await api.post("/api/patients/", payload)
      alert("Paciente salvo com sucesso!")
      setShowForm(false)
      setTouched({})
      setFormData({
        full_name: "",
        birth_date: "",
        sex: "",
        schooling: "",
        school_name: "",
        mother_name: "",
        father_name: "",
        phone: "",
        email: "",
        city: "",
        state: "",
        notes: "",
        grade_year: "",
        responsible_name: "",
        responsible_phone: "",
      })
      fetchPatients()
    } catch (err: any) {
      console.error("Erro:", err)
      alert("Erro ao salvar: " + (err?.message || "Erro desconhecido"))
    }
  }

  return (
    <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
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

          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">Pacientes</h1>
              <p className="mt-1 text-sm text-zinc-600">Gerencie seus pacientes</p>
            </div>
            <button 
              onClick={() => setShowForm(!showForm)}
              className="rounded-full bg-zinc-900 px-6 py-3 text-sm font-medium text-white shadow-lg hover:bg-zinc-800"
            >
              {showForm ? "Fechar" : "+ Novo Paciente"}
            </button>
          </div>

          {showForm && (
            <div className="mb-6 rounded-2xl bg-white p-6 shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Cadastrar novo paciente</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome completo *</label>
                  <input
                    type="text"
                    value={formData.full_name}
                    onChange={(e) => handleInputChange("full_name", e.target.value)}
                    onBlur={() => handleBlur("full_name")}
                    className={`w-full rounded-xl border bg-white px-4 py-2 ${
                      getFieldError("full_name") ? "border-red-500" : "border-black/10"
                    }`}
                    placeholder="Digite o nome completo"
                  />
                  {getFieldError("full_name") && (
                    <p className="text-xs text-red-500">{getFieldError("full_name")}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Data de nascimento *</label>
                  <input
                    type="date"
                    value={formData.birth_date}
                    onChange={(e) => handleInputChange("birth_date", e.target.value)}
                    onBlur={() => handleBlur("birth_date")}
                    className={`w-full rounded-xl border bg-white px-4 py-2 ${
                      getFieldError("birth_date") ? "border-red-500" : "border-black/10"
                    }`}
                  />
                  {getFieldError("birth_date") && (
                    <p className="text-xs text-red-500">{getFieldError("birth_date")}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Sexo *</label>
                  <select
                    value={formData.sex}
                    onChange={(e) => handleInputChange("sex", e.target.value)}
                    onBlur={() => handleBlur("sex")}
                    className={`w-full rounded-xl border bg-white px-4 py-2 ${
                      getFieldError("sex") ? "border-red-500" : "border-black/10"
                    }`}
                  >
                    <option value="">Selecione...</option>
                    <option value="M">Masculino</option>
                    <option value="F">Feminino</option>
                  </select>
                  {getFieldError("sex") && (
                    <p className="text-xs text-red-500">{getFieldError("sex")}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Escolaridade *</label>
                  <select
                    value={formData.schooling}
                    onChange={(e) => handleInputChange("schooling", e.target.value)}
                    onBlur={() => handleBlur("schooling")}
                    className={`w-full rounded-xl border bg-white px-4 py-2 ${
                      getFieldError("schooling") ? "border-red-500" : "border-black/10"
                    }`}
                  >
                    <option value="">Selecione...</option>
                    <option value="preschool">Ensino Pré-escolar</option>
                    <option value="elementary">Ensino Fundamental</option>
                    <option value="middle">Ensino Médio</option>
                    <option value="higher">Ensino Superior</option>
                    <option value="higher_incomplete">Ensino Superior Incompleto</option>
                  </select>
                  {getFieldError("schooling") && (
                    <p className="text-xs text-red-500">{getFieldError("schooling")}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome da escola *</label>
                  <input
                    type="text"
                    value={formData.school_name}
                    onChange={(e) => handleInputChange("school_name", e.target.value)}
                    onBlur={() => handleBlur("school_name")}
                    className={`w-full rounded-xl border bg-white px-4 py-2 ${
                      getFieldError("school_name") ? "border-red-500" : "border-black/10"
                    }`}
                    placeholder="Nome da escola"
                  />
                  {getFieldError("school_name") && (
                    <p className="text-xs text-red-500">{getFieldError("school_name")}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Série/Ano</label>
                  <input
                    type="number"
                    min="1"
                    max="12"
                    value={formData.grade_year}
                    onChange={(e) => handleInputChange("grade_year", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                    placeholder="Ex: 5"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Telefone</label>
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => handleInputChange("phone", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                    placeholder="(62) 99999-9999"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">E-mail</label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange("email", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                    placeholder="email@exemplo.com"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Cidade</label>
                  <input
                    type="text"
                    value={formData.city}
                    onChange={(e) => handleInputChange("city", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Estado</label>
                  <input
                    type="text"
                    value={formData.state}
                    onChange={(e) => handleInputChange("state", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                    placeholder="GO"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome da mãe</label>
                  <input
                    type="text"
                    value={formData.mother_name}
                    onChange={(e) => handleInputChange("mother_name", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome do pai</label>
                  <input
                    type="text"
                    value={formData.father_name}
                    onChange={(e) => handleInputChange("father_name", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                  />
                </div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Nome do responsável</label>
                  <input
                    type="text"
                    value={formData.responsible_name}
                    onChange={(e) => handleInputChange("responsible_name", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Telefone do responsável</label>
                  <input
                    type="text"
                    value={formData.responsible_phone}
                    onChange={(e) => handleInputChange("responsible_phone", e.target.value)}
                    className="w-full rounded-xl border border-black/10 bg-white px-4 py-2"
                    placeholder="(62) 99999-9999"
                  />
                </div>
              </div>
              <div className="mt-4 space-y-2">
                <label className="text-sm font-medium">Observações</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => handleInputChange("notes", e.target.value)}
                  className="w-full rounded-xl border border-black/10 bg-white px-4 py-2 min-h-[100px]"
                  placeholder="Descreva a queixa principal e histórico clínico..."
                />
              </div>
              <div className="mt-4 flex gap-2">
                <button
                  onClick={handleSave}
                  className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white"
                >
                  Salvar paciente
                </button>
                <button
                  onClick={() => setShowForm(false)}
                  className="rounded-full border border-black/10 bg-white px-6 py-2 text-sm font-medium"
                >
                  Cancelar
                </button>
              </div>
            </div>
          )}

          <div className="mb-6 flex flex-wrap gap-4">
            <div className="flex-1 min-w-[280px]">
              <input
                type="text"
                placeholder="Buscar paciente..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full rounded-2xl border border-black/10 bg-white px-5 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
              />
            </div>
            <select 
              value={ageFilter}
              onChange={(e) => setAgeFilter(e.target.value)}
              className="rounded-2xl border border-black/10 bg-white px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
            >
              <option value="">Todas as idades</option>
              <option value="0-5">0-5 anos</option>
              <option value="6-10">6-10 anos</option>
              <option value="11-15">11-15 anos</option>
              <option value="16+">16+ anos</option>
            </select>
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="rounded-2xl border border-black/10 bg-white px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
            >
              <option value="">Ordenar por</option>
              <option value="name">Nome A-Z</option>
              <option value="recent">Mais recente</option>
            </select>
            <div className="flex rounded-2xl border border-black/10 bg-white overflow-hidden shadow-sm">
              <button
                onClick={() => setViewMode("cards")}
                className={`px-4 py-3 text-sm font-medium transition ${
                  viewMode === "cards" ? "bg-zinc-800 text-white" : "bg-white text-zinc-600 hover:bg-zinc-50"
                }`}
              >
                Cards
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`px-4 py-3 text-sm font-medium transition ${
                  viewMode === "list" ? "bg-zinc-800 text-white" : "bg-white text-zinc-600 hover:bg-zinc-50"
                }`}
              >
                Lista
              </button>
            </div>
          </div>

          {loading ? (
            <div className="text-center py-12">
              <p className="text-zinc-500">Carregando pacientes...</p>
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-500">{error}</p>
              <button onClick={fetchPatients} className="mt-2 text-sm underline">Tentar novamente</button>
            </div>
          ) : filteredPatients.length > 0 ? (
            viewMode === "cards" ? (
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
              {filteredPatients.map((patient) => (
                <Link
                  key={patient.id}
                  href={`/dashboard/patients/${patient.id}`}
                  className="group rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5 transition hover:scale-[1.02] hover:shadow-xl cursor-pointer block"
                >
                  <div className="flex items-start gap-4">
                    <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-zinc-800 text-xl font-medium text-white">
                      {patient.full_name?.charAt(0) || "?"}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="truncate text-lg font-medium text-zinc-900 group-hover:text-zinc-700">
                        {patient.full_name}
                      </h3>
                      <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-zinc-500">
                        <span className="rounded-full bg-zinc-100 px-2 py-1">
                          {patient.sex || 'Não informado'}
                        </span>
                        {patient.schooling && (
                          <span className="rounded-full bg-amber-100 px-2 py-1 text-amber-700">
                            {patient.schooling}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 flex items-center justify-between border-t border-dashed border-black/10 pt-4">
                    <span className="text-xs text-zinc-500">Nascimento</span>
                    <span className="text-sm font-medium text-zinc-700">
                      {patient.birth_date || '—'}
                    </span>
                  </div>
                </Link>
              ))}
            </div>
            ) : (
            <div className="rounded-[28px] bg-white/70 overflow-hidden shadow-lg ring-1 ring-black/5">
              <table className="w-full">
                <thead className="bg-zinc-50 border-b border-black/10">
                  <tr>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-zinc-500 uppercase">Paciente</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-zinc-500 uppercase">Sexo</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-zinc-500 uppercase">Escolaridade</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-zinc-500 uppercase">Nascimento</th>
                    <th className="text-left px-5 py-3 text-xs font-semibold text-zinc-500 uppercase">Cidade</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-black/5">
                  {filteredPatients.map((patient) => (
                    <tr key={patient.id} className="hover:bg-zinc-50 transition cursor-pointer" onClick={() => window.location.href = `/dashboard/patients/${patient.id}`}>
                      <td className="px-5 py-4">
                        <div className="flex items-center gap-3">
                          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-zinc-800 text-sm font-medium text-white">
                            {patient.full_name?.charAt(0) || "?"}
                          </div>
                          <span className="font-medium text-zinc-900">{patient.full_name}</span>
                        </div>
                      </td>
                      <td className="px-5 py-4 text-sm text-zinc-600">{patient.sex || '—'}</td>
                      <td className="px-5 py-4 text-sm text-zinc-600">{patient.schooling || '—'}</td>
                      <td className="px-5 py-4 text-sm text-zinc-600">{patient.birth_date || '—'}</td>
                      <td className="px-5 py-4 text-sm text-zinc-600">{patient.city || '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            )
          ) : (
            <div className="rounded-[28px] bg-white/70 p-12 text-center shadow-lg ring-1 ring-black/5">
              <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-zinc-100 text-3xl">👥</div>
              <h3 className="text-xl font-medium text-zinc-900">
                {searchTerm || ageFilter ? "Nenhum paciente encontrado" : "Nenhum paciente encontrado"}
              </h3>
              <p className="mt-2 text-sm text-zinc-500">
                {searchTerm || ageFilter 
                  ? "Tente ajustar os filtros de busca." 
                  : "Comece adicionando seu primeiro paciente."}
              </p>
              {!searchTerm && !ageFilter && (
              <button 
                onClick={() => setShowForm(true)}
                className="mt-6 rounded-full bg-zinc-900 px-6 py-3 text-sm font-medium text-white shadow-lg hover:bg-zinc-800"
              >
                + Novo Paciente
              </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
