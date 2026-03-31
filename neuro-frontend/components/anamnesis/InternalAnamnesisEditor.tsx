"use client"

import { useMemo, useState } from "react"
import { useRouter } from "next/navigation"

import { FormStepRenderer } from "@/components/anamnesis/FormStepRenderer"
import { ProgressHeader } from "@/components/anamnesis/ProgressHeader"
import { ReviewSummary } from "@/components/anamnesis/ReviewSummary"
import { AnamnesisSchema, AnamnesisStep } from "@/components/anamnesis/types"
import { api } from "@/lib/api"

type Props = {
  evaluationId: number
  patientId: number
  responseId?: number
  templateId?: number
  schema: AnamnesisSchema
  initialAnswers?: Record<string, any>
  initialSubmittedByName?: string
  initialSubmittedByRelation?: string
}

export function InternalAnamnesisEditor({ evaluationId, patientId, responseId, templateId, schema, initialAnswers = {}, initialSubmittedByName = "", initialSubmittedByRelation = "" }: Props) {
  const router = useRouter()
  const steps = useMemo<AnamnesisStep[]>(() => schema.steps || [], [schema])
  const [currentStep, setCurrentStep] = useState(0)
  const [answers, setAnswers] = useState<Record<string, any>>({
    ...initialAnswers,
    submitted_by_name: initialAnswers.submitted_by_name || initialSubmittedByName,
    submitted_by_relation: initialAnswers.submitted_by_relation || initialSubmittedByRelation,
  })
  const [saving, setSaving] = useState(false)
  const [notice, setNotice] = useState<string | null>(null)

  const isReviewStep = currentStep === steps.length

  function updateField(fieldId: string, value: any) {
    setAnswers((prev) => ({ ...prev, [fieldId]: value }))
  }

  async function saveDraft() {
    setSaving(true)
    try {
      if (responseId) {
        await api.patch(`/api/anamnesis/responses/${responseId}`, {
          answers_payload: answers,
          submitted_by_name: answers.submitted_by_name || "",
          submitted_by_relation: answers.submitted_by_relation || "",
        })
      } else {
        const created = await api.post<{ id: number }>(`/api/anamnesis/responses/`, {
          evaluation_id: evaluationId,
          patient_id: patientId,
          template_id: templateId,
          answers_payload: answers,
          submitted_by_name: answers.submitted_by_name || "",
          submitted_by_relation: answers.submitted_by_relation || "",
        })
        router.replace(`/dashboard/evaluations/${evaluationId}/anamnesis/${created.id}`)
      }
      setNotice("Rascunho salvo com sucesso.")
    } catch (err: any) {
      setNotice(err?.message || "Erro ao salvar rascunho.")
    } finally {
      setSaving(false)
    }
  }

  async function submitResponse() {
    if (!responseId) {
      await saveDraft()
      return
    }
    setSaving(true)
    try {
      await api.post(`/api/anamnesis/responses/${responseId}/submit`, {
        answers_payload: answers,
        submitted_by_name: answers.submitted_by_name || "",
        submitted_by_relation: answers.submitted_by_relation || "",
      })
      setNotice("Anamnese enviada para revisão.")
      router.refresh()
    } catch (err: any) {
      setNotice(err?.message || "Erro ao enviar anamnese.")
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="space-y-6">
      <ProgressHeader steps={isReviewStep ? [...steps, { id: "review", title: "Revisão", fields: [] }] : steps} currentStep={currentStep} />

      {notice && <div className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700">{notice}</div>}

      <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
        {!isReviewStep && steps[currentStep] ? (
          <FormStepRenderer step={steps[currentStep]} answers={answers} onChange={updateField} />
        ) : (
          <div className="space-y-4">
            <div>
              <h2 className="text-xl font-semibold text-slate-900">Revisão final</h2>
              <p className="mt-1 text-sm text-slate-500">Confira os dados antes de concluir.</p>
            </div>
            <ReviewSummary steps={steps} answers={answers} />
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="flex gap-2">
          <button type="button" onClick={() => setCurrentStep((prev) => Math.max(prev - 1, 0))} disabled={currentStep === 0} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm disabled:opacity-50">Voltar</button>
          <button type="button" onClick={() => setCurrentStep((prev) => Math.min(prev + 1, steps.length))} disabled={isReviewStep} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm disabled:opacity-50">Avançar</button>
        </div>
        <div className="flex gap-2">
          <button type="button" onClick={saveDraft} disabled={saving} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm">{saving ? "Salvando..." : "Salvar rascunho"}</button>
          <button type="button" onClick={submitResponse} disabled={saving} className="rounded-xl bg-slate-900 px-4 py-2 text-sm text-white">Enviar</button>
        </div>
      </div>
    </div>
  )
}
