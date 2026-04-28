"use client";

import { Suspense, useEffect, useMemo, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { api } from "@/lib/api";

type ScaredItem = {
  item: number;
  pergunta: string;
};

type ScaredFormData = {
  label: string;
  items: ScaredItem[];
};

const FORM_OPTIONS = [
  { value: "child", label: "Autorrelato" },
  { value: "parent", label: "Pais/Cuidadores" },
];

function SCAREDTestPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  // Estados separados para cada formulário
  const [childScores, setChildScores] = useState<Record<string, string>>({});
  const [parentScores, setParentScores] = useState<Record<string, string>>({});
  
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [formsData, setFormsData] = useState<Record<string, ScaredFormData>>({});
  const [form, setForm] = useState<string>("child");
  
  // IDs das aplicações salvas
  const [childApplicationId, setChildApplicationId] = useState<number | null>(null);
  const [parentApplicationId, setParentApplicationId] = useState<number | null>(null);

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");
  const isEditMode = searchParams.get("edit") === "true";
  const requestedForm = searchParams.get("form");

  const currentForm = formsData[form];
  const items = useMemo(() => currentForm?.items || [], [currentForm]);
  
  // Escolhe qual state usar baseado no formulário atual
  const currentScores = form === "child" ? childScores : parentScores;
  const currentSetScores = form === "child" ? setChildScores : setParentScores;
  const currentAppId = form === "child" ? childApplicationId : parentApplicationId;

  const alternateForm = FORM_OPTIONS.find(o => o.value !== form)?.value || "parent";
  const alternateFormLabel = FORM_OPTIONS.find(o => o.value === alternateForm)?.label || "Outro formulário";

  useEffect(() => {
    async function fetchData() {
      if (requestedForm === "child" || requestedForm === "parent") {
        setForm(requestedForm);
      }

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`);
          if (result?.evaluation_id && !evaluationId) {
            router.replace(`/dashboard/tests/scared?application_id=${applicationId}&evaluation_id=${result.evaluation_id}&edit=true`);
            return;
          }
          if (result?.is_validated && !isEditMode) {
            const resultEvaluationId = result.evaluation_id ? `?evaluation_id=${result.evaluation_id}` : "";
            router.push(`/dashboard/tests/scared/${applicationId}/result${resultEvaluationId}`);
            return;
          }
          if (result?.raw_payload) {
            const raw = result.raw_payload;
            const appForm = raw.form || "child";
            const existingScores: Record<string, string> = {};
            const responses = raw.responses || {};
            for (let i = 1; i <= 41; i++) {
              const key = String(i);
              if (responses[key] !== undefined) {
                existingScores[key] = String(responses[key]);
              }
            }
            
            if (appForm === "child") {
              setChildScores(existingScores);
              setChildApplicationId(result.id);
            } else {
              setParentScores(existingScores);
              setParentApplicationId(result.id);
            }
            setForm(appForm);
          }
        } catch {
          console.log("Teste não encontrado, redirecionando para formulário...");
        }
      }

      try {
        const itemsData = await api.get<Record<string, ScaredFormData>>("/api/tests/scared/items");
        setFormsData(itemsData || {});
      } catch (error) {
        console.error("Erro ao buscar itens do SCARED:", error);
      }

      if (!evaluationId) {
        setLoading(false);
        return;
      }

      try {
        const data = await api.get<any>(`/api/evaluations/${evaluationId}`);
        setEvaluation(data);
      } catch (error: any) {
        console.error("Erro ao buscar avaliação:", error);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [applicationId, evaluationId, isEditMode, requestedForm, router]);

  const clearForm = () => {
    if (confirm("Deseja realmente limpar todos os campos do formulário atual?")) {
      if (form === "child") {
        setChildScores({});
        setChildApplicationId(null);
      } else {
        setParentScores({});
        setParentApplicationId(null);
      }
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

    if (calcAge > 18) {
      alert("Este teste é indicado para pacientes de até 18 anos. A idade calculada é de " + calcAge + " anos.");
      return;
    }

    const responseObj: Record<string, number> = {};
    for (let i = 1; i <= 41; i++) {
      const key = String(i);
      responseObj[key] = parseInt(currentScores[key]) || 0;
    }

    const payload = {
      application_id: currentAppId || undefined,
      evaluation_id: parseInt(evaluationId),
      form,
      gender: evaluation?.patient_sex || "M",
      age: calcAge,
      responses: responseObj,
    };

    setSaving(true);
    try {
      const result = await api.post<{ application_id: number }>("/api/tests/scared/submit", payload);
      
      if (form === "child") {
        setChildApplicationId(result.application_id);
      } else {
        setParentApplicationId(result.application_id);
      }
      
      router.push(`/dashboard/tests/scared/${result.application_id}/result?evaluation_id=${evaluationId}`);
    } catch (error: any) {
      console.error("Erro:", error);
      alert("Erro ao salvar: " + (error?.message || "Tente novamente"));
    } finally {
      setSaving(false);
    }
  };

  const handleSwitchForm = () => {
    setForm(alternateForm);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

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
            <CardDescription>
              {form === "parent" ? "Versão respondida por pais ou cuidadores." : "Versão de autorrelato para criança ou adolescente."}
            </CardDescription>
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
                {items.map((item, idx) => (
                  <div
                    key={`${form}-${item.item}`}
                    className={`grid grid-cols-[60px_1fr_80px] items-center px-4 py-3 border-t ${idx % 2 === 0 ? "bg-white" : "bg-slate-50/50"}`}
                  >
                    <div className="text-sm font-medium text-slate-900">{String(item.item).padStart(2, "0")}</div>
                    <div className="text-sm text-slate-700 pr-4">{item.pergunta}</div>
                    <div className="flex justify-center">
                      <Input
                        type="text"
                        inputMode="numeric"
                        maxLength={1}
                        className="h-8 w-16 rounded-lg text-center"
                        value={currentScores[String(item.item)] || ""}
                        onChange={(e) => {
                          const val = e.target.value;
                          if (val === "" || ["0", "1", "2"].includes(val)) {
                            currentSetScores({ ...currentScores, [String(item.item)]: val });
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
              <Button className="rounded-xl gap-2 bg-emerald-600 hover:bg-emerald-700 text-white shadow-lg shadow-emerald-100 transition-all font-bold" onClick={handleSave} disabled={saving}>
                <Save className="h-4 w-4" />
                {isEditMode ? "Salvar Alterações" : "Salvar aplicação"}
              </Button>
              {evaluationId && !applicationId && (
                <Button
                  variant="outline"
                  className="rounded-xl"
                  onClick={handleSwitchForm}
                  disabled={saving}
                >
                  Preencher {alternateFormLabel}
                </Button>
              )}
              <Button variant="outline" className="rounded-xl text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200" onClick={clearForm} disabled={saving}>
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
              <label className="font-medium text-slate-900">Formulário</label>
              <select
                value={form}
                onChange={(e) => setForm(e.target.value)}
                className="w-full mt-1 p-2 border rounded-lg"
              >
                {FORM_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </div>
            <div>
              <p className="font-medium text-slate-900">SCARED</p>
              <p>Screen for Child Anxiety Related Emotional Disorders</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Paciente</p>
              <p>{evaluation?.patient_name || "Não informado"}</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Itens</p>
              <p>41 itens com escala Likert de 3 pontos</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Status</p>
              <p>
                {form === "child" 
                  ? childApplicationId ? "Autorrelato salvo" : "Autorrelato não salvo"
                  : parentApplicationId ? "Pais/Cuidadores salvo" : "Pais/Cuidadores não salvo"
                }
              </p>
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