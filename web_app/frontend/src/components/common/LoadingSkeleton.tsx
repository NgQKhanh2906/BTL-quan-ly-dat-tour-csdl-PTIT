export function SkeletonLine({ className = 'h-4 w-full' }: { className?: string }) {
  return <div className={`animate-pulse rounded-lg bg-slate-200/75 ${className}`} />;
}

export function SkeletonCard({ className = '' }: { className?: string }) {
  return (
    <div
      className={`rounded-[20px] border border-slate-200/70 bg-white overflow-hidden shadow-[var(--shadow-card)] ${className}`}
    >
      <div className="aspect-[4/3] w-full animate-pulse bg-slate-200/75" />
      <div className="p-4 space-y-3">
        <SkeletonLine className="h-4 w-3/4" />
        <SkeletonLine className="h-3.5 w-1/2" />
        <div className="pt-2 flex items-center justify-between">
          <SkeletonLine className="h-5 w-24" />
          <SkeletonLine className="h-8 w-24 rounded-full" />
        </div>
      </div>
    </div>
  );
}

export function SkeletonTableRows({
  rows = 5,
  columns = 6,
}: {
  rows?: number;
  columns?: number;
}) {
  return (
    <>
      {Array.from({ length: rows }, (_, rowIdx) => (
        <tr key={rowIdx} className="border-b border-slate-100">
          {Array.from({ length: columns }, (_, colIdx) => (
            <td key={colIdx} className="px-4 py-3.5">
              <SkeletonLine className="h-4 w-full max-w-[140px]" />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}

export interface LoadingSkeletonProps {
  variant?: 'cards' | 'list' | 'table' | 'kpi';
  count?: number;
  className?: string;
}

export function LoadingSkeleton({
  variant = 'cards',
  count = 4,
  className = '',
}: LoadingSkeletonProps) {
  if (variant === 'kpi') {
    return (
      <div className={`grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 ${className}`}>
        {Array.from({ length: count }, (_, idx) => (
          <div
            key={idx}
            className="rounded-2xl border border-slate-200 bg-white p-5 space-y-3"
          >
            <SkeletonLine className="h-3.5 w-28" />
            <SkeletonLine className="h-8 w-36" />
            <SkeletonLine className="h-3 w-20" />
          </div>
        ))}
      </div>
    );
  }

  if (variant === 'list') {
    return (
      <div className={`space-y-4 ${className}`}>
        {Array.from({ length: count }, (_, idx) => (
          <div
            key={idx}
            className="rounded-[20px] border border-slate-200/80 bg-white p-5 space-y-3"
          >
            <div className="flex items-center justify-between gap-4">
              <SkeletonLine className="h-5 w-52" />
              <SkeletonLine className="h-6 w-28 rounded-full" />
            </div>
            <SkeletonLine className="h-4 w-2/3" />
            <SkeletonLine className="h-4 w-1/3" />
          </div>
        ))}
      </div>
    );
  }

  if (variant === 'table') {
    return (
      <div className={`rounded-2xl border border-slate-200 bg-white overflow-hidden ${className}`}>
        <div className="p-4 space-y-3">
          {Array.from({ length: count }, (_, idx) => (
            <SkeletonLine key={idx} className="h-10 w-full" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 ${className}`}>
      {Array.from({ length: count }, (_, idx) => (
        <SkeletonCard key={idx} />
      ))}
    </div>
  );
}
