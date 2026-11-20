"""Các endpoint đặt tour, xem đơn hàng cá nhân, đánh giá chuyến đi và xuất phiếu PDF cho chủ đơn."""

from __future__ import annotations

import unicodedata
from typing import Any

import mysql.connector
from fastapi import APIRouter, Depends, HTTPException, Query, Response

try:
    from .. import pdf_service, queries
    from ..dependencies import (
        AppValidationError,
        clean_user_message,
        db,
        ensure_customer_or_admin,
        get_optional_auth,
        mysql_error_to_http,
        parse_datetime_input,
        require_customer,
        services,
        sign_customer_token,
        to_int,
        to_iso,
    )
    from ..schemas import (
        BookingCreateRequest,
        BookingCreateResponse,
        BookingEstimateRequest,
        BookingEstimateResponse,
        CustomerItem,
        CustomerOrderItem,
        PendingReviewItem,
        ReviewCreateRequest,
        ReviewCreateResponse,
    )
except ImportError:
    import pdf_service
    import queries
    from dependencies import (
        AppValidationError,
        clean_user_message,
        db,
        ensure_customer_or_admin,
        get_optional_auth,
        mysql_error_to_http,
        parse_datetime_input,
        require_customer,
        services,
        sign_customer_token,
        to_int,
        to_iso,
    )
    from schemas import (
        BookingCreateRequest,
        BookingCreateResponse,
        BookingEstimateRequest,
        BookingEstimateResponse,
        CustomerItem,
        CustomerOrderItem,
        PendingReviewItem,
        ReviewCreateRequest,
        ReviewCreateResponse,
    )

router = APIRouter(prefix="/api", tags=["bookings"])


def _normalize_full_name(raw: str | None) -> str:
    return " ".join(unicodedata.normalize("NFC", raw or "").strip().split())


def _validate_full_name(raw: str | None) -> str | None:
    cleaned = _normalize_full_name(raw)
    if not cleaned or len(cleaned) > 100:
        return None
    if len(cleaned.replace(" ", "")) < 2 or not all(ch.isalpha() or ch == " " for ch in cleaned):
        return (
            "Họ và tên chỉ được chứa chữ cái và khoảng trắng "
            "(tối thiểu 2 ký tự, không chứa số hoặc ký tự đặc biệt)."
        )
    return None


@router.post("/bookings/estimate", response_model=BookingEstimateResponse)
def estimate_booking(body: BookingEstimateRequest) -> BookingEstimateResponse:
    if body.so_khach < 0 or body.gia_co_ban < 0 or body.so_phong < 0 or body.gia_phong_moi_dem < 0:
        raise AppValidationError("Thông số tính dự toán chi phí không được âm.")
    tien_tour, tien_phong, tong_tien = services.tinh_du_toan_f1(
        so_khach=body.so_khach,
        gia_co_ban=body.gia_co_ban,
        so_phong=body.so_phong,
        gia_phong_moi_dem=body.gia_phong_moi_dem,
        so_dem=body.so_dem,
        co_nha_nghi=body.co_nha_nghi,
    )
    return BookingEstimateResponse(
        tien_tour=int(tien_tour),
        tien_phong=int(tien_phong),
        tong_tien=int(tong_tien),
    )


