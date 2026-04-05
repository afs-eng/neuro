"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams, useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Printer, Share2 } from "lucide-react";
import { api } from "@/lib/api";

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

  const interpretation = result.interpretation || "";
  const lines = interpretation.split("\n");

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
        <pre className="p-6 text-xs font-mono leading-relaxed whitespace-pre">
          {interpretation}
        </pre>
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
