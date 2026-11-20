import re
from datetime import datetime, timedelta
import streamlit as st
from db import doc, dinh_dang_ngay, dinh_dang_tien, ghi, hien_tai, thong_bao_loi

st.set_page_config(page_title="F1 - Đặt tour", layout="wide")

st.title("F1. Form tiếp nhận và đặt tour du lịch")
st.caption("Điền thông tin khách hàng, chọn lịch trình, số khách, nơi nghỉ theo tỉnh đến và đăng ký xe trung chuyển.")

# F1.2: Lich trinh chua khoi hanh, con cho
SQL_LICH_TRINH = """
SELECT lt.MaLichTrinh,
       t.TenTour,
       lt.NgayXuatPhat,
       lt.NgayKetThuc,
       DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS SoDem,
       lt.GiaCoBan,
       lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
       t.MaTinhDen
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
WHERE lt.NgayXuatPhat > %(HienTai)s
  AND lt.SoChoToiDa - lt.SoChoDaDat > 0
ORDER BY lt.NgayXuatPhat
"""

# F1.3: Noi nghi o tinh diem den
SQL_NOI_NGHI = """
SELECT MaNhaNghi, TenNhaNghi, LoaiHinh, GiaPhongMoiDem
FROM NhaNghi
WHERE MaTinh = %(MaTinhDen)s
ORDER BY GiaPhongMoiDem
"""

# F1.4: Sinh ma don moi
SQL_MA_DON_MOI = """
SELECT CONCAT('DH', LPAD(COALESCE(MAX(CAST(SUBSTRING(MaDonHang, 3) AS UNSIGNED)), 0) + 1, 3, '0')) AS MaDonHangMoi
FROM DonHang
"""

# Sinh ma khach hang moi
SQL_MA_KH_MOI = """
SELECT CONCAT('KH', LPAD(COALESCE(MAX(CAST(SUBSTRING(MaKH, 3) AS UNSIGNED)), 0) + 1, 3, '0')) AS MaKHMoi
FROM KhachHang
"""

# Kiểm tra khớp thông tin khách hàng cũ theo Họ tên, Số điện thoại và Email
SQL_KHOP_THONG_TIN_KH = """
SELECT kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi, sdt.SoDienThoai
FROM KhachHang kh
JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
WHERE LOWER(TRIM(kh.HoTen)) = LOWER(TRIM(%(HoTen)s))
  AND sdt.SoDienThoai = TRIM(%(SoDienThoai)s)
  AND LOWER(TRIM(kh.Email)) = LOWER(TRIM(%(Email)s))
LIMIT 1;
"""

# Kiểm tra Email hoặc Số điện thoại đã được sử dụng trong hệ thống chưa
SQL_KIEM_TRA_TRUNG_EMAIL_SDT = """
SELECT
    (SELECT COUNT(*) FROM KhachHang WHERE LOWER(Email) = LOWER(%(Email)s)) AS TrungEmail,
    (SELECT COUNT(*) FROM SDT_KhachHang WHERE SoDienThoai = %(SoDienThoai)s) AS TrungSDT;
"""

# F1.5: Tong tien du kien
SQL_TONG_TIEN = """
SELECT %(SoKhach)s * lt.GiaCoBan AS TienTour,
       %(SoPhong)s * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TienPhong,
       %(SoKhach)s * lt.GiaCoBan
       + %(SoPhong)s * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TongTienDuKien
FROM LichTrinh lt
LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = %(MaNhaNghi)s
WHERE lt.MaLichTrinh = %(MaLichTrinh)s
"""

# Them khach hang va so dien thoai moi
THEM_KHACH_HANG = """
INSERT INTO KhachHang (MaKH, HoTen, Email, DiaChi)
VALUES (%(MaKH)s, %(HoTen)s, %(Email)s, %(DiaChi)s)
"""

THEM_SDT_KHACH_HANG = """
INSERT INTO SDT_KhachHang (MaKH, SoDienThoai)
VALUES (%(MaKH)s, %(SoDienThoai)s)
"""

