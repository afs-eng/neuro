import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Plus } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Laudos</h1>
          <p className="text-sm text-slate-500 mt-1">Gestão de documentos clínicos e relatórios neuropsicológicos.</p>
        </div>
        <Button className="rounded-2xl gap-2">
          <Plus className="h-4 w-4" />
          Novo laudo
        </Button>
      </div>

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center py-12">
            <FileText className="h-12 w-12 text-slate-300 mb-4" />
            <p className="text-slate-500">Nenhum laudo em produção no momento.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
