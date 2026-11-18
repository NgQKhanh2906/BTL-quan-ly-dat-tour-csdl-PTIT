import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import mysql.connector

APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import db
import services
from tests.helpers import (
    chay_kiem_tra_rang_buoc,
    khoi_phuc_dh004,
    khoi_phuc_dh010,
    khoi_phuc_f1_mau,
    khoi_phuc_trang_thai_don,
    xoa_don_va_khach_thu_nghiem,
)


class TestDbHelpersAndConnection(unittest.TestCase):
    def test_thong_bao_loi_check_constraints(self):
        expected_checks = {
            "chk_LichTrinh_SoChoDaDat": "Lịch trình không còn đủ chỗ cho số khách này",
            "chk_DonHang_NhaNghi": "Số phòng phải từ 1 đến số khách",
            "chk_DonHang_NgayHuy": "Ngày hủy phải sau ngày đặt",
            "chk_DonHang_DiemTour": "Điểm đánh giá phải từ 1 đến 5",
            "chk_DonHang_DiemNhaNghi": "Điểm đánh giá phải từ 1 đến 5",
            "chk_DonHang_NhanXet": "Có nhận xét thì phải chấm điểm",
            "chk_KhachHang_Email": "Email không đúng định dạng",
            "chk_SDTKhachHang_SoDienThoai": "Số điện thoại phải gồm đúng 10 chữ số bắt đầu bằng 0",
            "chk_DonHang_SoLuongKhach": "Số lượng khách phải lớn hơn 0",
            "chk_DonHang_Huy": "Trạng thái hủy và ngày hủy không hợp lệ",
            "chk_DonHang_LyDoHuy": "Chỉ được nhập lý do hủy khi đơn đã có ngày hủy",
            "chk_DonHang_DanhGia": "Chỉ đơn ở trạng thái Hoàn thành mới được phép đánh giá",
            "chk_DonHang_DanhGiaNhaNghi": "Chỉ được đánh giá nhà nghỉ khi đơn hàng có đặt nhà nghỉ",
            "chk_DonHang_NgayDanhGia": "Ngày đánh giá và điểm đánh giá phải đồng bộ",
            "chk_ChuyenTrungChuyen_Loai": "Loại chuyến trung chuyển chỉ gồm DON_TAI_NHA hoặc VE_NOI_NGHI",
            "chk_ChuyenTrungChuyen_DiaChiDon": "Chuyến đón tại nhà phải có địa chỉ đón",
        }
        for constraint_name, expected_message in expected_checks.items():
            with self.subTest(constraint=constraint_name):
                err = mysql.connector.errors.DatabaseError(
                    errno=3819,
                    msg=f"Check constraint '{constraint_name}' is violated.",
                )
                actual = db.thong_bao_loi(err)
                self.assertFalse(actual.startswith("Dữ liệu không hợp lệ:"))
                self.assertEqual(actual, expected_message)

        err_none_msg = mysql.connector.errors.DatabaseError(errno=3819, msg="placeholder")
        err_none_msg.msg = None
        self.assertEqual(db.thong_bao_loi(err_none_msg), "Dữ liệu không hợp lệ: ")

    def test_thong_bao_loi_mysql_errnos(self):
        expected_errnos = {
            1045: "Sai tài khoản hoặc mật khẩu MySQL (kiểm tra biến môi trường MYSQL_PASSWORD)",
            1049: "Cơ sở dữ liệu QuanLyDatTour chưa được tạo trên MySQL",
            1062: "Dữ liệu đã tồn tại",
            1406: "Dữ liệu nhập vào vượt quá độ dài tối đa cho phép",
            1451: "Không thể xóa hoặc sửa bản ghi đang được dữ liệu khác tham chiếu",
            1452: "Dữ liệu được chọn không còn tồn tại, vui lòng tải lại trang",
            2002: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
            2003: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
        }
        for errno, expected_message in expected_errnos.items():
            with self.subTest(errno=errno):
                err = mysql.connector.errors.DatabaseError(errno=errno, msg="test error")
                actual = db.thong_bao_loi(err)
                self.assertFalse(actual.startswith("Lỗi cơ sở dữ liệu, mã"))
                self.assertEqual(actual, expected_message)

    def test_dinh_dang_ngay_handles_datetime_string_and_none(self):
        self.assertEqual(db.dinh_dang_ngay(None), "")
        self.assertEqual(db.dinh_dang_ngay(datetime(2026, 10, 23, 8, 0)), "23/10/2026 08:00")
        self.assertEqual(db.dinh_dang_ngay("2026-10-23 08:00:00"), "23/10/2026 08:00")
        self.assertEqual(db.dinh_dang_ngay(" 2026-10-23T08:00:00 "), "23/10/2026 08:00")
        self.assertEqual(db.dinh_dang_ngay("khong-hop-le"), "khong-hop-le")

    def test_dinh_dang_tien(self):
        self.assertEqual(db.dinh_dang_tien(None), "")
        self.assertEqual(db.dinh_dang_tien(32020000), "32.020.000 đ")
        self.assertEqual(db.dinh_dang_tien(Decimal("6250000")), "6.250.000 đ")

    def test_db_live_connection_and_rb22_to_rb32_clean(self):
        tables = db.doc(
            """
            SELECT TABLE_NAME
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = 'QuanLyDatTour' AND TABLE_TYPE = 'BASE TABLE'
            """
        )
        self.assertEqual(len(tables), 12)
        self.assertEqual(chay_kiem_tra_rang_buoc(), [])


