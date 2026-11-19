# Bản Thiết Kế Hệ Thống Web Đặt Tour Miền Bắc (Bắc Việt Travel)

- **Ngày lập:** 19/11/2026
- **Phạm vi:** Xây dựng mới ứng dụng Web Full-Stack (React + Vite + FastAPI) tái sử dụng toàn bộ tầng dữ liệu và nghiệp vụ MySQL trong `tour_app/db.py` và `tour_app/services.py`, đồng thời giữ nguyên thư mục `tour_app/` gốc để đối chiếu và bảo toàn bộ kiểm thử hiện có.
- **Tài liệu quy tắc Design System đi kèm:** `docs/superpowers/specs/2026-11-19-design-system-rules.md`

### Cập nhật giao diện dạng Form & Bảng (19/11/2026)
Theo điều chỉnh phạm vi mới nhất, tầng giao diện Frontend chuyển từ bố cục Landing Page quảng bá nhiều hình ảnh sang **giao diện ứng dụng Form và Bảng gọn nhẹ, dễ điền và dễ nhận biết** phù hợp đồ án CSDL:
- Loại bỏ toàn bộ thư mục 11 ảnh mẫu (`web_app/frontend/public/images/`) và các component quảng bá (`HeroOrganicFrame`, `FloatingSearchBar`, `TourCard`, `HeroFlightArc`), chỉ giữ font `Be Vietnam Pro` đồng nhất.
- Trang chủ (`/`) trở thành trang **Tổng quan hệ thống** gọn nhẹ gồm 4 thẻ số liệu thực từ MySQL, lối tắt mở nhanh từng biểu mẫu theo 2 vai trò (`Khách hàng` và `Quản trị & Điều hành`), và bảng lịch khởi hành sắp tới.
- Trang Tra cứu (`/explore`) hiển thị trực tiếp biểu mẫu lọc 8 tiêu chí kèm bảng kết quả toàn chiều rộng; trang Đặt tour (`/book`) và Đơn của tôi (`/my-bookings`) sử dụng form và danh sách không ảnh minh họa.
- Giữ nguyên toàn bộ kiến trúc `web_app/backend/`, cơ chế phân quyền User/Admin bằng HMAC-SHA256, quy tắc loại bỏ mã `F1..R2` / chú thích kỹ thuật kiểu AI / thông tin PTIT-12 bảng, và xuất file **PDF khổ A4** cho cả Báo cáo doanh thu lẫn Phiếu xác nhận.

---

## 1. Mục tiêu, Non-goals và Anti-goals

### Mục tiêu (Goals)
1. **Giao diện hiện đại, giàu cảm hứng du lịch (theo chuẩn ảnh mẫu tham chiếu):**
   - Nền sáng trong trẻo, xanh dương cobalt làm màu nhấn chính, kết hợp typography biên tập (tiêu đề serif tạo điểm nhấn trên Landing Page + sans-serif tối ưu tiếng Việt cho toàn bộ giao diện vận hành).
   - Hình khối bo cong organic ở phần Hero, thanh tìm kiếm nổi dạng pill, thẻ điểm đến full-bleed có hiệu ứng phóng ảnh nhẹ khi di chuột, và chuyển cảnh mượt giữa các màn hình.
   - Sử dụng bộ ảnh phong cảnh miền Bắc lưu cục bộ trong dự án cho 9 tuyến tour (`T01`–`T09`), ảnh Hero và ảnh banner nổi bật.
2. **Phân tách rõ giao diện theo vai trò (Role-based UX) mà giữ nguyên 12 bảng MySQL:**
   - **Cổng Khách hàng (User Portal):** Tập trung khám phá tour, tìm kiếm, đặt tour trực tiếp và quản lý đơn cá nhân / đánh giá sau chuyến đi.
   - **Cổng Quản trị (Admin Portal):** Giao diện Dashboard vận hành riêng (thanh điều hướng bên trái tối màu, bảng dữ liệu mật độ cao, ngăn chi tiết dạng slide-over) cho việc theo dõi toàn bộ đơn hàng, xử lý trạng thái/hủy đơn, xuất phiếu xác nhận và xem báo cáo doanh thu.
3. **Loại bỏ hoàn toàn dấu vết bài tập kỹ thuật và văn phong kiểu AI:**
   - Không hiển thị mã chức năng (`F1.`, `F2.`, `F3.`, `S1.`, `R1.`, `R2.`) trên menu, tiêu đề trang hay tên bảng.
   - Không hiển thị các dòng ghi chú mờ giải thích quy tắc ràng buộc kỹ thuật (`HOANTHANH`, `MaNhaNghi IS NULL`, `chk_DonHang_DanhGiaNhaNghi`, `RB22`, `RB23`...).
   - Trang chủ không hiển thị thông tin môn học PTIT, số lượng 12 bảng CSDL, đồng hồ demo hay danh sách đánh số chức năng; biến hoàn toàn thành Landing Page du lịch.
4. **Xuất file PDF thật khổ A4:**
   - Cả **Báo cáo doanh thu (A4 ngang)** và **Phiếu xác nhận đặt tour (A4 dọc)** đều xuất trực tiếp thành file `.pdf` hoàn chỉnh (không chỉ xuất file `.html` như trước), giữ đúng cấu trúc chữ ký, bảng tổng hợp và tiếng Việt chuẩn.

### Phạm vi không thực hiện (Non-goals)
- Không thay đổi cấu trúc 12 bảng, 2 view và dữ liệu mẫu trong `database/1_QuanLyDatTour_v3.sql`.
- Không chỉnh sửa hay phá vỡ thư mục `tour_app/` gốc (các file `app.py`, `pages/*.py`, `tests/*` giữ nguyên để bộ test cũ vẫn chạy xanh 100%).
- Không xây dựng cổng thanh toán thực tế hay xác thực JWT/OAuth2 phức tạp với mật khẩu băm trong CSDL (phân quyền hoạt động ở tầng ứng dụng bằng phiên demo và đối chiếu bảng `KhachHang`).
- Không hỗ trợ CRUD tạo/xóa Tour, Lịch trình hay Nhà nghỉ (ngoài phạm vi nghiệp vụ hiện có của hệ thống).

