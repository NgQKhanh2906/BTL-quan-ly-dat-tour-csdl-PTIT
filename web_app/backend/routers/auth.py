"""Các endpoint danh sách khách hàng demo, kiểm tra trùng khách và đăng nhập phiên Khách/Quản trị."""

from __future__ import annotations

import hmac

from fastapi import APIRouter, HTTPException

try:
    from .. import queries
    from ..dependencies import (
        AppValidationError,
        get_admin_credentials,
        services,
        sign_admin_token,
        sign_customer_token,
    )
    from ..schemas import (
        AdminLoginRequest,
        AdminLoginResponse,
        CheckDuplicateRequest,
        CheckDuplicateResponse,
        CustomerItem,
        CustomerLoginRequest,
        CustomerLoginResponse,
    )
except ImportError:
    import queries
    from dependencies import (
        AppValidationError,
        get_admin_credentials,
        services,
        sign_admin_token,
        sign_customer_token,
    )
    from schemas import (
        AdminLoginRequest,
        AdminLoginResponse,
        CheckDuplicateRequest,
        CheckDuplicateResponse,
        CustomerItem,
        CustomerLoginRequest,
        CustomerLoginResponse,
    )

router = APIRouter(prefix="/api", tags=["auth"])


def _fetch_customers_list() -> list[CustomerItem]:
    rows = services.lay_ds_khach_hang_f1()
    return [
        CustomerItem(
            ma_kh=r["MaKH"],
            ho_ten=r["HoTen"],
            email=r["Email"],
            dia_chi=r.get("DiaChi") or "",
            so_dien_thoai=r.get("SoDienThoai") or "",
        )
        for r in rows
    ]


@router.get("/customers", response_model=list[CustomerItem])
def list_customers() -> list[CustomerItem]:
    return _fetch_customers_list()


@router.get("/auth/customers", response_model=list[CustomerItem], include_in_schema=False)
def list_customers_alias() -> list[CustomerItem]:
    return _fetch_customers_list()


@router.post("/customers/check-duplicate", response_model=CheckDuplicateResponse)
def check_duplicate_customer(body: CheckDuplicateRequest) -> CheckDuplicateResponse:
    # 1. Kiểm tra khớp chính xác cả 3 thuộc tính (Họ tên, SĐT, Email)
    exact_match = queries.find_customer_by_name_phone_email(body.ho_ten, body.so_dien_thoai, body.email)
    if exact_match is not None:
        customer = CustomerItem(
            ma_kh=exact_match["ma_kh"],
            ho_ten=exact_match["ho_ten"],
            email=exact_match["email"],
            dia_chi=exact_match.get("dia_chi") or "",
            so_dien_thoai=exact_match.get("so_dien_thoai") or "",
        )
        return CheckDuplicateResponse(duplicate=True, customer=customer, matched_exact=True, conflict=False)

    # 2. Không khớp cả 3: kiểm tra xem Email hoặc SĐT có bị trùng không
    matched = services.kiem_tra_trung_khach_hang(body.email, body.so_dien_thoai)
    if matched is None:
        return CheckDuplicateResponse(duplicate=False, customer=None, matched_exact=False, conflict=False)

    customer = CustomerItem(
        ma_kh=matched["MaKH"],
        ho_ten=matched["HoTen"],
        email=matched["Email"],
        dia_chi=matched.get("DiaChi") or "",
        so_dien_thoai=matched.get("CacSDT") or "",
    )
    is_conflict = bool(body.ho_ten.strip())
    return CheckDuplicateResponse(duplicate=True, customer=customer, matched_exact=False, conflict=is_conflict)


@router.post("/auth/customer-login", response_model=CustomerLoginResponse)
def customer_login(body: CustomerLoginRequest) -> CustomerLoginResponse:
    identifier = (body.identifier or "").strip()
    if not identifier:
        raise AppValidationError("Vui lòng nhập email hoặc số điện thoại để đăng nhập.")

    customer = queries.find_customer_by_identifier(identifier)
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản khách hàng khớp với email hoặc số điện thoại đã nhập.",
        )

    token = sign_customer_token(customer["ma_kh"])
    return CustomerLoginResponse(token=token, customer=CustomerItem(**customer))


@router.post("/auth/admin-login", response_model=AdminLoginResponse)
def admin_login(body: AdminLoginRequest) -> AdminLoginResponse:
    expected_user, expected_pass, default_staff = get_admin_credentials()
    username = (body.username or "").strip()
    password = body.password or ""

    valid_user = hmac.compare_digest(username, expected_user)
    valid_pass = hmac.compare_digest(password, expected_pass)
    if not (valid_user and valid_pass):
        raise HTTPException(
            status_code=401,
            detail="Tên đăng nhập hoặc mật khẩu quản trị không chính xác.",
        )

    staff_name = (body.staff_name or "").strip() or default_staff
    token = sign_admin_token(username=username, staff_name=staff_name)
    return AdminLoginResponse(token=token, username=username, staff_name=staff_name)