@router.post("/bookings", response_model=BookingCreateResponse)
def create_booking(body: BookingCreateRequest) -> BookingCreateResponse:
    schedule = queries.get_schedule_for_booking(body.ma_lich_trinh.strip())
    if schedule is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy lịch trình đã chọn.")

    now = db.hien_tai()
    so_dem = to_int(schedule["SoDem"])
    so_cho_con_lai = to_int(schedule["SoChoConLai"])

    ma_nha_nghi = (body.ma_nha_nghi or "").strip() or None
    co_nha_nghi = ma_nha_nghi is not None
    so_phong = int(body.so_phong) if co_nha_nghi else 0

    errors: list[str] = []

    if co_nha_nghi:
        accommodation = queries.get_accommodation_by_id(ma_nha_nghi)
        if accommodation is None:
            errors.append("Nơi nghỉ đã chọn không tồn tại trong hệ thống.")
        elif accommodation["MaTinh"] != schedule["MaTinhDen"]:
            errors.append("Nơi nghỉ đã chọn không thuộc tỉnh điểm đến của hành trình.")

    if not body.la_khach_moi:
        ma_kh_clean = (body.ma_kh or "").strip()
        if ma_kh_clean and queries.get_customer_by_id(ma_kh_clean) is None:
            errors.append("Khách hàng đã chọn không tồn tại trong hệ thống.")

    dt_don = None
    if body.co_xe_don:
        try:
            dt_don = parse_datetime_input(body.gio_don)
        except ValueError:
            errors.append("Thời gian đón tại nhà không đúng định dạng ngày giờ.")

    dt_ve = None
    if body.co_xe_ve:
        try:
            dt_ve = parse_datetime_input(body.gio_ve_noi_nghi)
        except ValueError:
            errors.append("Thời gian xe về nơi nghỉ không đúng định dạng ngày giờ.")

    normalized_ho_ten = _normalize_full_name(body.ho_ten)

    validation_errors = services.kiem_tra_dat_tour(
        la_khach_moi=body.la_khach_moi,
        ma_kh=body.ma_kh,
        ho_ten=normalized_ho_ten,
        so_dien_thoai=body.so_dien_thoai or "",
        email=body.email or "",
        dia_chi=body.dia_chi or "",
        so_khach=body.so_khach,
        so_cho_con_lai=so_cho_con_lai,
        so_dem=so_dem,
        co_nha_nghi=co_nha_nghi,
        so_phong=so_phong,
        co_xe_don=body.co_xe_don,
        dia_chi_don=body.dia_chi_don if body.co_xe_don else None,
        dt_don=dt_don,
        co_xe_ve=body.co_xe_ve,
        dt_ve=dt_ve,
        thoi_diem_hien_tai=now,
        ngay_xuat_phat=schedule["NgayXuatPhat"],
        ngay_ket_thuc=schedule["NgayKetThuc"],
    )
    errors.extend(clean_user_message(msg) for msg in validation_errors)

    target_la_khach_moi = body.la_khach_moi
    target_ma_kh = (body.ma_kh or "").strip() or None

    if target_la_khach_moi:
        full_name_error = _validate_full_name(normalized_ho_ten)
        if full_name_error:
            errors.append(full_name_error)

        # Kiểm tra nếu trùng cả 3 thông tin (Họ tên, SĐT, Email) -> tự động chuyển sang gắn khách cũ
        exact_customer = queries.find_customer_by_name_phone_email(
            normalized_ho_ten,
            body.so_dien_thoai or "",
            body.email or "",
        )
        if exact_customer is not None:
            target_la_khach_moi = False
            target_ma_kh = exact_customer["ma_kh"]
        else:
            duplicate = services.kiem_tra_trung_khach_hang(
                body.email or "",
                body.so_dien_thoai or "",
            )
            if duplicate is not None:
                errors.append(
                    f"Email hoặc số điện thoại đã thuộc về khách hàng {duplicate['HoTen']} "
                    f"({duplicate['MaKH']}). Vui lòng kiểm tra lại họ tên hoặc thông tin liên hệ."
                )

    if errors:
        raise AppValidationError(detail=errors[0], errors=errors, status_code=400)

    payload = {
        "LaKhachMoi": target_la_khach_moi,
        "MaKH": target_ma_kh,
        "HoTen": normalized_ho_ten,
        "SoDienThoai": (body.so_dien_thoai or "").strip(),
        "Email": (body.email or "").strip(),
        "DiaChi": (body.dia_chi or "").strip(),
        "MaLichTrinh": schedule["MaLichTrinh"],
        "SoKhach": int(body.so_khach),
        "MaNhaNghi": ma_nha_nghi,
        "SoPhong": so_phong,
        "DiaChiDon": (body.dia_chi_don or "").strip() if body.co_xe_don else None,
        "GioDon": dt_don if body.co_xe_don else None,
        "GioVeNoiNghi": dt_ve if body.co_xe_ve else None,
        "NgayDat": now,
    }

    try:
        ma_don_hang = services.luu_dat_tour(payload)
    except (mysql.connector.Error, db.KhongCoDongNao, ValueError) as exc:
        raise mysql_error_to_http(exc) from exc

    created = queries.get_order_basic_for_booking_response(ma_don_hang)
    if created is None:
        raise HTTPException(
            status_code=500,
            detail="Không thể đọc lại thông tin đơn hàng vừa tạo.",
        )

    ma_kh_saved = created["MaKH"]
    customer = queries.get_customer_by_id(ma_kh_saved)
    if customer is None:
        raise HTTPException(
            status_code=500,
            detail="Không thể đọc lại thông tin khách hàng vừa tạo.",
        )

    token = sign_customer_token(ma_kh_saved)
    return BookingCreateResponse(
        ma_don_hang=ma_don_hang,
        ma_kh=ma_kh_saved,
        tong_tien=to_int(created["TongTien"]),
        customer=CustomerItem(**customer),
        customer_token=token,
    )


