'use client'

import { Suspense, useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import { useRouter, useSearchParams } from 'next/navigation'

import { api } from '@/lib/api'

import { WASI_COMPOSITE_LABELS, WASI_SUBTESTS, formatPtBrNumber } from './data'

type ExistingApplication = {
  evaluation_id?: number
  is_validated?: boolean
  raw_payload?: Record<string, any>
}

function WASIPageContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const evaluationId = searchParams.get('evaluation_id')
  const applicationId = searchParams.get('application_id')
  const isEditMode = searchParams.get('edit') === 'true'

  const [evaluation, setEvaluation] = useState<any>(null)
  const [scores, setScores] = useState<Record<string, string>>({})
  const [confidenceLevel, setConfidenceLevel] = useState('95')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    async function fetchData() {
      let currentEvaluationId = evaluationId

      if (applicationId) {
        try {
          const result = await api.get<ExistingApplication>(`/api/tests/applications/${applicationId}`)
          if (result?.evaluation_id && !currentEvaluationId) {
            router.replace(`/dashboard/tests/wasi?application_id=${applicationId}&evaluation_id=${result.evaluation_id}&edit=true`)
            return
          }
          if (result?.is_validated && !isEditMode) {
            router.push(`/dashboard/tests/wasi/${applicationId}/result?evaluation_id=${result.evaluation_id}`)
            return
          }
          const raw = result?.raw_payload || {}
          const nextScores: Record<string, string> = {}
          for (const subtest of WASI_SUBTESTS) {
            if (raw[subtest.key] !== undefined && raw[subtest.key] !== null) {
              nextScores[subtest.key] = String(raw[subtest.key])
            }
          }
          setScores(nextScores)
          if (raw.confidence_level) {
            setConfidenceLevel(String(raw.confidence_level))
          }
          if (result?.evaluation_id) {
            currentEvaluationId = String(result.evaluation_id)
          }
        } catch (error) {
          console.log('WASI sem aplicação anterior')
        }
      }

      if (!currentEvaluationId) {
        setLoading(false)
        return
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${currentEvaluationId}`)
        setEvaluation(data)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [applicationId, evaluationId, isEditMode, router])

  const previewSums = useMemo(() => {
    const values = Object.fromEntries(WASI_SUBTESTS.map((subtest) => [subtest.key, Number.parseInt(scores[subtest.key] || '0', 10) || 0]))
    return {
      qi_verbal: values.vc + values.sm,
      qi_execucao: values.cb + values.rm,
      qit_4: values.vc + values.sm + values.cb + values.rm,
      qit_2: values.vc + values.rm,
    }
  }, [scores])

  function handleChange(key: string, value: string) {
    if (value === '' || /^\d+$/.test(value)) {
      setScores((prev) => ({ ...prev, [key]: value }))
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!evaluationId) {
      alert('ID da avaliação não encontrado.')
      return
    }

    setSaving(true)
    try {
      const payload = {
        evaluation_id: Number.parseInt(evaluationId, 10),
        confidence_level: confidenceLevel,
        vc: Number.parseInt(scores.vc || '0', 10) || 0,
        sm: Number.parseInt(scores.sm || '0', 10) || 0,
        cb: Number.parseInt(scores.cb || '0', 10) || 0,
        rm: Number.parseInt(scores.rm || '0', 10) || 0,
      }
      const result = await api.post<{ application_id: number }>('/api/tests/wasi/submit', payload)
      router.push(`/dashboard/tests/wasi/${result.application_id}/result?evaluation_id=${evaluationId}`)
    } catch (error: any) {
      alert(error?.message || 'Erro ao salvar WASI.')
    } finally {
      setSaving(false)
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
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">WASI</h1>
              <p className="mt-1 text-sm text-zinc-600">Escala Wechsler Abreviada de Inteligência</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Informações</h3>
              {loading ? (
                <div className="py-4 text-center text-zinc-500">Carregando dados do paciente...</div>
              ) : evaluation ? (
                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                  <div>
                    <label className="mb-2 block text-sm font-medium text-zinc-700">Paciente</label>
                    <div className="w-full rounded-2xl border border-black/10 bg-slate-50 px-4 py-3 text-sm shadow-sm">{evaluation.patient_name}</div>
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-medium text-zinc-700">Data de nascimento</label>
                    <div className="w-full rounded-2xl border border-black/10 bg-slate-50 px-4 py-3 text-sm shadow-sm">{evaluation.patient_birth_date || '—'}</div>
                  </div>
                  <div>
                    <label className="mb-2 block text-sm font-medium text-zinc-700">Intervalo de confiança</label>
                    <select value={confidenceLevel} onChange={(e) => setConfidenceLevel(e.target.value)} className="w-full rounded-2xl border border-black/10 bg-white px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/10">
                      <option value="90">90%</option>
                      <option value="95">95%</option>
                    </select>
                  </div>
                </div>
              ) : (
                <div className="py-4 text-center text-red-500">Avaliação não encontrada</div>
              )}
            </div>

            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Pontos Brutos</h3>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
                {WASI_SUBTESTS.map((subtest) => (
                  <div key={subtest.key} className={`rounded-2xl border p-4 shadow-sm ${subtest.color}`}>
                    <div className="mb-2 flex items-center justify-between">
                      <span className="font-medium text-zinc-900">{subtest.name}</span>
                      <span className="rounded-full bg-white/80 px-2 py-0.5 text-xs text-zinc-600">{subtest.code}</span>
                    </div>
                    <input
                      type="number"
                      min="0"
                      value={scores[subtest.key] || ''}
                      onChange={(e) => handleChange(subtest.key, e.target.value)}
                      className="w-full rounded-xl border border-black/10 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-zinc-900/20"
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Preview das Somas</h3>
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
                {Object.entries(WASI_COMPOSITE_LABELS).map(([key, label]) => (
                  <div key={key} className="rounded-2xl border border-black/10 bg-white p-4 shadow-sm">
                    <p className="text-sm font-medium text-zinc-700">{label}</p>
                    <p className="mt-2 text-3xl font-semibold text-zinc-900">{formatPtBrNumber(previewSums[key as keyof typeof previewSums], 0)}</p>
                    <p className="mt-1 text-xs text-zinc-500">Soma dos pontos brutos dos subtestes envolvidos</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end gap-3">
              <Link href={evaluationId ? `/dashboard/evaluations/${evaluationId}?tab=overview` : '/dashboard/tests'} className="rounded-full border border-black/10 bg-white px-5 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50">
                Cancelar
              </Link>
              <button type="submit" disabled={saving} className="rounded-full bg-zinc-900 px-5 py-2 text-sm font-medium text-white shadow-lg disabled:opacity-50">
                {saving ? 'Salvando...' : isEditMode ? 'Salvar alterações' : 'Salvar WASI'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

function WASIPageFallback() {
  return <div className="space-y-6" />
}

export default function WASIPage() {
  return (
    <Suspense fallback={<WASIPageFallback />}>
      <WASIPageContent />
    </Suspense>
  )
}
