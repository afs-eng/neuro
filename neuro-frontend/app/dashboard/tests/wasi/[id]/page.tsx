'use client'

import { useEffect } from 'react'
import { useRouter, useParams, useSearchParams } from 'next/navigation'

export default function TestEditPage() {
  const router = useRouter()
  const params = useParams()
  const searchParams = useSearchParams()

  useEffect(() => {
    const applicationId = params.id as string
    const evaluationId = searchParams.get('evaluation_id')

    let url = `/dashboard/tests/wasi?application_id=${applicationId}&edit=true`
    if (evaluationId) {
      url += `&evaluation_id=${evaluationId}`
    }

    router.replace(url)
  }, [params.id, searchParams, router])

  return null
}
