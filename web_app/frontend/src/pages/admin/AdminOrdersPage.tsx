import { useCallback, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  AlertCircle,
  CheckCircle2,
  ChevronRight,
  ClipboardList,
  FileText,
  RefreshCw,
  Search,
  X,
} from 'lucide-react';
import { ApiError, api } from '../../api/client';
import type { AdminOrderCounts, AdminOrderSummary, OrderStatusCode } from '../../api/types';
import { OrderActionDrawer } from '../../components/admin/OrderActionDrawer';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { SkeletonTableRows } from '../../components/common/LoadingSkeleton';
import { StatusBadge } from '../../components/common/StatusBadge';
import { formatDateTime, formatVnd } from '../../utils/format';

type StatusFilter = 'ALL' | OrderStatusCode;

const STATUS_PILLS: Array<{ key: StatusFilter; label: string }> = [
  { key: 'ALL', label: 'Tất cả' },
  { key: 'DAT', label: 'Đã đặt tour' },
  { key: 'THANHTOAN', label: 'Đã thanh toán' },
  { key: 'HOANTHANH', label: 'Hoàn thành tour' },
  { key: 'HUY', label: 'Đã hủy tour' },
];

const EMPTY_COUNTS: AdminOrderCounts = {
  ALL: 0,
  DAT: 0,
  THANHTOAN: 0,
  HOANTHANH: 0,
  HUY: 0,
};