### Tiêu chí thất bại cần tránh (Anti-goals)
- Giao diện giống bản Streamlit khoác thêm màu nền hoặc vẫn còn thanh sidebar mặc định/nhãn kỹ thuật.
- Thông số thống kê bịa đặt trên Landing Page (mọi số liệu như số tỉnh thành, số tuyến tour, số lịch trình, số khách phục vụ, điểm đánh giá phải đọc thật từ MySQL).
- Hình ảnh lỗi link ngoài (broken image) hoặc tỷ lệ méo mó.
- Bất kỳ vi phạm ràng buộc CSDL nào (đặt quá chỗ, hủy sau giờ khởi hành, đánh giá nhà nghỉ khi không đặt nhà nghỉ, đánh giá lần 2, số phòng > số khách).
- Sử dụng emoji trong giao diện người dùng.

---

## 2. Phương án kiến trúc đã lựa chọn (Approaches)

### Các phương án đã cân nhắc
1. **Phương án 1 (Đã chọn): Xây mới Frontend React + Vite (TypeScript) kết nối Backend FastAPI, tái sử dụng 100% `tour_app/db.py` và `tour_app/services.py` (giữ nguyên `tour_app/` cũ).**
   - *Ưu điểm:* Tự do hoàn toàn trong việc dựng hình khối organic SVG clip-path, hiệu ứng glassmorphism, thanh tìm kiếm nổi chồng lớp, chuyển cảnh trang mượt (Framer Motion), tách biệt hoàn toàn layout Landing Page (Khách hàng) và Admin Dashboard. Tái sử dụng toàn bộ SQL, giao dịch nguyên tử và validation của `services.py`. Bảo toàn 100% ứng dụng Streamlit và bộ test gốc.
   - *Đánh đổi:* Cần chạy thêm tiến trình Node/Vite khi phát triển (hoặc build tĩnh `dist/` để FastAPI phục vụ trực tiếp trên 1 cổng duy nhất). Cần viết thêm test API/Frontend cho phần mới.
2. **Phương án 2 (Loại bỏ): Giữ nguyên Streamlit 1.66.0 + `st.navigation` + Custom CSS/HTML.**
   - *Lý do loại:* Streamlit chạy server-rerun toàn trang khi đổi widget, khó kiểm soát hình khối cắt lớp tương tác (như đặt form tìm kiếm sống đè ranh giới ảnh hero bo cong), chuyển cảnh giật và dễ vỡ DOM khi tùy biến sâu.
3. **Phương án 3 (Loại bỏ): Thêm bảng `TaiKhoan`/`Users` vào MySQL để phân quyền.**
   - *Lý do loại:* Phá vỡ chuẩn 12 bảng đang được kiểm tra trong `test_db_and_services.py` và làm lệch ERD/Data Diagram của đồ án.

---

## 3. Kiến trúc kỹ thuật tổng thể

```text
d:\Khanh\CSDL\
├── database/                  (GIỮ NGUYÊN - 12 bảng, 2 view, dữ liệu mẫu)
├── tour_app/                  (GIỮ NGUYÊN - db.py, services.py, templates/, tests/)
└── web_app/                   (MỚI)
    ├── backend/
    │   ├── main.py            (FastAPI app, CORS, router mounting, optional static SPA serve)
    │   ├── dependencies.py    (Nạp tour_app vào sys.path, xử lý lỗi MySQL -> HTTP 400/404/409/500)
    │   ├── schemas.py         (Pydantic request/response models)
    │   ├── queries.py         (Truy vấn bổ sung chỉ-đọc cho Landing Page, Admin Orders, User Orders, Customer Lookup)
    │   ├── pdf_service.py     (Chuyển HTML từ templates/ -> PDF A4 bytes qua Chrome/Edge headless)
    │   ├── routers/
    │   │   ├── public.py      (/api/meta, /api/landing, /api/provinces, /api/schedules, /api/accommodations)
    │   │   ├── auth.py        (/api/auth/customers, /api/auth/customer-login, /api/auth/admin-login)
    │   │   ├── bookings.py    (/api/bookings, /api/customers/check-duplicate, /api/bookings/my, /api/reviews)
    │   │   └── admin.py       (/api/admin/orders, /api/admin/orders/{id}/..., /api/admin/reports/...)
    │   ├── requirements.txt   (fastapi, pydantic, httpx)
    │   └── tests/
    │       └── test_api.py    (Kiểm thử tự động REST API + xuất PDF + toàn vẹn MySQL)
    └── frontend/
        ├── package.json       (React 19, TypeScript, Vite, Tailwind CSS, react-router-dom, framer-motion, lucide-react, recharts)
        ├── index.html         (Google Fonts: Spectral + Be Vietnam Pro, metadata tiếng Việt)
        ├── public/
        │   └── images/        (Ảnh cục bộ: hero-northern-vietnam.png, promo-cruise.png, tour-T01.png ... tour-T09.png)
        └── src/
            ├── styles/        (tokens.css, globals.css)
            ├── api/           (client.ts, types.ts)
            ├── context/       (AuthContext.tsx - quản lý phiên User/Admin tại client)
            ├── components/    (layout/, common/, user/, admin/)
            └── pages/
                ├── user/      (LandingPage, ExplorePage, BookingPage, MyBookingsPage)
                └── admin/     (AdminLoginPage, AdminDashboardPage, AdminOrdersPage, AdminConfirmationsPage)
```

