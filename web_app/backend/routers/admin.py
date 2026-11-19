"""Các endpoint quản trị: quản lý đơn hàng, xử lý trạng thái/hủy đơn, phiếu xác nhận và báo cáo doanh thu."""

from __future__ import annotations

from datetime import date
from typing import Any

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, Response

try:
    from .. import pdf_service, queries
    from ..dependencies import (
        AppValidationError,
        clean_user_message,
        db,
        mysql_error_to_http,
        parse_date_input,
        parse_datetime_input,
        require_admin,
        services,
        to_int,
        to_iso,
        to_opt_float,
        to_opt_int,
    )
    from ..schemas import (
        AccommodationRankRow,
        AdminOrderDetail,
        AdminOrderFullResponse,
        AdminOrdersListResponse,
        CancelOrderRequest,
        CancelOrderResponse,
        CancelPreviewRequest,
        CancelPreviewResponse,
        ConfirmationHtmlResponse,
        RevenueHtmlRequest,
        RevenueHtmlResponse,
        RevenueReportResponse,
        RevenueSummary,
        RevenueTourRow,
        ShuttleItem,
        UpdateOrderStatusRequest,
        UpdateOrderStatusResponse,
        ValidNextStatus,
    )
except ImportError:
    import pdf_service
    import queries
    from dependencies import (
        AppValidationError,
        clean_user_message,
        db,
        mysql_error_to_http,
        parse_date_input,
        parse_datetime_input,
        require_admin,
        services,
        to_int,
        to_iso,
        to_opt_float,
        to_opt_int,
    )
    from schemas import (
        AccommodationRankRow,
        AdminOrderDetail,
        AdminOrderFullResponse,
        AdminOrdersListResponse,
        CancelOrderRequest,
        CancelOrderResponse,
        CancelPreviewRequest,
        CancelPreviewResponse,
        ConfirmationHtmlResponse,
        RevenueHtmlRequest,
        RevenueHtmlResponse,
        RevenueReportResponse,
        RevenueSummary,
        RevenueTourRow,
        ShuttleItem,
        UpdateOrderStatusRequest,
        UpdateOrderStatusResponse,
        ValidNextStatus,
    )

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)],
)


def _validate_report_range(tu_ngay_raw: str | None, den_ngay_raw: str | None) -> tuple[date, date]:
    try:
        tu_ngay = parse_date_input(tu_ngay_raw) or date(2026, 9, 1)
        den_ngay = parse_date_input(den_ngay_raw) or date(2026, 12, 31)
    except ValueError as exc:
        raise AppValidationError("Định dạng kỳ báo cáo không hợp lệ (YYYY-MM-DD).") from exc

    if den_ngay < tu_ngay:
        raise AppValidationError("Đến ngày phải lớn hơn hoặc bằng từ ngày.")
    return tu_ngay, den_ngay


@router.get("/orders", response_model=AdminOrdersListResponse)
def list_admin_orders(
    trang_thai: str | None = Query(default=None),
    tu_khoa: str | None = Query(default=None),
) -> AdminOrdersListResponse:
    data = queries.get_admin_orders(trang_thai=trang_thai, tu_khoa=tu_khoa)
    return AdminOrdersListResponse(**data)


