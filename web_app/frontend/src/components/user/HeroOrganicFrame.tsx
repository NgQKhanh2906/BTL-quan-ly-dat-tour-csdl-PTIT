import { useEffect, useId, useState } from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowDown, Star, Users } from 'lucide-react';
import type { LandingStats } from '../../api/types';
import { HERO_IMAGE } from '../../constants/tourImages';

interface HeroOrganicFrameProps {
  stats: LandingStats | null;
  onExploreHighlight: () => void;
}

const TRAVELER_AVATARS = [
  { initials: 'NA', bg: 'bg-[#1D63ED] text-white' },
  { initials: 'TB', bg: 'bg-[#0EA5E9] text-white' },
  { initials: 'LC', bg: 'bg-[#10B981] text-white' },
  { initials: 'PM', bg: 'bg-[#F59E0B] text-white' },
];

function useIsDesktop(): boolean {
  const [isDesktop, setIsDesktop] = useState<boolean>(() => {
    if (typeof window === 'undefined') return true;
    return window.matchMedia('(min-width: 1024px)').matches;
  });

  useEffect(() => {
    const media = window.matchMedia('(min-width: 1024px)');
    const handleChange = (event: MediaQueryListEvent) => setIsDesktop(event.matches);
    setIsDesktop(media.matches);
    media.addEventListener('change', handleChange);
    return () => media.removeEventListener('change', handleChange);
  }, []);

  return isDesktop;
}

