import re
from datetime import date, datetime
from html import escape
from pathlib import Path
from string import Template

import mysql.connector

from db import dinh_dang_ngay, dinh_dang_tien, doc, ghi, hien_tai


def _lam_sach_nhan_xet(gia_tri: str | None) -> str | None:
    if gia_tri is None:
        return None
    sach = gia_tri.strip()
    return sach if sach else None


def _chuyen_datetime(gia_tri: datetime | str) -> datetime:
    """Chuyển chuỗi thời gian sang datetime để so sánh và định dạng đồng nhất."""
    if isinstance(gia_tri, datetime):
        return gia_tri
    return datetime.fromisoformat(str(gia_tri).strip())


def _dinh_dang_sql_datetime(gia_tri: datetime | str) -> str:
    """Chuẩn hóa datetime sang chuỗi YYYY-MM-DD HH:MM:SS dùng cho tham số SQL."""
    return _chuyen_datetime(gia_tri).strftime("%Y-%m-%d %H:%M:%S")


def _chuyen_date(gia_tri: date | datetime | str | None) -> date | None:
    """Chuyển đổi giá trị ngày sang kiểu date để lọc theo ngày khởi hành."""
    if gia_tri is None:
        return None
    if isinstance(gia_tri, datetime):
        return gia_tri.date()
    if isinstance(gia_tri, date):
        return gia_tri
    sach = str(gia_tri).strip()
    if not sach:
        return None
    return date.fromisoformat(sach[:10])


def lay_ds_tinh_thanh() -> list[dict]:
    """Lấy danh sách tỉnh thành phục vụ lọc điểm đến trên màn hình S1."""
    return doc("SELECT MaTinh, TenTinh FROM TinhThanh ORDER BY TenTinh")


def tim_kiem_lich_trinh(
    tu_khoa: str | None = None,
    ma_tinh_den: str | None = None,
    gia_tu: int | None = None,
    gia_den: int | None = None,
    tu_ngay=None,
    den_ngay=None,
    so_khach: int = 1,
    diem_toi_thieu: float | None = None,
) -> list[dict]:
    """Tra cứu lịch trình tour theo 8 tiêu chí động của màn hình S1."""
    sql = """
        SELECT lt.MaLichTrinh,
               t.TenTour,
               txp.TenTinh AS NoiDi,
               tden.TenTinh AS NoiDen,
               lt.NgayXuatPhat,
               DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) + 1 AS SoNgay,
               lt.GiaCoBan,
               lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
               dg.DiemTB,
               COALESCE(dg.SoLuot, 0) AS SoLuotDanhGia
        FROM LichTrinh lt
        JOIN Tour t ON t.MaTour = lt.MaTour
        JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
        JOIN TinhThanh tden ON tden.MaTinh = t.MaTinhDen
        LEFT JOIN (
            SELECT l.MaTour, ROUND(AVG(d.DiemTour), 1) AS DiemTB, COUNT(d.DiemTour) AS SoLuot
            FROM DonHang d
            JOIN LichTrinh l ON l.MaLichTrinh = d.MaLichTrinh
            WHERE d.DiemTour IS NOT NULL
            GROUP BY l.MaTour
        ) AS dg ON dg.MaTour = t.MaTour
        WHERE (%(TuKhoa)s IS NULL OR t.TenTour LIKE CONCAT('%', %(TuKhoa)s, '%'))
          AND (%(MaTinhDen)s IS NULL OR t.MaTinhDen = %(MaTinhDen)s)
          AND (%(GiaTu)s IS NULL OR lt.GiaCoBan >= %(GiaTu)s)
          AND (%(GiaDen)s IS NULL OR lt.GiaCoBan <= %(GiaDen)s)
          AND lt.NgayXuatPhat >= %(TuNgay)s
          AND (%(DenNgay)s IS NULL OR lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY)
          AND lt.SoChoToiDa - lt.SoChoDaDat >= %(SoKhach)s
          AND (%(DiemToiThieu)s IS NULL OR dg.DiemTB >= %(DiemToiThieu)s)
        ORDER BY lt.NgayXuatPhat, lt.GiaCoBan
    """
    tu_khoa_sach = _lam_sach_nhan_xet(tu_khoa)
    ma_tinh_sach = _lam_sach_nhan_xet(ma_tinh_den)
    gia_tu_tham_so = int(gia_tu) if gia_tu is not None and int(gia_tu) > 0 else None
    gia_den_tham_so = int(gia_den) if gia_den is not None and int(gia_den) > 0 else None
    tu_ngay_tham_so = _chuyen_date(tu_ngay) or hien_tai().date()
    den_ngay_tham_so = _chuyen_date(den_ngay)
    so_khach_tham_so = int(so_khach) if so_khach is not None else 1
    diem_tham_so = float(diem_toi_thieu) if diem_toi_thieu is not None else None

    tham_so = {
        "TuKhoa": tu_khoa_sach,
        "MaTinhDen": ma_tinh_sach,
        "GiaTu": gia_tu_tham_so,
        "GiaDen": gia_den_tham_so,
        "TuNgay": tu_ngay_tham_so,
        "DenNgay": den_ngay_tham_so,
        "SoKhach": so_khach_tham_so,
        "DiemToiThieu": diem_tham_so,
    }
    return doc(sql, tham_so)


def lay_ds_khach_hang() -> list[dict]:
    """Lấy danh sách khách hàng phục vụ chọn khách trên giao diện."""
    return doc("SELECT MaKH, HoTen, Email, DiaChi FROM KhachHang ORDER BY MaKH")


