import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  AlertCircle,
  CheckCircle2,
  Download,
  FileText,
  Printer,
  RefreshCw,
  Search,
  UserPen,
  X,
} from 'lucide-react';
import { ApiError, api } from '../../api/client';
import type { AdminOrderSummary } from '../../api/types';
import { DocumentPreviewFrame } from '../../components/admin/DocumentPreviewFrame';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { SkeletonLine } from '../../components/common/LoadingSkeleton';
import { StatusBadge } from '../../components/common/StatusBadge';
import { useAuth } from '../../context/AuthContext';
import { formatDate, formatVnd } from '../../utils/format';

export function AdminConfirmationsPage() {
  const { admin } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const orderFromUrl = searchParams.get('order')?.trim() || '';

  const printFnRef = useRef<(() => void) | null>(null);
  const issuerInputRef = useRef<HTMLInputElement | null>(null);
  const initialOrderParamRef = useRef<string>(orderFromUrl);

  const [orders, setOrders] = useState<AdminOrderSummary[]>([]);
  const [ordersLoading, setOrdersLoading] = useState(true);
  const [ordersError, setOrdersError] = useState<string | null>(null);

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedOrderId, setSelectedOrderId] = useState<string>(orderFromUrl);

  const [nguoiLap, setNguoiLap] = useState(admin?.staff_name || 'Nguyễn Quốc Khánh');
  const [debouncedNguoiLap, setDebouncedNguoiLap] = useState(
    admin?.staff_name || 'Nguyễn Quốc Khánh'
  );
  const [issuerError, setIssuerError] = useState<string | null>(null);

  const [html, setHtml] = useState<string | null>(null);
  const [htmlLoading, setHtmlLoading] = useState(false);
  const [htmlError, setHtmlError] = useState<string | null>(null);

  const [pdfLoading, setPdfLoading] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: 'success' | 'error';
    text: string;
  } | null>(null);

  // Debounce staff issuer name so preview updates smoothly without spamming backend
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedNguoiLap(nguoiLap.trim());
    }, 350);
    return () => window.clearTimeout(timer);
  }, [nguoiLap]);

  const loadOrders = useCallback(async () => {
    setOrdersLoading(true);
    setOrdersError(null);
    try {
      const res = await api.getAdminOrders();
      setOrders(res.orders);
      const initialOrder = initialOrderParamRef.current;
      setSelectedOrderId((prev) => {
        if (prev && res.orders.some((o) => o.ma_don_hang === prev)) {
          return prev;
        }
        if (initialOrder && res.orders.some((o) => o.ma_don_hang === initialOrder)) {
          return initialOrder;
        }
        return res.orders[0]?.ma_don_hang ?? '';
      });
    } catch (err) {
      setOrdersError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tải danh sách đơn hàng.'
      );
    } finally {
      setOrdersLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadOrders();
  }, [loadOrders]);

  // Sync when URL query ?order= changes externally
  useEffect(() => {
    if (orderFromUrl) {
      setSelectedOrderId(orderFromUrl);
    }
  }, [orderFromUrl]);

  const loadConfirmationHtml = useCallback(
    async (orderId: string, issuer: string) => {
      if (!orderId) {
        setHtml(null);
        return;
      }
      setHtmlLoading(true);
      setHtmlError(null);
      try {
        const res = await api.getConfirmationHtml(
          orderId,
          issuer || admin?.staff_name || 'Nguyễn Quốc Khánh'
        );
        setHtml(res.html);
      } catch (err) {
        setHtml(null);
        setHtmlError(
          err instanceof ApiError
            ? err.message
            : 'Không thể tải bản xem trước phiếu xác nhận.'
        );
      } finally {
        setHtmlLoading(false);
      }
    },
    [admin?.staff_name]
  );

  useEffect(() => {
    if (!selectedOrderId) return;
    void loadConfirmationHtml(selectedOrderId, debouncedNguoiLap);
  }, [selectedOrderId, debouncedNguoiLap, loadConfirmationHtml]);

  const filteredOrders = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return orders;
    return orders.filter(
      (o) =>
        o.ma_don_hang.toLowerCase().includes(q) ||
        o.ho_ten.toLowerCase().includes(q) ||
        o.ten_tour.toLowerCase().includes(q) ||
        o.tinh_den.toLowerCase().includes(q)
    );
  }, [orders, searchQuery]);

  const selectedOrder = useMemo(
    () => orders.find((o) => o.ma_don_hang === selectedOrderId) ?? null,
    [orders, selectedOrderId]
  );

  const selectedInFiltered = useMemo(
    () => filteredOrders.some((o) => o.ma_don_hang === selectedOrderId),
    [filteredOrders, selectedOrderId]
  );

  const handleSelectOrder = (maDon: string) => {
    if (!maDon) return;
    setSelectedOrderId(maDon);
    setFeedback(null);
    setSearchParams({ order: maDon }, { replace: true });
  };

  const handleDownloadPdf = async () => {
    setFeedback(null);
    if (!selectedOrderId) return;
    const cleanIssuer = nguoiLap.trim();
    if (!cleanIssuer) {
      setIssuerError('Vui lòng nhập họ tên nhân viên lập phiếu.');
      issuerInputRef.current?.focus();
      return;
    }
    setIssuerError(null);
    setPdfLoading(true);
    try {
      await api.downloadConfirmationPdf(selectedOrderId, cleanIssuer);
      setFeedback({
        type: 'success',
        text: `Đã tải phiếu xác nhận đặt tour ${selectedOrderId} (PDF khổ A4 dọc).`,
      });
    } catch (err) {
      setFeedback({
        type: 'error',
        text:
          err instanceof ApiError
            ? err.message
            : 'Không thể xuất file PDF phiếu xác nhận.',
      });
    } finally {
      setPdfLoading(false);
    }
  };

  const handleDirectPrint = () => {
    printFnRef.current?.();
  };

  const handleRegisterPrint = useCallback((fn: () => void) => {
    printFnRef.current = fn;
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8 space-y-6">
      {/* Tiêu đề trang */}
      <div>
        <h1 className="text-2xl sm:text-[28px] font-bold text-slate-900 tracking-tight">
          Phiếu xác nhận đặt tour
        </h1>
      </div>

      {/* Compact Full-Width Horizontal Control Bar */}
      <section className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[0_2px_10px_rgba(15,23,42,0.03)] space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-4 items-start">
          {/* Quick Search Filter */}
          <div className="md:col-span-3">
            <label
              htmlFor="confirmation-search"
              className="block text-xs font-semibold text-slate-700 mb-1.5"
            >
              Lọc nhanh đơn hàng
            </label>
            <div className="relative">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                id="confirmation-search"
                type="search"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Mã đơn, khách hàng, tour..."
                className="h-10 w-full rounded-[10px] border border-slate-200 bg-white pl-9 pr-8 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              />
              {searchQuery && (
                <button
                  type="button"
                  onClick={() => setSearchQuery('')}
                  aria-label="Xóa từ khóa lọc"
                  className="absolute right-2.5 top-1/2 -translate-y-1/2 inline-flex h-5 w-5 items-center justify-center rounded text-slate-400 hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                >
                  <X className="h-3.5 w-3.5" strokeWidth={1.75} />
                </button>
              )}
            </div>
          </div>

          {/* Order Selector Dropdown */}
          <div className="md:col-span-5">
            <div className="flex items-center justify-between gap-2 mb-1.5">
              <label
                htmlFor="confirmation-order-select"
                className="block text-xs font-semibold text-slate-700"
              >
                Chọn đơn hàng
              </label>
              <span className="text-[11px] font-medium text-slate-500 tabular-nums">
                {filteredOrders.length}/{orders.length} đơn
              </span>
            </div>

            {ordersLoading ? (
              <SkeletonLine className="h-10 w-full rounded-[10px]" />
            ) : ordersError ? (
              <div className="flex items-center justify-between gap-2 rounded-[10px] border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
                <span className="truncate">{ordersError}</span>
                <button
                  type="button"
                  onClick={() => void loadOrders()}
                  className="inline-flex shrink-0 items-center gap-1 font-semibold underline cursor-pointer"
                >
                  <RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />
                  Thử lại
                </button>
              </div>
            ) : (
              <select
                id="confirmation-order-select"
                value={selectedInFiltered ? selectedOrderId : ''}
                onChange={(e) => handleSelectOrder(e.target.value)}
                disabled={filteredOrders.length === 0}
                className="h-10 w-full rounded-[10px] border border-slate-200 bg-white px-3 text-sm text-slate-900 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15 disabled:bg-slate-50 disabled:text-slate-400"
              >
                {filteredOrders.length === 0 ? (
                  <option value="">Không có đơn hàng khớp từ khóa</option>
                ) : (
                  <>
                    {!selectedInFiltered && (
                      <option value="" disabled>
                        Chọn trong {filteredOrders.length} đơn hàng phù hợp...
                      </option>
                    )}
                    {filteredOrders.map((order) => (
                      <option key={order.ma_don_hang} value={order.ma_don_hang}>
                        {order.ma_don_hang} — {order.ho_ten} · {order.ten_tour} ({order.ten_trang_thai})
                      </option>
                    ))}
                  </>
                )}
              </select>
            )}
          </div>

          {/* Staff Issuer Input */}
          <div className="md:col-span-4">
            <label
              htmlFor="confirmation-issuer"
              className="block text-xs font-semibold text-slate-700 mb-1.5"
            >
              Nhân viên lập phiếu <span className="text-red-600">*</span>
            </label>
            <div className="relative">
              <UserPen
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                ref={issuerInputRef}
                id="confirmation-issuer"
                type="text"
                value={nguoiLap}
                onChange={(e) => {
                  setNguoiLap(e.target.value);
                  if (issuerError && e.target.value.trim()) {
                    setIssuerError(null);
                  }
                }}
                placeholder="Nhập họ tên nhân viên lập phiếu..."
                aria-invalid={Boolean(issuerError)}
                className={[
                  'h-10 w-full rounded-[10px] border bg-white pl-9 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2',
                  issuerError
                    ? 'border-red-300 focus:border-red-500 focus:ring-red-500/15'
                    : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
                ].join(' ')}
              />
            </div>
            {issuerError && (
              <p role="alert" className="mt-1 text-xs font-medium text-red-600">
                {issuerError}
              </p>
            )}
          </div>
        </div>

        {/* Selected Order Summary & Primary Actions */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-3.5">
          <div className="flex flex-wrap items-center gap-2.5 text-xs text-slate-600 min-w-0">
            {selectedOrder ? (
              <>
                <span className="font-bold text-slate-900 tabular-nums">
                  {selectedOrder.ma_don_hang}
                </span>
                <StatusBadge
                  status={selectedOrder.ma_trang_thai}
                  label={selectedOrder.ten_trang_thai}
                  size="sm"
                />
                <span className="text-slate-300" aria-hidden="true">
                  |
                </span>
                <span className="font-semibold text-slate-800">{selectedOrder.ho_ten}</span>
                <span className="text-slate-300" aria-hidden="true">
                  ·
                </span>
                <span className="tabular-nums">
                  Khởi hành {formatDate(selectedOrder.ngay_xuat_phat)}
                </span>
                <span className="text-slate-300" aria-hidden="true">
                  ·
                </span>
                <span className="font-bold text-[#1D63ED] tabular-nums">
                  {formatVnd(selectedOrder.tong_tien)}
                </span>
              </>
            ) : (
              <span className="text-slate-500">
                Chọn một đơn hàng phía trên để xem trước và xuất phiếu xác nhận.
              </span>
            )}
          </div>

          <div className="flex flex-wrap items-center gap-2.5 shrink-0">
            <Button
              variant="secondary"
              size="md"
              shape="rounded"
              disabled={!selectedOrderId || htmlLoading || !html}
              onClick={handleDirectPrint}
              leftIcon={<Printer className="h-4 w-4" strokeWidth={1.75} />}
            >
              In trực tiếp
            </Button>

            <Button
              variant="primary"
              size="md"
              shape="rounded"
              loading={pdfLoading}
              disabled={!selectedOrderId || htmlLoading}
              onClick={() => void handleDownloadPdf()}
              leftIcon={<Download className="h-4 w-4" strokeWidth={1.75} />}
            >
              Tải phiếu xác nhận (PDF - A4 dọc)
            </Button>
          </div>
        </div>

        {feedback && (
          <div
            role={feedback.type === 'error' ? 'alert' : 'status'}
            className={[
              'flex items-center justify-between gap-3 rounded-xl border px-4 py-2.5 text-xs font-medium',
              feedback.type === 'success'
                ? 'border-emerald-200 bg-emerald-50 text-emerald-900'
                : 'border-red-200 bg-red-50 text-red-900',
            ].join(' ')}
          >
            <div className="flex items-center gap-2">
              {feedback.type === 'success' ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" strokeWidth={1.75} />
              ) : (
                <AlertCircle className="h-4 w-4 shrink-0 text-red-600" strokeWidth={1.75} />
              )}
              <span>{feedback.text}</span>
            </div>
            <button
              type="button"
              onClick={() => setFeedback(null)}
              className="text-xs underline underline-offset-2 opacity-80 hover:opacity-100 cursor-pointer"
            >
              Đóng
            </button>
          </div>
        )}
      </section>

      {/* Full-Width Centered Live A4 Portrait Preview */}
      {!ordersLoading && orders.length === 0 ? (
        <EmptyState
          icon={<FileText className="h-7 w-7" strokeWidth={1.75} />}
          title="Chưa có đơn hàng để xuất phiếu xác nhận"
          description="Hệ thống hiện chưa có đơn đặt tour nào để tạo phiếu xác nhận."
        />
      ) : (
        <DocumentPreviewFrame
          title={
            selectedOrder
              ? `Phiếu xác nhận đặt tour — ${selectedOrder.ma_don_hang}`
              : 'Xem trước Phiếu xác nhận đặt tour'
          }
          subtitle={
            selectedOrder
              ? `${selectedOrder.ho_ten} · ${selectedOrder.ten_tour} · Người lập: ${
                  nguoiLap.trim() || admin?.staff_name || 'Nguyễn Quốc Khánh'
                }`
              : 'Chọn một đơn hàng ở thanh điều khiển phía trên để xem trước biểu mẫu in'
          }
          orientation="portrait"
          html={html}
          loading={htmlLoading || (ordersLoading && !html)}
          error={htmlError}
          onRetry={() => {
            if (selectedOrderId) {
              void loadConfirmationHtml(selectedOrderId, debouncedNguoiLap);
            }
          }}
          showPrintButton={false}
          onPrintReady={handleRegisterPrint}
        />
      )}
    </div>
  );
}

export default AdminConfirmationsPage;
