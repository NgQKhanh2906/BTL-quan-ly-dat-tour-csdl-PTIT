from datetime import datetime
from html import escape
from string import Template
import streamlit as st
from db import doc, dinh_dang_tien, hien_tai, thong_bao_loi

st.set_page_config(page_title="R2 - Báo cáo doanh thu", layout="wide")

st.title("R2. Báo cáo tổng hợp doanh thu và đánh giá tour")
st.caption("Tổng hợp doanh thu, số đơn, số khách và điểm đánh giá theo từng tour du lịch và cơ sở lưu trú.")

NOI_NHAN = "Ban Giám đốc công ty du lịch"

# R2.1: Truy vấn doanh thu theo tour (có dòng ROLLUP tổng cộng)
SQL_DOANH_THU_TOUR = """
SELECT IF(GROUPING(t.MaTour), 'TỔNG CỘNG', t.MaTour) AS MaTour,
       IF(GROUPING(t.MaTour), '', t.TenTour) AS TenTour,
       COUNT(DISTINCT lt.MaLichTrinh) AS SoLichTrinh,
       COALESCE(SUM(v.MaTrangThai <> 'HUY'), 0) AS SoDon,
       COALESCE(SUM(CASE WHEN v.MaTrangThai <> 'HUY' THEN v.SoLuongKhach END), 0) AS SoKhach,
       COALESCE(SUM(v.MaTrangThai = 'HUY'), 0) AS SoDonHuy,
       COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0) AS DoanhThuDichVu,
       COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TienPhatHuy,
       COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0)
       + COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TongDoanhThu,
       ROUND(AVG(v.DiemTour), 1) AS DiemTourTB
FROM Tour t
JOIN LichTrinh lt ON lt.MaTour = t.MaTour
LEFT JOIN v_DonHang_ChiTiet v ON v.MaLichTrinh = lt.MaLichTrinh
WHERE lt.NgayXuatPhat >= %(TuNgay)s AND lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY
GROUP BY t.MaTour, t.TenTour WITH ROLLUP
HAVING GROUPING(t.TenTour) = 0 OR GROUPING(t.MaTour) = 1;
"""

# R2.2: Truy vấn xếp hạng nơi nghỉ
SQL_XEP_HANG_NOI_NGHI = """
SELECT nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh,
       COUNT(d.DiemNhaNghi) AS SoLuotDanhGia,
       ROUND(AVG(d.DiemNhaNghi), 1) AS DiemTB
FROM NhaNghi nn
JOIN TinhThanh tt ON tt.MaTinh = nn.MaTinh
JOIN DonHang d ON d.MaNhaNghi = nn.MaNhaNghi
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.DiemNhaNghi IS NOT NULL
  AND lt.NgayXuatPhat >= %(TuNgay)s AND lt.NgayXuatPhat < %(DenNgay)s + INTERVAL 1 DAY
GROUP BY nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh
ORDER BY DiemTB DESC, SoLuotDanhGia DESC;
"""

# Bộ lọc kỳ báo cáo
col_ngay1, col_ngay2 = st.columns(2)
tu_ngay = col_ngay1.date_input("Kỳ báo cáo từ ngày", value=datetime(2026, 9, 1).date())
den_ngay = col_ngay2.date_input("Kỳ báo cáo đến ngày", value=datetime(2026, 12, 31).date())

if den_ngay < tu_ngay:
    st.error("Kỳ báo cáo đến ngày phải lớn hơn hoặc bằng từ ngày")
    st.stop()

# Nhập người lập và hiển thị nơi nhận (Tiêu chí chấm điểm 7)
nguoi_lap = st.text_input("Người lập báo cáo", max_chars=100, placeholder="Họ tên nhân viên kế toán")
st.caption(f"Nơi nhận: {NOI_NHAN}")

tham_so = {
    "TuNgay": tu_ngay,
    "DenNgay": den_ngay,
}

