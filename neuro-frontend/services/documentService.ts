import { api } from '@/lib/api'
import type { EvaluationDocument } from '@/types/shared'

export const documentService = {
  list: (evaluationId?: number) =>
    api.get<EvaluationDocument[]>(evaluationId ? `/api/documents?evaluation_id=${evaluationId}` : '/api/documents'),

  upload: (data: FormData) =>
    api.post<EvaluationDocument>('/api/documents/upload', data),

  delete: (documentId: number | string) =>
    api.delete(`/api/documents/${documentId}`),
}
