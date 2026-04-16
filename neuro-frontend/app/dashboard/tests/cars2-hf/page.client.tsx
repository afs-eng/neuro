"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Save, AlertCircle, User, ClipboardList, CheckCircle2, Sigma } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

const ITEMS = [
  ["compreensao_socio_emocional", "Compreensão sócio-emocional"],
  ["expressao_emocional_regulacao", "Expressão emocional e regulação das emoções"],
  ["relacionamento_com_pessoas", "Relacionamento com pessoas"],
  ["uso_do_corpo", "Uso do corpo"],
  ["uso_objetos_brincadeiras", "Uso de objetos nas brincadeiras"],
  ["adaptacao_mudancas_interesses_restritos", "Adaptação a mudanças / interesses restritos"],
  ["resposta_visual", "Resposta visual"],
  ["resposta_auditiva", "Resposta auditiva"],
  ["resposta_sensorial", "Resposta a, ou uso de, sabor, cheiro e toque"],
  ["medo_ou_ansiedade", "Medo ou ansiedade"],
  ["comunicacao_verbal", "Comunicação verbal"],
  ["comunicacao_nao_verbal", "Comunicação não verbal"],
  ["integracao_pensamento_cognicao", "Habilidades de integração de pensamento/cognitiva"],
  ["resposta_intelectual", "Leve e consistente resposta intelectual"],
  ["impressoes_gerais", "Impressões gerais"],
] as const;

type ItemKey = (typeof ITEMS)[number][0];

type ItemState = {
  score: string;
  observations: string;
};

type FormState = Record<ItemKey, ItemState>;

const EMPTY_STATE = Object.fromEntries(
  ITEMS.map(([key]) => [key, { score: "", observations: "" }]),
) as FormState;

const SCORE_OPTIONS = ["1", "2", "3", "4"] as const;

const SCORE_MAP: Record<(typeof SCORE_OPTIONS)[number], string> = {
  1: "1",
  2: "1.5",
  3: "2.5",
  4: "3.5",
};

function normalizeScore(rawScore: unknown) {
  const score = String(rawScore ?? "");
  if (score === "1") return "1";
  if (score === "1.5") return "2";
  if (score === "2.5") return "3";
  if (score === "3.5") return "4";
  return score;
}

