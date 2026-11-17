from html import escape
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from db import doc, dinh_dang_tien, dinh_dang_ngay, hien_tai

st.set_page_config(page_title="R1 - Phiếu xác nhận đặt tour", layout="wide")
st.title("R1. Phiếu xác nhận đặt tour du lịch (Biểu mẫu in A4)")
st.caption(
    "Biểu mẫu do Nhân viên kinh doanh lập để giao cho Khách hàng xác nhận thông tin "
    "chuyến đi, lưu trú, xe trung chuyển, tổng chi phí hoặc thông tin hoàn tiền khi hủy."
)

# R1.1: Nap danh sach toan bo don hang
ds_don = doc(
    """
    SELECT MaDonHang, HoTen, TenTour,
           NgayXuatPhat, TenTrangThai, TongTien
    FROM v_DonHang_ChiTiet
    ORDER BY MaDonHang
    """
)

if not ds_don:
    st.info("Hiện không có đơn hàng nào trong hệ thống.")
    st.stop()

col1, col2 = st.columns([2, 1])
chon_don = col1.selectbox(
    "Chọn đơn hàng cần xuất phiếu xác nhận",
    ds_don,
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['HoTen']} | {r['TenTour']} "
        f"| {r['TenTrangThai']} | {dinh_dang_tien(r['TongTien'])}"
    ),
)
nguoi_lap = col2.text_input(
    "Nhân viên lập phiếu (*)",
    value="Nguyễn Quốc Khánh - Phòng Kinh doanh",
    max_chars=100,
)

if not nguoi_lap.strip():
    st.warning("Vui lòng nhập họ tên Nhân viên lập phiếu để hiển thị trên biểu mẫu.")
    st.stop()

# R1.1: Truy van thong tin chinh cua don hang
ct_rows = doc(
    """
    SELECT v.MaDonHang, v.NgayDat, v.TenTrangThai,
           v.MaKH, v.HoTen AS TenKhachHang, kh.Email, kh.DiaChi AS DiaChiKH,
           kh.SoID, th.LoaiThe,
           t.MaTour, v.TenTour, txp.TenTinh AS TinhXuatPhat, v.TinhDen,
           v.MaLichTrinh, v.NgayXuatPhat, v.NgayKetThuc, v.SoDem, lt.DiemTapTrung,
           v.SoLuongKhach, v.GiaCoBan, v.TienTour,
           d.MaNhaNghi, v.TenNhaNghi, nn.LoaiHinh, nn.DiaChi AS DiaChiNhaNghi,
           v.SoPhong, v.GiaPhongMoiDem, v.TienPhong, v.TongTien,
           v.NgayHuy, v.LyDoHuy, v.TyLePhat, v.TienPhat, v.TienHoan
    FROM v_DonHang_ChiTiet v
    JOIN DonHang d ON d.MaDonHang = v.MaDonHang
    JOIN KhachHang kh ON kh.MaKH = v.MaKH
    LEFT JOIN TheThanhToan th ON th.SoID = kh.SoID
    JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
    JOIN Tour t ON t.MaTour = v.MaTour
    JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
    LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
    WHERE v.MaDonHang = %(MaDonHang)s
    """,
    {"MaDonHang": chon_don["MaDonHang"]},
)

if not ct_rows:
    st.error("Không tìm thấy thông tin đơn hàng.")
    st.stop()

ct = ct_rows[0]

# R1.2: Truy van cac so dien thoai cua khach
sdt_rows = doc(
    """
    SELECT GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ') AS SoDienThoai
    FROM DonHang d
    JOIN SDT_KhachHang sdt ON sdt.MaKH = d.MaKH
    WHERE d.MaDonHang = %(MaDonHang)s
    """,
    {"MaDonHang": chon_don["MaDonHang"]},
)
danh_sach_sdt = sdt_rows[0]["SoDienThoai"] if sdt_rows and sdt_rows[0]["SoDienThoai"] else "Chưa cập nhật"