### Nguyên tắc tái sử dụng tầng dữ liệu và nghiệp vụ
- Mọi thao tác ghi CSDL (`luu_dat_tour`, `chuyen_trang_thai_don`, `huy_don`, `luu_danh_gia`), tính toán nghiệp vụ (`tinh_du_toan_f1`, `tinh_xem_truoc_phat_huy`, `kiem_tra_dat_tour`, `kiem_tra_huy_don`, `kiem_tra_danh_gia`, `kiem_tra_trung_khach_hang`), tìm kiếm 8 tiêu chí (`tim_kiem_lich_trinh`), và dựng HTML biểu mẫu (`tao_html_phieu_xac_nhan`, `tao_html_bao_cao_doanh_thu`) **gọi trực tiếp** từ `tour_app/services.py` và `tour_app/db.py`.
- Xử lý mốc thời gian demo (`db.hien_tai()`): Backend cung cấp endpoint `GET /api/meta` trả về `current_date` (`2026-10-23`) để các ô lọc ngày ở Frontend tự lấy mốc hợp lệ với dữ liệu mẫu (nhưng **không** hiển thị thanh trạng thái kỹ thuật này lên giao diện trang chủ).

### Chi tiết dịch vụ xuất PDF (`web_app/backend/pdf_service.py`)
- Tái sử dụng kỹ thuật đã kiểm chứng trên chính máy Windows hiện tại (từ `tour_app/tests/test_db_and_services.py`):
  1. Dựng chuỗi HTML bằng `services.tao_html_bao_cao_doanh_thu(...)` hoặc `services.tao_html_phieu_xac_nhan(...)` (đã có sẵn `@page { size: A4 landscape }` / `@page { size: A4 portrait }`, CSS bảng biểu, chống XSS `escape()`, và ẩn nút in trong `@media print`).
  2. **Đồng bộ thương hiệu biểu mẫu (Đề xuất của kỹ thuật - không chạm `tour_app/`):** Để giữ tính nhất quán thương hiệu thương mại trên ứng dụng web mới trong khi vẫn bảo toàn nguyên vẹn `tour_app/templates/phieu_xac_nhan.html` cho bộ test cũ, `web_app/backend/pdf_service.py` hậu xử lý phần tiêu đề tĩnh của HTML phiếu xác nhận (chuyển `PTIT TOUR` / `PTIT Tour` / `dieuhanh@ptittour.edu.vn` sang `BẮC VIỆT TRAVEL` / `Bắc Việt Travel` / `lienhe@bacviettravel.vn`, địa chỉ `Số 10 Nguyễn Trãi, Hà Đông, Hà Nội`). Đầu ra PDF A4 dọc vẫn được kiểm chứng tự động vừa khít đúng **1 trang A4** trên Chrome/Edge headless.
  3. Tìm trình duyệt headless theo thứ tự ưu tiên: `chrome.exe` / `msedge.exe` (PATH và các thư mục cài đặt chuẩn trên Windows).
  4. Chạy `subprocess.run` với `--headless`, `--disable-gpu`, `--no-pdf-header-footer`, `--print-to-pdf=<tmp.pdf>` trong `tempfile.TemporaryDirectory()` cô lập, timeout 30 giây.
  5. Trả về `Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": 'attachment; filename="..."'})` hoặc `inline` khi xem trước.
  6. Kiểm tra hợp lệ: byte đầu phải bắt đầu bằng `%PDF-`. Nếu máy không tìm thấy Chrome/Edge, trả HTTP 503 kèm thông báo tiếng Việt rõ ràng.

---

## 4. Cơ chế phân quyền (Role Separation) ở tầng ứng dụng

### Cơ chế xác thực phiên phía Server (Đề xuất của kỹ thuật)
- Backend cấp **token phiên ký bằng HMAC-SHA256** (không lưu bảng mới trong MySQL, dùng khóa bí mật qua biến môi trường `APP_SESSION_SECRET` với giá trị mặc định cục bộ):
  - **Phiên Khách hàng (`X-Customer-Token`):** Cấp bởi `POST /api/auth/customer-login` (và tự động cấp kèm sau khi đặt tour thành công ở `POST /api/bookings`), chứa `{"role": "user", "ma_kh": "<MaKH>"}`.
  - **Phiên Quản trị viên (`X-Admin-Token`):** Cấp bởi `POST /api/auth/admin-login`, chứa `{"role": "admin", "staff_name": "<HoTen>"}`.
- **Kiểm soát quyền sở hữu trên Server (trả HTTP 401/403 nếu vi phạm):**
  - `GET /api/customers/{ma_kh}/orders` và `GET /api/customers/{ma_kh}/pending-reviews`: Bắt buộc có `X-Customer-Token` trùng khớp `ma_kh` (hoặc `X-Admin-Token`).
  - `POST /api/reviews`: Bắt buộc có `X-Customer-Token` và Backend xác minh `DonHang.MaKH == token.ma_kh` trước khi gọi `services.luu_danh_gia`.
  - `GET /api/orders/{ma_don}/confirmation/pdf`: Chấp nhận `X-Admin-Token` (tải mọi đơn) HOẶC `X-Customer-Token` có `ma_kh` trùng với chủ đơn `DonHang.MaKH`.
  - Toàn bộ `/api/admin/*`: Bắt buộc có `X-Admin-Token` hợp lệ.

### Hai vai trò tách biệt và luồng đặt tour nhất quán
1. **Khách hàng (`role: "user"`):**
   - **Khách vãng lai (chưa đăng nhập):** Xem tự do Landing Page (`/`), Khám phá & Tìm kiếm tour (`/explore`), và Đặt tour (`/book` với 2 lựa chọn: nhập `Khách hàng mới` hoặc chọn `Khách hàng có sẵn` để tiện demo). Khi `POST /api/bookings` thành công, Backend trả kèm `customer` và `customer_token` cho chính `MaKH` vừa tạo/đặt đơn; Frontend tự động cập nhật phiên đăng nhập đó nên các nút `Tải phiếu xác nhận (PDF)` và `Xem đơn của tôi` trên màn hình xác nhận hoạt động liền mạch ngay lập tức.
   - **Khách hàng đã đăng nhập:** Đăng nhập bằng **Email** hoặc **Số điện thoại** khớp với bảng `KhachHang` / `SDT_KhachHang` (có danh sách tài khoản mẫu chọn nhanh 1 click trong modal đăng nhập). Khi đã đăng nhập:
     - Trang Đặt tour (`/book`) khóa gọn thông tin người đặt theo đúng tài khoản đang đăng nhập (tự điền địa chỉ đón mặc định) để đảm bảo quyền sở hữu đơn nhất quán, kèm liên kết phụ `"Đăng xuất để đặt cho khách khác"` nếu cần đổi người đặt.
     - Trang Đơn hàng của tôi (`/my-bookings`) hiển thị toàn bộ lịch sử đơn của riêng `MaKH` đó, cho phép đánh giá các đơn `HOANTHANH` chưa đánh giá và tải Phiếu xác nhận PDF của đơn mình.
