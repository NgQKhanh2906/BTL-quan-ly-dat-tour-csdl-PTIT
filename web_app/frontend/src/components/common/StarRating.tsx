import { useState } from 'react';
import { Star } from 'lucide-react';

export interface StarRatingProps {
  value: number;
  max?: number;
  interactive?: boolean;
  onChange?: (next: number) => void;
  size?: 'sm' | 'md' | 'lg';
  showValue?: boolean;
  reviewCount?: number;
  ariaLabelPrefix?: string;
  className?: string;
}

const SIZE_MAP = {
  sm: 'h-3.5 w-3.5',
  md: 'h-4.5 w-4.5',
  lg: 'h-6 w-6',
};

const RATING_LABELS: Record<number, string> = {
  1: 'Rất chưa hài lòng',
  2: 'Chưa hài lòng',
  3: 'Bình thường',
  4: 'Hài lòng',
  5: 'Rất hài lòng',
};

export function StarRating({
  value,
  max = 5,
  interactive = false,
  onChange,
  size = 'md',
  showValue = false,
  reviewCount,
  ariaLabelPrefix = 'Chấm điểm',
  className = '',
}: StarRatingProps) {
  const [hoverValue, setHoverValue] = useState<number | null>(null);
  const displayValue = interactive && hoverValue !== null ? hoverValue : value;
  const iconClass = SIZE_MAP[size];

  return (
    <div className={`inline-flex items-center gap-1.5 ${className}`}>
      <div
        className="inline-flex items-center gap-0.5"
        role={interactive ? 'radiogroup' : undefined}
        aria-label={interactive ? ariaLabelPrefix : undefined}
        onMouseLeave={() => interactive && setHoverValue(null)}
      >
        {Array.from({ length: max }, (_, idx) => {
          const starNum = idx + 1;
          const isFilled = starNum <= Math.round(displayValue);

          if (!interactive) {
            return (
              <Star
                key={starNum}
                className={`${iconClass} ${
                  isFilled ? 'fill-[#F59E0B] text-[#F59E0B]' : 'fill-transparent text-slate-300'
                }`}
                strokeWidth={1.75}
                aria-hidden="true"
              />
            );
          }

          return (
            <button
              key={starNum}
              type="button"
              role="radio"
              aria-checked={value === starNum}
              aria-label={`${ariaLabelPrefix} ${starNum} sao`}
              onMouseEnter={() => setHoverValue(starNum)}
              onFocus={() => setHoverValue(starNum)}
              onBlur={() => setHoverValue(null)}
              onClick={() => onChange?.(starNum)}
              className="p-0.5 rounded-md transition-transform duration-150 hover:scale-110 cursor-pointer focus-visible:outline-2 focus-visible:outline-[#1D63ED]"
            >
              <Star
                className={`${iconClass} transition-colors duration-150 ${
                  isFilled ? 'fill-[#F59E0B] text-[#F59E0B]' : 'fill-transparent text-slate-300 hover:text-amber-400'
                }`}
                strokeWidth={1.75}
              />
            </button>
          );
        })}
      </div>

      {interactive && displayValue > 0 && (
        <span className="text-xs font-medium text-slate-600 ml-1">
          {displayValue}/5 — {RATING_LABELS[Math.round(displayValue)] ?? ''}
        </span>
      )}

      {!interactive && showValue && (
        <span className="text-xs font-semibold text-slate-800 tabular-nums">
          {value.toFixed(1)}
          {reviewCount !== undefined && (
            <span className="font-normal text-slate-500"> ({reviewCount})</span>
          )}
        </span>
      )}
    </div>
  );
}
