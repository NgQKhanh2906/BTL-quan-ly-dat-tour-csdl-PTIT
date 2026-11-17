import sys
from datetime import datetime, timedelta
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_ngay, dinh_dang_tien, hien_tai, thong_bao_loi
from services import (
    kiem_tra_dat_tour,
    kiem_tra_trung_khach_hang,
    lay_ds_khach_hang_f1,
    lay_lich_trinh_con_cho,
    lay_noi_nghi_theo_tinh,
    luu_dat_tour,
    tinh_du_toan_f1,
)

st.set_page_config(page_title="F1 - Đặt tour", layout="wide")

st.title("F1. Form tiếp nhận và đặt tour du lịch")
st.caption(
    "Điền thông tin khách hàng, chọn lịch trình, số khách, nơi nghỉ theo tỉnh đến và đăng ký xe trung chuyển."
)

flash_success = st.session_state.pop("f1_flash_success", None)
if flash_success:
    st.success(flash_success)

moc_hien_tai = hien_tai()

# F1.2: Nạp danh sách lịch trình chưa khởi hành và còn chỗ
try:
    ds_lich_trinh = lay_lich_trinh_con_cho(moc_hien_tai)
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_lich_trinh:
    st.warning("Hiện tại không có lịch trình nào còn chỗ và chưa khởi hành.")
    st.stop()

# ----------------- 1. THÔNG TIN KHÁCH HÀNG -----------------
st.subheader("1. Thông tin khách hàng")

loai_khach = st.radio(
    "Hình thức khách hàng",
    ["Khách hàng có sẵn", "Khách hàng mới"],
    horizontal=True,
    key="f1_loai_khach",
)

ma_kh = None
la_khach_moi = loai_khach == "Khách hàng mới"
ho_ten_chot = ""
sdt_chot = ""
email_chot = ""
dia_chi_mac_dinh = ""
kh_trung = None

if not la_khach_moi:
    try:
        ds_kh = lay_ds_khach_hang_f1()
    except Exception as loi:
        st.error(thong_bao_loi(loi))
        st.stop()

    if not ds_kh:
        st.warning(
            "Hiện chưa có khách hàng nào trong hệ thống. Vui lòng chuyển sang mục 'Khách hàng mới'."
        )
        st.stop()

    kh_chon = st.selectbox(
        "Khách hàng (*)",
        ds_kh,
        format_func=lambda r: r["HienThi"],
        key="f1_chon_kh",
    )
    ma_kh = kh_chon["MaKH"]
    ho_ten_chot = kh_chon["HoTen"]
    email_chot = kh_chon["Email"]
    dia_chi_mac_dinh = kh_chon.get("DiaChi") or ""
    sdt_hien_thi = kh_chon.get("SoDienThoai") or "Chưa cập nhật"

    st.info(
        f"**Mã KH:** `{ma_kh}` | **Họ tên:** {ho_ten_chot} | "
        f"**Email:** {email_chot} | **SĐT:** {sdt_hien_thi} | "
        f"**Địa chỉ:** {dia_chi_mac_dinh if dia_chi_mac_dinh else 'Chưa cập nhật'}"
    )
else:
    c_ten, c_sdt = st.columns(2)
    with c_ten:
        ho_ten_nhap = st.text_input(
            "Họ và tên khách hàng (*)",
            placeholder="Ví dụ: Nguyễn Minh Tuấn",
            max_chars=100,
            key="f1_kh_ten",
        )
    with c_sdt:
        sdt_nhap = st.text_input(
            "Số điện thoại (10 chữ số) (*)",
            placeholder="Ví dụ: 0912345678",
            max_chars=10,
            key="f1_kh_sdt",
        )

    c_email, c_dc = st.columns(2)
    with c_email:
        email_nhap = st.text_input(
            "Email (*)",
            placeholder="Ví dụ: tuan.nguyen@gmail.com",
            max_chars=100,
            key="f1_kh_email",
        )
    with c_dc:
        dia_chi_nhap = st.text_input(
            "Địa chỉ liên hệ (*)",
            placeholder="Ví dụ: 15 Phố Huế, Hà Nội",
            max_chars=255,
            key="f1_kh_diachi",
        )

    ho_ten_chot = ho_ten_nhap.strip()
    sdt_chot = sdt_nhap.strip()
    email_chot = email_nhap.strip()
    dia_chi_mac_dinh = dia_chi_nhap.strip()

    if email_chot or sdt_chot:
        try:
            kh_trung = kiem_tra_trung_khach_hang(email_chot, sdt_chot)
        except Exception as loi:
            st.error(thong_bao_loi(loi))
            st.stop()

    if kh_trung is not None:
        st.warning(
            f"Email hoặc số điện thoại đã thuộc về khách hàng {kh_trung['MaKH']} - {kh_trung['HoTen']} "
            f"({kh_trung['Email']} | SĐT: {kh_trung['CacSDT'] or 'Chưa có'}). "
            "Vui lòng chuyển sang mục 'Khách hàng có sẵn' để đặt đơn cho khách hàng này."
        )
    else:
        st.caption(
            "Khách hàng mới sẽ được lưu vào hệ thống cùng đơn đặt tour khi bấm xác nhận."
        )