export function AdminOrdersPage() {
  const [statusFilter, setStatusFilter] = useState<StatusFilter>('ALL');
  const [searchInput, setSearchInput] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');

  const [orders, setOrders] = useState<AdminOrderSummary[]>([]);
  const [counts, setCounts] = useState<AdminOrderCounts>(EMPTY_COUNTS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [systemDateTime, setSystemDateTime] = useState<string | null>(null);
  const [selectedOrderId, setSelectedOrderId] = useState<string | null>(null);
  const [bannerMessage, setBannerMessage] = useState<string | null>(null);

  // Debounce search text
  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedSearch(searchInput.trim());
    }, 250);
    return () => window.clearTimeout(timer);
  }, [searchInput]);

  // Fetch system meta datetime once for drawer cancel default
  useEffect(() => {
    api
      .getMeta()
      .then((meta) => setSystemDateTime(meta.current_datetime))
      .catch(() => {
        // Fallback handled inside OrderActionDrawer
      });
  }, []);

  const fetchOrders = useCallback(async (status: StatusFilter, keyword: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getAdminOrders({
        trang_thai: status === 'ALL' ? undefined : status,
        tu_khoa: keyword || undefined,
      });
      setOrders(res.orders);
      setCounts(res.counts);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tải danh sách đơn hàng.'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchOrders(statusFilter, debouncedSearch);
  }, [statusFilter, debouncedSearch, fetchOrders]);

  const handleOrderUpdated = useCallback(
    (message: string) => {
      setBannerMessage(message);
      void fetchOrders(statusFilter, debouncedSearch);
    },
    [fetchOrders, statusFilter, debouncedSearch]
  );

  const hasActiveFilter = statusFilter !== 'ALL' || debouncedSearch.length > 0;

  return (
    <div className="space-y-5">
      {/* Status pills + Search toolbar */}
      <section className="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 shadow-[0_2px_10px_rgba(15,23,42,0.03)] space-y-4">
        <div
          className="flex flex-wrap items-center gap-2"
          role="tablist"
          aria-label="Lọc theo trạng thái đơn hàng"
        >
          {STATUS_PILLS.map((pill) => {
            const isActive = statusFilter === pill.key;
            const countValue = counts[pill.key] ?? 0;
            return (
              <button
                key={pill.key}
                type="button"
                role="tab"
                aria-selected={isActive}
                onClick={() => setStatusFilter(pill.key)}
                className={[
                  'inline-flex items-center gap-2 rounded-full border px-3.5 py-1.5 text-xs font-semibold transition-colors duration-150 cursor-pointer',
                  isActive
                    ? 'border-[#1D63ED] bg-[#1D63ED] text-white shadow-[0_4px_12px_rgba(29,99,237,0.22)]'
                    : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50',
                ].join(' ')}
              >
                <span>{pill.label}</span>
                <span
                  className={[
                    'inline-flex min-w-[22px] items-center justify-center rounded-full px-1.5 py-0.5 text-[11px] font-bold tabular-nums',
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-100 text-slate-600',
                  ].join(' ')}
                >
                  {countValue}
                </span>
              </button>
            );
          })}
        </div>

        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <div className="relative flex-1">
            <Search
              className="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
              strokeWidth={1.75}
            />
            <input
              type="search"
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              placeholder="Tìm theo mã đơn hàng (vd: DH001), tên khách hàng hoặc tên tour..."
              aria-label="Tìm kiếm đơn hàng"
              className="h-10 w-full rounded-[10px] border border-slate-200 bg-white pl-10 pr-9 text-sm text-slate-900 placeholder:text-slate-400 focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
            />
            {searchInput && (
              <button
                type="button"
                onClick={() => setSearchInput('')}
                aria-label="Xóa từ khóa tìm kiếm"
                className="absolute right-2.5 top-1/2 -translate-y-1/2 inline-flex h-6 w-6 items-center justify-center rounded-md text-slate-400 hover:bg-slate-100 hover:text-slate-700 cursor-pointer"
              >
                <X className="h-3.5 w-3.5" strokeWidth={1.75} />
              </button>
            )}
          </div>

          <div className="flex items-center justify-between sm:justify-end gap-2.5 shrink-0">
            <span className="text-xs text-slate-500 tabular-nums">
              Hiển thị <strong className="text-slate-800">{orders.length}</strong> đơn hàng
            </span>
            <Button
              variant="secondary"
              size="sm"
              shape="rounded"
              onClick={() => void fetchOrders(statusFilter, debouncedSearch)}
              disabled={loading}
              leftIcon={<RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />}
            >
              Làm mới
            </Button>
          </div>
        </div>
      </section>

      {/* Mutation feedback banner */}
      {bannerMessage && (
        <div
          role="status"
          className="flex items-center justify-between gap-3 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-xs font-medium text-emerald-900"
        >
          <div className="flex items-center gap-2">
            <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" strokeWidth={1.75} />
            <span>{bannerMessage}</span>
          </div>
          <button
            type="button"
            onClick={() => setBannerMessage(null)}
            aria-label="Đóng thông báo"
            className="inline-flex h-6 w-6 items-center justify-center rounded-md text-emerald-700 hover:bg-emerald-100 cursor-pointer"
          >
            <X className="h-3.5 w-3.5" strokeWidth={1.75} />
          </button>
        </div>
      )}

      {/* Load error banner */}
      {error && (
        <div
          role="alert"
          className="flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-red-200 bg-white px-5 py-4"
        >
          <div className="flex items-center gap-2.5 text-sm text-red-900">
            <AlertCircle className="h-5 w-5 shrink-0 text-red-600" strokeWidth={1.75} />
            <span className="font-medium">{error}</span>
          </div>
          <Button
            variant="secondary"
            size="sm"
            shape="rounded"
            onClick={() => void fetchOrders(statusFilter, debouncedSearch)}
            leftIcon={<RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />}
          >
            Thử lại
          </Button>
        </div>
      )}

      {/* Orders Table */}
      <section className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-[0_2px_10px_rgba(15,23,42,0.03)]">
        {!loading && orders.length === 0 ? (
          <EmptyState
            className="border-0 rounded-none bg-transparent"
            icon={<ClipboardList className="h-6 w-6" strokeWidth={1.75} />}
            title={
              hasActiveFilter
                ? 'Không tìm thấy đơn hàng phù hợp'
                : 'Chưa có đơn hàng nào trong hệ thống'
            }
            description={
              hasActiveFilter
                ? 'Thử thay đổi bộ lọc trạng thái hoặc xóa từ khóa tìm kiếm để xem toàn bộ đơn hàng.'
                : 'Khi khách hàng đặt tour mới, đơn hàng sẽ hiển thị ngay tại đây.'
            }
            action={
              hasActiveFilter ? (
                <Button
                  variant="secondary"
                  size="sm"
                  shape="rounded"
                  onClick={() => {
                    setStatusFilter('ALL');
                    setSearchInput('');
                  }}
                >
                  Xóa bộ lọc
                </Button>
              ) : undefined
            }
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50/90 text-xs font-semibold text-slate-600">
                  <th className="pl-4 pr-3 py-3 whitespace-nowrap">Mã đơn</th>
                  <th className="px-3 py-3 whitespace-nowrap">Khách hàng</th>
                  <th className="px-3 py-3">Tour &amp; Điểm đến</th>
                  <th className="px-3 py-3 whitespace-nowrap">Khởi hành</th>
                  <th className="px-2.5 py-3 text-right whitespace-nowrap">Khách</th>
                  <th className="px-3 py-3 text-right whitespace-nowrap">Tổng tiền</th>
                  <th className="px-3 py-3 whitespace-nowrap">Trạng thái</th>
                  <th className="pl-3 pr-4 py-3 text-right whitespace-nowrap">Thao tác</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-sm">
                {loading ? (
                  <SkeletonTableRows rows={7} columns={8} />
                ) : (
                  orders.map((order) => (
                    <tr
                      key={order.ma_don_hang}
                      onClick={() => setSelectedOrderId(order.ma_don_hang)}
                      className="group hover:bg-[#F8FAFF] transition-colors cursor-pointer"
                    >
                      <td className="pl-4 pr-3 py-3 whitespace-nowrap">
                        <span className="font-bold text-[#1D63ED] group-hover:underline tabular-nums">
                          {order.ma_don_hang}
                        </span>
                        <span className="block text-[11px] text-slate-400 tabular-nums">
                          {formatDateTime(order.ngay_dat)}
                        </span>
                      </td>

                      <td className="px-3 py-3 max-w-[160px]">
                        <p
                          className="font-semibold text-slate-900 leading-snug truncate"
                          title={order.ho_ten}
                        >
                          {order.ho_ten}
                        </p>
                        <p className="text-xs text-slate-500 tabular-nums truncate">
                          {order.ma_kh}
                        </p>
                      </td>

                      <td className="px-3 py-3 max-w-[200px]">
                        <p
                          className="font-medium text-slate-900 truncate"
                          title={order.ten_tour}
                        >
                          {order.ten_tour}
                        </p>
                        <p
                          className="text-xs text-slate-500 truncate"
                          title={`${order.tinh_den} · ${order.ma_lich_trinh}${order.ten_nha_nghi ? ` · ${order.ten_nha_nghi}` : ''}`}
                        >
                          {order.tinh_den} · {order.ma_lich_trinh}
                          {order.ten_nha_nghi ? ` · ${order.ten_nha_nghi}` : ''}
                        </p>
                      </td>

                      <td className="px-3 py-3 text-xs text-slate-700 tabular-nums whitespace-nowrap">
                        {formatDateTime(order.ngay_xuat_phat)}
                      </td>

                      <td className="px-2.5 py-3 text-right tabular-nums font-medium text-slate-800 whitespace-nowrap">
                        {order.so_luong_khach}
                      </td>

                      <td className="px-3 py-3 text-right tabular-nums font-semibold text-slate-900 whitespace-nowrap">
                        {formatVnd(order.tong_tien)}
                      </td>

                      <td className="px-3 py-3 whitespace-nowrap">
                        <StatusBadge
                          status={order.ma_trang_thai}
                          label={order.ten_trang_thai}
                          size="sm"
                        />
                      </td>

                      <td
                        className="pl-3 pr-4 py-3 text-right whitespace-nowrap"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <div className="inline-flex items-center gap-1.5">
                          <Link
                            to={`/admin/confirmations?order=${encodeURIComponent(order.ma_don_hang)}`}
                            title="Mở phiếu xác nhận"
                            aria-label={`Mở phiếu xác nhận cho đơn ${order.ma_don_hang}`}
                            className="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50 hover:text-[#1D63ED] transition-colors"
                          >
                            <FileText className="h-3.5 w-3.5" strokeWidth={1.75} />
                          </Link>
                          <Button
                            variant="secondary"
                            size="sm"
                            shape="rounded"
                            className="h-8 px-2.5"
                            onClick={() => setSelectedOrderId(order.ma_don_hang)}
                            rightIcon={<ChevronRight className="h-3.5 w-3.5" strokeWidth={1.75} />}
                          >
                            Xử lý
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      {/* Slide-over Order Detail & Actions Drawer */}
      <OrderActionDrawer
        orderId={selectedOrderId}
        open={selectedOrderId !== null}
        defaultSystemDateTime={systemDateTime}
        onClose={() => setSelectedOrderId(null)}
        onOrderUpdated={handleOrderUpdated}
      />
    </div>
  );
}

export default AdminOrdersPage;
