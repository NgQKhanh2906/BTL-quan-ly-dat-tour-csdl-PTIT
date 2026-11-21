"""Các hàm truy vấn chỉ-đọc bổ sung hỗ trợ REST API mà không sửa tour_app/."""

from __future__ import annotations

import unicodedata
from datetime import datetime

try:
    from .dependencies import db, to_int, to_iso, to_opt_float, to_opt_int
except ImportError:
    from dependencies import db, to_int, to_iso, to_opt_float, to_opt_int


def get_landing_stats(thoi_diem: datetime) -> dict:
    """Đọc các chỉ số thực tế trực tiếp từ MySQL cho trang chủ."""
    sql = """
        SELECT
            (SELECT COUNT(*) FROM TinhThanh) AS total_provinces,
            (SELECT COUNT(*) FROM Tour) AS total_tours,
            (
                SELECT COUNT(*)
                FROM LichTrinh
                WHERE NgayXuatPhat > %(HienTai)s
                  AND SoChoToiDa - SoChoDaDat > 0
            ) AS open_schedules,
            (
                SELECT COALESCE(SUM(SoLuongKhach), 0)
                FROM DonHang
                WHERE MaTrangThai <> 'HUY'
            ) AS total_travelers_served,
            (
                SELECT ROUND(AVG(DiemTour), 1)
                FROM DonHang
                WHERE DiemTour IS NOT NULL
            ) AS avg_rating,
            (
                SELECT COUNT(DiemTour)
                FROM DonHang
                WHERE DiemTour IS NOT NULL
            ) AS total_reviews
    """
    row = db.doc(sql, {"HienTai": thoi_diem.strftime("%Y-%m-%d %H:%M:%S")})[0]
    return {
        "total_provinces": to_int(row.get("total_provinces")),
        "total_tours": to_int(row.get("total_tours")),
        "open_schedules": to_int(row.get("open_schedules")),
        "total_travelers_served": to_int(row.get("total_travelers_served")),
        "avg_rating": to_opt_float(row.get("avg_rating")),
        "total_reviews": to_int(row.get("total_reviews")),
    }


def enrich_search_schedules(rows: list[dict]) -> list[dict]:
    """Bổ sung MaTour và MoTa cho kết quả trả về từ services.tim_kiem_lich_trinh."""
    if not rows:
        return []

    ma_lts = [r["MaLichTrinh"] for r in rows]
    placeholders = ", ".join(["%s"] * len(ma_lts))
    meta_rows = db.doc(
        f"""
        SELECT lt.MaLichTrinh, t.MaTour, COALESCE(t.MoTa, '') AS MoTa
        FROM LichTrinh lt
        JOIN Tour t ON t.MaTour = lt.MaTour
        WHERE lt.MaLichTrinh IN ({placeholders})
        """,
        tuple(ma_lts),
    )
    meta_map = {r["MaLichTrinh"]: r for r in meta_rows}

    result: list[dict] = []
    for r in rows:
        extra = meta_map.get(r["MaLichTrinh"], {})
        result.append(
            {
                "ma_lich_trinh": r["MaLichTrinh"],
                "ma_tour": extra.get("MaTour", ""),
                "ten_tour": r["TenTour"],
                "mo_ta": extra.get("MoTa", "") or "",
                "noi_di": r["NoiDi"],
                "noi_den": r["NoiDen"],
                "ngay_xuat_phat": to_iso(r["NgayXuatPhat"]),
                "so_ngay": to_int(r["SoNgay"]),
                "gia_co_ban": to_int(r["GiaCoBan"]),
                "so_cho_con_lai": to_int(r["SoChoConLai"]),
                "diem_tb": to_opt_float(r.get("DiemTB")),
                "so_luot_danh_gia": to_int(r.get("SoLuotDanhGia")),
            }
        )
    return result


