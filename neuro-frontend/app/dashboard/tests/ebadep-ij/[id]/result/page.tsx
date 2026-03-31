'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { ArrowLeft, Download, Edit, LayoutDashboard, Printer } from 'lucide-react'

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'

const ITEM_LABELS: Record<number, string> = {
  1: 'Humor deprimido',
  2: 'Perda ou diminuição de prazer',
  3: 'Choro',
  4: 'Desesperança',
  5: 'Desamparo',
  6: 'Indecisão',
  7: 'Sentimento de incapacidade',
  8: 'Sentimentos de inadequação',
  9: 'Inutilidade',
  10: 'Carência/dependência',
  11: 'Negativismo',
  12: 'Esquiva de situações sociais',
  13: 'Queda de rendimento na escola',
  14: 'Autocrítica exacerbada',
  15: 'Culpa',
  16: 'Diminuição de concentração',
  17: 'Pensamento de morte',
  18: 'Autoestima rebaixada',
  19: 'Falta de perspectiva sobre o presente',
  20: 'Falta de perspectiva sobre o futuro',
  21: 'Alteração de apetite',
  22: 'Alteração de peso',
  23: 'Insônia ou hipersonia',
  24: 'Lentidão ou agitação psicomotora',
  25: 'Fadiga ou perda de energia',
  26: 'Sintomas físicos',
  27: 'Irritação',
}

const CLASSIFICATION_STYLES: Record<string, string> = {
  Mínimo: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Leve: 'bg-blue-50 text-blue-700 border-blue-200',
  Moderado: 'bg-amber-50 text-amber-700 border-amber-200',
  Grave: 'bg-red-50 text-red-700 border-red-200',
  Severo: 'bg-rose-50 text-rose-700 border-rose-200',
}

function getClassificationStyle(classificacao: string) {
  return CLASSIFICATION_STYLES[classificacao] || 'bg-slate-100 text-slate-700 border-slate-200'
}

function getScoreLabel(value: number) {
  if (value === 0) return 'Nunca/Poucas vezes'
  if (value === 1) return 'Algumas vezes'
  if (value === 2) return 'Muitas vezes/Sempre'
  return '—'
}

