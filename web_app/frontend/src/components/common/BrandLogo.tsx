interface BrandLogoProps {
  variant?: 'user' | 'admin';
  size?: 'sm' | 'md';
  showSubtitle?: boolean;
  className?: string;
}

export function BrandLogo({
  variant = 'user',
  size = 'md',
  showSubtitle = true,
  className = '',
}: BrandLogoProps) {
  const isAdmin = variant === 'admin';
  const markDim = size === 'sm' ? 'h-9 w-9' : 'h-10 w-10';
  const titleClass =
    size === 'sm'
      ? isAdmin
        ? 'text-[15px] font-bold tracking-tight text-white'
        : 'text-[16px] font-bold tracking-tight text-slate-900'
      : isAdmin
        ? 'text-[17px] font-bold tracking-tight text-white'
        : 'text-[18px] font-bold tracking-tight text-slate-900';

  const subtitleClass = isAdmin
    ? 'text-[11px] font-medium text-slate-400'
    : 'text-[11px] font-medium text-slate-500';

  return (
    <span className={`inline-flex items-center gap-2.5 select-none ${className}`}>
      <span
        className={`relative inline-flex ${markDim} shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-[#2563EB] to-[#154EC2] shadow-[0_6px_16px_rgba(29,99,237,0.28)]`}
        aria-hidden="true"
      >
        <svg
          viewBox="0 0 36 36"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
        >
          {/* Rising sun behind Northern limestone peaks */}
          <circle cx="24.5" cy="11.5" r="3" fill="#FDE68A" />
          {/* Mountain peaks */}
          <path
            d="M5.5 23.5L13 11.5L18.5 19.5L22.5 15L30.5 23.5H5.5Z"
            fill="#FFFFFF"
            fillOpacity="0.96"
          />
          {/* Bay water wave */}
          <path
            d="M6.5 26.8C9.8 25.1 13.2 28.4 16.8 26.8C20.4 25.2 23.8 28.4 29.5 26.4"
            stroke="#BFDBFE"
            strokeWidth="2.1"
            strokeLinecap="round"
          />
        </svg>
      </span>
      <span className="flex flex-col leading-tight">
        <span className={titleClass}>{isAdmin ? 'Bắc Việt Admin' : 'Bắc Việt Travel'}</span>
        {showSubtitle && (
          <span className={subtitleClass}>
            {isAdmin ? 'Điều hành & Vận hành' : 'Du lịch miền Bắc'}
          </span>
        )}
      </span>
    </span>
  );
}

export function HeroFlightArc({ className = '' }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 132 30"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      aria-hidden="true"
    >
      <path
        d="M2 22C28 7 68 4 108 14"
        stroke="#93C5FD"
        strokeWidth="1.6"
        strokeDasharray="4 4"
        strokeLinecap="round"
      />
      <path
        d="M113 14.5L125 11.5L117 19.5L116 15.8L113 14.5Z"
        fill="#1D63ED"
      />
      <path
        d="M116 15.8L125 11.5"
        stroke="#1D63ED"
        strokeWidth="1.2"
        strokeLinecap="round"
      />
    </svg>
  );
}
