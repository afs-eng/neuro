"use client";

import React, { useState, useEffect } from "react";
import { SystemLayout, NAV } from "@/components/layout/SystemLayout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import {
  Users,
  ClipboardList,
  FlaskConical,
  FileText,
  FolderOpen,
  Brain,
  AlertTriangle,
  Clock3,
  Upload,
  Plus,
  ChevronRight,
  CheckCircle2,
  Search,
  ArrowLeft,
} from "lucide-react";
import { useRouter } from "next/navigation";

const TESTS_AVAILABLE = [
  { code: "wisc4", name: "WISC-IV", category: "Inteligência infantil" },
  { code: "bpa2", name: "BPA-2", category: "Atenção" },
  { code: "ebadep-a", name: "EBADEP-A", category: "Depressão em adultos" },
  { code: "ebadep-ij", name: "EBADEP-IJ", category: "Depressão infantojuvenil" },
  { code: "epq-j", name: "EPQ-J", category: "Personalidade infantojuvenil" },
  { code: "etdah-ad", name: "ETDAH-AD", category: "TDAH em adultos" },
];

const patients: any[] = [];

const evaluations = [
  { id: "AV-2201", patient: "Marina Carvalho", examiner: "Dr. André", stage: "Coleta de dados", start: "19/03/2026", tests: 4 },
  { id: "AV-2202", patient: "João Pedro", examiner: "Dr. André", stage: "Redação do laudo", start: "18/03/2026", tests: 3 },
  { id: "AV-2203", patient: "Renato Vitulli", examiner: "Dr. André", stage: "Aprovado", start: "11/03/2026", tests: 5 },
];

function StatusBadge({ children }: { children: string }) {
  const map: Record<string, string> = {
    "Em avaliação": "bg-amber-50 text-amber-700 border-amber-200",
    "Laudo em redação": "bg-blue-50 text-blue-700 border-blue-200",
    "Finalizado": "bg-emerald-50 text-emerald-700 border-emerald-200",
    "Aguardando documentos": "bg-slate-100 text-slate-700 border-slate-200",
    "Coleta de dados": "bg-amber-50 text-amber-700 border-amber-200",
    "Redação do laudo": "bg-blue-50 text-blue-700 border-blue-200",
    "Aprovado": "bg-emerald-50 text-emerald-700 border-emerald-200",
  };
  return <Badge className={`rounded-full border ${map[children] || "bg-slate-100 text-slate-700 border-slate-200"}`}>{children}</Badge>;
}

function StatCard({ title, value, hint, icon: Icon }: { title: string; value: string; hint: string; icon: React.ElementType }) {
  return (
    <Card className="rounded-2xl border-slate-200 shadow-sm">
      <CardContent className="p-5 flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-500">{title}</p>
          <p className="mt-2 text-3xl font-semibold tracking-tight text-slate-900">{value}</p>
          <p className="mt-2 text-sm text-slate-500">{hint}</p>
        </div>
        <div className="rounded-2xl border border-slate-200 p-3 bg-white">
          <Icon className="h-5 w-5 text-slate-700" />
        </div>
      </CardContent>
    </Card>
  );
}

