'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

const FACTOR_NAMES: Record<string, string> = {
  D: "Fator 1 - Desatenção (D)",
  I: "Fator 2 - Impulsividade (I)",
  AE: "Fator 3 - Aspectos Emocionais (AE)",
  AAMA: "Fator 4 - Autorregulação da Atenção, Motivação e Ação (AAMA)",
  H: "Fator 5 - Hiperatividade (H)",
}

export default function ETDAHADResultPage() {
  const params = useParams()
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const { api } = await import('@/lib/api')
        const data = await api.get<any>(`/api/tests/etdah-ad/result/${params.id}`)
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

  const raw = result.raw_payload || {}
  const classified = result.classified_payload || {}

  const rawScores = result.raw_scores || {}
  const results = result.results || {}

  const itemKeys = Object.keys(raw).filter(k => k.startsWith('item_'))
  const items: { number: number, value: any }[] = []
  
  if (raw.responses) {
    Object.keys(raw.responses).forEach(key => {
      items.push({ number: parseInt(key), value: raw.responses[key] })
    })
  } else {
    itemKeys.forEach(key => {
      items.push({ number: parseInt(key.replace('item_', '')), value: raw[key] })
    })
  }
  items.sort((a, b) => a.number - b.number)

  const factorOrder = ["D", "I", "AE", "AAMA", "H"]

  return (
    <div className="min-h-screen bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                Florescer
              </div>
            </div>
            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard?tab=tests" className="rounded-full px-4 py-2 hover:bg-black/5">Testes</Link>
            </nav>
          </header>

          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">ETDAH-AD - Resultado</h1>
              <p className="mt-1 text-sm text-zinc-600">
                {result.patient_name} • Aplicado em {result.applied_on}
              </p>
            </div>
            <div className="flex gap-3">
              <Link href={`/dashboard/tests/etdah-ad?evaluation_id=${result.evaluation_id}&application_id=${params.id}&edit=true`} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50">
                Editar
              </Link>
              <button className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm">
                Exportar PDF
              </button>
              <Link href="/dashboard?tab=tests" className="rounded-full bg-zinc-900 px-4 py-2 text-sm font-medium text-white shadow-lg">
                Voltar
              </Link>
            </div>
          </div>

          <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5 mb-6">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Escores por Fator</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dashed border-black/10">
                    <th className="pb-3 text-left text-xs font-semibold text-zinc-500 uppercase">Fator</th>
                    <th className="pb-3 text-center text-xs font-semibold text-zinc-500 uppercase">Escore Bruto</th>
                    <th className="pb-3 text-center text-xs font-semibold text-zinc-500 uppercase">Média</th>
                    <th className="pb-3 text-center text-xs font-semibold text-zinc-500 uppercase">Percentil</th>
                    <th className="pb-3 text-left text-xs font-semibold text-zinc-500 uppercase">Classificação</th>
                  </tr>
                </thead>
                <tbody>
                  {factorOrder.map((factor) => {
                    const r = results[factor] || {}
                    return (
                      <tr key={factor} className="border-b border-dashed border-black/5">
                        <td className="py-3 text-zinc-900 font-medium">{FACTOR_NAMES[factor]}</td>
                        <td className="py-3 text-center font-medium text-zinc-900">{r.raw_score ?? rawScores[factor] ?? '—'}</td>
                        <td className="py-3 text-center text-zinc-600">{r.mean ?? '—'}</td>
                        <td className="py-3 text-center text-zinc-600">{r.percentile_text ?? '—'}</td>
                        <td className="py-3 text-zinc-600">{r.classification ?? '—'}</td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>

          <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5 mb-6">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Itens (69 itens)</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dashed border-black/10">
                    <th className="pb-3 text-left text-xs font-semibold text-zinc-500 uppercase">Item</th>
                    <th className="pb-3 text-center text-xs font-semibold text-zinc-500 uppercase">Valor</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.number} className="border-b border-dashed border-black/5">
                      <td className="py-2 text-zinc-900">Item {item.number}</td>
                      <td className="py-2 text-center font-medium text-zinc-900">{item.value}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {results && Object.keys(results).length > 0 && (
            <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Interpretação</h3>
              
              <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-4">
                <p className="text-sm text-amber-800">
                  <strong>Escolaridade:</strong> {(() => {
                    const sc = result.computed_payload?.schooling || result.classified_payload?.schooling
                    const labels: Record<string, string> = {
                      "preschool": "Ensino Pré-escolar",
                      "elementary": "Ensino Fundamental",
                      "middle": "Ensino Médio",
                      "higher": "Ensino Superior",
                      "higher_incomplete": "Ensino Superior Incompleto",
                    }
                    return labels[sc] || sc || 'Não informada'
                  })()}
                </p>
              </div>

              <div className="space-y-4">
                {factorOrder.map((factor) => {
                  const r = results[factor] || {}
                  const classification = r.classification || ''
                  const bgClass = classification.includes('Superior') ? 'bg-emerald-50 border-emerald-200' 
                    : classification.includes('Média') || classification.includes('Médio') ? 'bg-blue-50 border-blue-200'
                    : 'bg-red-50 border-red-200'
                  
                  return (
                    <div key={factor} className={`rounded-xl p-4 border ${bgClass}`}>
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-zinc-900">{FACTOR_NAMES[factor]}</h4>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                          classification.includes('Superior') ? 'bg-emerald-100 text-emerald-700'
                          : classification.includes('Média') || classification.includes('Médio') ? 'bg-blue-100 text-blue-700'
                          : 'bg-red-100 text-red-700'
                        }`}>
                          {classification}
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="text-zinc-500">Escore Bruto:</span>
                          <span className="ml-2 font-medium text-zinc-900">{r.raw_score ?? '—'}</span>
                        </div>
                        <div>
                          <span className="text-zinc-500">Média:</span>
                          <span className="ml-2 font-medium text-zinc-900">{r.mean ?? '—'}</span>
                        </div>
                        <div>
                          <span className="text-zinc-500">Percentil:</span>
                          <span className="ml-2 font-medium text-zinc-900">{r.percentile_text ?? '—'}</span>
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
