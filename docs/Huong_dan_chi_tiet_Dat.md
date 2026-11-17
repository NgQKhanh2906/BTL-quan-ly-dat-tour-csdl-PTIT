# Hướng dẫn Cầm tay Chỉ việc Chi tiết cho ĐẠT (Từ A đến Z)

- **Họ và tên thành viên:** Nguyễn Tất Đạt (`B24DCCN117`)
- **Trạng thái hoàn thành (17/11/2026):** Đã hoàn thành `D1` đến `D7` (`ERD.drawio` đã sửa nhãn `DenTai`, `TenTour`, `LyDoHuy`; `1_Dat_tour.py` hỗ trợ chọn khách có sẵn + tạo khách mới chặn trùng Email/SĐT; đã chụp `Hinh04`, `Hinh05a`, `Hinh05b`; đã lập `docs/GopY_Dat.md`). Việc cần làm tiếp ở ngoài môi trường code: mở `ERD.drawio` trong draw.io xuất lại `ERD.png`/`Hinh01_ERD.png` khớp nhãn vừa sửa, thử máy sạch (`D8`) và tập thuyết trình (`D9`).
- **Vai trò trong nhóm:** Phụ trách Sơ đồ Thực thể Liên kết (`ERD.drawio`, `ERD.png`), Ánh xạ mô hình ERD sang 12 lược đồ quan hệ, Lập trình màn hình Form đặt tour (`F1` - `tour_app/pages/1_Dat_tour.py`), Kiểm thử trên máy sạch và Phụ trách báo cáo các mục 2.3, 3.1, 3.2, 6.2.
- **Mục tiêu của tài liệu này:** Bạn chỉ cần đọc duy nhất tài liệu này và làm lần lượt từng bước là hoàn thành 100% công việc của mình mà không cần tra cứu lại bất kỳ tài liệu nào khác. Mọi mã định dạng `draw.io`, tọa độ vẽ hình, câu lệnh SQL, code Python, kịch bản kiểm thử và lệnh Git đều được hướng dẫn tận tay tại đây.

---

## Phần 1. Tổng quan Lịch làm việc của Đạt theo Ngày (D1 -> D9)

| Mã Task | Ngày thực hiện | Tên công việc | Nền tảng sử dụng | Sản phẩm đầu ra (File cụ thể) | Cách tự kiểm tra đã đạt |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **D1** | **05/11 - 06/11** | Vẽ và hoàn thiện sơ đồ ERD bản cuối (11 thực thể, 12 mối liên kết, có `TheThanhToan`) | Web `app.diagrams.net` hoặc phần mềm **draw.io** | `docs/diagrams/ERD.drawio`, `docs/diagrams/ERD.png`, `screenshots/Hinh01_ERD.png` | Đủ 11 thực thể, 12 hình thoi quan hệ, đúng 4 ký hiệu đặc biệt (thực thể yếu, đa trị, dẫn xuất, phức hợp), nền trắng, phóng 200% rõ chữ |
| **D2** | **06/11/2026** | Báo cáo tình trạng màn hình `F1` tại buổi họp nhóm H1 (tối 06/11) | Streamlit, MySQL Workbench | Danh sách ca kiểm thử đã đạt và chưa đạt | Chạy thử được ít nhất Ca 1 trên máy cá nhân |
| **D3** | **08/11 - 10/11** | Hoàn thiện code màn hình Form đặt tour `F1` vượt qua toàn bộ ca kiểm thử | VS Code, PowerShell, Streamlit, MySQL Workbench | `tour_app/pages/1_Dat_tour.py` (trên nhánh `feature/f1-dat-tour`) | Đạt đủ 6 ca kiểm thử trong báo cáo (8 ca chi tiết); tạo được đơn `DH015` tổng `32.020.000 đ`, `LT10` còn `15` chỗ |
| **D4** | **11/11/2026** | Chụp 3 ảnh màn hình của `F1` (`Hinh04`, `Hinh05a`, `Hinh05b`) | Trình duyệt Edge (zoom 100%), Paint | `screenshots/Hinh04_F1_GiaoDien.png`, `Hinh05a_F1_Loi.png`, `Hinh05b_F1_Loi.png` | Ảnh rõ nét, đúng số liệu `32.020.000 đ` và thông báo lỗi tiếng Việt |
| **D5** | **12/11 - 13/11** | Rà soát báo cáo các mục 2.3, 3.1, 3.2, 6.2 và gửi thông tin cá nhân (Họ tên, MSSV) | Microsoft Word (chế độ đọc), VS Code | `docs/GopY_Dat.md` | Tên thực thể, thuộc tính, 12 lược đồ quan hệ và SQL mục 6.2 khớp 100% với ERD và code `1_Dat_tour.py` |
| **D6** | **14/11/2026** | Kiểm thử chéo màn hình `S1` (Tìm kiếm) và `R2` (Báo cáo doanh thu) của Khánh | Streamlit, MySQL Workbench | Danh sách lỗi gửi Khánh (nếu có) | Kiểm tra đủ 6 ca của `S1`; kiểm tra `R2` kỳ `01/09 - 31/12/2026` có tổng cộng `79.110.000 đ` |
| **D7** | **15/11 - 16/11** | Sửa lỗi `F1` (nếu Thịnh báo) và đối chiếu tên bảng/cột giữa ERD, Data Diagram, Báo cáo, Code | VS Code, MySQL Workbench | Bảng đối chiếu xác nhận không lệch tên | Không còn bất kỳ tên thực thể, bảng hay cột nào viết khác nhau giữa 4 nơi |
| **D8** | **17/11/2026** | Cài đặt thử toàn bộ dự án trên một máy tính sạch theo đúng Phụ lục báo cáo | Máy tính thứ hai có MySQL 8.0 & Python | Danh sách bước thiếu trong Phụ lục (nếu có) và **Laptop dự phòng** cho buổi bảo vệ | Cài và mở được trang chủ `12 bảng` mà không cần hỏi Khánh |
| **D9** | **18/11 - 21/11** | Kiểm tra lại ảnh `ERD.png` độ phân giải cao và tập thuyết trình phần ERD | PowerPoint, Ứng dụng | Phần trình bày 3 phút (`1:30 - 4:30`) và thuyết minh demo `F1` | Nói trôi chảy không nhìn giấy, trả lời được 5 câu hỏi vấn đáp |

