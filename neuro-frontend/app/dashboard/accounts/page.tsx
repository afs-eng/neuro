import { Card, CardContent } from "@/components/ui/card";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { ShieldCheck } from "lucide-react";

export default function AccountsPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Usuários"
        subtitle="Gestão de usuários e permissões do sistema."
      />

      <Card className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <CardContent className="p-6">
          <EmptyState
            icon={<ShieldCheck className="h-12 w-12" />}
            title="Gestão de usuários"
            description="Módulo de gestão de usuários e permissões em desenvolvimento."
          />
        </CardContent>
      </Card>
    </PageContainer>
  );
}
