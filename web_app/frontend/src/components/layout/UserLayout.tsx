import { useEffect, useRef, useState } from 'react';
import { Link, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { motion, useReducedMotion } from 'framer-motion';
import {
  CalendarCheck,
  ChevronDown,
  LogOut,
  Mail,
  MapPin,
  Menu,
  Phone,
  ShieldCheck,
  User,
  X,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { getInitials } from '../../utils/format';
import { BrandLogo } from '../common/BrandLogo';
import { Button } from '../common/Button';
import { CustomerLoginModal } from './CustomerLoginModal';

const NAV_ITEMS = [
  { to: '/', label: 'Trang chủ', end: true },
  { to: '/explore', label: 'Khám phá tour', end: false },
  { to: '/book', label: 'Đặt tour', end: false },
  { to: '/my-bookings', label: 'Đơn của tôi', end: false },
];

export function UserLayout() {
  const { customer, logoutCustomer, openCustomerLoginModal } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const prefersReducedMotion = useReducedMotion();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [accountMenuOpen, setAccountMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const accountMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMobileMenuOpen(false);
    setAccountMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'auto' });
  }, [location.pathname, location.search]);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    if (!accountMenuOpen) return;
    const handleClickOutside = (event: MouseEvent) => {
      if (accountMenuRef.current && !accountMenuRef.current.contains(event.target as Node)) {
        setAccountMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [accountMenuOpen]);

  return (
    <div className="min-h-screen flex flex-col bg-[#F7FAFF] text-slate-900">
      <header
        className={[
          'sticky top-0 z-40 transition-all duration-200',
          scrolled
            ? 'bg-white/92 backdrop-blur-md border-b border-slate-200/80 shadow-[0_4px_20px_rgba(15,23,42,0.04)]'
            : 'bg-[#F7FAFF]/85 backdrop-blur-sm border-b border-transparent',
        ].join(' ')}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 flex items-center justify-between gap-4">
          <Link to="/" className="shrink-0 focus-visible:outline-2 rounded-xl">
            <BrandLogo variant="user" />
          </Link>

          <nav className="hidden md:flex items-center gap-8" aria-label="Điều hướng chính">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  [
                    'relative py-2 text-sm font-medium transition-colors duration-200',
                    isActive
                      ? 'text-slate-950 font-semibold'
                      : 'text-slate-600 hover:text-[#1D63ED]',
                  ].join(' ')
                }
              >
                {({ isActive }) => (
                  <>
                    <span>{item.label}</span>
                    {isActive && (
                      <span
                        className="absolute left-1/2 -bottom-0.5 -translate-x-1/2 h-1.5 w-1.5 rounded-full bg-[#1D63ED]"
                        aria-hidden="true"
                      />
                    )}
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-2.5">
            {customer ? (
              <div className="relative" ref={accountMenuRef}>
                <button
                  type="button"
                  onClick={() => setAccountMenuOpen((prev) => !prev)}
                  className="inline-flex items-center gap-2.5 rounded-full border border-slate-200 bg-white pl-1.5 pr-3.5 py-1.5 text-sm font-semibold text-slate-800 shadow-[0_2px_10px_rgba(15,23,42,0.05)] hover:border-slate-300 transition-colors cursor-pointer"
                  aria-expanded={accountMenuOpen}
                >
                  <span className="inline-flex h-7 w-7 items-center justify-center rounded-full bg-[#1D63ED] text-xs font-bold text-white">
                    {getInitials(customer.ho_ten)}
                  </span>
                  <span className="max-w-[140px] truncate">{customer.ho_ten}</span>
                  <ChevronDown
                    className={`h-4 w-4 text-slate-400 transition-transform duration-200 ${
                      accountMenuOpen ? 'rotate-180' : ''
                    }`}
                    strokeWidth={1.75}
                  />
                </button>

                {accountMenuOpen && (
                  <div className="absolute right-0 mt-2 w-60 rounded-2xl border border-slate-200/90 bg-white p-2 shadow-[0_16px_40px_rgba(15,23,42,0.12)] z-50">
                    <div className="px-3 py-2 border-b border-slate-100">
                      <p className="text-sm font-bold text-slate-900 truncate">{customer.ho_ten}</p>
                      <p className="text-xs text-slate-500 truncate">{customer.email}</p>
                    </div>
                    <div className="py-1">
                      <Link
                        to="/my-bookings"
                        className="flex items-center gap-2.5 rounded-xl px-3 py-2 text-sm font-medium text-slate-700 hover:bg-[#F7FAFF] hover:text-[#1D63ED] transition-colors"
                      >
                        <CalendarCheck className="h-4 w-4" strokeWidth={1.75} />
                        Đơn hàng của tôi
                      </Link>
                      <Link
                        to="/admin/login"
                        className="flex items-center gap-2.5 rounded-xl px-3 py-2 text-sm font-medium text-slate-700 hover:bg-[#F7FAFF] hover:text-[#1D63ED] transition-colors"
                      >
                        <ShieldCheck className="h-4 w-4" strokeWidth={1.75} />
                        Chuyển sang Quản trị
                      </Link>
                    </div>
                    <div className="pt-1 border-t border-slate-100">
                      <button
                        type="button"
                        onClick={() => {
                          logoutCustomer();
                          setAccountMenuOpen(false);
                        }}
                        className="w-full flex items-center gap-2.5 rounded-xl px-3 py-2 text-sm font-medium text-[#B91C1C] hover:bg-red-50 transition-colors cursor-pointer"
                      >
                        <LogOut className="h-4 w-4" strokeWidth={1.75} />
                        Đăng xuất
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <>
                <Link
                  to="/admin/login"
                  className="inline-flex items-center gap-1.5 rounded-full px-3.5 py-2 text-sm font-medium text-slate-600 hover:bg-white hover:text-slate-900 transition-colors"
                >
                  <ShieldCheck className="h-4 w-4 text-slate-500" strokeWidth={1.75} />
                  Quản trị
                </Link>
                <Button
                  variant="primary"
                  size="sm"
                  shape="pill"
                  leftIcon={<User className="h-3.5 w-3.5" strokeWidth={1.75} />}
                  onClick={openCustomerLoginModal}
                >
                  Đăng nhập
                </Button>
              </>
            )}
          </div>

          <button
            type="button"
            onClick={() => setMobileMenuOpen((prev) => !prev)}
            aria-label={mobileMenuOpen ? 'Đóng menu điều hướng' : 'Mở menu điều hướng'}
            className="md:hidden inline-flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 bg-white text-slate-700 shadow-xs cursor-pointer"
          >
            {mobileMenuOpen ? (
              <X className="h-5 w-5" strokeWidth={1.75} />
            ) : (
              <Menu className="h-5 w-5" strokeWidth={1.75} />
            )}
          </button>
        </div>

        {mobileMenuOpen && (
          <div className="md:hidden border-t border-slate-200/80 bg-white px-4 pt-3 pb-5 shadow-lg">
            <nav className="flex flex-col gap-1" aria-label="Điều hướng di động">
              {NAV_ITEMS.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  end={item.end}
                  className={({ isActive }) =>
                    [
                      'rounded-xl px-3.5 py-2.5 text-sm font-semibold transition-colors',
                      isActive
                        ? 'bg-[#EFF5FF] text-[#1D63ED]'
                        : 'text-slate-700 hover:bg-slate-50',
                    ].join(' ')
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>

            <div className="mt-4 pt-4 border-t border-slate-100 space-y-2.5">
              {customer ? (
                <>
                  <div className="flex items-center gap-3 px-2">
                    <span className="inline-flex h-9 w-9 items-center justify-center rounded-full bg-[#1D63ED] text-xs font-bold text-white">
                      {getInitials(customer.ho_ten)}
                    </span>
                    <div className="min-w-0">
                      <p className="text-sm font-bold text-slate-900 truncate">{customer.ho_ten}</p>
                      <p className="text-xs text-slate-500 truncate">{customer.email}</p>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      shape="pill"
                      className="flex-1"
                      onClick={() => navigate('/admin/login')}
                    >
                      Quản trị
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      shape="pill"
                      className="flex-1 text-[#B91C1C]"
                      onClick={logoutCustomer}
                    >
                      Đăng xuất
                    </Button>
                  </div>
                </>
              ) : (
                <div className="flex gap-2">
                  <Button
                    variant="primary"
                    size="sm"
                    shape="pill"
                    className="flex-1"
                    onClick={() => {
                      setMobileMenuOpen(false);
                      openCustomerLoginModal();
                    }}
                  >
                    Đăng nhập
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    shape="pill"
                    className="flex-1"
                    onClick={() => navigate('/admin/login')}
                  >
                    Quản trị
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}
      </header>

      <main className="flex-1">
        <motion.div
          key={location.pathname}
          initial={prefersReducedMotion ? false : { opacity: 0.01, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.24, ease: [0.22, 1, 0.36, 1] }}
        >
          <Outlet />
        </motion.div>
      </main>

      <footer className="mt-16 border-t border-slate-200/80 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
            <div className="md:col-span-5 space-y-3">
              <BrandLogo variant="user" />
              <p className="text-sm text-slate-600 leading-relaxed max-w-sm">
                Đồng hành cùng những hành trình khám phá vẻ đẹp miền Bắc — từ vịnh di sản Hạ Long,
                mây trời Sa Pa đến đèo núi Hà Giang.
              </p>
            </div>

            <div className="md:col-span-3 space-y-2.5">
              <h3 className="text-sm font-bold text-slate-900">Khám phá</h3>
              <ul className="space-y-2 text-sm text-slate-600">
                <li>
                  <Link to="/explore" className="hover:text-[#1D63ED] transition-colors">
                    Tất cả lịch trình
                  </Link>
                </li>
                <li>
                  <Link
                    to="/explore?gia_tu=10000000"
                    className="hover:text-[#1D63ED] transition-colors"
                  >
                    Hành trình cao cấp
                  </Link>
                </li>
                <li>
                  <Link to="/book" className="hover:text-[#1D63ED] transition-colors">
                    Đặt tour trực tuyến
                  </Link>
                </li>
                <li>
                  <Link to="/my-bookings" className="hover:text-[#1D63ED] transition-colors">
                    Đơn hàng của tôi
                  </Link>
                </li>
              </ul>
            </div>

            <div className="md:col-span-4 space-y-2.5">
              <h3 className="text-sm font-bold text-slate-900">Liên hệ</h3>
              <ul className="space-y-2 text-sm text-slate-600">
                <li className="flex items-start gap-2">
                  <MapPin className="h-4 w-4 text-[#1D63ED] mt-0.5 shrink-0" strokeWidth={1.75} />
                  <span>Số 10 Nguyễn Trãi, Hà Đông, Hà Nội</span>
                </li>
                <li className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                  <span className="tabular-nums">1900 6868</span>
                </li>
                <li className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-[#1D63ED] shrink-0" strokeWidth={1.75} />
                  <span>lienhe@bacviettravel.vn</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="mt-8 pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500">
            <span>© 2026 Bắc Việt Travel. Giữ trọn trải nghiệm du lịch miền Bắc.</span>
            <Link to="/admin/login" className="hover:text-[#1D63ED] transition-colors">
              Cổng điều hành nội bộ
            </Link>
          </div>
        </div>
      </footer>

      <CustomerLoginModal />
    </div>
  );
}