2. **Quản trị viên / Điều hành (`role: "admin"`):**
   - Đăng nhập tại `/admin/login` (hoặc qua nút `"Quản trị"` trên thanh header).
   - Xác thực tầng ứng dụng với tài khoản điều hành demo cấu hình qua biến môi trường (`ADMIN_USERNAME`/`ADMIN_PASSWORD`, mặc định `admin` / `admin123`, kèm tên nhân viên mặc định có thể chỉnh sửa khi lập phiếu/báo cáo; có nút điền nhanh thông tin demo trên màn hình đăng nhập).
   - Toàn bộ route `/admin/*` được bảo vệ bằng guard phía client (chưa đăng nhập admin sẽ điều hướng về `/admin/login`) và xác thực `X-Admin-Token` ở mọi endpoint `/api/admin/*`.
   - Giao diện Admin có layout riêng hoàn toàn (Sidebar tối màu bên trái + Topbar nội bộ + nút `"Về trang khách hàng"`).

---

## 5. Thiết kế chi tiết từng màn hình & Luồng người dùng

### A. Cổng Khách hàng (User Portal)

#### 1. Thanh điều hướng chung (Top Navigation Bar)
- Cấu trúc 3 vùng cân đối (cảm hứng ảnh mẫu 1):
  - **Trái:** Logo `Bắc Việt Travel` (biểu tượng SVG núi non & sóng biển tối giản, 2 dòng: tên thương hiệu + phụ đề `Du lịch miền Bắc`).
  - **Giữa:** 4 liên kết sạch, không đánh số, có chấm xanh chỉ báo mục đang chọn:
    - `Trang chủ` (`/`)
    - `Khám phá tour` (`/explore`)
    - `Đặt tour` (`/book`)
    - `Đơn của tôi` (`/my-bookings`)
  - **Phải:**
    - Nếu chưa đăng nhập: Nút `"Đăng nhập"` (mở modal chọn/nhập Email hoặc SĐT khách hàng) + nút phụ tinh tế `"Quản trị"` (dẫn tới `/admin/login`).
    - Nếu đã đăng nhập khách: Pill hiển thị tên khách (`Nguyễn Văn An`) có menu thả xuống (`Đơn hàng của tôi`, `Chuyển sang Quản trị`, `Đăng xuất`).

#### 2. Trang chủ — Landing Page (`/`)
Chế độ thị giác: **Persuade** (chủ đề sáng, hình khối bo cong organic, truyền cảm hứng).
- **Khối 1 — Hero Editorial bất đối xứng (1 màn hình đầu tiên):**
  - **Cột trái (~44% chiều rộng):**
    - Kicker viết hoa giãn chữ nhỏ (`KHÁM PHÁ · TRẢI NGHIỆM · LƯU GIỮ`) kèm đường nét đứt cong nhẹ với biểu tượng máy bay/la bàn nhỏ ở đuôi (SVG mỏng).
    - Tiêu đề H1 lớn bằng font Serif (`Spectral`):
      - Dòng 1 (đậm, màu navy `#0F172A`): `Miền Bắc`
      - Dòng 2 (nghiêng italic, màu xanh cobalt `#1D63ED`): *trọn vẹn sắc màu.*
    - Đoạn mô tả ngắn 2 dòng (plain copy, không sáo rỗng): *"Từ vịnh di sản Hạ Long đến đỉnh Fansipan mờ sương, chọn lịch trình khởi hành phù hợp và đặt chỗ trực tuyến trong vài bước."*
    - Nút CTA chính dạng pill xanh dương `#1D63ED`: `Khám phá lịch trình` kèm vòng tròn mũi tên trắng bên phải (hover trượt nhẹ mũi tên + nâng nút 2px).
  - **Cột phải (~56% chiều rộng):**
    - Ảnh phong cảnh Vịnh Hạ Long / non nước miền Bắc chất lượng cao, bo cắt bằng **SVG organic wave clip-path** ở cạnh trái và đáy giống bố cục ảnh mẫu 1.
    - **Thẻ nổi Glassmorphism (góc trên phải ảnh):** Hiển thị số liệu thực từ CSDL (ví dụ: điểm đánh giá trung bình `4.5/5` và tổng lượt khách đã phục vụ từ `DonHang`), kèm nhóm avatar chữ cái đầu cách điệu.
    - **Nút nổi hình tròn** nằm giao giữa đường cong ảnh và nền trắng bên trái (tương tác mở hộp xem nhanh điểm nổi bật hành trình / cuộn xuống danh sách tour nổi bật).
- **Thanh tìm kiếm nhanh nổi dạng Pill (Floating Search Bar):**
  - Nằm chồng nhẹ lên cạnh dưới của khối Hero (đổ bóng mềm `0 20px 50px rgba(15, 23, 42, 0.08)`).
  - Gồm 4 ô ngăn bởi đường kẻ dọc mảnh + 1 nút kính lúp tròn xanh dương:
    1. `Điểm đến` (dropdown danh sách 15 tỉnh miền Bắc lấy từ `TinhThanh`)
    2. `Khởi hành từ` (chọn ngày, mặc định theo mốc hệ thống)
    3. `Đến ngày` (tùy chọn)
    4. `Số khách` (chọn số lượng 1–20)
    5. Nút tròn xanh dương `Tìm kiếm` -> điều hướng sang `/explore` kèm query string tương ứng.
