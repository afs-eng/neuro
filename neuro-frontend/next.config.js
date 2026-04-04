/** @type {import('next').NextConfig} */
const normalizeBackendUrl = (value) => {
  const fallbackUrl = 'http://127.0.0.1:8000'

  if (!value) {
    return fallbackUrl
  }

  const normalized = value.replace(/\/$/, '')
  return normalized.endsWith('/api') ? normalized.slice(0, -4) : normalized
}

const isVercel = process.env.VERCEL === '1'

const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', '127.0.0.1'],
  },
  output: (!isVercel && process.env.BUILD_STANDALONE === 'true') ? 'standalone' : undefined,
  async rewrites() {
    // INTERNAL_API_BASE_URL dita o alvo interno do SSR no cluster Docker ou backend Deploy (ex: http://backend:8000)
    const backendUrl = normalizeBackendUrl(process.env.INTERNAL_API_BASE_URL)
    return [
      {
        source: '/api/:path*',
        destination: `${backendUrl}/api/:path*`,
      },
      {
        source: '/api/:path',
        destination: `${backendUrl}/api/:path/`,
      },
    ]
  },
}

module.exports = nextConfig
