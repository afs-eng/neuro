"use client"

import Link from "next/link"
import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

import { api } from "@/lib/api"

type ResponseItem = {
  id: number
  template_name: string
  response_type: string
  source: string
  status: string
  submitted_by_name: string
  updated_at: string
}

export default function EvaluationAnamnesisPage() {
  const params = useParams()
  const evaluationId = Number(params.id)
  const [responses, setResponses] = useState<ResponseItem[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const data = await api.get<ResponseItem[]>(`/api/anamnesis/responses/?evaluation_id=${evaluationId}`)
        setResponses(data)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [evaluationId])

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Anamnese</h1>
          <p className="text-sm text-slate-500">Respostas internas e externas vinculadas à avaliação.</p>
        </div>
        <Link href={`/dashboard/evaluations/${evaluationId}/anamnesis/new`} className="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white">Nova anamnese</Link>
      </div>

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        {loading ? (
          <div className="text-sm text-slate-500">Carregando...</div>
        ) : responses.length === 0 ? (
          <div className="text-sm text-slate-500">Nenhuma anamnese registrada ainda.</div>
        ) : (
          <div className="space-y-3">
            {responses.map((response) => (
              <Link key={response.id} href={`/dashboard/evaluations/${evaluationId}/anamnesis/${response.id}`} className="block rounded-2xl border border-slate-200 bg-slate-50 p-4 hover:bg-slate-100">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="font-medium text-slate-900">{response.template_name}</p>
                    <p className="text-sm text-slate-500">{response.source} • {response.submitted_by_name || "Sem informante"}</p>
                  </div>
                  <div className="text-sm text-slate-600">{response.status}</div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
