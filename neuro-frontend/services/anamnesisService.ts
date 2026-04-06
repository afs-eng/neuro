import { api } from '@/lib/api'

export const anamnesisService = {
  // Templates
  getTemplates: () => api.get<any[]>('/api/anamnesis/templates/'),

  // Invites
  getInvites: (evaluationId?: number) => 
    api.get<any[]>(evaluationId ? `/api/anamnesis/invites/?evaluation_id=${evaluationId}` : '/api/anamnesis/invites/'),
    
  createInvite: (data: any) => api.post<any>('/api/anamnesis/invites/', data),
  
  sendEmail: (inviteId: number | string) => api.post<any>(`/api/anamnesis/invites/${inviteId}/send-email`, {}),
  
  sendWhatsapp: (inviteId: number | string) => api.post<any>(`/api/anamnesis/invites/${inviteId}/send-whatsapp`, {}),
  
  resendInvite: (inviteId: number | string) => api.post<any>(`/api/anamnesis/invites/${inviteId}/resend`, {}),
  
  cancelInvite: (inviteId: number | string) => api.post<any>(`/api/anamnesis/invites/${inviteId}/cancel`, {}),

  // Responses
  getResponses: (evaluationId?: number) => 
    api.get<any[]>(evaluationId ? `/api/anamnesis/responses/?evaluation_id=${evaluationId}` : '/api/anamnesis/responses/'),
    
  reviewResponse: (responseId: number | string) => 
    api.patch<any>(`/api/anamnesis/responses/${responseId}/review`, { status: "reviewed" }),
}