# ----------------- 2. THÔNG TIN CHUYẾN ĐI -----------------
st.markdown("---")
st.subheader("2. Thông tin chuyến đi")

lt_chon = st.selectbox(
    "Lịch trình còn chỗ (*)",
    ds_lich_trinh,
    format_func=lambda r: (
        f"{r['MaLichTrinh']} | {r['TenTour']} | Khởi hành: {dinh_dang_ngay(r['NgayXuatPhat'])} "
        f"| Giá: {dinh_dang_tien(r['GiaCoBan'])} | Còn: {r['SoChoConLai']} chỗ"
    ),
    key="f1_chon_lich_trinh",
    help="Chỉ liệt kê các lịch trình chưa khởi hành và còn chỗ",
)

ma_lich_trinh = lt_chon["MaLichTrinh"]
so_cho_con_lai = int(lt_chon["SoChoConLai"])
so_dem = int(lt_chon["SoDem"])
ma_tinh_den = lt_chon["MaTinhDen"]
ngay_xuat_phat = lt_chon["NgayXuatPhat"]
ngay_ket_thuc = lt_chon["NgayKetThuc"]
gia_co_ban = int(lt_chon["GiaCoBan"])

col_sk, col_nn, col_sp = st.columns([1, 2, 1])

with col_sk:
    so_khach = st.number_input(
        "Số lượng khách (*)",
        min_value=1,
        max_value=max(1, so_cho_con_lai),
        value=1,
        step=1,
        key=f"f1_so_khach_{ma_lich_trinh}",
        help=f"Từ 1 đến số chỗ còn lại của chuyến ({so_cho_con_lai} chỗ).",
    )

ma_nha_nghi = None
gia_phong_moi_dem = 0
so_phong = 0

if so_dem == 0:
    with col_nn:
        st.info("Tour trong ngày (0 đêm): không áp dụng đặt nơi nghỉ và xe về nơi nghỉ.")
    with col_sp:
        st.caption("Số phòng: 0")
else:
    try:
        ds_noi_nghi = lay_noi_nghi_theo_tinh(ma_tinh_den)
    except Exception as loi:
        st.error(thong_bao_loi(loi))
        st.stop()

    cac_lua_chon_nn = [
        {
            "MaNhaNghi": None,
            "TenNhaNghi": "Không đặt nơi nghỉ",
            "LoaiHinh": "",
            "GiaPhongMoiDem": 0,
        }
    ] + ds_noi_nghi

    with col_nn:
        nn_chon = st.selectbox(
            "Nơi nghỉ (lọc theo tỉnh đến)",
            cac_lua_chon_nn,
            format_func=lambda r: (
                "Không đặt nơi nghỉ"
                if r["MaNhaNghi"] is None
                else (
                    f"{r['MaNhaNghi']} - {r['TenNhaNghi']} ({r['LoaiHinh']}) "
                    f"- {dinh_dang_tien(r['GiaPhongMoiDem'])}/đêm"
                )
            ),
            key=f"f1_noi_nghi_{ma_lich_trinh}",
            help="Tự động lọc nhà nghỉ, homestay tại đúng tỉnh điểm đến của tour",
        )
        ma_nha_nghi = nn_chon["MaNhaNghi"]
        gia_phong_moi_dem = int(nn_chon["GiaPhongMoiDem"])

    with col_sp:
        if ma_nha_nghi is not None:
            so_phong = st.number_input(
                "Số phòng (*)",
                min_value=1,
                value=1,
                step=1,
                key=f"f1_so_phong_{ma_lich_trinh}",
                help="Số phòng phải từ 1 đến số khách",
            )
        else:
            so_phong = 0
            st.caption("Số phòng: 0")

