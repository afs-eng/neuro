'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Mail, Lock, ArrowRight } from 'lucide-react'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const { api } = await import('@/lib/api')
      const response = await api.post<{ access: string; user: any }>('/api/accounts/login', {
        username: email,
        password: password,
      })
      
      if (response.access) {
        localStorage.setItem('token', response.access)
        localStorage.setItem('user', JSON.stringify(response.user))
        router.push('/dashboard')
      }
    } catch (err: any) {
      console.error('Login error:', err)
      setError(err?.message || 'Credenciais inválidas. Tente novamente.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-300 p-4 md:p-10">
      <div className="mx-auto grid max-w-6xl grid-cols-1 overflow-hidden rounded-[38px] bg-[#f3f0e4] shadow-2xl ring-1 ring-black/5 lg:grid-cols-[1.1fr_.95fr]">
        <div className="bg-gradient-to-br from-[#f6f4ed] via-[#f3efe4] to-[#efe7bf] p-8 md:p-12">
          <div className="inline-flex rounded-full border border-black/15 bg-white/80 px-5 py-2 text-2xl tracking-tight text-zinc-900 shadow-sm">
            Florescer
          </div>
          <div className="mt-12 max-w-xl">
            <div className="text-5xl font-medium tracking-tight text-zinc-900">
              Sistema clínico para psicologia e neuropsicologia
            </div>
            <p className="mt-4 text-lg text-zinc-600">
              Interface moderna para cadastro de pacientes, agenda, aplicação de testes e construção de laudos.
            </p>
          </div>

          <div className="mt-10 grid grid-cols-1 gap-4 md:grid-cols-3">
            <div className="rounded-[24px] bg-white/60 p-4 shadow ring-1 ring-black/5">
              <div className="text-lg font-medium text-zinc-900">Pacientes</div>
              <div className="text-sm text-zinc-600">Cadastro e histórico</div>
            </div>
            <div className="rounded-[24px] bg-white/60 p-4 shadow ring-1 ring-black/5">
              <div className="text-lg font-medium text-zinc-900">Testes</div>
              <div className="text-sm text-zinc-600">Aplicação e correção</div>
            </div>
            <div className="rounded-[24px] bg-white/60 p-4 shadow ring-1 ring-black/5">
              <div className="text-lg font-medium text-zinc-900">Laudos</div>
              <div className="text-sm text-zinc-600">Modelos clínicos</div>
            </div>
          </div>

          <div className="mt-10 rounded-[30px] bg-zinc-900 p-5 text-white shadow-lg">
            <div className="text-xl font-medium">Módulos incluídos</div>
            <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-2">
              {[
                'Tela de login',
                'Dashboard principal',
                'Cadastro de pacientes',
                'Módulo de testes',
                'Agenda clínica',
                'Laudos e documentação',
              ].map((item) => (
                <div key={item} className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="flex items-center justify-center p-8 md:p-12">
          <div className="w-full max-w-md rounded-[34px] bg-white/80 p-6 shadow-xl ring-1 ring-black/5 backdrop-blur">
            <div className="text-3xl font-medium tracking-tight text-zinc-900">Entrar no sistema</div>
            <div className="mt-1 text-zinc-500">Acesso da clínica psicológica</div>

            <form onSubmit={handleLogin} className="mt-8 space-y-4">
              <div className="flex items-center gap-3 rounded-2xl border border-black/10 bg-[#f7f3e8] px-4 py-4">
                <Mail className="h-4 w-4 text-zinc-500" />
                <input
                  type="text"
                  placeholder="Usuário"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-transparent text-sm outline-none"
                  required
                />
              </div>

              <div className="flex items-center gap-3 rounded-2xl border border-black/10 bg-[#f7f3e8] px-4 py-4">
                <Lock className="h-4 w-4 text-zinc-500" />
                <input
                  type="password"
                  placeholder="Senha"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-transparent text-sm outline-none"
                  required
                />
              </div>

              {error && (
                <div className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-600">
                  {error}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="flex w-full items-center justify-center gap-2 rounded-full bg-zinc-900 px-5 py-4 text-sm text-white shadow hover:bg-zinc-800 disabled:opacity-50"
              >
                {loading ? 'Entrando...' : 'Entrar'}
                <ArrowRight className="h-4 w-4" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}