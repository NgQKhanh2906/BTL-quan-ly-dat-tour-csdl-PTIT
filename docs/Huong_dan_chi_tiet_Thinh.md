# HƯỚNG DẪN CÔNG VIỆC CHI TIẾT DÀNH RIÊNG CHO THỊNH (DATABASE NORMALIZATION, F3 & WORD REPORT EDITOR)

- **Họ và tên thành viên:** Nguyễn Tiến Thịnh (`B24DCCN546`)
- **Trạng thái hoàn thành (17/11/2026):** Đã hoàn thành `TH1` đến `TH8` (`3_Danh_gia.py`, `Hinh08_F3_GiaoDien.png`, `docs/GopY_Thinh.md`, tổng hợp góp ý và chèn đủ 13 hình + điền mã môn `INT1313` / Nhóm `14` vào `Bao_cao_BTL_CSDL_QuanLyDatTour.docx`). Còn lại: điền `[Họ tên giảng viên]` và `[Tên giáo trình...]`, cập nhật Mục lục (`Update Field`) và xuất `.pdf` bằng Microsoft Word (`TH9` - `TH10`). Lưu ý xem mục 2 của `docs/GopY_Thinh.md` về các chỗ sai lệch cột/hàm cũ bên dưới tài liệu này.
- **Vai trò trong nhóm:** Database Normalization Specialist, UI Developer (`F3`) & Chief Report Editor (Phụ trách kiểm chứng chuẩn hóa 3NF tại Chương 4, lập trình màn hình `F3 - Đánh giá sau chuyến đi`, và là **người duy nhất** biên tập trực tiếp file báo cáo Word `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` + xuất file `.pdf` hoàn chỉnh)
- **Phạm vi file được phép chỉnh sửa trực tiếp:**
  1. `tour_app/pages/3_Danh_gia.py`
  2. `screenshots/Hinh08_F3_GiaoDien.png`
  3. `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` và bản xuất `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.pdf`
- **Nguyên tắc quan trọng:** Tài liệu này đã bao gồm **100% bảng đối chiếu 11 thực thể, 12 bảng quan hệ, 32 quy tắc toàn vẹn (`RB01` - `RB32`), phân tích chuẩn hóa 3NF, câu lệnh SQL, mã nguồn Python và từng phím tắt trên Microsoft Word** dành cho bạn. Bạn chỉ cần làm đúng từ trên xuống dưới theo từng ngày mà không cần mở bất kỳ tài liệu cũ nào khác.

---

## MỤC LỤC

