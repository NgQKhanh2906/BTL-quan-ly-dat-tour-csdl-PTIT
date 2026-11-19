import { useCallback, useEffect, useRef, useState } from 'react';
import { AlertCircle, Download, FileText, Printer, RefreshCw } from 'lucide-react';
import { Button } from '../common/Button';
import { SkeletonLine } from '../common/LoadingSkeleton';

export interface DocumentPreviewFrameProps {
  title: string;
  subtitle?: string;
  orientation: 'portrait' | 'landscape';
  html: string | null;
  loading?: boolean;
  error?: string | null;
  onRetry?: () => void;
  onDownloadPdf?: () => void;
  downloadingPdf?: boolean;
  downloadLabel?: string;
  showPrintButton?: boolean;
  className?: string;
  onPrintReady?: (printFn: () => void) => void;
}

export function DocumentPreviewFrame({
  title,
  subtitle,
  orientation,
  html,
  loading = false,
  error = null,
  onRetry,
  onDownloadPdf,
  downloadingPdf = false,
  downloadLabel,
  showPrintButton = true,
  className = '',
  onPrintReady,
}: DocumentPreviewFrameProps) {
  const iframeRef = useRef<HTMLIFrameElement | null>(null);
  const defaultMinHeight = orientation === 'portrait' ? 1040 : 720;
  const [frameHeight, setFrameHeight] = useState<number>(defaultMinHeight);

  useEffect(() => {
    setFrameHeight(defaultMinHeight);
  }, [defaultMinHeight, html]);

  const handlePrint = useCallback(() => {
    const win = iframeRef.current?.contentWindow;
    if (!win) return;
    win.focus();
    win.print();
  }, []);

  useEffect(() => {
    onPrintReady?.(handlePrint);
  }, [handlePrint, onPrintReady]);

  const handleIframeLoad = () => {
    try {
      const doc = iframeRef.current?.contentDocument;
      if (!doc) return;
      const measured = Math.max(
        doc.body?.scrollHeight ?? 0,
        doc.documentElement?.scrollHeight ?? 0
      );
      if (measured > 200) {
        setFrameHeight(Math.max(defaultMinHeight, measured + 24));
      }
    } catch {
      setFrameHeight(defaultMinHeight);
    }
  };

  const paperWidthClass =
    orientation === 'portrait'
      ? 'w-full max-w-[820px]'
      : 'w-full max-w-[1040px] min-w-[780px]';
  const orientationBadge = orientation === 'portrait' ? 'Khổ A4 dọc' : 'Khổ A4 ngang';

  return (
    <div
      className={[
        'rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-[0_2px_10px_rgba(15,23,42,0.03)]',
        className,
      ].join(' ')}
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-white px-5 py-3.5">
        <div className="flex items-center gap-3 min-w-0">
          <span
            className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-slate-50 text-slate-700"
            aria-hidden="true"
          >
            <FileText className="h-4.5 w-4.5" strokeWidth={1.75} />
          </span>
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-sm font-bold text-slate-900 truncate">{title}</h2>
              <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-[11px] font-medium text-slate-600">
                {orientationBadge}
              </span>
            </div>
            {subtitle && (
              <p className="mt-0.5 text-xs text-slate-500 truncate">{subtitle}</p>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {showPrintButton && (
            <Button
              variant="secondary"
              size="sm"
              shape="rounded"
              disabled={loading || !html}
              onClick={handlePrint}
              leftIcon={<Printer className="h-4 w-4" strokeWidth={1.75} />}
            >
              In trực tiếp
            </Button>
          )}
          {onDownloadPdf && (
            <Button
              variant="primary"
              size="sm"
              shape="rounded"
              loading={downloadingPdf}
              disabled={loading}
              onClick={onDownloadPdf}
              leftIcon={<Download className="h-4 w-4" strokeWidth={1.75} />}
            >
              {downloadLabel ?? (orientation === 'portrait' ? 'Tải PDF (A4 dọc)' : 'Tải PDF (A4 ngang)')}
            </Button>
          )}
        </div>
      </div>

      <div className="bg-slate-100/90 p-4 sm:p-6 overflow-x-auto">
        {loading ? (
          <div
            className={`mx-auto ${paperWidthClass} max-w-full rounded-xl border border-slate-200 bg-white p-8 space-y-4 shadow-[0_10px_28px_rgba(15,23,42,0.06)]`}
          >
            <div className="flex justify-between gap-4">
              <SkeletonLine className="h-5 w-52" />
              <SkeletonLine className="h-5 w-40" />
            </div>
            <SkeletonLine className="h-7 w-2/3 mx-auto" />
            <SkeletonLine className="h-4 w-1/2 mx-auto" />
            <div className="pt-4 space-y-3">
              <SkeletonLine className="h-24 w-full" />
              <SkeletonLine className="h-40 w-full" />
              <SkeletonLine className="h-32 w-full" />
            </div>
          </div>
        ) : error ? (
          <div className="mx-auto max-w-lg rounded-xl border border-red-200 bg-white p-6 text-center">
            <div className="mx-auto mb-3 inline-flex h-11 w-11 items-center justify-center rounded-xl bg-red-50 text-red-600">
              <AlertCircle className="h-5 w-5" strokeWidth={1.75} />
            </div>
            <p className="text-sm font-semibold text-slate-900">Không thể tải bản xem trước</p>
            <p className="mt-1 text-xs text-slate-600">{error}</p>
            {onRetry && (
              <div className="mt-4">
                <Button
                  variant="secondary"
                  size="sm"
                  shape="rounded"
                  onClick={onRetry}
                  leftIcon={<RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />}
                >
                  Thử tải lại
                </Button>
              </div>
            )}
          </div>
        ) : !html ? (
          <div className="mx-auto max-w-md rounded-xl border border-slate-200 bg-white p-8 text-center">
            <FileText className="mx-auto h-7 w-7 text-slate-400" strokeWidth={1.75} />
            <p className="mt-2.5 text-sm font-semibold text-slate-700">
              Chưa có tài liệu để hiển thị
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Chọn đơn hàng hoặc áp dụng kỳ báo cáo để tải bản xem trước.
            </p>
          </div>
        ) : (
          <div
            className={`mx-auto ${paperWidthClass} rounded-lg border border-slate-200/90 bg-white shadow-[0_12px_32px_rgba(15,23,42,0.09)] overflow-hidden`}
          >
            <iframe
              ref={iframeRef}
              title={title}
              srcDoc={html}
              onLoad={handleIframeLoad}
              style={{ height: `${frameHeight}px` }}
              className="block w-full border-0 bg-white"
            />
          </div>
        )}
      </div>
    </div>
  );
}
