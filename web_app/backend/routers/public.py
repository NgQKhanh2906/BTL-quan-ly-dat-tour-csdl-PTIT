"""Các endpoint công khai: metadata, trang chủ, tỉnh thành, tra cứu lịch trình, nơi nghỉ."""

from __future__ import annotations

from fastapi import APIRouter, Query

try:
    from .. import queries
    from ..dependencies import (
        AppValidationError,
        db,
        parse_date_input,
        services,
        to_iso,
    )
    from ..schemas import (
        AccommodationItem,
        LandingResponse,
        MetaResponse,
        OpenScheduleItem,
        ProvinceItem,
        ScheduleSearchItem,
    )
except ImportError:
    import queries
    from dependencies import (
        AppValidationError,
        db,
        parse_date_input,
        services,
        to_iso,
    )
    from schemas import (
        AccommodationItem,
        LandingResponse,
        MetaResponse,
        OpenScheduleItem,
        ProvinceItem,
        ScheduleSearchItem,
    )

router = APIRouter(prefix="/api", tags=["public"])


def _parse_optional_int(raw: str | None, field_label: str) -> int | None:
    if raw is None or not str(raw).strip():
        return None
    try:
        return int(str(raw).strip())
    except ValueError as exc:
        raise AppValidationError(f"Giá trị {field_label} không hợp lệ.") from exc


def _parse_optional_float(raw: str | None, field_label: str) -> float | None:
    if raw is None or not str(raw).strip():
        return None
    try:
        return float(str(raw).strip())
    except ValueError as exc:
        raise AppValidationError(f"Giá trị {field_label} không hợp lệ.") from exc


@router.get("/meta", response_model=MetaResponse)
def get_meta() -> MetaResponse:
    now = db.hien_tai()
    return MetaResponse(
        current_datetime=to_iso(now),
        current_date=now.strftime("%Y-%m-%d"),
        brand_name="Bắc Việt Travel",
    )


@router.get("/landing", response_model=LandingResponse)
def get_landing() -> LandingResponse:
    now = db.hien_tai()
    stats = queries.get_landing_stats(now)
    raw_schedules = services.tim_kiem_lich_trinh(tu_ngay=now.date(), so_khach=1)
    featured = queries.enrich_search_schedules(raw_schedules)
    return LandingResponse(stats=stats, featured_schedules=featured)


@router.get("/provinces", response_model=list[ProvinceItem])
def get_provinces() -> list[ProvinceItem]:
    rows = services.lay_ds_tinh_thanh()
    return [
        ProvinceItem(ma_tinh=r["MaTinh"], ten_tinh=r["TenTinh"])
        for r in rows
    ]


@router.get("/schedules/search", response_model=list[ScheduleSearchItem])
def search_schedules(
    tu_khoa: str | None = Query(default=None),
    ma_tinh_den: str | None = Query(default=None),
    gia_tu: str | None = Query(default=None),
    gia_den: str | None = Query(default=None),
    tu_ngay: str | None = Query(default=None),
    den_ngay: str | None = Query(default=None),
    so_khach: str | None = Query(default="1"),
    diem_toi_thieu: str | None = Query(default=None),
) -> list[ScheduleSearchItem]:
    gia_tu_val = _parse_optional_int(gia_tu, "giá từ")
    gia_den_val = _parse_optional_int(gia_den, "giá đến")
    so_khach_val = _parse_optional_int(so_khach, "số khách")
    so_khach_val = 1 if so_khach_val is None else so_khach_val
    diem_val = _parse_optional_float(diem_toi_thieu, "điểm đánh giá tối thiểu")

    try:
        tu_ngay_val = parse_date_input(tu_ngay)
        den_ngay_val = parse_date_input(den_ngay)
    except ValueError as exc:
        raise AppValidationError("Định dạng ngày lọc không hợp lệ (YYYY-MM-DD).") from exc

    errors: list[str] = []
    if so_khach_val < 1:
        errors.append("Số lượng khách phải lớn hơn hoặc bằng 1.")
    if gia_tu_val is not None and gia_tu_val < 0:
        errors.append("Giá từ không được âm.")
    if gia_den_val is not None and gia_den_val < 0:
        errors.append("Giá đến không được âm.")
    if (
        gia_tu_val is not None
        and gia_den_val is not None
        and gia_tu_val > 0
        and gia_den_val > 0
        and gia_den_val < gia_tu_val
    ):
        errors.append("Giá đến phải lớn hơn hoặc bằng giá từ.")

    effective_tu_ngay = tu_ngay_val or db.hien_tai().date()
    if den_ngay_val is not None and den_ngay_val < effective_tu_ngay:
        errors.append("Ngày kết thúc tìm kiếm phải lớn hơn hoặc bằng ngày bắt đầu.")

    if diem_val is not None and not (0.0 <= diem_val <= 5.0):
        errors.append("Điểm đánh giá tối thiểu phải nằm trong khoảng từ 0 đến 5.")

    if errors:
        raise AppValidationError(detail=errors[0], errors=errors)

    raw_rows = services.tim_kiem_lich_trinh(
        tu_khoa=tu_khoa,
        ma_tinh_den=ma_tinh_den,
        gia_tu=gia_tu_val,
        gia_den=gia_den_val,
        tu_ngay=effective_tu_ngay,
        den_ngay=den_ngay_val,
        so_khach=so_khach_val,
        diem_toi_thieu=diem_val,
    )
    enriched = queries.enrich_search_schedules(raw_rows)
    return [ScheduleSearchItem(**row) for row in enriched]


@router.get("/schedules/open", response_model=list[OpenScheduleItem])
def get_open_schedules() -> list[OpenScheduleItem]:
    raw_rows = services.lay_lich_trinh_con_cho(db.hien_tai())
    enriched = queries.enrich_open_schedules(raw_rows)
    return [OpenScheduleItem(**row) for row in enriched]


@router.get("/accommodations", response_model=list[AccommodationItem])
def get_accommodations(
    ma_tinh_den: str = Query(..., min_length=1, description="Mã tỉnh điểm đến"),
) -> list[AccommodationItem]:
    raw_rows = services.lay_noi_nghi_theo_tinh(ma_tinh_den.strip())
    enriched = queries.enrich_accommodations(raw_rows)
    return [AccommodationItem(**row) for row in enriched]
