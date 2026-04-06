export default function EvaluationTestsPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 border-b pb-2 mb-4">
        Instrumentos Aplicados
      </h3>
      <p className="text-sm text-gray-500 mb-6">
        Gerencie os testes e protocolos associados a este caso clínico.
      </p>
      
      {/* TODO: Componente TestApplicationList */}
      <div className="bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
        <span className="text-gray-500">Nenhum teste listado ainda.</span>
      </div>
    </div>
  )
}