1. [Tổng quan lịch trình của Thịnh từ 05/11 đến 22/11/2026](#1-tổng-quan-lịch-trình-của-thịnh-từ-0511-đến-22112026)
2. [Chuẩn bị môi trường và quy trình Git dành riêng cho Thịnh](#2-chuẩn-bị-môi-trường-và-quy-trình-git-dành-riêng-cho-thịnh)
3. [Nhiệm vụ TH1 & TH2 (05/11 - 07/11): Quản lý báo cáo Word và Rà soát Mục 2.1, 3.3, 3.4](#3-nhiệm-vụ-th1--th2-0511---0711-quản-lý-báo-cáo-word-và-rà-soát-mục-21-33-34)
4. [Nhiệm vụ TH3 (08/11 - 09/11): Xây dựng màn hình F3 - Đánh giá sau chuyến đi](#4-nhiệm-vụ-th3-0811---0911-xây-dựng-màn-hình-f3---đánh-giá-sau-chuyến-đi)
5. [Nhiệm vụ TH4 (10/11): Kiểm chứng chuẩn hóa 3NF tại Chương 4](#5-nhiệm-vụ-th4-1011-kiểm-chứng-chuẩn-hóa-3nf-tại-chương-4)
6. [Nhiệm vụ TH5, TH6, TH7, TH8, TH9, TH10 (11/11 - 21/11): Chụp ảnh, Kiểm thử chéo và Hoàn thiện báo cáo Word/PDF](#6-nhiệm-vụ-th5-th6-th7-th8-th9-th10-1111---2111-chụp-ảnh-kiểm-thử-chéo-và-hoàn-thiện-báo-cáo-wordpdf)
7. [Kịch bản thuyết trình và Trả lời vấn đáp dành riêng cho Thịnh](#7-kịch-bản-thuyết-trình-và-trả-lời-vấn-đáp-dành-riêng-cho-thịnh)

---

## 1. TỔNG QUAN LỊCH TRÌNH CỦA THỊNH TỪ 05/11 ĐẾN 22/11/2026

| Mã việc | Ngày thực hiện | Tên công việc | Đầu ra bắt buộc (Deliverables) |
| :--- | :--- | :--- | :--- |
| **TH1** | 05/11 | Mở và kiểm tra định dạng chuẩn của file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` trên Microsoft Word | Đảm bảo khổ giấy A4, lề chuẩn, font Times New Roman 13pt |
| **TH2** | 06/11 - 07/11 | Đối chiếu Mục 2.1 (11 thực thể), Mục 3.3 (Từ điển dữ liệu 12 bảng) và Mục 3.4 (32 ràng buộc `RB01` - `RB32`) với file `1_QuanLyDatTour_v3.sql` | Cập nhật số liệu 12 bảng, 13 `FK`, 56 ràng buộc khai báo vào file Word |
| **TH3** | 08/11 - 09/11 | Lập trình màn hình `F3 - Đánh giá sau chuyến đi` (`tour_app/pages/3_Danh_gia.py`) | Code chạy qua 6 ca kiểm thử, tạo Pull Request `feature/f3-danh-gia` |
| **TH4** | 10/11 | Rà soát Chương 4 (Chuẩn hóa lược đồ CSDL 1NF -> 2NF -> 3NF) và chạy thử SQL chứng minh trên MySQL | Chương 4 khớp 100% với Phương án A (12 bảng đều đạt chuẩn 3NF) |
| **TH5** | 11/11 - 12/11 | Chụp ảnh giao diện `screenshots/Hinh08_F3_GiaoDien.png` | File `Hinh08_F3_GiaoDien.png` đẩy lên Git |
| **TH6** | 14/11 | Kiểm thử chéo màn hình `F1 - Đặt tour mới` của Đạt theo 6 kịch bản | Báo cáo kết quả kiểm thử `F1` cho Đạt |
| **TH7** | 15/11 | Tổng hợp góp ý từ 3 file `GopY_Dat.md`, `GopY_Tuan.md`, `GopY_Khanh.md` và cập nhật vào báo cáo Word | Nội dung văn bản các chương từ 1 đến 9 hoàn chỉnh |
| **TH8** | 16/11 - 18/11 | Chèn 13 hình ảnh chuẩn vào báo cáo Word (không mất đầu ảnh) và điền/xóa sạch toàn bộ nền vàng (`Highlight`) | Bản báo cáo nháp `v0.9` không còn bất kỳ dấu `[CẦN BỔ SUNG]` nào |
| **TH9** | 19/11 | Cập nhật tự động Mục lục (`Update Field`) và gửi bản `v0.9` cho cả nhóm đọc soát | File Word cập nhật số trang chính xác (`<= 50 trang`) |
| **TH10** | 21/11 | Sửa các lỗi nhỏ cuối cùng (nếu có) và xuất file `Bao_cao_BTL_CSDL_QuanLyDatTour.pdf` có Bookmarks | File `.docx` và `.pdf` bản `v1.0` chính thức để nộp bài |

---

## 2. CHUẨN BỊ MÔI TRƯỜNG VÀ QUY TRÌNH GIT DÀNH RIÊNG CHO THỊNH

### 2.1. Tại sao chỉ một mình Thịnh được sửa trực tiếp file `.docx`?

- File Microsoft Word (`.docx`) là một file nhị phân nén (`binary archive`). Khác với file code `.py` hay `.sql`, Git **không thể tự động trộn (merge)** 2 phiên bản `.docx` nếu 2 người cùng sửa một lúc — người đẩy lên sau sẽ ghi đè làm mất toàn bộ công sức của người đẩy lên trước.
- Vì vậy, nhóm áp dụng quy tắc **Single-Editor**: Khánh, Đạt, Tuân chỉ đọc file `.docx` và ghi nhận xét vào `docs/GopY_*.md`; **duy nhất Thịnh** là người mở file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`, chỉnh sửa và đẩy lên Git.

### 2.2. Các bước cài đặt môi trường lần đầu tiên (Ngày 05/11/2026)

- **Bước 1:** Mở **Windows PowerShell**, tải kho mã nguồn của nhóm về máy:
  ```powershell
  cd D:\
  git clone https://github.com/NgQKhanh2906/BTL-quan-ly-dat-tour-csdl-PTIT.git
  cd BTL-quan-ly-dat-tour-csdl-PTIT
  ```
- **Bước 2:** Sau khi Khánh báo đã đẩy bộ khung dự án lên `main` (tối ngày 06/11), bạn kéo code mới nhất về và tạo môi trường ảo Python:
  ```powershell
  git checkout main
  git pull origin main
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
  - *Lưu ý:* Nếu PowerShell báo lỗi đỏ `running scripts is disabled on this system`, hãy chạy lệnh sau rồi chạy lại lệnh `Activate.ps1`:
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
- **Bước 3:** Cài đặt thư viện và lưu mật khẩu MySQL vào biến môi trường:
  ```powershell
  pip install -r tour_app/requirements.txt
  setx MYSQL_PASSWORD "mat_khau_mysql_cua_ban"
  ```
  - Đóng cửa sổ PowerShell lại, mở một cửa sổ PowerShell mới để biến `MYSQL_PASSWORD` có hiệu lực:
    ```powershell
    cd D:\BTL-quan-ly-dat-tour-csdl-PTIT
    .\.venv\Scripts\Activate.ps1
    ```
- **Bước 4:** Mở **MySQL Workbench**, nhấn `Ctrl + Shift + O`, chọn file `database/1_QuanLyDatTour_v3.sql` và nhấn biểu tượng **Tia sét** (`Ctrl + Shift + Enter`) để khởi tạo CSDL `QuanLyDatTour` (12 bảng, 104 dòng dữ liệu mẫu).

### 2.3. Quy trình Git dành cho Thịnh

1. **Khi lập trình màn hình `F3` (Ngày 08/11 - 09/11):**
   ```powershell
   git checkout main
   git pull origin main
   git checkout -b feature/f3-danh-gia
   ```
   Sau khi code và test xong `tour_app/pages/3_Danh_gia.py`:
   ```powershell
   git status
   git add tour_app/pages/3_Danh_gia.py
   git commit -m "feat(f3): hoan thien man hinh danh gia sau chuyen di"
   git push -u origin feature/f3-danh-gia
   ```
   Lên GitHub tạo **Pull Request** vào nhánh `main` và nhắn Khánh duyệt.
2. **Khi cập nhật báo cáo Word (Từ 07/11 đến 21/11):**
   - Trước khi mở file Word để sửa, **luôn luôn** kéo bản mới nhất từ `main` về:
     ```powershell
     git checkout main
     git pull origin main
     ```
   - Sửa xong trên Microsoft Word, nhấn `Ctrl + S` và **đóng hẳn phần mềm Word** (để Word xóa file tạm `~$Bao_cao...`), sau đó đẩy lên Git:
     ```powershell
     git add docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx
     git commit -m "docs(report): cap nhat noi dung bao cao BTL"
     git push origin main
     ```

---

## 3. NHIỆM VỤ TH1 & TH2 (05/11 - 07/11): QUẢN LÝ BÁO CÁO WORD VÀ RÀ SOÁT MỤC 2.1, 3.3, 3.4

### 3.1. Nhiệm vụ TH1 (05/11): Kiểm tra thông số định dạng chuẩn của file Word

Mở file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` bằng Microsoft Word và kiểm tra các thông số định dạng (không tự ý đổi sang font khác):
- **Khổ giấy:** `A4` (`21 cm x 29,7 cm`).
- **Căn lề (Margins):** Trên (`Top`) `2 cm`, Dưới (`Bottom`) `2 cm`, Phải (`Right`) `2 cm`, Trái (`Left`) `3 cm` (chừa lề đóng gáy).
- **Font chữ nội dung (`Normal`):** `Times New Roman`, cỡ chữ `13 pt`, giãn dòng `1,4 lines`, căn đều 2 bên (`Justify`).
- **Font chữ khối lệnh SQL / Code:** `Consolas`, cỡ chữ `10 pt` - `10.5 pt`, nền xám nhạt, tuyệt đối không căn đều 2 bên (`Left align`).

### 3.2. Nhiệm vụ TH2 (06/11 - 07/11): Đối chiếu Mục 2.1, Mục 3.3 và Mục 3.4 với `database/1_QuanLyDatTour_v3.sql`

#### A. Bảng chuẩn 11 thực thể và thuộc tính (Đối chiếu với Mục 2.1 trong báo cáo Word)

Đảm bảo Mục 2.1 trong báo cáo mô tả đầy đủ **11 thực thể** (bao gồm thực thể thứ 11 là `TheThanhToan` đã tách ra theo Phương án A):

| STT | Tên thực thể | Loại thực thể | Khóa chính / Khóa bộ phận | Danh sách thuộc tính trên ERD |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `TinhThanh` | Thực thể mạnh | `MaTinh` | `MaTinh`, `TenTinh` (duy nhất) |
| 2 | `TheThanhToan` | Thực thể mạnh | `SoID` | `SoID` (16 chữ số thẻ), `LoaiThe` (`Visa`, `MasterCard`, `JCB`, `Napas`) |
| 3 | `KhachHang` | Thực thể mạnh | `MaKH` | `MaKH`, `HoTen`, `DiaChi`, `Email` (duy nhất), `SDT` (**thuộc tính đa trị** — hình elip nét đôi) |
| 4 | `Tour` | Thực thể mạnh | `MaTour` | `MaTour`, `TenTour`, `MoTa`, `SoNgay`, `GiaCoBan` |
| 5 | `LichTrinh` | Thực thể mạnh | `MaLichTrinh` | `MaLichTrinh`, `NgayKhoiHanh`, `NgayKetThuc`, `SoChoToiDa`, `SoChoDaDat` |
| 6 | `NhaNghi` | Thực thể mạnh | `MaNhaNghi` | `MaNhaNghi`, `TenNhaNghi`, `DiaChi`, `SucChuaPhong`, `GiaPhongMoiDem` |
| 7 | `DonViVanTai` | Thực thể mạnh | `MaDonVi` | `MaDonVi`, `TenDonVi`, `DiaChi`, `SoDienThoai`, `Email` (duy nhất) |
| 8 | `Xe` | Thực thể mạnh | `MaXe` | `MaXe`, `BienSoXe` (duy nhất), `LoaiXe`, `SoChoNgoi` |
| 9 | `TrangThaiDonHang` | Thực thể mạnh | `MaTrangThai` | `MaTrangThai` (`DAT`, `THANHTOAN`, `HOANTHANH`, `HUY`), `TenTrangThai`, `MoTa` |
| 10 | `DonHang` | Thực thể mạnh | `MaDonHang` | `MaDonHang`, `NgayDat`, `SoLuongKhach`, `SoPhong`, `/TongTien/` (**thuộc tính dẫn xuất** — elip nét đứt), `ThongTinHuy(NgayHuy, LyDoHuy, PhiPhatHuy)` (**phức hợp**), `DanhGiaTour(DiemDanhGiaTour, NhanXetTour, NgayDanhGia)` (**phức hợp**), `DanhGiaNhaNghi(DiemDanhGiaNhaNghi, NhanXetNhaNghi)` (**phức hợp**) |
| 11 | `ChuyenTrungChuyen` | **Thực thể yếu** (hình chữ nhật nét đôi, phụ thuộc `DonHang` qua `CoChuyen`) | `SoThuTuChuyen` (**khóa bộ phận** — gạch chân nét đứt) | `SoThuTuChuyen` (`1` = lượt đón, `2` = lượt trả), `DiemDon`, `DiemTra` |

#### B. Bảng tổng hợp 12 bảng quan hệ và 56 ràng buộc khai báo (Đối chiếu với Mục 3.1, 3.2, 3.3)

Kiểm tra trong Mục 3.1, 3.2 và 3.3 của báo cáo Word xem bảng thống kê đã khớp chính xác các con số sau chưa:

| STT | Tên bảng quan hệ | Khóa chính (`PK`) | Số khóa ngoại (`FK`) | Số ràng buộc `UNIQUE` | Số ràng buộc `CHECK` | Số dòng dữ liệu mẫu |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| 1 | `TinhThanh` | `MaTinh` | 0 | 1 (`uq_TinhThanh_TenTinh`) | 1 (`chk_TinhThanh_KhongRong`) | 8 |
| 2 | `TheThanhToan` | `SoID` | 0 | 0 | 2 (`chk_TheThanhToan_SoID`, `chk_TheThanhToan_LoaiThe`) | 5 |
| 3 | `KhachHang` | `MaKH` | 1 (`fk_KH_TheThanhToan`) | 1 (`uq_KhachHang_Email`) | 2 (`chk_KH_KhongRong`, `chk_KH_Email`) | 8 |
| 4 | `SDT_KhachHang` | `(MaKH, SoDienThoai)` | 1 (`fk_SDT_KhachHang`) | 0 | 1 (`chk_SDT_DinhDang`) | 12 |
| 5 | `Tour` | `MaTour` | 2 (`fk_Tour_TinhXP`, `fk_Tour_TinhDen`) | 0 | 4 (`chk_Tour_KhongRong`, `chk_Tour_SoNgay`, `chk_Tour_GiaCoBan`, `chk_Tour_TinhKhacNhau`) | 6 |
| 6 | `LichTrinh` | `MaLichTrinh` | 1 (`fk_LT_Tour`) | 0 | 3 (`chk_LT_KhongRong`, `chk_LT_Ngay`, `chk_LT_SoCho`) | 12 |
| 7 | `NhaNghi` | `MaNhaNghi` | 1 (`fk_NN_TinhThanh`) | 0 | 3 (`chk_NN_KhongRong`, `chk_NN_SucChua`, `chk_NN_GiaPhong`) | 7 |
| 8 | `DonViVanTai` | `MaDonVi` | 0 | 1 (`uq_DVVT_Email`) | 3 (`chk_DVVT_KhongRong`, `chk_DVVT_SDT`, `chk_DVVT_Email`) | 3 |
| 9 | `Xe` | `MaXe` | 1 (`fk_Xe_DonViVanTai`) | 1 (`uq_Xe_BienSo`) | 2 (`chk_Xe_KhongRong`, `chk_Xe_SoChoNgoi`) | 7 |
| 10 | `TrangThaiDonHang` | `MaTrangThai` | 0 | 0 | 1 (`chk_TTDH_Ma`) | 4 |
| 11 | `DonHang` | `MaDonHang` | 4 (`fk_DonHang_KH`, `fk_DonHang_LT`, `fk_DonHang_NN`, `fk_DonHang_TrangThai`) | 0 | 8 (`chk_DonHang_MaKhongRong`, `chk_DonHang_SoKhach`, `chk_DonHang_PhongNhaNghi`, `chk_DonHang_Huy`, `chk_DonHang_DanhGia`, `chk_DonHang_DiemTour`, `chk_DonHang_DiemNN`, `chk_DonHang_NhanXet`) | 13 |
| 12 | `ChuyenTrungChuyen` | `(MaDonHang, SoThuTuChuyen)` | 2 (`fk_CTC_DonHang`, `fk_CTC_Xe`) | 0 | 2 (`chk_CTC_ThuTu`, `chk_CTC_DiemDonTra`) | 19 |
| **TỔNG** | **12 bảng** | **12 `PK`** | **13 `FK`** | **4 `UNIQUE`** | **27 `CHECK`** | **104 dòng** |

- **Tổng số ràng buộc khai báo trong DDL:** `12 PK + 13 FK + 27 CHECK + 4 UNIQUE = 56 ràng buộc`.

#### C. Bảng đối chiếu 32 quy tắc toàn vẹn `RB01` - `RB32` (Đối chiếu với Mục 3.4 trong báo cáo Word)

Kiểm tra Mục 3.4 đảm bảo 32 quy tắc toàn vẹn được phân thành 5 nhóm rõ ràng (trong đó `RB06` được cài đặt bằng bảng `TheThanhToan` và khóa ngoại `fk_KH_TheThanhToan`):

1. **Nhóm 1 — Ràng buộc miền giá trị & Định dạng (`RB01` - `RB13`, cài đặt bằng `CHECK` trong DDL):**
   - `RB01`: Mã định danh và tên bắt buộc ở các bảng danh mục không được rỗng sau khi cắt khoảng trắng (`TRIM(...) <> ''`).
   - `RB02`: `Tour.SoNgay >= 1` (`chk_Tour_SoNgay`).
   - `RB03`: `Tour.GiaCoBan > 0` (`chk_Tour_GiaCoBan`).
   - `RB04`: `NhaNghi.SucChuaPhong >= 1` và `GiaPhongMoiDem > 0` (`chk_NN_SucChua`, `chk_NN_GiaPhong`).
   - `RB05`: `Xe.SoChoNgoi` nằm trong khoảng `4..60` (`chk_Xe_SoChoNgoi`).
   - `RB06`: `TheThanhToan.SoID` đúng 16 chữ số (`REGEXP '^[0-9]{16}$'`), `LoaiThe` thuộc `('Visa', 'MasterCard', 'JCB', 'Napas')`, và `KhachHang.SoID` tham chiếu qua `fk_KH_TheThanhToan`.
   - `RB07`: `KhachHang.Email` và `DonViVanTai.Email` đúng định dạng thư điện tử (`chk_KH_Email`, `chk_DVVT_Email`).
   - `RB08`: `SDT_KhachHang.SoDienThoai` và `DonViVanTai.SoDienThoai` gồm 10 - 11 chữ số bắt đầu bằng `0` (`REGEXP '^0[0-9]{9,10}$'`).
   - `RB09`: `TrangThaiDonHang.MaTrangThai` chỉ nhận 1 trong 4 giá trị `('DAT', 'THANHTOAN', 'HOANTHANH', 'HUY')`.
   - `RB10`: `DonHang.SoLuongKhach >= 1` (`chk_DonHang_SoKhach`).
   - `RB11`: `DonHang.DiemDanhGiaTour` và `DiemDanhGiaNhaNghi` (khi khác `NULL`) nằm trong khoảng `1..5` (`chk_DonHang_DiemTour`, `chk_DonHang_DiemNN`).
   - `RB12`: `DonHang.NhanXetTour` và `NhanXetNhaNghi` nếu có nhập thì không được chỉ chứa khoảng trắng (`chk_DonHang_NhanXet`).
   - `RB13`: `ChuyenTrungChuyen.SoThuTuChuyen >= 1` (`chk_CTC_ThuTu`).
2. **Nhóm 2 — Ràng buộc liên thuộc tính trên cùng một bảng (`RB14` - `RB20`, cài đặt bằng `CHECK` cấp bảng):**
   - `RB14`: `Tour.MaTinhXuatPhat <> Tour.MaTinhDen` (`chk_Tour_TinhKhacNhau`).
   - `RB15`: `LichTrinh.NgayKetThuc >= LichTrinh.NgayKhoiHanh` (`chk_LT_Ngay`).
   - `RB16`: `0 <= LichTrinh.SoChoDaDat <= LichTrinh.SoChoToiDa` (`chk_LT_SoCho`).
   - `RB17`: Trong `DonHang`, nếu `MaNhaNghi IS NULL` thì `SoPhong = 0`; nếu `MaNhaNghi IS NOT NULL` thì `SoPhong >= 1` (`chk_DonHang_PhongNhaNghi`).
   - `RB18`: Trong `DonHang`, nếu `MaTrangThai = 'HUY'` thì `NgayHuy`, `LyDoHuy` (khác rỗng), `PhiPhatHuy >= 0` đều phải `NOT NULL` và `NgayHuy >= NgayDat`; ngược lại nếu `MaTrangThai <> 'HUY'` thì cả 3 cột phải là `NULL` (`chk_DonHang_Huy`).
   - `RB19`: Trong `DonHang`, chỉ khi `MaTrangThai = 'HOANTHANH'` mới được phép có dữ liệu đánh giá (`NgayDanhGia >= NgayDat` và `DiemDanhGiaTour IS NOT NULL`); nếu có đánh giá nhà nghỉ thì đơn đó phải có đặt nhà nghỉ (`MaNhaNghi IS NOT NULL`) (`chk_DonHang_DanhGia`).
   - `RB20`: Trong `ChuyenTrungChuyen`, `DiemDon` và `DiemTra` không rỗng và `TRIM(DiemDon) <> TRIM(DiemTra)` (`chk_CTC_DiemDonTra`).
3. **Nhóm 3 — Ràng buộc khóa chính & Duy nhất (`RB21` - `RB22`, cài đặt bằng `PRIMARY KEY` và `UNIQUE`):**
   - `RB21`: Khóa chính của cả 12 bảng là duy nhất và khác `NULL` (`12 PRIMARY KEY`).
   - `RB22`: Tên tỉnh thành, Email khách hàng, Email đơn vị vận tải và Biển số xe là duy nhất (`4 UNIQUE`).
4. **Nhóm 4 — Ràng buộc tham chiếu khóa ngoại (`RB23`, cài đặt bằng `13 FOREIGN KEY`):**
   - `RB23`: Toàn bộ 13 khóa ngoại đảm bảo tính toàn vẹn tham chiếu; riêng `SDT_KhachHang.MaKH` và `ChuyenTrungChuyen.MaDonHang` dùng `ON DELETE CASCADE` (vì là thuộc tính đa trị và thực thể yếu phụ thuộc tồn tại), các khóa ngoại còn lại dùng `ON DELETE RESTRICT` để bảo vệ lịch sử giao dịch.
5. **Nhóm 5 — Ràng buộc liên bảng & Nghiệp vụ xử lý tại tầng ứng dụng + `Transaction` (`RB24` - `RB32`):**
   - `RB24`: Khoảng ngày của `LichTrinh` phải khớp với `Tour.SoNgay`: `DATEDIFF(NgayKetThuc, NgayKhoiHanh) + 1 = Tour.SoNgay`.
   - `RB25`: Nếu `DonHang` có chọn `MaNhaNghi`, nhà nghỉ đó phải nằm tại tỉnh điểm đến của tour (`NhaNghi.MaTinh = Tour.MaTinhDen`) và `SoPhong <= NhaNghi.SucChuaPhong`.
   - `RB26`: Đơn hàng ở trạng thái `'HUY'` không được giữ các dòng xe trung chuyển trong `ChuyenTrungChuyen` (khi hủy đơn phải xóa chuyến trung chuyển trong cùng `Transaction`).
   - `RB27`: Xe trung chuyển được gán cho đơn hàng phải có sức chứa đủ cho đoàn khách (`Xe.SoChoNgoi >= DonHang.SoLuongKhach`).
   - `RB28`: Tổng `SoLuongKhach` của các đơn hàng chưa hủy (`MaTrangThai <> 'HUY'`) thuộc cùng một `MaLichTrinh` phải luôn bằng `LichTrinh.SoChoDaDat` và không vượt quá `SoChoToiDa`.
   - `RB29`: Phí phạt hủy tour (`PhiPhatHuy`) phải tính đúng theo 5 bậc thời gian (`0%`, `10%`, `30%`, `50%`, `100%`).
   - `RB30`: Luồng chuyển trạng thái đơn hàng một chiều (`DAT -> THANHTOAN -> HOANTHANH` hoặc `DAT/THANHTOAN -> HUY`).
   - `RB31`: Công thức tính tổng tiền đơn hàng `TongTien = SoLuongKhach * GiaCoBan + SoPhong * GiaPhongMoiDem * DATEDIFF(NgayKetThuc, NgayKhoiHanh)` (cài đặt qua View `v_DonHang_ChiTiet`).
   - `RB32`: Mỗi đơn hàng hoàn thành (`HOANTHANH`) chỉ được gửi đánh giá đúng 1 lần (`WHERE MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL`).

---

## 4. NHIỆM VỤ TH3 (08/11 - 09/11): XÂY DỰNG MÀN HÌNH F3 - ĐÁNH GIÁ SAU CHUYẾN ĐI

### 4.1. Tại sao màn hình F3 lại được thiết kế như vậy? (Giải thích lý do kỹ thuật)

1. **Tại sao thông tin đánh giá lại lưu ngay trong bảng `DonHang` mà không tách ra bảng `DanhGia` riêng?**
   - Theo mô hình ERD ở Chương 2, mỗi đơn đặt tour sau khi hoàn thành (`HOANTHANH`) chỉ có **tối đa 1 lượt đánh giá duy nhất** (quan hệ `1 : 1` với đơn hàng). Vì vậy, hai thuộc tính phức hợp `DanhGiaTour(DiemDanhGiaTour, NhanXetTour, NgayDanhGia)` và `DanhGiaNhaNghi(DiemDanhGiaNhaNghi, NhanXetNhaNghi)` được làm phẳng (flatten) trực tiếp thành 5 cột trong bảng `DonHang`. Thiết kế này vừa đạt chuẩn **3NF** (vì mọi cột đánh giá đều phụ thuộc hàm trực tiếp vào khóa chính `MaDonHang`), vừa tránh phải `JOIN` thêm bảng phụ khi thống kê điểm trung bình.
2. **Tại sao khi người dùng không nhập nhận xét bằng chữ, code Python phải truyền giá trị `None` (tức `NULL` trong SQL) thay vì chuỗi rỗng `""`?**
   - Trong bảng `DonHang`, ràng buộc `chk_DonHang_NhanXet` quy định:
     `CHECK ((NhanXetTour IS NULL OR TRIM(NhanXetTour) <> '') AND (NhanXetNhaNghi IS NULL OR TRIM(NhanXetNhaNghi) <> ''))`
   - Nghĩa là: khách hàng **có quyền không viết nhận xét chữ** (khi đó cột phải là `NULL`), nhưng nếu đã lưu chuỗi ký tự vào cột thì chuỗi đó không được rỗng hoặc toàn dấu cách. Do đó trong Python, biểu thức `nhan_xet_tour.strip() or None` sẽ tự động biến chuỗi rỗng `""` thành `None` (`NULL`), giúp câu lệnh `UPDATE` chạy qua `chk_DonHang_NhanXet` êm ái.
3. **Tại sao câu lệnh `UPDATE` đánh giá phải có điều kiện `WHERE MaDonHang = %s AND MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL` kèm `phai_co_dong=True`?**
   - Để đảm bảo quy tắc `RB32` (mỗi chuyến đi chỉ được đánh giá đúng 1 lần). Nếu khách hàng mở 2 tab trình duyệt cùng bấm gửi đánh giá cho đơn `DH004`, tab thứ nhất cập nhật `NgayDanhGia = '2026-10-23 08:00:00'` thành công; tab thứ hai chạy sau sẽ thấy `NgayDanhGia IS NULL` không còn đúng nữa (`rowcount == 0`), hệ thống lập tức chặn lại và báo đơn đã được đánh giá rồi!

### 4.2. Bảng thiết kế 6 trường và kiểm tra hợp lệ 2 tầng của màn hình F3

| STT | Nhãn hiển thị trên giao diện | Loại điều khiển Streamlit | Kiểm tra hợp lệ tại Tầng 1 (Giao diện Python) | Ràng buộc tương ứng tại Tầng 2 (MySQL) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Khách hàng** | `st.selectbox` | Chọn từ danh sách khách hàng trong bảng `KhachHang` | `FK` `fk_DonHang_KH` |
| 2 | **Chuyến đi hoàn thành chưa đánh giá** | `st.selectbox` | Chỉ nạp các đơn của khách đó có `MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL` | `chk_DonHang_DanhGia` & `RB32` |
| 3 | **Điểm đánh giá tour (*)** | `st.slider` | Số nguyên từ `1` đến `5` sao (mặc định `5`) | `chk_DonHang_DiemTour` (`BETWEEN 1 AND 5`) |
| 4 | **Nhận xét về chuyến tour** | `st.text_area` | Tối đa `500` ký tự; nếu để trống hoặc toàn khoảng trắng thì chuyển thành `None` (`NULL`) | `chk_DonHang_NhanXet` |
| 5 | **Điểm đánh giá nhà nghỉ** *(Chỉ bật khi đơn có `MaNhaNghi IS NOT NULL`)* | `st.checkbox` + `st.slider` | Số nguyên từ `1` đến `5` sao; nếu đơn không đặt nhà nghỉ thì tự động khóa và gán `None` | `chk_DonHang_DanhGia` & `chk_DonHang_DiemNN` |
| 6 | **Nhận xét về nhà nghỉ** *(Chỉ bật khi đơn có `MaNhaNghi IS NOT NULL`)* | `st.text_area` | Tối đa `500` ký tự; nếu nhập nhận xét nhà nghỉ mà chưa tích chọn chấm điểm sao nhà nghỉ thì báo lỗi | `chk_DonHang_DanhGia` & `chk_DonHang_NhanXet` |

### 4.3. Toàn bộ 2 câu lệnh SQL chuẩn của màn hình F3 (`F3.1` và `F3.2`)

1. **`F3.1` — Nạp danh sách các đơn hàng đã hoàn thành nhưng chưa đánh giá của khách hàng đang chọn:**
   ```sql
   SELECT dh.MaDonHang, t.MaTour, t.TenTour,
          lt.NgayKhoiHanh, lt.NgayKetThuc,
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
   ORDER BY lt.NgayKetThuc DESC;
   ```
2. **`F3.2` — Giao dịch ghi nhận đánh giá chuyến đi (Chỉ cập nhật đúng 1 lần khi `NgayDanhGia IS NULL`):**
   ```sql
   UPDATE DonHang
   SET DiemDanhGiaTour    = %s,
       NhanXetTour        = %s,
       NgayDanhGia        = %s,
       DiemDanhGiaNhaNghi = %s,
       NhanXetNhaNghi     = %s
   WHERE MaDonHang = %s
     AND MaTrangThai = 'HOANTHANH'
     AND NgayDanhGia IS NULL;
   ```

### 4.4. Toàn bộ mã nguồn file `tour_app/pages/3_Danh_gia.py`

Bạn mở VS Code, tạo/mở file `tour_app/pages/3_Danh_gia.py` và viết đầy đủ đoạn mã sau:

```python
import streamlit as st
from db import doc_sql, chay_giao_dich, dinh_dang_tien, lay_hien_tai

st.set_page_config(page_title="F3 - Đánh giá sau chuyến đi", layout="wide")
st.title("F3. Đánh giá chất lượng tour và nhà nghỉ sau chuyến đi")
st.caption(
    "Chỉ những đơn hàng ở trạng thái Hoàn thành (HOANTHANH) và chưa từng đánh giá "
    "mới được phép gửi điểm và nhận xét."
)

ds_kh = doc_sql("SELECT MaKH, HoTen, Email FROM KhachHang ORDER BY MaKH")
chon_kh = st.selectbox(
    "1. Chọn khách hàng",
    ds_kh.to_dict("records"),
    format_func=lambda r: f"{r['MaKH']} - {r['HoTen']} ({r['Email']})",
)

# F3.1: Nap danh sach cac don HOANTHANH chua danh gia cua khach hang
ds_don_ht = doc_sql(
    """
    SELECT dh.MaDonHang, t.MaTour, t.TenTour,
           lt.NgayKhoiHanh, lt.NgayKetThuc,
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

if ds_don_ht.empty:
    st.info(
        f"Khách hàng **{chon_kh['HoTen']}** (`{chon_kh['MaKH']}`) hiện không có chuyến đi nào "
        f"ở trạng thái Hoàn thành đang chờ đánh giá (hoặc tất cả các chuyến hoàn thành đã được đánh giá)."
    )
    st.stop()

chon_don = st.selectbox(
    "2. Chọn chuyến đi đã hoàn thành cần đánh giá",
    ds_don_ht.to_dict("records"),
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['TenTour']} "
        f"({r['NgayKhoiHanh']} -> {r['NgayKetThuc']}) | {dinh_dang_tien(r['TongTien'])}"
    ),
)

st.info(
    f"**Mã đơn:** `{chon_don['MaDonHang']}` | **Tour:** {chon_don['TenTour']} (`{chon_don['MaTour']}`)  \n"
    f"**Hành trình:** {chon_don['NgayKhoiHanh']} đến {chon_don['NgayKetThuc']} | "
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
        ngay_dg_str = lay_hien_tai().strftime("%Y-%m-%d %H:%M:%S")
        # F3.2: Cap nhat danh gia vao bang DonHang
        ds_lenh = [
            (
                """
                UPDATE DonHang
                SET DiemDanhGiaTour    = %s,
                    NhanXetTour        = %s,
                    NgayDanhGia        = %s,
                    DiemDanhGiaNhaNghi = %s,
                    NhanXetNhaNghi     = %s
                WHERE MaDonHang = %s
                  AND MaTrangThai = 'HOANTHANH'
                  AND NgayDanhGia IS NULL
                """,
                (
                    int(diem_tour),
                    nx_tour_val,
                    ngay_dg_str,
                    int(diem_nn) if diem_nn is not None else None,
                    nx_nn_val,
                    chon_don["MaDonHang"],
                ),
                True,
            )
        ]
        ok, tb = chay_giao_dich(ds_lenh)
        if ok:
            st.success(
                f"Đã ghi nhận đánh giá cho đơn `{chon_don['MaDonHang']}` "
                f"(Điểm tour: {diem_tour}/5 sao"
                f"{f', Điểm nhà nghỉ: {diem_nn}/5 sao' if diem_nn else ''}) "
                f"vào lúc {ngay_dg_str}!"
            )
        else:
            st.error(tb)
```

### 4.5. Hướng dẫn tự chạy 6 ca kiểm thử nghiệm thu màn hình F3

Mở PowerShell chạy ứng dụng (`streamlit run app.py`), bấm vào mục **3_Danh_gia** ở thanh bên trái và thực hiện **6 ca kiểm thử** sau:

| Ca kiểm thử | Thao tác thực hiện trên giao diện | Kết quả mong đợi (Pass Criteria) |
| :---: | :--- | :--- |
| **Ca 1 (Đánh giá hợp lệ - Hợp đồng giao diện với màn hình `S1` của Khánh)** | Chọn khách hàng `KH004 - Phạm Thị Dung`. Hệ thống nạp đơn `DH004` (Tour `T002 - Khám phá Sa Pa`, nhà nghỉ `NN03 - Sapa Mountain View`). Chọn Điểm đánh giá tour = **4 sao**, nhập nhận xét `"Lịch trình hợp lý, hướng dẫn viên nhiệt tình."`. Chọn Điểm nhà nghỉ = **4 sao**, nhập nhận xét `"Phòng ấm áp, view núi đẹp."`. Bấm **Gửi đánh giá chuyến đi**. | 1. Hiện thông báo thành công màu xanh vào lúc `2026-10-23 08:00:00`.<br>2. Chuyển sang màn hình **4_Tim_kiem_tour (`S1`)**, gõ từ khóa `"sa pa"`, bấm Tìm kiếm: Cột **Điểm đánh giá TB** của tour `T002` lập tức cập nhật từ **`5,0 (1 lượt)`** sang **`4,5 (2 lượt)`**! |
| **Ca 2 (Khách hàng đã đánh giá hết các chuyến đi hoàn thành)** | Chọn khách hàng `KH001 - Nguyễn Văn An` (có đơn `DH001` đã hoàn thành nhưng đã đánh giá từ trước, và `DH007` chưa khởi hành). | Hiện hộp thông báo màu xanh dương: `"Khách hàng Nguyễn Văn An (KH001) hiện không có chuyến đi nào ở trạng thái Hoàn thành đang chờ đánh giá..."` |
| **Ca 3 (Nhập nhận xét nhà nghỉ nhưng bỏ tích chấm điểm sao nhà nghỉ)** | Khôi phục lại CSDL gốc, chọn `KH004` -> đơn `DH004`. Bỏ tích ô `"Tôi muốn chấm điểm cho Sapa Mountain View (NN03)"`, nhưng gõ chữ `"Phòng sạch"` vào ô Nhận xét nhà nghỉ, bấm **Gửi đánh giá chuyến đi**. | Hiện thông báo lỗi màu đỏ chặn lại: `"Bạn đã nhập nhận xét cho nhà nghỉ nhưng chưa tích chọn chấm điểm sao nhà nghỉ..."` |
| **Ca 4 (Kiểm tra giới hạn 500 ký tự và chuỗi toàn dấu cách)** | Tại ô Nhận xét tour, gõ chỉ toàn dấu cách `"     "`, giữ điểm tour 5 sao, bấm gửi. | Chuỗi dấu cách được tự động chuyển thành `NULL` (`None`), không vi phạm `chk_DonHang_NhanXet`, lưu thành công. |
| **Ca 5 (Đơn hoàn thành nhưng không sử dụng nhà nghỉ)** | Giả sử có đơn hoàn thành mà `MaNhaNghi IS NULL` (ví dụ chuyển `DH013` sang `HOANTHANH` trên `F2` rồi mở `F3` chọn `KH007`). | Cột bên phải tự động ẩn thanh trượt điểm nhà nghỉ và ghi rõ đơn hàng không đăng ký dịch vụ nhà nghỉ. |
| **Ca 6 (Kiểm thử 2 tab trình duyệt bấm gửi đánh giá cùng lúc)** | Khôi phục CSDL gốc, mở 2 tab trình duyệt cùng chọn `KH004` -> `DH004`. Bấm gửi ở Tab 1 trước, ngay lập tức bấm gửi ở Tab 2. | Tab 1 báo thành công. Tab 2 báo lỗi: `"Dữ liệu vừa được cập nhật bởi thao tác khác trên hệ thống. Vui lòng tải lại trang và kiểm tra lại."` |

---

## 5. NHIỆM VỤ TH4 (10/11): KIỂM CHỨNG CHUẨN HÓA 3NF TẠI CHƯƠNG 4

Đây là chương lý thuyết ăn điểm cao nhất của bạn khi bảo vệ trước giảng viên. Hãy nắm vững toàn bộ lập luận và chạy thử các câu lệnh SQL chứng minh dưới đây trên MySQL Workbench.

### 5.1. Định nghĩa 3 dạng chuẩn sử dụng trong Chương 4

1. **Dạng chuẩn 1 (`1NF`):** Mọi thuộc tính trong quan hệ đều mang giá trị nguyên tố (atomic), không có thuộc tính lặp hay thuộc tính đa trị.
2. **Dạng chuẩn 2 (`2NF`):** Quan hệ đạt `1NF` và mọi thuộc tính không khóa đều phụ thuộc hàm đầy đủ vào khóa chính (không tồn tại phụ thuộc hàm bộ phận vào một tập con thực sự của khóa chính ghép).
3. **Dạng chuẩn 3 (`3NF`):** Quan hệ đạt `2NF` và không có thuộc tính không khóa nào phụ thuộc bắc cầu (transitive dependency) vào khóa chính thông qua một thuộc tính không khóa khác. Nói cách khác, với mọi phụ thuộc hàm không tầm thường $X \rightarrow A$, thì $X$ phải là siêu khóa (superkey) hoặc $A$ là thuộc tính khóa (prime attribute).

### 5.2. Tổng hợp 5 bước chuẩn hóa đã thực hiện từ mô hình thực tế sang lược đồ 12 bảng

1. **Tách thuộc tính đa trị `SDT` của `KhachHang` (Đạt `1NF`):**
   - Một khách hàng có nhiều số điện thoại. Nếu lưu gộp vào 1 cột dạng `"0901234567, 0987654321"` sẽ vi phạm `1NF`. Nhóm đã tách thành bảng `SDT_KhachHang(MaKH, SoDienThoai)` có khóa chính ghép `(MaKH, SoDienThoai)`.
2. **Làm phẳng 3 thuộc tính phức hợp trong `DonHang` (Đạt `1NF`):**
   - `ThongTinHuy`, `DanhGiaTour`, `DanhGiaNhaNghi` được tách thành các cột đơn nguyên tố trong bảng `DonHang`.
3. **Không lưu cứng thuộc tính dẫn xuất `TongTien` trong bảng `DonHang` (Tránh vi phạm `3NF`):**
   - Nếu lưu cột `TongTien` trong `DonHang`, sẽ xuất hiện phụ thuộc hàm liên bảng từ `(MaLichTrinh, SoLuongKhach, MaNhaNghi, SoPhong) -> TongTien` và dễ gây dị thường cập nhật khi đổi giá phòng hoặc số khách. Nhóm tính động `TongTien` qua View `v_DonHang_ChiTiet`.
4. **Không lưu lại `MaTinh` trong `DonHang` hay `MaDonVi` trong `ChuyenTrungChuyen` (Tránh phụ thuộc bắc cầu `3NF`):**
   - Tỉnh của nhà nghỉ đã xác định qua `MaNhaNghi -> MaTinh` tại bảng `NhaNghi`; đơn vị vận tải đã xác định qua `MaXe -> MaDonVi` tại bảng `Xe`.
5. **Phát hiện và xử lý phụ thuộc bắc cầu `MaKH -> SoID -> LoaiThe` tại bảng `KhachHang` (Tách bảng thứ 12 `TheThanhToan` để đạt chuẩn `3NF`):**
   - **Phân tích nguyên nhân vi phạm nếu để chung trong `KhachHang`:**
     - Trong bảng `KhachHang` ban đầu có các thuộc tính: `MaKH` (khóa chính), `HoTen`, `DiaChi`, `Email`, `SoID` (số thẻ 16 chữ số), `LoaiThe` (`Visa`, `MasterCard`, `JCB`, `Napas`).
     - Mỗi khách hàng có tối đa 1 thẻ thanh toán mặc định nên `MaKH -> SoID`.
     - Tuy nhiên, nhiều khách hàng trong cùng một gia đình (ví dụ hai vợ chồng `KH001 - Nguyễn Văn An` và `KH002 - Trần Thị Bình`) có thể dùng chung một thẻ thanh toán gia đình (`SoID = '4111111111111111'`). Do đó `SoID` **không phải là khóa ứng viên** của bảng `KhachHang`.
     - Mặt khác, mỗi số thẻ `SoID` chỉ thuộc về đúng một tổ chức phát hành thẻ duy nhất (số thẻ đầu `4` luôn là `Visa`), tức là tồn tại phụ thuộc hàm `SoID -> LoaiThe`.
     - Kết hợp lại ta có chuỗi phụ thuộc bắc cầu: **`MaKH -> SoID -> LoaiThe`**, trong đó `SoID` không phải siêu khóa và `LoaiThe` không phải thuộc tính khóa. Điều này **vi phạm chuẩn `3NF`**, dẫn đến 3 dị thường dữ liệu (Anomalies):
       1. *Dị thường cập nhật (Update Anomaly):* Nếu cập nhật `LoaiThe` của thẻ `'4111111111111111'` ở dòng `KH001` mà quên cập nhật ở dòng `KH002`, cùng một số thẻ sẽ mang 2 loại thẻ khác nhau!
       2. *Dị thường chèn (Insert Anomaly):* Không thể lưu thông tin một thẻ thanh toán hợp lệ nếu chưa gắn với khách hàng nào.
       3. *Dị thường xóa (Delete Anomaly):* Nếu xóa khách hàng cuối cùng đang dùng một thẻ, thông tin loại thẻ của số thẻ đó cũng bị mất.
   - **Giải pháp phân rã (Phương án A):**
     - Tách quan hệ `KhachHang` thành 2 quan hệ:
       1. `TheThanhToan(SoID, LoaiThe)` với khóa chính `SoID` và phụ thuộc hàm `SoID -> LoaiThe` (đạt `3NF`).
       2. `KhachHang(MaKH, HoTen, DiaChi, Email, SoID)` với khóa chính `MaKH`, khóa dự tuyển `Email`, và khóa ngoại `SoID` tham chiếu `TheThanhToan(SoID)` (đạt `3NF`).
     - Theo **Định lý Heath**, vì `SoID -> LoaiThe` giữ nguyên và $R_1 \cap R_2 = \{\text{SoID}\}$ là khóa chính của bảng `TheThanhToan`, phép phân rã này **bảo toàn thông tin (Lossless-Join Decomposition)** và **bảo toàn toàn bộ phụ thuộc hàm (Dependency-Preserving)**.

### 5.3. Bảng tổng hợp kiểm tra dạng chuẩn của toàn bộ 12 bảng trong Chương 4

| STT | Tên bảng quan hệ | Khóa ứng viên (Candidate Keys) | Các phụ thuộc hàm không tầm thường ($F$) | Dạng chuẩn đạt được | Giải thích ngắn gọn |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | `TinhThanh` | `MaTinh`, `TenTinh` | `MaTinh -> TenTinh`; `TenTinh -> MaTinh` | **Đạt 3NF** | Mọi vế trái đều là khóa ứng viên |
| 2 | `TheThanhToan` | `SoID` | `SoID -> LoaiThe` | **Đạt 3NF** | Bảng có 2 thuộc tính, vế trái `SoID` là khóa chính |
| 3 | `KhachHang` | `MaKH`, `Email` | `MaKH -> HoTen, DiaChi, Email, SoID`; `Email -> MaKH, HoTen, DiaChi, SoID` | **Đạt 3NF** | Đã tách `LoaiThe` sang `TheThanhToan`, không còn phụ thuộc bắc cầu |
| 4 | `SDT_KhachHang` | `(MaKH, SoDienThoai)` | *(Không có phụ thuộc hàm không tầm thường vì toàn bộ bảng là khóa)* | **Đạt 3NF** | Quan hệ toàn khóa (All-key relation) |
| 5 | `Tour` | `MaTour` | `MaTour -> TenTour, MoTa, SoNgay, GiaCoBan, MaTinhXuatPhat, MaTinhDen` | **Đạt 3NF** | Khóa đơn `MaTour` xác định trực tiếp mọi cột |
| 6 | `LichTrinh` | `MaLichTrinh` | `MaLichTrinh -> MaTour, NgayKhoiHanh, NgayKetThuc, SoChoToiDa, SoChoDaDat` | **Đạt 3NF** | Khóa đơn `MaLichTrinh` xác định trực tiếp mọi cột |
| 7 | `NhaNghi` | `MaNhaNghi` | `MaNhaNghi -> TenNhaNghi, DiaChi, MaTinh, SucChuaPhong, GiaPhongMoiDem` | **Đạt 3NF** | Khóa đơn `MaNhaNghi` xác định trực tiếp mọi cột |
| 8 | `DonViVanTai` | `MaDonVi`, `Email` | `MaDonVi -> TenDonVi, DiaChi, SoDienThoai, Email`; `Email -> MaDonVi, ...` | **Đạt 3NF** | Mọi vế trái đều là khóa ứng viên |
| 9 | `Xe` | `MaXe`, `BienSoXe` | `MaXe -> BienSoXe, LoaiXe, SoChoNgoi, MaDonVi`; `BienSoXe -> MaXe, ...` | **Đạt 3NF** | Mọi vế trái đều là khóa ứng viên |
| 10 | `TrangThaiDonHang` | `MaTrangThai` | `MaTrangThai -> TenTrangThai, MoTa` | **Đạt 3NF** | Khóa đơn `MaTrangThai` xác định trực tiếp mọi cột |
| 11 | `DonHang` | `MaDonHang` | `MaDonHang -> MaKH, MaLichTrinh, MaNhaNghi, NgayDat, SoLuongKhach, SoPhong, MaTrangThai, NgayHuy, LyDoHuy, PhiPhatHuy, DiemDanhGiaTour, NhanXetTour, NgayDanhGia, DiemDanhGiaNhaNghi, NhanXetNhaNghi` | **Đạt 3NF** | Mọi thuộc tính đều phụ thuộc trực tiếp vào khóa đơn `MaDonHang` |
| 12 | `ChuyenTrungChuyen` | `(MaDonHang, SoThuTuChuyen)` | `(MaDonHang, SoThuTuChuyen) -> MaXe, DiemDon, DiemTra` | **Đạt 3NF** | Phụ thuộc đầy đủ vào khóa ghép `(MaDonHang, SoThuTuChuyen)`, không có phụ thuộc bộ phận hay bắc cầu |

### 5.4. Câu lệnh SQL kiểm chứng phép nối không mất thông tin (Lossless-Join) trên MySQL Workbench

Bạn mở MySQL Workbench và chạy câu lệnh sau để kiểm chứng việc nối `KhachHang` với `TheThanhToan` khôi phục đúng **8 dòng khách hàng** ban đầu (bao gồm cả `KH001` và `KH002` dùng chung thẻ `'4111111111111111'` và `KH007` không lưu thẻ `SoID IS NULL`):

```sql
USE QuanLyDatTour;

SELECT kh.MaKH, kh.HoTen, kh.Email, kh.SoID, th.LoaiThe
FROM KhachHang kh
LEFT JOIN TheThanhToan th ON th.SoID = kh.SoID
ORDER BY kh.MaKH;
```

---

## 6. NHIỆM VỤ TH5, TH6, TH7, TH8, TH9, TH10 (11/11 - 21/11): CHỤP ẢNH, KIỂM THỬ CHÉO VÀ HOÀN THIỆN BÁO CÁO WORD/PDF

### 6.1. Nhiệm vụ TH5 (11/11 - 12/11): Chụp ảnh giao diện `screenshots/Hinh08_F3_GiaoDien.png`

1. Mở MySQL Workbench chạy lại file `database/1_QuanLyDatTour_v3.sql` để dữ liệu về trạng thái gốc.
2. Mở ứng dụng trên Microsoft Edge ở chế độ **Light Mode**, độ phóng đại `100%`, chọn trang **3_Danh_gia (`F3`)**.
3. Chọn khách hàng `KH004 - Phạm Thị Dung` -> chọn chuyến đi `DH004` (`Khám phá Sa Pa`).
4. Kéo thanh trượt Điểm đánh giá tour = **4 sao**, nhập nhận xét `"Lịch trình hợp lý, hướng dẫn viên nhiệt tình."`.
5. Kéo thanh trượt Điểm đánh giá nhà nghỉ = **4 sao**, nhập nhận xét `"Phòng ấm áp, view núi đẹp."`.
6. Bấm nút **Gửi đánh giá chuyến đi** để hiện thông báo màu xanh thành công ở dưới, sau đó nhấn `Win + Shift + S` chụp toàn bộ màn hình lưu thành `screenshots/Hinh08_F3_GiaoDien.png` và đẩy lên Git.

### 6.2. Nhiệm vụ TH6 (14/11): Kiểm thử chéo màn hình `F1 - Đặt tour mới` của Đạt

Vào ngày 14/11, bạn mở trang `1_Dat_tour.py` của Đạt và chạy thử 6 ca kiểm thử:
1. Đặt đơn `DH014` cho `KH002`, tour `T001`, lịch trình `LT02`, 2 khách, nhà nghỉ `NN01`, 1 phòng, có xe trung chuyển (`XE01`, `XE02`) -> kiểm tra tổng tiền `6.250.000 đ` và lưu thành công.
2. Đặt đơn không chọn nhà nghỉ (`SoPhong` tự khóa về `0`).
3. Chọn nhà nghỉ nhưng cố tình chỉnh `SoPhong > SucChuaPhong` (xem slider có chặn tối đa ở `SucChuaPhong` không).
4. Tích chọn xe trung chuyển nhưng bỏ trống Điểm đón hoặc nhập Điểm đón trùng Điểm trả -> kiểm tra thông báo lỗi màu đỏ.
5. Chọn lịch trình chỉ còn ít chỗ trống và kiểm tra giới hạn `SoLuongKhach`.
6. Mở 2 tab cùng đặt hết chỗ trống cuối cùng của `LT01` -> kiểm tra Tab 2 bị `ROLLBACK` an toàn.

### 6.3. Nhiệm vụ TH7 & TH8 (15/11 - 18/11): Tổng hợp góp ý, Chèn 13 hình ảnh chuẩn và Xóa sạch nền vàng (`Highlight`) trên Microsoft Word

#### A. Danh sách đầy đủ 13 hình ảnh cần chèn vào báo cáo Word

Sau khi Khánh, Đạt, Tuân và bạn đã đẩy đủ ảnh vào thư mục `screenshots/`, bạn kiểm tra đủ 13 file ảnh sau:

| Số hiệu hình trong báo cáo | Tên file ảnh trong `screenshots/` | Người chụp | Kích thước chèn chuẩn trong Word |
| :---: | :--- | :---: | :--- |
| **Hình 2.1 (Hình 1)** | `Hinh01_ERD_Chen.png` | Đạt | `Width = 16 cm` (`In Line with Text`, căn giữa) |
| **Hình 3.1 (Hình 2)** | `Hinh02_DataDiagram_Workbench.png` | Khánh | `Width = 16 cm` (`In Line with Text`, căn giữa) |
| **Hình 5.1 (Hình 3)** | `Hinh03_MinhChung_RangBuoc.png` | Khánh | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.1 (Hình 4)** | `Hinh04_F1_GiaoDien.png` | Đạt | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.2a & 6.2b (Hình 5)** | `Hinh05a_F1_Loi1.png` và `Hinh05b_F1_Loi2.png` | Đạt | Đặt cạnh nhau trên cùng 1 dòng hoặc bảng 2 cột không viền, mỗi ảnh `Width = 7,8 cm` |
| **Hình 6.3 (Hình 6)** | `Hinh06_F2_GiaoDien.png` | Tuân | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.4 (Hình 7)** | `Hinh07_F2_Loi.png` | Tuân | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.5 (Hình 8)** | `Hinh08_F3_GiaoDien.png` | Thịnh | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.6 (Hình 9)** | `Hinh09_S1_GiaoDien.png` | Khánh | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.7 (Hình 10)** | `Hinh10_R1_ManHinh.png` | Tuân | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.8 (Hình 11)** | `Hinh11_R1_PDF.png` | Tuân | `Height = 11 cm` (để vừa gọn cùng chú thích trên 1 trang, `In Line with Text`, căn giữa) |
| **Hình 6.9 (Hình 12)** | `Hinh12_R2_ManHinh.png` | Khánh | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |
| **Hình 6.10 (Hình 13)** | `Hinh13_R2_PDF.png` | Khánh | `Width = 15,5 cm` (`In Line with Text`, căn giữa) |

#### B. Quy trình 6 bước bấm phím trên Word để chèn ảnh KHÔNG bị mất phần đầu ảnh (Rất quan trọng!)

- **Tại sao khi chèn ảnh vào Word đôi khi ảnh chỉ hiện một dải mỏng ở đáy còn phần trên biến mất?**
  - Vì đoạn văn (`Paragraph`) đang được đặt giãn dòng cố định (`Line spacing: Exactly`). Nếu bạn chèn ảnh vào một dòng có `Exactly 14 pt`, Word sẽ cắt cụt toàn bộ phần ảnh cao hơn `14 pt`!
- **6 bước thao tác chuẩn xác cho từng vị trí chèn ảnh:**
  1. **Bước 1:** Nhấp chuột **3 lần liên tiếp (`Triple-click`)** vào dòng chữ giữ chỗ màu vàng `[CẦN BỔ SUNG HÌNH ...]` để bôi đen toàn bộ dòng đó.
  2. **Bước 2:** Nhấn tổ hợp phím **`Shift + Mũi tên sang trái` (`Shift + Left Arrow`) đúng 1 lần** (để bỏ chọn ký tự xuống dòng `Paragraph Mark` ở cuối dòng, giúp giữ nguyên định dạng của dòng chú thích ảnh ngay bên dưới).
  3. **Bước 3:** Nhấn phím **`Delete`** để xóa dòng chữ giữ chỗ.
  4. **Bước 4:** Nhấn tổ hợp phím **`Ctrl + Q`** (lệnh `Reset Paragraph Formatting` của Word — bước này đưa giãn dòng về `Single` tự động co giãn theo chiều cao bức ảnh và xóa sạch nền vàng của đoạn!).
  5. **Bước 5:** Nhấn tổ hợp phím **`Ctrl + E`** để căn giữa dòng (`Center`).
  6. **Bước 6:** Vào thẻ **Insert -> Pictures -> This Device...**, chọn file ảnh tương ứng trong thư mục `screenshots/`. Nhấp chuột phải vào ảnh vừa chèn -> **Wrap Text -> In Line with Text**, sau đó vào thẻ **Picture Format** trên góc phải chỉnh **Width** theo đúng bảng kích thước ở trên.

#### C. Quy trình tìm và xóa sạch 100% các chỗ tô nền vàng (`Highlight`) trong báo cáo Word

Thông tin Họ tên, Mã số sinh viên (MSSV) và Công việc phụ trách của cả 4 thành viên (`Nguyễn Tất Đạt - B24DCCN117`, `Nguyễn Tiến Thịnh - B24DCCN546`, `Bùi Đức Tuân - B24DCCN590`, `Nguyễn Quốc Khánh - B24DCCN311`) đã được điền sẵn vào Trang bìa và Bảng 2 (trang 4). Sau khi chèn xong 13 hình ảnh, bạn thực hiện bài kiểm tra tự động sau trên Word để chắc chắn không còn sót bất kỳ dòng `[CẦN BỔ SUNG]` nào:

1. Nhấn tổ hợp phím **`Ctrl + H`** để mở hộp thoại **Find and Replace**, chuyển sang thẻ **Find**.
2. Để trống ô **Find what**, bấm vào nút **More >>** ở góc dưới.
3. Bấm vào nút **Format** ở góc dưới bên trái -> chọn **Highlight**. (Lúc này dưới ô Find what sẽ hiện dòng chữ `Format: Highlight`).
4. Bấm vào nút **Find In** -> chọn **Main Document**.
5. Word sẽ bôi đen tất cả các đoạn văn bản còn dính nền vàng trong tài liệu:
   - Đi đến từng vị trí đó, điền nốt thông tin thực tế (nếu còn sót) rồi bôi đen văn bản -> vào thẻ **Home -> Text Highlight Color -> chọn `No Color`**.
6. Lặp lại bước bấm **Find Next** với `Format: Highlight` cho đến khi Word thông báo: **`"We couldn't find what you were looking for."`** (Kết quả bằng `0`).

### 6.4. Nhiệm vụ TH9 & TH10 (19/11 - 21/11): Cập nhật Mục lục và Xuất file PDF có Bookmarks

1. **Cập nhật Mục lục tự động (`TH9` - Ngày 19/11):**
   - Cuộn lên trang Mục lục ở đầu báo cáo Word, nhấp chuột phải vào bảng Mục lục -> chọn **Update Field...** -> tích chọn **Update entire table** -> bấm **OK**.
   - Kiểm tra tổng số trang của toàn bộ báo cáo ở góc dưới bên trái cửa sổ Word: đảm bảo **`<= 50 trang`** (thường rơi vào khoảng 42 - 46 trang).
2. **Xuất file PDF chuẩn có thanh điều hướng Bookmarks (`TH10` - Ngày 21/11):**
   - Trong Microsoft Word, vào **File -> Save As -> Browse**.
   - Chọn thư mục `docs/report/`, đặt tên file `Bao_cao_BTL_CSDL_QuanLyDatTour.pdf`, tại ô **Save as type** chọn **`PDF (*.pdf)`**.
   - Bấm vào nút **Options...** ngay phía dưới:
     - Tích chọn ô **`Create bookmarks using: Headings`**.
     - Bấm **OK** rồi bấm **Save**.
   - Mở file `.pdf` vừa xuất bằng Microsoft Edge, bấm vào biểu tượng **Table of Contents (Mục lục)** trên thanh công cụ PDF để kiểm tra khi bấm vào từng chương/mục thì trang giấy nhảy đến đúng chương/mục đó.

---

## 7. KỊCH BẢN THUYẾT TRÌNH VÀ TRẢ LỜI VẤN ĐÁP DÀNH RIÊNG CHO THỊNH

### 7.1. Lời thoại thuyết trình của Thịnh (Phút 4:30 - 7:00, Slide 4 & Slide 5)

> "Tiếp nối phần trình bày ERD của bạn Đạt, em là Thịnh, xin phép trình bày Chương 3 (Thiết kế Lược đồ Quan hệ) và Chương 4 (Chuẩn hóa Cơ sở dữ liệu) trên Slide 4 và Slide 5 ạ.
>
> Trên Slide 4 là sơ đồ Data Diagram trích xuất trực tiếp từ MySQL Workbench:
> - Từ 11 thực thể và 12 mối kết hợp trên ERD, nhóm em ánh xạ thành **12 bảng quan hệ** với **13 khóa ngoại (`FOREIGN KEY`)**.
> - Đặc biệt, thuộc tính đa trị `SDT` của khách hàng được tách thành bảng `SDT_KhachHang(MaKH, SoDienThoai)` có khóa chính ghép; thực thể yếu `ChuyenTrungChuyen` nhận khóa chính ghép `(MaDonHang, SoThuTuChuyen)`.
> - Toàn bộ lược đồ được bảo vệ bởi **56 ràng buộc toàn vẹn khai báo** ngay trong MySQL (`12 PRIMARY KEY`, `13 FOREIGN KEY`, `27 CHECK`, `4 UNIQUE`) cùng **2 khung nhìn (`VIEW`)** tính toán tự động tổng tiền và lịch xe trung chuyển.
>
> Trên Slide 5 là kết quả phân tích chuẩn hóa từ `1NF`, `2NF` lên `3NF`:
> - Qua kiểm tra phụ thuộc hàm trên bảng `KhachHang` ban đầu, nhóm phát hiện: nhiều khách hàng trong cùng gia đình có thể dùng chung một số thẻ `SoID` (ví dụ `KH001` và `KH002` cùng dùng thẻ `'4111111111111111'`), nên `SoID` không phải là khóa ứng viên của `KhachHang`. Tuy nhiên mỗi số thẻ `SoID` lại xác định duy nhất một `LoaiThe` (`SoID -> LoaiThe`), tạo ra phụ thuộc bắc cầu **`MaKH -> SoID -> LoaiThe`** vi phạm chuẩn `3NF`.
> - Để giải quyết triệt để dị thường cập nhật, nhóm đã tách bảng thứ 12 là `TheThanhToan(SoID, LoaiThe)` theo định lý Heath. Sau bước phân rã này, **100% cả 12 bảng trong hệ thống đều đạt chuẩn 3NF**, vừa bảo toàn thông tin (Lossless-Join), vừa bảo toàn phụ thuộc hàm.
> Tiếp theo, em xin mời bạn Khánh trình bày về kiến trúc ứng dụng và điều phối phần Demo trực tiếp ạ."

### 7.2. Bộ câu hỏi vấn đáp trọng tâm dành cho Thịnh (Câu 1, Câu 2, Câu 15 và 5 câu hỏi xoáy về Chuẩn hóa 3NF)

#### Câu 1: "Hãy nêu điều kiện để một lược đồ quan hệ đạt chuẩn 1NF, 2NF và 3NF. Trong 12 bảng của nhóm, bảng nào có khóa chính ghép và tại sao bảng đó đạt 2NF, 3NF?"

- **Cách trả lời chuẩn xác:**
  > "Thưa thầy/cô:
  > - Một lược đồ đạt `1NF` khi mọi thuộc tính đều mang giá trị đơn nguyên tố; đạt `2NF` khi đạt `1NF` và mọi thuộc tính không khóa đều phụ thuộc hàm đầy đủ vào khóa chính (không phụ thuộc vào một phần của khóa ghép); đạt `3NF` khi đạt `2NF` và không có thuộc tính không khóa nào phụ thuộc bắc cầu vào khóa chính.
  > - Trong 12 bảng của nhóm em có 2 bảng dùng khóa chính ghép là `SDT_KhachHang(MaKH, SoDienThoai)` và `ChuyenTrungChuyen(MaDonHang, SoThuTuChuyen, MaXe, DiemDon, DiemTra)`. Bảng `SDT_KhachHang` có toàn bộ các cột đều thuộc khóa chính nên hiển nhiên đạt `2NF` và `3NF`. Còn ở bảng `ChuyenTrungChuyen`, mỗi đơn hàng có thể có cả chuyến đón (`SoThuTuChuyen = 1`) và chuyến trả (`SoThuTuChuyen = 2`) với xe, điểm đón, điểm trả khác nhau nên phải kết hợp cả `(MaDonHang, SoThuTuChuyen)` mới xác định được `MaXe`, `DiemDon`, `DiemTra` — tức là phụ thuộc hàm đầy đủ (đạt `2NF`) và không có phụ thuộc bắc cầu giữa các cột không khóa (đạt `3NF`) ạ."

#### Câu 2: "Hãy chứng minh phụ thuộc bắc cầu ở bảng KhachHang trước khi tách và chứng minh phép tách bảng TheThanhToan không làm mất mát thông tin."

- **Cách trả lời chuẩn xác:**
  > "Thưa thầy/cô:
  > 1. **Về phụ thuộc bắc cầu:** Trong bảng `KhachHang` trước khi tách, `MaKH` là khóa chính nên `MaKH -> SoID`. Vì nhiều thành viên trong gia đình (`KH001` và `KH002`) có thể thanh toán bằng cùng một thẻ `'4111111111111111'`, nên `SoID` không xác định duy nhất `MaKH` (`SoID` không phải siêu khóa). Nhưng mỗi số thẻ `SoID` lại chỉ thuộc một loại thẻ duy nhất (`SoID -> LoaiThe`). Do đó `MaKH -> SoID -> LoaiThe` là phụ thuộc hàm bắc cầu, vi phạm `3NF`. Nếu không tách, khi sửa `LoaiThe` của `KH001` mà không sửa `KH002` sẽ gây dị thường cập nhật.
  > 2. **Về bảo toàn thông tin (Lossless-Join):** Khi tách thành $R_1(\text{SoID}, \text{LoaiThe})$ và $R_2(\text{MaKH}, \text{HoTen}, \text{DiaChi}, \text{Email}, \text{SoID})$, phần giao của 2 lược đồ là $R_1 \cap R_2 = \{\text{SoID}\}$. Vì `SoID` là khóa chính của $R_1$ (`SoID -> LoaiThe`), theo định lý Heath phép phân rã này bảo toàn thông tin 100%. Khi thực hiện `LEFT JOIN` giữa `KhachHang` và `TheThanhToan` qua `SoID`, ta thu lại đúng 8 dòng khách hàng như ban đầu mà không sinh ra bất kỳ bộ giả (spurious tuples) nào ạ."

#### Câu 15: "Làm thế nào hệ thống đảm bảo khách hàng chỉ đánh giá được chuyến đi đã hoàn thành và mỗi đơn chỉ đánh giá đúng 1 lần?"

- **Cách trả lời chuẩn xác:**
  > "Thưa thầy/cô, nhóm em bảo vệ ở cả 2 tầng:
  > - **Ở tầng CSDL (MySQL):** Ràng buộc `chk_DonHang_DanhGia` kiểm tra nếu `MaTrangThai <> 'HOANTHANH'` thì toàn bộ 5 cột đánh giá (`DiemDanhGiaTour`, `NhanXetTour`, `NgayDanhGia`, `DiemDanhGiaNhaNghi`, `NhanXetNhaNghi`) bắt buộc phải là `NULL`. Nếu câu lệnh nào cố tình ghi điểm đánh giá cho đơn đang ở trạng thái `DAT`, `THANHTOAN` hoặc `HUY`, MySQL sẽ từ chối ngay.
  > - **Ở tầng Ứng dụng & Giao dịch (`F3`):** Câu truy vấn `F3.1` chỉ nạp các đơn có `MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL`. Khi lưu đánh giá, câu lệnh `UPDATE` (`F3.2`) kiểm tra lại điều kiện `WHERE MaDonHang = %s AND MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL` kèm cờ `phai_co_dong = True`. Ngay khi đánh giá lần đầu thành công, cột `NgayDanhGia` khác `NULL` nên đơn đó không thể bị đánh giá lần thứ hai ạ."

#### 5 câu hỏi phản biện chuyên sâu về Chuẩn hóa 3NF (Dành cho điểm 9 - 10)

1. **"Tại sao cột `SoChoDaDat` trong bảng `LichTrinh` có thể tính được từ `SUM(SoLuongKhach)` của bảng `DonHang` mà nhóm vẫn lưu trong bảng `LichTrinh`? Như vậy có vi phạm 3NF không?"**
   - *Trả lời:* Xét trong phạm vi nội bộ một quan hệ `LichTrinh`, `SoChoDaDat` chỉ phụ thuộc vào khóa chính `MaLichTrinh` (`MaLichTrinh -> SoChoDaDat`), không phụ thuộc bắc cầu qua cột không khóa nào trong bảng `LichTrinh`, nên xét theo định nghĩa phụ thuộc hàm trong một quan hệ thì bảng `LichTrinh` vẫn đạt `3NF`. Về mặt thiết kế hệ thống, đây là kỹ thuật **dư thừa có kiểm soát (Controlled Redundancy)** nhằm phục vụ khóa dòng (`Row-level Locking`) và kiểm tra tức thời `CHECK (SoChoDaDat <= SoChoToiDa)` ngay tại bảng `LichTrinh` để chống đặt quá số chỗ (Overbooking) khi có nhiều giao dịch đồng thời, được đồng bộ tuyệt đối bằng `Transaction` ở `F1` và `F2`.
2. **"Trong bảng `DonHang` có nhiều cột có thể nhận giá trị `NULL` (như `MaNhaNghi`, `NgayHuy`, `LyDoHuy`, `PhiPhatHuy`, `DiemDanhGiaTour`...). Việc có nhiều cột `NULL` có vi phạm 3NF không?"**
   - *Trả lời:* Không vi phạm `3NF` vì khi các thuộc tính này có giá trị, chúng đều phụ thuộc hàm trực tiếp và duy nhất vào khóa chính `MaDonHang`. Nhóm không tách thành các bảng con `HuyDonHang` hay `DanhGiaDonHang` vì mỗi đơn chỉ có tối đa 1 lần hủy hoặc 1 lần đánh giá (quan hệ `1 : 0..1`), và nhóm đã dùng các ràng buộc `chk_DonHang_Huy`, `chk_DonHang_DanhGia` để kiểm soát chặt chẽ khi nào các cột này được phép `NULL` hay `NOT NULL`.
3. **"Tại sao không lưu cứng cột `TongTien` vào bảng `DonHang`?"**
   - *Trả lời:* Vì `TongTien` được tính từ `SoLuongKhach * GiaCoBan + SoPhong * GiaPhongMoiDem * SoDem`. Nếu lưu cứng vào `DonHang`, khi thay đổi số phòng hoặc nhà nghỉ mà quên tính lại sẽ gây bất nhất dữ liệu. Do đó nhóm cài đặt `TongTien` qua View `v_DonHang_ChiTiet` để luôn chính xác theo thời gian thực.
4. **"Phụ thuộc hàm được xác định dựa trên 104 dòng dữ liệu mẫu hay dựa trên quy tắc nghiệp vụ?"**
   - *Trả lời:* Phụ thuộc hàm **luôn luôn được xác định dựa trên quy tắc nghiệp vụ (Business Rules)** của bài toán chứ không phải chỉ nhìn vào vài dòng dữ liệu mẫu hiện tại. Dữ liệu mẫu chỉ dùng để minh họa trường hợp phản ví dụ (như `KH001` và `KH002` dùng chung 1 thẻ thanh toán).
5. **"Trong bảng `ChuyenTrungChuyen(MaDonHang, SoThuTuChuyen, MaXe, DiemDon, DiemTra)`, có phụ thuộc hàm bộ phận nào vào riêng `MaDonHang` không?"**
   - *Trả lời:* Không có ạ. Vì một đơn hàng có 2 chuyến trung chuyển (chuyến 1 là lượt đón, chuyến 2 là lượt trả), mỗi chuyến có điểm đón, điểm trả và xe phục vụ khác nhau (`XE01` đón, `XE02` trả). Do đó phải kết hợp cả cặp `(MaDonHang, SoThuTuChuyen)` mới xác định được `MaXe`, `DiemDon`, `DiemTra`, tức là đạt chuẩn `2NF` và `3NF`.
