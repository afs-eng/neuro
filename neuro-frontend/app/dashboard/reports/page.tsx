import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { FileText, Plus } from "lucide-react";

export default function ReportsPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Laudos"
        subtitle="Gestão de documentos clínicos e relatórios neuropsicológicos."
        actions={
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Novo laudo
          </Button>
        }
      />

      <Card className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <CardContent className="p-6">
          <EmptyState
            icon={<FileText className="h-12 w-12" />}
            title="Nenhum laudo em produção"
            description="Laudos e relatórios neuropsicológicos aparecerão aqui quando iniciarem uma avaliação."
          />
        </CardContent>
      </Card>
    </PageContainer>
  );
}
