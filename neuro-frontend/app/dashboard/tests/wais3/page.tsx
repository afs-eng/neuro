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

const subtests: Subtest[] = [
  // Escala de Execução
  { code: 'completar_figuras', name: 'Completar Figuras', domain: 'execucao' },
  { code: 'vocabulario', name: 'Vocabulário', domain: 'verbal' },
  { code: 'codigos', name: 'Códigos', domain: 'execucao' },
  { code: 'semelhancas', name: 'Semelhanças', domain: 'verbal' },
  { code: 'cubos', name: 'Cubos', domain: 'execucao' },
  { code: 'aritmetica', name: 'Aritmética', domain: 'verbal' },
  { code: 'raciocinio_matricial', name: 'Raciocínio Matricial', domain: 'execucao' },
  { code: 'digitos', name: 'Dígitos', domain: 'verbal' },
  { code: 'informacao', name: 'Informação', domain: 'verbal' },
  { code: 'arranjo_figuras', name: 'Arranjo de Figuras', domain: 'execucao' },
  { code: 'compreensao', name: 'Compreensão', domain: 'verbal' },
  { code: 'procurar_simbolos', name: 'Procurar Símbolos', domain: 'execucao' },
  { code: 'sequencia_numeros_letras', name: 'Sequência de Números e Letras', domain: 'suplementar' },
  { code: 'armar_objetos', name: 'Armar Objetos', domain: 'suplementar' },
]

function WAIS3PageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const evaluationId = searchParams.get('evaluation_id')
  const applicationId = searchParams.get('application_id')
  const isEditMode = searchParams.get('edit') === 'true'

  const [evaluation, setEvaluation] = useState<any>(null)
  const [scores, setScores] = useState<Record<string, number | null>>({})
  const [loading, setLoading] = useState(true)

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
    setScores((prev) => ({ ...prev, [code]: value === '' ? null : parseInt(value, 10) }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!evaluationId) {
      alert('ID da avaliação não encontrado.')
      return
    }

    const payload: Record<string, string | number> = {
      evaluation_id: parseInt(evaluationId, 10),
    }
    for (const subtest of subtests) {
      payload[subtest.code] = scores[subtest.code] == null ? '' : String(scores[subtest.code])
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
                      </div>
                      <input
                        type="number"
                        min="0"
                        value={scores[subtest.code] ?? ''}
                        onChange={(e) => handleChange(subtest.code, e.target.value)}
                        className="w-full rounded-xl border border-black/10 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
                      />
                    </div>
                  )
                })}
              </div>
            </div>

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
