# Skill — Gráfico de Perfil BAI (React + JSX + Tailwind)

## Objetivo

Implementar no sistema um gráfico de **Perfil** para o teste **BAI**, reproduzindo o modelo visual já validado:

- título grande `Perfil`
- subtítulo do instrumento
- descrição da norma aplicada
- coluna lateral de **Dados brutos**
- coluna lateral de **Normas**
- régua superior com:
  - `min`
  - `-s`
  - `m`
  - `+s`
  - `max`
- faixa cinza com divisões verticais brancas
- ponto vermelho indicando a posição do **Escore T**
- bloco à direita com `Escore Total`

---

## Código base do gráfico

```jsx
export default function BaiPerfilGrafico({
  rawScore = 10,
  tScore = 47,
  title = "Perfil",
  subtitle = "Inventário de Ansiedade • Padrão",
  description = "Amostra Geral • Escore T (50+10z)",
  scaleLabel = "Escore Total",
}) {
  const min = 20;
  const max = 80;
  const ticks = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80];
  const specialLabels = {
    20: "min",
    40: "-s",
    50: "m",
    60: "+s",
    80: "max",
  };

  const safeT = Math.max(min, Math.min(max, tScore));
  const markerPercent = ((safeT - min) / (max - min)) * 100;

  return (
    <div className="w-full bg-white px-6 py-4 text-black">
      <div className="mx-auto w-full max-w-6xl">
        <h1 className="font-serif text-[82px] font-bold leading-[0.9] tracking-tight md:text-[108px]">
          {title}
        </h1>

        <div className="mt-14 space-y-2">
          <p className="text-[24px] font-bold leading-none">{subtitle}</p>
          <p className="text-[22px] font-bold leading-none md:text-[24px]">{description}</p>
        </div>

        <div className="mt-10 overflow-x-auto">
          <div className="min-w-[900px]">
            <div className="grid grid-cols-[40px_40px_1fr_200px] items-end">
              <div className="pb-2 flex justify-center">
                <span className="[writing-mode:vertical-rl] rotate-180 text-xs font-bold text-black">
                  Dados brutos
                </span>
              </div>

              <div className="pb-2 flex justify-center">
                <span className="[writing-mode:vertical-rl] rotate-180 text-xs font-bold text-black">
                  Normas
                </span>
              </div>

              <div className="relative h-24">
                <div className="absolute inset-x-0 bottom-0 flex h-full items-end justify-between px-4 pb-8">
                  {ticks.map((tick) => (
                    <div key={tick} className="flex flex-1 flex-col items-center">
                      {specialLabels[tick] ? (
                        <span className="mb-1 text-[11px] leading-none text-neutral-700">
                          {specialLabels[tick]}
                        </span>
                      ) : (
                        <span className="mb-1 text-[11px] leading-none opacity-0">_</span>
                      )}

                      <span className="mb-2 text-[11px] text-neutral-700">{tick}</span>
                      <div className="h-3 w-px bg-black" />
                    </div>
                  ))}
                </div>

                <div className="absolute inset-x-[4%] bottom-8 h-px bg-black" />
              </div>

              <div />
            </div>

            <div className="grid h-24 grid-cols-[40px_40px_1fr_200px]">
              <div className="flex items-center justify-center border-r border-white bg-[#e9fdff] text-sm text-[#4d626c]">
                {rawScore}
              </div>

              <div className="flex items-center justify-center border-r border-white bg-[#e9fdff] text-sm text-[#4d626c]">
                {safeT}
              </div>

              <div className="relative flex items-center bg-[#cccccc]">
                <div className="absolute inset-0 flex justify-between px-4">
                  {Array.from({ length: 13 }).map((_, i) => (
                    <div key={i} className="h-full w-[2px] bg-white" />
                  ))}
                </div>

                <div
                  className="absolute h-4 w-4 -translate-x-1/2 rounded-full bg-[#c0000e]"
                  style={{ left: `${markerPercent}%` }}
                />
              </div>

              <div className="flex items-center bg-[#e9fdff] px-4">
                <span className="text-sm font-bold uppercase text-black">{scaleLabel}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

---

## O que a IA deve fazer no sistema

A IA deve usar esse gráfico como **componente base** do BAI e adaptar para a arquitetura do projeto.

### Requisitos funcionais

1. O componente deve receber os dados por `props`.
2. O valor do ponto vermelho deve ser calculado a partir do **Escore T**.
3. O gráfico deve aceitar:
   - `rawScore`
   - `tScore`
   - `title`
   - `subtitle`
   - `description`
   - `scaleLabel`
4. O componente deve ser responsivo, mas preservar a proporção do modelo.
5. A régua deve permanecer fixa entre **20 e 80**.
6. O ponto vermelho deve ser posicionado com esta fórmula:

```ts
const markerPercent = ((safeT - min) / (max - min)) * 100;
```

7. O valor de `tScore` deve ser limitado ao intervalo da escala:

```ts
const safeT = Math.max(min, Math.min(max, tScore));
```

---

## Estrutura recomendada no sistema

```text
frontend/
  src/
    components/
      tests/
        bai/
          BaiPerfilGrafico.jsx
    features/
      tests/
        bai/
          helpers/
            baiChartUtils.ts
          sections/
            BaiProfileSection.jsx
