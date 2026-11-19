export type OrderStatusCode = 'DAT' | 'THANHTOAN' | 'HOANTHANH' | 'HUY';

export interface MetaResponse {
  current_datetime: string;
  current_date: string;
  brand_name: string;
}

export interface ProvinceItem {
  ma_tinh: string;
  ten_tinh: string;
}

export interface ScheduleSearchItem {
  ma_lich_trinh: string;
  ma_tour: string;
  ten_tour: string;
  mo_ta: string | null;
  noi_di: string;
  noi_den: string;
  ngay_xuat_phat: string;
  so_ngay: number;
  gia_co_ban: number;
  so_cho_con_lai: number;
  diem_tb: number | null;
  so_luot_danh_gia: number;
}

export interface ScheduleSearchParams {
  tu_khoa?: string;
  ma_tinh_den?: string;
  gia_tu?: number | null;
  gia_den?: number | null;
  tu_ngay?: string;
  den_ngay?: string;
  so_khach?: number;
  diem_toi_thieu?: number | null;
}

export interface LandingStats {
  total_provinces: number;
  total_tours: number;
  open_schedules: number;
  total_travelers_served: number;
  avg_rating: number | null;
  total_reviews: number;
}

export interface LandingResponse {
  stats: LandingStats;
  featured_schedules: ScheduleSearchItem[];
}

export interface OpenScheduleItem {
  ma_lich_trinh: string;
  ma_tour: string;
  ten_tour: string;
  mo_ta: string | null;
  noi_di: string;
  ma_tinh_den: string;
  ten_tinh_den: string;
  diem_tap_trung: string;
  ngay_xuat_phat: string;
  ngay_ket_thuc: string;
  so_dem: number;
  gia_co_ban: number;
  so_cho_con_lai: number;
}

export interface AccommodationItem {
  ma_nha_nghi: string;
  ten_nha_nghi: string;
  loai_hinh: string;
  dia_chi: string;
  gia_phong_moi_dem: number;
}

export interface CustomerItem {
  ma_kh: string;
  ho_ten: string;
  email: string;
  dia_chi: string;
  so_dien_thoai: string;
}

export interface DuplicateCheckResponse {
  duplicate: boolean;
  customer: CustomerItem | null;
}

export interface CustomerLoginResponse {
  token: string;
  customer: CustomerItem;
}

export interface AdminUser {
  username: string;
  staff_name: string;
}

export interface AdminLoginResponse {
  token: string;
  username: string;
  staff_name: string;
}

export interface BookingEstimateRequest {
  so_khach: number;
  gia_co_ban: number;
  so_phong: number;
  gia_phong_moi_dem: number;
  so_dem: number;
  co_nha_nghi: boolean;
}

export interface BookingEstimateResponse {
  tien_tour: number;
  tien_phong: number;
  tong_tien: number;
}

export interface CreateBookingRequest {
  la_khach_moi: boolean;
  ma_kh?: string | null;
  ho_ten?: string | null;
  so_dien_thoai?: string | null;
  email?: string | null;
  dia_chi?: string | null;
  ma_lich_trinh: string;
  so_khach: number;
  ma_nha_nghi?: string | null;
  so_phong: number;
  co_xe_don: boolean;
  dia_chi_don?: string | null;
  gio_don?: string | null;
  co_xe_ve: boolean;
  gio_ve_noi_nghi?: string | null;
}

export interface CreateBookingResponse {
  ma_don_hang: string;
  ma_kh: string;
  tong_tien: number;
  customer: CustomerItem;
  customer_token: string;
}

export interface CustomerOrderItem {
  ma_don_hang: string;
  ma_tour: string;
  ten_tour: string;
  tinh_den: string;
  ma_lich_trinh: string;
  ngay_dat: string;
  ngay_xuat_phat: string;
  ngay_ket_thuc: string;
  so_luong_khach: number;
  ma_nha_nghi: string | null;
  ten_nha_nghi: string | null;
  so_phong: number;
  tien_tour: number;
  tien_phong: number;
  tong_tien: number;
  ma_trang_thai: OrderStatusCode;
  ten_trang_thai: string;
  ngay_huy: string | null;
  ly_do_huy: string | null;
  ty_le_phat: number | null;
  tien_phat: number | null;
  tien_hoan: number | null;
  diem_tour: number | null;
  nhan_xet_tour: string | null;
  diem_nha_nghi: number | null;
  nhan_xet_nha_nghi: string | null;
  ngay_danh_gia: string | null;
  co_the_danh_gia: boolean;
}

export interface PendingReviewItem {
  ma_don_hang: string;
  ma_tour: string;
  ten_tour: string;
  ngay_xuat_phat: string;
  ngay_ket_thuc: string;
  ma_nha_nghi: string | null;
  ten_nha_nghi: string | null;
  ngay_dat: string;
  tong_tien: number;
}