def enrich_open_schedules(rows: list[dict]) -> list[dict]:
    """Bổ sung DiemTapTrung, NoiDi, MoTa cho kết quả services.lay_lich_trinh_con_cho."""
    if not rows:
        return []

    ma_lts = [r["MaLichTrinh"] for r in rows]
    placeholders = ", ".join(["%s"] * len(ma_lts))
    meta_rows = db.doc(
        f"""
        SELECT lt.MaLichTrinh,
               lt.DiemTapTrung,
               txp.TenTinh AS NoiDi,
               COALESCE(t.MoTa, '') AS MoTa
        FROM LichTrinh lt
        JOIN Tour t ON t.MaTour = lt.MaTour
        JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
        WHERE lt.MaLichTrinh IN ({placeholders})
        """,
        tuple(ma_lts),
    )
    meta_map = {r["MaLichTrinh"]: r for r in meta_rows}

    result: list[dict] = []
    for r in rows:
        extra = meta_map.get(r["MaLichTrinh"], {})
        result.append(
            {
                "ma_lich_trinh": r["MaLichTrinh"],
                "ma_tour": r["MaTour"],
                "ten_tour": r["TenTour"],
                "mo_ta": extra.get("MoTa", "") or "",
                "noi_di": extra.get("NoiDi", "") or "",
                "ma_tinh_den": r["MaTinhDen"],
                "ten_tinh_den": r["TenTinhDen"],
                "diem_tap_trung": extra.get("DiemTapTrung", "") or "",
                "ngay_xuat_phat": to_iso(r["NgayXuatPhat"]),
                "ngay_ket_thuc": to_iso(r["NgayKetThuc"]),
                "so_dem": to_int(r["SoDem"]),
                "gia_co_ban": to_int(r["GiaCoBan"]),
                "so_cho_con_lai": to_int(r["SoChoConLai"]),
            }
        )
    return result


def enrich_accommodations(rows: list[dict]) -> list[dict]:
    """Bổ sung DiaChi cho danh sách nơi nghỉ từ services.lay_noi_nghi_theo_tinh."""
    if not rows:
        return []

    ma_nns = [r["MaNhaNghi"] for r in rows]
    placeholders = ", ".join(["%s"] * len(ma_nns))
    meta_rows = db.doc(
        f"SELECT MaNhaNghi, DiaChi FROM NhaNghi WHERE MaNhaNghi IN ({placeholders})",
        tuple(ma_nns),
    )
    meta_map = {r["MaNhaNghi"]: r["DiaChi"] for r in meta_rows}

    return [
        {
            "ma_nha_nghi": r["MaNhaNghi"],
            "ten_nha_nghi": r["TenNhaNghi"],
            "loai_hinh": r["LoaiHinh"],
            "dia_chi": meta_map.get(r["MaNhaNghi"], "") or "",
            "gia_phong_moi_dem": to_int(r["GiaPhongMoiDem"]),
        }
        for r in rows
    ]


def get_schedule_for_booking(ma_lich_trinh: str) -> dict | None:
    """Lấy thông tin một lịch trình bất kỳ phục vụ kiểm tra hợp lệ khi đặt tour."""
    rows = db.doc(
        """
        SELECT lt.MaLichTrinh,
               t.MaTour,
               t.TenTour,
               t.MaTinhDen,
               lt.NgayXuatPhat,
               lt.NgayKetThuc,
               DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS SoDem,
               lt.GiaCoBan,
               lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai
        FROM LichTrinh lt
        JOIN Tour t ON t.MaTour = lt.MaTour
        WHERE lt.MaLichTrinh = %(MaLichTrinh)s
        """,
        {"MaLichTrinh": ma_lich_trinh},
    )
    return rows[0] if rows else None


def get_accommodation_by_id(ma_nha_nghi: str) -> dict | None:
    rows = db.doc(
        "SELECT MaNhaNghi, TenNhaNghi, MaTinh, GiaPhongMoiDem FROM NhaNghi WHERE MaNhaNghi = %(MaNhaNghi)s",
        {"MaNhaNghi": ma_nha_nghi},
    )
    return rows[0] if rows else None


