import sys
from datetime import date
from pathlib import Path

import streamlit as st

_APP_DIR = str(Path(__file__).resolve().parent.parent)
if _APP_DIR not in sys.path:
    sys.path.insert(0, _APP_DIR)

from db import dinh_dang_tien, hien_tai, thong_bao_loi
from services import (
    NOI_NHAN_R2,
    lay_doanh_thu_tour_r2,
    lay_xep_hang_noi_nghi_r2,
    tao_html_bao_cao_doanh_thu,
)

st.set_page_config(page_title="R2 - Báo cáo doanh thu", layout="wide")

st.title("R2. Báo cáo tổng hợp doanh thu và đánh giá tour")
st.caption("Tổng hợp doanh thu, số đơn, số khách và điểm đánh giá theo từng tour du lịch và cơ sở lưu trú.")

# Bộ lọc kỳ báo cáo
col_ngay1, col_ngay2 = st.columns(2)
tu_ngay = col_ngay1.date_input(
    "Kỳ báo cáo từ ngày",
    value=date(2026, 9, 1),
    key="r2_tu_ngay",
)
den_ngay = col_ngay2.date_input(
    "Kỳ báo cáo đến ngày",
    value=date(2026, 12, 31),
    key="r2_den_ngay",
)

if tu_ngay is None or den_ngay is None:
    st.error("Vui lòng chọn đầy đủ từ ngày và đến ngày cho kỳ báo cáo")
    st.stop()

if den_ngay < tu_ngay:
    st.error("Kỳ báo cáo đến ngày phải lớn hơn hoặc bằng từ ngày")
    st.stop()

# Nhập người lập và hiển thị nơi nhận
nguoi_lap = st.text_input(
    "Người lập báo cáo",
    max_chars=100,
    placeholder="Họ tên nhân viên kế toán",
    key="r2_nguoi_lap",
)
st.caption(f"Nơi nhận: {NOI_NHAN_R2}")

# Thực thi truy vấn dữ liệu
try:
    ds_tour = lay_doanh_thu_tour_r2(tu_ngay, den_ngay)
    ds_noi_nghi = lay_xep_hang_noi_nghi_r2(tu_ngay, den_ngay)
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

# Tách dòng tổng cộng (ROLLUP)
dong_tong = next((r for r in ds_tour if r["MaTour"] == "TỔNG CỘNG"), None)

# 4 ô chỉ số tổng
st.markdown("### Chỉ số tổng quan")
m1, m2, m3, m4 = st.columns(4)
tong_dt = dong_tong["TongDoanhThu"] if dong_tong else 0
so_don = dong_tong["SoDon"] if dong_tong else 0
so_khach = dong_tong["SoKhach"] if dong_tong else 0
so_don_huy = dong_tong["SoDonHuy"] if dong_tong else 0

m1.metric("Tổng doanh thu", dinh_dang_tien(tong_dt))
m2.metric("Số đơn thành công", f"{so_don} đơn")
m3.metric("Số khách phục vụ", f"{so_khach} khách")
m4.metric("Số đơn đã hủy", f"{so_don_huy} đơn")

st.markdown("---")

# Bảng A: Doanh thu theo tour
st.subheader("A. Tổng hợp doanh thu theo tour")
if not ds_tour:
    st.info("Không có dữ liệu doanh thu trong kỳ báo cáo")
else:
    bang_tour_hien_thi = []
    for r in ds_tour:
        diem_tb = f"{r['DiemTourTB']} sao" if r["DiemTourTB"] is not None else "-"
        bang_tour_hien_thi.append({
            "Mã tour": r["MaTour"],
            "Tên tour": r["TenTour"],
            "Số LT": r["SoLichTrinh"],
            "Số đơn": r["SoDon"],
            "Số khách": r["SoKhach"],
            "Đơn hủy": r["SoDonHuy"],
            "Doanh thu DV": dinh_dang_tien(r["DoanhThuDichVu"]),
            "Tiền phạt hủy": dinh_dang_tien(r["TienPhatHuy"]),
            "Tổng doanh thu": dinh_dang_tien(r["TongDoanhThu"]),
            "Điểm TB": diem_tb,
        })
    st.dataframe(bang_tour_hien_thi, width="stretch")

# Bảng B: Xếp hạng nơi nghỉ
st.subheader("B. Bảng xếp hạng đánh giá nơi nghỉ")
if not ds_noi_nghi:
    st.info("Chưa có lượt đánh giá nơi nghỉ nào trong kỳ này")
else:
    bang_nn_hien_thi = []
    for r in ds_noi_nghi:
        bang_nn_hien_thi.append({
            "Mã nơi nghỉ": r["MaNhaNghi"],
            "Tên nơi nghỉ": r["TenNhaNghi"],
            "Loại hình": r["LoaiHinh"],
            "Tỉnh thành": r["TenTinh"],
            "Số lượt đánh giá": f"{r['SoLuotDanhGia']} lượt",
            "Điểm trung bình": f"{r['DiemTB']} sao",
        })
    st.dataframe(bang_nn_hien_thi, width="stretch")

st.markdown("---")

# Kiểm tra người lập trước khi mở nút tải báo cáo
if not nguoi_lap.strip():
    st.warning("Nhập tên người lập báo cáo để tải và in báo cáo")
    st.stop()

html_noi_dung = tao_html_bao_cao_doanh_thu(
    tu_ngay=tu_ngay,
    den_ngay=den_ngay,
    ds_tour=ds_tour,
    ds_noi_nghi=ds_noi_nghi,
    nguoi_lap=nguoi_lap,
    ngay_xuat=hien_tai(),
)

st.download_button(
    label="Tải báo cáo HTML (Khổ in A4 ngang)",
    data=html_noi_dung,
    file_name=f"bao_cao_doanh_thu_{tu_ngay.strftime('%Y%m%d')}_{den_ngay.strftime('%Y%m%d')}.html",
    mime="text/html",
    width="stretch",
)

with st.expander("Xem trước biểu mẫu in (A4 ngang)", expanded=False):
    st.iframe(html_noi_dung, height=620)
