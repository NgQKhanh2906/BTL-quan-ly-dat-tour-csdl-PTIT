import type { ReactNode } from 'react';
import { Compass } from 'lucide-react';

export interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function EmptyState({
  icon,
  title,
  description,
  action,
  className = '',
}: EmptyStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center text-center rounded-[20px] border border-slate-200/80 bg-white px-6 py-12 ${className}`}
    >
      <div className="mb-4 inline-flex h-14 w-14 items-center justify-center rounded-2xl bg-[#EFF5FF] text-[#1D63ED]">
        {icon ?? <Compass className="h-7 w-7" strokeWidth={1.75} />}
      </div>
      <h3 className="text-base font-bold text-slate-900">{title}</h3>
      {description && (
        <p className="mt-1.5 max-w-md text-sm text-slate-600 leading-relaxed">{description}</p>
      )}
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