- **Khối 2 — Ưu đãi nổi bật & Điểm đến đặc sắc (bố cục 2 cột giống nửa dưới ảnh mẫu 1):**
  - **Cột trái (~30%):**
    - **Thẻ Banner Xanh Gradient (Tour Cao Cấp):** Ảnh nền du thuyền Vịnh Hạ Long phủ lớp chuyển sắc xanh dương cobalt, nhãn pill nhỏ `TRẢI NGHIỆM CAO CẤP`, tiêu đề `Du thuyền & Hành trình riêng từ 10 triệu`, nút trắng pill `Xem ngay ->` (dẫn thẳng tới `/explore?gia_tu=10000000`).
    - **Thẻ Chỉ số thực từ CSDL (nền trắng bo tròn):** 3 chỉ số ngang có icon xanh/ngọc/vàng nhạt từ `lucide-react`:
      - `<so_tinh>` `Tỉnh miền Bắc`
      - `<so_tour>` `Tuyến hành trình`
      - `<so_lich_trinh_mo>` `Lịch khởi hành mở bán`
  - **Cột phải (~70%):**
    - Tiêu đề `Điểm đến nổi bật` bên trái + liên kết `Xem tất cả >` bên phải.
    - Lưới 4 thẻ (có nút mũi tên trượt qua lại nếu có nhiều hơn 4 lịch trình mở bán) hiển thị các tour tiêu biểu sắp khởi hành lấy trực tiếp từ MySQL:
      - Ảnh dọc bo góc lớn (`20px`), full-bleed, phóng `scale(1.04)` mượt khi hover.
      - Lớp gradient tối nhẹ ở đáy ảnh để chữ trắng luôn đạt độ tương phản cao.
      - Tên điểm đến/tour, `Từ <Giá định dạng>`, badge sao nền trắng góc phải dưới (`4.8` hoặc `Mới`), badge chỗ trống góc trên trái.
      - Click vào thẻ -> điều hướng tới `/book?schedule=<MaLichTrinh>` (hoặc mở drawer chi tiết nhanh + nút `Đặt tour ngay`).
- **Footer gọn gàng:** Tên thương hiệu `Bắc Việt Travel`, điều hướng nhanh các trang Khách hàng, thông tin liên hệ hiển thị gọn gàng (Km10 Nguyễn Trãi, Hà Đông, Hà Nội), không chứa thuật ngữ kỹ thuật hay đồ án.

#### 3. Trang Khám phá & Tìm kiếm tour (`/explore`)
Chế độ thị giác: **Operate + Discovery**.
- **Thanh lọc trực quan (Filter Bar + Bộ lọc mở rộng):**
  - Đầy đủ 8 tiêu chí từ `services.tim_kiem_lich_trinh`: Từ khóa tên tour, Tỉnh đến, Giá từ, Giá đến, Khởi hành từ ngày, Khởi hành đến ngày (tùy chọn), Số khách tối thiểu, Điểm đánh giá tối thiểu (`Tất cả`, `3.0+`, `4.0+`, `4.5+`).
  - Nút lọc nhanh: `Tour cao cấp (từ 10 triệu)` và `Đặt lại bộ lọc`.
  - Kiểm tra hợp lệ tức thời (`Giá đến >= Giá từ`, `Đến ngày >= Từ ngày`) với thông báo lỗi tiếng Việt ngay dưới trường tương ứng.
- **Hiển thị kết quả:**
  - Bộ đếm số lịch trình phù hợp + nút chuyển chế độ xem (`Dạng thẻ` mặc định / `Dạng bảng`).
  - Mỗi **Thẻ lịch trình** hiển thị: Ảnh điểm đến theo `MaTour`, tuyến `Nơi đi -> Nơi đến`, tên tour, ngày khởi hành, thời lượng (`3 ngày`), số chỗ còn lại, điểm đánh giá TB & số lượt, giá cơ bản nổi bật, và nút chính **`Đặt tour này`** (chuyển sang `/book?schedule=<MaLichTrinh>`).
  - Trạng thái rỗng rõ ràng kèm nút `Xóa bộ lọc` khi không có kết quả khớp.

#### 4. Trang Đặt tour (`/book`)
Chế độ thị giác: **Operate (Transaction Focus)** — dành riêng cho việc tạo đơn đặt tour, tách hoàn toàn khỏi danh sách quản lý đơn.
- **Bố cục 2 cột (Trái 65% Form theo từng thẻ nhóm rõ ràng | Phải 35% Thẻ Dự toán chi phí dính `sticky`):**
  - **Nhóm 1 — Chọn lịch trình & Số lượng khách:**
    - Chọn lịch trình chưa khởi hành và còn chỗ (tự động chọn sẵn nếu đi từ `/explore` hoặc Landing Page). Hiển thị card tóm tắt trực quan: ảnh thu nhỏ, tuyến đường, ngày khởi hành–kết thúc, số đêm, điểm tập trung, chỗ trống còn lại.
    - Bộ tăng/giảm `Số lượng khách` (từ `1` đến `SoChoConLai`).
  - **Nhóm 2 — Thông tin khách hàng:**
    - Nếu đã đăng nhập Khách hàng: hiển thị thẻ thông tin tài khoản hiện tại (tự lấy `MaKH` và địa chỉ đón mặc định), kèm nút phụ `"Đăng xuất để đặt cho khách khác"`.
    - Nếu là khách vãng lai: tab chọn gọn `Khách hàng mới` hoặc `Khách hàng có sẵn`. Khi chọn `Khách hàng mới`: 4 ô nhập (Họ tên, SĐT 10 số, Email, Địa chỉ liên hệ), kiểm tra trùng Email/SĐT qua API ngay khi rời ô (`onBlur`) và cảnh báo nếu đã có trong hệ thống để chuyển sang dùng khách có sẵn.
  - **Nhóm 3 — Dịch vụ lưu trú (Nhà nghỉ / Homestay):**
    - Nếu là tour trong ngày (`0 đêm`): ẩn lựa chọn phòng và hiển thị thông báo ngắn gọn tự nhiên `"Chuyến đi trong ngày không bao gồm lưu trú qua đêm."` (không ghi thuật ngữ CSDL).
    - Nếu tour nhiều ngày: hiển thị danh sách Nhà nghỉ/Homestay đã lọc tự động theo tỉnh đến (dạng thẻ radio chọn trực quan: tên, loại hình Homestay/Nhà nghỉ, giá/đêm, hoặc `Không đặt nơi nghỉ`) + ô `Số phòng` (`1` đến `SoLuongKhach`).
  - **Nhóm 4 — Xe trung chuyển (tối đa 2 chuyến):**
    - Công tắc bật/tắt `Xe đón tại nhà`: tự điền sẵn địa chỉ khách (giữ nguyên chỉnh sửa của người dùng nếu tự đổi), ngày & giờ đón mặc định trước giờ xuất phát 2 tiếng.
    - Công tắc bật/tắt `Xe về nơi nghỉ` (chỉ bật khi tour > 0 đêm và có chọn nơi nghỉ): chọn ngày & giờ về nơi nghỉ trong khung thời gian tour.
  - **Cột phải (Sticky Summary Card):**
    - Tóm tắt tên tour, ảnh, ngày khởi hành, số khách, tên nơi nghỉ & số phòng (nếu có), xe trung chuyển đã chọn.
    - Bảng tính trực tiếp (gọi công thức `tinh_du_toan_f1`): Tiền tour cơ bản, Tiền phòng lưu trú, **Tổng tiền dự kiến**.
    - Nút chính **`Xác nhận đặt tour`**.
