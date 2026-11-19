import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AlertCircle,
  AlertTriangle,
  Bus,
  Calendar,
  CheckCircle2,
  Download,
  ExternalLink,
  Home,
  MapPin,
  Phone,
  RefreshCw,
  User,
  XCircle,
} from 'lucide-react';
import { ApiError, api } from '../../api/client';
import type { AdminOrderFullResponse, CancelPreviewResponse } from '../../api/types';
import { useAuth } from '../../context/AuthContext';
import {
  extractDatePart,
  extractTimePart,
  formatDateTime,
  formatDuration,
  formatVnd,
  toSqlDateTimeInput,
} from '../../utils/format';
import { Button } from '../common/Button';
import { SkeletonLine } from '../common/LoadingSkeleton';
import { SlideOverDrawer } from '../common/SlideOverDrawer';
import { StatusBadge } from '../common/StatusBadge';

export interface OrderActionDrawerProps {
  orderId: string | null;
  open: boolean;
  defaultSystemDateTime?: string | null;
  onClose: () => void;
  onOrderUpdated: (message: string) => void;
}

export function OrderActionDrawer({
  orderId,
  open,
  defaultSystemDateTime,
  onClose,
  onOrderUpdated,
}: OrderActionDrawerProps) {
  const { admin } = useAuth();

  const [data, setData] = useState<AdminOrderFullResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [actionLoading, setActionLoading] = useState(false);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  // Cancel order flow state
  const [cancelPanelOpen, setCancelPanelOpen] = useState(false);
  const [cancelDate, setCancelDate] = useState('');
  const [cancelTime, setCancelTime] = useState('09:00');
  const [cancelReason, setCancelReason] = useState('');
  const [agreedPenalty, setAgreedPenalty] = useState(false);
  const [cancelPreview, setCancelPreview] = useState<CancelPreviewResponse | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);
  const [cancelSubmitting, setCancelSubmitting] = useState(false);

  const resetCancelState = useCallback(
    (sysDt?: string | null) => {
      const refIso = sysDt ?? defaultSystemDateTime ?? '';
      setCancelPanelOpen(false);
      setCancelDate(extractDatePart(refIso) || '2026-10-23');
      setCancelTime(extractTimePart(refIso) || '09:00');
      setCancelReason('');
      setAgreedPenalty(false);
      setCancelPreview(null);
      setPreviewError(null);
    },
    [defaultSystemDateTime]
  );

  const loadOrderDetail = useCallback(async (id: string) => {
    setLoading(true);
    setLoadError(null);
    try {
      const res = await api.getAdminOrderDetail(id);
      setData(res);
    } catch (err) {
      setLoadError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tải thông tin chi tiết đơn hàng.'
      );
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!open || !orderId) return;
    setActionError(null);
    setActionSuccess(null);
    resetCancelState(defaultSystemDateTime);
    void loadOrderDetail(orderId);

    if (!defaultSystemDateTime) {
      api
        .getMeta()
        .then((meta) => {
          setCancelDate(extractDatePart(meta.current_datetime) || meta.current_date);
          setCancelTime(extractTimePart(meta.current_datetime) || '09:00');
        })
        .catch(() => {
          // Keep fallback date/time if meta fails
        });
    }
  }, [open, orderId, defaultSystemDateTime, loadOrderDetail, resetCancelState]);

  // Live penalty preview whenever cancel panel is open & cancelDate/cancelTime change
  useEffect(() => {
    if (!open || !orderId || !cancelPanelOpen) return;
    const sqlDt = toSqlDateTimeInput(cancelDate, cancelTime);
    if (!sqlDt) {
      setCancelPreview(null);
      return;
    }

    let cancelled = false;
    setPreviewLoading(true);
    setPreviewError(null);

    const timer = window.setTimeout(async () => {
      try {
        const preview = await api.previewCancelOrder(orderId, sqlDt);
        if (!cancelled) {
          setCancelPreview(preview);
        }
      } catch (err) {
        if (!cancelled) {
          setCancelPreview(null);
          setPreviewError(
            err instanceof ApiError
              ? err.message
              : 'Không thể tính mức phí phạt hủy cho thời điểm đã chọn.'
          );
        }
      } finally {
        if (!cancelled) {
          setPreviewLoading(false);
        }
      }
    }, 180);

    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [open, orderId, cancelPanelOpen, cancelDate, cancelTime]);

  const handleUpdateStatus = async (nextStatus: 'THANHTOAN' | 'HOANTHANH') => {
    if (!orderId) return;
    setActionLoading(true);
    setActionError(null);
    setActionSuccess(null);
    try {
      const res = await api.updateOrderStatus(orderId, nextStatus);
      const label =
        nextStatus === 'THANHTOAN'
          ? `Đã xác nhận thanh toán cho đơn ${orderId}.`
          : `Đã đánh dấu hoàn thành cho đơn ${orderId}.`;
      setActionSuccess(res.message || label);
      await loadOrderDetail(orderId);
      onOrderUpdated(label);
    } catch (err) {
      setActionError(
        err instanceof ApiError
          ? err.message
          : 'Không thể cập nhật trạng thái đơn hàng.'
      );
    } finally {
      setActionLoading(false);
    }
  };

  const handleConfirmCancel = async () => {
    if (!orderId) return;
    setActionError(null);
    setActionSuccess(null);

    const trimmedReason = cancelReason.trim();
    if (!trimmedReason) {
      setActionError('Vui lòng nhập lý do hủy đơn hàng.');
      return;
    }
    if (!agreedPenalty) {
      setActionError('Vui lòng xác nhận khách hàng đã đồng ý với mức phí phạt hủy tour.');
      return;
    }
    const sqlDt = toSqlDateTimeInput(cancelDate, cancelTime);
    if (!sqlDt) {
      setActionError('Vui lòng chọn đầy đủ ngày và giờ hủy đơn.');
      return;
    }

    setCancelSubmitting(true);
    try {
      const res = await api.cancelOrder(orderId, {
        ngay_gio_huy: sqlDt,
        ly_do_huy: trimmedReason,
        da_dong_y_phat: agreedPenalty,
      });
      const summaryMsg = `Đã hủy đơn ${orderId} · Hoàn ${res.so_cho_hoan} chỗ · Phí phạt ${formatVnd(res.tien_phat)} · Hoàn khách ${formatVnd(res.tien_hoan)}.`;
      setCancelPanelOpen(false);
      setActionSuccess(summaryMsg);
      await loadOrderDetail(orderId);
      onOrderUpdated(summaryMsg);
    } catch (err) {
      setActionError(
        err instanceof ApiError ? err.message : 'Không thể thực hiện hủy đơn hàng.'
      );
    } finally {
      setCancelSubmitting(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!orderId) return;
    setPdfLoading(true);
    setActionError(null);
    try {
      await api.downloadConfirmationPdf(orderId, admin?.staff_name);
    } catch (err) {
      setActionError(
        err instanceof ApiError
          ? err.message
          : 'Không thể xuất file PDF phiếu xác nhận.'
      );
    } finally {
      setPdfLoading(false);
    }
  };

  const detail = data?.detail;
  const validNext = data?.valid_next_statuses ?? [];
  const canPay = validNext.some((s) => s.ma_trang_thai === 'THANHTOAN');
  const canComplete = validNext.some((s) => s.ma_trang_thai === 'HOANTHANH');
  const canCancel = validNext.some((s) => s.ma_trang_thai === 'HUY');

  // Client-side time range warning for cancel picker
  let cancelTimeWarning: string | null = null;
  if (detail && cancelPanelOpen && cancelDate) {
    const chosenIso = toSqlDateTimeInput(cancelDate, cancelTime);
    const bookedIso = detail.ngay_dat.replace(' ', 'T').slice(0, 19);
    const departIso = detail.ngay_xuat_phat.replace(' ', 'T').slice(0, 19);
    if (chosenIso < bookedIso) {
      cancelTimeWarning = `Thời điểm hủy không được sớm hơn thời điểm đặt (${formatDateTime(detail.ngay_dat)}).`;
    } else if (chosenIso >= departIso) {
      cancelTimeWarning = `Thời điểm hủy phải trước giờ khởi hành (${formatDateTime(detail.ngay_xuat_phat)}).`;
    }
  }

  return (
    <SlideOverDrawer
      open={open}
      onClose={onClose}
      widthClass="max-w-2xl"
      title={detail ? `Đơn hàng ${detail.ma_don_hang}` : orderId ? `Đơn hàng ${orderId}` : 'Chi tiết đơn hàng'}
      subtitle={
        detail
          ? `${detail.ten_tour} · Đặt lúc ${formatDateTime(detail.ngay_dat)}`
          : 'Đang tải thông tin đơn hàng...'
      }
      footer={
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Button
              variant="primary"
              size="sm"
              shape="rounded"
              loading={pdfLoading}
              disabled={!detail}
              onClick={handleDownloadPdf}
              leftIcon={<Download className="h-4 w-4" strokeWidth={1.75} />}
            >
              Xuất phiếu xác nhận (PDF)
            </Button>
            {detail && (
              <Link
                to={`/admin/confirmations?order=${encodeURIComponent(detail.ma_don_hang)}`}
                className="inline-flex h-9 items-center gap-1.5 rounded-[10px] border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors"
              >
                <ExternalLink className="h-3.5 w-3.5" strokeWidth={1.75} />
                Xem trước phiếu
              </Link>
            )}
          </div>
          <Button variant="secondary" size="sm" shape="rounded" onClick={onClose}>
            Đóng
          </Button>
        </div>
      }
    >
      {loading ? (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <SkeletonLine className="h-6 w-32 rounded-full" />
            <SkeletonLine className="h-5 w-40" />
          </div>
          <div className="space-y-3 border-t border-slate-100 pt-5">
            <SkeletonLine className="h-4 w-40" />
            <SkeletonLine className="h-16 w-full" />
          </div>
          <div className="space-y-3 border-t border-slate-100 pt-5">
            <SkeletonLine className="h-4 w-44" />
            <SkeletonLine className="h-24 w-full" />
          </div>
          <div className="space-y-3 border-t border-slate-100 pt-5">
            <SkeletonLine className="h-4 w-36" />
            <SkeletonLine className="h-28 w-full" />
          </div>
        </div>
      ) : loadError ? (
        <div className="rounded-xl border border-red-200 bg-red-50/60 p-5 text-center">
          <AlertCircle className="mx-auto h-6 w-6 text-red-600" strokeWidth={1.75} />
          <p className="mt-2 text-sm font-semibold text-slate-900">{loadError}</p>
          {orderId && (
            <div className="mt-4">
              <Button
                variant="secondary"
                size="sm"
                shape="rounded"
                onClick={() => void loadOrderDetail(orderId)}
                leftIcon={<RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />}
              >
                Thử tải lại
              </Button>
            </div>
          )}
        </div>
      ) : detail && data ? (
        <div className="space-y-6">
          {/* Status & feedback alerts */}
          <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50/70 px-4 py-3">
            <div className="flex items-center gap-2.5">
              <span className="text-xs font-medium text-slate-500">Trạng thái hiện tại:</span>
              <StatusBadge status={detail.ma_trang_thai} label={detail.ten_trang_thai} />
            </div>
            <span className="text-xs font-semibold text-slate-700 tabular-nums">
              Tổng cộng: {formatVnd(detail.tong_tien)}
            </span>
          </div>

          {actionSuccess && (
            <div
              role="status"
              className="flex items-start gap-2.5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-xs text-emerald-900"
            >
              <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600 mt-0.5" strokeWidth={1.75} />
              <p className="leading-relaxed font-medium">{actionSuccess}</p>
            </div>
          )}

          {actionError && (
            <div
              role="alert"
              className="flex items-start gap-2.5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-xs text-red-900"
            >
              <AlertCircle className="h-4 w-4 shrink-0 text-red-600 mt-0.5" strokeWidth={1.75} />
              <p className="leading-relaxed font-medium">{actionError}</p>
            </div>
          )}

          {/* Section: Operations actions */}
          <section className="space-y-3">
            <h3 className="text-sm font-bold text-slate-900">Xử lý đơn hàng</h3>

            {validNext.length > 0 ? (
              <div className="space-y-3">
                <div className="flex flex-wrap items-center gap-2.5">
                  {canPay && (
                    <Button
                      variant="primary"
                      size="sm"
                      shape="rounded"
                      loading={actionLoading}
                      disabled={cancelSubmitting}
                      onClick={() => void handleUpdateStatus('THANHTOAN')}
                      leftIcon={<CheckCircle2 className="h-4 w-4" strokeWidth={1.75} />}
                    >
                      Xác nhận thanh toán
                    </Button>
                  )}

                  {canComplete && (
                    <Button
                      variant="primary"
                      size="sm"
                      shape="rounded"
                      loading={actionLoading}
                      disabled={cancelSubmitting}
                      onClick={() => void handleUpdateStatus('HOANTHANH')}
                      leftIcon={<CheckCircle2 className="h-4 w-4" strokeWidth={1.75} />}
                    >
                      Đánh dấu hoàn thành
                    </Button>
                  )}

                  {canCancel && (
                    <Button
                      variant={cancelPanelOpen ? 'secondary' : 'danger'}
                      size="sm"
                      shape="rounded"
                      disabled={actionLoading || cancelSubmitting}
                      onClick={() => {
                        setActionError(null);
                        setCancelPanelOpen((prev) => !prev);
                      }}
                      leftIcon={<XCircle className="h-4 w-4" strokeWidth={1.75} />}
                    >
                      {cancelPanelOpen ? 'Đóng biểu mẫu hủy' : 'Hủy đơn hàng'}
                    </Button>
                  )}
                </div>

                {/* Cancel order inline panel */}
                {canCancel && cancelPanelOpen && (
                  <div className="rounded-xl border border-red-200 bg-red-50/40 p-4 space-y-4">
                    <div className="flex items-start gap-2.5">
                      <AlertTriangle
                        className="h-4.5 w-4.5 shrink-0 text-red-600 mt-0.5"
                        strokeWidth={1.75}
                      />
                      <div>
                        <p className="text-sm font-bold text-slate-900">
                          Hủy đơn hàng {detail.ma_don_hang}
                        </p>
                        <p className="mt-0.5 text-xs text-slate-600 leading-relaxed">
                          Thao tác sẽ chuyển đơn sang đã hủy, hoàn lại {detail.so_luong_khach} chỗ cho lịch trình và hủy toàn bộ xe trung chuyển liên quan.
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label
                          htmlFor="cancel-date"
                          className="block text-xs font-semibold text-slate-700 mb-1.5"
                        >
                          Ngày hủy đơn
                        </label>
                        <input
                          id="cancel-date"
                          type="date"
                          value={cancelDate}
                          onChange={(e) => setCancelDate(e.target.value)}
                          className="h-10 w-full rounded-[10px] border border-slate-200 bg-white px-3 text-sm text-slate-900 tabular-nums focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                        />
                      </div>
                      <div>
                        <label
                          htmlFor="cancel-time"
                          className="block text-xs font-semibold text-slate-700 mb-1.5"
                        >
                          Giờ hủy đơn
                        </label>
                        <input
                          id="cancel-time"
                          type="time"
                          value={cancelTime}
                          onChange={(e) => setCancelTime(e.target.value)}
                          className="h-10 w-full rounded-[10px] border border-slate-200 bg-white px-3 text-sm text-slate-900 tabular-nums focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                        />
                      </div>
                    </div>

                    {cancelTimeWarning && (
                      <p className="text-xs font-medium text-red-700 bg-red-100/70 border border-red-200 rounded-lg px-3 py-2">
                        {cancelTimeWarning}
                      </p>
                    )}

                    {/* Live Penalty Preview Box */}
                    <div className="rounded-xl border border-slate-200 bg-white p-3.5 space-y-2.5">
                      <div className="flex items-center justify-between gap-2">
                        <p className="text-xs font-bold text-slate-800">
                          Dự tính phí phạt hủy tour
                        </p>
                        {cancelPreview && !previewLoading && (
                          <span className="inline-flex items-center rounded-full border border-amber-200 bg-amber-50 px-2.5 py-0.5 text-xs font-bold text-amber-800 tabular-nums">
                            Mức phạt {cancelPreview.ty_le_phat}%
                          </span>
                        )}
                      </div>

                      {previewLoading ? (
                        <div className="grid grid-cols-2 gap-3 pt-1">
                          <SkeletonLine className="h-10 w-full" />
                          <SkeletonLine className="h-10 w-full" />
                        </div>
                      ) : previewError ? (
                        <p className="text-xs text-red-600">{previewError}</p>
                      ) : cancelPreview ? (
                        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-xs">
                          <div className="flex justify-between gap-2 py-1 border-b border-slate-100">
                            <span className="text-slate-500">Sau thời điểm đặt</span>
                            <span className="font-semibold text-slate-800 tabular-nums">
                              {cancelPreview.so_gio_sau_khi_dat} giờ
                            </span>
                          </div>
                          <div className="flex justify-between gap-2 py-1 border-b border-slate-100">
                            <span className="text-slate-500">Trước khởi hành</span>
                            <span className="font-semibold text-slate-800 tabular-nums">
                              {cancelPreview.so_ngay_truoc_khoi_hanh} ngày
                            </span>
                          </div>
                          <div className="flex justify-between gap-2 py-1">
                            <span className="text-slate-500">Phí phạt giữ lại</span>
                            <span className="font-bold text-red-700 tabular-nums">
                              {formatVnd(cancelPreview.tien_phat)}
                            </span>
                          </div>
                          <div className="flex justify-between gap-2 py-1">
                            <span className="text-slate-500">Hoàn lại khách</span>
                            <span className="font-bold text-emerald-700 tabular-nums">
                              {formatVnd(cancelPreview.tien_hoan)}
                            </span>
                          </div>
                        </div>
                      ) : null}
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <label
                          htmlFor="cancel-reason"
                          className="text-xs font-semibold text-slate-700"
                        >
                          Lý do hủy tour <span className="text-red-600">*</span>
                        </label>
                        <span className="text-[11px] text-slate-400 tabular-nums">
                          {cancelReason.length}/255
                        </span>
                      </div>
                      <textarea
                        id="cancel-reason"
                        rows={2}
                        maxLength={255}
                        value={cancelReason}
                        onChange={(e) => setCancelReason(e.target.value)}
                        placeholder="Nhập lý do hủy từ yêu cầu của khách hàng..."
                        className="w-full rounded-[10px] border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15 resize-none"
                      />
                    </div>

                    <label className="flex items-start gap-2.5 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        checked={agreedPenalty}
                        onChange={(e) => setAgreedPenalty(e.target.checked)}
                        className="mt-0.5 h-4 w-4 rounded border-slate-300 text-[#1D63ED] focus:ring-[#1D63ED]"
                      />
                      <span className="text-xs font-medium text-slate-800 leading-relaxed">
                        Khách hàng đã đồng ý với mức phí phạt hủy tour nêu trên
                      </span>
                    </label>

                    <div className="flex items-center justify-end gap-2 pt-1">
                      <Button
                        variant="secondary"
                        size="sm"
                        shape="rounded"
                        disabled={cancelSubmitting}
                        onClick={() => setCancelPanelOpen(false)}
                      >
                        Giữ lại đơn
                      </Button>
                      <Button
                        variant="danger"
                        size="sm"
                        shape="rounded"
                        loading={cancelSubmitting}
                        disabled={
                          !cancelReason.trim() ||
                          !agreedPenalty ||
                          Boolean(cancelTimeWarning)
                        }
                        onClick={() => void handleConfirmCancel()}
                      >
                        Xác nhận hủy đơn
                      </Button>
                    </div>
                  </div>
                )}
              </div>
            ) : detail.ma_trang_thai === 'HUY' ? (
              <div className="rounded-xl border border-red-200 bg-red-50/50 p-4 space-y-2 text-xs">
                <p className="font-bold text-red-900">Thông tin hủy đơn &amp; hoàn tiền</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 pt-1">
                  <div>
                    <span className="text-slate-500">Thời điểm hủy:</span>{' '}
                    <span className="font-semibold text-slate-900 tabular-nums">
                      {formatDateTime(detail.ngay_huy)}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Mức phạt áp dụng:</span>{' '}
                    <span className="font-semibold text-red-700 tabular-nums">
                      {detail.ty_le_phat ?? 0}% ({formatVnd(detail.tien_phat)})
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Tiền hoàn khách:</span>{' '}
                    <span className="font-semibold text-emerald-700 tabular-nums">
                      {formatVnd(detail.tien_hoan)}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Lý do hủy:</span>{' '}
                    <span className="font-medium text-slate-800">
                      {detail.ly_do_huy?.trim() || 'Không ghi nhận'}
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-xs text-slate-600">
                {detail.ma_trang_thai === 'HOANTHANH'
                  ? 'Chuyến đi đã hoàn thành và không cần thao tác cập nhật thêm.'
                  : 'Đơn hàng đang chờ đến sau thời điểm kết thúc chuyến đi để đánh dấu hoàn thành.'}
              </p>
            )}
          </section>

          {/* Section: Customer Info */}
          <section className="border-t border-slate-200 pt-5 space-y-3">
            <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900">
              <User className="h-4 w-4 text-slate-500" strokeWidth={1.75} />
              Thông tin khách hàng
            </h3>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-xs">
              <div>
                <dt className="text-slate-500">Họ và tên</dt>
                <dd className="mt-0.5 font-semibold text-slate-900">
                  {detail.ho_ten}{' '}
                  <span className="font-normal text-slate-500">({detail.ma_kh})</span>
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Số điện thoại</dt>
                <dd className="mt-0.5 font-semibold text-slate-900 tabular-nums inline-flex items-center gap-1.5">
                  <Phone className="h-3.5 w-3.5 text-slate-400" strokeWidth={1.75} />
                  {data.phone_numbers || 'Chưa cập nhật'}
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Email</dt>
                <dd className="mt-0.5 font-medium text-slate-800 break-all">
                  {detail.email || 'Chưa cập nhật'}
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Địa chỉ liên hệ</dt>
                <dd className="mt-0.5 font-medium text-slate-800">
                  {detail.dia_chi_kh || 'Chưa cập nhật'}
                </dd>
              </div>
            </dl>
          </section>

          {/* Section: Schedule & Accommodation */}
          <section className="border-t border-slate-200 pt-5 space-y-3">
            <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900">
              <Calendar className="h-4 w-4 text-slate-500" strokeWidth={1.75} />
              Lịch trình &amp; Lưu trú
            </h3>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-xs">
              <div className="sm:col-span-2">
                <dt className="text-slate-500">Chương trình tour</dt>
                <dd className="mt-0.5 font-semibold text-slate-900">
                  {detail.ten_tour}{' '}
                  <span className="font-normal text-slate-500">
                    ({detail.ma_tour} · Lịch trình {detail.ma_lich_trinh})
                  </span>
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Tuyến hành trình</dt>
                <dd className="mt-0.5 font-medium text-slate-800">
                  {detail.tinh_xuat_phat ? `${detail.tinh_xuat_phat} → ${detail.tinh_den}` : detail.tinh_den}
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Thời lượng &amp; Số khách</dt>
                <dd className="mt-0.5 font-medium text-slate-800 tabular-nums">
                  {formatDuration(detail.so_dem)} · {detail.so_luong_khach} khách
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Khởi hành</dt>
                <dd className="mt-0.5 font-semibold text-slate-900 tabular-nums">
                  {formatDateTime(detail.ngay_xuat_phat)}
                </dd>
              </div>
              <div>
                <dt className="text-slate-500">Kết thúc</dt>
                <dd className="mt-0.5 font-semibold text-slate-900 tabular-nums">
                  {formatDateTime(detail.ngay_ket_thuc)}
                </dd>
              </div>
              {detail.diem_tap_trung && (
                <div className="sm:col-span-2">
                  <dt className="text-slate-500">Điểm tập trung</dt>
                  <dd className="mt-0.5 font-medium text-slate-800 inline-flex items-start gap-1.5">
                    <MapPin className="h-3.5 w-3.5 shrink-0 text-slate-400 mt-0.5" strokeWidth={1.75} />
                    <span>{detail.diem_tap_trung}</span>
                  </dd>
                </div>
              )}
              <div className="sm:col-span-2 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 py-2.5">
                <div className="flex items-center gap-1.5 text-slate-500 font-medium">
                  <Home className="h-3.5 w-3.5" strokeWidth={1.75} />
                  Cơ sở lưu trú
                </div>
                {detail.ma_nha_nghi ? (
                  <div className="mt-1 space-y-0.5">
                    <p className="font-semibold text-slate-900">
                      {detail.ten_nha_nghi}
                      {detail.loai_hinh_nha_nghi ? ` · ${detail.loai_hinh_nha_nghi}` : ''}
                    </p>
                    <p className="text-slate-600 tabular-nums">
                      {detail.so_phong} phòng × {detail.so_dem} đêm
                      {detail.gia_phong_moi_dem
                        ? ` (${formatVnd(detail.gia_phong_moi_dem)}/đêm)`
                        : ''}
                    </p>
                    {detail.dia_chi_nha_nghi && (
                      <p className="text-slate-500">{detail.dia_chi_nha_nghi}</p>
                    )}
                  </div>
                ) : (
                  <p className="mt-1 text-slate-600">Không sử dụng dịch vụ lưu trú.</p>
                )}
              </div>
            </dl>
          </section>

          {/* Section: Shuttle transfers */}
          <section className="border-t border-slate-200 pt-5 space-y-3">
            <h3 className="flex items-center gap-2 text-sm font-bold text-slate-900">
              <Bus className="h-4 w-4 text-slate-500" strokeWidth={1.75} />
              Xe trung chuyển ({data.shuttles.length})
            </h3>
            {data.shuttles.length === 0 ? (
              <p className="text-xs text-slate-500">
                Không có chuyến xe trung chuyển nào cho đơn hàng này.
              </p>
            ) : (
              <div className="overflow-x-auto rounded-xl border border-slate-200">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
                    <tr>
                      <th className="px-3 py-2 font-semibold">Loại chuyến</th>
                      <th className="px-3 py-2 font-semibold">Giờ đón</th>
                      <th className="px-3 py-2 font-semibold">Điểm đón → Điểm trả</th>
                      <th className="px-3 py-2 font-semibold">Xe / Đơn vị</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 bg-white">
                    {data.shuttles.map((trip, idx) => (
                      <tr key={`${trip.ten_loai_chuyen}-${idx}`}>
                        <td className="px-3 py-2.5 font-semibold text-slate-800 whitespace-nowrap">
                          {trip.ten_loai_chuyen}
                        </td>
                        <td className="px-3 py-2.5 text-slate-700 tabular-nums whitespace-nowrap">
                          {formatDateTime(trip.thoi_gian_don)}
                        </td>
                        <td className="px-3 py-2.5 text-slate-700 min-w-[180px]">
                          <span>{trip.diem_don}</span>
                          <span className="text-slate-400"> → </span>
                          <span>{trip.diem_tra}</span>
                        </td>
                        <td className="px-3 py-2.5 text-slate-600 whitespace-nowrap">
                          <span className="font-medium text-slate-800">{trip.bien_so_xe}</span>
                          <span className="block text-[11px] text-slate-500">
                            {trip.don_vi_van_tai}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>

          {/* Section: Cost Breakdown */}
          <section className="border-t border-slate-200 pt-5 space-y-2.5">
            <h3 className="text-sm font-bold text-slate-900">Chi tiết chi phí</h3>
            <div className="rounded-xl border border-slate-200 bg-slate-50/60 p-4 space-y-2 text-xs">
              <div className="flex items-center justify-between gap-4">
                <span className="text-slate-600">
                  Tiền tour ({detail.so_luong_khach} khách × {formatVnd(detail.gia_co_ban)})
                </span>
                <span className="font-semibold text-slate-900 tabular-nums">
                  {formatVnd(detail.tien_tour)}
                </span>
              </div>
              <div className="flex items-center justify-between gap-4">
                <span className="text-slate-600">
                  Tiền phòng lưu trú
                  {detail.so_phong > 0 && detail.so_dem > 0
                    ? ` (${detail.so_phong} phòng × ${detail.so_dem} đêm)`
                    : ''}
                </span>
                <span className="font-semibold text-slate-900 tabular-nums">
                  {formatVnd(detail.tien_phong)}
                </span>
              </div>
              <div className="flex items-center justify-between gap-4 border-t border-slate-200 pt-2.5 text-sm">
                <span className="font-bold text-slate-900">Tổng giá trị đơn hàng</span>
                <span className="font-bold text-[#1D63ED] tabular-nums">
                  {formatVnd(detail.tong_tien)}
                </span>
              </div>
            </div>
          </section>
        </div>
      ) : null}
    </SlideOverDrawer>
  );
}
