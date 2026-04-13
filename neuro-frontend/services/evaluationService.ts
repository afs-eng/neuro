import { api } from '@/lib/api'
import type { Evaluation, ProgressEntry } from '@/types/shared'

export const evaluationService = {
  list: () => api.get<Evaluation[]>('/api/evaluations'),

  get: (id: number | string) => api.get<Evaluation>(`/api/evaluations/${id}`),

  create: (data: Partial<Evaluation>) => api.post<Evaluation>('/api/evaluations', data),

  update: (id: number | string, data: Partial<Evaluation>) => api.put<Evaluation>(`/api/evaluations/${id}`, data),

  delete: (id: number | string) => api.delete(`/api/evaluations/${id}`),

  // Progress Entries
  getProgressEntries: (id: number | string) => api.get<ProgressEntry[]>(`/api/evaluations/${id}/progress-entries`),
  createProgressEntry: (data: Record<string, unknown>) => api.post<ProgressEntry>('/api/evaluations/progress-entries', data),
  deleteProgressEntry: (entryId: number | string) => api.delete(`/api/evaluations/progress-entries/${entryId}`),
}
