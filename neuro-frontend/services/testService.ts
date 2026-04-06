import { api } from '@/lib/api'

export const testService = {
  // Instruments
  getInstruments: () => api.get<any[]>('/api/tests/instruments/'),
  
  // Applications
  addApplication: (evaluationId: number, instrumentId: number) => 
    api.post<any>('/api/tests/applications/', {
      evaluation_id: evaluationId,
      instrument_id: instrumentId,
    }),
    
  removeApplication: (applicationId: number | string) => 
    api.delete(`/api/tests/applications/${applicationId}/`),
}
