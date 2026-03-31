const API_URL = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export interface ApiError {
  message: string
  status: number
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null

  const isGetRequest = !options.method || options.method === 'GET'
  const isFormData = typeof FormData !== 'undefined' && options.body instanceof FormData
  
  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    cache: isGetRequest ? 'no-store' : undefined,
    headers: {
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(isFormData ? {} : { 'Content-Type': 'application/json' }),
      ...options.headers,
    },
  })

  if (!res.ok) {
    let errorMessage = `Erro: ${res.status}`
    try {
      const errorData = await res.json()
      errorMessage = errorData.message || errorData.detail || errorMessage
    } catch {}
    const error: ApiError = {
      message: errorMessage,
      status: res.status,
    }
    throw error
  }

  const text = await res.text()
  if (!text) return {} as T
  return JSON.parse(text)
}

export const api = {
  get: <T>(url: string) => fetchAPI<T>(url),
  post: <T>(url: string, data: unknown) =>
    fetchAPI<T>(url, { method: 'POST', body: data instanceof FormData ? data : JSON.stringify(data) }),
  put: <T>(url: string, data: unknown) =>
    fetchAPI<T>(url, { method: 'PUT', body: data instanceof FormData ? data : JSON.stringify(data) }),
  patch: <T>(url: string, data: unknown) =>
    fetchAPI<T>(url, { method: 'PATCH', body: data instanceof FormData ? data : JSON.stringify(data) }),
  delete: <T>(url: string) => fetchAPI<T>(url, { method: 'DELETE' }),
}

// Auth helpers
export function setToken(token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token)
  }
}

export function getToken(): string | null {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token')
  }
  return null
}

export function removeToken() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token')
  }
}
