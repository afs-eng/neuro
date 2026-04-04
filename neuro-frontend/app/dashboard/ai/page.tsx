import { Card, CardContent } from "@/components/ui/card";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { Brain } from "lucide-react";

export default function AIPage() {
  return (
    <PageContainer>
      <PageHeader
        title="IA Clínica"
        subtitle="Assistente de inteligência artificial para análise e sugestões."
      />

      <Card className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <CardContent className="p-6">
          <EmptyState
            icon={<Brain className="h-12 w-12" />}
            title="Módulo de IA em desenvolvimento"
            description="Novas funcionalidades de IA serão disponibilizadas em breve."
          />
        </CardContent>
      </Card>
    </PageContainer>
  );
}