function SectionTitle({ title, subtitle, action }: { title: string; subtitle?: string; action?: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight text-slate-900">{title}</h2>
        {subtitle && <p className="text-sm text-slate-500 mt-1">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

// Dashboard Page
function DashboardContent() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Visão geral do sistema"
        subtitle="Painel central para pacientes, avaliações, testes, laudos e automações assistidas por IA."
        action={<Button className="rounded-2xl gap-2"><Plus className="h-4 w-4" /> Nova avaliação</Button>}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard title="Pacientes ativos" value="248" hint="17 novos neste mês" icon={Users} />
        <StatCard title="Avaliações em andamento" value="31" hint="9 em redação" icon={ClipboardList} />
        <StatCard title="Testes processados" value="186" hint="últimos 30 dias" icon={FlaskConical} />
        <StatCard title="Laudos aprovados" value="54" hint="12 aguardando revisão" icon={CheckCircle2} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Pipeline clínico</CardTitle>
            <CardDescription>Acompanhamento das etapas operacionais do sistema.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[
              { title: "Aguardando documentos", value: 8, progress: 22, icon: FolderOpen },
              { title: "Coleta de dados", value: 11, progress: 46, icon: ClipboardList },
              { title: "Pontuação de testes", value: 7, progress: 64, icon: FlaskConical },
              { title: "Redação e revisão", value: 12, progress: 78, icon: FileText },
            ].map((item) => (
              <div key={item.title} className="rounded-2xl border border-slate-200 p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <item.icon className="h-4 w-4 text-slate-600" />
                    <span className="font-medium text-slate-800">{item.title}</span>
                  </div>
                  <span className="text-sm text-slate-500">{item.value}</span>
                </div>
                <Progress value={item.progress} className="h-2" />
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Alertas</CardTitle>
            <CardDescription>Pendências operacionais e clínicas.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              [AlertTriangle, "3 protocolos aguardando conferência manual"],
              [Clock3, "2 laudos com prazo vencendo hoje"],
              [Brain, "5 sugestões de inconsistência emitidas pela IA"],
              [Upload, "4 documentos novos sem vínculo de avaliação"],
            ].map(([Icon, text], idx) => (
              <div key={idx} className="flex items-start gap-3 rounded-2xl border border-slate-200 p-3">
                <Icon className="h-4 w-4 text-slate-700 mt-0.5" />
                <p className="text-sm text-slate-700">{String(text)}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Últimas avaliações</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Paciente</TableHead>
                  <TableHead>Etapa</TableHead>
                  <TableHead>Início</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {evaluations.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <div>
                        <p className="font-medium text-slate-900">{item.patient}</p>
                        <p className="text-xs text-slate-500">{item.id}</p>
                      </div>
                    </TableCell>
                    <TableCell><StatusBadge>{item.stage}</StatusBadge></TableCell>
                    <TableCell>{item.start}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Módulos do sistema</CardTitle>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3">
            {[
              ["Cadastro clínico", Users],
              ["Fluxo de avaliação", ClipboardList],
              ["Testes com regras", FlaskConical],
              ["Editor de laudos", FileText],
              ["Gestão documental", FolderOpen],
              ["IA assistiva", Brain],
            ].map(([label, Icon]) => (
              <div key={String(label)} className="rounded-2xl border border-slate-200 p-4 flex items-center gap-3">
                <div className="rounded-xl border border-slate-200 p-2"><Icon className="h-4 w-4" /></div>
                <span className="text-sm font-medium text-slate-800">{String(label)}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

// Patients Page
function PatientsContent({ onPatientClick }: { onPatientClick: (id: string) => void }) {
  const router = useRouter();
  const [patientsList, setPatientsList] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    async function fetchPatients() {
      try {
        const { api } = await import("@/lib/api");
        const data = await api.get<any[]>("/api/patients/");
        setPatientsList(data);
      } catch (error) {
        console.error("Erro ao buscar pacientes:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchPatients();
  }, []);

  const filteredPatients = patientsList.filter((p: any) => 
    (p.full_name || "").toLowerCase().includes(searchTerm.toLowerCase()) ||
    String(p.id).toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-slate-500">Carregando pacientes...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <SectionTitle
        title="Pacientes"
        subtitle="Cadastro clínico com busca rápida, dados demográficos e acesso ao histórico de avaliações."
        action={<Button className="rounded-2xl gap-2" onClick={() => window.location.href = '/dashboard/patients'}><Plus className="h-4 w-4" /> Novo paciente</Button>}
      />

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-4">
          <div className="relative mb-4">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              placeholder="Buscar pacientes por nome ou ID..."
              className="pl-10 rounded-xl"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Paciente</TableHead>
                <TableHead>Idade</TableHead>
                <TableHead>Cidade</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Última avaliação</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPatients.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                    Nenhum paciente encontrado
                  </TableCell>
                </TableRow>
              ) : (
                filteredPatients.map((item: any) => (
                  <TableRow 
                    key={item.id} 
                    className="cursor-pointer hover:bg-slate-50"
                    onClick={() => onPatientClick(item.id)}
                  >
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center text-sm font-medium text-slate-700">
                          {item.full_name?.charAt(0) || "?"}
                        </div>
                        <div>
                          <p className="font-medium text-slate-900">{item.full_name}</p>
                          <p className="text-xs text-slate-500">ID: {item.id}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>{item.birth_date || "—"}</TableCell>
                    <TableCell>{item.city || "—"}</TableCell>
                    <TableCell><StatusBadge>{item.sex || "Não informado"}</StatusBadge></TableCell>
                    <TableCell>{item.schooling || "—"}</TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

// Patient Detail Page
function PatientDetailContent({ patientId, onBack }: { patientId: string; onBack: () => void }) {
  const router = useRouter();
  const [patient, setPatient] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPatient() {
      try {
        const { api } = await import("@/lib/api");
        const data = await api.get<any>(`/api/patients/${patientId}/`);
        setPatient(data);
      } catch (error) {
        console.error("Erro ao buscar paciente:", error);
        setPatient(null);
      } finally {
        setLoading(false);
      }
    }
    fetchPatient();
  }, [patientId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <p className="text-slate-500">Carregando...</p>
      </div>
    );
  }

  if (!patient) {
    return (
      <div className="flex flex-col items-center justify-center h-96">
        <p className="text-slate-500 mb-4">Paciente não encontrado</p>
        <Button variant="outline" onClick={onBack}>Voltar</Button>
      </div>
    );
  }

  const handleApplyTest = (testCode: string) => {
    router.push(`/dashboard/tests/${testCode}`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" size="icon" onClick={onBack} className="rounded-full">
          <ArrowLeft className="h-5 w-5" />
        </Button>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">{patient.full_name}</h2>
          <p className="text-sm text-slate-500">ID: {patient.id}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2 space-y-6">
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Dados do paciente</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-slate-500">Data de nascimento</p>
                  <p className="font-medium text-slate-900">{patient.birth_date || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Sexo</p>
                  <p className="font-medium text-slate-900">{patient.sex || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Escolaridade</p>
                  <p className="font-medium text-slate-900">{patient.schooling || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Cidade</p>
                  <p className="font-medium text-slate-900">{patient.city || "—"}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Contato e Responsáveis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-slate-500">Telefone</p>
                  <p className="font-medium text-slate-900">{patient.phone || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">E-mail</p>
                  <p className="font-medium text-slate-900">{patient.email || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Nome da mãe</p>
                  <p className="font-medium text-slate-900">{patient.mother_name || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Nome do pai</p>
                  <p className="font-medium text-slate-900">{patient.father_name || "—"}</p>
                </div>
                <div>
                  <p className="text-sm text-slate-500">Estado</p>
                  <p className="font-medium text-slate-900">{patient.state || "—"}</p>
                </div>
              </div>
              {patient.notes && (
                <div className="mt-4">
                  <p className="text-sm text-slate-500">Observações</p>
                  <p className="font-medium text-slate-900">{patient.notes}</p>
                </div>
              )}
            </CardContent>
          </Card>

          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Avaliações anteriores</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Teste</TableHead>
                    <TableHead>Data</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow>
                    <TableCell>WISC-IV</TableCell>
                    <TableCell>15/03/2026</TableCell>
                    <TableCell><StatusBadge>Finalizado</StatusBadge></TableCell>
                    <TableCell><Button size="sm" variant="outline" className="rounded-xl">Ver resultado</Button></TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>BPA-2</TableCell>
                    <TableCell>15/03/2026</TableCell>
                    <TableCell><StatusBadge>Finalizado</StatusBadge></TableCell>
                    <TableCell><Button size="sm" variant="outline" className="rounded-xl">Ver resultado</Button></TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-4">
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Aplicar teste</CardTitle>
              <CardDescription>Selecione um instrumento para aplicar</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              {TESTS_AVAILABLE.map((test) => (
                <Button
                  key={test.code}
                  variant="outline"
                  className="w-full justify-start rounded-xl"
                  onClick={() => handleApplyTest(test.code)}
                >
                  <FlaskConical className="h-4 w-4 mr-2" />
                  {test.name}
                </Button>
              ))}
            </CardContent>
          </Card>

          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Ações</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" className="w-full justify-start rounded-xl">
                <FileText className="h-4 w-4 mr-2" />
                Gerar laudo
              </Button>
              <Button variant="outline" className="w-full justify-start rounded-xl">
                <ClipboardList className="h-4 w-4 mr-2" />
                Nova avaliação
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

// Tests Page
function TestsContent() {
  const router = useRouter();

  const handleApplyTest = (testCode: string) => {
    router.push(`/dashboard/tests/${testCode}`);
  };

  return (
    <div className="space-y-6">
      <SectionTitle
        title="Catálogo de testes"
        subtitle="Lista de instrumentos disponíveis para aplicação."
        action={<Button className="rounded-2xl gap-2"><Plus className="h-4 w-4" /> Adicionar teste</Button>}
      />

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
  );
}

// Reports Page
function ReportsContent() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Laudos"
        subtitle="Gestão de documentos clínicos e relatórios neuropsicológicos."
        action={<Button className="rounded-2xl gap-2"><Plus className="h-4 w-4" /> Novo laudo</Button>}
      />

      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-6">
          <p className="text-slate-500">Nenhum laudo em produção no momento.</p>
        </CardContent>
      </Card>
    </div>
  );
}

// Default/Placeholder Page
function DefaultContent() {
  return (
    <div className="flex items-center justify-center h-96">
      <div className="text-center">
        <Brain className="h-16 w-16 text-slate-300 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-slate-900">Em breve</h2>
        <p className="text-slate-500 mt-2">Este módulo está em desenvolvimento.</p>
      </div>
    </div>
  );
}

// Main Page Component
export default function DashboardPage() {
  const router = useRouter();
  const [currentPage, setCurrentPage] = useState("dashboard");
  const [selectedPatientId, setSelectedPatientId] = useState<string | null>(null);

  const handlePatientClick = (id: string) => {
    setSelectedPatientId(id);
    setCurrentPage("patient-detail");
  };

  const handleBackToPatients = () => {
    setSelectedPatientId(null);
    setCurrentPage("patients");
  };

  const renderContent = () => {
    if (currentPage === "patient-detail" && selectedPatientId) {
      return <PatientDetailContent patientId={selectedPatientId} onBack={handleBackToPatients} />;
    }

    switch (currentPage) {
      case "dashboard":
        return <DashboardContent />;
      case "patients":
        return <PatientsContent onPatientClick={handlePatientClick} />;
      case "tests":
        return <TestsContent />;
      case "reports":
        return <ReportsContent />;
      case "evaluations":
      case "documents":
      case "ai":
      case "accounts":
        return <DefaultContent />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <SystemLayout currentPage={currentPage} onNavigate={setCurrentPage}>
      {renderContent()}
    </SystemLayout>
  );
}