# ----------------- 3. XE TRUNG CHUYỂN -----------------
st.markdown("---")
st.subheader("3. Đăng ký xe trung chuyển (tối đa 2 chuyến)")
col_xe1, col_xe2 = st.columns(2)

nguon_dia_chi = (
    ("moi", dia_chi_mac_dinh)
    if la_khach_moi
    else ("co_san", ma_kh, dia_chi_mac_dinh)
)

with col_xe1:
    co_xe_don = st.checkbox(
        "Cần xe đón tại nhà",
        value=False,
        key=f"f1_co_xe_don_{ma_lich_trinh}",
    )
    dia_chi_don = ""
    dt_don = None
    if co_xe_don:
        key_dia_chi_don = f"f1_dia_chi_don_{ma_lich_trinh}"
        key_nguon_dia_chi = f"f1_nguon_dia_chi_{ma_lich_trinh}"
        if (
            key_dia_chi_don not in st.session_state
            or st.session_state.get(key_nguon_dia_chi) != nguon_dia_chi
        ):
            st.session_state[key_dia_chi_don] = dia_chi_mac_dinh
            st.session_state[key_nguon_dia_chi] = nguon_dia_chi

        dia_chi_don = st.text_input(
            "Địa chỉ đón (*)",
            max_chars=255,
            placeholder="Nhập địa chỉ đón khách",
            key=key_dia_chi_don,
        )
        thoi_gian_mac_dinh_don = ngay_xuat_phat - timedelta(hours=2)
        c_ngay_don, c_gio_don = st.columns(2)
        with c_ngay_don:
            ngay_don = st.date_input(
                "Ngày đón (*)",
                value=thoi_gian_mac_dinh_don.date(),
                key=f"f1_ngay_don_{ma_lich_trinh}",
            )
        with c_gio_don:
            gio_don = st.time_input(
                "Giờ đón (*)",
                value=thoi_gian_mac_dinh_don.time().replace(second=0, microsecond=0),
                key=f"f1_gio_don_{ma_lich_trinh}",
            )
        if ngay_don is not None and gio_don is not None:
            dt_don = datetime.combine(ngay_don, gio_don)
        else:
            st.info("Vui lòng chọn đầy đủ ngày và giờ đón tại nhà.")

with col_xe2:
    co_xe_ve = False
    dt_ve = None
    if so_dem > 0 and ma_nha_nghi is not None:
        co_xe_ve = st.checkbox(
            "Cần xe về nơi nghỉ",
            value=False,
            key=f"f1_co_xe_ve_{ma_lich_trinh}",
        )
        if co_xe_ve:
            thoi_gian_mac_dinh_ve = ngay_xuat_phat + timedelta(hours=4)
            if thoi_gian_mac_dinh_ve > ngay_ket_thuc:
                thoi_gian_mac_dinh_ve = ngay_xuat_phat
            c_ngay_ve, c_gio_ve = st.columns(2)
            with c_ngay_ve:
                ngay_ve = st.date_input(
                    "Ngày về nơi nghỉ (*)",
                    value=thoi_gian_mac_dinh_ve.date(),
                    key=f"f1_ngay_ve_{ma_lich_trinh}",
                )
            with c_gio_ve:
                gio_ve = st.time_input(
                    "Giờ về nơi nghỉ (*)",
                    value=thoi_gian_mac_dinh_ve.time().replace(second=0, microsecond=0),
                    key=f"f1_gio_ve_{ma_lich_trinh}",
                )
            if ngay_ve is not None and gio_ve is not None:
                dt_ve = datetime.combine(ngay_ve, gio_ve)
            else:
                st.info("Vui lòng chọn đầy đủ ngày và giờ về nơi nghỉ.")
    elif so_dem == 0:
        st.info("Tour trong ngày (0 đêm) không áp dụng chuyến xe về nơi nghỉ.")
    else:
        st.info("Chuyến xe về nơi nghỉ chỉ áp dụng khi khách có đăng ký nơi nghỉ.")

# ----------------- 4. DỰ TOÁN VÀ XÁC NHẬN -----------------
st.markdown("---")
co_nha_nghi = ma_nha_nghi is not None
tien_tour, tien_phong, tong_tien_du_kien = tinh_du_toan_f1(
    so_khach=int(so_khach),
    gia_co_ban=gia_co_ban,
    so_phong=int(so_phong),
    gia_phong_moi_dem=gia_phong_moi_dem,
    so_dem=so_dem,
    co_nha_nghi=co_nha_nghi,
)

