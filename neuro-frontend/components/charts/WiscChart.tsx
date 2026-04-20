type WiscDatum = {
  label: string;
  value: number;
};

type WiscChartProps = {
  data: WiscDatum[];
};

const BANDS = [
  { from: 130, to: 160, color: "#b8d87a" },
  { from: 120, to: 130, color: "#c8e08a" },
  { from: 110, to: 120, color: "#d8e8a0" },
  { from: 90, to: 110, color: "#c8d8e8" },
  { from: 80, to: 90, color: "#f0f0a0" },
  { from: 70, to: 80, color: "#f0f000" },
  { from: 40, to: 70, color: "#f0d080" },
];

const BAR_COLORS: Record<string, string> = {
  ICV: "#4472C4",
  IOP: "#ED7D31",
  IMO: "#808080",
  IVP: "#FFC000",
  "QI Total": "#70AD47",
  GAI: "#4472C4",
  CPI: "#843C0C",
};

const CHART = {
  width: 860,
  height: 380,
  marginTop: 44,
  marginRight: 28,
  marginBottom: 56,
  marginLeft: 56,
  minY: 40,
  maxY: 160,
  stepY: 10,
  barWidth: 54,
  gap: 28,
  groupGap: 46,
};

function yScale(value: number) {
  const plotHeight = CHART.height - CHART.marginTop - CHART.marginBottom;
  return CHART.marginTop + ((CHART.maxY - value) / (CHART.maxY - CHART.minY)) * plotHeight;
}

export function WiscChart({ data }: WiscChartProps) {
  if (!data.length) return null;

  const positions: number[] = [];
  let cursor = CHART.marginLeft + 18;
  data.forEach((item) => {
    positions.push(cursor);
    cursor += CHART.barWidth + CHART.gap;
    if (item.label === "IVP") {
      cursor += CHART.groupGap;
    }
  });

  const plotRight = CHART.width - CHART.marginRight;
  const ticks = [] as number[];
  for (let v = CHART.minY; v <= CHART.maxY; v += CHART.stepY) {
    ticks.push(v);
  }

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4">
      <svg viewBox={`0 0 ${CHART.width} ${CHART.height}`} className="h-auto w-full">
        <text
          x={CHART.width / 2}
          y={22}
          textAnchor="middle"
          style={{ fontFamily: '"Liberation Serif", "Times New Roman", serif', fontSize: 20, fill: '#70AD47' }}
        >
          WISC-IV INDICES QIs
        </text>

        {BANDS.map((band) => (
          <rect
            key={`${band.from}-${band.to}`}
            x={CHART.marginLeft}
            y={yScale(band.to)}
            width={plotRight - CHART.marginLeft}
            height={yScale(band.from) - yScale(band.to)}
            fill={band.color}
          />
        ))}

        {ticks.map((tick) => (
          <g key={tick}>
            <line
              x1={CHART.marginLeft}
              x2={plotRight}
              y1={yScale(tick)}
              y2={yScale(tick)}
              stroke="white"
              strokeWidth="1.2"
            />
            <text
              x={CHART.marginLeft - 10}
              y={yScale(tick) + 4}
              textAnchor="end"
              style={{ fontFamily: '"Liberation Serif", "Times New Roman", serif', fontSize: 10, fill: '#555555' }}
            >
              {tick}
            </text>
          </g>
        ))}

        {positions.map((x) => (
          <line
            key={`grid-${x}`}
            x1={x + CHART.barWidth / 2}
            x2={x + CHART.barWidth / 2}
            y1={CHART.marginTop}
            y2={CHART.height - CHART.marginBottom}
            stroke="white"
            strokeWidth="1.2"
          />
        ))}

        <line x1={CHART.marginLeft} x2={CHART.marginLeft} y1={CHART.marginTop} y2={CHART.height - CHART.marginBottom} stroke="#aaaaaa" />
        <line x1={CHART.marginLeft} x2={plotRight} y1={CHART.height - CHART.marginBottom} y2={CHART.height - CHART.marginBottom} stroke="#aaaaaa" />

        <text
          x={18}
          y={CHART.height / 2}
          textAnchor="middle"
          transform={`rotate(-90 18 ${CHART.height / 2})`}
          style={{ fontFamily: '"Liberation Serif", "Times New Roman", serif', fontSize: 11, fill: '#3a5a1a' }}
        >
          Pontos Compostos
        </text>

        {data.map((item, index) => {
          const x = positions[index];
          const y = yScale(item.value);
          const baseY = yScale(CHART.minY);
          const centerX = x + CHART.barWidth / 2;
          const errorTop = yScale(Math.min(CHART.maxY, item.value + 10));
          const errorBottom = yScale(Math.max(CHART.minY, item.value - 10));

          return (
            <g key={item.label}>
              <rect
                x={x}
                y={y}
                width={CHART.barWidth}
                height={baseY - y}
                fill={BAR_COLORS[item.label] || '#5B9BD5'}
              />

              <line x1={centerX} x2={centerX} y1={errorTop} y2={errorBottom} stroke="black" strokeWidth="1.8" />
              <line x1={centerX - 6} x2={centerX + 6} y1={errorTop} y2={errorTop} stroke="black" strokeWidth="1.8" />
              <line x1={centerX - 6} x2={centerX + 6} y1={errorBottom} y2={errorBottom} stroke="black" strokeWidth="1.8" />

              <text
                x={centerX}
                y={yScale(42)}
                textAnchor="middle"
                style={{ fontFamily: '"Liberation Serif", "Times New Roman", serif', fontSize: 11, fontWeight: 700, fill: 'white' }}
              >
                {item.value}
              </text>

              <text
                x={centerX}
                y={CHART.height - CHART.marginBottom + 22}
                textAnchor="middle"
                style={{ fontFamily: '"Liberation Serif", "Times New Roman", serif', fontSize: 10, fill: 'black' }}
              >
                {item.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
