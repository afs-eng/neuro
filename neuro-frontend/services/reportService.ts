import { api } from '@/lib/api'

export const reportService = {
  list: (evaluationId?: number) => 
    api.get<any[]>(evaluationId ? `/api/reports/?evaluation_id=${evaluationId}` : '/api/reports/'),
    
  get: (reportId: number | string) => 
    api.get<any>(`/api/reports/${reportId}/`),
    
  create: (data: any) => 
    api.post<any>('/api/reports/', data),
    
  build: (reportId: number | string) => 
    api.post<any>(`/api/reports/${reportId}/build`, {}),
    
  saveSection: (sectionId: number | string, editedText: string) => 
    api.patch<any>(`/api/reports/sections/${sectionId}`, { edited_text: editedText }),
}