st.subheader("4. Dự toán chi phí và Xác nhận")
m1, m2, m3 = st.columns(3)
m1.metric(
    "Tiền tour cơ bản",
    dinh_dang_tien(tien_tour),
    f"{int(so_khach)} khách x {dinh_dang_tien(gia_co_ban)}",
)
m2.metric(
    "Tiền phòng lưu trú",
    dinh_dang_tien(tien_phong),
    f"{int(so_phong)} phòng x {so_dem} đêm x {dinh_dang_tien(gia_phong_moi_dem)}"
    if co_nha_nghi
    else "Không đặt nơi nghỉ",
)
m3.metric("TỔNG TIỀN DỰ KIẾN", dinh_dang_tien(tong_tien_du_kien))

if st.button("Xác nhận đặt tour", type="primary", width="stretch"):
    ds_loi = kiem_tra_dat_tour(
        la_khach_moi=la_khach_moi,
        ma_kh=ma_kh,
        ho_ten=ho_ten_chot,
        so_dien_thoai=sdt_chot,
        email=email_chot,
        dia_chi=dia_chi_mac_dinh,
        so_khach=int(so_khach),
        so_cho_con_lai=so_cho_con_lai,
        so_dem=so_dem,
        co_nha_nghi=co_nha_nghi,
        so_phong=int(so_phong),
        co_xe_don=co_xe_don,
        dia_chi_don=dia_chi_don,
        dt_don=dt_don,
        co_xe_ve=co_xe_ve,
        dt_ve=dt_ve,
        thoi_diem_hien_tai=moc_hien_tai,
        ngay_xuat_phat=ngay_xuat_phat,
        ngay_ket_thuc=ngay_ket_thuc,
    )

    if la_khach_moi and kh_trung is not None:
        ds_loi.append(
            f"Email hoặc số điện thoại đã thuộc về khách hàng {kh_trung['MaKH']} - {kh_trung['HoTen']}. "
            "Vui lòng chọn ở mục 'Khách hàng có sẵn'."
        )

    if ds_loi:
        for msg in ds_loi:
            st.error(msg)
    else:
        du_lieu_luu = {
            "LaKhachMoi": la_khach_moi,
            "MaKH": ma_kh,
            "HoTen": ho_ten_chot,
            "Email": email_chot,
            "SoDienThoai": sdt_chot,
            "DiaChi": dia_chi_mac_dinh,
            "MaLichTrinh": ma_lich_trinh,
            "SoKhach": int(so_khach),
            "MaNhaNghi": ma_nha_nghi,
            "SoPhong": int(so_phong) if co_nha_nghi else 0,
            "DiaChiDon": dia_chi_don.strip() if co_xe_don else None,
            "GioDon": dt_don if co_xe_don else None,
            "GioVeNoiNghi": dt_ve if co_xe_ve else None,
            "NgayDat": moc_hien_tai,
        }
        try:
            ma_don_moi = luu_dat_tour(du_lieu_luu)
            st.session_state["f1_flash_success"] = (
                f"Đã tạo đơn {ma_don_moi}, tổng tiền {dinh_dang_tien(tong_tien_du_kien)}"
            )
            for khoa in (
                "f1_chon_lich_trinh",
                "f1_chon_kh",
                "f1_loai_khach",
                "f1_kh_ten",
                "f1_kh_sdt",
                "f1_kh_email",
                "f1_kh_diachi",
                f"f1_so_khach_{ma_lich_trinh}",
                f"f1_noi_nghi_{ma_lich_trinh}",
                f"f1_so_phong_{ma_lich_trinh}",
                f"f1_co_xe_don_{ma_lich_trinh}",
                f"f1_dia_chi_don_{ma_lich_trinh}",
                f"f1_nguon_dia_chi_{ma_lich_trinh}",
                f"f1_ngay_don_{ma_lich_trinh}",
                f"f1_gio_don_{ma_lich_trinh}",
                f"f1_co_xe_ve_{ma_lich_trinh}",
                f"f1_ngay_ve_{ma_lich_trinh}",
                f"f1_gio_ve_{ma_lich_trinh}",
            ):
                st.session_state.pop(khoa, None)
            st.rerun()
        except Exception as loi:
            st.error(thong_bao_loi(loi))