@router.get("/orders/{ma_don}", response_model=AdminOrderFullResponse)
def get_admin_order_detail(ma_don: str) -> AdminOrderFullResponse:
    ct_f2 = services.lay_chi_tiet_don_f2(ma_don)
    if ct_f2 is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    ct_r1 = services.lay_chi_tiet_don_r1(ma_don) or {}
    valid_next = services.lay_trang_thai_dich_f2(ma_don, db.hien_tai())
    phone_numbers = services.lay_sdt_khach_r1(ma_don)
    raw_shuttles = services.lay_lich_trung_chuyen_r1(ma_don)

    detail = AdminOrderDetail(
        ma_don_hang=ct_f2["MaDonHang"],
        ma_kh=ct_f2["MaKH"],
        ho_ten=ct_f2["HoTen"],
        email=ct_r1.get("Email"),
        dia_chi=ct_r1.get("DiaChiKH"),
        dia_chi_kh=ct_r1.get("DiaChiKH"),
        ma_tour=ct_r1.get("MaTour") or "",
        ten_tour=ct_r1.get("TenTour") or "",
        tinh_xuat_phat=ct_r1.get("TinhXuatPhat"),
        tinh_den=ct_r1.get("TinhDen") or "",
        ma_lich_trinh=ct_f2["MaLichTrinh"],
        diem_tap_trung=ct_r1.get("DiemTapTrung"),
        ngay_xuat_phat=to_iso(ct_f2["NgayXuatPhat"]),
        ngay_ket_thuc=to_iso(ct_f2["NgayKetThuc"]),
        so_dem=to_int(ct_r1.get("SoDem")),
        ma_nha_nghi=ct_f2.get("MaNhaNghi"),
        ten_nha_nghi=ct_f2.get("TenNhaNghi"),
        loai_hinh_nha_nghi=ct_r1.get("LoaiHinh"),
        dia_chi_nha_nghi=ct_r1.get("DiaChiNhaNghi"),
        so_luong_khach=to_int(ct_f2["SoLuongKhach"]),
        so_phong=to_int(ct_f2["SoPhong"]),
        gia_co_ban=to_int(ct_r1.get("GiaCoBan")),
        gia_phong_moi_dem=to_opt_int(ct_r1.get("GiaPhongMoiDem")),
        ngay_dat=to_iso(ct_f2["NgayDat"]),
        ma_trang_thai=ct_f2["MaTrangThai"],
        ten_trang_thai=ct_f2["TenTrangThai"],
        tien_tour=to_int(ct_f2["TienTour"]),
        tien_phong=to_int(ct_f2["TienPhong"]),
        tong_tien=to_int(ct_f2["TongTien"]),
        ngay_huy=to_iso(ct_r1.get("NgayHuy")),
        ly_do_huy=ct_r1.get("LyDoHuy"),
        ty_le_phat=to_opt_int(ct_r1.get("TyLePhat")),
        tien_phat=to_opt_int(ct_r1.get("TienPhat")),
        tien_hoan=to_opt_int(ct_r1.get("TienHoan")),
    )

    shuttles = [
        ShuttleItem(
            ten_loai_chuyen=r["TenLoaiChuyen"],
            thoi_gian_don=to_iso(r["ThoiGianDon"]),
            diem_don=r["DiemDon"] or "",
            diem_tra=r["DiemTra"] or "",
            bien_so_xe=r["BienSoXe"] or "Chưa xếp xe",
            don_vi_van_tai=r["DonViVanTai"] or "Chưa xếp",
        )
        for r in raw_shuttles
    ]

    return AdminOrderFullResponse(
        detail=detail,
        valid_next_statuses=[
            ValidNextStatus(
                ma_trang_thai=r["MaTrangThai"],
                ten_trang_thai=r["TenTrangThai"],
            )
            for r in valid_next
        ],
        phone_numbers=phone_numbers,
        shuttles=shuttles,
    )


@router.post("/orders/{ma_don}/cancel-preview", response_model=CancelPreviewResponse)
def preview_cancel_order(
    ma_don: str,
    body: CancelPreviewRequest,
) -> CancelPreviewResponse:
    try:
        ngay_gio_huy = parse_datetime_input(body.ngay_gio_huy)
    except ValueError as exc:
        raise AppValidationError("Thời điểm hủy không đúng định dạng ngày giờ.") from exc

    if ngay_gio_huy is None:
        raise AppValidationError("Vui lòng chọn thời điểm hủy đơn hàng.")

    preview = services.tinh_xem_truoc_phat_huy(ma_don, ngay_gio_huy)
    if preview is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    return CancelPreviewResponse(
        ma_don_hang=preview["MaDonHang"],
        tong_tien=to_int(preview["TongTien"]),
        so_ngay_truoc_khoi_hanh=to_int(preview["SoNgayTruocKhoiHanh"]),
        so_gio_sau_khi_dat=to_int(preview["SoGioSauKhiDat"]),
        ty_le_phat=to_int(preview["TyLePhat"]),
        tien_phat=to_int(preview["TienPhat"]),
        tien_hoan=to_int(preview["TienHoan"]),
    )


