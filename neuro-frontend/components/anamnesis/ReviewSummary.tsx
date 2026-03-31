import { AnamnesisStep } from "./types"

export function ReviewSummary({ steps, answers }: { steps: AnamnesisStep[]; answers: Record<string, any> }) {
  return (
    <div className="space-y-4">
      {steps.map((step) => (
        <div key={step.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
          <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-500">{step.title}</h3>
          <div className="mt-3 space-y-2">
            {step.fields.map((field) => {
              const value = answers[field.id]
              if (value === undefined || value === null || value === "" || (Array.isArray(value) && value.length === 0)) return null
              return (
                <div key={field.id} className="text-sm">
                  <span className="font-medium text-slate-900">{field.label}: </span>
                  <span className="text-slate-600 whitespace-pre-wrap">{typeof value === "object" ? JSON.stringify(value) : String(value)}</span>
                </div>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
