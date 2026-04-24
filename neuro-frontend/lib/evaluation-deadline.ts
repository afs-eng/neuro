const FINISHED_STATUSES = new Set(["approved", "archived"])

export interface EvaluationDeadlineMeta {
  label: string
  helperText: string
  badgeClassName: string
  sortOrder: number
  timestamp: number
  isOverdue: boolean
}

function parseDateValue(value: string | null | undefined): Date | null {
  if (!value) return null

  const [year, month, day] = value.split("-").map(Number)

  if (!year || !month || !day) {
    return null
  }

  const date = new Date(year, month - 1, day)
  return Number.isNaN(date.getTime()) ? null : date
}

function formatDate(value: string | null | undefined): string {
  const date = parseDateValue(value)

  if (!date) return "sem data"

  return date.toLocaleDateString("pt-BR")
}

function getToday(): Date {
  const now = new Date()
  return new Date(now.getFullYear(), now.getMonth(), now.getDate())
}

function getDaysUntil(date: Date): number {
  const today = getToday()
  const diff = date.getTime() - today.getTime()
  return Math.round(diff / 86400000)
}

export function getEvaluationDeadlineMeta(endDate: string | null | undefined, status?: string | null): EvaluationDeadlineMeta {
  const deadline = parseDateValue(endDate)

  if (!deadline) {
    return {
      label: "Sem prazo",
      helperText: "Defina uma previsao de entrega para entrar na agenda.",
      badgeClassName: "border-slate-200 bg-slate-50 text-slate-500",
      sortOrder: 4,
      timestamp: Number.MAX_SAFE_INTEGER,
      isOverdue: false,
    }
  }

  if (status && FINISHED_STATUSES.has(status)) {
    return {
      label: "Finalizada",
      helperText: `Prazo registrado para ${formatDate(endDate)}.`,
      badgeClassName: "border-emerald-200 bg-emerald-50 text-emerald-700",
      sortOrder: 3,
      timestamp: deadline.getTime(),
      isOverdue: false,
    }
  }

  const daysUntil = getDaysUntil(deadline)

  if (daysUntil < 0) {
    const daysLate = Math.abs(daysUntil)

    return {
      label: daysLate === 1 ? "Atrasada ha 1 dia" : `Atrasada ha ${daysLate} dias`,
      helperText: `Entrega prevista para ${formatDate(endDate)}.`,
      badgeClassName: "border-rose-200 bg-rose-50 text-rose-700",
      sortOrder: 0,
      timestamp: deadline.getTime(),
      isOverdue: true,
    }
  }

  if (daysUntil === 0) {
    return {
      label: "Vence hoje",
      helperText: "Priorize esta avaliacao na agenda de hoje.",
      badgeClassName: "border-amber-200 bg-amber-50 text-amber-700",
      sortOrder: 1,
      timestamp: deadline.getTime(),
      isOverdue: false,
    }
  }

  if (daysUntil <= 7) {
    return {
      label: daysUntil === 1 ? "Vence em 1 dia" : `Vence em ${daysUntil} dias`,
      helperText: `Entrega prevista para ${formatDate(endDate)}.`,
      badgeClassName: "border-blue-200 bg-blue-50 text-blue-700",
      sortOrder: 2,
      timestamp: deadline.getTime(),
      isOverdue: false,
    }
  }

  return {
    label: `Prazo ${formatDate(endDate)}`,
    helperText: "Meta de prazo registrada para organizacao futura.",
    badgeClassName: "border-slate-200 bg-white text-slate-600",
    sortOrder: 2,
    timestamp: deadline.getTime(),
    isOverdue: false,
  }
}

export function compareEvaluationsByDeadline<T extends { end_date: string | null; status?: string | null; created_at?: string | null }>(
  first: T,
  second: T,
): number {
  const firstDeadline = getEvaluationDeadlineMeta(first.end_date, first.status)
  const secondDeadline = getEvaluationDeadlineMeta(second.end_date, second.status)

  if (firstDeadline.sortOrder !== secondDeadline.sortOrder) {
    return firstDeadline.sortOrder - secondDeadline.sortOrder
  }

  if (firstDeadline.timestamp !== secondDeadline.timestamp) {
    return firstDeadline.timestamp - secondDeadline.timestamp
  }

  const firstCreatedAt = first.created_at ? new Date(first.created_at).getTime() : 0
  const secondCreatedAt = second.created_at ? new Date(second.created_at).getTime() : 0

  return secondCreatedAt - firstCreatedAt
}
