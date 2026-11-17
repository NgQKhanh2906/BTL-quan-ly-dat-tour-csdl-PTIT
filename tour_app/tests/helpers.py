import re
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import db


def _loai_bo_comment_sql(raw_sql: str) -> str:
    """Loại bỏ comment khối (/* ... */) và dòng comment (--) khỏi nội dung SQL."""
    khong_block = re.sub(r"/\*.*?\*/", "", raw_sql, flags=re.DOTALL)
    cac_dong = [
        dong for dong in khong_block.splitlines() if not dong.lstrip().startswith("--")
    ]
    return "\n".join(cac_dong)


def doc_cau_lenh_kiem_tra_rang_buoc() -> list[str]:
    """Đọc các câu lệnh SELECT kiểm tra từ database/4_KiemTra_RangBuoc.sql."""
    sql_path = ROOT_DIR / "database" / "4_KiemTra_RangBuoc.sql"
    raw_sql = sql_path.read_text(encoding="utf-8")
    sach = _loai_bo_comment_sql(raw_sql)
    cau_lenh: list[str] = []
    for stmt in sach.split(";"):
        stmt_sach = stmt.strip()
        if not stmt_sach:
            continue
        if stmt_sach.upper().startswith("USE "):
            continue
        cau_lenh.append(stmt_sach)
    if not cau_lenh:
        raise ValueError("Không tìm thấy câu lệnh SELECT nào trong 4_KiemTra_RangBuoc.sql")
    return cau_lenh


def chay_kiem_tra_rang_buoc() -> list[dict]:
    """Chạy 4_KiemTra_RangBuoc.sql và trả về danh sách dòng vi phạm (rỗng nếu sạch)."""
    vi_pham: list[dict] = []
    for stmt in doc_cau_lenh_kiem_tra_rang_buoc():
        vi_pham.extend(db.doc(stmt))
    return vi_pham


def khoi_phuc_dh004() -> None:
    """Khôi phục trạng thái chưa đánh giá của đơn mẫu DH004."""
    db.ghi(
        [
            (
                """
                UPDATE DonHang
                SET DiemTour = NULL,
                    NhanXetTour = NULL,
                    DiemNhaNghi = NULL,
                    NhanXetNhaNghi = NULL,
                    NgayDanhGia = NULL
                WHERE MaDonHang = %s
                """,
                ("DH004",),
                False,
            )
        ]
    )


def khoi_phuc_dh010() -> None:
    """Khôi phục trạng thái mẫu của đơn DH010, lịch trình LT05 và chuyến trung chuyển."""
    db.ghi(
        [
            (
                """
                UPDATE DonHang
                SET MaTrangThai = 'DAT',
                    NgayHuy = NULL,
                    LyDoHuy = NULL
                WHERE MaDonHang = %s
                """,
                ("DH010",),
                False,
            ),
            (
                """
                UPDATE LichTrinh
                SET SoChoDaDat = 4
                WHERE MaLichTrinh = %s
                """,
                ("LT05",),
                False,
            ),
            (
                "DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
                ("DH010",),
                False,
            ),
            (
                """
                INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon, BienSoXe)
                VALUES (%s, %s, %s, %s, %s)
                """,
                ("DH010", "DON_TAI_NHA", "45 Lê Lợi, Hải Phòng", "2026-11-14 04:00:00", None),
                False,
            ),
        ]
    )


def khoi_phuc_trang_thai_don(ma_don: str, ma_trang_thai: str) -> None:
    """Khôi phục trạng thái (DAT/THANHTOAN/HOANTHANH) cho đơn chưa hủy."""
    db.ghi(
        [
            (
                """
                UPDATE DonHang
                SET MaTrangThai = %s,
                    NgayHuy = NULL,
                    LyDoHuy = NULL
                WHERE MaDonHang = %s
                """,
                (ma_trang_thai, ma_don),
                False,
            )
        ]
    )


def xoa_don_va_khach_thu_nghiem(
    ma_don_list: list[str] | tuple[str, ...] = (),
    ma_kh_list: list[str] | tuple[str, ...] = (),
    cap_nhat_lt: dict[str, int] | None = None,
) -> None:
    """Xóa các đơn hàng, chuyến trung chuyển, khách hàng thử nghiệm và khôi phục số chỗ lịch trình."""
    cac_lenh: list[tuple[str, tuple, bool]] = []
    for ma_don in ma_don_list:
        cac_lenh.append(
            ("DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s", (ma_don,), False)
        )
        cac_lenh.append(("DELETE FROM DonHang WHERE MaDonHang = %s", (ma_don,), False))
    for ma_kh in ma_kh_list:
        cac_lenh.append(("DELETE FROM SDT_KhachHang WHERE MaKH = %s", (ma_kh,), False))
        cac_lenh.append(("DELETE FROM KhachHang WHERE MaKH = %s", (ma_kh,), False))
    if cap_nhat_lt:
        for ma_lt, so_cho_da_dat in cap_nhat_lt.items():
            cac_lenh.append(
                (
                    "UPDATE LichTrinh SET SoChoDaDat = %s WHERE MaLichTrinh = %s",
                    (int(so_cho_da_dat), ma_lt),
                    False,
                )
            )
    if cac_lenh:
        db.ghi(cac_lenh)


def khoi_phuc_f1_mau() -> None:
    """Dọn sạch các đơn hàng (>= DH015) và khách hàng (>= KH009) phát sinh khi kiểm thử F1."""
    db.ghi(
        [
            (
                """
                DELETE FROM ChuyenTrungChuyen
                WHERE CAST(SUBSTRING(MaDonHang, 3) AS UNSIGNED) >= 15
                """,
                (),
                False,
            ),
            (
                """
                DELETE FROM DonHang
                WHERE CAST(SUBSTRING(MaDonHang, 3) AS UNSIGNED) >= 15
                """,
                (),
                False,
            ),
            (
                """
                DELETE FROM SDT_KhachHang
                WHERE CAST(SUBSTRING(MaKH, 3) AS UNSIGNED) >= 9
                """,
                (),
                False,
            ),
            (
                """
                DELETE FROM KhachHang
                WHERE CAST(SUBSTRING(MaKH, 3) AS UNSIGNED) >= 9
                """,
                (),
                False,
            ),
            ("UPDATE LichTrinh SET SoChoDaDat = 2 WHERE MaLichTrinh = %s", ("LT04",), False),
            ("UPDATE LichTrinh SET SoChoDaDat = 4 WHERE MaLichTrinh = %s", ("LT05",), False),
            ("UPDATE LichTrinh SET SoChoDaDat = 3 WHERE MaLichTrinh = %s", ("LT06",), False),
            ("UPDATE LichTrinh SET SoChoDaDat = 2 WHERE MaLichTrinh = %s", ("LT08",), False),
            ("UPDATE LichTrinh SET SoChoDaDat = 0 WHERE MaLichTrinh = %s", ("LT10",), False),
        ]
    )

