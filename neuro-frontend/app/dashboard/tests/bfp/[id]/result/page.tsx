"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, LayoutDashboard } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

import {
  BFP_FACTOR_GROUPS,
  BFP_FACET_NAMES,
  BFP_RESPONSE_OPTIONS,
  formatScaleValue,
  getBfpClassificationColor,
} from "../../data";

type ScaleResult = {
  code: string;
  name: string;
  raw_score: number;
  mean: number;
  sd: number;
  z_score: number;
  weighted_score: number;
  percentile: number;
  classification: string;
};

type ApplicationData = {
  id: number;
  evaluation_id?: number;
  patient_name?: string;
  applied_on?: string | null;
  raw_payload?: {
    sample?: string;
    responses?: Record<string, number>;
  };
  computed_payload?: {
    sample?: string;
    sample_label?: string;
    factors?: Record<string, ScaleResult>;
    facets?: Record<string, ScaleResult>;
  };
  interpretation_text?: string;
};

function PercentileMiniChart({
  factorName,
  rows,
}: {
  factorName: string;
  rows: Array<{ label: string; percentile: number }>;
}) {
  const width = 360;
  const height = 140;
  const leftPad = 34;
  const rightPad = 12;
  const topPad = 18;
  const bottomPad = 28;
  const chartWidth = width - leftPad - rightPad;
  const chartHeight = height - topPad - bottomPad;
  const stepX = rows.length > 1 ? chartWidth / (rows.length - 1) : chartWidth;
  const y = (value: number) => topPad + chartHeight - (Math.max(0, Math.min(100, value)) / 100) * chartHeight;
  const points = rows
    .map((row, index) => `${leftPad + index * stepX},${y(row.percentile)}`)
    .join(" ");

  return (
    <svg viewBox={`0 0 ${width} ${height}`} className="h-[170px] w-full min-w-[320px]">
      <rect x={leftPad} y={topPad} width={chartWidth} height={chartHeight * 0.15} fill="#cbd5e1" />
      <rect x={leftPad} y={topPad + chartHeight * 0.15} width={chartWidth} height={chartHeight * 0.15} fill="#d1fae5" />
      <rect x={leftPad} y={topPad + chartHeight * 0.3} width={chartWidth} height={chartHeight * 0.4} fill="#bbf7d0" />
      <rect x={leftPad} y={topPad + chartHeight * 0.7} width={chartWidth} height={chartHeight * 0.15} fill="#fef08a" />
      <rect x={leftPad} y={topPad + chartHeight * 0.85} width={chartWidth} height={chartHeight * 0.15} fill="#fecaca" />

      {[0, 20, 40, 60, 80, 100].map((tick) => (
        <g key={tick}>
          <line x1={leftPad} y1={y(tick)} x2={width - rightPad} y2={y(tick)} stroke="#cbd5e1" strokeWidth="1" />
          <text x={leftPad - 8} y={y(tick) + 4} textAnchor="end" className="fill-slate-500 text-[10px]">
            {tick}
          </text>
        </g>
      ))}

      {rows.map((row, index) => {
        const x = leftPad + index * stepX;
        return (
          <g key={row.label}>
            <line x1={x} y1={topPad} x2={x} y2={topPad + chartHeight} stroke="#e2e8f0" strokeWidth="1" />
            <text x={x} y={height - 8} textAnchor="middle" className="fill-slate-600 text-[9px]">
              {row.label}
            </text>
          </g>
        );
      })}

      {rows.length > 1 ? <polyline fill="none" stroke="#111827" strokeWidth="1.5" points={points} /> : null}
      {rows.map((row, index) => {
        const x = leftPad + index * stepX;
        const cy = y(row.percentile);
        return (
          <g key={`${row.label}-point`}>
            <line x1={x} y1={topPad + chartHeight} x2={x} y2={cy} stroke="#f87171" strokeWidth="1" opacity="0.7" />
            <path d={`M ${x - 4} ${cy - 4} L ${x + 4} ${cy + 4} M ${x + 4} ${cy - 4} L ${x - 4} ${cy + 4}`} stroke="#111827" strokeWidth="1.5" />
          </g>
        );
      })}

      <text x={width / 2} y={12} textAnchor="middle" className="fill-slate-900 text-[12px] font-bold uppercase">
        {factorName}
      </text>
      <text x={12} y={topPad + chartHeight / 2} transform={`rotate(-90 12 ${topPad + chartHeight / 2})`} textAnchor="middle" className="fill-slate-500 text-[10px]">
        Percentil
      </text>
    </svg>
  );
}

