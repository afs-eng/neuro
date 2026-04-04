'use client'

import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { api } from '@/lib/api'

const LISTA_A = [
  "BALÃO", "FLOR", "SALA", "BOCA", "CHUVA", "MÃE", "CIRCO", "PEIXE", "LUA", "CORPO", "CESTA", "LÁPIS", "MESA", "CHAPÉU", "MILHO"
]

const LISTA_B = [
  "CARRO", "MEIA", "PATO", "FOGO", "SOFÁ", "DOCE", "PONTO", "VASO", "LIVRO", "PORTA", "ÍNDIO", "VACA", "ROUPA", "CAIXA", "RIO"
]

const RECOGNITION_WORDS = [
  { word: "TAMBOR", type: "A" },
  { word: "CORTINA", type: "A" },
  { word: "SINO", type: "A" },
  { word: "CAFÉ", type: "A" },
  { word: "ESCOLA", type: "A" },
  { word: "LUA", type: "A" },
  { word: "GALO", type: "B" },
  { word: "FOGO", type: "B" },
  { word: "COR", type: "D" },
  { word: "CASA", type: "D" },
  { word: "JARDIM", type: "A" },
  { word: "CHAPÉU", type: "A" },
  { word: "ESTRADA", type: "B" },
  { word: "CÉU", type: "D" },
  { word: "SOL", type: "A" },
  { word: "PEIXE", type: "A" },
  { word: "MAÇÃ", type: "B" },
  { word: "BARCO", type: "A" },
  { word: "FERRO", type: "D" },
  { word: "AGULHA", type: "A" },
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

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");

  useEffect(() => {
    async function fetchEvaluation() {
      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
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

  const toggleCheckbox = (wordIndex: number, trial: string) => {
    const key = `${wordIndex}-${trial}`
    setCheckboxes(prev => {
      const newState = { ...prev, [key]: !prev[key] }
      const trialCheckboxes = Object.entries(newState)
        .filter(([k]) => k.endsWith(`-${trial}`))
        .filter(([, v]) => v).length
      setScores(prev => ({ ...prev, [trial]: trialCheckboxes }))
      return newState
    })
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
      a1: 'bg-[#001e42]', a2: 'bg-[#001e42]', a3: 'bg-[#001e42]', a4: 'bg-[#001e42]', a5: 'bg-[#001e42]',
      b: 'bg-orange-500', a6: 'bg-[#001e42]', a7: 'bg-purple-500'
    }
    return colors[trial] || 'bg-zinc-500'
  }

  const getScoreForTrial = (trial: string) => {
    return Object.entries(checkboxes)
      .filter(([k]) => k.endsWith(`-${trial}`))
      .filter(([, v]) => v).length
  }

  const toggleRecognition = (index: number) => {
    setRecognitionChecks(prev => ({ ...prev, [index]: !prev[index] }))
  }

  const getRecognitionStats = () => {
    const acertosA = Object.entries(recognitionChecks)
      .filter(([k, v]) => {
        const word = RECOGNITION_WORDS[parseInt(k)]
        return word?.type === 'A' && v
      }).length
    const acertosB = Object.entries(recognitionChecks)
      .filter(([k, v]) => {
        const word = RECOGNITION_WORDS[parseInt(k)]
        return word?.type === 'B' && v
      }).length
    const falsos = Object.entries(recognitionChecks)
      .filter(([k, v]) => {
        const word = RECOGNITION_WORDS[parseInt(k)]
        return word?.type === 'D' && v
      }).length
    return { acertosA, acertosB, falsos }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!evaluationId) {
      alert('ID da avaliação não encontrado.')
      return
    }

    setSaving(true)
    try {
      const stats = getRecognitionStats()
      const payload = {
        evaluation_id: parseInt(evaluationId),
        a1: scores['a1'] || 0,
        a2: scores['a2'] || 0,
        a3: scores['a3'] || 0,
        a4: scores['a4'] || 0,
        a5: scores['a5'] || 0,
        b: scores['b'] || 0,
        a6: scores['a6'] || 0,
        a7: scores['a7'] || 0,
        reconhecimento: stats.acertosA + 35,
      }

      const result = await api.post<{ application_id: number }>('/api/tests/ravlt/submit', payload)
      alert('RAVLT salvo com sucesso!')
      router.push(`/dashboard/tests/ravlt/${result.application_id}/result?evaluation_id=${evaluationId}`)
    } catch (error: any) {
      console.error('Erro completo:', error)
      alert('Erro ao salvar. Ver console para detalhes.')
    } finally {
      setSaving(false)
    }
  }

  if (loadingEvaluation) {
    return (
      <div className="min-h-screen w-full bg-[#f6fafe] p-4">
        <div className="mx-auto max-w-6xl rounded-2xl bg-white p-8 shadow-lg">
          <div className="flex items-center justify-center py-20">
            <div className="text-zinc-600">Carregando...</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen w-full bg-[#f6fafe] p-4 md:p-6">
      <div className="mx-auto max-w-6xl">
        
        <header className="mb-6 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center gap-3">
            <Link href="/dashboard/tests" className="rounded-full bg-white p-2 shadow-sm hover:bg-zinc-50">
              ←
            </Link>
            <div>
              <h1 className="text-xl font-bold text-[#001e42]">RAVLT</h1>
              <p className="text-sm text-zinc-500">{evaluation?.patient_name || 'Paciente'}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('general')}
              className={`px-4 py-2 rounded-lg font-bold text-sm transition-all ${
                activeTab === 'general'
                  ? 'bg-[#001e42] text-white'
                  : 'bg-white text-zinc-600 border border-zinc-200'
              }`}
            >
              Geral
            </button>
            <button
              onClick={() => setActiveTab('recognition')}
              className={`px-4 py-2 rounded-lg font-bold text-sm transition-all ${
                activeTab === 'recognition'
                  ? 'bg-[#001e42] text-white'
                  : 'bg-white text-zinc-600 border border-zinc-200'
              }`}
            >
              Reconhecimento
            </button>
          </div>
        </header>

        {activeTab === 'general' ? (
          <>
            <div className="mb-4 flex gap-2 overflow-x-auto pb-2">
              {TRIALS.map((trial) => (
                <button
                  key={trial}
                  onClick={() => setCurrentTrial(trial)}
                  className={`flex-shrink-0 px-4 py-2 rounded-lg font-bold text-sm transition-all ${
                    currentTrial === trial
                      ? `${getTrialColor(trial)} text-white shadow-md`
                      : 'bg-white text-zinc-600 border border-zinc-200 hover:bg-zinc-50'
                  }`}
                >
                  {getTrialLabel(trial)}
                  <span className="ml-1 text-xs opacity-75">({getScoreForTrial(trial)})</span>
                </button>
              ))}
            </div>

            <div className="mb-4 overflow-x-auto rounded-xl border border-[#c3c6d1] bg-white shadow-sm">
              <table className="w-full min-w-[800px] border-collapse text-xs">
                <thead className="sticky top-0 z-10 bg-[#e4e9ed]">
                  <tr>
                    <th className="px-2 py-3 border-b border-r border-[#c3c6d1] font-bold text-[#001e42] bg-white sticky left-0 z-20 w-20">
                      LISTA A
                    </th>
                    {TRIALS.map((trial) => (
                      <th 
                        key={trial} 
                        className={`px-2 py-3 border-b border-r border-[#c3c6d1] text-center font-bold text-white min-w-[50px] ${
                          trial === 'b' ? 'bg-orange-500' : trial === 'a7' ? 'bg-purple-500' : 'bg-[#001e42]'
                        }`}
                      >
                        {getTrialLabel(trial)}
                      </th>
                    ))}
                    <th className="px-2 py-3 border-b border-[#c3c6d1] font-bold text-[#001e42] bg-white sticky right-0 z-20 w-20">
                      LISTA A
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#c3c6d1]">
                  {LISTA_A.map((word, idx) => (
                    <tr key={idx} className="hover:bg-[#eaeef2] transition-colors">
                      <td className="px-2 py-2 border-r border-[#c3c6d1] font-bold text-[#001e42] bg-white sticky left-0 z-10">
                        {word}
                      </td>
                      {TRIALS.map((trial) => {
                        const key = `${idx}-${trial}`
                        const isChecked = checkboxes[key]
                        return (
                          <td key={trial} className="p-0 border-r border-[#c3c6d1]">
                            <button
                              onClick={() => toggleCheckbox(idx, trial)}
                              className={`w-full h-10 flex items-center justify-center transition-all duration-200 hover:scale-105 ${
                                isChecked
                                  ? `${getTrialColor(trial)}`
                                  : 'bg-transparent border-2 border-[#c3c6d1] rounded-sm hover:border-[#001e42]'
                              }`}
                            >
                              {isChecked && (
                                <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                              )}
                            </button>
                          </td>
                        )
                      })}
                      <td className="px-2 py-2 font-bold text-[#001e42] bg-white sticky right-0 z-10 border-l border-[#c3c6d1]">
                        {word}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="rounded-xl bg-blue-50 p-4 border border-blue-200">
                <div className="text-sm font-bold text-blue-700 mb-2">Fase Aprendizagem (A1-A5)</div>
                <div className="text-3xl font-bold text-blue-800">
                  {TRIALS.slice(0, 5).reduce((sum, t) => sum + (scores[t] || getScoreForTrial(t)), 0)}
                </div>
                <div className="text-xs text-blue-600">/ 75 pontos</div>
              </div>
              <div className="rounded-xl bg-orange-50 p-4 border border-orange-200">
                <div className="text-sm font-bold text-orange-700 mb-2">Interferência (B1)</div>
                <div className="text-3xl font-bold text-orange-800">
                  {scores['b'] || getScoreForTrial('b')}
                </div>
                <div className="text-xs text-orange-600">/ 15 pontos</div>
              </div>
              <div className="rounded-xl bg-purple-50 p-4 border border-purple-200">
                <div className="text-sm font-bold text-purple-700 mb-2">Evocação Prolongada</div>
                <div className="text-3xl font-bold text-purple-800">
                  {scores['a7'] || getScoreForTrial('a7')}
                </div>
                <div className="text-xs text-purple-600">A7 - 30 min</div>
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="mb-6 bg-[#f0f4f8] p-6 rounded-full border border-[#c3c6d1]/15">
              <div className="flex items-start gap-4">
                <span className="text-[#001e42] text-2xl">ℹ️</span>
                <div>
                  <h2 className="text-sm font-extrabold text-[#001e42] uppercase mb-2">Instrução de Aplicação</h2>
                  <p className="text-[#43474f] font-medium">
                    Assinale as palavras que o paciente reconhecer como pertencentes às listas anteriores.
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#d6e3ff] text-[#001e42]">A (LISTA A)</span>
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#d0e1fb] text-[#54647a]">B (LISTA B)</span>
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-[#dfe3e7] text-[#737780]">S/F (DISTRATORES)</span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {RECOGNITION_WORDS.map((item, idx) => {
                  const isChecked = recognitionChecks[idx]
                  return (
                    <button
                      key={idx}
                      onClick={() => toggleRecognition(idx)}
                      className={`flex items-center justify-between p-4 rounded-xl border transition-all ${
                        isChecked
                          ? 'bg-[#001e42] text-white border-[#001e42]'
                          : 'bg-white border-[#c3c6d1] hover:border-[#001e42] hover:bg-[#f0f4f8]'
                      }`}
                    >
                      <span className={`font-bold ${isChecked ? 'text-white' : 'text-[#001e42]'}`}>
                        {item.word}
                      </span>
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          isChecked ? 'bg-white/20 text-white' : 
                          item.type === 'A' ? 'bg-[#d6e3ff] text-[#001e42]' :
                          item.type === 'B' ? 'bg-[#d0e1fb] text-[#54647a]' :
                          'bg-[#dfe3e7] text-[#737780]'
                        }`}>
                          {item.type === 'A' ? 'A' : item.type === 'B' ? 'B' : 'S/F'}
                        </span>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-4">
              <div className="bg-[#eaeef2] p-6 rounded-full border border-[#c3c6d1]/10 flex flex-col items-center">
                <span className="text-[10px] font-bold uppercase text-[#505f76] mb-1">Acertos Lista A</span>
                <span className="text-4xl font-bold text-[#001e42]">
                  {getRecognitionStats().acertosA}<span className="text-lg text-[#505f76] font-medium">/15</span>
                </span>
              </div>
              <div className="bg-[#f0f4f8] p-6 rounded-full border border-[#c3c6d1]/10 flex flex-col items-center">
                <span className="text-[10px] font-bold uppercase text-[#505f76] mb-1">Acertos Lista B</span>
                <span className="text-4xl font-bold text-[#001e42]">
                  {getRecognitionStats().acertosB}<span className="text-lg text-[#505f76] font-medium">/15</span>
                </span>
              </div>
              <div className="bg-red-50 p-6 rounded-full border border-red-200 flex flex-col items-center">
                <span className="text-[10px] font-bold uppercase text-red-700 mb-1">Falsos Positivos</span>
                <span className="text-4xl font-bold text-red-600">{getRecognitionStats().falsos}</span>
              </div>
            </div>
          </>
        )}

        <div className="mt-6 flex justify-end gap-4">
          <Link
            href="/dashboard/tests"
            className="rounded-full border border-[#c3c6d1] bg-white px-6 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50"
          >
            Cancelar
          </Link>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="rounded-full bg-[#001e42] px-8 py-2 text-sm font-medium text-white shadow-md hover:bg-[#002244] disabled:opacity-50"
          >
            {saving ? 'Salvando...' : 'Salvar Resultado'}
          </button>
        </div>
      </div>
    </div>
  )
}

function RAVLTFormPageFallback() {
  return <div className="min-h-screen w-full bg-[#f6fafe] p-4" />
}

export default function RAVLTFormPage() {
  return (
    <Suspense fallback={<RAVLTFormPageFallback />}>
      <RAVLTFormPageContent />
    </Suspense>
  )
}