function CARS2HFPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [patientName, setPatientName] = useState("");
  const [applicationStatus, setApplicationStatus] = useState<"nova" | "rascunho" | "finalizada">("nova");
  const [states, setStates] = useState<FormState>(EMPTY_STATE);

  const totalScore = useMemo(
    () =>
      ITEMS.reduce((sum, [key]) => sum + (Number(states[key].score) || 0), 0).toFixed(1),
    [states],
  );

  const completedItems = useMemo(
    () => ITEMS.filter(([key]) => states[key].score !== "").length,
    [states],
  );

  useEffect(() => {
    async function loadApplication() {
      if (!applicationId) {
        setLoading(false);
        return;
      }

      try {
        const result = await api.get<any>(`/api/tests/applications/${applicationId}`);
        if (result?.patient_name) setPatientName(result.patient_name);
        setApplicationStatus(result?.is_validated ? "finalizada" : result?.raw_payload ? "rascunho" : "nova");

        if (result?.is_validated && searchParams.get("edit") !== "true") {
          const evalQuery = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : "";
          router.replace(`/dashboard/tests/cars2-hf/${applicationId}/result${evalQuery}`);
          return;
        }

        const rawItems = result?.raw_payload?.items || {};
        const nextState = { ...EMPTY_STATE };
        for (const [key] of ITEMS) {
          nextState[key] = {
            score: rawItems[key]?.score !== undefined ? normalizeScore(rawItems[key].score) : "",
            observations: rawItems[key]?.observations || "",
          };
        }
        setStates(nextState);
      } catch (err) {
        console.error("Erro ao carregar aplicação:", err);
      } finally {
        setLoading(false);
      }
    }

    loadApplication();
  }, [applicationId, router, searchParams]);

  const updateItem = (key: ItemKey, field: keyof ItemState, value: string) => {
    setStates((prev) => ({
      ...prev,
      [key]: { ...prev[key], [field]: value },
    }));
  };

  const handleSave = async () => {
    if (!evaluationId) {
      setError("evaluation_id não encontrado na URL.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      const payload = {
        evaluation_id: Number(evaluationId),
        applied_on: undefined,
        items: Object.fromEntries(
          ITEMS.map(([key]) => [
            key,
            {
              score: Number(SCORE_MAP[states[key].score as (typeof SCORE_OPTIONS)[number]] || 0),
              observations: states[key].observations,
            },
          ]),
        ),
      };

      const result = await api.post<{ application_id: number }>("/api/tests/cars2-hf/submit", payload);
      router.push(`/dashboard/tests/cars2-hf/${result.application_id}/result?evaluation_id=${evaluationId}`);
    } catch (err: any) {
      setError(err?.message || "Erro ao salvar CARS2-HF.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div className="py-16 text-center text-slate-500">Carregando CARS2-HF...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full border border-slate-200 bg-white shadow-sm">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">CARS2 – HF</h2>
          <p className="text-sm text-slate-500">Childhood Autism Rating Scale, Second Edition, High Functioning Version</p>
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
            {patientName ? `Paciente: ${patientName}` : "Preencha os 15 itens do protocolo."}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <User className="h-4 w-4" />
                Paciente
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{patientName || "Não informado"}</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <ClipboardList className="h-4 w-4" />
                Aplicação
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{applicationId ? `#${applicationId}` : "Nova"}</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <CheckCircle2 className="h-4 w-4" />
                Status
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">
                {applicationStatus === "finalizada" ? "Finalizada" : applicationStatus === "rascunho" ? "Rascunho" : "Nova"}
              </div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">
                <Sigma className="h-4 w-4" />
                Total
              </div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{totalScore}</div>
            </div>
          </div>

          <div className="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
            <div className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-4 text-sm leading-6 text-amber-900">
              <div className="mb-2 font-semibold">Orientação clínica</div>
              Protocolo destinado à versão de alto funcionamento. Verificar compatibilidade com o perfil cognitivo do examinando e priorizar registros observacionais quando houver discrepância entre pontuações e comportamento clínico.
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white px-4 py-4">
              <div className="text-sm font-semibold text-slate-900">Progresso</div>
              <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-100">
                <div
                  className="h-full rounded-full bg-indigo-600 transition-all"
                  style={{ width: `${(completedItems / ITEMS.length) * 100}%` }}
                />
              </div>
              <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                <span>{completedItems} de {ITEMS.length} itens preenchidos</span>
                <span>{Math.round((completedItems / ITEMS.length) * 100)}%</span>
              </div>
            </div>
          </div>

          <div className="grid gap-3 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-white p-4">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">1 = 1</div>
              <div className="mt-1 text-sm text-slate-700">Faixa discreta / menor presença do indicador</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-4">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">2 = 1.5</div>
              <div className="mt-1 text-sm text-slate-700">Faixa intermediária / observação clínica relevante</div>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-white p-4">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">3 = 2.5 · 4 = 3.5</div>
              <div className="mt-1 text-sm text-slate-700">Maior comprometimento / impacto funcional mais amplo</div>
            </div>
          </div>

          <div className="grid gap-4">
            {ITEMS.map(([key, label]) => (
              <div key={key} className="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-3">
                <div className="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
                  <div className="text-sm font-medium text-slate-900">{label}</div>
                  <div className="text-xs text-slate-500">Selecione a pontuação e adicione observações, se necessário.</div>
                </div>
                <div className="flex flex-wrap gap-2">
                  {SCORE_OPTIONS.map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => updateItem(key, "score", option)}
                      className={`rounded-full px-3 py-1.5 text-sm border transition ${states[key].score === option ? "border-indigo-600 bg-indigo-600 text-white" : "border-slate-300 bg-white text-slate-700"}`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
                <div className="text-xs text-slate-500">Escala: 1 = 1, 2 = 1.5, 3 = 2.5, 4 = 3.5</div>
                <textarea
                  className="min-h-20 w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-indigo-500"
                  placeholder="Observações clínicas, exemplos comportamentais ou contexto"
                  value={states[key].observations}
                  onChange={(e) => updateItem(key, "observations", e.target.value)}
                />
              </div>
            ))}
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-4 flex items-center justify-between">
            <div>
              <div className="text-sm text-slate-500">Escore bruto parcial</div>
              <div className="text-2xl font-semibold text-slate-900">{totalScore}</div>
            </div>
            <Button onClick={handleSave} disabled={saving} className="gap-2 rounded-xl">
              <Save className="h-4 w-4" />
              {saving ? "Salvando..." : "Salvar"}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default function CARS2HFPage() {
  return <CARS2HFPageContent />;
}