@router.get("/customers/{ma_kh}/orders", response_model=list[CustomerOrderItem])
def get_customer_orders(
    ma_kh: str,
    auth: dict[str, dict[str, Any] | None] = Depends(get_optional_auth),
) -> list[CustomerOrderItem]:
    ensure_customer_or_admin(auth, ma_kh)
    rows = queries.get_customer_orders(ma_kh)
    return [CustomerOrderItem(**r) for r in rows]


@router.get("/customers/{ma_kh}/pending-reviews", response_model=list[PendingReviewItem])
def get_pending_reviews(
    ma_kh: str,
    auth: dict[str, dict[str, Any] | None] = Depends(get_optional_auth),
) -> list[PendingReviewItem]:
    ensure_customer_or_admin(auth, ma_kh)
    rows = services.lay_don_cho_danh_gia(ma_kh)
    return [
        PendingReviewItem(
            ma_don_hang=r["MaDonHang"],
            ma_tour=r["MaTour"],
            ten_tour=r["TenTour"],
            ngay_xuat_phat=to_iso(r["NgayXuatPhat"]),
            ngay_ket_thuc=to_iso(r["NgayKetThuc"]),
            ma_nha_nghi=r.get("MaNhaNghi"),
            ten_nha_nghi=r.get("TenNhaNghi"),
            ngay_dat=to_iso(r["NgayDat"]),
            tong_tien=to_int(r["TongTien"]),
        )
        for r in rows
    ]


@router.get("/reviews/pending-orders", response_model=list[PendingReviewItem])
def get_all_pending_reviews(
    ma_kh: str | None = Query(default=None),
) -> list[PendingReviewItem]:
    """Lấy danh sách các đơn hàng hoàn thành chưa đánh giá trên toàn hệ thống hoặc theo khách hàng."""
    if ma_kh and ma_kh.strip():
        rows = services.lay_don_cho_danh_gia(ma_kh.strip())
    else:
        sql = """
            SELECT dh.MaDonHang, t.MaTour, t.TenTour,
                   lt.NgayXuatPhat, lt.NgayKetThuc,
                   dh.MaNhaNghi, nn.TenNhaNghi,
                   dh.NgayDat, v.TongTien
            FROM DonHang dh
            JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
            JOIN Tour t              ON t.MaTour = lt.MaTour
            LEFT JOIN NhaNghi nn     ON nn.MaNhaNghi = dh.MaNhaNghi
            JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
            WHERE dh.MaTrangThai = 'HOANTHANH'
              AND dh.NgayDanhGia IS NULL
            ORDER BY lt.NgayKetThuc DESC
        """
        rows = db.doc(sql)
    return [
        PendingReviewItem(
            ma_don_hang=r["MaDonHang"],
            ma_tour=r["MaTour"],
            ten_tour=r["TenTour"],
            ngay_xuat_phat=to_iso(r["NgayXuatPhat"]),
            ngay_ket_thuc=to_iso(r["NgayKetThuc"]),
            ma_nha_nghi=r.get("MaNhaNghi"),
            ten_nha_nghi=r.get("TenNhaNghi"),
            ngay_dat=to_iso(r["NgayDat"]),
            tong_tien=to_int(r["TongTien"]),
        )
        for r in rows
    ]


