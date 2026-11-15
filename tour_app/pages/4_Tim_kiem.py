from datetime import datetime
import streamlit as st
from db import doc, dinh_dang_tien, dinh_dang_ngay, hien_tai, thong_bao_loi

st.set_page_config(page_title="S1 - Tìm kiếm lịch trình", layout="wide")

st.title("S1. Tra cứu và tìm kiếm lịch trình tour")
st.caption("Tìm kiếm lịch trình theo từ khóa, điểm đến, khoảng giá, ngày khởi hành, số chỗ và điểm đánh giá.")

# S1.1: Danh sách tỉnh thành
SQL_TINH_THANH = """
SELECT MaTinh, TenTinh
FROM TinhThanh
ORDER BY TenTinh;
"""

# S1.2: Truy vấn tìm kiếm lịch trình động với tham số tĩnh
SQL_TIM_KIEM = """
SELECT lt.MaLichTrinh,
       t.TenTour,
       txp.TenTinh AS NoiDi,
       tden.TenTinh AS NoiDen,
       lt.NgayXuatPhat,
       DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) + 1 AS SoNgay,
       lt.GiaCoBan,
       lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
       dg.DiemTB,
       COALESCE(dg.SoLuot, 0) AS SoLuotDanhGia
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
JOIN TinhThanh tden ON tden.MaTinh = t.MaTinhDen
LEFT JOIN (
    SELECT l.MaTour, ROUND(AVG(d.DiemTour), 1) AS DiemTB, COUNT(d.DiemTour) AS SoLuot
    FROM DonHang d
    JOIN LichTrinh l ON l.MaLichTrinh = d.MaLichTrinh
    WHERE d.DiemTour IS NOT NULL
    GROUP BY l.MaTour
) AS dg ON dg.MaTour = t.MaTour
WHERE (%(TuKhoa)s IS NULL OR t.TenTour LIKE CONCAT('%', %(TuKhoa)s, '%'))
  AND (%(MaTinhDen)s IS NULL OR t.MaTinhDen = %(MaTinhDen)s)
  AND (%(GiaTu)s IS NULL OR lt.GiaCoBan >= %(GiaTu)s)
  AND (%(GiaDen)s IS NULL OR lt.GiaCoBan <= %(GiaDen)s)
  AND lt.NgayXuatPhat >= %(TuNgay)s
  AND (%(DenNgay)s IS NULL OR lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY)
  AND lt.SoChoToiDa - lt.SoChoDaDat >= %(SoKhach)s
  AND (%(DiemToiThieu)s IS NULL OR dg.DiemTB >= %(DiemToiThieu)s)
ORDER BY lt.NgayXuatPhat, lt.GiaCoBan;
"""

# Quản lý trạng thái bộ lọc qua session_state để hỗ trợ nút bấm nhanh
if "s1_gia_tu" not in st.session_state:
    st.session_state["s1_gia_tu"] = 0
if "s1_tu_khoa" not in st.session_state:
    st.session_state["s1_tu_khoa"] = ""
if "s1_ma_tinh_den" not in st.session_state:
    st.session_state["s1_ma_tinh_den"] = "Tất cả"

col_btn1, col_btn2 = st.columns([2, 8])
with col_btn1:
    if st.button("Tour cao cấp (từ 10 triệu)", use_container_width=True):
        st.session_state["s1_gia_tu"] = 10000000
        st.session_state["s1_tu_khoa"] = ""
        st.session_state["s1_ma_tinh_den"] = "Tất cả"
        st.rerun()

with col_btn2:
    if st.button("Đặt lại bộ lọc"):
        st.session_state["s1_gia_tu"] = 0
        st.session_state["s1_tu_khoa"] = ""
        st.session_state["s1_ma_tinh_den"] = "Tất cả"
        st.rerun()

st.markdown("---")

# Nạp danh sách tỉnh thành
try:
    ds_tinh = doc(SQL_TINH_THANH)
    danh_sach_tinh = ["Tất cả"] + [f"{t['MaTinh']} - {t['TenTinh']}" for t in ds_tinh]
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

# 8 bộ lọc chia làm 2 hàng
r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
with r1_c1:
    tu_khoa = st.text_input(
        "1. Từ khóa tên tour",
        value=st.session_state["s1_tu_khoa"],
        max_chars=100,
        placeholder="Ví dụ: Hạ Long, Sa Pa...",
    )
with r1_c2:
    idx_tinh = 0
    if st.session_state["s1_ma_tinh_den"] != "Tất cả":
        for i, item in enumerate(danh_sach_tinh):
            if item.startswith(st.session_state["s1_ma_tinh_den"]):
                idx_tinh = i
                break
    tinh_den_chon = st.selectbox("2. Tỉnh đến", danh_sach_tinh, index=idx_tinh)
with r1_c3:
    gia_tu = st.number_input(
        "3. Giá từ (VNĐ)",
        min_value=0,
        step=500000,
        value=st.session_state["s1_gia_tu"],
    )
with r1_c4:
    gia_den = st.number_input(
        "4. Giá đến (VNĐ - 0 là không giới hạn)",
        min_value=0,
        step=500000,
        value=0,
    )

r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
with r2_c1:
    tu_ngay = st.date_input("5. Khởi hành từ ngày", value=hien_tai().date())
with r2_c2:
    co_den_ngay = st.checkbox("Lọc theo ngày đến", value=False)
    den_ngay = (
        st.date_input("6. Khởi hành đến ngày", value=hien_tai().date())
        if co_den_ngay
        else None
    )
with r2_c3:
    so_khach = st.number_input("7. Số khách", min_value=1, value=1, step=1)
with r2_c4:
    diem_danh_gia = st.selectbox(
        "8. Điểm đánh giá tối thiểu",
        ["Tất cả", "3.0", "4.0", "4.5"],
        index=0,
    )

# Kiểm tra ràng buộc hợp lệ của bộ lọc
if gia_den > 0 and gia_den < gia_tu:
    st.error("Giá đến phải lớn hơn hoặc bằng giá từ")
    st.stop()

if den_ngay is not None and den_ngay < tu_ngay:
    st.error("Khởi hành đến ngày phải lớn hơn hoặc bằng từ ngày")
    st.stop()

# Đóng gói tham số cho SQL
ma_tinh_tham_so = None
if tinh_den_chon != "Tất cả":
    ma_tinh_tham_so = tinh_den_chon.split(" - ")[0]

diem_tham_so = None
if diem_danh_gia != "Tất cả":
    diem_tham_so = float(diem_danh_gia)

tham_so = {
    "TuKhoa": tu_khoa.strip() if tu_khoa.strip() else None,
    "MaTinhDen": ma_tinh_tham_so,
    "GiaTu": gia_tu if gia_tu > 0 else None,
    "GiaDen": gia_den if gia_den > 0 else None,
    "TuNgay": tu_ngay,
    "DenNgay": den_ngay,
    "SoKhach": so_khach,
    "DiemToiThieu": diem_tham_so,
}

# Thực thi truy vấn
try:
    ket_qua = doc(SQL_TIM_KIEM, tham_so)
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
    st.dataframe(du_lieu_bang, use_container_width=True)