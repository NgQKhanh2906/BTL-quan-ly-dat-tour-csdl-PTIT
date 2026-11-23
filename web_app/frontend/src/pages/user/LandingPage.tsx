import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowRight,
  BarChart3,
  CalendarCheck2,
  ClipboardList,
  Compass,
  FileText,
  MapPinned,
  MessageSquareHeart,
  PlusCircle,
  Search,
  Star,
} from 'lucide-react';
import { api } from '../../api/client';
import type { LandingResponse } from '../../api/types';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { formatDateTime, formatVnd } from '../../utils/format';

const BUSINESS_FORMS = [
  {
    to: '/explore',
    title: 'Tra cứu lịch trình tour',
    description: 'Lọc lịch khởi hành theo từ khóa, tỉnh đến, khoảng giá, ngày đi, số khách và điểm đánh giá.',
    icon: Search,
    color: 'text-[#1D63ED] bg-[#EFF6FF] border-blue-100',
    buttonText: 'Mở bộ lọc tra cứu',
  },
  {
    to: '/book',
    title: 'Đặt tour trực tuyến',
    description: 'Điền thông tin đặt tour mới, chọn nơi nghỉ theo tỉnh đến và đăng ký xe trung chuyển đón trả.',
    icon: PlusCircle,
    color: 'text-emerald-600 bg-emerald-50 border-emerald-100',
    buttonText: 'Mở form đặt tour',
  },
  {
    to: '/orders',
    title: 'Quản lý và Hủy đơn tour',
    description: 'Xem toàn bộ danh sách đơn hàng, cập nhật trạng thái, xem trước tiền phạt và hủy đơn hoàn chỗ.',
    icon: ClipboardList,
    color: 'text-amber-600 bg-amber-50 border-amber-100',
    buttonText: 'Mở danh sách đơn',
  },
  {
    to: '/reviews',
    title: 'Đánh giá chuyến đi',
    description: 'Ghi nhận điểm số sao và nhận xét của khách hàng đối với chương trình tour và nơi lưu trú.',
    icon: MessageSquareHeart,
    color: 'text-rose-600 bg-rose-50 border-rose-100',
    buttonText: 'Mở form đánh giá',
  },
  {
    to: '/confirmations',
    title: 'Phiếu xác nhận đặt tour (PDF)',
    description: 'Xem trước biểu mẫu xác nhận dịch vụ theo từng đơn hàng, in trực tiếp và tải file PDF khổ A4 dọc.',
    icon: FileText,
    color: 'text-indigo-600 bg-indigo-50 border-indigo-100',
    buttonText: 'Mở biểu mẫu in phiếu',
  },
  {
    to: '/reports',
    title: 'Thống kê & Báo cáo doanh thu (PDF)',
    description: 'Tổng hợp doanh thu theo tuyến tour, xếp hạng chất lượng nơi nghỉ và xuất báo cáo PDF khổ A4 ngang.',
    icon: BarChart3,
    color: 'text-sky-600 bg-sky-50 border-sky-100',
    buttonText: 'Mở báo cáo doanh thu',
  },
];

