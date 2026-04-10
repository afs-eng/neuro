"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Brain, ArrowRight, Loader2, Mail, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const { api } = await import("@/lib/api");
      const response = await api.post<{ message: string }>("/api/accounts/forgot-password", { email: email.trim() });
      setSuccess(response.message);
    } catch (err: any) {
      setError(err?.message || "Nao foi possivel enviar as instrucoes agora.");
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
            <h1 className="text-2xl font-semibold text-slate-900">Recuperar acesso</h1>
            <p className="mt-2 text-sm text-slate-500">
              Informe seu email para receber o link de redefinicao de senha.
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
              <label className="text-sm font-medium text-slate-700">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
                <Input
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="h-11 pl-10"
                  required
                />
              </div>
            </div>

            <Button type="submit" className="h-11 w-full gap-2 bg-indigo-600 hover:bg-indigo-700" disabled={loading}>
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <>
                  Enviar link de redefinicao
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Lembrou da senha?{" "}
            <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-700">
              Voltar para o login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
