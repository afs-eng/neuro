"use client";

import React, { useMemo, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Brain, ArrowRight, Loader2, Lock, Eye, EyeOff, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ResetPasswordPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const uid = useMemo(() => searchParams.get("uid") || "", [searchParams]);
  const token = useMemo(() => searchParams.get("token") || "", [searchParams]);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const hasValidLink = Boolean(uid && token);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!hasValidLink) {
      setError("Link invalido ou incompleto.");
      return;
    }

    if (password !== confirmPassword) {
      setError("As senhas digitadas nao coincidem.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const { api } = await import("@/lib/api");
      const response = await api.post<{ message: string }>("/api/accounts/reset-password/confirm", {
        uid,
        token,
        password,
      });
      setSuccess(response.message);
      setTimeout(() => router.push("/login"), 1800);
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel redefinir a senha.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-slate-50">
      <div className="flex w-full items-center justify-center p-8">
        <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-10 shadow-sm">
          <div className="mb-8 flex items-center justify-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-600">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <span className="text-xl font-semibold text-slate-900">NeuroAvalia</span>
          </div>

          <div className="mb-8 text-center">
            <h1 className="text-2xl font-semibold text-slate-900">Definir nova senha</h1>
            <p className="mt-2 text-sm text-slate-500">
              Escolha uma nova senha para acessar sua conta.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5">
            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                {error}
              </div>
            )}

            {success && (
              <div className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
                <div className="flex items-start gap-2">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0" />
                  <span>{success}</span>
                </div>
              </div>
            )}

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Nova senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="h-11 pl-10 pr-11"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-600"
                  aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">Confirmar nova senha</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="Repita a nova senha"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  className="h-11 pl-10"
                  required
                />
              </div>
            </div>

            <Button
              type="submit"
              className="h-11 w-full gap-2 bg-indigo-600 hover:bg-indigo-700"
              disabled={loading || !hasValidLink}
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  Salvar nova senha
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </form>

          {!hasValidLink && (
            <p className="mt-4 text-center text-sm text-slate-500">
              Solicite um novo link em{" "}
              <Link href="/forgot-password" className="font-medium text-indigo-600 hover:text-indigo-700">
                recuperar senha
              </Link>
              .
            </p>
          )}

          <p className="mt-6 text-center text-sm text-slate-500">
            <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-700">
              Voltar para o login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
