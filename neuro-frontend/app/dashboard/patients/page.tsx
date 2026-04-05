"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
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
  FileText
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
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

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
                        <div className="flex items-center gap-4">
                          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-primary/5 text-primary text-xs font-black shadow-sm transition-all group-hover:bg-primary group-hover:text-white">
                            {patient.full_name?.charAt(0).toUpperCase()}
                          </div>
                          <div className="min-w-0">
                            <p className="font-bold text-slate-900 truncate">{patient.full_name}</p>
                            <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mt-0.5">#{String(patient.id).padStart(4, '0')}</p>
                          </div>
                        </div>
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
                        <Link href={`/dashboard/patients/${patient.id}`}>
                          <Button variant="ghost" size="sm" className="h-9 w-9 p-0 opacity-0 group-hover:opacity-100 transition-opacity text-primary hover:bg-primary/5">
                            <ChevronRight className="h-5 w-5" />
                          </Button>
                        </Link>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          )}
        </SectionCard>
      </div>
    </PageContainer>
  );
}
