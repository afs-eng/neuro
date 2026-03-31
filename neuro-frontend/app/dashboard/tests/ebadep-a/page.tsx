"use client";

import { Suspense, useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { api } from "@/lib/api";

const QUESTIONS = [
  "Choro: ausência de vontade de chorar <-> vontade de chorar",
  "Bem-estar: sentir-se muito bem <-> sentir-se mais angustiado",
  "Tarefas: consegue realizar tarefas <-> sente-se impotente para realizá-las",
  "Problemas: resolve problemas <-> sente-se menos capaz de enfrentá-los",
  "Prazer: faz coisas de que gosta <-> não tem mais vontade de fazê-las",
  "Choro recente: não tem chorado <-> tem chorado",
  "Solidão: não sente solidão <-> sente-se cada vez mais sozinho",
  "Comportamento: sabe agir nas situações <-> não sabe mais como agir",
  "Autonomia: consegue se virar sozinho <-> não consegue mais",
  "Futuro: acredita que será melhor <-> não acredita em melhora",
  "Atitudes: parecem normais <-> parecem menos adequadas que antes",
  "Planejamento: faz planos para o futuro <-> não consegue planejar",
  "Crença em si: acredita em si mesmo <-> está acreditando menos em si",
  "Decisão: não tem problemas para decidir <-> está mais difícil decidir",
  "Escolhas: escolhe com facilidade <-> não consegue mais escolher sozinho",
  "Independência: faz tarefas sem ajuda <-> precisa de ajuda para realizá-las",
  "Atividades: sente prazer em realizá-las <-> elas não agradam como antes",
  "Vida: sente-se feliz com a vida <-> antes era mais feliz",
  "Situação atual: acha que as coisas vão bem <-> acha que nada vai bem",
  "Utilidade: faz coisas que ajudam os outros <-> acha que não ajuda mais ninguém",
  "Convívio: estar com pessoas é bom <-> passou a evitar encontros",
  "Eventos sociais: vai a festas/reuniões <-> tem evitado mesmo convidado",
  "Concentração: consegue se concentrar <-> não consegue mais",
  "Ritmo de trabalho: realiza tarefas normalmente <-> está mais lento",
  "Agitação: realiza tarefas normalmente <-> sente-se mais agitado",
  "História de vida: sempre achou a vida boa <-> hoje avalia o passado como ruim",
  "Energia matinal: sente-se disposto <-> acorda esgotado",
  "Vida atual: acha a vida boa <-> percebe a vida cada vez pior",
  "Ideias sobre morrer: morrer não é solução <-> pensa que seria melhor estar morto",
  "Autoeficácia: acredita em si <-> não acredita mais em si",
  "Sono: dorme bem <-> não consegue dormir a noite inteira",
  "Necessário do dia a dia: faz o necessário normalmente <-> não consegue mais",
  "Valor da vida: gosta muito da própria vida <-> não dá mais valor à vida",
  "Autoimagem: gosta de si <-> não gosta mais de si",
  "Finalização: termina tarefas <-> não termina mais",
  "Tranquilidade: está tranquilo <-> perde a paciência com pouco",
  "Nervosismo: não tem se sentido nervoso <-> qualquer coisa o deixa nervoso",
  "Disposição: sente-se com disposição <-> anda mais cansado",
  "Vontade de agir: sente-se disposto <-> não tem mais vontade de fazer as coisas",
  "Padrão de sono: dorme normalmente <-> tem dormido muito",
  "Apetite: fome continua como sempre <-> tem comido menos",
  "Desejo sexual: continua como antes <-> vem diminuindo muito",
  "Peso: continua o mesmo <-> emagreceu sem fazer regime",
  "Medicação: toma remédio apenas quando precisa <-> toma por precaução",
  "Culpa: não costuma sentir culpa <-> vem se sentindo culpado pelos problemas",
];

function EBADEPATestPageContent() {
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
            router.push(`/dashboard/tests/ebadep-a/${applicationId}/result`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            const existingScores: Record<string, string> = {}
            for (let i = 1; i <= 45; i++) {
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
    
    for (let i = 1; i <= 45; i++) {
      payload[`item_${i.toString().padStart(2, '0')}`] = parseInt(scores[`item_${i}`]) || 0;
    }

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/ebadep-a/submit', payload);
      alert('EBADEP-A salvo com sucesso!');
      router.push(`/dashboard/tests/ebadep-a/${result.application_id}/result`);
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
          <h2 className="text-2xl font-semibold text-slate-900">EBADEP-A</h2>
          <p className="text-sm text-slate-500">Escala Brasileira de Avaliação de Déficits de Atenção e Hiperatividade - Adulto</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Itens do instrumento</CardTitle>
            <CardDescription>Marque a intensidade de 0 a 3 para cada item.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-lg bg-slate-50 p-4 text-sm text-slate-600">
              <p className="font-medium mb-2">Escala de intensidade:</p>
              <div className="grid grid-cols-4 gap-2">
                <span>0 = Mínima</span>
                <span>1 = Leve</span>
                <span>2 = Moderada</span>
                <span>3 = Máxima</span>
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
                          if (val === "" || ["0", "1", "2", "3"].includes(val)) {
                            setScores({ ...scores, [`item_${idx + 1}`]: val });
                          }
                        }}
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
              <p className="font-medium text-slate-900">EBADEP-A</p>
              <p>Escala Brasileira de Avaliação de Déficits de Atenção e Hiperatividade - Versão Adulto</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>45 itens com escala Likert de 4 pontos</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Aplicação</p>
              <p>Autorrelato adulto</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function EBADEPATestPageFallback() {
  return <div className="space-y-6" />;
}

export default function EBADEPATestPage() {
  return (
    <Suspense fallback={<EBADEPATestPageFallback />}>
      <EBADEPATestPageContent />
    </Suspense>
  );
}
