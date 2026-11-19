import { useCallback, useEffect, useMemo, useState, type FormEvent } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  AlertTriangle,
  ArrowRight,
  Building2,
  Calendar,
  Car,
  CheckCircle2,
  Download,
  LogOut,
  MapPin,
  Minus,
  Plus,
  Sparkles,
  UserCheck,
  UserPlus,
  Users,
} from 'lucide-react';
import { api, ApiError } from '../../api/client';
import type {
  AccommodationItem,
  BookingEstimateResponse,
  CreateBookingResponse,
  CustomerItem,
  OpenScheduleItem,
} from '../../api/types';
import { useAuth } from '../../context/AuthContext';
import {
  formatDateTime,
  formatDuration,
  formatVnd,
  getInitials,
  shiftHoursToDateAndTime,
  toSqlDateTimeInput,
} from '../../utils/format';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { BookingSummaryCard } from '../../components/user/BookingSummaryCard';

interface ConfirmedReceipt {
  response: CreateBookingResponse;
  schedule: OpenScheduleItem;
  soKhach: number;
  accommodation: AccommodationItem | null;
  soPhong: number;
  coXeDon: boolean;
  coXeVe: boolean;
}

export default function BookingPage() {
  const [searchParams] = useSearchParams();
  const initialScheduleParam = searchParams.get('schedule') || '';
  const { customer, setCustomerSession, logoutCustomer } = useAuth();

  // Master data
  const [schedules, setSchedules] = useState<OpenScheduleItem[]>([]);
  const [customers, setCustomers] = useState<CustomerItem[]>([]);
  const [accommodations, setAccommodations] = useState<AccommodationItem[]>([]);
  const [loadingSchedules, setLoadingSchedules] = useState(true);
  const [loadingAccommodations, setLoadingAccommodations] = useState(false);

  // Selected schedule & guest count
  const [selectedScheduleId, setSelectedScheduleId] = useState(initialScheduleParam);
  const [soKhach, setSoKhach] = useState(2);

  // Guest mode (only when not logged in)
  const [guestMode, setGuestMode] = useState<'new' | 'existing'>('new');
  const [selectedExistingMaKh, setSelectedExistingMaKh] = useState('');
  const [hoTen, setHoTen] = useState('');
  const [soDienThoai, setSoDienThoai] = useState('');
  const [email, setEmail] = useState('');
  const [diaChi, setDiaChi] = useState('');
  const [duplicateCustomer, setDuplicateCustomer] = useState<CustomerItem | null>(null);
  const [checkingDuplicate, setCheckingDuplicate] = useState(false);

  // Accommodation
  const [selectedAccId, setSelectedAccId] = useState<string | null>(null);
  const [soPhong, setSoPhong] = useState(0);

  // Shuttle transfers (max 2)
  const [coXeDon, setCoXeDon] = useState(false);
  const [diaChiDon, setDiaChiDon] = useState('');
  const [pickupEditedByUser, setPickupEditedByUser] = useState(false);
  const [gioDonDate, setGioDonDate] = useState('');
  const [gioDonTime, setGioDonTime] = useState('06:00');

  const [coXeVe, setCoXeVe] = useState(false);
  const [gioVeDate, setGioVeDate] = useState('');
  const [gioVeTime, setGioVeTime] = useState('14:00');

  // Estimate & submission
  const [estimate, setEstimate] = useState<BookingEstimateResponse>({
    tien_tour: 0,
    tien_phong: 0,
    tong_tien: 0,
  });
  const [submitting, setSubmitting] = useState(false);
  const [formErrors, setFormErrors] = useState<string[]>([]);
  const [confirmed, setConfirmed] = useState<ConfirmedReceipt | null>(null);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [pdfError, setPdfError] = useState<string | null>(null);

  const loadInitialData = useCallback(async (preferredScheduleId?: string) => {
    setLoadingSchedules(true);
    try {
      const [openList, customerList] = await Promise.all([
        api.getOpenSchedules(),
        api.getCustomers().catch(() => [] as CustomerItem[]),
      ]);
      setSchedules(openList);
      setCustomers(customerList);

      if (customerList.length > 0 && !selectedExistingMaKh) {
        setSelectedExistingMaKh(customerList[0].ma_kh);
      }

      if (openList.length > 0) {
        const match =
          (preferredScheduleId && openList.find((s) => s.ma_lich_trinh === preferredScheduleId)) ||
          openList[0];
        setSelectedScheduleId(match.ma_lich_trinh);
        setSoKhach((prev) => Math.min(Math.max(1, prev), match.so_cho_con_lai));
      }
    } catch {
      setSchedules([]);
    } finally {
      setLoadingSchedules(false);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    loadInitialData(initialScheduleParam);
  }, [initialScheduleParam, loadInitialData]);

  const selectedSchedule = useMemo(
    () => schedules.find((s) => s.ma_lich_trinh === selectedScheduleId) ?? null,
    [schedules, selectedScheduleId]
  );

  const selectedAccommodation = useMemo(
    () => accommodations.find((a) => a.ma_nha_nghi === selectedAccId) ?? null,
    [accommodations, selectedAccId]
  );

  const activeCustomerAddress = useMemo(() => {
    if (customer) return customer.dia_chi;
    if (guestMode === 'existing') {
      return customers.find((c) => c.ma_kh === selectedExistingMaKh)?.dia_chi ?? '';
    }
    return diaChi;
  }, [customer, guestMode, customers, selectedExistingMaKh, diaChi]);

  // Sync pickup address automatically unless user manually edited it
  useEffect(() => {
    if (!pickupEditedByUser) {
      setDiaChiDon(activeCustomerAddress);
    }
  }, [activeCustomerAddress, pickupEditedByUser]);

  // Update accommodations & default shuttle times whenever schedule changes
  useEffect(() => {
    if (!selectedSchedule) return;

    setSoKhach((prev) => Math.min(Math.max(1, prev), selectedSchedule.so_cho_con_lai));

    const pickupDefault = shiftHoursToDateAndTime(selectedSchedule.ngay_xuat_phat, -2);
    setGioDonDate(pickupDefault.date);
    setGioDonTime(pickupDefault.time);

    const returnDefault = shiftHoursToDateAndTime(selectedSchedule.ngay_xuat_phat, 4);
    setGioVeDate(returnDefault.date);
    setGioVeTime(returnDefault.time);

    if (selectedSchedule.so_dem === 0) {
      setAccommodations([]);
      setSelectedAccId(null);
      setSoPhong(0);
      setCoXeVe(false);
      return;
    }

    let active = true;
    setLoadingAccommodations(true);
    setSelectedAccId(null);
    setSoPhong(0);
    setCoXeVe(false);

    api
      .getAccommodations(selectedSchedule.ma_tinh_den)
      .then((list) => {
        if (active) setAccommodations(list);
      })
      .catch(() => {
        if (active) setAccommodations([]);
      })
      .finally(() => {
        if (active) setLoadingAccommodations(false);
      });

    return () => {
      active = false;
    };
  }, [selectedSchedule]);

  // Ensure soPhong <= soKhach when guest count decreases
  useEffect(() => {
    if (selectedAccId && soPhong > soKhach) {
      setSoPhong(soKhach);
    }
  }, [selectedAccId, soKhach, soPhong]);

  // Disable shuttle-to-accommodation if accommodation deselected
  useEffect(() => {
    if (!selectedAccId || (selectedSchedule && selectedSchedule.so_dem === 0)) {
      setCoXeVe(false);
    }
  }, [selectedAccId, selectedSchedule]);

  // Live cost estimate (immediate local calculation + backend sync)
  useEffect(() => {
    if (!selectedSchedule) {
      setEstimate({ tien_tour: 0, tien_phong: 0, tong_tien: 0 });
      return;
    }

    const coNhaNghi = Boolean(selectedAccommodation && selectedSchedule.so_dem > 0);
    const giaPhong = selectedAccommodation?.gia_phong_moi_dem ?? 0;
    const rooms = coNhaNghi ? Math.max(1, Math.min(soPhong || 1, soKhach)) : 0;

    // Immediate zero-flicker preview
    const localTour = soKhach * selectedSchedule.gia_co_ban;
    const localRoom = coNhaNghi ? rooms * giaPhong * selectedSchedule.so_dem : 0;
    setEstimate({
      tien_tour: localTour,
      tien_phong: localRoom,
      tong_tien: localTour + localRoom,
    });

    let active = true;
    api
      .estimateBooking({
        so_khach: soKhach,
        gia_co_ban: selectedSchedule.gia_co_ban,
        so_phong: rooms,
        gia_phong_moi_dem: giaPhong,
        so_dem: selectedSchedule.so_dem,
        co_nha_nghi: coNhaNghi,
      })
      .then((res) => {
        if (active) setEstimate(res);
      })
      .catch(() => {
        // Keep local calculation on transient network issue
      });

    return () => {
      active = false;
    };
  }, [selectedSchedule, selectedAccommodation, soKhach, soPhong]);

  const handleCheckDuplicate = async () => {
    if (customer || guestMode !== 'new') return;
    const cleanEmail = email.trim();
    const cleanPhone = soDienThoai.trim();
    if (!cleanEmail && !cleanPhone) {
      setDuplicateCustomer(null);
      return;
    }
    setCheckingDuplicate(true);
    try {
      const res = await api.checkDuplicateCustomer(cleanEmail, cleanPhone);
      setDuplicateCustomer(res.duplicate ? res.customer : null);
    } catch {
      setDuplicateCustomer(null);
    } finally {
      setCheckingDuplicate(false);
    }
  };

  const handleUseDuplicateCustomer = (dup: CustomerItem) => {
    setGuestMode('existing');
    setSelectedExistingMaKh(dup.ma_kh);
    setDuplicateCustomer(null);
    setPickupEditedByUser(false);
    setFormErrors([]);
  };

  const handleSelectAccommodation = (accId: string | null) => {
    setSelectedAccId(accId);
    if (accId) {
      setSoPhong((prev) => (prev >= 1 ? Math.min(prev, soKhach) : 1));
    } else {
      setSoPhong(0);
      setCoXeVe(false);
    }
  };

  const handleSubmit = async (event?: FormEvent) => {
    event?.preventDefault();
    if (!selectedSchedule) return;

    const clientErrors: string[] = [];
    const isNewGuest = !customer && guestMode === 'new';

    if (isNewGuest) {
      if (!hoTen.trim()) clientErrors.push('Vui lòng nhập họ và tên khách hàng.');
      if (!/^0[0-9]{9}$/.test(soDienThoai.trim())) {
        clientErrors.push('Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.');
      }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email.trim())) {
        clientErrors.push('Vui lòng nhập địa chỉ email hợp lệ.');
      }
      if (!diaChi.trim()) clientErrors.push('Vui lòng nhập địa chỉ liên hệ.');
    } else if (!customer && !selectedExistingMaKh) {
      clientErrors.push('Vui lòng chọn khách hàng trong danh sách.');
    }

    if (coXeDon && !diaChiDon.trim()) {
      clientErrors.push('Vui lòng nhập địa chỉ đón tại nhà.');
    }

    if (clientErrors.length > 0) {
      setFormErrors(clientErrors);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    const isDayTour = selectedSchedule.so_dem === 0;
    const finalAccId = isDayTour ? null : selectedAccId;
    const finalRooms = finalAccId ? Math.max(1, Math.min(soPhong, soKhach)) : 0;
    const finalXeVe = Boolean(!isDayTour && finalAccId && coXeVe);

    setSubmitting(true);
    setFormErrors([]);
    try {
      const result = await api.createBooking({
        la_khach_moi: isNewGuest,
        ma_kh: customer ? customer.ma_kh : isNewGuest ? null : selectedExistingMaKh,
        ho_ten: isNewGuest ? hoTen.trim() : null,
        so_dien_thoai: isNewGuest ? soDienThoai.trim() : null,
        email: isNewGuest ? email.trim() : null,
        dia_chi: isNewGuest ? diaChi.trim() : null,
        ma_lich_trinh: selectedSchedule.ma_lich_trinh,
        so_khach: soKhach,
        ma_nha_nghi: finalAccId,
        so_phong: finalRooms,
        co_xe_don: coXeDon,
        dia_chi_don: coXeDon ? diaChiDon.trim() : null,
        gio_don: coXeDon ? toSqlDateTimeInput(gioDonDate, gioDonTime) : null,
        co_xe_ve: finalXeVe,
        gio_ve_noi_nghi: finalXeVe ? toSqlDateTimeInput(gioVeDate, gioVeTime) : null,
      });

      // Auto sign-in guest (or refresh session) so immediate PDF download & My Bookings work seamlessly
      setCustomerSession(result.customer, result.customer_token);

      setConfirmed({
        response: result,
        schedule: selectedSchedule,
        soKhach,
        accommodation: finalAccId ? selectedAccommodation : null,
        soPhong: finalRooms,
        coXeDon,
        coXeVe: finalXeVe,
      });
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.errors && err.errors.length > 0) {
          setFormErrors(err.errors);
        } else {
          setFormErrors([err.message]);
        }
      } else {
        setFormErrors(['Không thể hoàn tất đặt tour lúc này. Vui lòng thử lại.']);
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } finally {
      setSubmitting(false);
    }
  };

  const handleDownloadPdf = async (maDon: string) => {
    setDownloadingPdf(true);
    setPdfError(null);
    try {
      await api.downloadConfirmationPdf(maDon);
    } catch (err) {
      setPdfError(
        err instanceof ApiError ? err.message : 'Không thể tải phiếu xác nhận PDF lúc này.'
      );
    } finally {
      setDownloadingPdf(false);
    }
  };

  const handleBookAnother = () => {
    setConfirmed(null);
    setFormErrors([]);
    setPdfError(null);
    setSelectedAccId(null);
    setSoPhong(0);
    setCoXeDon(false);
    setCoXeVe(false);
    setPickupEditedByUser(false);
    loadInitialData();
  };

  if (confirmed) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-14">
        <div className="rounded-[28px] border border-slate-200/85 bg-white p-6 sm:p-10 shadow-[var(--shadow-floating)]">
          <div className="flex flex-col items-center text-center">
            <span className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-emerald-50 text-emerald-600 mb-4">
              <CheckCircle2 className="h-9 w-9" strokeWidth={1.75} />
            </span>
            <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-950">
              Đặt tour thành công
            </h1>
            <p className="mt-2 text-sm sm:text-base text-slate-600 max-w-lg">
              Đơn hàng của bạn đã được ghi nhận trên hệ thống. Bạn có thể tải phiếu xác nhận khổ A4
              ngay bây giờ hoặc theo dõi chi tiết trong mục Đơn của tôi.
            </p>
          </div>

          <div className="mt-7 rounded-2xl border border-slate-200/80 bg-[#F7FAFF] p-5 space-y-3 text-sm">
            <div className="flex items-center justify-between gap-4 pb-3 border-b border-slate-200/70">
              <span className="text-slate-500">Mã đơn hàng</span>
              <span className="text-base font-bold text-[#1D63ED] tabular-nums">
                {confirmed.response.ma_don_hang}
              </span>
            </div>
            <div className="flex items-start justify-between gap-4">
              <span className="text-slate-500">Khách hàng</span>
              <span className="font-semibold text-slate-900 text-right">
                {confirmed.response.customer.ho_ten} ({confirmed.response.customer.email})
              </span>
            </div>
            <div className="flex items-start justify-between gap-4">
              <span className="text-slate-500">Hành trình</span>
              <span className="font-semibold text-slate-900 text-right">
                {confirmed.schedule.ten_tour}
              </span>
            </div>
            <div className="flex items-center justify-between gap-4">
              <span className="text-slate-500">Thời gian khởi hành</span>
              <span className="font-medium text-slate-800 tabular-nums">
                {formatDateTime(confirmed.schedule.ngay_xuat_phat)}
              </span>
            </div>
            <div className="flex items-center justify-between gap-4">
              <span className="text-slate-500">Số lượng khách</span>
              <span className="font-medium text-slate-800 tabular-nums">
                {confirmed.soKhach} khách
              </span>
            </div>
            <div className="flex items-start justify-between gap-4">
              <span className="text-slate-500">Lưu trú</span>
              <span className="font-medium text-slate-800 text-right">
                {confirmed.accommodation
                  ? `${confirmed.accommodation.ten_nha_nghi} (${confirmed.soPhong} phòng)`
                  : confirmed.schedule.so_dem === 0
                    ? 'Chuyến đi trong ngày'
                    : 'Không đặt nơi nghỉ'}
              </span>
            </div>
            <div className="flex items-baseline justify-between gap-4 pt-3 border-t border-slate-200/70">
              <span className="font-bold text-slate-900">Tổng chi phí</span>
              <span className="text-xl font-bold text-[#1D63ED] tabular-nums">
                {formatVnd(confirmed.response.tong_tien)}
              </span>
            </div>
          </div>

          {pdfError && (
            <p className="mt-4 text-center text-xs font-medium text-[#B91C1C]" role="alert">
              {pdfError}
            </p>
          )}

          <div className="mt-7 flex flex-col sm:flex-row items-center justify-center gap-3">
            <Button
              variant="primary"
              shape="pill"
              size="lg"
              loading={downloadingPdf}
              leftIcon={<Download className="h-4.5 w-4.5" strokeWidth={1.85} />}
              onClick={() => handleDownloadPdf(confirmed.response.ma_don_hang)}
              className="w-full sm:w-auto"
            >
              Tải phiếu xác nhận (PDF)
            </Button>
            <Link
              to="/my-bookings"
              className="w-full sm:w-auto inline-flex items-center justify-center rounded-full border border-slate-200 bg-white px-6 h-12 text-sm font-semibold text-slate-800 hover:bg-slate-50 transition-colors"
            >
              Xem đơn của tôi
            </Link>
            <Button
              variant="ghost"
              shape="pill"
              size="md"
              onClick={handleBookAnother}
              className="w-full sm:w-auto"
            >
              Đặt thêm tour khác
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-10">
      <div className="mb-7">
        <h1 className="font-display text-3xl sm:text-4xl font-bold text-slate-950 tracking-tight">
          Đặt tour trực tuyến
        </h1>
        <p className="mt-2 text-sm sm:text-base text-slate-600 max-w-2xl">
          Chọn lịch trình khởi hành, tùy chỉnh lưu trú và xe trung chuyển — chi phí được tính minh
          bạch ngay trước khi xác nhận.
        </p>
      </div>

      {formErrors.length > 0 && (
        <div
          role="alert"
          className="mb-6 rounded-2xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-[#B91C1C]"
        >
          <p className="font-bold flex items-center gap-2">
            <AlertTriangle className="h-4.5 w-4.5 shrink-0" strokeWidth={1.85} />
            Vui lòng kiểm tra lại thông tin đặt tour
          </p>
          <ul className="mt-2 list-disc list-inside space-y-1">
            {formErrors.map((msg, idx) => (
              <li key={idx}>{msg}</li>
            ))}
          </ul>
        </div>
      )}

      {loadingSchedules ? (
        <LoadingSkeleton variant="list" count={3} />
      ) : schedules.length === 0 ? (
        <EmptyState
          title="Hiện không còn lịch trình mở bán"
          description="Tất cả các chuyến đi sắp tới đã kín chỗ. Vui lòng quay lại trang khám phá để theo dõi lịch khởi hành mới."
          action={
            <Link
              to="/explore"
              className="inline-flex items-center rounded-full bg-[#1D63ED] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2]"
            >
              Quay lại Khám phá tour
            </Link>
          }
        />
      ) : (
        <form onSubmit={handleSubmit} className="grid grid-cols-1 lg:grid-cols-12 gap-7 items-start">
          {/* Left Form Column (65%) */}
          <div className="lg:col-span-8 space-y-6">
            {/* Section 1: Schedule & Guest Count */}
            <section className="rounded-[24px] border border-slate-200/85 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-5">
              <div className="flex items-center gap-2.5">
                <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
                  <Calendar className="h-4 w-4" strokeWidth={1.85} />
                </span>
                <h2 className="text-lg font-bold text-slate-900">Lịch trình &amp; Số lượng khách</h2>
              </div>

              <div>
                <label
                  htmlFor="booking-schedule-select"
                  className="block text-xs font-semibold text-slate-700 mb-1.5"
                >
                  Chọn lịch trình khởi hành
                </label>
                <select
                  id="booking-schedule-select"
                  value={selectedScheduleId}
                  onChange={(e) => {
                    setSelectedScheduleId(e.target.value);
                    setFormErrors([]);
                  }}
                  className="w-full h-11.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm font-medium text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15 cursor-pointer"
                >
                  {schedules.map((s) => (
                    <option key={s.ma_lich_trinh} value={s.ma_lich_trinh}>
                      {s.ten_tour} · {formatDateTime(s.ngay_xuat_phat)} · {formatVnd(s.gia_co_ban)} (Còn{' '}
                      {s.so_cho_con_lai} chỗ)
                    </option>
                  ))}
                </select>
              </div>

              {selectedSchedule && (
                <div className="rounded-2xl bg-[#F7FAFF] border border-slate-200/70 p-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
                  <div className="flex items-start gap-2.5">
                    <MapPin className="h-4 w-4 text-[#1D63ED] mt-0.5 shrink-0" strokeWidth={1.75} />
                    <div>
                      <p className="text-xs text-slate-500">Tuyến &amp; điểm tập trung</p>
                      <p className="font-semibold text-slate-900 inline-flex flex-wrap items-center gap-1">
                        <span>{selectedSchedule.noi_di}</span>
                        <ArrowRight className="h-3.5 w-3.5 text-slate-400 shrink-0" strokeWidth={2} />
                        <span>{selectedSchedule.ten_tinh_den}</span>
                      </p>
                      <p className="text-xs text-slate-600 mt-0.5">{selectedSchedule.diem_tap_trung}</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-2.5">
                    <Calendar className="h-4 w-4 text-[#1D63ED] mt-0.5 shrink-0" strokeWidth={1.75} />
                    <div>
                      <p className="text-xs text-slate-500">Thời gian chuyến đi</p>
                      <p className="font-semibold text-slate-900 tabular-nums">
                        {formatDateTime(selectedSchedule.ngay_xuat_phat)} –{' '}
                        {formatDateTime(selectedSchedule.ngay_ket_thuc)}
                      </p>
                      <p className="text-xs text-slate-600 mt-0.5">
                        {formatDuration(selectedSchedule.so_dem)} · Còn{' '}
                        <span className="font-semibold text-[#1D63ED] tabular-nums">
                          {selectedSchedule.so_cho_con_lai} chỗ trống
                        </span>
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {selectedSchedule && (
                <div className="flex flex-wrap items-center justify-between gap-4 pt-2">
                  <div>
                    <p className="text-sm font-semibold text-slate-900">Số lượng khách tham gia</p>
                    <p className="text-xs text-slate-500 tabular-nums">
                      Tối đa {selectedSchedule.so_cho_con_lai} khách cho lịch khởi hành này
                    </p>
                  </div>
                  <div className="inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white px-2 py-1.5">
                    <button
                      type="button"
                      disabled={soKhach <= 1}
                      onClick={() => setSoKhach((prev) => Math.max(1, prev - 1))}
                      aria-label="Giảm số lượng khách"
                      className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200 disabled:opacity-40 cursor-pointer"
                    >
                      <Minus className="h-4 w-4" strokeWidth={1.9} />
                    </button>
                    <span className="min-w-10 text-center text-base font-bold text-slate-900 tabular-nums">
                      {soKhach}
                    </span>
                    <button
                      type="button"
                      disabled={soKhach >= selectedSchedule.so_cho_con_lai}
                      onClick={() =>
                        setSoKhach((prev) => Math.min(selectedSchedule.so_cho_con_lai, prev + 1))
                      }
                      aria-label="Tăng số lượng khách"
                      className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED] hover:bg-[#DBEAFE] disabled:opacity-40 cursor-pointer"
                    >
                      <Plus className="h-4 w-4" strokeWidth={1.9} />
                    </button>
                  </div>
                </div>
              )}
            </section>

            {/* Section 2: Customer Information */}
            <section className="rounded-[24px] border border-slate-200/85 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
                    <Users className="h-4 w-4" strokeWidth={1.85} />
                  </span>
                  <h2 className="text-lg font-bold text-slate-900">Thông tin khách hàng</h2>
                </div>

                {customer && (
                  <button
                    type="button"
                    onClick={() => {
                      logoutCustomer();
                      setPickupEditedByUser(false);
                    }}
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-[#1D63ED] transition-colors cursor-pointer"
                  >
                    <LogOut className="h-3.5 w-3.5" strokeWidth={1.75} />
                    Đăng xuất để đặt cho khách khác
                  </button>
                )}
              </div>

              {customer ? (
                <div className="rounded-2xl border border-[#BFDBFE] bg-[#F7FAFF] p-4 flex items-start gap-3.5">
                  <span className="inline-flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#1D63ED] text-sm font-bold text-white">
                    {getInitials(customer.ho_ten)}
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-base font-bold text-slate-900">{customer.ho_ten}</p>
                      <span className="rounded-full bg-[#DBEAFE] px-2.5 py-0.5 text-[11px] font-semibold text-[#1D4ED8]">
                        Tài khoản đang đăng nhập
                      </span>
                    </div>
                    <div className="mt-1.5 grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs text-slate-600">
                      <span>Email: {customer.email}</span>
                      <span className="tabular-nums">
                        Điện thoại: {customer.so_dien_thoai || 'Chưa cập nhật'}
                      </span>
                      <span className="sm:col-span-2">Địa chỉ: {customer.dia_chi}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <>
                  <div className="inline-flex rounded-full border border-slate-200 bg-slate-50 p-1">
                    <button
                      type="button"
                      onClick={() => {
                        setGuestMode('new');
                        setPickupEditedByUser(false);
                      }}
                      className={[
                        'inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-xs font-semibold transition-colors cursor-pointer',
                        guestMode === 'new'
                          ? 'bg-[#1D63ED] text-white shadow-xs'
                          : 'text-slate-600 hover:text-slate-900',
                      ].join(' ')}
                    >
                      <UserPlus className="h-3.5 w-3.5" strokeWidth={1.8} />
                      Khách hàng mới
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setGuestMode('existing');
                        setDuplicateCustomer(null);
                        setPickupEditedByUser(false);
                      }}
                      className={[
                        'inline-flex items-center gap-1.5 rounded-full px-4 py-2 text-xs font-semibold transition-colors cursor-pointer',
                        guestMode === 'existing'
                          ? 'bg-[#1D63ED] text-white shadow-xs'
                          : 'text-slate-600 hover:text-slate-900',
                      ].join(' ')}
                    >
                      <UserCheck className="h-3.5 w-3.5" strokeWidth={1.8} />
                      Khách hàng có sẵn
                    </button>
                  </div>

                  {guestMode === 'new' ? (
                    <div className="space-y-4">
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                          <label htmlFor="guest-name" className="block text-xs font-semibold text-slate-700 mb-1.5">
                            Họ và tên *
                          </label>
                          <input
                            id="guest-name"
                            type="text"
                            value={hoTen}
                            onChange={(e) => setHoTen(e.target.value)}
                            placeholder="Nguyễn Minh Anh"
                            className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                          />
                        </div>

                        <div>
                          <label htmlFor="guest-phone" className="block text-xs font-semibold text-slate-700 mb-1.5">
                            Số điện thoại (10 chữ số) *
                          </label>
                          <input
                            id="guest-phone"
                            type="tel"
                            value={soDienThoai}
                            onChange={(e) => setSoDienThoai(e.target.value)}
                            onBlur={handleCheckDuplicate}
                            placeholder="0912345678"
                            className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                          />
                        </div>

                        <div>
                          <label htmlFor="guest-email" className="block text-xs font-semibold text-slate-700 mb-1.5">
                            Email *
                          </label>
                          <input
                            id="guest-email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            onBlur={handleCheckDuplicate}
                            placeholder="minhanh@gmail.com"
                            className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                          />
                        </div>

                        <div>
                          <label htmlFor="guest-address" className="block text-xs font-semibold text-slate-700 mb-1.5">
                            Địa chỉ liên hệ *
                          </label>
                          <input
                            id="guest-address"
                            type="text"
                            value={diaChi}
                            onChange={(e) => setDiaChi(e.target.value)}
                            placeholder="Số 25 Láng Hạ, Đống Đa, Hà Nội"
                            className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                          />
                        </div>
                      </div>

                      {checkingDuplicate && (
                        <p className="text-xs text-slate-500">Đang kiểm tra thông tin khách hàng...</p>
                      )}

                      {duplicateCustomer && (
                        <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                          <div className="text-xs text-amber-950">
                            <p className="font-bold">
                              Email hoặc số điện thoại này đã thuộc về khách hàng {duplicateCustomer.ho_ten}
                            </p>
                            <p className="mt-0.5 text-amber-800">
                              {duplicateCustomer.email} · {duplicateCustomer.so_dien_thoai}
                            </p>
                          </div>
                          <Button
                            variant="secondary"
                            size="sm"
                            shape="pill"
                            onClick={() => handleUseDuplicateCustomer(duplicateCustomer)}
                            className="shrink-0"
                          >
                            Dùng khách hàng này
                          </Button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <label htmlFor="existing-customer-select" className="block text-xs font-semibold text-slate-700">
                        Chọn khách hàng đã đăng ký
                      </label>
                      <select
                        id="existing-customer-select"
                        value={selectedExistingMaKh}
                        onChange={(e) => {
                          setSelectedExistingMaKh(e.target.value);
                          setPickupEditedByUser(false);
                        }}
                        className="w-full h-11 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm font-medium text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15 cursor-pointer"
                      >
                        {customers.map((c) => (
                          <option key={c.ma_kh} value={c.ma_kh}>
                            {c.ho_ten} — {c.email} ({c.so_dien_thoai})
                          </option>
                        ))}
                      </select>

                      {(() => {
                        const picked = customers.find((c) => c.ma_kh === selectedExistingMaKh);
                        if (!picked) return null;
                        return (
                          <div className="rounded-xl bg-slate-50 border border-slate-200/70 px-4 py-3 text-xs text-slate-600 space-y-1">
                            <p>
                              <span className="font-semibold text-slate-800">Địa chỉ:</span> {picked.dia_chi}
                            </p>
                            <p className="tabular-nums">
                              <span className="font-semibold text-slate-800">Số điện thoại:</span>{' '}
                              {picked.so_dien_thoai}
                            </p>
                          </div>
                        );
                      })()}
                    </div>
                  )}
                </>
              )}
            </section>

            {/* Section 3: Accommodation */}
            <section className="rounded-[24px] border border-slate-200/85 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-4">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
                    <Building2 className="h-4 w-4" strokeWidth={1.85} />
                  </span>
                  <h2 className="text-lg font-bold text-slate-900">Dịch vụ lưu trú</h2>
                </div>
                {selectedSchedule && selectedSchedule.so_dem > 0 && (
                  <span className="text-xs font-medium text-slate-500">
                    Khu vực {selectedSchedule.ten_tinh_den} · {selectedSchedule.so_dem} đêm
                  </span>
                )}
              </div>

              {selectedSchedule && selectedSchedule.so_dem === 0 ? (
                <div className="rounded-2xl bg-[#F7FAFF] border border-slate-200/70 px-4 py-4 flex items-center gap-3 text-sm text-slate-700">
                  <Sparkles className="h-4.5 w-4.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                  <span>Chuyến đi trong ngày không bao gồm lưu trú qua đêm.</span>
                </div>
              ) : loadingAccommodations ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="h-24 rounded-2xl bg-slate-100 animate-pulse" />
                  ))}
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => handleSelectAccommodation(null)}
                      className={[
                        'rounded-2xl border p-4 text-left transition-all cursor-pointer',
                        selectedAccId === null
                          ? 'border-[#1D63ED] bg-[#EFF5FF]/70 ring-2 ring-[#1D63ED]/15'
                          : 'border-slate-200 bg-white hover:border-slate-300',
                      ].join(' ')}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <span className="text-sm font-bold text-slate-900">Không đặt nơi nghỉ</span>
                        <span className="text-xs font-bold text-slate-600 tabular-nums">0 đ</span>
                      </div>
                      <p className="mt-1 text-xs text-slate-500">
                        Tự túc phòng nghỉ trong suốt hành trình
                      </p>
                    </button>

                    {accommodations.map((acc) => {
                      const active = selectedAccId === acc.ma_nha_nghi;
                      return (
                        <button
                          key={acc.ma_nha_nghi}
                          type="button"
                          onClick={() => handleSelectAccommodation(acc.ma_nha_nghi)}
                          className={[
                            'rounded-2xl border p-4 text-left transition-all cursor-pointer',
                            active
                              ? 'border-[#1D63ED] bg-[#EFF5FF]/70 ring-2 ring-[#1D63ED]/15'
                              : 'border-slate-200 bg-white hover:border-slate-300',
                          ].join(' ')}
                        >
                          <div className="flex items-start justify-between gap-2">
                            <span className="text-sm font-bold text-slate-900 leading-snug">
                              {acc.ten_nha_nghi}
                            </span>
                            <span className="shrink-0 rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-semibold text-slate-700">
                              {acc.loai_hinh}
                            </span>
                          </div>
                          <p className="mt-1 text-xs text-slate-500 line-clamp-1">{acc.dia_chi}</p>
                          <p className="mt-2 text-xs font-bold text-[#1D63ED] tabular-nums">
                            {formatVnd(acc.gia_phong_moi_dem)} / phòng / đêm
                          </p>
                        </button>
                      );
                    })}
                  </div>

                  {selectedAccommodation && (
                    <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-4">
                      <div>
                        <p className="text-sm font-semibold text-slate-900">Số lượng phòng đặt</p>
                        <p className="text-xs text-slate-500 tabular-nums">
                          Từ 1 đến tối đa {soKhach} phòng (tương ứng số khách)
                        </p>
                      </div>
                      <div className="inline-flex items-center gap-3 rounded-full border border-slate-200 bg-white px-2 py-1.5">
                        <button
                          type="button"
                          disabled={soPhong <= 1}
                          onClick={() => setSoPhong((prev) => Math.max(1, prev - 1))}
                          aria-label="Giảm số phòng"
                          className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-slate-100 text-slate-700 hover:bg-slate-200 disabled:opacity-40 cursor-pointer"
                        >
                          <Minus className="h-4 w-4" strokeWidth={1.9} />
                        </button>
                        <span className="min-w-10 text-center text-base font-bold text-slate-900 tabular-nums">
                          {soPhong}
                        </span>
                        <button
                          type="button"
                          disabled={soPhong >= soKhach}
                          onClick={() => setSoPhong((prev) => Math.min(soKhach, prev + 1))}
                          aria-label="Tăng số phòng"
                          className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED] hover:bg-[#DBEAFE] disabled:opacity-40 cursor-pointer"
                        >
                          <Plus className="h-4 w-4" strokeWidth={1.9} />
                        </button>
                      </div>
                    </div>
                  )}
                </>
              )}
            </section>

            {/* Section 4: Shuttle Transfers (Max 2) */}
            <section className="rounded-[24px] border border-slate-200/85 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] space-y-4">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2.5">
                  <span className="inline-flex h-8 w-8 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
                    <Car className="h-4 w-4" strokeWidth={1.85} />
                  </span>
                  <h2 className="text-lg font-bold text-slate-900">Xe trung chuyển</h2>
                </div>
                <span className="text-xs font-medium text-slate-500">Tối đa 2 chuyến đi kèm</span>
              </div>

              {/* Shuttle 1: Pickup at home */}
              <div className="rounded-2xl border border-slate-200/80 p-4 space-y-4">
                <label className="flex items-center justify-between gap-3 cursor-pointer">
                  <div>
                    <p className="text-sm font-bold text-slate-900">Xe đón tại nhà</p>
                    <p className="text-xs text-slate-500">
                      Đưa đón từ địa chỉ của bạn tới điểm tập trung trước giờ khởi hành
                    </p>
                  </div>
                  <input
                    type="checkbox"
                    checked={coXeDon}
                    onChange={(e) => setCoXeDon(e.target.checked)}
                    className="h-5 w-5 rounded border-slate-300 text-[#1D63ED] focus:ring-[#1D63ED] cursor-pointer"
                  />
                </label>

                {coXeDon && (
                  <div className="pt-3 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                    <div className="sm:col-span-2">
                      <label htmlFor="shuttle-pickup-address" className="block text-xs font-semibold text-slate-700 mb-1.5">
                        Địa chỉ đón *
                      </label>
                      <input
                        id="shuttle-pickup-address"
                        type="text"
                        value={diaChiDon}
                        onChange={(e) => {
                          setDiaChiDon(e.target.value);
                          setPickupEditedByUser(true);
                        }}
                        placeholder="Nhập số nhà, đường, quận/huyện..."
                        className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3.5 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                      />
                    </div>
                    <div>
                      <label htmlFor="shuttle-pickup-date" className="block text-xs font-semibold text-slate-700 mb-1.5">
                        Ngày đón
                      </label>
                      <input
                        id="shuttle-pickup-date"
                        type="date"
                        value={gioDonDate}
                        onChange={(e) => setGioDonDate(e.target.value)}
                        className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                      />
                    </div>
                    <div>
                      <label htmlFor="shuttle-pickup-time" className="block text-xs font-semibold text-slate-700 mb-1.5">
                        Giờ đón
                      </label>
                      <input
                        id="shuttle-pickup-time"
                        type="time"
                        value={gioDonTime}
                        onChange={(e) => setGioDonTime(e.target.value)}
                        className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                      />
                    </div>
                  </div>
                )}
              </div>

              {/* Shuttle 2: Return to accommodation (only when multi-day + accommodation selected) */}
              {selectedSchedule && selectedSchedule.so_dem > 0 && selectedAccommodation && (
                <div className="rounded-2xl border border-slate-200/80 p-4 space-y-4">
                  <label className="flex items-center justify-between gap-3 cursor-pointer">
                    <div>
                      <p className="text-sm font-bold text-slate-900">Xe về nơi nghỉ</p>
                      <p className="text-xs text-slate-500">
                        Đưa khách về {selectedAccommodation.ten_nha_nghi} trong khung thời gian tour
                      </p>
                    </div>
                    <input
                      type="checkbox"
                      checked={coXeVe}
                      onChange={(e) => setCoXeVe(e.target.checked)}
                      className="h-5 w-5 rounded border-slate-300 text-[#1D63ED] focus:ring-[#1D63ED] cursor-pointer"
                    />
                  </label>

                  {coXeVe && (
                    <div className="pt-3 border-t border-slate-100 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                      <div>
                        <label htmlFor="shuttle-return-date" className="block text-xs font-semibold text-slate-700 mb-1.5">
                          Ngày đón về nơi nghỉ
                        </label>
                        <input
                          id="shuttle-return-date"
                          type="date"
                          value={gioVeDate}
                          onChange={(e) => setGioVeDate(e.target.value)}
                          className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                        />
                      </div>
                      <div>
                        <label htmlFor="shuttle-return-time" className="block text-xs font-semibold text-slate-700 mb-1.5">
                          Giờ đón về nơi nghỉ
                        </label>
                        <input
                          id="shuttle-return-time"
                          type="time"
                          value={gioVeTime}
                          onChange={(e) => setGioVeTime(e.target.value)}
                          className="w-full h-10.5 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15"
                        />
                      </div>
                    </div>
                  )}
                </div>
              )}
            </section>
          </div>

          {/* Right Sticky Cost Estimator Column (35%) */}
          <div className="lg:col-span-4">
            <BookingSummaryCard
              schedule={selectedSchedule}
              soKhach={soKhach}
              accommodation={selectedSchedule?.so_dem === 0 ? null : selectedAccommodation}
              soPhong={selectedSchedule?.so_dem === 0 ? 0 : soPhong}
              coXeDon={coXeDon}
              coXeVe={Boolean(selectedSchedule && selectedSchedule.so_dem > 0 && selectedAccommodation && coXeVe)}
              estimate={estimate}
              submitting={submitting}
            />
          </div>
        </form>
      )}
    </div>
  );
}
