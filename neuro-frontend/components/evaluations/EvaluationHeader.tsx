import React from 'react'

interface EvaluationHeaderProps {
  evaluationId: string | number
}

export function EvaluationHeader({ evaluationId }: EvaluationHeaderProps) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            Avaliação EA-{evaluationId}
          </h2>
          <p className="mt-1 text-sm text-gray-500">
            Resumo e painel clínico.
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
            Em Andamento
          </span>
        </div>
      </div>
    </div>
  )
}
