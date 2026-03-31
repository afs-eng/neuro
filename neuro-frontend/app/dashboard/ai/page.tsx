import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain } from "lucide-react";

export default function AIPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">IA Clínica</h1>
          <p className="text-sm text-slate-500 mt-1">Assistente de inteligência artificial para análise e sugestões.</p>
        </div>
      </div>

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center py-12">
            <Brain className="h-12 w-12 text-slate-300 mb-4" />
            <p className="text-slate-500">Módulo de IA em desenvolvimento.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
