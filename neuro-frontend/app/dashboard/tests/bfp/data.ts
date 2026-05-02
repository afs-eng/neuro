export const BFP_ITEM_COUNT = 126;

export const BFP_RESPONSE_OPTIONS = [
  { value: 1, label: "Discordo Totalmente" },
  { value: 2, label: "Discordo" },
  { value: 3, label: "Discordo Parcialmente" },
  { value: 4, label: "Neutro" },
  { value: 5, label: "Concordo Parcialmente" },
  { value: 6, label: "Concordo" },
  { value: 7, label: "Concordo Totalmente" },
];

export const BFP_SAMPLE_OPTIONS = [
  { value: "geral", label: "Geral" },
  { value: "masculino", label: "Masculino" },
  { value: "feminino", label: "Feminino" },
];

export const BFP_FACTOR_GROUPS = [
  {
    code: "NN",
    name: "Neuroticismo",
    facets: ["N1", "N2", "N3", "N4"],
    summary:
      "Relaciona-se à vulnerabilidade emocional, oscilação afetiva, passividade e tendência a interpretações negativas do cotidiano.",
  },
  {
    code: "EE",
    name: "Extroversão",
    facets: ["E1", "E2", "E3", "E4"],
    summary:
      "Descreve comunicação, senso de valor pessoal, dinamismo e busca por interação social.",
  },
  {
    code: "SS",
    name: "Socialização",
    facets: ["S1", "S2", "S3"],
    summary:
      "Refere-se a amabilidade, postura pró-social e confiança nas outras pessoas.",
  },
  {
    code: "RR",
    name: "Realização",
    facets: ["R1", "R2", "R3"],
    summary:
      "Avalia busca de objetivos, prudência para agir e nível de comprometimento com tarefas.",
  },
  {
    code: "AA",
    name: "Abertura",
    facets: ["A1", "A2", "A3"],
    summary:
      "Descreve abertura a ideias, flexibilização de valores e busca por novidades.",
  },
];

export const BFP_FACET_NAMES: Record<string, string> = {
  N1: "Vulnerabilidade",
  N2: "Instabilidade Emocional",
  N3: "Passividade/Falta de Energia",
  N4: "Depressão",
  E1: "Comunicação",
  E2: "Altivez",
  E3: "Dinamismo",
  E4: "Interações Sociais",
  S1: "Amabilidade",
  S2: "Pró-Sociabilidade",
  S3: "Confiança nas Pessoas",
  R1: "Competência",
  R2: "Ponderação/Prudência",
  R3: "Empenho/Comprometimento",
  A1: "Abertura a Ideias",
  A2: "Liberalismo",
  A3: "Busca por Novidades",
};

export function getBfpClassificationColor(classification: string) {
  const key = classification.toLowerCase();
  if (key.includes("muito superior")) return "bg-red-50 text-red-700 border-red-200";
  if (key === "superior") return "bg-orange-50 text-orange-700 border-orange-200";
  if (key.includes("média superior") || key.includes("media superior")) return "bg-amber-50 text-amber-700 border-amber-200";
  if (key === "média" || key === "media") return "bg-yellow-50 text-yellow-700 border-yellow-200";
  if (key.includes("média inferior") || key.includes("media inferior")) return "bg-lime-50 text-lime-700 border-lime-200";
  if (key === "baixo") return "bg-blue-50 text-blue-700 border-blue-200";
  if (key.includes("muito baixo")) return "bg-emerald-50 text-emerald-700 border-emerald-200";
  return "bg-slate-100 text-slate-700 border-slate-200";
}

export function formatScaleValue(value: number | undefined | null, digits = 1) {
  if (value === null || value === undefined || Number.isNaN(value)) return "-";

  if (digits <= 0) {
    return new Intl.NumberFormat("pt-BR", {
      maximumFractionDigits: 0,
    }).format(value);
  }

  return new Intl.NumberFormat("pt-BR", {
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value);
}
