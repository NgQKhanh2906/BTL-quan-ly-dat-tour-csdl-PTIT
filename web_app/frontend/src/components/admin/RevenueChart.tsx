import { useMemo } from 'react';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { BarChart3 } from 'lucide-react';
import type { RevenueTourRow } from '../../api/types';
import { formatVnd } from '../../utils/format';

export interface RevenueChartProps {
  tours: RevenueTourRow[];
}

interface ChartDatum {
  code: string;
  name: string;
  axisLabel: string;
  doanh_thu_dich_vu: number;
  tien_phat_huy: number;
  tong_doanh_thu: number;
  so_don: number;
  so_khach: number;
}

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{
    payload: ChartDatum;
  }>;
}

interface YAxisTickProps {
  x?: number;
  y?: number;
  payload?: {
    value: string;
  };
}

function formatCompactVnd(value: number): string {
  if (value === 0) return '0';
  const abs = Math.abs(value);
  if (abs >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(1).replace(/\.0$/, '')} tỷ`;
  }
  if (abs >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1).replace(/\.0$/, '')} tr`;
  }
  if (abs >= 1_000) {
    return `${Math.round(value / 1_000)}k`;
  }
  return String(value);
}

function splitLabelIntoLines(label: string, maxCharsPerLine: number): string[] {
  const words = label.trim().split(/\s+/);
  const lines: string[] = [];
  let current = '';

  for (const word of words) {
    const candidate = current ? `${current} ${word}` : word;
    if (candidate.length <= maxCharsPerLine) {
      current = candidate;
    } else {
      if (current) {
        lines.push(current);
      }
      current = word;
    }
  }
  if (current) {
    lines.push(current);
  }

  if (lines.length <= 2) {
    return lines;
  }

  const remainderWords = lines.slice(1).join(' ').split(/\s+/);
  let secondLine = '';
  for (const word of remainderWords) {
    const next = secondLine ? `${secondLine} ${word}` : word;
    if (next.length <= maxCharsPerLine - 1) {
      secondLine = next;
    } else {
      break;
    }
  }
  return [lines[0], `${secondLine || lines[1].slice(0, maxCharsPerLine - 1)}…`];
}

function TourYAxisTick({ x = 0, y = 0, payload }: YAxisTickProps) {
  const text = payload?.value ?? '';
  const lines = splitLabelIntoLines(text, 25);

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={-6}
        y={0}
        textAnchor="end"
        fill="#334155"
        fontSize={12}
        fontWeight={500}
      >
        {lines.map((line, idx) => (
          <tspan
            key={`${line}-${idx}`}
            x={-6}
            dy={lines.length === 1 ? '0.35em' : idx === 0 ? '-0.25em' : '1.25em'}
          >
            {line}
          </tspan>
        ))}
      </text>
    </g>
  );
}

function RevenueTooltip({ active, payload }: CustomTooltipProps) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const item = payload[0].payload;
  return (
    <div className="rounded-xl border border-slate-200 bg-white px-3.5 py-3 shadow-[0_12px_28px_rgba(15,23,42,0.12)] text-xs min-w-[230px]">
      <p className="font-bold text-slate-900 leading-snug">
        {item.code} — {item.name}
      </p>
      <p className="mt-0.5 text-[11px] text-slate-500 tabular-nums">
        {item.so_don} đơn · {item.so_khach} khách
      </p>
      <div className="mt-2.5 space-y-1.5 border-t border-slate-100 pt-2">
        <div className="flex items-center justify-between gap-4">
          <span className="inline-flex items-center gap-1.5 text-slate-600">
            <span className="h-2 w-2 rounded-sm bg-[#1D63ED]" aria-hidden="true" />
            Doanh thu dịch vụ
          </span>
          <span className="font-semibold text-slate-900 tabular-nums">
            {formatVnd(item.doanh_thu_dich_vu)}
          </span>
        </div>
        <div className="flex items-center justify-between gap-4">
          <span className="inline-flex items-center gap-1.5 text-slate-600">
            <span className="h-2 w-2 rounded-sm bg-[#F59E0B]" aria-hidden="true" />
            Tiền phạt hủy
          </span>
          <span className="font-semibold text-slate-900 tabular-nums">
            {formatVnd(item.tien_phat_huy)}
          </span>
        </div>
        <div className="flex items-center justify-between gap-4 border-t border-slate-100 pt-1.5">
          <span className="font-semibold text-slate-700">Tổng doanh thu</span>
          <span className="font-bold text-[#1D63ED] tabular-nums">
            {formatVnd(item.tong_doanh_thu)}
          </span>
        </div>
      </div>
    </div>
  );
}