export function HeroOrganicFrame({ stats, onExploreHighlight }: HeroOrganicFrameProps) {
  const uid = useId().replace(/:/g, '');
  const clipId = `hero-organic-clip-${uid}`;
  const arcTextId = `hero-arc-text-${uid}`;
  const prefersReducedMotion = useReducedMotion();
  const isDesktop = useIsDesktop();

  const travelersCount = stats ? stats.total_travelers_served : null;
  const avgRating = stats?.avg_rating ?? null;
  const totalReviews = stats?.total_reviews ?? 0;

  return (
    <motion.div
      initial={prefersReducedMotion ? false : { opacity: 0.01, scale: 0.985 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.55, ease: [0.22, 1, 0.36, 1] }}
      className="relative w-full"
    >
      {isDesktop ? (
        <>
          {/* Hidden SVG clipPath definition for smooth organic wave silhouette */}
          <svg
            width="0"
            height="0"
            aria-hidden="true"
            className="absolute pointer-events-none"
          >
            <defs>
              <clipPath id={clipId} clipPathUnits="objectBoundingBox">
                <path d="M 0.38 0 C 0.30 0.13, 0.18 0.13, 0.09 0.25 C 0.005 0.37, 0.005 0.61, 0.075 0.78 C 0.145 0.94, 0.31 0.99, 0.51 0.95 C 0.70 0.91, 0.87 0.99, 0.965 0.89 C 0.995 0.85, 1.00 0.78, 1.00 0.68 L 1.00 0.055 C 1.00 0.02, 0.98 0, 0.945 0 Z" />
              </clipPath>
            </defs>
          </svg>

          {/* Soft cobalt ambient glow behind curve (desktop) */}
          <div
            aria-hidden="true"
            className="absolute -inset-x-4 -inset-y-3 rounded-[48px] bg-gradient-to-tr from-[#DBEAFE]/65 via-[#EFF6FF]/40 to-transparent blur-2xl -z-10"
          />

          {/* Desktop Organic Clipped Photo */}
          <div className="relative h-[475px] xl:h-[515px] w-full">
            <div
              className="h-full w-full overflow-hidden bg-slate-200"
              style={{ clipPath: `url(#${clipId})` }}
            >
              <img
                src={HERO_IMAGE}
                alt="Toàn cảnh Vịnh Hạ Long xanh trong nắng sớm miền Bắc Việt Nam"
                loading="eager"
                className="h-full w-full object-cover object-center scale-[1.01]"
              />
              {/* Subtle atmospheric highlight to ensure crisp overlay readability */}
              <div
                aria-hidden="true"
                className="pointer-events-none absolute inset-0 bg-gradient-to-tr from-slate-950/20 via-transparent to-sky-900/10"
              />
            </div>

            {/* Frosted Glass Real-DB Stats Card (upper right inside photo) */}
            <motion.div
              initial={prefersReducedMotion ? false : { opacity: 0.01, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.45, delay: 0.18, ease: [0.22, 1, 0.36, 1] }}
              className="absolute top-6 right-5 xl:right-7 w-[204px] rounded-[22px] bg-white/88 backdrop-blur-md border border-white/80 p-4 shadow-[var(--shadow-glass)]"
            >
              <div className="flex items-center justify-between gap-2">
                <div className="flex -space-x-2">
                  {TRAVELER_AVATARS.slice(0, 2).map((av) => (
                    <span
                      key={av.initials}
                      className={`inline-flex h-8 w-8 items-center justify-center rounded-full border-2 border-white text-[11px] font-bold ${av.bg}`}
                    >
                      {av.initials}
                    </span>
                  ))}
                </div>
                <span className="inline-flex h-9 min-w-11 px-2.5 items-center justify-center rounded-full bg-[#1D63ED] text-xs font-bold text-white tabular-nums shadow-[0_6px_14px_rgba(29,99,237,0.3)]">
                  {travelersCount !== null ? `${travelersCount}+` : '—'}
                </span>
              </div>

              <div className="mt-3">
                <p className="text-sm font-bold text-slate-900 leading-tight">
                  Khách đã đồng hành
                </p>
                <div className="mt-1 flex items-center gap-1.5 text-xs text-slate-600">
                  {avgRating !== null ? (
                    <>
                      <Star
                        className="h-3.5 w-3.5 fill-[#F59E0B] text-[#F59E0B] shrink-0"
                        strokeWidth={1.75}
                      />
                      <span className="font-semibold text-slate-800 tabular-nums">
                        {avgRating.toFixed(1)}/5
                      </span>
                      <span className="text-slate-500 tabular-nums">({totalReviews} đánh giá)</span>
                    </>
                  ) : (
                    <>
                      <Users className="h-3.5 w-3.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                      <span>Hành trình miền Bắc</span>
                    </>
                  )}
                </div>
              </div>

              <div className="mt-3 pt-2.5 border-t border-slate-200/70 flex items-center justify-between">
                <div className="flex -space-x-1.5">
                  {TRAVELER_AVATARS.map((av) => (
                    <span
                      key={av.initials}
                      className={`inline-flex h-6 w-6 items-center justify-center rounded-full border border-white text-[9px] font-bold ${av.bg}`}
                    >
                      {av.initials}
                    </span>
                  ))}
                </div>
                <svg
                  viewBox="0 0 46 10"
                  fill="none"
                  className="h-2.5 w-11 text-[#1D63ED]"
                  aria-hidden="true"
                >
                  <path
                    d="M1 6.5C8 2 16 9 23 5C30 1 38 8 45 4"
                    stroke="currentColor"
                    strokeWidth="1.6"
                    strokeLinecap="round"
                  />
                </svg>
              </div>
            </motion.div>

            {/* Interactive Circular Action Button straddling lower-left organic curve */}
            <motion.button
              type="button"
              onClick={onExploreHighlight}
              initial={prefersReducedMotion ? false : { opacity: 0.01, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.45, delay: 0.25, ease: [0.22, 1, 0.36, 1] }}
              aria-label="Xem danh sách điểm đến nổi bật"
              className="group absolute left-[-24px] bottom-[96px] z-20 flex h-28 w-28 items-center justify-center rounded-full bg-[#EFF5FF]/80 backdrop-blur-md border border-white/80 shadow-[0_14px_34px_rgba(15,23,42,0.10)] cursor-pointer transition-transform duration-300 hover:scale-105"
            >
              <svg
                viewBox="0 0 112 112"
                className="absolute inset-0 h-full w-full pointer-events-none"
                aria-hidden="true"
              >
                <defs>
                  <path
                    id={arcTextId}
                    d="M 56,56 m -40,0 a 40,40 0 1,1 80,0"
                  />
                </defs>
                <text
                  fill="#334155"
                  fontSize="8.3"
                  fontWeight="600"
                  letterSpacing="1.35"
                >
                  <textPath href={`#${arcTextId}`} startOffset="50%" textAnchor="middle">
                    ĐIỂM ĐẾN NỔI BẬT
                  </textPath>
                </text>
              </svg>
              <span className="relative flex h-13 w-13 items-center justify-center rounded-full bg-white text-slate-900 shadow-[0_8px_20px_rgba(15,23,42,0.14)] group-hover:bg-[#1D63ED] group-hover:text-white transition-colors duration-200">
                <ArrowDown
                  className="h-5 w-5 transition-transform duration-200 group-hover:translate-y-0.5"
                  strokeWidth={1.85}
                />
              </span>
            </motion.button>
          </div>
        </>
      ) : (
        /* Mobile & Tablet Responsive Rounded Photo Card */
        <div className="relative rounded-[28px] overflow-hidden aspect-[16/11] bg-slate-200 shadow-[var(--shadow-floating)]">
          <img
            src={HERO_IMAGE}
            alt="Toàn cảnh Vịnh Hạ Long xanh trong nắng sớm miền Bắc Việt Nam"
            loading="eager"
            className="h-full w-full object-cover"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 bg-gradient-to-t from-slate-950/35 via-transparent to-transparent"
          />
          <div className="absolute top-3.5 right-3.5 rounded-2xl bg-white/90 backdrop-blur-md border border-white/80 px-3.5 py-2.5 shadow-[var(--shadow-glass)]">
            <div className="flex items-center gap-2">
              <span className="inline-flex h-7 px-2.5 items-center justify-center rounded-full bg-[#1D63ED] text-xs font-bold text-white tabular-nums">
                {travelersCount !== null ? `${travelersCount}+` : '—'}
              </span>
              <div>
                <p className="text-xs font-bold text-slate-900 leading-tight">Khách đã đồng hành</p>
                {avgRating !== null && (
                  <p className="text-[11px] font-semibold text-slate-600 inline-flex items-center gap-1 tabular-nums">
                    <Star className="h-3 w-3 fill-[#F59E0B] text-[#F59E0B]" strokeWidth={1.75} />
                    {avgRating.toFixed(1)}/5 ({totalReviews})
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </motion.div>
  );
}
