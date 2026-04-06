function normalizeApiBaseUrl(value?: string) {
  // Verificamos se estamos rodando no navegador ou no servidor do Next.js
  const isBrowser = typeof window !== 'undefined';
  const isLocalHost = isBrowser && (
    window.location.hostname === 'localhost' || 
    window.location.hostname === '127.0.0.1' ||
    window.location.hostname.includes('192.168.')
  );

  // Se for localhost (desenvolvimento), usamos o back-end local
  if (isLocalHost) return 'http://127.0.0.1:8000';

  // Se tivermos um endereço configurado (Vercel), usamos ele como prioridade
  if (value && value !== 'http://backend:8000') {
    const normalized = value.replace(/\/$/, '')
    return normalized.endsWith('/api') ? normalized.slice(0, -4) : normalized
  }

  // Fallback absoluto para PRODUÇÃO (Render)
  return 'https://neuro-k06p.onrender.com';
}

const API_URL = normalizeApiBaseUrl(process.env.NEXT_PUBLIC_API_BASE_URL)

if (typeof window !== 'undefined') {
  console.log('🔌 Conectando API em:', API_URL)
}

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
  
  const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  const res = await fetch(`${API_URL}${normalizedEndpoint}`, {
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
      if (typeof errorData === 'string') {
        errorMessage = errorData
      } else if (errorData.message) {
        errorMessage = errorData.message
      } else if (errorData.detail) {
        errorMessage = errorData.detail
      } else if (Array.isArray(errorData)) {
        errorMessage = errorData.map((e: any) => e.msg || JSON.stringify(e)).join(', ')
      } else if (typeof errorData === 'object') {
        const firstKey = Object.keys(errorData)[0]
        const firstError = errorData[firstKey]
        if (Array.isArray(firstError)) {
          errorMessage = `${firstKey}: ${firstError[0]}`
        } else if (typeof firstError === 'object' && firstError.msg) {
          errorMessage = firstError.msg
        } else {
          errorMessage = String(firstError)
        }
      }
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
