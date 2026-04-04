"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { PageContainer, PageHeader, SectionCard, StatCard, EmptyState } from "@/components/ui/page";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
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
  GraduationCap,
  Phone,
  User,
  Mail,
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
        subtitle={`${patients.length} pacientes cadastrados`}
        actions={
          <Link href="/dashboard/patients/new">
            <Button className="gap-2 bg-indigo-600 hover:bg-indigo-700">
              <Plus className="h-4 w-4" />
              Novo Paciente
            </Button>
          </Link>
        }
      />

      {/* Stats */}
      <div className="mb-6 grid gap-4 md:grid-cols-4">
        <div className="bg-indigo-500 rounded-xl p-5 text-white">
          <p className="text-sm font-medium text-indigo-100">Total</p>
          <p className="mt-1 text-3xl font-bold">{patients.length}</p>
        </div>
        <div className="bg-cyan-500 rounded-xl p-5 text-white">
          <p className="text-sm font-medium text-cyan-100">Novos este mês</p>
          <p className="mt-1 text-3xl font-bold">12</p>
        </div>
        <div className="bg-emerald-500 rounded-xl p-5 text-white">
          <p className="text-sm font-medium text-emerald-100">Avaliações ativas</p>
          <p className="mt-1 text-3xl font-bold">23</p>
        </div>
        <div className="bg-amber-500 rounded-xl p-5 text-white">
          <p className="text-sm font-medium text-amber-100">Laudos emitidos</p>
          <p className="mt-1 text-3xl font-bold">156</p>
        </div>
      </div>

      {/* Search & Filters */}
      <SectionCard className="mb-6">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative w-full max-w-md">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              placeholder="Buscar pacientes..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-10 border-slate-200"
            />
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="gap-2 border-slate-200">
              <Filter className="h-4 w-4" />
              Filtros
            </Button>
          </div>
        </div>
      </SectionCard>

      {/* Patients Table */}
      <SectionCard title="" className="">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-indigo-100 border-t-indigo-600"></div>
          </div>
        ) : filteredPatients.length === 0 ? (
          <EmptyState
            title="Nenhum paciente encontrado"
            description={search ? "Tente buscar por outro termo" : "Cadastre seu primeiro paciente"}
            action={
              <Link href="/dashboard/patients/new">
                <Button className="gap-2 bg-indigo-600 hover:bg-indigo-700">
                  <Plus className="h-4 w-4" />
                  Novo Paciente
                </Button>
              </Link>
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <Table>
              <TableHeader>
                <TableRow className="hover:bg-transparent">
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase">Paciente</TableHead>
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase">Idade</TableHead>
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase">Sexo</TableHead>
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase">Escolaridade</TableHead>
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase">Cidade</TableHead>
                  <TableHead className="text-xs font-semibold text-slate-500 uppercase w-12"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPatients.map((patient) => (
                  <TableRow key={patient.id} className="hover:bg-slate-50/50">
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-100 text-indigo-600 font-semibold">
                          {patient.full_name?.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-medium text-slate-900">{patient.full_name}</p>
                          {patient.mother_name && (
                            <p className="text-xs text-slate-500">Mãe: {patient.mother_name}</p>
                          )}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell className="text-slate-600">
                      <span className="inline-flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {calculateAge(patient.birth_date)}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center px-2 py-1 rounded-md bg-slate-100 text-slate-600 text-xs">
                        {patient.sex === "M" ? "Masculino" : patient.sex === "F" ? "Feminino" : "—"}
                      </span>
                    </TableCell>
                    <TableCell className="text-slate-600">{patient.schooling || "—"}</TableCell>
                    <TableCell className="text-slate-600">
                      <span className="inline-flex items-center gap-1">
                        <MapPin className="h-3 w-3" />
                        {patient.city || "—"}
                      </span>
                    </TableCell>
                    <TableCell>
                      <Link href={`/dashboard/patients/${patient.id}`}>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <ChevronRight className="h-4 w-4 text-slate-400" />
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
    </PageContainer>
  );
}
