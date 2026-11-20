"""Các hàm truy vấn chỉ-đọc bổ sung hỗ trợ REST API mà không sửa tour_app/."""

from __future__ import annotations

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
