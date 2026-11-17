from datetime import datetime
import streamlit as st
from db import doc, ghi, dinh_dang_tien, dinh_dang_ngay, hien_tai, thong_bao_loi

st.set_page_config(page_title="F2 - Quản lý đơn & hủy tour", layout="wide")
st.title("F2. Cập nhật trạng thái và hủy đơn đặt tour")
st.caption(
    "Chuyển trạng thái đơn theo đúng quy trình (DAT -> THANHTOAN -> HOANTHANH) "
    "hoặc hủy đơn kèm tính phí phạt tự động và hoàn trả chỗ cho lịch trình."
)

# F2.1: Nap danh sach cac don hang dang o trang thai DAT hoac THANHTOAN
ds_don = doc(
    """
    SELECT MaDonHang, HoTen, TenTour, NgayXuatPhat, SoLuongKhach, TongTien, MaTrangThai, TenTrangThai
    FROM v_DonHang_ChiTiet
    WHERE MaTrangThai IN ('DAT', 'THANHTOAN')
    ORDER BY NgayXuatPhat DESC
    """
)

if not ds_don:
    st.info("Hiện không có đơn hàng nào ở trạng thái chờ xử lý (DAT hoặc THANHTOAN).")
    st.stop()

chon_don = st.selectbox(
    "Chọn đơn hàng cần xử lý",
    ds_don,
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['HoTen']} | {r['TenTour']} "
        f"(Khởi hành: {dinh_dang_ngay(r['NgayXuatPhat'])}) | {r['TenTrangThai']}"
    ),
)

# F2.2: Xem chi tiet don hang dang chon
ct_rows = doc(
    """
    SELECT v.MaDonHang, v.MaKH, v.HoTen,
           v.MaLichTrinh, v.NgayXuatPhat, v.NgayKetThuc,
           d.MaNhaNghi, v.TenNhaNghi, v.SoLuongKhach, v.SoPhong,
           v.NgayDat, v.MaTrangThai, v.TenTrangThai,
           v.TienTour, v.TienPhong, v.TongTien
    FROM v_DonHang_ChiTiet v
    JOIN DonHang d ON d.MaDonHang = v.MaDonHang
    WHERE v.MaDonHang = %(MaDonHang)s
    """,
    {"MaDonHang": chon_don["MaDonHang"]},
)

if not ct_rows:
    st.error("Không tìm thấy thông tin chi tiết đơn hàng.")
    st.stop()

ct = ct_rows[0]

