"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Save } from "lucide-react";
import { api } from "@/lib/api";

export default function BPA2TestPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [scores, setScores] = useState({
    ac_brutos: "",
    ac_erros: "",
    ac_omissoes: "",
    ad_brutos: "",
    ad_erros: "",
    ad_omissoes: "",
    aa_brutos: "",
    aa_erros: "",
    aa_omissoes: "",
  });
  const [evaluation, setEvaluation] = useState<any>(null);
  const [loadingEvaluation, setLoadingEvaluation] = useState(true);

  const evaluationId = searchParams.get("evaluation_id");
  const applicationId = searchParams.get("application_id");

  useEffect(() => {
    async function fetchEvaluation() {
      if (!evaluationId) {
        setLoadingEvaluation(false);
        return;
      }

      if (applicationId) {
        try {
          const result = await api.get<any>(`/api/tests/applications/${applicationId}`)
          if (result && result.is_validated) {
            router.push(`/dashboard/tests/bpa2/${applicationId}/result`)
            return
          }
          if (result && result.raw_payload) {
            const raw = result.raw_payload
            setScores({
              ac_brutos: String(raw.ac?.brutos || ''),
              ac_erros: String(raw.ac?.erros || ''),
              ac_omissoes: String(raw.ac?.omissoes || ''),
              ad_brutos: String(raw.ad?.brutos || ''),
              ad_erros: String(raw.ad?.erros || ''),
              ad_omissoes: String(raw.ad?.omissoes || ''),
              aa_brutos: String(raw.aa?.brutos || ''),
              aa_erros: String(raw.aa?.erros || ''),
              aa_omissoes: String(raw.aa?.omissoes || ''),
            })
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
  }, [evaluationId, applicationId]);

  const domains = [
    { name: "Atenção Concentrada (AC)", fields: ["ac_brutos", "ac_erros", "ac_omissoes"] },
    { name: "Atenção Dividida (AD)", fields: ["ad_brutos", "ad_erros", "ad_omissoes"] },
    { name: "Atenção Alternada (AA)", fields: ["aa_brutos", "aa_erros", "aa_omissoes"] },
  ];

  const handleSave = async () => {
    if (!evaluationId) {
      alert("ID da avaliação não encontrado. Acesse este teste através de uma avaliação.");
      return;
    }
    const payload = {
      evaluation_id: parseInt(evaluationId),
      norm_type: "idade",
      ac: {
        brutos: parseInt(scores.ac_brutos) || 0,
        erros: parseInt(scores.ac_erros) || 0,
        omissoes: parseInt(scores.ac_omissoes) || 0,
      },
      ad: {
        brutos: parseInt(scores.ad_brutos) || 0,
        erros: parseInt(scores.ad_erros) || 0,
        omissoes: parseInt(scores.ad_omissoes) || 0,
      },
      aa: {
        brutos: parseInt(scores.aa_brutos) || 0,
        erros: parseInt(scores.aa_erros) || 0,
        omissoes: parseInt(scores.aa_omissoes) || 0,
      },
    };

    try {
      const result = await api.post<{ application_id: number }>('/api/tests/bpa2/submit', payload);
      alert('BPA-2 salvo com sucesso!');
      router.push(`/dashboard/tests/bpa2/${result.application_id}/result`);
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
          <h2 className="text-2xl font-semibold text-slate-900">BPA-2</h2>
          <p className="text-sm text-slate-500">Brief Psychological Assessment - 2ª Edição</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Dados da aplicação</CardTitle>
            <CardDescription>Preencha os escores brutos do teste.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {domains.map((domain) => (
                <div key={domain.name} className="rounded-xl bg-slate-50 p-4 space-y-4">
                  <h3 className="font-medium text-slate-900">{domain.name}</h3>
                  <div className="space-y-3">
                    <div className="space-y-1">
                      <label className="text-xs text-slate-600">Acertos</label>
                      <Input
                        type="number"
                        className="rounded-lg"
                        value={scores[domain.fields[0] as keyof typeof scores]}
                        onChange={(e) => setScores({ ...scores, [domain.fields[0]]: e.target.value })}
                        placeholder="0"
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs text-slate-600">Erros</label>
                      <Input
                        type="number"
                        className="rounded-lg"
                        value={scores[domain.fields[1] as keyof typeof scores]}
                        onChange={(e) => setScores({ ...scores, [domain.fields[1]]: e.target.value })}
                        placeholder="0"
                      />
                    </div>
                    <div className="space-y-1">
                      <label className="text-xs text-slate-600">Omissões</label>
                      <Input
                        type="number"
                        className="rounded-lg"
                        value={scores[domain.fields[2] as keyof typeof scores]}
                        onChange={(e) => setScores({ ...scores, [domain.fields[2]]: e.target.value })}
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
              <p className="font-medium text-slate-900">BPA-2</p>
              <p>Brief Psychological Assessment - 2ª Edição</p>
            </div>
            <div>
              <p className="font-medium text-slate-900">Domínios</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Atenção Concentrada</li>
                <li>Atenção Dividida</li>
                <li>Atenção Alternada</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
