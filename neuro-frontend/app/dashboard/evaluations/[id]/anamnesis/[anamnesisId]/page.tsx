"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

import { InternalAnamnesisEditor } from "@/components/anamnesis/InternalAnamnesisEditor"
import { api } from "@/lib/api"

export default function EditAnamnesisPage() {
  const params = useParams()
  const evaluationId = Number(params.id)
  const anamnesisId = Number(params.anamnesisId)
  const [response, setResponse] = useState<any | null>(null)
  const [template, setTemplate] = useState<any | null>(null)

  useEffect(() => {
    async function load() {
      const responseData = await api.get<any>(`/api/anamnesis/responses/${anamnesisId}`)
      setResponse(responseData)
      const templateData = await api.get<any>(`/api/anamnesis/templates/${responseData.template_id}`)
      setTemplate(templateData)
    }
    load()
  }, [anamnesisId])

  if (!response || !template) {
    return <div className="p-6 text-sm text-slate-500">Carregando anamnese...</div>
  }

  const summary = response.summary_payload || {}

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">{template.name}</h1>
        <p className="text-sm text-slate-500">Edite, salve em rascunho ou envie para revisão.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div>
      <InternalAnamnesisEditor
        evaluationId={evaluationId}
        patientId={response.patient_id}
        responseId={response.id}
        schema={template.schema_payload}
        initialAnswers={response.answers_payload}
        initialSubmittedByName={response.submitted_by_name}
        initialSubmittedByRelation={response.submitted_by_relation}
      />
        </div>

        <aside className="space-y-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Resumo clínico</h2>
            <div className="mt-4 space-y-3 text-sm text-slate-600">
              {summary.chief_complaint && <div><span className="font-medium text-slate-900">Queixa principal:</span> {summary.chief_complaint}</div>}
              {summary.family_context_summary && <div><span className="font-medium text-slate-900">Contexto familiar:</span> {summary.family_context_summary}</div>}
              {summary.development_summary && <div><span className="font-medium text-slate-900">Desenvolvimento:</span> {summary.development_summary}</div>}
              {summary.medical_history_summary && <div><span className="font-medium text-slate-900">Histórico clínico:</span> {summary.medical_history_summary}</div>}
              {summary.school_history_summary && <div><span className="font-medium text-slate-900">Histórico escolar:</span> {summary.school_history_summary}</div>}
              {summary.sleep_eating_summary && <div><span className="font-medium text-slate-900">Sono e alimentação:</span> {summary.sleep_eating_summary}</div>}
              {summary.routine_summary && <div><span className="font-medium text-slate-900">Rotina:</span> {summary.routine_summary}</div>}
              {!summary.chief_complaint && !summary.family_context_summary && !summary.development_summary && !summary.medical_history_summary && !summary.school_history_summary && !summary.sleep_eating_summary && !summary.routine_summary && (
                <div>O resumo clínico será enriquecido conforme a anamnese for salva e revisada.</div>
              )}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">Pontos relevantes</h2>
            <div className="mt-4 space-y-2 text-sm text-slate-600">
              {(summary.clinically_relevant_points || []).length > 0 ? (
                (summary.clinically_relevant_points || []).map((item: string, index: number) => (
                  <div key={index}>- {item}</div>
                ))
              ) : (
                <div>Nenhum ponto relevante identificado ainda.</div>
              )}
            </div>
            {(summary.risk_flags || []).length > 0 && (
              <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-3 text-sm text-amber-800">
                Alertas: {(summary.risk_flags || []).join(", ")}
              </div>
            )}
          </div>
        </aside>
      </div>
    </div>
  )
}
