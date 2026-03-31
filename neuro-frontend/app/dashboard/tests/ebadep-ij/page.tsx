"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { api } from "@/lib/api";

const QUESTIONS = [
  "Humor deprimido",
  "Perda ou diminuição de prazer",
  "Choro",
  "Desesperança",
  "Desamparo",
  "Indecisão",
  "Sentimento de incapacidade",
  "Sentimentos de inadequação",
  "Inutilidade",
  "Carência/dependência",
  "Negativismo",
  "Esquiva de situações sociais",
  "Queda de rendimento na escola",
  "Autocrítica exacerbada",
  "Culpa",
  "Diminuição de concentração",
  "Pensamento de morte",
  "Autoestima rebaixada",
  "Falta de perspectiva sobre o presente",
  "Falta de perspectiva sobre o futuro (desesperança)",
  "Alteração de apetite",
  "Alteração de peso",
  "Insônia/hipersonia",
  "Lentidão/agitação psicomotora",
  "Fadiga/perda de energia",
  "Sintomas físicos (ex.: dores)",
  "Irritação",
];

function EBADEPIJTestPageContent() {
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
      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result && result.is_validated && !isEditMode) {
            router.push(`/dashboard/tests/ebadep-ij/${applicationId}/result`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingScores: Record<string, string> = {}
            for (let i = 1; i <= 27; i++) {
              const key = `item_${i.toString().padStart(2, '0')}`
              if (raw[key] !== undefined) {
                existingScores[`item_${i}`] = String(raw[key])
              }
            }
            setScores(existingScores)
          }
        } catch (error) {
          console.log("Teste não encontrado, redirecionando para formulário...")
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
  }, [evaluationId, applicationId, isEditMode, router]);

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }
    const payload: Record<string, unknown> = {
      evaluation_id: parseInt(evaluationId),
    };
    
    for (let i = 1; i <= 27; i++) {
      payload[`item_${i.toString().padStart(2, '0')}`] = parseInt(scores[`item_${i}`]) || 0;
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/ebadep-ij/submit', payload);
      alert('EBADEP-IJ salvo com sucesso!');
      router.push(`/dashboard/tests/ebadep-ij/${result.application_id}/result`);
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
          <h2 className="text-2xl font-semibold text-slate-900">EBADEP-IJ</h2>
          <p className="text-sm text-slate-500">Escala Brasileira de Avaliação de Déficits de Atenção e Hiperatividade - Infantojuvenil</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Itens do instrumento</CardTitle>
            <CardDescription>Marque a frequência para cada item.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de frequência:</p>
              <div className="grid grid-cols-3 gap-2">
                <span>0 = Nunca / Poucas vezes</span>
                <span>1 = Algumas vezes</span>
                <span>2 = Muitas vezes / Sempre</span>
              </div>
            </div>

            <div className="border rounded-xl overflow-hidden">
              <div className="grid grid-cols-[60px_1fr_80px] bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                <div>Item</div>
                <div>Descrição</div>
                <div className="text-center">Resp.</div>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                {QUESTIONS.map((text, idx) => (
                  <div
                    key={idx}
                    className={`grid grid-cols-[60px_1fr_80px] items-center px-4 py-3 border-t ${
                      idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"
                    }`}
                  >
                    <div className="text-sm font-medium text-slate-900">{String(idx + 1).padStart(2, "0")}</div>
                    <div className="text-sm text-slate-700 pr-4">{text}</div>
                    <div className="flex justify-center">
                      <Input
                        type="text"
                        inputMode="numeric"
                        maxLength={1}
                        className="h-8 w-16 rounded-lg text-center"
                        value={scores[`item_${idx + 1}`] || ""}
                        onChange={(e) => {
                          const val = e.target.value;
                          if (val === "" || ["0", "1", "2"].includes(val)) {
                            setScores({ ...scores, [`item_${idx + 1}`]: val });
                          }
                        }}
                        placeholder="0-2"
                      />
                    </div>
                  </div>
                ))}
              </div>
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
              <p className="font-medium text-slate-900">EBADEP-IJ</p>
              <p>Escala Brasileira de Avaliação de Déficits de Atenção e Hiperatividade - Versão Infantojuvenil</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>27 itens com escala Likert de 3 pontos</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Aplicação</p>
              <p>Autorrelato ou informant (pais)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function EBADEPIJTestPageFallback() {
  return <div className="space-y-6" />;
}

export default function EBADEPIJTestPage() {
  return (
    <Suspense fallback={<EBADEPIJTestPageFallback />}>
      <EBADEPIJTestPageContent />
    </Suspense>
  );
}
