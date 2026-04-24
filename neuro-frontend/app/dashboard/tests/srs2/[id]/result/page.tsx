"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams, useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Printer, Share2 } from "lucide-react";
import { api } from "@/lib/api";

const CLASSIFICATION_STYLES: Record<string, string> = {
  "Dentro dos limites Normais": "bg-emerald-50 text-emerald-700 border-emerald-200",
  Leve: "bg-amber-50 text-amber-700 border-amber-200",
  Moderado: "bg-orange-50 text-orange-700 border-orange-200",
  Grave: "bg-red-50 text-red-700 border-red-200",
  "Norma não localizada": "bg-slate-100 text-slate-700 border-slate-200",
};

function getClassificationStyle(value: string) {
  return CLASSIFICATION_STYLES[value] || "bg-slate-100 text-slate-700 border-slate-200";
}

function formatAppliedOn(value: string) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString("pt-BR");
}

function getFormLabel(value: string) {
  const labels: Record<string, string> = {
    pre_escola: "Pré-escola",
    idade_escolar: "Idade escolar",
    adulto_autorrelato: "Adulto autorrelato",
    adulto_heterorrelato: "Adulto heterorrelato",
  };

  return labels[value] || value || "-";
}

function SRS2ResultPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const params = useParams();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const applicationId = params.id as string;

  useEffect(() => {
    async function fetchResult() {
      if (!applicationId) {
        setError("ID da aplicação não encontrado");
        setLoading(false);
        return;
      }

      try {
        const data = await api.get<any>(`/api/tests/srs2/result/${applicationId}`);
        setResult(data);
      } catch (err: any) {
        setError(err.message || "Erro ao carregar resultado");
      } finally {
        setLoading(false);
      }
    }

    fetchResult();
  }, [applicationId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.push("/dashboard/tests")}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-black text-slate-900">SRS-2</h1>
            <p className="text-sm text-slate-500">Resultado</p>
          </div>
        </div>
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-700 font-medium">{error || "Erro ao carregar resultado"}</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const classified = result.classified_payload || result.results || {};
  const scoreResults = classified.resultados || [];
  const totalResult = scoreResults.find((item: any) => item.variavel === "total");
  const cisResult = scoreResults.find((item: any) => item.variavel === "cis");
  const interpretation = String(result.interpretation || result.interpretation_text || "").trim();
  const interpretationParagraphs = interpretation
    .split(/\n\s*\n/)
    .map((paragraph: string) => paragraph.trim())
    .filter(Boolean);

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.push("/dashboard/tests")}>
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-black text-slate-900">SRS-2</h1>
            <p className="text-sm text-slate-500">Resultado da Avaliação</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="icon" className="rounded-xl">
            <Printer className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="icon" className="rounded-xl">
            <Share2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <Card className="border-slate-100 shadow-spike overflow-hidden">
        <CardHeader>
          <CardTitle className="text-xl font-semibold text-slate-900">Resumo da aplicação</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Paciente</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{result.patient_name || "-"}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Aplicado em</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{formatAppliedOn(result.applied_on)}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Formulário</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{getFormLabel(classified.form)}</p>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Faixa etária normativa</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{classified.faixa_etaria || "-"}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <p className="text-sm text-slate-500">Pontuação Total</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{totalResult?.tscore ?? "-"}</p>
              <p className="mt-2 text-sm text-slate-600">Bruto: {totalResult?.bruto ?? "-"} • Percentil: {totalResult?.percentil ?? "-"}</p>
              <div className="mt-3">
                <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${getClassificationStyle(totalResult?.classificacao || "")}`}>
                  {totalResult?.classificacao || "-"}
                </span>
              </div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-5">
              <p className="text-sm text-slate-500">Comunicação e Interação Social</p>
              <p className="mt-2 text-3xl font-semibold text-slate-900">{cisResult?.tscore ?? "-"}</p>
              <p className="mt-2 text-sm text-slate-600">Bruto: {cisResult?.bruto ?? "-"} • Percentil: {cisResult?.percentil ?? "-"}</p>
              <div className="mt-3">
                <span className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium ${getClassificationStyle(cisResult?.classificacao || "")}`}>
                  {cisResult?.classificacao || "-"}
                </span>
              </div>
            </div>
          </div>

          <div className="overflow-x-auto rounded-2xl border border-slate-200">
            <table className="w-full text-sm">
              <thead className="bg-slate-100 text-slate-700">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">Escala</th>
                  <th className="px-4 py-3 text-center font-medium">Bruto</th>
                  <th className="px-4 py-3 text-center font-medium">T-Score</th>
                  <th className="px-4 py-3 text-center font-medium">Percentil</th>
                  <th className="px-4 py-3 text-left font-medium">Classificação</th>
                </tr>
              </thead>
              <tbody>
                {scoreResults.map((item: any, index: number) => (
                  <tr key={item.variavel || item.nome || index} className={`border-t border-slate-200 ${index % 2 === 0 ? "bg-white" : "bg-slate-50/50"}`}>
                    <td className="px-4 py-3 font-medium text-slate-900">{item.nome || "-"}</td>
                    <td className="px-4 py-3 text-center text-slate-700">{item.bruto ?? "-"}</td>
                    <td className="px-4 py-3 text-center text-slate-700">{item.tscore ?? "-"}</td>
                    <td className="px-4 py-3 text-center text-slate-700">{item.percentil ?? "-"}</td>
                    <td className="px-4 py-3 text-slate-700">{item.classificacao || "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-5">
            <h2 className="text-lg font-semibold text-slate-900">Interpretação</h2>
            {interpretationParagraphs.length > 0 ? (
              <div className="mt-3 space-y-3 text-sm leading-6 text-slate-700">
                {interpretationParagraphs.map((paragraph: string, index: number) => (
                  <p key={index}>{paragraph}</p>
                ))}
              </div>
            ) : (
              <p className="mt-3 text-sm text-slate-500">Sem interpretação disponível para esta aplicação.</p>
            )}
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-4">
        <Button
          onClick={() => router.push(`/dashboard/tests/srs2?evaluation_id=${searchParams.get("evaluation_id")}&edit=true&application_id=${applicationId}`)}
          className="h-12 px-6 rounded-2xl font-black uppercase tracking-widest gap-2"
        >
          Editar
        </Button>
        <Button
          variant="outline"
          onClick={() => router.push("/dashboard/tests")}
          className="h-12 px-6 rounded-2xl font-black uppercase tracking-widest"
        >
          Voltar
        </Button>
      </div>
    </div>
  );
}

export default function SRS2ResultPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    }>
      <SRS2ResultPageContent />
    </Suspense>
  );
}
