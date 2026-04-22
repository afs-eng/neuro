"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Edit } from "lucide-react";
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
  Média: "bg-slate-100 text-slate-700 border-slate-200",
  Superior: "bg-amber-50 text-amber-700 border-amber-200",
  "Muito Superior": "bg-red-50 text-red-700 border-red-200",
};

function getClassificationStyle(classificacao: string) {
  return CLASSIFICATION_STYLES[classificacao] || "bg-slate-100 text-slate-700 border-slate-200";
}

function getFormLabel(formType?: string) {
  return formType === "parent" ? "Pais/Cuidadores" : "Autorrelato";
}

function getAlternateForm(formType?: string) {
  return formType === "parent" ? "child" : "parent";
}

function getDisplayClassification(formType: string | undefined, classificacao: string) {
  if (formType === "parent") {
    return classificacao;
  }

  const classificationMap: Record<string, string> = {
    "Na Média": "Média",
    Elevado: "Superior",
    "Muito Elevado": "Muito Superior",
  };

  return classificationMap[classificacao] || classificacao;
}

function formatNumber(value: unknown) {
  if (value === undefined || value === null || value === "") {
    return "-";
  }

  if (typeof value === "number") {
    return value.toLocaleString("pt-BR", {
      minimumFractionDigits: value % 1 === 0 ? 0 : 2,
      maximumFractionDigits: 2,
    });
  }

  return String(value);
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
  const formType = classified.form_type || computed.form || "child";
  const formLabel = getFormLabel(formType);
  const isParentForm = formType === "parent";
  const alternateForm = getAlternateForm(formType);
  const alternateFormLabel = getFormLabel(alternateForm);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={handleGoBack} className="gap-2 text-slate-600">
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </Button>
        <div className="flex gap-2">
          {evaluationId && (
            <Button
              variant="outline"
              size="sm"
              onClick={() =>
                router.push(
                  `/dashboard/tests/scared?evaluation_id=${evaluationId}&form=${alternateForm}`
                )
              }
              className="gap-2"
            >
              Adicionar {alternateFormLabel}
            </Button>
          )}
          <Button variant="outline" size="sm" onClick={handleEdit} className="gap-2">
            <Edit className="h-4 w-4" />
            Editar
          </Button>
        </div>
      </div>

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardHeader>
          <div className="flex items-start justify-between gap-4">
            <div>
              <CardTitle className="text-2xl font-semibold text-slate-900">SCARED - {formLabel}</CardTitle>
              <p className="mt-1 text-sm text-slate-500">
                {isParentForm
                  ? "Versão para pais e cuidadores com leitura por ponto de corte clínico."
                  : "Versão de autorrelato com comparação por média normativa e percentil."}
              </p>
            </div>
            <Badge variant="outline">{formLabel}</Badge>
          </div>
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
            <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
              <div className={`grid ${isParentForm ? "grid-cols-[2fr_1fr_1fr_1fr_1.2fr]" : "grid-cols-[2fr_1fr_1fr_1fr_1.2fr]"} bg-slate-100 px-4 py-3 text-sm font-medium text-slate-700`}>
                <div>Escala</div>
                <div className="text-center">Pontos Brutos</div>
                <div className="text-center">{isParentForm ? "Nota de Corte" : "Média"}</div>
                <div className="text-center">Percentil</div>
                <div className="text-center">Classificação</div>
              </div>
              {analise.map((item: any, idx: number) => {
                const fatorNome = FATORES_DISPLAY[item.fator as keyof typeof FATORES_DISPLAY] || item.fator;
                const displayClassification = getDisplayClassification(formType, item.classificacao);
                return (
                  <div
                    key={idx}
                    className={`grid ${isParentForm ? "grid-cols-[2fr_1fr_1fr_1fr_1.2fr]" : "grid-cols-[2fr_1fr_1fr_1fr_1.2fr]"} items-center border-t px-4 py-3 text-sm ${idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"}`}
                  >
                    <div className="pr-4 font-medium text-slate-900">{fatorNome}</div>
                    <div className="text-center text-slate-700">{formatNumber(item.escore_bruto)}</div>
                    <div className="text-center text-slate-700">
                      {formatNumber(isParentForm ? item.nota_corte : item.media)}
                    </div>
                    <div className="text-center text-slate-700">
                      {formatNumber(item.percentil ?? item.percentual)}
                    </div>
                    <div className="flex justify-center">
                      <Badge className={getClassificationStyle(displayClassification)}>
                        {displayClassification}
                      </Badge>
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
            <Badge variant="outline">{formLabel}</Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
