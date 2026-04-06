/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['localhost', '127.0.0.1', 'neuro-k06p.onrender.com'],
  },
  // Removemos rewrites para evitar confusão com domínios internos do Docker
  // O frontend agora conecta DIRETAMENTE na URL do Render via lib/api.ts
}

module.exports = nextConfig
