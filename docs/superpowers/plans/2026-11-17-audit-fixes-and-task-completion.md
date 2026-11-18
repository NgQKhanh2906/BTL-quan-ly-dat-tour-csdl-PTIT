# Audit Fixes and Task Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sửa toàn bộ lỗi liên kết Frontend–Backend–Database, bổ sung bộ kiểm thử tự động theo TDD, và hoàn thiện các task còn thiếu của 4 thành viên (Khánh, Đạt, Tuân, Thịnh) trên dự án Hệ thống Quản lý Đặt Tour Du lịch Miền Bắc.

**Architecture:** Ứng dụng web đa trang viết bằng Streamlit (`tour_app/app.py` và `tour_app/pages/1..6_*.py`), giao tiếp MySQL 8.0 qua lớp truy cập dữ liệu tập trung `tour_app/db.py` (parameterized queries + transaction `ghi()`), kết hợp xuất biểu mẫu A4 qua HTML templates (`tour_app/templates/*.html`). Mọi nghiệp vụ liên bảng được kiểm tra hai lớp (Form Python + ràng buộc khai báo MySQL và hậu kiểm bằng `database/4_KiemTra_RangBuoc.sql`).

**Tech Stack:** Python 3.11 (`tour_app/.venv`), Streamlit `1.66.0`, `mysql-connector-python` `26.7.0`, `pandas` `3.0.6`, MySQL Server 8.0 (`QuanLyDatTour`), `unittest` / `pytest`, Chrome/Edge & `chrome-devtools` MCP cho kiểm thử E2E và xuất PDF A4.

