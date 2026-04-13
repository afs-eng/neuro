"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Settings, Users, Palette, Bell, Shield, Database } from "lucide-react";

export default function SettingsPage() {
  const sections = [
    {
      icon: Users,
      title: "Usuários e Permissões",
      description: "Gerencie usuários, papéis e permissões de acesso",
      href: "/dashboard/accounts",
      status: "Disponível",
    },
    {
      icon: Palette,
      title: "Aparência",
      description: "Personalize cores, fontes e layout do sistema",
      href: "#",
      status: "Em breve",
    },
    {
      icon: Bell,
      title: "Notificações",
      description: "Configure alertas e notificações por e-mail e WhatsApp",
      href: "#",
      status: "Em breve",
    },
    {
      icon: Shield,
      title: "Segurança",
      description: "Configurações de autenticação, sessões e auditoria",
      href: "#",
      status: "Em breve",
    },
    {
      icon: Database,
      title: "Dados e Backups",
      description: "Exportação de dados, backups e gerenciamento de armazenamento",
      href: "#",
      status: "Em breve",
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100">
          <Settings className="h-5 w-5 text-slate-600" />
        </div>
        <div>
          <h2 className="text-2xl font-semibold text-slate-900">Configurações</h2>
          <p className="text-sm text-slate-500">Gerencie as configurações do sistema</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sections.map((section) => {
          const Icon = section.icon;
          const isAvailable = section.status === "Disponível";
          return (
            <Card
              key={section.title}
              className={`rounded-2xl border-slate-200 shadow-sm transition-all ${
                isAvailable
                  ? "cursor-pointer hover:shadow-md hover:border-slate-300"
                  : "opacity-60 cursor-not-allowed"
              }`}
              onClick={() => {
                if (isAvailable && section.href !== "#") {
                  window.location.href = section.href;
                }
              }}
            >
              <CardHeader>
                <div className="flex items-center gap-3 mb-2">
                  <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100">
                    <Icon className="h-5 w-5 text-slate-600" />
                  </div>
                  <div>
                    <CardTitle className="text-base">{section.title}</CardTitle>
                    <span
                      className={`text-xs font-medium ${
                        isAvailable ? "text-emerald-600" : "text-slate-400"
                      }`}
                    >
                      {section.status}
                    </span>
                  </div>
                </div>
                <CardDescription>{section.description}</CardDescription>
              </CardHeader>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
