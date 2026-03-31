"use client";

import React, { useMemo, useState } from "react";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Users,
  ClipboardList,
  FlaskConical,
  FileText,
  FolderOpen,
  Brain,
  ShieldCheck,
  Search,
  Bell,
  Settings,
  Plus,
  CalendarDays,
  CheckCircle2,
  AlertTriangle,
  Clock3,
  ChevronRight,
  Filter,
  Download,
  Eye,
  Wand2,
  Upload,
  BarChart3,
  ArrowLeft,
  Save,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Progress } from "@/components/ui/progress";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

const NAV = [
  { key: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { key: "patients", label: "Pacientes", icon: Users },
  { key: "evaluations", label: "Avaliações", icon: ClipboardList },
  { key: "tests", label: "Testes", icon: FlaskConical },
  { key: "reports", label: "Laudos", icon: FileText },
  { key: "documents", label: "Documentos", icon: FolderOpen },
  { key: "ai", label: "IA Clínica", icon: Brain },
  { key: "accounts", label: "Usuários", icon: ShieldCheck },
];

const patients = [
  {
    id: "P-1042",
    name: "Marina Carvalho",
    age: "16 anos",
    city: "Goiânia - GO",
    status: "Em avaliação",
    lastEvaluation: "WISC-IV + BPA-2",
  },
  {
    id: "P-1043",
    name: "João Pedro",
    age: "9 anos",
    city: "Aparecida de Goiânia - GO",
    status: "Laudo em redação",
    lastEvaluation: "SON-R + Portage",
  },
  {
    id: "P-1044",
    name: "Renato Vitulli",
    age: "42 anos",
    city: "Goiânia - GO",
    status: "Finalizado",
    lastEvaluation: "WAIS-III + BPA-2 + RAVLT",
  },
  {
    id: "P-1045",
    name: "Valentina Rocha",
    age: "8 anos",
    city: "Goiânia - GO",
    status: "Aguardando documentos",
    lastEvaluation: "WISC-IV + FDT",
  },
];

const evaluations = [
  {
    id: "AV-2201",
    patient: "Marina Carvalho",
    examiner: "Dr. André",
    stage: "Coleta de dados",
    start: "19/03/2026",
    tests: 4,
  },
  {
    id: "AV-2202",
    patient: "João Pedro",
    examiner: "Dr. André",
    stage: "Redação do laudo",
    start: "18/03/2026",
    tests: 3,
  },
  {
    id: "AV-2203",
    patient: "Renato Vitulli",
    examiner: "Dr. André",
    stage: "Aprovado",
    start: "11/03/2026",
    tests: 5,
  },
];

const testApplications = [
  {
    code: "WISC4",
    test: "WISC-IV",
    patient: "Marina Carvalho",
    method: "Faixa etária",
    progress: 86,
    state: "Pontuado",
  },
  {
    code: "BPA2",
    test: "BPA-2",
    patient: "Marina Carvalho",
    method: "Faixa etária",
    progress: 72,
    state: "Processado",
  },
  {
    code: "FDT",
    test: "FDT",
    patient: "João Pedro",
    method: "Manual",
    progress: 44,
    state: "Em conferência",
  },
  {
    code: "RAVLT",
    test: "RAVLT",
    patient: "Renato Vitulli",
    method: "Manual",
    progress: 100,
    state: "Final",
  },
];

const documents = [
  { name: "anamnese_marina.pdf", type: "PDF", status: "Extraído", linked: "AV-2201" },
  { name: "protocolo_wisc4_marina.jpg", type: "Imagem", status: "Pendente revisão", linked: "AV-2201" },
  { name: "ravlt_renato.pdf", type: "PDF", status: "Extraído", linked: "AV-2203" },
  { name: "laudo_joao_v2.docx", type: "DOCX", status: "Versionado", linked: "AV-2202" },
];

const reports = [
  { patient: "Marina Carvalho", version: "v1.4", section: "Conclusão", status: "Em revisão" },
  { patient: "João Pedro", version: "v2.1", section: "Funções executivas", status: "Rascunho IA" },
  { patient: "Renato Vitulli", version: "v3.0", section: "Final", status: "Aprovado" },
];

const availableTests = [
  ["WISC-IV", "Inteligência infantil"],
  ["WAIS-III", "Inteligência para adultos"],
  ["WASI", "Inteligência abreviada"],
  ["BPA-2", "Atenção"],
  ["FDT", "Funções executivas"],
  ["RAVLT", "Memória e aprendizagem"],
  ["SRS-2", "Responsividade social"],
  ["ETDAH-AD", "Autorrelato TDAH"],
  ["ETDAH-PAIS", "Pais"],
  ["SCARED", "Ansiedade"],
  ["EBADEP-A", "Depressão em adultos"],
  ["EBADEP-IJ", "Depressão infantojuvenil"],
  ["EPQ-J", "Personalidade infantojuvenil"],
];

const ebadepItems = [
  ["01", "1. Choro: ausência de vontade de chorar <-> vontade de chorar"],
  ["02", "2. Bem-estar: sentir-se muito bem <-> sentir-se mais angustiado"],
  ["03", "3. Tarefas: consegue realizar tarefas <-> sente-se impotente para realizá-las"],
  ["04", "4. Problemas: resolve problemas <-> sente-se menos capaz de enfrentá-los"],
  ["05", "5. Prazer: faz coisas de que gosta <-> não tem mais vontade de fazê-las"],
  ["06", "6. Choro recente: não tem chorado <-> tem chorado"],
  ["07", "7. Solidão: não sente solidão <-> sente-se cada vez mais sozinho"],
  ["08", "8. Comportamento: sabe agir nas situações <-> não sabe mais como agir"],
  ["09", "9. Autonomia: consegue se virar sozinho <-> não consegue mais"],
  ["10", "10. Futuro: acredita que será melhor <-> não acredita em melhora"],
  ["11", "11. Atitudes: parecem normais <-> parecem menos adequadas que antes"],
  ["12", "12. Planejamento: faz planos para o futuro <-> não consegue planejar"],
  ["13", "13. Crença em si: acredita em si mesmo <-> está acreditando menos em si"],
  ["14", "14. Decisão: não tem problemas para decidir <-> está mais difícil decidir"],
  ["15", "15. Escolhas: escolhe com facilidade <-> não consegue mais escolher sozinho"],
  ["16", "16. Independência: faz tarefas sem ajuda <-> precisa de ajuda para realizá-las"],
  ["17", "17. Atividades: sente prazer em realizá-las <-> elas não agradam como antes"],
  ["18", "18. Vida: sente-se feliz com a vida <-> antes era mais feliz"],
  ["19", "19. Situação atual: acha que as coisas vão bem <-> acha que nada vai bem"],
  ["20", "20. Utilidade: faz coisas que ajudam os outros <-> acha que não ajuda mais ninguém"],
  ["21", "21. Convívio: estar com pessoas é bom <-> passou a evitar encontros"],
  ["22", "22. Eventos sociais: vai a festas/reuniões <-> tem evitado mesmo convidado"],
  ["23", "23. Concentração: consegue se concentrar <-> não consegue mais"],
  ["24", "24. Ritmo de trabalho: realiza tarefas normalmente <-> está mais lento"],
  ["25", "25. Agitação: realiza tarefas normalmente <-> sente-se mais agitado"],
  ["26", "26. História de vida: sempre achou a vida boa <-> hoje avalia o passado como ruim"],
  ["27", "27. Energia matinal: sente-se disposto <-> acorda esgotado"],
  ["28", "28. Vida atual: acha a vida boa <-> percebe a vida cada vez pior"],
  ["29", "29. Ideias sobre morrer: morrer não é solução <-> pensa que seria melhor estar morto"],
  ["30", "30. Autoeficácia: acredita em si <-> não acredita mais em si"],
  ["31", "31. Sono: dorme bem <-> não consegue dormir a noite inteira"],
  ["32", "32. Necessário do dia a dia: faz o necessário normalmente <-> não consegue mais"],
  ["33", "33. Valor da vida: gosta muito da própria vida <-> não dá mais valor à vida"],
  ["34", "34. Autoimagem: gosta de si <-> não gosta mais de si"],
  ["35", "35. Finalização: termina tarefas <-> não termina mais"],
  ["36", "36. Tranquilidade: está tranquilo <-> perde a paciência com pouco"],
  ["37", "37. Nervosismo: não tem se sentido nervoso <-> qualquer coisa o deixa nervoso"],
  ["38", "38. Disposição: sente-se com disposição <-> anda mais cansado"],
  ["39", "39. Vontade de agir: sente-se disposto <-> não tem mais vontade de fazer as coisas"],
  ["40", "40. Padrão de sono: dorme normalmente <-> tem dormido muito"],
  ["41", "41. Apetite: fome continua como sempre <-> tem comido menos"],
  ["42", "42. Desejo sexual: continua como antes <-> vem diminuindo muito"],
  ["43", "43. Peso: continua o mesmo <-> emagreceu sem fazer regime"],
  ["44", "44. Medicação: toma remédio apenas quando precisa <-> toma por precaução"],
  ["45", "45. Culpa: não costuma sentir culpa <-> vem se sentindo culpado pelos problemas"],
];

const ebadepIjItems = [
  ["01", "Sente-se triste com frequência"],
  ["02", "Chora com facilidade"],
  ["03", "Perdeu o interesse pelas coisas que gostava"],
  ["04", "Sente-se cansado sem motivo"],
  ["05", "Fica irritado com facilidade"],
  ["06", "Tem dificuldade para dormir"],
  ["07", "Sente-se sozinho mesmo entre pessoas"],
  ["08", "Perdeu o apetite ou come demais"],
  ["09", "Sente-se feliz com a vida ★"],
  ["10", "Concentra-se facilmente nas atividades"],
  ["11", "Preocupa-se demais com o futuro"],
  ["12", "Tem boa relação com os colegas ★"],
  ["13", "Diverte-se com as atividades do dia a dia ★"],
  ["14", "Sente-se seguro(a) de si mesmo(a) ★"],
  ["15", "Tem esperança no futuro ★"],
  ["16", "Gosta de ir à escola ★"],
  ["17", "Consegue se expressar bem ★"],
  ["18", "Sente-se amado(a) pela família ★"],
  ["19", "Brinca e se diverte como antes ★"],
  ["20", "Sente-se preocupado(a) sem motivo"],
  ["21", "Evita sair de casa"],
  ["22", "Tem pensamentos negativos com frequência"],
  ["23", "Sente-se importante e valorizado(a) ★"],
  ["24", "Tem dificuldade para tomar decisões"],
  ["25", "Consegue lidar bem com os problemas ★"],
  ["26", "Sente-se desanimado(a) com frequência"],
  ["27", "Tem dificuldade para fazer as tarefas"],
];

const epqjItems = [
  ["01", "Alguma vez você já foi dormir sem escovar os dentes?"],
  ["02", "Você já chorou quando alguém riu de você na frente de outras pessoas?"],
  ["03", "Você se diverte com piadas que, às vezes, incomodam os outros?"],
  ["04", "Você sempre faz imediatamente o que lhe pedem?"],
  ["05", "Quando vai dormir, você tem pensamentos que lhe tiram o sono?"],
  ["06", "No colégio, você sempre cumpre tudo o que lhe dizem e mandam?"],
  ["07", "Você gostaria que outros colegas tivessem medo de você?"],
  ["08", "Você é muito alegre e animado(a)?"],
  ["09", "Há muitas coisas que incomodam você?"],
  ["10", "Você acha engraçado quando um colega cai e se machuca?"],
  ["11", "Você tem muitos amigos?"],
  ["12", "Alguma vez você se sentiu triste sem nenhum motivo?"],
  ["13", "Às vezes, você gosta de provocar e irritar os animais?"],
  ["14", "Alguma vez você fingiu que não ouviu quando alguém o(a) chamou?"],
  ["15", "Com frequência você pensa que a vida é muito triste?"],
  ["16", "Você frequentemente discute com seus colegas?"],
  ["17", "Em casa, você sempre acaba os deveres antes de sair para se divertir?"],
  ["18", "Você se preocupa com coisas ruins que possam acontecer no futuro?"],
  ["19", "Alguma vez você já substituiu o almoço por um hambúrguer?"],
  ["20", "Você se sente facilmente magoado(a) quando as pessoas encontram falhas em seu comportamento ou trabalho?"],
  ["21", "Você se assusta ao ver um acidente de carro com vítimas na rua?"],
  ["22", "Alguém quer se vingar de você por causa de alguma brincadeira de mau gosto que você fez gratuitamente?"],
  ["23", "Você acha que deve ser muito divertido saltar de uma cachoeira?"],
  ["24", "Você se sente frequentemente cansado(a) sem motivo?"],
  ["25", "Em geral, você acha divertido incomodar as pessoas?"],
  ["26", "Você sempre fica calado(a) quando as pessoas mais velhas estão falando?"],
  ["27", "Em geral, é você quem dá o primeiro passo para fazer um novo(a) amigo(a)?"],
  ["28", "Você sempre encontra defeito em qualquer coisa que faça?"],
  ["29", "Você acredita que se envolve em mais brigas que as outras pessoas?"],
  ["30", "Alguma vez você disse um palavrão ou insultou alguém?"],
  ["31", "Você gosta de contar piadas ou historinhas divertidas para seus amigos?"],
  ["32", "Em sala de aula, você entra em mais confusões ou problemas que os outros colegas?"],
  ["33", "Em geral, você recolhe do chão os papéis ou a sujeira que os colegas atiram na sala de aula?"],
  ["34", "Você tem muitos passatempos ou se interessa por muitas coisas diferentes?"],
  ["35", "Algumas coisas facilmente o(a) magoam ou o(a) deixam triste?"],
  ["36", "Você gosta de debochar ou pregar peça nos outros?"],
  ["37", "Alguma vez você desobedeceu a seus pais?"],
  ["38", "Frequentemente você se sente “cansado(a) de tudo”?"],
  ["39", "Às vezes, é bastante divertido ver como um grupo de meninos mais velhos incomoda ou assusta um menino menor?"],
  ["40", "Você sempre se comporta bem em sala de aula, mesmo que o professor não esteja nela?"],
  ["41", "Quando uma pessoa o critica, você passa muito tempo pensando no que ela disse?"],
  ["42", "Você acha que quando alguém nos provoca é melhor brigar que conversar?"],
  ["43", "Você sempre diz a verdade?"],
  ["44", "Você gosta de estar com outros colegas e se divertir com eles?"],
  ["45", "Você gostaria de pular de paraquedas?"],
  ["46", "Você sempre come tudo o que lhe põem no prato?"],
  ["47", "Sempre que alguém o(a) corrige na frente dos seus amigos ou familiares, você se sente envergonhado(a) ou magoado(a)?"],
  ["48", "Você alguma vez foi atrevido(a) com seus pais?"],
  ["49", "Você tem dificuldade de prestar atenção nas aulas da escola quando tem problemas em casa?"],
  ["50", "Você gosta de se jogar ou pular na água em uma piscina ou no mar?"],
  ["51", "Quando você está preocupado(a) com alguma coisa, tem dificuldade de dormir à noite?"],
  ["52", "As outras pessoas pensam que você é muito alegre e animado(a)?"],
  ["53", "Frequentemente você se sente sozinho(a)?"],
  ["54", "Você acha que uma criança de 6 anos deve ser protegida quando é agredida por um adolescente?"],
  ["55", "Você faz tudo o que seus pais lhe pedem?"],
  ["56", "Você gosta muito de passear?"],
  ["57", "Alguma vez você já deixou de fazer o dever de casa para assistir à televisão?"],
  ["58", "Algumas vezes você se sente alegre, outras vezes se sente triste, sem nenhum motivo?"],
  ["59", "Com frequência você precisa de bons amigos que lhe compreendam e animem?"],
  ["60", "Você gostaria de participar de um treinamento de sobrevivência na selva?"],
];

const wiscSubtests = [
  { label: "Cubos", sigla: "CB", optional: false },
  { label: "Semelhanças", sigla: "SM", optional: false },
  { label: "Dígitos", sigla: "DG", optional: false },
  { label: "Conceitos Figurativos", sigla: "CN", optional: false },
  { label: "Código", sigla: "CD", optional: false },
  { label: "Vocabulário", sigla: "VC", optional: false },
  { label: "Seq. de Núm. e Letras", sigla: "SNL", optional: false },
  { label: "Raciocínio Matricial", sigla: "RM", optional: false },
  { label: "Compreensão", sigla: "CO", optional: false },
  { label: "Procurar Símbolos", sigla: "PS", optional: false },
  { label: "Completar Figuras", sigla: "CF", optional: true },
  { label: "Cancelamento", sigla: "CA", optional: true },
  { label: "Informação", sigla: "IN", optional: true },
  { label: "Raciocínio com Palavras", sigla: "RP", optional: true },
];

const bpaDomains = [
  { title: "Atenção Concentrada", sigla: "AC" },
  { title: "Atenção Dividida", sigla: "AD" },
  { title: "Atenção Alternada", sigla: "AA" },
];

function StatCard({ title, value, hint, icon: Icon }) {
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

function SectionTitle({ title, subtitle, action }) {
  return (
    <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight text-slate-900">{title}</h2>
        <p className="text-sm text-slate-500 mt-1">{subtitle}</p>
      </div>
      {action}
    </div>
  );
}

function StatusBadge({ children }) {
  const map = {
    "Em avaliação": "bg-amber-50 text-amber-700 border-amber-200",
    "Laudo em redação": "bg-blue-50 text-blue-700 border-blue-200",
    "Finalizado": "bg-emerald-50 text-emerald-700 border-emerald-200",
    "Aguardando documentos": "bg-slate-100 text-slate-700 border-slate-200",
    "Coleta de dados": "bg-amber-50 text-amber-700 border-amber-200",
    "Redação do laudo": "bg-blue-50 text-blue-700 border-blue-200",
    "Aprovado": "bg-emerald-50 text-emerald-700 border-emerald-200",
    "Pontuado": "bg-violet-50 text-violet-700 border-violet-200",
    "Processado": "bg-cyan-50 text-cyan-700 border-cyan-200",
    "Em conferência": "bg-orange-50 text-orange-700 border-orange-200",
    "Final": "bg-emerald-50 text-emerald-700 border-emerald-200",
    "Extraído": "bg-cyan-50 text-cyan-700 border-cyan-200",
    "Pendente revisão": "bg-amber-50 text-amber-700 border-amber-200",
    "Versionado": "bg-violet-50 text-violet-700 border-violet-200",
    "Em revisão": "bg-blue-50 text-blue-700 border-blue-200",
    "Rascunho IA": "bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200",
  };

  return <Badge className={`rounded-full border ${map[children] || "bg-slate-100 text-slate-700 border-slate-200"}`}>{children}</Badge>;
}

function DashboardPage() {
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
              { title: "Pontuação de testes", value: 7, progress: 64, icon: BarChart3 },
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
                <p className="text-sm text-slate-700">{text}</p>
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
              <div key={label} className="rounded-2xl border border-slate-200 p-4 flex items-center gap-3">
                <div className="rounded-xl border border-slate-200 p-2"><Icon className="h-4 w-4" /></div>
                <span className="text-sm font-medium text-slate-800">{label}</span>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function TestApplicationForm({ patient, selectedTest, onBack }) {
  const isWisc = selectedTest === "WISC-IV";
  const isBpa = selectedTest === "BPA-2";
  const isEbadep = selectedTest === "EBADEP-A";
  const isEbadepIj = selectedTest === "EBADEP-IJ";
  const isEpqj = selectedTest === "EPQ-J";

  return (
    <div className="space-y-6">
      <SectionTitle
        title={`Aplicação do teste · ${selectedTest}`}
        subtitle={`Paciente: ${patient.name}. Preencha os dados necessários para iniciar a aplicação e o processamento técnico do instrumento.`}
        action={
          <div className="flex gap-2">
            <Button variant="outline" className="rounded-2xl gap-2" onClick={onBack}>
              <ArrowLeft className="h-4 w-4" /> Voltar
            </Button>
            <Button className="rounded-2xl gap-2">
              <Save className="h-4 w-4" /> Salvar aplicação
            </Button>
          </div>
        }
      />

      <div className="grid grid-cols-1 xl:grid-cols-[1.1fr_0.9fr] gap-4">
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Dados da aplicação</CardTitle>
            <CardDescription>Vínculo com paciente, avaliação e configuração do instrumento.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Paciente</label>
                <Input className="rounded-2xl" value={patient.name} readOnly />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Teste</label>
                <Input className="rounded-2xl" value={selectedTest} readOnly />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Avaliação vinculada</label>
                <Select>
                  <SelectTrigger className="rounded-2xl">
                    <SelectValue placeholder="Selecione a avaliação" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="av-2201">AV-2201 · Em andamento</SelectItem>
                    <SelectItem value="av-2202">AV-2202 · Redação do laudo</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Data de aplicação</label>
                <Input className="rounded-2xl" placeholder="dd/mm/aaaa" />
              </div>
            </div>

            {isWisc && (
              <>
                <Separator />
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-slate-800">Dados normativos do WISC-IV</p>
                    <p className="text-xs text-slate-500 mt-1">Esses campos são usados para calcular a idade e selecionar automaticamente a tabela CSV correta.</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Data de nascimento</label>
                      <Input className="rounded-2xl" placeholder="dd/mm/aaaa" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Data de aplicação</label>
                      <Input className="rounded-2xl" placeholder="dd/mm/aaaa" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Faixa etária calculada</label>
                      <Input className="rounded-2xl" value="idade_14-0-14-3.csv" readOnly />
                    </div>
                  </div>
                </div>

                <Separator />
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-medium text-slate-800">Subtestes do WISC-IV</p>
                      <p className="text-xs text-slate-500 mt-1">Modelo em tabela para digitação rápida dos pontos brutos, inspirado na ficha manual e adaptado para o sistema.</p>
                    </div>
                    <Button variant="outline" className="rounded-2xl gap-2">
                      <Wand2 className="h-4 w-4" /> Converter automaticamente
                    </Button>
                  </div>

                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
                    <div className="grid grid-cols-[1.6fr_120px_140px] bg-slate-100/80 px-4 py-3 text-sm font-medium text-slate-700">
                      <div>Subtestes</div>
                      <div className="text-center">PB</div>
                      <div className="text-center">Pontos Ponderados</div>
                    </div>

                    <div className="divide-y divide-slate-200">
                      {wiscSubtests.map((subtest, index) => (
                        <div
                          key={subtest.sigla}
                          className={`grid grid-cols-[1.6fr_120px_140px] items-center px-4 py-3 ${
                            subtest.optional
                              ? "bg-violet-50/70"
                              : index % 2 === 0
                                ? "bg-white"
                                : "bg-slate-50/60"
                          }`}
                        >
                          <div className="pr-4">
                            <div className="flex items-center gap-2">
                              <p className="text-sm font-medium text-slate-900">{subtest.label} ({subtest.sigla})</p>
                              {subtest.optional && (
                                <Badge variant="outline" className="rounded-full border-violet-200 bg-violet-100 text-violet-700">
                                  Opcional
                                </Badge>
                              )}
                            </div>
                          </div>
                          <div className="flex justify-center">
                            <Input
                              className={`h-10 w-20 rounded-xl text-center ${subtest.optional ? "border-violet-200 bg-white" : ""}`}
                              placeholder="—"
                            />
                          </div>
                          <div className="flex justify-center">
                            <div
                              className={`flex h-10 w-24 items-center justify-center rounded-xl border text-sm font-medium ${
                                subtest.optional
                                  ? "border-violet-200 bg-violet-100/80 text-violet-700"
                                  : "border-slate-200 bg-slate-100 text-slate-600"
                              }`}
                            >
                              —
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="rounded-2xl border p-4 bg-slate-50">
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Compreensão Verbal</p>
                      <div className="mt-3 flex items-end justify-between">
                        <span className="text-sm text-slate-600">Soma ICV</span>
                        <span className="text-2xl font-semibold text-slate-900">6</span>
                      </div>
                    </div>
                    <div className="rounded-2xl border p-4 bg-slate-50">
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Organização Perceptual</p>
                      <div className="mt-3 flex items-end justify-between">
                        <span className="text-sm text-slate-600">Soma IOP</span>
                        <span className="text-2xl font-semibold text-slate-900">6</span>
                      </div>
                    </div>
                    <div className="rounded-2xl border p-4 bg-slate-50">
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">Memória + Velocidade</p>
                      <div className="mt-3 flex items-end justify-between">
                        <span className="text-sm text-slate-600">IMO / IVP</span>
                        <span className="text-2xl font-semibold text-slate-900">2 / 3</span>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}

            {isBpa && (
              <>
                <Separator />
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-slate-800">Método normativo</p>
                    <p className="text-xs text-slate-500 mt-1">Escolha obrigatoriamente entre faixa etária e escolaridade para processar o BPA-2.</p>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Método</label>
                      <Select>
                        <SelectTrigger className="rounded-2xl">
                          <SelectValue placeholder="Selecione..." />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="age">Faixa etária</SelectItem>
                          <SelectItem value="schooling">Escolaridade</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Idade</label>
                      <Input className="rounded-2xl" placeholder="Ex: 13" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium text-slate-700">Escolaridade</label>
                      <Input className="rounded-2xl" placeholder="Ex: ensino_fundamental" />
                    </div>
                  </div>
                </div>

                <Separator />
                <div className="space-y-4">
                  <div>
                    <p className="text-sm font-medium text-slate-800">Campos do BPA-2</p>
                    <p className="text-xs text-slate-500 mt-1">Layout de preenchimento com os três domínios principais do teste: atenção concentrada, dividida e alternada.</p>
                  </div>

                  <div className="grid grid-cols-1 gap-5 max-w-xl">
                    {bpaDomains.map((domain) => (
                      <div key={domain.sigla} className="rounded-[28px] bg-neutral-100 p-6 space-y-5 shadow-sm border border-neutral-200">
                        <div>
                          <p className="text-[18px] font-semibold tracking-tight text-slate-900">{domain.title}</p>
                        </div>

                        <div className="space-y-4">
                          <div className="space-y-2">
                            <label className="block text-[15px] text-slate-700">Acertos</label>
                            <Input className="h-10 rounded-2xl border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="Digite o valor" />
                          </div>

                          <div className="space-y-2">
                            <label className="block text-[15px] text-slate-700">Erros</label>
                            <Input className="h-10 rounded-2xl border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="Digite o valor" />
                          </div>

                          <div className="space-y-2">
                            <label className="block text-[15px] text-slate-700">Omissões</label>
                            <Input className="h-10 rounded-2xl border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="Digite o valor" />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {isEbadep && (
              <>
                <Separator />
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-medium text-slate-800">Itens do Instrumento</p>
                      <p className="text-xs text-slate-500 mt-1">Tela de aplicação do EBADEP-A com os 45 itens do instrumento e campo de resposta para cada item.</p>
                    </div>
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                  </div>

                  <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 space-y-3">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">Instruções do teste</p>
                      <p className="text-sm text-slate-600 mt-1">Marque a intensidade correspondente à resposta do item.</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-slate-700">
                      <p><strong>0</strong> = Primeiro círculo (menor intensidade)</p>
                      <p><strong>1</strong> = Segundo círculo</p>
                      <p><strong>2</strong> = Terceiro círculo</p>
                      <p><strong>3</strong> = Quarto círculo (maior intensidade)</p>
                    </div>
                  </div>

                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
                    <div className="grid grid-cols-[90px_1fr_90px] bg-slate-100/80 px-4 py-3 text-sm font-medium text-slate-700">
                      <div>Item</div>
                      <div>Descrição</div>
                      <div className="text-center">Resposta</div>
                    </div>
                    <div className="divide-y divide-slate-200 max-h-[720px] overflow-y-auto">
                      {ebadepItems.map(([code, text], index) => (
                        <div
                          key={code}
                          className={`grid grid-cols-[90px_1fr_90px] items-center gap-4 px-4 py-3 ${index % 2 === 0 ? "bg-white" : "bg-slate-50/60"}`}
                        >
                          <div>
                            <p className="text-sm font-semibold text-slate-900">{code}</p>
                          </div>
                          <div>
                            <p className="text-sm text-slate-800 leading-6">{text}</p>
                          </div>
                          <div className="flex justify-center">
                            <Input className="h-10 w-16 rounded-xl text-center border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="—" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end gap-2">
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                    <Button variant="outline" className="rounded-2xl">
                      Limpar
                    </Button>
                  </div>
                </div>
              </>
            )}

            {isEbadepIj && (
              <>
                <Separator />
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-medium text-slate-800">Itens do Instrumento</p>
                      <p className="text-xs text-slate-500 mt-1">Tela de aplicação do EBADEP-IJ com os itens do instrumento e campo de resposta para cada item.</p>
                    </div>
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                  </div>

                  <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 space-y-3">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">Instruções do teste</p>
                      <p className="text-sm text-slate-600 mt-1">Marque a frequência correspondente à resposta do item.</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-sm text-slate-700">
                      <p><strong>0</strong> = Nunca / Poucas vezes</p>
                      <p><strong>1</strong> = Algumas vezes</p>
                      <p><strong>2</strong> = Muitas vezes / Sempre</p>
                    </div>
                  </div>

                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
                    <div className="grid grid-cols-[90px_1fr_90px] bg-slate-100/80 px-4 py-3 text-sm font-medium text-slate-700">
                      <div>Item</div>
                      <div>Descrição</div>
                      <div className="text-center">Resposta</div>
                    </div>
                    <div className="divide-y divide-slate-200 max-h-[720px] overflow-y-auto">
                      {ebadepIjItems.map(([code, text], index) => (
                        <div
                          key={code}
                          className={`grid grid-cols-[90px_1fr_90px] items-center gap-4 px-4 py-3 ${index % 2 === 0 ? "bg-white" : "bg-slate-50/60"}`}
                        >
                          <div>
                            <p className="text-sm font-semibold text-slate-900">{code}</p>
                          </div>
                          <div>
                            <p className="text-sm text-slate-800 leading-6">{text}</p>
                          </div>
                          <div className="flex justify-center">
                            <Input className="h-10 w-16 rounded-xl text-center border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="—" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end gap-2">
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                    <Button variant="outline" className="rounded-2xl">
                      Limpar
                    </Button>
                  </div>
                </div>
              </>
            )}

            {isEpqj && (
              <>
                <Separator />
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-medium text-slate-800">Itens do Instrumento</p>
                      <p className="text-xs text-slate-500 mt-1">Tela de aplicação do EPQ-J com marcação binária para resposta Sim ou Não.</p>
                    </div>
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                  </div>

                  <div className="rounded-2xl border border-sky-200 bg-sky-50/70 p-4 space-y-3">
                    <div>
                      <p className="text-sm font-semibold text-slate-900">Instruções do teste</p>
                      <p className="text-sm text-slate-600 mt-1">Para cada item, o psicólogo deverá marcar os valores 1 ou 0 de acordo com a resposta Sim ou Não dada pelo respondente.</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-slate-700">
                      <p><strong>1</strong> = Sim</p>
                      <p><strong>0</strong> = Não</p>
                    </div>
                  </div>

                  <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">
                    <div className="grid grid-cols-[90px_1fr_90px] bg-slate-100/80 px-4 py-3 text-sm font-medium text-slate-700">
                      <div>Item</div>
                      <div>Descrição</div>
                      <div className="text-center">Resposta</div>
                    </div>
                    <div className="divide-y divide-slate-200 max-h-[720px] overflow-y-auto">
                      {epqjItems.map(([code, text], index) => (
                        <div
                          key={code}
                          className={`grid grid-cols-[90px_1fr_90px] items-center gap-4 px-4 py-3 ${index % 2 === 0 ? "bg-white" : "bg-slate-50/60"}`}
                        >
                          <div>
                            <p className="text-sm font-semibold text-slate-900">{code}</p>
                          </div>
                          <div>
                            <p className="text-sm text-slate-800 leading-6">{text}</p>
                          </div>
                          <div className="flex justify-center">
                            <Input className="h-10 w-16 rounded-xl text-center border-slate-200 bg-white shadow-sm transition-colors hover:border-sky-300 hover:bg-sky-50/50" placeholder="0/1" />
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end gap-2">
                    <Button variant="outline" className="rounded-2xl gap-2">
                      Salvar respostas
                    </Button>
                    <Button variant="outline" className="rounded-2xl">
                      Limpar
                    </Button>
                  </div>
                </div>
              </>
            )}

            {!isWisc && !isBpa && !isEbadep && !isEbadepIj && !isEpqj && (
              <>
                <Separator />
                <div className="rounded-2xl border border-dashed p-8 text-center text-sm text-slate-500">
                  Estrutura base da aplicação pronta. O layout específico deste teste pode ser expandido com campos, regras e processamento próprios.
                </div>
              </>
            )}
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Painel lateral da aplicação</CardTitle>
            <CardDescription>Resumo técnico, status e ações rápidas do teste selecionado.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="rounded-2xl border p-4 bg-slate-50">
              <p className="text-sm text-slate-500">Paciente</p>
              <p className="mt-2 font-medium text-slate-900">{patient.name}</p>
              <p className="text-xs text-slate-500 mt-1">{patient.id} · {patient.age}</p>
            </div>
            <div className="rounded-2xl border p-4">
              <p className="text-sm text-slate-500">Teste</p>
              <p className="mt-2 font-medium text-slate-900">{selectedTest}</p>
            </div>
            <div className="rounded-2xl border p-4">
              <p className="text-sm text-slate-500">Status da aplicação</p>
              <div className="mt-2"><StatusBadge>Em conferência</StatusBadge></div>
            </div>
            <div className="rounded-2xl border p-4">
              <p className="text-sm font-medium text-slate-800">Ações</p>
              <div className="mt-3 grid gap-2">
                <Button className="rounded-2xl gap-2 justify-start">
                  <Wand2 className="h-4 w-4" /> Processar teste
                </Button>
                <Button variant="outline" className="rounded-2xl gap-2 justify-start">
                  <Save className="h-4 w-4" /> Salvar rascunho
                </Button>
                <Button variant="outline" className="rounded-2xl gap-2 justify-start">
                  <Eye className="h-4 w-4" /> Pré-visualizar resultado
                </Button>
              </div>
            </div>
            <div className="rounded-2xl border p-4 text-sm text-slate-600">
              Este layout simula a tela que o usuário verá ao clicar em <strong>Iniciar aplicação do teste</strong>, com campos específicos por instrumento e painel lateral de apoio.
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function PatientsPage() {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [selectedPatientId, setSelectedPatientId] = useState(patients[0]?.id ?? null);
  const [selectedTest, setSelectedTest] = useState("WISC-IV");
  const [showTestApplication, setShowTestApplication] = useState(false);

  const selectedPatient = patients.find((item) => item.id === selectedPatientId) ?? null;

  if (showTestApplication && selectedPatient) {
    return (
      <TestApplicationForm
        patient={selectedPatient}
        selectedTest={selectedTest}
        onBack={() => setShowTestApplication(false)}
      />
    );
  }

  return (
    <div className="space-y-6">
      <SectionTitle
        title="Pacientes"
        subtitle="Cadastro clínico com busca rápida, dados demográficos e acesso ao histórico de avaliações."
        action={
          <Button className="rounded-2xl gap-2" onClick={() => setShowCreateForm((prev) => !prev)}>
            <Plus className="h-4 w-4" /> {showCreateForm ? "Fechar cadastro" : "Novo paciente"}
          </Button>
        }
      />

      {showCreateForm && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Cadastro de paciente</CardTitle>
              <CardDescription>Preencha os dados principais para criar um novo cadastro clínico no sistema.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                <div className="xl:col-span-2 space-y-2">
                  <label className="text-sm font-medium text-slate-700">Nome Completo *</label>
                  <Input className="rounded-2xl" placeholder="Digite o nome completo do paciente" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Data de Nascimento</label>
                  <Input className="rounded-2xl" placeholder="dd/mm/aaaa" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Sexo</label>
                  <Select>
                    <SelectTrigger className="rounded-2xl">
                      <SelectValue placeholder="Selecione..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="feminino">Feminino</SelectItem>
                      <SelectItem value="masculino">Masculino</SelectItem>
                      <SelectItem value="outro">Outro</SelectItem>
                      <SelectItem value="nao_informado">Não informado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Escolaridade</label>
                  <Input className="rounded-2xl" placeholder="Ex: 5º ano fundamental" />
                </div>

                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium text-slate-700">Escola</label>
                  <Input className="rounded-2xl" placeholder="Digite o nome da escola" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Telefone</label>
                  <Input className="rounded-2xl" placeholder="(00) 00000-0000" />
                </div>

                <div className="space-y-2 md:col-span-2">
                  <label className="text-sm font-medium text-slate-700">E-mail</label>
                  <Input className="rounded-2xl" placeholder="responsavel@email.com" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Nome da Mãe</label>
                  <Input className="rounded-2xl" placeholder="Digite o nome da mãe" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Nome do Pai</label>
                  <Input className="rounded-2xl" placeholder="Digite o nome do pai" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Cidade</label>
                  <Input className="rounded-2xl" placeholder="Ex: Goiânia" />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Estado</label>
                  <Input className="rounded-2xl" placeholder="Ex: GO" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Observações</label>
                <textarea
                  className="min-h-[130px] w-full rounded-2xl border border-slate-200 bg-white px-3 py-3 text-sm text-slate-900 outline-none ring-0 placeholder:text-slate-400 focus:border-slate-300"
                  placeholder="Adicione observações relevantes para o cadastro clínico do paciente"
                />
              </div>

              <div className="flex flex-col gap-3 border-t border-slate-200 pt-4 md:flex-row md:items-center md:justify-between">
                <p className="text-sm text-slate-500">Os campos marcados com * são obrigatórios para criação do cadastro.</p>
                <div className="flex gap-2">
                  <Button variant="outline" className="rounded-2xl" onClick={() => setShowCreateForm(false)}>
                    Cancelar
                  </Button>
                  <Button className="rounded-2xl gap-2">
                    <CheckCircle2 className="h-4 w-4" /> Salvar paciente
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-[1.25fr_0.95fr] gap-4">
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardContent className="p-4 space-y-4">
            <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
              <div className="flex items-center gap-3 w-full md:max-w-md">
                <div className="relative w-full">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                  <Input className="pl-9 rounded-2xl" placeholder="Buscar por nome, mãe, pai, e-mail ou telefone" />
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" className="rounded-2xl gap-2"><Filter className="h-4 w-4" /> Filtros</Button>
                <Button variant="outline" className="rounded-2xl gap-2"><Download className="h-4 w-4" /> Exportar</Button>
              </div>
            </div>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Paciente</TableHead>
                  <TableHead>Idade</TableHead>
                  <TableHead>Cidade</TableHead>
                  <TableHead>Última avaliação</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {patients.map((item) => {
                  const selected = item.id === selectedPatientId;
                  return (
                    <TableRow
                      key={item.id}
                      className={`cursor-pointer transition ${selected ? "bg-slate-100/80" : ""}`}
                      onClick={() => setSelectedPatientId(item.id)}
                    >
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <Avatar><AvatarFallback>{item.name.split(" ").slice(0,2).map(v=>v[0]).join("")}</AvatarFallback></Avatar>
                          <div>
                            <p className="font-medium text-slate-900">{item.name}</p>
                            <p className="text-xs text-slate-500">{item.id}</p>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>{item.age}</TableCell>
                      <TableCell>{item.city}</TableCell>
                      <TableCell>{item.lastEvaluation}</TableCell>
                      <TableCell><StatusBadge>{item.status}</StatusBadge></TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Paciente selecionado</CardTitle>
            <CardDescription>Resumo do cadastro e ações rápidas para iniciar testes e avaliações.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            {selectedPatient ? (
              <>
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <div className="flex items-center gap-3">
                    <Avatar className="h-12 w-12"><AvatarFallback>{selectedPatient.name.split(" ").slice(0,2).map(v=>v[0]).join("")}</AvatarFallback></Avatar>
                    <div>
                      <p className="text-lg font-semibold text-slate-900">{selectedPatient.name}</p>
                      <p className="text-sm text-slate-500">{selectedPatient.id} · {selectedPatient.age}</p>
                    </div>
                  </div>
                  <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
                    <div>
                      <p className="text-slate-500">Cidade</p>
                      <p className="font-medium text-slate-800">{selectedPatient.city}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Status</p>
                      <div className="mt-1"><StatusBadge>{selectedPatient.status}</StatusBadge></div>
                    </div>
                    <div className="col-span-2">
                      <p className="text-slate-500">Última avaliação</p>
                      <p className="font-medium text-slate-800">{selectedPatient.lastEvaluation}</p>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div>
                    <p className="text-sm font-medium text-slate-800">Escolher teste a ser aplicado</p>
                    <p className="text-xs text-slate-500 mt-1">Selecione o instrumento e inicie uma nova aplicação para este paciente.</p>
                  </div>
                  <Select value={selectedTest} onValueChange={setSelectedTest}>
                    <SelectTrigger className="rounded-2xl">
                      <SelectValue placeholder="Selecione o teste" />
                    </SelectTrigger>
                    <SelectContent>
                      {availableTests.map(([name, category]) => (
                        <SelectItem key={name} value={name}>
                          {name} · {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Teste selecionado</p>
                    <p className="mt-2 font-medium text-slate-900">{selectedTest}</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-2">
                  <Button className="rounded-2xl gap-2 justify-start" onClick={() => setShowTestApplication(true)}>
                    <FlaskConical className="h-4 w-4" /> Iniciar aplicação do teste
                  </Button>
                  <Button variant="outline" className="rounded-2xl gap-2 justify-start">
                    <ClipboardList className="h-4 w-4" /> Abrir nova avaliação
                  </Button>
                  <Button variant="outline" className="rounded-2xl gap-2 justify-start">
                    <Eye className="h-4 w-4" /> Ver histórico do paciente
                  </Button>
                </div>
              </>
            ) : (
              <div className="rounded-2xl border border-dashed p-8 text-center text-sm text-slate-500">
                Selecione um paciente na lista para visualizar o cadastro e escolher os testes a serem aplicados.
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function EvaluationsPage() {
  const [showCreateEvaluation, setShowCreateEvaluation] = useState(false);
  const [showLinkedTestApplication, setShowLinkedTestApplication] = useState(false);
  const [selectedLinkedTest, setSelectedLinkedTest] = useState(null);
  const [selectedEvaluationTest, setSelectedEvaluationTest] = useState("WISC-IV");
  const [evaluationList, setEvaluationList] = useState(evaluations);
  const [selectedEvaluationId, setSelectedEvaluationId] = useState(evaluations[0]?.id ?? null);
  const [linkedTests, setLinkedTests] = useState([
    {
      evaluationId: "AV-2201",
      code: "WISC4",
      test: "WISC-IV",
      patient: "Marina Carvalho",
      method: "Faixa etária",
      progress: 86,
      state: "Pontuado",
      date: "20/03/2026",
    },
    {
      evaluationId: "AV-2201",
      code: "BPA2",
      test: "BPA-2",
      patient: "Marina Carvalho",
      method: "Faixa etária",
      progress: 72,
      state: "Processado",
      date: "20/03/2026",
    },
    {
      evaluationId: "AV-2202",
      code: "FDT",
      test: "FDT",
      patient: "João Pedro",
      method: "Manual",
      progress: 44,
      state: "Em conferência",
      date: "19/03/2026",
    },
    {
      evaluationId: "AV-2203",
      code: "RAVLT",
      test: "RAVLT",
      patient: "Renato Vitulli",
      method: "Manual",
      progress: 100,
      state: "Final",
      date: "12/03/2026",
    },
  ]);

  const [newEvaluationForm, setNewEvaluationForm] = useState({
    patientId: patients[0]?.id ?? "",
    examiner: "Dr. André",
    status: "Coleta de dados",
    start: "",
    end: "",
    referralReason: "",
    purpose: "",
    notes: "",
  });

  const selectedEvaluation = evaluationList.find((item) => item.id === selectedEvaluationId) ?? evaluationList[0];
  const selectedPatient = patients.find((item) => item.name === selectedEvaluation?.patient);
  const selectedEvaluationTests = linkedTests.filter((item) => item.evaluationId === selectedEvaluation?.id);

  if (showLinkedTestApplication && selectedLinkedTest) {
    const linkedPatient = patients.find((item) => item.name === selectedLinkedTest.patient) ?? patients[0];
    return (
      <TestApplicationForm
        patient={linkedPatient}
        selectedTest={selectedLinkedTest.test}
        onBack={() => {
          setShowLinkedTestApplication(false);
          setSelectedLinkedTest(null);
        }}
      />
    );
  }

  const handleCreateEvaluation = () => {
    const patient = patients.find((item) => item.id === newEvaluationForm.patientId) ?? patients[0];
    const nextNumber = 2201 + evaluationList.length;
    const nextEvaluation = {
      id: `AV-${nextNumber}`,
      patient: patient.name,
      patientAge: patient.age,
      examiner: newEvaluationForm.examiner || "Dr. André",
      stage: newEvaluationForm.status || "Coleta de dados",
      start: newEvaluationForm.start || "Hoje",
      end: newEvaluationForm.end || "—",
      tests: 0,
      referralReason: newEvaluationForm.referralReason || "Motivo do encaminhamento não informado.",
      purpose: newEvaluationForm.purpose || "Finalidade da avaliação não informada.",
      notes: newEvaluationForm.notes || "Sem observações iniciais registradas.",
    };

    setEvaluationList((prev) => [nextEvaluation, ...prev]);
    setSelectedEvaluationId(nextEvaluation.id);
    setShowCreateEvaluation(false);
    setNewEvaluationForm({
      patientId: patients[0]?.id ?? "",
      examiner: "Dr. André",
      status: "Coleta de dados",
      start: "",
      end: "",
      referralReason: "",
      purpose: "",
      notes: "",
    });
  };

  const handleLinkTest = () => {
    if (!selectedEvaluation) return;

    const codeMap = {
      "WISC-IV": "WISC4",
      "WAIS-III": "WAIS3",
      "WASI": "WASI",
      "BPA-2": "BPA2",
      "FDT": "FDT",
      "RAVLT": "RAVLT",
      "SRS-2": "SRS2",
      "ETDAH-AD": "ETDAH-AD",
      "ETDAH-PAIS": "ETDAH-PAIS",
      "SCARED": "SCARED",
      "EBADEP-A": "EBADEP-A",
      "EBADEP-IJ": "EBADEP-IJ",
      "EPQ-J": "EPQ-J",
    };

    const methodMap = {
      "WISC-IV": "Faixa etária",
      "WAIS-III": "Manual",
      "WASI": "Manual",
      "BPA-2": "Faixa etária",
      "FDT": "Manual",
      "RAVLT": "Manual",
      "SRS-2": "Manual",
      "ETDAH-AD": "Manual",
      "ETDAH-PAIS": "Manual",
      "SCARED": "Manual",
      "EBADEP-A": "Manual",
      "EBADEP-IJ": "Manual",
      "EPQ-J": "Manual",
    };

    const newLinkedTest = {
      evaluationId: selectedEvaluation.id,
      code: codeMap[selectedEvaluationTest] || selectedEvaluationTest.toUpperCase(),
      test: selectedEvaluationTest,
      patient: selectedEvaluation.patient,
      method: methodMap[selectedEvaluationTest] || "Manual",
      progress: 0,
      state: "Em conferência",
      date: "Hoje",
    };

    setLinkedTests((prev) => [newLinkedTest, ...prev]);
    setEvaluationList((prev) =>
      prev.map((item) =>
        item.id === selectedEvaluation.id ? { ...item, tests: (item.tests || 0) + 1 } : item
      )
    );
  };

  return (
    <div className="space-y-6">
      <SectionTitle
        title="Avaliações"
        subtitle="Painel do caso clínico com visão integrada do paciente, testes, documentos, evolução e laudo."
        action={
          <Button className="rounded-2xl gap-2" onClick={() => setShowCreateEvaluation((prev) => !prev)}>
            <ClipboardList className="h-4 w-4" /> {showCreateEvaluation ? "Fechar formulário" : "Nova avaliação"}
          </Button>
        }
      />

      {showCreateEvaluation && (
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Nova avaliação</CardTitle>
              <CardDescription>Preencha os dados principais para abrir um novo caso clínico no sistema.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Paciente</label>
                  <Select value={newEvaluationForm.patientId} onValueChange={(value) => setNewEvaluationForm((prev) => ({ ...prev, patientId: value }))}>
                    <SelectTrigger className="rounded-2xl">
                      <SelectValue placeholder="Selecione o paciente" />
                    </SelectTrigger>
                    <SelectContent>
                      {patients.map((patient) => (
                        <SelectItem key={patient.id} value={patient.id}>
                          {patient.name}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Responsável</label>
                  <Select value={newEvaluationForm.examiner} onValueChange={(value) => setNewEvaluationForm((prev) => ({ ...prev, examiner: value }))}>
                    <SelectTrigger className="rounded-2xl">
                      <SelectValue placeholder="Selecione o profissional" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Dr. André">Dr. André</SelectItem>
                      <SelectItem value="Assistente clínico">Assistente clínico</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Status inicial</label>
                  <Select value={newEvaluationForm.status} onValueChange={(value) => setNewEvaluationForm((prev) => ({ ...prev, status: value }))}>
                    <SelectTrigger className="rounded-2xl">
                      <SelectValue placeholder="Selecione o status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Rascunho">Rascunho</SelectItem>
                      <SelectItem value="Coleta de dados">Coleta de dados</SelectItem>
                      <SelectItem value="Redação do laudo">Redação do laudo</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Data de início</label>
                  <Input className="rounded-2xl" placeholder="dd/mm/aaaa" value={newEvaluationForm.start} onChange={(e) => setNewEvaluationForm((prev) => ({ ...prev, start: e.target.value }))} />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium text-slate-700">Data de término</label>
                  <Input className="rounded-2xl" placeholder="dd/mm/aaaa" value={newEvaluationForm.end} onChange={(e) => setNewEvaluationForm((prev) => ({ ...prev, end: e.target.value }))} />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Motivo do encaminhamento</label>
                <textarea
                  className="min-h-[110px] w-full rounded-2xl border border-slate-200 bg-white px-3 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-slate-300"
                  placeholder="Descreva o motivo do encaminhamento clínico"
                  value={newEvaluationForm.referralReason}
                  onChange={(e) => setNewEvaluationForm((prev) => ({ ...prev, referralReason: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Finalidade da avaliação</label>
                <textarea
                  className="min-h-[110px] w-full rounded-2xl border border-slate-200 bg-white px-3 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-slate-300"
                  placeholder="Descreva o objetivo principal da avaliação"
                  value={newEvaluationForm.purpose}
                  onChange={(e) => setNewEvaluationForm((prev) => ({ ...prev, purpose: e.target.value }))}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">Observações gerais</label>
                <textarea
                  className="min-h-[130px] w-full rounded-2xl border border-slate-200 bg-white px-3 py-3 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-slate-300"
                  placeholder="Adicione observações clínicas, administrativas ou operacionais do caso"
                  value={newEvaluationForm.notes}
                  onChange={(e) => setNewEvaluationForm((prev) => ({ ...prev, notes: e.target.value }))}
                />
              </div>

              <div className="flex flex-col gap-3 border-t border-slate-200 pt-4 md:flex-row md:items-center md:justify-between">
                <p className="text-sm text-slate-500">Ao salvar, a avaliação será criada e ficará disponível para vincular testes, documentos e laudo.</p>
                <div className="flex gap-2">
                  <Button variant="outline" className="rounded-2xl" onClick={() => setShowCreateEvaluation(false)}>
                    Cancelar
                  </Button>
                  <Button className="rounded-2xl gap-2" onClick={handleCreateEvaluation}>
                    <CheckCircle2 className="h-4 w-4" /> Salvar avaliação
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-[1.1fr_0.9fr] gap-4">
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardContent className="p-5 space-y-5">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
              <div className="space-y-4 flex-1">
                <div className="flex items-center gap-3">
                  <div className="rounded-2xl border border-slate-200 bg-white p-3">
                    <ClipboardList className="h-5 w-5 text-slate-700" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-500">Avaliação ativa</p>
                    <h3 className="text-2xl font-semibold tracking-tight text-slate-900">{selectedEvaluation?.id}</h3>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                  <div>
                    <p className="text-slate-500">Paciente</p>
                    <p className="mt-1 font-medium text-slate-900">{selectedEvaluation?.patient}</p>
                    <p className="text-slate-500">{selectedEvaluation?.patientAge || selectedPatient?.age}</p>
                  </div>
                  <div>
                    <p className="text-slate-500">Responsável</p>
                    <p className="mt-1 font-medium text-slate-900">{selectedEvaluation?.examiner}</p>
                  </div>
                  <div>
                    <p className="text-slate-500">Data de início</p>
                    <p className="mt-1 font-medium text-slate-900">{selectedEvaluation?.start}</p>
                  </div>
                  <div>
                    <p className="text-slate-500">Data de término</p>
                    <p className="mt-1 font-medium text-slate-900">{selectedEvaluation?.end}</p>
                  </div>
                </div>
              </div>

              <div className="flex flex-col items-start gap-3 lg:items-end">
                <StatusBadge>{selectedEvaluation?.stage}</StatusBadge>
                <div className="flex flex-wrap gap-2">
                  <Button className="rounded-2xl gap-2" onClick={handleLinkTest}><FlaskConical className="h-4 w-4" /> Adicionar teste</Button>
                  <Button variant="outline" className="rounded-2xl gap-2"><Upload className="h-4 w-4" /> Anexar documento</Button>
                  <Button variant="outline" className="rounded-2xl gap-2"><FileText className="h-4 w-4" /> Abrir laudo</Button>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-[0.9fr_1.1fr] gap-4">
              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-sm font-medium text-slate-800 mb-3">Lista de avaliações</p>
                <div className="space-y-2">
                  {evaluationList.map((item) => {
                    const active = item.id === selectedEvaluationId;
                    return (
                      <button
                        key={item.id}
                        onClick={() => setSelectedEvaluationId(item.id)}
                        className={`w-full rounded-2xl border px-4 py-3 text-left transition ${active ? "border-slate-900 bg-white shadow-sm" : "border-slate-200 bg-white hover:bg-slate-50"}`}
                      >
                        <div className="flex items-center justify-between gap-3">
                          <div>
                            <p className="text-sm font-medium text-slate-900">{item.id}</p>
                            <p className="text-xs text-slate-500 mt-1">{item.patient}</p>
                          </div>
                          <StatusBadge>{item.stage}</StatusBadge>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-[1fr_auto] gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <div className="grid grid-cols-1 md:grid-cols-[1fr_220px] gap-3 items-end">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-slate-700">Adicionar teste para aplicar nesta avaliação</label>
                    <Select value={selectedEvaluationTest} onValueChange={setSelectedEvaluationTest}>
                      <SelectTrigger className="rounded-2xl bg-white">
                        <SelectValue placeholder="Selecione o teste" />
                      </SelectTrigger>
                      <SelectContent>
                        {availableTests.map(([name, category]) => (
                          <SelectItem key={name} value={name}>
                            {name} · {category}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3">
                    <p className="text-xs text-slate-500">Selecionado</p>
                    <p className="mt-1 text-sm font-medium text-slate-900">{selectedEvaluationTest}</p>
                  </div>
                </div>
                <div className="flex items-end">
                  <Button className="rounded-2xl gap-2 w-full xl:w-auto" onClick={handleLinkTest}>
                    <Plus className="h-4 w-4" /> Vincular teste
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Resumo operacional</CardTitle>
            <CardDescription>Situação atual do caso e próximos passos.</CardDescription>
          </CardHeader>
          <CardContent className="grid grid-cols-2 gap-3">
            {[
              ["Testes vinculados", String(selectedEvaluationTests.length)],
              ["Documentos", String(documents.filter((item) => item.linked === selectedEvaluation?.id).length)],
              ["Pendências", "2"],
              ["Versão do laudo", "v1.4"],
            ].map(([title, value]) => (
              <div key={title} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-wide text-slate-500">{title}</p>
                <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">{value}</p>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard title="Testes aplicados" value={String(selectedEvaluationTests.length)} hint="vinculados a esta avaliação" icon={FlaskConical} />
        <StatCard title="Documentos anexados" value={String(documents.filter((item) => item.linked === selectedEvaluation?.id).length)} hint="arquivos do caso" icon={FolderOpen} />
        <StatCard title="Laudo" value="68%" hint="em redação" icon={FileText} />
        <StatCard title="Alertas" value="2" hint="1 inconsistência, 1 pendência" icon={AlertTriangle} />
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList className="rounded-2xl bg-slate-100">
          <TabsTrigger value="overview" className="rounded-xl">Visão geral</TabsTrigger>
          <TabsTrigger value="tests" className="rounded-xl">Testes</TabsTrigger>
          <TabsTrigger value="documents" className="rounded-xl">Documentos</TabsTrigger>
          <TabsTrigger value="evolution" className="rounded-xl">Evolução</TabsTrigger>
          <TabsTrigger value="report" className="rounded-xl">Laudo</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          <div className="grid grid-cols-1 xl:grid-cols-[1.15fr_0.85fr] gap-4">
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Dados clínicos principais</CardTitle>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <p className="text-sm text-slate-500">Motivo do encaminhamento</p>
                  <p className="mt-2 text-sm leading-7 text-slate-800">{selectedEvaluation?.referralReason}</p>
                </div>
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <p className="text-sm text-slate-500">Finalidade da avaliação</p>
                  <p className="mt-2 text-sm leading-7 text-slate-800">{selectedEvaluation?.purpose}</p>
                </div>
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <p className="text-sm text-slate-500">Observações gerais</p>
                  <p className="mt-2 text-sm leading-7 text-slate-800">{selectedEvaluation?.notes}</p>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Pipeline da avaliação</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  ["Cadastro do paciente concluído", true],
                  ["Abertura da avaliação realizada", true],
                  ["Testes principais adicionados", selectedEvaluationTests.length > 0],
                  ["Processamento e revisão técnica", false],
                  ["Redação do laudo", false],
                  ["Aprovação final e exportação", false],
                ].map(([label, done], index) => (
                  <div key={label} className="flex items-center gap-3 rounded-2xl border border-slate-200 p-3">
                    <div className={`h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium ${done ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-700"}`}>
                      {index + 1}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-800">{label}</p>
                    </div>
                    {done ? <CheckCircle2 className="h-4 w-4 text-emerald-600" /> : <Clock3 className="h-4 w-4 text-slate-400" />}
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="tests">
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Testes vinculados à avaliação</CardTitle>
              <CardDescription>Instrumentos já cadastrados e estágio de processamento.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Teste</TableHead>
                    <TableHead>Data</TableHead>
                    <TableHead>Método</TableHead>
                    <TableHead>Progresso</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {selectedEvaluationTests.map((item) => (
                    <TableRow
                      key={item.code + item.patient + item.evaluationId}
                      className="cursor-pointer hover:bg-slate-50"
                      onClick={() => {
                        setSelectedLinkedTest(item);
                        setShowLinkedTestApplication(true);
                      }}
                    >
                      <TableCell>
                        <div>
                          <p className="font-medium text-slate-900">{item.test}</p>
                          <p className="text-xs text-slate-500">{item.code}</p>
                        </div>
                      </TableCell>
                      <TableCell>{item.date}</TableCell>
                      <TableCell>{item.method}</TableCell>
                      <TableCell className="w-[220px]">
                        <div className="flex items-center gap-3">
                          <Progress value={item.progress} className="h-2" />
                          <span className="text-xs text-slate-500 w-10">{item.progress}%</span>
                        </div>
                      </TableCell>
                      <TableCell><StatusBadge>{item.state}</StatusBadge></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="documents">
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardHeader>
              <CardTitle>Documentos do caso</CardTitle>
              <CardDescription>Arquivos enviados, extraídos e vinculados à avaliação.</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Arquivo</TableHead>
                    <TableHead>Tipo</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Vínculo</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {documents.filter((item) => item.linked === selectedEvaluation?.id).map((item) => (
                    <TableRow key={item.name}>
                      <TableCell>{item.name}</TableCell>
                      <TableCell>{item.type}</TableCell>
                      <TableCell><StatusBadge>{item.status}</StatusBadge></TableCell>
                      <TableCell>{item.linked}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="evolution">
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
            {[
              {
                date: "19/03/2026",
                title: "Sessão inicial e abertura do caso",
                content: "Realizada entrevista inicial, revisão do encaminhamento médico e organização dos documentos já disponíveis. Paciente apresentou boa colaboração e compreensão geral da proposta avaliativa.",
              },
              {
                date: "20/03/2026",
                title: "Aplicação de WISC-IV e BPA-2",
                content: "Aplicados instrumentos principais. Observou-se oscilação do foco ao longo das tarefas mais extensas, com melhor engajamento em atividades visuais estruturadas.",
              },
              {
                date: "22/03/2026",
                title: "Conferência de resultados e integração inicial",
                content: "Iniciada a conferência técnica dos resultados e preparação da redação do laudo. Identificadas pendências para conclusão de uma análise executiva complementar.",
              },
            ].map((item) => (
              <Card key={item.date + item.title} className="rounded-2xl border-slate-200 shadow-sm">
                <CardContent className="p-5 space-y-3">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-slate-500">{item.date}</p>
                    <Badge variant="outline" className="rounded-full">Evolução</Badge>
                  </div>
                  <h3 className="font-medium text-slate-900">{item.title}</h3>
                  <p className="text-sm leading-7 text-slate-700">{item.content}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="report">
          <div className="grid grid-cols-1 xl:grid-cols-[1.15fr_0.85fr] gap-4">
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Status do laudo</CardTitle>
                <CardDescription>Andamento da redação e das revisões da avaliação.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <p className="text-sm text-slate-500">Versão atual</p>
                  <p className="mt-2 text-2xl font-semibold tracking-tight text-slate-900">v1.4</p>
                  <p className="mt-1 text-sm text-slate-600">Seção em edição: Conclusão geral</p>
                </div>
                <div className="rounded-2xl border p-4 bg-slate-50">
                  <p className="text-sm text-slate-500">Progresso do texto</p>
                  <div className="mt-3 flex items-center gap-3">
                    <Progress value={68} className="h-2" />
                    <span className="text-sm text-slate-600">68%</span>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2">
                  <Button className="rounded-2xl gap-2"><FileText className="h-4 w-4" /> Abrir editor</Button>
                  <Button variant="outline" className="rounded-2xl gap-2"><Eye className="h-4 w-4" /> Pré-visualizar</Button>
                  <Button variant="outline" className="rounded-2xl gap-2"><Download className="h-4 w-4" /> Exportar</Button>
                </div>
              </CardContent>
            </Card>

            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Pendências do caso</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {[
                  "Conferir coerência entre BPA-2 e texto interpretativo.",
                  "Finalizar análise integrada das funções executivas.",
                  "Revisar conclusão e hipótese diagnóstica antes da aprovação.",
                ].map((item) => (
                  <div key={item} className="rounded-2xl border border-slate-200 p-4 text-sm text-slate-700">
                    {item}
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function TestsPage() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Testes e aplicações"
        subtitle="Módulo técnico para instrumentos, payloads, processamento normativo e interpretação inicial."
        action={<Button className="rounded-2xl gap-2"><Plus className="h-4 w-4" /> Nova aplicação</Button>}
      />

      <Tabs defaultValue="applications" className="space-y-4">
        <TabsList className="rounded-2xl bg-slate-100">
          <TabsTrigger value="applications" className="rounded-xl">Aplicações</TabsTrigger>
          <TabsTrigger value="wisc4" className="rounded-xl">WISC-IV</TabsTrigger>
          <TabsTrigger value="bpa2" className="rounded-xl">BPA-2</TabsTrigger>
        </TabsList>

        <TabsContent value="applications">
          <Card className="rounded-2xl border-slate-200 shadow-sm">
            <CardContent className="p-4">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Teste</TableHead>
                    <TableHead>Paciente</TableHead>
                    <TableHead>Método</TableHead>
                    <TableHead>Progresso</TableHead>
                    <TableHead>Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {testApplications.map((item) => (
                    <TableRow key={item.code + item.patient}>
                      <TableCell>
                        <div>
                          <p className="font-medium text-slate-900">{item.test}</p>
                          <p className="text-xs text-slate-500">{item.code}</p>
                        </div>
                      </TableCell>
                      <TableCell>{item.patient}</TableCell>
                      <TableCell>{item.method}</TableCell>
                      <TableCell className="w-[220px]">
                        <div className="flex items-center gap-3">
                          <Progress value={item.progress} className="h-2" />
                          <span className="text-xs text-slate-500 w-10">{item.progress}%</span>
                        </div>
                      </TableCell>
                      <TableCell><StatusBadge>{item.state}</StatusBadge></TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="wisc4">
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Layout funcional do WISC-IV</CardTitle>
                <CardDescription>Entrada de datas, escores brutos, conversão por faixa etária e resultados compostos.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Data de aplicação</p>
                    <p className="mt-2 font-medium">18/12/2017</p>
                  </div>
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Data de nascimento</p>
                    <p className="mt-2 font-medium">28/08/2003</p>
                  </div>
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Idade calculada</p>
                    <p className="mt-2 font-medium">14 anos, 3 meses, 20 dias</p>
                  </div>
                </div>
                <div className="rounded-2xl border p-4">
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <p className="font-medium text-slate-900">Subtestes principais</p>
                      <p className="text-sm text-slate-500">Entrada de PB, conversão para ponderado e soma por índice.</p>
                    </div>
                    <Button variant="outline" className="rounded-2xl gap-2"><Wand2 className="h-4 w-4" /> Processar</Button>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-3 text-sm">
                    {[
                      ["Cubos", "4", "2"],
                      ["Semelhanças", "54", "4"],
                      ["Dígitos", "1", "1"],
                      ["Conceitos Figurativos", "73", "3"],
                      ["Código", "71", "1"],
                      ["Vocabulário", "111", "1"],
                      ["SNL", "-", "-"],
                      ["Rac. Matricial", "41", "1"],
                      ["Compreensão", "71", "1"],
                      ["Proc. Símbolos", "52", "2"],
                    ].map(([label, bruto, pond]) => (
                      <div key={label} className="rounded-2xl border p-3">
                        <p className="text-slate-500">{label}</p>
                        <div className="mt-3 flex items-center justify-between">
                          <span>PB: <strong>{bruto}</strong></span>
                          <span>Pond.: <strong>{pond}</strong></span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Índices</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {[
                  ["ICV", "51", "Extremamente Baixo"],
                  ["IOP", "51", "Extremamente Baixo"],
                  ["IMO", "45", "Extremamente Baixo"],
                  ["IVP", "49", "Extremamente Baixo"],
                  ["QIT", "44", "Extremamente Baixo"],
                ].map(([sigla, valor, classe]) => (
                  <div key={sigla} className="rounded-2xl border p-4">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{sigla}</span>
                      <span className="text-2xl font-semibold">{valor}</span>
                    </div>
                    <p className="mt-2 text-sm text-slate-500">{classe}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="bpa2">
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
            <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Layout funcional do BPA-2</CardTitle>
                <CardDescription>Escolha obrigatória do método normativo: faixa etária ou escolaridade.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Método normativo</p>
                    <p className="mt-2 font-medium">Faixa etária</p>
                  </div>
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Referência</p>
                    <p className="mt-2 font-medium">13 anos</p>
                  </div>
                  <div className="rounded-2xl border p-4">
                    <p className="text-sm text-slate-500">Status</p>
                    <p className="mt-2 font-medium">Processado</p>
                  </div>
                </div>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Domínio</TableHead>
                      <TableHead>Bruto</TableHead>
                      <TableHead>Percentil</TableHead>
                      <TableHead>Classificação</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {[
                      ["Atenção Concentrada", "23", "1", "Muito inferior"],
                      ["Atenção Dividida", "18", "30", "Médio inferior"],
                      ["Atenção Alternada", "23", "1", "Muito inferior"],
                      ["Atenção Geral", "59", "25", "Médio inferior"],
                    ].map(([a, b, c, d]) => (
                      <TableRow key={a}>
                        <TableCell className="font-medium">{a}</TableCell>
                        <TableCell>{b}</TableCell>
                        <TableCell>{c}</TableCell>
                        <TableCell>{d}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
            <Card className="rounded-2xl border-slate-200 shadow-sm">
              <CardHeader>
                <CardTitle>Regras do módulo</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-slate-600">
                <div className="rounded-2xl border p-3">Obrigar escolha entre análise por idade ou escolaridade.</div>
                <div className="rounded-2xl border p-3">Carregar tabelas CSV específicas por domínio.</div>
                <div className="rounded-2xl border p-3">Salvar bruto, percentil e classificação no payload.</div>
                <div className="rounded-2xl border p-3">Gerar interpretação técnica padronizada.</div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function ReportsPage() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Laudos"
        subtitle="Editor por seções, versionamento, revisão clínica e exportação final em DOCX/PDF."
        action={<Button className="rounded-2xl gap-2"><FileText className="h-4 w-4" /> Novo laudo</Button>}
      />
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Editor de laudo</CardTitle>
            <CardDescription>Modelo por seções com apoio de IA e revisão humana obrigatória.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {[
                "Identificação",
                "Descrição da demanda",
                "Anamnese",
                "Eficiência intelectual",
                "Atenção",
                "Funções executivas",
                "Conclusão",
                "Hipótese diagnóstica",
              ].map((item) => (
                <Badge key={item} variant="secondary" className="rounded-full px-3 py-1">{item}</Badge>
              ))}
            </div>
            <div className="rounded-2xl border p-4 min-h-[280px] bg-slate-50">
              <p className="text-sm text-slate-700 leading-7">
                Em análise clínica, os resultados evidenciam perfil cognitivo heterogêneo, com rebaixamento global dos índices fatoriais e impacto funcional nas demandas de raciocínio verbal, memória operacional e velocidade de processamento. A redação aqui simula o editor do sistema, com suporte para templates, rascunhos por IA, revisão por seção e versionamento.
              </p>
            </div>
            <div className="flex gap-2">
              <Button className="rounded-2xl gap-2"><Wand2 className="h-4 w-4" /> Gerar seção</Button>
              <Button variant="outline" className="rounded-2xl gap-2"><Eye className="h-4 w-4" /> Pré-visualizar</Button>
              <Button variant="outline" className="rounded-2xl gap-2"><Download className="h-4 w-4" /> Exportar</Button>
            </div>
          </CardContent>
        </Card>
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Versões recentes</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {reports.map((item) => (
              <div key={item.patient + item.version} className="rounded-2xl border p-4">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-900">{item.patient}</span>
                  <Badge variant="outline" className="rounded-full">{item.version}</Badge>
                </div>
                <p className="text-sm text-slate-500 mt-2">Seção atual: {item.section}</p>
                <div className="mt-3"><StatusBadge>{item.status}</StatusBadge></div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function DocumentsPage() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Documentos"
        subtitle="Upload, extração, versionamento e vínculo de arquivos aos casos clínicos."
        action={<Button className="rounded-2xl gap-2"><Upload className="h-4 w-4" /> Enviar arquivo</Button>}
      />
      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardContent className="p-4">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Arquivo</TableHead>
                <TableHead>Tipo</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Vínculo</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {documents.map((item) => (
                <TableRow key={item.name}>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>{item.type}</TableCell>
                  <TableCell><StatusBadge>{item.status}</StatusBadge></TableCell>
                  <TableCell>{item.linked}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}

function AIPage() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="IA Clínica"
        subtitle="Camada assistiva para extração, revisão de consistência, interpretação e conclusão."
        action={<Button className="rounded-2xl gap-2"><Brain className="h-4 w-4" /> Nova rotina IA</Button>}
      />
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {[
          ["Extração estruturada", "PDF/DOCX/Imagem → JSON", Upload],
          ["Interpretação", "Teste → texto técnico", Wand2],
          ["Revisor", "Conferência número × texto", ShieldCheck],
          ["Conclusão", "Integração final do laudo", FileText],
        ].map(([title, desc, Icon]) => (
          <Card key={title} className="rounded-2xl border-slate-200 shadow-sm">
            <CardContent className="p-5 space-y-4">
              <div className="rounded-2xl border w-fit p-3"><Icon className="h-5 w-5" /></div>
              <div>
                <h3 className="font-medium text-slate-900">{title}</h3>
                <p className="text-sm text-slate-500 mt-1">{desc}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
      <Card className="rounded-2xl border-slate-200 shadow-sm">
        <CardHeader>
          <CardTitle>Painel de rotinas</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="rounded-2xl border p-4">
            <p className="text-sm text-slate-500">Última revisão de consistência</p>
            <p className="mt-2 font-medium">Marina Carvalho · WISC-IV</p>
            <p className="mt-2 text-sm text-slate-600">2 alertas detectados entre classificações e texto da conclusão.</p>
          </div>
          <div className="rounded-2xl border p-4">
            <p className="text-sm text-slate-500">Base de conhecimento ativa</p>
            <p className="mt-2 font-medium">36 templates clínicos</p>
            <p className="mt-2 text-sm text-slate-600">Modelos de BPA-2, RAVLT, WISC-IV, FDT, conclusões e hipóteses diagnósticas.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function AccountsPage() {
  return (
    <div className="space-y-6">
      <SectionTitle
        title="Usuários e permissões"
        subtitle="Gestão de contas, papéis de acesso e chaves da API do sistema."
        action={<Button className="rounded-2xl gap-2"><Plus className="h-4 w-4" /> Novo usuário</Button>}
      />
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <Card className="xl:col-span-2 rounded-2xl border-slate-200 shadow-sm">
          <CardContent className="p-4">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Usuário</TableHead>
                  <TableHead>Papel</TableHead>
                  <TableHead>Especialidade</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {[
                  ["admin", "Administrador", "Gestão do sistema", "Ativo"],
                  ["andre", "Neuropsicólogo", "Laudos neuropsicológicos", "Ativo"],
                  ["assistente1", "Assistente", "Cadastro e documentos", "Ativo"],
                ].map(([u, p, e, s]) => (
                  <TableRow key={u}>
                    <TableCell>{u}</TableCell>
                    <TableCell>{p}</TableCell>
                    <TableCell>{e}</TableCell>
                    <TableCell><StatusBadge>{s === "Ativo" ? "Final" : s}</StatusBadge></TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
        <Card className="rounded-2xl border-slate-200 shadow-sm">
          <CardHeader>
            <CardTitle>Segurança</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 text-sm text-slate-600">
            <div className="rounded-2xl border p-3">Autenticação do painel por sessão do Django.</div>
            <div className="rounded-2xl border p-3">API protegida por Bearer token.</div>
            <div className="rounded-2xl border p-3">Papéis: admin, neuropsychologist, assistant, reviewer, readonly.</div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

export default function NeuroSystemLayoutPreview() {
  const [active, setActive] = useState("dashboard");
  const [search, setSearch] = useState("");

  const activeMeta = useMemo(() => NAV.find((item) => item.key === active), [active]);

  const renderPage = () => {
    switch (active) {
      case "patients":
        return <PatientsPage />;
      case "evaluations":
        return <EvaluationsPage />;
      case "tests":
        return <TestsPage />;
      case "reports":
        return <ReportsPage />;
      case "documents":
        return <DocumentsPage />;
      case "ai":
        return <AIPage />;
      case "accounts":
        return <AccountsPage />;
      default:
        return <DashboardPage />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="grid min-h-screen grid-cols-1 xl:grid-cols-[280px_1fr]">
        <aside className="border-r border-slate-200 bg-white px-4 py-5 xl:px-5">
          <div className="flex items-center gap-3 px-2">
            <div className="rounded-2xl border border-slate-200 p-3 shadow-sm bg-white">
              <Brain className="h-5 w-5" />
            </div>
            <div>
              <p className="text-lg font-semibold tracking-tight">Neuro Sistema</p>
              <p className="text-xs text-slate-500">Clínica psicológica e neuroavaliação</p>
            </div>
          </div>

          <div className="mt-6 px-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Buscar módulo"
                className="rounded-2xl pl-9"
              />
            </div>
          </div>

          <ScrollArea className="mt-6 h-[calc(100vh-220px)] pr-2">
            <nav className="space-y-1 px-1">
              {NAV.filter((item) => item.label.toLowerCase().includes(search.toLowerCase())).map((item) => {
                const Icon = item.icon;
                const selected = active === item.key;
                return (
                  <button
                    key={item.key}
                    onClick={() => setActive(item.key)}
                    className={`w-full rounded-2xl px-3 py-3 text-left transition flex items-center justify-between ${selected ? "bg-slate-900 text-white shadow-sm" : "hover:bg-slate-100 text-slate-700"}`}
                  >
                    <div className="flex items-center gap-3">
                      <Icon className="h-4 w-4" />
                      <span className="text-sm font-medium">{item.label}</span>
                    </div>
                    <ChevronRight className={`h-4 w-4 ${selected ? "opacity-100" : "opacity-30"}`} />
                  </button>
                );
              })}
            </nav>
          </ScrollArea>

          <div className="mt-4 rounded-3xl border border-slate-200 p-4 bg-slate-50">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarFallback>AD</AvatarFallback>
              </Avatar>
              <div>
                <p className="text-sm font-medium">Dr. André</p>
                <p className="text-xs text-slate-500">Neuropsicólogo</p>
              </div>
            </div>
          </div>
        </aside>

        <main className="min-w-0">
          <header className="sticky top-0 z-10 border-b border-slate-200 bg-white/90 backdrop-blur">
            <div className="flex flex-col gap-4 px-4 py-4 md:px-6 xl:px-8 md:flex-row md:items-center md:justify-between">
              <div>
                <p className="text-sm text-slate-500">Módulo ativo</p>
                <div className="mt-1 flex items-center gap-2">
                  {activeMeta?.icon && <activeMeta.icon className="h-5 w-5 text-slate-700" />}
                  <h1 className="text-xl md:text-2xl font-semibold tracking-tight">{activeMeta?.label}</h1>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" className="rounded-2xl gap-2"><CalendarDays className="h-4 w-4" /> Agenda</Button>
                <Button variant="outline" className="rounded-2xl gap-2"><Bell className="h-4 w-4" /> Alertas</Button>
                <Button variant="outline" className="rounded-2xl gap-2"><Settings className="h-4 w-4" /> Configurações</Button>
              </div>
            </div>
          </header>

          <motion.div
            key={active}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className="px-4 py-6 md:px-6 xl:px-8"
          >
            {renderPage()}
          </motion.div>
        </main>
      </div>
    </div>
  );
}