# F1.6: Cac lenh luu don trong 1 transaction
DAT_DON = """
INSERT INTO DonHang (MaDonHang, NgayDat, SoLuongKhach, SoPhong, MaKH, MaLichTrinh, MaNhaNghi)
VALUES (%(MaDonHang)s, %(HienTai)s, %(SoKhach)s, %(SoPhong)s, %(MaKH)s, %(MaLichTrinh)s, %(MaNhaNghi)s)
"""

TRU_CHO = """
UPDATE LichTrinh
SET SoChoDaDat = SoChoDaDat + %(SoKhach)s
WHERE MaLichTrinh = %(MaLichTrinh)s
"""

DON_TAI_NHA = """
INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon)
VALUES (%(MaDonHang)s, 'DON_TAI_NHA', %(DiaChiDon)s, %(GioDon)s)
"""

VE_NOI_NGHI = """
INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, ThoiGianDon)
VALUES (%(MaDonHang)s, 'VE_NOI_NGHI', %(GioVeNoiNghi)s)
"""


def luu_don(tham_so):
    tham_so = dict(tham_so, HienTai=hien_tai())
    cac_lenh = []
    if tham_so.get("LaKhachMoi"):
        cac_lenh.append((THEM_KHACH_HANG, tham_so, True))
        cac_lenh.append((THEM_SDT_KHACH_HANG, tham_so, True))
    cac_lenh.append((DAT_DON, tham_so, True))
    cac_lenh.append((TRU_CHO, tham_so, True))
    if tham_so.get("GioDon"):
        cac_lenh.append((DON_TAI_NHA, tham_so, True))
    if tham_so.get("GioVeNoiNghi"):
        cac_lenh.append((VE_NOI_NGHI, tham_so, True))
    ghi(cac_lenh)


# Nạp danh sách lịch trình
try:
    ds_lich_trinh = doc(SQL_LICH_TRINH, {"HienTai": hien_tai()})
except Exception as loi:
    st.error(thong_bao_loi(loi))
    st.stop()

if not ds_lich_trinh:
    st.warning("Hiện tại không có lịch trình nào còn chỗ và chưa khởi hành.")
    st.stop()

# ----------------- 1. THÔNG TIN KHÁCH HÀNG -----------------
st.subheader("1. Thông tin khách hàng")

c_ten, c_sdt = st.columns(2)
with c_ten:
    ho_ten_nhap = st.text_input("Họ và tên khách hàng (*)", placeholder="Ví dụ: Nguyễn Văn A", max_chars=100)
with c_sdt:
    sdt_nhap = st.text_input("Số điện thoại (10 chữ số) (*)", placeholder="Ví dụ: 0123456789", max_chars=10)

c_email, c_dc = st.columns(2)
with c_email:
    email_nhap = st.text_input("Email (*)", placeholder="Ví dụ: nguyenvana@gmail.com", max_chars=100)
with c_dc:
    dia_chi_nhap = st.text_input("Địa chỉ liên hệ (*)", placeholder="Ví dụ: số 123, đường ABC, thành phố XYZ", max_chars=255)

ma_kh = None
la_khach_moi = True
ho_ten_chot = ho_ten_nhap.strip()
email_chot = email_nhap.strip()
sdt_chot = sdt_nhap.strip()
dia_chi_chot = dia_chi_nhap.strip()

# Danh sách thu thập lỗi trên toàn bộ form
cac_loi_form = []

# Kiểm tra định dạng cơ bản tại chỗ nhập
loi_sdt_inline = None
if sdt_chot and not re.match(r"^0[0-9]{9}$", sdt_chot):
    loi_sdt_inline = "Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0."
    cac_loi_form.append(loi_sdt_inline)

loi_email_inline = None
if email_chot and not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_chot):
    loi_email_inline = "Email không đúng định dạng (ví dụ: ten@domain.com)."
    cac_loi_form.append(loi_email_inline)

