import { useEffect, useState, type FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, CalendarRange, MapPin, Search, Users } from 'lucide-react';
import type { ProvinceItem } from '../../api/types';

interface FloatingSearchBarProps {
  provinces: ProvinceItem[];
  defaultFromDate: string;
}

export function FloatingSearchBar({ provinces, defaultFromDate }: FloatingSearchBarProps) {
  const navigate = useNavigate();
  const [maTinhDen, setMaTinhDen] = useState('');
  const [tuNgay, setTuNgay] = useState(defaultFromDate);
  const [denNgay, setDenNgay] = useState('');
  const [soKhach, setSoKhach] = useState(2);

  useEffect(() => {
    if (defaultFromDate && !tuNgay) {
      setTuNgay(defaultFromDate);
    }
  }, [defaultFromDate, tuNgay]);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    const params = new URLSearchParams();
    if (maTinhDen) params.set('ma_tinh_den', maTinhDen);
    if (tuNgay) params.set('tu_ngay', tuNgay);
    if (denNgay && (!tuNgay || denNgay >= tuNgay)) params.set('den_ngay', denNgay);
    if (soKhach > 1) params.set('so_khach', String(soKhach));
    const qs = params.toString();
    navigate(qs ? `/explore?${qs}` : '/explore');
  };

  return (
    <form
      onSubmit={handleSubmit}
      aria-label="Tìm nhanh lịch trình tour"
      className="relative z-20 mx-auto w-full max-w-5xl rounded-[26px] lg:rounded-full bg-white border border-slate-200/75 shadow-[var(--shadow-floating)] p-3 sm:p-4 lg:py-2.5 lg:pl-5 lg:pr-2.5"
    >
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-[1.25fr_1fr_1fr_0.9fr_auto] items-center gap-3 lg:gap-0 lg:divide-x lg:divide-slate-200/80">
        {/* Field 1: Destination */}
        <div className="flex items-center gap-3 px-2 lg:pr-4">
          <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
            <MapPin className="h-4.5 w-4.5" strokeWidth={1.75} />
          </span>
          <div className="min-w-0 flex-1">
            <label
              htmlFor="hero-search-province"
              className="block text-xs font-bold text-slate-900"
            >
              Điểm đến
            </label>
            <select
              id="hero-search-province"
              value={maTinhDen}
              onChange={(e) => setMaTinhDen(e.target.value)}
              className="mt-0.5 w-full bg-transparent text-sm text-slate-600 font-medium focus:outline-none cursor-pointer truncate"
            >
              <option value="">Tất cả tỉnh miền Bắc</option>
              {provinces.map((p) => (
                <option key={p.ma_tinh} value={p.ma_tinh}>
                  {p.ten_tinh}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Field 2: Departure from */}
        <div className="flex items-center gap-3 px-2 lg:px-4">
          <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
            <Calendar className="h-4.5 w-4.5" strokeWidth={1.75} />
          </span>
          <div className="min-w-0 flex-1">
            <label
              htmlFor="hero-search-from"
              className="block text-xs font-bold text-slate-900"
            >
              Khởi hành từ
            </label>
            <input
              id="hero-search-from"
              type="date"
              value={tuNgay}
              onChange={(e) => {
                const next = e.target.value;
                setTuNgay(next);
                if (denNgay && next && denNgay < next) {
                  setDenNgay('');
                }
              }}
              className="mt-0.5 w-full bg-transparent text-sm text-slate-600 font-medium tabular-nums focus:outline-none cursor-pointer"
            />
          </div>
        </div>

        {/* Field 3: Departure to (optional) */}
        <div className="flex items-center gap-3 px-2 lg:px-4">
          <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
            <CalendarRange className="h-4.5 w-4.5" strokeWidth={1.75} />
          </span>
          <div className="min-w-0 flex-1">
            <label
              htmlFor="hero-search-to"
              className="block text-xs font-bold text-slate-900"
            >
              Đến ngày
            </label>
            <input
              id="hero-search-to"
              type="date"
              value={denNgay}
              min={tuNgay || undefined}
              onChange={(e) => setDenNgay(e.target.value)}
              className="mt-0.5 w-full bg-transparent text-sm text-slate-600 font-medium tabular-nums focus:outline-none cursor-pointer"
            />
          </div>
        </div>

        {/* Field 4: Travelers */}
        <div className="flex items-center gap-3 px-2 lg:px-4">
          <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
            <Users className="h-4.5 w-4.5" strokeWidth={1.75} />
          </span>
          <div className="min-w-0 flex-1">
            <label
              htmlFor="hero-search-guests"
              className="block text-xs font-bold text-slate-900"
            >
              Số khách
            </label>
            <select
              id="hero-search-guests"
              value={soKhach}
              onChange={(e) => setSoKhach(Number(e.target.value))}
              className="mt-0.5 w-full bg-transparent text-sm text-slate-600 font-medium tabular-nums focus:outline-none cursor-pointer"
            >
              {Array.from({ length: 20 }, (_, i) => i + 1).map((n) => (
                <option key={n} value={n}>
                  {n} khách
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Submit button */}
        <div className="sm:col-span-2 lg:col-span-1 lg:pl-3 flex justify-end">
          <button
            type="submit"
            aria-label="Tìm kiếm lịch trình"
            className="w-full lg:w-13 h-12 lg:h-13 inline-flex items-center justify-center gap-2 rounded-full bg-[#1D63ED] text-white font-semibold text-sm shadow-[0_10px_24px_rgba(29,99,237,0.32)] hover:bg-[#154EC2] active:scale-[0.98] transition-all duration-200 cursor-pointer"
          >
            <Search className="h-5 w-5" strokeWidth={1.9} />
            <span className="lg:hidden">Tìm lịch trình</span>
          </button>
        </div>
      </div>
    </form>
  );
}
