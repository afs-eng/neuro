'use client'

import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { api } from '@/lib/api'
import { PageContainer, PageHeader, SectionCard, StatCard } from '@/components/ui/page'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Save, Info, Brain, Activity, Target } from 'lucide-react'

// ... (keep the constants exactly the same)
const LISTA_A = [
  "BALÃO", "FLOR", "SALA", "BOCA", "CHUVA", "MÃE", "CIRCO", "PEIXE", "LUA", "CORPO", "CESTA", "LÁPIS", "MESA", "CHAPÉU", "MILHO"
]

const LISTA_B = [
  "CARRO", "MEIA", "PATO", "FOGO", "SOFÁ", "DOCE", "PONTO", "VASO", "LIVRO", "PORTA", "ÍNDIO", "VACA", "ROUPA", "CAIXA", "RIO"
]

const RECOGNITION_WORDS = [
  // Coluna 1
  { word: "LUA", type: "A" }, { word: "GALO", type: "SB" }, { word: "FOGO", type: "B" }, { word: "CHAPÉU", type: "A" }, { word: "VASO", type: "B" }, { word: "MESA", type: "A" }, { word: "LAGO", type: "SB" }, { word: "PORTA", type: "B" }, { word: "DENTE", type: "SA" }, { word: "RIO", type: "B" },
  // Coluna 2
  { word: "COR", type: "FA" }, { word: "ÍNDIO", type: "B" }, { word: "BALÃO", type: "A" }, { word: "RUA", type: "FA" }, { word: "PLANTA", type: "SA/SB" }, { word: "ROUPA", type: "B" }, { word: "CORPO", type: "A" }, { word: "PATO", type: "B" }, { word: "CESTA", type: "A" }, { word: "LIVRO", type: "B" },
  // Coluna 3
  { word: "PONTO", type: "B" }, { word: "FLOR", type: "A" }, { word: "ISCA", type: "SA" }, { word: "BOCA", type: "A" }, { word: "CHUVA", type: "A" }, { word: "CAIXA", type: "B" }, { word: "ROSA", type: "SA" }, { word: "CIRCO", type: "A" }, { word: "CARRO", type: "B" }, { word: "LÁPIS", type: "A" },
  // Coluna 4
  { word: "VACA", type: "B" }, { word: "SALA", type: "A" }, { word: "FILHO", type: "SA/FA" }, { word: "BOLA", type: "SA" }, { word: "AULA", type: "SA" }, { word: "MILHO", type: "A" }, { word: "BOLO", type: "SB" }, { word: "PEIXE", type: "A" }, { word: "BOTÃO", type: "FA" }, { word: "LEITE", type: "SA" },
  // Coluna 5
  { word: "MEIA", type: "B" }, { word: "JARDIM", type: "SA" }, { word: "SOFÁ", type: "B" }, { word: "FESTA", type: "FA" }, { word: "DOCE", "type": "B" }, { word: "SOL", type: "SA" }, { word: "MÃE", "type": "A" }, { word: "PAPEL", type: "FA" }, { word: "MAR", type: "SB" }, { word: "VENTO", type: "FB" }
]

const TRIALS = ['a1', 'a2', 'a3', 'a4', 'a5', 'b', 'a6', 'a7']

function RAVLTFormPageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [scores, setScores] = useState<Record<string, number>>({})
  const [checkboxes, setCheckboxes] = useState<Record<string, boolean>>({})
  const [recognitionChecks, setRecognitionChecks] = useState<Record<string, boolean>>({})
  const [evaluation, setEvaluation] = useState<any>(null)
  const [loadingEvaluation, setLoadingEvaluation] = useState(true)
  const [saving, setSaving] = useState(false)
  const [currentTrial, setCurrentTrial] = useState('a1')
  const [activeTab, setActiveTab] = useState<'general' | 'recognition'>('general')
  const [isPointerDown, setIsPointerDown] = useState(false)
  const [dragMode, setDragMode] = useState<'check' | 'uncheck'>('check')

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");

  useEffect(() => {
    async function fetchEvaluation() {
      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result && result.evaluation_id && !evaluationId) {
            const newEvalId = result.evaluation_id.toString();
            router.replace(`/dashboard/tests/ravlt?application_id=${applicationId}&evaluation_id=${newEvalId}&edit=true`)
            return
          }
          if (result && result.is_validated && !searchParams.get("edit")) {
            router.push(`/dashboard/tests/ravlt/${applicationId}/result?evaluation_id=${evaluationId}`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingCheckboxes: Record<string, boolean> = {}
            const existingScores: Record<string, number> = {}
            const trials = ['a1', 'a2', 'a3', 'a4', 'a5', 'b', 'a6', 'a7']
            trials.forEach((trial) => {
              const score = raw[trial] || 0
              existingScores[trial] = score
              for (let i = 0; i < score; i++) {
                existingCheckboxes[`${i}-${trial}`] = true
              }
            })
            setCheckboxes(existingCheckboxes)
            setScores(existingScores)
            if (raw.reconhecimento) {
              const recScore = raw.reconhecimento - 35
              const recWords = RECOGNITION_WORDS.filter(w => w.type === 'A').slice(0, recScore)
              const recChecks: Record<string, boolean> = {}
              recWords.forEach((w, idx) => {
                const realIdx = RECOGNITION_WORDS.findIndex(rw => rw.word === w.word)
                if (realIdx >= 0) recChecks[realIdx] = true
              })
              setRecognitionChecks(recChecks)
            }
          }
        } catch (error) {
          console.log("Teste não encontrado")
        }
      }

      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${evaluationId}`)
        setEvaluation(data)
      } catch (error: any) {
        console.error("Erro ao buscar avaliação:", error)
      } finally {
        setLoadingEvaluation(false)
      }
    }
    fetchEvaluation()
  }, [evaluationId, applicationId, router, searchParams])

  useEffect(() => {
    const handlePointerUp = () => {
      setIsPointerDown(false)
    }

    window.addEventListener('mouseup', handlePointerUp)
    return () => window.removeEventListener('mouseup', handlePointerUp)
  }, [])

  const updateTrialScore = (state: Record<string, boolean>, trial: string) => {
    const trialCheckboxes = Object.entries(state)
      .filter(([k]) => k.endsWith(`-${trial}`))
      .filter(([, v]) => v).length
    setScores(prev => ({ ...prev, [trial]: trialCheckboxes }))
  }

  const setCheckboxValue = (wordIndex: number, trial: string, checked: boolean) => {
    const key = `${wordIndex}-${trial}`
    setCheckboxes(prev => {
      if (prev[key] === checked) {
        return prev
      }

      const newState = { ...prev, [key]: checked }
      updateTrialScore(newState, trial)
      return newState
    })
  }

  const handleCheckboxMouseDown = (wordIndex: number, trial: string) => {
    const key = `${wordIndex}-${trial}`
    const nextMode = checkboxes[key] ? 'uncheck' : 'check'
    setIsPointerDown(true)
    setDragMode(nextMode)
    setCheckboxValue(wordIndex, trial, nextMode === 'check')
  }

  const handleCheckboxMouseEnter = (wordIndex: number, trial: string) => {
    if (!isPointerDown) {
      return
    }

    setCheckboxValue(wordIndex, trial, dragMode === 'check')
  }

  const setRecognitionValue = (index: number, checked: boolean) => {
    setRecognitionChecks(prev => {
      if (prev[index] === checked) {
        return prev
      }

      return { ...prev, [index]: checked }
    })
  }

  const handleRecognitionMouseDown = (index: number) => {
    const nextMode = recognitionChecks[index] ? 'uncheck' : 'check'
    setIsPointerDown(true)
    setDragMode(nextMode)
    setRecognitionValue(index, nextMode === 'check')
  }

  const handleRecognitionMouseEnter = (index: number) => {
    if (!isPointerDown) {
      return
    }

    setRecognitionValue(index, dragMode === 'check')
  }

  const getTrialLabel = (trial: string) => {
    const labels: Record<string, string> = {
      a1: 'A1', a2: 'A2', a3: 'A3', a4: 'A4', a5: 'A5',
      b: 'B1', a6: 'A6', a7: 'A7'
    }
    return labels[trial] || trial
  }

  const getTrialColor = (trial: string) => {
    const colors: Record<string, string> = {
      b: 'bg-amber-500', 
      a7: 'bg-purple-600'
    }
    return colors[trial] || 'bg-primary'
  }

  const getTrialTextColor = (trial: string) => {
    const colors: Record<string, string> = {
      b: 'text-amber-600', 
      a7: 'text-purple-600'
    }
    return colors[trial] || 'text-primary'
  }

  const getScoreForTrial = (trial: string) => {
    return Object.entries(checkboxes)
      .filter(([k]) => k.endsWith(`-${trial}`))
      .filter(([, v]) => v).length
  }

  const getRecognitionStats = () => {
    const totalAcertos = Object.values(recognitionChecks).filter(Boolean).length
    return { totalAcertos }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!evaluationId) {
      alert('ID da avaliação não encontrado.')
      return
    }

    if (Object.keys(recognitionChecks).length === 0) {
      alert('Preencha a fase de reconhecimento antes de salvar o resultado.')
      setActiveTab('recognition')
      return
    }

    setSaving(true)
    try {
      const stats = getRecognitionStats()
      const payload = {
        evaluation_id: parseInt(evaluationId),
        applied_on: new Date().toISOString().split('T')[0],
        a1: parseInt(String(scores['a1'] || 0)),
        a2: parseInt(String(scores['a2'] || 0)),
        a3: parseInt(String(scores['a3'] || 0)),
        a4: parseInt(String(scores['a4'] || 0)),
        a5: parseInt(String(scores['a5'] || 0)),
        b: parseInt(String(scores['b'] || 0)),
        a6: parseInt(String(scores['a6'] || 0)),
        a7: parseInt(String(scores['a7'] || 0)),
        reconhecimento: parseInt(String(stats.totalAcertos)),
      }

      const result = await api.post<any>('/api/tests/ravlt/submit', payload)
      alert('RAVLT salvo com sucesso!')
      router.push(`/dashboard/tests/ravlt/${result.application_id}/result?evaluation_id=${evaluationId}`)
    } catch (error: any) {
      console.error('Erro completo:', error)
      alert(String(error?.message || 'Erro ao salvar o teste.'))
    } finally {
      setSaving(false)
    }
  }

  if (loadingEvaluation) {
    return (
      <PageContainer>
        <div className="py-20 text-center animate-pulse text-slate-300 font-bold uppercase tracking-widest text-xs">
          Aguarde... Carregando dados da avaliação
        </div>
      </PageContainer>
    )
  }

  return (
    <PageContainer>
      <PageHeader
        title="RAVLT"
        subtitle={`Teste de Aprendizado Auditivo-Verbal de Rey para: ${evaluation?.patient_name || 'Paciente'}`}
        actions={
          <div className="flex gap-2">
            <Link href="/dashboard/tests">
              <Button variant="ghost" className="gap-2 font-bold text-slate-500">
                <ArrowLeft className="h-4 w-4" />
                Cancelar
              </Button>
            </Link>
          </div>
        }
      />

      <SectionCard className="mb-8 p-0 overflow-hidden bg-transparent border-none">
          <div className="flex bg-slate-100 rounded-2xl p-1 mb-8 w-max">
            <button
              onClick={() => setActiveTab('general')}
              className={`px-6 py-2.5 rounded-xl font-black uppercase tracking-widest text-[10px] transition-all ${
                activeTab === 'general'
                  ? 'bg-white text-primary shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Aplicação Geral
            </button>
            <button
              onClick={() => setActiveTab('recognition')}
              className={`px-6 py-2.5 rounded-xl font-black uppercase tracking-widest text-[10px] transition-all ${
                activeTab === 'recognition'
                  ? 'bg-white text-primary shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              Fase de Reconhecimento
            </button>
          </div>

        {activeTab === 'general' ? (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-8">
            <SectionCard title="Controle de Aplicação" description="Marque as palavras evocadas pelo paciente em cada tentativa.">
              <div className="mb-6 flex gap-2 overflow-x-auto pb-2">
                {TRIALS.map((trial) => (
                  <button
                    key={trial}
                    onClick={() => setCurrentTrial(trial)}
                    className={`flex-shrink-0 px-5 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all ${
                      currentTrial === trial
                        ? `${getTrialColor(trial)} text-white shadow-md border-none`
                        : 'bg-white text-slate-500 border border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    {getTrialLabel(trial)}
                    <span className="ml-2 px-2 py-0.5 rounded-full bg-white/20 text-[10px]">
                      {getScoreForTrial(trial)}
                    </span>
                  </button>
                ))}
              </div>

              <div className="overflow-x-auto rounded-[24px] border border-slate-200 bg-white shadow-sm mb-8">
                <table className="w-full min-w-[800px] border-collapse text-xs">
                  <thead className="bg-slate-50">
                    <tr>
                      <th className="px-4 py-4 border-b border-r border-slate-200 font-black text-slate-400 text-[10px] uppercase tracking-widest sticky left-0 z-20 w-24 bg-slate-50 text-left">
                        Lista A
                      </th>
                      {TRIALS.map((trial) => (
                        <th 
                          key={trial} 
                          className="p-1 border-b border-r border-slate-200 text-center"
                        >
                          <div className={`w-10 h-6 mx-auto flex items-center justify-center rounded-md font-black text-[10px] uppercase tracking-widest transition-all ${
                            currentTrial === trial ? `${getTrialColor(trial)} text-white shadow-sm` : 'text-slate-500'
                          }`}>
                            {getTrialLabel(trial)}
                          </div>
                        </th>
                      ))}
                      <th className="px-4 py-4 border-b border-l border-slate-200 font-black text-slate-400 text-[10px] uppercase tracking-widest sticky right-0 z-20 w-24 bg-slate-50 text-right">
                        Lista A
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {LISTA_A.map((word, idx) => (
                      <tr key={idx} className="hover:bg-slate-50/50 transition-colors">
                        <td className="px-4 py-3 border-r border-slate-100 font-bold text-slate-900 bg-white sticky left-0 z-10 text-left">
                          {word}
                        </td>
                        {TRIALS.map((trial) => {
                          const key = `${idx}-${trial}`
                          const isChecked = checkboxes[key]
                          return (
                            <td key={trial} className={`p-1 border-r border-slate-100 ${currentTrial === trial ? 'bg-primary/5' : ''}`}>
                              <button
                                type="button"
                                onMouseDown={() => handleCheckboxMouseDown(idx, trial)}
                                onMouseEnter={(event) => {
                                  if (event.buttons === 1) {
                                    handleCheckboxMouseEnter(idx, trial)
                                  }
                                }}
                                className={`w-10 h-6 mx-auto flex items-center justify-center transition-all duration-200 rounded-md ${
                                  isChecked
                                    ? `${getTrialColor(trial)} text-white shadow-sm`
                                    : 'bg-white border-2 border-slate-200 hover:border-slate-300'
                                }`}
                              >
                                {isChecked && (
                                  <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                  </svg>
                                )}
                              </button>
                            </td>
                          )
                        })}
                        <td className="px-4 py-3 font-bold text-slate-900 bg-white sticky right-0 z-10 border-l border-slate-100 text-right">
                          {word}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="rounded-[24px] bg-blue-50 p-6 border border-blue-100 text-center flex flex-col justify-center relative overflow-hidden">
                  <Activity className="absolute -right-4 -bottom-4 h-24 w-24 text-blue-500/10" />
                  <div className="text-[10px] font-black uppercase tracking-[0.2em] text-blue-500 mb-2">Fase Aprendizagem (A1-A5)</div>
                  <div className="text-4xl font-black text-blue-700 tracking-tight">
                    {TRIALS.slice(0, 5).reduce((sum, t) => sum + (scores[t] || getScoreForTrial(t)), 0)}
                    <span className="text-sm text-blue-400 font-bold ml-1">/ 75</span>
                  </div>
                </div>
                <div className="rounded-[24px] bg-amber-50 p-6 border border-amber-100 text-center flex flex-col justify-center relative overflow-hidden">
                  <Target className="absolute -right-4 -bottom-4 h-24 w-24 text-amber-500/10" />
                  <div className="text-[10px] font-black uppercase tracking-[0.2em] text-amber-600 mb-2">Interferência (B1)</div>
                  <div className="text-4xl font-black text-amber-700 tracking-tight">
                    {scores['b'] || getScoreForTrial('b')}
                    <span className="text-sm text-amber-400 font-bold ml-1">/ 15</span>
                  </div>
                </div>
                <div className="rounded-[24px] bg-purple-50 p-6 border border-purple-100 text-center flex flex-col justify-center relative overflow-hidden">
                  <Brain className="absolute -right-4 -bottom-4 h-24 w-24 text-purple-500/10" />
                  <div className="text-[10px] font-black uppercase tracking-[0.2em] text-purple-600 mb-2">Evocação Prolongada (A7)</div>
                  <div className="text-4xl font-black text-purple-700 tracking-tight">
                    {scores['a7'] || getScoreForTrial('a7')}
                    <span className="text-sm text-purple-400 font-bold ml-1">/ 15</span>
                  </div>
                </div>
              </div>
            </SectionCard>
          </div>
        ) : (
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-8">
            <SectionCard title="Fase de Reconhecimento" description="Assinale as palavras que o paciente reconhecer como pertencentes às listas anteriores.">
              
              <div className="mb-8 p-6 rounded-[24px] bg-slate-50 border border-slate-100 flex flex-wrap gap-4 items-center justify-between">
                <div className="flex items-center gap-3">
                  <Info className="h-5 w-5 text-slate-400" />
                  <p className="text-sm font-bold text-slate-600">Legenda de Distratores:</p>
                </div>
                <div className="flex flex-wrap items-center gap-3">
                  <span className="px-4 py-2 rounded-xl text-[10px] font-black tracking-widest bg-emerald-50 text-emerald-600 border border-emerald-100">A (Lista A)</span>
                  <span className="px-4 py-2 rounded-xl text-[10px] font-black tracking-widest bg-amber-50 text-amber-600 border border-amber-100">B (Lista B)</span>
                  <span className="px-4 py-2 rounded-xl text-[10px] font-black tracking-widest bg-rose-50 text-rose-600 border border-rose-100">S/F (Distratores)</span>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8 max-w-4xl mx-auto">
                {/* Divide in chunks of 10 to recreate the layout */}
                {Array.from({ length: 5 }).map((_, colIdx) => (
                  <div key={colIdx} className="space-y-1.5">
                    {RECOGNITION_WORDS.slice(colIdx * 10, (colIdx + 1) * 10).map((item, localIdx) => {
                      const idx = colIdx * 10 + localIdx
                      const isChecked = recognitionChecks[idx]
                      const isTypeA = item.type === 'A' || item.type.startsWith('A')
                      const isTypeB = item.type === 'B' || item.type.startsWith('B')
                      const typeClass = isTypeA 
                        ? (isChecked ? 'bg-white/20 text-white' : 'bg-emerald-50 text-emerald-600') 
                        : isTypeB 
                        ? (isChecked ? 'bg-white/20 text-white' : 'bg-amber-50 text-amber-600') 
                        : (isChecked ? 'bg-white/20 text-white' : 'bg-rose-50 text-rose-600')

                      return (
                        <button 
                          key={idx} 
                          type="button"
                          onMouseDown={() => handleRecognitionMouseDown(idx)}
                          onMouseEnter={(event) => {
                            if (event.buttons === 1) {
                              handleRecognitionMouseEnter(idx)
                            }
                          }}
                          className={`w-full flex items-center justify-between px-2 py-1.5 rounded-md border transition-all ${
                            isChecked 
                              ? 'bg-primary text-white border-primary shadow-sm transform hover:scale-105' 
                              : 'bg-white border-slate-200 hover:border-primary/40 hover:bg-slate-50'
                          }`}
                        >
                          <span className={`font-bold text-[10px] ${isChecked ? 'text-white' : 'text-slate-700'}`}>{item.word}</span>
                          <span className={`text-[8px] font-black tracking-widest px-1.5 py-0.5 rounded ${typeClass}`}>{item.type}</span>
                        </button>
                      )
                    })}
                  </div>
                ))}
              </div>

              <div className="grid md:grid-cols-2 gap-6 pt-8 border-t border-slate-100 max-w-2xl mx-auto">
                <div className="bg-emerald-50 p-6 rounded-[24px] border border-emerald-100 flex flex-col items-center justify-center relative overflow-hidden">
                   <div className="text-[10px] font-black uppercase text-emerald-600 mb-2 tracking-[0.2em] text-center">Itens Corretos (Marcados)</div>
                   <div className="text-5xl font-black text-emerald-700">
                     {getRecognitionStats().totalAcertos}<span className="text-xl text-emerald-400 font-bold ml-1">/50</span>
                   </div>
                   <div className="text-[9px] text-emerald-600 font-bold mt-2 text-center">Paciente identificou ou rejeitou corretamente</div>
                </div>

                <div className="bg-blue-50 p-6 rounded-[24px] border border-blue-100 flex flex-col items-center justify-center relative overflow-hidden">
                   <div className="text-[10px] font-black uppercase text-blue-700 mb-2 tracking-[0.2em] text-center">Escore Final de Reconhecimento</div>
                   <div className="text-5xl font-black text-blue-700">
                     {getRecognitionStats().totalAcertos - 35}<span className="text-xl text-blue-400 font-bold ml-1">/15</span>
                   </div>
                   <div className="text-[9px] text-blue-600 font-bold mt-2 text-center">Corretos (50) - 35</div>
                </div>
              </div>
            </SectionCard>
          </div>
        )}

        <div className="mt-8 flex justify-end">
          <Button
            onClick={handleSubmit}
            disabled={saving}
            className="px-12 h-14 rounded-2xl font-black uppercase tracking-widest gap-3 shadow-spike border-none text-white w-full sm:w-auto"
          >
            <Save className="h-5 w-5" />
            {saving ? 'Registrando Aplicação...' : 'Salvar Resultado'}
          </Button>
        </div>
      </SectionCard>
    </PageContainer>
  )
}

function RAVLTFormPageFallback() {
  return (
    <PageContainer>
      <div className="py-20 text-center text-slate-300 font-bold uppercase tracking-widest text-xs">Carregando módulo RAVLT...</div>
    </PageContainer>
  )
}

export default function RAVLTFormPage() {
  return (
    <Suspense fallback={<RAVLTFormPageFallback />}>
      <RAVLTFormPageContent />
    </Suspense>
  )
}
