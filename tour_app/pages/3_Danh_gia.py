import sys
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_ngay, dinh_dang_tien, hien_tai, thong_bao_loi
from services import kiem_tra_danh_gia, lay_don_cho_danh_gia, lay_ds_khach_hang, luu_danh_gia

st.set_page_config(page_title="F3 - Đánh giá sau chuyến đi", layout="wide")
st.title("F3. Đánh giá chất lượng tour và nhà nghỉ sau chuyến đi")
st.caption(
    "Chỉ những đơn hàng ở trạng thái Hoàn thành (HOANTHANH) và chưa từng đánh giá "
    "mới được phép gửi điểm và nhận xét."
)

flash_success = st.session_state.pop("f3_flash_success", None)
if flash_success:
    st.success(flash_success)

try:
    ds_kh = lay_ds_khach_hang()
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_kh:
    st.info("Hiện chưa có khách hàng nào trong hệ thống.")
    st.stop()

chon_kh = st.selectbox(
    "1. Chọn khách hàng",
    ds_kh,
    key="f3_chon_kh",
    format_func=lambda r: f"{r['MaKH']} - {r['HoTen']} ({r['Email']})",
)

# F3.1: Nap danh sach cac don HOANTHANH chua danh gia cua khach hang
try:
    ds_don_ht = lay_don_cho_danh_gia(chon_kh["MaKH"])
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_don_ht:
    st.info(
        f"Khách hàng **{chon_kh['HoTen']}** (`{chon_kh['MaKH']}`) hiện không có chuyến đi nào "
        f"ở trạng thái Hoàn thành đang chờ đánh giá (hoặc tất cả các chuyến hoàn thành đã được đánh giá)."
    )
    st.stop()

chon_don = st.selectbox(
    "2. Chọn chuyến đi đã hoàn thành cần đánh giá",
    ds_don_ht,
    key="f3_chon_don",
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['TenTour']} "
        f"({dinh_dang_ngay(r['NgayXuatPhat'])} -> {dinh_dang_ngay(r['NgayKetThuc'])}) "
        f"| {dinh_dang_tien(r['TongTien'])}"
    ),
)

ma_don = chon_don["MaDonHang"]

st.info(
    f"**Mã đơn:** `{ma_don}` | **Tour:** {chon_don['TenTour']} (`{chon_don['MaTour']}`)  \n"
    f"**Hành trình:** {dinh_dang_ngay(chon_don['NgayXuatPhat'])} đến "
    f"{dinh_dang_ngay(chon_don['NgayKetThuc'])} | "
    f"**Nhà nghỉ lưu trú:** {chon_don['TenNhaNghi'] if chon_don['MaNhaNghi'] else 'Không sử dụng nhà nghỉ'}"
)

st.divider()
col_tour, col_nn = st.columns(2)

with col_tour:
    st.subheader("Đánh giá chương trình Tour (*)")
    diem_tour = st.slider(
        "Điểm đánh giá tour (1 = Rất tệ, 5 = Rất hài lòng)",
        min_value=1,
        max_value=5,
        value=5,
        key=f"f3_diem_tour_{ma_don}",
    )
    nhan_xet_tour = st.text_area(
        "Nhận xét về chương trình tour (Tùy chọn, tối đa 500 ký tự)",
        max_chars=500,
        placeholder="Chia sẻ cảm nhận về lịch trình, hướng dẫn viên, phương tiện di chuyển...",
        key=f"f3_nx_tour_{ma_don}",
    )

with col_nn:
    st.subheader("Đánh giá Nhà nghỉ / Khách sạn")
    if chon_don["MaNhaNghi"]:
        co_dg_nn = st.checkbox(
            f"Tôi muốn chấm điểm cho {chon_don['TenNhaNghi']} ({chon_don['MaNhaNghi']})",
            value=True,
            key=f"f3_co_dg_nn_{ma_don}",
        )
        if co_dg_nn:
            diem_nn = st.slider(
                "Điểm đánh giá nhà nghỉ (1 - 5 sao)",
                min_value=1,
                max_value=5,
                value=4,
                key=f"f3_diem_nn_{ma_don}",
            )
        else:
            diem_nn = None
        nhan_xet_nn = st.text_area(
            "Nhận xét về nhà nghỉ (Tùy chọn, tối đa 500 ký tự)",
            max_chars=500,
            placeholder="Chia sẻ cảm nhận về phòng ốc, vệ sinh, thái độ phục vụ...",
            key=f"f3_nx_nn_{ma_don}",
        )
    else:
        st.caption(
            "Đơn hàng này không đăng ký dịch vụ nhà nghỉ (`MaNhaNghi IS NULL`), "
            "do đó phần đánh giá nhà nghỉ được tự động ẩn theo ràng buộc `chk_DonHang_DanhGiaNhaNghi`."
        )
        diem_nn = None
        nhan_xet_nn = ""

if st.button("Gửi đánh giá chuyến đi", type="primary"):
    co_nha_nghi = bool(chon_don["MaNhaNghi"])
    ds_loi, nx_tour_val, diem_nn_val, nx_nn_val = kiem_tra_danh_gia(
        diem_tour,
        nhan_xet_tour,
        co_nha_nghi,
        diem_nn,
        nhan_xet_nn,
    )
    if ds_loi:
        for msg in ds_loi:
            st.error(msg)
    else:
        ngay_dg = hien_tai()
        try:
            # F3.2: Ghi đánh giá vào CSDL thông qua services.luu_danh_gia
            luu_danh_gia(
                ma_don,
                int(diem_tour),
                nx_tour_val,
                diem_nn_val,
                nx_nn_val,
                ngay_dg,
            )
            st.session_state["f3_flash_success"] = (
                f"Đã ghi nhận đánh giá cho đơn `{ma_don}` "
                f"(Điểm tour: {int(diem_tour)}/5 sao"
                f"{f', Điểm nhà nghỉ: {diem_nn_val}/5 sao' if diem_nn_val is not None else ''}) "
                f"vào lúc {dinh_dang_ngay(ngay_dg)}!"
            )
            st.session_state.pop("f3_chon_don", None)
            st.rerun()
        except Exception as loi:
            st.error(thong_bao_loi(loi))
