'use client'

import { usePathname } from 'next/navigation'
import Link from 'next/link'

interface EvaluationTabsProps {
  evaluationId: string | number
}

export function EvaluationTabs({ evaluationId }: EvaluationTabsProps) {
  const pathname = usePathname()

  const tabs = [
    { name: 'Visão Geral', href: `/dashboard/evaluations/${evaluationId}/overview` },
    { name: 'Testes', href: `/dashboard/evaluations/${evaluationId}/tests` },
    { name: 'Anamnese', href: `/dashboard/evaluations/${evaluationId}/anamnesis` },
    { name: 'Documentos', href: `/dashboard/evaluations/${evaluationId}/documents` },
    { name: 'Evolução', href: `/dashboard/evaluations/${evaluationId}/progress` },
    { name: 'Laudo', href: `/dashboard/evaluations/${evaluationId}/report` },
  ]

  return (
    <div className="border-b border-gray-200">
      <nav className="-mb-px flex space-x-8" aria-label="Tabs">
        {tabs.map((tab) => {
          const isActive = pathname.startsWith(tab.href)
          return (
            <Link
              key={tab.name}
              href={tab.href}
              className={`${
                isActive
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
            >
              {tab.name}
            </Link>
          )
        })}
      </nav>
    </div>
  )
}
