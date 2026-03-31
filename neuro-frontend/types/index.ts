export interface Patient {
  id: number
  full_name: string
  birth_date: string
  sex: string
  schooling?: string
  created_at?: string
}

export interface Evaluation {
  id: number
  patient: Patient
  test_type: string
  status: 'pending' | 'in_progress' | 'completed'
  start_date: string
  end_date?: string
}

export interface WISC4Index {
  indice: string
  nome: string
  soma_ponderados: number
  escore_composto: number
  percentil: number
  intervalo_confianca: [number, number]
}

export interface WISC4Result {
  qi_total: number
  qit_data: {
    soma_ponderados: number
    escore_composto: number
    percentil: number
    intervalo_confianca: [number, number]
  }
  gai_data: {
    soma_ponderados: number
    escore_composto: number
    percentil: number
    intervalo_confianca: [number, number]
    classificacao: string
  }
  cpi_data: {
    soma_ponderados: number
    escore_composto: number
    percentil: number
    intervalo_confianca: [number, number]
    classificacao: string
  }
  indices: WISC4Index[]
}