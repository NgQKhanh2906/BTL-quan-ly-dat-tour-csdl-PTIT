import os
from datetime import datetime

import mysql.connector

CAU_HINH = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": "QuanLyDatTour",
    "charset": "utf8mb4",
    "collation": "utf8mb4_0900_ai_ci",
}

CHE_DO_DEMO = True
HIEN_TAI_DEMO = datetime(2026, 10, 23, 8, 0, 0)

THONG_BAO_CHECK = {
    "chk_LichTrinh_SoChoDaDat": "Lịch trình không còn đủ chỗ cho số khách này",
    "chk_DonHang_NhaNghi": "Số phòng phải từ 1 đến số khách",
    "chk_DonHang_NgayHuy": "Ngày hủy phải sau ngày đặt",
    "chk_DonHang_DiemTour": "Điểm đánh giá phải từ 1 đến 5",
    "chk_DonHang_DiemNhaNghi": "Điểm đánh giá phải từ 1 đến 5",
    "chk_DonHang_NhanXet": "Có nhận xét thì phải chấm điểm",
}

THONG_BAO_MA_LOI = {
    1045: "Sai tài khoản hoặc mật khẩu MySQL (kiểm tra biến môi trường MYSQL_PASSWORD)",
    1062: "Dữ liệu đã tồn tại",
    1452: "Dữ liệu được chọn không còn tồn tại, vui lòng tải lại trang",
    2002: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
    2003: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
}


class KhongCoDongNao(Exception):
    pass


def hien_tai():
    if CHE_DO_DEMO:
        return HIEN_TAI_DEMO
    return datetime.now().replace(microsecond=0)


def ket_noi():
    return mysql.connector.connect(**CAU_HINH)


def doc(sql, tham_so=None):
    cn = ket_noi()
    try:
        cur = cn.cursor(dictionary=True)
        cur.execute(sql, tham_so or {})
        return cur.fetchall()
    finally:
        cn.close()


def ghi(cac_lenh):
    cn = ket_noi()
    try:
        cn.start_transaction()
        cur = cn.cursor()
        for sql, tham_so, phai_co_dong in cac_lenh:
            cur.execute(sql, tham_so)
            if phai_co_dong and cur.rowcount == 0:
                raise KhongCoDongNao()
        cn.commit()
    except Exception:
        cn.rollback()
        raise
    finally:
        cn.close()


def thong_bao_loi(loi):
    if isinstance(loi, KhongCoDongNao):
        return "Đơn đã thay đổi hoặc không còn ở trạng thái phù hợp, vui lòng tải lại trang"
    if isinstance(loi, mysql.connector.Error):
        if loi.errno == 3819:
            for ten, cau in THONG_BAO_CHECK.items():
                if ten in loi.msg:
                    return cau
            return "Dữ liệu không hợp lệ: " + loi.msg
        return THONG_BAO_MA_LOI.get(loi.errno, "Lỗi cơ sở dữ liệu, mã " + str(loi.errno))
    return "Lỗi không xác định: " + str(loi)


def dinh_dang_tien(so):
    if so is None:
        return ""
    return f"{int(so):,}".replace(",", ".") + " đ"


def dinh_dang_ngay(gia_tri):
    if gia_tri is None:
        return ""
    return gia_tri.strftime("%d/%m/%Y %H:%M")