**Spec:**
- [Ke_hoach_Tong_hop_BTL_CSDL.md](file:///D:/Khanh/CSDL/docs/Ke_hoach_Tong_hop_BTL_CSDL.md)
- [1_QuanLyDatTour_v3.sql](file:///D:/Khanh/CSDL/database/1_QuanLyDatTour_v3.sql)
- [3_QuanLyDatTour_v3_UngDung.sql](file:///D:/Khanh/CSDL/database/3_QuanLyDatTour_v3_UngDung.sql)
- [4_KiemTra_RangBuoc.sql](file:///D:/Khanh/CSDL/database/4_KiemTra_RangBuoc.sql)
- [Bao_cao_BTL_CSDL_QuanLyDatTour.docx](file:///D:/Khanh/CSDL/docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx)

## Global Constraints

- CSDL `QuanLyDatTour` (`utf8mb4_0900_ai_ci`) giữ nguyên cấu trúc 12 bảng, 2 view (`v_DonHang_ChiTiet`, `v_LichTrungChuyen`), 56 ràng buộc khai báo (`12 PK`, `13 FK`, `27 CHECK`, `4 UNIQUE`) và 104 dòng mẫu; không dùng Stored Procedure, Function hoặc Trigger.
- Toàn bộ truy vấn SQL trong Python phải dùng parameterized queries (`%s` hoặc `%(Ten)s`), tuyệt đối không nối chuỗi input người dùng.
- Mật khẩu MySQL đọc qua biến môi trường `MYSQL_PASSWORD` trong `tour_app/db.py`, tuyệt đối không ghi cứng mật khẩu vào mã nguồn.
- Chế độ demo `CHE_DO_DEMO = True` cố định `hien_tai()` tại `2026-10-23 08:00:00`.
- Tầng ứng dụng chỉ dùng giao diện tiếng Việt, không để lộ Python traceback ra UI khi CSDL lỗi hoặc tắt; kiểm tra đầu vào hai lớp (Form + MySQL).
- Báo cáo `R1` xuất PDF khổ A4 dọc (Portrait) vừa khít **1 trang** cho cả `DH007` và `DH008`; báo cáo `R2` xuất PDF khổ A4 ngang (Landscape) vừa khít **1 trang**, có người lập, nơi nhận và khối ký; mọi chuỗi chèn vào HTML phải qua `html.escape()`.
- Mọi thao tác sửa dữ liệu trong kiểm thử tự động phải khôi phục hoặc kiểm tra lại `database/4_KiemTra_RangBuoc.sql` trả về **0 dòng** vi phạm.

## Review Focus

1. **MySQL tắt, sai mật khẩu hoặc bảng rỗng (`KhachHang`, `DonHang`, `LichTrinh`):** Mọi màn hình (`F1`, `F2`, `F3`, `S1`, `R1`, `R2`) phải bắt ngoại lệ quanh mọi lệnh `doc()` và `ghi()`, hiển thị thông báo tiếng Việt qua `thong_bao_loi()`, và xử lý an toàn khi danh sách trả về rỗng (`[]`) không văng `IndexError`/`TypeError`.
2. **Xung đột đồng thời và khóa duy nhất (`KhongCoDongNao`, lỗi `1062`):** Thao tác đồng thời trên `F2` (hủy/chuyển trạng thái 2 tab), `F3` (gửi đánh giá 2 tab) và sinh mã mới trên `F1` (`MaKH`, `MaDonHang`) không được trừ chỗ 2 lần hay ghi trùng.
3. **Các ca biên của `F1` (khách hàng và dịch vụ đi kèm):** Tour trong ngày (`SoDem == 0`, ví dụ `LT06`) phải ẩn nơi nghỉ và xe về nơi nghỉ (`SoPhong = 0`); chọn nơi nghỉ phải kiểm tra `1 <= SoPhong <= SoLuongKhach`; khớp khách hàng cũ vs tạo khách mới không được gán nhầm hồ sơ hay bỏ sót Email/SĐT trùng.
4. **Ràng buộc hủy đơn `RB23` và trạng thái widget trên `F2` / `F3` / `S1`:** `F2` phải chặn `NgayHuy >= NgayXuatPhat` (ngoài `NgayHuy < NgayDat`), bắt buộc lý do hủy và xác nhận khách đồng ý mức phạt; đổi đơn trên `F2`/`F3` không rò rỉ input cũ; nút `"Tour cao cấp"` và `"Đặt lại bộ lọc"` trên `S1` phải reset sạch kể cả `gia_den` và các ô vừa chỉnh tay.
5. **Xuất HTML và in A4 (`R1`, `R2`) độc lập thư mục chạy:** Đọc template qua `Path(__file__).resolve().parent.parent / "templates" / ...` để chạy đúng từ cả `D:\Khanh\CSDL` lẫn `D:\Khanh\CSDL\tour_app`; thoát ký tự HTML cho toàn bộ dữ liệu động; kiểm tra `MaTrangThai == 'HUY'` chính xác và xử lý `LyDoHuy`/`SoID` khi `NULL`.

---

## File Structure

- **Logic & Kết nối CSDL:**
  - `tour_app/db.py`: Bổ sung mapping CHECK constraint và mã lỗi MySQL còn thiếu trong `THONG_BAO_CHECK` và `THONG_BAO_MA_LOI`.
  - `tour_app/services.py` *(mới, tách các hàm nghiệp vụ/SQL thuần không phụ thuộc Streamlit UI để kiểm thử TDD trực tiếp không cần mock toàn bộ runtime Streamlit)*.
- **6 màn hình Streamlit & 2 HTML Templates:**
  - `tour_app/pages/1_Dat_tour.py`: Đồng nhất luồng chọn/nhập khách hàng, sửa `try/except`, logic sinh mã và giao dịch, cập nhật state sau lưu.
  - `tour_app/pages/2_Quan_ly_don.py`: Sửa thiếu `try/except`, bổ sung kiểm tra `RB23` (`NgayHuy < NgayXuatPhat`), checkbox xác nhận mức phạt, `st.rerun()`, key theo `MaDonHang`.
  - `tour_app/pages/3_Danh_gia.py`: Sửa lỗi gọi `ghi([(sql, tham_so, True)])`, hiển thị `st.error(thong_bao_loi(e))`, thêm `try/except`, guard rỗng, `dinh_dang_ngay()`, key theo `MaDonHang`, `st.rerun()`.
  - `tour_app/pages/4_Tim_kiem.py`: Gắn `key` và `session_state` đồng bộ cho cả 8 bộ lọc, sửa nút `"Tour cao cấp"` và `"Đặt lại bộ lọc"`, bỏ `use_container_width` deprecated.
  - `tour_app/pages/5_Phieu_xac_nhan.py` & `tour_app/templates/phieu_xac_nhan.html`: Sửa `MaTrangThai == 'HUY'`, `LyDoHuy`/`SoID` `NULL`, hiển thị `ThoiGianDon`/`DiemTapTrung`, thêm `st.download_button`, bổ sung `try/except`, tinh chỉnh CSS để vừa khít **1 trang A4 dọc** cho cả `DH007` và `DH008`.
  - `tour_app/pages/6_Bao_cao_doanh_thu.py` & `tour_app/templates/bao_cao_doanh_thu.html`: Sửa đường dẫn tương đối template bằng `Path(__file__).resolve()`, bổ sung `escape()` cho dữ liệu bảng, xử lý bảng rỗng.
- **Bộ kiểm thử tự động:**
  - `tour_app/tests/test_db_and_services.py` *(mới)*: Kiểm thử đơn vị và tích hợp MySQL cho `db.py` và nghiệp vụ `F1`, `F2`, `F3`, `S1`, `R1`, `R2` + hậu kiểm `4_KiemTra_RangBuoc.sql`.
  - `tour_app/tests/test_pages_smoke.py` *(mới)*: Kiểm thử luồng render/tương tác giao diện Streamlit bằng `streamlit.testing.v1.AppTest` cho cả `app.py` và 6 trang `pages/*.py`.
- **Tài liệu & Thiết kế (tùy phạm vi được duyệt):**
  - `docs/diagrams/ERD.drawio`: Sửa 3 nhãn sai (`NoiDen` -> `DenTai`, `LiDoHuy` -> `LyDoHuy`, `TênTour` -> `TenTour`).
  - `screenshots/`: Chụp bổ sung `Hinh04_F1_GiaoDien.png`, `Hinh05a_F1_Loi.png`, `Hinh05b_F1_Loi.png`; chụp lại `Hinh08_F3_GiaoDien.png`, `Hinh10_R1_ManHinh.png`, `Hinh11_R1_PDF.png` (`DH008` vừa 1 trang A4 dọc không dính header/footer).
  - `docs/GopY_Dat.md`, `docs/GopY_Khanh.md`, `docs/GopY_Thinh.md`, `docs/GopY_Tuan.md`, `README.md`: Cập nhật khớp 100% thực tế code và trạng thái hoàn thành.

---

### Task 1: Hoàn thiện ánh xạ lỗi trong `tour_app/db.py` và dựng nền tảng test

**Files:**
- Modify: `tour_app/db.py:19-34`
- Create: `tour_app/tests/test_db_and_services.py`

**Interfaces:**
- Consumes: `db.doc(sql, tham_so)`, `db.ghi(cac_lenh)`, `db.thong_bao_loi(loi)`, `db.dinh_dang_tien(so)`, `db.dinh_dang_ngay(gia_tri)`, `db.hien_tai()`
- Produces: Đầy đủ thông báo tiếng Việt cho các CHECK constraint (`chk_KhachHang_Email`, `chk_SDT_KhachHang_SoDienThoai`, `chk_DonHang_SoLuongKhach`, `chk_DonHang_Huy`, `chk_DonHang_LyDoHuy`, `chk_DonHang_DanhGia`, `chk_DonHang_DanhGiaNhaNghi`, `chk_DonHang_NgayDanhGia`, `chk_ChuyenTrungChuyen_Loai`, `chk_ChuyenTrungChuyen_DiaChiDon`) và mã lỗi MySQL (`1049`, `1406`, `1451`).

- [ ] **Step 1: Write the failing test**

Viết test `test_thong_bao_loi_covers_check_constraints_and_mysql_errnos` trong `tour_app/tests/test_db_and_services.py` kiểm tra `db.thong_bao_loi(...)` trả về câu tiếng Việt rõ ràng (không chứa `"Lỗi cơ sở dữ liệu, mã"` hay `"Dữ liệu không hợp lệ:"`) cho các ràng buộc `chk_KhachHang_Email`, `chk_SDT_KhachHang_SoDienThoai`, `chk_DonHang_DanhGiaNhaNghi`, `chk_DonHang_SoLuongKhach` và mã lỗi `1451`, `1406`, `1049`.

- [ ] **Step 2: Run test to verify it fails**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py -v`
Expected: FAIL vì `THONG_BAO_CHECK` và `THONG_BAO_MA_LOI` chưa có các khóa mới.

- [ ] **Step 3: Implement mapping additions in `tour_app/db.py`**

Cập nhật `THONG_BAO_CHECK` và `THONG_BAO_MA_LOI` trong `tour_app/db.py:19-34`; kiểm tra `dinh_dang_ngay` xử lý an toàn cả chuỗi ISO lẫn `datetime`.

- [ ] **Step 4: Run test to verify it passes**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py -v`
Expected: PASS.

---

### Task 2: Sửa màn hình `F3` (`tour_app/pages/3_Danh_gia.py`) — Crash `ghi()` và hiển thị lỗi

**Files:**
- Modify: `tour_app/pages/3_Danh_gia.py:1-151`
- Modify: `tour_app/services.py` (tạo helper `lay_khach_hang()`, `lay_don_cho_danh_gia(ma_kh)`, `luu_danh_gia(...)`)
- Test: `tour_app/tests/test_db_and_services.py`, `tour_app/tests/test_pages_smoke.py`

**Interfaces:**
- Consumes: `db.doc`, `db.ghi`, `db.hien_tai`, `db.dinh_dang_ngay`, `db.dinh_dang_tien`, `db.thong_bao_loi`
- Produces: `luu_danh_gia(ma_don, diem_tour, nx_tour, diem_nn, nx_nn, ngay_dg) -> None` (gọi `ghi([(sql, tham_so, True)])`), UI `3_Danh_gia.py` hiển thị lỗi qua `st.error(thong_bao_loi(e))`, bọc `try/except` mọi `doc()`, gắn `key` theo `MaDonHang`, và gọi `st.rerun()` sau khi lưu thành công (giữ thông báo thành công qua `session_state`).

- [ ] **Step 1: Write the failing tests**

1. Trong `test_db_and_services.py`: `test_f3_luu_danh_gia_thanh_cong_va_chan_danh_gia_lan_2` — kiểm tra đánh giá `DH004` thành công, `NgayDanhGia` được cập nhật, đánh giá lại lần 2 ném `db.KhongCoDongNao`, sau đó rollback/reset lại trạng thái gốc của `DH004`.
2. Trong `test_pages_smoke.py`: `test_f3_page_renders_and_submits_without_crash` — dùng `AppTest.from_file("tour_app/pages/3_Danh_gia.py")` chọn `KH004` (`DH004`), kiểm tra định dạng ngày `dd/mm/yyyy HH:MM`, kiểm tra Ca 3 (nhập nhận xét nhà nghỉ, bỏ tick chấm điểm -> hiện `st.error`), và kiểm tra gửi đánh giá hợp lệ không bị `TypeError` (sau test reset DB về gốc).

- [ ] **Step 2: Run tests to verify they fail**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL với `TypeError: ghi() takes 1 positional argument but 3 were given` hoặc thiếu thông báo lỗi.

- [ ] **Step 3: Implement `luu_danh_gia` và sửa `tour_app/pages/3_Danh_gia.py`**

- Sửa dòng 139 thành gọi `ghi([(sql, tham_so, True)])` (hoặc qua `services.luu_danh_gia`).
- Sửa dòng 149 thành `st.error(thong_bao_loi(e))`.
- Bọc `try/except` + `thong_bao_loi` quanh `doc(...)` dòng 11, 19; xử lý khi `ds_kh` rỗng (`st.info` + `st.stop()`).
- Dùng `dinh_dang_ngay(...)` thay vì in thô `datetime`, sửa chú thích `chk_DonHang_DanhGiaNhaNghi`, gắn `key` theo `chon_don["MaDonHang"]`, lưu flash message vào `st.session_state` và `st.rerun()` khi lưu thành công.

- [ ] **Step 4: Run tests to verify they pass**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: PASS; kiểm tra `4_KiemTra_RangBuoc.sql` trả về 0 dòng.

---

### Task 3: Sửa màn hình `F2` (`tour_app/pages/2_Quan_ly_don.py`) — Bổ sung `RB23`, `try/except`, xác nhận mức phạt và refresh

**Files:**
- Modify: `tour_app/pages/2_Quan_ly_don.py:1-255`
- Modify: `tour_app/services.py` (`kiem_tra_huy_don`, `huy_don`, `chuyen_trang_thai_don`)
- Test: `tour_app/tests/test_db_and_services.py`, `tour_app/tests/test_pages_smoke.py`

**Interfaces:**
- Consumes: `db.doc`, `db.ghi`, `db.hien_tai`, `db.thong_bao_loi`
- Produces: Kiểm tra 2 lớp đầy đủ cho `F2`: chặn `ngay_gio_huy < ngay_dat_dt` VÀ chặn `ngay_gio_huy >= ct["NgayXuatPhat"]` (`RB23`), checkbox `"Khách đã đồng ý mức phạt"`, bọc `try/except` cho cả 4 lệnh `doc()`, guard `if not xem_truoc_rows`, key widget theo `ct["MaDonHang"]`, và `st.rerun()` kèm flash message sau khi cập nhật/hủy thành công.

- [ ] **Step 1: Write the failing tests**

1. `test_f2_chan_ngay_huy_sau_khoi_hanh_rb23` — kiểm tra chọn ngày hủy `>= NgayXuatPhat` của `DH010` bị chặn với thông báo lỗi rõ ràng, không ghi vào DB.
2. `test_f2_huy_don_dh010_va_kiem_tra_rb26_rb30` — kiểm tra hủy `DH010` tại `2026-10-23 08:00:00` khi đã tick xác nhận: phí phạt `1.600.000`, hoàn `14.400.000`, `LT05.SoChoDaDat` giảm từ `4` xuống `0`, `ChuyenTrungChuyen` của `DH010` còn `0` dòng, `4_KiemTra_RangBuoc.sql` trả về 0 dòng, sau đó khôi phục DB.
3. `test_f2_page_requires_penalty_confirmation_checkbox` — `AppTest` kiểm tra khi chưa tick `"Khách đã đồng ý mức phạt"` thì bấm hủy báo lỗi.

- [ ] **Step 2: Run tests to verify they fail**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL do chưa chặn `ngay_gio_huy >= NgayXuatPhat` và chưa có checkbox xác nhận.

- [ ] **Step 3: Implement fixes in `tour_app/pages/2_Quan_ly_don.py` and `services.py`**

Bổ sung `try/except` + `thong_bao_loi`, kiểm tra `ngay_gio_huy >= ct["NgayXuatPhat"]`, thêm `dong_y_phat = st.checkbox("Khách đã đồng ý mức phạt", key=f"f2_dong_y_{ct['MaDonHang']}")`, gắn `key` theo mã đơn, chuẩn hóa định dạng ngày trong câu lỗi, và `st.rerun()` sau khi thành công.

- [ ] **Step 4: Run tests to verify they pass**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: PASS.

---

### Task 4: Sửa màn hình `F1` (`tour_app/pages/1_Dat_tour.py`) — Đồng nhất luồng khách hàng, `try/except`, Transaction an toàn

**Files:**
- Modify: `tour_app/pages/1_Dat_tour.py:1-501`
- Modify: `tour_app/services.py` (`luu_dat_tour`)
- Test: `tour_app/tests/test_db_and_services.py`, `tour_app/tests/test_pages_smoke.py`

**Interfaces:**
- Consumes: `db.doc`, `db.ghi`, `db.hien_tai`, `db.thong_bao_loi`
- Produces: Màn hình `F1` theo đúng phương án người dùng duyệt (dự kiến: hỗ trợ chọn nhanh khách có sẵn `F1.1` + chế độ nhập/tạo khách mới không gây gắn nhầm khách khác), bọc `try/except` mọi lệnh `doc()`, bảo vệ sinh mã trong/cùng luồng an toàn, xóa bỏ emoji và `SQL_TONG_TIEN` thừa, giữ ổn định `dia_chi_don` và cập nhật `SoChoConLai` bằng `st.rerun()` sau khi đặt thành công.

- [ ] **Step 1: Write the failing tests**

1. `test_f1_dat_don_dh015_kh006_lt10_va_kiem_tra_rang_buoc` — kiểm tra đặt đơn `DH015` (5 khách, `NN08`, 2 phòng, 2 chuyến xe): tổng tiền `32.020.000`, `LT10` còn `15` chỗ, 2 dòng `ChuyenTrungChuyen`, `4_KiemTra_RangBuoc.sql` == 0 dòng; sau đó khôi phục DB.
2. `test_f1_chan_khach_trung_email_hoac_sdt_khac_nguoi` — kiểm tra không gán nhầm đơn khi trùng một phần Email/SĐT hoặc trùng Tên+Địa chỉ nhưng khác Email/SĐT.
3. `test_f1_tour_trong_ngay_lt06_an_noi_nghi` và `test_f1_overbooking_layer2_rollback` — kiểm tra `LT06` ẩn nơi nghỉ và `SoChoDaDat > SoChoToiDa` bị `chk_LichTrinh_SoChoDaDat` chặn + rollback toàn bộ.

- [ ] **Step 2: Run tests to verify they fail**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL ở các case sai logic khớp khách và thiếu exception handling.

- [ ] **Step 3: Implement fixes in `tour_app/pages/1_Dat_tour.py` and `services.py`**

Cập nhật luồng chọn/nhập khách hàng theo phương án đã chốt với người dùng, bọc `try/except` + `thong_bao_loi`, dọn code thừa và emoji, giữ `key` ổn định theo `MaLichTrinh` thay vì `range(...)`, `st.rerun()` sau khi đặt thành công.

- [ ] **Step 4: Run tests to verify they pass**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: PASS.

---

### Task 5: Sửa màn hình `S1` (`tour_app/pages/4_Tim_kiem.py`) — Đồng bộ `session_state` 8 bộ lọc

**Files:**
- Modify: `tour_app/pages/4_Tim_kiem.py:1-192`
- Test: `tour_app/tests/test_pages_smoke.py`, `tour_app/tests/test_db_and_services.py`

**Interfaces:**
- Produces: Cả 8 widget lọc (`s1_tu_khoa`, `s1_tinh_den`, `s1_gia_tu`, `s1_gia_den`, `s1_tu_ngay`, `s1_co_den_ngay`, `s1_den_ngay`, `s1_so_khach`, `s1_diem`) đều gắn `key=` vào `st.session_state`; nút `"Tour cao cấp (từ 10 triệu)"` và `"Đặt lại bộ lọc"` reset đầy đủ toàn bộ bộ lọc xung đột; bỏ `use_container_width=True` deprecated.

- [ ] **Step 1: Write the failing test**

Trong `test_pages_smoke.py`: `test_s1_reset_and_luxury_button_override_manual_filters` — mô phỏng người dùng nhập `tu_khoa="sa pa"`, `gia_den=5000000`, sau đó bấm `"Tour cao cấp (từ 10 triệu)"`: kỳ vọng trả về đúng 3 lịch trình (`LT08`, `LT09`, `LT12`) chứ không báo lỗi `"Giá đến phải lớn hơn hoặc bằng giá từ"`; sau đó bấm `"Đặt lại bộ lọc"`: kỳ vọng cả 8 bộ lọc quay về mặc định.

- [ ] **Step 2: Run test to verify it fails**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL với lỗi `"Giá đến phải lớn hơn hoặc bằng giá từ"` hoặc không reset được `tu_khoa`.

- [ ] **Step 3: Implement `session_state` keys và thay `width="stretch"` trong `4_Tim_kiem.py`**

- [ ] **Step 4: Run test to verify it passes**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_pages_smoke.py -v`
Expected: PASS.

---

### Task 6: Sửa báo cáo `R1` (`5_Phieu_xac_nhan.py` & `phieu_xac_nhan.html`) — Nút tải HTML, sửa lỗi logic và chuẩn hóa in 1 trang A4 dọc

**Files:**
- Modify: `tour_app/pages/5_Phieu_xac_nhan.py:1-222`
- Modify: `tour_app/templates/phieu_xac_nhan.html:1-259`
- Test: `tour_app/tests/test_db_and_services.py`, `tour_app/tests/test_pages_smoke.py`

**Interfaces:**
- Consumes: `db.doc`, `db.dinh_dang_tien`, `db.dinh_dang_ngay`, `db.hien_tai`, `db.thong_bao_loi`
- Produces: Thêm `st.download_button` tải file HTML (chỉ hiện khi `nguoi_lap.strip()` khác rỗng), bọc `try/except` mọi `doc()`, sửa `v.MaTrangThai == 'HUY'`, xử lý `LyDoHuy`/`SoID` `NULL`, hiển thị thêm `ThoiGianDon` và `DiemTapTrung`, thay thế placeholder an toàn một lượt, tinh chỉnh CSS `@page` / khoảng cách dòng để cả `DH007` và `DH008` in ra **đúng 1 trang A4 dọc** (kiểm chứng bằng `chrome --headless --print-to-pdf` và đếm trang PDF).

- [ ] **Step 1: Write the failing tests**

1. `test_r1_renders_dh007_dh008_and_dh013_without_raw_none_or_the_prefix` — kiểm tra HTML sinh ra cho `DH007` (đủ 2 SĐT, `6.250.000 đ`, `ThoiGianDon`), `DH008` (khối hủy 30%, `2.610.000 đ`, `6.090.000 đ`, không dính `"None"` nếu `LyDoHuy` `NULL`), và `DH013` / khách không có `SoID` không hiển thị `"Thẻ Tiền mặt / Chuyển khoản"`.
2. `test_r1_empty_nguoi_lap_hides_download_and_preview` — `AppTest` kiểm tra khi xóa trống `nguoi_lap` thì hiện `st.warning` và không có `download_button`.

- [ ] **Step 2: Run tests to verify they fail**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL do chưa có `st.download_button` và còn chuỗi `"Thẻ Tiền mặt..."` / thiếu `ThoiGianDon`.

- [ ] **Step 3: Implement fixes in `5_Phieu_xac_nhan.py` and `templates/phieu_xac_nhan.html`**

- [ ] **Step 4: Run tests and verify A4 1-page PDF layout via headless Chrome/Edge**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: PASS và PDF xuất ra cho `DH007`, `DH008` có đúng `1` trang.

---

### Task 7: Sửa báo cáo `R2` (`6_Bao_cao_doanh_thu.py` & `bao_cao_doanh_thu.html`)

**Files:**
- Modify: `tour_app/pages/6_Bao_cao_doanh_thu.py:1-198`
- Modify: `tour_app/templates/bao_cao_doanh_thu.html:1-192`
- Test: `tour_app/tests/test_db_and_services.py`, `tour_app/tests/test_pages_smoke.py`

**Interfaces:**
- Produces: Mở template bằng `Path(__file__).resolve().parent.parent / "templates" / "bao_cao_doanh_thu.html"`, `html.escape()` mọi trường text DB trong HTML, dòng fallback khi `ds_tour` rỗng, bỏ biến thừa và `use_container_width=True` deprecated.

- [ ] **Step 1: Write the failing test**

`test_r2_runs_from_repo_root_and_escapes_html` — chạy render `R2` khi CWD là `D:\Khanh\CSDL` (không phải `tour_app/`), nhập `nguoi_lap="<b>Test</b>"` và kiểm tra không `FileNotFoundError`, HTML chứa `&lt;b&gt;Test&lt;/b&gt;`, số liệu kỳ `01/09/2026 - 31/12/2026` đạt `79.110.000 đ` / `10` / `26` / `4`.

- [ ] **Step 2: Run test to verify it fails**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_pages_smoke.py -v`
Expected: FAIL với `FileNotFoundError: [Errno 2] No such file or directory: 'templates/bao_cao_doanh_thu.html'`.

- [ ] **Step 3: Implement fixes in `6_Bao_cao_doanh_thu.py` and `templates/bao_cao_doanh_thu.html`**

- [ ] **Step 4: Run test to verify it passes**

Run: `tour_app\.venv\Scripts\python.exe -m unittest tour_app/tests/test_db_and_services.py tour_app/tests/test_pages_smoke.py -v`
Expected: PASS.

---

### Task 8: Hoàn thiện tài liệu, sơ đồ, ảnh chụp và đối chiếu 4 thành viên (theo phạm vi được duyệt)

**Files:**
- Modify: `docs/diagrams/ERD.drawio` (sửa `NoiDen` -> `DenTai`, `LiDoHuy` -> `LyDoHuy`, `TênTour` -> `TenTour`)
- Create / Update: `docs/GopY_Dat.md`, `docs/GopY_Khanh.md`, `docs/GopY_Thinh.md`, `docs/GopY_Tuan.md`, `README.md`
- Create / Update: `screenshots/Hinh04_F1_GiaoDien.png`, `Hinh05a_F1_Loi.png`, `Hinh05b_F1_Loi.png`, `Hinh08_F3_GiaoDien.png`, `Hinh10_R1_ManHinh.png`, `Hinh11_R1_PDF.png` (và các mục `.docx` / `Slide_Nhom.pptx` / gói nộp nếu nằm trong phạm vi người dùng xác nhận).

- [ ] **Step 1:** Sửa `docs/diagrams/ERD.drawio` và rà soát toàn bộ các lỗi mâu thuẫn tài liệu ghi vào `docs/GopY_*.md`.
- [ ] **Step 2:** Khởi động `streamlit run tour_app/app.py` với dữ liệu gốc (`1_QuanLyDatTour_v3.sql`), dùng Browser Subagent + `chrome-devtools` MCP thực hiện từng kịch bản chuẩn và chụp ảnh sắc nét đúng quy cách.
- [ ] **Step 3:** Cập nhật `README.md` và tài liệu kế hoạch phản ánh đúng trạng thái hoàn thiện.

---

### Task 9: Kiểm thử toàn diện & Xác minh E2E (`verification-before-completion`)

- [ ] **Step 1:** Chạy `python -m py_compile` trên toàn bộ file Python trong `tour_app/`.
- [ ] **Step 2:** Chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc, chạy toàn bộ `unittest` (`test_db_and_services.py`, `test_pages_smoke.py`), xác nhận 100% PASS.
- [ ] **Step 3:** Chạy `database/4_KiemTra_RangBuoc.sql` xác nhận trả về **0 dòng** vi phạm.
- [ ] **Step 4:** Khởi động ứng dụng Streamlit thực tế (`BypassSandbox: true` khi cần user truy cập hoặc trong kiểm thử browser), dùng Browser Subagent + `chrome-devtools` MCP duyệt xuyên suốt cả 6 màn hình (`F1`, `F2`, `F3`, `S1`, `R1`, `R2`), kiểm tra console log, network requests và chụp ảnh xác nhận cuối cùng; reset CSDL về trạng thái gốc sạch sẽ.