- **Màn hình kết quả sau khi đặt thành công:**
  - Hiển thị thẻ xác nhận thành công với mã đơn (`DHxxx`), tổng chi phí, thông tin lịch trình và 3 hành động: `Tải phiếu xác nhận (PDF)`, `Xem đơn của tôi`, `Đặt thêm tour khác`.

#### 5. Trang Đơn hàng của tôi & Đánh giá (`/my-bookings`)
- Nếu chưa đăng nhập Khách hàng: Hiển thị khung đăng nhập gọn ngay giữa trang (nhập Email/SĐT hoặc chọn nhanh khách hàng mẫu để xem lịch sử đơn).
- **2 Tab rõ ràng:**
  - **Tab 1 — Đơn đã đặt:** Liệt kê tất cả đơn hàng của khách đang đăng nhập (`MaDonHang`, ảnh tour, tên tour, ngày khởi hành–kết thúc, nơi nghỉ, số khách, tổng tiền, trạng thái dạng badge màu ngữ nghĩa).
    - Đơn đã hủy hiển thị rõ phí phạt và số tiền hoàn.
    - Mỗi đơn có nút **`Tải phiếu xác nhận (PDF)`**.
    - Đơn ở trạng thái `Hoàn thành tour` và chưa đánh giá có nút nổi bật **`Viết đánh giá`** (mở thẳng sang Tab Đánh giá chọn sẵn đơn đó).
  - **Tab 2 — Đánh giá chuyến đi:**
    - Chỉ hiển thị các chuyến đã hoàn thành và chưa đánh giá (nếu không còn đơn nào, hiển thị empty state lịch sự kèm nút khám phá tour mới).
    - Chọn chuyến đi cần đánh giá -> chấm điểm **1–5 sao tương tác trực quan** + ô nhận xét tour (tối đa 500 ký tự).
    - Khối đánh giá Nhà nghỉ chỉ hiện khi đơn có đặt nhà nghỉ, kèm checkbox bật/tắt chấm điểm nhà nghỉ và chọn 1–5 sao + nhận xét. (Tuyệt đối không hiện dòng chú thích `MaNhaNghi IS NULL` hay `chk_DonHang_DanhGiaNhaNghi`).

---

### B. Cổng Quản trị (Admin Portal — `/admin/*`)

Chế độ thị giác: **Operate (Executive & Operations Dashboard)**.
- **Khung bố cục riêng biệt:**
  - **Sidebar cố định bên trái (nền xanh đen `#0F172A`, chữ trắng sáng `#F8FAFC`, mục đang chọn nền xanh cobalt `#1D63ED`):**
    - Logo `Bắc Việt Admin`
    - `Tổng quan & Báo cáo` (`/admin/dashboard`)
    - `Quản lý đơn hàng` (`/admin/orders`)
    - `Phiếu xác nhận` (`/admin/confirmations`)
    - Chân sidebar: Thông tin nhân viên đang trực, nút `Về trang Khách hàng`, nút `Đăng xuất`.
  - **Vùng nội dung chính:** Nền xám lạnh nhẹ (`#F8FAFC`), các thẻ dữ liệu trắng viền mảnh (`#E2E8F0`), kiểu chữ bảng số thẳng hàng (`tabular-nums`).

#### 1. Tổng quan & Báo cáo doanh thu (`/admin/dashboard`)
- **Thanh lọc kỳ báo cáo:** `Từ ngày` (mặc định `01/09/2026`), `Đến ngày` (mặc định `31/12/2026`), ô `Người lập báo cáo` (mặc định theo tên nhân viên đăng nhập, cho sửa tự do), và nút chính **`Xuất báo cáo PDF (A4 ngang)`** + nút phụ **`Xem trước bản in`**.
- **4 thẻ KPI nổi bật:** `Tổng doanh thu`, `Đơn thành công`, `Khách phục vụ`, `Đơn đã hủy` (cập nhật ngay theo kỳ báo cáo).
- **Biểu đồ trực quan (Recharts):** Biểu đồ cột ngang so sánh `Doanh thu dịch vụ` và `Tiền phạt hủy` theo từng tour trong kỳ (loại trừ dòng tổng ROLLUP trên biểu đồ để tránh lệch thang đo).
- **Hai bảng dữ liệu chuẩn:**
  - `Tổng hợp doanh thu theo tour` (dòng `TỔNG CỘNG` tô nền nổi bật ở cuối bảng).
  - `Xếp hạng đánh giá cơ sở lưu trú` (hiển thị sao trực quan + số lượt đánh giá).
- **Logic xuất PDF:** Bấm `Xuất báo cáo PDF (A4 ngang)` kiểm tra `Người lập báo cáo` không trống -> gọi `POST /api/admin/reports/revenue/pdf` -> tải thẳng file `.pdf` khổ A4 ngang về máy người dùng.

