import { useState, type FormEvent } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import {
  AlertCircle,
  ArrowLeft,
  BarChart3,
  ClipboardList,
  Eye,
  EyeOff,
  FileText,
  KeyRound,
  Lock,
  Sparkles,
  User,
  UserCheck,
} from 'lucide-react';
import { ApiError } from '../../api/client';
import { BrandLogo } from '../../components/common/BrandLogo';
import { Button } from '../../components/common/Button';
import { useAuth } from '../../context/AuthContext';

interface LocationState {
  from?: string;
}

const OPERATIONS_HIGHLIGHTS = [
  {
    icon: BarChart3,
    title: 'Báo cáo doanh thu & chất lượng',
    desc: 'Theo dõi doanh thu dịch vụ, phí phạt hủy, đánh giá lưu trú và xuất báo cáo A4 ngang.',
  },
  {
    icon: ClipboardList,
    title: 'Điều phối & xử lý đơn hàng',
    desc: 'Cập nhật trạng thái thanh toán, hoàn thành chuyến đi và xử lý hủy đơn minh bạch.',
  },
  {
    icon: FileText,
    title: 'Phát hành phiếu xác nhận PDF',
    desc: 'Xem trước biểu mẫu chuẩn khổ A4 dọc, in trực tiếp hoặc tải file PDF gửi khách hàng.',
  },
];

