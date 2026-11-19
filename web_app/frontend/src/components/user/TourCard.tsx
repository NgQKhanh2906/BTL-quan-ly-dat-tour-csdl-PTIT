import { Link } from 'react-router-dom';
import { ArrowRight, Calendar, Clock, MapPin, Star, Users } from 'lucide-react';
import type { ScheduleSearchItem } from '../../api/types';
import { getTourImage, getTourImageAlt } from '../../constants/tourImages';
import { formatDate, formatDateTime, formatVnd } from '../../utils/format';

interface TourCardProps {
  item: ScheduleSearchItem;
  variant?: 'featured' | 'catalog';
}

export function TourCard({ item, variant = 'catalog' }: TourCardProps) {
  const imageSrc = getTourImage(item.ma_tour);
  const imageAlt = getTourImageAlt(item.ma_tour, item.ten_tour);
  const bookHref = `/book?schedule=${encodeURIComponent(item.ma_lich_trinh)}`;

  if (variant === 'featured') {
    return (
      <Link
        to={bookHref}
        className="group relative block aspect-[3/4] w-full overflow-hidden rounded-[20px] bg-slate-200 shadow-[var(--shadow-card)] hover:shadow-[0_16px_36px_rgba(15,23,42,0.16)] transition-shadow duration-300 focus-visible:outline-2"
      >
        <img
          src={imageSrc}
          alt={imageAlt}
          loading="lazy"
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        />

        {/* High-contrast bottom scrim */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-t from-slate-950/90 via-slate-950/35 to-slate-950/10"
        />

        {/* Top pills: seats + duration */}
        <div className="absolute top-3 left-3 right-3 flex items-center justify-between gap-1.5">
          <span className="inline-flex items-center gap-1 rounded-full bg-slate-950/55 backdrop-blur-md px-2.5 py-1 text-[11px] font-semibold text-white tabular-nums whitespace-nowrap">
            Còn {item.so_cho_con_lai} chỗ
          </span>
          <span className="inline-flex items-center rounded-full bg-white/90 backdrop-blur-md px-2.5 py-1 text-[11px] font-semibold text-slate-900 tabular-nums whitespace-nowrap">
            {item.so_ngay} ngày
          </span>
        </div>

        {/* Bottom info: full-width title + single-line price & compact rating pill */}
        <div className="absolute inset-x-0 bottom-0 p-3 space-y-1.5">
          <div>
            <p className="text-[11px] font-medium text-sky-100/95 truncate">
              {item.noi_den} · {formatDate(item.ngay_xuat_phat)}
            </p>
            <h3 className="mt-0.5 text-[14px] font-bold text-white leading-snug line-clamp-2">
              {item.ten_tour}
            </h3>
          </div>

          <div className="flex items-center justify-between gap-1.5 pt-0.5">
            <p className="text-[12px] font-semibold text-white/95 tabular-nums whitespace-nowrap tracking-[-0.01em]">
              Từ {formatVnd(item.gia_co_ban)}
            </p>

            <span className="shrink-0 inline-flex items-center gap-0.5 rounded-full bg-white px-2 py-0.5 text-[11px] font-bold text-slate-900 shadow-sm tabular-nums whitespace-nowrap">
              <Star
                className="h-3 w-3 fill-[#F59E0B] text-[#F59E0B] shrink-0"
                strokeWidth={1.75}
              />
              {item.diem_tb !== null ? item.diem_tb.toFixed(1) : 'Mới'}
            </span>
          </div>
        </div>
      </Link>
    );
  }

  return (
    <article className="group flex flex-col overflow-hidden rounded-[20px] border border-slate-200/80 bg-white shadow-[var(--shadow-card)] hover:shadow-[0_14px_34px_rgba(15,23,42,0.09)] transition-all duration-300">
      <Link to={bookHref} className="relative block aspect-[16/10] overflow-hidden bg-slate-100">
        <img
          src={imageSrc}
          alt={imageAlt}
          loading="lazy"
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-104"
        />
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 bg-gradient-to-t from-slate-950/45 via-transparent to-transparent"
        />

        <div className="absolute top-3 left-3 right-3 flex items-center justify-between gap-2">
          <span className="inline-flex items-center gap-1 rounded-full bg-white/92 backdrop-blur-md px-3 py-1 text-xs font-semibold text-slate-900 shadow-xs">
            <MapPin className="h-3.5 w-3.5 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
            <span>{item.noi_di}</span>
            <ArrowRight className="h-3 w-3 text-slate-400 shrink-0" strokeWidth={2} />
            <span>{item.noi_den}</span>
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-white/95 backdrop-blur-md px-2.5 py-1 text-xs font-bold text-slate-900 shadow-xs tabular-nums">
            <Star
              className="h-3.5 w-3.5 fill-[#F59E0B] text-[#F59E0B]"
              strokeWidth={1.75}
            />
            {item.diem_tb !== null ? item.diem_tb.toFixed(1) : 'Mới'}
          </span>
        </div>

        <div className="absolute bottom-3 left-3 flex items-center gap-2">
          <span className="inline-flex items-center gap-1 rounded-full bg-slate-950/60 backdrop-blur-md px-2.5 py-1 text-[11px] font-semibold text-white tabular-nums">
            <Clock className="h-3 w-3" strokeWidth={1.75} />
            {item.so_ngay} ngày
          </span>
          <span className="inline-flex items-center gap-1 rounded-full bg-slate-950/60 backdrop-blur-md px-2.5 py-1 text-[11px] font-semibold text-white tabular-nums">
            <Users className="h-3 w-3" strokeWidth={1.75} />
            Còn {item.so_cho_con_lai} chỗ
          </span>
        </div>
      </Link>

      <div className="flex flex-1 flex-col p-5">
        <div className="flex items-center justify-between gap-2 text-xs text-slate-500">
          <span className="inline-flex items-center gap-1.5 font-medium text-slate-600 tabular-nums">
            <Calendar className="h-3.5 w-3.5 text-[#1D63ED]" strokeWidth={1.75} />
            {formatDateTime(item.ngay_xuat_phat)}
          </span>
          <span className="text-slate-400 tabular-nums">{item.ma_lich_trinh}</span>
        </div>

        <h3 className="mt-2 text-base font-bold text-slate-900 leading-snug line-clamp-2 group-hover:text-[#1D63ED] transition-colors">
          <Link to={bookHref}>{item.ten_tour}</Link>
        </h3>

        {item.mo_ta && (
          <p className="mt-1.5 text-sm text-slate-600 line-clamp-2 leading-relaxed">
            {item.mo_ta}
          </p>
        )}

        <div className="mt-auto pt-4 border-t border-slate-100 flex items-end justify-between gap-3">
          <div>
            <p className="text-[11px] font-medium text-slate-500">Giá cơ bản / khách</p>
            <p className="text-lg font-bold text-[#1D63ED] tabular-nums leading-tight whitespace-nowrap">
              {formatVnd(item.gia_co_ban)}
            </p>
            {item.so_luot_danh_gia > 0 && (
              <p className="text-[11px] text-slate-500 tabular-nums mt-0.5">
                {item.so_luot_danh_gia} lượt đánh giá
              </p>
            )}
          </div>

          <Link
            to={bookHref}
            className="inline-flex items-center gap-1.5 rounded-full bg-[#1D63ED] px-4 py-2.5 text-xs font-semibold text-white shadow-[0_8px_18px_rgba(29,99,237,0.22)] hover:bg-[#154EC2] transition-colors shrink-0"
          >
            <span>Đặt tour này</span>
            <ArrowRight className="h-3.5 w-3.5" strokeWidth={1.9} />
          </Link>
        </div>
      </div>
    </article>
  );
}
