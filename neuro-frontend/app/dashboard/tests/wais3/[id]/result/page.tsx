'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

interface IndexData {
  nome: string
  soma_ponderada?: number | null
  pontuacao_composta?: number | null
  percentil?: number | null
  classificacao?: string | null
}

interface SubtestData {
  nome: string
  pontos_brutos?: number | null
  escore_ponderado?: number | null
  classificacao?: string | null
}

interface ResultData {
  id: number
  evaluation_id: number
  patient_name: string
  applied_on?: string
  classified_payload?: {
    indices?: Record<string, IndexData>
    subtestes?: Record<string, SubtestData>
  }
  interpretation_text?: string
}

export default function WAIS3ResultPage() {
  const params = useParams()
  const [result, setResult] = useState<ResultData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const { api } = await import('@/lib/api')
        const data = await api.get<ResultData>(`/api/tests/applications/${params.id}`)
        if (!data) {
          setError('Resultado não encontrado')
        } else {
          setResult(data)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erro ao carregar resultado')
      } finally {
        setLoading(false)
      }
    }
    if (params.id) fetchResult()
  }, [params.id])

  if (loading) return <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center"><div className="text-zinc-600">Carregando...</div></div>
  if (error || !result) return <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center"><div className="text-red-600">{error || 'Resultado não encontrado'}</div></div>

  const classified = result.classified_payload || {}
  const indices = classified.indices || {}
  const subtests = classified.subtestes || {}

  return (
    <div className="min-h-screen bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">NeuroAvalia</div>
            <div className="flex gap-3">
              <Link href={`/dashboard/tests/wais3?evaluation_id=${result.evaluation_id}&application_id=${params.id}&edit=true`} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50">Editar</Link>
              <Link href={`/dashboard/evaluations/${result.evaluation_id}?tab=overview`} className="rounded-full bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-lg">Voltar</Link>
            </div>
          </header>

          <div className="mb-6">
            <h1 className="text-3xl font-medium tracking-tight text-zinc-900">WAIS-III - Resultado</h1>
            <p className="mt-1 text-sm text-zinc-600">{result.patient_name}</p>
            {result.applied_on && <p className="mt-1 text-xs text-zinc-500">Avaliado em: {new Date(result.applied_on).toLocaleDateString('pt-BR')}</p>}
          </div>

          {/* Índices Principais */}
          {Object.keys(indices).length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-6">
              <div className="px-5 py-4 border-b border-slate-200"><h3 className="font-semibold text-slate-900">Índices Fatoriais e QI</h3></div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead><tr className="bg-slate-50"><th className="text-left px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Índice</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Soma Ponderada</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Escore Composto</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Percentil</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Classificação</th></tr></thead>
                  <tbody className="divide-y divide-slate-200">
                    {Object.entries(indices).map(([key, item]) => (
                      <tr key={key} className="hover:bg-slate-50">
                        <td className="px-5 py-3 text-sm font-medium text-slate-900">{item.nome || key}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700 font-semibold">{item.soma_ponderada ?? '—'}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700 font-semibold">{item.pontuacao_composta ?? '—'}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700">{item.percentil ?? '—'}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700">{item.classificacao ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Subtestes */}
          {Object.keys(subtests).length > 0 && (
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-6">
              <div className="px-5 py-4 border-b border-slate-200"><h3 className="font-semibold text-slate-900">Subtestes</h3></div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead><tr className="bg-slate-50"><th className="text-left px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Subteste</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Bruto</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Ponderado</th><th className="text-center px-5 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wide">Classificação</th></tr></thead>
                  <tbody className="divide-y divide-slate-200">
                    {Object.entries(subtests).map(([key, item]) => (
                      <tr key={key} className="hover:bg-slate-50">
                        <td className="px-5 py-3 text-sm text-slate-700">{item.nome || key}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700 font-semibold">{item.pontos_brutos ?? '—'}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700 font-semibold">{item.escore_ponderado ?? '—'}</td>
                        <td className="px-5 py-3 text-sm text-center text-slate-700">{item.classificacao ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Interpretação */}
          {result.interpretation_text && (
            <div className="bg-white rounded-xl border border-slate-200 p-5">
              <h3 className="font-semibold text-slate-900 mb-3">Interpretação</h3>
              <p className="text-sm leading-7 text-slate-700 whitespace-pre-wrap">{result.interpretation_text}</p>
            </div>
          )}

          {/* Sem dados */}
          {Object.keys(indices).length === 0 && Object.keys(subtests).length === 0 && !result.interpretation_text && (
            <div className="bg-yellow-50 rounded-xl border border-yellow-200 p-5">
              <p className="text-sm text-yellow-800">Nenhum resultado disponível para exibir. Verifique se o teste foi processado corretamente.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
