"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Save } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

import {
  BFP_FACTOR_GROUPS,
  BFP_ITEM_COUNT,
  BFP_RESPONSE_OPTIONS,
  BFP_SAMPLE_OPTIONS,
} from "./data";

type EvaluationSummary = {
  id: number;
  patient_name?: string;
  patient_birth_date?: string | null;
  patient_sex?: string | null;
};

type ExistingApplication = {
  evaluation_id?: number;
  is_validated?: boolean;
  raw_payload?: {
    sample?: string;
    responses?: Record<string, number>;
  };
};

function BFPPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const isEditMode = searchParams.get("edit") === "true";

  const [evaluation, setEvaluation] = useState<EvaluationSummary | null>(null);
  const [loadingEvaluation, setLoadingEvaluation] = useState(true);
  const [sample, setSample] = useState("geral");
  const [responses, setResponses] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  const items = useMemo(() => Array.from({ length: BFP_ITEM_COUNT }, (_, index) => index + 1), []);

  useEffect(() => {
    async function fetchEvaluation() {
      let currentEvaluationId = evaluationId;

      if (applicationId) {
        try {
          const result = await api.get<ExistingApplication>(`/api/tests/applications/${applicationId}`);
          if (result?.evaluation_id && !currentEvaluationId) {
            router.replace(`/dashboard/tests/bfp?application_id=${applicationId}&evaluation_id=${result.evaluation_id}&edit=true`);
            return;
          }
          if (result?.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : "";
            router.push(`/dashboard/tests/bfp/${applicationId}/result${resultEvaluationId}`);
            return;
          }
          if (result?.raw_payload?.sample) {
            setSample(result.raw_payload.sample);
          }
          if (result?.raw_payload?.responses) {
            const nextResponses: Record<string, string> = {};
            Object.entries(result.raw_payload.responses).forEach(([key, value]) => {
              nextResponses[key] = String(value);
            });
            setResponses(nextResponses);
          }
          if (result?.evaluation_id && !currentEvaluationId) {
            currentEvaluationId = String(result.evaluation_id);
          }
        } catch (error) {
          console.log("Aplicação do BFP não encontrada, seguindo para formulário...");
        }
      }

      if (!currentEvaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      try {
        const data = await api.get<EvaluationSummary>(`/api/evaluations/${currentEvaluationId}`);
        setEvaluation(data);
      } catch (error) {
        console.error("Erro ao buscar avaliação:", error);
      } finally {
        setLoadingEvaluation(false);
      }
    }

    fetchEvaluation();
  }, [applicationId, evaluationId, isEditMode, router]);

  function handleResponseChange(item: number, value: string) {
    const numeric = Number.parseInt(value, 10);
    if (value === "" || (!Number.isNaN(numeric) && numeric >= 1 && numeric <= 7)) {
      setResponses((prev) => ({ ...prev, [String(item)]: value }));
    }
  }

  function focusNextItem(item: number) {
    const nextItem = item + 1;
    if (nextItem > BFP_ITEM_COUNT) {
      return;
    }
    const nextInput = document.getElementById(`input-item-${nextItem}`) as HTMLInputElement | null;
    nextInput?.focus();
    nextInput?.select();
  }

  function clearForm() {
    if (confirm("Deseja realmente limpar todas as respostas do BFP?")) {
      setResponses({});
      setSample("geral");
    }
  }

  const answeredCount = Object.values(responses).filter(Boolean).length;

  async function handleSave() {
    const evalId = evaluationId || String(evaluation?.id || "");
    if (!evalId) {
      alert("ID da avaliação não encontrado. Acesse este teste a partir de uma avaliação.");
      return;
    }

    const payloadResponses: Record<string, number> = {};
    for (let item = 1; item <= BFP_ITEM_COUNT; item += 1) {
      payloadResponses[String(item)] = Number.parseInt(responses[String(item)] || "0", 10) || 0;
    }

    setSaving(true);
    try {
      const result = await api.post<{ application_id: number }>("/api/tests/bfp/submit", {
        evaluation_id: Number.parseInt(evalId, 10),
        sample,
        responses: payloadResponses,
      });
      router.push(`/dashboard/tests/bfp/${result.application_id}/result?evaluation_id=${evalId}`);
    } catch (error: any) {
      console.error("Erro ao salvar BFP:", error);
      alert(`Erro ao salvar BFP: ${error?.message || "Tente novamente."}`);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">BFP</h2>
          <p className="text-sm text-slate-500">Bateria Fatorial de Personalidade</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Dados da aplicação
              {isEditMode ? <Badge variant="outline" className="border-amber-200 bg-amber-50 text-amber-600">Modo Edição</Badge> : null}
            </CardTitle>
            <CardDescription>Preencha as respostas da escala BFP e selecione a amostra normativa.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            {loadingEvaluation ? (
              <div className="py-4 text-center text-slate-500">Carregando dados do paciente...</div>
            ) : evaluation ? (
              <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Paciente</label>
                  <div className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm font-medium text-slate-700">
                    {evaluation.patient_name || "—"}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Sexo</label>
                  <div className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                    {evaluation.patient_sex === "M" ? "Masculino" : evaluation.patient_sex === "F" ? "Feminino" : "—"}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Amostra normativa</label>
                  <select
                    value={sample}
                    onChange={(event) => setSample(event.target.value)}
                    className="flex h-10 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-primary/20"
                  >
                    {BFP_SAMPLE_OPTIONS.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            ) : (
              <div className="py-4 text-center text-red-500">Avaliação não encontrada</div>
            )}

            <div className="rounded-xl bg-slate-50 p-4 text-sm text-slate-600">
              <p className="mb-2 font-medium text-slate-900">Escala de resposta</p>
              <div className="grid grid-cols-1 gap-1 md:grid-cols-2">
                {BFP_RESPONSE_OPTIONS.map((option) => (
                  <span key={option.value}>
                    <strong>{option.value}</strong> = {option.label}
                  </span>
                ))}
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <p className="text-sm font-semibold text-slate-900">Progresso de preenchimento</p>
                  <p className="text-xs text-slate-500">{answeredCount} de {BFP_ITEM_COUNT} itens respondidos</p>
                </div>
                <div className="h-3 w-40 overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-primary transition-all" style={{ width: `${(answeredCount / BFP_ITEM_COUNT) * 100}%` }} />
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-slate-200 bg-slate-100 p-3 md:p-4">
              <div className="grid grid-cols-3 gap-3 md:grid-cols-6 md:gap-4">
                {Array.from({ length: 6 }, (_, index) => (
                  <div key={index} className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-center text-xs font-bold uppercase tracking-wider text-slate-600 shadow-sm">
                    Itens {String(index * 21 + 1).padStart(3, "0")} a {String(index * 21 + 21).padStart(3, "0")}
                  </div>
                ))}
              </div>
              <div className="mt-3 max-h-[620px] overflow-y-auto pr-1 md:mt-4">
                <div className="grid grid-cols-3 gap-3 md:grid-cols-6 md:gap-4">
                  {Array.from({ length: 6 }, (_, columnIndex) => {
                    const start = columnIndex * 21 + 1;
                    const columnItems = items.slice(start - 1, start + 20);
                    return (
                      <div key={columnIndex} className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
                        {columnItems.map((item) => (
                          <div key={item} className="space-y-2 border-b border-slate-100 px-3 py-3 last:border-b-0 md:px-4">
                            <div className="flex items-center justify-between">
                              <span className="text-sm font-semibold text-slate-900">Item {String(item).padStart(3, "0")}</span>
                              <span className="text-[11px] uppercase tracking-widest text-slate-400">BFP</span>
                            </div>
                            <Input
                              type="text"
                              inputMode="numeric"
                              maxLength={1}
                              value={responses[String(item)] || ""}
                              onChange={(event) => handleResponseChange(item, event.target.value)}
                              onKeyDown={(event) => {
                                if (event.key === "Enter") {
                                  event.preventDefault();
                                  focusNextItem(item);
                                }
                              }}
                              onFocus={(event) => event.currentTarget.select()}
                              className="h-9 rounded-lg text-center"
                              placeholder="1-7"
                              id={`input-item-${item}`}
                            />
                          </div>
                        ))}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>

            <div className="flex gap-2">
              <Button className="gap-2 rounded-xl" onClick={handleSave} disabled={saving}>
                <Save className="h-4 w-4" />
                {saving ? "Salvando..." : isEditMode ? "Salvar Alterações" : "Salvar aplicação"}
              </Button>
              <Button variant="outline" className="rounded-xl border-red-200 text-red-600 hover:bg-red-50 hover:text-red-700" onClick={clearForm}>
                Limpar Campos
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Informações do teste</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4 text-sm text-slate-600">
            <div>
              <p className="font-medium text-slate-900">Estrutura</p>
              <p>126 itens em escala Likert de 7 pontos, com correção por facetas e fatores.</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Correção</p>
              <p>Médias das facetas, médias dos fatores, z-score, escore ponderado, percentil e classificação.</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Amostras</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {BFP_SAMPLE_OPTIONS.map((option) => (
                  <Badge key={option.value} variant="outline" className="border-slate-200 bg-slate-50 text-slate-700">
                    {option.label}
                  </Badge>
                ))}
              </div>
            </div>
            <div>
              <p className="font-medium text-slate-900">Fatores</p>
              <div className="mt-2 space-y-3">
                {BFP_FACTOR_GROUPS.map((factor) => (
                  <div key={factor.code} className="rounded-xl border border-slate-100 bg-slate-50 p-3">
                    <p className="font-medium text-slate-900">{factor.name}</p>
                    <p className="mt-1 text-xs leading-5 text-slate-500">{factor.summary}</p>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-3 text-xs leading-5 text-slate-500">
              Os enunciados dos 126 itens não estão expostos na planilha de correção. Nesta primeira versão, o formulário usa a numeração oficial dos itens para permitir teste completo de aplicação, correção e resultado.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function BFPPageFallback() {
  return <div className="space-y-6" />;
}

export default function BFPPage() {
  return (
    <Suspense fallback={<BFPPageFallback />}>
      <BFPPageContent />
    </Suspense>
  );
}