@router.post("/reviews", response_model=ReviewCreateResponse)
def submit_review(
    body: ReviewCreateRequest,
    auth: dict[str, dict[str, Any] | None] = Depends(get_optional_auth),
) -> ReviewCreateResponse:
    if auth["admin"] is None and auth["customer"] is None:
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập để gửi đánh giá chuyến đi.",
        )

    order = queries.get_order_for_review(body.ma_don_hang.strip())
    if order is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    if auth["admin"] is None and auth["customer"] is not None:
        if order["MaKH"] != auth["customer"]["ma_kh"]:
            raise HTTPException(
                status_code=403,
                detail="Bạn chỉ có thể đánh giá các đơn hàng thuộc tài khoản của mình.",
            )

    if order["MaTrangThai"] != "HOANTHANH":
        raise AppValidationError("Chỉ đơn hàng đã hoàn thành chuyến đi mới có thể đánh giá.")

    if order["NgayDanhGia"] is not None:
        raise HTTPException(
            status_code=409,
            detail="Đơn hàng này đã được đánh giá trước đó.",
        )

    co_nha_nghi = order["MaNhaNghi"] is not None
    extra_errors: list[str] = []

    if body.co_danh_gia_nha_nghi and not co_nha_nghi:
        extra_errors.append("Chỉ được đánh giá nơi nghỉ khi đơn hàng có đặt nơi nghỉ.")
    elif body.co_danh_gia_nha_nghi and co_nha_nghi and body.diem_nha_nghi is None:
        extra_errors.append("Vui lòng chọn số sao đánh giá cho nơi nghỉ.")

    diem_nn_input = body.diem_nha_nghi if (body.co_danh_gia_nha_nghi or body.diem_nha_nghi is not None) else None
    nx_nn_input = body.nhan_xet_nha_nghi

    errors, nx_tour, diem_nn, nx_nn = services.kiem_tra_danh_gia(
        diem_tour=body.diem_tour,
        nhan_xet_tour=body.nhan_xet_tour,
        co_nha_nghi=co_nha_nghi,
        diem_nn=diem_nn_input,
        nhan_xet_nn=nx_nn_input,
    )
    all_errors = extra_errors + [msg for msg in errors if msg not in extra_errors]
    if all_errors:
        raise AppValidationError(detail=all_errors[0], errors=all_errors, status_code=400)

    ngay_dg = db.hien_tai()
    try:
        services.luu_danh_gia(
            ma_don=order["MaDonHang"],
            diem_tour=body.diem_tour,
            nhan_xet_tour=nx_tour,
            diem_nn=diem_nn,
            nhan_xet_nn=nx_nn,
            ngay_danh_gia=ngay_dg,
        )
    except (mysql.connector.Error, db.KhongCoDongNao, ValueError) as exc:
        raise mysql_error_to_http(exc) from exc

    return ReviewCreateResponse(
        message="Cảm ơn bạn đã gửi đánh giá chuyến đi.",
        ma_don_hang=order["MaDonHang"],
        ngay_danh_gia=to_iso(ngay_dg),
    )


@router.get("/orders/{ma_don}/confirmation/pdf")
def download_order_confirmation_pdf(
    ma_don: str,
    nguoi_lap: str | None = Query(default=None),
    auth: dict[str, dict[str, Any] | None] = Depends(get_optional_auth),
) -> Response:
    if auth["admin"] is None and auth["customer"] is None:
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập để tải phiếu xác nhận đặt tour.",
        )

    ct = services.lay_chi_tiet_don_r1(ma_don)
    if ct is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")

    if auth["admin"] is None and auth["customer"]["ma_kh"] != ct["MaKH"]:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền tải phiếu xác nhận của đơn hàng khác.",
        )

    default_issuer = (
        auth["admin"]["staff_name"]
        if auth["admin"] is not None
        else "Bộ phận Điều hành Bắc Việt Travel"
    )
    issuer = (nguoi_lap or "").strip() or default_issuer

    html = pdf_service.build_confirmation_html(ma_don, issuer)
    pdf_bytes = pdf_service.render_html_to_pdf(html)
    filename = f"PhieuXacNhan_{ma_don}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