if loi_sdt_inline:
    st.error(f"⚠️ {loi_sdt_inline}")
if loi_email_inline:
    st.error(f"⚠️ {loi_email_inline}")

# Kiểm tra: Đối chiếu CSDL khi đã nhập đủ Họ tên, Số điện thoại và Email hợp lệ
da_nhap_thong_tin_dinh_danh = bool(ho_ten_chot and sdt_chot and email_chot and not loi_sdt_inline and not loi_email_inline)

if da_nhap_thong_tin_dinh_danh:
    # 1. Kiểm tra khớp cả 3 thông tin định danh: Họ tên, Số điện thoại và Email
    try:
        kq_khop = doc(
            SQL_KHOP_THONG_TIN_KH,
            {
                "HoTen": ho_ten_chot,
                "SoDienThoai": sdt_chot,
                "Email": email_chot,
            },
        )
    except Exception:
        kq_khop = []

    if kq_khop:
        # Trùng Họ tên, Số điện thoại và Email -> Gắn với khách hàng cũ
        kh_info = kq_khop[0]
        ma_kh = kh_info["MaKH"]
        la_khach_moi = False

        st.success(f"Khách hàng cũ đã có thông tin trong hệ thống: **{kh_info['MaKH']} - {kh_info['HoTen']}**")
        st.markdown(
            f"""
            - **Mã khách hàng:** `{kh_info['MaKH']}`
            - **Họ và tên:** {kh_info['HoTen']}
            - **Số điện thoại:** {kh_info['SoDienThoai']}
            - **Email:** {kh_info['Email']}
            """
        )
        st.info("Hệ thống sẽ tự động liên kết đơn đặt tour với hồ sơ khách hàng hiện có.")
    else:
        # 2. Không khớp cả 3: kiểm tra xem Email hoặc SĐT đã có trong DB chưa
        try:
            kq_trung = doc(
                SQL_KIEM_TRA_TRUNG_EMAIL_SDT,
                {
                    "Email": email_chot,
                    "SoDienThoai": sdt_chot,
                },
            )
            trung_email = kq_trung[0]["TrungEmail"] > 0 if kq_trung else False
            trung_sdt = kq_trung[0]["TrungSDT"] > 0 if kq_trung else False
        except Exception:
            trung_email = False
            trung_sdt = False

        if trung_email and trung_sdt:
            thong_bao_trung = "Cả Email và số điện thoại này đã được sử dụng trong hệ thống (Họ tên không khớp). Vui lòng kiểm tra lại!"
            st.error(f"Cảnh báo: {thong_bao_trung}")
            cac_loi_form.append(thong_bao_trung)
        elif trung_email:
            thong_bao_trung = "Email này đã được sử dụng bởi khách hàng khác trong hệ thống. Vui lòng kiểm tra lại họ tên hoặc nhập email khác!"
            st.error(f"Cảnh báo: {thong_bao_trung}")
            cac_loi_form.append(thong_bao_trung)
        elif trung_sdt:
            thong_bao_trung = "Số điện thoại này đã được sử dụng bởi khách hàng khác trong hệ thống. Vui lòng kiểm tra lại họ tên hoặc nhập số điện thoại khác!"
            st.error(f"Cảnh báo: {thong_bao_trung}")
            cac_loi_form.append(thong_bao_trung)
        else:
            # Hoàn toàn không trùng -> Khách hàng mới
            la_khach_moi = True
            st.info("Khách hàng mới: Thông tin sẽ được tự động lưu vào hệ thống khi xác nhận đặt tour.")
else:
    if not (loi_sdt_inline or loi_email_inline):
        st.caption("Vui lòng điền đủ Họ tên, Số điện thoại, Email và Địa chỉ để hệ thống kiểm tra và xác nhận hồ sơ.")

# ----------------- 2. THÔNG TIN CHUYẾN ĐI -----------------
st.markdown("---")
st.subheader("2. Thông tin chuyến đi")