# R1.3: Truy van lich xe trung chuyen
ds_ctc = doc(
    """
    SELECT TenLoaiChuyen, ThoiGianDon, DiemDon, DiemTra,
           COALESCE(BienSoXe, 'Chưa xếp xe') AS BienSoXe,
           COALESCE(TenDonVi, 'Chưa xếp') AS DonViVanTai
    FROM v_LichTrungChuyen
    WHERE MaDonHang = %(MaDonHang)s
    ORDER BY ThoiGianDon
    """,
    {"MaDonHang": chon_don["MaDonHang"]},
)

# Tao khoi HTML cho muc 3: Nha nghi
if ct["MaNhaNghi"]:
    khoi_nha_nghi = (
        f"<table class='info-grid'>"
        f"<tr><td style='width:50%;'><strong>Nơi nghỉ lưu trú:</strong> "
        f"{escape(str(ct['TenNhaNghi']))} ({escape(str(ct['MaNhaNghi']))})</td>"
        f"<td style='width:50%;'><strong>Số lượng phòng:</strong> {int(ct['SoPhong'])} phòng "
        f"&times; {int(ct['SoDem'])} đêm ({dinh_dang_tien(ct['GiaPhongMoiDem'])}/đêm)</td></tr>"
        f"<tr><td colspan='2'><strong>Địa chỉ lưu trú:</strong> "
        f"{escape(str(ct['DiaChiNhaNghi']))} ({escape(str(ct['LoaiHinh']))})</td></tr>"
        f"</table>"
    )
    dien_giai_phong = (
        f"{int(ct['SoPhong'])} phòng &times; {int(ct['SoDem'])} đêm "
        f"&times; {dinh_dang_tien(ct['GiaPhongMoiDem'])}"
    )
else:
    khoi_nha_nghi = (
        "<div style='padding: 3px 6px; font-style: italic;'>"
        "Khách hàng không đăng ký dịch vụ nhà nghỉ đi kèm (0 phòng)."
        "</div>"
    )
    dien_giai_phong = "Không sử dụng (0 phòng)"

# Tao khoi HTML cho muc 4: Xe trung chuyen
if ds_ctc:
    dong_html = []
    for idx, r in enumerate(ds_ctc, 1):
        dong_html.append(
            f"<tr>"
            f"<td class='text-center'>{idx}</td>"
            f"<td>{escape(str(r['TenLoaiChuyen']))}</td>"
            f"<td>{escape(str(r['DiemDon']))}</td>"
            f"<td>{escape(str(r['DiemTra']))}</td>"
            f"<td class='text-center'>{escape(str(r['BienSoXe']))}</td>"
            f"<td>{escape(str(r['DonViVanTai']))}</td>"
            f"</tr>"
        )
    khoi_trung_chuyen = (
        "<table class='data-table'>"
        "<thead><tr>"
        "<th style='width:6%;'>STT</th>"
        "<th style='width:18%;'>Loại chuyến</th>"
        "<th style='width:24%;'>Điểm đón</th>"
        "<th style='width:24%;'>Điểm trả</th>"
        "<th style='width:14%;'>Biển số xe</th>"
        "<th style='width:14%;'>Đơn vị vận tải</th>"
        "</tr></thead>"
        f"<tbody>{''.join(dong_html)}</tbody></table>"
    )
else:
    khoi_trung_chuyen = (
        "<div style='padding: 3px 6px; font-style: italic;'>"
        "Không có chuyến xe trung chuyển đang hoạt động cho đơn hàng này."
        "</div>"
    )

# Tao khoi HTML cho muc 6: Thong tin huy tour
if ct["TenTrangThai"] == "Đã hủy" or ct["NgayHuy"] is not None:
    khoi_huy = (
        f"<table class='info-grid'>"
        f"<tr><td style='width:50%;'><strong>Thời điểm hủy đơn:</strong> {dinh_dang_ngay(ct['NgayHuy'])}</td>"
        f"<td style='width:50%;'><strong>Phí phạt hủy tour:</strong> "
        f"<strong>{dinh_dang_tien(ct['TienPhat'])} ({int(ct['TyLePhat'])}%)</strong></td></tr>"
        f"<tr><td><strong>Lý do hủy:</strong> {escape(str(ct['LyDoHuy']))}</td>"
        f"<td><strong>Số tiền hoàn lại cho khách:</strong> "
        f"<strong>{dinh_dang_tien(ct['TienHoan'])}</strong></td></tr>"
        f"</table>"
    )
