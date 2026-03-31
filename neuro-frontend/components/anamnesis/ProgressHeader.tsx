import { AnamnesisStep } from "./types"

export function ProgressHeader({ steps, currentStep }: { steps: AnamnesisStep[]; currentStep: number }) {
  const progress = steps.length ? Math.round(((currentStep + 1) / steps.length) * 100) : 0

  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <div className="text-sm font-medium text-slate-900">Etapa {currentStep + 1} de {steps.length}</div>
          <div className="text-xs text-slate-500">Progresso do preenchimento</div>
        </div>
        <div className="text-sm font-semibold text-slate-700">{progress}%</div>
      </div>
      <div className="mt-3 h-2 rounded-full bg-slate-200">
        <div className="h-2 rounded-full bg-slate-900" style={{ width: `${progress}%` }} />
      </div>
    </div>
  )
}
