import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_ngay, dinh_dang_tien, hien_tai, thong_bao_loi
from services import (
    chuyen_trang_thai_don,
    huy_don,
    kiem_tra_huy_don,
    lay_chi_tiet_don_f2,
    lay_don_dang_mo,
    lay_trang_thai_dich_f2,
    tinh_xem_truoc_phat_huy,
)

st.set_page_config(page_title="F2 - Quản lý đơn & hủy tour", layout="wide")
st.title("F2. Cập nhật trạng thái và hủy đơn đặt tour")
st.caption(
    "Chuyển trạng thái đơn theo đúng quy trình (DAT -> THANHTOAN -> HOANTHANH) "
    "hoặc hủy đơn kèm tính phí phạt tự động và hoàn trả chỗ cho lịch trình."
)

flash_success = st.session_state.pop("f2_flash_success", None)
if flash_success:
    st.success(flash_success)

# F2.1: Nap danh sach cac don hang dang o trang thai DAT hoac THANHTOAN
try:
    ds_don = lay_don_dang_mo()
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_don:
    st.info("Hiện không có đơn hàng nào ở trạng thái chờ xử lý (DAT hoặc THANHTOAN).")
    st.stop()

chon_don = st.selectbox(
    "Chọn đơn hàng cần xử lý",
    ds_don,
    key="f2_chon_don",
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['HoTen']} | {r['TenTour']} "
        f"(Khởi hành: {dinh_dang_ngay(r['NgayXuatPhat'])}) | {r['TenTrangThai']}"
    ),
)

# F2.2: Xem chi tiet don hang dang chon
try:
    ct = lay_chi_tiet_don_f2(chon_don["MaDonHang"])
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if ct is None:
    st.error("Không tìm thấy thông tin chi tiết đơn hàng.")
    st.stop()

ma_don = ct["MaDonHang"]

c1, c2, c3 = st.columns(3)
c1.markdown(
    f"**Mã đơn:** `{ma_don}`  \n"
    f"**Khách hàng:** {ct['HoTen']} (`{ct['MaKH']}`)  \n"
    f"**Ngày đặt:** {dinh_dang_ngay(ct['NgayDat'])}"
)
c2.markdown(
    f"**Lịch trình:** `{ct['MaLichTrinh']}` ({dinh_dang_ngay(ct['NgayXuatPhat'])} -> {dinh_dang_ngay(ct['NgayKetThuc'])})  \n"
    f"**Số khách:** {int(ct['SoLuongKhach'])} | **Số phòng:** {int(ct['SoPhong'])}  \n"
    f"**Nơi nghỉ:** `{ct['TenNhaNghi'] if ct['TenNhaNghi'] else 'Không sử dụng'}`"
)
c3.markdown(
    f"**Tiền tour:** {dinh_dang_tien(ct['TienTour'])}  \n"
    f"**Tiền phòng:** {dinh_dang_tien(ct['TienPhong'])}  \n"
    f"**Tổng tiền:** **{dinh_dang_tien(ct['TongTien'])}**  \n"
    f"**Trạng thái hiện tại:** `{ct['TenTrangThai']}`"
)

st.divider()

# F2.3: Nap danh sach trang thai dich hop le
moc_hien_tai = hien_tai()
try:
    ds_tt_moi = lay_trang_thai_dich_f2(ma_don, moc_hien_tai)
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_tt_moi:
    st.info("Đơn hàng hiện không có trạng thái mới hợp lệ để chuyển.")
    st.stop()

tt_moi = st.selectbox(
    "Chọn trạng thái mới",
    ds_tt_moi,
    key=f"f2_tt_moi_{ma_don}",
    format_func=lambda r: f"{r['TenTrangThai']} ({r['MaTrangThai']})",
)

