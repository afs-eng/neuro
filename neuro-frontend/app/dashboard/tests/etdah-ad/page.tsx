"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

function formatSexLabel(sex?: string | null) {
  if (sex === "M") return "Masculino";
  if (sex === "F") return "Feminino";
  return "Nao informado";
}

const QUESTIONS = [
  "É atento quando conversa com alguém.",
  "É afobado no trabalho.",
  "Necessita fazer lista de tudo o que tem para fazer para não se esquecer de nada.",
  "Sente-se chateado e infeliz.",
  "Quando tem de seguir instruções (receitas, montagem de móveis), segue passo a passo e em sequência, tal como lhe é apresentado.",
  "É desorganizado financeiramente.",
  "É solitário.",
  "Termina tudo o que começa.",
  "Explode com facilidade (é do tipo pavio curto).",
  "É detalhista e minucioso.",
  "Arruma encrenca e confusão facilmente.",
  "Mostra-se insensível à dor e ao perigo.",
  "Tem sono agitado, mexe-se na cama.",
  "É bem-aceito por todos.",
  "Costuma se dar mal por falar as coisas sem pensar.",
  "É persistente e insistente diante de uma ideia.",
  "Acidenta-se com facilidade (cai, tropeça, esbarra em móveis).",
  "Tende a discordar das regras e normas.",
  "Dá impressão de que não sabe o que quer.",
  "Evita trabalhos longos, detalhados e complicados.",
  "Tem dificuldade para se adaptar às mudanças.",
  "A qualidade do trabalho é comprometida porque não presta atenção suficiente.",
  "Inicia uma atividade com entusiasmo e dificilmente chega ao fim, é do tipo fogo de palha.",
  "Evita as atividades que exijam esforço mental prolongado (p. ex., leitura, filmes).",
  "Perde a paciência com os familiares.",
  "É rebelde com as pessoas e as situações.",
  "Persiste quando quer alguma coisa.",
  "Tem tendência a sonhar acordado.",
  "Faz planos cuidadosamente, considera todos os passos do começo ao fim.",
  "Parece sonhar acordado.",
  "Faz seu trabalho rápido demais.",
  "É distraído com tudo.",
  "Dificilmente chega ao final de um projeto.",
  "Seu hábito de trabalho é confuso e desorganizado.",
  "Necessita estar em constante movimentação.",
  "Atrasa os pagamentos porque se esquece das datas de vencimento.",
  "Mostra-se apático e indiferente diante das situações.",
  "Tem fortes reações emocionais (p. ex., choros, explosões de raiva, bate portas, quebra objetos, etc.).",
  "É agressivo.",
  "Tem problemas com a lei e/ou com a justiça.",
  "É imprudente, arrisca sempre.",
  "É tolerante diante das situações.",
  "Tem dificuldade para permanecer sentado, quando isso se faz necessário.",
  "É conhecido pelos outros como desligado, parecendo viver no espaço.",
  "Seu jeito de ser é motivo de discussão em casa.",
  "Tira conclusões mesmo antes de conhecer os fatos.",
  "Necessita estar em situações mais perigosas e arriscadas.",
  "Tem dificuldade em aceitar a opinião dos outros.",
  "Faz as coisas devagar, apresenta um ritmo de trabalho lento.",
  "Distrai-se enquanto trabalha e outras pessoas conversam.",
  "A mente voa longe enquanto lê.",
  "Faz tudo o que dá em sua cabeça.",
  "Costuma vingar-se das pessoas, não engole sapo.",
  "Precisa ser lembrado dos compromissos diários.",
  "Vive isolado, evita as atividades de grupo.",
  "É mais desorganizado do que a maioria das pessoas.",
  "Não observa detalhes e minúcias.",
  "Persiste até o fim com os seus objetivos, mesmo que sejam difíceis de alcançar.",
  "Sabe aguardar a vez (p. ex., fila de banco, em consultório, etc.).",
  "Responde antes de ouvir a pergunta inteira.",
  "É criticado por seu jeito de ser.",
  "Intromete-se em assuntos que não lhe dizem respeito.",
  "Costuma criticar os outros.",
  "Tem memória ruim para guardar instruções, ordens recebidas ou para decorar o que é preciso.",
  "Planeja suas ações, respeitando cada etapa do processo.",
  "É impulsivo; age antes de pensar.",
  "Costuma se esquecer de datas, números de telefone, compromissos importantes, a não ser que os anote.",
  "Necessita de novidades e de variedades na sua vida.",
  "Tem dificuldade para processar as informações recebidas.",
];



