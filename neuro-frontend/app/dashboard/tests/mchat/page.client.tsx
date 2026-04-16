"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, AlertCircle, Save, ShieldAlert, ShieldCheck, Baby } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

const ITEMS = [
  [1, "gosta_de_balancar", "Seu filho gosta de se balançar, de pular no seu joelho, etc.?"],
  [2, "interesse_outras_criancas", "Seu filho tem interesse por outras crianças?"],
  [3, "gosta_de_subir", "Seu filho gosta de subir em coisas, como escadas ou móveis?"],
  [4, "brinca_esconder_mostrar", "Seu filho gosta de brincar de esconder e mostrar o rosto ou de esconde-esconde?"],
  [5, "brinca_faz_de_conta", "Seu filho já brincou de faz-de-conta?"],
  [6, "aponta_para_pedir", "Seu filho já usou o dedo indicador para apontar, para pedir alguma coisa?"],
  [7, "aponta_para_mostrar_interesse", "Seu filho já usou o dedo indicador para apontar, para indicar interesse em algo?"],
  [8, "brinca_corretamente_com_objetos", "Seu filho consegue brincar de forma correta com brinquedos pequenos?"],
  [9, "traz_objetos_para_mostrar", "O seu filho alguma vez trouxe objetos para você para mostrar?"],
  [10, "contato_visual", "O seu filho olha para você no olho por mais de um segundo ou dois?"],
  [11, "hipersensibilidade_a_ruido", "O seu filho já pareceu muito sensível ao barulho?"],
  [12, "sorri_em_resposta", "O seu filho sorri em resposta ao seu rosto ou ao seu sorriso?"],
  [13, "imita_o_adulto", "O seu filho imita você?"],
  [14, "responde_ao_nome", "O seu filho responde quando você chama ele pelo nome?"],
  [15, "segue_apontar", "Se você aponta um brinquedo do outro lado do cômodo, o seu filho olha para ele?"],
  [16, "ja_sabe_andar", "Seu filho já sabe andar?"],
  [17, "olha_para_o_que_o_adulto_olha", "O seu filho olha para coisas que você está olhando?"],
  [18, "movimentos_estranhos_dedos_rosto", "O seu filho faz movimentos estranhos com os dedos perto do rosto dele?"],
  [19, "busca_atencao_para_atividade", "O seu filho tenta atrair a sua atenção para a atividade dele?"],
  [20, "suspeita_de_surdez", "Você alguma vez já se perguntou se seu filho é surdo?"],
  [21, "entende_o_que_dizem", "O seu filho entende o que as pessoas dizem?"],
  [22, "fica_aereo_ou_deambula", "O seu filho às vezes fica aéreo, olhando para o nada?"],
  [23, "checa_reacao_facial", "O seu filho olha para o seu rosto para conferir a sua reação quando vê algo estranho?"],
] as const;

const CRITICAL_ITEMS = new Set([2, 7, 9, 13, 14, 15]);

const FAILURE_RULES: Record<number, "1" | "0"> = {
  1: "0",
  2: "0",
  3: "0",
  4: "0",
  5: "0",
  6: "0",
  7: "0",
  8: "0",
  9: "0",
  10: "0",
  11: "1",
  12: "0",
  13: "0",
  14: "0",
  15: "0",
  16: "0",
  17: "0",
  18: "1",
  19: "0",
  20: "1",
  21: "0",
  22: "1",
  23: "0",
};

type ItemKey = (typeof ITEMS)[number][1];

type FormState = Record<ItemKey, "" | "1" | "0">;

const EMPTY_STATE = Object.fromEntries(ITEMS.map(([, key]) => [key, ""])) as FormState;

function isFailure(itemNumber: number, answer: "1" | "0") {
  return FAILURE_RULES[itemNumber] === answer;
}

function normalizeScore(value: string) {
  if (value === "1" || value === "0") return value;
  if (value === "Sim" || value === "sim") return "1";
  if (value === "Não" || value === "nao" || value === "não") return "0";
  return "";
}

function MCHATPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [patientName, setPatientName] = useState("");
  const [state, setState] = useState<FormState>(EMPTY_STATE);

  const results = useMemo(() => {
    let totalFailures = 0;
    let criticalFailures = 0;

    for (const [number, key] of ITEMS) {
      const answer = state[key];
      if (!answer) continue;
      if (isFailure(number, answer)) {
        totalFailures += 1;
        if (CRITICAL_ITEMS.has(number)) criticalFailures += 1;
      }
    }

    return {
      totalFailures,
      criticalFailures,
      positive: totalFailures >= 3 || criticalFailures >= 2,
      completed: ITEMS.filter(([, key]) => Boolean(state[key])).length,
    };
  }, [state]);

  useEffect(() => {
    async function loadApplication() {
      if (!applicationId) {
        setLoading(false);
        return;
      }

      try {
        const result = await api.get<any>(`/api/tests/applications/${applicationId}`);
        if (result?.patient_name) setPatientName(result.patient_name);

        if (result?.is_validated && searchParams.get("edit") !== "true") {
          const evalQuery = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : "";
          router.replace(`/dashboard/tests/mchat/${applicationId}/result${evalQuery}`);
          return;
        }

        const rawItems = result?.raw_payload?.items || {};
        const nextState = { ...EMPTY_STATE };
        for (const [, key] of ITEMS) {
          const answer = rawItems[key]?.answer;
          nextState[key] = answer === "1" || answer === "0" ? answer : answer === "Sim" ? "1" : answer === "Não" ? "0" : "";
        }
        setState(nextState);
      } catch (err) {
        console.error("Erro ao carregar aplicação:", err);
      } finally {
        setLoading(false);
      }
    }

    loadApplication();
  }, [applicationId, router, searchParams]);

  const handleScoreChange = (itemNumber: number, value: string) => {
    const nextValue = normalizeScore(value);
    const key = ITEMS[itemNumber - 1][1];
    setState((prev) => ({ ...prev, [key]: nextValue }));
  };

  const clearForm = () => {
    if (confirm("Deseja realmente limpar todos os campos do formulário?")) {
      setState(EMPTY_STATE);
    }
  };

  const handleSave = async () => {
    if (!evaluationId) {
      setError("evaluation_id não encontrado na URL.");
      return;
    }

    const missing = ITEMS.filter(([, key]) => !state[key]);
    if (missing.length > 0) {
      setError("Responda todos os 23 itens antes de salvar.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      const payload = {
        evaluation_id: Number(evaluationId),
        respondent_name: "",
        respondent_relationship: "",
        items: Object.fromEntries(
          ITEMS.map(([, key]) => [key, { answer: state[key] }]),
        ),
      };

      const result = await api.post<{ application_id: number }>("/api/tests/mchat/submit", payload);
      router.push(`/dashboard/tests/mchat/${result.application_id}/result?evaluation_id=${evaluationId}`);
    } catch (err: any) {
      setError(err?.message || "Erro ao salvar M-CHAT.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="py-16 text-center text-slate-500">Carregando M-CHAT...</div>;
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6 px-2 sm:px-4">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full border border-slate-200 bg-white shadow-sm">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">M-CHAT</h2>
          <p className="text-sm text-slate-500">Modified Checklist for Autism in Toddlers</p>
        </div>
      </div>

      {error && (
        <div className="flex items-center gap-2 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Dados da aplicação</CardTitle>
          <CardDescription>
            {patientName ? `Paciente: ${patientName}` : "Preencha os 23 itens da triagem."}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <Baby className="h-4 w-4" />
                Triagem
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">M-CHAT</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <ShieldCheck className="h-4 w-4" />
                Concluídos
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{results.completed} / 23</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <ShieldAlert className="h-4 w-4" />
                Falhas
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{results.totalFailures}</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <ShieldAlert className="h-4 w-4" />
                Críticas
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{results.criticalFailures}</div>
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
            <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-4 text-sm leading-6 text-amber-900">
              <div className="mb-2 font-semibold">Orientação clínica</div>
              M-CHAT é uma triagem precoce, voltada a crianças de 18 a 24 meses. Resultado positivo não confirma diagnóstico e deve ser interpretado com avaliação clínica complementar.
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white px-4 py-4">
              <div className="text-sm font-semibold text-slate-900">Resultado parcial</div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                <div className="h-full rounded-full bg-indigo-600 transition-all" style={{ width: `${(results.completed / 23) * 100}%` }} />
              </div>
              <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                <span>{results.completed} de 23 itens preenchidos</span>
                <span>{Math.round((results.completed / 23) * 100)}%</span>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <Badge className="rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">Passa</Badge>
            <Badge className="rounded-full bg-rose-50 text-rose-700 border border-rose-200">Falha</Badge>
            <Badge className="rounded-full bg-amber-50 text-amber-700 border border-amber-200">Item crítico</Badge>
          </div>

          <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
            <p className="font-medium mb-2">Escala de resposta:</p>
            <div className="grid grid-cols-2 gap-2">
              <span><strong>1</strong> = Sim</span>
              <span><strong>0</strong> = Não</span>
            </div>
          </div>

          <div className="border rounded-xl overflow-hidden">
            <div className="grid grid-cols-[52px_1fr_72px] bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700">
              <div>Item</div>
              <div>Descrição</div>
              <div className="text-center">Resp.</div>
            </div>
            <div className="max-h-[520px] overflow-y-auto">
                {ITEMS.map(([number, key, label], idx) => {
                  const answer = state[key];
                  const failed = answer ? isFailure(number, answer) : false;

                  return (
                    <div
                      key={key}
                      className={`grid grid-cols-[52px_1fr_72px] items-center px-3 py-3 border-t ${
                        idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"
                      } ${CRITICAL_ITEMS.has(number) ? "ring-1 ring-amber-200 ring-inset" : ""}`}
                    >
                      <div className="text-sm font-medium text-slate-900">{String(number).padStart(2, "0")}</div>
                      <div className="pr-4">
                        <div className="text-sm text-slate-700">{label}</div>
                        <div className="mt-1 text-xs text-slate-500">
                          {CRITICAL_ITEMS.has(number) ? "Item crítico" : ""}
                        </div>
                      </div>
                      <div className="flex justify-center">
                        <Input
                          type="text"
                          inputMode="numeric"
                          maxLength={1}
                          className="h-8 w-16 rounded-lg text-center"
                          value={answer || ""}
                          onChange={(e) => handleScoreChange(number, e.target.value)}
                          onKeyDown={(e) => {
                            if (e.key === "Enter") {
                              e.preventDefault();
                              const nextId = `input-item-${idx + 2}`;
                              document.getElementById(nextId)?.focus();
                            }
                          }}
                          id={`input-item-${idx + 1}`}
                          placeholder="0/1"
                        />
                      </div>
                    </div>
                  );
                })}
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-500">
            <span className="inline-flex h-2.5 w-2.5 rounded-full bg-emerald-500" /> Passa
            <span className="ml-4 inline-flex h-2.5 w-2.5 rounded-full bg-rose-500" /> Falha
            <span className="ml-4 inline-flex h-2.5 w-2.5 rounded-full bg-amber-500" /> Item crítico
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-4 flex items-center justify-between gap-4">
            <div>
              <div className="text-sm text-slate-500">Resumo automático</div>
              <div className={`text-lg font-semibold ${results.positive ? "text-rose-600" : "text-emerald-700"}`}>
                {results.positive ? "Triagem positiva" : "Triagem negativa"}
              </div>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" onClick={clearForm} className="gap-2 rounded-xl">
                Limpar campos
              </Button>
              <Button onClick={handleSave} disabled={saving} className="gap-2 rounded-xl">
                <Save className="h-4 w-4" />
                {saving ? "Salvando..." : "Salvar"}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function MCHATPage() {
  return <MCHATPageContent />;
}
