"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

const EPQJ_ITEMS = [
  "Alguma vez você já foi dormir sem escovar os dentes?",
  "Você já chorou quando alguém riu de você na frente de outras pessoas?",
  "Você se diverte com piadas que, às vezes, incomodam os outros?",
  "Você sempre faz imediatamente o que lhe pedem?",
  "Quando vai dormir, você tem pensamentos que lhe tiram o sono?",
  "No colégio, você sempre cumpre tudo o que lhe dizem e mandam?",
  "Você gostaria que outros colegas tivessem medo de você?",
  "Você é muito alegre e animado(a)?",
  "Há muitas coisas que incomodam você?",
  "Você acha engraçado quando um colega cai e se machuca?",
  "Você tem muitos amigos?",
  "Alguma vez você se sentiu triste sem nenhum motivo?",
  "Às vezes, você gosta de provocar e irritar os animais?",
  "Alguma vez você fingiu que não ouviu quando alguém o(a) chamou?",
  "Com frequência você pensa que a vida é muito triste?",
  "Você frequentemente discute com seus colegas?",
  "Em casa, você sempre acaba os deveres antes de sair para se diverte?",
  "Você se preocupa com coisas ruins que possam acontecer no futuro?",
  "Alguma vez você já substituiu o almoço por um hambúrguer?",
  "Você se sente facilmente magoado(a) quando as pessoas encontram falhas em seu comportamento ou trabalho?",
  "Você se assusta ao ver um acidente de carro com vítimas na rua?",
  "Alguém quer se vingar de você por causa de alguma brincadeira de mau gosto que você fez gratuitamente?",
  "Você acha que deve ser muito divertido saltar de uma cachoeira?",
  "Você se sente frequentemente cansado(a) sem motivo?",
  "Em geral, você acha divertido incomodar as pessoas?",
  "Você sempre fica calado(a) quando as pessoas mais velhas estão falando?",
  "Em geral, é você quem dá o primeiro passo para fazer um novo(a) amigo(a)?",
  "Você sempre encontra defeito em qualquer coisa que faça?",
  "Você acredita que se envolve em mais brigas que as outras pessoas?",
  "Alguma vez você disse um palavrão ou insultou alguém?",
  "Você gosta de contar piadas ou historinhas divertidas para seus amigos?",
  "Em sala de aula, você entra em mais confusões ou problemas que os outros colegas?",
  "Em geral, você recolhe do chão os papéis ou a sujeira que os colegas atiram na sala de aula?",
  "Você tem muitos passatempos ou se interessa por muitas coisas diferentes?",
  "Algumas coisas facilmente o(a) magoam ou o(a) deixa triste?",
  "Você gosta de debochar ou pregar peça nos outros?",
  "Alguma vez você desobedeceu a seus pais?",
  "Frequentemente você se sente 'cansado(a) de tudo'?",
  "Às vezes, é bastante divertido ver como um grupo de meninos mais velhos incomoda ou assusta um menino menor?",
  "Você sempre se comporta bem em sala de aula, mesmo que o professor não esteja nela?",
  "Quando uma pessoa o critica, você passa muito tempo pensando no que ela disse?",
  "Você acha que quando alguém nos provoca é melhor brigar que conversar?",
  "Você sempre diz a verdade?",
  "Você gosta de estar com outros colegas e se divertir com eles?",
  "Você gostaria de pular de paraquedas?",
  "Você sempre come tudo o que lhe põem no prato?",
  "Sempre que alguém o(a) corrige na frente dos seus amigos ou familiares, você se sente envergonhado(a) ou magoado(a)?",
  "Você alguma vez foi atrevido(a) com seus pais?",
  "Você tem dificuldade de prestar atenção nas aulas da escola quando tem problemas em casa?",
  "Você gosta de se jogar ou pular na água em uma piscina ou no mar?",
  "Quando você está preocupado(a) com alguma coisa, tem dificuldade de dormir à noite?",
  "As outras pessoas pensam que você é muito alegre e animado(a)?",
  "Frequentemente você se sente sozinho(a)?",
  "Você acha que uma criança de 6 anos deve ser protegida quando é agressiva por um adolescente?",
  "Você faz tudo o que seus pais lhe pedem?",
  "Você gosta muito de passear?",
  "Alguma vez você já deixou de fazer o dever de casa para assistir à televisão?",
  "Algumas vezes você se sente alegre, outras vezes se sente triste, sem nenhum motivo?",
  "Com frequência você precisa de bons amigos que lhe compreendam e animem?",
  "Você gostaria de participar de um treinamento de sobrevivência na selva?",
];

const ITENS_EPQJ = {
  P: [3, 7, 10, 13, 16, 21, 22, 25, 29, 32, 36, 39, 42, 54],
  E: [8, 11, 23, 27, 31, 34, 44, 45, 50, 52, 56, 60],
  N: [2, 5, 9, 12, 15, 18, 20, 24, 28, 35, 38, 41, 47, 49, 51, 53, 58, 59],
  S: [1, 4, 6, 14, 17, 19, 26, 30, 33, 37, 40, 43, 46, 48, 55, 57],
};

function calcularEscores(respostas: Record<string, string>) {
  const escores: Record<string, number> = { P: 0, E: 0, N: 0, S: 0 };
  for (const [fator, itens] of Object.entries(ITENS_EPQJ)) {
    for (const item of itens) {
      const key = `item_${item}`;
      if (respostas[key] === "1") {
        escores[fator]++;
      }
    }
  }
  return escores;
}

