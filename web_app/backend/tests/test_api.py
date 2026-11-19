"""Kiểm thử toàn diện REST API, phân quyền HMAC, toàn vẹn MySQL và xuất PDF A4 thật."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[3]
TOUR_APP_DIR = ROOT_DIR / "tour_app"
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(TOUR_APP_DIR) not in sys.path:
    sys.path.insert(0, str(TOUR_APP_DIR))

import db  # noqa: E402
from tests.helpers import (  # noqa: E402
    chay_kiem_tra_rang_buoc,
    khoi_phuc_dh004,
    khoi_phuc_dh010,
    khoi_phuc_f1_mau,
    khoi_phuc_trang_thai_don,
    xoa_don_va_khach_thu_nghiem,
)
from web_app.backend.main import app  # noqa: E402

ISO_DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$")
PDF_PAGE_RE = re.compile(rb"/Type\s*/Page(?!s)\b")


def _count_pdf_pages(pdf_bytes: bytes) -> int:
    return len(PDF_PAGE_RE.findall(pdf_bytes))


class BaseApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def login_customer(self, identifier: str) -> tuple[str, dict]:
        resp = self.client.post("/api/auth/customer-login", json={"identifier": identifier})
        self.assertEqual(resp.status_code, 200, resp.text)
        data = resp.json()
        return data["token"], data["customer"]

    def login_admin(
        self,
        username: str = "admin",
        password: str = "admin123",
        staff_name: str | None = None,
    ) -> tuple[str, dict]:
        payload: dict = {"username": username, "password": password}
        if staff_name is not None:
            payload["staff_name"] = staff_name
        resp = self.client.post("/api/auth/admin-login", json=payload)
        self.assertEqual(resp.status_code, 200, resp.text)
        data = resp.json()
        return data["token"], data


class TestPublicAndSerialization(BaseApiTestCase):
    def test_meta_landing_provinces_open_schedules_accommodations_types(self) -> None:
        # GET /api/meta
        meta_resp = self.client.get("/api/meta")
        self.assertEqual(meta_resp.status_code, 200)
        meta = meta_resp.json()
        self.assertEqual(meta["brand_name"], "Bắc Việt Travel")
        self.assertEqual(meta["current_date"], "2026-10-23")
        self.assertRegex(meta["current_datetime"], ISO_DATETIME_RE)

        # GET /api/landing
        landing_resp = self.client.get("/api/landing")
        self.assertEqual(landing_resp.status_code, 200)
        landing = landing_resp.json()
        stats = landing["stats"]
        self.assertEqual(stats["total_provinces"], 15)
        self.assertEqual(stats["total_tours"], 9)
        self.assertEqual(stats["open_schedules"], 9)
        self.assertEqual(stats["total_travelers_served"], 26)
        self.assertEqual(stats["total_reviews"], 4)
        self.assertIs(type(stats["total_provinces"]), int)
        self.assertIs(type(stats["total_travelers_served"]), int)
        self.assertIs(type(stats["avg_rating"]), float)
        self.assertEqual(stats["avg_rating"], 4.5)

        featured = landing["featured_schedules"]
        self.assertEqual(len(featured), 9)
        lt04 = next(item for item in featured if item["ma_lich_trinh"] == "LT04")
        self.assertEqual(lt04["ma_tour"], "T01")
        self.assertTrue(lt04["mo_ta"])
        self.assertRegex(lt04["ngay_xuat_phat"], ISO_DATETIME_RE)
        self.assertIs(type(lt04["gia_co_ban"]), int)
        self.assertIs(type(lt04["so_ngay"]), int)
        self.assertIs(type(lt04["so_cho_con_lai"]), int)
        self.assertIs(type(lt04["so_luot_danh_gia"]), int)
        self.assertIs(type(lt04["diem_tb"]), float)

        # GET /api/provinces
        prov_resp = self.client.get("/api/provinces")
        self.assertEqual(prov_resp.status_code, 200)
        provinces = prov_resp.json()
        self.assertEqual(len(provinces), 15)
        self.assertTrue(any(p["ma_tinh"] == "LC" and p["ten_tinh"] == "Lào Cai" for p in provinces))

        # GET /api/schedules/open
        open_resp = self.client.get("/api/schedules/open")
        self.assertEqual(open_resp.status_code, 200)
        open_items = open_resp.json()
        self.assertEqual(len(open_items), 9)
        lt06 = next(item for item in open_items if item["ma_lich_trinh"] == "LT06")
        self.assertEqual(lt06["so_dem"], 0)
        self.assertEqual(lt06["noi_di"], "Hà Nội")
        self.assertTrue(lt06["diem_tap_trung"])
        self.assertTrue(lt06["mo_ta"])
        self.assertRegex(lt06["ngay_xuat_phat"], ISO_DATETIME_RE)
        self.assertRegex(lt06["ngay_ket_thuc"], ISO_DATETIME_RE)
        self.assertIs(type(lt06["gia_co_ban"]), int)

        # GET /api/accommodations
        acc_resp = self.client.get("/api/accommodations", params={"ma_tinh_den": "QN"})
        self.assertEqual(acc_resp.status_code, 200)
        accs = acc_resp.json()
        self.assertEqual([a["ma_nha_nghi"] for a in accs], ["NN02", "NN01"])
        for acc in accs:
            self.assertTrue(acc["dia_chi"])
            self.assertIs(type(acc["gia_phong_moi_dem"]), int)

    def test_search_schedules_8_filters_and_validation(self) -> None:
        # Luxury filter >= 10M
        resp_lux = self.client.get("/api/schedules/search", params={"gia_tu": 10000000})
        self.assertEqual(resp_lux.status_code, 200)
        self.assertEqual(
            [item["ma_lich_trinh"] for item in resp_lux.json()],
            ["LT08", "LT09", "LT12"],
        )

        # Keyword + seats
        resp_hl = self.client.get(
            "/api/schedules/search",
            params={"tu_khoa": "ha long", "so_khach": 2},
        )
        self.assertEqual(resp_hl.status_code, 200)
        self.assertEqual(
            [item["ma_lich_trinh"] for item in resp_hl.json()],
            ["LT04", "LT08", "LT12"],
        )

        # Combined filters for Sa Pa
        resp_sapa = self.client.get(
            "/api/schedules/search",
            params={
                "ma_tinh_den": "LC",
                "gia_den": 4000000,
                "tu_ngay": "2026-10-23",
                "den_ngay": "2026-12-31",
                "so_khach": 4,
                "diem_toi_thieu": 4.5,
            },
        )
        self.assertEqual(resp_sapa.status_code, 200)
        sapa_items = resp_sapa.json()
        self.assertEqual([item["ma_lich_trinh"] for item in sapa_items], ["LT05"])
        self.assertEqual(sapa_items[0]["ma_tour"], "T02")
        self.assertIs(type(sapa_items[0]["diem_tb"]), float)
        self.assertEqual(sapa_items[0]["diem_tb"], 5.0)

        # Empty string optional params handled cleanly
        resp_empty_strings = self.client.get(
            "/api/schedules/search",
            params={
                "tu_khoa": "",
                "ma_tinh_den": "",
                "gia_tu": "",
                "gia_den": "",
                "tu_ngay": "",
                "den_ngay": "",
                "so_khach": "1",
                "diem_toi_thieu": "",
            },
        )
        self.assertEqual(resp_empty_strings.status_code, 200)
        self.assertEqual(len(resp_empty_strings.json()), 9)

        # Validation errors: gia_den < gia_tu and den_ngay < tu_ngay
        bad_price = self.client.get(
            "/api/schedules/search",
            params={"gia_tu": 5000000, "gia_den": 2000000},
        )
        self.assertEqual(bad_price.status_code, 400)
        self.assertIn("detail", bad_price.json())

        bad_date = self.client.get(
            "/api/schedules/search",
            params={"tu_ngay": "2026-12-01", "den_ngay": "2026-11-01"},
        )
        self.assertEqual(bad_date.status_code, 400)


class TestAuthAndOwnershipBoundary(BaseApiTestCase):
    def test_auth_endpoints_and_duplicate_check(self) -> None:
        # GET /api/customers
        cust_resp = self.client.get("/api/customers")
        self.assertEqual(cust_resp.status_code, 200)
        customers = cust_resp.json()
        self.assertEqual(len(customers), 8)
        self.assertEqual(customers[0]["ma_kh"], "KH001")

        # Duplicate check: email (case-insensitive), phone, and clean
        dup_email = self.client.post(
            "/api/customers/check-duplicate",
            json={"email": "AN.NGUYEN@GMAIL.COM", "so_dien_thoai": "0999888777"},
        )
        self.assertEqual(dup_email.status_code, 200)
        self.assertTrue(dup_email.json()["duplicate"])
        self.assertEqual(dup_email.json()["customer"]["ma_kh"], "KH001")

        dup_phone = self.client.post(
            "/api/customers/check-duplicate",
            json={"email": "chua.co@gmail.com", "so_dien_thoai": "0398765432"},
        )
        self.assertEqual(dup_phone.status_code, 200)
        self.assertTrue(dup_phone.json()["duplicate"])
        self.assertEqual(dup_phone.json()["customer"]["ma_kh"], "KH006")

        not_dup = self.client.post(
            "/api/customers/check-duplicate",
            json={"email": "khach.moi@gmail.com", "so_dien_thoai": "0911223344"},
        )
        self.assertEqual(not_dup.status_code, 200)
        self.assertFalse(not_dup.json()["duplicate"])
        self.assertIsNone(not_dup.json()["customer"])

        # Customer login by email and by phone
        token_email, cust_email = self.login_customer("AN.NGUYEN@GMAIL.COM")
        self.assertTrue(token_email)
        self.assertEqual(cust_email["ma_kh"], "KH001")

        token_phone, cust_phone = self.login_customer("0978123456")
        self.assertTrue(token_phone)
        self.assertEqual(cust_phone["ma_kh"], "KH004")

        # Unknown customer -> 404
        not_found = self.client.post(
            "/api/auth/customer-login",
            json={"identifier": "khongtontai@example.com"},
        )
        self.assertEqual(not_found.status_code, 404)

        # Admin login: wrong password -> 401; valid -> 200
        bad_admin = self.client.post(
            "/api/auth/admin-login",
            json={"username": "admin", "password": "wrong"},
        )
        self.assertEqual(bad_admin.status_code, 401)

        admin_token, admin_data = self.login_admin()
        self.assertTrue(admin_token)
        self.assertEqual(admin_data["username"], "admin")
        self.assertEqual(admin_data["staff_name"], "Nguyễn Quốc Khánh")

        _, admin_custom = self.login_admin(staff_name="Trần Minh Quân")
        self.assertEqual(admin_custom["staff_name"], "Trần Minh Quân")

    def test_ownership_isolation_401_403_and_admin_guard(self) -> None:
        kh001_token, _ = self.login_customer("an.nguyen@gmail.com")
        kh004_token, _ = self.login_customer("dung.pham@outlook.com")
        admin_token, _ = self.login_admin()

        # Unauthenticated customer endpoints -> 401
        self.assertEqual(self.client.get("/api/customers/KH004/orders").status_code, 401)
        self.assertEqual(self.client.get("/api/customers/KH004/pending-reviews").status_code, 401)
        self.assertEqual(
            self.client.post(
                "/api/reviews",
                json={
                    "ma_don_hang": "DH004",
                    "diem_tour": 5,
                    "co_danh_gia_nha_nghi": False,
                },
            ).status_code,
            401,
        )
        self.assertEqual(self.client.get("/api/orders/DH008/confirmation/pdf").status_code, 401)

        # Review Focus #2: KH001 accessing KH004 orders, pending-reviews, reviewing DH004, downloading DH008 PDF -> 403
        self.assertEqual(
            self.client.get(
                "/api/customers/KH004/orders",
                headers={"X-Customer-Token": kh001_token},
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                "/api/customers/KH004/pending-reviews",
                headers={"X-Customer-Token": kh001_token},
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh001_token},
                json={
                    "ma_don_hang": "DH004",
                    "diem_tour": 5,
                    "nhan_xet_tour": "Thử đánh giá chéo",
                    "co_danh_gia_nha_nghi": False,
                },
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.get(
                "/api/orders/DH008/confirmation/pdf",
                headers={"X-Customer-Token": kh001_token},
            ).status_code,
            403,
        )

        # KH004 accessing own orders & pending reviews -> 200 with clean types
        own_orders_resp = self.client.get(
            "/api/customers/KH004/orders",
            headers={"X-Customer-Token": kh004_token},
        )
        self.assertEqual(own_orders_resp.status_code, 200)
        own_orders = own_orders_resp.json()
        self.assertEqual({o["ma_don_hang"] for o in own_orders}, {"DH004", "DH014"})
        dh004 = next(o for o in own_orders if o["ma_don_hang"] == "DH004")
        self.assertTrue(dh004["co_the_danh_gia"])
        self.assertIs(type(dh004["tong_tien"]), int)
        self.assertRegex(dh004["ngay_dat"], ISO_DATETIME_RE)

        own_pending_resp = self.client.get(
            "/api/customers/KH004/pending-reviews",
            headers={"X-Customer-Token": kh004_token},
        )
        self.assertEqual(own_pending_resp.status_code, 200)
        self.assertEqual([r["ma_don_hang"] for r in own_pending_resp.json()], ["DH004"])

        # Admin can read any customer's orders
        admin_read = self.client.get(
            "/api/customers/KH004/orders",
            headers={"X-Admin-Token": admin_token},
        )
        self.assertEqual(admin_read.status_code, 200)

        # Unauthenticated / customer-only / tampered token on /api/admin/* -> 401
        admin_endpoints = [
            ("GET", "/api/admin/orders", None),
            ("GET", "/api/admin/orders/DH007", None),
            ("POST", "/api/admin/orders/DH010/cancel-preview", {"ngay_gio_huy": "2026-10-23T08:00:00"}),
            (
                "POST",
                "/api/admin/orders/DH010/cancel",
                {"ngay_gio_huy": "2026-10-23T08:00:00", "ly_do_huy": "Test", "da_dong_y_phat": True},
            ),
            ("PATCH", "/api/admin/orders/DH013/status", {"trang_thai_moi": "THANHTOAN"}),
            ("GET", "/api/admin/orders/DH007/confirmation/html", None),
            ("GET", "/api/admin/reports/revenue", None),
            (
                "POST",
                "/api/admin/reports/revenue/html",
                {"tu_ngay": "2026-09-01", "den_ngay": "2026-12-31", "nguoi_lap": "Test"},
            ),
            (
                "POST",
                "/api/admin/reports/revenue/pdf",
                {"tu_ngay": "2026-09-01", "den_ngay": "2026-12-31", "nguoi_lap": "Test"},
            ),
        ]
        for method, path, body in admin_endpoints:
            with self.subTest(method=method, path=path):
                r_no_auth = self.client.request(method, path, json=body)
                self.assertEqual(r_no_auth.status_code, 401)

                r_cust_only = self.client.request(
                    method,
                    path,
                    json=body,
                    headers={"X-Customer-Token": kh001_token},
                )
                self.assertEqual(r_cust_only.status_code, 401)

                r_tampered = self.client.request(
                    method,
                    path,
                    json=body,
                    headers={"X-Admin-Token": admin_token + "tampered"},
                )
                self.assertEqual(r_tampered.status_code, 401)


class TestBookingFlowsAndReviewEdgeCases(BaseApiTestCase):
    def test_estimate_and_guest_day_tour_lt06_with_auto_token_pdf_and_rollback(self) -> None:
        khoi_phuc_f1_mau()
        try:
            # Estimate multi-day and day tour
            est_multi = self.client.post(
                "/api/bookings/estimate",
                json={
                    "so_khach": 5,
                    "gia_co_ban": 5900000,
                    "so_phong": 2,
                    "gia_phong_moi_dem": 420000,
                    "so_dem": 3,
                    "co_nha_nghi": True,
                },
            )
            self.assertEqual(est_multi.status_code, 200)
            self.assertEqual(
                est_multi.json(),
                {"tien_tour": 29500000, "tien_phong": 2520000, "tong_tien": 32020000},
            )

            est_day = self.client.post(
                "/api/bookings/estimate",
                json={
                    "so_khach": 2,
                    "gia_co_ban": 900000,
                    "so_phong": 1,
                    "gia_phong_moi_dem": 400000,
                    "so_dem": 0,
                    "co_nha_nghi": False,
                },
            )
            self.assertEqual(est_day.status_code, 200)
            self.assertEqual(
                est_day.json(),
                {"tien_tour": 1800000, "tien_phong": 0, "tong_tien": 1800000},
            )

            # Snapshot row counts before invalid bookings
            orders_before = int(db.doc("SELECT COUNT(*) AS c FROM DonHang")[0]["c"])
            customers_before = int(db.doc("SELECT COUNT(*) AS c FROM KhachHang")[0]["c"])

            # Invalid #1: duplicate email for new customer -> 400 + rollback
            bad_dup = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": True,
                    "ho_ten": "Khách Trùng Email",
                    "so_dien_thoai": "0911223344",
                    "email": "an.nguyen@gmail.com",
                    "dia_chi": "10 Nguyễn Trãi, Hà Nội",
                    "ma_lich_trinh": "LT06",
                    "so_khach": 2,
                    "ma_nha_nghi": None,
                    "so_phong": 0,
                    "co_xe_don": False,
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(bad_dup.status_code, 400)
            self.assertIn("errors", bad_dup.json())

            # Invalid #2: SoPhong > SoLuongKhach -> 400
            bad_rooms = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": False,
                    "ma_kh": "KH006",
                    "ma_lich_trinh": "LT10",
                    "so_khach": 2,
                    "ma_nha_nghi": "NN08",
                    "so_phong": 3,
                    "co_xe_don": False,
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(bad_rooms.status_code, 400)
            self.assertIn("Số phòng", bad_rooms.json()["detail"])

            # Invalid #3: co_xe_don=True missing dia_chi_don -> 400
            bad_pickup = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": False,
                    "ma_kh": "KH006",
                    "ma_lich_trinh": "LT10",
                    "so_khach": 2,
                    "ma_nha_nghi": None,
                    "so_phong": 0,
                    "co_xe_don": True,
                    "dia_chi_don": "   ",
                    "gio_don": "2026-11-26T17:00:00",
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(bad_pickup.status_code, 400)
            self.assertIn("địa chỉ đón", bad_pickup.json()["detail"].lower())

            # Invalid #4: Day tour LT06 with accommodation -> 400
            bad_day_acc = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": False,
                    "ma_kh": "KH006",
                    "ma_lich_trinh": "LT06",
                    "so_khach": 2,
                    "ma_nha_nghi": "NN01",
                    "so_phong": 1,
                    "co_xe_don": False,
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(bad_day_acc.status_code, 400)

            # Invalid #5: Overbooking LT08 (only 10 seats left) -> 400
            bad_overbook = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": False,
                    "ma_kh": "KH006",
                    "ma_lich_trinh": "LT08",
                    "so_khach": 11,
                    "ma_nha_nghi": None,
                    "so_phong": 0,
                    "co_xe_don": False,
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(bad_overbook.status_code, 400)

            # Confirm DB row counts completely unchanged
            self.assertEqual(int(db.doc("SELECT COUNT(*) AS c FROM DonHang")[0]["c"]), orders_before)
            self.assertEqual(int(db.doc("SELECT COUNT(*) AS c FROM KhachHang")[0]["c"]), customers_before)

            # Valid guest new-customer booking on day tour LT06 (Review Focus #3 & #4)
            guest_resp = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": True,
                    "ho_ten": "Nguyễn Minh Tuấn",
                    "so_dien_thoai": "0911223344",
                    "email": "tuan.moi@gmail.com",
                    "dia_chi": "15 Phố Huế, Hà Nội",
                    "ma_lich_trinh": "LT06",
                    "so_khach": 2,
                    "ma_nha_nghi": None,
                    "so_phong": 0,
                    "co_xe_don": False,
                    "co_xe_ve": False,
                },
            )
            self.assertEqual(guest_resp.status_code, 200, guest_resp.text)
            created = guest_resp.json()
            self.assertEqual(created["ma_don_hang"], "DH015")
            self.assertEqual(created["ma_kh"], "KH009")
            self.assertEqual(created["tong_tien"], 1800000)
            self.assertIs(type(created["tong_tien"]), int)
            self.assertEqual(created["customer"]["ho_ten"], "Nguyễn Minh Tuấn")
            self.assertTrue(created["customer_token"])

            # Immediate customer orders view using auto-issued token
            my_orders_resp = self.client.get(
                f"/api/customers/{created['ma_kh']}/orders",
                headers={"X-Customer-Token": created["customer_token"]},
            )
            self.assertEqual(my_orders_resp.status_code, 200)
            self.assertEqual([o["ma_don_hang"] for o in my_orders_resp.json()], ["DH015"])

            # Full multi-day booking on LT10 with accommodation + 2 shuttles
            full_resp = self.client.post(
                "/api/bookings",
                json={
                    "la_khach_moi": False,
                    "ma_kh": "KH006",
                    "ma_lich_trinh": "LT10",
                    "so_khach": 5,
                    "ma_nha_nghi": "NN08",
                    "so_phong": 2,
                    "co_xe_don": True,
                    "dia_chi_don": "3 Hùng Vương, Lào Cai",
                    "gio_don": "2026-11-26T15:00:00",
                    "co_xe_ve": True,
                    "gio_ve_noi_nghi": "2026-11-27T10:00:00",
                },
            )
            self.assertEqual(full_resp.status_code, 200, full_resp.text)
            self.assertEqual(full_resp.json()["tong_tien"], 32020000)

            self.assertEqual(chay_kiem_tra_rang_buoc(), [])

            # Immediate PDF download using auto-issued guest customer_token (Review Focus #3 & #5)
            pdf_resp = self.client.get(
                f"/api/orders/{created['ma_don_hang']}/confirmation/pdf",
                headers={"X-Customer-Token": created["customer_token"]},
            )
            self.assertEqual(pdf_resp.status_code, 200)
            self.assertEqual(pdf_resp.headers["content-type"], "application/pdf")
            self.assertTrue(pdf_resp.content.startswith(b"%PDF-"))
            self.assertEqual(_count_pdf_pages(pdf_resp.content), 1)
        finally:
            xoa_don_va_khach_thu_nghiem(["DH015", "DH016"], ["KH009"], {"LT06": 3, "LT10": 0})
            khoi_phuc_f1_mau()

    def test_review_submission_duplicate_block_and_no_accommodation_edge_case(self) -> None:
        khoi_phuc_dh004()
        khoi_phuc_f1_mau()
        try:
            kh004_token, _ = self.login_customer("dung.pham@outlook.com")

            # Comment on accommodation without rating -> 400
            bad_rev = self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh004_token},
                json={
                    "ma_don_hang": "DH004",
                    "diem_tour": 4,
                    "nhan_xet_tour": "Tốt",
                    "co_danh_gia_nha_nghi": False,
                    "diem_nha_nghi": None,
                    "nhan_xet_nha_nghi": "Phòng sạch nhưng chưa chọn sao",
                },
            )
            self.assertEqual(bad_rev.status_code, 400)

            # Valid review on DH004 -> 200
            ok_rev = self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh004_token},
                json={
                    "ma_don_hang": "DH004",
                    "diem_tour": 4,
                    "nhan_xet_tour": "Lịch trình hợp lý.",
                    "co_danh_gia_nha_nghi": True,
                    "diem_nha_nghi": 4,
                    "nhan_xet_nha_nghi": "Phòng sạch.",
                },
            )
            self.assertEqual(ok_rev.status_code, 200, ok_rev.text)
            self.assertRegex(ok_rev.json()["ngay_danh_gia"], ISO_DATETIME_RE)

            # Second review on DH004 -> 409
            dup_rev = self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh004_token},
                json={
                    "ma_don_hang": "DH004",
                    "diem_tour": 5,
                    "co_danh_gia_nha_nghi": False,
                },
            )
            self.assertEqual(dup_rev.status_code, 409)

            # Edge case (Review Focus #4): completed order WITHOUT MaNhaNghi
            db.ghi(
                [
                    (
                        """
                        INSERT INTO DonHang (MaDonHang, NgayDat, SoLuongKhach, SoPhong, MaTrangThai, MaKH, MaLichTrinh, MaNhaNghi)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, NULL)
                        """,
                        ("DH099", "2026-10-01 09:00:00", 1, 0, "HOANTHANH", "KH004", "LT03"),
                        True,
                    ),
                    (
                        "UPDATE LichTrinh SET SoChoDaDat = SoChoDaDat + 1 WHERE MaLichTrinh = %s",
                        ("LT03",),
                        True,
                    ),
                ]
            )

            # Trying to rate accommodation on order without MaNhaNghi -> 400 without DB jargon
            bad_no_acc = self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh004_token},
                json={
                    "ma_don_hang": "DH099",
                    "diem_tour": 5,
                    "co_danh_gia_nha_nghi": True,
                    "diem_nha_nghi": 5,
                    "nhan_xet_nha_nghi": "Thử chấm phòng",
                },
            )
            self.assertEqual(bad_no_acc.status_code, 400)
            self.assertNotIn("chk_", bad_no_acc.json()["detail"])
            self.assertNotIn("MaNhaNghi", bad_no_acc.json()["detail"])

            # Tour-only review succeeds cleanly
            ok_no_acc = self.client.post(
                "/api/reviews",
                headers={"X-Customer-Token": kh004_token},
                json={
                    "ma_don_hang": "DH099",
                    "diem_tour": 5,
                    "nhan_xet_tour": "Chuyến đi tuyệt vời.",
                    "co_danh_gia_nha_nghi": False,
                    "diem_nha_nghi": None,
                    "nhan_xet_nha_nghi": None,
                },
            )
            self.assertEqual(ok_no_acc.status_code, 200, ok_no_acc.text)
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])
        finally:
            xoa_don_va_khach_thu_nghiem(["DH099"], [], {"LT03": 2})
            khoi_phuc_dh004()
            khoi_phuc_f1_mau()


class TestAdminOperationsAndPdfOutputs(BaseApiTestCase):
    def test_admin_orders_list_detail_status_and_atomic_cancel(self) -> None:
        khoi_phuc_dh010()
        khoi_phuc_trang_thai_don("DH013", "DAT")
        khoi_phuc_trang_thai_don("DH012", "THANHTOAN")
        try:
            admin_token, _ = self.login_admin()
            headers = {"X-Admin-Token": admin_token}

            # Full orders list & status counts
            list_resp = self.client.get("/api/admin/orders", headers=headers)
            self.assertEqual(list_resp.status_code, 200)
            data = list_resp.json()
            self.assertEqual(
                data["counts"],
                {"ALL": 14, "DAT": 3, "THANHTOAN": 2, "HOANTHANH": 5, "HUY": 4},
            )
            self.assertEqual(len(data["orders"]), 14)

            # Filter by status HUY keeps full counts intact
            huy_resp = self.client.get(
                "/api/admin/orders",
                headers=headers,
                params={"trang_thai": "HUY"},
            )
            self.assertEqual(huy_resp.status_code, 200)
            self.assertEqual(huy_resp.json()["counts"]["ALL"], 14)
            self.assertEqual(len(huy_resp.json()["orders"]), 4)

            # Filter by keyword
            kw_resp = self.client.get(
                "/api/admin/orders",
                headers=headers,
                params={"tu_khoa": "DH007"},
            )
            self.assertEqual(kw_resp.status_code, 200)
            self.assertEqual([o["ma_don_hang"] for o in kw_resp.json()["orders"]], ["DH007"])

            # Order detail DH007
            det_resp = self.client.get("/api/admin/orders/DH007", headers=headers)
            self.assertEqual(det_resp.status_code, 200)
            det = det_resp.json()
            self.assertEqual(det["phone_numbers"], "0912345678, 0987654321")
            self.assertEqual(len(det["shuttles"]), 2)
            self.assertEqual([s["ma_trang_thai"] for s in det["valid_next_statuses"]], ["HUY"])
            self.assertIs(type(det["detail"]["tong_tien"]), int)
            self.assertEqual(det["detail"]["tong_tien"], 6250000)
            self.assertRegex(det["detail"]["ngay_dat"], ISO_DATETIME_RE)

            # Status transitions: DH013 DAT -> THANHTOAN (200), DH012 THANHTOAN -> HOANTHANH before end (409)
            st_ok = self.client.patch(
                "/api/admin/orders/DH013/status",
                headers=headers,
                json={"trang_thai_moi": "THANHTOAN"},
            )
            self.assertEqual(st_ok.status_code, 200)
            self.assertEqual(st_ok.json()["ma_trang_thai"], "THANHTOAN")

            st_early = self.client.patch(
                "/api/admin/orders/DH012/status",
                headers=headers,
                json={"trang_thai_moi": "HOANTHANH"},
            )
            self.assertEqual(st_early.status_code, 409)

            # Cancel preview DH010
            prev_resp = self.client.post(
                "/api/admin/orders/DH010/cancel-preview",
                headers=headers,
                json={"ngay_gio_huy": "2026-10-23T08:00:00"},
            )
            self.assertEqual(prev_resp.status_code, 200)
            prev = prev_resp.json()
            self.assertEqual(prev["so_ngay_truoc_khoi_hanh"], 22)
            self.assertEqual(prev["ty_le_phat"], 10)
            self.assertEqual(prev["tien_phat"], 1600000)
            self.assertEqual(prev["tien_hoan"], 14400000)
            self.assertIs(type(prev["tien_phat"]), int)

            # Cancel without consent -> 400
            bad_cancel = self.client.post(
                "/api/admin/orders/DH010/cancel",
                headers=headers,
                json={
                    "ngay_gio_huy": "2026-10-23T08:00:00",
                    "ly_do_huy": "Khách bận",
                    "da_dong_y_phat": False,
                },
            )
            self.assertEqual(bad_cancel.status_code, 400)

            # Valid atomic cancel DH010
            ok_cancel = self.client.post(
                "/api/admin/orders/DH010/cancel",
                headers=headers,
                json={
                    "ngay_gio_huy": "2026-10-23T08:00:00",
                    "ly_do_huy": "Khách bận công tác đột xuất",
                    "da_dong_y_phat": True,
                },
            )
            self.assertEqual(ok_cancel.status_code, 200, ok_cancel.text)
            c_data = ok_cancel.json()
            self.assertEqual(c_data["tien_phat"], 1600000)
            self.assertEqual(c_data["tien_hoan"], 14400000)
            self.assertEqual(c_data["so_cho_hoan"], 4)

            lt05 = db.doc("SELECT SoChoDaDat FROM LichTrinh WHERE MaLichTrinh = %s", ("LT05",))[0]
            self.assertEqual(int(lt05["SoChoDaDat"]), 0)
            ctc = db.doc(
                "SELECT COUNT(*) AS cnt FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
                ("DH010",),
            )[0]
            self.assertEqual(int(ctc["cnt"]), 0)
            self.assertEqual(chay_kiem_tra_rang_buoc(), [])

            # Duplicate cancel -> 409
            dup_cancel = self.client.post(
                "/api/admin/orders/DH010/cancel",
                headers=headers,
                json={
                    "ngay_gio_huy": "2026-10-23T08:00:00",
                    "ly_do_huy": "Hủy lần 2",
                    "da_dong_y_phat": True,
                },
            )
            self.assertEqual(dup_cancel.status_code, 409)
        finally:
            khoi_phuc_dh010()
            khoi_phuc_trang_thai_don("DH013", "DAT")
            khoi_phuc_trang_thai_don("DH012", "THANHTOAN")

    def test_confirmation_branding_xss_and_real_1_page_pdfs(self) -> None:
        admin_token, _ = self.login_admin()
        kh007_token, _ = self.login_customer("khai.dang@gmail.com")
        admin_headers = {"X-Admin-Token": admin_token}

        # Confirmation HTML: branding transform + XSS escaping (Review Focus #5)
        xss_issuer = '<script>alert("xss")</script><b>Khánh</b>'
        html_resp = self.client.get(
            "/api/admin/orders/DH007/confirmation/html",
            headers=admin_headers,
            params={"nguoi_lap": xss_issuer},
        )
        self.assertEqual(html_resp.status_code, 200)
        html_text = html_resp.json()["html"]
        self.assertIn("BẮC VIỆT TRAVEL", html_text)
        self.assertIn("Bắc Việt Travel", html_text)
        self.assertIn("lienhe@bacviettravel.vn", html_text)
        self.assertIn("Số 10 Nguyễn Trãi, Hà Đông, Hà Nội", html_text)
        self.assertNotIn("PTIT", html_text)
        self.assertNotIn("<script>", html_text)
        self.assertIn("&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;", html_text)

        # Revenue Report JSON + HTML XSS (runs before headless PDF assertions)
        rev_resp = self.client.get(
            "/api/admin/reports/revenue",
            headers=admin_headers,
            params={"tu_ngay": "2026-09-01", "den_ngay": "2026-12-31"},
        )
        self.assertEqual(rev_resp.status_code, 200)
        rev = rev_resp.json()
        self.assertEqual(
            rev["summary"],
            {
                "tong_doanh_thu": 79110000,
                "so_don": 10,
                "so_khach": 26,
                "so_don_huy": 4,
            },
        )
        self.assertIs(type(rev["summary"]["tong_doanh_thu"]), int)
        self.assertEqual(rev["noi_nhan"], "Ban Giám đốc công ty du lịch")
        rollup = next(t for t in rev["tours"] if t["ma_tour"] == "TỔNG CỘNG")
        self.assertEqual(rollup["diem_tour_tb"], 4.5)
        self.assertIs(type(rollup["diem_tour_tb"]), float)
        self.assertGreater(len(rev["accommodations"]), 0)

        # Invalid report date range -> 400
        bad_range = self.client.get(
            "/api/admin/reports/revenue",
            headers=admin_headers,
            params={"tu_ngay": "2026-12-31", "den_ngay": "2026-09-01"},
        )
        self.assertEqual(bad_range.status_code, 400)

        # Empty nguoi_lap rejected with 400
        bad_rev_pdf = self.client.post(
            "/api/admin/reports/revenue/pdf",
            headers=admin_headers,
            json={"tu_ngay": "2026-09-01", "den_ngay": "2026-12-31", "nguoi_lap": "   "},
        )
        self.assertEqual(bad_rev_pdf.status_code, 400)

        # Revenue HTML escapes XSS
        rev_html_resp = self.client.post(
            "/api/admin/reports/revenue/html",
            headers=admin_headers,
            json={
                "tu_ngay": "2026-09-01",
                "den_ngay": "2026-12-31",
                "nguoi_lap": xss_issuer,
            },
        )
        self.assertEqual(rev_html_resp.status_code, 200)
        rev_html = rev_html_resp.json()["html"]
        self.assertNotIn("<script>", rev_html)
        self.assertIn("&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;", rev_html)

        # Confirmation PDF (Admin for DH007, Owner KH007 for DH008) -> real 1-page A4 PDF
        for ma_don, hdrs in (
            ("DH007", admin_headers),
            ("DH008", {"X-Customer-Token": kh007_token}),
        ):
            with self.subTest(ma_don=ma_don):
                pdf_resp = self.client.get(
                    f"/api/orders/{ma_don}/confirmation/pdf",
                    headers=hdrs,
                    params={"nguoi_lap": "Nguyễn Quốc Khánh"},
                )
                self.assertEqual(pdf_resp.status_code, 200)
                self.assertEqual(pdf_resp.headers["content-type"], "application/pdf")
                self.assertTrue(pdf_resp.content.startswith(b"%PDF-"))
                self.assertEqual(_count_pdf_pages(pdf_resp.content), 1)

        # Revenue PDF returns real 1-page A4 landscape PDF
        rev_pdf_resp = self.client.post(
            "/api/admin/reports/revenue/pdf",
            headers=admin_headers,
            json={
                "tu_ngay": "2026-09-01",
                "den_ngay": "2026-12-31",
                "nguoi_lap": "Nguyễn Quốc Khánh",
            },
        )
        self.assertEqual(rev_pdf_resp.status_code, 200)
        self.assertEqual(rev_pdf_resp.headers["content-type"], "application/pdf")
        self.assertTrue(rev_pdf_resp.content.startswith(b"%PDF-"))
        self.assertEqual(_count_pdf_pages(rev_pdf_resp.content), 1)


if __name__ == "__main__":
    unittest.main()