export default function EBADEPIJResultPage() {
  const params = useParams()
  const router = useRouter()
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
    if (params.id) fetchResult()
  }, [params.id])

  if (loading) {
    return <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center"><div className="text-zinc-600">Carregando...</div></div>
  }

  if (!result) {
    return <div className="min-h-screen bg-slate-300 p-6 md:p-10 flex items-center justify-center"><div className="text-zinc-600">Resultado não encontrado</div></div>
  }

  const classified = result.classified_payload || {}
  const protocol = classified.result || {}
  const detailItems = protocol.detalhe_itens || []
  const norms = classified.normas || protocol.normas || {}
  const criticalItems = classified.items_criticos || []
  const responseRows = []

  for (let i = 0; i < 7; i++) {
    responseRows.push([i + 1, i + 8, i + 15, i + 22].filter((item) => item <= 27))
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">EBADEP-IJ - Resultado</h2>
            <p className="text-sm text-slate-500">Escala Baptista de Depressão - Infantojuvenil</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="rounded-xl gap-2" onClick={() => router.push('/dashboard')}>
            <LayoutDashboard className="h-4 w-4" />
            Dashboard
          </Button>
          <Button variant="outline" className="rounded-xl gap-2" onClick={() => router.push(`/dashboard/tests/ebadep-ij?evaluation_id=${result.evaluation_id}&application_id=${params.id}&edit=true`)}>
            <Edit className="h-4 w-4" />
            Editar
          </Button>
          <Button variant="outline" className="rounded-xl gap-2">
            <Printer className="h-4 w-4" />
            Imprimir
          </Button>
          <Button className="rounded-xl gap-2">
            <Download className="h-4 w-4" />
            Exportar PDF
          </Button>
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-8">
        <div className="text-center border-b pb-6">
          <h1 className="text-2xl font-bold text-slate-900">EBADEP-IJ</h1>
          <p className="text-lg text-slate-600">Escala Baptista de Depressão - Infantojuvenil</p>
          <p className="text-sm text-slate-500 mt-1">Relatório estruturado do protocolo</p>
        </div>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">DADOS DA APLICAÇÃO</h2>
          <div className="border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <tbody>
                <tr className="border-b"><td className="py-3 px-4 font-medium text-slate-700 w-1/3">Paciente</td><td className="py-3 px-4 text-slate-900">{result.patient_name}</td></tr>
                <tr className="border-b"><td className="py-3 px-4 font-medium text-slate-700">Aplicação</td><td className="py-3 px-4 text-slate-900">{result.applied_on || '—'}</td></tr>
                <tr className="border-b"><td className="py-3 px-4 font-medium text-slate-700">Total de itens</td><td className="py-3 px-4 text-slate-900">27</td></tr>
                <tr><td className="py-3 px-4 font-medium text-slate-700">Itens críticos</td><td className="py-3 px-4 text-slate-900">{criticalItems.length}</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">SÍNTESE DOS RESULTADOS</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="rounded-xl border border-slate-200 p-5 bg-slate-50">
              <p className="text-sm text-slate-500">Pontuação total</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{classified.pontuacao_total ?? '—'}</p>
            </div>
            <div className="rounded-xl border border-slate-200 p-5 bg-slate-50">
              <p className="text-sm text-slate-500">Classificação</p>
              <div className="mt-3"><Badge className={getClassificationStyle(classified.classificacao || '')}>{classified.classificacao || '—'}</Badge></div>
            </div>
            <div className="rounded-xl border border-slate-200 p-5 bg-slate-50">
              <p className="text-sm text-slate-500">Síntese</p>
              <p className="mt-2 text-sm font-medium text-slate-900">{classified.sintese || '—'}</p>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">NORMAS</h2>
          <div className="border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <tbody>
                <tr className="border-b"><td className="py-3 px-4 font-medium text-slate-700 w-1/3">Percentil</td><td className="py-3 px-4 text-slate-900">{norms.percentil ?? '—'}</td></tr>
                <tr className="border-b"><td className="py-3 px-4 font-medium text-slate-700">T</td><td className="py-3 px-4 text-slate-900">{norms.T ?? '—'}</td></tr>
                <tr><td className="py-3 px-4 font-medium text-slate-700">Estanino</td><td className="py-3 px-4 text-slate-900">{norms.estanino ?? '—'}</td></tr>
              </tbody>
            </table>
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">PONTUAÇÕES DO PROTOCOLO</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="border rounded-xl p-4">
              <h3 className="font-semibold text-slate-900 mb-2">Itens negativos</h3>
              <p className="text-3xl font-semibold text-slate-900">{protocol.soma_itens_negativos ?? '—'}</p>
            </div>
            <div className="border rounded-xl p-4">
              <h3 className="font-semibold text-slate-900 mb-2">Itens positivos</h3>
              <p className="text-3xl font-semibold text-slate-900">{protocol.soma_itens_positivos ?? '—'}</p>
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">ITENS CRÍTICOS</h2>
          {criticalItems.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {criticalItems.map((item: any) => (
                <Badge key={item.item} className="bg-red-50 text-red-700 border-red-200">Item {item.item}</Badge>
              ))}
            </div>
          ) : (
            <div className="border rounded-xl p-4 text-sm text-slate-600">Nenhum item crítico identificado.</div>
          )}
        </section>

        <section>
          <h2 className="text-lg font-semibold text-slate-900 mb-4">REGISTRO DE RESPOSTAS</h2>
          <p className="text-sm text-slate-600 mb-4">Legenda: 0 = Nunca/Poucas vezes | 1 = Algumas vezes | 2 = Muitas vezes/Sempre</p>
          <div className="border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-slate-100">
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-12">Item</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-16">Resp.</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-12">Item</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-16">Resp.</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-12">Item</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-16">Resp.</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-12">Item</th>
                  <th className="py-2 px-2 text-center font-medium text-slate-700 w-16">Resp.</th>
                </tr>
              </thead>
              <tbody>
                {responseRows.map((row, idx) => (
                  <tr key={idx} className={`border-t ${idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50'}`}>
                    {row.map((itemNumber) => {
                      const item = detailItems.find((entry: any) => entry.item === itemNumber)
                      return (
                        <>
                          <td className="py-1 px-2 text-center text-slate-700 font-medium">{String(itemNumber).padStart(2, '0')}</td>
                          <td className="py-1 px-2 text-center">
                            <span className={`inline-block w-8 h-6 leading-6 rounded font-bold ${item?.resposta === 2 ? 'bg-red-100 text-red-800' : item?.resposta === 1 ? 'bg-amber-100 text-amber-800' : item?.resposta === 0 ? 'bg-slate-200 text-slate-700' : 'bg-slate-100 text-slate-400'}`}>
                              {item?.resposta ?? '-'}
                            </span>
                          </td>
                        </>
                      )
                    })}
                    {Array.from({ length: 4 - row.length }).map((_, emptyIdx) => (
                      <>
                        <td key={`empty-item-${idx}-${emptyIdx}`} className="py-1 px-2" />
                        <td key={`empty-resp-${idx}-${emptyIdx}`} className="py-1 px-2" />
                      </>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {result.interpretation_text && (
          <section>
            <h2 className="text-lg font-semibold text-slate-900 mb-4">INTERPRETAÇÃO</h2>
            <div className="border rounded-xl p-4 whitespace-pre-wrap text-sm text-slate-600 leading-relaxed">
              {result.interpretation_text}
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
