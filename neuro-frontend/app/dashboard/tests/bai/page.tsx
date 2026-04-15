"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

const BAI_ITEMS = [
  "Dormência ou formigamento",
  "Sensação de calor",
  "Tremores nas pernas",
  "Incapaz de relaxar",
  "Medo que aconteça o pior",
  "Atordoado ou tonto",
  "Palpitação ou aceleração do coração",
  "Sem equilíbrio",
  "Aterrorizado",
  "Nervoso",
  "Sensação de sufocação",
  "Tremores nas mãos",
  "Trêmulo",
  "Medo de perder o controle",
  "Dificuldade de respirar",
  "Medo de morrer",
  "Assustado",
  "Indigestão ou desconforto no abdômen",
  "Sensação de desmaio",
  "Rosto afogueado",
  "Suor (não devido ao calor)",
];

const RESPONSE_OPTIONS = {
  0: "Absolutamente não",
  1: "Levemente: Não me incomodou muito",
  2: "Moderadamente: Foi muito desagradável, mas pude suportar",
  3: "Gravemente: Dificilmente pude suportar",
};

function BAITestPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [scores, setScores] = useState<Record<string, string>>({});
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loadingEvaluation, setLoadingEvaluation] = useState(true);

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const isEditMode = searchParams.get("edit") === "true";

  useEffect(() => {
    async function fetchEvaluation() {
      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result && result.evaluation_id && !evaluationId) {
            const newEvalId = result.evaluation_id.toString();
            router.replace(`/dashboard/tests/bai?application_id=${applicationId}&evaluation_id=${newEvalId}&edit=true`)
            return
          }
          if (result && result.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : ""
            router.push(`/dashboard/tests/bai/${applicationId}/result${resultEvaluationId}`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingScores: Record<string, string> = {}
            for (let i = 1; i <= 21; i++) {
              const paddedKey = `item_${i.toString().padStart(2, '0')}`
              const unpaddedKey = `item_${i}`

              if (raw[paddedKey] !== undefined) {
                existingScores[unpaddedKey] = String(raw[paddedKey])
              } else if (raw[unpaddedKey] !== undefined) {
                existingScores[unpaddedKey] = String(raw[unpaddedKey])
              }
            }
            if (Object.keys(existingScores).length > 0) {
              setScores(existingScores)
            }
          }
        } catch (error) {
          console.log("Teste não encontrado, redirecionando para formulário...")
        }
      }

      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
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
  }, [evaluationId, applicationId, isEditMode, router]);

  const clearForm = () => {
    if (confirm("Deseja realmente limpar todos os campos do formulário?")) {
      setScores({});
    }
  };

  const handleScoreChange = (item: number, value: string) => {
    const num = parseInt(value);
    if (value === "" || (!isNaN(num) && num >= 0 && num <= 3)) {
      setScores({ ...scores, [`item_${item}`]: value });
    }
  };

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }

    const payload: Record<string, unknown> = {
      evaluation_id: parseInt(evaluationId),
    };

    for (let i = 1; i <= 21; i++) {
      const key = `item_${i}`;
      const paddedKey = `item_${i.toString().padStart(2, '0')}`;
      payload[paddedKey] = parseInt(scores[key]) || 0;
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/bai/submit', payload);
      router.push(`/dashboard/tests/bai/${result.application_id}/result?evaluation_id=${evaluationId}`);
    } catch (error: any) {
      console.error('Erro:', error);
      alert('Erro ao salvar: ' + (error?.message || 'Tente novamente'));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">BAI</h2>
          <p className="text-sm text-slate-500">Inventário de Ansiedade de Beck</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Dados da aplicação
              {isEditMode && <Badge variant="outline" className="text-amber-600 border-amber-200 bg-amber-50">Modo Edição</Badge>}
            </CardTitle>
            <CardDescription>Preencha as respostas do paciente para cada sintoma.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {loadingEvaluation ? (
              <div className="text-center py-4 text-slate-500">Carregando dados do paciente...</div>
            ) : evaluation ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Paciente</label>
                  <div className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700 font-medium">
                    {evaluation.patient_name}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Data de nascimento</label>
                  <div className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                    {evaluation.patient_birth_date || "—"}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-4 text-red-500">Avaliação não encontrada</div>
            )}

            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de resposta:</p>
              <div className="grid grid-cols-2 gap-2">
                <span><strong>0</strong> = {RESPONSE_OPTIONS[0]}</span>
                <span><strong>1</strong> = {RESPONSE_OPTIONS[1]}</span>
                <span><strong>2</strong> = {RESPONSE_OPTIONS[2]}</span>
                <span><strong>3</strong> = {RESPONSE_OPTIONS[3]}</span>
              </div>
            </div>

            <div className="border rounded-xl overflow-hidden">
              <div className="grid grid-cols-[60px_1fr_80px] bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                <div>Item</div>
                <div>Descrição</div>
                <div className="text-center">Resp.</div>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                {BAI_ITEMS.map((text, idx) => (
                  <div
                    key={idx}
                    className={`grid grid-cols-[60px_1fr_80px] items-center px-4 py-3 border-t ${
                      idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"
                    }`}
                  >
                    <div className="text-sm font-medium text-slate-900">{String(idx + 1).padStart(2, "0")}</div>
                    <div className="text-sm text-slate-700 pr-4">{text}</div>
                    <div className="flex justify-center">
                      <input
                        type="text"
                        inputMode="numeric"
                        maxLength={1}
                        className="h-8 w-16 rounded-lg text-center border border-slate-200 focus:ring-2 focus:ring-primary/20 focus:border-primary outline-none transition-all"
                        value={scores[`item_${idx + 1}`] || ""}
                        onChange={(e) => handleScoreChange(idx + 1, e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            const nextInput = document.querySelector(`input[id="input-item-${idx + 2}"]`) as HTMLInputElement;
                            nextInput?.focus();
                          }
                        }}
                        id={`input-item-${idx + 1}`}
                        placeholder="0-3"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              <Button className="rounded-xl gap-2" onClick={handleSave}>
                <Save className="h-4 w-4" />
                {isEditMode ? "Salvar Alterações" : "Salvar aplicação"}
              </Button>
              <Button variant="outline" className="rounded-xl text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200" onClick={clearForm}>
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
              <p className="font-medium text-slate-900">BAI - Beck Anxiety Inventory</p>
              <p>Inventário de Ansiedade de Beck</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>21 itens com escala de 4 pontos (0-3)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Escore total</p>
              <p>Faixa de 0 a 63 pontos</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Classificação</p>
              <div className="flex flex-wrap gap-1 mt-2">
                <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200">Mínimo (0-10)</Badge>
                <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">Leve (11-19)</Badge>
                <Badge variant="outline" className="bg-yellow-50 text-yellow-700 border-yellow-200">Moderado (20-30)</Badge>
                <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200">Grave (31-63)</Badge>
              </div>
            </div>
            <div>
              <p className="font-medium text-slate-900">Objetivo</p>
              <p>Avaliar a intensidade de sintomas ansiosos somáticos e cognitivos</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function BAITestPageFallback() {
  return <div className="space-y-6" />;
}

export default function BAITestPage() {
  return (
    <Suspense fallback={<BAITestPageFallback />}>
      <BAITestPageContent />
    </Suspense>
  );
}
