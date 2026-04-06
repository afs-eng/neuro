export default function EvaluationReportPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 border-b pb-2 mb-4">
        Laudo Neuropsicológico
      </h3>
      <p className="text-sm text-gray-500 mb-6">
        Área de redação e aprovação do Laudo final usando blocos construídos por IA.
      </p>
      
      {/* TODO: Componente ReportSectionEditor */}
      <div className="bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
        <span className="text-gray-500">Laudo não iniciado.</span>
      </div>
    </div>
  )
}
