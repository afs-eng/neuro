"use client";

import React from "react";
import { Printer, CheckCircle2, ChevronRight, FileText } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface Field {
  id: string;
  label: string;
  type: string;
  options?: string[];
}

interface Step {
  id: string;
  title: string;
  fields: Field[];
}

interface AnamnesisTemplate {
  schema_payload: {
    steps: Step[];
  };
}

interface Props {
  answers: Record<string, any>;
  template?: AnamnesisTemplate;
}

export function AnamnesisResponseViewer({ answers, template }: Props) {
  // Se não tiver template, tenta extrair o que der das chaves do JSON
  if (!template || !template.schema_payload?.steps) {
    return (
      <div className="p-6 rounded-2xl bg-slate-50 border border-slate-100 italic text-slate-400">
        Carregando estrutura do relatório...
      </div>
    );
  }

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-8 print:p-0 print:m-0">
      <div className="flex items-center justify-between print:hidden mb-4">
        <h3 className="text-[10px] font-black uppercase tracking-widest text-slate-400">Detalhamento das Respostas</h3>
        <Button 
          variant="outline" 
          size="sm" 
          className="gap-2 h-8 text-[11px] font-black uppercase tracking-tighter"
          onClick={handlePrint}
        >
          <Printer className="h-4 w-4" /> Imprimir Relatório
        </Button>
      </div>

      {/* Relatório Clínico Formato Leitura */}
      <div className="space-y-8 bg-white print:bg-white p-2">
        {template.schema_payload.steps.map((step) => {
          // Filtrar campos respondidos nesta seção
          const answeredFields = step.fields.filter(f => 
            answers[f.id] !== undefined && 
            answers[f.id] !== null && 
            answers[f.id] !== ""
          );

          if (answeredFields.length === 0) return null;

          return (
            <div key={step.id} className="space-y-4 break-inside-avoid">
              <div className="flex items-center gap-2 border-b border-slate-100 pb-2">
                <div className="h-5 w-1 bg-primary rounded-full" />
                <h4 className="text-sm font-black uppercase tracking-widest text-slate-800">{step.title}</h4>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
                {answeredFields.map((field) => {
                  const value = answers[field.id];
                  let displayValue = "";

                  if (typeof value === 'boolean') {
                    displayValue = value ? "Sim" : "Não";
                  } else if (Array.isArray(value)) {
                    displayValue = value.join(", ");
                  } else if (typeof value === 'object' && value !== null) {
                    displayValue = JSON.stringify(value);
                  } else {
                    displayValue = String(value);
                  }

                  return (
                    <div key={field.id} className="space-y-1">
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-tight">{field.label}</p>
                      <p className="text-sm text-slate-700 font-medium leading-relaxed">{displayValue}</p>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>

      {/* Estilos para Impressão */}
      <style jsx global>{`
        @media print {
          body * {
            visibility: hidden;
          }
          .print-area, .print-area * {
            visibility: visible;
          }
          .print-area {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
          }
          .print\\:hidden {
            display: none !important;
          }
        }
      `}</style>
    </div>
  );
}
