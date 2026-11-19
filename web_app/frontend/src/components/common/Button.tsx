import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { Loader2 } from 'lucide-react';

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';
export type ButtonSize = 'sm' | 'md' | 'lg';
export type ButtonShape = 'pill' | 'rounded';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  shape?: ButtonShape;
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

const VARIANT_CLASSES: Record<ButtonVariant, string> = {
  primary:
    'bg-[#1D63ED] text-white hover:bg-[#154EC2] active:bg-[#103FA3] shadow-[0_8px_20px_rgba(29,99,237,0.22)] hover:shadow-[0_10px_24px_rgba(29,99,237,0.30)] border border-transparent',
  secondary:
    'bg-white text-slate-800 border border-slate-200 hover:bg-slate-50 hover:border-slate-300 active:bg-slate-100 shadow-[0_2px_8px_rgba(15,23,42,0.04)]',
  ghost:
    'bg-transparent text-slate-700 border border-transparent hover:bg-slate-100/90 hover:text-slate-900 active:bg-slate-200/70',
  danger:
    'bg-[#DC2626] text-white hover:bg-[#B91C1C] active:bg-[#991B1B] shadow-[0_6px_16px_rgba(220,38,38,0.20)] border border-transparent',
};

const SIZE_CLASSES: Record<ButtonSize, string> = {
  sm: 'h-9 px-3.5 text-xs gap-1.5',
  md: 'h-10.5 px-4.5 text-sm gap-2',
  lg: 'h-12 px-6 text-[15px] gap-2.5',
};

const SHAPE_CLASSES: Record<ButtonShape, string> = {
  pill: 'rounded-full',
  rounded: 'rounded-[10px]',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  {
    variant = 'primary',
    size = 'md',
    shape = 'rounded',
    loading = false,
    disabled,
    leftIcon,
    rightIcon,
    children,
    className = '',
    type = 'button',
    ...rest
  },
  ref
) {
  const isDisabled = disabled || loading;

  return (
    <button
      ref={ref}
      type={type}
      disabled={isDisabled}
      className={[
        'inline-flex items-center justify-center font-semibold transition-all duration-200 cursor-pointer select-none',
        'disabled:opacity-55 disabled:cursor-not-allowed disabled:shadow-none',
        VARIANT_CLASSES[variant],
        SIZE_CLASSES[size],
        SHAPE_CLASSES[shape],
        className,
      ].join(' ')}
      {...rest}
    >
      {loading ? (
        <Loader2 className="h-4 w-4 animate-spin shrink-0" strokeWidth={1.75} aria-hidden="true" />
      ) : (
        leftIcon && <span className="inline-flex shrink-0">{leftIcon}</span>
      )}
      <span>{children}</span>
      {!loading && rightIcon && <span className="inline-flex shrink-0">{rightIcon}</span>}
    </button>
  );
});