class TestF3DanhGiaServices(unittest.TestCase):
    def test_f3_luu_danh_gia_thanh_cong_va_chan_danh_gia_lan_2(self):
        khoi_phuc_dh004()
        try:
            ds_kh = services.lay_ds_khach_hang()
            self.assertEqual(len(ds_kh), 8)
            self.assertIn("DiaChi", ds_kh[0])

            ds_kh004 = services.lay_don_cho_danh_gia("KH004")
            self.assertEqual([d["MaDonHang"] for d in ds_kh004], ["DH004"])
            self.assertEqual(services.lay_don_cho_danh_gia("KH001"), [])

            s1_sql = """
                SELECT ROUND(AVG(d.DiemTour), 1) AS DiemTB, COUNT(d.DiemTour) AS SoLuot
                FROM DonHang d
                JOIN LichTrinh l ON l.MaLichTrinh = d.MaLichTrinh
                WHERE l.MaTour = %s AND d.DiemTour IS NOT NULL
            """
            truoc = db.doc(s1_sql, ("T02",))[0]
            self.assertEqual(float(truoc["DiemTB"]), 5.0)
            self.assertEqual(truoc["SoLuot"], 1)

            services.luu_danh_gia(
                "DH004",
                4,
                "Lịch trình hợp lý.",
                4,
                "Phòng sạch.",
                db.hien_tai(),
            )

            self.assertEqual(services.lay_don_cho_danh_gia("KH004"), [])
            sau = db.doc(s1_sql, ("T02",))[0]
            self.assertEqual(float(sau["DiemTB"]), 4.5)
            self.assertEqual(sau["SoLuot"], 2)

            dh004 = db.doc(
                """
                SELECT DiemTour, NhanXetTour, DiemNhaNghi, NhanXetNhaNghi, NgayDanhGia
                FROM DonHang
                WHERE MaDonHang = %s
                """,
                ("DH004",),
            )[0]
            self.assertEqual(dh004["DiemTour"], 4)
            self.assertEqual(dh004["NhanXetTour"], "Lịch trình hợp lý.")
            self.assertEqual(dh004["DiemNhaNghi"], 4)
            self.assertEqual(dh004["NhanXetNhaNghi"], "Phòng sạch.")
            self.assertEqual(dh004["NgayDanhGia"], db.hien_tai())

            with self.assertRaises(db.KhongCoDongNao):
                services.luu_danh_gia(
                    "DH004",
                    5,
                    "Gửi đánh giá lần 2.",
                    5,
                    "Phòng đẹp.",
                    db.hien_tai(),
                )
        finally:
            khoi_phuc_dh004()

    def test_f3_kiem_tra_danh_gia_chan_nhan_xet_khong_diem(self):
        loi, nx_tour, diem_nn, nx_nn = services.kiem_tra_danh_gia(
            5, "   ", True, None, "Phòng sạch"
        )
        self.assertTrue(loi)
        self.assertIsNone(nx_tour)
        self.assertIsNone(diem_nn)
        self.assertEqual(nx_nn, "Phòng sạch")

        loi_ok, nx_tour_ok, diem_nn_ok, nx_nn_ok = services.kiem_tra_danh_gia(
            4, "   ", True, 4, "   "
        )
        self.assertEqual(loi_ok, [])
        self.assertIsNone(nx_tour_ok)
        self.assertEqual(diem_nn_ok, 4)
        self.assertIsNone(nx_nn_ok)

        loi_khong_nn, nx_tour_khong_nn, diem_nn_khong_nn, nx_nn_khong_nn = services.kiem_tra_danh_gia(
            5, "  Tour rất tốt  ", False, None, "   "
        )
        self.assertEqual(loi_khong_nn, [])
        self.assertEqual(nx_tour_khong_nn, "Tour rất tốt")
        self.assertIsNone(diem_nn_khong_nn)
        self.assertIsNone(nx_nn_khong_nn)


