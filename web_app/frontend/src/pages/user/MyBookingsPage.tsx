import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  Building2,
  Calendar,
  CheckCircle2,
  Compass,
  Download,
  Mail,
  MessageSquareHeart,
  Phone,
  Search,
  Star,
  Ticket,
  UserCheck,
  Users,
} from 'lucide-react';
import { api, ApiError } from '../../api/client';
import type { CustomerItem, CustomerOrderItem, PendingReviewItem } from '../../api/types';
import { useAuth } from '../../context/AuthContext';
import { formatDate, formatDateTime, formatVnd, getInitials } from '../../utils/format';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { StarRating } from '../../components/common/StarRating';
import { StatusBadge } from '../../components/common/StatusBadge';

export default function MyBookingsPage() {
  const { customer, loginCustomer } = useAuth();

  // Inline guest login state
  const [identifier, setIdentifier] = useState('');
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loggingIn, setLoggingIn] = useState(false);
  const [sampleCustomers, setSampleCustomers] = useState<CustomerItem[]>([]);

  // Active customer bookings & reviews
  const [activeTab, setActiveTab] = useState<'orders' | 'reviews'>('orders');
  const [orders, setOrders] = useState<CustomerOrderItem[]>([]);
  const [pendingReviews, setPendingReviews] = useState<PendingReviewItem[]>([]);
  const [loadingData, setLoadingData] = useState(false);
  const [dataError, setDataError] = useState<string | null>(null);
  const [downloadingOrderId, setDownloadingOrderId] = useState<string | null>(null);
  const [actionBanner, setActionBanner] = useState<{ type: 'success' | 'error'; text: string } | null>(
    null
  );

  // Review form state
  const [selectedReviewOrderId, setSelectedReviewOrderId] = useState('');
  const [diemTour, setDiemTour] = useState(5);
  const [nhanXetTour, setNhanXetTour] = useState('');
  const [coDanhGiaNhaNghi, setCoDanhGiaNhaNghi] = useState(false);
  const [diemNhaNghi, setDiemNhaNghi] = useState(5);
  const [nhanXetNhaNghi, setNhanXetNhaNghi] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewError, setReviewError] = useState<string | null>(null);

  useEffect(() => {
    if (customer) return;
    let active = true;
    api
      .getCustomers()
      .then((list) => {
        if (active) setSampleCustomers(list);
      })
      .catch(() => {
        if (active) setSampleCustomers([]);
      });
    return () => {
      active = false;
    };
  }, [customer]);

  const loadCustomerData = useCallback(async (maKh: string) => {
    setLoadingData(true);
    setDataError(null);
    try {
      const [orderList, pendingList] = await Promise.all([
        api.getCustomerOrders(maKh),
        api.getPendingReviews(maKh),
      ]);
      setOrders(orderList);
      setPendingReviews(pendingList);
      setSelectedReviewOrderId((prev) => {
        if (prev && pendingList.some((p) => p.ma_don_hang === prev)) return prev;
        return pendingList[0]?.ma_don_hang ?? '';
      });
    } catch (err) {
      setDataError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tải danh sách đơn hàng của bạn. Vui lòng thử lại.'
      );
    } finally {
      setLoadingData(false);
    }
  }, []);

  useEffect(() => {
    if (customer) {
      loadCustomerData(customer.ma_kh);
    } else {
      setOrders([]);
      setPendingReviews([]);
    }
  }, [customer, loadCustomerData]);

  const selectedPending = useMemo(
    () => pendingReviews.find((p) => p.ma_don_hang === selectedReviewOrderId) ?? null,
    [pendingReviews, selectedReviewOrderId]
  );

  // Reset accommodation review state whenever selected order changes
  useEffect(() => {
    setCoDanhGiaNhaNghi(false);
    setDiemNhaNghi(5);
    setNhanXetNhaNghi('');
    setReviewError(null);
  }, [selectedReviewOrderId]);

  const handleInlineLogin = async (event: FormEvent) => {
    event.preventDefault();
    if (!identifier.trim()) {
      setLoginError('Vui lòng nhập email hoặc số điện thoại đã đăng ký.');
      return;
    }
    setLoggingIn(true);
    setLoginError(null);
    try {
      await loginCustomer(identifier.trim());
      setIdentifier('');
    } catch (err) {
      setLoginError(
        err instanceof ApiError ? err.message : 'Không tìm thấy khách hàng khớp với thông tin này.'
      );
    } finally {
      setLoggingIn(false);
    }
  };

  const handleQuickSampleLogin = async (cust: CustomerItem) => {
    const idVal = cust.email || cust.so_dien_thoai.split(',')[0]?.trim() || '';
    if (!idVal) return;
    setLoggingIn(true);
    setLoginError(null);
    try {
      await loginCustomer(idVal);
    } catch (err) {
      setLoginError(err instanceof ApiError ? err.message : 'Đăng nhập không thành công.');
    } finally {
      setLoggingIn(false);
    }
  };

  const handleDownloadPdf = async (maDon: string) => {
    setDownloadingOrderId(maDon);
    setActionBanner(null);
    try {
      await api.downloadConfirmationPdf(maDon);
    } catch (err) {
      setActionBanner({
        type: 'error',
        text: err instanceof ApiError ? err.message : 'Không thể tải phiếu xác nhận PDF lúc này.',
      });
    } finally {
      setDownloadingOrderId(null);
    }
  };

  const handleJumpToReview = (maDon: string) => {
    setSelectedReviewOrderId(maDon);
    setActiveTab('reviews');
    setActionBanner(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSubmitReview = async (event: FormEvent) => {
    event.preventDefault();
    if (!customer || !selectedPending) return;

    const hasAccommodation = Boolean(selectedPending.ma_nha_nghi);
    const includeAccReview = hasAccommodation && coDanhGiaNhaNghi;

    setSubmittingReview(true);
    setReviewError(null);
    setActionBanner(null);

    try {
      const res = await api.submitReview({
        ma_don_hang: selectedPending.ma_don_hang,
        diem_tour: diemTour,
        nhan_xet_tour: nhanXetTour.trim() || null,
        co_danh_gia_nha_nghi: includeAccReview,
        diem_nha_nghi: includeAccReview ? diemNhaNghi : null,
        nhan_xet_nha_nghi: includeAccReview ? nhanXetNhaNghi.trim() || null : null,
      });

      setActionBanner({
        type: 'success',
        text: res.message || `Cảm ơn bạn đã gửi đánh giá cho đơn ${selectedPending.ma_don_hang}.`,
      });
      setDiemTour(5);
      setNhanXetTour('');
      setCoDanhGiaNhaNghi(false);
      setDiemNhaNghi(5);
      setNhanXetNhaNghi('');

      await loadCustomerData(customer.ma_kh);
    } catch (err) {
      setReviewError(
        err instanceof ApiError ? err.message : 'Không thể gửi đánh giá lúc này. Vui lòng thử lại.'
      );
    } finally {
      setSubmittingReview(false);
    }
  };

  // Guest Login Gate
  if (!customer) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12">
        <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-[var(--shadow-floating)]">
          <div className="text-center">
            <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-[#EFF6FF] text-[#1D63ED] mb-3.5">
              <Ticket className="h-6 w-6" strokeWidth={1.75} />
            </span>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Đơn của tôi &amp; Đánh giá
            </h1>
            <p className="mt-1.5 text-sm text-slate-600 max-w-md mx-auto">
              Đăng nhập bằng email hoặc số điện thoại đã đặt tour để xem danh sách đơn hàng, tải
              phiếu xác nhận PDF và gửi đánh giá chuyến đi.
            </p>
          </div>

          <form onSubmit={handleInlineLogin} className="mt-6 space-y-4">
            <div className="relative">
              <Search
                className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                type="text"
                value={identifier}
                onChange={(e) => {
                  setIdentifier(e.target.value);
                  if (loginError) setLoginError(null);
                }}
                placeholder="Nhập email hoặc số điện thoại của bạn..."
                className="w-full h-11 rounded-[10px] border border-slate-200 bg-slate-50/70 pl-10 pr-4 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              />
            </div>

            {loginError && (
              <p className="text-xs font-medium text-[#B91C1C]" role="alert">
                {loginError}
              </p>
            )}

            <Button
              type="submit"
              variant="primary"
              shape="rounded"
              size="lg"
              loading={loggingIn}
              rightIcon={<ArrowRight className="h-4 w-4" strokeWidth={1.85} />}
              className="w-full"
            >
              Xem đơn hàng của tôi
            </Button>
          </form>

          {sampleCustomers.length > 0 && (
            <div className="mt-7 pt-6 border-t border-slate-100">
              <p className="text-xs font-semibold text-slate-600 mb-3">
                Hoặc chọn nhanh khách hàng để trải nghiệm:
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {sampleCustomers.slice(0, 6).map((cust) => {
                  const primaryPhone = cust.so_dien_thoai.split(',')[0]?.trim();
                  return (
                    <button
                      key={cust.ma_kh}
                      type="button"
                      disabled={loggingIn}
                      onClick={() => handleQuickSampleLogin(cust)}
                      className="flex items-center justify-between gap-2.5 rounded-xl border border-slate-200/80 bg-white px-3 py-2.5 text-left hover:border-[#1D63ED]/50 hover:bg-[#F7FAFF] transition-colors cursor-pointer disabled:opacity-60"
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <span className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-xs font-bold text-[#1D63ED]">
                          {getInitials(cust.ho_ten)}
                        </span>
                        <div className="min-w-0">
                          <p className="text-xs font-bold text-slate-900 truncate">{cust.ho_ten}</p>
                          <p className="text-[11px] text-slate-500 truncate">
                            {cust.email || primaryPhone}
                          </p>
                        </div>
                      </div>
                      <UserCheck className="h-4 w-4 text-slate-400 shrink-0" strokeWidth={1.75} />
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8">
      {/* Customer Header */}
      <div className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] mb-6 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4 min-w-0">
          <span className="inline-flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#1D63ED] text-sm font-bold text-white">
            {getInitials(customer.ho_ten)}
          </span>
          <div className="min-w-0">
            <h1 className="text-xl sm:text-2xl font-bold text-slate-900 truncate">
              {customer.ho_ten}
            </h1>
            <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500">
              <span className="inline-flex items-center gap-1.5">
                <Mail className="h-3.5 w-3.5 text-[#1D63ED]" strokeWidth={1.75} />
                {customer.email}
              </span>
              {customer.so_dien_thoai && (
                <span className="inline-flex items-center gap-1.5 tabular-nums">
                  <Phone className="h-3.5 w-3.5 text-[#1D63ED]" strokeWidth={1.75} />
                  {customer.so_dien_thoai}
                </span>
              )}
            </div>
          </div>
        </div>

        <Link
          to="/explore"
          className="inline-flex items-center justify-center gap-2 rounded-[10px] bg-[#1D63ED] px-4 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2] transition-colors shrink-0"
        >
          <Compass className="h-4 w-4" strokeWidth={1.8} />
          Tra cứu tour mới
        </Link>
      </div>

      {/* Tabs */}
      <div className="flex flex-wrap items-center gap-2 border-b border-slate-200 pb-3 mb-6">
        <button
          type="button"
          onClick={() => setActiveTab('orders')}
          className={[
            'inline-flex items-center gap-2 rounded-[10px] px-4 py-2 text-sm font-semibold transition-colors cursor-pointer',
            activeTab === 'orders'
              ? 'bg-[#1D63ED] text-white'
              : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50',
          ].join(' ')}
        >
          <Ticket className="h-4 w-4" strokeWidth={1.8} />
          <span>Đơn đã đặt</span>
          <span
            className={[
              'inline-flex min-w-5 h-5 px-1.5 items-center justify-center rounded-md text-xs font-bold tabular-nums',
              activeTab === 'orders' ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-700',
            ].join(' ')}
          >
            {orders.length}
          </span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('reviews')}
          className={[
            'inline-flex items-center gap-2 rounded-[10px] px-4 py-2 text-sm font-semibold transition-colors cursor-pointer',
            activeTab === 'reviews'
              ? 'bg-[#1D63ED] text-white'
              : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50',
          ].join(' ')}
        >
          <MessageSquareHeart className="h-4 w-4" strokeWidth={1.8} />
          <span>Đánh giá chuyến đi</span>
          <span
            className={[
              'inline-flex min-w-5 h-5 px-1.5 items-center justify-center rounded-md text-xs font-bold tabular-nums',
              activeTab === 'reviews'
                ? 'bg-white/20 text-white'
                : pendingReviews.length > 0
                  ? 'bg-amber-100 text-amber-800'
                  : 'bg-slate-100 text-slate-700',
            ].join(' ')}
          >
            {pendingReviews.length}
          </span>
        </button>
      </div>

      {actionBanner && (
        <div
          role={actionBanner.type === 'error' ? 'alert' : 'status'}
          className={[
            'mb-6 rounded-2xl border px-4 py-3.5 text-sm font-medium flex items-center gap-2.5',
            actionBanner.type === 'success'
              ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
              : 'border-red-200 bg-red-50 text-[#B91C1C]',
          ].join(' ')}
        >
          <CheckCircle2 className="h-4.5 w-4.5 shrink-0" strokeWidth={1.85} />
          <span>{actionBanner.text}</span>
        </div>
      )}

      {dataError && (
        <div
          role="alert"
          className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-4 py-3.5 text-sm font-medium text-[#B91C1C]"
        >
          {dataError}
        </div>
      )}

      {loadingData ? (
        <LoadingSkeleton variant="list" count={3} />
      ) : activeTab === 'orders' ? (
        orders.length === 0 ? (
          <EmptyState
            title="Bạn chưa có đơn đặt tour nào"
            description="Hãy tra cứu lịch trình đang mở bán để đặt chỗ cho chuyến đi tiếp theo."
            action={
              <Link
                to="/explore"
                className="inline-flex items-center rounded-[10px] bg-[#1D63ED] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2]"
              >
                Tra cứu lịch trình
              </Link>
            }
          />
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <article
                key={order.ma_don_hang}
                className="rounded-xl border border-slate-200 bg-white shadow-[var(--shadow-card)] overflow-hidden"
              >
                <div className="p-5 sm:p-6 space-y-4">
                  <div>
                    <div className="flex flex-wrap items-center justify-between gap-2">
                      <div className="flex items-center gap-2.5">
                        <span className="text-xs font-bold text-[#1D4ED8] bg-[#EFF6FF] border border-[#BFDBFE] px-2.5 py-0.5 rounded-md tabular-nums">
                          {order.ma_don_hang}
                        </span>
                        <span className="text-xs text-slate-500 tabular-nums">
                          Đặt ngày {formatDate(order.ngay_dat)}
                        </span>
                      </div>
                      <StatusBadge
                        status={order.ma_trang_thai}
                        label={order.ten_trang_thai}
                      />
                    </div>

                    <h2 className="mt-2.5 text-base sm:text-lg font-bold text-slate-900 leading-snug">
                      {order.ten_tour}
                    </h2>

                    <div className="mt-3 grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-xs text-slate-600">
                      <span className="inline-flex items-center gap-1.5 tabular-nums">
                        <Calendar className="h-3.5 w-3.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                        {formatDate(order.ngay_xuat_phat)} – {formatDate(order.ngay_ket_thuc)}
                      </span>
                      <span className="inline-flex items-center gap-1.5 tabular-nums">
                        <Users className="h-3.5 w-3.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                        {order.so_luong_khach} khách
                      </span>
                      <span className="inline-flex items-center gap-1.5">
                        <Building2 className="h-3.5 w-3.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                        {order.ten_nha_nghi
                          ? `${order.ten_nha_nghi} (${order.so_phong} phòng)`
                          : 'Không đặt nơi nghỉ'}
                      </span>
                    </div>

                    {/* Cancellation summary if cancelled */}
                    {order.ma_trang_thai === 'HUY' && (
                      <div className="mt-3.5 rounded-xl border border-red-200/80 bg-red-50/75 p-3.5 text-xs text-red-900 space-y-1">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className="font-semibold">
                            Thời điểm hủy: {formatDateTime(order.ngay_huy)}
                          </span>
                          <span className="tabular-nums font-bold">
                            Phí phạt: {formatVnd(order.tien_phat)} ({order.ty_le_phat ?? 0}%) ·
                            Hoàn lại: {formatVnd(order.tien_hoan)}
                          </span>
                        </div>
                        {order.ly_do_huy && <p className="text-red-800">Lý do: {order.ly_do_huy}</p>}
                      </div>
                    )}

                    {/* Submitted review display */}
                    {order.ngay_danh_gia && order.diem_tour !== null && (
                      <div className="mt-3.5 rounded-xl border border-slate-200 bg-[#F8FAFC] p-3.5 text-xs text-slate-700 space-y-1.5">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className="font-semibold text-slate-900 inline-flex items-center gap-2">
                            Đánh giá của bạn:
                            <StarRating value={order.diem_tour} size="sm" showValue />
                          </span>
                          <span className="text-slate-400 tabular-nums">
                            {formatDate(order.ngay_danh_gia)}
                          </span>
                        </div>
                        {order.nhan_xet_tour && <p className="text-slate-600">{order.nhan_xet_tour}</p>}
                        {order.diem_nha_nghi !== null && (
                          <div className="pt-1.5 border-t border-slate-200/60 flex flex-wrap items-center gap-2">
                            <span className="font-semibold text-slate-800">Lưu trú:</span>
                            <StarRating value={order.diem_nha_nghi} size="sm" showValue />
                            {order.nhan_xet_nha_nghi && (
                              <span className="text-slate-600">— {order.nhan_xet_nha_nghi}</span>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Footer actions & price */}
                  <div className="pt-3.5 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
                    <div>
                      <p className="text-[11px] text-slate-500">Tổng chi phí đơn hàng</p>
                      <p className="text-lg font-bold text-[#1D63ED] tabular-nums">
                        {formatVnd(order.tong_tien)}
                      </p>
                    </div>

                    <div className="flex flex-wrap items-center gap-2.5">
                      <Button
                        variant="secondary"
                        size="sm"
                        shape="rounded"
                        loading={downloadingOrderId === order.ma_don_hang}
                        leftIcon={<Download className="h-3.5 w-3.5" strokeWidth={1.8} />}
                        onClick={() => handleDownloadPdf(order.ma_don_hang)}
                      >
                        Tải phiếu xác nhận (PDF)
                      </Button>

                      {order.co_the_danh_gia && (
                        <Button
                          variant="primary"
                          size="sm"
                          shape="rounded"
                          leftIcon={<Star className="h-3.5 w-3.5" strokeWidth={1.85} />}
                          onClick={() => handleJumpToReview(order.ma_don_hang)}
                        >
                          Viết đánh giá
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              </article>
            ))}
          </div>
        )
      ) : pendingReviews.length === 0 ? (
        <EmptyState
          icon={<MessageSquareHeart className="h-7 w-7" strokeWidth={1.75} />}
          title="Không còn chuyến đi nào chờ đánh giá"
          description="Mọi hành trình đã hoàn tất của bạn đều đã được ghi nhận đánh giá."
          action={
            <Link
              to="/explore"
              className="inline-flex items-center rounded-[10px] bg-[#1D63ED] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2]"
            >
              Tra cứu lịch trình mới
            </Link>
          }
        />
      ) : (
        <form
          onSubmit={handleSubmitReview}
          className="rounded-xl border border-slate-200 bg-white p-6 sm:p-7 shadow-[var(--shadow-card)] space-y-6 max-w-3xl"
        >
          <div>
            <label
              htmlFor="review-order-select"
              className="block text-sm font-bold text-slate-900 mb-2"
            >
              Chọn chuyến đi muốn đánh giá
            </label>
            <select
              id="review-order-select"
              value={selectedReviewOrderId}
              onChange={(e) => setSelectedReviewOrderId(e.target.value)}
              className="w-full h-11.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm font-medium text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15 cursor-pointer"
            >
              {pendingReviews.map((item) => (
                <option key={item.ma_don_hang} value={item.ma_don_hang}>
                  {item.ma_don_hang} — {item.ten_tour} ({formatDate(item.ngay_xuat_phat)} –{' '}
                  {formatDate(item.ngay_ket_thuc)})
                </option>
              ))}
            </select>
          </div>

          {selectedPending && (
            <>
              {/* Tour rating block */}
              <div className="pt-5 border-t border-slate-100 space-y-4">
                <div>
                  <h2 className="text-base font-bold text-slate-900">
                    Trải nghiệm chương trình tour
                  </h2>
                  <p className="mt-0.5 text-xs text-slate-500">{selectedPending.ten_tour}</p>
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-700 mb-2">Mức độ hài lòng *</p>
                  <StarRating
                    value={diemTour}
                    interactive
                    size="lg"
                    ariaLabelPrefix="Đánh giá chương trình tour"
                    onChange={setDiemTour}
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label htmlFor="review-tour-comment" className="text-xs font-semibold text-slate-700">
                      Nhận xét về hành trình (tùy chọn)
                    </label>
                    <span className="text-[11px] text-slate-400 tabular-nums">
                      {nhanXetTour.length}/500
                    </span>
                  </div>
                  <textarea
                    id="review-tour-comment"
                    rows={3}
                    maxLength={500}
                    value={nhanXetTour}
                    onChange={(e) => setNhanXetTour(e.target.value)}
                    placeholder="Chia sẻ điều bạn thích nhất về cảnh quan, hướng dẫn viên hoặc lịch trình..."
                    className="w-full rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                  />
                </div>
              </div>

              {/* Accommodation rating block: cleanly shown ONLY when order includes accommodation */}
              {selectedPending.ma_nha_nghi && (
                <div className="pt-5 border-t border-slate-100 space-y-4">
                  <label className="flex items-center justify-between gap-3 cursor-pointer">
                    <div>
                      <h2 className="text-base font-bold text-slate-900">
                        Đánh giá cơ sở lưu trú
                      </h2>
                      <p className="mt-0.5 text-xs text-slate-500">
                        {selectedPending.ten_nha_nghi}
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={coDanhGiaNhaNghi}
                      onChange={(e) => setCoDanhGiaNhaNghi(e.target.checked)}
                      className="h-5 w-5 rounded border-slate-300 text-[#1D63ED] focus:ring-[#1D63ED] cursor-pointer"
                    />
                  </label>

                  {coDanhGiaNhaNghi && (
                    <div className="space-y-4 pt-2">
                      <div>
                        <p className="text-xs font-semibold text-slate-700 mb-2">
                          Chất lượng phòng nghỉ *
                        </p>
                        <StarRating
                          value={diemNhaNghi}
                          interactive
                          size="lg"
                          ariaLabelPrefix="Đánh giá cơ sở lưu trú"
                          onChange={setDiemNhaNghi}
                        />
                      </div>

                      <div>
                        <div className="flex items-center justify-between mb-1.5">
                          <label
                            htmlFor="review-acc-comment"
                            className="text-xs font-semibold text-slate-700"
                          >
                            Nhận xét về nơi lưu trú (tùy chọn)
                          </label>
                          <span className="text-[11px] text-slate-400 tabular-nums">
                            {nhanXetNhaNghi.length}/500
                          </span>
                        </div>
                        <textarea
                          id="review-acc-comment"
                          rows={3}
                          maxLength={500}
                          value={nhanXetNhaNghi}
                          onChange={(e) => setNhanXetNhaNghi(e.target.value)}
                          placeholder="Chia sẻ trải nghiệm về phòng ốc, không gian và thái độ phục vụ..."
                          className="w-full rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 py-2.5 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}

              {reviewError && (
                <p className="text-xs font-medium text-[#B91C1C]" role="alert">
                  {reviewError}
                </p>
              )}

              <div className="pt-2 flex justify-end">
                <Button
                  type="submit"
                  variant="primary"
                  shape="rounded"
                  size="lg"
                  loading={submittingReview}
                  leftIcon={<CheckCircle2 className="h-4.5 w-4.5" strokeWidth={1.85} />}
                >
                  Gửi đánh giá
                </Button>
              </div>
            </>
          )}
        </form>
      )}
    </div>
  );
}
