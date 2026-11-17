import os
import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import mysql.connector
from streamlit.testing.v1 import AppTest

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


class TestPagesSmoke(unittest.TestCase):
    def test_f3_page_renders_validation_and_submits(self):
        khoi_phuc_dh004()
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "3_Danh_gia.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            kh004_idx = next(
                i
                for i, opt in enumerate(at.selectbox[0].options)
                if opt.startswith("KH004")
            )
            at.selectbox[0].select_index(kh004_idx).run()
            self.assertFalse(at.exception)

            self.assertGreaterEqual(len(at.selectbox), 2)
            don_options = at.selectbox[1].options
            self.assertTrue(
                any("DH004" in opt and "02/10/2026 06:30" in opt for opt in don_options),
                don_options,
            )

            # Ca 3: Bo tich cham diem nha nghi nhung nhap nhan xet nha nghi -> bao loi
            at.checkbox[0].uncheck().run()
            self.assertFalse(at.exception)
            at.text_area[1].set_value("Phòng sạch")
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("nhà nghỉ" in err.value.lower() for err in at.error),
                [err.value for err in at.error],
            )

            # Tich lai cham diem nha nghi va gui danh gia hop le
            at.checkbox[0].check().run()
            self.assertFalse(at.exception)
            at.slider[0].set_value(4)
            at.text_area[0].set_value("Lịch trình hợp lý.")
            at.slider[1].set_value(4)
            at.text_area[1].set_value("Phòng sạch.")
            at.button[0].click().run()
            self.assertFalse(at.exception)

            self.assertTrue(
                any("DH004" in suc.value for suc in at.success),
                [suc.value for suc in at.success],
            )
            self.assertFalse(
                any("DH004" in opt for sb in at.selectbox for opt in sb.options),
                [sb.options for sb in at.selectbox],
            )
        finally:
            khoi_phuc_dh004()

    def test_f3_page_handles_empty_customers_and_db_error(self):
        with patch("services.lay_ds_khach_hang", return_value=[]):
            at_empty = AppTest.from_file(
                str(APP_DIR / "pages" / "3_Danh_gia.py"),
                default_timeout=15,
            )
            at_empty.run()
            self.assertFalse(at_empty.exception)
            self.assertTrue(
                any("chưa có khách hàng" in info.value.lower() for info in at_empty.info),
                [info.value for info in at_empty.info],
            )

        err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
        with patch("services.lay_ds_khach_hang", side_effect=err_conn):
            at_err = AppTest.from_file(
                str(APP_DIR / "pages" / "3_Danh_gia.py"),
                default_timeout=15,
            )
            at_err.run()
            self.assertFalse(at_err.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                [e.value for e in at_err.error],
            )

        with patch("services.luu_danh_gia", side_effect=db.KhongCoDongNao()):
            at_conflict = AppTest.from_file(
                str(APP_DIR / "pages" / "3_Danh_gia.py"),
                default_timeout=15,
            )
            at_conflict.run()
            kh004_idx = next(
                i
                for i, opt in enumerate(at_conflict.selectbox[0].options)
                if opt.startswith("KH004")
            )
            at_conflict.selectbox[0].select_index(kh004_idx).run()
            at_conflict.button[0].click().run()
            self.assertFalse(at_conflict.exception)
            self.assertTrue(
                any("Đơn đã thay đổi" in e.value for e in at_conflict.error),
                [e.value for e in at_conflict.error],
            )

    def test_f2_page_validation_and_cancel_dh010(self):
        khoi_phuc_dh010()
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "2_Quan_ly_don.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            dh010_idx = next(
                i
                for i, opt in enumerate(at.selectbox[0].options)
                if opt.startswith("DH010")
            )
            at.selectbox[0].select_index(dh010_idx).run()
            self.assertFalse(at.exception)

            huy_idx = next(
                i
                for i, opt in enumerate(at.selectbox[1].options)
                if "(HUY)" in opt
            )
            at.selectbox[1].select_index(huy_idx).run()
            self.assertFalse(at.exception)

            self.assertTrue(
                any("1.600.000 đ" in w.value and "14.400.000 đ" in w.value for w in at.warning),
                [w.value for w in at.warning],
            )

            # Nhap ly do huy nhung chua tich "Khách đã đồng ý mức phạt" -> bao loi
            at.text_input[0].set_value("Khách bận công tác đột xuất")
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("đồng ý mức phạt" in err.value.lower() for err in at.error),
                [err.value for err in at.error],
            )

            # Tich xac nhan muc phat va bam huy -> thanh cong va DH010 bien mat
            self.assertGreaterEqual(len(at.checkbox), 1)
            at.checkbox[0].check().run()
            self.assertFalse(at.exception)
            at.button[0].click().run()
            self.assertFalse(at.exception)

            self.assertTrue(
                any("DH010" in suc.value for suc in at.success),
                [suc.value for suc in at.success],
            )
            self.assertFalse(
                any("DH010" in opt for sb in at.selectbox for opt in sb.options),
                [sb.options for sb in at.selectbox],
            )
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            khoi_phuc_dh010()

    def test_f2_page_handles_empty_orders_and_db_error(self):
        with patch("services.lay_don_dang_mo", return_value=[]):
            at_empty = AppTest.from_file(
                str(APP_DIR / "pages" / "2_Quan_ly_don.py"),
                default_timeout=15,
            )
            at_empty.run()
            self.assertFalse(at_empty.exception)
            self.assertTrue(
                any("không có đơn hàng nào" in info.value.lower() for info in at_empty.info),
                [info.value for info in at_empty.info],
            )

        err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
        with patch("services.lay_don_dang_mo", side_effect=err_conn):
            at_err = AppTest.from_file(
                str(APP_DIR / "pages" / "2_Quan_ly_don.py"),
                default_timeout=15,
            )
            at_err.run()
            self.assertFalse(at_err.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                [e.value for e in at_err.error],
            )

        with patch("services.huy_don", side_effect=db.KhongCoDongNao()):
            at_conflict = AppTest.from_file(
                str(APP_DIR / "pages" / "2_Quan_ly_don.py"),
                default_timeout=15,
            )
            at_conflict.run()
            dh010_idx = next(
                i
                for i, opt in enumerate(at_conflict.selectbox[0].options)
                if opt.startswith("DH010")
            )
            at_conflict.selectbox[0].select_index(dh010_idx).run()
            huy_idx = next(
                i
                for i, opt in enumerate(at_conflict.selectbox[1].options)
                if "(HUY)" in opt
            )
            at_conflict.selectbox[1].select_index(huy_idx).run()
            at_conflict.text_input[0].set_value("Khách hủy do xung đột")
            at_conflict.checkbox[0].check().run()
            at_conflict.button[0].click().run()
            self.assertFalse(at_conflict.exception)
            self.assertTrue(
                any("Đơn đã thay đổi" in e.value for e in at_conflict.error),
                [e.value for e in at_conflict.error],
            )

    def test_f2_page_blocks_rb23_and_updates_status_dh013(self):
        khoi_phuc_dh010()
        khoi_phuc_trang_thai_don("DH013", "DAT")
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "2_Quan_ly_don.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            dh010_idx = next(
                i
                for i, opt in enumerate(at.selectbox[0].options)
                if opt.startswith("DH010")
            )
            at.selectbox[0].select_index(dh010_idx).run()
            huy_idx = next(
                i
                for i, opt in enumerate(at.selectbox[1].options)
                if "(HUY)" in opt
            )
            at.selectbox[1].select_index(huy_idx).run()

            # Chon ngay huy >= NgayXuatPhat (14/11/2026 06:30) -> chan theo RB23
            at.date_input[0].set_value(date(2026, 11, 14)).run()
            at.text_input[0].set_value("Thử hủy sau khởi hành")
            at.checkbox[0].check().run()
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("khởi hành" in err.value for err in at.error),
                [err.value for err in at.error],
            )

            # Chuyen sang DH013 va cap nhat sang THANHTOAN -> thanh cong
            dh013_idx = next(
                i
                for i, opt in enumerate(at.selectbox[0].options)
                if opt.startswith("DH013")
            )
            at.selectbox[0].select_index(dh013_idx).run()
            self.assertFalse(at.exception)
            tt_idx = next(
                i
                for i, opt in enumerate(at.selectbox[1].options)
                if "(THANHTOAN)" in opt
            )
            at.selectbox[1].select_index(tt_idx).run()
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("DH013" in suc.value for suc in at.success),
                [suc.value for suc in at.success],
            )
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            khoi_phuc_dh010()
            khoi_phuc_trang_thai_don("DH013", "DAT")

    def test_f1_page_existing_customer_lt06_validation_and_booking(self):
        khoi_phuc_f1_mau()
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            # Mac dinh la "Khách hàng có sẵn"
            self.assertEqual(at.radio(key="f1_loai_khach").value, "Khách hàng có sẵn")

            # Chon lich trinh LT06 (0 dem) -> an noi nghi va xe ve noi nghi
            lt_sb = at.selectbox(key="f1_chon_lich_trinh")
            lt06_idx = next(
                i for i, opt in enumerate(lt_sb.options) if opt.startswith("LT06")
            )
            lt_sb.select_index(lt06_idx).run()
            self.assertFalse(at.exception)
            self.assertEqual(len(at.selectbox), 2)
            self.assertEqual(len(at.checkbox), 1)

            # Chon KH006 va LT10 -> hien noi nghi va chon NN08
            kh_sb = at.selectbox(key="f1_chon_kh")
            kh006_idx = next(
                i for i, opt in enumerate(kh_sb.options) if opt.startswith("KH006")
            )
            kh_sb.select_index(kh006_idx).run()
            self.assertFalse(at.exception)

            lt_sb = at.selectbox(key="f1_chon_lich_trinh")
            lt10_idx = next(
                i for i, opt in enumerate(lt_sb.options) if opt.startswith("LT10")
            )
            lt_sb.select_index(lt10_idx).run()
            self.assertFalse(at.exception)

            nn_sb = at.selectbox(key="f1_noi_nghi_LT10")
            nn08_idx = next(
                i for i, opt in enumerate(nn_sb.options) if opt.startswith("NN08")
            )
            nn_sb.select_index(nn08_idx).run()
            self.assertFalse(at.exception)

            # Ca 4: 2 khach, 3 phong -> bao loi "Số phòng phải từ 1 đến số khách"
            at.number_input(key="f1_so_khach_LT10").set_value(2)
            at.number_input(key="f1_so_phong_LT10").set_value(3)
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("Số phòng phải từ 1 đến số khách" in err.value for err in at.error),
                [err.value for err in at.error],
            )

            # Ca 1 + Ca 5: 5 khach, NN08, 2 phong, tich 2 chuyen xe; giu edit dia chi don & chan khi de trong
            at.number_input(key="f1_so_khach_LT10").set_value(5)
            at.number_input(key="f1_so_phong_LT10").set_value(2)
            at.checkbox(key="f1_co_xe_don_LT10").check().run()
            self.assertFalse(at.exception)
            self.assertEqual(
                at.text_input(key="f1_dia_chi_don_LT10").value,
                "3 Hùng Vương, Lào Cai",
            )
            at.text_input(key="f1_dia_chi_don_LT10").set_value("99 Đường Mới, Hà Nội")
            at.checkbox(key="f1_co_xe_ve_LT10").check().run()
            self.assertFalse(at.exception)
            self.assertEqual(
                at.text_input(key="f1_dia_chi_don_LT10").value,
                "99 Đường Mới, Hà Nội",
            )

            # Ca 5: Xoa trang dia chi don -> bao loi "Vui lòng nhập địa chỉ đón"
            at.text_input(key="f1_dia_chi_don_LT10").set_value("   ")
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("Vui lòng nhập địa chỉ đón" in err.value for err in at.error),
                [err.value for err in at.error],
            )

            # Dien lai dia chi don hop le va xac nhan dat don -> thanh cong DH015, 32.020.000 d, LT10 con 15 cho
            at.text_input(key="f1_dia_chi_don_LT10").set_value("3 Hùng Vương, Lào Cai")
            at.button[0].click().run()
            self.assertFalse(at.exception)
            self.assertTrue(
                any("DH015" in suc.value and "32.020.000 đ" in suc.value for suc in at.success),
                [suc.value for suc in at.success],
            )
            lt_options_after = at.selectbox(key="f1_chon_lich_trinh").options
            self.assertTrue(
                any(opt.startswith("LT10") and "15 chỗ" in opt for opt in lt_options_after),
                lt_options_after,
            )
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            xoa_don_va_khach_thu_nghiem(["DH015"], [], {"LT10": 0})
            khoi_phuc_f1_mau()

    def test_f1_page_new_customer_duplicate_blocked(self):
        khoi_phuc_f1_mau()
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            at.radio(key="f1_loai_khach").set_value("Khách hàng mới").run()
            self.assertFalse(at.exception)

            at.text_input(key="f1_kh_ten").set_value("Nguyễn Test Trùng")
            at.text_input(key="f1_kh_sdt").set_value("0911223355")
            at.text_input(key="f1_kh_email").set_value("an.nguyen@gmail.com")
            at.text_input(key="f1_kh_diachi").set_value("100 Kim Mã, Hà Nội")
            at.button[0].click().run()
            self.assertFalse(at.exception)

            self.assertTrue(
                any("an.nguyen@gmail.com" in w.value or "KH001" in w.value for w in at.warning),
                [w.value for w in at.warning],
            )
            self.assertGreaterEqual(len(at.error), 1)
            self.assertEqual(
                db.doc("SELECT MaDonHang FROM DonHang WHERE MaDonHang = %s", ("DH015",)),
                [],
            )
            self.assertEqual(
                len(db.doc("SELECT MaKH FROM KhachHang")),
                8,
            )
        finally:
            khoi_phuc_f1_mau()

    def test_f1_page_handles_empty_schedules_and_db_error(self):
        with patch("services.lay_lich_trinh_con_cho", return_value=[]):
            at_empty = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at_empty.run()
            self.assertFalse(at_empty.exception)
            self.assertTrue(
                any("không có lịch trình" in w.value.lower() for w in at_empty.warning),
                [w.value for w in at_empty.warning],
            )

        err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
        with patch("services.lay_lich_trinh_con_cho", side_effect=err_conn):
            at_err = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at_err.run()
            self.assertFalse(at_err.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                [e.value for e in at_err.error],
            )

        with patch("services.lay_ds_khach_hang_f1", return_value=[]):
            at_no_kh = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at_no_kh.run()
            self.assertFalse(at_no_kh.exception)
            self.assertTrue(
                any("chưa có khách hàng" in w.value.lower() for w in at_no_kh.warning),
                [w.value for w in at_no_kh.warning],
            )

        with patch("services.lay_ds_khach_hang_f1", side_effect=err_conn):
            at_err_kh = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at_err_kh.run()
            self.assertFalse(at_err_kh.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err_kh.error),
                [e.value for e in at_err_kh.error],
            )

        with patch("services.lay_noi_nghi_theo_tinh", side_effect=err_conn):
            at_err_nn = AppTest.from_file(
                str(APP_DIR / "pages" / "1_Dat_tour.py"),
                default_timeout=15,
            )
            at_err_nn.run()
            self.assertFalse(at_err_nn.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err_nn.error),
                [e.value for e in at_err_nn.error],
            )

    def test_s1_luxury_and_reset_buttons_override_manual_filters(self):
        at = AppTest.from_file(
            str(APP_DIR / "pages" / "4_Tim_kiem.py"),
            default_timeout=15,
        )
        at.run()
        self.assertFalse(at.exception)
        self.assertFalse(at.error)

        # Nhap tay bo loc thu cong
        at.text_input(key="s1_tu_khoa").set_value("sa pa")
        at.number_input(key="s1_gia_den").set_value(5_000_000)
        at.number_input(key="s1_so_khach").set_value(4)
        at.run()
        self.assertFalse(at.exception)
        self.assertFalse(at.error)
        self.assertGreaterEqual(len(at.dataframe), 1)
        self.assertTrue(
            any("1 lịch trình phù hợp" in sh.value for sh in at.subheader),
            [sh.value for sh in at.subheader],
        )

        # Bam nut "Tour cao cấp (từ 10 triệu)" -> reset bo loc khac, khong bi loi gia_den < gia_tu
        btn_cao_cap = next(
            b for b in at.button if b.label == "Tour cao cấp (từ 10 triệu)"
        )
        btn_cao_cap.click().run()
        self.assertFalse(at.exception)
        self.assertFalse(at.error)
        self.assertEqual(at.text_input(key="s1_tu_khoa").value, "")
        self.assertEqual(at.selectbox(key="s1_tinh_den").value, "Tất cả")
        self.assertEqual(at.number_input(key="s1_gia_tu").value, 10_000_000)
        self.assertEqual(at.number_input(key="s1_gia_den").value, 0)
        self.assertEqual(at.number_input(key="s1_so_khach").value, 1)
        self.assertFalse(at.checkbox(key="s1_co_den_ngay").value)
        self.assertEqual(at.selectbox(key="s1_diem").value, "Tất cả")
        self.assertTrue(
            any("3 lịch trình phù hợp" in sh.value for sh in at.subheader),
            [sh.value for sh in at.subheader],
        )

        # Sua tay lai tu_khoa roi bam "Đặt lại bộ lọc"
        at.text_input(key="s1_tu_khoa").set_value("ha long").run()
        self.assertFalse(at.exception)
        btn_dat_lai = next(b for b in at.button if b.label == "Đặt lại bộ lọc")
        btn_dat_lai.click().run()
        self.assertFalse(at.exception)
        self.assertFalse(at.error)
        self.assertEqual(at.text_input(key="s1_tu_khoa").value, "")
        self.assertEqual(at.number_input(key="s1_gia_tu").value, 0)
        self.assertTrue(
            any("9 lịch trình phù hợp" in sh.value for sh in at.subheader),
            [sh.value for sh in at.subheader],
        )

    def test_s1_validation_errors_and_db_error(self):
        # gia_den < gia_tu -> loi tieng Viet
        at_gia = AppTest.from_file(
            str(APP_DIR / "pages" / "4_Tim_kiem.py"),
            default_timeout=15,
        )
        at_gia.run()
        at_gia.number_input(key="s1_gia_tu").set_value(5_000_000)
        at_gia.number_input(key="s1_gia_den").set_value(2_000_000)
        at_gia.run()
        self.assertFalse(at_gia.exception)
        self.assertTrue(
            any("Giá đến phải lớn hơn hoặc bằng giá từ" in err.value for err in at_gia.error),
            [err.value for err in at_gia.error],
        )

        # den_ngay < tu_ngay -> loi tieng Viet
        at_ngay = AppTest.from_file(
            str(APP_DIR / "pages" / "4_Tim_kiem.py"),
            default_timeout=15,
        )
        at_ngay.run()
        at_ngay.checkbox(key="s1_co_den_ngay").check().run()
        self.assertFalse(at_ngay.exception)
        at_ngay.date_input(key="s1_den_ngay").set_value(date(2026, 10, 1)).run()
        self.assertFalse(at_ngay.exception)
        self.assertTrue(
            any(
                "Khởi hành đến ngày phải lớn hơn hoặc bằng từ ngày" in err.value
                for err in at_ngay.error
            ),
            [err.value for err in at_ngay.error],
        )

        # DB loi khi nap danh sach tinh thanh -> hien at.error tieng Viet, khong exception
        err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
        with patch("services.lay_ds_tinh_thanh", side_effect=err_conn):
            at_err = AppTest.from_file(
                str(APP_DIR / "pages" / "4_Tim_kiem.py"),
                default_timeout=15,
            )
            at_err.run()
            self.assertFalse(at_err.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                [e.value for e in at_err.error],
            )

        # DB loi khi tim kiem lich trinh -> hien at.error tieng Viet, khong exception
        with patch("services.tim_kiem_lich_trinh", side_effect=err_conn):
            at_err_search = AppTest.from_file(
                str(APP_DIR / "pages" / "4_Tim_kiem.py"),
                default_timeout=15,
            )
            at_err_search.run()
            self.assertFalse(at_err_search.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err_search.error),
                [e.value for e in at_err_search.error],
            )

    def test_r1_page_requires_nguoi_lap_and_shows_download_button(self):
        at = AppTest.from_file(
            str(APP_DIR / "pages" / "5_Phieu_xac_nhan.py"),
            default_timeout=15,
        )
        at.run()
        self.assertFalse(at.exception)

        # Mac dinh nguoi_lap de trong -> canh bao va an nut tai / khung xem truoc
        self.assertEqual(at.text_input(key="r1_nguoi_lap").value, "")
        self.assertTrue(
            any("nhân viên lập phiếu" in w.value.lower() for w in at.warning),
            [w.value for w in at.warning],
        )
        self.assertEqual(len(at.get("download_button")), 0)
        self.assertEqual(len(at.get("iframe")), 0)

        # Chon DH007 va nhap nguoi_lap -> hien nut tai HTML va khung xem truoc
        dh007_idx = next(
            i
            for i, opt in enumerate(at.selectbox(key="r1_chon_don").options)
            if opt.startswith("DH007")
        )
        at.selectbox(key="r1_chon_don").select_index(dh007_idx)
        at.text_input(key="r1_nguoi_lap").set_value("Nguyễn Quốc Khánh")
        at.run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.warning), 0)
        self.assertEqual(len(at.error), 0)
        self.assertEqual(len(at.get("download_button")), 1)
        self.assertEqual(len(at.get("iframe")), 1)

        srcdoc_007 = at.get("iframe")[0].proto.srcdoc
        self.assertIn("6.250.000 đ", srcdoc_007)
        self.assertIn("Nguyễn Quốc Khánh", srcdoc_007)
        self.assertIn("Thẻ Visa (**** **** **** 1111)", srcdoc_007)

        # Chuyen sang DH008 -> hien thong tin huy don 30%
        dh008_idx = next(
            i
            for i, opt in enumerate(at.selectbox(key="r1_chon_don").options)
            if opt.startswith("DH008")
        )
        at.selectbox(key="r1_chon_don").select_index(dh008_idx).run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.get("download_button")), 1)
        srcdoc_008 = at.get("iframe")[0].proto.srcdoc
        self.assertIn("2.610.000 đ (30%)", srcdoc_008)
        self.assertIn("6.090.000 đ", srcdoc_008)

    def test_r1_page_handles_empty_orders_and_db_error(self):
        with patch("services.lay_ds_don_r1", return_value=[]):
            at_empty = AppTest.from_file(
                str(APP_DIR / "pages" / "5_Phieu_xac_nhan.py"),
                default_timeout=15,
            )
            at_empty.run()
            self.assertFalse(at_empty.exception)
            self.assertTrue(
                any("không có đơn hàng nào" in info.value.lower() for info in at_empty.info),
                [info.value for info in at_empty.info],
            )

        err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
        with patch("services.lay_ds_don_r1", side_effect=err_conn):
            at_err = AppTest.from_file(
                str(APP_DIR / "pages" / "5_Phieu_xac_nhan.py"),
                default_timeout=15,
            )
            at_err.run()
            self.assertFalse(at_err.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                [e.value for e in at_err.error],
            )

        with patch("services.lay_chi_tiet_don_r1", side_effect=err_conn):
            at_err_ct = AppTest.from_file(
                str(APP_DIR / "pages" / "5_Phieu_xac_nhan.py"),
                default_timeout=15,
            )
            at_err_ct.run()
            at_err_ct.text_input(key="r1_nguoi_lap").set_value("Nguyễn Quốc Khánh").run()
            self.assertFalse(at_err_ct.exception)
            self.assertTrue(
                any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err_ct.error),
                [e.value for e in at_err_ct.error],
            )

    def test_r2_page_runs_from_repo_root_and_gates_download(self):
        cwd_cu = os.getcwd()
        os.chdir(ROOT_DIR)
        try:
            at = AppTest.from_file(
                str(APP_DIR / "pages" / "6_Bao_cao_doanh_thu.py"),
                default_timeout=15,
            )
            at.run()
            self.assertFalse(at.exception)

            self.assertEqual(
                [m.value for m in at.metric],
                ["79.110.000 đ", "10 đơn", "26 khách", "4 đơn"],
            )

            # Mac dinh nguoi_lap trong -> hien canh bao, an download_button va iframe
            self.assertGreaterEqual(len(at.warning), 1)
            self.assertEqual(len(at.get("download_button")), 0)
            self.assertEqual(len(at.get("iframe")), 0)

            # Nhap nguoi_lap co the HTML -> het warning, co download_button va iframe escape XSS
            at.text_input[0].set_value("<b>Kế toán</b>").run()
            self.assertFalse(at.exception)
            self.assertEqual(len(at.warning), 0)
            self.assertEqual(len(at.error), 0)
            self.assertEqual(len(at.get("download_button")), 1)
            self.assertEqual(len(at.get("iframe")), 1)
            srcdoc = at.get("iframe")[0].proto.srcdoc
            self.assertIn("&lt;b&gt;Kế toán&lt;/b&gt;", srcdoc)
            self.assertNotIn("<b>Kế toán</b>", srcdoc)

            # den_ngay < tu_ngay -> hien at.error
            at_bad_date = AppTest.from_file(
                str(APP_DIR / "pages" / "6_Bao_cao_doanh_thu.py"),
                default_timeout=15,
            )
            at_bad_date.run()
            at_bad_date.date_input[1].set_value(date(2026, 8, 1)).run()
            self.assertFalse(at_bad_date.exception)
            self.assertTrue(
                any("đến ngày phải lớn hơn hoặc bằng từ ngày" in e.value for e in at_bad_date.error),
                [e.value for e in at_bad_date.error],
            )

            # DB loi -> hien at.error tieng Viet, khong exception
            err_conn = mysql.connector.errors.DatabaseError(errno=2003, msg="Can't connect")
            with patch("services.lay_doanh_thu_tour_r2", side_effect=err_conn):
                at_err = AppTest.from_file(
                    str(APP_DIR / "pages" / "6_Bao_cao_doanh_thu.py"),
                    default_timeout=15,
                )
                at_err.run()
                self.assertFalse(at_err.exception)
                self.assertTrue(
                    any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err.error),
                    [e.value for e in at_err.error],
                )

            with patch("services.lay_xep_hang_noi_nghi_r2", side_effect=err_conn):
                at_err_nn = AppTest.from_file(
                    str(APP_DIR / "pages" / "6_Bao_cao_doanh_thu.py"),
                    default_timeout=15,
                )
                at_err_nn.run()
                self.assertFalse(at_err_nn.exception)
                self.assertTrue(
                    any("Không kết nối được cơ sở dữ liệu" in e.value for e in at_err_nn.error),
                    [e.value for e in at_err_nn.error],
                )

            # Ky bao cao khong co du lieu -> hien st.info + HTML fallback
            with (
                patch("services.lay_doanh_thu_tour_r2", return_value=[]),
                patch("services.lay_xep_hang_noi_nghi_r2", return_value=[]),
            ):
                at_empty = AppTest.from_file(
                    str(APP_DIR / "pages" / "6_Bao_cao_doanh_thu.py"),
                    default_timeout=15,
                )
                at_empty.run()
                at_empty.text_input[0].set_value("Kế toán trưởng").run()
                self.assertFalse(at_empty.exception)
                self.assertEqual(
                    [m.value for m in at_empty.metric],
                    ["0 đ", "0 đơn", "0 khách", "0 đơn"],
                )
                self.assertEqual(len(at_empty.info), 2)
                empty_srcdoc = at_empty.get("iframe")[0].proto.srcdoc
                self.assertIn("Không có dữ liệu trong kỳ báo cáo", empty_srcdoc)
                self.assertIn("Chưa có đánh giá", empty_srcdoc)
        finally:
            os.chdir(cwd_cu)

    def test_app_home_page_renders_12_tables(self):
        at = AppTest.from_file(
            str(APP_DIR / "app.py"),
            default_timeout=15,
        )
        at.run()
        self.assertFalse(at.exception)
        self.assertTrue(
            any("Đã kết nối cơ sở dữ liệu: 12 bảng" in s.value for s in at.success),
            [s.value for s in at.success],
        )


if __name__ == "__main__":
    unittest.main()