class TestF2QuanLyDonServices(unittest.TestCase):
    def test_f2_kiem_tra_huy_don_chan_rb23_va_thieu_xac_nhan(self):
        ngay_dat = datetime(2026, 10, 12, 9, 30, 0)
        ngay_xuat_phat = datetime(2026, 11, 14, 6, 30, 0)

        # RB23: Huy dung bang hoac sau thoi diem khoi hanh
        for moc_huy in (
            datetime(2026, 11, 14, 6, 30, 0),
            datetime(2026, 11, 15, 8, 0, 0),
        ):
            with self.subTest(moc_huy=moc_huy):
                loi = services.kiem_tra_huy_don(
                    ngay_dat,
                    ngay_xuat_phat,
                    moc_huy,
                    "Khách đổi kế hoạch",
                    True,
                )
                self.assertTrue(
                    any("14/11/2026 06:30" in msg and "khởi hành" in msg for msg in loi),
                    loi,
                )

        # Ngay huy nho hon ngay dat -> dinh_dang_ngay dong nhat 2 ve
        loi_truoc_dat = services.kiem_tra_huy_don(
            ngay_dat,
            ngay_xuat_phat,
            datetime(2026, 10, 12, 9, 0, 0),
            "Khách đổi kế hoạch",
            True,
        )
        self.assertTrue(
            any(
                "12/10/2026 09:00" in msg and "12/10/2026 09:30" in msg
                for msg in loi_truoc_dat
            ),
            loi_truoc_dat,
        )

        # Ly do huy rong / khoang trang
        loi_ly_do = services.kiem_tra_huy_don(
            ngay_dat,
            ngay_xuat_phat,
            datetime(2026, 10, 23, 8, 0, 0),
            "   ",
            True,
        )
        self.assertTrue(
            any("Lý do hủy tour" in msg for msg in loi_ly_do),
            loi_ly_do,
        )

        # Chua xac nhan khach dong y muc phat
        loi_xac_nhan = services.kiem_tra_huy_don(
            ngay_dat,
            ngay_xuat_phat,
            datetime(2026, 10, 23, 8, 0, 0),
            "Khách bận việc",
            False,
        )
        self.assertTrue(
            any("đồng ý mức phạt" in msg for msg in loi_xac_nhan),
            loi_xac_nhan,
        )

        # Hop le hoan toan
        loi_ok = services.kiem_tra_huy_don(
            ngay_dat,
            ngay_xuat_phat,
            datetime(2026, 10, 23, 8, 0, 0),
            "Khách bận việc",
            True,
        )
        self.assertEqual(loi_ok, [])

    def test_f2_huy_don_dh010_hoan_cho_xoa_trung_chuyen_va_chan_huy_lap(self):
        khoi_phuc_dh010()
        try:
            ds_mo = services.lay_don_dang_mo()
            self.assertEqual(
                [d["MaDonHang"] for d in ds_mo],
                ["DH007", "DH010", "DH012", "DH013", "DH014"],
            )

            ct = services.lay_chi_tiet_don_f2("DH010")
            self.assertIsNotNone(ct)
            self.assertEqual(ct["MaLichTrinh"], "LT05")
            self.assertEqual(int(ct["SoLuongKhach"]), 4)
            self.assertEqual(int(ct["TongTien"]), 16000000)

            ngay_huy = datetime(2026, 10, 23, 8, 0, 0)
            xem_truoc = services.tinh_xem_truoc_phat_huy("DH010", ngay_huy)
            self.assertIsNotNone(xem_truoc)
            self.assertEqual(int(xem_truoc["SoNgayTruocKhoiHanh"]), 22)
            self.assertEqual(int(xem_truoc["TyLePhat"]), 10)
            self.assertEqual(int(xem_truoc["TienPhat"]), 1600000)
            self.assertEqual(int(xem_truoc["TienHoan"]), 14400000)
            self.assertEqual(db.dinh_dang_tien(xem_truoc["TienPhat"]), "1.600.000 đ")
            self.assertEqual(db.dinh_dang_tien(xem_truoc["TienHoan"]), "14.400.000 đ")

            services.huy_don("DH010", ngay_huy, "  Khách bận công tác đột xuất  ")

            dh010 = db.doc(
                "SELECT MaTrangThai, NgayHuy, LyDoHuy FROM DonHang WHERE MaDonHang = %s",
                ("DH010",),
            )[0]
            self.assertEqual(dh010["MaTrangThai"], "HUY")
            self.assertEqual(dh010["NgayHuy"], ngay_huy)
            self.assertEqual(dh010["LyDoHuy"], "Khách bận công tác đột xuất")

            lt05 = db.doc(
                "SELECT SoChoDaDat FROM LichTrinh WHERE MaLichTrinh = %s",
                ("LT05",),
            )[0]
            self.assertEqual(int(lt05["SoChoDaDat"]), 0)

            ctc = db.doc(
                "SELECT COUNT(*) AS SoDong FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
                ("DH010",),
            )[0]
            self.assertEqual(int(ctc["SoDong"]), 0)

            self.assertEqual(chay_kiem_tra_rang_buoc(), [])

            with self.assertRaises(db.KhongCoDongNao):
                services.huy_don("DH010", ngay_huy, "Hủy lần 2")
        finally:
            khoi_phuc_dh010()

    def test_f2_chuyen_trang_thai_dh013_va_dh012(self):
        khoi_phuc_trang_thai_don("DH013", "DAT")
        khoi_phuc_trang_thai_don("DH012", "THANHTOAN")
        try:
            moc_hien_tai = datetime(2026, 10, 23, 8, 0, 0)

            ds_dich_dh013 = services.lay_trang_thai_dich_f2("DH013", moc_hien_tai)
            self.assertEqual(
                [r["MaTrangThai"] for r in ds_dich_dh013],
                ["THANHTOAN", "HUY"],
            )

            services.chuyen_trang_thai_don("DH013", "THANHTOAN", moc_hien_tai)
            dh013 = db.doc(
                "SELECT MaTrangThai FROM DonHang WHERE MaDonHang = %s",
                ("DH013",),
            )[0]
            self.assertEqual(dh013["MaTrangThai"], "THANHTOAN")

            ds_dich_dh012 = services.lay_trang_thai_dich_f2("DH012", moc_hien_tai)
            self.assertEqual(
                [r["MaTrangThai"] for r in ds_dich_dh012],
                ["HUY"],
            )

            with self.assertRaises(db.KhongCoDongNao):
                services.chuyen_trang_thai_don("DH012", "HOANTHANH", moc_hien_tai)

            dh012 = db.doc(
                "SELECT MaTrangThai FROM DonHang WHERE MaDonHang = %s",
                ("DH012",),
            )[0]
            self.assertEqual(dh012["MaTrangThai"], "THANHTOAN")
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            khoi_phuc_trang_thai_don("DH013", "DAT")
            khoi_phuc_trang_thai_don("DH012", "THANHTOAN")


