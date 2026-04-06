export default function EvaluationDocumentsPage({ params }: { params: { id: string } }) {
  return (
    <div>
      <h3 className="text-lg font-medium leading-6 text-gray-900 border-b pb-2 mb-4">
        Documentos do Caso
      </h3>
      <p className="text-sm text-gray-500 mb-6">
        Faça o upload e gerencie PDFs, laudos antigos e documentos escolares associados.
      </p>
      
      {/* TODO: Componente DocumentList */}
      <div className="bg-gray-50 rounded-lg border-2 border-dashed border-gray-300 p-12 text-center">
        <span className="text-gray-500">Nenhum documento anexado.</span>
      </div>
    </div>
  )
}