def get_customer_by_id(ma_kh: str) -> dict | None:
    rows = db.doc(
        """
        SELECT kh.MaKH,
               kh.HoTen,
               kh.Email,
               COALESCE(kh.DiaChi, '') AS DiaChi,
               COALESCE(
                   GROUP_CONCAT(DISTINCT sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', '),
                   ''
               ) AS SoDienThoai
        FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE kh.MaKH = %(MaKH)s
        GROUP BY kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi
        """,
        {"MaKH": ma_kh},
    )
    if not rows:
        return None
    r = rows[0]
    return {
        "ma_kh": r["MaKH"],
        "ho_ten": r["HoTen"],
        "email": r["Email"],
        "dia_chi": r["DiaChi"] or "",
        "so_dien_thoai": r["SoDienThoai"] or "",
    }


def find_customer_by_identifier(identifier: str) -> dict | None:
    """Tra cứu khách hàng theo Email (không phân biệt hoa thường) hoặc Số điện thoại."""
    clean = (identifier or "").strip()
    if not clean:
        return None
    rows = db.doc(
        """
        SELECT kh.MaKH,
               kh.HoTen,
               kh.Email,
               COALESCE(kh.DiaChi, '') AS DiaChi,
               COALESCE(
                   GROUP_CONCAT(DISTINCT sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', '),
                   ''
               ) AS SoDienThoai
        FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE LOWER(kh.Email) = LOWER(%(Identifier)s)
           OR EXISTS (
               SELECT 1
               FROM SDT_KhachHang sdt2
               WHERE sdt2.MaKH = kh.MaKH
                 AND sdt2.SoDienThoai = %(Identifier)s
           )
        GROUP BY kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi
        ORDER BY kh.MaKH
        LIMIT 1
        """,
        {"Identifier": clean},
    )
    if not rows:
        return None
    r = rows[0]
    return {
        "ma_kh": r["MaKH"],
        "ho_ten": r["HoTen"],
        "email": r["Email"],
        "dia_chi": r["DiaChi"] or "",
        "so_dien_thoai": r["SoDienThoai"] or "",
    }


def find_customer_by_name_phone_email(ho_ten: str | None, so_dien_thoai: str | None, email: str | None) -> dict | None:
    """Tìm khách hàng khớp cả 3 thông tin: Họ tên, Số điện thoại và Email."""
    ten_sach = (ho_ten or "").strip()
    sdt_sach = (so_dien_thoai or "").strip()
    email_sach = (email or "").strip()
    if not (ten_sach and sdt_sach and email_sach):
        return None
    rows = db.doc(
        """
        SELECT kh.MaKH,
               kh.HoTen,
               kh.Email,
               COALESCE(kh.DiaChi, '') AS DiaChi,
               sdt.SoDienThoai
        FROM KhachHang kh
        JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE LOWER(TRIM(kh.HoTen)) = LOWER(%(HoTen)s)
          AND sdt.SoDienThoai = %(SoDienThoai)s
          AND LOWER(TRIM(kh.Email)) = LOWER(%(Email)s)
        LIMIT 1
        """,
        {"HoTen": ten_sach, "SoDienThoai": sdt_sach, "Email": email_sach},
    )
    if not rows:
        return None
    r = rows[0]
    return {
        "ma_kh": r["MaKH"],
        "ho_ten": r["HoTen"],
        "email": r["Email"],
        "dia_chi": r["DiaChi"] or "",
        "so_dien_thoai": r["SoDienThoai"] or "",
    }


def _collapse_whitespace(raw: str | None) -> str:
    return " ".join(unicodedata.normalize("NFC", raw or "").strip().split())


def _normalize_text_for_match(raw: str | None) -> str:
    return _collapse_whitespace(raw).casefold()


def _mask_name(name: str) -> str:
    cleaned = _collapse_whitespace(name)
    if not cleaned:
        return "***"
    parts = cleaned.split(" ")
    if len(parts) == 1:
        return f"{parts[0][0]}***"
    if len(parts) == 2:
        return f"{parts[0]} ***"
    return f"{parts[0]} *** {parts[-1]}"


def _mask_email(email: str) -> str:
    clean = (email or "").strip()
    if "@" not in clean:
        return "***"
    local, domain = clean.split("@", 1)
    if len(local) <= 1:
        prefix = "*"
    elif len(local) <= 2:
        prefix = local[0]
    else:
        prefix = local[:2]
    return f"{prefix}***@{domain}"