class TestF1DatTourServices(unittest.TestCase):
    def test_f1_dat_don_dh015_kh006_lt10_va_kiem_tra_rang_buoc(self):
        khoi_phuc_f1_mau()
        try:
            ds_kh = services.lay_ds_khach_hang_f1()
            self.assertEqual(len(ds_kh), 8)
            kh006 = next(r for r in ds_kh if r["MaKH"] == "KH006")
            self.assertEqual(kh006["HienThi"], "KH006 - Vũ Thị Hà")
            self.assertEqual(kh006["DiaChi"], "3 Hùng Vương, Lào Cai")
            self.assertIn("0398765432", kh006["SoDienThoai"])

            moc = datetime(2026, 10, 23, 8, 0, 0)
            ds_lt = services.lay_lich_trinh_con_cho(moc)
            ma_lts = [r["MaLichTrinh"] for r in ds_lt]
            self.assertEqual(len(ma_lts), 9)
            self.assertIn("LT06", ma_lts)
            self.assertIn("LT10", ma_lts)

            lt06 = next(r for r in ds_lt if r["MaLichTrinh"] == "LT06")
            self.assertEqual(int(lt06["SoDem"]), 0)

            lt10 = next(r for r in ds_lt if r["MaLichTrinh"] == "LT10")
            self.assertEqual(int(lt10["SoDem"]), 3)
            self.assertEqual(int(lt10["SoChoConLai"]), 20)
            self.assertEqual(lt10["MaTinhDen"], "TQ")

            ds_nn = services.lay_noi_nghi_theo_tinh("TQ")
            self.assertEqual([r["MaNhaNghi"] for r in ds_nn], ["NN08"])
            nn08 = ds_nn[0]

            tien_tour, tien_phong, tong_tien = services.tinh_du_toan_f1(
                so_khach=5,
                gia_co_ban=int(lt10["GiaCoBan"]),
                so_phong=2,
                gia_phong_moi_dem=int(nn08["GiaPhongMoiDem"]),
                so_dem=int(lt10["SoDem"]),
                co_nha_nghi=True,
            )
            self.assertEqual((tien_tour, tien_phong, tong_tien), (29500000, 2520000, 32020000))
            self.assertEqual(services.tinh_du_toan_f1(2, 900000, 1, 400000, 0, False), (1800000, 0, 1800000))

            dt_don = datetime(2026, 11, 26, 15, 0, 0)
            dt_ve = datetime(2026, 11, 27, 10, 0, 0)
            loi = services.kiem_tra_dat_tour(
                la_khach_moi=False,
                ma_kh="KH006",
                ho_ten="",
                so_dien_thoai="",
                email="",
                dia_chi="",
                so_khach=5,
                so_cho_con_lai=int(lt10["SoChoConLai"]),
                so_dem=int(lt10["SoDem"]),
                co_nha_nghi=True,
                so_phong=2,
                co_xe_don=True,
                dia_chi_don="3 Hùng Vương, Lào Cai",
                dt_don=dt_don,
                co_xe_ve=True,
                dt_ve=dt_ve,
                thoi_diem_hien_tai=moc,
                ngay_xuat_phat=lt10["NgayXuatPhat"],
                ngay_ket_thuc=lt10["NgayKetThuc"],
            )
            self.assertEqual(loi, [])

            ma_don_moi = services.luu_dat_tour(
                {
                    "LaKhachMoi": False,
                    "MaKH": "KH006",
                    "MaLichTrinh": "LT10",
                    "SoKhach": 5,
                    "MaNhaNghi": "NN08",
                    "SoPhong": 2,
                    "DiaChiDon": "3 Hùng Vương, Lào Cai",
                    "GioDon": dt_don,
                    "GioVeNoiNghi": dt_ve,
                    "NgayDat": moc,
                }
            )
            self.assertEqual(ma_don_moi, "DH015")

            v_don = db.doc(
                """
                SELECT MaDonHang, MaKH, MaLichTrinh, SoLuongKhach, SoPhong,
                       TienTour, TienPhong, TongTien, MaTrangThai
                FROM v_DonHang_ChiTiet
                WHERE MaDonHang = %s
                """,
                ("DH015",),
            )[0]
            self.assertEqual(v_don["MaKH"], "KH006")
            self.assertEqual(v_don["MaLichTrinh"], "LT10")
            self.assertEqual(int(v_don["SoLuongKhach"]), 5)
            self.assertEqual(int(v_don["SoPhong"]), 2)
            self.assertEqual(int(v_don["TongTien"]), 32020000)
            self.assertEqual(v_don["MaTrangThai"], "DAT")

            lt10_sau = db.doc(
                "SELECT SoChoToiDa - SoChoDaDat AS ConLai, SoChoDaDat FROM LichTrinh WHERE MaLichTrinh = %s",
                ("LT10",),
            )[0]
            self.assertEqual(int(lt10_sau["ConLai"]), 15)
            self.assertEqual(int(lt10_sau["SoChoDaDat"]), 5)

            ds_chuyen = db.doc(
                """
                SELECT LoaiChuyen, DiaChiDon, ThoiGianDon
                FROM ChuyenTrungChuyen
                WHERE MaDonHang = %s
                ORDER BY LoaiChuyen
                """,
                ("DH015",),
            )
            self.assertEqual(len(ds_chuyen), 2)
            self.assertEqual(ds_chuyen[0]["LoaiChuyen"], "DON_TAI_NHA")
            self.assertEqual(ds_chuyen[0]["DiaChiDon"], "3 Hùng Vương, Lào Cai")
            self.assertEqual(ds_chuyen[0]["ThoiGianDon"], dt_don)
            self.assertEqual(ds_chuyen[1]["LoaiChuyen"], "VE_NOI_NGHI")
            self.assertIsNone(ds_chuyen[1]["DiaChiDon"])
            self.assertEqual(ds_chuyen[1]["ThoiGianDon"], dt_ve)

            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            xoa_don_va_khach_thu_nghiem(["DH015"], [], {"LT10": 0})
            khoi_phuc_f1_mau()

    def test_f1_khach_hang_moi_va_chan_trung_email_sdt(self):
        khoi_phuc_f1_mau()
        try:
            # Trung Email (khong phan biet hoa/thuong)
            trung_email = services.kiem_tra_trung_khach_hang("AN.NGUYEN@GMAIL.COM", "0999888777")
            self.assertIsNotNone(trung_email)
            self.assertEqual(trung_email["MaKH"], "KH001")

            # Trung SDT cua khach khac
            trung_sdt = services.kiem_tra_trung_khach_hang("khac.hoan.toan@gmail.com", "0398765432")
            self.assertIsNotNone(trung_sdt)
            self.assertEqual(trung_sdt["MaKH"], "KH006")

            # Khach moi hoan toan (ke ca trung HoTen/DiaChi voi KH001 nhung khac Email & SDT -> khong trung)
            self.assertIsNone(
                services.kiem_tra_trung_khach_hang("moi.hoantoan@gmail.com", "0911223344")
            )

            moc = datetime(2026, 10, 23, 8, 0, 0)
            loi_moi = services.kiem_tra_dat_tour(
                la_khach_moi=True,
                ma_kh=None,
                ho_ten="Nguyễn Minh Tuấn",
                so_dien_thoai="0911223344",
                email="moi.hoantoan@gmail.com",
                dia_chi="15 Phố Huế, Hà Nội",
                so_khach=2,
                so_cho_con_lai=20,
                so_dem=0,
                co_nha_nghi=False,
                so_phong=0,
                co_xe_don=False,
                dia_chi_don=None,
                dt_don=None,
                co_xe_ve=False,
                dt_ve=None,
                thoi_diem_hien_tai=moc,
                ngay_xuat_phat=datetime(2026, 11, 21, 7, 30, 0),
                ngay_ket_thuc=datetime(2026, 11, 21, 19, 0, 0),
            )
            self.assertEqual(loi_moi, [])

            ma_don_moi = services.luu_dat_tour(
                {
                    "LaKhachMoi": True,
                    "HoTen": "Nguyễn Minh Tuấn",
                    "SoDienThoai": "0911223344",
                    "Email": "moi.hoantoan@gmail.com",
                    "DiaChi": "15 Phố Huế, Hà Nội",
                    "MaLichTrinh": "LT06",
                    "SoKhach": 2,
                    "MaNhaNghi": None,
                    "SoPhong": 0,
                    "NgayDat": moc,
                }
            )
            self.assertEqual(ma_don_moi, "DH015")

            kh_moi = db.doc(
                "SELECT MaKH, HoTen, Email, DiaChi FROM KhachHang WHERE MaKH = %s",
                ("KH009",),
            )
            self.assertEqual(len(kh_moi), 1)
            self.assertEqual(kh_moi[0]["HoTen"], "Nguyễn Minh Tuấn")
            self.assertEqual(kh_moi[0]["Email"], "moi.hoantoan@gmail.com")

            sdt_moi = db.doc(
                "SELECT SoDienThoai FROM SDT_KhachHang WHERE MaKH = %s",
                ("KH009",),
            )
            self.assertEqual([r["SoDienThoai"] for r in sdt_moi], ["0911223344"])

            dh_moi = db.doc(
                "SELECT MaKH, MaLichTrinh, SoLuongKhach, SoPhong, MaNhaNghi FROM DonHang WHERE MaDonHang = %s",
                ("DH015",),
            )[0]
            self.assertEqual(dh_moi["MaKH"], "KH009")
            self.assertEqual(dh_moi["MaLichTrinh"], "LT06")
            self.assertIsNone(dh_moi["MaNhaNghi"])
            self.assertEqual(int(dh_moi["SoPhong"]), 0)
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            xoa_don_va_khach_thu_nghiem(["DH015"], ["KH009"], {"LT06": 3})
            khoi_phuc_f1_mau()

    def test_f1_chan_loi_phong_dia_chi_gio_don_va_layer2_overbooking(self):
        khoi_phuc_f1_mau()
        try:
            moc = datetime(2026, 10, 23, 8, 0, 0)
            xp = datetime(2026, 11, 26, 20, 0, 0)
            kt = datetime(2026, 11, 29, 20, 0, 0)

            # 2 khach 3 phong
            loi_phong = services.kiem_tra_dat_tour(
                la_khach_moi=False,
                ma_kh="KH006",
                ho_ten="",
                so_dien_thoai="",
                email="",
                dia_chi="",
                so_khach=2,
                so_cho_con_lai=20,
                so_dem=3,
                co_nha_nghi=True,
                so_phong=3,
                co_xe_don=False,
                dia_chi_don=None,
                dt_don=None,
                co_xe_ve=False,
                dt_ve=None,
                thoi_diem_hien_tai=moc,
                ngay_xuat_phat=xp,
                ngay_ket_thuc=kt,
            )
            self.assertTrue(
                any("Số phòng phải từ 1 đến số khách" in msg for msg in loi_phong),
                loi_phong,
            )

            # Thieu dia chi don + gio don >= gio xuat phat
            loi_xe_don = services.kiem_tra_dat_tour(
                la_khach_moi=False,
                ma_kh="KH006",
                ho_ten="",
                so_dien_thoai="",
                email="",
                dia_chi="",
                so_khach=2,
                so_cho_con_lai=20,
                so_dem=3,
                co_nha_nghi=False,
                so_phong=0,
                co_xe_don=True,
                dia_chi_don="   ",
                dt_don=xp,
                co_xe_ve=False,
                dt_ve=None,
                thoi_diem_hien_tai=moc,
                ngay_xuat_phat=xp,
                ngay_ket_thuc=kt,
            )
            self.assertTrue(any("địa chỉ đón" in msg.lower() for msg in loi_xe_don), loi_xe_don)
            self.assertTrue(any("giờ đón" in msg.lower() for msg in loi_xe_don), loi_xe_don)

            # Tour 0 dem nhung co noi nghi + xe ve noi nghi
            loi_0_dem = services.kiem_tra_dat_tour(
                la_khach_moi=False,
                ma_kh="KH006",
                ho_ten="",
                so_dien_thoai="",
                email="",
                dia_chi="",
                so_khach=2,
                so_cho_con_lai=27,
                so_dem=0,
                co_nha_nghi=True,
                so_phong=1,
                co_xe_don=False,
                dia_chi_don=None,
                dt_don=None,
                co_xe_ve=True,
                dt_ve=datetime(2026, 11, 21, 10, 0, 0),
                thoi_diem_hien_tai=moc,
                ngay_xuat_phat=datetime(2026, 11, 21, 7, 30, 0),
                ngay_ket_thuc=datetime(2026, 11, 21, 19, 0, 0),
            )
            self.assertTrue(any("0 đêm" in msg for msg in loi_0_dem), loi_0_dem)

            # Layer 2 MySQL CHECK: LT08 chi con 10 cho (ToiDa=12, DaDat=2), goi truc tiep 11 khach
            with self.assertRaises(mysql.connector.Error) as ctx:
                services.luu_dat_tour(
                    {
                        "LaKhachMoi": False,
                        "MaKH": "KH006",
                        "MaLichTrinh": "LT08",
                        "SoKhach": 11,
                        "MaNhaNghi": None,
                        "SoPhong": 0,
                        "NgayDat": moc,
                    }
                )
            self.assertEqual(
                db.thong_bao_loi(ctx.exception),
                "Lịch trình không còn đủ chỗ cho số khách này",
            )

            # ROLLBACK sach: khong co don DH015 va LT08 van la 2 cho da dat
            self.assertEqual(
                db.doc("SELECT MaDonHang FROM DonHang WHERE MaDonHang = %s", ("DH015",)),
                [],
            )
            lt08 = db.doc("SELECT SoChoDaDat FROM LichTrinh WHERE MaLichTrinh = %s", ("LT08",))[0]
            self.assertEqual(int(lt08["SoChoDaDat"]), 2)
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            khoi_phuc_f1_mau()


