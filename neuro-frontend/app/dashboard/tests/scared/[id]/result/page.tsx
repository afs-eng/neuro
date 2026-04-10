"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Download, Edit, Printer } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

const FATORES_DISPLAY = {
  panico_sintomas_somaticos: "Pânico / Sintomas Somáticos",
  ansiedade_generalizada: "Ansiedade Generalizada",
  ansiedade_separacao: "Ansiedade de Separação",
  fobia_social: "Fobia Social",
  evitacao_escolar: "Evitação Escolar",
  total: "Total",
};

const CLASSIFICATION_STYLES: Record<string, string> = {
  "Não clínico": "bg-emerald-50 text-emerald-700 border-emerald-200",
  Fronteiriço: "bg-amber-50 text-amber-700 border-amber-200",
  Clínico: "bg-red-50 text-red-700 border-red-200",
};

function getClassificationStyle(classificacao: string) {
  return CLASSIFICATION_STYLES[classificacao] || "bg-slate-100 text-slate-700 border-slate-200";
}

export default function SCAREDResultPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const evaluationId = searchParams.get("evaluation_id");

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const { api } = await import("@/lib/api");
        const data = await api.get<any>(`/api/tests/scared/result/${params.id}`);
        setResult(data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    if (params.id) fetchResult();
  }, [params.id]);

  const handleEdit = () => {
    const targetUrl = evaluationId
      ? `/dashboard/tests/scared/${params.id}?evaluation_id=${evaluationId}&edit=true`
      : `/dashboard/tests/scared/${params.id}?edit=true`;
    router.push(targetUrl);
  };

  const handleGoBack = () => {
    if (evaluationId) {
      router.push(`/dashboard/evaluations/${evaluationId}/overview`);
    } else {
      router.push("/dashboard/tests");
    }
  };

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-8 bg-slate-200 rounded w-1/3" />
        <div className="grid grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-32 bg-slate-100 rounded-xl" />
          ))}
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" onClick={handleGoBack} className="gap-2">
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <p className="text-slate-600">Resultado não encontrado.</p>
      </div>
    );
  }

  const computed = result.computed_payload || {};
  const classified = result.classified_payload || {};
  const analise = classified.analise_geral || [];
  const sintese = classified.sintese || "";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={handleGoBack} className="gap-2 text-slate-600">
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={handleEdit} className="gap-2">
            <Edit className="h-4 w-4" />
            Editar
          </Button>
        </div>
      </div>

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold text-slate-900">SCARED - Resultado</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {sintese && (
            <div className="bg-slate-50 rounded-xl p-4">
              <p className="font-medium text-slate-900">Síntese</p>
              <p className="text-slate-700 mt-1">{sintese}</p>
            </div>
          )}

          <div>
            <h3 className="font-semibold text-slate-900 mb-4">Análise por Fator</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {analise.map((item: any, idx: number) => {
                const fatorNome = FATORES_DISPLAY[item.fator as keyof typeof FATORES_DISPLAY] || item.fator;
                return (
                  <div
                    key={idx}
                    className="bg-white rounded-xl border border-slate-200 p-4 shadow-sm"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-sm font-medium text-slate-600">{fatorNome}</span>
                      <Badge className={getClassificationStyle(item.classificacao)}>
                        {item.classificacao}
                      </Badge>
                    </div>
                    <div className="space-y-1">
                      <div className="text-2xl font-bold text-slate-900">
                        {item.escore_bruto}
                      </div>
                      {item.percentil !== undefined && (
                        <div className="text-sm text-slate-500">
                          Percentil: {item.percentil}
                        </div>
                      )}
                      {item.z_score !== undefined && (
                        <div className="text-sm text-slate-500">
                          Escore Z: {item.z_score}
                        </div>
                      )}
                      {item.nota_corte !== undefined && (
                        <div className="text-sm text-slate-500">
                          Ponto de corte: {item.nota_corte}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="flex justify-between items-center pt-4 border-t border-slate-200">
            <div className="text-sm text-slate-500">
              <span className="font-medium">Status:</span>{" "}
              {result.is_validated ? (
                <span className="text-emerald-600">Validado</span>
              ) : (
                <span className="text-amber-600">Pendente</span>
              )}
            </div>
            <Badge variant="outline">{computed.form === "parent" ? "Pais/Cuidadores" : "Autorrelato"}</Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}