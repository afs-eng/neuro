import { api } from '@/lib/api'
import type { AnamnesisTemplate, AnamnesisInvite, AnamnesisResponse } from '@/types/shared'

export const anamnesisService = {
  // Templates
  getTemplates: () => api.get<AnamnesisTemplate[]>('/api/anamnesis/templates'),

  // Invites
  getInvites: (evaluationId?: number) =>
    api.get<AnamnesisInvite[]>(evaluationId ? `/api/anamnesis/invites?evaluation_id=${evaluationId}` : '/api/anamnesis/invites'),

  createInvite: (data: Record<string, unknown>) => api.post<AnamnesisInvite>('/api/anamnesis/invites', data),

  sendEmail: (inviteId: number | string) => api.post<Record<string, unknown>>(`/api/anamnesis/invites/${inviteId}/send-email`, {}),

  sendWhatsapp: (inviteId: number | string) => api.post<Record<string, unknown>>(`/api/anamnesis/invites/${inviteId}/send-whatsapp`, {}),

  resendInvite: (inviteId: number | string) => api.post<Record<string, unknown>>(`/api/anamnesis/invites/${inviteId}/resend`, {}),

  cancelInvite: (inviteId: number | string) => api.post<Record<string, unknown>>(`/api/anamnesis/invites/${inviteId}/cancel`, {}),

  // Responses
  getResponses: (evaluationId?: number) =>
    api.get<AnamnesisResponse[]>(evaluationId ? `/api/anamnesis/responses?evaluation_id=${evaluationId}` : '/api/anamnesis/responses'),

  getCurrentResponse: (evaluationId: number | string) =>
    api.get<AnamnesisResponse>(`/api/anamnesis/responses/current/${evaluationId}`),

  reviewResponse: (responseId: number | string) =>
    api.patch<AnamnesisResponse>(`/api/anamnesis/responses/${responseId}/review`, { status: "reviewed" }),
}
