"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
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
  ChevronRight,
  ArrowLeft,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

const NAV = [
  { key: "dashboard", label: "Dashboard", icon: LayoutDashboard, href: "/dashboard" },
  { key: "patients", label: "Pacientes", icon: Users, href: "/dashboard/patients" },
  { key: "evaluations", label: "Avaliações", icon: ClipboardList, href: "/dashboard/evaluations" },
  { key: "tests", label: "Testes", icon: FlaskConical, href: "/dashboard/tests" },
  { key: "reports", label: "Laudos", icon: FileText, href: "/dashboard/reports" },
  { key: "documents", label: "Documentos", icon: FolderOpen, href: "/dashboard/documents" },
  { key: "ai", label: "IA Clínica", icon: Brain, href: "/dashboard/ai" },
  { key: "accounts", label: "Usuários", icon: ShieldCheck, href: "/dashboard/accounts" },
];

interface SystemLayoutProps {
  children: React.ReactNode;
  currentPage: string;
  onNavigate: (page: string) => void;
}

export function SystemLayout({ children, currentPage, onNavigate }: SystemLayoutProps) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-slate-100">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-white shadow-sm">
        <div className="flex h-16 items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="rounded-lg bg-zinc-900 p-2">
                <Brain className="h-5 w-5 text-white" />
              </div>
              <span className="text-xl font-bold text-zinc-900">NeuroAvalia</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
              <Input
                placeholder="Buscar pacientes, avaliações..."
                className="w-64 rounded-full border-slate-200 pl-10"
              />
            </div>
            <Button variant="ghost" size="icon" className="relative">
              <Bell className="h-5 w-5 text-slate-600" />
              <span className="absolute -right-1 -top-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] text-white">
                3
              </span>
            </Button>
            <Button variant="ghost" size="icon">
              <Settings className="h-5 w-5 text-slate-600" />
            </Button>
            <div className="flex items-center gap-2 border-l pl-3">
              <div className="h-8 w-8 rounded-full bg-zinc-900 flex items-center justify-center text-white text-sm font-medium">
                DR
              </div>
              <div className="text-sm">
                <p className="font-medium text-zinc-900">Dr. André</p>
                <p className="text-xs text-slate-500">Neuropsicólogo</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] border-r bg-white transition-all duration-300 ${
            sidebarCollapsed ? "w-16" : "w-64"
          }`}
        >
          <div className="flex h-full flex-col">
            {/* Collapse button */}
            <button
              onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
              className="absolute -right-3 top-6 flex h-6 w-6 items-center justify-center rounded-full border bg-white shadow"
            >
              <ChevronRight
                className={`h-4 w-4 text-slate-600 transition-transform ${
                  sidebarCollapsed ? "rotate-180" : ""
                }`}
              />
            </button>

            {/* New evaluation button */}
            <div className="p-4">
              <Button className="w-full rounded-xl gap-2" onClick={() => onNavigate("new-evaluation")}>
                <Plus className="h-4 w-4" />
                {!sidebarCollapsed && "Nova avaliação"}
              </Button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 overflow-y-auto p-2">
              {NAV.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href || (item.href !== "/dashboard" && pathname?.startsWith(item.href || ""));
                return (
                  <Link
                    key={item.key}
                    href={item.href}
                    className={`mb-1 flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-left transition-colors ${
                      isActive
                        ? "bg-zinc-900 text-white"
                        : "text-slate-600 hover:bg-slate-100"
                    } ${sidebarCollapsed ? "justify-center" : ""}`}
                  >
                    <Icon className="h-5 w-5 shrink-0" />
                    {!sidebarCollapsed && (
                      <>
                        <span className="text-sm font-medium">{item.label}</span>
                        {isActive && (
                          <ChevronRight className="ml-auto h-4 w-4 opacity-60" />
                        )}
                      </>
                    )}
                  </Link>
                );
              })}
            </nav>

            {/* User info at bottom */}
            {!sidebarCollapsed && (
              <div className="border-t p-4">
                <div className="rounded-lg bg-slate-50 p-3">
                  <p className="text-xs text-slate-500">Pacientes ativos</p>
                  <p className="text-2xl font-semibold text-zinc-900">248</p>
                </div>
              </div>
            )}
          </div>
        </aside>

        {/* Main content */}
        <main
          className={`flex-1 transition-all duration-300 ${
            sidebarCollapsed ? "ml-16" : "ml-64"
          } p-6`}
        >
          {children}
        </main>
      </div>
    </div>
  );
}

export { NAV };