else:
    khoi_huy = (
        "<div style='padding: 3px 6px; font-style: italic;'>"
        "Đơn hàng đang hoạt động bình thường (Không phát sinh hủy tour)."
        "</div>"
    )

duong_dan_mau = Path(__file__).resolve().parent.parent / "templates" / "phieu_xac_nhan.html"
html_goc = duong_dan_mau.read_text(encoding="utf-8")

so_id_the = str(ct["SoID"]) if ct["SoID"] else ""
so_id_an = f"**** **** **** {so_id_the[-4:]}" if len(so_id_the) >= 4 else "Không lưu thẻ"
loai_the_str = str(ct["LoaiThe"]) if ct["LoaiThe"] else "Tiền mặt / Chuyển khoản"

bang_thay_the = {
    "{{MA_DON_HANG}}": escape(str(ct["MaDonHang"])),
    "{{NGAY_IN}}": hien_tai().strftime("%d/%m/%Y %H:%M"),
    "{{NGAY_DAT}}": dinh_dang_ngay(ct["NgayDat"]),
    "{{TEN_TRANG_THAI}}": escape(str(ct["TenTrangThai"])),
    "{{NGUOI_LAP}}": escape(nguoi_lap.strip()),
    "{{TEN_KHACH_HANG}}": escape(str(ct["TenKhachHang"])),
    "{{MA_KH}}": escape(str(ct["MaKH"])),
    "{{DANH_SACH_SDT}}": escape(str(danh_sach_sdt)),
    "{{EMAIL_KH}}": escape(str(ct["Email"] or "Chưa cập nhật")),
    "{{LOAI_THE}}": escape(loai_the_str),
    "{{SO_ID_THE}}": escape(so_id_an),
    "{{DIA_CHI_KH}}": escape(str(ct["DiaChiKH"] or "Chưa cập nhật")),
    "{{TEN_TOUR}}": escape(str(ct["TenTour"])),
    "{{MA_TOUR}}": escape(str(ct["MaTour"])),
    "{{TINH_XUAT_PHAT}}": escape(str(ct["TinhXuatPhat"])),
    "{{TINH_DEN}}": escape(str(ct["TinhDen"])),
    "{{MA_LICH_TRINH}}": escape(str(ct["MaLichTrinh"])),
    "{{THOI_LUONG}}": f"{int(ct['SoDem']) + 1} ngày {int(ct['SoDem'])} đêm",
    "{{NGAY_KHOI_HANH}}": dinh_dang_ngay(ct["NgayXuatPhat"]),
    "{{NGAY_KET_THUC}}": dinh_dang_ngay(ct["NgayKetThuc"]),
    "{{SO_LUONG_KHACH}}": str(int(ct["SoLuongKhach"])),
    "{{GIA_CO_BAN}}": dinh_dang_tien(ct["GiaCoBan"]),
    "{{KHOI_NHA_NGHI}}": khoi_nha_nghi,
    "{{KHOI_TRUNG_CHUYEN}}": khoi_trung_chuyen,
    "{{TIEN_TOUR}}": dinh_dang_tien(ct["TienTour"]),
    "{{DIEN_GIAI_PHONG}}": dien_giai_phong,
    "{{TIEN_PHONG}}": dinh_dang_tien(ct["TienPhong"]),
    "{{TONG_TIEN}}": dinh_dang_tien(ct["TongTien"]),
    "{{KHOI_THONG_TIN_HUY}}": khoi_huy,
}

html_ket_qua = html_goc
for k, v in bang_thay_the.items():
    html_ket_qua = html_ket_qua.replace(k, v)

components.html(html_ket_qua, height=960, scrolling=True)
