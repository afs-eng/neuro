"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { PageContainer, PageHeader, SectionCard, StatCard, EmptyState, InfoCard } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Users,
  Plus,
  Search,
  Filter,
  ChevronRight,
  Calendar,
  MapPin,
  Sparkles,
  ClipboardList,
  FileText,
  Edit,
  Trash2,
  AlertTriangle
} from "lucide-react";

export const dynamic = "force-dynamic";

interface Patient {
  id: number;
  full_name: string;
  birth_date: string | null;
  sex: string | null;
  schooling: string | null;
  city: string | null;
  phone: string | null;
  mother_name: string | null;
}

function calculateAge(birthDate: string | null): string {
  if (!birthDate) return "—";
  const birth = new Date(birthDate);
  const today = new Date();
  if (isNaN(birth.getTime())) return "—";

  let years = today.getFullYear() - birth.getFullYear();
  let months = today.getMonth() - birth.getMonth();

  if (today.getDate() < birth.getDate()) months--;
  if (months < 0) { years--; months += 12; }

  if (years <= 0) return `${months} ${months === 1 ? "mês" : "meses"}`;
  return `${years} ${years === 1 ? "ano" : "anos"}`;
}

export default function PatientsPage() {
  const router = useRouter();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [deletePatientId, setDeletePatientId] = useState<number | null>(null);
  const [deleteConfirmationOpen, setDeleteConfirmationOpen] = useState(false);
  const [deletingPatient, setDeletingPatient] = useState(false);

  useEffect(() => {
    fetchPatients();
  }, []);

  async function fetchPatients() {
    try {
      setLoading(true);
      const data = await api.get<Patient[]>("/api/patients/");
      setPatients(data);
    } catch (err) {
      console.error("Erro ao buscar pacientes:", err);
    } finally {
      setLoading(false);
    }
  }

  function handleOpenDeleteDialog(patientId: number) {
    setDeletePatientId(patientId);
    setDeleteConfirmationOpen(true);
  }

  function handleCloseDeleteDialog() {
    setDeletePatientId(null);
    setDeleteConfirmationOpen(false);
  }

  async function handleDeletePatient() {
    if (!deletePatientId) return;

    try {
      setDeletingPatient(true);
      await api.delete(`/api/patients/${deletePatientId}`);

      // Remove from local state
      setPatients(prev => prev.filter(p => p.id !== deletePatientId));

      handleCloseDeleteDialog();
    } catch (err) {
      console.error("Erro ao excluir paciente:", err);
      alert("Não foi possível excluir o paciente. Tente novamente.");
    } finally {
      setDeletingPatient(false);
    }
  }

  const filteredPatients = patients.filter((patient) =>
    patient.full_name?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <PageContainer>
      <PageHeader
        title="Pacientes"
        subtitle="Gerenciamento de prontuários e histórico clínico."
        actions={
          <Link href="/dashboard/patients/new">
            <Button className="gap-2 shadow-spike font-bold">
              <Plus className="h-4 w-4" />
              Novo Paciente
            </Button>
          </Link>
        }
      />

      {/* Stats */}
      <div className="mb-10 grid gap-6 md:grid-cols-4">
        <StatCard title="Total Cadastrados" value={patients.length} icon={Users} />
        <StatCard title="Novos este mês" value="12" trend={{ value: 15, label: "vs mês ant." }} icon={Plus} />
        <StatCard title="Avaliações Ativas" value="23" icon={ClipboardList} />
        <StatCard title="Laudos Emitidos" value="156" icon={FileText} />
      </div>

      <div className="space-y-6">
        {/* Search & Filters */}
        <SectionCard>
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="relative w-full max-w-md group">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400 group-focus-within:text-primary transition-colors" />
              <Input
                placeholder="Pesquisar por nome ou CPF..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="pl-10 border-slate-100 bg-slate-50 transition-all focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary/20"
              />
            </div>
            <div className="flex gap-2">
              <Button variant="outline" className="gap-2 border-slate-100 font-bold hover:bg-slate-50">
                <Filter className="h-4 w-4 text-slate-400" />
                Filtros Avançados
              </Button>
            </div>
          </div>
        </SectionCard>

        {/* Patients Table */}
        <SectionCard title="Lista de Pacientes" description="Todos os registros da clínica.">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4">
              <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-100 border-t-primary"></div>
              <p className="text-sm font-bold text-slate-400 animate-pulse uppercase tracking-widest">Carregando Prontuários...</p>
            </div>
          ) : filteredPatients.length === 0 ? (
            <EmptyState
              title="Nenhum paciente encontrado"
              icon={<Users className="h-12 w-12 text-slate-200" />}
              description={search ? "Não encontramos resultados para sua busca." : "Sua base de pacientes está vazia. Comece cadastrando um novo paciente."}
              action={
                <Link href="/dashboard/patients/new">
                  <Button className="gap-2 font-bold shadow-md">
                    <Plus className="h-4 w-4" />
                    Cadastrar Primeiro Paciente
                  </Button>
                </Link>
              }
            />
          ) : (
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="hover:bg-transparent">
                    <TableHead>Identificação</TableHead>
                    <TableHead>Idade</TableHead>
                    <TableHead>Sexo</TableHead>
                    <TableHead>Escolaridade</TableHead>
                    <TableHead>Cidade/Local</TableHead>
                    <TableHead className="w-12"></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPatients.map((patient) => (
                    <TableRow key={patient.id} className="group hover:bg-slate-50/50 transition-colors">
                      <TableCell>
                        <Link href={`/dashboard/patients/${patient.id}`} className="flex items-center gap-4 group/name">
                          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary/5 text-primary text-xs font-black shadow-sm transition-all group-hover:bg-primary group-hover:text-white">
                            {patient.full_name?.charAt(0).toUpperCase()}
                          </div>
                          <div className="min-w-0">
                            <p className="font-bold text-slate-900 truncate transition-colors group-hover/name:text-primary">{patient.full_name}</p>
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mt-0.5">#{String(patient.id).padStart(4, '0')}</p>
                          </div>
                        </Link>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Calendar className="h-3.5 w-3.5 text-slate-300" />
                          <span className="text-sm font-bold text-slate-600">{calculateAge(patient.birth_date)}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black uppercase tracking-widest border ${
                          patient.sex === "M"
                          ? "bg-blue-50 text-blue-600 border-blue-100"
                          : patient.sex === "F"
                          ? "bg-pink-50 text-pink-600 border-pink-100"
                          : "bg-slate-50 text-slate-500 border-slate-100"
                        }`}>
                          {patient.sex === "M" ? "Masc" : patient.sex === "F" ? "Fem" : "N/I"}
                        </span>
                      </TableCell>
                      <TableCell>
                        <div className="flex flex-col">
                          <span className="text-sm font-bold text-slate-600 truncate max-w-[150px]">{patient.schooling || "—"}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2 text-slate-400">
                          <MapPin className="h-3.5 w-3.5" />
                          <span className="text-sm font-medium">{patient.city || "Não inf."}</span>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-1 justify-end">
                          <Link href={`/dashboard/patients/${patient.id}/edit`}>
                            <Button variant="ghost" size="sm" className="h-9 w-9 p-0 opacity-0 group-hover:opacity-100 transition-opacity text-slate-500 hover:bg-slate-100 hover:text-slate-700">
                              <Edit className="h-4 w-4" />
                            </Button>
                          </Link>
                          <Link href={`/dashboard/patients/${patient.id}`}>
                            <Button variant="ghost" size="sm" className="h-9 w-9 p-0 opacity-0 group-hover:opacity-100 transition-opacity text-primary hover:bg-primary/5">
                              <ChevronRight className="h-5 w-5" />
                            </Button>
                          </Link>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-9 w-9 p-0 opacity-0 group-hover:opacity-100 transition-opacity text-red-400 hover:bg-red-50 hover:text-red-600"
                            onClick={() => handleOpenDeleteDialog(patient.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </SectionCard>
      </div>

      {/* Delete Patient Confirmation Dialog */}
      {deleteConfirmationOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-red-50">
                <AlertTriangle className="h-6 w-6 text-red-500" />
              </div>
              <div className="flex-1 space-y-2">
                <h3 className="text-lg font-bold text-slate-900">Excluir Paciente?</h3>
                <p className="text-sm text-slate-600">
                  Esta ação irá remover permanentemente o paciente e todos os dados vinculados:
                </p>
                <ul className="ml-4 list-disc space-y-1 text-xs text-slate-500">
                  <li>Avaliações neuropsicológicas</li>
                  <li>Testes aplicados e resultados</li>
                  <li>Evoluções clínicas</li>
                  <li>Documentos anexados</li>
                  <li>Anamneses vinculadas</li>
                  <li>Laudos gerados</li>
                </ul>
                <p className="text-sm font-bold text-red-600">Esta ação não pode ser desfeita.</p>
              </div>
            </div>
            <div className="mt-6 flex justify-end gap-3">
              <Button
                variant="outline"
                className="font-bold"
                onClick={handleCloseDeleteDialog}
                disabled={deletingPatient}
              >
                Cancelar
              </Button>
              <Button
                variant="destructive"
                className="font-bold"
                onClick={handleDeletePatient}
                disabled={deletingPatient}
              >
                {deletingPatient ? (
                  <>
                    <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                    Excluindo...
                  </>
                ) : (
                  <>
                    <Trash2 className="mr-2 h-4 w-4" />
                    Sim, Excluir
                  </>
                )}
              </Button>
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
