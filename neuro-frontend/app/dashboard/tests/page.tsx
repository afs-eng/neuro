"use client";

import { useRouter } from "next/navigation";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { FlaskConical, Plus, ArrowLeft } from "lucide-react";

const TESTS_AVAILABLE = [
  { code: "fdt", name: "FDT", category: "Funções executivas" },
  { code: "wisc4", name: "WISC-IV", category: "Inteligência infantil" },
  { code: "bpa2", name: "BPA-2", category: "Atenção" },
  { code: "ebadep-a", name: "EBADEP-A", category: "Depressão em adultos" },
  { code: "ebadep-ij", name: "EBADEP-IJ", category: "Depressão infantojuvenil" },
  { code: "epq-j", name: "EPQ-J", category: "Personalidade infantojuvenil" },
  { code: "etdah-ad", name: "ETDAH-AD", category: "TDAH em adultos" },
];

export default function TestsPage() {
  const router = useRouter();

  const handleApplyTest = (testCode: string) => {
    router.push(`/dashboard/tests/${testCode}`);
  };

  return (
    <div className="min-h-screen w-full bg-slate-300 p-6 md:p-10">
      <div className="mx-auto max-w-7xl rounded-[36px] bg-[#f3f0e4] p-5 shadow-2xl ring-1 ring-black/5 md:p-7">
        <div className="rounded-[28px] bg-gradient-to-r from-[#f6f4ed] via-[#f2efe4] to-[#efe7bf] p-5 md:p-6">
          <header className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div className="flex items-center gap-4">
              <Button variant="ghost" size="icon" onClick={() => router.back()} className="rounded-full">
                <ArrowLeft className="h-5 w-5" />
              </Button>
              <div className="rounded-full border border-black/20 bg-white/70 px-5 py-2 text-lg font-medium tracking-tight text-zinc-800 shadow-sm">
                NeuroAvalia
              </div>
            </div>

            <nav className="flex flex-wrap items-center gap-2 rounded-full bg-white/70 px-3 py-2 text-sm text-zinc-700 shadow-sm">
              <Link href="/dashboard" className="rounded-full px-4 py-2 hover:bg-black/5">Dashboard</Link>
              <Link href="/dashboard/patients" className="rounded-full px-4 py-2 hover:bg-black/5">Pacientes</Link>
              <Link href="/dashboard/evaluations" className="rounded-full px-4 py-2 hover:bg-black/5">Avaliações</Link>
              <Link href="/dashboard/tests" className="rounded-full px-4 py-2 bg-zinc-900 text-white shadow">Testes</Link>
              <Link href="/dashboard/reports" className="rounded-full px-4 py-2 hover:bg-black/5">Laudos</Link>
            </nav>
          </header>

          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-medium tracking-tight text-zinc-900">Catálogo de testes</h1>
              <p className="mt-1 text-sm text-zinc-600">Lista de instrumentos disponíveis para aplicação.</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {TESTS_AVAILABLE.map((test) => (
              <Card key={test.code} className="rounded-2xl border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between">
                    <div>
                      <Badge variant="outline" className="mb-2">{test.category}</Badge>
                      <h3 className="text-lg font-semibold text-slate-900">{test.name}</h3>
                    </div>
                    <FlaskConical className="h-5 w-5 text-slate-400" />
                  </div>
                  <div className="mt-4 flex gap-2">
                    <Button size="sm" variant="outline" className="rounded-xl">Configurar</Button>
                    <Button size="sm" className="rounded-xl" onClick={() => handleApplyTest(test.code)}>Aplicar</Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
