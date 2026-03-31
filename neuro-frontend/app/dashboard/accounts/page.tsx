import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldCheck } from "lucide-react";

export default function AccountsPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight text-slate-900">Usuários</h1>
          <p className="text-sm text-slate-500 mt-1">Gestão de usuários e permissões do sistema.</p>
        </div>
      </div>

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center py-12">
            <ShieldCheck className="h-12 w-12 text-slate-300 mb-4" />
            <p className="text-slate-500">Módulo de gestão de usuários em desenvolvimento.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
