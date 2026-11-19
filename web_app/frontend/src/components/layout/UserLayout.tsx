import { useEffect, useState } from 'react';
import { Link, NavLink, Outlet, useLocation } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import { Menu, X } from 'lucide-react';
import { BrandLogo } from '../common/BrandLogo';

const NAV_ITEMS = [
  { to: '/', label: 'Tổng quan', end: true },
  { to: '/explore', label: 'Tra cứu lịch trình', end: false },
  { to: '/book', label: 'Đặt tour', end: false },
  { to: '/orders', label: 'Quản lý & Hủy đơn', end: false },
  { to: '/reviews', label: 'Đánh giá chuyến đi', end: false },
  { to: '/confirmations', label: 'Phiếu xác nhận', end: false },
  { to: '/reports', label: 'Báo cáo doanh thu', end: false },
];

export function UserLayout() {
  const location = useLocation();
  const prefersReducedMotion = useReducedMotion();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, [location.pathname, location.search]);

  return (
    <div className="min-h-screen flex flex-col bg-[#F8FAFC] text-slate-900">
      <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
          <Link to="/" className="shrink-0 focus-visible:outline-2 rounded-lg">
            <BrandLogo variant="user" size="sm" />
          </Link>

          <nav className="hidden xl:flex items-center gap-1" aria-label="Điều hướng chính">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  [
                    'relative rounded-lg px-3 py-2 text-sm font-medium transition-colors duration-150 whitespace-nowrap',
                    isActive
                      ? 'bg-[#EFF6FF] text-[#1D63ED] font-semibold'
                      : 'text-slate-600 hover:bg-slate-100/80 hover:text-slate-900',
                  ].join(' ')
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="hidden lg:flex items-center gap-2 text-xs font-semibold text-slate-600 bg-slate-100/80 px-3 py-1.5 rounded-full border border-slate-200 whitespace-nowrap shrink-0">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            <span>Hệ thống trực tuyến</span>
          </div>

          <button
            type="button"
            onClick={() => setMobileMenuOpen((prev) => !prev)}
            aria-label={mobileMenuOpen ? 'Đóng menu điều hướng' : 'Mở menu điều hướng'}
            className="xl:hidden inline-flex h-9.5 w-9.5 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-700 cursor-pointer"
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" strokeWidth={1.75} />
            ) : (
              <Menu className="h-5 w-5" strokeWidth={1.75} />
            )}
          </button>
        </div>

        {mobileMenuOpen && (
          <div className="xl:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-4 shadow-md">
            <nav className="flex flex-col gap-1" aria-label="Điều hướng di động">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    [
                      'rounded-lg px-3.5 py-2.5 text-sm font-semibold transition-colors',
                      isActive
                        ? 'bg-[#EFF6FF] text-[#1D63ED]'
                        : 'text-slate-700 hover:bg-slate-50',
                    ].join(' ')
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>
        )}
      </header>

      <main className="flex-1">
        <motion.div
          key={location.pathname}
          initial={prefersReducedMotion ? false : { opacity: 0.01, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
        >
          <Outlet />
        </motion.div>
      </main>

      <footer className="mt-12 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
          <span>Bắc Việt Travel · Hệ thống quản lý đặt tour du lịch miền Bắc</span>
          <span>Bài tập lớn Cơ sở dữ liệu</span>
        </div>
      </footer>
    </div>
  );
}