function ETDAHADTestPageContent() {
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
            router.replace(`/dashboard/tests/etdah-ad?application_id=${applicationId}&evaluation_id=${newEvalId}&edit=true`)
            return
          }
          if (result && result.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : ""
            router.push(`/dashboard/tests/etdah-ad/${applicationId}/result${resultEvaluationId}`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingScores: Record<string, string> = {}
            for (let i = 1; i <= 69; i++) {
              const paddedKey = `item_${i.toString().padStart(2, '0')}`
              const unpaddedKey = `item_${i}`
              
              // Tenta várias possibilidades de onde o valor pode estar (devido a versões antigas)
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
    if (value === "" || (!isNaN(num) && num >= 0 && num <= 5)) {
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
    
    for (let i = 1; i <= 69; i++) {
      const key = `item_${i}`;
      const paddedKey = `item_${i.toString().padStart(2, '0')}`;
      payload[paddedKey] = parseInt(scores[key]) || 0;
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/etdah-ad/submit', payload);
      router.push(`/dashboard/tests/etdah-ad/${result.application_id}/result?evaluation_id=${evaluationId}`);
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
          <h2 className="text-2xl font-semibold text-slate-900">ETDAH-AD</h2>
          <p className="text-sm text-slate-500">Escala de Transtorno de Déficit de Atenção e Hiperatividade - Versão Adulta</p>
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
                <label className="text-sm font-medium text-slate-700">Sexo do paciente</label>
                <div className="w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-700">
                  {formatSexLabel(evaluation?.patient_sex)}
                </div>
              </div>
            </div>

            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de resposta:</p>
              <div className="grid grid-cols-3 gap-2">
                <span><strong>0</strong> = Nunca</span>
                <span><strong>1-2</strong> = Raramente</span>
                <span><strong>3</strong> = Às vezes</span>
                <span><strong>4</strong> = Frequentemente</span>
                <span><strong>5</strong> = Sempre</span>
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
                        onChange={(e) => handleScoreChange(idx + 1, e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            const nextId = `input-item-${idx + 2}`;
                            document.getElementById(nextId)?.focus();
                          }
                        }}
                        id={`input-item-${idx + 1}`}
                        placeholder="0-5"
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
              <p className="font-medium text-slate-900">ETDAH-AD</p>
              <p>Escala de Transtorno de Déficit de Atenção e Hiperatividade - Versão Adulta</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>69 itens com escala Likert de 6 pontos (0-5)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Fatores</p>
              <div className="flex flex-wrap gap-1 mt-2">
                <Badge>D - Desatenção</Badge>
                <Badge>I - Impulsividade</Badge>
                <Badge>AE - Aspectos Emocionais</Badge>
                <Badge>AAMA - Autorregulação</Badge>
                <Badge>H - Hiperatividade</Badge>
              </div>
            </div>
            <div>
              <p className="font-medium text-slate-900">Normas</p>
              <p>Por escolaridade (Fundamental, Médio, Superior)</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Público-alvo</p>
              <p>Adultos (18+ anos)</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function ETDAHADTestPageFallback() {
  return <div className="space-y-6" />;
}

export default function ETDAHADTestPage() {
  return (
    <Suspense fallback={<ETDAHADTestPageFallback />}>
      <ETDAHADTestPageContent />
    </Suspense>
  );
}
