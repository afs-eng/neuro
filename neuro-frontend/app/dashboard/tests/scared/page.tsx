"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

const PERGUNTAS = [
  "Quando eu fico com medo, eu tenho dificuldade de respirar.",
  "Eu sinto dor de cabeça quando estou na escola.",
  "Eu não gosto de estar com pessoas que não conheço bem.",
  "Fico com medo quando durmo fora de casa.",
  "Eu me preocupo se outras pessoas gosta de mim.",
  "Quando eu fico com medo, eu sinto como se eu fosse desmaiar.",
  "Eu sou nervoso(a).",
  "Eu sigo a minha mãe ou o meu pai aonde eles vão.",
  "As pessoas me dizem que pareço nervoso(a).",
  "Eu fico nervoso(a) com pessoas que eu não conheço bem.",
  "Eu tenho dor de barriga na escola.",
  "Quando eu fico com medo, eu acho que vou enlouquecer.",
  "Eu tenho medo de dormir sozinho(a).",
  "Eu me preocupo em ser tão bom quanto as outras crianças.",
  "Quando eu fico com medo, tenho a impressão de que as coisas não são reais.",
  "Eu tenho pesadelos com coisas ruins acontecendo com os meus pais.",
  "Eu fico preocupo quando tenho que ir à escola.",
  "Quando eu fico com medo, o meu coração bate rápido.",
  "Quando eu fico nervoso(a), eu tremo de medo.",
  "Eu tenho pesadelos com alguma coisa ruim acontecendo comigo.",
  "Eu fico preocupado(a) se as coisas vão dar certo para mim.",
  "Quando eu fico com medo, eu suo muito.",
  "Eu sou muito preocupado(a).",
  "Eu fico com muito medo sem nenhum motivo.",
  "Eu tenho medo de ficar sozinho(a) em casa.",
  "Eu tenho dificuldades para falar com pessoas que não conheço bem.",
  "Quando eu fico com medo, eu me sinto sufocado.",
  "As pessoas dizem que eu me preocupo demais.",
  "Eu não gosto de ficar longe da família.",
  "Eu tenho medo de ter ataques de ansiedade (ou ataques de pânico).",
  "Eu tenho medo de que alguma coisa ruim aconteça com meus pais.",
  "Eu fico com vergonha na frente de pessoas que não conhecer bem.",
  "Eu me preocupo muito com o que vai acontecer no futuro.",
  "Quando eu fico com medo, eu tenho vontade de vomitar.",
  "Eu me preocupo muito em fazer as coisas bem feitas.",
  "Eu tenho medo de ir à escola.",
  "Eu me preocupo com as coisas que já aconteceram.",
  "Quando eu fico com medo, eu me sinto tonto(a).",
  "Fico nervoso(a) quando estou com outras crianças ou adultos e tenho que fazer algo enquanto eles me olham (por exemplo, ler em voz alta, falar, jogar um jogo ou praticar um esporte).",
  "Eu fico nervoso(a) para ir a festas, bailes ou qualquer lugar onde estejam pessoas que não conheço bem.",
  "Eu sou tímido(a).",
];

function SCAREDTestPageContent() {
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
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`);
          if (result && result.evaluation_id && !evaluationId) {
            const newEvalId = result.evaluation_id.toString();
            router.replace(`/dashboard/tests/scared?application_id=${applicationId}&evaluation_id=${newEvalId}&edit=true`);
            return;
          }
          if (result && result.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : "";
            router.push(`/dashboard/tests/scared/${applicationId}/result${resultEvaluationId}`);
            return;
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload;
            const existingScores: Record<string, string> = {};
            const responses = raw.responses || {};
            for (let i = 1; i <= 41; i++) {
              const key = String(i);
              if (responses[key] !== undefined) {
                existingScores[key] = String(responses[key]);
              }
            }
            setScores(existingScores);
          }
        } catch (error) {
          console.log("Teste não encontrado, redirecionando para formulário...");
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

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }

    const calcAge = evaluation?.patient_birth_date
      ? Math.floor((new Date().getTime() - new Date(evaluation.patient_birth_date).getTime()) / (365.25 * 24 * 60 * 60 * 1000))
      : 10;

    const responseObj: Record<string, number> = {};
    for (let i = 1; i <= 41; i++) {
      const key = String(i);
      responseObj[key] = parseInt(scores[key]) || 0;
    }

    const payload = {
      evaluation_id: parseInt(evaluationId),
      form: "child",
      gender: evaluation?.patient_sex || "M",
      age: calcAge,
      responses: responseObj,
    };

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/scared/submit', payload);
      router.push(`/dashboard/tests/scared/${result.application_id}/result?evaluation_id=${evaluationId}`);
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
          <h2 className="text-2xl font-semibold text-slate-900">SCARED</h2>
          <p className="text-sm text-slate-500">Screen for Child Anxiety Related Emotional Disorders</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Itens do instrumento
              {isEditMode && <Badge variant="outline" className="text-amber-600 border-amber-200 bg-amber-50">Modo Edição</Badge>}
            </CardTitle>
            <CardDescription>Marque a frequência para cada item.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de frequência:</p>
              <div className="grid grid-cols-3 gap-2">
                <span>0 = Nunca ou raramente verdadeiro</span>
                <span>1 = Algumas vezes verdadeiro</span>
                <span>2 = Bastante ou frequentemente verdadeiro</span>
              </div>
            </div>

            <div className="border rounded-xl overflow-hidden">
              <div className="grid grid-cols-[60px_1fr_80px] bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                <div>Item</div>
                <div>Descrição</div>
                <div className="text-center">Resp.</div>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                {PERGUNTAS.map((text, idx) => (
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
                        value={scores[`${idx + 1}`] || ""}
                        onChange={(e) => {
                          const val = e.target.value;
                          if (val === "" || ["0", "1", "2"].includes(val)) {
                            setScores({ ...scores, [`${idx + 1}`]: val });
                          }
                        }}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            const nextId = `input-item-${idx + 2}`;
                            document.getElementById(nextId)?.focus();
                          }
                        }}
                        id={`input-item-${idx + 1}`}
                        placeholder="0-2"
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex gap-2">
              <Button className="rounded-xl gap-2 bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-100 transition-all font-bold" onClick={handleSave}>
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
              <p className="font-medium text-slate-900">SCARED</p>
              <p>Screen for Child Anxiety Related Emotional Disorders</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>41 itens com escala Likert de 3 pontos</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Aplicação</p>
              <p>Autorrelato (criança/adolescente)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function SCAREDTestPageFallback() {
  return <div className="space-y-6" />;
}

export default function SCAREDTestPage() {
  return (
    <Suspense fallback={<SCAREDTestPageFallback />}>
      <SCAREDTestPageContent />
    </Suspense>
  );
}