function BFPResultPageContent() {
  const router = useRouter();
  const params = useParams();
  const searchParams = useSearchParams();
  const applicationId = params.id as string;
  const [application, setApplication] = useState<ApplicationData | null>(null);
  const [loading, setLoading] = useState(true);
  const [evaluationId, setEvaluationId] = useState(searchParams.get("evaluation_id") || "");

  useEffect(() => {
    async function fetchApplication() {
      try {
        const result = await api.get<ApplicationData>(`/api/tests/applications/${applicationId}`);
        setApplication(result);
        if (result?.evaluation_id && !evaluationId) {
          setEvaluationId(String(result.evaluation_id));
        }
      } catch (error) {
        console.error("Erro ao buscar resultado do BFP:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchApplication();
  }, [applicationId, evaluationId]);

  const backHref = useMemo(() => {
    return evaluationId ? `/dashboard/evaluations/${evaluationId}?tab=overview` : "/dashboard/evaluations?tab=overview";
  }, [evaluationId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-24">
        <div className="text-center">
          <div className="mx-auto mb-4 h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
          <p className="text-sm text-slate-500">Carregando resultado...</p>
        </div>
      </div>
    );
  }

  if (!application) {
    return <div className="py-12 text-center text-red-500">Resultado do BFP não encontrado.</div>;
  }

  const computed = application.computed_payload || {};
  const factors = computed.factors || {};
  const facets = computed.facets || {};
  const interpretation = application.interpretation_text || "";
  const responseValues = Object.values(application.raw_payload?.responses || {});
  const sampleLabel = computed.sample_label || application.raw_payload?.sample || "Geral";
  const appliedOn = application.applied_on ? new Date(application.applied_on).toLocaleDateString("pt-BR") : "—";
  const answeredCount = responseValues.filter((value) => value >= 1 && value <= 7).length;

  return (
    <div className="mx-auto max-w-6xl space-y-8">
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => router.push(backHref)} className="rounded-full">
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div>
            <h2 className="text-2xl font-semibold text-slate-900">BFP - Resultado</h2>
            <p className="text-sm text-slate-500">Bateria Fatorial de Personalidade</p>
          </div>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2 rounded-xl" onClick={() => router.push(`/dashboard/tests/bfp?application_id=${applicationId}&edit=true${evaluationId ? `&evaluation_id=${evaluationId}` : ""}`)}>
            Editar aplicação
          </Button>
          <Button variant="outline" className="gap-2 rounded-xl" onClick={() => router.push(backHref)}>
            <LayoutDashboard className="h-4 w-4" />
            Voltar à Avaliação
          </Button>
        </div>
      </div>

      <div className="rounded-[30px] border border-slate-200 bg-white px-6 py-6 shadow-sm sm:px-8">
        <div className="flex flex-col gap-5 border-b border-slate-200 pb-5 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">Visão Geral</p>
            <h1 className="mt-2 font-serif text-[2.6rem] font-semibold leading-none tracking-[-0.04em] text-slate-950 sm:text-[4rem]">
              BFP
            </h1>
            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">
              Resultado dos cinco grandes fatores de personalidade e suas facetas, com correção normativa e interpretação clínica integrada.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm text-slate-600 sm:text-right">
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">Paciente</p>
              <p className="mt-1 font-medium text-slate-800">{application.patient_name || "—"}</p>
            </div>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">Aplicação</p>
              <p className="mt-1 font-medium text-slate-800">{appliedOn}</p>
            </div>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">Amostra</p>
              <p className="mt-1 font-medium text-slate-800">{sampleLabel}</p>
            </div>
            <div>
              <p className="text-[11px] font-semibold uppercase tracking-[0.18em] text-slate-400">Itens válidos</p>
              <p className="mt-1 font-medium text-slate-800">{answeredCount} / 126</p>
            </div>
          </div>
        </div>

        <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-3">
          <Card className="rounded-2xl border-slate-200 shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-500">Fatores avaliados</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-slate-900">5</div>
              <p className="mt-2 text-xs text-slate-500">Neuroticismo, Extroversão, Socialização, Realização e Abertura</p>
            </CardContent>
          </Card>

          <Card className="rounded-2xl border-slate-200 shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-500">Facetas calculadas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-slate-900">17</div>
              <p className="mt-2 text-xs text-slate-500">Médias facetais com itens invertidos aplicados quando necessário</p>
            </CardContent>
          </Card>

          <Card className="rounded-2xl border-slate-200 shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-slate-500">Escala de resposta</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-slate-900">1-7</div>
              <p className="mt-2 text-xs text-slate-500">Likert de discordância total a concordância total</p>
            </CardContent>
          </Card>
        </div>
      </div>

      <section className="space-y-6">
        {BFP_FACTOR_GROUPS.map((factor) => {
          const factorResult = factors[factor.code];
          if (!factorResult) {
            return null;
          }

          const chartRows = [
            { label: factor.name, percentile: factorResult.percentile },
            ...factor.facets
              .map((facetCode) => facets[facetCode])
              .filter(Boolean)
              .map((facet) => ({ label: facet.name, percentile: facet.percentile })),
          ];

          return (
            <div key={factor.code} className="rounded-[28px] border border-slate-200 bg-white px-5 py-6 shadow-sm sm:px-8 sm:py-8">
              <div className="grid grid-cols-1 gap-6 xl:grid-cols-[minmax(0,1.4fr)_360px] xl:items-start">
                <div className="overflow-x-auto">
                  <table className="min-w-full text-sm">
                    <thead>
                      <tr className="bg-slate-900 text-white">
                        <th className="px-4 py-3 text-left font-semibold">Fator</th>
                        <th className="px-4 py-3 text-center font-semibold">Pts Bts</th>
                        <th className="px-4 py-3 text-center font-semibold">Média</th>
                        <th className="px-4 py-3 text-center font-semibold">D.P.</th>
                        <th className="px-4 py-3 text-center font-semibold">Z-Score</th>
                        <th className="px-4 py-3 text-center font-semibold">Ponder</th>
                        <th className="px-4 py-3 text-center font-semibold">Percentil</th>
                        <th className="px-4 py-3 text-center font-semibold">Classificação</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr className="border-b border-slate-200 bg-slate-50">
                        <td className="px-4 py-3 font-semibold text-slate-900">{factor.name} {factor.code}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.raw_score, 2)}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.mean, 2)}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.sd, 2)}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.z_score, 3)}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.weighted_score, 1)}</td>
                        <td className="px-4 py-3 text-center">{formatScaleValue(factorResult.percentile)}</td>
                        <td className="px-4 py-3 text-center">
                          <Badge className={`border ${getBfpClassificationColor(factorResult.classification)}`}>{factorResult.classification}</Badge>
                        </td>
                      </tr>
                      {factor.facets.map((facetCode) => {
                        const result = facets[facetCode];
                        if (!result) {
                          return null;
                        }
                        return (
                          <tr key={facetCode} className="border-b border-slate-100 last:border-b-0">
                            <td className="px-4 py-3 text-slate-800">{BFP_FACET_NAMES[facetCode] || facetCode} {facetCode}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.raw_score, 2)}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.mean, 2)}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.sd, 2)}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.z_score, 3)}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.weighted_score, 1)}</td>
                            <td className="px-4 py-3 text-center">{formatScaleValue(result.percentile)}</td>
                            <td className="px-4 py-3 text-center">
                              <Badge className={`border ${getBfpClassificationColor(result.classification)}`}>{result.classification}</Badge>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-3">
                  <PercentileMiniChart factorName={factor.name.toUpperCase()} rows={chartRows} />
                </div>
              </div>
            </div>
          );
        })}
      </section>

      <section className="rounded-[28px] border border-slate-200 bg-white px-5 py-6 shadow-sm sm:px-8 sm:py-8">
        <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">Aplicação</p>
        <h3 className="font-serif text-[2.3rem] font-semibold leading-none tracking-[-0.03em] text-slate-950 sm:text-[3.2rem]">
          Respostas Registradas
        </h3>
        <div className="mt-6 grid grid-cols-1 gap-3 md:grid-cols-3 xl:grid-cols-6">
          {Array.from({ length: 126 }, (_, index) => {
            const item = index + 1;
            const score = application.raw_payload?.responses?.[String(item)];
            const label = BFP_RESPONSE_OPTIONS.find((option) => option.value === score)?.label || "Não respondido";
            return (
              <div key={item} className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-center">
                <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">Item {String(item).padStart(3, "0")}</p>
                <p className="mt-2 text-xl font-bold text-slate-900">{score || "-"}</p>
                <p className="mt-1 text-[11px] leading-4 text-slate-500">{label}</p>
              </div>
            );
          })}
        </div>
      </section>

      <section className="rounded-[28px] border border-slate-200 bg-white px-5 py-6 shadow-sm sm:px-8 sm:py-8">
        <p className="mb-2 text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">Interpretação Clínica</p>
        <h3 className="font-serif text-[2.3rem] font-semibold leading-none tracking-[-0.03em] text-slate-950 sm:text-[3.2rem]">
          Síntese Narrativa
        </h3>
        <div className="mt-6 whitespace-pre-line text-sm leading-7 text-slate-700">
          {interpretation || "Interpretação ainda não disponível para esta aplicação."}
        </div>
      </section>
    </div>
  );
}

function BFPResultFallback() {
  return <div className="space-y-8" />;
}

export default function BFPResultPage() {
  return (
    <Suspense fallback={<BFPResultFallback />}>
      <BFPResultPageContent />
    </Suspense>
  );
}