def _mask_phone(phone: str) -> str:
    clean = (phone or "").strip()
    if len(clean) < 6:
        return "***"
    return f"{clean[:3]}****{clean[-3:]}"


def _mask_address(address: str) -> str:
    cleaned = _collapse_whitespace(address)
    if not cleaned:
        return ""
    segments = [seg.strip() for seg in cleaned.split(",") if seg.strip()]
    if len(segments) >= 2:
        return f"***, {segments[-1]}"
    return "***"


def find_existing_customer_suggestion(
    ho_ten: str = "",
    so_dien_thoai: str = "",
    email: str = "",
    dia_chi: str = "",
) -> dict | None:
    """Tìm khách hàng cũ khi khớp >= 2 trường thông tin và che các trường chưa nhập."""
    ten_clean = _collapse_whitespace(ho_ten)
    ten_norm = ten_clean.casefold()
    sdt_clean = (so_dien_thoai or "").strip()
    email_clean = (email or "").strip()
    email_norm = email_clean.lower()
    dia_chi_clean = _collapse_whitespace(dia_chi)
    dia_chi_norm = dia_chi_clean.casefold()

    filled_count = sum(bool(v) for v in (ten_norm, sdt_clean, email_norm, dia_chi_norm))
    if filled_count < 2:
        return None

    rows = db.doc(
        """
        SELECT kh.MaKH,
               kh.HoTen,
               kh.Email,
               COALESCE(kh.DiaChi, '') AS DiaChi,
               COALESCE(
                   GROUP_CONCAT(DISTINCT sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ','),
                   ''
               ) AS CacSDT
        FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE (%(Email)s <> '' AND LOWER(TRIM(kh.Email)) = LOWER(%(Email)s))
           OR (%(HoTen)s <> '' AND LOWER(TRIM(kh.HoTen)) = LOWER(%(HoTen)s))
           OR (%(DiaChi)s <> '' AND LOWER(TRIM(kh.DiaChi)) = LOWER(%(DiaChi)s))
           OR (
               %(SoDienThoai)s <> ''
               AND EXISTS (
                   SELECT 1
                   FROM SDT_KhachHang sdt2
                   WHERE sdt2.MaKH = kh.MaKH
                     AND sdt2.SoDienThoai = %(SoDienThoai)s
               )
           )
        GROUP BY kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi
        ORDER BY kh.MaKH
        """,
        {
            "HoTen": ten_clean,
            "SoDienThoai": sdt_clean,
            "Email": email_clean,
            "DiaChi": dia_chi_clean,
        },
    )

    candidates: list[tuple[int, int, dict, list[str], list[str], str | None]] = []
    for r in rows:
        phones = [p.strip() for p in (r.get("CacSDT") or "").split(",") if p.strip()]
        matched_fields: list[str] = []
        matched_phone: str | None = None

        if ten_norm and _normalize_text_for_match(r.get("HoTen")) == ten_norm:
            matched_fields.append("ho_ten")
        if sdt_clean and sdt_clean in phones:
            matched_fields.append("so_dien_thoai")
            matched_phone = sdt_clean
        if email_norm and (r.get("Email") or "").strip().lower() == email_norm:
            matched_fields.append("email")
        if dia_chi_norm and _normalize_text_for_match(r.get("DiaChi")) == dia_chi_norm:
            matched_fields.append("dia_chi")

        if len(matched_fields) >= 2:
            unique_hits = sum(1 for f in matched_fields if f in ("email", "so_dien_thoai"))
            candidates.append((len(matched_fields), unique_hits, r, matched_fields, phones, matched_phone))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    best_count, best_unique, best_row, best_fields, phones, best_phone = candidates[0]
    if len(candidates) > 1 and (candidates[1][0], candidates[1][1]) == (best_count, best_unique):
        return None

    primary_phone = phones[0] if phones else ""
    return {
        "ma_kh": best_row["MaKH"],
        "ho_ten_hien_thi": best_row["HoTen"] if "ho_ten" in best_fields else _mask_name(best_row["HoTen"]),
        "email_hien_thi": best_row["Email"] if "email" in best_fields else _mask_email(best_row["Email"]),
        "so_dien_thoai_hien_thi": (
            best_phone if ("so_dien_thoai" in best_fields and best_phone) else _mask_phone(primary_phone)
        ),
        "dia_chi_hien_thi": best_row["DiaChi"] if "dia_chi" in best_fields else _mask_address(best_row["DiaChi"]),
        "matched_fields": best_fields,
        "matched_count": best_count,
    }


