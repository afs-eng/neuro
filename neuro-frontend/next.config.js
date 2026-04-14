/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  images: {
    domains: ['localhost', '127.0.0.1'],
  },
  env: {
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL || '',
  },
  async rewrites() {
    const apiBaseUrl = process.env.INTERNAL_API_BASE_URL || 'http://backend:8000';
    return [
      {
        source: '/api/:path*',
        destination: `${apiBaseUrl}/api/:path*`,
      },
    ];
  },
}

module.exports = nextConfig
