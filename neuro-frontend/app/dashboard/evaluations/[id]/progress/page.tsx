export default function EvaluationProgressPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 border-b pb-2 mb-4">
        Evolução Clínica
      </h3>
      <p className="text-sm text-gray-500 mb-6">
        Registre as sessões, observações livres e anotações comportamentais do paciente durante as visitas.
      </p>
      
      {/* TODO: Componente ProgressTimeline */}
      <div className="bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
        <span className="text-gray-500">Nenhuma evolução documentada.</span>
      </div>
    </div>
  )
}
