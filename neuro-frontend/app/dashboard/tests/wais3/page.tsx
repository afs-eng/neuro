'use client'

import { Suspense, useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'
import { api } from '@/lib/api'

type Subtest = {
  code: string
  name: string
  maxScore?: number
  domain?: 'verbal' | 'execucao' | 'suplementar'
}

type ProcessScore = {
  key: string
  name: string
  group: 'digitos' | 'sequencia'
}

const subtests: Subtest[] = [
  // Escala de Execução
  { code: 'completar_figuras', name: 'Completar Figuras', maxScore: 25, domain: 'execucao' },
  { code: 'vocabulario', name: 'Vocabulário', maxScore: 66, domain: 'verbal' },
  { code: 'codigos', name: 'Códigos', maxScore: 133, domain: 'execucao' },
  { code: 'semelhancas', name: 'Semelhanças', maxScore: 38, domain: 'verbal' },
  { code: 'cubos', name: 'Cubos', maxScore: 68, domain: 'execucao' },
  { code: 'aritmetica', name: 'Aritmética', maxScore: 22, domain: 'verbal' },
  { code: 'raciocinio_matricial', name: 'Raciocínio Matricial', maxScore: 26, domain: 'execucao' },
  { code: 'digitos', name: 'Dígitos', maxScore: 30, domain: 'verbal' },
  { code: 'informacao', name: 'Informação', maxScore: 28, domain: 'verbal' },
  { code: 'arranjo_figuras', name: 'Arranjo de Figuras', maxScore: 22, domain: 'execucao' },
  { code: 'compreensao', name: 'Compreensão', maxScore: 33, domain: 'verbal' },
  { code: 'procurar_simbolos', name: 'Procurar Símbolos', maxScore: 60, domain: 'execucao' },
  { code: 'sequencia_numeros_letras', name: 'Sequência de Números e Letras', maxScore: 21, domain: 'suplementar' },
  { code: 'armar_objetos', name: 'Armar Objetos', maxScore: 52, domain: 'suplementar' },
]

const processScores: ProcessScore[] = [
  { key: 'digitos_ordem_direta', name: 'Dígitos - Ordem Direta', group: 'digitos' },
  { key: 'digitos_ordem_inversa', name: 'Dígitos - Ordem Inversa', group: 'digitos' },
  { key: 'maior_sequencia_digitos_direta', name: 'Maior Sequência de Dígitos OD', group: 'sequencia' },
  { key: 'maior_sequencia_digitos_inversa', name: 'Maior Sequência de Dígitos OI', group: 'sequencia' },
]

function WAIS3PageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const evaluationId = searchParams.get('evaluation_id')
  const applicationId = searchParams.get('application_id')
  const isEditMode = searchParams.get('edit') === 'true'

  const [evaluation, setEvaluation] = useState<any>(null)
  const [scores, setScores] = useState<Record<string, number | null>>({})
  const [digitProcessScores, setDigitProcessScores] = useState<Record<string, number | null>>({})
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [loading, setLoading] = useState(true)
  const [preview, setPreview] = useState<any>(null)
  const [previewLoading, setPreviewLoading] = useState(false)

  useEffect(() => {
    async function fetchData() {
      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result?.evaluation_id && !evaluationId) {
            router.replace(`/dashboard/tests/wais3?application_id=${applicationId}&evaluation_id=${result.evaluation_id}&edit=true`)
            return
          }
          if (result?.is_validated && !isEditMode) {
            router.push(`/dashboard/tests/wais3/${applicationId}/result?evaluation_id=${result.evaluation_id}`)
            return
          }
          const raw = result?.raw_payload || {}
          const existing = raw.subtestes || {}
          const nextScores: Record<string, number | null> = {}
          for (const subtest of subtests) {
            nextScores[subtest.code] = existing[subtest.code]?.pontos_brutos ?? null
          }
          setScores(nextScores)
          const nextProcessScores: Record<string, number | null> = {}
          const existingProcess = raw.process_scores || {}
          for (const field of processScores) {
            nextProcessScores[field.key] = existingProcess[field.key] ?? null
          }
          setDigitProcessScores(nextProcessScores)
        } catch (error) {
          console.log('WAIS-III ainda sem aplicação existente')
        }
      }

      if (!evaluationId) {
        setLoading(false)
        return
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${evaluationId}`)
        setEvaluation(data)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [applicationId, evaluationId, isEditMode, router])

  const handleChange = (code: string, value: string) => {
    const subtest = subtests.find(s => s.code === code)
    const numVal = value === '' ? null : parseInt(value, 10)

    if (numVal !== null && subtest?.maxScore && numVal > subtest.maxScore) {
      setErrors(prev => ({ ...prev, [code]: `Valor máximo permitido: ${subtest.maxScore}` }))
    } else {
      setErrors(prev => {
        const next = { ...prev }
        delete next[code]
        return next
      })
    }

    setScores((prev) => ({ ...prev, [code]: numVal }))
  }

  const handleProcessChange = (key: string, value: string) => {
    const numVal = value === '' ? null : parseInt(value, 10)
    setDigitProcessScores((prev) => ({ ...prev, [key]: numVal }))
  }

  // Fetch preview whenever scores change
  useEffect(() => {
    if (!evaluationId) return
    
    const hasAnyScore = Object.values(scores).some(v => v !== null)
    if (!hasAnyScore) {
      setPreview(null)
      return
    }

    const fetchPreview = async () => {
      setPreviewLoading(true)
      try {
        const payload: Record<string, any> = {
          evaluation_id: parseInt(evaluationId, 10),
        }
        for (const subtest of subtests) {
          payload[subtest.code] = scores[subtest.code] == null ? '' : String(scores[subtest.code])
        }
        for (const field of processScores) {
          payload[field.key] = digitProcessScores[field.key] == null ? '' : String(digitProcessScores[field.key])
        }
        
        const result = await api.post<any>('/api/tests/wais3/preview', payload)
        setPreview(result)
      } catch (error) {
        console.error('Preview error:', error)
        setPreview(null)
      } finally {
        setPreviewLoading(false)
      }
    }

    const timer = setTimeout(fetchPreview, 500)
    return () => clearTimeout(timer)
  }, [scores, digitProcessScores, evaluationId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!evaluationId) {
      alert('ID da avaliação não encontrado.')
      return
    }

    // Validate max scores before submit
    const validationErrors: Record<string, string> = {}
    for (const subtest of subtests) {
      const val = scores[subtest.code]
      if (val !== null && subtest.maxScore && val > subtest.maxScore) {
        validationErrors[subtest.code] = `Valor máximo permitido: ${subtest.maxScore}`
      }
    }
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors)
      const firstError = Object.values(validationErrors)[0]
      alert(`Erro de validação: ${firstError}`)
      return
    }

    const payload: Record<string, string | number> = {
      evaluation_id: parseInt(evaluationId, 10),
    }
    for (const subtest of subtests) {
      payload[subtest.code] = scores[subtest.code] == null ? '' : String(scores[subtest.code])
    }
    for (const field of processScores) {
      payload[field.key] = digitProcessScores[field.key] == null ? '' : String(digitProcessScores[field.key])
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/wais3/submit', payload)
      router.push(`/dashboard/tests/wais3/${result.application_id}/result?evaluation_id=${evaluationId}`)
    } catch (error: any) {
      alert(error?.message || 'Erro ao salvar WAIS-III.')
    }
  }

  return (
    <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">NeuroAvalia</div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
              <Link href="/dashboard/tests" className="rounded-full px-4 py-2 bg-zinc-900 text-white shadow">Testes</Link>
            </nav>
          </header>

          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">WAIS-III</h1>
              <p className="mt-1 text-sm text-zinc-600">Escala de Inteligência Wechsler para Adultos</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Informações</h3>
              {loading ? (
                <div className="py-4 text-center text-zinc-500">Carregando dados do paciente...</div>
              ) : evaluation ? (
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-zinc-700">Paciente</label>
                    <div className="w-full rounded-2xl border border-black/10 bg-slate-50 px-4 py-3 text-sm shadow-sm">{evaluation.patient_name}</div>
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-medium text-zinc-700">Data de nascimento</label>
                    <div className="w-full rounded-2xl border border-black/10 bg-slate-50 px-4 py-3 text-sm shadow-sm">{evaluation.patient_birth_date || '—'}</div>
                  </div>
                </div>
              ) : (
                <div className="py-4 text-center text-red-500">Avaliação não encontrada</div>
              )}
            </div>

            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <div className="mb-4 flex items-center justify-between">
                <h3 className="text-lg font-semibold text-zinc-900">Pontos Brutos</h3>
                <div className="flex gap-3 text-xs">
                  <div className="flex items-center gap-1">
                    <div className="h-3 w-3 rounded bg-blue-200"></div>
                    <span className="text-zinc-600">Execução</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="h-3 w-3 rounded bg-yellow-200"></div>
                    <span className="text-zinc-600">Verbal</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <div className="h-3 w-3 rounded bg-green-200"></div>
                    <span className="text-zinc-600">Suplementar</span>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
                {subtests.map((subtest) => {
                  const domainColors = {
                    execucao: 'bg-blue-50 border-blue-200',
                    verbal: 'bg-yellow-50 border-yellow-200',
                    suplementar: 'bg-green-50 border-green-200',
                  }
                  const bgClass = subtest.domain ? domainColors[subtest.domain] || 'bg-white border-black/10' : 'bg-white border-black/10'
                  
                  return (
                    <div key={subtest.code} className={`rounded-2xl border p-4 shadow-sm ${bgClass}`}>
                      <div className="mb-2 flex items-center justify-between">
                        <span className="font-medium text-zinc-900">{subtest.name}</span>
                        {subtest.maxScore && <span className="text-xs text-zinc-500">máx: {subtest.maxScore}</span>}
                      </div>
                      <input
                        type="number"
                        min="0"
                        max={subtest.maxScore}
                        value={scores[subtest.code] ?? ''}
                        onChange={(e) => handleChange(subtest.code, e.target.value)}
                        className={`w-full rounded-xl border px-3 py-2 text-sm focus:outline-none focus:ring-2 ${errors[subtest.code] ? 'border-red-400 focus:ring-red-500/20' : 'border-black/10 focus:ring-zinc-900/20'}`}
                      />
                      {errors[subtest.code] && (
                        <p className="mt-1 text-xs text-red-600">{errors[subtest.code]}</p>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Escores de Processo - Dígitos</h3>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
                {processScores.map((field) => (
                  <div key={field.key} className="rounded-2xl border border-black/10 bg-white p-4 shadow-sm">
                    <div className="mb-2 flex items-center justify-between">
                      <span className="font-medium text-zinc-900">{field.name}</span>
                      <span className={`rounded-full px-2 py-0.5 text-xs ${field.group === 'digitos' ? 'bg-purple-100 text-purple-700' : 'bg-teal-100 text-teal-700'}`}>
                        {field.group === 'digitos' ? 'B.6' : 'B.7'}
                      </span>
                    </div>
                    <input
                      type="number"
                      min="0"
                      value={digitProcessScores[field.key] ?? ''}
                      onChange={(e) => handleProcessChange(field.key, e.target.value)}
                      className="w-full rounded-xl border border-black/10 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
                    />
                  </div>
                ))}
              </div>
            </div>

            {/* Preview Section */}
            {preview && (
              <div className="space-y-4">
                {/* Índices */}
                {Object.keys(preview.indices || {}).length > 0 && (
                  <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
                    <h3 className="mb-4 text-lg font-semibold text-zinc-900">Índices e QI (Preview)</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-black/10">
                            <th className="px-3 py-2 text-left font-semibold text-zinc-700">Índice</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Soma</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Escore</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Percentil</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Classificação</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-black/5">
                          {Object.entries(preview.indices || {}).map(([key, idx]: [string, any]) => (
                            <tr key={key} className="hover:bg-black/2">
                              <td className="px-3 py-2 text-zinc-900">{idx.nome || key}</td>
                              <td className="px-3 py-2 text-center text-zinc-700">{idx.soma_ponderada ?? '—'}</td>
                              <td className="px-3 py-2 text-center font-medium text-zinc-900">{idx.pontuacao_composta ?? '—'}</td>
                              <td className="px-3 py-2 text-center text-zinc-700">{idx.percentil ?? '—'}</td>
                              <td className="px-3 py-2 text-center text-zinc-700">{idx.classificacao ?? '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Subtestes */}
                {Object.keys(preview.subtestes || {}).length > 0 && (
                  <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
                    <h3 className="mb-4 text-lg font-semibold text-zinc-900">Subtestes (Preview)</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-black/10">
                            <th className="px-3 py-2 text-left font-semibold text-zinc-700">Subteste</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Bruto</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Ponderado</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Classificação</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-black/5">
                          {Object.entries(preview.subtestes || {}).map(([key, st]: [string, any]) => (
                            <tr key={key} className="hover:bg-black/2">
                              <td className="px-3 py-2 text-zinc-900">{st.nome || key}</td>
                              <td className="px-3 py-2 text-center font-medium text-zinc-700">{st.pontos_brutos ?? '—'}</td>
                              <td className="px-3 py-2 text-center font-medium text-zinc-900">{st.escore_ponderado ?? '—'}</td>
                              <td className="px-3 py-2 text-center text-zinc-700">{st.classificacao ?? '—'}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {/* Warnings */}
                {preview.warnings && preview.warnings.length > 0 && (
                  <div className="rounded-[28px] bg-yellow-50/70 p-5 shadow-lg ring-1 ring-yellow-200">
                    <h3 className="mb-2 text-sm font-semibold text-yellow-900">⚠️ Avisos</h3>
                    <ul className="space-y-1">
                      {preview.warnings.map((w: string, i: number) => (
                        <li key={i} className="text-xs text-yellow-800">• {w}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {preview.digitos && Object.keys(preview.digitos).length > 0 && (
                  <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
                    <h3 className="mb-4 text-lg font-semibold text-zinc-900">Dígitos - Processo (Preview)</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="border-b border-black/10">
                            <th className="px-3 py-2 text-left font-semibold text-zinc-700">Medida</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Bruto</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Freq. Acum.</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Percentil</th>
                            <th className="px-3 py-2 text-center font-semibold text-zinc-700">Classificação</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-black/5">
                          {[
                            ['ordem_direta', 'Dígitos - Ordem Direta'],
                            ['ordem_inversa', 'Dígitos - Ordem Inversa'],
                            ['maior_sequencia_direta', 'Maior Sequência OD'],
                            ['maior_sequencia_inversa', 'Maior Sequência OI'],
                            ['diferenca_maior_sequencia', 'Diferença OD - OI'],
                          ].map(([key, label]) => {
                            const item = preview.digitos?.[key]
                            if (!item) return null
                            return (
                              <tr key={key} className="hover:bg-black/2">
                                <td className="px-3 py-2 text-zinc-900">{label}</td>
                                <td className="px-3 py-2 text-center text-zinc-700">{item.difference ?? item.raw_score ?? '—'}</td>
                                <td className="px-3 py-2 text-center text-zinc-700">{item.cumulative_frequency ?? '—'}</td>
                                <td className="px-3 py-2 text-center text-zinc-700">{item.percentile ?? '—'}</td>
                                <td className="px-3 py-2 text-center text-zinc-700">{item.classification ?? '—'}</td>
                              </tr>
                            )
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="flex items-center justify-end gap-3">
              <Link href={evaluationId ? `/dashboard/evaluations/${evaluationId}?tab=overview` : '/dashboard/tests'} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50">Cancelar</Link>
              <button type="submit" className="rounded-full bg-zinc-900 px-5 py-2 text-sm font-medium text-white shadow-lg">Salvar WAIS-III</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

export default function WAIS3Page() {
  return (
    <Suspense>
      <WAIS3PageContent />
    </Suspense>
  )
}
