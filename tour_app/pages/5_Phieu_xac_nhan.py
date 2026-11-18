import sys
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_tien, hien_tai, thong_bao_loi
from services import (
    lay_chi_tiet_don_r1,
    lay_ds_don_r1,
    lay_lich_trung_chuyen_r1,
    lay_sdt_khach_r1,
    tao_html_phieu_xac_nhan,
)

st.set_page_config(page_title="R1 - Phiếu xác nhận đặt tour", layout="wide")
st.title("R1. Phiếu xác nhận đặt tour du lịch (Biểu mẫu in A4)")
st.caption(
    "Biểu mẫu do Nhân viên kinh doanh lập để giao cho Khách hàng xác nhận thông tin "
    "chuyến đi, lưu trú, xe trung chuyển, tổng chi phí hoặc thông tin hoàn tiền khi hủy."
)

# R1.1: Nạp danh sách toàn bộ đơn hàng
try:
    ds_don = lay_ds_don_r1()
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_don:
    st.info("Hiện không có đơn hàng nào trong hệ thống.")
    st.stop()

col1, col2 = st.columns([2, 1])
chon_don = col1.selectbox(
    "Chọn đơn hàng cần xuất phiếu xác nhận",
    ds_don,
    key="r1_chon_don",
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['HoTen']} | {r['TenTour']} "
        f"| {r['TenTrangThai']} | {dinh_dang_tien(r['TongTien'])}"
    ),
)
nguoi_lap = col2.text_input(
    "Nhân viên lập phiếu (*)",
    value="",
    max_chars=100,
    placeholder="Họ tên nhân viên kinh doanh",
    key="r1_nguoi_lap",
)
st.caption("Người nhận: Khách hàng đặt tour")

if not nguoi_lap.strip():
    st.warning("Nhập tên nhân viên lập phiếu để xem, tải và in phiếu.")
    st.stop()

ma_don = chon_don["MaDonHang"]

try:
    ct = lay_chi_tiet_don_r1(ma_don)
    if ct is None:
        st.error("Không tìm thấy thông tin đơn hàng.")
        st.stop()
    danh_sach_sdt = lay_sdt_khach_r1(ma_don)
    ds_ctc = lay_lich_trung_chuyen_r1(ma_don)
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

html_ket_qua = tao_html_phieu_xac_nhan(
    ct=ct,
    danh_sach_sdt=danh_sach_sdt,
    ds_ctc=ds_ctc,
    nguoi_lap=nguoi_lap,
    ngay_in=hien_tai(),
)

st.download_button(
    label="Tải phiếu xác nhận HTML (Khổ in A4 dọc)",
    data=html_ket_qua,
    file_name=f"phieu_xac_nhan_{ct['MaDonHang']}.html",
    mime="text/html",
    width="stretch",
)

st.iframe(html_ket_qua, height=960)
