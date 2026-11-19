import { useEffect, type ReactNode } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { X } from 'lucide-react';

export interface SlideOverDrawerProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  subtitle?: string;
  widthClass?: string;
  footer?: ReactNode;
  children: ReactNode;
}

export function SlideOverDrawer({
  open,
  onClose,
  title,
  subtitle,
  widthClass = 'max-w-2xl',
  footer,
  children,
}: SlideOverDrawerProps) {
  useEffect(() => {
    if (!open) return;
    const prevOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => {
      document.body.style.overflow = prevOverflow;
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, [open, onClose]);

  return (
    <AnimatePresence>
      {open && (
        <div
          className="fixed inset-0 z-50 flex justify-end"
          role="dialog"
          aria-modal="true"
          aria-label={title || 'Chi tiết'}
        >
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            onClick={onClose}
            className="fixed inset-0 bg-slate-950/45 backdrop-blur-[2px]"
          />

          <motion.aside
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ duration: 0.28, ease: [0.22, 1, 0.36, 1] }}
            className={`relative z-10 flex h-full w-full ${widthClass} flex-col bg-white shadow-[0_24px_60px_rgba(15,23,42,0.22)] border-l border-slate-200`}
          >
            <div className="flex items-start justify-between gap-4 px-6 py-5 border-b border-slate-200 bg-white shrink-0">
              <div className="min-w-0">
                {title && (
                  <h2 className="text-lg font-bold text-slate-900 truncate">{title}</h2>
                )}
                {subtitle && (
                  <p className="mt-0.5 text-sm text-slate-500 truncate">{subtitle}</p>
                )}
              </div>
              <button
                type="button"
                onClick={onClose}
                aria-label="Đóng ngăn chi tiết"
                className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-slate-500 hover:bg-slate-100 hover:text-slate-900 transition-colors cursor-pointer"
              >
                <X className="h-5 w-5" strokeWidth={1.75} />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-6 py-5">{children}</div>

            {footer && (
              <div className="shrink-0 border-t border-slate-200 bg-slate-50/80 px-6 py-4">
                {footer}
              </div>
            )}
          </motion.aside>
        </div>
      )}
    </AnimatePresence>
  );
}
