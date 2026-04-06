import { redirect } from 'next/navigation'

export default function EvaluationRoot({ params }: { params: { id: string } }) {
  // Redireciona a raiz da avaliação diretamente para a aba "Visão Geral" (Overview)
  redirect(`/dashboard/evaluations/${params.id}/overview`)
}