export function RevenueChart({ tours }: RevenueChartProps) {
  const chartData = useMemo<ChartDatum[]>(() => {
    return tours
      .filter((row) => row.ma_tour !== 'TỔNG CỘNG' && row.ten_tour.trim() !== '')
      .map((row) => {
        const trimmedName = row.ten_tour.trim();
        return {
          code: row.ma_tour,
          name: trimmedName,
          axisLabel: `${row.ma_tour} · ${trimmedName}`,
          doanh_thu_dich_vu: row.doanh_thu_dich_vu,
          tien_phat_huy: row.tien_phat_huy,
          tong_doanh_thu: row.tong_doanh_thu,
          so_don: row.so_don,
          so_khach: row.so_khach,
        };
      })
      .sort((a, b) => b.tong_doanh_thu - a.tong_doanh_thu);
  }, [tours]);

  const hasAnyRevenue = chartData.some(
    (d) => d.doanh_thu_dich_vu > 0 || d.tien_phat_huy > 0
  );

  if (chartData.length === 0 || !hasAnyRevenue) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white p-6">
        <div className="flex items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-900">
              Cơ cấu doanh thu theo tuyến tour
            </h2>
            <p className="mt-0.5 text-xs text-slate-500">
              So sánh doanh thu dịch vụ và tiền phạt hủy từng tuyến trong kỳ báo cáo
            </p>
          </div>
        </div>
        <div className="mt-6 flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-200 bg-slate-50/70 px-6 py-12 text-center">
          <BarChart3 className="h-7 w-7 text-slate-400" strokeWidth={1.75} />
          <p className="mt-2.5 text-sm font-semibold text-slate-700">
            Chưa có dữ liệu doanh thu để hiển thị biểu đồ
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Điều chỉnh khoảng ngày khởi hành ở bộ lọc phía trên để xem kết quả.
          </p>
        </div>
      </div>
    );
  }

  const chartHeight = Math.max(280, chartData.length * 54 + 64);

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[0_2px_10px_rgba(15,23,42,0.03)]">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">
            Cơ cấu doanh thu theo tuyến tour
          </h2>
          <p className="mt-0.5 text-xs text-slate-500">
            So sánh trực tiếp doanh thu dịch vụ và tiền phạt hủy theo từng tuyến tour
          </p>
        </div>
        <span className="text-xs font-medium text-slate-500 tabular-nums">
          {chartData.length} tuyến tour
        </span>
      </div>

      <div className="w-full overflow-x-auto">
        <div className="min-w-[560px]" style={{ height: chartHeight }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 8, right: 24, left: 8, bottom: 8 }}
              barCategoryGap="24%"
              barGap={4}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                horizontal={false}
                stroke="#E2E8F0"
              />
              <XAxis
                type="number"
                tickFormatter={formatCompactVnd}
                tick={{ fontSize: 12, fill: '#64748B' }}
                axisLine={{ stroke: '#E2E8F0' }}
                tickLine={false}
              />
              <YAxis
                type="category"
                dataKey="axisLabel"
                width={195}
                interval={0}
                tick={<TourYAxisTick />}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                cursor={{ fill: '#F8FAFC' }}
                content={<RevenueTooltip />}
              />
              <Legend
                verticalAlign="top"
                align="right"
                iconType="circle"
                iconSize={9}
                wrapperStyle={{ paddingBottom: 14, fontSize: '12px', color: '#475569' }}
              />
              <Bar
                dataKey="doanh_thu_dich_vu"
                name="Doanh thu dịch vụ"
                fill="#1D63ED"
                radius={[0, 6, 6, 0]}
                maxBarSize={18}
              />
              <Bar
                dataKey="tien_phat_huy"
                name="Tiền phạt hủy"
                fill="#F59E0B"
                radius={[0, 6, 6, 0]}
                maxBarSize={18}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
