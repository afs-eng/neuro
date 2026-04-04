import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PageContainer, PageHeader, EmptyState } from "@/components/ui/page";
import { FolderOpen, Plus, Upload } from "lucide-react";

export default function DocumentsPage() {
  return (
    <PageContainer>
      <PageHeader
        title="Documentos"
        subtitle="Gestão de documentos e arquivos clínicos."
        actions={
          <Button className="gap-2">
            <Upload className="h-4 w-4" />
            Enviar documento
          </Button>
        }
      />

      <Card className="rounded-xl border border-slate-200 bg-white shadow-sm">
        <CardContent className="p-6">
          <EmptyState
            icon={<FolderOpen className="h-12 w-12" />}
            title="Nenhum documento anexado"
            description="Envie documentos clínicos para armazenar e gerenciar na plataforma."
          />
        </CardContent>
      </Card>
    </PageContainer>
  );
}
