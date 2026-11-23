import { useCallback, useEffect, useState, type FormEvent } from 'react';
import {
  AlertCircle,
  Building2,
  Calendar,
  CheckCircle2,
  Star,
} from 'lucide-react';
import { api, ApiError } from '../../api/client';
import type { CustomerItem, PendingReviewItem } from '../../api/types';
import { Button } from '../../components/common/Button';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { formatDate, formatVnd } from '../../utils/format';

const STAR_LABELS = [
  '',
  'Chưa hài lòng (1 sao)',
  'Tạm được (2 sao)',
  'Hài lòng (3 sao)',
  'Rất hài lòng (4 sao)',
  'Tuyệt vời (5 sao)',
];

export default function ReviewsPage() {
  const [customers, setCustomers] = useState<CustomerItem[]>([]);
  const [customersLoading, setCustomersLoading] = useState(true);
  const [selectedMaKh, setSelectedMaKh] = useState<string>('');

  const [pendingOrders, setPendingOrders] = useState<PendingReviewItem[]>([]);
  const [ordersLoading, setOrdersLoading] = useState(false);
  const [selectedOrderId, setSelectedOrderId] = useState<string>('');

  // Form inputs
  const [diemTour, setDiemTour] = useState<number>(5);
  const [nhanXetTour, setNhanXetTour] = useState<string>('');
  const [coDanhGiaNhaNghi, setCoDanhGiaNhaNghi] = useState<boolean>(true);
  const [diemNhaNghi, setDiemNhaNghi] = useState<number>(5);
  const [nhanXetNhaNghi, setNhanXetNhaNghi] = useState<string>('');

  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Tải danh sách khách hàng
  useEffect(() => {
    let active = true;
    setCustomersLoading(true);
    api
      .getCustomers()
      .then((list) => {
        if (!active) return;
        setCustomers(list);
        if (list.length > 0) {
          setSelectedMaKh(list[0].ma_kh);
        }
      })
      .catch(() => {
        if (active) setCustomers([]);
      })
      .finally(() => {
        if (active) setCustomersLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  // Tải danh sách đơn chờ đánh giá theo khách hàng đã chọn
  const loadPendingOrders = useCallback(async (maKh: string) => {
    if (!maKh) {
      setPendingOrders([]);
      setSelectedOrderId('');
      return;
    }
    setOrdersLoading(true);
    setFormError(null);
    try {
      const list = await api.getPendingReviewOrders(maKh);
      setPendingOrders(list);
      setSelectedOrderId(list.length > 0 ? list[0].ma_don_hang : '');
    } catch {
      setPendingOrders([]);
      setSelectedOrderId('');
    } finally {
      setOrdersLoading(false);
    }
  }, []);

  useEffect(() => {
    if (selectedMaKh) {
      void loadPendingOrders(selectedMaKh);
    }
  }, [selectedMaKh, loadPendingOrders]);

  const activeCustomer = customers.find((c) => c.ma_kh === selectedMaKh);
  const activeOrder = pendingOrders.find((o) => o.ma_don_hang === selectedOrderId);
  const coNhaNghi = Boolean(activeOrder?.ma_nha_nghi);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedOrderId) {
      setFormError('Vui lòng chọn đơn hàng cần gửi đánh giá.');
      return;
    }
    if (diemTour < 1 || diemTour > 5) {
      setFormError('Điểm đánh giá chương trình tour phải từ 1 đến 5 sao.');
      return;
    }
    if (coNhaNghi && coDanhGiaNhaNghi && (diemNhaNghi < 1 || diemNhaNghi > 5)) {
      setFormError('Điểm đánh giá nơi nghỉ phải từ 1 đến 5 sao.');
      return;
    }

    setSubmitting(true);
    setFormError(null);
    setSuccessMessage(null);

    try {
      const res = await api.submitReview({
        ma_don_hang: selectedOrderId,
        diem_tour: diemTour,
        nhan_xet_tour: nhanXetTour.trim() || undefined,
        co_danh_gia_nha_nghi: coNhaNghi ? coDanhGiaNhaNghi : false,
        diem_nha_nghi: coNhaNghi && coDanhGiaNhaNghi ? diemNhaNghi : undefined,
        nhan_xet_nha_nghi:
          coNhaNghi && coDanhGiaNhaNghi && nhanXetNhaNghi.trim()
            ? nhanXetNhaNghi.trim()
            : undefined,
      });

      setSuccessMessage(
        res.message || 'Cảm ơn bạn đã gửi đánh giá. Dữ liệu đã được ghi nhận vào hệ thống.'
      );
      setNhanXetTour('');
      setNhanXetNhaNghi('');
      setDiemTour(5);
      setDiemNhaNghi(5);

      // Tải lại danh sách chuyến đi chờ đánh giá của khách
      await loadPendingOrders(selectedMaKh);
    } catch (err) {
      setFormError(
        err instanceof ApiError ? err.message : 'Không thể gửi đánh giá lúc này. Vui lòng thử lại.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8 space-y-6">
      {/* Tiêu đề trang - Không có mã chức năng, không có emoji */}
      <div>
        <h1 className="text-2xl sm:text-[28px] font-bold text-slate-900 tracking-tight">
          Đánh giá chất lượng tour và nơi nghỉ sau chuyến đi
        </h1>
      </div>

      {successMessage && (
        <div
          role="status"
          className="rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3.5 text-sm font-medium text-emerald-800 flex items-start gap-3"
        >
          <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" strokeWidth={1.75} />
          <div className="flex-1">
            <p className="font-semibold">{successMessage}</p>
          </div>
        </div>
      )}

      {formError && (
        <div
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 px-4 py-3.5 text-sm font-medium text-[#B91C1C] flex items-start gap-3"
        >
          <AlertCircle className="h-5 w-5 text-red-600 shrink-0 mt-0.5" strokeWidth={1.75} />
          <div className="flex-1">
            <p>{formError}</p>
          </div>
        </div>
      )}

      {/* Bước 1: Chọn khách hàng */}
      <section className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-base">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-[#EFF6FF] text-[#1D63ED] text-xs font-bold">
            1
          </span>
          <h2>Chọn khách hàng</h2>
        </div>

        {customersLoading ? (
          <LoadingSkeleton variant="cards" count={1} />
        ) : (
          <div>
            <label htmlFor="customerSelect" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Họ tên và tài khoản khách hàng
            </label>
            <div className="relative">
              <select
                id="customerSelect"
                value={selectedMaKh}
                onChange={(e) => {
                  setSelectedMaKh(e.target.value);
                  setSuccessMessage(null);
                  setFormError(null);
                }}
                className="w-full h-11 rounded-[10px] border border-slate-300 bg-white px-3.5 pr-9 text-sm font-medium text-slate-900 shadow-xs focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              >
                {customers.map((c) => (
                  <option key={c.ma_kh} value={c.ma_kh}>
                    {c.ma_kh} - {c.ho_ten} ({c.email || c.so_dien_thoai || 'Chưa có thông tin'})
                  </option>
                ))}
              </select>
            </div>
          </div>
        )}
      </section>

      {/* Bước 2: Danh sách chuyến đi chờ đánh giá */}
      <section className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-4">
        <div className="flex items-center gap-2 text-slate-900 font-bold text-base">
          <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-[#EFF6FF] text-[#1D63ED] text-xs font-bold">
            2
          </span>
          <h2>Chuyến đi chờ đánh giá</h2>
        </div>

        {ordersLoading ? (
          <LoadingSkeleton variant="table" count={2} />
        ) : pendingOrders.length === 0 ? (
          <div className="rounded-xl border border-sky-100 bg-[#F0F7FF] px-4 py-3.5 text-sm text-slate-700">
            Khách hàng <strong>{activeCustomer?.ho_ten || selectedMaKh}</strong> ({selectedMaKh}) hiện
            không có chuyến đi nào ở trạng thái chờ đánh giá (hoặc tất cả các chuyến hoàn thành đã được
            đánh giá trước đó).
          </div>
        ) : (
          <div className="space-y-3">
            <p className="text-xs font-semibold text-slate-600">
              Chọn chuyến đi cần gửi đánh giá ({pendingOrders.length} chuyến khả dụng):
            </p>
            <div className="grid grid-cols-1 gap-3">
              {pendingOrders.map((order) => {
                const isSelected = order.ma_don_hang === selectedOrderId;
                return (
                  <button
                    key={order.ma_don_hang}
                    type="button"
                    onClick={() => {
                      setSelectedOrderId(order.ma_don_hang);
                      setSuccessMessage(null);
                      setFormError(null);
                    }}
                    className={`w-full text-left rounded-xl border p-4 transition-all cursor-pointer ${
                      isSelected
                        ? 'border-[#1D63ED] bg-[#EFF6FF]/60 shadow-xs ring-1 ring-[#1D63ED]'
                        : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-[#1D63ED] bg-white px-2 py-0.5 rounded border border-blue-200">
                            {order.ma_don_hang}
                          </span>
                          <h3 className="font-bold text-slate-900 text-sm sm:text-base">
                            {order.ten_tour}
                          </h3>
                        </div>
                        <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-600">
                          <span className="inline-flex items-center gap-1">
                            <Calendar className="h-3.5 w-3.5 text-slate-400" />
                            {formatDate(order.ngay_xuat_phat)} - {formatDate(order.ngay_ket_thuc)}
                          </span>
                          {order.ten_nha_nghi && (
                            <span className="inline-flex items-center gap-1">
                              <Building2 className="h-3.5 w-3.5 text-slate-400" />
                              {order.ten_nha_nghi}
                            </span>
                          )}
                        </div>
                      </div>

                      <div className="text-right sm:shrink-0">
                        <span className="text-sm font-bold text-slate-900">
                          {formatVnd(order.tong_tien)}
                        </span>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}
      </section>

      {/* Bước 3: Biểu mẫu điền đánh giá */}
      {activeOrder && (
        <form
          onSubmit={handleSubmit}
          className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-6"
        >
          <div className="flex items-center gap-2 text-slate-900 font-bold text-base">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-[#EFF6FF] text-[#1D63ED] text-xs font-bold">
              3
            </span>
            <h2>Nội dung đánh giá</h2>
          </div>

          {/* Đánh giá Tour */}
          <div className="space-y-3.5 pt-1 border-t border-slate-100">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <label className="block text-sm font-bold text-slate-900">
                  Chương trình tour: {activeOrder.ten_tour}
                </label>
                <p className="text-xs text-slate-500">Mức độ hài lòng chung về lịch trình và dịch vụ tour</p>
              </div>
              <span className="text-xs font-semibold text-[#1D63ED] bg-blue-50 px-2.5 py-1 rounded-md">
                {STAR_LABELS[diemTour]}
              </span>
            </div>

            {/* Bộ chọn sao Tour */}
            <div className="flex items-center gap-2" role="radiogroup" aria-label="Đánh giá sao chương trình tour">
              {[1, 2, 3, 4, 5].map((star) => (
                <button
                  key={star}
                  type="button"
                  onClick={() => setDiemTour(star)}
                  className="p-1 rounded-lg hover:bg-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-[#1D63ED]"
                  aria-label={`${star} sao`}
                  aria-checked={diemTour === star}
                  role="radio"
                >
                  <Star
                    className={`h-7 w-7 transition-colors ${
                      star <= diemTour
                        ? 'fill-[#F59E0B] text-[#F59E0B]'
                        : 'fill-transparent text-slate-300'
                    }`}
                    strokeWidth={1.5}
                  />
                </button>
              ))}
            </div>

            <div>
              <label htmlFor="nhanXetTour" className="block text-xs font-semibold text-slate-700 mb-1">
                Nhận xét về chương trình tour (tùy chọn)
              </label>
              <textarea
                id="nhanXetTour"
                rows={3}
                value={nhanXetTour}
                onChange={(e) => setNhanXetTour(e.target.value)}
                maxLength={500}
                placeholder="Chia sẻ trải nghiệm của bạn về lịch trình, phương tiện di chuyển, thời gian tham quan..."
                className="w-full rounded-[10px] border border-slate-300 p-3 text-sm text-slate-900 shadow-xs focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              />
              <p className="mt-1 text-right text-xs text-slate-400">{nhanXetTour.length}/500 ký tự</p>
            </div>
          </div>

          {/* Đánh giá Nơi nghỉ (nếu đơn có nơi nghỉ) */}
          {coNhaNghi && (
            <div className="space-y-3.5 pt-4 border-t border-slate-100">
              <div className="flex items-center justify-between">
                <div>
                  <label className="block text-sm font-bold text-slate-900">
                    Nơi nghỉ lưu trú: {activeOrder.ten_nha_nghi}
                  </label>
                  <p className="text-xs text-slate-500">Đánh giá chất lượng phòng nghỉ và cơ sở lưu trú</p>
                </div>
                <label className="inline-flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-700">
                  <input
                    type="checkbox"
                    checked={coDanhGiaNhaNghi}
                    onChange={(e) => setCoDanhGiaNhaNghi(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-300 text-[#1D63ED] focus:ring-[#1D63ED]"
                  />
                  Chấm điểm nơi nghỉ
                </label>
              </div>

              {coDanhGiaNhaNghi && (
                <>
                  <div className="flex items-center gap-2" role="radiogroup" aria-label="Đánh giá sao nơi nghỉ">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <button
                        key={star}
                        type="button"
                        onClick={() => setDiemNhaNghi(star)}
                        className="p-1 rounded-lg hover:bg-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-[#1D63ED]"
                        aria-label={`${star} sao cho nơi nghỉ`}
                        aria-checked={diemNhaNghi === star}
                        role="radio"
                      >
                        <Star
                          className={`h-7 w-7 transition-colors ${
                            star <= diemNhaNghi
                              ? 'fill-[#F59E0B] text-[#F59E0B]'
                              : 'fill-transparent text-slate-300'
                          }`}
                          strokeWidth={1.5}
                        />
                      </button>
                    ))}
                    <span className="ml-2 text-xs font-semibold text-slate-600">
                      {STAR_LABELS[diemNhaNghi]}
                    </span>
                  </div>

                  <div>
                    <label htmlFor="nhanXetNhaNghi" className="block text-xs font-semibold text-slate-700 mb-1">
                      Nhận xét về nơi nghỉ lưu trú (tùy chọn)
                    </label>
                    <textarea
                      id="nhanXetNhaNghi"
                      rows={3}
                      value={nhanXetNhaNghi}
                      onChange={(e) => setNhanXetNhaNghi(e.target.value)}
                      maxLength={500}
                      placeholder="Chia sẻ nhận xét về tiện nghi phòng, vệ sinh, thái độ phục vụ..."
                      className="w-full rounded-[10px] border border-slate-300 p-3 text-sm text-slate-900 shadow-xs focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                    />
                    <p className="mt-1 text-right text-xs text-slate-400">{nhanXetNhaNghi.length}/500 ký tự</p>
                  </div>
                </>
              )}
            </div>
          )}

          {/* Nút gửi đánh giá */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-end gap-3">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              loading={submitting}
              className="w-full sm:w-auto px-8"
            >
              Gửi đánh giá chuyến đi
            </Button>
          </div>
        </form>
      )}
    </div>
  );
}