export interface SubmitReviewRequest {
  ma_don_hang: string;
  diem_tour: number;
  nhan_xet_tour?: string | null;
  co_danh_gia_nha_nghi: boolean;
  diem_nha_nghi?: number | null;
  nhan_xet_nha_nghi?: string | null;
}

export interface SubmitReviewResponse {
  message: string;
  ma_don_hang: string;
  ngay_danh_gia: string;
}

export interface AdminOrderCounts {
  ALL: number;
  DAT: number;
  THANHTOAN: number;
  HOANTHANH: number;
  HUY: number;
}

export interface AdminOrderSummary {
  ma_don_hang: string;
  ma_kh: string;
  ho_ten: string;
  ma_tour: string;
  ten_tour: string;
  tinh_den: string;
  ma_lich_trinh: string;
  ngay_dat: string;
  ngay_xuat_phat: string;
  ngay_ket_thuc: string;
  so_luong_khach: number;
  ma_nha_nghi: string | null;
  ten_nha_nghi: string | null;
  so_phong: number;
  tien_tour: number;
  tien_phong: number;
  tong_tien: number;
  ma_trang_thai: OrderStatusCode;
  ten_trang_thai: string;
  ngay_huy: string | null;
  tien_phat: number | null;
  tien_hoan: number | null;
}

export interface AdminOrdersResponse {
  counts: AdminOrderCounts;
  orders: AdminOrderSummary[];
}

export interface AdminOrderDetail {
  ma_don_hang: string;
  ma_kh: string;
  ho_ten: string;
  email: string | null;
  dia_chi: string | null;
  dia_chi_kh: string | null;
  ma_tour: string;
  ten_tour: string;
  tinh_xuat_phat: string | null;
  tinh_den: string;
  ma_lich_trinh: string;
  diem_tap_trung: string | null;
  ngay_xuat_phat: string;
  ngay_ket_thuc: string;
  so_dem: number;
  ma_nha_nghi: string | null;
  ten_nha_nghi: string | null;
  loai_hinh_nha_nghi: string | null;
  dia_chi_nha_nghi: string | null;
  so_luong_khach: number;
  so_phong: number;
  gia_co_ban: number;
  gia_phong_moi_dem: number | null;
  ngay_dat: string;
  ma_trang_thai: OrderStatusCode;
  ten_trang_thai: string;
  tien_tour: number;
  tien_phong: number;
  tong_tien: number;
  ngay_huy: string | null;
  ly_do_huy: string | null;
  ty_le_phat: number | null;
  tien_phat: number | null;
  tien_hoan: number | null;
}

export interface ValidNextStatus {
  ma_trang_thai: OrderStatusCode;
  ten_trang_thai: string;
}

export interface ShuttleItem {
  ten_loai_chuyen: string;
  thoi_gian_don: string;
  diem_don: string;
  diem_tra: string;
  bien_so_xe: string;
  don_vi_van_tai: string;
}

export interface AdminOrderFullResponse {
  detail: AdminOrderDetail;
  valid_next_statuses: ValidNextStatus[];
  phone_numbers: string;
  shuttles: ShuttleItem[];
}

export interface CancelPreviewResponse {
  ma_don_hang: string;
  tong_tien: number;
  so_ngay_truoc_khoi_hanh: number;
  so_gio_sau_khi_dat: number;
  ty_le_phat: number;
  tien_phat: number;
  tien_hoan: number;
}

export interface CancelOrderRequest {
  ngay_gio_huy: string;
  ly_do_huy: string;
  da_dong_y_phat: boolean;
}

export interface CancelOrderResponse {
  message: string;
  ma_don_hang: string;
  tien_phat: number;
  tien_hoan: number;
  so_cho_hoan: number;
}

export interface UpdateStatusResponse {
  message: string;
  ma_don_hang: string;
  ma_trang_thai: OrderStatusCode;
}

export interface ConfirmationHtmlResponse {
  html: string;
  ma_don_hang: string;
}

export interface RevenueSummary {
  tong_doanh_thu: number;
  so_don: number;
  so_khach: number;
  so_don_huy: number;
}

export interface RevenueTourRow {
  ma_tour: string;
  ten_tour: string;
  so_lich_trinh: number;
  so_don: number;
  so_khach: number;
  so_don_huy: number;
  doanh_thu_dich_vu: number;
  tien_phat_huy: number;
  tong_doanh_thu: number;
  diem_tour_tb: number | null;
}

export interface AccommodationRankRow {
  ma_nha_nghi: string;
  ten_nha_nghi: string;
  loai_hinh: string;
  ten_tinh: string;
  so_luot_danh_gia: number;
  diem_tb: number | null;
}

export interface RevenueReportResponse {
  summary: RevenueSummary;
  tours: RevenueTourRow[];
  accommodations: AccommodationRankRow[];
  noi_nhan: string;
}

export interface RevenueHtmlResponse {
  html: string;
}