def get_order_basic_for_booking_response(ma_don_hang: str) -> dict | None:
    rows = db.doc(
        "SELECT MaDonHang, MaKH, TongTien FROM v_DonHang_ChiTiet WHERE MaDonHang = %(MaDonHang)s",
        {"MaDonHang": ma_don_hang},
    )
    return rows[0] if rows else None


def get_order_for_review(ma_don_hang: str) -> dict | None:
    rows = db.doc(
        """
        SELECT MaDonHang, MaKH, MaTrangThai, MaNhaNghi, NgayDanhGia
        FROM DonHang
        WHERE MaDonHang = %(MaDonHang)s
        """,
        {"MaDonHang": ma_don_hang},
    )
    return rows[0] if rows else None


def get_customer_orders(ma_kh: str) -> list[dict]:
    """Lấy danh sách đầy đủ đơn hàng của một khách hàng kèm cờ co_the_danh_gia."""
    rows = db.doc(
        """
        SELECT v.MaDonHang,
               v.MaTour,
               v.TenTour,
               v.TinhDen,
               v.MaLichTrinh,
               v.NgayDat,
               v.NgayXuatPhat,
               v.NgayKetThuc,
               v.SoLuongKhach,
               d.MaNhaNghi,
               v.TenNhaNghi,
               v.SoPhong,
               v.TienTour,
               v.TienPhong,
               v.TongTien,
               v.MaTrangThai,
               v.TenTrangThai,
               v.NgayHuy,
               v.LyDoHuy,
               v.TyLePhat,
               v.TienPhat,
               v.TienHoan,
               v.DiemTour,
               v.NhanXetTour,
               v.DiemNhaNghi,
               v.NhanXetNhaNghi,
               v.NgayDanhGia
        FROM v_DonHang_ChiTiet v
        JOIN DonHang d ON d.MaDonHang = v.MaDonHang
        WHERE v.MaKH = %(MaKH)s
        ORDER BY v.NgayDat DESC, v.MaDonHang DESC
        """,
        {"MaKH": ma_kh},
    )
    return [
        {
            "ma_don_hang": r["MaDonHang"],
            "ma_tour": r["MaTour"],
            "ten_tour": r["TenTour"],
            "tinh_den": r["TinhDen"],
            "ma_lich_trinh": r["MaLichTrinh"],
            "ngay_dat": to_iso(r["NgayDat"]),
            "ngay_xuat_phat": to_iso(r["NgayXuatPhat"]),
            "ngay_ket_thuc": to_iso(r["NgayKetThuc"]),
            "so_luong_khach": to_int(r["SoLuongKhach"]),
            "ma_nha_nghi": r["MaNhaNghi"],
            "ten_nha_nghi": r["TenNhaNghi"],
            "so_phong": to_int(r["SoPhong"]),
            "tien_tour": to_int(r["TienTour"]),
            "tien_phong": to_int(r["TienPhong"]),
            "tong_tien": to_int(r["TongTien"]),
            "ma_trang_thai": r["MaTrangThai"],
            "ten_trang_thai": r["TenTrangThai"],
            "ngay_huy": to_iso(r["NgayHuy"]),
            "ly_do_huy": r["LyDoHuy"],
            "ty_le_phat": to_opt_int(r["TyLePhat"]),
            "tien_phat": to_opt_int(r["TienPhat"]),
            "tien_hoan": to_opt_int(r["TienHoan"]),
            "diem_tour": to_opt_int(r["DiemTour"]),
            "nhan_xet_tour": r["NhanXetTour"],
            "diem_nha_nghi": to_opt_int(r["DiemNhaNghi"]),
            "nhan_xet_nha_nghi": r["NhanXetNhaNghi"],
            "ngay_danh_gia": to_iso(r["NgayDanhGia"]),
            "co_the_danh_gia": bool(
                r["MaTrangThai"] == "HOANTHANH" and r["NgayDanhGia"] is None
            ),
        }
        for r in rows
    ]