if tt_moi["MaTrangThai"] == "HUY":
    st.subheader("Thông tin hủy tour và tính phí phạt tự động")
    col_d, col_t = st.columns(2)
    ngay_huy_d = col_d.date_input(
        "Ngày hủy",
        value=moc_hien_tai.date(),
        key=f"f2_ngay_huy_{ma_don}",
    )
    gio_huy_t = col_t.time_input(
        "Giờ hủy",
        value=moc_hien_tai.time().replace(second=0, microsecond=0),
        key=f"f2_gio_huy_{ma_don}",
    )
    ly_do_huy = st.text_input(
        "Lý do hủy tour (*)",
        max_chars=255,
        placeholder="Ví dụ: Khách bận công tác đột xuất, xin hủy đơn",
        key=f"f2_ly_do_huy_{ma_don}",
    )

    if ngay_huy_d is None or gio_huy_t is None:
        st.info("Vui lòng chọn đầy đủ ngày và giờ hủy.")
        st.stop()

    ngay_gio_huy = datetime.combine(ngay_huy_d, gio_huy_t)

    # F2.4: Tinh xem truoc muc phat huy tour
    try:
        xem_truoc = tinh_xem_truoc_phat_huy(ma_don, ngay_gio_huy)
    except Exception as loi:
        st.error(thong_bao_loi(loi))
        st.stop()

    if xem_truoc is None:
        st.error("Không tính được mức phạt hủy cho đơn hàng này.")
        st.stop()

    phi_phat = int(xem_truoc["TienPhat"])
    tien_hoan = int(xem_truoc["TienHoan"])

    st.warning(
        f"**Xem trước kết quả tính phí phạt hủy tour:**  \n"
        f"- Thời gian từ lúc đặt đến lúc hủy: **{int(xem_truoc['SoGioSauKhiDat'])} giờ**  \n"
        f"- Số ngày trước ngày khởi hành (`{dinh_dang_ngay(ct['NgayXuatPhat'])}`): "
        f"**{int(xem_truoc['SoNgayTruocKhoiHanh'])} ngày**  \n"
        f"- Mức phạt áp dụng: **{int(xem_truoc['TyLePhat'])}%**  \n"
        f"- Phí phạt hủy: **{dinh_dang_tien(phi_phat)}**  \n"
        f"- Số tiền hoàn lại cho khách: **{dinh_dang_tien(tien_hoan)}**"
    )

    dong_y_phat = st.checkbox(
        "Khách đã đồng ý mức phạt",
        value=False,
        key=f"f2_dong_y_phat_{ma_don}",
    )

    if st.button("Xác nhận hủy đơn hàng", type="primary"):
        loi_kiem_tra = kiem_tra_huy_don(
            ct["NgayDat"],
            ct["NgayXuatPhat"],
            ngay_gio_huy,
            ly_do_huy,
            dong_y_phat,
        )
        if loi_kiem_tra:
            for msg in loi_kiem_tra:
                st.error(msg)
        else:
            # F2.5: Giao dich 3 cau lenh nguyen tu khi huy don
            try:
                huy_don(ma_don, ngay_gio_huy, ly_do_huy)
                st.session_state["f2_flash_success"] = (
                    f"Đã hủy đơn `{ma_don}` thành công! "
                    f"Phí phạt: {dinh_dang_tien(phi_phat)}, "
                    f"đã hoàn trả {int(ct['SoLuongKhach'])} chỗ cho lịch trình `{ct['MaLichTrinh']}`."
                )
                st.session_state.pop("f2_chon_don", None)
                st.session_state.pop(f"f2_tt_moi_{ma_don}", None)
                st.rerun()
            except Exception as loi:
                st.error(thong_bao_loi(loi))
else:
    if st.button("Cập nhật trạng thái đơn hàng", type="primary"):
        # F2.6: Chuyen trang thai thuong
        try:
            chuyen_trang_thai_don(ma_don, tt_moi["MaTrangThai"], moc_hien_tai)
            st.session_state["f2_flash_success"] = (
                f"Đã chuyển đơn `{ma_don}` sang trạng thái "
                f"`{tt_moi['TenTrangThai']}` thành công!"
            )
            st.session_state.pop("f2_chon_don", None)
            st.session_state.pop(f"f2_tt_moi_{ma_don}", None)
            st.rerun()
        except Exception as loi:
            st.error(thong_bao_loi(loi))
