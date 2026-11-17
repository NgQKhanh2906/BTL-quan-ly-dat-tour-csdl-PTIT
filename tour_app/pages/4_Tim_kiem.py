import sys
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_ngay, dinh_dang_tien, hien_tai, thong_bao_loi
from services import lay_ds_tinh_thanh, tim_kiem_lich_trinh

st.set_page_config(page_title="S1 - Tìm kiếm lịch trình", layout="wide")

st.title("S1. Tra cứu và tìm kiếm lịch trình tour")
st.caption(
    "Tìm kiếm lịch trình theo từ khóa, điểm đến, khoảng giá, ngày khởi hành, số chỗ và điểm đánh giá."
)


def _mac_dinh_bo_loc() -> dict:
    ngay_mac_dinh = hien_tai().date()
    return {
        "s1_tu_khoa": "",
        "s1_tinh_den": "Tất cả",
        "s1_gia_tu": 0,
        "s1_gia_den": 0,
        "s1_tu_ngay": ngay_mac_dinh,
        "s1_co_den_ngay": False,
        "s1_den_ngay": ngay_mac_dinh,
        "s1_so_khach": 1,
        "s1_diem": "Tất cả",
    }


def _khoi_tao_bo_loc() -> None:
    for khoa, gia_tri in _mac_dinh_bo_loc().items():
        if khoa not in st.session_state:
            st.session_state[khoa] = gia_tri


def _ap_dung_bo_loc_mac_dinh(gia_tu: int = 0) -> None:
    for khoa, gia_tri in _mac_dinh_bo_loc().items():
        st.session_state[khoa] = gia_tri
    st.session_state["s1_gia_tu"] = gia_tu


def _dat_bo_loc_cao_cap() -> None:
    _ap_dung_bo_loc_mac_dinh(gia_tu=10000000)


def _dat_lai_bo_loc() -> None:
    _ap_dung_bo_loc_mac_dinh(gia_tu=0)


# Khởi tạo đầy đủ khóa session_state cho 8 bộ lọc (9 widget keys)
_khoi_tao_bo_loc()

col_btn1, col_btn2 = st.columns([2, 8])
with col_btn1:
    st.button(
        "Tour cao cấp (từ 10 triệu)",
        key="s1_btn_cao_cap",
        width="stretch",
        on_click=_dat_bo_loc_cao_cap,
    )

with col_btn2:
    st.button(
        "Đặt lại bộ lọc",
        key="s1_btn_dat_lai",
        on_click=_dat_lai_bo_loc,
    )

st.markdown("---")

# S1.1: Nạp danh sách tỉnh thành
try:
    ds_tinh = lay_ds_tinh_thanh()
    danh_sach_tinh = ["Tất cả"] + [f"{t['MaTinh']} - {t['TenTinh']}" for t in ds_tinh]
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if st.session_state["s1_tinh_den"] not in danh_sach_tinh:
    st.session_state["s1_tinh_den"] = "Tất cả"

# 8 bộ lọc chia làm 2 hàng (dùng key= không truyền value=/index= để tránh xung đột session_state)
r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
with r1_c1:
    tu_khoa = st.text_input(
        "1. Từ khóa tên tour",
        max_chars=100,
        placeholder="Ví dụ: Hạ Long, Sa Pa...",
        key="s1_tu_khoa",
    )
with r1_c2:
    tinh_den_chon = st.selectbox(
        "2. Tỉnh đến",
        danh_sach_tinh,
        key="s1_tinh_den",
    )
with r1_c3:
    gia_tu = st.number_input(
        "3. Giá từ (VNĐ)",
        min_value=0,
        step=500000,
        key="s1_gia_tu",
    )
with r1_c4:
    gia_den = st.number_input(
        "4. Giá đến (VNĐ - 0 là không giới hạn)",
        min_value=0,
        step=500000,
        key="s1_gia_den",
    )

r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1:
    tu_ngay = st.date_input(
        "5. Khởi hành từ ngày",
        key="s1_tu_ngay",
    )
with r2_c2:
    co_den_ngay = st.checkbox(
        "Lọc theo ngày đến",
        key="s1_co_den_ngay",
    )
    den_ngay = (
        st.date_input(
            "6. Khởi hành đến ngày",
            key="s1_den_ngay",
        )
        if co_den_ngay
        else None
    )
with r2_c3:
    so_khach = st.number_input(
        "7. Số khách",
        min_value=1,
        step=1,
        key="s1_so_khach",
    )
with r2_c4:
    diem_danh_gia = st.selectbox(
        "8. Điểm đánh giá tối thiểu",
        ["Tất cả", "3.0", "4.0", "4.5"],
        key="s1_diem",
    )

# Bảo vệ trường hợp người dùng xóa trống ô ngày trên giao diện
if tu_ngay is None:
    tu_ngay = hien_tai().date()
if co_den_ngay and den_ngay is None:
    den_ngay = tu_ngay

gia_tu_val = int(gia_tu) if gia_tu is not None else 0
gia_den_val = int(gia_den) if gia_den is not None else 0
so_khach_val = int(so_khach) if so_khach is not None else 1

# Kiểm tra ràng buộc hợp lệ của bộ lọc
if gia_den_val > 0 and gia_den_val < gia_tu_val:
    st.error("Giá đến phải lớn hơn hoặc bằng giá từ")
    st.stop()

if den_ngay is not None and den_ngay < tu_ngay:
    st.error("Khởi hành đến ngày phải lớn hơn hoặc bằng từ ngày")
    st.stop()

# Đóng gói tham số và thực thi S1.2
ma_tinh_tham_so = None
if tinh_den_chon != "Tất cả":
    ma_tinh_tham_so = tinh_den_chon.split(" - ")[0]

diem_tham_so = None
if diem_danh_gia != "Tất cả":
    diem_tham_so = float(diem_danh_gia)

tu_khoa_tham_so = (tu_khoa or "").strip() or None

try:
    ket_qua = tim_kiem_lich_trinh(
        tu_khoa=tu_khoa_tham_so,
        ma_tinh_den=ma_tinh_tham_so,
        gia_tu=gia_tu_val if gia_tu_val > 0 else None,
        gia_den=gia_den_val if gia_den_val > 0 else None,
        tu_ngay=tu_ngay,
        den_ngay=den_ngay,
        so_khach=so_khach_val,
        diem_toi_thieu=diem_tham_so,
    )
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

# Hiển thị kết quả
st.subheader(f"Kết quả tìm kiếm ({len(ket_qua)} lịch trình phù hợp)")

if not ket_qua:
    st.info("Không có lịch trình nào phù hợp với bộ lọc")
else:
    du_lieu_bang = []
    for r in ket_qua:
        diem_tb = r["DiemTB"]
        so_luot = r["SoLuotDanhGia"]
        danh_gia_str = f"{diem_tb} ({so_luot} lượt)" if diem_tb is not None else "Chưa có đánh giá"
        du_lieu_bang.append({
            "Mã LT": r["MaLichTrinh"],
            "Tên tour": r["TenTour"],
            "Lộ trình": f"{r['NoiDi']} -> {r['NoiDen']}",
            "Khởi hành": dinh_dang_ngay(r["NgayXuatPhat"]),
            "Thời lượng": f"{r['SoNgay']} ngày",
            "Giá cơ bản": dinh_dang_tien(r["GiaCoBan"]),
            "Chỗ trống": f"{r['SoChoConLai']} chỗ",
            "Đánh giá TB": danh_gia_str,
        })
    st.dataframe(du_lieu_bang, width="stretch")