def lay_don_cho_danh_gia(ma_kh: str) -> list[dict]:
    """Lấy danh sách đơn hàng đã hoàn thành nhưng chưa đánh giá của khách hàng."""
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
        WHERE dh.MaKH = %(MaKH)s
          AND dh.MaTrangThai = 'HOANTHANH'
          AND dh.NgayDanhGia IS NULL
        ORDER BY lt.NgayKetThuc DESC
    """
    return doc(sql, {"MaKH": ma_kh})


def kiem_tra_danh_gia(
    diem_tour: int,
    nhan_xet_tour: str | None,
    co_nha_nghi: bool,
    diem_nn: int | None,
    nhan_xet_nn: str | None,
) -> tuple[list[str], str | None, int | None, str | None]:
    """Kiểm tra hợp lệ dữ liệu đánh giá (Tầng 1) và chuẩn hóa chuỗi nhận xét."""
    loi: list[str] = []
    nx_tour_sach = _lam_sach_nhan_xet(nhan_xet_tour)
    nx_nn_sach = _lam_sach_nhan_xet(nhan_xet_nn)

    if diem_tour is None or not (1 <= int(diem_tour) <= 5):
        loi.append("Điểm đánh giá tour phải từ 1 đến 5 sao.")
    if nx_tour_sach is not None and len(nx_tour_sach) > 500:
        loi.append("Nhận xét về chương trình tour tối đa 500 ký tự.")

    if not co_nha_nghi:
        if diem_nn is not None:
            loi.append("Chỉ được đánh giá nhà nghỉ khi đơn hàng có đặt nhà nghỉ.")
        if nx_nn_sach is not None:
            loi.append(
                "Chỉ được nhập nhận xét nhà nghỉ khi đơn hàng có đặt nhà nghỉ và đã chấm điểm."
            )
        return loi, nx_tour_sach, None, None

    diem_nn_sach: int | None = None
    if diem_nn is not None:
        diem_nn_int = int(diem_nn)
        if not (1 <= diem_nn_int <= 5):
            loi.append("Điểm đánh giá nhà nghỉ phải từ 1 đến 5 sao.")
        else:
            diem_nn_sach = diem_nn_int
    elif nx_nn_sach is not None:
        loi.append(
            "Bạn đã nhập nhận xét cho nhà nghỉ nhưng chưa tích chọn chấm điểm sao nhà nghỉ. "
            "Vui lòng tích chọn chấm điểm sao nhà nghỉ hoặc xóa nhận xét nhà nghỉ."
        )

    if nx_nn_sach is not None and len(nx_nn_sach) > 500:
        loi.append("Nhận xét về nhà nghỉ tối đa 500 ký tự.")

    return loi, nx_tour_sach, diem_nn_sach, nx_nn_sach


def luu_danh_gia(
    ma_don: str,
    diem_tour: int,
    nhan_xet_tour: str | None,
    diem_nn: int | None,
    nhan_xet_nn: str | None,
    ngay_danh_gia: datetime,
) -> None:
    """Lưu đánh giá của đơn hàng hoàn thành (chỉ cho phép ghi đúng 1 lần)."""
    ngay_dg_str = _dinh_dang_sql_datetime(ngay_danh_gia)
    sql = """
        UPDATE DonHang
        SET DiemTour       = %s,
            NhanXetTour    = %s,
            NgayDanhGia    = %s,
            DiemNhaNghi    = %s,
            NhanXetNhaNghi = %s
        WHERE MaDonHang = %s
          AND MaTrangThai = 'HOANTHANH'
          AND NgayDanhGia IS NULL
    """
    tham_so = (
        int(diem_tour),
        _lam_sach_nhan_xet(nhan_xet_tour),
        ngay_dg_str,
        int(diem_nn) if diem_nn is not None else None,
        _lam_sach_nhan_xet(nhan_xet_nn),
        ma_don,
    )
    ghi([(sql, tham_so, True)])


def lay_don_dang_mo() -> list[dict]:
    """Lấy danh sách đơn hàng đang mở (DAT hoặc THANHTOAN) theo ngày xuất phát tăng dần."""
    sql = """
        SELECT MaDonHang, HoTen, TenTour, NgayXuatPhat, SoLuongKhach, TongTien, MaTrangThai, TenTrangThai
        FROM v_DonHang_ChiTiet
        WHERE MaTrangThai IN ('DAT', 'THANHTOAN')
        ORDER BY NgayXuatPhat, MaDonHang
    """
    return doc(sql)


def lay_chi_tiet_don_f2(ma_don: str) -> dict | None:
    """Lấy thông tin chi tiết của một đơn hàng phục vụ màn hình quản lý đơn F2."""
    sql = """
        SELECT v.MaDonHang, v.MaKH, v.HoTen,
               v.MaLichTrinh, v.NgayXuatPhat, v.NgayKetThuc,
               d.MaNhaNghi, v.TenNhaNghi, v.SoLuongKhach, v.SoPhong,
               v.NgayDat, v.MaTrangThai, v.TenTrangThai,
               v.TienTour, v.TienPhong, v.TongTien
        FROM v_DonHang_ChiTiet v
        JOIN DonHang d ON d.MaDonHang = v.MaDonHang
        WHERE v.MaDonHang = %(MaDonHang)s
    """
    ket_qua = doc(sql, {"MaDonHang": ma_don})
    return ket_qua[0] if ket_qua else None


def lay_trang_thai_dich_f2(ma_don: str, thoi_diem: datetime) -> list[dict]:
    """Lấy các trạng thái đích hợp lệ theo luồng một chiều và điều kiện thời gian."""
    sql = """
        SELECT tt.MaTrangThai, tt.TenTrangThai
        FROM DonHang d
        JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
        JOIN TrangThaiDonHang tt
          ON (d.MaTrangThai = 'DAT' AND tt.MaTrangThai = 'THANHTOAN')
          OR (d.MaTrangThai = 'THANHTOAN' AND tt.MaTrangThai = 'HOANTHANH' AND lt.NgayKetThuc < %(HienTai)s)
          OR (d.MaTrangThai IN ('DAT', 'THANHTOAN') AND tt.MaTrangThai = 'HUY' AND lt.NgayXuatPhat > %(HienTai)s)
        WHERE d.MaDonHang = %(MaDonHang)s
        ORDER BY tt.ThuTu
    """
    return doc(
        sql,
        {
            "HienTai": _dinh_dang_sql_datetime(thoi_diem),
            "MaDonHang": ma_don,
        },
    )


def tinh_xem_truoc_phat_huy(ma_don: str, ngay_gio_huy: datetime) -> dict | None:
    """Tính xem trước tỷ lệ phạt, phí phạt và số tiền hoàn lại khi hủy đơn."""
    sql = """
        SELECT x.MaDonHang,
               x.TongTien,
               x.SoNgayTruocKhoiHanh,
               x.SoGioSauKhiDat,
               x.TyLePhat,
               ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienPhat,
               x.TongTien - ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienHoan
        FROM (
            SELECT v.MaDonHang,
                   v.TongTien,
                   TIMESTAMPDIFF(HOUR, v.NgayDat, %(NgayHuy)s) AS SoGioSauKhiDat,
                   DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) AS SoNgayTruocKhoiHanh,
                   CASE
                       WHEN TIMESTAMPDIFF(HOUR, v.NgayDat, %(NgayHuy)s) < 24
                            AND DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 7 THEN 0
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 15 THEN 10
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 7  THEN 30
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 3  THEN 50
                       ELSE 100
                   END AS TyLePhat
            FROM v_DonHang_ChiTiet v
            WHERE v.MaDonHang = %(MaDonHang)s
        ) AS x
    """
    ket_qua = doc(
        sql,
        {
            "NgayHuy": _dinh_dang_sql_datetime(ngay_gio_huy),
            "MaDonHang": ma_don,
        },
    )
    return ket_qua[0] if ket_qua else None


def kiem_tra_huy_don(
    ngay_dat: datetime,
    ngay_xuat_phat: datetime,
    ngay_gio_huy: datetime,
    ly_do_huy: str,
    da_dong_y_phat: bool,
) -> list[str]:
    """Kiểm tra dữ liệu hủy đơn ở tầng ứng dụng, bao gồm RB23 và xác nhận mức phạt."""
    loi: list[str] = []
    ly_do_sach = (ly_do_huy or "").strip()
    if not ly_do_sach:
        loi.append("Vui lòng nhập Lý do hủy tour (không được để trống).")
    elif len(ly_do_sach) > 255:
        loi.append("Lý do hủy tour tối đa 255 ký tự.")

    ngay_dat_dt = _chuyen_datetime(ngay_dat)
    ngay_xuat_phat_dt = _chuyen_datetime(ngay_xuat_phat)
    ngay_huy_dt = _chuyen_datetime(ngay_gio_huy)

    if ngay_huy_dt < ngay_dat_dt:
        loi.append(
            f"Thời điểm hủy ({dinh_dang_ngay(ngay_huy_dt)}) không được nhỏ hơn "
            f"thời điểm đặt tour ({dinh_dang_ngay(ngay_dat_dt)})."
        )
    if ngay_huy_dt >= ngay_xuat_phat_dt:
        loi.append(
            f"Thời điểm hủy ({dinh_dang_ngay(ngay_huy_dt)}) phải trước "
            f"thời điểm khởi hành của lịch trình ({dinh_dang_ngay(ngay_xuat_phat_dt)})."
        )
    if not da_dong_y_phat:
        loi.append("Vui lòng xác nhận khách đã đồng ý mức phạt trước khi hủy đơn.")

    return loi


def huy_don(ma_don: str, ngay_gio_huy: datetime, ly_do_huy: str) -> None:
    """Hủy đơn, hoàn chỗ lịch trình và xóa chuyến trung chuyển trong 1 giao dịch nguyên tử."""
    ngay_huy_str = _dinh_dang_sql_datetime(ngay_gio_huy)
    ly_do_sach = (ly_do_huy or "").strip()
    ds_lenh_huy = [
        (
            """
            UPDATE DonHang d
            JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
            SET d.MaTrangThai = 'HUY',
                d.NgayHuy     = %s,
                d.LyDoHuy     = %s
            WHERE d.MaDonHang = %s
              AND d.MaTrangThai IN ('DAT', 'THANHTOAN')
              AND %s < lt.NgayXuatPhat
            """,
            (ngay_huy_str, ly_do_sach, ma_don, ngay_huy_str),
            True,
        ),
        (
            """
            UPDATE LichTrinh lt
            JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh
            SET lt.SoChoDaDat = lt.SoChoDaDat - d.SoLuongKhach
            WHERE d.MaDonHang = %s
              AND lt.SoChoDaDat >= d.SoLuongKhach
            """,
            (ma_don,),
            True,
        ),
        (
            "DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
            (ma_don,),
            False,
        ),
    ]
    ghi(ds_lenh_huy)


def chuyen_trang_thai_don(ma_don: str, trang_thai_moi: str, thoi_diem: datetime) -> None:
    """Chuyển trạng thái xuôi (DAT -> THANHTOAN hoặc THANHTOAN -> HOANTHANH sau kết thúc tour)."""
    sql = """
        UPDATE DonHang d
        JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
        SET d.MaTrangThai = %(TrangThaiMoi)s
        WHERE d.MaDonHang = %(MaDonHang)s
          AND (
              (d.MaTrangThai = 'DAT' AND %(TrangThaiMoi)s = 'THANHTOAN')
           OR (
               d.MaTrangThai = 'THANHTOAN'
               AND %(TrangThaiMoi)s = 'HOANTHANH'
               AND lt.NgayKetThuc < %(HienTai)s
           )
          )
    """
    tham_so = {
        "TrangThaiMoi": trang_thai_moi,
        "MaDonHang": ma_don,
        "HienTai": _dinh_dang_sql_datetime(thoi_diem),
    }
    ghi([(sql, tham_so, True)])


def lay_ds_khach_hang_f1() -> list[dict]:
    """Lấy danh sách khách hàng cho màn hình đặt tour F1 kèm SĐT tổng hợp."""
    sql = """
        SELECT kh.MaKH,
               CONCAT(kh.MaKH, ' - ', kh.HoTen) AS HienThi,
               kh.HoTen,
               kh.Email,
               kh.DiaChi,
               COALESCE(
                   GROUP_CONCAT(DISTINCT sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', '),
                   ''
               ) AS SoDienThoai
        FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        GROUP BY kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi
        ORDER BY kh.MaKH
    """
    return doc(sql)


def kiem_tra_trung_khach_hang(email: str, so_dien_thoai: str) -> dict | None:
    """Kiểm tra trùng Email hoặc Số điện thoại của khách hàng hiện có."""
    email_sach = (email or "").strip()
    sdt_sach = (so_dien_thoai or "").strip()
    if not email_sach and not sdt_sach:
        return None

    sql = """
        SELECT kh.MaKH,
               kh.HoTen,
               kh.Email,
               kh.DiaChi,
               COALESCE(
                   GROUP_CONCAT(DISTINCT sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', '),
                   ''
               ) AS CacSDT
        FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE (%(Email)s <> '' AND LOWER(kh.Email) = LOWER(%(Email)s))
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
        LIMIT 1
    """
    ket_qua = doc(sql, {"Email": email_sach, "SoDienThoai": sdt_sach})
    return ket_qua[0] if ket_qua else None


def lay_lich_trinh_con_cho(thoi_diem: datetime) -> list[dict]:
    """Lấy danh sách lịch trình chưa khởi hành và còn chỗ tại thời điểm hiện tại."""
    sql = """
        SELECT lt.MaLichTrinh,
               t.MaTour,
               t.TenTour,
               lt.NgayXuatPhat,
               lt.NgayKetThuc,
               DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS SoDem,
               lt.GiaCoBan,
               lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
               t.MaTinhDen,
               tt.TenTinh AS TenTinhDen
        FROM LichTrinh lt
        JOIN Tour t ON t.MaTour = lt.MaTour
        JOIN TinhThanh tt ON tt.MaTinh = t.MaTinhDen
        WHERE lt.NgayXuatPhat > %(HienTai)s
          AND lt.SoChoToiDa - lt.SoChoDaDat > 0
        ORDER BY lt.NgayXuatPhat, lt.MaLichTrinh
    """
    return doc(sql, {"HienTai": _dinh_dang_sql_datetime(thoi_diem)})


def lay_noi_nghi_theo_tinh(ma_tinh_den: str) -> list[dict]:
    """Lấy danh sách nhà nghỉ / homestay thuộc đúng tỉnh điểm đến của tour."""
    sql = """
        SELECT MaNhaNghi, TenNhaNghi, LoaiHinh, GiaPhongMoiDem
        FROM NhaNghi
        WHERE MaTinh = %(MaTinhDen)s
        ORDER BY GiaPhongMoiDem, MaNhaNghi
    """
    return doc(sql, {"MaTinhDen": ma_tinh_den})


def tinh_du_toan_f1(
    so_khach: int,
    gia_co_ban: int,
    so_phong: int,
    gia_phong_moi_dem: int,
    so_dem: int,
    co_nha_nghi: bool,
) -> tuple[int, int, int]:
    """Tính tiền tour, tiền phòng và tổng tiền dự kiến theo công thức của v_DonHang_ChiTiet."""
    tien_tour = int(so_khach) * int(gia_co_ban)
    if co_nha_nghi and int(so_dem) > 0:
        tien_phong = int(so_phong) * int(gia_phong_moi_dem) * int(so_dem)
    else:
        tien_phong = 0
    return tien_tour, tien_phong, tien_tour + tien_phong


def kiem_tra_dat_tour(
    la_khach_moi: bool,
    ma_kh: str | None,
    ho_ten: str,
    so_dien_thoai: str,
    email: str,
    dia_chi: str,
    so_khach: int,
    so_cho_con_lai: int,
    so_dem: int,
    co_nha_nghi: bool,
    so_phong: int,
    co_xe_don: bool,
    dia_chi_don: str | None,
    dt_don: datetime | None,
    co_xe_ve: bool,
    dt_ve: datetime | None,
    thoi_diem_hien_tai: datetime,
    ngay_xuat_phat: datetime,
    ngay_ket_thuc: datetime,
) -> list[str]:
    """Kiểm tra toàn bộ ràng buộc đặt tour F1 ở tầng Form trước khi ghi MySQL."""
    loi: list[str] = []

    if la_khach_moi:
        ho_ten_sach = (ho_ten or "").strip()
        sdt_sach = (so_dien_thoai or "").strip()
        email_sach = (email or "").strip()
        dia_chi_sach = (dia_chi or "").strip()

        if not ho_ten_sach:
            loi.append("Vui lòng nhập họ và tên khách hàng.")
        elif len(ho_ten_sach) > 100:
            loi.append("Họ và tên khách hàng tối đa 100 ký tự.")

        if not sdt_sach:
            loi.append("Vui lòng nhập số điện thoại khách hàng.")
        elif not re.match(r"^0[0-9]{9}$", sdt_sach):
            loi.append("Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")

        if not email_sach:
            loi.append("Vui lòng nhập email khách hàng.")
        elif len(email_sach) > 100:
            loi.append("Email khách hàng tối đa 100 ký tự.")
        elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_sach):
            loi.append("Email không hợp lệ (ví dụ đúng: ten@domain.com).")

        if not dia_chi_sach:
            loi.append("Vui lòng nhập địa chỉ liên hệ của khách hàng.")
        elif len(dia_chi_sach) > 255:
            loi.append("Địa chỉ liên hệ tối đa 255 ký tự.")
    elif not (ma_kh or "").strip():
        loi.append("Vui lòng chọn khách hàng.")

    hien_tai_dt = _chuyen_datetime(thoi_diem_hien_tai)
    xp_dt = _chuyen_datetime(ngay_xuat_phat)
    kt_dt = _chuyen_datetime(ngay_ket_thuc)

    if xp_dt <= hien_tai_dt:
        loi.append("Lịch trình đã khởi hành hoặc quá thời điểm đặt tour (RB22).")

    so_cho_int = int(so_cho_con_lai)
    if so_cho_int <= 0:
        loi.append("Lịch trình đã hết chỗ, không thể đặt thêm.")

    if so_khach is None or int(so_khach) < 1:
        loi.append("Số lượng khách phải lớn hơn 0.")
    elif so_cho_int > 0 and int(so_khach) > so_cho_int:
        loi.append(f"Số lượng khách ({int(so_khach)}) vượt quá số chỗ còn lại ({so_cho_int}).")

    so_dem_int = int(so_dem)
    if so_dem_int == 0 and co_nha_nghi:
        loi.append("Tour trong ngày (0 đêm) không áp dụng đặt nơi nghỉ.")
    elif co_nha_nghi:
        so_khach_int = int(so_khach) if so_khach is not None else 0
        if (
            so_phong is None
            or int(so_phong) < 1
            or (so_khach_int >= 1 and int(so_phong) > so_khach_int)
        ):
            loi.append("Số phòng phải từ 1 đến số khách")

    if co_xe_don:
        dia_chi_don_sach = (dia_chi_don or "").strip()
        if not dia_chi_don_sach:
            loi.append("Vui lòng nhập địa chỉ đón")
        elif len(dia_chi_don_sach) > 255:
            loi.append("Địa chỉ đón tối đa 255 ký tự.")

        if dt_don is None:
            loi.append("Vui lòng chọn đầy đủ ngày và giờ đón tại nhà.")
        else:
            dt_don_dt = _chuyen_datetime(dt_don)
            if dt_don_dt <= hien_tai_dt or dt_don_dt >= xp_dt:
                loi.append("Giờ đón tại nhà phải sau thời điểm hiện tại và trước giờ xuất phát")

    if co_xe_ve:
        if not co_nha_nghi or so_dem_int == 0:
            loi.append("Chỉ có thể đăng ký xe về nơi nghỉ khi có đặt nơi nghỉ")
        elif dt_ve is None:
            loi.append("Vui lòng chọn đầy đủ ngày và giờ về nơi nghỉ.")
        else:
            dt_ve_dt = _chuyen_datetime(dt_ve)
            if dt_ve_dt < xp_dt or dt_ve_dt > kt_dt:
                loi.append("Giờ về nơi nghỉ phải nằm trong khoảng thời gian diễn ra tour")

    return loi


def luu_dat_tour(du_lieu: dict) -> str:
    """Sinh mã (nếu cần) và lưu đơn đặt tour cùng khách mới, trừ chỗ, xe trung chuyển trong 1 transaction."""
    sql_ma_kh = """
        SELECT CONCAT('KH', LPAD(COALESCE(MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)), 0) + 1, 3, '0')) AS MaKHMoi
        FROM KhachHang
    """
    sql_ma_don = """
        SELECT CONCAT('DH', LPAD(COALESCE(MAX(CAST(SUBSTRING(MaDonHang, 3) AS UNSIGNED)), 0) + 1, 3, '0')) AS MaDonHangMoi
        FROM DonHang
    """
    sql_them_kh = """
        INSERT INTO KhachHang (MaKH, HoTen, Email, DiaChi)
        VALUES (%(MaKH)s, %(HoTen)s, %(Email)s, %(DiaChi)s)
    """
    sql_them_sdt = """
        INSERT INTO SDT_KhachHang (MaKH, SoDienThoai)
        VALUES (%(MaKH)s, %(SoDienThoai)s)
    """
    sql_dat_don = """
        INSERT INTO DonHang (MaDonHang, NgayDat, SoLuongKhach, SoPhong, MaKH, MaLichTrinh, MaNhaNghi)
        VALUES (%(MaDonHang)s, %(HienTai)s, %(SoKhach)s, %(SoPhong)s, %(MaKH)s, %(MaLichTrinh)s, %(MaNhaNghi)s)
    """
    sql_tru_cho = """
        UPDATE LichTrinh
        SET SoChoDaDat = SoChoDaDat + %(SoKhach)s
        WHERE MaLichTrinh = %(MaLichTrinh)s
    """
    sql_don_tai_nha = """
        INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon)
        VALUES (%(MaDonHang)s, 'DON_TAI_NHA', %(DiaChiDon)s, %(GioDon)s)
    """
    sql_ve_noi_nghi = """
        INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, ThoiGianDon)
        VALUES (%(MaDonHang)s, 'VE_NOI_NGHI', %(GioVeNoiNghi)s)
    """

    la_khach_moi = bool(du_lieu.get("LaKhachMoi"))
    ma_kh_goc = (du_lieu.get("MaKH") or "").strip() or None
    ho_ten = (du_lieu.get("HoTen") or "").strip()
    email = (du_lieu.get("Email") or "").strip()
    so_dien_thoai = (du_lieu.get("SoDienThoai") or "").strip()
    dia_chi = (du_lieu.get("DiaChi") or "").strip()
    ma_lich_trinh = du_lieu["MaLichTrinh"]
    so_khach = int(du_lieu["SoKhach"])
    ma_nha_nghi = du_lieu.get("MaNhaNghi") or None
    so_phong = int(du_lieu.get("SoPhong") or 0)
    dia_chi_don = (du_lieu.get("DiaChiDon") or "").strip() or None
    gio_don = du_lieu.get("GioDon")
    gio_ve = du_lieu.get("GioVeNoiNghi")
    ngay_dat = du_lieu.get("NgayDat") or du_lieu.get("HienTai") or hien_tai()
    ngay_dat_str = _dinh_dang_sql_datetime(ngay_dat)

    for lan_thu in range(3):
        if la_khach_moi:
            kq_kh = doc(sql_ma_kh)
            ma_kh_luu = kq_kh[0]["MaKHMoi"] if kq_kh and kq_kh[0]["MaKHMoi"] else "KH001"
        else:
            if not ma_kh_goc:
                raise ValueError("Thiếu mã khách hàng để tạo đơn đặt tour.")
            ma_kh_luu = ma_kh_goc

        kq_don = doc(sql_ma_don)
        ma_don_moi = (
            kq_don[0]["MaDonHangMoi"]
            if kq_don and kq_don[0]["MaDonHangMoi"]
            else "DH001"
        )

        cac_lenh: list[tuple[str, dict, bool]] = []
        if la_khach_moi:
            cac_lenh.append(
                (
                    sql_them_kh,
                    {
                        "MaKH": ma_kh_luu,
                        "HoTen": ho_ten,
                        "Email": email,
                        "DiaChi": dia_chi,
                    },
                    True,
                )
            )
            cac_lenh.append(
                (
                    sql_them_sdt,
                    {"MaKH": ma_kh_luu, "SoDienThoai": so_dien_thoai},
                    True,
                )
            )

        cac_lenh.append(
            (
                sql_dat_don,
                {
                    "MaDonHang": ma_don_moi,
                    "HienTai": ngay_dat_str,
                    "SoKhach": so_khach,
                    "SoPhong": so_phong,
                    "MaKH": ma_kh_luu,
                    "MaLichTrinh": ma_lich_trinh,
                    "MaNhaNghi": ma_nha_nghi,
                },
                True,
            )
        )
        cac_lenh.append(
            (
                sql_tru_cho,
                {"SoKhach": so_khach, "MaLichTrinh": ma_lich_trinh},
                True,
            )
        )
        if gio_don is not None:
            cac_lenh.append(
                (
                    sql_don_tai_nha,
                    {
                        "MaDonHang": ma_don_moi,
                        "DiaChiDon": dia_chi_don,
                        "GioDon": _dinh_dang_sql_datetime(gio_don),
                    },
                    True,
                )
            )
        if gio_ve is not None:
            cac_lenh.append(
                (
                    sql_ve_noi_nghi,
                    {
                        "MaDonHang": ma_don_moi,
                        "GioVeNoiNghi": _dinh_dang_sql_datetime(gio_ve),
                    },
                    True,
                )
            )

        try:
            ghi(cac_lenh)
            return ma_don_moi
        except mysql.connector.Error as loi:
            la_trung_pk = loi.errno == 1062 and "PRIMARY" in (loi.msg or "")
            if la_trung_pk and lan_thu < 2:
                continue
            raise

    raise RuntimeError("Không thể sinh mã đơn đặt tour mới sau nhiều lần thử.")


def lay_ds_don_r1() -> list[dict]:
    """Lấy danh sách toàn bộ đơn hàng phục vụ chọn in phiếu xác nhận R1."""
    sql = """
        SELECT MaDonHang, HoTen, TenTour,
               NgayXuatPhat, TenTrangThai, TongTien
        FROM v_DonHang_ChiTiet
        ORDER BY MaDonHang
    """
    return doc(sql)


def lay_chi_tiet_don_r1(ma_don: str) -> dict | None:
    """Truy vấn thông tin chi tiết của một đơn hàng cho phiếu xác nhận R1.1."""
    sql = """
        SELECT v.MaDonHang, v.NgayDat, v.MaTrangThai, v.TenTrangThai,
               v.MaKH, v.HoTen AS TenKhachHang, kh.Email, kh.DiaChi AS DiaChiKH,
               kh.SoID, th.LoaiThe,
               t.MaTour, v.TenTour, txp.TenTinh AS TinhXuatPhat, v.TinhDen,
               v.MaLichTrinh, v.NgayXuatPhat, v.NgayKetThuc, v.SoDem, lt.DiemTapTrung,
               v.SoLuongKhach, v.GiaCoBan, v.TienTour,
               d.MaNhaNghi, v.TenNhaNghi, nn.LoaiHinh, nn.DiaChi AS DiaChiNhaNghi,
               v.SoPhong, v.GiaPhongMoiDem, v.TienPhong, v.TongTien,
               v.NgayHuy, v.LyDoHuy, v.TyLePhat, v.TienPhat, v.TienHoan
        FROM v_DonHang_ChiTiet v
        JOIN DonHang d ON d.MaDonHang = v.MaDonHang
        JOIN KhachHang kh ON kh.MaKH = v.MaKH
        LEFT JOIN TheThanhToan th ON th.SoID = kh.SoID
        JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
        JOIN Tour t ON t.MaTour = v.MaTour
        JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
        LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
        WHERE v.MaDonHang = %(MaDonHang)s
    """
    ket_qua = doc(sql, {"MaDonHang": ma_don})
    return ket_qua[0] if ket_qua else None


def lay_sdt_khach_r1(ma_don: str) -> str:
    """Truy vấn danh sách số điện thoại của khách hàng theo đơn hàng (R1.2)."""
    sql = """
        SELECT GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ') AS SoDienThoai
        FROM DonHang d
        JOIN SDT_KhachHang sdt ON sdt.MaKH = d.MaKH
        WHERE d.MaDonHang = %(MaDonHang)s
    """
    ket_qua = doc(sql, {"MaDonHang": ma_don})
    if ket_qua and ket_qua[0].get("SoDienThoai"):
        return ket_qua[0]["SoDienThoai"]
    return "Chưa cập nhật"


def lay_lich_trung_chuyen_r1(ma_don: str) -> list[dict]:
    """Truy vấn lịch xe trung chuyển theo đơn hàng từ view v_LichTrungChuyen (R1.3)."""
    sql = """
        SELECT TenLoaiChuyen, ThoiGianDon, DiemDon, DiemTra,
               COALESCE(BienSoXe, 'Chưa xếp xe') AS BienSoXe,
               COALESCE(TenDonVi, 'Chưa xếp') AS DonViVanTai
        FROM v_LichTrungChuyen
        WHERE MaDonHang = %(MaDonHang)s
        ORDER BY ThoiGianDon
    """
    return doc(sql, {"MaDonHang": ma_don})


def _tao_khoi_nha_nghi_r1(ct: dict, so_dem: int) -> tuple[str, str]:
    """Dựng khối HTML mục lưu trú và chuỗi diễn giải cách tính tiền phòng cho R1."""
    if not ct.get("MaNhaNghi"):
        khoi = (
            "<div class='note-empty'>"
            "Khách hàng không đăng ký dịch vụ nhà nghỉ đi kèm (0 phòng)."
            "</div>"
        )
        return khoi, "Không sử dụng (0 phòng)"

    so_phong = int(ct.get("SoPhong") or 0)
    gia_phong = escape(dinh_dang_tien(ct.get("GiaPhongMoiDem")))
    khoi = (
        "<table class='info-grid'>"
        "<tr><td style='width:50%;'><strong>Nơi nghỉ lưu trú:</strong> "
        f"{escape(str(ct.get('TenNhaNghi') or ''))} ({escape(str(ct['MaNhaNghi']))})</td>"
        f"<td style='width:50%;'><strong>Số lượng phòng:</strong> {so_phong} phòng "
        f"&times; {so_dem} đêm ({gia_phong}/đêm)</td></tr>"
        "<tr><td colspan='2'><strong>Địa chỉ lưu trú:</strong> "
        f"{escape(str(ct.get('DiaChiNhaNghi') or 'Chưa cập nhật'))} "
        f"({escape(str(ct.get('LoaiHinh') or ''))})</td></tr>"
        "</table>"
    )
    dien_giai = f"{so_phong} phòng &times; {so_dem} đêm &times; {gia_phong}"
    return khoi, dien_giai


def _tao_khoi_trung_chuyen_r1(ds_ctc: list[dict]) -> str:
    """Dựng bảng HTML lịch trình xe trung chuyển có cột Thời gian đón cho R1."""
    if not ds_ctc:
        return (
            "<div class='note-empty'>"
            "Không có chuyến xe trung chuyển đang hoạt động cho đơn hàng này."
            "</div>"
        )

    dong_html = []
    for idx, r in enumerate(ds_ctc, 1):
        dong_html.append(
            "<tr>"
            f"<td class='text-center'>{idx}</td>"
            f"<td>{escape(str(r.get('TenLoaiChuyen') or ''))}</td>"
            f"<td class='text-center'>{escape(dinh_dang_ngay(r.get('ThoiGianDon')))}</td>"
            f"<td>{escape(str(r.get('DiemDon') or ''))}</td>"
            f"<td>{escape(str(r.get('DiemTra') or ''))}</td>"
            f"<td class='text-center'>{escape(str(r.get('BienSoXe') or 'Chưa xếp xe'))}</td>"
            f"<td>{escape(str(r.get('DonViVanTai') or 'Chưa xếp'))}</td>"
            "</tr>"
        )
    return (
        "<table class='data-table'>"
        "<thead><tr>"
        "<th style='width:5%;'>STT</th>"
        "<th style='width:14%;'>Loại chuyến</th>"
        "<th style='width:16%;'>Thời gian đón</th>"
        "<th style='width:22%;'>Điểm đón</th>"
        "<th style='width:21%;'>Điểm trả</th>"
        "<th style='width:11%;'>Biển số xe</th>"
        "<th style='width:11%;'>Đơn vị vận tải</th>"
        "</tr></thead>"
        f"<tbody>{''.join(dong_html)}</tbody></table>"
    )


def _tao_khoi_huy_r1(ct: dict) -> str:
    """Dựng khối HTML thông tin hủy tour & hoàn tiền cho R1 dựa trên MaTrangThai == 'HUY'."""
    if ct.get("MaTrangThai") != "HUY" and ct.get("NgayHuy") is None:
        return (
            "<div class='note-empty'>"
            "Đơn hàng đang hoạt động bình thường (Không phát sinh hủy tour)."
            "</div>"
        )

    ly_do_raw = ct.get("LyDoHuy")
    ly_do_sach = str(ly_do_raw).strip() if ly_do_raw is not None else ""
    ly_do_hien_thi = escape(ly_do_sach) if ly_do_sach else "Không ghi nhận"
    ty_le_phat = int(ct["TyLePhat"]) if ct.get("TyLePhat") is not None else 0

    return (
        "<table class='info-grid'>"
        f"<tr><td style='width:50%;'><strong>Thời điểm hủy đơn:</strong> {escape(dinh_dang_ngay(ct.get('NgayHuy')))}</td>"
        f"<td style='width:50%;'><strong>Phí phạt hủy tour:</strong> "
        f"<strong>{escape(dinh_dang_tien(ct.get('TienPhat')))} ({ty_le_phat}%)</strong></td></tr>"
        f"<tr><td><strong>Lý do hủy:</strong> {ly_do_hien_thi}</td>"
        f"<td><strong>Số tiền hoàn lại cho khách:</strong> "
        f"<strong>{escape(dinh_dang_tien(ct.get('TienHoan')))}</strong></td></tr>"
        "</table>"
    )


def tao_html_phieu_xac_nhan(
    ct: dict,
    danh_sach_sdt: str,
    ds_ctc: list[dict],
    nguoi_lap: str,
    ngay_in: datetime | None = None,
) -> str:
    """Tạo chuỗi HTML hoàn chỉnh cho Phiếu xác nhận R1 bằng thay thế placeholder một lượt."""
    so_dem = int(ct.get("SoDem") or 0)
    thoi_luong = "1 ngày (trong ngày)" if so_dem == 0 else f"{so_dem + 1} ngày {so_dem} đêm"

    khoi_nha_nghi, dien_giai_phong = _tao_khoi_nha_nghi_r1(ct, so_dem)
    khoi_trung_chuyen = _tao_khoi_trung_chuyen_r1(ds_ctc)
    khoi_huy = _tao_khoi_huy_r1(ct)

    so_id_raw = str(ct["SoID"]).strip() if ct.get("SoID") else ""
    if so_id_raw:
        loai_the_raw = str(ct.get("LoaiThe") or "Thanh toán")
        so_id_an = f"**** **** **** {so_id_raw[-4:]}" if len(so_id_raw) >= 4 else so_id_raw
        phuong_thuc_tt = f"Thẻ {escape(loai_the_raw)} ({escape(so_id_an)})"
    else:
        phuong_thuc_tt = "Tiền mặt / Chuyển khoản (Chưa lưu thẻ)"

    ngay_in_dt = _chuyen_datetime(ngay_in) if ngay_in is not None else hien_tai()

    duong_dan_mau = Path(__file__).resolve().parent / "templates" / "phieu_xac_nhan.html"
    html_goc = duong_dan_mau.read_text(encoding="utf-8")

    bang_thay_the = {
        "{{MA_DON_HANG}}": escape(str(ct.get("MaDonHang") or "")),
        "{{NGAY_IN}}": escape(ngay_in_dt.strftime("%d/%m/%Y %H:%M")),
        "{{NGAY_DAT}}": escape(dinh_dang_ngay(ct.get("NgayDat"))),
        "{{TEN_TRANG_THAI}}": escape(str(ct.get("TenTrangThai") or "")),
        "{{NGUOI_LAP}}": escape((nguoi_lap or "").strip()),
        "{{TEN_KHACH_HANG}}": escape(str(ct.get("TenKhachHang") or "")),
        "{{MA_KH}}": escape(str(ct.get("MaKH") or "")),
        "{{DANH_SACH_SDT}}": escape(str(danh_sach_sdt or "Chưa cập nhật")),
        "{{EMAIL_KH}}": escape(str(ct.get("Email") or "Chưa cập nhật")),
        "{{PHUONG_THUC_THANH_TOAN}}": phuong_thuc_tt,
        "{{DIA_CHI_KH}}": escape(str(ct.get("DiaChiKH") or "Chưa cập nhật")),
        "{{TEN_TOUR}}": escape(str(ct.get("TenTour") or "")),
        "{{MA_TOUR}}": escape(str(ct.get("MaTour") or "")),
        "{{TINH_XUAT_PHAT}}": escape(str(ct.get("TinhXuatPhat") or "")),
        "{{TINH_DEN}}": escape(str(ct.get("TinhDen") or "")),
        "{{MA_LICH_TRINH}}": escape(str(ct.get("MaLichTrinh") or "")),
        "{{THOI_LUONG}}": escape(thoi_luong),
        "{{NGAY_KHOI_HANH}}": escape(dinh_dang_ngay(ct.get("NgayXuatPhat"))),
        "{{NGAY_KET_THUC}}": escape(dinh_dang_ngay(ct.get("NgayKetThuc"))),
        "{{DIEM_TAP_TRUNG}}": escape(str(ct.get("DiemTapTrung") or "Chưa cập nhật")),
        "{{SO_LUONG_KHACH}}": str(int(ct.get("SoLuongKhach") or 0)),
        "{{GIA_CO_BAN}}": escape(dinh_dang_tien(ct.get("GiaCoBan"))),
        "{{KHOI_NHA_NGHI}}": khoi_nha_nghi,
        "{{KHOI_TRUNG_CHUYEN}}": khoi_trung_chuyen,
        "{{TIEN_TOUR}}": escape(dinh_dang_tien(ct.get("TienTour"))),
        "{{DIEN_GIAI_PHONG}}": dien_giai_phong,
        "{{TIEN_PHONG}}": escape(dinh_dang_tien(ct.get("TienPhong"))),
        "{{TONG_TIEN}}": escape(dinh_dang_tien(ct.get("TongTien"))),
        "{{KHOI_THONG_TIN_HUY}}": khoi_huy,
    }
    bieu_thuc = re.compile("|".join(re.escape(k) for k in bang_thay_the))
    return bieu_thuc.sub(lambda m: bang_thay_the[m.group(0)], html_goc)


NOI_NHAN_R2 = "Ban Giám đốc công ty du lịch"


def lay_doanh_thu_tour_r2(tu_ngay: date, den_ngay: date) -> list[dict]:
    """Truy vấn tổng hợp doanh thu và đánh giá theo từng tour kèm dòng ROLLUP tổng cộng (R2.1)."""
    sql = """
        SELECT IF(GROUPING(t.MaTour), 'TỔNG CỘNG', t.MaTour) AS MaTour,
               IF(GROUPING(t.MaTour), '', t.TenTour) AS TenTour,
               COUNT(DISTINCT lt.MaLichTrinh) AS SoLichTrinh,
               COALESCE(SUM(v.MaTrangThai <> 'HUY'), 0) AS SoDon,
               COALESCE(SUM(CASE WHEN v.MaTrangThai <> 'HUY' THEN v.SoLuongKhach END), 0) AS SoKhach,
               COALESCE(SUM(v.MaTrangThai = 'HUY'), 0) AS SoDonHuy,
               COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0) AS DoanhThuDichVu,
               COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TienPhatHuy,
               COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0)
               + COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TongDoanhThu,
               ROUND(AVG(v.DiemTour), 1) AS DiemTourTB
        FROM Tour t
        JOIN LichTrinh lt ON lt.MaTour = t.MaTour
        LEFT JOIN v_DonHang_ChiTiet v ON v.MaLichTrinh = lt.MaLichTrinh
        WHERE lt.NgayXuatPhat >= %(TuNgay)s AND lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY
        GROUP BY t.MaTour, t.TenTour WITH ROLLUP
        HAVING GROUPING(t.TenTour) = 0 OR GROUPING(t.MaTour) = 1
    """
    return doc(
        sql,
        {
            "TuNgay": _chuyen_date(tu_ngay),
            "DenNgay": _chuyen_date(den_ngay),
        },
    )


def lay_xep_hang_noi_nghi_r2(tu_ngay: date, den_ngay: date) -> list[dict]:
    """Truy vấn bảng xếp hạng đánh giá cơ sở lưu trú trong kỳ báo cáo (R2.2)."""
    sql = """
        SELECT nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh,
               COUNT(d.DiemNhaNghi) AS SoLuotDanhGia,
               ROUND(AVG(d.DiemNhaNghi), 1) AS DiemTB
        FROM NhaNghi nn
        JOIN TinhThanh tt ON tt.MaTinh = nn.MaTinh
        JOIN DonHang d ON d.MaNhaNghi = nn.MaNhaNghi
        JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
        WHERE d.DiemNhaNghi IS NOT NULL
          AND lt.NgayXuatPhat >= %(TuNgay)s AND lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY
        GROUP BY nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh
        ORDER BY DiemTB DESC, SoLuotDanhGia DESC
    """
    return doc(
        sql,
        {
            "TuNgay": _chuyen_date(tu_ngay),
            "DenNgay": _chuyen_date(den_ngay),
        },
    )


def tao_html_bao_cao_doanh_thu(
    tu_ngay: date,
    den_ngay: date,
    ds_tour: list[dict],
    ds_noi_nghi: list[dict],
    nguoi_lap: str,
    ngay_xuat: datetime | None = None,
    noi_nhan: str = NOI_NHAN_R2,
) -> str:
    """Tạo chuỗi HTML hoàn chỉnh cho Báo cáo doanh thu R2 (khổ in A4 ngang)."""
    tu_ngay_dt = _chuyen_date(tu_ngay)
    den_ngay_dt = _chuyen_date(den_ngay)
    ngay_xuat_dt = _chuyen_datetime(ngay_xuat) if ngay_xuat is not None else hien_tai()

    dong_tong = next((r for r in ds_tour if r.get("MaTour") == "TỔNG CỘNG"), None)
    if dong_tong is not None:
        tong_dt = dong_tong.get("TongDoanhThu") or 0
        so_don = dong_tong.get("SoDon") or 0
        so_khach = dong_tong.get("SoKhach") or 0
        so_don_huy = dong_tong.get("SoDonHuy") or 0
    else:
        tong_dt = sum(int(r.get("TongDoanhThu") or 0) for r in ds_tour)
        so_don = sum(int(r.get("SoDon") or 0) for r in ds_tour)
        so_khach = sum(int(r.get("SoKhach") or 0) for r in ds_tour)
        so_don_huy = sum(int(r.get("SoDonHuy") or 0) for r in ds_tour)

    hang_tour_html = []
    for r in ds_tour:
        la_tong = r.get("MaTour") == "TỔNG CỘNG"
        cls = ' class="hang-tong"' if la_tong else ""
        diem_tb = f"{r['DiemTourTB']}" if r.get("DiemTourTB") is not None else "-"
        hang_tour_html.append(
            f"<tr{cls}>"
            f'<td class="text-center">{escape(str(r.get("MaTour") or ""))}</td>'
            f'<td>{escape(str(r.get("TenTour") or ""))}</td>'
            f'<td class="text-center">{int(r.get("SoLichTrinh") or 0)}</td>'
            f'<td class="text-center">{int(r.get("SoDon") or 0)}</td>'
            f'<td class="text-center">{int(r.get("SoKhach") or 0)}</td>'
            f'<td class="text-center">{int(r.get("SoDonHuy") or 0)}</td>'
            f'<td class="text-right">{escape(dinh_dang_tien(r.get("DoanhThuDichVu") or 0))}</td>'
            f'<td class="text-right">{escape(dinh_dang_tien(r.get("TienPhatHuy") or 0))}</td>'
            f'<td class="text-right">{escape(dinh_dang_tien(r.get("TongDoanhThu") or 0))}</td>'
            f'<td class="text-center">{escape(diem_tb)}</td>'
            f"</tr>"
        )

    hang_nn_html = []
    for r in ds_noi_nghi:
        diem_nn = f"{r['DiemTB']} sao" if r.get("DiemTB") is not None else "-"
        hang_nn_html.append(
            "<tr>"
            f'<td class="text-center">{escape(str(r.get("MaNhaNghi") or ""))}</td>'
            f'<td>{escape(str(r.get("TenNhaNghi") or ""))}</td>'
            f'<td class="text-center">{escape(str(r.get("LoaiHinh") or ""))}</td>'
            f'<td class="text-center">{escape(str(r.get("TenTinh") or ""))}</td>'
            f'<td class="text-center">{int(r.get("SoLuotDanhGia") or 0)}</td>'
            f'<td class="text-center">{escape(diem_nn)}</td>'
            "</tr>"
        )

    bang_tour_fallback = (
        '<tr><td colspan="10" class="text-center">Không có dữ liệu trong kỳ báo cáo</td></tr>'
    )
    bang_nn_fallback = (
        '<tr><td colspan="6" class="text-center">Chưa có đánh giá</td></tr>'
    )

    duong_dan_mau = Path(__file__).resolve().parent / "templates" / "bao_cao_doanh_thu.html"
    mau = Template(duong_dan_mau.read_text(encoding="utf-8"))

    return mau.substitute(
        tu_ngay=escape(tu_ngay_dt.strftime("%d/%m/%Y") if tu_ngay_dt else ""),
        den_ngay=escape(den_ngay_dt.strftime("%d/%m/%Y") if den_ngay_dt else ""),
        nguoi_lap=escape((nguoi_lap or "").strip()),
        noi_nhan=escape((noi_nhan or "").strip() or NOI_NHAN_R2),
        tong_doanh_thu=escape(dinh_dang_tien(tong_dt)),
        so_don=str(int(so_don)),
        so_khach=str(int(so_khach)),
        so_don_huy=str(int(so_don_huy)),
        bang_tour_html="\n".join(hang_tour_html) if hang_tour_html else bang_tour_fallback,
        bang_noi_nghi_html="\n".join(hang_nn_html) if hang_nn_html else bang_nn_fallback,
        ngay_xuat=escape(ngay_xuat_dt.strftime("%d/%m/%Y %H:%M")),
    )