function EPQJTestPageContent() {
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
      let currentEvalId = evaluationId;

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result && result.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : ""
            router.push(`/dashboard/tests/epq-j/${applicationId}/result${resultEvaluationId}`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload;
            const newScores: Record<string, string> = {};
            for (let i = 1; i <= 60; i++) {
              const paddedKey = `item_${i.toString().padStart(2, '0')}`;
              const unpaddedKey = `item_${i}`;
              if (raw[paddedKey] !== undefined) {
                newScores[unpaddedKey] = String(raw[paddedKey]);
              } else if (raw[unpaddedKey] !== undefined) {
                newScores[unpaddedKey] = String(raw[unpaddedKey]);
              }
            }
            setScores(newScores);
          }
          if (result && result.evaluation_id && !currentEvalId) {
            currentEvalId = String(result.evaluation_id);
          }
        } catch (error) {
          console.log("Teste não encontrado, redirecionando para formulário...")
        }
      }

      if (!currentEvalId) {
        setLoadingEvaluation(false);
        return;
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${currentEvalId}`);
        setEvaluation(data);
      } catch (error: any) {
        console.error("Erro ao buscar avaliação:", error);
      } finally {
        setLoadingEvaluation(false);
      }
    }
    fetchEvaluation();
  }, [evaluationId, applicationId, isEditMode, router]);

  const handleScoreChange = (item: number, value: string) => {
    if (value === "" || value === "0" || value === "1") {
      setScores({ ...scores, [`item_${item}`]: value });
    }
  };

  const clearForm = () => {
    if (confirm("Deseja realmente limpar todos os campos do formulário?")) {
      setScores({});
    }
  };

  const handleSave = async () => {
    const evalId = evaluationId || evaluation?.id;
    if (!evalId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }
    
    const escores = calcularEscores(scores);
    const sexo = evaluation?.patient_sex || "M";
    
    const payload: Record<string, unknown> = {
      evaluation_id: parseInt(evalId),
      sexo: sexo,
    };
    
    // Adiciona os itens (Garantindo formato item_01 no payload para o backend)
    for (let i = 1; i <= 60; i++) {
      const paddedKey = `item_${i.toString().padStart(2, '0')}`;
      const unpaddedKey = `item_${i}`;
      payload[paddedKey] = parseInt(scores[unpaddedKey]) || 0;
    }
    
    try {
      const result = await api.post<{ application_id: number; escore_bruto: any; resultados: any }>('/api/tests/epq-j/submit', payload);
      
      // Passa os dados via query params para a página de resultado
      const params = new URLSearchParams({
        evaluation_id: String(evaluation?.id || evalId || ""),
        paciente: String(evaluation?.patient_id || ""),
        nome: evaluation?.patient_name || "",
        sexo: sexo,
        p: escores.P.toString(),
        e: escores.E.toString(),
        n: escores.N.toString(),
        s: escores.S.toString(),
        app_id: result.application_id.toString(),
      });
      
      // Adiciona as respostas dos itens
      for (let i = 1; i <= 60; i++) {
        const key = `item_${i}`;
        if (scores[key] !== undefined) {
          params.set(`r${i}`, scores[key]);
        }
      }
      
      router.push(`/dashboard/tests/epq-j/${result.application_id}/result?${params.toString()}`);
    } catch (error: any) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao salvar teste: ' + (error?.message || 'Tente novamente'));
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">EPQ-J</h2>
          <p className="text-sm text-slate-500">Questionário de Personalidade para Crianças e Adolescentes</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Dados da aplicação
              {isEditMode && <Badge variant="outline" className="text-amber-600 border-amber-200 bg-amber-50">Modo Edição</Badge>}
            </CardTitle>
            <CardDescription>Preencha as respostas do paciente.</CardDescription>
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
                  <label className="text-sm font-medium text-slate-700">Sexo</label>
                  <div className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                    {evaluation.patient_sex === "M" ? "Masculino" : evaluation.patient_sex === "F" ? "Feminino" : "—"}
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-4 text-red-500">Avaliação não encontrada</div>
            )}

            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de resposta:</p>
              <div className="grid grid-cols-2 gap-2">
                <span><strong>1</strong> = Sim</span>
                <span><strong>0</strong> = Não</span>
              </div>
            </div>

            <div className="border rounded-xl overflow-hidden">
              <div className="grid grid-cols-[60px_1fr_80px] bg-slate-100 px-4 py-2 text-sm font-medium text-slate-700">
                <div>Item</div>
                <div>Descrição</div>
                <div className="text-center">Resp.</div>
              </div>
              <div className="max-h-[500px] overflow-y-auto">
                {EPQJ_ITEMS.map((text, idx) => (
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
                        onChange={(e) => handleScoreChange(idx + 1, e.target.value)}
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
              <p className="font-medium text-slate-900">EPQ-J</p>
              <p>Questionário de Personalidade para Crianças e Adolescentes</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Fatores</p>
              <div className="flex flex-wrap gap-1 mt-2">
                <Badge>P - Psicoticismo</Badge>
                <Badge>E - Extroversão</Badge>
                <Badge>N - Neuroticismo</Badge>
                <Badge>S - Socialização</Badge>
              </div>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>60 itens com resposta binária (Sim/Não)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Normas</p>
              <p>Separadas por sexo (M/F)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function EPQJTestPageFallback() {
  return <div className="space-y-6" />;
}

export default function EPQJTestPage() {
  return (
    <Suspense fallback={<EPQJTestPageFallback />}>
      <EPQJTestPageContent />
    </Suspense>
  );
}
