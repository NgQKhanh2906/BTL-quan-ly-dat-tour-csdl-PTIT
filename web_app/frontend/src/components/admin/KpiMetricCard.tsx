import type { ReactNode } from 'react';

export type KpiTone = 'blue' | 'emerald' | 'slate' | 'red';

export interface KpiMetricCardProps {
  label: string;
  value: string | number;
  sublabel?: string;
  icon: ReactNode;
  tone?: KpiTone;
  className?: string;
}

const TONE_ICON_STYLES: Record<KpiTone, string> = {
  blue: 'bg-[#EFF5FF] text-[#1D63ED] border-[#DBEAFE]',
  emerald: 'bg-[#ECFDF5] text-[#047857] border-[#D1FAE5]',
  slate: 'bg-slate-100 text-slate-700 border-slate-200',
  red: 'bg-[#FEF2F2] text-[#B91C1C] border-[#FEE2E2]',
};

const TONE_VALUE_STYLES: Record<KpiTone, string> = {
  blue: 'text-slate-900',
  emerald: 'text-slate-900',
  slate: 'text-slate-900',
  red: 'text-[#B91C1C]',
};

export function KpiMetricCard({
  label,
  value,
  sublabel,
  icon,
  tone = 'blue',
  className = '',
}: KpiMetricCardProps) {
  return (
    <div
      className={[
        'rounded-2xl border border-slate-200/90 bg-white p-5',
        'shadow-[0_2px_10px_rgba(15,23,42,0.03)] transition-colors duration-150 hover:border-slate-300',
        className,
      ].join(' ')}
    >
      <div className="flex items-start justify-between gap-3">
        <p className="text-xs font-semibold text-slate-500 leading-snug">{label}</p>
        <span
          className={[
            'inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border',
            TONE_ICON_STYLES[tone],
          ].join(' ')}
          aria-hidden="true"
        >
          {icon}
        </span>
      </div>

      <p
        className={[
          'mt-3 text-[21px] xl:text-2xl font-bold tracking-tight tabular-nums leading-tight break-words',
          TONE_VALUE_STYLES[tone],
        ].join(' ')}
        title={String(value)}
      >
        {value}
      </p>

      {sublabel && (
        <p className="mt-1.5 text-xs text-slate-500 tabular-nums leading-relaxed">{sublabel}</p>
      )}
    </div>
  );
}
