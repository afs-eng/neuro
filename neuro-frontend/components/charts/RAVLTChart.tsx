type RAVLTChartSeries = {
  key: string;
  label: string;
  color: string;
  values: number[];
};

type RAVLTChartData = {
  title: string;
  labels: string[];
  series: RAVLTChartSeries[];
  y_axis?: {
    min?: number;
    max?: number;
    ticks?: number[];
  };
};

type RAVLTChartProps = {
  data: RAVLTChartData | null | undefined;
};

const CHART = {
  width: 1080,
  height: 460,
  marginTop: 70,
  marginRight: 30,
  marginBottom: 130,
  marginLeft: 65,
};

function linePath(points: Array<{ x: number; y: number }>) {
  return points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x} ${point.y}`).join(' ');
}

export function RAVLTChart({ data }: RAVLTChartProps) {
  if (!data?.labels?.length || !data?.series?.length) return null;

  const yMin = data.y_axis?.min ?? 0;
  const yMax = data.y_axis?.max ?? 21;
  const yTicks = data.y_axis?.ticks?.length ? data.y_axis.ticks : [0, 5, 10, 15, 20];
  const plotWidth = CHART.width - CHART.marginLeft - CHART.marginRight;
  const plotHeight = CHART.height - CHART.marginTop - CHART.marginBottom;
  const stepX = data.labels.length > 1 ? plotWidth / (data.labels.length - 1) : plotWidth;

  const xScale = (index: number) => CHART.marginLeft + stepX * index;
  const yScale = (value: number) => CHART.marginTop + ((yMax - value) / (yMax - yMin)) * plotHeight;

  return (
    <div className="overflow-x-auto rounded-[28px] bg-[#efefef] p-5 shadow-lg ring-1 ring-black/5">
      <svg viewBox={`0 0 ${CHART.width} ${CHART.height}`} className="h-auto min-w-[920px] w-full">
        <text
          x={CHART.width / 2}
          y={34}
          textAnchor="middle"
          style={{ fontFamily: '"Times New Roman", "Liberation Serif", serif', fontSize: 24, fill: '#5B8A3C' }}
        >
          {data.title}
        </text>

        {yTicks.map((tick) => {
          const y = yScale(tick);
          return (
            <g key={tick}>
              <line x1={CHART.marginLeft} x2={CHART.width - CHART.marginRight} y1={y} y2={y} stroke="#c9c9c9" strokeWidth="1" />
              <text
                x={CHART.marginLeft - 14}
                y={y + 4}
                textAnchor="end"
                style={{ fontFamily: '"Times New Roman", "Liberation Serif", serif', fontSize: 12, fill: '#555555' }}
              >
                {tick}
              </text>
            </g>
          );
        })}

        {data.labels.map((label, index) => (
          <text
            key={label}
            x={xScale(index)}
            y={CHART.height - CHART.marginBottom + 28}
            textAnchor="middle"
            style={{ fontFamily: '"Times New Roman", "Liberation Serif", serif', fontSize: 13, fill: '#555555' }}
          >
            {label}
          </text>
        ))}

        {data.series.map((series) => {
          const points = series.values.map((value, index) => ({ x: xScale(index), y: yScale(value) }));

          return (
            <g key={series.key}>
              <path d={linePath(points)} fill="none" stroke={series.color} strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
              {points.map((point, index) => (
                <circle key={`${series.key}-${index}`} cx={point.x} cy={point.y} r="3.5" fill={series.color} />
              ))}
            </g>
          );
        })}

        {data.series.map((series, index) => {
          const blockWidth = 150;
          const totalWidth = data.series.length * blockWidth;
          const startX = (CHART.width - totalWidth) / 2;
          const x = startX + index * blockWidth;
          const y = CHART.height - 42;

          return (
            <g key={`legend-${series.key}`}>
              <line x1={x} x2={x + 28} y1={y} y2={y} stroke={series.color} strokeWidth="3" strokeLinecap="round" />
              <text
                x={x + 38}
                y={y + 4}
                style={{ fontFamily: '"Times New Roman", "Liberation Serif", serif', fontSize: 13, fill: '#666666' }}
              >
                {series.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
