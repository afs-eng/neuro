const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

console.log('API URL:', API_URL)

export interface ApiError {
  message: string
  status: number
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  console.log('Fetching:', API_URL + endpoint, 'token:', token ? 'yes' : 'no')

  const isGetRequest = !options.method || options.method === 'GET'
  
  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    cache: isGetRequest ? 'no-store' : undefined,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  console.log('Response:', res.status, res.statusText)

  if (!res.ok) {
    let errorMessage = `Erro: ${res.status}`
    try {
      const errorData = await res.json()
      console.log('Error data:', errorData)
      errorMessage = errorData.message || errorData.detail || errorMessage
    } catch (e) {
      console.log('Could not parse error response')
    }
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
    fetchAPI<T>(url, { method: 'POST', body: JSON.stringify(data) }),
  put: <T>(url: string, data: unknown) =>
    fetchAPI<T>(url, { method: 'PUT', body: JSON.stringify(data) }),
  patch: <T>(url: string, data: unknown) =>
    fetchAPI<T>(url, { method: 'PATCH', body: JSON.stringify(data) }),
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