@router.post("/orders/{ma_don}/cancel", response_model=CancelOrderResponse)
def cancel_order(
    ma_don: str,
    body: CancelOrderRequest,
) -> CancelOrderResponse:
    ct = services.lay_chi_tiet_don_f2(ma_don)
    if ct is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    if ct["MaTrangThai"] not in ("DAT", "THANHTOAN"):
        raise HTTPException(
            status_code=409,
            detail="Đơn hàng không còn ở trạng thái mở để thực hiện hủy.",
        )

    try:
        ngay_gio_huy = parse_datetime_input(body.ngay_gio_huy)
    except ValueError as exc:
        raise AppValidationError("Thời điểm hủy không đúng định dạng ngày giờ.") from exc

    if ngay_gio_huy is None:
        raise AppValidationError("Vui lòng chọn thời điểm hủy đơn hàng.")

    errors = services.kiem_tra_huy_don(
        ngay_dat=ct["NgayDat"],
        ngay_xuat_phat=ct["NgayXuatPhat"],
        ngay_gio_huy=ngay_gio_huy,
        ly_do_huy=body.ly_do_huy,
        da_dong_y_phat=body.da_dong_y_phat,
    )
    if errors:
        cleaned = [clean_user_message(m) for m in errors]
        raise AppValidationError(detail=cleaned[0], errors=cleaned, status_code=400)

    preview = services.tinh_xem_truoc_phat_huy(ma_don, ngay_gio_huy)
    if preview is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    try:
        services.huy_don(ma_don, ngay_gio_huy, body.ly_do_huy)
    except (mysql.connector.Error, db.KhongCoDongNao, ValueError) as exc:
        raise mysql_error_to_http(exc) from exc

    return CancelOrderResponse(
        message="Đã hủy đơn hàng, hoàn chỗ cho lịch trình và hủy chuyến trung chuyển liên quan.",
        ma_don_hang=ma_don,
        tien_phat=to_int(preview["TienPhat"]),
        tien_hoan=to_int(preview["TienHoan"]),
        so_cho_hoan=to_int(ct["SoLuongKhach"]),
    )


@router.patch("/orders/{ma_don}/status", response_model=UpdateOrderStatusResponse)
def update_order_status(
    ma_don: str,
    body: UpdateOrderStatusRequest,
) -> UpdateOrderStatusResponse:
    trang_thai_moi = (body.trang_thai_moi or "").strip().upper()
    if trang_thai_moi not in ("THANHTOAN", "HOANTHANH"):
        raise AppValidationError(
            "Trạng thái cập nhật không hợp lệ. Chỉ hỗ trợ chuyển sang Đã thanh toán hoặc Hoàn thành tour."
        )

    ct = services.lay_chi_tiet_don_f2(ma_don)
    if ct is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    try:
        services.chuyen_trang_thai_don(ma_don, trang_thai_moi, db.hien_tai())
    except (mysql.connector.Error, db.KhongCoDongNao, ValueError) as exc:
        raise mysql_error_to_http(exc) from exc

    return UpdateOrderStatusResponse(
        message="Đã cập nhật trạng thái đơn hàng thành công.",
        ma_don_hang=ma_don,
        ma_trang_thai=trang_thai_moi,
    )


@router.get("/orders/{ma_don}/confirmation/html", response_model=ConfirmationHtmlResponse)
def get_confirmation_html(
    ma_don: str,
    nguoi_lap: str | None = Query(default=None),
    admin: dict[str, Any] = Depends(require_admin),
) -> ConfirmationHtmlResponse:
    issuer = (nguoi_lap or "").strip() or admin["staff_name"]
    html = pdf_service.build_confirmation_html(ma_don, issuer)
    return ConfirmationHtmlResponse(html=html, ma_don_hang=ma_don)


