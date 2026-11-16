import streamlit as st
from db import doc, ghi, dinh_dang_tien, hien_tai

st.set_page_config(page_title="F3 - Đánh giá sau chuyến đi", layout="wide")
st.title("F3. Đánh giá chất lượng tour và nhà nghỉ sau chuyến đi")
st.caption(
    "Chỉ những đơn hàng ở trạng thái Hoàn thành (HOANTHANH) và chưa từng đánh giá "
    "mới được phép gửi điểm và nhận xét."
)

ds_kh = doc("SELECT MaKH, HoTen, Email FROM KhachHang ORDER BY MaKH")
chon_kh = st.selectbox(
    "1. Chọn khách hàng",
    ds_kh,
    format_func=lambda r: f"{r['MaKH']} - {r['HoTen']} ({r['Email']})",
)

# F3.1: Nap danh sach cac don HOANTHANH chua danh gia cua khach hang
ds_don_ht = doc(
    """
    SELECT dh.MaDonHang, t.MaTour, t.TenTour,
           lt.NgayXuatPhat, lt.NgayKetThuc,
           dh.MaNhaNghi, nn.TenNhaNghi,
           dh.NgayDat, v.TongTien
    FROM DonHang dh
    JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
    JOIN Tour t              ON t.MaTour = lt.MaTour
    LEFT JOIN NhaNghi nn     ON nn.MaNhaNghi = dh.MaNhaNghi
    JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
    WHERE dh.MaKH = %s
      AND dh.MaTrangThai = 'HOANTHANH'
      AND dh.NgayDanhGia IS NULL
    ORDER BY lt.NgayKetThuc DESC
    """,
    (chon_kh["MaKH"],),
)

if not ds_don_ht:
    st.info(
        f"Khách hàng **{chon_kh['HoTen']}** (`{chon_kh['MaKH']}`) hiện không có chuyến đi nào "
        f"ở trạng thái Hoàn thành đang chờ đánh giá (hoặc tất cả các chuyến hoàn thành đã được đánh giá)."
    )
    st.stop()

chon_don = st.selectbox(
    "2. Chọn chuyến đi đã hoàn thành cần đánh giá",
    ds_don_ht,
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['TenTour']} "
        f"({r['NgayXuatPhat']} -> {r['NgayKetThuc']}) | {dinh_dang_tien(r['TongTien'])}"
    ),
)

st.info(
    f"**Mã đơn:** `{chon_don['MaDonHang']}` | **Tour:** {chon_don['TenTour']} (`{chon_don['MaTour']}`)  \n"
    f"**Hành trình:** {chon_don['NgayXuatPhat']} đến {chon_don['NgayKetThuc']} | "
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
    )
    nhan_xet_tour = st.text_area(
        "Nhận xét về chương trình tour (Tùy chọn, tối đa 500 ký tự)",
        max_chars=500,
        placeholder="Chia sẻ cảm nhận về lịch trình, hướng dẫn viên, phương tiện di chuyển...",
    )

with col_nn:
    st.subheader("Đánh giá Nhà nghỉ / Khách sạn")
    if chon_don["MaNhaNghi"]:
        co_dg_nn = st.checkbox(
            f"Tôi muốn chấm điểm cho {chon_don['TenNhaNghi']} ({chon_don['MaNhaNghi']})",
            value=True,
        )
        if co_dg_nn:
            diem_nn = st.slider(
                "Điểm đánh giá nhà nghỉ (1 - 5 sao)",
                min_value=1,
                max_value=5,
                value=4,
            )
        else:
            diem_nn = None
        nhan_xet_nn = st.text_area(
            "Nhận xét về nhà nghỉ (Tùy chọn, tối đa 500 ký tự)",
            max_chars=500,
            placeholder="Chia sẻ cảm nhận về phòng ốc, vệ sinh, thái độ phục vụ...",
        )
    else:
        st.caption(
            "Đơn hàng này không đăng ký dịch vụ nhà nghỉ (`MaNhaNghi IS NULL`), "
            "do đó phần đánh giá nhà nghỉ được tự động ẩn theo ràng buộc `chk_DonHang_DanhGia`."
        )
        diem_nn = None
        nhan_xet_nn = ""

if st.button("Gửi đánh giá chuyến đi", type="primary"):
    nx_tour_val = nhan_xet_tour.strip() if nhan_xet_tour and nhan_xet_tour.strip() else None
    nx_nn_val = nhan_xet_nn.strip() if nhan_xet_nn and nhan_xet_nn.strip() else None

    if nx_nn_val is not None and diem_nn is None:
        st.error(
            "Bạn đã nhập nhận xét cho nhà nghỉ nhưng chưa tích chọn chấm điểm sao nhà nghỉ. "
            "Vui lòng tích chọn chấm điểm sao nhà nghỉ hoặc xóa nhận xét nhà nghỉ."
        )
    else:
        ngay_dg_str = hien_tai().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            UPDATE DonHang
            SET DiemTour       = %s,
                NhanXetTour    = %s,
                NgayDanhGia    = %s,
                DiemNhaNghi    = %s,
                NhanXetNhaNghi = %s
            WHERE MaDonHang = %s
              AND MaTrangThai = 'HOANTHANH'
              AND NgayDanhGia IS NULL
        """
        tham_so = (
            int(diem_tour),
            nx_tour_val,
            ngay_dg_str,
            int(diem_nn) if diem_nn is not None else None,
            nx_nn_val,
            chon_don["MaDonHang"]
        )
        
        try:
            # F3.2: Ghi trực tiếp vào CSDL
            ghi(sql, tham_so, True)
            st.success(
                f"Đã ghi nhận đánh giá cho đơn `{chon_don['MaDonHang']}` "
                f"(Điểm tour: {diem_tour}/5 sao"
                f"{f', Điểm nhà nghỉ: {diem_nn}/5 sao' if diem_nn else ''}) "
                f"vào lúc {ngay_dg_str}!"
            )
        except Exception as e:
            try:
                from db import thong_bao_loi
                thong_bao_loi(e)
            except:
                st.error(f"Lỗi: {e}")