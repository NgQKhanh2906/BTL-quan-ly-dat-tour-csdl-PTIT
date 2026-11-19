import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  ArrowRight,
  RotateCcw,
  Search,
  SlidersHorizontal,
  Sparkles,
  Star,
} from 'lucide-react';
import { api, ApiError } from '../../api/client';
import type { ProvinceItem, ScheduleSearchItem } from '../../api/types';
import { formatDateTime, formatVnd } from '../../utils/format';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';

interface FilterState {
  tuKhoa: string;
  maTinhDen: string;
  giaTu: string;
  giaDen: string;
  tuNgay: string;
  denNgay: string;
  soKhach: number;
  diemToiThieu: string;
}

const RATING_OPTIONS = [
  { value: '', label: 'Tất cả mức sao' },
  { value: '3', label: 'Từ 3.0 sao trở lên' },
  { value: '4', label: 'Từ 4.0 sao trở lên' },
  { value: '4.5', label: 'Từ 4.5 sao trở lên' },
];

export default function ExplorePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [provinces, setProvinces] = useState<ProvinceItem[]>([]);
  const [defaultFromDate, setDefaultFromDate] = useState('');
  const [metaReady, setMetaReady] = useState(false);
  const lastSyncedQueryRef = useRef<string | null>(null);

  const [filters, setFilters] = useState<FilterState>({
    tuKhoa: searchParams.get('tu_khoa') || '',
    maTinhDen: searchParams.get('ma_tinh_den') || '',
    giaTu: searchParams.get('gia_tu') || '',
    giaDen: searchParams.get('gia_den') || '',
    tuNgay: searchParams.get('tu_ngay') || '',
    denNgay: searchParams.get('den_ngay') || '',
    soKhach: Math.max(1, Number(searchParams.get('so_khach') || 1)),
    diemToiThieu: searchParams.get('diem_toi_thieu') || '',
  });

  const [results, setResults] = useState<ScheduleSearchItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState<string | null>(null);

  // Instant validation
  const giaTuNum = filters.giaTu.trim() !== '' ? Number(filters.giaTu) : null;
  const giaDenNum = filters.giaDen.trim() !== '' ? Number(filters.giaDen) : null;
  const minPriceError =
    giaTuNum !== null && (Number.isNaN(giaTuNum) || giaTuNum < 0 || !Number.isInteger(giaTuNum))
      ? 'Giá từ phải là số nguyên không âm.'
      : null;
  const maxPriceError =
    giaDenNum !== null && (Number.isNaN(giaDenNum) || giaDenNum < 0 || !Number.isInteger(giaDenNum))
      ? 'Giá đến phải là số nguyên không âm.'
      : giaTuNum !== null &&
          giaDenNum !== null &&
          !minPriceError &&
          giaDenNum < giaTuNum
        ? 'Giá đến phải lớn hơn hoặc bằng giá từ.'
        : null;
  const dateError =
    filters.tuNgay && filters.denNgay && filters.denNgay < filters.tuNgay
      ? 'Ngày kết thúc lọc phải lớn hơn hoặc bằng ngày khởi hành từ.'
      : null;
  const hasValidationError = Boolean(minPriceError || maxPriceError || dateError);

  const runSearch = useCallback(async (activeFilters: FilterState) => {
    setLoading(true);
    setApiError(null);
    try {
      const data = await api.searchSchedules({
        tu_khoa: activeFilters.tuKhoa.trim() || undefined,
        ma_tinh_den: activeFilters.maTinhDen || undefined,
        gia_tu:
          activeFilters.giaTu.trim() !== '' && Number(activeFilters.giaTu) > 0
            ? Number(activeFilters.giaTu)
            : undefined,
        gia_den:
          activeFilters.giaDen.trim() !== '' && Number(activeFilters.giaDen) > 0
            ? Number(activeFilters.giaDen)
            : undefined,
        tu_ngay: activeFilters.tuNgay || undefined,
        den_ngay: activeFilters.denNgay || undefined,
        so_khach: activeFilters.soKhach,
        diem_toi_thieu:
          activeFilters.diemToiThieu !== '' ? Number(activeFilters.diemToiThieu) : undefined,
      });
      setResults(data);
    } catch (err) {
      setApiError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tìm kiếm lịch trình lúc này. Vui lòng thử lại.'
      );
      setResults([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let active = true;
    Promise.all([api.getProvinces(), api.getMeta()])
      .then(([provinceList, meta]) => {
        if (!active) return;
        setProvinces(provinceList);
        setDefaultFromDate(meta.current_date);

        const initial: FilterState = {
          tuKhoa: searchParams.get('tu_khoa') || '',
          maTinhDen: searchParams.get('ma_tinh_den') || '',
          giaTu: searchParams.get('gia_tu') || '',
          giaDen: searchParams.get('gia_den') || '',
          tuNgay: searchParams.get('tu_ngay') || meta.current_date,
          denNgay: searchParams.get('den_ngay') || '',
          soKhach: Math.max(1, Number(searchParams.get('so_khach') || 1)),
          diemToiThieu: searchParams.get('diem_toi_thieu') || '',
        };
        setFilters(initial);
        lastSyncedQueryRef.current = searchParams.toString();
        setMetaReady(true);
        runSearch(initial);
      })
      .catch(() => {
        if (!active) return;
        lastSyncedQueryRef.current = searchParams.toString();
        setMetaReady(true);
        runSearch(filters);
      });
    return () => {
      active = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const currentQueryString = searchParams.toString();
  useEffect(() => {
    if (!metaReady) return;
    if (lastSyncedQueryRef.current === currentQueryString) return;
    lastSyncedQueryRef.current = currentQueryString;
    const synced: FilterState = {
      tuKhoa: searchParams.get('tu_khoa') || '',
      maTinhDen: searchParams.get('ma_tinh_den') || '',
      giaTu: searchParams.get('gia_tu') || '',
      giaDen: searchParams.get('gia_den') || '',
      tuNgay: searchParams.get('tu_ngay') || defaultFromDate,
      denNgay: searchParams.get('den_ngay') || '',
      soKhach: Math.max(1, Number(searchParams.get('so_khach') || 1)),
      diemToiThieu: searchParams.get('diem_toi_thieu') || '',
    };
    setFilters(synced);
    runSearch(synced);
  }, [currentQueryString, defaultFromDate, metaReady, runSearch, searchParams]);

  const syncQueryString = (next: FilterState) => {
    const sp = new URLSearchParams();
    if (next.tuKhoa.trim()) sp.set('tu_khoa', next.tuKhoa.trim());
    if (next.maTinhDen) sp.set('ma_tinh_den', next.maTinhDen);
    if (next.giaTu.trim()) sp.set('gia_tu', next.giaTu.trim());
    if (next.giaDen.trim()) sp.set('gia_den', next.giaDen.trim());
    if (next.tuNgay && next.tuNgay !== defaultFromDate) sp.set('tu_ngay', next.tuNgay);
    if (next.denNgay) sp.set('den_ngay', next.denNgay);
    if (next.soKhach > 1) sp.set('so_khach', String(next.soKhach));
    if (next.diemToiThieu) sp.set('diem_toi_thieu', next.diemToiThieu);
    lastSyncedQueryRef.current = sp.toString();
    setSearchParams(sp, { replace: true });
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (hasValidationError) return;
    syncQueryString(filters);
    runSearch(filters);
  };

  const handleLuxuryFilter = () => {
    const next: FilterState = {
      ...filters,
      giaTu: '10000000',
      giaDen: '',
      tuNgay: filters.tuNgay || defaultFromDate,
    };
    setFilters(next);
    syncQueryString(next);
    runSearch(next);
  };

  const handleResetFilters = () => {
    const reset: FilterState = {
      tuKhoa: '',
      maTinhDen: '',
      giaTu: '',
      giaDen: '',
      tuNgay: defaultFromDate,
      denNgay: '',
      soKhach: 1,
      diemToiThieu: '',
    };
    setFilters(reset);
    lastSyncedQueryRef.current = '';
    setSearchParams(new URLSearchParams(), { replace: true });
    runSearch(reset);
  };

  const isLuxuryActive = filters.giaTu === '10000000' && filters.giaDen === '';

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-6">
        <div>
          <h1 className="text-2xl sm:text-[28px] font-bold text-slate-900 tracking-tight">
            Tra cứu lịch trình tour
          </h1>
          <p className="mt-1.5 text-sm text-slate-600 max-w-2xl">
            Lọc lịch khởi hành theo từ khóa, tỉnh đến, khoảng giá, ngày đi, số chỗ trống và điểm
            đánh giá.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <Button
            variant={isLuxuryActive ? 'primary' : 'secondary'}
            size="sm"
            shape="rounded"
            leftIcon={<Sparkles className="h-3.5 w-3.5" strokeWidth={1.75} />}
            onClick={handleLuxuryFilter}
          >
            Tour cao cấp (từ 10 triệu)
          </Button>
          <Button
            variant="ghost"
            size="sm"
            shape="rounded"
            leftIcon={<RotateCcw className="h-3.5 w-3.5" strokeWidth={1.75} />}
            onClick={handleResetFilters}
          >
            Đặt lại bộ lọc
          </Button>
        </div>
      </div>

      {/* 8-Criteria Filter Form */}
      <form
        noValidate
        onSubmit={handleSubmit}
        className="rounded-xl border border-slate-200 bg-white p-5 sm:p-6 shadow-[var(--shadow-card)] mb-7"
      >
        <div className="flex items-center gap-2 text-sm font-bold text-slate-900 mb-4">
          <SlidersHorizontal className="h-4 w-4 text-[#1D63ED]" strokeWidth={1.75} />
          <span>Điều kiện tìm kiếm</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* 1. Keyword */}
          <div>
            <label htmlFor="filter-keyword" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Từ khóa tên tour
            </label>
            <div className="relative">
              <Search
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                id="filter-keyword"
                type="text"
                value={filters.tuKhoa}
                onChange={(e) => setFilters((prev) => ({ ...prev, tuKhoa: e.target.value }))}
                placeholder="Hạ Long, Sa Pa, Du thuyền..."
                className="w-full h-10 rounded-[10px] border border-slate-200 bg-slate-50/70 pl-9.5 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              />
            </div>
          </div>

          {/* 2. Destination Province */}
          <div>
            <label htmlFor="filter-province" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Tỉnh điểm đến
            </label>
            <select
              id="filter-province"
              value={filters.maTinhDen}
              onChange={(e) => setFilters((prev) => ({ ...prev, maTinhDen: e.target.value }))}
              className="w-full h-10 rounded-[10px] border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15 cursor-pointer"
            >
              <option value="">Tất cả tỉnh miền Bắc</option>
              {provinces.map((p) => (
                <option key={p.ma_tinh} value={p.ma_tinh}>
                  {p.ten_tinh}
                </option>
              ))}
            </select>
          </div>

          {/* 3. Min Price */}
          <div>
            <label htmlFor="filter-price-min" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Giá từ (VND)
            </label>
            <input
              id="filter-price-min"
              type="number"
              min={0}
              step={1}
              value={filters.giaTu}
              onChange={(e) => setFilters((prev) => ({ ...prev, giaTu: e.target.value }))}
              placeholder="Ví dụ: 2000000"
              aria-invalid={Boolean(minPriceError)}
              className={[
                'w-full h-10 rounded-[10px] border bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums placeholder:text-slate-400 focus:bg-white focus:outline-none focus:ring-2',
                minPriceError
                  ? 'border-[#DC2626] focus:border-[#DC2626] focus:ring-red-500/15'
                  : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
              ].join(' ')}
            />
            {minPriceError && (
              <p className="mt-1 text-xs font-medium text-[#B91C1C]" role="alert">
                {minPriceError}
              </p>
            )}
          </div>

          {/* 4. Max Price */}
          <div>
            <label htmlFor="filter-price-max" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Giá đến (VND)
            </label>
            <input
              id="filter-price-max"
              type="number"
              min={0}
              step={1}
              value={filters.giaDen}
              onChange={(e) => setFilters((prev) => ({ ...prev, giaDen: e.target.value }))}
              placeholder="Không giới hạn"
              aria-invalid={Boolean(maxPriceError)}
              className={[
                'w-full h-10 rounded-[10px] border bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums placeholder:text-slate-400 focus:bg-white focus:outline-none focus:ring-2',
                maxPriceError
                  ? 'border-[#DC2626] focus:border-[#DC2626] focus:ring-red-500/15'
                  : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
              ].join(' ')}
            />
            {maxPriceError && (
              <p className="mt-1 text-xs font-medium text-[#B91C1C]" role="alert">
                {maxPriceError}
              </p>
            )}
          </div>

          {/* 5. From Date */}
          <div>
            <label htmlFor="filter-date-from" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Khởi hành từ ngày
            </label>
            <input
              id="filter-date-from"
              type="date"
              value={filters.tuNgay}
              onChange={(e) => setFilters((prev) => ({ ...prev, tuNgay: e.target.value }))}
              className="w-full h-10 rounded-[10px] border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
            />
          </div>

          {/* 6. To Date */}
          <div>
            <label htmlFor="filter-date-to" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Khởi hành đến ngày
            </label>
            <input
              id="filter-date-to"
              type="date"
              value={filters.denNgay}
              min={filters.tuNgay || undefined}
              onChange={(e) => setFilters((prev) => ({ ...prev, denNgay: e.target.value }))}
              aria-invalid={Boolean(dateError)}
              className={[
                'w-full h-10 rounded-[10px] border bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:outline-none focus:ring-2',
                dateError
                  ? 'border-[#DC2626] focus:border-[#DC2626] focus:ring-red-500/15'
                  : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
              ].join(' ')}
            />
            {dateError && (
              <p className="mt-1 text-xs font-medium text-[#B91C1C]" role="alert">
                {dateError}
              </p>
            )}
          </div>

          {/* 7. Minimum Guests */}
          <div>
            <label htmlFor="filter-guests" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Số khách tối thiểu
            </label>
            <input
              id="filter-guests"
              type="number"
              min={1}
              max={50}
              value={filters.soKhach}
              onChange={(e) =>
                setFilters((prev) => ({
                  ...prev,
                  soKhach: Math.max(1, Number(e.target.value) || 1),
                }))
              }
              className="w-full h-10 rounded-[10px] border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 tabular-nums focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
            />
          </div>

          {/* 8. Minimum Rating */}
          <div>
            <label htmlFor="filter-rating" className="block text-xs font-semibold text-slate-700 mb-1.5">
              Điểm đánh giá tối thiểu
            </label>
            <select
              id="filter-rating"
              value={filters.diemToiThieu}
              onChange={(e) => setFilters((prev) => ({ ...prev, diemToiThieu: e.target.value }))}
              className="w-full h-10 rounded-[10px] border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-900 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15 cursor-pointer"
            >
              {RATING_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="mt-5 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3">
          <p className="text-sm font-medium text-slate-600">
            {loading ? (
              'Đang tải danh sách lịch trình...'
            ) : (
              <>
                Tìm thấy{' '}
                <span className="font-bold text-slate-950 tabular-nums">{results.length}</span> lịch
                trình phù hợp
              </>
            )}
          </p>

          <Button
            type="submit"
            variant="primary"
            shape="rounded"
            size="md"
            disabled={hasValidationError || !metaReady}
            loading={loading}
            leftIcon={<Search className="h-4 w-4" strokeWidth={1.85} />}
          >
            Tìm kiếm
          </Button>
        </div>
      </form>

      {apiError && (
        <div
          role="alert"
          className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm font-medium text-[#B91C1C]"
        >
          {apiError}
        </div>
      )}

      {loading ? (
        <LoadingSkeleton variant="table" count={6} />
      ) : results.length === 0 ? (
        <EmptyState
          title="Không tìm thấy lịch trình phù hợp"
          description="Thử nới lỏng khoảng giá, chọn lại ngày khởi hành hoặc đặt lại bộ lọc để xem toàn bộ lịch trình đang mở bán."
          action={
            <Button variant="primary" shape="rounded" onClick={handleResetFilters}>
              Xóa bộ lọc
            </Button>
          }
        />
      ) : (
        <div className="rounded-xl border border-slate-200 bg-white shadow-[var(--shadow-card)] overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50/85 text-xs font-semibold text-slate-600">
                  <th className="py-3.5 pl-4 pr-3 whitespace-nowrap">Mã LT</th>
                  <th className="py-3.5 px-3">Tên tour</th>
                  <th className="py-3.5 px-3 whitespace-nowrap">Tuyến đường</th>
                  <th className="py-3.5 px-3 whitespace-nowrap">Khởi hành</th>
                  <th className="py-3.5 px-3 text-center whitespace-nowrap">Thời lượng</th>
                  <th className="py-3.5 px-3 text-center whitespace-nowrap">Chỗ trống</th>
                  <th className="py-3.5 px-3 text-center whitespace-nowrap">Đánh giá</th>
                  <th className="py-3.5 px-3 text-right whitespace-nowrap">Giá cơ bản</th>
                  <th className="py-3.5 pl-3 pr-4 text-right whitespace-nowrap">Thao tác</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {results.map((item) => (
                  <tr key={item.ma_lich_trinh} className="hover:bg-[#F8FAFC] transition-colors">
                    <td className="py-3.5 pl-4 pr-3 font-semibold text-slate-900 tabular-nums whitespace-nowrap">
                      {item.ma_lich_trinh}
                    </td>
                    <td className="py-3.5 px-3 max-w-[230px]">
                      <p className="font-semibold text-slate-900 truncate" title={item.ten_tour}>
                        {item.ten_tour}
                      </p>
                      {item.mo_ta && (
                        <p className="text-xs text-slate-500 truncate mt-0.5" title={item.mo_ta}>
                          {item.mo_ta}
                        </p>
                      )}
                    </td>
                    <td className="py-3.5 px-3 text-slate-700 whitespace-nowrap">
                      <span className="inline-flex items-center gap-1">
                        <span>{item.noi_di}</span>
                        <ArrowRight className="h-3.5 w-3.5 text-slate-400 shrink-0" strokeWidth={1.75} />
                        <span>{item.noi_den}</span>
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-slate-700 tabular-nums whitespace-nowrap">
                      {formatDateTime(item.ngay_xuat_phat)}
                    </td>
                    <td className="py-3.5 px-3 text-center text-slate-700 tabular-nums whitespace-nowrap">
                      {item.so_ngay} ngày
                    </td>
                    <td className="py-3.5 px-3 text-center font-semibold text-slate-800 tabular-nums whitespace-nowrap">
                      {item.so_cho_con_lai}
                    </td>
                    <td className="py-3.5 px-3 text-center whitespace-nowrap">
                      <span className="inline-flex items-center gap-1 font-semibold text-slate-800 tabular-nums">
                        <Star
                          className="h-3.5 w-3.5 fill-[#F59E0B] text-[#F59E0B]"
                          strokeWidth={1.75}
                        />
                        {item.diem_tb !== null ? (
                          <span>
                            {item.diem_tb.toFixed(1)}{' '}
                            <span className="text-xs font-normal text-slate-500">
                              ({item.so_luot_danh_gia})
                            </span>
                          </span>
                        ) : (
                          <span className="text-xs font-medium text-slate-500">Chưa có</span>
                        )}
                      </span>
                    </td>
                    <td className="py-3.5 px-3 text-right font-bold text-[#1D63ED] tabular-nums whitespace-nowrap">
                      {formatVnd(item.gia_co_ban)}
                    </td>
                    <td className="py-3.5 pl-3 pr-4 text-right whitespace-nowrap">
                      <Link
                        to={`/book?schedule=${encodeURIComponent(item.ma_lich_trinh)}`}
                        className="inline-flex items-center gap-1 rounded-lg bg-[#1D63ED] px-3 py-1.5 text-xs font-semibold text-white hover:bg-[#154EC2] transition-colors"
                      >
                        <span>Đặt tour</span>
                        <ArrowRight className="h-3.5 w-3.5" strokeWidth={2} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