c1, c2, c3 = st.columns(3)
c1.markdown(
    f"**Mã đơn:** `{ct['MaDonHang']}`  \n"
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
ds_tt_moi = doc(
    """
    SELECT tt.MaTrangThai, tt.TenTrangThai
    FROM DonHang d
    JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
    JOIN TrangThaiDonHang tt
      ON (d.MaTrangThai = 'DAT' AND tt.MaTrangThai = 'THANHTOAN')
      OR (d.MaTrangThai = 'THANHTOAN' AND tt.MaTrangThai = 'HOANTHANH' AND lt.NgayKetThuc < %(HienTai)s)
      OR (d.MaTrangThai IN ('DAT', 'THANHTOAN') AND tt.MaTrangThai = 'HUY' AND lt.NgayXuatPhat > %(HienTai)s)
    WHERE d.MaDonHang = %(MaDonHang)s
    ORDER BY tt.ThuTu
    """,
    {"HienTai": hien_tai(), "MaDonHang": ct["MaDonHang"]},
)

if not ds_tt_moi:
    st.info("Đơn hàng hiện không có trạng thái mới hợp lệ để chuyển.")
    st.stop()

tt_moi = st.selectbox(
    "Chọn trạng thái mới",
    ds_tt_moi,
    format_func=lambda r: f"{r['TenTrangThai']} ({r['MaTrangThai']})",
)

if tt_moi["MaTrangThai"] == "HUY":
    st.subheader("Thông tin hủy tour và tính phí phạt tự động")
    moc_hien_tai = hien_tai()
    col_d, col_t = st.columns(2)
    ngay_huy_d = col_d.date_input("Ngày hủy", value=moc_hien_tai.date())
    gio_huy_t = col_t.time_input(
        "Giờ hủy",
        value=moc_hien_tai.time().replace(second=0, microsecond=0),
    )
    ngay_gio_huy = datetime.combine(ngay_huy_d, gio_huy_t)
    ngay_gio_huy_str = ngay_gio_huy.strftime("%Y-%m-%d %H:%M:%S")
    ly_do_huy = st.text_input(
        "Lý do hủy tour (*)",
        max_chars=255,
        placeholder="Ví dụ: Khách bận công tác đột xuất, xin hủy đơn",
    )

    # F2.4: Tinh xem truoc muc phat huy tour bang named parameters
    xem_truoc_rows = doc(
        """
        SELECT x.MaDonHang,
               x.TongTien,
               x.SoNgayTruocKhoiHanh,
               x.SoGioSauKhiDat,
               x.TyLePhat,
               ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienPhat,
               x.TongTien - ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienHoan
        FROM (
            SELECT v.MaDonHang,
                   v.TongTien,
                   TIMESTAMPDIFF(HOUR, v.NgayDat, %(NgayHuy)s) AS SoGioSauKhiDat,
                   DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) AS SoNgayTruocKhoiHanh,
                   CASE
                       WHEN TIMESTAMPDIFF(HOUR, v.NgayDat, %(NgayHuy)s) < 24
                            AND DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 7 THEN 0
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 15 THEN 10
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 7  THEN 30
                       WHEN DATEDIFF(v.NgayXuatPhat, DATE(%(NgayHuy)s)) >= 3  THEN 50
                       ELSE 100
                   END AS TyLePhat
            FROM v_DonHang_ChiTiet v
            WHERE v.MaDonHang = %(MaDonHang)s
        ) AS x
        """,
        {
            "NgayHuy": ngay_gio_huy_str,
            "MaDonHang": ct["MaDonHang"],
        },
    )
    xem_truoc = xem_truoc_rows[0]

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

    if st.button("Xác nhận hủy đơn hàng", type="primary"):
        loi = []
        if not ly_do_huy.strip():
            loi.append("Vui lòng nhập Lý do hủy tour (không được để trống).")
        ngay_dat_dt = (
            ct["NgayDat"]
            if isinstance(ct["NgayDat"], datetime)
            else datetime.strptime(str(ct["NgayDat"]), "%Y-%m-%d %H:%M:%S")
        )
        if ngay_gio_huy < ngay_dat_dt:
            loi.append(
                f"Thời điểm hủy ({ngay_gio_huy_str}) không được nhỏ hơn "
                f"thời điểm đặt tour ({dinh_dang_ngay(ngay_dat_dt)})."
            )

        if loi:
            for m in loi:
                st.error(m)
        else:
            # F2.5: Giao dich 3 cau lenh nguyen tu khi huy don
            ds_lenh_huy = [
                (
                    """
                    UPDATE DonHang
                    SET MaTrangThai = 'HUY',
                        NgayHuy     = %s,
                        LyDoHuy     = %s
                    WHERE MaDonHang = %s
                      AND MaTrangThai IN ('DAT', 'THANHTOAN')
                    """,
                    (ngay_gio_huy_str, ly_do_huy.strip(), ct["MaDonHang"]),
                    True,
                ),
                (
                    """
                    UPDATE LichTrinh lt
                    JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh
                    SET lt.SoChoDaDat = lt.SoChoDaDat - d.SoLuongKhach
                    WHERE d.MaDonHang = %s
                      AND lt.SoChoDaDat >= d.SoLuongKhach
                    """,
                    (ct["MaDonHang"],),
                    True,
                ),
                (
                    "DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
                    (ct["MaDonHang"],),
                    False,
                ),
            ]
            try:
                ghi(ds_lenh_huy)
                st.success(
                    f"Đã hủy đơn `{ct['MaDonHang']}` thành công! "
                    f"Phí phạt: {dinh_dang_tien(phi_phat)}, "
                    f"đã hoàn trả {int(ct['SoLuongKhach'])} chỗ cho lịch trình `{ct['MaLichTrinh']}`."
                )
            except Exception as e:
                st.error(thong_bao_loi(e))
else:
    if st.button("Cập nhật trạng thái đơn hàng", type="primary"):
        # F2.6: Chuyen trang thai thuong
        ds_lenh_tt = [
            (
                """
                UPDATE DonHang
                SET MaTrangThai = %s
                WHERE MaDonHang = %s
                  AND (
                      (MaTrangThai = 'DAT'       AND %s = 'THANHTOAN')
                   OR (MaTrangThai = 'THANHTOAN' AND %s = 'HOANTHANH')
                  )
                """,
                (
                    tt_moi["MaTrangThai"],
                    ct["MaDonHang"],
                    tt_moi["MaTrangThai"],
                    tt_moi["MaTrangThai"],
                ),
                True,
            )
        ]
        try:
            ghi(ds_lenh_tt)
            st.success(
                f"Đã chuyển đơn `{ct['MaDonHang']}` sang trạng thái "
                f"`{tt_moi['TenTrangThai']}` thành công!"
            )
        except Exception as e:
            st.error(thong_bao_loi(e))
