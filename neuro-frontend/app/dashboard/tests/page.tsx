"use client";

import { useRouter } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PageContainer, PageHeader } from "@/components/ui/page";
import { FlaskConical } from "lucide-react";

const TESTS_AVAILABLE = [
  { code: "fdt", name: "FDT", category: "Funções executivas" },
  { code: "wisc4", name: "WISC-IV", category: "Inteligência infantil" },
  { code: "bpa2", name: "BPA-2", category: "Atenção" },
  { code: "ebadep-a", name: "EBADEP-A", category: "Depressão em adultos" },
  { code: "ebadep-ij", name: "EBADEP-IJ", category: "Depressão infantojuvenil" },
  { code: "epq-j", name: "EPQ-J", category: "Personalidade infantojuvenil" },
  { code: "etdah-ad", name: "ETDAH-AD", category: "TDAH em adultos" },
  { code: "ravlt", name: "RAVLT", category: "Memória e aprendizagem" },
];

export default function TestsPage() {
  const router = useRouter();

  const handleApplyTest = (testCode: string) => {
    router.push(`/dashboard/tests/${testCode}`);
  };

  return (
    <PageContainer>
      <PageHeader
        title="Catálogo de testes"
        subtitle="Lista de instrumentos disponíveis para aplicação."
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {TESTS_AVAILABLE.map((test) => (
          <Card key={test.code} className="rounded-xl border border-slate-200 bg-white shadow-sm hover:shadow-md transition-shadow">
            <CardContent className="p-5">
              <div className="flex items-start justify-between">
                <div>
                  <Badge variant="outline" className="mb-2">{test.category}</Badge>
                  <h3 className="text-lg font-semibold text-slate-900">{test.name}</h3>
                </div>
                <FlaskConical className="h-5 w-5 text-slate-400" />
              </div>
              <div className="mt-4 flex gap-2">
                <Button size="sm" variant="outline" className="rounded-lg">Configurar</Button>
                <Button size="sm" className="rounded-lg" onClick={() => handleApplyTest(test.code)}>Aplicar</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </PageContainer>
  );
}