export function AdminLoginPage() {
  const { admin, adminToken, loginAdmin } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const state = location.state as LocationState | null;
  const redirectTo =
    state?.from && state.from.startsWith('/admin') && state.from !== '/admin/login'
      ? state.from
      : '/admin/dashboard';

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [staffName, setStaffName] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (admin && adminToken) {
    return <Navigate to={redirectTo} replace />;
  }

  const handleFillDemo = () => {
    setUsername('admin');
    setPassword('admin123');
    setStaffName((prev) => (prev.trim() ? prev : 'Nguyễn Quốc Khánh'));
    setError(null);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);

    if (!username.trim() || !password) {
      setError('Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.');
      return;
    }

    setSubmitting(true);
    try {
      await loginAdmin(username.trim(), password, staffName.trim() || undefined);
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'Không thể đăng nhập vào cổng điều hành. Vui lòng thử lại.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col lg:flex-row">
      {/* Left dark-slate brand & operations column */}
      <div className="relative bg-[#0F172A] text-slate-100 lg:w-[46%] xl:w-[44%] flex flex-col justify-between p-6 sm:p-10 lg:p-12 overflow-hidden">
        {/* Subtle architectural grid lines */}
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.06]"
          style={{
            backgroundImage:
              'linear-gradient(to right, #94A3B8 1px, transparent 1px), linear-gradient(to bottom, #94A3B8 1px, transparent 1px)',
            backgroundSize: '40px 40px',
          }}
          aria-hidden="true"
        />

        <div className="relative z-10">
          <div className="flex items-center justify-between gap-4">
            <Link to="/" className="focus-visible:outline-2 rounded-xl">
              <BrandLogo variant="admin" size="md" />
            </Link>
            <Link
              to="/"
              className="lg:hidden inline-flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-800/70 px-3 py-1.5 text-xs font-medium text-slate-200 hover:bg-slate-800 hover:text-white transition-colors"
            >
              <ArrowLeft className="h-3.5 w-3.5" strokeWidth={1.75} />
              Trang khách
            </Link>
          </div>

          <div className="mt-10 lg:mt-16 max-w-md">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white leading-snug">
              Trung tâm điều hành &amp; quản trị đặt tour
            </h1>
            <p className="mt-3 text-sm text-slate-300 leading-relaxed">
              Không gian làm việc dành riêng cho nhân viên điều hành Bắc Việt Travel: quản lý đơn đặt chỗ, theo dõi doanh thu và phát hành chứng từ PDF khổ A4.
            </p>
          </div>

          <ul className="mt-8 hidden lg:space-y-4 lg:block max-w-md">
            {OPERATIONS_HIGHLIGHTS.map((item) => {
              const Icon = item.icon;
              return (
                <li
                  key={item.title}
                  className="flex items-start gap-3.5 rounded-xl border border-slate-800 bg-slate-900/65 p-4"
                >
                  <span
                    className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-[#1D63ED]/20 text-[#93C5FD]"
                    aria-hidden="true"
                  >
                    <Icon className="h-4.5 w-4.5" strokeWidth={1.75} />
                  </span>
                  <div className="min-w-0">
                    <p className="text-sm font-semibold text-white">{item.title}</p>
                    <p className="mt-0.5 text-xs text-slate-400 leading-relaxed">
                      {item.desc}
                    </p>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>

        <div className="relative z-10 mt-8 hidden lg:flex items-center justify-between border-t border-slate-800 pt-6 text-xs text-slate-400">
          <span>Bắc Việt Travel · Hệ thống Điều hành nội bộ</span>
          <Link
            to="/"
            className="inline-flex items-center gap-1.5 font-medium text-slate-300 hover:text-white transition-colors"
          >
            <ArrowLeft className="h-3.5 w-3.5" strokeWidth={1.75} />
            Về trang Khách hàng
          </Link>
        </div>
      </div>

      {/* Right login form column */}
      <div className="flex-1 flex items-center justify-center p-6 sm:p-10 lg:p-14">
        <div className="w-full max-w-[440px]">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-[0_10px_32px_rgba(15,23,42,0.06)]">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold text-slate-900">Đăng nhập quản trị</h2>
                <p className="mt-1 text-sm text-slate-500">
                  Nhập thông tin tài khoản điều hành để bắt đầu phiên làm việc.
                </p>
              </div>
              <span
                className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-[#DBEAFE] bg-[#EFF5FF] text-[#1D63ED]"
                aria-hidden="true"
              >
                <KeyRound className="h-5 w-5" strokeWidth={1.75} />
              </span>
            </div>

            {error && (
              <div
                role="alert"
                className="mt-5 flex items-start gap-2.5 rounded-xl border border-red-200 bg-red-50 px-3.5 py-3 text-xs text-red-900"
              >
                <AlertCircle
                  className="h-4 w-4 shrink-0 text-red-600 mt-0.5"
                  strokeWidth={1.75}
                />
                <p className="font-medium leading-relaxed">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="mt-6 space-y-4" noValidate>
              <div>
                <label
                  htmlFor="admin-username"
                  className="block text-xs font-semibold text-slate-700 mb-1.5"
                >
                  Tên đăng nhập
                </label>
                <div className="relative">
                  <User
                    className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                    strokeWidth={1.75}
                  />
                  <input
                    id="admin-username"
                    type="text"
                    autoComplete="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Nhập tên đăng nhập (vd: admin)"
                    className="h-10.5 w-full rounded-[10px] border border-slate-200 bg-white pl-9.5 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="admin-password"
                  className="block text-xs font-semibold text-slate-700 mb-1.5"
                >
                  Mật khẩu
                </label>
                <div className="relative">
                  <Lock
                    className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                    strokeWidth={1.75}
                  />
                  <input
                    id="admin-password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Nhập mật khẩu"
                    className="h-10.5 w-full rounded-[10px] border border-slate-200 bg-white pl-9.5 pr-10 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword((prev) => !prev)}
                    aria-label={showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}
                    className="absolute right-2.5 top-1/2 -translate-y-1/2 inline-flex h-7 w-7 items-center justify-center rounded-md text-slate-400 hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" strokeWidth={1.75} />
                    ) : (
                      <Eye className="h-4 w-4" strokeWidth={1.75} />
                    )}
                  </button>
                </div>
              </div>

              <div>
                <label
                  htmlFor="admin-staff-name"
                  className="block text-xs font-semibold text-slate-700 mb-1.5"
                >
                  Họ tên nhân viên trực
                </label>
                <div className="relative">
                  <UserCheck
                    className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                    strokeWidth={1.75}
                  />
                  <input
                    id="admin-staff-name"
                    type="text"
                    value={staffName}
                    onChange={(e) => setStaffName(e.target.value)}
                    placeholder="Mặc định: Nguyễn Quốc Khánh"
                    className="h-10.5 w-full rounded-[10px] border border-slate-200 bg-white pl-9.5 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
                  />
                </div>
                <p className="mt-1 text-[11px] text-slate-500">
                  Tên này sẽ tự điền sẵn vào mục người lập phiếu xác nhận và báo cáo doanh thu.
                </p>
              </div>

              <div className="pt-1 space-y-2.5">
                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  shape="rounded"
                  loading={submitting}
                  className="w-full"
                >
                  Đăng nhập vào hệ thống
                </Button>

                <div className="flex items-center justify-between gap-3 rounded-xl border border-slate-200 bg-slate-50/80 px-3.5 py-2.5">
                  <div className="text-xs text-slate-600">
                    <span className="font-semibold text-slate-800">Tài khoản thử nghiệm:</span>{' '}
                    <span className="tabular-nums">admin / admin123</span>
                  </div>
                  <button
                    type="button"
                    onClick={handleFillDemo}
                    className="inline-flex shrink-0 items-center gap-1 rounded-lg border border-[#BFDBFE] bg-[#EFF6FF] px-2.5 py-1 text-xs font-semibold text-[#1D4ED8] hover:bg-[#DBEAFE] transition-colors cursor-pointer"
                  >
                    <Sparkles className="h-3.5 w-3.5" strokeWidth={1.75} />
                    Điền nhanh
                  </button>
                </div>
              </div>
            </form>
          </div>

          <div className="mt-5 text-center">
            <Link
              to="/"
              className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-[#1D63ED] transition-colors"
            >
              <ArrowLeft className="h-3.5 w-3.5" strokeWidth={1.75} />
              Quay về trang đặt tour dành cho Khách hàng
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminLoginPage;
