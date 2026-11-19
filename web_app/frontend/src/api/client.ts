import type {
  AccommodationItem,
  AdminLoginResponse,
  AdminOrderFullResponse,
  AdminOrdersResponse,
  BookingEstimateRequest,
  BookingEstimateResponse,
  CancelOrderRequest,
  CancelOrderResponse,
  CancelPreviewResponse,
  ConfirmationHtmlResponse,
  CreateBookingRequest,
  CreateBookingResponse,
  CustomerItem,
  CustomerLoginResponse,
  CustomerOrderItem,
  DuplicateCheckResponse,
  LandingResponse,
  MetaResponse,
  OpenScheduleItem,
  OrderStatusCode,
  PendingReviewItem,
  ProvinceItem,
  RevenueHtmlResponse,
  RevenueReportResponse,
  ScheduleSearchItem,
  ScheduleSearchParams,
  SubmitReviewRequest,
  SubmitReviewResponse,
  UpdateStatusResponse,
} from './types';

export const CUSTOMER_TOKEN_STORAGE_KEY = 'bvt_customer_token';
export const ADMIN_TOKEN_STORAGE_KEY = 'bvt_admin_token';

export class ApiError extends Error {
  status: number;
  errors?: string[];

  constructor(message: string, status: number, errors?: string[]) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.errors = errors;
  }
}

type AuthMode = 'none' | 'customer' | 'admin' | 'any';

function getStoredToken(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

function buildAuthHeaders(auth: AuthMode): Record<string, string> {
  const headers: Record<string, string> = {};
  const customerToken = getStoredToken(CUSTOMER_TOKEN_STORAGE_KEY);
  const adminToken = getStoredToken(ADMIN_TOKEN_STORAGE_KEY);

  if ((auth === 'customer' || auth === 'any') && customerToken) {
    headers['X-Customer-Token'] = customerToken;
  }
  if ((auth === 'admin' || auth === 'any') && adminToken) {
    headers['X-Admin-Token'] = adminToken;
  }
  return headers;
}

async function parseErrorResponse(res: Response): Promise<ApiError> {
  let message = 'Đã xảy ra lỗi khi kết nối hệ thống. Vui lòng thử lại.';
  let errors: string[] | undefined;

  try {
    const data = await res.json();
    if (typeof data?.detail === 'string' && data.detail.trim()) {
      message = data.detail;
    } else if (Array.isArray(data?.detail)) {
      const joined = data.detail
        .map((item: { msg?: string }) => item?.msg)
        .filter(Boolean)
        .join('; ');
      if (joined) message = joined;
    } else if (typeof data?.message === 'string' && data.message.trim()) {
      message = data.message;
    }
    if (Array.isArray(data?.errors)) {
      errors = data.errors.filter((e: unknown): e is string => typeof e === 'string');
      if (errors && errors.length > 0 && message === 'Đã xảy ra lỗi khi kết nối hệ thống. Vui lòng thử lại.') {
        message = errors[0];
      }
    }
  } catch {
    if (res.status === 401) {
      message = 'Phiên đăng nhập đã hết hạn hoặc chưa hợp lệ. Vui lòng đăng nhập lại.';
    } else if (res.status === 403) {
      message = 'Bạn không có quyền thực hiện thao tác này.';
    } else if (res.status === 404) {
      message = 'Không tìm thấy dữ liệu yêu cầu.';
    } else if (res.status >= 500) {
      message = 'Máy chủ đang gặp sự cố. Vui lòng thử lại sau ít phút.';
    }
  }

  return new ApiError(message, res.status, errors);
}

async function requestJson<T>(
  path: string,
  options: {
    method?: 'GET' | 'POST' | 'PATCH' | 'DELETE';
    body?: unknown;
    auth?: AuthMode;
  } = {}
): Promise<T> {
  const { method = 'GET', body, auth = 'none' } = options;
  const headers: Record<string, string> = {
    Accept: 'application/json',
    ...buildAuthHeaders(auth),
  };

  if (body !== undefined) {
    headers['Content-Type'] = 'application/json';
  }

  const res = await fetch(path, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    throw await parseErrorResponse(res);
  }

  return (await res.json()) as T;
}

function extractFilename(contentDisposition: string | null, fallback: string): string {
  if (!contentDisposition) return fallback;
  const utf8Match = contentDisposition.match(/filename\*=UTF-8''([^;]+)/i);
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1]);
    } catch {
      return utf8Match[1];
    }
  }
  const simpleMatch = contentDisposition.match(/filename="?([^";]+)"?/i);
  return simpleMatch?.[1] || fallback;
}