def get_admin_orders(trang_thai: str | None = None, tu_khoa: str | None = None) -> dict:
    """Lấy danh sách toàn bộ đơn hàng cho Admin kèm số đếm theo từng trạng thái."""
    count_rows = db.doc(
        "SELECT MaTrangThai, COUNT(*) AS SoLuong FROM DonHang GROUP BY MaTrangThai"
    )
    counts = {"ALL": 0, "DAT": 0, "THANHTOAN": 0, "HOANTHANH": 0, "HUY": 0}
    for row in count_rows:
        code = row["MaTrangThai"]
        qty = to_int(row["SoLuong"])
        counts["ALL"] += qty
        if code in counts:
            counts[code] = qty

    tt_clean = (trang_thai or "").strip().upper()
    if tt_clean in ("", "ALL"):
        tt_param = None
    else:
        tt_param = tt_clean

    kw_clean = (tu_khoa or "").strip()
    kw_param = kw_clean if kw_clean else None

    rows = db.doc(
        """
        SELECT v.MaDonHang,
               v.MaKH,
               v.HoTen,
               v.MaTour,
               v.TenTour,
               v.TinhDen,
               v.MaLichTrinh,
               v.NgayDat,
               v.NgayXuatPhat,
               v.NgayKetThuc,
               v.SoLuongKhach,
               d.MaNhaNghi,
               v.TenNhaNghi,
               v.SoPhong,
               v.TienTour,
               v.TienPhong,
               v.TongTien,
               v.MaTrangThai,
               v.TenTrangThai,
               v.NgayHuy,
               v.TienPhat,
               v.TienHoan
        FROM v_DonHang_ChiTiet v
        JOIN DonHang d ON d.MaDonHang = v.MaDonHang
        WHERE (%(TrangThai)s IS NULL OR v.MaTrangThai = %(TrangThai)s)
          AND (
              %(TuKhoa)s IS NULL
              OR v.MaDonHang LIKE CONCAT('%', %(TuKhoa)s, '%')
              OR v.MaKH LIKE CONCAT('%', %(TuKhoa)s, '%')
              OR v.HoTen LIKE CONCAT('%', %(TuKhoa)s, '%')
              OR v.TenTour LIKE CONCAT('%', %(TuKhoa)s, '%')
              OR v.TinhDen LIKE CONCAT('%', %(TuKhoa)s, '%')
          )
        ORDER BY v.NgayDat DESC, v.MaDonHang DESC
        """,
        {"TrangThai": tt_param, "TuKhoa": kw_param},
    )

    orders = [
        {
            "ma_don_hang": r["MaDonHang"],
            "ma_kh": r["MaKH"],
            "ho_ten": r["HoTen"],
            "ma_tour": r["MaTour"],
            "ten_tour": r["TenTour"],
            "tinh_den": r["TinhDen"],
            "ma_lich_trinh": r["MaLichTrinh"],
            "ngay_dat": to_iso(r["NgayDat"]),
            "ngay_xuat_phat": to_iso(r["NgayXuatPhat"]),
            "ngay_ket_thuc": to_iso(r["NgayKetThuc"]),
            "so_luong_khach": to_int(r["SoLuongKhach"]),
            "ma_nha_nghi": r["MaNhaNghi"],
            "ten_nha_nghi": r["TenNhaNghi"],
            "so_phong": to_int(r["SoPhong"]),
            "tien_tour": to_int(r["TienTour"]),
            "tien_phong": to_int(r["TienPhong"]),
            "tong_tien": to_int(r["TongTien"]),
            "ma_trang_thai": r["MaTrangThai"],
            "ten_trang_thai": r["TenTrangThai"],
            "ngay_huy": to_iso(r["NgayHuy"]),
            "tien_phat": to_opt_int(r["TienPhat"]),
            "tien_hoan": to_opt_int(r["TienHoan"]),
        }
        for r in rows
    ]

    return {"counts": counts, "orders": orders}