class TestS1TimKiemServices(unittest.TestCase):
    def test_s1_cac_ca_kiem_thu_chuan(self):
        ds_tinh = services.lay_ds_tinh_thanh()
        self.assertEqual(len(ds_tinh), 15)
        self.assertTrue(
            any(t["MaTinh"] == "LC" and t["TenTinh"] == "Lào Cai" for t in ds_tinh),
            ds_tinh,
        )

        ngay_moc = date(2026, 10, 23)

        # Ca 1: Khong loc -> 9 lich trinh (LT04..LT12)
        kq_tat_ca = services.tim_kiem_lich_trinh(tu_ngay=ngay_moc)
        self.assertEqual(len(kq_tat_ca), 9)
        self.assertEqual(
            {r["MaLichTrinh"] for r in kq_tat_ca},
            {f"LT{i:02d}" for i in range(4, 13)},
        )

        # Ca 2: gia_tu=10_000_000 -> dung 3 ma ["LT08", "LT09", "LT12"]
        kq_cao_cap = services.tim_kiem_lich_trinh(
            gia_tu=10_000_000,
            tu_ngay=ngay_moc,
        )
        self.assertEqual(
            [r["MaLichTrinh"] for r in kq_cao_cap],
            ["LT08", "LT09", "LT12"],
        )

        # Ca 3: tu_khoa="ha long", so_khach=2 -> dung 3 ma ["LT04", "LT08", "LT12"]
        kq_ha_long = services.tim_kiem_lich_trinh(
            tu_khoa="ha long",
            tu_ngay=ngay_moc,
            so_khach=2,
        )
        self.assertEqual(
            [r["MaLichTrinh"] for r in kq_ha_long],
            ["LT04", "LT08", "LT12"],
        )

        # Ca 4: ma_tinh_den="LC", gia_den=4_000_000, den_ngay=2026-12-31, so_khach=4, diem_toi_thieu=4.5 -> ["LT05"] (5.0)
        kq_sapa = services.tim_kiem_lich_trinh(
            ma_tinh_den="LC",
            gia_den=4_000_000,
            tu_ngay=ngay_moc,
            den_ngay=date(2026, 12, 31),
            so_khach=4,
            diem_toi_thieu=4.5,
        )
        self.assertEqual([r["MaLichTrinh"] for r in kq_sapa], ["LT05"])
        self.assertEqual(float(kq_sapa[0]["DiemTB"]), 5.0)

        # Ca 5: gia_tu=20_000_000 -> []
        kq_rong_gia = services.tim_kiem_lich_trinh(
            gia_tu=20_000_000,
            tu_ngay=ngay_moc,
        )
        self.assertEqual(kq_rong_gia, [])

        # Ca 6: tu_khoa="du thuyen", den_ngay=2026-11-30, so_khach=11 -> []
        kq_rong_cho = services.tim_kiem_lich_trinh(
            tu_khoa="du thuyen",
            tu_ngay=ngay_moc,
            den_ngay=date(2026, 11, 30),
            so_khach=11,
        )
        self.assertEqual(kq_rong_cho, [])


