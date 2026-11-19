import { ArrowRight, Building2, Calendar, Car, CheckCircle2, MapPin, Users } from 'lucide-react';
import type { AccommodationItem, BookingEstimateResponse, OpenScheduleItem } from '../../api/types';
import { formatDateTime, formatDuration, formatVnd } from '../../utils/format';
import { Button } from '../common/Button';

interface BookingSummaryCardProps {
  schedule: OpenScheduleItem | null;
  soKhach: number;
  accommodation: AccommodationItem | null;
  soPhong: number;
  coXeDon: boolean;
  coXeVe: boolean;
  estimate: BookingEstimateResponse;
  submitting: boolean;
  disabled?: boolean;
  onSubmitClick?: () => void;
}

export function BookingSummaryCard({
  schedule,
  soKhach,
  accommodation,
  soPhong,
  coXeDon,
  coXeVe,
  estimate,
  submitting,
  disabled = false,
  onSubmitClick,
}: BookingSummaryCardProps) {
  return (
    <aside className="lg:sticky lg:top-22 rounded-xl border border-slate-200 bg-white shadow-[var(--shadow-card)] overflow-hidden">
      {schedule ? (
        <>
          <div className="bg-[#EFF6FF]/75 border-b border-slate-200 px-5 py-4 space-y-2">
            <div className="flex items-center justify-between gap-2">
              <span className="inline-flex items-center rounded-md bg-white border border-[#BFDBFE] px-2.5 py-0.5 text-xs font-bold text-[#1D4ED8] tabular-nums">
                {schedule.ma_lich_trinh}
              </span>
              <span className="text-xs font-semibold text-slate-600">
                {formatDuration(schedule.so_dem)}
              </span>
            </div>
            <h2 className="text-base font-bold text-slate-900 leading-snug">{schedule.ten_tour}</h2>
            <p className="text-xs font-medium text-slate-600 inline-flex flex-wrap items-center gap-1">
              <span>{schedule.noi_di}</span>
              <ArrowRight className="h-3 w-3 text-slate-400 shrink-0" strokeWidth={2} />
              <span>{schedule.ten_tinh_den}</span>
            </p>
          </div>

          <div className="p-5 space-y-4">
            <div className="space-y-2.5 text-sm">
              <div className="flex items-start justify-between gap-3">
                <span className="inline-flex items-center gap-2 text-slate-500 shrink-0">
                  <Calendar className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
                  Khởi hành
                </span>
                <span className="font-semibold text-slate-900 text-right tabular-nums">
                  {formatDateTime(schedule.ngay_xuat_phat)}
                </span>
              </div>

              <div className="flex items-start justify-between gap-3">
                <span className="inline-flex items-center gap-2 text-slate-500 shrink-0">
                  <MapPin className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
                  Tập trung
                </span>
                <span className="font-medium text-slate-700 text-right line-clamp-2">
                  {schedule.diem_tap_trung}
                </span>
              </div>

              <div className="flex items-center justify-between gap-3">
                <span className="inline-flex items-center gap-2 text-slate-500">
                  <Users className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
                  Số khách
                </span>
                <span className="font-semibold text-slate-900 tabular-nums">{soKhach} khách</span>
              </div>

              <div className="flex items-start justify-between gap-3">
                <span className="inline-flex items-center gap-2 text-slate-500 shrink-0">
                  <Building2 className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
                  Lưu trú
                </span>
                <span className="font-medium text-slate-800 text-right">
                  {schedule.so_dem === 0
                    ? 'Tour trong ngày'
                    : accommodation
                      ? `${accommodation.ten_nha_nghi} (${soPhong} phòng)`
                      : 'Không đặt nơi nghỉ'}
                </span>
              </div>

              <div className="flex items-start justify-between gap-3">
                <span className="inline-flex items-center gap-2 text-slate-500 shrink-0">
                  <Car className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
                  Trung chuyển
                </span>
                <span className="font-medium text-slate-800 text-right">
                  {!coXeDon && !coXeVe
                    ? 'Tự túc di chuyển'
                    : [coXeDon ? 'Đón tại nhà' : null, coXeVe ? 'Về nơi nghỉ' : null]
                        .filter(Boolean)
                        .join(' + ')}
                </span>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 space-y-2.5 text-sm">
              <div className="flex items-center justify-between gap-3">
                <span className="text-slate-600">
                  Tiền tour ({soKhach} × {formatVnd(schedule.gia_co_ban)})
                </span>
                <span className="font-semibold text-slate-900 tabular-nums">
                  {formatVnd(estimate.tien_tour)}
                </span>
              </div>

              <div className="flex items-center justify-between gap-3">
                <span className="text-slate-600">
                  Tiền lưu trú
                  {accommodation && schedule.so_dem > 0
                    ? ` (${soPhong} phòng × ${schedule.so_dem} đêm)`
                    : ''}
                </span>
                <span className="font-semibold text-slate-900 tabular-nums">
                  {formatVnd(estimate.tien_phong)}
                </span>
              </div>

              <div className="pt-3 mt-1 border-t border-slate-200 flex items-baseline justify-between gap-3">
                <span className="text-base font-bold text-slate-900">Tổng tiền dự kiến</span>
                <span className="text-2xl font-bold text-[#1D63ED] tabular-nums">
                  {formatVnd(estimate.tong_tien)}
                </span>
              </div>
            </div>

            <Button
              type={onSubmitClick ? 'button' : 'submit'}
              onClick={onSubmitClick}
              variant="primary"
              shape="rounded"
              size="lg"
              loading={submitting}
              disabled={disabled || !schedule}
              leftIcon={<CheckCircle2 className="h-4.5 w-4.5" strokeWidth={1.85} />}
              className="w-full"
            >
              Xác nhận đặt tour
            </Button>
          </div>
        </>
      ) : (
        <div className="p-6 text-center text-sm text-slate-500">
          Vui lòng chọn một lịch trình khởi hành để xem dự toán chi phí chi tiết.
        </div>
      )}
    </aside>
  );
}
