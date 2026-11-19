"""Các mô hình Pydantic v2 định nghĩa hợp đồng JSON cho REST API Bắc Việt Travel."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MetaResponse(BaseModel):
    current_datetime: str
    current_date: str
    brand_name: str = "Bắc Việt Travel"


class ProvinceItem(BaseModel):
    ma_tinh: str
    ten_tinh: str


class ScheduleSearchItem(BaseModel):
    ma_lich_trinh: str
    ma_tour: str
    ten_tour: str
    mo_ta: str
    noi_di: str
    noi_den: str
    ngay_xuat_phat: str
    so_ngay: int
    gia_co_ban: int
    so_cho_con_lai: int
    diem_tb: float | None = None
    so_luot_danh_gia: int


class LandingStats(BaseModel):
    total_provinces: int
    total_tours: int
    open_schedules: int
    total_travelers_served: int
    avg_rating: float | None = None
    total_reviews: int


class LandingResponse(BaseModel):
    stats: LandingStats
    featured_schedules: list[ScheduleSearchItem]


class OpenScheduleItem(BaseModel):
    ma_lich_trinh: str
    ma_tour: str
    ten_tour: str
    mo_ta: str
    noi_di: str
    ma_tinh_den: str
    ten_tinh_den: str
    diem_tap_trung: str
    ngay_xuat_phat: str
    ngay_ket_thuc: str
    so_dem: int
    gia_co_ban: int
    so_cho_con_lai: int


class AccommodationItem(BaseModel):
    ma_nha_nghi: str
    ten_nha_nghi: str
    loai_hinh: str
    dia_chi: str
    gia_phong_moi_dem: int


class CustomerItem(BaseModel):
    ma_kh: str
    ho_ten: str
    email: str
    dia_chi: str
    so_dien_thoai: str


class CheckDuplicateRequest(BaseModel):
    email: str = ""
    so_dien_thoai: str = ""


class CheckDuplicateResponse(BaseModel):
    duplicate: bool
    customer: CustomerItem | None = None


class CustomerLoginRequest(BaseModel):
    identifier: str = Field(..., description="Email hoặc số điện thoại khách hàng")


class CustomerLoginResponse(BaseModel):
    token: str
    customer: CustomerItem


class AdminLoginRequest(BaseModel):
    username: str
    password: str
    staff_name: str | None = None


class AdminLoginResponse(BaseModel):
    token: str
    username: str
    staff_name: str


class BookingEstimateRequest(BaseModel):
    so_khach: int
    gia_co_ban: int
    so_phong: int = 0
    gia_phong_moi_dem: int = 0
    so_dem: int = 0
    co_nha_nghi: bool = False


class BookingEstimateResponse(BaseModel):
    tien_tour: int
    tien_phong: int
    tong_tien: int


class BookingCreateRequest(BaseModel):
    la_khach_moi: bool = False
    ma_kh: str | None = None
    ho_ten: str | None = None
    so_dien_thoai: str | None = None
    email: str | None = None
    dia_chi: str | None = None
    ma_lich_trinh: str
    so_khach: int
    ma_nha_nghi: str | None = None
    so_phong: int = 0
    co_xe_don: bool = False
    dia_chi_don: str | None = None
    gio_don: str | None = None
    co_xe_ve: bool = False
    gio_ve_noi_nghi: str | None = None


class BookingCreateResponse(BaseModel):
    ma_don_hang: str
    ma_kh: str
    tong_tien: int
    customer: CustomerItem
    customer_token: str


class CustomerOrderItem(BaseModel):
    ma_don_hang: str
    ma_tour: str
    ten_tour: str
    tinh_den: str
    ma_lich_trinh: str
    ngay_dat: str
    ngay_xuat_phat: str
    ngay_ket_thuc: str
    so_luong_khach: int
    ma_nha_nghi: str | None = None
    ten_nha_nghi: str | None = None
    so_phong: int
    tien_tour: int
    tien_phong: int
    tong_tien: int
    ma_trang_thai: str
    ten_trang_thai: str
    ngay_huy: str | None = None
    ly_do_huy: str | None = None
    ty_le_phat: int | None = None
    tien_phat: int | None = None
    tien_hoan: int | None = None
    diem_tour: int | None = None
    nhan_xet_tour: str | None = None
    diem_nha_nghi: int | None = None
    nhan_xet_nha_nghi: str | None = None
    ngay_danh_gia: str | None = None
    co_the_danh_gia: bool


class PendingReviewItem(BaseModel):
    ma_don_hang: str
    ma_tour: str
    ten_tour: str
    ngay_xuat_phat: str
    ngay_ket_thuc: str
    ma_nha_nghi: str | None = None
    ten_nha_nghi: str | None = None
    ngay_dat: str
    tong_tien: int


class ReviewCreateRequest(BaseModel):
    ma_don_hang: str
    diem_tour: int
    nhan_xet_tour: str | None = None
    co_danh_gia_nha_nghi: bool = False
    diem_nha_nghi: int | None = None
    nhan_xet_nha_nghi: str | None = None


class ReviewCreateResponse(BaseModel):
    message: str
    ma_don_hang: str
    ngay_danh_gia: str


class AdminOrderCounts(BaseModel):
    ALL: int
    DAT: int
    THANHTOAN: int
    HOANTHANH: int
    HUY: int


class AdminOrderSummary(BaseModel):
    ma_don_hang: str
    ma_kh: str
    ho_ten: str
    ma_tour: str
    ten_tour: str
    tinh_den: str
    ma_lich_trinh: str
    ngay_dat: str
    ngay_xuat_phat: str
    ngay_ket_thuc: str
    so_luong_khach: int
    ma_nha_nghi: str | None = None
    ten_nha_nghi: str | None = None
    so_phong: int
    tien_tour: int
    tien_phong: int
    tong_tien: int
    ma_trang_thai: str
    ten_trang_thai: str
    ngay_huy: str | None = None
    tien_phat: int | None = None
    tien_hoan: int | None = None


class AdminOrdersListResponse(BaseModel):
    counts: AdminOrderCounts
    orders: list[AdminOrderSummary]


class ValidNextStatus(BaseModel):
    ma_trang_thai: str
    ten_trang_thai: str


class ShuttleItem(BaseModel):
    ten_loai_chuyen: str
    thoi_gian_don: str
    diem_don: str
    diem_tra: str
    bien_so_xe: str
    don_vi_van_tai: str


class AdminOrderDetail(BaseModel):
    ma_don_hang: str
    ma_kh: str
    ho_ten: str
    email: str | None = None
    dia_chi: str | None = None
    dia_chi_kh: str | None = None
    ma_tour: str
    ten_tour: str
    tinh_xuat_phat: str | None = None
    tinh_den: str
    ma_lich_trinh: str
    diem_tap_trung: str | None = None
    ngay_xuat_phat: str
    ngay_ket_thuc: str
    so_dem: int
    ma_nha_nghi: str | None = None
    ten_nha_nghi: str | None = None
    loai_hinh_nha_nghi: str | None = None
    dia_chi_nha_nghi: str | None = None
    so_luong_khach: int
    so_phong: int
    gia_co_ban: int
    gia_phong_moi_dem: int | None = None
    ngay_dat: str
    ma_trang_thai: str
    ten_trang_thai: str
    tien_tour: int
    tien_phong: int
    tong_tien: int
    ngay_huy: str | None = None
    ly_do_huy: str | None = None
    ty_le_phat: int | None = None
    tien_phat: int | None = None
    tien_hoan: int | None = None


class AdminOrderFullResponse(BaseModel):
    detail: AdminOrderDetail
    valid_next_statuses: list[ValidNextStatus]
    phone_numbers: str
    shuttles: list[ShuttleItem]


class CancelPreviewRequest(BaseModel):
    ngay_gio_huy: str


class CancelPreviewResponse(BaseModel):
    ma_don_hang: str
    tong_tien: int
    so_ngay_truoc_khoi_hanh: int
    so_gio_sau_khi_dat: int
    ty_le_phat: int
    tien_phat: int
    tien_hoan: int


class CancelOrderRequest(BaseModel):
    ngay_gio_huy: str
    ly_do_huy: str
    da_dong_y_phat: bool


class CancelOrderResponse(BaseModel):
    message: str
    ma_don_hang: str
    tien_phat: int
    tien_hoan: int
    so_cho_hoan: int


class UpdateOrderStatusRequest(BaseModel):
    trang_thai_moi: str


class UpdateOrderStatusResponse(BaseModel):
    message: str
    ma_don_hang: str
    ma_trang_thai: str


class ConfirmationHtmlResponse(BaseModel):
    html: str
    ma_don_hang: str


class RevenueSummary(BaseModel):
    tong_doanh_thu: int
    so_don: int
    so_khach: int
    so_don_huy: int


class RevenueTourRow(BaseModel):
    ma_tour: str
    ten_tour: str
    so_lich_trinh: int
    so_don: int
    so_khach: int
    so_don_huy: int
    doanh_thu_dich_vu: int
    tien_phat_huy: int
    tong_doanh_thu: int
    diem_tour_tb: float | None = None


class AccommodationRankRow(BaseModel):
    ma_nha_nghi: str
    ten_nha_nghi: str
    loai_hinh: str
    ten_tinh: str
    so_luot_danh_gia: int
    diem_tb: float | None = None


class RevenueReportResponse(BaseModel):
    summary: RevenueSummary
    tours: list[RevenueTourRow]
    accommodations: list[AccommodationRankRow]
    noi_nhan: str


class RevenueHtmlRequest(BaseModel):
    tu_ngay: str
    den_ngay: str
    nguoi_lap: str


class RevenueHtmlResponse(BaseModel):
    html: str
