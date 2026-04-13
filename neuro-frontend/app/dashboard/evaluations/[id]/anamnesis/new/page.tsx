"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"

import { InternalAnamnesisEditor } from "@/components/anamnesis/InternalAnamnesisEditor"
import { api } from "@/lib/api"

export default function NewAnamnesisPage() {
  const params = useParams()
  const evaluationId = Number(params.id)
  const [templates, setTemplates] = useState<any[]>([])
  const [selectedTemplateId, setSelectedTemplateId] = useState<string>("")
  const [selectedTemplate, setSelectedTemplate] = useState<any | null>(null)
  const [evaluation, setEvaluation] = useState<any | null>(null)

  useEffect(() => {
    async function load() {
      const [templatesData, evaluationData] = await Promise.all([
        api.get<any[]>("/api/anamnesis/templates"),
        api.get<any>(`/api/evaluations/${evaluationId}`),
      ])
      const activeTemplates = (templatesData || []).filter(t => 
        t.schema_payload && 
        Array.isArray(t.schema_payload.steps) && 
        t.schema_payload.steps.length > 0
      )
      setTemplates(activeTemplates)
      setEvaluation(evaluationData)
    }
    load()
  }, [evaluationId])

  useEffect(() => {
    async function loadTemplate() {
      if (!selectedTemplateId) return
      const data = await api.get<any>(`/api/anamnesis/templates/${selectedTemplateId}`)
      setSelectedTemplate(data)
    }
    loadTemplate()
  }, [selectedTemplateId])

  return (
    <div className="space-y-6 p-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Nova anamnese</h1>
        <p className="text-sm text-slate-500">Escolha o modelo clínico adequado para iniciar o preenchimento.</p>
      </div>

      {!selectedTemplate ? (
        <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <label className="mb-2 block text-sm font-medium text-slate-700">Tipo de anamnese</label>
          <select value={selectedTemplateId} onChange={(e) => setSelectedTemplateId(e.target.value)} className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2">
            <option value="">Selecione...</option>
            {templates.map((template) => (
              <option key={template.id} value={template.id}>{template.name}</option>
            ))}
          </select>
        </div>
      ) : (
        <InternalAnamnesisEditor
          evaluationId={evaluationId}
          patientId={evaluation?.patient_id}
          templateId={selectedTemplate.id}
          schema={selectedTemplate.schema_payload}
          initialSubmittedByName={evaluation?.patient_name || ""}
          initialSubmittedByRelation={selectedTemplate.target_type === "adult" ? "proprio paciente" : "informante interno"}
        />
      )}
    </div>
  )
}
