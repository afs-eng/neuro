import { Patient } from './patient'

export interface Evaluation {
  id: number
  patient: Patient
  test_type: string
  status: 'pending' | 'in_progress' | 'completed'
  start_date: string
  end_date?: string
}
