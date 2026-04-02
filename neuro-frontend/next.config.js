/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', '127.0.0.1'],
  },
  output: process.env.BUILD_STANDALONE === 'true' ? 'standalone' : undefined, // standlone ativado via Dockerfile
  async rewrites() {
    // INTERNAL_API_BASE_URL dita o alvo interno do SSR no cluster Docker ou backend Deploy (ex: http://backend:8000)
    const backendUrl = process.env.INTERNAL_API_BASE_URL || 'http://127.0.0.1:8000';
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