idx_lt = st.selectbox(
    "Lịch trình còn chỗ (*)",
    range(len(ds_lich_trinh)),
    format_func=lambda i: (
        f"{ds_lich_trinh[i]['TenTour']} | Khởi hành: {dinh_dang_ngay(ds_lich_trinh[i]['NgayXuatPhat'])} "
        f"| Giá: {dinh_dang_tien(ds_lich_trinh[i]['GiaCoBan'])} | Còn: {ds_lich_trinh[i]['SoChoConLai']} chỗ"
    ),
    help="Chỉ liệt kê các lịch trình chưa khởi hành và còn chỗ",
)
lt_chon = ds_lich_trinh[idx_lt]
ma_lich_trinh = lt_chon["MaLichTrinh"]
so_cho_con_lai = int(lt_chon["SoChoConLai"])
so_dem = int(lt_chon["SoDem"])
ma_tinh_den = lt_chon["MaTinhDen"]
ngay_xuat_phat = lt_chon["NgayXuatPhat"]
ngay_ket_thuc = lt_chon["NgayKetThuc"]
gia_co_ban = lt_chon["GiaCoBan"]

col_sk, col_nn, col_sp = st.columns([1, 2, 1])

with col_sk:
    so_khach = st.number_input(
        "Số lượng khách (*)",
        min_value=1,
        max_value=max(1, so_cho_con_lai),
        value=1,
        step=1,
        help=f"Từ 1 đến số chỗ còn lại của chuyến ({so_cho_con_lai} chỗ).",
    )

ma_nha_nghi = None
gia_phong_moi_dem = 0
so_phong = 0
ten_nha_nghi_chon = None

if so_dem == 0:
    with col_nn:
        st.text_input("Nơi nghỉ", value="Tour trong ngày (0 đêm) - Không áp dụng lưu trú", disabled=True)
    with col_sp:
        st.text_input("Số phòng", value="0", disabled=True)
else:
    try:
        ds_noi_nghi = doc(SQL_NOI_NGHI, {"MaTinhDen": ma_tinh_den})
    except Exception as loi:
        st.error(thong_bao_loi(loi))
        st.stop()

    with col_nn:
        cac_lua_chon_nn = [
            {"MaNhaNghi": None, "TenNhaNghi": "Không đặt nơi nghỉ", "LoaiHinh": "", "GiaPhongMoiDem": 0}
        ] + ds_noi_nghi
        idx_nn = st.selectbox(
            "Nơi nghỉ (lọc theo tỉnh đến)",
            range(len(cac_lua_chon_nn)),
            format_func=lambda i: (
                "Không đặt nơi nghỉ"
                if i == 0
                else f"{cac_lua_chon_nn[i]['TenNhaNghi']} ({cac_lua_chon_nn[i]['LoaiHinh']}) - {dinh_dang_tien(cac_lua_chon_nn[i]['GiaPhongMoiDem'])}/đêm"
            ),
            help="Tự động lọc nhà nghỉ, homestay tại đúng tỉnh điểm đến của tour",
        )
        nn_chon = cac_lua_chon_nn[idx_nn]
        ma_nha_nghi = nn_chon["MaNhaNghi"]
        gia_phong_moi_dem = nn_chon["GiaPhongMoiDem"]
        ten_nha_nghi_chon = nn_chon["TenNhaNghi"]

    with col_sp:
        if ma_nha_nghi:
            so_phong = st.number_input(
                "Số phòng (*)",
                min_value=1,
                value=1,
                step=1,
                help="Số phòng phải từ 1 đến số khách",
            )
            if so_phong > so_khach:
                loi_sp = f"Số phòng ({so_phong}) không được vượt quá số khách ({so_khach})."
                st.error(f"⚠️ {loi_sp}")
                cac_loi_form.append(loi_sp)
        else:
            so_phong = 0
            st.text_input("Số phòng", value="0", disabled=True)