#### 2. Quản lý danh sách đơn hàng (`/admin/orders`)
- **Tách biệt hoàn toàn với trang đặt tour của khách.**
- **Thanh lọc & tìm kiếm nhanh:**
  - Pills lọc theo trạng thái kèm số lượng thực tế: `Tất cả`, `Đã đặt tour`, `Đã thanh toán`, `Hoàn thành tour`, `Đã hủy tour`.
  - Ô tìm kiếm theo mã đơn, tên khách hàng hoặc tên tour.
- **Bảng danh sách đơn hàng đầy đủ:**
  - Hiển thị toàn bộ đơn hàng hiện có (`MaDonHang`, Khách hàng, Tour & Tuyến, Khởi hành, Số khách, Tổng tiền, Trạng thái, Hành động).
- **Ngăn xử lý chi tiết dạng Slide-over Drawer (mở khi bấm vào 1 đơn):**
  - Thông tin đầy đủ đơn hàng: Khách hàng, Lịch trình, Lưu trú, Xe trung chuyển, Chi tiết chi phí.
  - Khối **Cập nhật trạng thái** (nếu đơn đang mở và có trạng thái đích hợp lệ từ `services.lay_trang_thai_dich_f2`):
    - Chuyển trạng thái xuôi (`Xác nhận đã thanh toán` hoặc `Đánh dấu hoàn thành` khi đã qua `NgayKetThuc`).
    - Hoặc chọn **Hủy đơn hàng**:
      - Chọn ngày/giờ hủy (mặc định theo `hien_tai()`), nhập `Lý do hủy`.
      - Khối **Xem trước phí phạt tự động** (gọi `services.tinh_xem_truoc_phat_huy` mỗi khi đổi ngày/giờ): hiển thị số giờ sau khi đặt, số ngày trước khởi hành, tỷ lệ phạt (`0%/10%/30%/50%/100%`), phí phạt và số tiền hoàn lại.
      - Checkbox xác nhận `"Khách hàng đã đồng ý với mức phí phạt hủy tour"`.
      - Nút `Xác nhận hủy đơn` (thực thi giao dịch nguyên tử 3 bước: cập nhật đơn `HUY`, hoàn chỗ lịch trình, xóa chuyến trung chuyển).
  - Nút **`Xuất phiếu xác nhận (PDF)`** ngay trong ngăn chi tiết.

#### 3. Xuất phiếu xác nhận đặt tour (`/admin/confirmations`)
- Chọn bất kỳ đơn hàng nào từ danh sách có tìm kiếm nhanh (hoặc nhận sẵn từ `?order=DHxxx`).
- Nhập `Nhân viên lập phiếu` (mặc định theo tài khoản quản trị đang đăng nhập, cho phép chỉnh sửa).
- **Khung xem trước biểu mẫu A4 trực tiếp** (render HTML chuẩn từ `phieu_xac_nhan.html`) + 2 nút rõ ràng:
  - **`Tải phiếu xác nhận (PDF - A4 dọc)`** (gọi API xuất file `.pdf` thật).
  - **`In trực tiếp`** (mở lệnh in trình duyệt cho khung phiếu).

---

## 6. Hợp đồng REST API (Backend Endpoints)

| Phương thức & Đường dẫn | Vai trò | Chức năng & Hàm `services.py` tái sử dụng |
|---|---|---|
| `GET /api/meta` | Public | Trả về ngày hệ thống hiện tại (`db.hien_tai()`), tên hệ thống. |
| `GET /api/landing` | Public | Thống kê thực từ DB (số tỉnh, số tour, số lịch trình mở, tổng khách, điểm TB) + danh sách tour nổi bật sắp khởi hành. |
| `GET /api/provinces` | Public | `services.lay_ds_tinh_thanh()` |
| `GET /api/schedules/search` | Public | `services.tim_kiem_lich_trinh(...)` với đầy đủ 8 tham số lọc. |
| `GET /api/schedules/open` | Public | `services.lay_lich_trinh_con_cho(hien_tai())` |
| `GET /api/accommodations` | Public | `services.lay_noi_nghi_theo_tinh(ma_tinh_den)` |
| `GET /api/customers` | Public/Demo | `services.lay_ds_khach_hang_f1()` (dùng cho chọn khách trên form đặt tour & đăng nhập demo). |
| `POST /api/customers/check-duplicate` | Public | `services.kiem_tra_trung_khach_hang(email, sdt)` |
| `POST /api/auth/customer-login` | Public | Tra cứu khách hàng theo Email hoặc SĐT từ `KhachHang` / `SDT_KhachHang`. |
| `POST /api/auth/admin-login` | Public | Xác thực tài khoản quản trị demo ở tầng ứng dụng, trả về token phiên và họ tên nhân viên. |
| `POST /api/bookings/estimate` | Public | `services.tinh_du_toan_f1(...)` |
| `POST /api/bookings` | Public | `services.kiem_tra_dat_tour(...)` + `services.kiem_tra_trung_khach_hang(...)` + `services.luu_dat_tour(...)`. |
| `GET /api/customers/{ma_kh}/orders` | User | Lấy toàn bộ đơn hàng của `ma_kh` từ `v_DonHang_ChiTiet` + cờ `CoTheDanhGia`. |
| `GET /api/customers/{ma_kh}/pending-reviews` | User | `services.lay_don_cho_danh_gia(ma_kh)` |
| `POST /api/reviews` | User | `services.kiem_tra_danh_gia(...)` + `services.luu_danh_gia(...)` |
| `GET /api/orders/{ma_don}/confirmation/pdf` | User/Admin | Xuất file PDF A4 dọc cho phiếu xác nhận (`tao_html_phieu_xac_nhan` -> `pdf_service`). User chỉ được tải đơn thuộc `ma_kh` của mình (hoặc Admin tải mọi đơn). |
| `GET /api/admin/orders` | Admin | Danh sách toàn bộ đơn hàng từ `v_DonHang_ChiTiet` (lọc theo trạng thái & từ khóa). |
| `GET /api/admin/orders/{ma_don}` | Admin | `services.lay_chi_tiet_don_f2(ma_don)` + `lay_trang_thai_dich_f2` + `lay_sdt_khach_r1` + `lay_lich_trung_chuyen_r1`. |
| `POST /api/admin/orders/{ma_don}/cancel-preview` | Admin | `services.tinh_xem_truoc_phat_huy(ma_don, ngay_gio_huy)` |
| `POST /api/admin/orders/{ma_don}/cancel` | Admin | `services.kiem_tra_huy_don(...)` + `services.huy_don(...)` |
| `PATCH /api/admin/orders/{ma_don}/status` | Admin | `services.chuyen_trang_thai_don(ma_don, trang_thai_moi, hien_tai())` |
| `GET /api/admin/orders/{ma_don}/confirmation/html` | Admin | Trả HTML xem trước của Phiếu xác nhận (`tao_html_phieu_xac_nhan`). |
| `GET /api/admin/reports/revenue` | Admin | `services.lay_doanh_thu_tour_r2(tu_ngay, den_ngay)` + `services.lay_xep_hang_noi_nghi_r2(tu_ngay, den_ngay)`. |
| `POST /api/admin/reports/revenue/html` | Admin | Trả HTML xem trước của Báo cáo doanh thu (`tao_html_bao_cao_doanh_thu`). |
| `POST /api/admin/reports/revenue/pdf` | Admin | Xuất file **`.pdf` A4 ngang** từ HTML Báo cáo doanh thu qua `pdf_service`. |

