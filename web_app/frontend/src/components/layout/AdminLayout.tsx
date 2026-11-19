import { useEffect, useState } from 'react';
import { Link, Navigate, NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  BarChart3,
  ClipboardList,
  FileText,
  LogOut,
  Menu,
  X,
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { getInitials } from '../../utils/format';
import { BrandLogo } from '../common/BrandLogo';

const ADMIN_NAV = [
  {
    to: '/admin/dashboard',
    label: 'Tổng quan & Báo cáo',
    icon: BarChart3,
  },
  {
    to: '/admin/orders',
    label: 'Quản lý đơn hàng',
    icon: ClipboardList,
  },
  {
    to: '/admin/confirmations',
    label: 'Phiếu xác nhận',
    icon: FileText,
  },
];

const ROUTE_TITLES: Record<string, string> = {
  '/admin/dashboard': 'Tổng quan & Báo cáo doanh thu',
  '/admin/orders': 'Quản lý đơn hàng',
  '/admin/confirmations': 'Xuất phiếu xác nhận đặt tour',
};

export function AdminLayout() {
  const { admin, adminToken, logoutAdmin } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    setSidebarOpen(false);
  }, [location.pathname]);

  if (!admin || !adminToken) {
    return <Navigate to="/admin/login" replace state={{ from: location.pathname }} />;
  }

  const pageTitle = ROUTE_TITLES[location.pathname] ?? 'Cổng điều hành';

  const handleLogout = () => {
    logoutAdmin();
    navigate('/admin/login', { replace: true });
  };

  const sidebarContent = (
    <div className="flex h-full flex-col bg-[#0F172A] text-slate-100">
      <div className="flex items-center justify-between px-5 h-18 border-b border-slate-800/90 shrink-0">
        <Link to="/admin/dashboard" className="focus-visible:outline-2 rounded-xl">
          <BrandLogo variant="admin" size="sm" />
        </Link>
        <button
          type="button"
          onClick={() => setSidebarOpen(false)}
          aria-label="Đóng thanh điều hướng"
          className="lg:hidden inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white cursor-pointer"
        >
          <X className="h-4.5 w-4.5" strokeWidth={1.75} />
        </button>
      </div>

      <nav className="flex-1 px-3 py-5 space-y-1.5 overflow-y-auto" aria-label="Điều hướng quản trị">
        {ADMIN_NAV.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                [
                  'flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-medium transition-colors duration-150',
                  isActive
                    ? 'bg-[#1D63ED] text-white shadow-[0_6px_16px_rgba(29,99,237,0.35)] font-semibold'
                    : 'text-slate-300 hover:bg-[#1E293B] hover:text-white',
                ].join(' ')
              }
            >
              <Icon className="h-4.5 w-4.5 shrink-0" strokeWidth={1.75} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="p-3.5 border-t border-slate-800/90 space-y-2.5 shrink-0">
        <div className="flex items-center gap-3 rounded-xl bg-slate-800/60 px-3 py-2.5">
          <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#1D63ED]/25 text-xs font-bold text-[#93C5FD]">
            {getInitials(admin.staff_name)}
          </span>
          <div className="min-w-0">
            <p className="text-sm font-semibold text-white truncate">{admin.staff_name}</p>
            <p className="text-xs text-slate-400 truncate">Điều hành · {admin.username}</p>
          </div>
        </div>

        <Link
          to="/"
          className="flex items-center gap-2.5 rounded-xl px-3 py-2 text-xs font-medium text-slate-300 hover:bg-[#1E293B] hover:text-white transition-colors"
        >
          <ArrowLeft className="h-4 w-4" strokeWidth={1.75} />
          Về trang Khách hàng
        </Link>

        <button
          type="button"
          onClick={handleLogout}
          className="w-full flex items-center gap-2.5 rounded-xl px-3 py-2 text-xs font-medium text-red-300 hover:bg-red-950/50 hover:text-red-200 transition-colors cursor-pointer"
        >
          <LogOut className="h-4 w-4" strokeWidth={1.75} />
          Đăng xuất
        </button>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900">
      {/* Desktop fixed sidebar */}
      <aside className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-30 lg:block lg:w-[260px]">
        {sidebarContent}
      </aside>

      {/* Mobile slide-over sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden flex">
          <div
            className="fixed inset-0 bg-slate-950/55 backdrop-blur-[1px]"
            onClick={() => setSidebarOpen(false)}
          />
          <aside className="relative z-10 w-[260px] max-w-[85vw] h-full shadow-2xl">
            {sidebarContent}
          </aside>
        </div>
      )}

      {/* Main content area */}
      <div className="lg:pl-[260px] flex min-h-screen flex-col">
        <header className="sticky top-0 z-20 h-16 bg-white/95 backdrop-blur-md border-b border-slate-200 px-4 sm:px-6 lg:px-8 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <button
              type="button"
              onClick={() => setSidebarOpen(true)}
              aria-label="Mở thanh điều hướng"
              className="lg:hidden inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-50 cursor-pointer"
            >
              <Menu className="h-5 w-5" strokeWidth={1.75} />
            </button>
            <h1 className="text-base sm:text-lg font-bold text-slate-900 truncate">{pageTitle}</h1>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <span className="hidden sm:inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700">
              <span className="h-2 w-2 rounded-full bg-emerald-500" aria-hidden="true" />
              {admin.staff_name}
            </span>
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-[1440px] w-full mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