export default function LandingPage() {
  const [landing, setLanding] = useState<LandingResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setLoading(true);
    api
      .getLanding()
      .then((data) => {
        if (!active) return;
        setLanding(data);
        setError(null);
      })
      .catch(() => {
        if (!active) return;
        setError('Không thể tải dữ liệu tổng quan lúc này. Vui lòng thử lại.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const stats = landing?.stats;
  const upcomingSchedules = (landing?.featured_schedules ?? []).slice(0, 6);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8 space-y-8">
      {/* Header tổng quan */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-[28px] font-bold text-slate-900 tracking-tight">
            Hệ thống quản lý đặt tour du lịch miền Bắc
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2.5 shrink-0">
          <Link
            to="/explore"
            className="inline-flex items-center gap-2 rounded-[10px] border border-slate-200 bg-white px-4 h-10 text-sm font-semibold text-slate-800 hover:bg-slate-50 hover:border-slate-300 transition-colors shadow-xs"
          >
            <Search className="h-4 w-4 text-slate-500" strokeWidth={1.75} />
            Tra cứu lịch trình
          </Link>
          <Link
            to="/book"
            className="inline-flex items-center gap-2 rounded-[10px] bg-[#1D63ED] px-4 h-10 text-sm font-semibold text-white hover:bg-[#154EC2] transition-colors shadow-[0_6px_16px_rgba(29,99,237,0.22)]"
          >
            <PlusCircle className="h-4 w-4" strokeWidth={1.85} />
            Đặt tour mới
          </Link>
        </div>
      </div>

      {error && (
        <div
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-[#B91C1C]"
        >
          {error}
        </div>
      )}

      {/* 4 Thẻ KPI số liệu thực */}
      {loading ? (
        <LoadingSkeleton variant="kpi" count={4} />
      ) : (
        <section aria-label="Số liệu tổng quan hệ thống" className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[var(--shadow-card)] flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-slate-500">Tỉnh thành miền Bắc</p>
              <p className="mt-1.5 text-2xl font-bold text-slate-900 tabular-nums">
                {stats ? stats.total_provinces : '—'}
              </p>
              <p className="mt-1 text-xs text-slate-500">Điểm đến trong mạng lưới</p>
            </div>
            <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#EFF6FF] text-[#1D63ED]">
              <MapPinned className="h-5 w-5" strokeWidth={1.75} />
            </span>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[var(--shadow-card)] flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-slate-500">Tuyến tour khai thác</p>
              <p className="mt-1.5 text-2xl font-bold text-slate-900 tabular-nums">
                {stats ? stats.total_tours : '—'}
              </p>
              <p className="mt-1 text-xs text-slate-500">Chương trình du lịch miền Bắc</p>
            </div>
            <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
              <Compass className="h-5 w-5" strokeWidth={1.75} />
            </span>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[var(--shadow-card)] flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-slate-500">Lịch trình mở bán</p>
              <p className="mt-1.5 text-2xl font-bold text-slate-900 tabular-nums">
                {stats ? stats.open_schedules : '—'}
              </p>
              <p className="mt-1 text-xs text-slate-500">Chuyến sắp khởi hành còn chỗ</p>
            </div>
            <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-sky-50 text-sky-600">
              <CalendarCheck2 className="h-5 w-5" strokeWidth={1.75} />
            </span>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[var(--shadow-card)] flex items-start justify-between gap-3">
            <div>
              <p className="text-xs font-medium text-slate-500">Đánh giá trung bình</p>
              <p className="mt-1.5 text-2xl font-bold text-slate-900 tabular-nums">
                {stats && stats.avg_rating !== null ? `${stats.avg_rating.toFixed(1)} / 5` : 'Chưa có'}
              </p>
              <p className="mt-1 text-xs text-slate-500 tabular-nums">
                {stats ? `${stats.total_reviews} lượt đánh giá thực tế` : 'Chờ dữ liệu'}
              </p>
            </div>
            <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-600">
              <Star className="h-5 w-5 fill-[#F59E0B] text-[#F59E0B]" strokeWidth={1.75} />
            </span>
          </div>
        </section>
      )}

      {/* Danh mục các biểu mẫu chức năng hệ thống */}
      <section aria-label="Danh mục các biểu mẫu chức năng hệ thống" className="space-y-4">
        <div>
          <h2 className="text-lg font-bold text-slate-900">Danh mục biểu mẫu nghiệp vụ</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Các màn hình thao tác nghiệp vụ chính của hệ thống đặt và quản lý tour.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {BUSINESS_FORMS.map((form) => {
            const Icon = form.icon;
            return (
              <div
                key={form.to}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-[var(--shadow-card)] flex flex-col justify-between hover:border-slate-300 hover:shadow-md transition-all"
              >
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <span
                      className={`inline-flex h-10 w-10 items-center justify-center rounded-xl border ${form.color}`}
                    >
                      <Icon className="h-5 w-5" strokeWidth={1.75} />
                    </span>
                    <h3 className="text-base font-bold text-slate-900">{form.title}</h3>
                  </div>
                  <p className="text-xs leading-relaxed text-slate-600">{form.description}</p>
                </div>

                <div className="pt-4 mt-2 border-t border-slate-100">
                  <Link
                    to={form.to}
                    className="w-full inline-flex items-center justify-between rounded-lg bg-slate-50 hover:bg-[#EFF6FF] px-3.5 py-2 text-xs font-semibold text-slate-700 hover:text-[#1D63ED] transition-colors"
                  >
                    <span>{form.buttonText}</span>
                    <ArrowRight className="h-3.5 w-3.5" strokeWidth={2} />
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Bảng Lịch trình sắp khởi hành còn chỗ */}
      <section aria-label="Lịch trình mở bán gần nhất" className="space-y-3.5">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900">Lịch khởi hành sắp tới còn chỗ</h2>
            <p className="text-xs text-slate-500 mt-0.5">
              Các chuyến tour đã sẵn sàng đón khách trong thời gian tới.
            </p>
          </div>
          <Link
            to="/explore"
            className="text-xs font-semibold text-[#1D63ED] hover:underline inline-flex items-center gap-1"
          >
            Xem tất cả
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {loading ? (
          <LoadingSkeleton variant="table" count={5} />
        ) : upcomingSchedules.length === 0 ? (
          <div className="rounded-xl border border-slate-200 bg-white p-6 text-center text-sm text-slate-500">
            Hiện chưa có lịch khởi hành mở bán.
          </div>
        ) : (
          <div className="rounded-xl border border-slate-200 bg-white shadow-[var(--shadow-card)] overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/80 text-xs font-bold text-slate-600">
                    <th scope="col" className="py-3 px-4">Mã LT</th>
                    <th scope="col" className="py-3 px-4">Tên tour</th>
                    <th scope="col" className="py-3 px-4">Tuyến đường</th>
                    <th scope="col" className="py-3 px-4">Khởi hành</th>
                    <th scope="col" className="py-3 px-4">Chỗ trống</th>
                    <th scope="col" className="py-3 px-4">Giá cơ bản</th>
                    <th scope="col" className="py-3 px-4 text-right">Thao tác</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {upcomingSchedules.map((item) => (
                    <tr key={item.ma_lich_trinh} className="hover:bg-slate-50/70 transition-colors">
                      <td className="py-3 px-4 font-mono text-xs font-bold text-[#1D63ED]">
                        {item.ma_lich_trinh}
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-900 max-w-[240px] truncate">
                        {item.ten_tour}
                      </td>
                      <td className="py-3 px-4 text-xs text-slate-600">
                        {item.noi_di} &rarr; {item.noi_den}
                      </td>
                      <td className="py-3 px-4 text-xs text-slate-700 whitespace-nowrap">
                        {formatDateTime(item.ngay_xuat_phat)}
                      </td>
                      <td className="py-3 px-4 text-xs font-semibold text-emerald-700 whitespace-nowrap">
                        {item.so_cho_con_lai} chỗ
                      </td>
                      <td className="py-3 px-4 font-bold text-slate-900 whitespace-nowrap">
                        {formatVnd(item.gia_co_ban)}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <Link
                          to={`/book?schedule=${encodeURIComponent(item.ma_lich_trinh)}`}
                          className="inline-flex items-center gap-1.5 rounded-lg bg-[#EFF6FF] text-[#1D63ED] hover:bg-[#1D63ED] hover:text-white px-3 py-1.5 text-xs font-semibold transition-colors"
                        >
                          <span>Đặt tour</span>
                          <ArrowRight className="h-3 w-3" />
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