---

## Phần 2. Bước Khởi đầu: Cài đặt Môi trường và Cách Dùng Git/GitHub cho Đạt

### I. Thiết lập lần đầu trên máy tính của Đạt (Chỉ làm 1 lần)
1. Mở **PowerShell** tại ổ đĩa của bạn (ví dụ `D:\`), tải dự án từ GitHub về máy:
   ```powershell
   git clone https://github.com/NgQKhanh2906/BTL-quan-ly-dat-tour-csdl-PTIT.git
   cd BTL-quan-ly-dat-tour-csdl-PTIT
   ```
2. Mở **MySQL Workbench 8.0**, đăng nhập vào Local instance -> bấm `File > Open SQL Script...` -> chọn file `database/1_QuanLyDatTour_v3.sql` -> nhấn `Ctrl + Shift + Enter` để tạo CSDL `QuanLyDatTour` (12 bảng, 2 view, 104 dòng mẫu).
3. Quay lại cửa sổ **PowerShell** đang đứng ở thư mục dự án, tạo môi trường ảo Python và cài thư viện:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r tour_app\requirements.txt
   ```
   *(Lưu ý: Nếu PowerShell báo lỗi không cho chạy `Activate.ps1`, hãy chạy lệnh `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` rồi gõ `Y` và nhấn Enter, sau đó chạy lại `.\.venv\Scripts\Activate.ps1`).*
4. Lưu mật khẩu tài khoản `root` MySQL của máy bạn vào biến môi trường (để `db.py` tự đọc mà bạn không cần sửa code của `db.py`):
   ```powershell
   setx MYSQL_PASSWORD "mat_khau_mysql_tren_may_cua_Dat"
   ```
   Sau khi chạy lệnh `setx`, hãy **đóng cửa sổ PowerShell đó lại** và mở một cửa sổ PowerShell mới tại thư mục dự án.
5. Chạy thử ứng dụng để kiểm tra:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   cd tour_app
   streamlit run app.py
   ```
   Trình duyệt tự mở `http://localhost:8501`. Nếu thấy dòng chữ màu xanh `"Đã kết nối cơ sở dữ liệu: 12 bảng"` nghĩa là máy của bạn đã sẵn sàng 100%.

### II. Quy tắc Vàng khi Đạt làm việc với Git
- Bạn **chỉ sửa** các file thuộc phạm vi của mình:
  - Sơ đồ ERD: `docs/diagrams/ERD.drawio`, `docs/diagrams/ERD.png`.
  - Code màn hình F1: `tour_app/pages/1_Dat_tour.py` (làm trên nhánh riêng `feature/f1-dat-tour`).
  - Ảnh chụp của Đạt: `screenshots/Hinh01_ERD.png`, `screenshots/Hinh04_F1_GiaoDien.png`, `screenshots/Hinh05a_F1_Loi.png`, `screenshots/Hinh05b_F1_Loi.png`.
  - File góp ý báo cáo: `docs/GopY_Dat.md`.
- **Tuyệt đối không sửa** trực tiếp file Word `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` (chỉ Thịnh sửa) và không sửa `tour_app/db.py` (chỉ Khánh sửa).

---

## Phần 3. Hướng dẫn Cầm tay Chỉ việc Từng Task của Đạt

---

### BƯỚC 1 (Task D1 - Hạn 06/11): Vẽ Sơ đồ ERD Ký hiệu Chen trên `draw.io`

#### 1. Tại sao phải vẽ đúng ký hiệu Chen và tại sao có 11 thực thể, 12 mối liên kết?
- **Lý do thang điểm:** Tiêu chí 2 (Vẽ và mô tả ERD) chiếm tới **2,5 / 10 điểm** (cao nhất trong 8 tiêu chí). Giảng viên chấm rất kỹ việc phân biệt: thực thể mạnh, thực thể yếu, thuộc tính khóa, khóa bộ phận, thuộc tính đa trị, thuộc tính dẫn xuất, thuộc tính phức hợp, bản số (`1`, `N`) và kiểu tham gia (đường đơn = tham gia một phần / Partial, đường đôi = tham gia toàn phần / Total).
- **Lý do nâng từ 10 lên 11 thực thể:** Sau khi chuẩn hóa bảng `KhachHang` đạt 3NF (loại bỏ phụ thuộc bắc cầu `MaKH -> SoID -> LoaiThe`), nhóm tách `SoID` và `LoaiThe` ra thành thực thể mạnh thứ 11 là `TheThanhToan`, nối với `KhachHang` qua mối liên kết thứ 12 là `ThanhToanBang`.

#### 2. Cách dán mã định dạng (Style) nhanh và chuẩn xác trên `draw.io`
1. Mở trang web `https://app.diagrams.net` (hoặc phần mềm draw.io trên máy), tạo sơ đồ trống hoặc mở file `ERD.drawio`.
2. Vào menu bên phải, bật `Grid` (Lưới) để căn thẳng hàng và đảm bảo `Background` (Màu nền) là màu trắng (không dùng nền đen vì in ra giấy sẽ bị mờ).
3. Để tạo bất kỳ hình nào đúng chuẩn ký hiệu Chen:
   - Kéo một hình cơ bản (chữ nhật, elip, hình thoi, đường thẳng) ra trang vẽ.
   - Nhấp chuột phải vào hình đó -> chọn **Edit Style...** (hoặc chọn hình rồi nhấn phím tắt `Ctrl + E`).
   - Xóa hết chữ cũ trong ô, dán đúng dòng mã trong bảng dưới đây vào rồi bấm **Apply**:

| Loại thành phần trên ERD | Hình dáng hiển thị | Mã Style dán vào ô `Edit Style` (`Ctrl + E`) | Áp dụng cho các đối tượng nào |
| :--- | :--- | :--- | :--- |
| **1. Thực thể mạnh** | Hình chữ nhật nét đơn, chữ in đậm | `rounded=0;whiteSpace=wrap;html=1;fontStyle=1;` | `TinhThanh`, `TheThanhToan`, `KhachHang`, `Tour`, `LichTrinh`, `NhaNghi`, `DonViVanTai`, `Xe`, `TrangThaiDonHang`, `DonHang` (10 thực thể mạnh) |
| **2. Thực thể yếu** | Hình chữ nhật **viền đôi**, chữ in đậm | `shape=ext;double=1;margin=3;rounded=0;whiteSpace=wrap;html=1;fontStyle=1;` | `ChuyenTrungChuyen` (1 thực thể yếu) |
| **3. Thuộc tính thường** | Hình elip nét đơn | `ellipse;whiteSpace=wrap;html=1;` | Các thuộc tính bình thường (`HoTen`, `Email`, `TenTour`...) |
| **4. Thuộc tính khóa chính** | Hình elip, chữ **gạch chân liền** | `ellipse;whiteSpace=wrap;html=1;fontStyle=4;` | 10 khóa chính: `MaTinh`, `SoID`, `MaKH`, `MaTour`, `MaLichTrinh`, `MaNhaNghi`, `MaDVVT`, `BienSo`, `MaTrangThai`, `MaDonHang` |
| **5. Khóa bộ phận (Thực thể yếu)** | Hình elip, chữ **gạch chân nét đứt** | Xem hướng dẫn làm thủ công 4 bước ngay dưới bảng này | `LoaiChuyen` (của thực thể yếu `ChuyenTrungChuyen`) |
| **6. Thuộc tính đa trị** | Hình elip **viền đôi** | `ellipse;shape=doubleEllipse;whiteSpace=wrap;html=1;` | `SDT` (của `KhachHang`) |
| **7. Thuộc tính dẫn xuất** | Hình elip **viền nét đứt** | `ellipse;whiteSpace=wrap;html=1;dashed=1;` | 4 thuộc tính: `SoDem` (của `LichTrinh`), `TongTien`, `TienPhat`, `TienHoan` (của `DonHang`) |
| **8. Thuộc tính phức hợp** | Elip cha nối với thực thể, các elip con nối vào elip cha | `ellipse;whiteSpace=wrap;html=1;` | 2 thuộc tính của `DonHang`: `DanhGiaTour` (nối ra 2 elip con `DiemTour`, `NhanXetTour`) và `DanhGiaNhaNghi` (nối ra 2 elip con `DiemNhaNghi`, `NhanXetNhaNghi`) |
| **9. Mối liên kết thường** | Hình thoi nét đơn | `rhombus;whiteSpace=wrap;html=1;` | 11 mối liên kết thường (`ThanhToanBang`, `Dat`, `CoTrangThai`, `ThuocLichTrinh`, `LuuTru`, `CoLichTrinh`, `NamTai`, `XuatPhatTu`, `DenTai`, `SoHuu`, `PhucVu`) |
| **10. Mối liên kết xác định** | Hình thoi **viền đôi** | `rhombus;double=1;whiteSpace=wrap;html=1;` | `CoChuyen` (nối giữa `DonHang` và thực thể yếu `ChuyenTrungChuyen`) |
| **11. Đường nối tham gia một phần (Partial)** | Đường thẳng nét đơn, không mũi tên | `endArrow=none;html=1;` | Các nhánh có tham gia một phần (Partial) và mọi đường nối thuộc tính |
| **12. Đường nối tham gia toàn phần (Total)** | Đường thẳng **nét đôi**, không mũi tên | `shape=link;html=1;` | Các nhánh bắt buộc tham gia toàn phần (Total) |

- **Cách vẽ thủ công Khóa bộ phận `LoaiChuyen` (gạch chân nét đứt):**
  1. Tạo 1 elip thường (`ellipse;whiteSpace=wrap;html=1;`), gõ chữ `LoaiChuyen` (không bật gạch chân).
  2. Vẽ 1 đoạn thẳng ngắn có độ dài bằng chữ `LoaiChuyen`, đặt ngay sát dưới chữ `LoaiChuyen`.
  3. Nhấn `Ctrl + E` vào đoạn thẳng đó, dán style: `endArrow=none;html=1;dashed=1;` rồi bấm Apply.
  4. Quét chọn cả elip `LoaiChuyen` và đoạn thẳng nét đứt, nhấn `Ctrl + G` để gom nhóm (Group) lại thành một khối.

#### 3. Bố cục Tọa độ và Cách nối 11 Thực thể - 12 Mối liên kết
- Đặt kích thước thống nhất: Thực thể `150 x 50 px` (cỡ chữ 14 đậm), Hình thoi quan hệ `120 x 60 px` (cỡ chữ 12), Thuộc tính `110 x 40 px` (hoặc `140 x 40 px` cho tên dài, cỡ chữ 11).
- Sắp xếp sơ đồ khung theo 4 hàng để không có đường nối nào cắt chéo qua hình khác:
  - **Hàng 1 (Trên cùng):** `[TheThanhToan]` -- `<ThanhToanBang>` (phía trái trên của `KhachHang`); `[TrangThaiDonHang]` -- `<CoTrangThai>` (phía trên `DonHang`).
  - **Hàng 2 (Giữa):** `[KhachHang]` -- `<Dat>` == `[DonHang]` == `<<CoChuyen>>` == `[[ChuyenTrungChuyen]]` -- `<PhucVu>` -- `[Xe]` == `<SoHuu>` -- `[DonViVanTai]`.
  - **Hàng 3 (Dưới Hàng 2):** `[LichTrinh]` (nối lên `DonHang` qua `<ThuocLichTrinh>`) và `[NhaNghi]` (nối lên `DonHang` qua `<LuuTru>`).
  - **Hàng 4 (Dưới cùng):** `[Tour]` (nối lên `LichTrinh` qua `<CoLichTrinh>`) == `<XuatPhatTu>` & `<DenTai>` -- `[TinhThanh]` (nối lên `NhaNghi` qua `<NamTai>`).

- **Bảng kiểm tra chính xác Bản số (`1`, `N`) và Loại đường nối (Đơn/Đôi) cho 12 Mối liên kết:**

| STT | Tên Hình thoi Liên kết | Loại hình thoi | Thực thể Bên `1` | Đường nối Bên `1` | Thực thể Bên `N` | Đường nối Bên `N` |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `ThanhToanBang` | Thoi đơn | `TheThanhToan` | Bản số `1`, **Đường đôi** (Total) | `KhachHang` | Bản số `N`, Đường đơn (Partial) |
| 2 | `Dat` | Thoi đơn | `KhachHang` | Bản số `1`, Đường đơn (Partial) | `DonHang` | Bản số `N`, **Đường đôi** (Total) |
| 3 | `CoTrangThai` | Thoi đơn | `TrangThaiDonHang` | Bản số `1`, Đường đơn (Partial) | `DonHang` | Bản số `N`, **Đường đôi** (Total) |
| 4 | `ThuocLichTrinh` | Thoi đơn | `LichTrinh` | Bản số `1`, Đường đơn (Partial) | `DonHang` | Bản số `N`, **Đường đôi** (Total) |
| 5 | `LuuTru` | Thoi đơn | `NhaNghi` | Bản số `1`, Đường đơn (Partial) | `DonHang` | Bản số `N`, Đường đơn (Partial) |
| 6 | `CoChuyen` | **Thoi viền đôi** | `DonHang` | Bản số `1`, Đường đơn (Partial) | `ChuyenTrungChuyen` | Bản số `N`, **Đường đôi** (Total) |
| 7 | `PhucVu` | Thoi đơn | `Xe` | Bản số `1`, Đường đơn (Partial) | `ChuyenTrungChuyen` | Bản số `N`, Đường đơn (Partial) |
| 8 | `SoHuu` | Thoi đơn | `DonViVanTai` | Bản số `1`, Đường đơn (Partial) | `Xe` | Bản số `N`, **Đường đôi** (Total) |
| 9 | `CoLichTrinh` | Thoi đơn | `Tour` | Bản số `1`, Đường đơn (Partial) | `LichTrinh` | Bản số `N`, **Đường đôi** (Total) |
| 10 | `NamTai` | Thoi đơn | `TinhThanh` | Bản số `1`, Đường đơn (Partial) | `NhaNghi` | Bản số `N`, **Đường đôi** (Total) |
| 11 | `XuatPhatTu` | Thoi đơn | `TinhThanh` | Bản số `1`, Đường đơn (Partial) | `Tour` | Bản số `N`, **Đường đôi** (Total) |
| 12 | `DenTai` | Thoi đơn | `TinhThanh` | Bản số `1`, Đường đơn (Partial) | `Tour` | Bản số `N`, **Đường đôi** (Total) |

- **Bảng kiểm tra đầy đủ các Elip Thuộc tính của từng Thực thể (Tuyệt đối không vẽ khóa ngoại lên ERD):**
  1. `TinhThanh`: **MaTinh** (gạch chân), `TenTinh`.
  2. `TheThanhToan`: **SoID** (gạch chân), `LoaiThe`.
  3. `KhachHang`: **MaKH** (gạch chân), `HoTen`, `Email`, `DiaChi`, `SDT` (elip **viền đôi**). *(Chú ý: Không còn `SoID` và `LoaiThe` ở đây).*
  4. `Tour`: **MaTour** (gạch chân), `TenTour`, `MoTa`.
  5. `LichTrinh`: **MaLichTrinh** (gạch chân), `NgayXuatPhat`, `NgayKetThuc`, `DiemTapTrung`, `DiemTraKhach`, `GiaCoBan`, `SoChoToiDa`, `SoChoDaDat`, `SoDem` (elip **nét đứt**).
  6. `NhaNghi`: **MaNhaNghi** (gạch chân), `TenNhaNghi`, `LoaiHinh`, `DiaChi`, `SoDienThoai`, `GiaPhongMoiDem`.
  7. `DonViVanTai`: **MaDVVT** (gạch chân), `TenDonVi`, `SoDienThoai`, `DiaChi`.
  8. `Xe`: **BienSo** (gạch chân), `SoCho`.
  9. `TrangThaiDonHang`: **MaTrangThai** (gạch chân), `TenTrangThai`, `ThuTu`.
  10. `DonHang` (chia thành 3 cụm quanh hình chữ nhật `DonHang` cho thoáng):
      - Cụm Đặt tour: **MaDonHang** (gạch chân), `NgayDat`, `SoLuongKhach`, `SoPhong`, `TongTien` (elip **nét đứt**).
      - Cụm Hủy tour: `NgayHuy`, `LyDoHuy`, `TienPhat` (elip **nét đứt**), `TienHoan` (elip **nét đứt**).
      - Cụm Đánh giá: `DanhGiaTour` (nối ra 2 elip con `DiemTour`, `NhanXetTour`), `DanhGiaNhaNghi` (nối ra 2 elip con `DiemNhaNghi`, `NhanXetNhaNghi`), `NgayDanhGia`.
  11. `ChuyenTrungChuyen`: `LoaiChuyen` (gạch chân **nét đứt**), `DiaChiDon`, `ThoiGianDon`.

#### 4. Xuất file và Đẩy lên GitHub
1. Bấm `File > Save as...` -> lưu vào `docs/diagrams/ERD.drawio`.
2. Bấm `File > Export as > PNG...` -> nhập `Zoom = 200%`, `Border Width = 10`, **bỏ tích** `Transparent Background` -> bấm `Export` và lưu thành 2 file: `docs/diagrams/ERD.png` và `screenshots/Hinh01_ERD.png`.
3. Mở PowerShell đẩy lên GitHub:
   ```powershell
   git checkout main
   git pull origin main
   git add docs/diagrams/ERD.drawio docs/diagrams/ERD.png screenshots/Hinh01_ERD.png
   git commit -m "docs: hoan thien so do ERD 11 thuc the 12 moi lien ket"
   git push origin main
   ```

---

### BƯỚC 2 (Task D3 - Hạn 10/11): Lập trình Màn hình Form Đặt Tour (`F1` - `tour_app/pages/1_Dat_tour.py`)

#### 1. Tại sao phải đặt ô Lịch trình và Nơi nghỉ ở ngoài `st.form` và dùng `ghi()` trong 1 Transaction?
- **Đặc điểm của Streamlit:** Các ô nhập đặt bên trong khối `with st.form(...)` sẽ không gửi sự kiện cập nhật lại giao diện cho đến khi người dùng bấm nút Submit. Trong khi đó, ở màn hình Đặt tour (`F1`), ngay khi người dùng đổi **Lịch trình**, giao diện phải lập tức: (1) lọc lại danh sách **Nơi nghỉ** theo đúng tỉnh đến của lịch trình đó (`RB24`), (2) ẩn phần nơi nghỉ và chuyến xe về nơi nghỉ nếu lịch trình là tour trong ngày (`SoDem == 0`, `RB25`), (3) cập nhật giới hạn tối đa của ô **Số khách** theo `SoChoConLai`, và (4) tính lại **Tổng tiền dự kiến** ngay trên màn hình. Do đó, phải đặt các ô điều khiển động ở ngoài hoặc dùng giao diện phản hồi trực tiếp rồi xử lý lưu khi bấm nút `"Xác nhận đặt tour"`.
- **Tại sao phải dùng `ghi()` trong 1 Transaction:** Khi khách đặt tour, hệ thống phải vừa thêm dòng vào `DonHang`, vừa cộng `SoChoDaDat` trong `LichTrinh`, vừa thêm 0-2 dòng vào `ChuyenTrungChuyen`. Nếu đặt trong 1 Transaction (`ghi()`), giả sử có 2 nhân viên cùng bấm đặt những chỗ cuối cùng của `LT08`, người bấm sau sẽ làm `SoChoDaDat > SoChoToiDa`, vi phạm `chk_LichTrinh_SoChoDaDat` (lỗi `3819`) và MySQL sẽ tự động `ROLLBACK` toàn bộ, không để lọt đơn hàng rác trong bảng `DonHang`.

#### 2. Bảng 11 Trường của Form Đặt Tour (`F1`) và Quy tắc Kiểm tra 2 Lớp

| # | Tên trường trên giao diện | Cách hiển thị | Nguồn dữ liệu | Kiểm tra Lớp 1 (Trên Form Python) | Kiểm tra Lớp 2 (Trong MySQL) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **Khách hàng** | `st.selectbox`, hiện `"KH001 - Nguyễn Văn An"` | Câu SQL `F1.1` | Bắt buộc chọn | `fk_DonHang_KhachHang` |
| 2 | **Lịch trình** | `st.selectbox`, hiện `"Tên tour | Ngày đi | Giá | Còn X chỗ"` | Câu SQL `F1.2` | Chỉ liệt kê lịch trình có `NgayXuatPhat > HienTai` và `SoChoConLai > 0` | Bảo đảm `RB22` |
| 3 | **Số khách** | `st.number_input`, `min_value=1`, `max_value=SoChoConLai` | Nhập số nguyên | Từ `1` đến `SoChoConLai` | `chk_DonHang_SoLuongKhach`, `chk_LichTrinh_SoChoDaDat` |
| 4 | **Nơi nghỉ** | `st.selectbox`, mục đầu là `"Không đặt nơi nghỉ"` | Câu SQL `F1.3` (lọc theo `MaTinhDen`) | Tự động ẩn hoàn toàn khi `SoDem == 0` (tour trong ngày) | Bảo đảm `RB24`, `RB25` |
| 5 | **Số phòng** | `st.number_input`, chỉ hiện khi có chọn Nơi nghỉ | Nhập số nguyên | Có nơi nghỉ: phải từ `1` đến `SoKhach` (nếu `SoPhong > SoKhach` thì báo lỗi chặn gửi); không đặt nơi nghỉ thì gán `0` | `chk_DonHang_NhaNghi` |
| 6 | **Cần xe đón tại nhà** | `st.checkbox` | Tích chọn | Tùy chọn | |
| 7 | **Địa chỉ đón** | `st.text_input` (`max_chars=255`), chỉ hiện khi tích ô 6, mặc định lấy `DiaChi` của khách từ `F1.1` | Nhập chuỗi | Khi tích ô 6, nếu để trống (`not dia_chi_don.strip()`) thì báo `"Vui lòng nhập địa chỉ đón"` | `chk_ChuyenTrungChuyen_DiaChiDon` |
| 8 | **Ngày giờ đón tại nhà** | `st.date_input` + `st.time_input`, mặc định trước `NgayXuatPhat` 2 tiếng | Nhập ngày giờ | Khi tích ô 6: phải `> hien_tai()` và `< NgayXuatPhat` (sai thì báo `"Giờ đón tại nhà phải sau thời điểm hiện tại và trước giờ xuất phát"`) | Bảo đảm `RB28` |
| 9 | **Cần xe về nơi nghỉ** | `st.checkbox`, chỉ hiện khi đã chọn Nơi nghỉ | Tích chọn | Tự động ẩn nếu không đặt nơi nghỉ | Bảo đảm `RB27` |
| 10 | **Ngày giờ về nơi nghỉ** | `st.date_input` + `st.time_input` | Nhập ngày giờ | Khi tích ô 9: phải `>= NgayXuatPhat` và `<= NgayKetThuc` (sai thì báo lỗi chặn gửi) | Bảo đảm `RB28` |
| 11 | **Tổng tiền dự kiến** | Hiển thị nổi bật (`st.metric` hoặc `st.info`) | Câu SQL `F1.5` | Tự động tính lại: `TienTour + TienPhong = Tổng tiền dự kiến` | Khớp công thức View `v_DonHang_ChiTiet` |

#### 3. Toàn bộ Câu lệnh SQL và Hàm Lưu đơn trong `tour_app/pages/1_Dat_tour.py`
1. Mở PowerShell tại thư mục dự án, tạo nhánh `feature/f1-dat-tour`:
   ```powershell
   git checkout main
   git pull origin main
   git checkout -b feature/f1-dat-tour
   ```
2. Mở VS Code, tạo/sửa file `tour_app/pages/1_Dat_tour.py` sử dụng đúng 6 câu SQL (`F1.1` đến `F1.6`) và hàm `luu_don()` dưới đây:

```python
from datetime import datetime, timedelta
import streamlit as st
from db import doc, dinh_dang_ngay, dinh_dang_tien, ghi, hien_tai, thong_bao_loi

# F1.1: Danh sach khach hang
SQL_KHACH_HANG = """
SELECT MaKH, CONCAT(MaKH, ' - ', HoTen) AS HienThi, DiaChi
FROM KhachHang
ORDER BY MaKH
"""

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
    cac_lenh = [(DAT_DON, tham_so, True), (TRU_CHO, tham_so, True)]
    if tham_so.get("GioDon"):
        cac_lenh.append((DON_TAI_NHA, tham_so, True))
    if tham_so.get("GioVeNoiNghi"):
        cac_lenh.append((VE_NOI_NGHI, tham_so, True))
    ghi(cac_lenh)
```

#### 4. Chạy Kiểm thử Nghiệm thu 8 Ca của `F1` (Bắt buộc thử đủ từng ca)
Trước khi kiểm thử, mở Workbench chạy lại `database/1_QuanLyDatTour_v3.sql`. Sau đó mở trang **Đặt tour** trên trình duyệt và thử lần lượt:
- **Ca 1 (Đặt đơn chuẩn có nơi nghỉ và 2 chuyến xe):**
  - Chọn khách `KH006 - Vũ Thị Hà`, lịch trình `LT10` (Hà Giang - Đồng Văn - Mã Pì Lèng 4N3Đ, đi `26/11/2026 20:00`), nhập `5` khách, chọn nơi nghỉ `NN08 - Homestay Cao Nguyên Đá`, nhập `2` phòng.
  - Tích chọn `"Cần xe đón tại nhà"`, địa chỉ đón mặc định `"3 Hùng Vương, Lào Cai"`, chọn ngày giờ đón `26/11/2026 15:00`.
  - Tích chọn `"Cần xe về nơi nghỉ"`, chọn ngày giờ về nơi nghỉ `27/11/2026 10:00`.
  - Kiểm tra tổng tiền dự kiến hiện đúng `32.020.000 đ` (Tiền tour `29.500.000 đ` + Tiền phòng `2.520.000 đ`).
  - Bấm `"Xác nhận đặt tour"` -> Hiện thông báo xanh `"Đã tạo đơn DH015, tổng tiền 32.020.000 đ"`.
  - Mở Workbench chạy 3 câu kiểm tra:
    ```sql
    SELECT MaDonHang, SoLuongKhach, SoPhong FROM DonHang WHERE MaDonHang = 'DH015';
    SELECT SoChoToiDa - SoChoDaDat AS ConLai FROM LichTrinh WHERE MaLichTrinh = 'LT10';
    SELECT MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon FROM ChuyenTrungChuyen WHERE MaDonHang = 'DH015';
    ```
    Kết quả phải ra: `DH015` (5 khách, 2 phòng), `LT10` còn `15` chỗ, và có đủ 2 chuyến trung chuyển.
- **Ca 2:** Chọn lịch trình `LT08` -> Ô Số khách chỉ cho tăng tối đa đến `10`.
- **Ca 3:** Chọn lịch trình `LT06` (Hà Nội - Tràng An - Bái Đính 1 ngày, `SoDem = 0`) -> Phần chọn Nơi nghỉ và Chuyến về nơi nghỉ tự động ẩn hoàn toàn.
- **Ca 4 (Lỗi số phòng > số khách):** Chọn `LT05`, nhập `2` khách, chọn nơi nghỉ `NN03`, nhập `3` phòng rồi bấm lưu -> Form chặn và báo lỗi `"Số phòng phải từ 1 đến số khách"`.
- **Ca 5 (Lỗi thiếu địa chỉ đón):** Tích `"Cần xe đón tại nhà"`, xóa trắng ô Địa chỉ đón rồi bấm lưu -> Form chặn và báo `"Vui lòng nhập địa chỉ đón"`.
- **Ca 6 (Lỗi giờ đón sai):** Tích `"Cần xe đón tại nhà"`, chọn giờ đón sau giờ xuất phát của lịch trình -> Form chặn và báo lỗi.
- **Ca 7:** Tạm tắt dịch vụ MySQL rồi bấm lưu -> Hiện thông báo tiếng Việt `"Không kết nối được cơ sở dữ liệu..."`, không văng traceback Python.
- **Ca 8 (Chứng minh Lớp 2 trong MySQL vẫn chặn khi Lớp 1 bị vượt qua):**
  - Mở code `1_Dat_tour.py`, tạm đổi `max_value` của ô Số khách thành `50`.
  - Trên trình duyệt, chọn `LT08` (chỉ còn 10 chỗ), nhập `11` khách rồi bấm `"Xác nhận đặt tour"`.
  - Kết quả phải hiện thông báo lỗi đỏ: `"Lịch trình không còn đủ chỗ cho số khách này"`, và trong bảng `DonHang` không có đơn mới nào được tạo.
  - Chụp màn hình lỗi này làm `screenshots/Hinh05b_F1_Loi.png`, sau đó **trả lại `max_value` trong code về đúng `SoChoConLai`**.

#### 5. Đẩy code `F1` lên GitHub
```powershell
git checkout feature/f1-dat-tour
git add tour_app/pages/1_Dat_tour.py
git commit -m "feat: hoan thien form dat tour F1 va kiem tra nghiem thu"
git push -u origin feature/f1-dat-tour
```
Sau khi chạy lệnh trên, mở trang GitHub của nhóm, bấm **Compare & pull request** -> **Create pull request** để Khánh gộp vào nhánh `main`.

---

### BƯỚC 3 (Tasks D4 & D5 - Hạn 13/11): Chụp Hình 4, 5a, 5b và Rà soát Báo cáo

#### 1. Chụp 3 ảnh của `F1` (Task `D4` - Ngày 11/11)
1. Mở Workbench chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc.
2. Mở trình duyệt ở tỷ lệ thu phóng `100%`, chiều rộng cửa sổ khoảng `1400 px`:
   - **`screenshots/Hinh04_F1_GiaoDien.png`:** Điền thông tin Ca 1 (`KH006`, `LT10`, `5` khách, `NN08`, `2` phòng, tích 2 chuyến xe), **chưa bấm nút Lưu**, chụp vùng giao diện đang hiện tổng tiền dự kiến `32.020.000 đ`.
   - **`screenshots/Hinh05a_F1_Loi.png`:** Làm Ca 4 (2 khách, 3 phòng) hoặc Ca 5 (để trống địa chỉ đón), nhấn `Win + Shift + S` chụp gọn vùng thông báo lỗi.
   - **`screenshots/Hinh05b_F1_Loi.png`:** Ảnh chụp thông báo lỗi `"Lịch trình không còn đủ chỗ cho số khách này"` khi thực hiện Ca 8 ở trên.

#### 2. Rà soát Báo cáo mục 2.3, 3.1, 3.2, 6.2 và Lập `docs/GopY_Dat.md` (Task `D5` - Ngày 12-13/11)
- Mở `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` (chỉ đọc, không sửa trực tiếp vào file Word), kiểm tra:
  - **Mục 2.3 (tr. 10):** Bảng giải thích ký hiệu ERD có khớp với hình `Hinh01_ERD.png` không.
  - **Mục 3.1 & 3.2 (tr. 11-12):** 4 quy tắc chuyển đổi ERD sang lược đồ quan hệ (Thực thể mạnh -> Bảng; Thuộc tính đa trị `SDT` -> Bảng `SDT_KhachHang`; Thực thể yếu `ChuyenTrungChuyen` -> Bảng có khóa chính `(MaDonHang, LoaiChuyen)`; Mối liên kết `1 - N` -> Khóa ngoại ở bảng bên `N`) và danh sách 12 lược đồ quan hệ (khóa chính gạch chân, khóa ngoại in nghiêng) có khớp 100% với tệp `1_QuanLyDatTour_v3.sql` không:
    1. `TinhThanh` (**MaTinh**, TenTinh)
    2. `TheThanhToan` (**SoID**, LoaiThe)
    3. `KhachHang` (**MaKH**, HoTen, Email, DiaChi, *SoID*)
    4. `SDT_KhachHang` (***MaKH***, **SoDienThoai**)
    5. `Tour` (**MaTour**, TenTour, MoTa, *MaTinhXuatPhat*, *MaTinhDen*)
    6. `LichTrinh` (**MaLichTrinh**, NgayXuatPhat, NgayKetThuc, DiemTapTrung, DiemTraKhach, GiaCoBan, SoChoToiDa, SoChoDaDat, *MaTour*)
    7. `NhaNghi` (**MaNhaNghi**, TenNhaNghi, LoaiHinh, DiaChi, SoDienThoai, GiaPhongMoiDem, *MaTinh*)
    8. `DonViVanTai` (**MaDVVT**, TenDonVi, SoDienThoai, DiaChi)
    9. `Xe` (**BienSo**, SoCho, *MaDVVT*)
    10. `TrangThaiDonHang` (**MaTrangThai**, TenTrangThai, ThuTu)
    11. `DonHang` (**MaDonHang**, NgayDat, SoLuongKhach, SoPhong, NgayHuy, LyDoHuy, DiemTour, NhanXetTour, DiemNhaNghi, NhanXetNhaNghi, NgayDanhGia, *MaTrangThai*, *MaKH*, *MaLichTrinh*, *MaNhaNghi*)
    12. `ChuyenTrungChuyen` (***MaDonHang***, **LoaiChuyen**, DiaChiDon, ThoiGianDon, *BienSoXe*)
  - **Mục 6.2 (tr. 23-26):** Bảng các trường của Form F1 và 2 khối câu lệnh SQL trong mục 6.2.2 có khớp với code `tour_app/pages/1_Dat_tour.py` không.
- Tạo file `docs/GopY_Dat.md` ghi lại mọi điểm cần sửa theo bảng: `| Trang | Mục | Đang ghi | Sửa thành | Lý do |`, kèm Họ tên đầy đủ và MSSV của bạn ở đầu file.
- Đẩy ảnh và file góp ý lên GitHub:
  ```powershell
  git checkout main
  git pull origin main
  git add screenshots/Hinh04_F1_GiaoDien.png screenshots/Hinh05a_F1_Loi.png screenshots/Hinh05b_F1_Loi.png docs/GopY_Dat.md
  git commit -m "docs: them hinh chup F1 (Hinh 4, 5a, 5b) va gop y bao cao cua Dat"
  git push origin main
  ```

---

### BƯỚC 4 (Tasks D6, D7, D8, D9 - Từ 14/11 đến 21/11): Kiểm thử Chéo, Đối chiếu Tên và Cài Máy Sạch

1. **Task `D6` (14/11 - Kiểm thử chéo `S1` và `R2` của Khánh):**
   - Chạy lại tệp SQL số 1, mở trang **Tìm kiếm (`S1`)**, thử lần lượt 6 ca ở mục 7.3 báo cáo (xem kết quả đúng tại `docs/Ke_hoach_Tong_hop_BTL_CSDL.md`).
   - Mở trang **Báo cáo doanh thu (`R2`)**, để kỳ `01/09/2026 - 31/12/2026`, kiểm tra dòng `TỔNG CỘNG` phải là `79.110.000 đ`, `10` đơn, `26` khách, `4` đơn hủy; thử xóa trống ô Người lập báo cáo xem nút tải file có bị ẩn không.
   - Nếu có lỗi, ghi rõ `"Thao tác -> Kết quả đúng -> Kết quả thực tế"` gửi cho Khánh.
2. **Task `D7` (16/11 - Đối chiếu tên bảng/cột):**
   - Kiểm tra chéo 4 nơi: `ERD.png`, `DataDiagram.png`, `Bao_cao_BTL_CSDL_QuanLyDatTour.docx` và `1_QuanLyDatTour_v3.sql` để chắc chắn không có lỗi gõ lệch chữ hoa/thường hay thiếu chữ (ví dụ: `DiaChi` không viết là `Diachi`, `SDT_KhachHang(MaKH, SoDienThoai)` thống nhất mọi nơi).
3. **Task `D8` (17/11 - Cài thử trên máy sạch):**
   - Mượn một laptop khác có MySQL 8.0, mở mục `PHỤ LỤC. HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY` trong báo cáo Word và làm đúng từng dòng lệnh mà không hỏi Khánh. Nếu bước nào người đọc dễ vướng thì báo Khánh bổ sung ngay vào Phụ lục. Giữ laptop này làm máy dự phòng mang đi hôm thuyết trình.

---

## Phần 4. Phần Thuyết trình và Câu hỏi Vấn đáp Bảo vệ của Đạt

### I. Nhiệm vụ trong 15 phút Bảo vệ
- **Từ phút `1:30` đến `4:30` (3 phút trình bày Slide 4 & Slide 5):**
  - Chỉ vào sơ đồ ERD trên Slide 4: giới thiệu hệ thống gồm **11 thực thể** và **12 mối liên kết** xoay quanh thực thể trung tâm là `DonHang`.
  - Chuyển sang Slide 5, giải thích ngắn gọn 4 điểm đặc biệt trên ERD:
    1. **Thực thể yếu `ChuyenTrungChuyen`** (chữ nhật viền đôi) và mối liên kết xác định `CoChuyen` (thoi viền đôi): mỗi chuyến xe trung chuyển phụ thuộc hoàn toàn vào đơn hàng, được phân biệt trong cùng một đơn bằng khóa bộ phận `LoaiChuyen` (`DON_TAI_NHA` hoặc `VE_NOI_NGHI`).
    2. **Thuộc tính đa trị `SDT`** (elip viền đôi của `KhachHang`): một khách hàng có thể lưu nhiều số điện thoại liên hệ.
    3. **4 thuộc tính dẫn xuất** (`SoDem`, `TongTien`, `TienPhat`, `TienHoan` — elip nét đứt): tính toán tự động từ dữ liệu gốc qua View `v_DonHang_ChiTiet`, không lưu cứng để tránh sai lệch dữ liệu.
    4. **2 thuộc tính phức hợp** (`DanhGiaTour`, `DanhGiaNhaNghi`): mỗi đánh giá gồm 2 thành phần con là Điểm (1-5) và Nhận xét.
- **Trong phần Demo (Bước 2 & Bước 3 — khoảng 1 phút 50 giây):** Khi Khánh điều khiển chuột trên màn hình `F1`, bạn thuyết minh thao tác đặt đơn `DH015` cho khách `KH006` (nơi nghỉ tự lọc theo tỉnh Tuyên Quang, tổng tiền `32.020.000 đ`, lưu trong 1 Transaction) và thuyết minh khi Khánh cố tình nhập sai `2` khách `3` phòng để chứng minh kiểm tra dữ liệu 2 lớp.

### II. 4 Câu hỏi Vấn đáp Trọng tâm Đạt Cần Thuộc Lòng

1. **Vì sao không lưu trực tiếp cột `TongTien`, `TienPhat`, `TienHoan` vào bảng `DonHang`?**
   - *Trả lời:* Vì đó là các thuộc tính dẫn xuất, hoàn toàn tính được từ `SoLuongKhach`, `GiaCoBan`, `SoPhong`, `GiaPhongMoiDem`, `NgayDat`, `NgayHuy` và `NgayXuatPhat`. Nếu lưu cứng thành cột trong bảng `DonHang` sẽ vi phạm dạng chuẩn 3NF (phụ thuộc bắc cầu) và có nguy cơ lệch số liệu khi cập nhật đơn. Nhóm tính các giá trị này trong view `v_DonHang_ChiTiet` nên lúc nào đọc ra cũng chính xác.
2. **Vì sao `ChuyenTrungChuyen` được thiết kế là thực thể yếu mà không phải thực thể mạnh có mã riêng?**
   - *Trả lời:* Một chuyến xe trung chuyển không tồn tại độc lập nếu không có đơn đặt tour, và mỗi đơn chỉ có tối đa 2 chuyến thuộc 2 loại cố định (`DON_TAI_NHA` và `VE_NOI_NGHI`). Do đó, dùng khóa của đơn hàng kết hợp với khóa bộ phận `LoaiChuyen` làm khóa chính `(MaDonHang, LoaiChuyen)` vừa phản ánh đúng bản chất thực thể yếu, vừa tự động chặn việc một đơn tạo trùng 2 chuyến đón tại nhà mà không cần thêm ràng buộc phụ.
3. **Thuộc tính đa trị `SDT` của `KhachHang` trên ERD khi chuyển sang mô hình quan hệ thì xử lý thế nào?**
   - *Trả lời:* Để thỏa mãn dạng chuẩn 1NF (mọi thuộc tính chỉ chứa giá trị nguyên tố), thuộc tính đa trị `SDT` được tách thành một bảng riêng là `SDT_KhachHang(MaKH, SoDienThoai)`, trong đó khóa chính là cặp `(MaKH, SoDienThoai)` và `MaKH` là khóa ngoại tham chiếu tới `KhachHang` với hành động `ON DELETE CASCADE`.
4. **Sơ đồ ERD khác sơ đồ Data Diagram ở điểm nào? Tại sao ERD có 11 thực thể, 12 mối liên kết nhưng Data Diagram lại có 12 bảng, 13 đường nối?**
   - *Trả lời:* ERD là mô hình mức khái niệm (biểu diễn thực thể, thuộc tính, mối liên kết bằng ký hiệu Chen), còn Data Diagram là mô hình mức logic/cài đặt trên MySQL (biểu diễn bảng, kiểu dữ liệu, khóa chính, khóa ngoại bằng ký hiệu chân gà). 11 thực thể trên ERD tạo thành 11 bảng, cộng thêm 1 bảng `SDT_KhachHang` sinh ra từ thuộc tính đa trị `SDT` nên tổng cộng có **12 bảng**. 12 mối liên kết `1 - N` trên ERD tạo thành 12 khóa ngoại, cộng thêm 1 khóa ngoại của bảng `SDT_KhachHang` trỏ về `KhachHang` nên tổng cộng có **13 đường nối khóa ngoại**.