def _tim_trinh_duyet_headless() -> str | None:
    cac_ung_vien = [
        shutil.which("chrome"),
        shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for duong_dan in cac_ung_vien:
        if duong_dan and os.path.exists(duong_dan):
            return duong_dan
    return None


def _xuat_pdf_a4_bytes(test_case: unittest.TestCase, html_noi_dung: str) -> bytes:
    trinh_duyet = _tim_trinh_duyet_headless()
    if not trinh_duyet:
        test_case.fail("Không tìm thấy chrome.exe hoặc msedge.exe để kiểm chứng xuất PDF A4.")

    with tempfile.TemporaryDirectory() as thu_muc_tam:
        td = Path(thu_muc_tam)
        html_path = td / "bieu_mau_in.html"
        pdf_path = td / "bieu_mau_in.pdf"
        profile_dir = td / "profile"
        profile_dir.mkdir()
        html_path.write_text(html_noi_dung, encoding="utf-8")

        ket_qua = subprocess.run(
            [
                trinh_duyet,
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile_dir}",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        test_case.assertEqual(
            ket_qua.returncode,
            0,
            f"Trình duyệt headless thất bại (rc={ket_qua.returncode}): {ket_qua.stderr}",
        )
        test_case.assertTrue(pdf_path.exists(), "Không tạo được file PDF đầu ra.")
        return pdf_path.read_bytes()


class TestR1PhieuXacNhanServices(unittest.TestCase):
    def _xuat_pdf_a4_bytes(self, html_noi_dung: str) -> bytes:
        return _xuat_pdf_a4_bytes(self, html_noi_dung)

    def test_r1_dh007_dh008_va_dh013_chinh_xac_va_chong_xss(self):
        ds_don = services.lay_ds_don_r1()
        self.assertEqual(len(ds_don), 14)
        self.assertEqual(
            [d["MaDonHang"] for d in ds_don],
            [f"DH{i:03d}" for i in range(1, 15)],
        )

        ngay_in = datetime(2026, 10, 23, 8, 0, 0)

        # DH007: Thanh toan day du, co nha nghi, 2 SDT, 2 chuyen trung chuyen, co the Visa
        ct_007 = services.lay_chi_tiet_don_r1("DH007")
        self.assertIsNotNone(ct_007)
        sdt_007 = services.lay_sdt_khach_r1("DH007")
        self.assertEqual(sdt_007, "0912345678, 0987654321")
        ctc_007 = services.lay_lich_trung_chuyen_r1("DH007")
        self.assertEqual(len(ctc_007), 2)

        html_007 = services.tao_html_phieu_xac_nhan(
            ct_007, sdt_007, ctc_007, "Nguyễn Quốc Khánh", ngay_in
        )
        self.assertIn("6.250.000 đ", html_007)
        self.assertIn("0912345678, 0987654321", html_007)
        self.assertIn("Thẻ Visa (**** **** **** 1111)", html_007)
        self.assertIn("Nhà hát Lớn, 1 Tràng Tiền, Hà Nội", html_007)
        self.assertIn("Thời gian đón", html_007)
        self.assertIn("24/10/2026 06:00", html_007)
        self.assertIn("24/10/2026 11:30", html_007)
        self.assertIn("2 ngày 1 đêm", html_007)
        self.assertIn("Đơn hàng đang hoạt động bình thường", html_007)
        self.assertNotIn("{{", html_007)
        self.assertNotIn("None", html_007)

        # DH008: Don huy (MaTrangThai = HUY, TyLePhat = 30%), phat 2.610.000 d, hoan 6.090.000 d
        ct_008 = services.lay_chi_tiet_don_r1("DH008")
        self.assertIsNotNone(ct_008)
        self.assertEqual(ct_008["MaTrangThai"], "HUY")
        sdt_008 = services.lay_sdt_khach_r1("DH008")
        ctc_008 = services.lay_lich_trung_chuyen_r1("DH008")
        html_008 = services.tao_html_phieu_xac_nhan(
            ct_008, sdt_008, ctc_008, "Nguyễn Quốc Khánh", ngay_in
        )
        self.assertIn("2.610.000 đ (30%)", html_008)
        self.assertIn("6.090.000 đ", html_008)
        self.assertIn("Trùng lịch công tác", html_008)
        self.assertNotIn("Thẻ Tiền mặt", html_008)
        self.assertNotIn("None", html_008)

        # DH008 voi LyDoHuy NULL -> hien "Không ghi nhận", khong bao gio in chu "None"
        ct_008_null = dict(ct_008)
        ct_008_null["LyDoHuy"] = None
        html_008_null = services.tao_html_phieu_xac_nhan(
            ct_008_null, sdt_008, ctc_008, "Nguyễn Quốc Khánh", ngay_in
        )
        self.assertIn("Không ghi nhận", html_008_null)
        self.assertNotIn("None", html_008_null)

        # DH013: Tour trong ngay (0 dem), khong nha nghi, co the Visa
        ct_013 = services.lay_chi_tiet_don_r1("DH013")
        self.assertIsNotNone(ct_013)
        html_013 = services.tao_html_phieu_xac_nhan(
            ct_013,
            services.lay_sdt_khach_r1("DH013"),
            services.lay_lich_trung_chuyen_r1("DH013"),
            "Nguyễn Quốc Khánh",
            ngay_in,
        )
        self.assertIn("1 ngày (trong ngày)", html_013)
        self.assertIn("Không sử dụng (0 phòng)", html_013)
        self.assertIn("Thẻ Visa (**** **** **** 0002)", html_013)
        self.assertIn("2.700.000 đ", html_013)

        # DH003: Khach hang khong luu the (SoID = NULL) -> khong in "Thẻ Tiền mặt..."
        ct_003 = services.lay_chi_tiet_don_r1("DH003")
        self.assertIsNotNone(ct_003)
        html_003 = services.tao_html_phieu_xac_nhan(
            ct_003,
            services.lay_sdt_khach_r1("DH003"),
            services.lay_lich_trung_chuyen_r1("DH003"),
            "Nguyễn Quốc Khánh",
            ngay_in,
        )
        self.assertIn("Tiền mặt / Chuyển khoản (Chưa lưu thẻ)", html_003)
        self.assertNotIn("Thẻ Tiền mặt", html_003)

        # Chong XSS & thay the placeholder day chuyen
        ct_xss = dict(ct_007)
        ct_xss["DiemTapTrung"] = "<script>alert(1)</script> {{MA_DON_HANG}}"
        html_xss = services.tao_html_phieu_xac_nhan(
            ct_xss,
            sdt_007,
            ctc_007,
            "<b>An</b> {{TONG_TIEN}}",
            ngay_in,
        )
        self.assertIn("&lt;b&gt;An&lt;/b&gt; {{TONG_TIEN}}", html_xss)
        self.assertNotIn("<b>An</b>", html_xss)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt; {{MA_DON_HANG}}", html_xss)
        self.assertNotIn("<script>alert(1)</script>", html_xss)

        # Ma don khong ton tai
        self.assertIsNone(services.lay_chi_tiet_don_r1("DH999"))
        self.assertEqual(services.lay_sdt_khach_r1("DH999"), "Chưa cập nhật")

    def test_r1_pdf_a4_mot_trang_cho_dh007_va_dh008(self):
        ngay_in = datetime(2026, 10, 23, 8, 0, 0)
        for ma_don in ("DH007", "DH008"):
            with self.subTest(ma_don=ma_don):
                ct = services.lay_chi_tiet_don_r1(ma_don)
                self.assertIsNotNone(ct)
                html_noi_dung = services.tao_html_phieu_xac_nhan(
                    ct,
                    services.lay_sdt_khach_r1(ma_don),
                    services.lay_lich_trung_chuyen_r1(ma_don),
                    "Nguyễn Quốc Khánh",
                    ngay_in,
                )
                pdf_bytes = self._xuat_pdf_a4_bytes(html_noi_dung)
                so_trang = len(re.findall(rb"/Type\s*/Page\b", pdf_bytes))
                self.assertEqual(
                    so_trang,
                    1,
                    f"Phiếu {ma_don} khi xuất PDF A4 phải đúng 1 trang nhưng đang là {so_trang} trang.",
                )


class TestR2BaoCaoDoanhThuServices(unittest.TestCase):
    def test_r2_so_lieu_ky_mac_dinh_va_escape_html_tu_cwd_goc(self):
        cwd_cu = os.getcwd()
        os.chdir(ROOT_DIR)
        try:
            tu_ngay = date(2026, 9, 1)
            den_ngay = date(2026, 12, 31)
            ds_tour = services.lay_doanh_thu_tour_r2(tu_ngay, den_ngay)
            ds_noi_nghi = services.lay_xep_hang_noi_nghi_r2(tu_ngay, den_ngay)

            dong_tong = next((r for r in ds_tour if r["MaTour"] == "TỔNG CỘNG"), None)
            self.assertIsNotNone(dong_tong)
            self.assertEqual(int(dong_tong["TongDoanhThu"]), 79110000)
            self.assertEqual(int(dong_tong["SoDon"]), 10)
            self.assertEqual(int(dong_tong["SoKhach"]), 26)
            self.assertEqual(int(dong_tong["SoDonHuy"]), 4)
            self.assertEqual(dong_tong["DiemTourTB"], Decimal("4.5"))
            self.assertGreater(len(ds_noi_nghi), 0)

            ds_tour_xss = [dict(r) for r in ds_tour]
            ds_tour_xss[0]["MaTour"] = "T<01>"
            ds_tour_xss[0]["TenTour"] = "<script>alert(1)</script>"
            ds_nn_xss = [dict(r) for r in ds_noi_nghi]
            ds_nn_xss[0]["MaNhaNghi"] = "NN<1>"
            ds_nn_xss[0]["TenNhaNghi"] = "Homestay <A&B>"
            ds_nn_xss[0]["LoaiHinh"] = "Resort & Spa"
            ds_nn_xss[0]["TenTinh"] = "Lào Cai <Test>"

            html_xss = services.tao_html_bao_cao_doanh_thu(
                tu_ngay=tu_ngay,
                den_ngay=den_ngay,
                ds_tour=ds_tour_xss,
                ds_noi_nghi=ds_nn_xss,
                nguoi_lap="<b>Test</b>",
                ngay_xuat=datetime(2026, 10, 23, 8, 0, 0),
                noi_nhan="Ban <Giám đốc>",
            )
            self.assertIn("&lt;b&gt;Test&lt;/b&gt;", html_xss)
            self.assertNotIn("<b>Test</b>", html_xss)
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html_xss)
            self.assertNotIn("<script>alert(1)</script>", html_xss)
            self.assertIn("T&lt;01&gt;", html_xss)
            self.assertIn("NN&lt;1&gt;", html_xss)
            self.assertIn("Homestay &lt;A&amp;B&gt;", html_xss)
            self.assertIn("Resort &amp; Spa", html_xss)
            self.assertIn("Lào Cai &lt;Test&gt;", html_xss)
            self.assertIn("Ban &lt;Giám đốc&gt;", html_xss)

            html_rong = services.tao_html_bao_cao_doanh_thu(
                tu_ngay=tu_ngay,
                den_ngay=den_ngay,
                ds_tour=[],
                ds_noi_nghi=[],
                nguoi_lap="Nguyễn Quốc Khánh",
                ngay_xuat=datetime(2026, 10, 23, 8, 0, 0),
            )
            self.assertIn("Không có dữ liệu trong kỳ báo cáo", html_rong)
            self.assertIn("Chưa có đánh giá", html_rong)
            self.assertIn(services.NOI_NHAN_R2, html_rong)
        finally:
            os.chdir(cwd_cu)

    def test_r2_pdf_a4_ngang_mot_trang(self):
        tu_ngay = date(2026, 9, 1)
        den_ngay = date(2026, 12, 31)
        ds_tour = services.lay_doanh_thu_tour_r2(tu_ngay, den_ngay)
        ds_noi_nghi = services.lay_xep_hang_noi_nghi_r2(tu_ngay, den_ngay)
        html_noi_dung = services.tao_html_bao_cao_doanh_thu(
            tu_ngay=tu_ngay,
            den_ngay=den_ngay,
            ds_tour=ds_tour,
            ds_noi_nghi=ds_noi_nghi,
            nguoi_lap="Nguyễn Quốc Khánh",
            ngay_xuat=datetime(2026, 10, 23, 8, 0, 0),
        )
        pdf_bytes = _xuat_pdf_a4_bytes(self, html_noi_dung)
        so_trang = len(re.findall(rb"/Type\s*/Page(?!s)\b", pdf_bytes))
        self.assertEqual(
            so_trang,
            1,
            f"Báo cáo R2 khi xuất PDF A4 ngang phải đúng 1 trang nhưng đang là {so_trang} trang.",
        )


if __name__ == "__main__":
    unittest.main()
