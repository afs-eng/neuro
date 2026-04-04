'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

export default function RAVLTResultPage() {
  const params = useParams()
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const { api } = await import('@/lib/api')
        const data = await api.get<any>(`/api/tests/ravlt/result/${params.id}`)
        setResult(data)
      } catch (e) {
        console.error(e)
      } finally {
        setLoading(false)
      }
    }
    if (params.id) {
      fetchResult()
    }
  }, [params.id])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Carregando...</div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center">
        <div className="text-zinc-600">Resultado não encontrado</div>
      </div>
    )
  }

  const rawPayload = result.raw_payload || {}
  const results = result.results || {}

  return (
    <div className="min-h-screen bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          {/* Header */}
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
              <Link href="/dashboard/tests" className="rounded-full px-4 py-2 hover:bg-black/5">Testes</Link>
            </nav>
          </header>

          {/* Title */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">RAVLT</h1>
              <p className="mt-1 text-sm text-zinc-600">Teste de Aprendizagem Auditivo-Verbal de Rey</p>
            </div>
            <Link
              href={`/dashboard/tests/ravlt/${params.id}?evaluation_id=${result.evaluation_id}&edit=true`}
              className="rounded-full bg-zinc-900 px-6 py-2 text-sm font-medium text-white"
            >
              Editar
            </Link>
          </div>

          {/* Patient Info */}
          <div className="mb-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Informações do Paciente</h3>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div>
                <span className="text-sm text-zinc-500">Paciente</span>
                <div className="text-lg font-medium text-zinc-900">{result.patient_name}</div>
              </div>
              <div>
                <span className="text-sm text-zinc-500">Data da Aplicação</span>
                <div className="text-lg font-medium text-zinc-900">{result.applied_on || '-'}</div>
              </div>
              <div>
                <span className="text-sm text-zinc-500">Avaliação</span>
                <div className="text-lg font-medium text-zinc-900">#{result.evaluation_id}</div>
              </div>
            </div>
          </div>

          {/* Learning Curve */}
          <div className="mb-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Curva de Aprendizagem (Tentativas A1-A5)</h3>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-5">
              {['a1', 'a2', 'a3', 'a4', 'a5'].map((trial, idx) => {
                const score = rawPayload[trial] || 0
                const maxScore = 15
                const percentage = (score / maxScore) * 100
                return (
                  <div key={trial} className="rounded-2xl border border-black/10 bg-white p-4 text-center">
                    <div className="text-sm font-medium text-zinc-500">Tentativa {idx + 1}</div>
                    <div className="mt-2 text-3xl font-semibold text-zinc-900">{score}</div>
                    <div className="mt-2 text-xs text-zinc-500">de {maxScore}</div>
                    <div className="mt-3 h-3 w-full rounded-full bg-zinc-100">
                      <div 
                        className="h-3 rounded-full bg-zinc-900 transition-all"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* All Scores */}
          <div className="mb-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Todos os Escores</h3>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
              {[
                { code: 'a1', name: 'Tentativa A1' },
                { code: 'a2', name: 'Tentativa A2' },
                { code: 'a3', name: 'Tentativa A3' },
                { code: 'a4', name: 'Tentativa A4' },
                { code: 'a5', name: 'Tentativa A5' },
                { code: 'b', name: 'Lista B (Interferência)' },
                { code: 'a6', name: 'A6 (Intervalo)' },
                { code: 'a7', name: 'A7 (30 min)' },
              ].map((item) => {
                const score = rawPayload[item.code] || 0
                return (
                  <div key={item.code} className="rounded-2xl border border-black/10 bg-white p-4">
                    <div className="text-sm text-zinc-500">{item.name}</div>
                    <div className="mt-1 text-2xl font-semibold text-zinc-900">{score}</div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Summary */}
          <div className="mb-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Análise do Desempenho</h3>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div className="rounded-2xl border border-black/10 bg-white p-4">
                <div className="text-sm text-zinc-500">Aprendizado Total (A1-A5)</div>
                <div className="mt-1 text-2xl font-semibold text-zinc-900">
                  {results.aprendizado_total || (rawPayload.a1 + rawPayload.a2 + rawPayload.a3 + rawPayload.a4 + rawPayload.a5) || '-'}
                </div>
              </div>
              <div className="rounded-2xl border border-black/10 bg-white p-4">
                <div className="text-sm text-zinc-500">Efeito de Interferência (A5 - B)</div>
                <div className="mt-1 text-2xl font-semibold text-zinc-900">
                  {results.efeito_interferencia || (rawPayload.a5 - rawPayload.b) || '-'}
                </div>
              </div>
              <div className="rounded-2xl border border-black/10 bg-white p-4">
                <div className="text-sm text-zinc-500">Evocação Prolongada (A7 - A6)</div>
                <div className="mt-1 text-2xl font-semibold text-zinc-900">
                  {results.evocacao_prolongada || (rawPayload.a7 - rawPayload.a6) || '-'}
                </div>
              </div>
            </div>
          </div>

          {/* Interpretation */}
          {result.interpretation && (
            <div className="mb-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Interpretação</h3>
              <div className="whitespace-pre-wrap text-sm text-zinc-700">
                {result.interpretation}
              </div>
            </div>
          )}

          {/* Back Button */}
          <div className="flex justify-start">
            <Link
              href={`/dashboard/evaluations/${result.evaluation_id}`}
              className="rounded-full border border-black/10 bg-white px-6 py-3 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50"
            >
              Voltar para Avaliação
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}