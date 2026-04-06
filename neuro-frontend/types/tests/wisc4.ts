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
