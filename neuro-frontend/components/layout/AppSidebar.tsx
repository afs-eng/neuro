"use client";

import React from "react";
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
  Settings,
  Plus,
  ChevronRight,
  FileQuestion,
  Stethoscope,
  LogOut,
} from "lucide-react";

interface NavItem {
  key: string;
  label: string;
  icon: React.ElementType;
  href: string;
  badge?: number;
}

const NAV_ITEMS: NavItem[] = [
  { key: "dashboard", label: "Dashboard", icon: LayoutDashboard, href: "/dashboard" },
  { key: "patients", label: "Pacientes", icon: Users, href: "/dashboard/patients" },
  { key: "evaluations", label: "Avaliações", icon: ClipboardList, href: "/dashboard/evaluations" },
  { key: "tests", label: "Testes", icon: FlaskConical, href: "/dashboard/tests" },
  { key: "anamnesis", label: "Anamnese", icon: Stethoscope, href: "/dashboard/evaluations" },
  { key: "reports", label: "Laudos", icon: FileText, href: "/dashboard/reports" },
  { key: "documents", label: "Documentos", icon: FolderOpen, href: "/dashboard/documents" },
  { key: "ai", label: "IA Clínica", icon: Brain, href: "/dashboard/ai" },
  { key: "accounts", label: "Usuários", icon: ShieldCheck, href: "/dashboard/accounts" },
  { key: "settings", label: "Configurações", icon: Settings, href: "/dashboard/settings" },
];

export function AppSidebar({ 
  collapsed, 
  onToggle,
  onNewEvaluation 
}: { 
  collapsed: boolean; 
  onToggle: () => void;
  onNewEvaluation?: () => void;
}) {
  const pathname = usePathname();

  return (
    <aside
      className={`fixed left-0 top-0 z-50 flex h-screen flex-col border-r border-slate-200 bg-white transition-all duration-300 ${
        collapsed ? "w-[72px]" : "w-[260px]"
      }`}
    >
      {/* Logo Area */}
      <div className="flex h-16 items-center justify-between border-b border-slate-200 px-4">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600">
            <Brain className="h-5 w-5 text-white" />
          </div>
          {!collapsed && (
            <span className="text-lg font-semibold text-slate-900">NeuroAvalia</span>
          )}
        </Link>
        <button
          onClick={onToggle}
          className="flex h-7 w-7 items-center justify-center rounded-md border border-slate-200 bg-white text-slate-500 hover:bg-slate-50 hover:text-slate-700"
        >
          <ChevronRight className={`h-4 w-4 transition-transform ${collapsed ? "rotate-180" : ""}`} />
        </button>
      </div>

      {/* New Evaluation Button */}
      <div className="border-b border-slate-200 p-3">
        <Link
          href="/dashboard/evaluations/new"
          className={`flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-indigo-700 ${collapsed ? "px-2" : ""}`}
        >
          <Plus className="h-4 w-4" />
          {!collapsed && <span>Nova avaliação</span>}
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-3">
        <ul className="space-y-1 px-2">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || 
              (item.href !== "/dashboard" && pathname?.startsWith(item.href || ""));

            return (
              <li key={item.key}>
                <Link
                  href={item.href}
                  className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-indigo-50 text-indigo-700"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  } ${collapsed ? "justify-center px-2" : ""}`}
                  title={collapsed ? item.label : undefined}
                >
                  <Icon className={`h-5 w-5 shrink-0 ${isActive ? "text-indigo-600" : "text-slate-400 group-hover:text-slate-600"}`} />
                  {!collapsed && (
                    <>
                      <span className="flex-1">{item.label}</span>
                      {item.badge && (
                        <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-indigo-100 px-1.5 text-xs font-medium text-indigo-700">
                          {item.badge}
                        </span>
                      )}
                    </>
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User Section */}
      <div className="border-t border-slate-200 p-3">
        <div className={`flex items-center gap-3 rounded-lg p-2 ${collapsed ? "justify-center" : ""}`}>
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-indigo-700 text-sm font-semibold">
            DR
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="truncate text-sm font-medium text-slate-900">Dr. André</p>
              <p className="truncate text-xs text-slate-500">Neuropsicólogo</p>
            </div>
          )}
          {!collapsed && (
            <button className="text-slate-400 hover:text-slate-600">
              <LogOut className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}

export { NAV_ITEMS };
