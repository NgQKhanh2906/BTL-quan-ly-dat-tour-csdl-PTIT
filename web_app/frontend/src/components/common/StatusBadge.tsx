import type { OrderStatusCode } from '../../api/types';

interface StatusBadgeProps {
  status: OrderStatusCode | string;
  label?: string;
  size?: 'sm' | 'md';
  className?: string;
}

const STATUS_STYLE_MAP: Record<
  OrderStatusCode,
  { bg: string; text: string; dot: string; defaultLabel: string }
> = {
  DAT: {
    bg: 'bg-[#EFF6FF] border-[#BFDBFE]',
    text: 'text-[#1D4ED8]',
    dot: 'bg-[#2563EB]',
    defaultLabel: 'Đã đặt tour',
  },
  THANHTOAN: {
    bg: 'bg-[#ECFDF5] border-[#A7F3D0]',
    text: 'text-[#047857]',
    dot: 'bg-[#059669]',
    defaultLabel: 'Đã thanh toán',
  },
  HOANTHANH: {
    bg: 'bg-[#F0FDF4] border-[#BBF7D0]',
    text: 'text-[#15803D]',
    dot: 'bg-[#16A34A]',
    defaultLabel: 'Hoàn thành tour',
  },
  HUY: {
    bg: 'bg-[#FEF2F2] border-[#FECACA]',
    text: 'text-[#B91C1C]',
    dot: 'bg-[#DC2626]',
    defaultLabel: 'Đã hủy tour',
  },
};

export function StatusBadge({
  status,
  label,
  size = 'md',
  className = '',
}: StatusBadgeProps) {
  const key = (status?.toUpperCase() as OrderStatusCode) || 'DAT';
  const cfg = STATUS_STYLE_MAP[key] ?? {
    bg: 'bg-slate-100 border-slate-200',
    text: 'text-slate-700',
    dot: 'bg-slate-500',
    defaultLabel: label || status,
  };

  const sizeClass =
    size === 'sm' ? 'px-2.5 py-0.5 text-[11px] gap-1.5' : 'px-3 py-1 text-xs gap-1.5';

  return (
    <span
      className={[
        'inline-flex items-center rounded-full border font-semibold whitespace-nowrap',
        cfg.bg,
        cfg.text,
        sizeClass,
        className,
      ].join(' ')}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${cfg.dot}`} aria-hidden="true" />
      <span>{label || cfg.defaultLabel}</span>
    </span>
  );
}
