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
      className={`fixed left-0 top-0 z-50 flex h-screen flex-col border-r border-slate-200 bg-white sidebar-transition ${
        collapsed ? "w-[72px]" : "w-[260px]"
      }`}
    >
      {/* Logo Area */}
      <div className="flex h-16 items-center justify-between px-4">
        <Link href="/dashboard" className="flex items-center gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-sm">
            <Brain className="h-6 w-6" />
          </div>
          {!collapsed && (
            <span className="text-xl font-bold tracking-tight text-slate-900">Neuro<span className="text-primary font-extrabold">Avalia</span></span>
          )}
        </Link>
      </div>

      {/* New Evaluation Button */}
      <div className="p-4">
        <Link
          href="/dashboard/evaluations/new"
          className={`flex items-center justify-center gap-2 rounded-lg bg-primary px-4 py-3 text-sm font-semibold text-primary-foreground shadow-spike transition-all hover:opacity-90 active:scale-95 ${collapsed ? "px-0 h-10 w-10 mx-auto" : ""}`}
        >
          <Plus className="h-5 w-5 shrink-0" />
          {!collapsed && <span>Nova avaliação</span>}
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto px-3 custom-scrollbar">
        <ul className="space-y-1.5">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || 
              (item.href !== "/dashboard" && pathname?.startsWith(item.href || ""));

            return (
              <li key={item.key}>
                <Link
                  href={item.href}
                  className={`group relative flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                    isActive
                      ? "bg-primary/5 text-primary"
                      : "text-slate-500 hover:bg-slate-50 hover:text-slate-900"
                  } ${collapsed ? "justify-center px-0 h-11 w-11 mx-auto" : ""}`}
                >
                  <div className={`flex shrink-0 items-center justify-center rounded-lg transition-colors ${
                    isActive 
                      ? "h-8 w-8 bg-primary text-primary-foreground shadow-sm" 
                      : "h-8 w-8 text-slate-400 group-hover:text-slate-600"
                  }`}>
                    <Icon className="h-5 w-5" />
                  </div>
                  
                  {!collapsed && (
                    <span className="flex-1 truncate">{item.label}</span>
                  )}
                  
                  {!collapsed && item.badge && (
                    <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-primary/10 px-1.5 text-[10px] font-bold text-primary">
                      {item.badge}
                    </span>
                  )}

                  {collapsed && isActive && (
                    <div className="absolute left-0 h-6 w-1 rounded-r-full bg-primary" />
                  )}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User Area */}
      <div className="mt-auto border-t border-slate-100 p-4">
        <div className={`flex items-center gap-3 rounded-xl bg-slate-50 p-2 border border-slate-100 ${collapsed ? "justify-center p-1" : ""}`}>
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white border border-slate-200 text-primary text-xs font-bold shadow-sm">
            DR
          </div>
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="truncate text-sm font-bold text-slate-900">Dr. André</p>
              <p className="truncate text-[11px] font-medium text-slate-500 uppercase tracking-wider">Neuropsicólogo</p>
            </div>
          )}
          {!collapsed && (
            <button className="text-slate-400 hover:text-primary transition-colors">
              <LogOut className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>
    </aside>
  );
}

export { NAV_ITEMS };