# ----------------- 3. XE TRUNG CHUYỂN -----------------
st.markdown("---")
st.subheader("3. Đăng ký xe trung chuyển (tối đa 2 chuyến)")
col_xe1, col_xe2 = st.columns(2)

with col_xe1:
    co_xe_don = st.checkbox("Cần xe đón tại nhà", value=False)
    dia_chi_don = ""
    gio_don_str = None
    dt_don = None
    if co_xe_don:
        dia_chi_don = st.text_input(
            "Địa chỉ đón (*)",
            value=dia_chi_chot,
            max_chars=255,
            placeholder="Nhập địa chỉ đón khách",
            key=f"dia_chi_don_{ma_kh if ma_kh else 'moi'}",
        )
        if not dia_chi_don.strip():
            loi_dc_don = "Vui lòng nhập địa chỉ đón khi chọn xe đón tại nhà."
            st.error(f"{loi_dc_don}")
            cac_loi_form.append(loi_dc_don)

        thoi_gian_mac_dinh_don = ngay_xuat_phat - timedelta(hours=2)
        c_ngay_don, c_gio_don = st.columns(2)
        with c_ngay_don:
            ngay_don = st.date_input("Ngày đón (*)", value=thoi_gian_mac_dinh_don.date(), key=f"ngay_don_{ma_lich_trinh}")
        with c_gio_don:
            gio_don = st.time_input("Giờ đón (*)", value=thoi_gian_mac_dinh_don.time(), key=f"gio_don_{ma_lich_trinh}")
        dt_don = datetime.combine(ngay_don, gio_don)
        gio_don_str = dt_don.strftime("%Y-%m-%d %H:%M:%S")

        if dt_don <= hien_tai() or dt_don >= ngay_xuat_phat:
            loi_gio_don = f"Giờ đón tại nhà ({dt_don.strftime('%d/%m/%Y %H:%M')}) phải sau thời điểm hiện tại và trước giờ xuất phát."
            st.error(f"{loi_gio_don}")
            cac_loi_form.append(loi_gio_don)

with col_xe2:
    co_xe_ve = False
    gio_ve_str = None
    dt_ve = None
    if ma_nha_nghi is not None:
        co_xe_ve = st.checkbox("Cần xe về nơi nghỉ", value=False)
        if co_xe_ve:
            thoi_gian_mac_dinh_ve = ngay_xuat_phat + timedelta(hours=4)
            if thoi_gian_mac_dinh_ve > ngay_ket_thuc:
                thoi_gian_mac_dinh_ve = ngay_xuat_phat
            c_ngay_ve, c_gio_ve = st.columns(2)
            with c_ngay_ve:
                ngay_ve = st.date_input("Ngày về nơi nghỉ (*)", value=thoi_gian_mac_dinh_ve.date(), key=f"ngay_ve_{ma_lich_trinh}")
            with c_gio_ve:
                gio_ve = st.time_input("Giờ về nơi nghỉ (*)", value=thoi_gian_mac_dinh_ve.time(), key=f"gio_ve_{ma_lich_trinh}")
            dt_ve = datetime.combine(ngay_ve, gio_ve)
            gio_ve_str = dt_ve.strftime("%Y-%m-%d %H:%M:%S")

            if dt_ve < ngay_xuat_phat or dt_ve > ngay_ket_thuc:
                loi_gio_ve = f"Giờ về nơi nghỉ ({dt_ve.strftime('%d/%m/%Y %H:%M')}) phải nằm trong khoảng thời gian diễn ra tour."
                st.error(f"{loi_gio_ve}")
                cac_loi_form.append(loi_gio_ve)
    else:
        st.info("Chuyến xe về nơi nghỉ chỉ áp dụng khi khách có đăng ký nơi nghỉ.")

# ----------------- 4. DỰ TOÁN VÀ XÁC NHẬN -----------------
st.markdown("---")
tien_tour = so_khach * gia_co_ban
tien_phong = so_phong * gia_phong_moi_dem * so_dem if ma_nha_nghi else 0
tong_tien_du_kien = tien_tour + tien_phong

