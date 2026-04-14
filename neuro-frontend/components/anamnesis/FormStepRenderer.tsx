import { FieldRenderer } from "./FieldRenderer"
import { AnamnesisStep } from "./types"

export function isVisible(field: any, answers: Record<string, any>) {
  if (!field.conditional) return true
  return answers[field.conditional.field] === field.conditional.equals
}

export function FormStepRenderer({ step, answers, onChange, invalidFieldIds = [] }: { step: AnamnesisStep; answers: Record<string, any>; onChange: (fieldId: string, value: any) => void; invalidFieldIds?: string[] }) {
  return (
    <div className="space-y-5">
      <div>
        <h2 className="text-xl font-semibold text-slate-900">{step.title}</h2>
        {step.description && <p className="mt-1 text-sm text-slate-500">{step.description}</p>}
      </div>
      <div className="grid grid-cols-1 gap-5 md:grid-cols-2">
        {step.fields.filter((field) => isVisible(field, answers)).map((field) => {
          const isInvalid = invalidFieldIds.includes(field.id)

          return (
            <div
              key={field.id}
              id={`anamnesis-field-${field.id}`}
              className={`space-y-2 rounded-2xl p-3 transition-colors ${field.type === "textarea" || field.type === "repeater" ? "md:col-span-2" : ""} ${isInvalid ? "border border-rose-300 bg-rose-50" : "border border-transparent"}`}
            >
              <label className={`text-sm font-medium ${isInvalid ? "text-rose-700" : "text-slate-800"}`}>{field.label}{field.required ? " *" : ""}</label>
              <FieldRenderer field={field} value={answers[field.id]} onChange={(value) => onChange(field.id, value)} invalid={isInvalid} inputId={`anamnesis-input-${field.id}`} />
              {field.help_text && <p className={`text-xs ${isInvalid ? "text-rose-600" : "text-slate-500"}`}>{field.help_text}</p>}
            </div>
          )
        })}
      </div>
    </div>
  )
}
