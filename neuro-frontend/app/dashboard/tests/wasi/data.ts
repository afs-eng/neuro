export const WASI_SUBTESTS = [
  { key: "vc", code: "VC", name: "Vocabulário", color: "bg-amber-50 border-amber-200" },
  { key: "sm", code: "SM", name: "Semelhanças", color: "bg-amber-50 border-amber-200" },
  { key: "cb", code: "CB", name: "Cubos", color: "bg-blue-50 border-blue-200" },
  { key: "rm", code: "RM", name: "Raciocínio Matricial", color: "bg-blue-50 border-blue-200" },
] as const;

export const WASI_COMPOSITE_LABELS: Record<string, string> = {
  qi_verbal: "QI Verbal",
  qi_execucao: "QI Execução",
  qit_4: "QIT-4",
  qit_2: "QIT-2",
};

export function getCompositeBadgeColor(classification?: string | null) {
  const key = (classification || "").toLowerCase();
  if (key.includes("muito superior")) return "bg-violet-100 text-violet-800 border-violet-200";
  if (key === "superior") return "bg-indigo-100 text-indigo-800 border-indigo-200";
  if (key.includes("média superior") || key.includes("media superior")) return "bg-sky-100 text-sky-800 border-sky-200";
  if (key === "média" || key === "media") return "bg-emerald-100 text-emerald-800 border-emerald-200";
  if (key.includes("média inferior") || key.includes("media inferior")) return "bg-amber-100 text-amber-800 border-amber-200";
  if (key.includes("limítrofe") || key.includes("limitrofe")) return "bg-orange-100 text-orange-800 border-orange-200";
  if (key.includes("baixo") || key.includes("deficit")) return "bg-rose-100 text-rose-800 border-rose-200";
  return "bg-slate-100 text-slate-700 border-slate-200";
}

export function formatPtBrNumber(value: number | string | null | undefined, digits = 1) {
  if (value === null || value === undefined || value === "") return "—";
  const numeric = typeof value === "number" ? value : Number(String(value).replace(",", "."));
  if (Number.isNaN(numeric)) return String(value);
  return new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(numeric);
}
