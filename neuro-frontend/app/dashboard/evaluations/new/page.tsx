"use client"

import { Suspense, useEffect, useState } from "react"
import Link from "next/link"
import { useRouter, useSearchParams } from "next/navigation"
import { api } from "@/lib/api"
import { PageContainer, PageHeader, SectionCard } from "@/components/ui/page"
import { Button } from "@/components/ui/button"
import { Calendar, FileText, ArrowLeft, Plus, ClipboardList, Target, User } from "lucide-react"

function NewEvaluationPageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const initialPatientId = searchParams.get("patient_id")
  
  const [patients, setPatients] = useState<any[]>([])
  const [selectedPatientId, setSelectedPatientId] = useState<string>(initialPatientId || "")
  const [patient, setPatient] = useState<any>(null)

  const [title, setTitle] = useState("")
  const [referralReason, setReferralReason] = useState("")
  const [evaluationPurpose, setEvaluationPurpose] = useState("")
  const [clinicalHypothesis, setClinicalHypothesis] = useState("")
  const [generalNotes, setGeneralNotes] = useState("")

  const [startDate, setStartDate] = useState("")
  const [endDate, setEndDate] = useState("")
  const [priority, setPriority] = useState("medium")

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    async function fetchInitialData() {
      try {
        const patientsData = await api.get<any[]>('/api/patients/')
        setPatients(patientsData)
        
        if (initialPatientId) {
          const data = await api.get<any>(`/api/patients/${initialPatientId}`)
          setPatient(data)
          setTitle(`Avaliação Neuropsicológica - ${data.full_name}`)
          setSelectedPatientId(initialPatientId)
        }
      } catch (err) {
        console.error("Erro ao buscar dados:", err)
      } finally {
        setLoading(false)
      }
    }
    fetchInitialData()
  }, [initialPatientId])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    
    const currentPatient = patient || patients.find(p => p.id.toString() === selectedPatientId)
    
    if (!currentPatient) {
      alert("Selecione um paciente")
      return
    }
    
    if (!startDate || !endDate) {
      alert("Data de início e data de conclusão são obrigatórias")
      return
    }
    
    setSaving(true)
    try {
      const evaluation = await api.post<{ id: number }>("/api/evaluations/", {
        patient_id: currentPatient.id,
        title: title || `Avaliação Neuropsicológica - ${currentPatient.full_name}`,
        referral_reason: referralReason,
        evaluation_purpose: evaluationPurpose,
        clinical_hypothesis: clinicalHypothesis,
        general_notes: generalNotes,
        priority: priority,
        start_date: startDate,
        end_date: endDate,
      })
      router.push(`/dashboard/evaluations/${evaluation.id}`)
    } catch (err) {
      console.error("Erro ao criar avaliação:", err)
      alert("Erro ao criar avaliação")
    } finally {
      setSaving(false)
    }
  }

  const labelStyle = "text-[10px] font-black uppercase tracking-widest text-slate-400 mb-2 block";
  const inputStyle = "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-primary/20 transition-all";
  const selectStyle = "w-full rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-bold text-slate-700 outline-none focus:ring-2 focus:ring-primary/20 transition-all appearance-none";
  const textareaStyle = "w-full rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-600 outline-none focus:ring-2 focus:ring-primary/20 transition-all min-h-[100px]";

  if (loading) {
    return (
      <PageContainer>
        <div className="py-20 text-center animate-pulse text-slate-300 font-bold uppercase tracking-widest text-xs">Aguarde... Carregando formulário</div>
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <PageHeader
        title="Nova Abertura de Avaliação"
        subtitle={patient ? `Vincular novo processo clínico para: ${patient.full_name}` : "Selecione o paciente e inicie o processo clínico."}
        actions={
          <Link href={patient ? `/dashboard/patients/${patient.id}` : "/dashboard/patients"}>
            <Button variant="ghost" className="gap-2 font-bold text-slate-500">
              <ArrowLeft className="h-4 w-4" />
              Cancelar
            </Button>
          </Link>
        }
      />

      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2 space-y-8">
            
            <SectionCard 
              title="Paciente e Encaminhamento" 
              description="Identificação e origem da solicitação clínica."
              icon={<User className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-6">
                <div>
                  <label className={labelStyle}>Paciente *</label>
                  {initialPatientId && patient ? (
                    <div className="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm font-bold text-slate-700 cursor-not-allowed">
                      {patient.full_name}
                    </div>
                  ) : (
                    <select
                      value={selectedPatientId}
                      onChange={(e) => {
                        setSelectedPatientId(e.target.value)
                        const p = patients.find(p => p.id.toString() === e.target.value)
                        if (p && !title) setTitle(`Avaliação Neuropsicológica - ${p.full_name}`)
                      }}
                      required
                      className={selectStyle}
                    >
                      <option value="">Selecione um paciente da base...</option>
                      {patients.map(p => (
                        <option key={p.id} value={p.id}>{p.full_name}</option>
                      ))}
                    </select>
                  )}
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <div>
                    <label className={labelStyle}>Motivo do Encaminhamento</label>
                    <textarea
                      value={referralReason}
                      onChange={(e) => setReferralReason(e.target.value)}
                      placeholder="Quem encaminhou e por qual motivo primário?"
                      className={textareaStyle}
                    />
                  </div>
                  <div>
                    <label className={labelStyle}>Finalidade da Avaliação</label>
                    <textarea
                      value={evaluationPurpose}
                      onChange={(e) => setEvaluationPurpose(e.target.value)}
                      placeholder="Diagnóstico, orientação, planejamento..."
                      className={textareaStyle}
                    />
                  </div>
                </div>
              </div>
            </SectionCard>

            <SectionCard 
              title="Informações do Processo" 
              description="Defina o título, hipótese e notas adicionais."
              icon={<ClipboardList className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-6">
                <div>
                  <label className={labelStyle}>Título da Avaliação</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="Ex: Avaliação Neuropsicológica - TDAH"
                    className={inputStyle}
                  />
                  <p className="mt-2 text-[10px] text-slate-400 font-medium">Nome padrão sugerido automaticamente caso selecionado paciente.</p>
                </div>
                <div>
                  <label className={labelStyle}>Hipótese Clínica</label>
                  <textarea
                    value={clinicalHypothesis}
                    onChange={(e) => setClinicalHypothesis(e.target.value)}
                    placeholder="Descreva brevemente a queixa ou hipótese principal..."
                    className={textareaStyle}
                  />
                </div>
                <div>
                  <label className={labelStyle}>Observações Gerais</label>
                  <textarea
                    value={generalNotes}
                    onChange={(e) => setGeneralNotes(e.target.value)}
                    placeholder="Outras observações sobre o paciente ou processo..."
                    className={textareaStyle}
                  />
                </div>
              </div>
            </SectionCard>
          </div>

          <div className="space-y-8">
            <SectionCard 
              title="Cronograma & Prioridade" 
              description="Datas previstas."
              icon={<Calendar className="h-5 w-5 text-primary" />}
            >
              <div className="space-y-6">
                <div>
                  <label className={labelStyle}>Prioridade do Caso</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className={selectStyle}
                  >
                    <option value="low">Baixa</option>
                    <option value="medium">Média</option>
                    <option value="high">Alta</option>
                    <option value="urgent">Urgente</option>
                  </select>
                </div>
                <div>
                  <label className={labelStyle}>Início Previsto *</label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    required
                    className={inputStyle}
                  />
                </div>
                <div>
                  <label className={labelStyle}>Previsão de Entrega *</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    required
                    className={inputStyle}
                  />
                </div>
              </div>
            </SectionCard>

            <div className="p-6 rounded-[32px] bg-primary/5 border border-primary/10 space-y-4">
              <div className="flex items-center gap-3 text-primary">
                <Target className="h-5 w-5" />
                <span className="text-xs font-black uppercase tracking-widest text-[10px]">Meta de Prazo</span>
              </div>
              <p className="text-[11px] font-bold text-primary/60 leading-relaxed">
                As datas ajudam o sistema a alertar sobre atrasos e organizar sua agenda de testagens.
              </p>
            </div>
          </div>
        </div>

        <div className="flex justify-end pt-8 border-t border-slate-100">
          <Button type="submit" disabled={saving || !startDate || !endDate} className="px-12 h-14 rounded-2xl font-black uppercase tracking-widest gap-3 shadow-spike border-none text-white">
            <Plus className="h-5 w-5" />
            {saving ? "Criando..." : "Proceder com Avaliação"}
          </Button>
        </div>
      </form>
    </PageContainer>
  )
}

function NewEvaluationPageFallback() {
  return (
    <PageContainer>
      <div className="py-20 text-center text-slate-300 font-bold uppercase tracking-widest text-xs">Carregando formulário...</div>
    </PageContainer>
  )
}

export default function NewEvaluationPage() {
  return (
    <Suspense fallback={<NewEvaluationPageFallback />}>
      <NewEvaluationPageContent />
    </Suspense>
  )
}
