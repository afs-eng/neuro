import { api } from '@/lib/api'
import type { Patient } from '@/types/shared'

export const patientService = {
  list: () => api.get<Patient[]>('/api/patients'),

  get: (id: number) => api.get<Patient>(`/api/patients/${id}`),

  create: (data: Partial<Patient>) => api.post<Patient>('/api/patients', data),

  update: (id: number, data: Partial<Patient>) => api.put<Patient>(`/api/patients/${id}`, data),

  delete: (id: number) => api.delete(`/api/patients/${id}`),

  search: (query: string) => api.get<Patient[]>(`/api/patients?search=${query}`),
}