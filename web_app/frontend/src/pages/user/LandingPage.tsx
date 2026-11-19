import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import {
  ArrowRight,
  CalendarCheck2,
  ChevronLeft,
  ChevronRight,
  Compass,
  MapPinned,
  Sparkles,
} from 'lucide-react';
import { api } from '../../api/client';
import type { LandingResponse, ProvinceItem } from '../../api/types';
import { PROMO_CRUISE_IMAGE } from '../../constants/tourImages';
import { HeroFlightArc } from '../../components/common/BrandLogo';
import { EmptyState } from '../../components/common/EmptyState';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { FloatingSearchBar } from '../../components/user/FloatingSearchBar';
import { HeroOrganicFrame } from '../../components/user/HeroOrganicFrame';
import { TourCard } from '../../components/user/TourCard';

const FEATURED_PAGE_SIZE = 4;

export default function LandingPage() {
  const prefersReducedMotion = useReducedMotion();
  const [landing, setLanding] = useState<LandingResponse | null>(null);
  const [provinces, setProvinces] = useState<ProvinceItem[]>([]);
  const [defaultFromDate, setDefaultFromDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [carouselOffset, setCarouselOffset] = useState(0);

  useEffect(() => {
    let active = true;
    setLoading(true);
    Promise.all([api.getLanding(), api.getProvinces(), api.getMeta()])
      .then(([landingData, provinceList, metaData]) => {
        if (!active) return;
        setLanding(landingData);
        setProvinces(provinceList);
        setDefaultFromDate(metaData.current_date);
        setError(null);
      })
      .catch(() => {
        if (!active) return;
        setError('Không thể tải danh sách điểm đến nổi bật lúc này. Vui lòng thử lại.');
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const featuredList = landing?.featured_schedules ?? [];
  const maxOffset = Math.max(0, featuredList.length - FEATURED_PAGE_SIZE);
  const safeOffset = Math.min(carouselOffset, maxOffset);
  const visibleFeatured = featuredList.slice(safeOffset, safeOffset + FEATURED_PAGE_SIZE);

  const handleScrollToFeatured = () => {
    const el = document.getElementById('featured-destinations');
    el?.scrollIntoView({ behavior: prefersReducedMotion ? 'auto' : 'smooth', block: 'start' });
  };

  const stats = landing?.stats;

  return (
    <div className="pb-6">
      {/* Hero Editorial Split */}
      <section className="relative overflow-x-clip pt-4 sm:pt-6 lg:pt-8">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute top-0 right-0 h-[440px] w-[55%] rounded-bl-[160px] bg-gradient-to-bl from-[#E0ECFF]/60 via-[#EFF5FF]/40 to-transparent -z-10"
        />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-6 items-center">
            {/* Left Copy Column (~44%) */}
            <motion.div
              initial={prefersReducedMotion ? false : { opacity: 0.01, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.48, ease: [0.22, 1, 0.36, 1] }}
              className="lg:col-span-5 relative z-10 pb-2 lg:pb-14"
            >
              <HeroFlightArc className="mb-3 h-7 w-32 opacity-90" />

              <h1 className="font-display text-[44px] sm:text-[56px] xl:text-[66px] leading-[1.04] tracking-[-0.03em] text-slate-950 font-bold">
                <span className="block">Miền Bắc</span>
                <span className="block italic text-[#1D63ED] font-semibold mt-1">
                  trọn vẹn sắc màu.
                </span>
              </h1>

              <p className="mt-5 max-w-[44ch] text-[15px] sm:text-base text-slate-600 leading-relaxed">
                Từ vịnh di sản Hạ Long đến đỉnh Fansipan mờ sương, chọn lịch trình khởi hành phù hợp
                và đặt chỗ trực tuyến chỉ trong vài bước.
              </p>

              <div className="mt-7 flex flex-wrap items-center gap-3.5">
                <Link
                  to="/explore"
                  className="group inline-flex items-center gap-3.5 rounded-full bg-[#1D63ED] pl-6 pr-2 py-2 text-[15px] font-semibold text-white shadow-[0_12px_28px_rgba(29,99,237,0.28)] hover:bg-[#154EC2] hover:-translate-y-0.5 transition-all duration-200"
                >
                  <span>Khám phá lịch trình</span>
                  <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-white text-[#1D63ED] transition-transform duration-200 group-hover:translate-x-0.5">
                    <ArrowRight className="h-4.5 w-4.5" strokeWidth={2} />
                  </span>
                </Link>

                <Link
                  to="/book"
                  className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-5 py-3 text-sm font-semibold text-slate-700 hover:border-slate-300 hover:text-slate-950 transition-colors shadow-xs"
                >
                  Đặt tour ngay
                </Link>
              </div>
            </motion.div>

            {/* Right Organic Photo Column (~56%) */}
            <div className="lg:col-span-7">
              <HeroOrganicFrame
                stats={stats ?? null}
                onExploreHighlight={handleScrollToFeatured}
              />
            </div>
          </div>

          {/* Floating Pill Search Bar Overlapping Hero Bottom Edge */}
          <div className="mt-6 lg:-mt-12 relative z-20">
            <FloatingSearchBar provinces={provinces} defaultFromDate={defaultFromDate} />
          </div>
        </div>
      </section>

      {/* Lower 2-Column Section: Luxury Cruise Promo + Live Stats | Featured Destinations */}
      <section
        id="featured-destinations"
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 lg:mt-14 scroll-mt-24"
      >
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-7 items-stretch">
          {/* Left Column (~32%): Cobalt Promo Card + Live DB Stats */}
          <div className="lg:col-span-4 flex flex-col gap-5">
            <div className="relative flex-1 min-h-[228px] overflow-hidden rounded-[24px] bg-[#154EC2] shadow-[0_16px_36px_rgba(29,99,237,0.22)] flex flex-col justify-between p-6">
              <img
                src={PROMO_CRUISE_IMAGE}
                alt="Du thuyền cao cấp trên Vịnh Hạ Long lúc hoàng hôn"
                loading="lazy"
                className="absolute inset-0 h-full w-full object-cover object-right"
              />
              <div
                aria-hidden="true"
                className="absolute inset-0 bg-gradient-to-r from-[#0B3A99] via-[#1D63ED]/88 to-[#1D63ED]/15"
              />

              <div className="relative z-10">
                <span className="inline-flex items-center gap-1.5 rounded-full bg-white/18 backdrop-blur-sm border border-white/20 px-3 py-1 text-[11px] font-semibold text-sky-50">
                  <Sparkles className="h-3 w-3" strokeWidth={1.75} />
                  Trải nghiệm cao cấp
                </span>

                <h2 className="mt-3.5 text-xl sm:text-[22px] font-bold text-white leading-snug max-w-[235px]">
                  Du thuyền &amp; Hành trình từ 10 triệu
                </h2>

                <p className="mt-2 text-xs text-sky-100/95 leading-relaxed max-w-[225px]">
                  Trọn gói du thuyền nghỉ đêm trên vịnh di sản và cung đường chọn lọc.
                </p>
              </div>

              <div className="relative z-10 mt-5">
                <Link
                  to="/explore?gia_tu=10000000"
                  className="group inline-flex items-center gap-2 rounded-full bg-white px-4.5 py-2.5 text-xs font-bold text-[#154EC2] shadow-sm hover:bg-sky-50 transition-colors"
                >
                  <span>Xem ngay</span>
                  <ArrowRight
                    className="h-3.5 w-3.5 transition-transform duration-200 group-hover:translate-x-0.5"
                    strokeWidth={2}
                  />
                </Link>
              </div>
            </div>

            {/* Live MySQL Stats Strip */}
            <div className="rounded-[20px] border border-slate-200/80 bg-white p-5 shadow-[var(--shadow-card)]">
              <div className="grid grid-cols-3 gap-3">
                <div className="flex flex-col sm:flex-row lg:flex-col xl:flex-row items-start sm:items-center lg:items-start xl:items-center gap-2.5">
                  <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-[#1D63ED]">
                    <MapPinned className="h-4.5 w-4.5" strokeWidth={1.75} />
                  </span>
                  <div className="min-w-0">
                    <p className="text-lg font-bold text-slate-900 tabular-nums leading-tight">
                      {stats ? stats.total_provinces : '—'}
                    </p>
                    <p className="text-[11px] font-medium text-slate-500 leading-tight mt-0.5">
                      Tỉnh miền Bắc
                    </p>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row lg:flex-col xl:flex-row items-start sm:items-center lg:items-start xl:items-center gap-2.5">
                  <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
                    <Compass className="h-4.5 w-4.5" strokeWidth={1.75} />
                  </span>
                  <div className="min-w-0">
                    <p className="text-lg font-bold text-slate-900 tabular-nums leading-tight">
                      {stats ? stats.total_tours : '—'}
                    </p>
                    <p className="text-[11px] font-medium text-slate-500 leading-tight mt-0.5">
                      Tuyến hành trình
                    </p>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row lg:flex-col xl:flex-row items-start sm:items-center lg:items-start xl:items-center gap-2.5">
                  <span className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-amber-50 text-amber-600">
                    <CalendarCheck2 className="h-4.5 w-4.5" strokeWidth={1.75} />
                  </span>
                  <div className="min-w-0">
                    <p className="text-lg font-bold text-slate-900 tabular-nums leading-tight">
                      {stats ? stats.open_schedules : '—'}
                    </p>
                    <p className="text-[11px] font-medium text-slate-500 leading-tight mt-0.5">
                      Lịch khởi hành
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column (~68%): Featured Destinations 4-Card Carousel/Grid */}
          <div className="lg:col-span-8 flex flex-col justify-between">
            <div className="flex items-center justify-between gap-4 mb-4">
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
                Điểm đến nổi bật
              </h2>

              <div className="flex items-center gap-3">
                {featuredList.length > FEATURED_PAGE_SIZE && (
                  <div className="hidden sm:flex items-center gap-1.5">
                    <button
                      type="button"
                      disabled={safeOffset === 0}
                      onClick={() => setCarouselOffset((prev) => Math.max(0, prev - 1))}
                      aria-label="Xem điểm đến trước"
                      className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 hover:border-[#1D63ED] hover:text-[#1D63ED] disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
                    >
                      <ChevronLeft className="h-4 w-4" strokeWidth={1.9} />
                    </button>
                    <button
                      type="button"
                      disabled={safeOffset >= maxOffset}
                      onClick={() => setCarouselOffset((prev) => Math.min(maxOffset, prev + 1))}
                      aria-label="Xem điểm đến tiếp theo"
                      className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 hover:border-[#1D63ED] hover:text-[#1D63ED] disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
                    >
                      <ChevronRight className="h-4 w-4" strokeWidth={1.9} />
                    </button>
                  </div>
                )}

                <Link
                  to="/explore"
                  className="inline-flex items-center gap-1 text-sm font-semibold text-[#1D63ED] hover:text-[#154EC2] transition-colors"
                >
                  <span>Xem tất cả</span>
                  <ChevronRight className="h-4 w-4" strokeWidth={2} />
                </Link>
              </div>
            </div>

            {loading ? (
              <LoadingSkeleton variant="cards" count={4} />
            ) : error ? (
              <EmptyState
                title="Chưa thể tải lịch trình nổi bật"
                description={error}
                action={
                  <Link
                    to="/explore"
                    className="inline-flex items-center gap-2 rounded-full bg-[#1D63ED] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2]"
                  >
                    Tới trang Khám phá tour
                  </Link>
                }
              />
            ) : visibleFeatured.length === 0 ? (
              <EmptyState
                title="Hiện chưa có lịch trình sắp khởi hành"
                description="Vui lòng khám phá toàn bộ danh sách tour để chọn thời gian khởi hành phù hợp."
                action={
                  <Link
                    to="/explore"
                    className="inline-flex items-center gap-2 rounded-full bg-[#1D63ED] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#154EC2]"
                  >
                    Khám phá tour
                  </Link>
                }
              />
            ) : (
              <div className="relative">
                {featuredList.length > FEATURED_PAGE_SIZE && safeOffset > 0 && (
                  <button
                    type="button"
                    onClick={() => setCarouselOffset((prev) => Math.max(0, prev - 1))}
                    aria-label="Trượt sang trái"
                    className="hidden xl:inline-flex absolute -left-4 top-1/2 -translate-y-1/2 z-10 h-10 w-10 items-center justify-center rounded-full bg-white border border-slate-200 text-slate-800 shadow-[0_8px_22px_rgba(15,23,42,0.14)] hover:bg-[#1D63ED] hover:text-white hover:border-[#1D63ED] transition-colors cursor-pointer"
                  >
                    <ChevronLeft className="h-5 w-5" strokeWidth={1.9} />
                  </button>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  {visibleFeatured.map((schedule) => (
                    <TourCard
                      key={schedule.ma_lich_trinh}
                      item={schedule}
                      variant="featured"
                    />
                  ))}
                </div>

                {featuredList.length > FEATURED_PAGE_SIZE && safeOffset < maxOffset && (
                  <button
                    type="button"
                    onClick={() => setCarouselOffset((prev) => Math.min(maxOffset, prev + 1))}
                    aria-label="Trượt sang phải"
                    className="hidden xl:inline-flex absolute -right-4 top-1/2 -translate-y-1/2 z-10 h-10 w-10 items-center justify-center rounded-full bg-white border border-slate-200 text-slate-800 shadow-[0_8px_22px_rgba(15,23,42,0.14)] hover:bg-[#1D63ED] hover:text-white hover:border-[#1D63ED] transition-colors cursor-pointer"
                  >
                    <ChevronRight className="h-5 w-5" strokeWidth={1.9} />
                  </button>
                )}
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