function triggerBlobDownload(blob: Blob, filename: string): void {
  const url = window.URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  window.setTimeout(() => window.URL.revokeObjectURL(url), 1000);
}

function buildQuery(params: Record<string, string | number | null | undefined>): string {
  const sp = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && String(value).trim() !== '') {
      sp.set(key, String(value));
    }
  });
  const qs = sp.toString();
  return qs ? `?${qs}` : '';
}

export const api = {
  getMeta(): Promise<MetaResponse> {
    return requestJson<MetaResponse>('/api/meta');
  },

  getLanding(): Promise<LandingResponse> {
    return requestJson<LandingResponse>('/api/landing');
  },

  getProvinces(): Promise<ProvinceItem[]> {
    return requestJson<ProvinceItem[]>('/api/provinces');
  },

  searchSchedules(params: ScheduleSearchParams = {}): Promise<ScheduleSearchItem[]> {
    const qs = buildQuery({
      tu_khoa: params.tu_khoa,
      ma_tinh_den: params.ma_tinh_den,
      gia_tu: params.gia_tu,
      gia_den: params.gia_den,
      tu_ngay: params.tu_ngay,
      den_ngay: params.den_ngay,
      so_khach: params.so_khach,
      diem_toi_thieu: params.diem_toi_thieu,
    });
    return requestJson<ScheduleSearchItem[]>(`/api/schedules/search${qs}`);
  },

  getOpenSchedules(): Promise<OpenScheduleItem[]> {
    return requestJson<OpenScheduleItem[]>('/api/schedules/open');
  },

  getAccommodations(maTinhDen: string): Promise<AccommodationItem[]> {
    const qs = buildQuery({ ma_tinh_den: maTinhDen });
    return requestJson<AccommodationItem[]>(`/api/accommodations${qs}`);
  },

  getCustomers(): Promise<CustomerItem[]> {
    return requestJson<CustomerItem[]>('/api/customers');
  },

  checkDuplicateCustomer(email: string, sdt: string): Promise<DuplicateCheckResponse> {
    return requestJson<DuplicateCheckResponse>('/api/customers/check-duplicate', {
      method: 'POST',
      body: { email, so_dien_thoai: sdt },
    });
  },

  customerLogin(identifier: string): Promise<CustomerLoginResponse> {
    return requestJson<CustomerLoginResponse>('/api/auth/customer-login', {
      method: 'POST',
      body: { identifier },
    });
  },

  adminLogin(username: string, password: string, staffName?: string): Promise<AdminLoginResponse> {
    return requestJson<AdminLoginResponse>('/api/auth/admin-login', {
      method: 'POST',
      body: {
        username,
        password,
        staff_name: staffName?.trim() || undefined,
      },
    });
  },

  estimateBooking(payload: BookingEstimateRequest): Promise<BookingEstimateResponse> {
    return requestJson<BookingEstimateResponse>('/api/bookings/estimate', {
      method: 'POST',
      body: payload,
    });
  },

  createBooking(payload: CreateBookingRequest): Promise<CreateBookingResponse> {
    return requestJson<CreateBookingResponse>('/api/bookings', {
      method: 'POST',
      body: payload,
    });
  },

  getCustomerOrders(maKh: string): Promise<CustomerOrderItem[]> {
    return requestJson<CustomerOrderItem[]>(`/api/customers/${encodeURIComponent(maKh)}/orders`, {
      auth: 'any',
    });
  },

  getPendingReviews(maKh: string): Promise<PendingReviewItem[]> {
    return requestJson<PendingReviewItem[]>(
      `/api/customers/${encodeURIComponent(maKh)}/pending-reviews`,
      { auth: 'any' }
    );
  },

  submitReview(payload: SubmitReviewRequest): Promise<SubmitReviewResponse> {
    return requestJson<SubmitReviewResponse>('/api/reviews', {
      method: 'POST',
      body: payload,
      auth: 'customer',
    });
  },

  async downloadConfirmationPdf(maDon: string, nguoiLap?: string): Promise<void> {
    const qs = buildQuery({ nguoi_lap: nguoiLap });
    const res = await fetch(`/api/orders/${encodeURIComponent(maDon)}/confirmation/pdf${qs}`, {
      method: 'GET',
      headers: {
        Accept: 'application/pdf',
        ...buildAuthHeaders('any'),
      },
    });
    if (!res.ok) {
      throw await parseErrorResponse(res);
    }
    const blob = await res.blob();
    const filename = extractFilename(
      res.headers.get('Content-Disposition'),
      `phieu_xac_nhan_${maDon}.pdf`
    );
    triggerBlobDownload(blob, filename);
  },

  getAdminOrders(params: { trang_thai?: string; tu_khoa?: string } = {}): Promise<AdminOrdersResponse> {
    const qs = buildQuery({
      trang_thai: params.trang_thai && params.trang_thai !== 'ALL' ? params.trang_thai : undefined,
      tu_khoa: params.tu_khoa,
    });
    return requestJson<AdminOrdersResponse>(`/api/admin/orders${qs}`, { auth: 'admin' });
  },

  getAdminOrderDetail(maDon: string): Promise<AdminOrderFullResponse> {
    return requestJson<AdminOrderFullResponse>(`/api/admin/orders/${encodeURIComponent(maDon)}`, {
      auth: 'admin',
    });
  },

  previewCancelOrder(maDon: string, ngayGioHuy: string): Promise<CancelPreviewResponse> {
    return requestJson<CancelPreviewResponse>(
      `/api/admin/orders/${encodeURIComponent(maDon)}/cancel-preview`,
      {
        method: 'POST',
        body: { ngay_gio_huy: ngayGioHuy },
        auth: 'admin',
      }
    );
  },

  cancelOrder(maDon: string, payload: CancelOrderRequest): Promise<CancelOrderResponse> {
    return requestJson<CancelOrderResponse>(
      `/api/admin/orders/${encodeURIComponent(maDon)}/cancel`,
      {
        method: 'POST',
        body: payload,
        auth: 'admin',
      }
    );
  },

  updateOrderStatus(maDon: string, trangThaiMoi: OrderStatusCode | string): Promise<UpdateStatusResponse> {
    return requestJson<UpdateStatusResponse>(
      `/api/admin/orders/${encodeURIComponent(maDon)}/status`,
      {
        method: 'PATCH',
        body: { trang_thai_moi: trangThaiMoi },
        auth: 'admin',
      }
    );
  },

  getConfirmationHtml(maDon: string, nguoiLap?: string): Promise<ConfirmationHtmlResponse> {
    const qs = buildQuery({ nguoi_lap: nguoiLap });
    return requestJson<ConfirmationHtmlResponse>(
      `/api/admin/orders/${encodeURIComponent(maDon)}/confirmation/html${qs}`,
      { auth: 'admin' }
    );
  },

  getRevenueReport(tuNgay: string, denNgay: string): Promise<RevenueReportResponse> {
    const qs = buildQuery({ tu_ngay: tuNgay, den_ngay: denNgay });
    return requestJson<RevenueReportResponse>(`/api/admin/reports/revenue${qs}`, {
      auth: 'admin',
    });
  },

  getRevenueHtml(tuNgay: string, denNgay: string, nguoiLap: string): Promise<RevenueHtmlResponse> {
    return requestJson<RevenueHtmlResponse>('/api/admin/reports/revenue/html', {
      method: 'POST',
      body: { tu_ngay: tuNgay, den_ngay: denNgay, nguoi_lap: nguoiLap },
      auth: 'admin',
    });
  },

  async downloadRevenuePdf(tuNgay: string, denNgay: string, nguoiLap: string): Promise<void> {
    const res = await fetch('/api/admin/reports/revenue/pdf', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/pdf',
        ...buildAuthHeaders('admin'),
      },
      body: JSON.stringify({ tu_ngay: tuNgay, den_ngay: denNgay, nguoi_lap: nguoiLap }),
    });
    if (!res.ok) {
      throw await parseErrorResponse(res);
    }
    const blob = await res.blob();
    const filename = extractFilename(
      res.headers.get('Content-Disposition'),
      `bao_cao_doanh_thu_${tuNgay}_${denNgay}.pdf`
    );
    triggerBlobDownload(blob, filename);
  },
};
