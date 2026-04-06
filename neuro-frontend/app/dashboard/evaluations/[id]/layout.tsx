import { ReactNode } from "react"

export default function ClinicalEvaluationLayout({
  children,
}: {
  children: ReactNode
}) {
  return (
    <div className="w-full min-h-screen">
      {children}
    </div>
  )
}