```

---

## Separação de responsabilidades

### `BaiPerfilGrafico.jsx`
Responsável apenas pela renderização visual do gráfico.

### `baiChartUtils.ts`
Responsável por:
- normalizar `tScore`
- calcular posição do marcador
- fornecer labels da régua
- fornecer metadados visuais da escala

Exemplo:

```ts
export const BAI_MIN_T = 20;
export const BAI_MAX_T = 80;

export const BAI_TICKS = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80];

export const BAI_SPECIAL_LABELS: Record<number, string> = {
  20: "min",
  40: "-s",
  50: "m",
  60: "+s",
  80: "max",
};

export function clampBaiTScore(tScore: number) {
  return Math.max(BAI_MIN_T, Math.min(BAI_MAX_T, tScore));
}

export function getBaiMarkerPercent(tScore: number) {
  const safeT = clampBaiTScore(tScore);
  return ((safeT - BAI_MIN_T) / (BAI_MAX_T - BAI_MIN_T)) * 100;
}
```

### `BaiProfileSection.jsx`
Responsável por consumir os dados vindos do backend e montar o gráfico.

---

## Payload esperado do backend

O backend deve entregar algo semelhante a:

```json
{
  "raw_score": 10,
  "t_score": 47,
  "profile_chart": {
    "title": "Perfil",
    "subtitle": "Inventário de Ansiedade • Padrão",
    "description": "Amostra Geral • Escore T (50+10z)",
    "scale_label": "Escore Total"
  }
}
```

---

## Exemplo de uso no frontend

```jsx
import BaiPerfilGrafico from "@/components/tests/bai/BaiPerfilGrafico";

export default function BaiProfileSection({ result }) {
  return (
    <BaiPerfilGrafico
      rawScore={result.raw_score}
      tScore={result.t_score}
      title={result.profile_chart?.title ?? "Perfil"}
      subtitle={result.profile_chart?.subtitle ?? "Inventário de Ansiedade • Padrão"}
      description={result.profile_chart?.description ?? "Amostra Geral • Escore T (50+10z)"}
      scaleLabel={result.profile_chart?.scale_label ?? "Escore Total"}
    />
  );
}
```

---

## Regras visuais obrigatórias

A IA deve manter exatamente esta lógica visual:

- duas colunas estreitas à esquerda
- rótulos verticais `Dados brutos` e `Normas`
- valores numéricos centralizados no bloco inferior
- faixa central cinza
- divisões verticais brancas com espessura maior que `1px`
- ponto vermelho circular centralizado verticalmente
- bloco lateral direito azul-claro com `Escore Total`
- régua superior separada da faixa cinza
- textos `min`, `-s`, `m`, `+s`, `max` acima da numeração

### Cores base

```ts
const colors = {
  leftPanel: "#e9fdff",
  chartBg: "#cccccc",
  chartGrid: "#ffffff",
  marker: "#c0000e",
  labelText: "#4d626c",
  text: "#000000",
};
```

---

## O que não fazer

A IA não deve:

- misturar esse gráfico com cards, header fixo, navbar, paciente, validação ou observações clínicas
- alterar a lógica da régua
- trocar os rótulos verticais por horizontais
- usar biblioteca de gráficos como Chart.js ou Recharts
- transformar isso em canvas SVG sem necessidade
- criar layout diferente do modelo aprovado

---

## Prompt operacional para a IA

Use este prompt para pedir a implementação no sistema:

```text
Implemente no frontend do sistema um componente React + JSX + Tailwind chamado BaiPerfilGrafico, reproduzindo exatamente o gráfico de perfil do BAI já validado.

Requisitos:
- usar 4 colunas: Dados brutos, Normas, área do gráfico, Escore Total
- manter rótulos verticais nas duas primeiras colunas
- manter régua superior com min, -s, m, +s, max
- manter numeração 20 a 80 de 5 em 5
- manter faixa cinza com divisões brancas verticais
- manter ponto vermelho posicionado pelo Escore T
- receber props: rawScore, tScore, title, subtitle, description, scaleLabel
- criar helper para clamp do tScore e cálculo percentual do marcador
- não usar bibliotecas externas de gráfico
- deixar pronto para integração com os resultados do BAI vindos do backend
- preservar o layout visual aprovado no protótipo
```

---

## Saída esperada da IA

A implementação final deve gerar:

1. `BaiPerfilGrafico.jsx`
2. `baiChartUtils.ts`
3. `BaiProfileSection.jsx`
4. integração simples com os dados do resultado do teste
5. componente pronto para reutilização em laudo, tela de resultado e PDF HTML
