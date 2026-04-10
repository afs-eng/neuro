import { api } from '@/lib/api'

export const documentService = {
  list: (evaluationId?: number) => 
    api.get<any[]>(evaluationId ? `/api/documents/?evaluation_id=${evaluationId}` : '/api/documents/'),
    
  upload: (data: FormData) => 
    api.post<any>('/api/documents/upload/', data),
    
  delete: (documentId: number | string) => 
    api.delete(`/api/documents/${documentId}`),
}
