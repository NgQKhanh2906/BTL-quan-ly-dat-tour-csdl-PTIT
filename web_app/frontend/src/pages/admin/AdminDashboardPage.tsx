import { useCallback, useEffect, useRef, useState } from 'react';
import {
  AlertCircle,
  Building2,
  Calendar,
  CheckCircle2,
  Download,
  Eye,
  EyeOff,
  RefreshCw,
  Star,
  UserPen,
  Users,
  Wallet,
  XCircle,
} from 'lucide-react';
import { ApiError, api } from '../../api/client';
import type { RevenueReportResponse } from '../../api/types';
import { DocumentPreviewFrame } from '../../components/admin/DocumentPreviewFrame';
import { KpiMetricCard } from '../../components/admin/KpiMetricCard';
import { RevenueChart } from '../../components/admin/RevenueChart';
import { Button } from '../../components/common/Button';
import { EmptyState } from '../../components/common/EmptyState';
import { LoadingSkeleton } from '../../components/common/LoadingSkeleton';
import { StarRating } from '../../components/common/StarRating';
import { useAuth } from '../../context/AuthContext';
import { formatDate, formatVnd } from '../../utils/format';

const DEFAULT_START_DATE = '2026-09-01';
const DEFAULT_END_DATE = '2026-12-31';