---

## 7. Tài nguyên hình ảnh cục bộ

Bộ 11 ảnh phong cảnh miền Bắc chất lượng cao thuộc phạm vi triển khai: được sinh trực tiếp bằng subagent `image-generator` của hệ thống ngay trong giai đoạn đầu triển khai (phong cách nhiếp ảnh du lịch tự nhiên, ánh sáng trong trẻo, không chữ, không watermark) và lưu cố định tại `web_app/frontend/public/images/`:
- `hero-northern-vietnam.png` — Toàn cảnh Vịnh Hạ Long nắng sáng xanh trong (cho khung Hero bo cong organic).
- `promo-cruise.png` — Du thuyền sang trọng trên vịnh di sản lúc hoàng hôn nhẹ (cho thẻ Tour cao cấp).
- `tour-T01.png` — Vịnh Hạ Long & chèo kayak giữa núi đá vôi.
- `tour-T02.png` — Sa Pa & biển mây Fansipan, ruộng bậc thang Lào Cai.
- `tour-T03.png` — Thuyền nan trên sông Ngô Đồng / Tràng An, Ninh Bình.
- `tour-T04.png` — Đồi chè xanh mướt Mộc Châu, Sơn La.
- `tour-T05.png` — Đảo Cát Bà & Vịnh Lan Hạ nước xanh ngọc, Hải Phòng.
- `tour-T06.png` — Thác Bản Giốc hùng vĩ, Cao Bằng.
- `tour-T07.png` — Du thuyền cao cấp qua đêm giữa Vịnh Hạ Long – Lan Hạ.
- `tour-T08.png` — Cung đường đèo núi Tây Bắc & thung lũng Mường Thanh, Điện Biên.
- `tour-T09.png` — Đèo Mã Pì Lèng & dòng sông Nho Quế xanh biếc, Hà Giang.

Ánh xạ ảnh được quản lý tập trung tại `web_app/frontend/src/constants/tourImages.ts` kèm fallback mặc định để không bao giờ xảy ra lỗi thiếu ảnh.

---

## 8. Quyền quyết định để lại cho đội triển khai (Left to Builder)
- Tổ chức chi tiết thư mục con component trong `web_app/frontend/src/components/`.
- Cấu hình cụ thể Vite proxy `/api` -> `http://127.0.0.1:8000` và script khởi chạy 2 server (FastAPI + Vite) hoặc build tĩnh.
- Lựa chọn cụ thể biểu đồ (Recharts `BarChart` ngang hay dọc) và cấu trúc skeleton loading state cho từng màn hình.
- Thiết kế các test case bổ sung cho `web_app/backend/tests/test_api.py` (bao gồm kiểm tra xuất PDF trả về `%PDF-` 1 trang A4).

---

## 9. Tiêu chí kiểm chứng hoàn thành (Definition of Done)
1. **Kiểm thử gốc giữ xanh 100%:** `python -m unittest discover -s tour_app\tests -v` đạt PASS toàn bộ, `4_KiemTra_RangBuoc.sql` trả kết quả rỗng.
2. **Kiểm thử Backend mới:** `python -m unittest discover -s web_app\backend\tests -v` đạt PASS toàn bộ (bao gồm test tìm kiếm 8 tiêu chí, đặt tour, hủy đơn hoàn chỗ, đánh giá, phân quyền admin, và xuất file `.pdf` A4 hợp lệ cho cả Báo cáo doanh thu lẫn Phiếu xác nhận).
3. **Build Frontend không lỗi:** `npm run build` trong `web_app/frontend` thành công với 0 lỗi TypeScript/Vite.
4. **Kiểm chứng trực quan trên trình duyệt thật (desktop 1440px và mobile 390px):**
   - Landing Page hiển thị đúng chủ đề sáng xanh cobalt, hình khối hero bo cong organic, thanh tìm kiếm nổi, thẻ tour có ảnh thật miền Bắc, không còn thông tin PTIT/12 bảng/đồng hồ demo.
   - Không xuất hiện bất kỳ mã `F1.`, `F2.`, `F3.`, `S1.`, `R1.`, `R2.` hay các dòng ghi chú kỹ thuật kiểu AI nào.
   - Luồng User (Khám phá -> Đặt tour -> Xem đơn của tôi -> Đánh giá -> Tải phiếu PDF) và luồng Admin (Đăng nhập -> Dashboard & tải Báo cáo PDF A4 ngang -> Quản lý đơn & hủy đơn -> Xuất phiếu xác nhận PDF A4 dọc) hoạt động trơn tru trên dữ liệu MySQL thực.
