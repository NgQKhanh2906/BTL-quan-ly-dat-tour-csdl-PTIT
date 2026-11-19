import { useEffect, useState, type FormEvent } from 'react';
import { ArrowRight, Mail, Phone, Search, UserCheck } from 'lucide-react';
import { api, ApiError } from '../../api/client';
import type { CustomerItem } from '../../api/types';
import { useAuth } from '../../context/AuthContext';
import { getInitials } from '../../utils/format';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';

export function CustomerLoginModal() {
  const { isCustomerLoginModalOpen, closeCustomerLoginModal, loginCustomer } = useAuth();
  const [identifier, setIdentifier] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [sampleCustomers, setSampleCustomers] = useState<CustomerItem[]>([]);
  const [loadingSamples, setLoadingSamples] = useState(false);

  useEffect(() => {
    if (!isCustomerLoginModalOpen) return;
    setError(null);
    let active = true;
    setLoadingSamples(true);
    api
      .getCustomers()
      .then((list) => {
        if (active) setSampleCustomers(list);
      })
      .catch(() => {
        if (active) setSampleCustomers([]);
      })
      .finally(() => {
        if (active) setLoadingSamples(false);
      });
    return () => {
      active = false;
    };
  }, [isCustomerLoginModalOpen]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const cleaned = identifier.trim();
    if (!cleaned) {
      setError('Vui lòng nhập email hoặc số điện thoại đã đăng ký.');
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      await loginCustomer(cleaned);
      setIdentifier('');
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError('Không tìm thấy tài khoản khớp với thông tin vừa nhập.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleQuickLogin = async (cust: CustomerItem) => {
    const idValue = cust.email || cust.so_dien_thoai.split(',')[0]?.trim() || '';
    if (!idValue) return;
    setSubmitting(true);
    setError(null);
    try {
      await loginCustomer(idValue);
      setIdentifier('');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Đăng nhập không thành công.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Modal
      open={isCustomerLoginModalOpen}
      onClose={closeCustomerLoginModal}
      title="Đăng nhập khách hàng"
      description="Tra cứu lịch sử đặt tour, tải phiếu xác nhận PDF và viết đánh giá chuyến đi."
      size="md"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label
            htmlFor="customer-login-identifier"
            className="block text-sm font-semibold text-slate-800 mb-1.5"
          >
            Email hoặc số điện thoại
          </label>
          <div className="relative">
            <Search
              className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
              strokeWidth={1.75}
            />
            <input
              id="customer-login-identifier"
              type="text"
              value={identifier}
              onChange={(e) => {
                setIdentifier(e.target.value);
                if (error) setError(null);
              }}
              placeholder="Ví dụ: an.nguyen@gmail.com hoặc 0901234567"
              autoFocus
              className="w-full h-11 rounded-xl border border-slate-200 bg-slate-50/70 pl-10 pr-4 text-sm text-slate-900 placeholder:text-slate-400 focus:bg-white focus:border-[#1D63ED] focus:outline-none focus:ring-3 focus:ring-[#1D63ED]/15 transition-all"
            />
          </div>
          {error && (
            <p className="mt-2 text-xs font-medium text-[#B91C1C]" role="alert">
              {error}
            </p>
          )}
        </div>

        <Button
          type="submit"
          variant="primary"
          shape="pill"
          size="md"
          loading={submitting}
          rightIcon={<ArrowRight className="h-4 w-4" strokeWidth={1.75} />}
          className="w-full"
        >
          Tiếp tục
        </Button>
      </form>

      <div className="mt-6 pt-5 border-t border-slate-100">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-semibold text-slate-600">
            Chọn nhanh tài khoản khách hàng
          </span>
          <span className="text-xs text-slate-400 tabular-nums">
            {sampleCustomers.length > 0 ? `${sampleCustomers.length} khách hàng` : ''}
          </span>
        </div>

        {loadingSamples ? (
          <div className="space-y-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-14 rounded-xl bg-slate-100 animate-pulse" />
            ))}
          </div>
        ) : sampleCustomers.length === 0 ? (
          <p className="text-xs text-slate-500">
            Nhập trực tiếp email hoặc số điện thoại của bạn ở ô phía trên để đăng nhập.
          </p>
        ) : (
          <div className="space-y-2 max-h-60 overflow-y-auto pr-1">
            {sampleCustomers.slice(0, 8).map((cust) => {
              const primaryPhone = cust.so_dien_thoai.split(',')[0]?.trim();
              return (
                <button
                  key={cust.ma_kh}
                  type="button"
                  disabled={submitting}
                  onClick={() => handleQuickLogin(cust)}
                  className="w-full flex items-center justify-between gap-3 rounded-xl border border-slate-200/80 bg-white px-3.5 py-2.5 text-left hover:border-[#1D63ED]/50 hover:bg-[#F7FAFF] transition-colors cursor-pointer disabled:opacity-60"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#EFF5FF] text-xs font-bold text-[#1D63ED]">
                      {getInitials(cust.ho_ten)}
                    </span>
                    <div className="min-w-0">
                      <div className="text-sm font-semibold text-slate-900 truncate">
                        {cust.ho_ten}
                      </div>
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-0.5 text-xs text-slate-500">
                        <span className="inline-flex items-center gap-1 truncate">
                          <Mail className="h-3 w-3 shrink-0" strokeWidth={1.75} />
                          <span className="truncate">{cust.email}</span>
                        </span>
                        {primaryPhone && (
                          <span className="inline-flex items-center gap-1 tabular-nums">
                            <Phone className="h-3 w-3 shrink-0" strokeWidth={1.75} />
                            {primaryPhone}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <UserCheck
                    className="h-4 w-4 shrink-0 text-slate-400"
                    strokeWidth={1.75}
                    aria-hidden="true"
                  />
                </button>
              );
            })}
          </div>
        )}
      </div>
    </Modal>
  );
}