@router.get("/reports/revenue", response_model=RevenueReportResponse)
def get_revenue_report(
    tu_ngay: str | None = Query(default=None),
    den_ngay: str | None = Query(default=None),
) -> RevenueReportResponse:
    start_date, end_date = _validate_report_range(tu_ngay, den_ngay)
    ds_tour = services.lay_doanh_thu_tour_r2(start_date, end_date)
    ds_noi_nghi = services.lay_xep_hang_noi_nghi_r2(start_date, end_date)

    rollup = next((r for r in ds_tour if r.get("MaTour") == "TỔNG CỘNG"), None)
    if rollup is not None:
        summary = RevenueSummary(
            tong_doanh_thu=to_int(rollup.get("TongDoanhThu")),
            so_don=to_int(rollup.get("SoDon")),
            so_khach=to_int(rollup.get("SoKhach")),
            so_don_huy=to_int(rollup.get("SoDonHuy")),
        )
    else:
        summary = RevenueSummary(
            tong_doanh_thu=sum(to_int(r.get("TongDoanhThu")) for r in ds_tour),
            so_don=sum(to_int(r.get("SoDon")) for r in ds_tour),
            so_khach=sum(to_int(r.get("SoKhach")) for r in ds_tour),
            so_don_huy=sum(to_int(r.get("SoDonHuy")) for r in ds_tour),
        )

    tours = [
        RevenueTourRow(
            ma_tour=str(r.get("MaTour") or ""),
            ten_tour=str(r.get("TenTour") or ""),
            so_lich_trinh=to_int(r.get("SoLichTrinh")),
            so_don=to_int(r.get("SoDon")),
            so_khach=to_int(r.get("SoKhach")),
            so_don_huy=to_int(r.get("SoDonHuy")),
            doanh_thu_dich_vu=to_int(r.get("DoanhThuDichVu")),
            tien_phat_huy=to_int(r.get("TienPhatHuy")),
            tong_doanh_thu=to_int(r.get("TongDoanhThu")),
            diem_tour_tb=to_opt_float(r.get("DiemTourTB")),
        )
        for r in ds_tour
    ]

    accommodations = [
        AccommodationRankRow(
            ma_nha_nghi=str(r.get("MaNhaNghi") or ""),
            ten_nha_nghi=str(r.get("TenNhaNghi") or ""),
            loai_hinh=str(r.get("LoaiHinh") or ""),
            ten_tinh=str(r.get("TenTinh") or ""),
            so_luot_danh_gia=to_int(r.get("SoLuotDanhGia")),
            diem_tb=to_opt_float(r.get("DiemTB")),
        )
        for r in ds_noi_nghi
    ]

    return RevenueReportResponse(
        summary=summary,
        tours=tours,
        accommodations=accommodations,
        noi_nhan=services.NOI_NHAN_R2,
    )


@router.post("/reports/revenue/html", response_model=RevenueHtmlResponse)
def get_revenue_report_html(body: RevenueHtmlRequest) -> RevenueHtmlResponse:
    start_date, end_date = _validate_report_range(body.tu_ngay, body.den_ngay)
    nguoi_lap = (body.nguoi_lap or "").strip()
    if not nguoi_lap:
        raise AppValidationError("Vui lòng nhập họ tên người lập báo cáo.")

    html = pdf_service.build_revenue_report_html(start_date, end_date, nguoi_lap)
    return RevenueHtmlResponse(html=html)


@router.post("/reports/revenue/pdf")
def download_revenue_report_pdf(body: RevenueHtmlRequest) -> Response:
    start_date, end_date = _validate_report_range(body.tu_ngay, body.den_ngay)
    nguoi_lap = (body.nguoi_lap or "").strip()
    if not nguoi_lap:
        raise AppValidationError("Vui lòng nhập họ tên người lập báo cáo.")

    html = pdf_service.build_revenue_report_html(start_date, end_date, nguoi_lap)
    pdf_bytes = pdf_service.render_html_to_pdf(html)
    filename = f"BaoCaoDoanhThu_{start_date.isoformat()}_{end_date.isoformat()}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
