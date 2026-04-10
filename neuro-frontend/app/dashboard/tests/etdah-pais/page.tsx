"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

const QUESTIONS = [
  // Fator 1 - Regulação Emocional (19 itens)
  "Faz amizade, mas não consegue mantê-las",
  "Implica com tudo",
  "Tem fortes reações emocionais (explosões de raiva)",
  "É irritadiço (Tudo o incomoda)",
  "Muda facilmente de humor",
  "Explode com facilidade (é tipo 'pavio curto')",
  "Da a impressão de estar sempre insatisfeito",
  "É rebelde (Não aceita nada)",
  "É agressivo",
  "Sente-se infeliz",
  "Faz birra quando quer algo",
  "Mostra-se tenso e rígido",
  "Implica com os irmãos",
  "As atividades e reuniões são desagradáveis",
  "Todos têm que fazer o que ele quer",
  "A hora de acordar e das refeições é desagradável",
  "Exige mais tempo e atenção dos pais do que outros filhos",
  "Tem dificuldade para se adaptar às mudanças",
  "É sensível",
  // Fator 2 - Hiperatividade/Impulsividade (13 itens)
  "Movimenta-se muito",
  "É inquieto e agitado",
  "Mexe-se e contorce-se durante as refeições",
  "Tem sempre muita pressa",
  "Age sem pensar (é impulsivo)",
  "É inconsequente",
  "Intromete-se em assuntos que não lhe dizem respeito",
  "Responde antes de ouvir a pergunta inteira",
  "É imprudente",
  "Irrita os outros com suas palhaçadas",
  "Tende a discordar com as regras e normas de jogos",
  "É persistente e insiste diante de uma ideia",
  "Faz os deveres escolares rápido demais",
  // Fator 3 - Comportamento Adaptativo (14 itens - todos invertidos)
  "Aceita facilmente regras, normas e limites",
  "Parece ser uma criança tranquila e sossegada",
  "É tolerante, quando preciso",
  "Respeita normas e regras",
  "É obediente",
  "Obedece aos pais e as normas da casa",
  "Sabe aguardar sua vez (é paciente)",
  "Faz suas tarefas e almoça com bastante tranquilidade",
  "Faz as coisas com muito cuidado",
  "Seu comportamento é adequado socialmente",
  "Fala pouco",
  "A criança permite que o ambiente familiar seja tranquilo",
  "Consegue expressar claramente os seus pensamentos",
  "É atento quando conversa com alguém",
  // Fator 4 - Atenção (12 itens, item 1 invertido)
  "É independente para realizar suas tarefas de casa",
  "É distraído com quase tudo",
  "Evita atividades que exigem esforço mental constante",
  "Esquece rápido o que acabou de ser dito",
  "Inicia uma atividade com entusiasmo e facilmente chega ao final",
  "Tem dificuldade para realizar as coisas importantes",
  "Não termina o que começa",
  "Parece sonhar acordado (estar no mundo da lua)",
  "Mostra-se concentrado, apenas em atividades de seu interesse",
  "Da impressão de que não ouve bem (só escuta o que quer)",
  "Dificilmente observa detalhes",
  "Ocorrem discussões entre os pais e a criança",
];


function ETDAHPAISTestPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [scores, setScores] = useState<Record<string, string>>({});
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loadingEvaluation, setLoadingEvaluation] = useState(true);
  const [sex, setSex] = useState("M");
  
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
            router.replace(`/dashboard/tests/etdah-pais?application_id=${applicationId}&evaluation_id=${newEvalId}&edit=true`)
            return
          }
          if (result && result.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : ""
            router.push(`/dashboard/tests/etdah-pais/${applicationId}/result${resultEvaluationId}`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingScores: Record<string, string> = {}
            for (let i = 1; i <= 58; i++) {
              const paddedKey = `item_${i.toString().padStart(2, '0')}`
              const unpaddedKey = `item_${i}`
              
              if (raw.responses && raw.responses[i] !== undefined) {
                existingScores[unpaddedKey] = String(raw.responses[i])
              } else if (raw.responses && raw.responses[paddedKey] !== undefined) {
                existingScores[unpaddedKey] = String(raw.responses[paddedKey])
              } else if (raw[paddedKey] !== undefined) {
                existingScores[unpaddedKey] = String(raw[paddedKey])
              } else if (raw[unpaddedKey] !== undefined) {
                existingScores[unpaddedKey] = String(raw[unpaddedKey])
              }
            }
            if (Object.keys(existingScores).length > 0) {
              setScores(existingScores)
            }
            if (raw.sex) {
              setSex(raw.sex)
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
    if (value === "" || (!isNaN(num) && num >= 1 && num <= 6)) {
      setScores({ ...scores, [`item_${item}`]: value });
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent, item: number) => {
    if (e.key === "Enter" && item < 58) {
      e.preventDefault();
      const nextInput = document.querySelector(`[data-item="${item + 1}"]`) as HTMLInputElement;
      if (nextInput) nextInput.focus();
    }
  };

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }
    
    const payload: Record<string, unknown> = {
      evaluation_id: parseInt(evaluationId),
      sex: sex,
    };
    
    for (let i = 1; i <= 58; i++) {
      const key = `item_${i}`;
      const paddedKey = `item_${i.toString().padStart(2, '0')}`;
      payload[paddedKey] = parseInt(scores[key]) || 1;
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/etdah-pais/submit', payload);
      router.push(`/dashboard/tests/etdah-pais/${result.application_id}/result?evaluation_id=${evaluationId}`);
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
          <h2 className="text-2xl font-semibold text-slate-900">ETDAH-PAIS</h2>
          <p className="text-sm text-slate-500">Escala de Transtorno de Déficit de Atenção e Hiperatividade - Versão para Pais</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              Dados da aplicação
              {isEditMode && <Badge variant="outline" className="text-amber-600 border-amber-200 bg-amber-50">Modo Edição</Badge>}
            </CardTitle>
            <CardDescription>Preencha as respostas do responsável.</CardDescription>
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

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Sexo da criança</label>
                <select
                  value={sex}
                  onChange={(e) => setSex(e.target.value)}
                  className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700"
                >
                  <option value="M">Masculino</option>
                  <option value="F">Feminino</option>
                </select>
              </div>
            </div>

            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de resposta:</p>
              <div className="grid grid-cols-3 gap-2">
                <span><strong>1</strong> = Nunca</span>
                <span><strong>2-3</strong> = Raramente</span>
                <span><strong>4</strong> = Às vezes</span>
                <span><strong>5</strong> = Frequentemente</span>
                <span><strong>6</strong> = Sempre</span>
              </div>
              <p className="mt-2 text-xs text-slate-500">* Itens do Fator 3 e item 1 do Fator 4 são invertidos na correção</p>
            </div>

            <div className="space-y-6">
              {[
                { name: "Fator 1 - Regulação Emocional (RE)", items: QUESTIONS.slice(0, 19), startIdx: 0, color: "bg-rose-50 border-rose-200", text: "text-rose-700" },
                { name: "Fator 2 - Hiperatividade / Impulsividade (HI)", items: QUESTIONS.slice(19, 32), startIdx: 19, color: "bg-amber-50 border-amber-200", text: "text-amber-700" },
                { name: "Fator 3 - Comportamento Adaptativo (CA)", items: QUESTIONS.slice(32, 46), startIdx: 32, color: "bg-emerald-50 border-emerald-200", text: "text-emerald-700" },
                { name: "Fator 4 - Atenção (A)", items: QUESTIONS.slice(46, 58), startIdx: 46, color: "bg-blue-50 border-blue-200", text: "text-blue-700" },
              ].map((factor, factorIdx) => (
                <div key={factor.name} className="rounded-xl border overflow-hidden">
                  <div className={`px-4 py-3 ${factor.color} border-b`}>
                    <h3 className={`font-semibold ${factor.text}`}>{factor.name}</h3>
                    <p className="text-xs text-slate-500 mt-1">{factor.items.length} itens</p>
                  </div>
                  <div className="bg-white">
                    <div className="grid grid-cols-[60px_1fr_80px] bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 border-b">
                      <div>Item</div>
                      <div>Descrição</div>
                      <div className="text-center">Resp.</div>
                    </div>
                    {factor.items.map((text, idx) => {
                      const itemNum = factor.startIdx + idx + 1;
                      const relativeNum = idx + 1;
                      const isReversed = (itemNum >= 33 && itemNum <= 46) || itemNum === 47;
                      return (
                        <div
                          key={idx}
                          className={`grid grid-cols-[60px_1fr_80px] items-center px-4 py-3 border-b last:border-b-0 ${
                            idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"
                          }`}
                        >
                          <div className="text-sm font-medium text-slate-900">
                            {String(relativeNum).padStart(2, "0")}
                            {isReversed && <span className="text-red-500 ml-1">*</span>}
                          </div>
                          <div className="text-sm text-slate-700 pr-4">{text}</div>
                          <div className="flex justify-center">
                            <Input
                              type="text"
                              inputMode="numeric"
                              maxLength={1}
                              data-item={itemNum}
                              className="h-8 w-16 rounded-lg text-center"
                              value={scores[`item_${itemNum}`] || ""}
                              onChange={(e) => handleScoreChange(itemNum, e.target.value)}
                              onKeyDown={(e) => handleKeyDown(e, itemNum)}
                              placeholder="1-6"
                            />
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
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
              <p className="font-medium text-slate-900">ETDAH-PAIS</p>
              <p>Escala de Transtorno de Déficit de Atenção e Hiperatividade - Versão para Pais</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>58 itens com escala Likert de 6 pontos (1-6)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Fatores</p>
              <div className="flex flex-wrap gap-1 mt-2">
                <Badge>RE - Regulação Emocional</Badge>
                <Badge>HI - Hiperatividade/Impulsividade</Badge>
                <Badge>CA - Comportamento Adaptativo</Badge>
                <Badge>A - Atenção</Badge>
              </div>
            </div>
            <div>
              <p className="font-medium text-slate-900">Normas</p>
              <p>Por sexo e faixa etária (2-5, 6-9, 10-13, 14-17 anos)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Público-alvo</p>
              <p>Crianças e adolescentes (2-17 anos)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ETDAHPAISTestPageFallback() {
  return <div className="space-y-6" />;
}

export default function ETDAHPAISTestPage() {
  return (
    <Suspense fallback={<ETDAHPAISTestPageFallback />}>
      <ETDAHPAISTestPageContent />
    </Suspense>
  );
}