st.subheader("4. Dự toán chi phí và Xác nhận")
m1, m2, m3 = st.columns(3)
m1.metric("Tiền tour cơ bản", dinh_dang_tien(tien_tour), f"{so_khach} khách x {dinh_dang_tien(gia_co_ban)}")
m2.metric(
    "Tiền phòng lưu trú",
    dinh_dang_tien(tien_phong),
    f"{so_phong} phòng x {so_dem} đêm x {dinh_dang_tien(gia_phong_moi_dem)}" if ma_nha_nghi else "Không đặt nơi nghỉ",
)
m3.metric("TỔNG TIỀN DỰ KIẾN", dinh_dang_tien(tong_tien_du_kien))

# Tổng hợp tất cả các lỗi trên form
cac_loi_tong = []

# 1. Kiểm tra họ và tên
if not ho_ten_chot:
    cac_loi_tong.append("Chưa nhập họ và tên khách hàng.")

# 2. Kiểm tra số điện thoại
if not sdt_chot:
    cac_loi_tong.append("Chưa nhập số điện thoại khách hàng.")
elif not re.match(r"^0[0-9]{9}$", sdt_chot):
    cac_loi_tong.append("Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0.")

# 3. Kiểm tra email
if not email_chot:
    cac_loi_tong.append("Chưa nhập email khách hàng.")
elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_chot):
    cac_loi_tong.append("Email không đúng định dạng (ví dụ: ten@domain.com).")

# 4. Kiểm tra địa chỉ
if not dia_chi_chot:
    cac_loi_tong.append("Chưa nhập địa chỉ liên hệ của khách hàng.")

# 5. Thêm tất cả lỗi thu thập từ các phần nhập liệu (trùng email/sđt, số phòng, giờ đón, giờ về...)
cac_loi_tong.extend(cac_loi_form)

# Loại bỏ các lỗi trùng lặp nếu có
cac_loi_tong = list(dict.fromkeys(cac_loi_tong))

# Hiển thị cảnh báo tổng quan nếu form có lỗi
if cac_loi_tong:
    st.warning(f"⚠️ Form đang có **{len(cac_loi_tong)}** thông tin chưa hợp lệ. Vui lòng kiểm tra lại các mục báo đỏ ở trên trước khi bấm xác nhận.")

