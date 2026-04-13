import { api } from '@/lib/api'
import type { WISC4Result } from '@/types/tests/wisc4'

interface WISC4CalculatePayload {
  patient_id: number
  confidence_level: string
  scores: Record<string, number>
}

export const wisc4Service = {
  calculate: (data: WISC4CalculatePayload) =>
    api.post<WISC4Result>('/api/tests/wisc4/calculate', data),

  getResult: (id: number) =>
    api.get<WISC4Result>(`/api/tests/wisc4/result/${id}`),

  getSubtests: () =>
    api.get<{ code: string; name: string; max_score: number }[]>('/api/tests/wisc4/subtests'),
}