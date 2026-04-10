import { api } from '@/lib/api'

export const reportService = {
  list: (evaluationId?: number) =>
    api.get<any[]>(evaluationId ? `/api/reports/?evaluation_id=${evaluationId}` : '/api/reports/'),

  getByEvaluation: (evaluationId: number | string) =>
    api.get<any[]>(`/api/reports/by-evaluation/${evaluationId}`),

  get: (reportId: number | string) =>
    api.get<any>(`/api/reports/${reportId}/`),

  create: (data: any) =>
    api.post<any>('/api/reports/', data),

  generateFromEvaluation: (evaluationId: number | string) =>
    api.post<any>(`/api/reports/generate-from-evaluation/${evaluationId}`, {}),

  regenerateReport: (reportId: number | string) =>
    api.post<any>(`/api/reports/${reportId}/regenerate`, {}),

  build: (reportId: number | string) =>
    api.post<any>(`/api/reports/${reportId}/build`, {}),

  regenerateSection: (reportId: number | string, sectionKey: string) =>
    api.post<any>(`/api/reports/${reportId}/regenerate-section/${sectionKey}`, {}),

  saveSection: (sectionId: number | string, editedText: string) =>
    api.patch<any>(`/api/reports/sections/${sectionId}`, { edited_text: editedText }),

  finalize: (reportId: number | string) =>
    api.post<any>(`/api/reports/${reportId}/finalize`, {}),

  exportHtml: (reportId: number | string) =>
    api.post<{ html: string }>(`/api/reports/${reportId}/export-html`, {}),
}
