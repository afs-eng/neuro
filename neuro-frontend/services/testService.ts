import { api } from '@/lib/api'
import type { Instrument, TestApplication } from '@/types/shared'

export const testService = {
  // Instruments
  getInstruments: () => api.get<Instrument[]>('/api/tests/instruments'),

  // Applications
  addApplication: (evaluationId: number, instrumentId: number) =>
    api.post<TestApplication>('/api/tests/applications', {
      evaluation_id: evaluationId,
      instrument_id: instrumentId,
    }),

  removeApplication: (applicationId: number | string) =>
    api.delete(`/api/tests/applications/${applicationId}`),
}