export function AdminDashboardPage() {
  const { admin } = useAuth();
  const nguoiLapInputRef = useRef<HTMLInputElement | null>(null);

  const [tuNgay, setTuNgay] = useState(DEFAULT_START_DATE);
  const [denNgay, setDenNgay] = useState(DEFAULT_END_DATE);
  const [nguoiLap, setNguoiLap] = useState(admin?.staff_name || 'Nguyễn Quốc Khánh');

  const [report, setReport] = useState<RevenueReportResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [reportError, setReportError] = useState<string | null>(null);

  const [nguoiLapError, setNguoiLapError] = useState<string | null>(null);
  const [pdfLoading, setPdfLoading] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: 'success' | 'error';
    text: string;
  } | null>(null);

  // Toggleable A4 landscape print preview
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewHtml, setPreviewHtml] = useState<string | null>(null);
  const [previewLoading, setPreviewLoading] = useState(false);
  const [previewError, setPreviewError] = useState<string | null>(null);

  const isDateRangeInvalid = Boolean(tuNgay && denNgay && denNgay < tuNgay);

  const fetchReport = useCallback(async (start: string, end: string) => {
    if (!start || !end || end < start) return;
    setLoading(true);
    setReportError(null);
    try {
      const res = await api.getRevenueReport(start, end);
      setReport(res);
    } catch (err) {
      setReportError(
        err instanceof ApiError
          ? err.message
          : 'Không thể tải dữ liệu báo cáo doanh thu.'
      );
      setReport(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchPreviewHtml = useCallback(
    async (start: string, end: string, issuer: string) => {
      setPreviewLoading(true);
      setPreviewError(null);
      try {
        const res = await api.getRevenueHtml(start, end, issuer);
        setPreviewHtml(res.html);
      } catch (err) {
        setPreviewHtml(null);
        setPreviewError(
          err instanceof ApiError
            ? err.message
            : 'Không thể tạo bản xem trước báo cáo.'
        );
      } finally {
        setPreviewLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    if (!isDateRangeInvalid && tuNgay && denNgay) {
      void fetchReport(tuNgay, denNgay);
    }
  }, [tuNgay, denNgay, isDateRangeInvalid, fetchReport]);

  // Keep inline preview synced when dates change while preview is open
  useEffect(() => {
    if (previewOpen && !isDateRangeInvalid && tuNgay && denNgay && nguoiLap.trim()) {
      const timer = window.setTimeout(() => {
        void fetchPreviewHtml(tuNgay, denNgay, nguoiLap.trim());
      }, 280);
      return () => window.clearTimeout(timer);
    }
  }, [previewOpen, tuNgay, denNgay, nguoiLap, isDateRangeInvalid, fetchPreviewHtml]);

  const validateBeforeExport = (): string | null => {
    if (isDateRangeInvalid || !tuNgay || !denNgay) {
      setFeedback({
        type: 'error',
        text: 'Vui lòng chọn khoảng kỳ báo cáo hợp lệ (Đến ngày phải lớn hơn hoặc bằng Từ ngày).',
      });
      return null;
    }
    const cleanIssuer = nguoiLap.trim();
    if (!cleanIssuer) {
      setNguoiLapError('Vui lòng nhập họ tên người lập báo cáo.');
      nguoiLapInputRef.current?.focus();
      return null;
    }
    setNguoiLapError(null);
    return cleanIssuer;
  };

  const handleDownloadPdf = async () => {
    setFeedback(null);
    const cleanIssuer = validateBeforeExport();
    if (!cleanIssuer) return;

    setPdfLoading(true);
    try {
      await api.downloadRevenuePdf(tuNgay, denNgay, cleanIssuer);
      setFeedback({
        type: 'success',
        text: `Đã xuất báo cáo doanh thu khổ A4 ngang kỳ ${formatDate(tuNgay)} – ${formatDate(denNgay)}.`,
      });
    } catch (err) {
      setFeedback({
        type: 'error',
        text:
          err instanceof ApiError
            ? err.message
            : 'Không thể xuất file PDF báo cáo doanh thu.',
      });
    } finally {
      setPdfLoading(false);
    }
  };

  const handleTogglePreview = () => {
    setFeedback(null);
    if (previewOpen) {
      setPreviewOpen(false);
      return;
    }
    const cleanIssuer = validateBeforeExport();
    if (!cleanIssuer) return;
    setPreviewOpen(true);
    void fetchPreviewHtml(tuNgay, denNgay, cleanIssuer);
  };

  const summary = report?.summary;
  const totalOrdersInclCancelled = (summary?.so_don ?? 0) + (summary?.so_don_huy ?? 0);
  const cancelRateText =
    totalOrdersInclCancelled > 0
      ? `${Math.round(((summary?.so_don_huy ?? 0) / totalOrdersInclCancelled) * 100)}% tổng số đơn trong kỳ`
      : 'Chưa có phát sinh hủy';

  const tourRows = report?.tours ?? [];
  const rollupRow = tourRows.find((r) => r.ma_tour === 'TỔNG CỘNG');
  const serviceRevenueSub = rollupRow
    ? `Dịch vụ ${formatVnd(rollupRow.doanh_thu_dich_vu)} · Phạt ${formatVnd(rollupRow.tien_phat_huy)}`
    : `Kỳ ${formatDate(tuNgay)} – ${formatDate(denNgay)}`;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-7 sm:py-8 space-y-6">
      {/* Tiêu đề trang */}
      <div>
        <h1 className="text-2xl sm:text-[28px] font-bold text-slate-900 tracking-tight">
          Báo cáo doanh thu và xếp hạng dịch vụ
        </h1>
      </div>

      {/* Filter & Export Controls */}
      <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_2px_10px_rgba(15,23,42,0.03)]">
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-12 gap-4 items-start">
          <div className="xl:col-span-2">
            <label
              htmlFor="report-start-date"
              className="block text-xs font-semibold text-slate-700 mb-1.5"
            >
              Từ ngày
            </label>
            <div className="relative">
              <Calendar
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                id="report-start-date"
                type="date"
                value={tuNgay}
                onChange={(e) => setTuNgay(e.target.value)}
                className="h-10 w-full rounded-[10px] border border-slate-200 bg-white pl-9 pr-2.5 text-sm text-slate-900 tabular-nums focus:border-[#1D63ED] focus:outline-none focus:ring-2 focus:ring-[#1D63ED]/15"
              />
            </div>
          </div>

          <div className="xl:col-span-2">
            <label
              htmlFor="report-end-date"
              className="block text-xs font-semibold text-slate-700 mb-1.5"
            >
              Đến ngày
            </label>
            <div className="relative">
              <Calendar
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                id="report-end-date"
                type="date"
                value={denNgay}
                onChange={(e) => setDenNgay(e.target.value)}
                aria-invalid={isDateRangeInvalid}
                className={[
                  'h-10 w-full rounded-[10px] border bg-white pl-9 pr-2.5 text-sm text-slate-900 tabular-nums focus:outline-none focus:ring-2',
                  isDateRangeInvalid
                    ? 'border-red-300 focus:border-red-500 focus:ring-red-500/15'
                    : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
                ].join(' ')}
              />
            </div>
            {isDateRangeInvalid && (
              <p className="mt-1 text-xs font-medium text-red-600">
                Đến ngày phải lớn hơn hoặc bằng từ ngày.
              </p>
            )}
          </div>

          <div className="md:col-span-2 xl:col-span-4">
            <label
              htmlFor="report-issuer"
              className="block text-xs font-semibold text-slate-700 mb-1.5"
            >
              Người lập báo cáo <span className="text-red-600">*</span>
            </label>
            <div className="relative">
              <UserPen
                className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400"
                strokeWidth={1.75}
              />
              <input
                ref={nguoiLapInputRef}
                id="report-issuer"
                type="text"
                value={nguoiLap}
                onChange={(e) => {
                  setNguoiLap(e.target.value);
                  if (nguoiLapError && e.target.value.trim()) {
                    setNguoiLapError(null);
                  }
                }}
                placeholder="Nhập họ tên người lập báo cáo..."
                aria-invalid={Boolean(nguoiLapError)}
                className={[
                  'h-10 w-full rounded-[10px] border bg-white pl-9 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2',
                  nguoiLapError
                    ? 'border-red-300 focus:border-red-500 focus:ring-red-500/15'
                    : 'border-slate-200 focus:border-[#1D63ED] focus:ring-[#1D63ED]/15',
                ].join(' ')}
              />
            </div>
            {nguoiLapError && (
              <p role="alert" className="mt-1 text-xs font-medium text-red-600">
                {nguoiLapError}
              </p>
            )}
          </div>

          <div className="md:col-span-2 xl:col-span-4 flex flex-wrap items-center xl:justify-end gap-2.5 xl:pt-[22px]">
            <Button
              variant="secondary"
              size="md"
              shape="rounded"
              onClick={handleTogglePreview}
              disabled={isDateRangeInvalid}
              leftIcon={
                previewOpen ? (
                  <EyeOff className="h-4 w-4" strokeWidth={1.75} />
                ) : (
                  <Eye className="h-4 w-4" strokeWidth={1.75} />
                )
              }
            >
              {previewOpen ? 'Ẩn bản xem trước' : 'Xem trước bản in'}
            </Button>

            <Button
              variant="primary"
              size="md"
              shape="rounded"
              loading={pdfLoading}
              disabled={isDateRangeInvalid}
              onClick={() => void handleDownloadPdf()}
              leftIcon={<Download className="h-4 w-4" strokeWidth={1.75} />}
            >
              Xuất báo cáo PDF (A4 ngang)
            </Button>
          </div>
        </div>

        {feedback && (
          <div
            role={feedback.type === 'error' ? 'alert' : 'status'}
            className={[
              'mt-4 flex items-center justify-between gap-3 rounded-xl border px-4 py-2.5 text-xs font-medium',
              feedback.type === 'success'
                ? 'border-emerald-200 bg-emerald-50 text-emerald-900'
                : 'border-red-200 bg-red-50 text-red-900',
            ].join(' ')}
          >
            <div className="flex items-center gap-2">
              {feedback.type === 'success' ? (
                <CheckCircle2 className="h-4 w-4 shrink-0 text-emerald-600" strokeWidth={1.75} />
              ) : (
                <AlertCircle className="h-4 w-4 shrink-0 text-red-600" strokeWidth={1.75} />
              )}
              <span>{feedback.text}</span>
            </div>
            <button
              type="button"
              onClick={() => setFeedback(null)}
              className="text-xs underline underline-offset-2 opacity-80 hover:opacity-100 cursor-pointer"
            >
              Đóng
            </button>
          </div>
        )}
      </section>

      {/* Error State for Report Data */}
      {reportError && (
        <div className="rounded-2xl border border-red-200 bg-white p-6 text-center">
          <AlertCircle className="mx-auto h-7 w-7 text-red-600" strokeWidth={1.75} />
          <p className="mt-2.5 text-sm font-bold text-slate-900">
            Không thể tải dữ liệu báo cáo
          </p>
          <p className="mt-1 text-xs text-slate-600">{reportError}</p>
          <div className="mt-4">
            <Button
              variant="secondary"
              size="sm"
              shape="rounded"
              onClick={() => void fetchReport(tuNgay, denNgay)}
              leftIcon={<RefreshCw className="h-3.5 w-3.5" strokeWidth={1.75} />}
            >
              Thử tải lại
            </Button>
          </div>
        </div>
      )}

      {/* 4 KPI Cards */}
      {loading ? (
        <LoadingSkeleton variant="kpi" count={4} />
      ) : summary ? (
        <section
          aria-label="Chỉ số tổng quan kỳ báo cáo"
          className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4"
        >
          <KpiMetricCard
            label="Tổng doanh thu"
            value={formatVnd(summary.tong_doanh_thu)}
            sublabel={serviceRevenueSub}
            tone="blue"
            icon={<Wallet className="h-4.5 w-4.5" strokeWidth={1.75} />}
          />
          <KpiMetricCard
            label="Đơn thành công"
            value={new Intl.NumberFormat('vi-VN').format(summary.so_don)}
            sublabel="Đơn đặt hợp lệ không bị hủy"
            tone="emerald"
            icon={<CheckCircle2 className="h-4.5 w-4.5" strokeWidth={1.75} />}
          />
          <KpiMetricCard
            label="Khách phục vụ"
            value={new Intl.NumberFormat('vi-VN').format(summary.so_khach)}
            sublabel="Tổng lượt khách tham gia tour"
            tone="slate"
            icon={<Users className="h-4.5 w-4.5" strokeWidth={1.75} />}
          />
          <KpiMetricCard
            label="Đơn đã hủy"
            value={new Intl.NumberFormat('vi-VN').format(summary.so_don_huy)}
            sublabel={cancelRateText}
            tone="red"
            icon={<XCircle className="h-4.5 w-4.5" strokeWidth={1.75} />}
          />
        </section>
      ) : null}

      {/* Inline Toggleable A4 Landscape Print Preview */}
      {previewOpen && (
        <DocumentPreviewFrame
          title="Xem trước Báo cáo tổng hợp doanh thu"
          subtitle={`Kỳ ${formatDate(tuNgay)} – ${formatDate(denNgay)} · Người lập: ${nguoiLap.trim()}`}
          orientation="landscape"
          html={previewHtml}
          loading={previewLoading}
          error={previewError}
          onRetry={() => {
            const cleanIssuer = validateBeforeExport();
            if (cleanIssuer) {
              void fetchPreviewHtml(tuNgay, denNgay, cleanIssuer);
            }
          }}
          onDownloadPdf={() => void handleDownloadPdf()}
          downloadingPdf={pdfLoading}
          downloadLabel="Xuất báo cáo PDF (A4 ngang)"
        />
      )}

      {/* Recharts Horizontal Bar Chart */}
      {loading ? (
        <LoadingSkeleton variant="table" count={5} />
      ) : report ? (
        <RevenueChart tours={report.tours} />
      ) : null}

      {/* Table 1: Tour Revenue Summary */}
      {loading ? (
        <LoadingSkeleton variant="table" count={6} />
      ) : report ? (
        <section className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-[0_2px_10px_rgba(15,23,42,0.03)]">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 px-5 py-4">
            <div>
              <h2 className="text-base font-bold text-slate-900">
                Tổng hợp doanh thu theo tour
              </h2>
              <p className="mt-0.5 text-xs text-slate-500">
                Kỳ khởi hành từ {formatDate(tuNgay)} đến {formatDate(denNgay)} · Nơi nhận:{' '}
                {report.noi_nhan}
              </p>
            </div>
            <span className="text-xs font-medium text-slate-500 tabular-nums">
              {report.tours.filter((r) => r.ma_tour !== 'TỔNG CỘNG').length} tuyến tour
            </span>
          </div>

          {report.tours.length === 0 ? (
            <EmptyState
              className="border-0 rounded-none bg-transparent"
              title="Không có dữ liệu doanh thu trong kỳ báo cáo"
              description="Không có lịch trình khởi hành nào trong khoảng thời gian đã chọn. Hãy mở rộng khoảng ngày để xem số liệu."
              action={
                <Button
                  variant="secondary"
                  size="sm"
                  shape="rounded"
                  onClick={() => {
                    setTuNgay(DEFAULT_START_DATE);
                    setDenNgay(DEFAULT_END_DATE);
                  }}
                >
                  Đặt lại kỳ mặc định
                </Button>
              }
            />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[920px] text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/90 text-xs font-semibold text-slate-600">
                    <th className="px-4 py-3 whitespace-nowrap">Mã tour</th>
                    <th className="px-4 py-3">Tên chương trình tour</th>
                    <th className="px-3 py-3 text-right whitespace-nowrap">Số lịch trình</th>
                    <th className="px-3 py-3 text-right whitespace-nowrap">Số đơn</th>
                    <th className="px-3 py-3 text-right whitespace-nowrap">Số khách</th>
                    <th className="px-3 py-3 text-right whitespace-nowrap">Đơn hủy</th>
                    <th className="px-4 py-3 text-right whitespace-nowrap">Doanh thu dịch vụ</th>
                    <th className="px-4 py-3 text-right whitespace-nowrap">Tiền phạt hủy</th>
                    <th className="px-4 py-3 text-right whitespace-nowrap">Tổng doanh thu</th>
                    <th className="px-4 py-3 text-center whitespace-nowrap">Điểm TB</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-sm">
                  {report.tours.map((row) => {
                    const isTotalRow = row.ma_tour === 'TỔNG CỘNG';
                    return (
                      <tr
                        key={isTotalRow ? '__TOTAL__' : row.ma_tour}
                        className={
                          isTotalRow
                            ? 'bg-[#EFF5FF] font-bold text-slate-900 border-t-2 border-slate-300'
                            : 'hover:bg-slate-50/80 transition-colors'
                        }
                      >
                        <td className="px-4 py-3.5 text-xs font-bold whitespace-nowrap tabular-nums">
                          {isTotalRow ? (
                            <span className="text-[#1D63ED]">TỔNG CỘNG</span>
                          ) : (
                            <span className="inline-flex items-center rounded-md border border-slate-200 bg-slate-50 px-2 py-0.5 text-slate-700">
                              {row.ma_tour}
                            </span>
                          )}
                        </td>
                        <td className="px-4 py-3.5 text-slate-900 font-medium">
                          {isTotalRow ? 'Toàn bộ các tuyến tour trong kỳ' : row.ten_tour}
                        </td>
                        <td className="px-3 py-3.5 text-right tabular-nums text-slate-700">
                          {row.so_lich_trinh}
                        </td>
                        <td className="px-3 py-3.5 text-right tabular-nums text-slate-700">
                          {row.so_don}
                        </td>
                        <td className="px-3 py-3.5 text-right tabular-nums text-slate-700">
                          {row.so_khach}
                        </td>
                        <td className="px-3 py-3.5 text-right tabular-nums text-slate-700">
                          {row.so_don_huy > 0 ? (
                            <span className="text-red-700 font-semibold">{row.so_don_huy}</span>
                          ) : (
                            <span className="text-slate-400">0</span>
                          )}
                        </td>
                        <td className="px-4 py-3.5 text-right tabular-nums whitespace-nowrap text-slate-800">
                          {formatVnd(row.doanh_thu_dich_vu)}
                        </td>
                        <td className="px-4 py-3.5 text-right tabular-nums whitespace-nowrap text-slate-700">
                          {formatVnd(row.tien_phat_huy)}
                        </td>
                        <td
                          className={[
                            'px-4 py-3.5 text-right tabular-nums whitespace-nowrap',
                            isTotalRow
                              ? 'text-[#1D63ED] font-bold'
                              : 'text-slate-900 font-semibold',
                          ].join(' ')}
                        >
                          {formatVnd(row.tong_doanh_thu)}
                        </td>
                        <td className="px-4 py-3.5 text-center tabular-nums whitespace-nowrap">
                          {row.diem_tour_tb !== null ? (
                            <span className="inline-flex items-center gap-1 font-semibold text-slate-800">
                              <Star
                                className="h-3.5 w-3.5 fill-[#F59E0B] text-[#F59E0B]"
                                strokeWidth={1.75}
                                aria-hidden="true"
                              />
                              {row.diem_tour_tb.toFixed(1)}
                            </span>
                          ) : (
                            <span className="text-slate-400">—</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      ) : null}

      {/* Table 2: Accommodation Ranking */}
      {!loading && report && (
        <section className="rounded-2xl border border-slate-200 bg-white overflow-hidden shadow-[0_2px_10px_rgba(15,23,42,0.03)]">
          <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 px-5 py-4">
            <div className="flex items-center gap-2.5">
              <span
                className="inline-flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-slate-700"
                aria-hidden="true"
              >
                <Building2 className="h-4 w-4" strokeWidth={1.75} />
              </span>
              <div>
                <h2 className="text-base font-bold text-slate-900">
                  Xếp hạng đánh giá cơ sở lưu trú
                </h2>
                <p className="text-xs text-slate-500">
                  Thứ hạng nhà nghỉ và homestay theo điểm đánh giá của khách hàng trong kỳ
                </p>
              </div>
            </div>
            <span className="text-xs font-medium text-slate-500 tabular-nums">
              {report.accommodations.length} cơ sở có đánh giá
            </span>
          </div>

          {report.accommodations.length === 0 ? (
            <EmptyState
              className="border-0 rounded-none bg-transparent"
              icon={<Building2 className="h-6 w-6" strokeWidth={1.75} />}
              title="Chưa có đánh giá cơ sở lưu trú"
              description="Trong khoảng kỳ báo cáo đã chọn chưa ghi nhận lượt đánh giá nào cho các cơ sở lưu trú."
            />
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[680px] text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-200 bg-slate-50/90 text-xs font-semibold text-slate-600">
                    <th className="px-4 py-3 text-center w-16">Hạng</th>
                    <th className="px-4 py-3 whitespace-nowrap">Mã</th>
                    <th className="px-4 py-3">Tên cơ sở lưu trú</th>
                    <th className="px-4 py-3 whitespace-nowrap">Loại hình</th>
                    <th className="px-4 py-3 whitespace-nowrap">Tỉnh thành</th>
                    <th className="px-4 py-3 text-right whitespace-nowrap">Số lượt đánh giá</th>
                    <th className="px-4 py-3 whitespace-nowrap">Điểm trung bình</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-sm">
                  {report.accommodations.map((acc, idx) => (
                    <tr key={acc.ma_nha_nghi} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-4 py-3.5 text-center tabular-nums">
                        <span
                          className={[
                            'inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold',
                            idx === 0
                              ? 'bg-[#EFF6FF] text-[#1D63ED] border border-[#BFDBFE]'
                              : 'bg-slate-100 text-slate-600',
                          ].join(' ')}
                        >
                          {idx + 1}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-xs font-semibold text-slate-600 tabular-nums whitespace-nowrap">
                        {acc.ma_nha_nghi}
                      </td>
                      <td className="px-4 py-3.5 font-semibold text-slate-900">
                        {acc.ten_nha_nghi}
                      </td>
                      <td className="px-4 py-3.5 whitespace-nowrap">
                        <span className="inline-flex items-center rounded-full border border-slate-200 bg-slate-50 px-2.5 py-0.5 text-xs font-medium text-slate-700">
                          {acc.loai_hinh}
                        </span>
                      </td>
                      <td className="px-4 py-3.5 text-slate-700 whitespace-nowrap">
                        {acc.ten_tinh}
                      </td>
                      <td className="px-4 py-3.5 text-right tabular-nums font-medium text-slate-800">
                        {acc.so_luot_danh_gia}
                      </td>
                      <td className="px-4 py-3.5 whitespace-nowrap">
                        {acc.diem_tb !== null ? (
                          <StarRating value={acc.diem_tb} size="sm" showValue />
                        ) : (
                          <span className="text-xs text-slate-400">—</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  );
}

export default AdminDashboardPage;
