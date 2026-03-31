"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Save } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

const STAGES = [
  { code: "leitura", label: "Leitura" },
  { code: "contagem", label: "Contagem" },
  { code: "escolha", label: "Escolha" },
  { code: "alternancia", label: "Alternância" },
] as const;

type StageCode = (typeof STAGES)[number]["code"];

type StageState = {
  tempo: string;
  erros: string;
};

type FormState = Record<StageCode, StageState>;

const EMPTY_STATE: FormState = {
  leitura: { tempo: "", erros: "0" },
  contagem: { tempo: "", erros: "0" },
  escolha: { tempo: "", erros: "0" },
  alternancia: { tempo: "", erros: "0" },
};

function FDTPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [scores, setScores] = useState<FormState>(EMPTY_STATE);
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loadingEvaluation, setLoadingEvaluation] = useState(true);

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const isEditMode = searchParams.get("edit") === "true";

  useEffect(() => {
    async function fetchEvaluation() {
      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`);
          if (result && result.is_validated && !isEditMode) {
            router.push(`/dashboard/tests/fdt/${applicationId}/result`);
            return;
          }
          if (result && result.raw_payload) {
            setScores({
              leitura: {
                tempo: String(result.raw_payload.leitura?.tempo ?? ""),
                erros: String(result.raw_payload.leitura?.erros ?? 0),
              },
              contagem: {
                tempo: String(result.raw_payload.contagem?.tempo ?? ""),
                erros: String(result.raw_payload.contagem?.erros ?? 0),
              },
              escolha: {
                tempo: String(result.raw_payload.escolha?.tempo ?? ""),
                erros: String(result.raw_payload.escolha?.erros ?? 0),
              },
              alternancia: {
                tempo: String(result.raw_payload.alternancia?.tempo ?? ""),
                erros: String(result.raw_payload.alternancia?.erros ?? 0),
              },
            });
          }
        } catch (error) {
          console.log("Teste não encontrado, redirecionando para formulário...");
        }
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${evaluationId}`);
        setEvaluation(data);
      } catch (error: any) {
        console.error("Erro ao buscar avaliação:", error);
      } finally {
        setLoadingEvaluation(false);
      }
    }

    fetchEvaluation();
  }, [applicationId, evaluationId, isEditMode, router]);

  const updateStage = (stage: StageCode, field: keyof StageState, value: string) => {
    setScores((prev) => ({
      ...prev,
      [stage]: {
        ...prev[stage],
        [field]: value,
      },
    }));
  };

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }

    const payload = {
      evaluation_id: parseInt(evaluationId, 10),
      leitura: {
        tempo: parseFloat(scores.leitura.tempo.replace(",", ".")) || 0,
        erros: parseInt(scores.leitura.erros, 10) || 0,
      },
      contagem: {
        tempo: parseFloat(scores.contagem.tempo.replace(",", ".")) || 0,
        erros: parseInt(scores.contagem.erros, 10) || 0,
      },
      escolha: {
        tempo: parseFloat(scores.escolha.tempo.replace(",", ".")) || 0,
        erros: parseInt(scores.escolha.erros, 10) || 0,
      },
      alternancia: {
        tempo: parseFloat(scores.alternancia.tempo.replace(",", ".")) || 0,
        erros: parseInt(scores.alternancia.erros, 10) || 0,
      },
    };

    try {
      const result = await api.post<{ application_id: number }>("/api/tests/fdt/submit", payload);
      router.push(`/dashboard/tests/fdt/${result.application_id}/result`);
    } catch (error: any) {
      console.error("Erro:", error);
      alert("Erro ao salvar: " + (error?.message || "Tente novamente"));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">FDT</h2>
          <p className="text-sm text-slate-500">Five Digits Test</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Dados da aplicação</CardTitle>
            <CardDescription>Informe o tempo e os erros de cada etapa do FDT.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {loadingEvaluation ? (
              <div className="py-4 text-center text-slate-500">Carregando dados do paciente...</div>
            ) : evaluation ? (
              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Paciente</label>
                  <div className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                    {evaluation.patient_name}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Data de nascimento</label>
                  <div className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                    {evaluation.patient_birth_date || "—"}
                  </div>
                </div>
              </div>
            ) : (
              <div className="py-4 text-center text-red-500">Avaliação não encontrada</div>
            )}

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {STAGES.map((stage) => (
                <div key={stage.code} className="rounded-xl bg-slate-50 p-4 space-y-4">
                  <h3 className="font-medium text-slate-900">{stage.label}</h3>
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <label className="text-xs text-slate-600">Tempo (segundos)</label>
                      <Input
                        type="number"
                        step="0.01"
                        min="0"
                        className="rounded-lg"
                        value={scores[stage.code].tempo}
                        onChange={(e) => updateStage(stage.code, "tempo", e.target.value)}
                        placeholder="0.00"
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs text-slate-600">Erros</label>
                      <Input
                        type="number"
                        min="0"
                        className="rounded-lg"
                        value={scores[stage.code].erros}
                        onChange={(e) => updateStage(stage.code, "erros", e.target.value)}
                        placeholder="0"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex gap-2">
              <Button className="rounded-xl gap-2" onClick={handleSave}>
                <Save className="h-4 w-4" />
                Salvar aplicação
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
              <p className="font-medium text-slate-900">FDT</p>
              <p>Five Digits Test com normas por faixa etária.</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Etapas</p>
              <ul className="list-inside list-disc space-y-1">
                <li>Leitura</li>
                <li>Contagem</li>
                <li>Escolha</li>
                <li>Alternância</li>
              </ul>
            </div>
            <div>
              <p className="font-medium text-slate-900">Índices derivados</p>
              <p>Inibição = Escolha - Leitura; Flexibilidade = Alternância - Leitura.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function FDTPageFallback() {
  return <div className="space-y-6" />;
}

export default function FDTPage() {
  return (
    <Suspense fallback={<FDTPageFallback />}>
      <FDTPageContent />
    </Suspense>
  );
}
