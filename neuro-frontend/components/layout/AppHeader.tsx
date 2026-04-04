"use client";

import React from "react";
import { useRouter } from "next/navigation";
import {
  Search,
  Bell,
  Settings,
  ChevronDown,
  LogOut,
  User,
  HelpCircle,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function AppHeader({ sidebarCollapsed }: { sidebarCollapsed: boolean }) {
  const router = useRouter();

  return (
    <header
      className={`fixed top-0 right-0 z-40 h-16 border-b border-slate-200 bg-white transition-all duration-300 ${
        sidebarCollapsed ? "left-[72px]" : "left-[260px]"
      }`}
    >
      <div className="flex h-full items-center justify-between px-6">
        {/* Search */}
        <div className="w-full max-w-md">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <Input
              placeholder="Buscar pacientes, avaliações, laudos..."
              className="h-10 w-full rounded-lg border-slate-200 bg-slate-50 pl-10 text-sm placeholder:text-slate-400 focus:bg-white focus:border-indigo-500 focus:ring-indigo-500/20"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-2">
          {/* Help */}
          <Button variant="ghost" size="icon" className="h-10 w-10 text-slate-500 hover:text-slate-700 hover:bg-slate-100">
            <HelpCircle className="h-5 w-5" />
          </Button>

          {/* Notifications */}
          <Button variant="ghost" size="icon" className="relative h-10 w-10 text-slate-500 hover:text-slate-700 hover:bg-slate-100">
            <Bell className="h-5 w-5" />
            <span className="absolute right-2 top-2 flex h-2 w-2">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-red-400 opacity-75"></span>
              <span className="relative inline-flex h-2 w-2 rounded-full bg-red-500"></span>
            </span>
          </Button>

          {/* Settings */}
          <Button 
            variant="ghost" 
            size="icon" 
            className="h-10 w-10 text-slate-500 hover:text-slate-700 hover:bg-slate-100"
            onClick={() => router.push("/dashboard/settings")}
          >
            <Settings className="h-5 w-5" />
          </Button>

          {/* Divider */}
          <div className="mx-2 h-8 w-px bg-slate-200"></div>

          {/* User Menu */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="flex items-center gap-2 rounded-lg px-2 py-1.5 hover:bg-slate-100">
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-100 text-indigo-700 text-sm font-semibold">
                  DR
                </div>
                <div className="text-left hidden sm:block">
                  <p className="text-sm font-medium text-slate-900">Dr. André</p>
                  <p className="text-xs text-slate-500">Admin</p>
                </div>
                <ChevronDown className="h-4 w-4 text-slate-400" />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-56">
              <DropdownMenuLabel>Minha Conta</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <User className="mr-2 h-4 w-4" />
                Perfil
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Settings className="mr-2 h-4 w-4" />
                Configurações
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="text-red-600">
                <LogOut className="mr-2 h-4 w-4" />
                Sair
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