# Nút xác nhận đặt tour
if st.button("Xác nhận đặt tour", type="primary", use_container_width=True):
    # NẾU CÓ BẤT KỲ LỖI NÀO: CHẶN NGAY LẬP TỨC, TUYỆT ĐỐI KHÔNG INSERT VÀO DATABASE
    if cac_loi_tong:
        st.error("**Không thể xác nhận đặt tour vì các thông tin sau chưa hợp lệ:**")
        for loi in cac_loi_tong:
            st.error(f"- {loi}")
        st.stop()

    # Xác định khách hàng và kiểm tra lại CSDL một lần nữa trước khi lưu
    kq_khop_submit = doc(
        SQL_KHOP_THONG_TIN_KH,
        {
            "HoTen": ho_ten_chot,
            "SoDienThoai": sdt_chot,
            "Email": email_chot,
        },
    )

    if kq_khop_submit:
        # Khớp 3 thông tin (Họ tên, SĐT, Email) -> khách hàng cũ, tái sử dụng MaKH
        ma_kh_luu = kq_khop_submit[0]["MaKH"]
        la_khach_moi_luu = False
    else:
        # Kiểm tra xem Email hoặc SĐT có bị trùng với ai trong hệ thống không
        kq_check_trung = doc(
            SQL_KIEM_TRA_TRUNG_EMAIL_SDT,
            {
                "Email": email_chot,
                "SoDienThoai": sdt_chot,
            },
        )
        trung_email = kq_check_trung[0]["TrungEmail"] > 0 if kq_check_trung else False
        trung_sdt = kq_check_trung[0]["TrungSDT"] > 0 if kq_check_trung else False

        if trung_email and trung_sdt:
            st.error("Cả Email và số điện thoại này đều đã được sử dụng trong hệ thống. Vui lòng kiểm tra và nhập lại!")
            st.stop()
        elif trung_email:
            st.error("Email này đã được sử dụng trong hệ thống. Vui lòng nhập lại email khác!")
            st.stop()
        elif trung_sdt:
            st.error("Số điện thoại này đã được sử dụng trong hệ thống. Vui lòng nhập lại số điện thoại khác!")
            st.stop()

        # Khách hàng mới hoàn toàn -> Cấp mã khách hàng mới
        la_khach_moi_luu = True
        try:
            kq_kh = doc(SQL_MA_KH_MOI)
            ma_kh_luu = kq_kh[0]["MaKHMoi"] if kq_kh else "KH001"
        except Exception as loi:
            st.error(thong_bao_loi(loi))
            st.stop()

    # Kiểm tra thêm số chỗ còn lại của lịch trình (Lớp 1)
    if so_cho_con_lai <= 0:
        st.error("Lịch trình đã hết chỗ, không thể đặt thêm.")
        st.stop()

    if so_khach < 1 or so_khach > so_cho_con_lai:
        st.error(f"Số lượng khách ({so_khach}) không hợp lệ (còn lại: {so_cho_con_lai} chỗ).")
        st.stop()

    if ma_nha_nghi and (so_phong < 1 or so_phong > so_khach):
        st.error(f"Số phòng ({so_phong}) phải từ 1 đến số khách ({so_khach}).")
        st.stop()

    if co_xe_don:
        if not dia_chi_don.strip():
            st.error("Vui lòng nhập địa chỉ đón khi chọn xe đón tại nhà.")
            st.stop()
        if dt_don <= hien_tai() or dt_don >= ngay_xuat_phat:
            st.error("Giờ đón tại nhà phải sau thời điểm hiện tại và trước giờ xuất phát.")
            st.stop()

    if co_xe_ve:
        if not ma_nha_nghi:
            st.error("Chỉ có thể đăng ký xe về nơi nghỉ khi có đặt nơi nghỉ.")
            st.stop()
        if dt_ve < ngay_xuat_phat or dt_ve > ngay_ket_thuc:
            st.error("Giờ về nơi nghỉ phải nằm trong khoảng thời gian diễn ra tour.")
            st.stop()

    # Sinh mã đơn hàng mới (F1.4)
    try:
        kq_ma = doc(SQL_MA_DON_MOI)
        ma_don_moi = kq_ma[0]["MaDonHangMoi"] if kq_ma else "DH001"
    except Exception as loi:
        st.error(thong_bao_loi(loi))
        st.stop()

    # Chuẩn bị tham số và gọi luu_don trong 1 transaction (F1.6)
    tham_so_luu = {
        "LaKhachMoi": la_khach_moi_luu,
        "HoTen": ho_ten_chot,
        "Email": email_chot,
        "SoDienThoai": sdt_chot,
        "DiaChi": dia_chi_chot,
        "MaDonHang": ma_don_moi,
        "SoKhach": so_khach,
        "SoPhong": so_phong,
        "MaKH": ma_kh_luu,
        "MaLichTrinh": ma_lich_trinh,
        "MaNhaNghi": ma_nha_nghi,
        "DiaChiDon": dia_chi_don.strip() if co_xe_don else None,
        "GioDon": gio_don_str if co_xe_don else None,
        "GioVeNoiNghi": gio_ve_str if co_xe_ve else None,
    }

    try:
        luu_don(tham_so_luu)
        st.success(f"Đã đặt tour thành công cho khách hàng **{ho_ten_chot}**! Mã đơn đặt tour: **{ma_don_moi}**, tổng tiền: **{dinh_dang_tien(tong_tien_du_kien)}**.")
        st.balloons()
    except Exception as loi:
        st.error(thong_bao_loi(loi))