# Thực thi truy vấn dữ liệu
try:
    ds_tour = doc(SQL_DOANH_THU_TOUR, tham_so)
    ds_noi_nghi = doc(SQL_XEP_HANG_NOI_NGHI, tham_so)
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

# Tách dòng tổng cộng (ROLLUP) và các dòng chi tiết
dong_tong = next((r for r in ds_tour if r["MaTour"] == "TỔNG CỘNG"), None)
dong_tour = [r for r in ds_tour if r["MaTour"] != "TỔNG CỘNG"]

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
st.dataframe(bang_tour_hien_thi, use_container_width=True)

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
    st.dataframe(bang_nn_hien_thi, use_container_width=True)

st.markdown("---")

# Kiểm tra người lập trước khi mở nút tải báo cáo
if not nguoi_lap.strip():
    st.warning("Nhập tên người lập báo cáo để tải và in báo cáo")
    st.stop()

# Hàm tạo chuỗi HTML từ template
def tao_html():
    hang_tour_html = []
    for r in ds_tour:
        la_tong = (r["MaTour"] == "TỔNG CỘNG")
        cls = " class=\"hang-tong\"" if la_tong else ""
        diem_tb = f"{r['DiemTourTB']}" if r["DiemTourTB"] is not None else "-"
        hang_tour_html.append(
            f"<tr{cls}>"
            f"<td class=\"text-center\">{r['MaTour']}</td>"
            f"<td>{r['TenTour']}</td>"
            f"<td class=\"text-center\">{r['SoLichTrinh']}</td>"
            f"<td class=\"text-center\">{r['SoDon']}</td>"
            f"<td class=\"text-center\">{r['SoKhach']}</td>"
            f"<td class=\"text-center\">{r['SoDonHuy']}</td>"
            f"<td class=\"text-right\">{dinh_dang_tien(r['DoanhThuDichVu'])}</td>"
            f"<td class=\"text-right\">{dinh_dang_tien(r['TienPhatHuy'])}</td>"
            f"<td class=\"text-right\">{dinh_dang_tien(r['TongDoanhThu'])}</td>"
            f"<td class=\"text-center\">{diem_tb}</td>"
            f"</tr>"
        )

    hang_nn_html = []
    for r in ds_noi_nghi:
        hang_nn_html.append(
            f"<tr>"
            f"<td class=\"text-center\">{r['MaNhaNghi']}</td>"
            f"<td>{r['TenNhaNghi']}</td>"
            f"<td class=\"text-center\">{r['LoaiHinh']}</td>"
            f"<td class=\"text-center\">{r['TenTinh']}</td>"
            f"<td class=\"text-center\">{r['SoLuotDanhGia']}</td>"
            f"<td class=\"text-center\">{r['DiemTB']} sao</td>"
            f"</tr>"
        )

    with open("templates/bao_cao_doanh_thu.html", "r", encoding="utf-8") as f:
        mau = Template(f.read())

    return mau.substitute(
        tu_ngay=tu_ngay.strftime("%d/%m/%Y"),
        den_ngay=den_ngay.strftime("%d/%m/%Y"),
        nguoi_lap=escape(nguoi_lap.strip()),
        noi_nhan=escape(NOI_NHAN),
        tong_doanh_thu=dinh_dang_tien(tong_dt),
        so_don=str(so_don),
        so_khach=str(so_khach),
        so_don_huy=str(so_don_huy),
        bang_tour_html="\n".join(hang_tour_html),
        bang_noi_nghi_html="\n".join(hang_nn_html) if hang_nn_html else "<tr><td colspan=\"6\" class=\"text-center\">Chưa có đánh giá</td></tr>",
        ngay_xuat=hien_tai().strftime("%d/%m/%Y %H:%M"),
    )

html_noi_dung = tao_html()

st.download_button(
    label="Tải báo cáo HTML (Khổ in A4 ngang)",
    data=html_noi_dung,
    file_name=f"bao_cao_doanh_thu_{tu_ngay.strftime('%Y%m%d')}_{den_ngay.strftime('%Y%m%d')}.html",
    mime="text/html",
    use_container_width=True,
)