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

# Kiểm tra khớp đầy đủ 4 thông tin khách hàng (trừ mã khách hàng)
SQL_KHOP_THONG_TIN_KH = """
SELECT kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi, sdt.SoDienThoai
FROM KhachHang kh
JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
WHERE LOWER(kh.HoTen) = LOWER(%(HoTen)s)
  AND sdt.SoDienThoai = %(SoDienThoai)s
  AND LOWER(kh.Email) = LOWER(%(Email)s)
  AND LOWER(COALESCE(kh.DiaChi, '')) = LOWER(%(DiaChi)s)
LIMIT 1;
"""

# Kiểm tra trùng lặp Email hoặc SĐT đã có trong hệ thống để tránh ghi thừa/lỗi khóa UNIQUE
SQL_KIEM_TRA_TRUNG_EMAIL_SDT = """
SELECT kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi,
       GROUP_CONCAT(DISTINCT sdt.SoDienThoai SEPARATOR ', ') AS CacSDT
FROM KhachHang kh
LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
WHERE LOWER(kh.Email) = LOWER(%(Email)s)
   OR sdt.SoDienThoai = %(SoDienThoai)s
GROUP BY kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi
LIMIT 1;
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
st.caption("Vui lòng điền đủ 4 thông tin: Họ tên, Số điện thoại, Email và Địa chỉ liên hệ.")

c_ten, c_sdt = st.columns(2)
with c_ten:
    ho_ten_nhap = st.text_input("Họ và tên khách hàng (*)", placeholder="Ví dụ: Vũ Thị Hà", max_chars=100)
with c_sdt:
    sdt_nhap = st.text_input("Số điện thoại (10 chữ số) (*)", placeholder="Ví dụ: 0398765432", max_chars=10)

c_email, c_dc = st.columns(2)
with c_email:
    email_nhap = st.text_input("Email (*)", placeholder="Ví dụ: ha.vu@gmail.com", max_chars=100)
with c_dc:
    dia_chi_nhap = st.text_input("Địa chỉ liên hệ (*)", placeholder="Ví dụ: 3 Hùng Vương, Lào Cai", max_chars=255)

ma_kh = None
la_khach_moi = True
ho_ten_chot = ho_ten_nhap.strip()
email_chot = email_nhap.strip()
sdt_chot = sdt_nhap.strip()
dia_chi_chot = dia_chi_nhap.strip()

# Kiểm tra: Chỉ khi người dùng đã nhập đủ cả 4 thông tin thì mới đối chiếu CSDL
da_nhap_du_4_thong_tin = bool(ho_ten_chot and sdt_chot and email_chot and dia_chi_chot)

if da_nhap_du_4_thong_tin:
    # 1. Kiểm tra khớp tất cả 4 thuộc tính (trừ mã khách hàng)
    try:
        kq_khop = doc(
            SQL_KHOP_THONG_TIN_KH,
            {
                "HoTen": ho_ten_chot,
                "SoDienThoai": sdt_chot,
                "Email": email_chot,
                "DiaChi": dia_chi_chot,
            },
        )
    except Exception:
        kq_khop = []

    if kq_khop:
        # Khớp toàn bộ 4 thuộc tính -> Nhận diện chính xác 100% khách hàng cũ, không sợ trùng tên
        kh_info = kq_khop[0]
        ma_kh = kh_info["MaKH"]
        la_khach_moi = False

        st.success("✅ Khách hàng đã có thông tin trong cơ sở dữ liệu (khớp đầy đủ tất cả thông tin):")
        st.markdown(
            f"""
            - **Họ và tên:** {kh_info['HoTen']}
            - **Số điện thoại:** {kh_info['SoDienThoai']}
            - **Email:** {kh_info['Email']}
            - **Địa chỉ:** {kh_info['DiaChi']}
            """
        )
        st.info("📌 Hệ thống sẽ tự động liên kết đơn đặt tour với hồ sơ khách hàng hiện có. Không tạo bản ghi trùng lặp.")
    else:
        # 2. Nếu không khớp cả 4, kiểm tra xem Email hoặc SĐT đã có trong DB chưa để xử lý trường hợp bấm tạo mới gây thừa/lỗi
        try:
            kq_trung = doc(
                SQL_KIEM_TRA_TRUNG_EMAIL_SDT,
                {
                    "Email": email_chot,
                    "SoDienThoai": sdt_chot,
                },
            )
        except Exception:
            kq_trung = []

        if kq_trung:
            # Phát hiện Email hoặc SĐT đã có chủ
            kh_trung = kq_trung[0]
            ma_kh = kh_trung["MaKH"]
            la_khach_moi = False

            st.warning(
                f"⚠️ Email hoặc Số điện thoại này đã thuộc về khách hàng trong hệ thống: **{kh_trung['HoTen']}** "
                f"({kh_trung['Email']} | SĐT: {kh_trung['CacSDT']})."
            )
            st.info("📌 Để tránh tạo bản ghi dư thừa và lỗi trùng lặp dữ liệu, đơn đặt tour sẽ được gắn vào hồ sơ khách hàng đã có này.")
        else:
            # Hoàn toàn mới
            la_khach_moi = True
            st.info("✨ Khách hàng mới: Thông tin sẽ được tự động lưu vào cơ sở dữ liệu khi xác nhận đặt tour.")
else:
    st.caption("ℹ️ Vui lòng điền đủ 4 thông tin (Họ tên, Số điện thoại, Email, Địa chỉ) để hệ thống kiểm tra và xác nhận hồ sơ.")

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
            help="Tự động lọc nhà nghỉ, homestay tại đúng tỉnh điểm đến của tour (RB24)",
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
                help="Số phòng phải từ 1 đến số khách (RB16)",
            )
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
        thoi_gian_mac_dinh_don = ngay_xuat_phat - timedelta(hours=2)
        c_ngay_don, c_gio_don = st.columns(2)
        with c_ngay_don:
            ngay_don = st.date_input("Ngày đón (*)", value=thoi_gian_mac_dinh_don.date(), key=f"ngay_don_{ma_lich_trinh}")
        with c_gio_don:
            gio_don = st.time_input("Giờ đón (*)", value=thoi_gian_mac_dinh_don.time(), key=f"gio_don_{ma_lich_trinh}")
        dt_don = datetime.combine(ngay_don, gio_don)
        gio_don_str = dt_don.strftime("%Y-%m-%d %H:%M:%S")

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
    else:
        st.info("Chuyến xe về nơi nghỉ chỉ áp dụng khi khách có đăng ký nơi nghỉ (RB27).")

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

# Nút xác nhận đặt tour
if st.button("Xác nhận đặt tour", type="primary", use_container_width=True):
    # Validation thông tin khách hàng
    if not ho_ten_chot:
        st.error("Vui lòng nhập họ và tên khách hàng.")
        st.stop()

    if not sdt_chot:
        st.error("Vui lòng nhập số điện thoại khách hàng.")
        st.stop()

    if not re.match(r"^0[0-9]{9}$", sdt_chot):
        st.error("Số điện thoại phải gồm đúng 10 chữ số và bắt đầu bằng số 0 (RB02).")
        st.stop()

    if not email_chot:
        st.error("Vui lòng nhập email khách hàng.")
        st.stop()

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_chot):
        st.error("Email không hợp lệ (ví dụ đúng: ten@domain.com).")
        st.stop()

    if not dia_chi_chot:
        st.error("Vui lòng nhập địa chỉ liên hệ của khách hàng.")
        st.stop()

    # Xử lý chống thêm bản ghi dư thừa / lỗi khóa UNIQUE trong database
    # Kiểm tra lại một lần nữa trong CSDL trước khi quyết định insert hay reuse
    check_kh = doc(
        """
        SELECT kh.MaKH FROM KhachHang kh
        LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
        WHERE LOWER(kh.Email) = LOWER(%(Email)s)
           OR sdt.SoDienThoai = %(SoDienThoai)s
           OR (LOWER(kh.HoTen) = LOWER(%(HoTen)s) AND LOWER(COALESCE(kh.DiaChi, '')) = LOWER(%(DiaChi)s))
        LIMIT 1;
        """,
        {
            "Email": email_chot,
            "SoDienThoai": sdt_chot,
            "HoTen": ho_ten_chot,
            "DiaChi": dia_chi_chot,
        },
    )

    if check_kh:
        # Đã tồn tại khách hàng này trong database -> Sử dụng lại MaKH, KHÔNG insert mới
        ma_kh = check_kh[0]["MaKH"]
        la_khach_moi = False
    elif la_khach_moi:
        try:
            kq_kh = doc(SQL_MA_KH_MOI)
            ma_kh = kq_kh[0]["MaKHMoi"] if kq_kh else "KH001"
        except Exception as loi:
            st.error(thong_bao_loi(loi))
            st.stop()

    # Validation tầng form chuyến đi (Lớp 1)
    if so_cho_con_lai <= 0:
        st.error("Lịch trình đã hết chỗ, không thể đặt thêm.")
        st.stop()

    if so_khach < 1:
        st.error("Số lượng khách phải lớn hơn 0.")
        st.stop()

    if so_khach > so_cho_con_lai:
        st.error(f"Số lượng khách ({so_khach}) vượt quá số chỗ còn lại ({so_cho_con_lai}).")
        st.stop()

    if ma_nha_nghi:
        if so_phong < 1 or so_phong > so_khach:
            st.error("Số phòng phải từ 1 đến số khách")
            st.stop()
    else:
        so_phong = 0

    if co_xe_don:
        if not dia_chi_don.strip():
            st.error("Vui lòng nhập địa chỉ đón")
            st.stop()
        if dt_don <= hien_tai() or dt_don >= ngay_xuat_phat:
            st.error("Giờ đón tại nhà phải sau thời điểm hiện tại và trước giờ xuất phát")
            st.stop()

    if co_xe_ve:
        if not ma_nha_nghi:
            st.error("Chỉ có thể đăng ký xe về nơi nghỉ khi có đặt nơi nghỉ")
            st.stop()
        if dt_ve < ngay_xuat_phat or dt_ve > ngay_ket_thuc:
            st.error("Giờ về nơi nghỉ phải nằm trong khoảng thời gian diễn ra tour")
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
        "LaKhachMoi": la_khach_moi,
        "HoTen": ho_ten_chot,
        "Email": email_chot,
        "SoDienThoai": sdt_chot,
        "DiaChi": dia_chi_chot,
        "MaDonHang": ma_don_moi,
        "SoKhach": so_khach,
        "SoPhong": so_phong,
        "MaKH": ma_kh,
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
