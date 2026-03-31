'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'

export default function EBADEPIJResultPage() {
  const params = useParams()
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const { api } = await import('@/lib/api')
        const data = await api.get<any>(`/api/tests/applications/${params.id}`)
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

  const itemKeys = Object.keys(raw).filter(k => k.startsWith('item_'))
  const items = itemKeys.map(key => ({
    number: parseInt(key.replace('item_', '')),
    value: raw[key]
  })).sort((a, b) => a.number - b.number)

  const getScoreLabel = (value: number) => {
    if (value === 0) return 'Nunca'
    if (value === 1) return 'Às vezes'
    if (value === 2) return 'Frequentemente'
    if (value === 3) return 'Sempre'
    return '—'
  }

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
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">EBADEP-IJ - Resultado</h1>
              <p className="mt-1 text-sm text-zinc-600">
                {result.patient_name} • Aplicado em {result.applied_on}
              </p>
            </div>
            <div className="flex gap-3">
              <Link href={`/dashboard/tests/ebadep-ij?evaluation_id=${result.evaluation_id}&application_id=${params.id}&edit=true`} className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-zinc-700 shadow-sm hover:bg-zinc-50">
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

          <div className="rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
            <h3 className="mb-4 text-lg font-semibold text-zinc-900">Itens (27 itens)</h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-dashed border-black/10">
                    <th className="pb-3 text-left text-xs font-semibold text-zinc-500 uppercase">Item</th>
                    <th className="pb-3 text-center text-xs font-semibold text-zinc-500 uppercase">Valor</th>
                    <th className="pb-3 text-left text-xs font-semibold text-zinc-500 uppercase">Classificação</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((item) => (
                    <tr key={item.number} className="border-b border-dashed border-black/5">
                      <td className="py-2 text-zinc-900">Item {item.number}</td>
                      <td className="py-2 text-center font-medium text-zinc-900">{item.value}</td>
                      <td className="py-2 text-zinc-600">{getScoreLabel(item.value)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {result.interpretation_text && (
            <div className="mt-6 rounded-[28px] bg-white/70 p-5 shadow-lg ring-1 ring-black/5">
              <h3 className="mb-4 text-lg font-semibold text-zinc-900">Interpretação</h3>
              <div className="whitespace-pre-wrap text-sm text-zinc-700">
                {result.interpretation_text}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}