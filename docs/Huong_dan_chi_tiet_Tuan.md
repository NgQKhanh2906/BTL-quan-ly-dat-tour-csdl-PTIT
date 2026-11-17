# HƯỚNG DẪN CÔNG VIỆC CHI TIẾT DÀNH RIÊNG CHO TUÂN (UI/FRONTEND, SLIDE & SUBMISSION)

- **Họ và tên thành viên:** Bùi Đức Tuân (`B24DCCN590`)
- **Trạng thái hoàn thành (17/11/2026):** Đã hoàn thành `TU2` đến `TU7` (`2_Quan_ly_don.py`, `5_Phieu_xac_nhan.py`, `phieu_xac_nhan.html`, chụp lại `Hinh06`, `Hinh07`, `Hinh10`, `Hinh11`, cập nhật `docs/GopY_Tuan.md` và đối chiếu Bảng 2 thành viên). Việc còn lại ngoài repo: xin tên giảng viên + tài liệu tham khảo cho phần bìa báo cáo (`TU1`), kiểm thử chéo bổ sung & tạo `Slide_Nhom.pptx` (`TU8`, `TU9`, lưu ý xem phần đính chính schema tại `docs/GopY_Thinh.md` mục 2) và nộp Google Drive (`TU11`).
- **Vai trò trong nhóm:** UI/Frontend Developer, Slide Designer & Submission Coordinator (Phụ trách màn hình `F2 - Quản lý đơn & hủy tour`, màn hình `R1 - Phiếu xác nhận đặt tour` in PDF A4 1 trang, thiết kế slide thuyết trình 8 trang, liên hệ giảng viên và nộp bài lên Google Drive)
- **Phạm vi file được phép chỉnh sửa trực tiếp:**
  1. `tour_app/pages/2_Quan_ly_don.py`
  2. `tour_app/pages/5_Phieu_xac_nhan.py`
  3. `tour_app/templates/phieu_xac_nhan.html`
  4. `screenshots/Hinh06_F2_GiaoDien.png`, `screenshots/Hinh07_F2_Loi.png`, `screenshots/Hinh10_R1_ManHinh.png`, `screenshots/Hinh11_R1_PDF.png`
  5. `docs/GopY_Tuan.md` (File ghi chú góp ý cho Chương 1, Mục 2.2, Chương 9 của báo cáo Word)
  6. `Slide_Nhom.pptx` (File slide thuyết trình của nhóm)
- **Nguyên tắc quan trọng:** Tài liệu này đã bao gồm **100% thông tin, công thức nghiệp vụ, câu lệnh SQL, mã nguồn Python, HTML/CSS và từng bước bấm chuột** dành cho bạn. Bạn chỉ cần làm đúng từ trên xuống dưới theo từng ngày mà không cần mở bất kỳ tài liệu cũ nào khác.

---

## MỤC LỤC

1. [Tổng quan lịch trình của Tuân từ 05/11 đến 22/11/2026](#1-tổng-quan-lịch-trình-của-tuân-từ-0511-đến-22112026)
2. [Chuẩn bị môi trường và quy trình Git dành riêng cho Tuân](#2-chuẩn-bị-môi-trường-và-quy-trình-git-dành-riêng-cho-tuân)
3. [Nhiệm vụ TU1 & TU2 (05/11 - 07/11): Hỏi giảng viên và Rà soát Chương 1, Mục 2.2, Chương 9](#3-nhiệm-vụ-tu1--tu2-0511---0711-hỏi-giảng-viên-và-rà-soát-chương-1-mục-22-chương-9)
4. [Nhiệm vụ TU3 (08/11 - 09/11): Xây dựng màn hình F2 - Quản lý đơn & hủy tour](#4-nhiệm-vụ-tu3-0811---0911-xây-dựng-màn-hình-f2---quản-lý-đơn--hủy-tour)
5. [Nhiệm vụ TU4 & TU5 (09/11 - 10/11): Xây dựng báo cáo R1 - Phiếu xác nhận đặt tour & In PDF](#5-nhiệm-vụ-tu4--tu5-0911---1011-xây-dựng-báo-cáo-r1---phiếu-xac-nhan-dat-tour--in-pdf)
6. [Nhiệm vụ TU6 & TU7 (11/11 - 13/11): Chụp 4 ảnh minh họa và Thu thập thông tin hành chính](#6-nhiệm-vụ-tu6--tu7-1111---1311-chụp-4-ảnh-minh-họa-và-thu-thập-thông-tin-hành-chính)
7. [Nhiệm vụ TU8, TU9, TU10, TU11 (14/11 - 22/11): Kiểm thử chéo, Làm Slide, Đọc soát và Nộp bài](#7-nhiệm-vụ-tu8-tu9-tu10-tu11-1411---2211-kiểm-thử-chéo-làm-slide-đọc-soát-và-nộp-bài)
8. [Kịch bản thuyết trình và Trả lời vấn đáp dành riêng cho Tuân](#8-kịch-bản-thuyết-trình-và-trả-lời-vấn-đáp-dành-riêng-cho-tuân)

---

## 1. TỔNG QUAN LỊCH TRÌNH CỦA TUÂN TỪ 05/11 ĐẾN 22/11/2026

| Mã việc | Ngày thực hiện | Tên công việc | Đầu ra bắt buộc (Deliverables) |
| :--- | :--- | :--- | :--- |
| **TU1** | 05/11 - 06/11 | Nhắn tin / hỏi trực tiếp giảng viên 4 câu hỏi về quy cách nộp bài và lịch vấn đáp | Tin nhắn báo kết quả vào nhóm chat |
| **TU2** | 06/11 - 07/11 | Đọc và kiểm tra Chương 1 (Mô tả bài toán), Mục 2.2 (12 mối kết hợp) và Chương 9 (Kết luận) | File `docs/GopY_Tuan.md` đẩy lên Git |
| **TU3** | 08/11 - 09/11 | Lập trình màn hình `F2 - Quản lý đơn & hủy tour` (`tour_app/pages/2_Quan_ly_don.py`) | Code chạy qua 7 ca kiểm thử, tạo Pull Request `feature/f2-quan-ly-don` |
| **TU4** | 09/11 - 10/11 | Lập trình màn hình `R1 - Phiếu xác nhận đặt tour` (`tour_app/pages/5_Phieu_xac_nhan.py`) và biểu mẫu HTML (`tour_app/templates/phieu_xac_nhan.html`) | Code chạy qua 4 ca kiểm thử, tạo Pull Request `feature/r1-phieu-xac-nhan` |
| **TU5** | 10/11 | Kiểm tra in PDF A4 Dọc (Portrait) cho đơn `DH007` và `DH008` trên Microsoft Edge | Bản in PDF vừa gọn 1 trang A4 |
| **TU6** | 11/11 - 12/11 | Chụp 4 ảnh giao diện và bản in PDF (`Hinh06`, `Hinh07`, `Hinh10`, `Hinh11`) | 4 file ảnh `.png` trong thư mục `screenshots/` |
| **TU7** | 13/11 | Thu thập Họ tên, MSSV, Lớp và tỷ lệ đóng góp (`%`) của 4 thành viên gửi cho Thịnh | Bảng thông tin gửi cho Thịnh điền vào trang bìa và Mục 1.3 |
| **TU8** | 14/11 | Kiểm thử chéo màn hình `F3 - Đánh giá sau chuyến đi` của Thịnh | Báo cáo kết quả kiểm thử `F3` cho Thịnh |
| **TU9** | 15/11 - 18/11 | Soạn thảo `Slide_Nhom.pptx` gồm đúng 8 slide cô đọng | File `Slide_Nhom.pptx` hoàn chỉnh |
| **TU10** | 19/11 - 20/11 | Đọc soát toàn bộ báo cáo `v0.9` từ đầu đến cuối, kiểm tra chính tả và số thứ tự hình/bảng | Danh sách lỗi chính tả (nếu có) gửi Thịnh sửa |
| **TU11** | 22/11 (Trước 21:00) | Nộp bài lên Google Drive của lớp và kiểm tra quyền truy cập ở cửa sổ ẩn danh | Ảnh chụp màn hình đã nộp bài thành công gửi vào nhóm chat |

---

## 2. CHUẨN BỊ MÔI TRƯỜNG VÀ QUY TRÌNH GIT DÀNH RIÊNG CHO TUÂN

### 2.1. Tại sao phải cài đặt môi trường ảo `.venv` và làm việc trên nhánh riêng?

1. **Tại sao dùng `.venv`:** Giúp cài đặt đúng phiên bản thư viện (`streamlit==1.66.0`, `mysql-connector-python==26.7.0`, `pandas==3.0.6`) mà không xung đột với các môn học khác trên máy tính của bạn.
2. **Tại sao tạo nhánh `feature/f2-quan-ly-don` và `feature/r1-phieu-xac-nhan`:** Để khi bạn viết code cho trang số 2 và trang số 5, bạn không vô tình ghi đè lên code của Khánh, Đạt hoặc Thịnh.

### 2.2. Các bước cài đặt lần đầu tiên (Ngày 05/11/2026)

- **Bước 1:** Mở **Windows PowerShell**, di chuyển vào ổ đĩa `D:\` (hoặc thư mục học tập của bạn) và tải kho mã nguồn của nhóm về máy:
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

### 2.3. Quy trình Git cho từng nhiệm vụ lập trình của Tuân

1. **Khi bắt đầu làm màn hình `F2` (Sáng 08/11):**
   ```powershell
   git checkout main
   git pull origin main
   git checkout -b feature/f2-quan-ly-don
   ```
   Sau khi code và test xong `tour_app/pages/2_Quan_ly_don.py`:
   ```powershell
   git status
   git add tour_app/pages/2_Quan_ly_don.py
   git commit -m "feat(f2): hoan thien man hinh quan ly don hang va huy tour"
   git push -u origin feature/f2-quan-ly-don
   ```
   Lên GitHub tạo **Pull Request** vào nhánh `main` và nhắn Khánh duyệt.
2. **Khi bắt đầu làm màn hình `R1` (Chiều 09/11):**
   ```powershell
   git checkout main
   git pull origin main
   git checkout -b feature/r1-phieu-xac-nhan
   ```
   Sau khi code và test xong `tour_app/pages/5_Phieu_xac_nhan.py` và `tour_app/templates/phieu_xac_nhan.html`:
   ```powershell
   git status
   git add tour_app/pages/5_Phieu_xac_nhan.py tour_app/templates/phieu_xac_nhan.html
   git commit -m "feat(r1): hoan thien phieu xac nhan dat tour va bieu mau in A4"
   git push -u origin feature/r1-phieu-xac-nhan
   ```
   Lên GitHub tạo **Pull Request** vào nhánh `main` và nhắn Khánh duyệt.

---

## 3. NHIỆM VỤ TU1 & TU2 (05/11 - 07/11): HỎI GIẢNG VIÊN VÀ RÀ SOÁT CHƯƠNG 1, MỤC 2.2, CHƯƠNG 9

### 3.1. Nhiệm vụ TU1 (05/11 - 06/11): Hỏi giảng viên 4 thông tin hành chính

- **Tại sao phải hỏi sớm từ ngày đầu tiên:** Mỗi giảng viên có thể có quy định riêng về cách đặt tên file nộp bài và định dạng báo cáo (`.pdf` hay `.docx`). Hỏi sớm giúp Thịnh và Khánh chuẩn bị gói nộp bài đúng chuẩn ngay từ đầu.
- **Nội dung tin nhắn mẫu gửi giảng viên (hoặc hỏi trực tiếp trên lớp):**
  > "Em chào thầy/cô ạ. Em là Tuân, đại diện nhóm làm đề tài Hệ thống Quản lý Đặt Tour Du lịch. Thầy/cô cho nhóm em xin phép hỏi 4 thông tin về quy cách nộp Bài tập lớn để nhóm chuẩn bị đúng yêu cầu ạ:
  > 1. Báo cáo nộp trên thư mục Google Drive của lớp nộp bản `.pdf`, bản `.docx`, hay nộp cả hai ạ?
  > 2. Mã nguồn ứng dụng và các file `.sql` nộp dưới dạng một file nén `.zip` hay để nguyên thư mục con trên Google Drive ạ?
  > 3. Thầy/cô có quy định cú pháp đặt tên file/thư mục nộp bài cụ thể không ạ (ví dụ `NhomXX_QuanLyDatTour`)?
  > 4. Lịch thuyết trình và bảo vệ Bài tập lớn của lớp mình dự kiến vào tuần 23/11 hay 30/11 ạ?
  > Em cảm ơn thầy/cô ạ!"
- Sau khi giảng viên phản hồi, bạn chụp màn hình tin nhắn gửi ngay vào nhóm chat của 4 anh em.

### 3.2. Nhiệm vụ TU2 (06/11 - 07/11): Đọc và kiểm tra Chương 1, Mục 2.2 và Chương 9 của báo cáo Word

- **Tại sao Tuân phụ trách kiểm tra các mục này:**
  - Chương 1 chứa toàn bộ **quy tắc nghiệp vụ đặt tour, tính tổng tiền, quy trình 4 trạng thái đơn hàng và 5 mức phạt hủy tour** — đây chính là các công thức bạn sẽ lập trình trong màn hình `F2` và `R1`.
  - Mục 2.2 mô tả **12 mối kết hợp (Relationships)** trên sơ đồ ERD.
  - Chương 9 tổng kết kết quả đạt được của dự án.
- **Quy tắc quan trọng:** Để tránh xung đột file Word nhị phân (`.docx`), bạn **không sửa trực tiếp vào file `.docx`** mà mở file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` để đọc và ghi nhận xét vào file `docs/GopY_Tuan.md`.

#### A. Bảng đối chiếu quy tắc nghiệp vụ trong Chương 1 (Trang 5 - 7)

Hãy đọc kỹ Chương 1 trong file Word và đối chiếu với các công thức chuẩn dưới đây:

1. **Công thức tính tổng tiền đơn hàng (`TongTien`):**
   - `TienTour = SoLuongKhach * GiaCoBan` (lấy `GiaCoBan` từ bảng `Tour` thông qua `LichTrinh`).
   - `SoDem = DATEDIFF(NgayKetThuc, NgayKhoiHanh)` (số đêm lưu trú của lịch trình).
   - `TienPhong = SoPhong * GiaPhongMoiDem * SoDem` (nếu đơn không đặt nhà nghỉ, tức `MaNhaNghi IS NULL` và `SoPhong = 0`, thì `TienPhong = 0`).
   - `TongTien = TienTour + TienPhong`.
   - *Lưu ý:* `TongTien` là thuộc tính dẫn xuất (`Derived Attribute`), không lưu cứng trong bảng `DonHang` mà được tính tự động qua View `v_DonHang_ChiTiet`.

2. **Quy tắc chuyển trạng thái đơn hàng (4 trạng thái trong bảng `TrangThaiDonHang`):**
   - Luồng đi xuôi hợp lệ:
     - `DAT` (*Đã đặt, chờ thanh toán*) -> `THANHTOAN` (*Đã thanh toán*) -> `HOANTHANH` (*Hoàn thành chuyến đi*).
   - Luồng hủy đơn hợp lệ:
     - `DAT` -> `HUY` (*Đã hủy tour*).
     - `THANHTOAN` -> `HUY` (*Đã hủy tour*).
   - Các trạng thái kết thúc (không được phép chuyển sang bất kỳ trạng thái nào khác):
     - `HOANTHANH` và `HUY`.

3. **Công thức 5 mức phạt hủy tour (Quy tắc ưu tiên `< 24h` trước, sau đó xét số ngày trước khởi hành):**

| Thứ tự xét | Điều kiện áp dụng | Mức phạt (%) | Công thức `PhiPhatHuy` | Đơn hàng mẫu trong CSDL để kiểm chứng |
| :---: | :--- | :---: | :--- | :--- |
| **1 (Ưu tiên cao nhất)** | `TIMESTAMPDIFF(HOUR, NgayDat, NgayHuy) < 24` **VÀ** `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy)) >= 7` (Hủy trong vòng 24 giờ kể từ lúc đặt và còn cách ngày khởi hành ít nhất 7 ngày) | **0%** | `0 đ` | **`DH011`**: Đặt `18/10/2026 09:00`, hủy `18/10/2026 20:00` (sau 11 giờ), lịch trình `LT05` khởi hành `14/11/2026` (còn 27 ngày) -> Phạt `0%` (`0 đ`). |
| **2** | Không thỏa điều kiện 1, và `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy)) >= 15` (Hủy trước ngày khởi hành từ 15 ngày trở lên) | **10%** | `ROUND(TongTien * 0.10, 0)` | **`DH009`**: Tổng tiền `7.800.000 đ`, đặt `01/10`, hủy `12/10`, khởi hành `01/11` (còn 20 ngày) -> Phạt `10%` = `780.000 đ`. |
| **3** | Không thỏa điều kiện 1, và `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy))` từ **7 đến 14 ngày** | **30%** | `ROUND(TongTien * 0.30, 0)` | **`DH008`**: Tổng tiền `8.700.000 đ`, đặt `25/09`, hủy `10/10`, khởi hành `20/10` (còn 10 ngày) -> Phạt `30%` = `2.610.000 đ`, hoàn lại `6.090.000 đ`. |
| **4** | `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy))` từ **3 đến 6 ngày** | **50%** | `ROUND(TongTien * 0.50, 0)` | (Trường hợp kiểm thử biên trên giao diện) |
| **5** | `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy)) < 3` (Hủy sát ngày khởi hành dưới 3 ngày) | **100%** | `TongTien` | **`DH006`**: Tổng tiền `3.600.000 đ`, đặt `01/10`, hủy `09/10`, khởi hành `10/10` (còn 1 ngày) -> Phạt `100%` = `3.600.000 đ`. |

#### B. Bảng đối chiếu 12 mối kết hợp trong Mục 2.2

Kiểm tra Mục 2.2 trong file Word xem đã có đủ **12 mối kết hợp** (bao gồm mối kết hợp số 12 là `ThanhToanBang` giữa `KhachHang` và `TheThanhToan`) chưa:

| STT | Tên mối kết hợp | Thực thể tham gia | Bản số (Cardinality) | Tham gia bắt buộc / tùy chọn | Ý nghĩa nghiệp vụ |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | `XuatPhatTu` | `Tour` — `TinhThanh` | `N : 1` | `Tour` bắt buộc (`1,1`), `TinhThanh` tùy chọn (`0,N`) | Mỗi tour có đúng 1 tỉnh/thành xuất phát |
| 2 | `DenTai` | `Tour` — `TinhThanh` | `N : 1` | `Tour` bắt buộc (`1,1`), `TinhThanh` tùy chọn (`0,N`) | Mỗi tour có đúng 1 tỉnh/thành điểm đến |
| 3 | `NamTai` | `NhaNghi` — `TinhThanh` | `N : 1` | `NhaNghi` bắt buộc (`1,1`), `TinhThanh` tùy chọn (`0,N`) | Mỗi nhà nghỉ nằm tại đúng 1 tỉnh/thành |
| 4 | `CoLichTrinh` | `Tour` — `LichTrinh` | `1 : N` | `Tour` tùy chọn (`0,N`), `LichTrinh` bắt buộc (`1,1`) | Một tour có nhiều lịch trình khởi hành theo các đợt khác nhau |
| 5 | `ThanhToanBang` | `KhachHang` — `TheThanhToan` | `N : 1` | `KhachHang` tùy chọn (`0,1`), `TheThanhToan` tùy chọn (`0,N`) | Khách hàng có thể lưu 1 thẻ thanh toán; nhiều khách hàng trong cùng gia đình có thể dùng chung 1 thẻ |
| 6 | `Dat` | `KhachHang` — `DonHang` | `1 : N` | `KhachHang` tùy chọn (`0,N`), `DonHang` bắt buộc (`1,1`) | Một khách hàng có thể đặt nhiều đơn hàng; mỗi đơn thuộc về đúng 1 khách hàng |
| 7 | `ThuocLichTrinh` | `LichTrinh` — `DonHang` | `1 : N` | `LichTrinh` tùy chọn (`0,N`), `DonHang` bắt buộc (`1,1`) | Mỗi đơn hàng đăng ký tham gia đúng 1 lịch trình khởi hành |
| 8 | `LuuTru` | `NhaNghi` — `DonHang` | `1 : N` | `NhaNghi` tùy chọn (`0,N`), `DonHang` tùy chọn (`0,1`) | Đơn hàng có thể chọn lưu trú tại 1 nhà nghỉ hoặc không chọn (`NULL`) |
| 9 | `CoTrangThai` | `TrangThaiDonHang` — `DonHang` | `1 : N` | `TrangThaiDonHang` tùy chọn (`0,N`), `DonHang` bắt buộc (`1,1`) | Mỗi đơn hàng tại một thời điểm có đúng 1 trạng thái xử lý |
| 10 | `SoHuu` | `DonViVanTai` — `Xe` | `1 : N` | `DonViVanTai` tùy chọn (`0,N`), `Xe` bắt buộc (`1,1`) | Một đơn vị vận tải sở hữu nhiều xe; mỗi xe thuộc đúng 1 đơn vị |
| 11 | `CoChuyen` (Mối kết hợp xác định) | `DonHang` — `ChuyenTrungChuyen` | `1 : N` | `DonHang` tùy chọn (`0,N`), `ChuyenTrungChuyen` bắt buộc (`1,1` — nét đôi) | Thực thể yếu `ChuyenTrungChuyen` phụ thuộc tồn tại vào `DonHang` |
| 12 | `PhucVu` | `Xe` — `ChuyenTrungChuyen` | `1 : N` | `Xe` tùy chọn (`0,N`), `ChuyenTrungChuyen` bắt buộc (`1,1`) | Mỗi chuyến trung chuyển được phục vụ bởi đúng 1 xe cụ thể |

#### C. Kiểm tra Chương 9 (Kết luận)

Kiểm tra các con số tổng kết trong Chương 9 phải khớp với kiến trúc đã chuẩn hóa 3NF:
- Tổng số thực thể trên ERD: **11 thực thể** (10 thực thể mạnh + 1 thực thể yếu `ChuyenTrungChuyen`) và **12 mối kết hợp**.
- Tổng số bảng quan hệ trong MySQL: **12 bảng** (tất cả đạt chuẩn **3NF**), **13 khóa ngoại (`FOREIGN KEY`)**, **56 ràng buộc toàn vẹn khai báo (`12 PK + 13 FK + 27 CHECK + 4 UNIQUE`)**, **2 khung nhìn (`VIEW`)**, **104 dòng dữ liệu mẫu**.

#### D. Tạo file `docs/GopY_Tuan.md` và đẩy lên Git

Sau khi kiểm tra xong, bạn tạo file `docs/GopY_Tuan.md` ghi rõ các điểm đã khớp hoặc cần chỉnh sửa trong Chương 1, Mục 2.2, Chương 9 rồi đẩy lên Git để Thịnh tổng hợp.

---

## 4. NHIỆM VỤ TU3 (08/11 - 09/11): XÂY DỰNG MÀN HÌNH F2 - QUẢN LÝ ĐƠN & HỦY TOUR

### 4.1. Tại sao màn hình F2 lại được thiết kế như vậy? (Giải thích lý do kỹ thuật)

1. **Tại sao ô chọn đơn hàng chỉ hiển thị các đơn đang ở trạng thái `DAT` hoặc `THANHTOAN`?**
   - Theo nghiệp vụ, đơn hàng đã `HOANTHANH` hoặc đã `HUY` là trạng thái kết thúc, không thể chuyển trạng thái hay hủy thêm lần nữa. Lọc ngay từ câu `SELECT` (`WHERE dh.MaTrangThai IN ('DAT', 'THANHTOAN')`) giúp nhân viên không bao giờ thao tác nhầm vào đơn đã đóng.
2. **Tại sao ô "Trạng thái mới" chỉ hiển thị các trạng thái đích hợp lệ theo luồng?**
   - Nếu đơn đang là `DAT` (*Đã đặt, chờ thanh toán*), nhân viên chỉ được chuyển sang `THANHTOAN` (*Đã thanh toán*) hoặc `HUY` (*Đã hủy tour*) — không được nhảy cóc từ `DAT` sang `HOANTHANH`.
   - Nếu đơn đang là `THANHTOAN` (*Đã thanh toán*), nhân viên chỉ được chuyển sang `HOANTHANH` (*Hoàn thành chuyến đi*) hoặc `HUY` (*Đã hủy tour*) — không được lùi ngược về `DAT`.
3. **Tại sao khi hủy đơn hàng phải chạy 3 câu lệnh SQL trong cùng 1 `Transaction`?**
   - Khi hủy 1 đơn hàng, hệ thống phải làm đồng thời 3 việc:
     1. Cập nhật trạng thái đơn sang `'HUY'`, ghi `NgayHuy`, `LyDoHuy`, `PhiPhatHuy`.
     2. Hoàn trả lại số chỗ (`SoChoDaDat = SoChoDaDat - SoLuongKhach`) cho bảng `LichTrinh`.
     3. Xóa các dòng xe trung chuyển của đơn đó trong bảng `ChuyenTrungChuyen` (để thỏa mãn quy tắc nghiệp vụ `RB26`: đơn đã hủy không giữ xe trung chuyển).
   - Nếu câu lệnh số 1 chạy xong mà câu lệnh số 2 hoặc số 3 bị lỗi, dữ liệu sẽ bị sai lệch (đơn đã hủy nhưng lịch trình vẫn bị trừ chỗ). Gói cả 3 câu vào hàm `chay_giao_dich()` đảm bảo nguyên lý **All-or-Nothing (Atomicity)**: hoặc cả 3 cùng thành công, hoặc `ROLLBACK` toàn bộ.
4. **Tại sao trong `chay_giao_dich()` của thao tác hủy đơn, câu lệnh 1 và 2 đặt `phai_co_dong=True` nhưng câu lệnh 3 (`DELETE FROM ChuyenTrungChuyen`) lại đặt `phai_co_dong=False`?**
   - Câu 1 (`UPDATE DonHang ... WHERE MaDonHang = %s AND MaTrangThai IN ('DAT', 'THANHTOAN')`) bắt buộc `phai_co_dong=True` (tức `rowcount > 0`). Nếu có 2 nhân viên mở 2 tab trình duyệt cùng bấm hủy 1 đơn cùng lúc, người thứ hai chạy câu `UPDATE` này sẽ thấy `rowcount == 0` (vì người thứ nhất đã đổi `MaTrangThai` sang `'HUY'` rồi). Nhờ `phai_co_dong=True`, hệ thống sẽ lập tức `ROLLBACK` và không hoàn trả chỗ 2 lần!
   - Ngược lại, câu 3 (`DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s`) phải đặt `phai_co_dong=False` vì **có những đơn hàng ngay từ đầu không đăng ký xe trung chuyển** (ví dụ `DH013`), nên khi xóa sẽ có `0` dòng bị xóa (`rowcount == 0`). Nếu đặt `True`, các đơn không có xe trung chuyển sẽ không bao giờ hủy được!

### 4.2. Bảng thiết kế 7 trường và kiểm tra hợp lệ 2 tầng của màn hình F2

| STT | Nhãn hiển thị trên giao diện | Loại điều khiển Streamlit | Kiểm tra hợp lệ tại Tầng 1 (Giao diện Python) | Ràng buộc tương ứng tại Tầng 2 (MySQL) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Đơn hàng cần xử lý** | `st.selectbox` | Chỉ nạp các đơn có `MaTrangThai IN ('DAT', 'THANHTOAN')` | `FK` `fk_DonHang_TrangThai` |
| 2 | **Thông tin tóm tắt đơn** | `st.info` / 3 cột thông tin | Chỉ đọc: hiển thị Khách hàng, Tour, Lịch trình, Số khách, Số phòng, Tổng tiền, Trạng thái hiện tại | View `v_DonHang_ChiTiet` |
| 3 | **Trạng thái mới** | `st.selectbox` | Chỉ nạp trạng thái đích hợp lệ theo luồng (`DAT -> THANHTOAN/HUY`; `THANHTOAN -> HOANTHANH/HUY`) | `RB30` (Luồng chuyển trạng thái) |
| 4 | **Ngày hủy** *(Chỉ hiện khi chọn `Đã hủy tour`)* | `st.date_input` | Mặc định theo đồng hồ hệ thống (`23/10/2026` ở chế độ Demo) | `chk_DonHang_Huy` (`NgayHuy >= NgayDat`) |
| 5 | **Giờ hủy** *(Chỉ hiện khi chọn `Đã hủy tour`)* | `st.time_input` | Mặc định `08:00` ở chế độ Demo; kiểm tra ghép `NgayGioHuy >= NgayDat` trước khi lưu | `chk_DonHang_Huy` (`NgayHuy >= NgayDat`) |
| 6 | **Lý do hủy tour** *(Chỉ hiện khi chọn `Đã hủy tour`)* | `st.text_input` | Bắt buộc nhập khác rỗng sau khi `.strip()`, tối đa 255 ký tự | `chk_DonHang_Huy` (`TRIM(LyDoHuy) <> ''`) |
| 7 | **Bảng xem trước mức phạt & tiền hoàn** *(Chỉ hiện khi chọn `Đã hủy tour`)* | `st.warning` | Tự động tính và hiển thị: Số giờ từ lúc đặt, Số ngày trước khởi hành, Mức phạt (`0%`, `10%`, `30%`, `50%`, `100%`), `PhiPhatHuy`, Số tiền hoàn lại | `chk_DonHang_Huy` (`PhiPhatHuy >= 0`) |

### 4.3. Toàn bộ 6 câu lệnh SQL chuẩn của màn hình F2 (`F2.1` đến `F2.6`)

1. **`F2.1` — Nạp danh sách các đơn hàng đang mở (`DAT`, `THANHTOAN`):**
   ```sql
   SELECT dh.MaDonHang, kh.HoTen, t.TenTour,
          lt.NgayKhoiHanh, dh.SoLuongKhach,
          v.TongTien, dh.MaTrangThai, tt.TenTrangThai
   FROM DonHang dh
   JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
   JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
   JOIN Tour t              ON t.MaTour = lt.MaTour
   JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
   JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
   WHERE dh.MaTrangThai IN ('DAT', 'THANHTOAN')
   ORDER BY dh.NgayDat DESC;
   ```
2. **`F2.2` — Xem chi tiết 1 đơn hàng đang chọn:**
   ```sql
   SELECT dh.MaDonHang, dh.MaKH, kh.HoTen,
          dh.MaLichTrinh, lt.NgayKhoiHanh, lt.NgayKetThuc,
          dh.MaNhaNghi, dh.SoLuongKhach, dh.SoPhong,
          dh.NgayDat, dh.MaTrangThai, tt.TenTrangThai,
          v.TienTour, v.TienPhong, v.TongTien
   FROM DonHang dh
   JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
   JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
   JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
   JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
   WHERE dh.MaDonHang = %s;
   ```
3. **`F2.3` — Nạp danh sách trạng thái đích hợp lệ theo trạng thái hiện tại:**
   ```sql
   SELECT MaTrangThai, TenTrangThai
   FROM TrangThaiDonHang
   WHERE (%s = 'DAT'       AND MaTrangThai IN ('THANHTOAN', 'HUY'))
      OR (%s = 'THANHTOAN' AND MaTrangThai IN ('HOANTHANH', 'HUY'))
   ORDER BY MaTrangThai;
   ```
4. **`F2.4` — Tính xem trước mức phạt hủy tour và số tiền hoàn lại:**
   ```sql
   SELECT dh.MaDonHang, dh.NgayDat, lt.NgayKhoiHanh, v.TongTien,
          TIMESTAMPDIFF(HOUR, dh.NgayDat, %s)            AS SoGioSauKhiDat,
          DATEDIFF(lt.NgayKhoiHanh, DATE(%s))            AS SoNgayTruocKhoiHanh,
          CASE
              WHEN TIMESTAMPDIFF(HOUR, dh.NgayDat, %s) < 24
               AND DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7 THEN 0
              WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 15 THEN 10
              WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7  THEN 30
              WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 3  THEN 50
              ELSE 100
          END AS MucPhatPhanTram,
          ROUND(v.TongTien * (
              CASE
                  WHEN TIMESTAMPDIFF(HOUR, dh.NgayDat, %s) < 24
                   AND DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7 THEN 0
                  WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 15 THEN 10
                  WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7  THEN 30
                  WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 3  THEN 50
                  ELSE 100
              END
          ) / 100, 0) AS PhiPhatDuKien
   FROM DonHang dh
   JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
   JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
   WHERE dh.MaDonHang = %s;
   ```
5. **`F2.5` — Giao dịch (`Transaction`) hủy đơn hàng (Gồm 3 câu lệnh nguyên tử):**
   - Câu 1 (`phai_co_dong=True`):
     ```sql
     UPDATE DonHang
     SET MaTrangThai = 'HUY',
         NgayHuy     = %s,
         LyDoHuy     = %s,
         PhiPhatHuy  = %s
     WHERE MaDonHang = %s
       AND MaTrangThai IN ('DAT', 'THANHTOAN');
     ```
   - Câu 2 (`phai_co_dong=True`):
     ```sql
     UPDATE LichTrinh
     SET SoChoDaDat = SoChoDaDat - %s
     WHERE MaLichTrinh = %s
       AND SoChoDaDat >= %s;
     ```
   - Câu 3 (`phai_co_dong=False`):
     ```sql
     DELETE FROM ChuyenTrungChuyen
     WHERE MaDonHang = %s;
     ```
6. **`F2.6` — Giao dịch chuyển trạng thái thường (`DAT -> THANHTOAN` hoặc `THANHTOAN -> HOANTHANH`):**
   - Câu 1 (`phai_co_dong=True`):
     ```sql
     UPDATE DonHang
     SET MaTrangThai = %s
     WHERE MaDonHang = %s
       AND (
           (MaTrangThai = 'DAT'       AND %s = 'THANHTOAN')
        OR (MaTrangThai = 'THANHTOAN' AND %s = 'HOANTHANH')
       );
     ```

### 4.4. Toàn bộ mã nguồn file `tour_app/pages/2_Quan_ly_don.py`

Bạn mở VS Code, tạo/mở file `tour_app/pages/2_Quan_ly_don.py` và viết đầy đủ đoạn mã sau:

```python
from datetime import datetime
import streamlit as st
from db import doc_sql, chay_giao_dich, dinh_dang_tien, lay_hien_tai

st.set_page_config(page_title="F2 - Quản lý đơn & hủy tour", layout="wide")
st.title("F2. Cập nhật trạng thái và hủy đơn đặt tour")
st.caption(
    "Chuyển trạng thái đơn theo đúng quy trình (DAT -> THANHTOAN -> HOANTHANH) "
    "hoặc hủy đơn kèm tính phí phạt tự động và hoàn trả chỗ cho lịch trình."
)

# F2.1: Nap danh sach cac don hang dang o trang thai DAT hoac THANHTOAN
ds_don = doc_sql(
    """
    SELECT dh.MaDonHang, kh.HoTen, t.TenTour,
           lt.NgayKhoiHanh, dh.SoLuongKhach,
           v.TongTien, dh.MaTrangThai, tt.TenTrangThai
    FROM DonHang dh
    JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
    JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
    JOIN Tour t              ON t.MaTour = lt.MaTour
    JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
    JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
    WHERE dh.MaTrangThai IN ('DAT', 'THANHTOAN')
    ORDER BY dh.NgayDat DESC
    """
)

if ds_don.empty:
    st.info("Hiện không có đơn hàng nào ở trạng thái chờ xử lý (DAT hoặc THANHTOAN).")
    st.stop()

chon_don = st.selectbox(
    "Chọn đơn hàng cần xử lý",
    ds_don.to_dict("records"),
    format_func=lambda r: (
        f"{r['MaDonHang']} | {r['HoTen']} | {r['TenTour']} "
        f"(KH: {r['NgayKhoiHanh']}) | {r['TenTrangThai']}"
    ),
)

# F2.2: Xem chi tiet don hang dang chon
ct = doc_sql(
    """
    SELECT dh.MaDonHang, dh.MaKH, kh.HoTen,
           dh.MaLichTrinh, lt.NgayKhoiHanh, lt.NgayKetThuc,
           dh.MaNhaNghi, dh.SoLuongKhach, dh.SoPhong,
           dh.NgayDat, dh.MaTrangThai, tt.TenTrangThai,
           v.TienTour, v.TienPhong, v.TongTien
    FROM DonHang dh
    JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
    JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
    JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
    JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
    WHERE dh.MaDonHang = %s
    """,
    (chon_don["MaDonHang"],),
).iloc[0]

c1, c2, c3 = st.columns(3)
c1.markdown(
    f"**Mã đơn:** `{ct['MaDonHang']}`  \n"
    f"**Khách hàng:** {ct['HoTen']} (`{ct['MaKH']}`)  \n"
    f"**Ngày đặt:** {ct['NgayDat']}"
)
c2.markdown(
    f"**Lịch trình:** `{ct['MaLichTrinh']}` ({ct['NgayKhoiHanh']} -> {ct['NgayKetThuc']})  \n"
    f"**Số khách:** {int(ct['SoLuongKhach'])} | **Số phòng:** {int(ct['SoPhong'])}  \n"
    f"**Nhà nghỉ:** `{ct['MaNhaNghi'] if ct['MaNhaNghi'] else 'Không sử dụng'}`"
)
c3.markdown(
    f"**Tiền tour:** {dinh_dang_tien(ct['TienTour'])}  \n"
    f"**Tiền phòng:** {dinh_dang_tien(ct['TienPhong'])}  \n"
    f"**Tổng tiền:** **{dinh_dang_tien(ct['TongTien'])}**  \n"
    f"**Trạng thái hiện tại:** `{ct['TenTrangThai']}`"
)

st.divider()

# F2.3: Nap danh sach trang thai dich hop le
ds_tt_moi = doc_sql(
    """
    SELECT MaTrangThai, TenTrangThai
    FROM TrangThaiDonHang
    WHERE (%s = 'DAT'       AND MaTrangThai IN ('THANHTOAN', 'HUY'))
       OR (%s = 'THANHTOAN' AND MaTrangThai IN ('HOANTHANH', 'HUY'))
    ORDER BY MaTrangThai
    """,
    (ct["MaTrangThai"], ct["MaTrangThai"]),
)

tt_moi = st.selectbox(
    "Chọn trạng thái mới",
    ds_tt_moi.to_dict("records"),
    format_func=lambda r: f"{r['TenTrangThai']} ({r['MaTrangThai']})",
)

if tt_moi["MaTrangThai"] == "HUY":
    st.subheader("Thông tin hủy tour và tính phí phạt tự động")
    moc_hien_tai = lay_hien_tai()
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

    # F2.4: Tinh xem truoc muc phat huy tour
    xem_truoc = doc_sql(
        """
        SELECT dh.MaDonHang, dh.NgayDat, lt.NgayKhoiHanh, v.TongTien,
               TIMESTAMPDIFF(HOUR, dh.NgayDat, %s) AS SoGioSauKhiDat,
               DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) AS SoNgayTruocKhoiHanh,
               CASE
                   WHEN TIMESTAMPDIFF(HOUR, dh.NgayDat, %s) < 24
                    AND DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7 THEN 0
                   WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 15 THEN 10
                   WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7  THEN 30
                   WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 3  THEN 50
                   ELSE 100
               END AS MucPhatPhanTram,
               ROUND(v.TongTien * (
                   CASE
                       WHEN TIMESTAMPDIFF(HOUR, dh.NgayDat, %s) < 24
                        AND DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7 THEN 0
                       WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 15 THEN 10
                       WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 7  THEN 30
                       WHEN DATEDIFF(lt.NgayKhoiHanh, DATE(%s)) >= 3  THEN 50
                       ELSE 100
                   END
               ) / 100, 0) AS PhiPhatDuKien
        FROM DonHang dh
        JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
        JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
        WHERE dh.MaDonHang = %s
        """,
        (
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ngay_gio_huy_str,
            ct["MaDonHang"],
        ),
    ).iloc[0]

    phi_phat = int(xem_truoc["PhiPhatDuKien"])
    tien_hoan = int(ct["TongTien"]) - phi_phat

    st.warning(
        f"**Xem trước kết quả tính phí phạt hủy tour:**  \n"
        f"- Thời gian từ lúc đặt đến lúc hủy: **{int(xem_truoc['SoGioSauKhiDat'])} giờ**  \n"
        f"- Số ngày trước ngày khởi hành (`{ct['NgayKhoiHanh']}`): "
        f"**{int(xem_truoc['SoNgayTruocKhoiHanh'])} ngày**  \n"
        f"- Mức phạt áp dụng: **{int(xem_truoc['MucPhatPhanTram'])}%**  \n"
        f"- Phí phạt hủy (`PhiPhatHuy`): **{dinh_dang_tien(phi_phat)}**  \n"
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
                f"thời điểm đặt tour ({ngay_dat_dt.strftime('%Y-%m-%d %H:%M:%S')})."
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
                        LyDoHuy     = %s,
                        PhiPhatHuy  = %s
                    WHERE MaDonHang = %s
                      AND MaTrangThai IN ('DAT', 'THANHTOAN')
                    """,
                    (ngay_gio_huy_str, ly_do_huy.strip(), phi_phat, ct["MaDonHang"]),
                    True,
                ),
                (
                    """
                    UPDATE LichTrinh
                    SET SoChoDaDat = SoChoDaDat - %s
                    WHERE MaLichTrinh = %s
                      AND SoChoDaDat >= %s
                    """,
                    (
                        int(ct["SoLuongKhach"]),
                        ct["MaLichTrinh"],
                        int(ct["SoLuongKhach"]),
                    ),
                    True,
                ),
                (
                    "DELETE FROM ChuyenTrungChuyen WHERE MaDonHang = %s",
                    (ct["MaDonHang"],),
                    False,
                ),
            ]
            ok, tb = chay_giao_dich(ds_lenh_huy)
            if ok:
                st.success(
                    f"Đã hủy đơn `{ct['MaDonHang']}` thành công! "
                    f"Phí phạt: {dinh_dang_tien(phi_phat)}, "
                    f"đã hoàn trả {int(ct['SoLuongKhach'])} chỗ cho lịch trình `{ct['MaLichTrinh']}`."
                )
            else:
                st.error(tb)
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
        ok, tb = chay_giao_dich(ds_lenh_tt)
        if ok:
            st.success(
                f"Đã chuyển đơn `{ct['MaDonHang']}` sang trạng thái "
                f"`{tt_moi['TenTrangThai']}` thành công!"
            )
        else:
            st.error(tb)
```

### 4.5. Hướng dẫn tự chạy 7 ca kiểm thử nghiệm thu màn hình F2

Mở PowerShell, chạy ứng dụng:
```powershell
cd D:\BTL-quan-ly-dat-tour-csdl-PTIT\tour_app
streamlit run app.py
```
Trên trình duyệt, bấm vào mục **2_Quan_ly_don** ở thanh bên trái và thực hiện lần lượt **7 ca kiểm thử** sau:

| Ca kiểm thử | Thao tác thực hiện trên giao diện | Kết quả mong đợi (Pass Criteria) |
| :---: | :--- | :--- |
| **Ca 1 (Hủy đơn hợp lệ - Hợp đồng giao diện với Khánh & Thịnh)** | Chọn đơn `DH010` (Khách `KH004`, lịch trình `LT05` khởi hành `14/11/2026`, 2 khách, tổng tiền `16.000.000 đ`, có 2 chuyến xe trung chuyển). Chọn trạng thái mới = `Đã hủy tour (HUY)`. Giữ nguyên Ngày hủy `2026-10-23`, Giờ hủy `08:00`. Nhập lý do `"Khách bận công tác đột xuất, xin hủy đơn"`. Bấm **Xác nhận hủy đơn hàng**. | 1. Hộp xem trước hiển thị: Còn **22 ngày** trước khởi hành -> Mức phạt **10%** -> Phí phạt `1.600.000 đ` -> Tiền hoàn lại `14.400.000 đ`.<br>2. Bấm nút báo thành công màu xanh.<br>3. Mở MySQL Workbench kiểm tra: `LT05` giảm `SoChoDaDat` từ `2` về `0`; bảng `ChuyenTrungChuyen` của `DH010` còn `0` dòng. |
| **Ca 2 (Chuyển trạng thái xuôi `DAT -> THANHTOAN`)** | Chọn đơn `DH013` (đang ở trạng thái `Đã đặt, chờ thanh toán`). Chọn trạng thái mới = `Đã thanh toán (THANHTOAN)`. Bấm **Cập nhật trạng thái đơn hàng**. | Báo thành công. Trong MySQL, `DH013` đổi `MaTrangThai = 'THANHTOAN'`, các cột `NgayHuy`, `LyDoHuy`, `PhiPhatHuy` vẫn là `NULL`. |
| **Ca 3 (Kiểm tra khóa luồng chuyển ngược)** | Chọn đơn `DH012` (đang ở trạng thái `Đã thanh toán`). Mở ô **Chọn trạng thái mới**. | Ô chọn chỉ hiển thị `Hoàn thành chuyến đi (HOANTHANH)` và `Đã hủy tour (HUY)`, **tuyệt đối không có** lựa chọn quay ngược về `Đã đặt, chờ thanh toán (DAT)`. |
| **Ca 4 (Bỏ trống Lý do hủy)** | Chọn đơn `DH007`, chọn trạng thái mới = `Đã hủy tour (HUY)`, để trống ô **Lý do hủy tour (*)** (hoặc chỉ gõ dấu cách), bấm **Xác nhận hủy đơn hàng**. | Hiện thông báo lỗi màu đỏ: `"Vui lòng nhập Lý do hủy tour (không được để trống)."` Đơn `DH007` không bị hủy. |
| **Ca 5 (Chọn Ngày hủy nhỏ hơn Ngày đặt)** | Chọn đơn `DH007` (Ngày đặt `2026-10-12 10:00:00`), chọn `Đã hủy tour (HUY)`, đổi Ngày hủy thành `2026-10-10`, nhập lý do `"Khách đổi lịch"`, bấm **Xác nhận hủy đơn hàng**. | Hiện thông báo lỗi màu đỏ chặn lại: `"Thời điểm hủy (2026-10-10 08:00:00) không được nhỏ hơn thời điểm đặt tour (2026-10-12 10:00:00)."` |
| **Ca 6 (Đơn đã hoàn thành hoặc đã hủy không xuất hiện)** | Mở danh sách **Chọn đơn hàng cần xử lý**, tìm mã đơn `DH001` (đã hoàn thành) hoặc `DH008` (đã hủy). | Không xuất hiện trong danh sách chọn. |
| **Ca 7 (Kiểm thử 2 tab trình duyệt bấm hủy cùng lúc - Concurrency Test)** | Mở 2 tab trình duyệt cùng vào trang `F2`, cùng chọn đơn `DH013`, cùng chọn `Đã hủy tour (HUY)` và nhập lý do. Bấm nút hủy ở Tab 1 trước, ngay lập tức sang Tab 2 bấm nút hủy. | Tab 1 báo hủy thành công. Tab 2 báo lỗi: `"Dữ liệu vừa được cập nhật bởi thao tác khác trên hệ thống. Vui lòng tải lại trang và kiểm tra lại."` Kiểm tra lịch trình `LT06` chỉ được hoàn trả chỗ đúng **1 lần**, không bị trừ âm. |

- *Lưu ý sau khi kiểm thử xong:* Hãy chạy lại file `database/1_QuanLyDatTour_v3.sql` trong MySQL Workbench để khôi phục dữ liệu mẫu về trạng thái gốc trước khi chuyển sang nhiệm vụ tiếp theo.

---

## 5. NHIỆM VỤ TU4 & TU5 (09/11 - 10/11): XÂY DỰNG BÁO CÁO R1 - PHIẾU XÁC NHẬN ĐẶT TOUR & IN PDF

### 5.1. Tại sao báo cáo R1 phải thiết kế theo bố cục này? (Giải thích lý do kỹ thuật & Tiêu chí chấm điểm)

1. **Đáp ứng Tiêu chí 7 của giảng viên:**
   - Tiêu chí 7 quy định mọi biểu mẫu báo cáo phải nêu rõ **Ai là người lập** và **Lập gửi cho ai**, đồng thời trình bày chuẩn chỉ trên khổ giấy A4.
   - Với báo cáo `R1 - Phiếu xác nhận đặt tour`:
     - **Người lập:** Nhân viên kinh doanh / điều hành tour (nhập họ tên trên giao diện, bắt buộc khác rỗng).
     - **Người nhận:** Khách hàng đặt tour (hiển thị họ tên, mã khách hàng, địa chỉ, email và toàn bộ số điện thoại trên phiếu).
2. **Tại sao phải dùng `GROUP_CONCAT` ở câu lệnh `R1.2`?**
   - Trong thiết kế CSDL đạt chuẩn 3NF, một khách hàng có thể có nhiều số điện thoại lưu ở bảng `SDT_KhachHang` (ví dụ `KH001` có 2 số `0901234567` và `0987654321`). Dùng `GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ')` giúp gom tất cả số điện thoại của khách thành một chuỗi gọn gàng `"0901234567, 0987654321"` để hiển thị trên 1 dòng của phiếu xác nhận.
3. **Tại sao phải dùng hàm `html.escape()` khi đưa dữ liệu vào template HTML?**
   - Để chống lỗi hiển thị HTML và lỗ hổng XSS (Cross-Site Scripting) nếu tên khách hàng, lý do hủy hoặc tên nhân viên lập phiếu có chứa các ký tự đặc biệt như `<`, `>`, `&`, `"`.
4. **Tại sao phải thiết kế CSS `@page { size: A4 portrait; margin: 10mm 12mm; }`?**
   - Để khi giảng viên hoặc bạn bấm nút **In phiếu xác nhận (A4)**, trình duyệt tự động căn chỉnh lề và cỡ chữ vừa khít **1 trang A4 Dọc (Portrait) duy nhất**, không bị tràn 2 dòng chữ ký sang trang thứ 2.

### 5.2. Bố cục chuẩn của Phiếu xác nhận đặt tour (`R1`) trên 1 trang A4 Dọc

| Khu vực trên trang A4 | Nội dung hiển thị chi tiết |
| :--- | :--- |
| **Phần đầu (Header)** | - Bên trái: Tên đơn vị **CÔNG TY DU LỊCH & LỮ HÀNH PTIT TOUR**, địa chỉ, hotline.<br>- Bên phải: Quốc hiệu, Tiêu ngữ, ngày giờ in phiếu.<br>- Giữa: Tiêu đề lớn **PHIẾU XÁC NHẬN ĐẶT TOUR DU LỊCH**, Mã đơn hàng, Ngày đặt, Trạng thái đơn, **Người lập phiếu** (Nhân viên kinh doanh) và **Người nhận phiếu** (Khách hàng). |
| **1. Thông tin khách hàng** | Mã khách hàng (`MaKH`), Họ và tên (`HoTen`), Số điện thoại liên hệ (gom từ `SDT_KhachHang`), Email, Địa chỉ, Loại thẻ thanh toán (`LoaiThe` lấy từ bảng `TheThanhToan`). |
| **2. Thông tin chuyến đi** | Mã tour (`MaTour`), Tên tour (`TenTour`), Tuyến hành trình (`TinhXuatPhat -> TinhDen`), Mã lịch trình (`MaLichTrinh`), Ngày khởi hành (`NgayKhoiHanh`), Ngày kết thúc (`NgayKetThuc`), Thời lượng (`SoNgay` ngày / `SoDem` đêm), Số lượng khách (`SoLuongKhach`). |
| **3. Dịch vụ lưu trú (Nhà nghỉ)** | Nếu đơn có đặt nhà nghỉ (`MaNhaNghi IS NOT NULL`): Hiển thị Mã nhà nghỉ, Tên nhà nghỉ, Địa chỉ, Tỉnh/Thành, Số phòng (`SoPhong`), Số đêm (`SoDem`), Đơn giá phòng/đêm (`GiaPhongMoiDem`). Nếu không đặt: Ghi rõ *"Khách không đăng ký dịch vụ nhà nghỉ đi kèm"*. |
| **4. Lịch trình xe trung chuyển** | Bảng danh sách các chuyến đón/trả từ bảng `ChuyenTrungChuyen` kết nối với `Xe` và `DonViVanTai`: STT, Lượt đi (`1` = Đón khách, `2` = Trả khách), Điểm đón, Điểm trả, Biển số xe, Loại xe, Đơn vị vận tải. Nếu đơn không có xe trung chuyển (hoặc đã hủy): Ghi rõ *"Không có chuyến xe trung chuyển đang hoạt động"*. |
| **5. Chi tiết thanh toán** | Bảng 3 dòng tính tiền: (1) Tiền tour cơ bản (`SoLuongKhach x GiaCoBan = TienTour`), (2) Tiền phòng lưu trú (`SoPhong x SoDem x GiaPhongMoiDem = TienPhong`), (3) **TỔNG CỘNG THANH TOÁN (`TongTien`)**. |
| **6. Thông tin hủy tour** *(Chỉ hiện hoặc ghi rõ nếu đơn ở trạng thái `HUY`)* | Nếu `MaTrangThai = 'HUY'`: Hiển thị Thời điểm hủy (`NgayHuy`), Lý do hủy (`LyDoHuy`), Phí phạt hủy (`PhiPhatHuy`), và **Số tiền hoàn lại cho khách (`TongTien - PhiPhatHuy`)**. Nếu đơn không hủy: Ghi *"Đơn hàng đang hoạt động bình thường (Không phát sinh hủy)"*. |
| **Phần cuối (Footer)** | - Hộp tóm tắt chính sách 5 mức phạt hủy tour (`<24h & >=7 ngày: 0%`, `>=15 ngày: 10%`, `7-14 ngày: 30%`, `3-6 ngày: 50%`, `<3 ngày: 100%`).<br>- 2 ô chữ ký song song: **KHÁCH HÀNG (NGƯỜI NHẬN PHIẾU)** và **NHÂN VIÊN LẬP PHIẾU**. |

### 5.3. Toàn bộ 3 câu lệnh SQL chuẩn của màn hình R1 (`R1.1` đến `R1.3`)

1. **`R1.1` — Nạp danh sách toàn bộ 13 đơn hàng để chọn in phiếu:**
   ```sql
   SELECT dh.MaDonHang, kh.HoTen, t.TenTour,
          lt.NgayKhoiHanh, tt.TenTrangThai, v.TongTien
   FROM DonHang dh
   JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
   JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
   JOIN Tour t              ON t.MaTour = lt.MaTour
   JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
   JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
   ORDER BY dh.MaDonHang;
   ```
2. **`R1.2` — Truy vấn toàn bộ thông tin chi tiết của 1 đơn hàng (kèm loại thẻ từ `TheThanhToan` và danh sách SĐT từ `SDT_KhachHang`):**
   ```sql
   SELECT v.MaDonHang, v.NgayDat,
          v.MaKH, v.TenKhachHang, kh.Email, kh.DiaChi AS DiaChiKH,
          kh.SoID, th.LoaiThe,
          GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ') AS DanhSachSDT,
          v.MaTour, v.TenTour, t.SoNgay, t.MoTa AS MoTaTour,
          tt_di.TenTinh  AS TinhXuatPhat,
          tt_den.TenTinh AS TinhDen,
          v.MaLichTrinh, v.NgayKhoiHanh, v.NgayKetThuc, v.SoDem,
          v.SoLuongKhach, v.GiaCoBan, v.TienTour,
          v.MaNhaNghi, v.TenNhaNghi, nn.DiaChi AS DiaChiNhaNghi,
          v.SoPhong, v.GiaPhongMoiDem, v.TienPhong,
          v.TongTien,
          v.MaTrangThai, v.TenTrangThai,
          v.NgayHuy, v.LyDoHuy, v.PhiPhatHuy,
          CASE
              WHEN v.MaTrangThai = 'HUY' THEN (v.TongTien - IFNULL(v.PhiPhatHuy, 0))
              ELSE NULL
          END AS SoTienHoanLai
   FROM v_DonHang_ChiTiet v
   JOIN KhachHang kh        ON kh.MaKH = v.MaKH
   LEFT JOIN TheThanhToan th ON th.SoID = kh.SoID
   LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
   JOIN Tour t              ON t.MaTour = v.MaTour
   JOIN TinhThanh tt_di     ON tt_di.MaTinh = t.MaTinhXuatPhat
   JOIN TinhThanh tt_den    ON tt_den.MaTinh = t.MaTinhDen
   LEFT JOIN NhaNghi nn     ON nn.MaNhaNghi = v.MaNhaNghi
   WHERE v.MaDonHang = %s
   GROUP BY v.MaDonHang, v.NgayDat,
            v.MaKH, v.TenKhachHang, kh.Email, kh.DiaChi,
            kh.SoID, th.LoaiThe,
            v.MaTour, v.TenTour, t.SoNgay, t.MoTa,
            tt_di.TenTinh, tt_den.TenTinh,
            v.MaLichTrinh, v.NgayKhoiHanh, v.NgayKetThuc, v.SoDem,
            v.SoLuongKhach, v.GiaCoBan, v.TienTour,
            v.MaNhaNghi, v.TenNhaNghi, nn.DiaChi,
            v.SoPhong, v.GiaPhongMoiDem, v.TienPhong,
            v.TongTien,
            v.MaTrangThai, v.TenTrangThai,
            v.NgayHuy, v.LyDoHuy, v.PhiPhatHuy;
   ```
3. **`R1.3` — Truy vấn danh sách các chuyến xe trung chuyển của đơn hàng:**
   ```sql
   SELECT ctc.SoThuTuChuyen,
          CASE ctc.SoThuTuChuyen
              WHEN 1 THEN 'Lượt đón khách'
              WHEN 2 THEN 'Lượt trả khách'
              ELSE CONCAT('Chuyến thứ ', ctc.SoThuTuChuyen)
          END AS TenLuot,
          ctc.DiemDon, ctc.DiemTra,
          x.BienSoXe, x.LoaiXe, x.SoChoNgoi,
          dv.TenDonVi, dv.SoDienThoai AS SDTDonVi
   FROM ChuyenTrungChuyen ctc
   JOIN Xe x            ON x.MaXe = ctc.MaXe
   JOIN DonViVanTai dv  ON dv.MaDonVi = x.MaDonVi
   WHERE ctc.MaDonHang = %s
   ORDER BY ctc.SoThuTuChuyen;
   ```

### 5.4. Toàn bộ mã nguồn file `tour_app/templates/phieu_xac_nhan.html`

Bạn mở VS Code, tạo file `tour_app/templates/phieu_xac_nhan.html` (lưu với bảng mã `UTF-8`) và dán chính xác nội dung sau:

```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Phiếu xác nhận đặt tour - {{MA_DON_HANG}}</title>
    <style>
        @page {
            size: A4 portrait;
            margin: 10mm 12mm;
        }
        * {
            box-sizing: border-box;
        }
        body {
            font-family: "Times New Roman", Times, serif;
            font-size: 12pt;
            line-height: 1.32;
            color: #111;
            margin: 0;
            padding: 8px;
            background: #fff;
        }
        .toolbar-print {
            text-align: right;
            margin-bottom: 8px;
        }
        .btn-print {
            background: #0b5ed7;
            color: #fff;
            border: none;
            padding: 6px 14px;
            font-size: 11pt;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        @media print {
            .toolbar-print {
                display: none !important;
            }
            body {
                padding: 0;
            }
        }
        .header-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 6px;
        }
        .header-table td {
            vertical-align: top;
            font-size: 10.5pt;
        }
        .title-block {
            text-align: center;
            margin: 6px 0 8px 0;
            border-top: 1.5px solid #222;
            border-bottom: 1.5px solid #222;
            padding: 6px 0;
        }
        .title-block h1 {
            font-size: 15pt;
            margin: 0 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .meta-line {
            font-size: 10.5pt;
            margin: 2px 0;
        }
        .section-title {
            font-weight: bold;
            font-size: 11.5pt;
            text-transform: uppercase;
            background: #f0f4f8;
            border-left: 4px solid #0b5ed7;
            padding: 3px 8px;
            margin: 8px 0 4px 0;
        }
        table.info-grid, table.data-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 4px;
            font-size: 10.8pt;
        }
        table.info-grid td {
            padding: 2px 6px;
            vertical-align: top;
        }
        table.data-table th, table.data-table td {
            border: 1px solid #444;
            padding: 4px 6px;
        }
        table.data-table th {
            background: #e9ecef;
            text-align: center;
            font-weight: bold;
        }
        .text-right {
            text-align: right;
        }
        .text-center {
            text-align: center;
        }
        .policy-box {
            border: 1px dashed #555;
            padding: 5px 8px;
            font-size: 9.8pt;
            margin-top: 6px;
            background: #fafafa;
        }
        .sign-table {
            width: 100%;
            margin-top: 10px;
            text-align: center;
            font-size: 10.8pt;
        }
        .sign-table td {
            width: 50%;
            vertical-align: top;
        }
        .sign-space {
            height: 48px;
        }
    </style>
</head>
<body>
    <div class="toolbar-print">
        <button class="btn-print" onclick="window.print()">In phiếu xác nhận (A4)</button>
    </div>

    <table class="header-table">
        <tr>
            <td style="width: 52%;">
                <strong>CÔNG TY DU LỊCH &amp; LỮ HÀNH PTIT TOUR</strong><br>
                Địa chỉ: Km10, Đường Nguyễn Trãi, Quận Hà Đông, Hà Nội<br>
                Hotline: 1900 1234 | Email: dieuhanh@ptittour.edu.vn
            </td>
            <td style="width: 48%; text-align: right;">
                <strong>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</strong><br>
                <span>Độc lập - Tự do - Hạnh phúc</span><br>
                <em>Ngày in phiếu: {{NGAY_IN}}</em>
            </td>
        </tr>
    </table>

    <div class="title-block">
        <h1>PHIẾU XÁC NHẬN ĐẶT TOUR DU LỊCH</h1>
        <div class="meta-line">
            <strong>Mã đơn hàng:</strong> {{MA_DON_HANG}} &nbsp;|&nbsp;
            <strong>Ngày đặt:</strong> {{NGAY_DAT}} &nbsp;|&nbsp;
            <strong>Trạng thái:</strong> {{TEN_TRANG_THAI}}
        </div>
        <div class="meta-line">
            <strong>Người lập phiếu (Nhân viên KD):</strong> {{NGUOI_LAP}} &nbsp;|&nbsp;
            <strong>Người nhận phiếu (Khách hàng):</strong> {{TEN_KHACH_HANG}} ({{MA_KH}})
        </div>
    </div>

    <div class="section-title">1. Thông tin khách hàng</div>
    <table class="info-grid">
        <tr>
            <td style="width: 50%;"><strong>Họ và tên khách hàng:</strong> {{TEN_KHACH_HANG}} ({{MA_KH}})</td>
            <td style="width: 50%;"><strong>Số điện thoại:</strong> {{DANH_SACH_SDT}}</td>
        </tr>
        <tr>
            <td><strong>Email:</strong> {{EMAIL_KH}}</td>
            <td><strong>Phương thức thanh toán:</strong> Thẻ {{LOAI_THE}} ({{SO_ID_THE}})</td>
        </tr>
        <tr>
            <td colspan="2"><strong>Địa chỉ liên hệ:</strong> {{DIA_CHI_KH}}</td>
        </tr>
    </table>

    <div class="section-title">2. Thông tin chuyến đi &amp; lịch trình</div>
    <table class="info-grid">
        <tr>
            <td colspan="2"><strong>Tên chương trình tour:</strong> {{TEN_TOUR}} (Mã tour: {{MA_TOUR}})</td>
        </tr>
        <tr>
            <td style="width: 50%;"><strong>Tuyến hành trình:</strong> {{TINH_XUAT_PHAT}} &rarr; {{TINH_DEN}}</td>
            <td style="width: 50%;"><strong>Mã lịch trình:</strong> {{MA_LICH_TRINH}} ({{THOI_LUONG}})</td>
        </tr>
        <tr>
            <td><strong>Ngày khởi hành:</strong> {{NGAY_KHOI_HANH}}</td>
            <td><strong>Ngày kết thúc:</strong> {{NGAY_KET_THUC}}</td>
        </tr>
        <tr>
            <td><strong>Số lượng khách đăng ký:</strong> {{SO_LUONG_KHACH}} khách</td>
            <td><strong>Đơn giá tour cơ bản:</strong> {{GIA_CO_BAN}} / khách</td>
        </tr>
    </table>

    <div class="section-title">3. Dịch vụ lưu trú (Nhà nghỉ / Khách sạn)</div>
    {{KHOI_NHA_NGHI}}

    <div class="section-title">4. Lịch trình xe trung chuyển đón / trả khách</div>
    {{KHOI_TRUNG_CHUYEN}}

    <div class="section-title">5. Chi tiết thanh toán</div>
    <table class="data-table">
        <thead>
            <tr>
                <th style="width: 8%;">STT</th>
                <th style="width: 44%;">Hạng mục dịch vụ</th>
                <th style="width: 26%;">Diễn giải cách tính</th>
                <th style="width: 22%;">Thành tiền</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="text-center">1</td>
                <td>Chi phí chương trình tour du lịch</td>
                <td class="text-center">{{SO_LUONG_KHACH}} khách &times; {{GIA_CO_BAN}}</td>
                <td class="text-right">{{TIEN_TOUR}}</td>
            </tr>
            <tr>
                <td class="text-center">2</td>
                <td>Chi phí phòng nghỉ lưu trú</td>
                <td class="text-center">{{DIEN_GIAI_PHONG}}</td>
                <td class="text-right">{{TIEN_PHONG}}</td>
            </tr>
            <tr>
                <td colspan="3" class="text-right"><strong>TỔNG CỘNG GIÁ TRỊ ĐƠN HÀNG (1 + 2):</strong></td>
                <td class="text-right"><strong>{{TONG_TIEN}}</strong></td>
            </tr>
        </tbody>
    </table>

    <div class="section-title">6. Thông tin hủy tour &amp; hoàn tiền (Nếu có)</div>
    {{KHOI_THONG_TIN_HUY}}

    <div class="policy-box">
        <strong>Quy định mức phí phạt hủy tour của PTIT Tour:</strong>
        (1) Hủy trong vòng 24 giờ sau khi đặt và còn trước khởi hành từ 7 ngày trở lên: <strong>0%</strong>;
        (2) Trước khởi hành &ge; 15 ngày: <strong>10%</strong>;
        (3) Trước 7 - 14 ngày: <strong>30%</strong>;
        (4) Trước 3 - 6 ngày: <strong>50%</strong>;
        (5) Dưới 3 ngày trước khởi hành: <strong>100% tổng giá trị đơn hàng</strong>.
    </div>

    <table class="sign-table">
        <tr>
            <td>
                <strong>KHÁCH HÀNG (NGƯỜI NHẬN PHIẾU)</strong><br>
                <em>(Ký và ghi rõ họ tên)</em>
                <div class="sign-space"></div>
                <strong>{{TEN_KHACH_HANG}}</strong>
            </td>
            <td>
                <strong>NHÂN VIÊN LẬP PHIẾU</strong><br>
                <em>(Ký và ghi rõ họ tên)</em>
                <div class="sign-space"></div>
                <strong>{{NGUOI_LAP}}</strong>
            </td>
        </tr>
    </table>
</body>
</html>
```

### 5.5. Toàn bộ mã nguồn file `tour_app/pages/5_Phieu_xac_nhan.py`

Bạn mở VS Code, tạo/mở file `tour_app/pages/5_Phieu_xac_nhan.py` và viết đầy đủ đoạn mã sau:

```python
from html import escape
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from db import doc_sql, dinh_dang_tien, lay_hien_tai

st.set_page_config(page_title="R1 - Phiếu xác nhận đặt tour", layout="wide")
st.title("R1. Phiếu xác nhận đặt tour du lịch (Biểu mẫu in A4)")
st.caption(
    "Biểu mẫu do Nhân viên kinh doanh lập để giao cho Khách hàng xác nhận thông tin "
    "chuyến đi, lưu trú, xe trung chuyển, tổng chi phí hoặc thông tin hoàn tiền khi hủy."
)

# R1.1: Nap danh sach toan bo 13 don hang
ds_don = doc_sql(
    """
    SELECT dh.MaDonHang, kh.HoTen, t.TenTour,
           lt.NgayKhoiHanh, tt.TenTrangThai, v.TongTien
    FROM DonHang dh
    JOIN KhachHang kh        ON kh.MaKH = dh.MaKH
    JOIN LichTrinh lt        ON lt.MaLichTrinh = dh.MaLichTrinh
    JOIN Tour t              ON t.MaTour = lt.MaTour
    JOIN TrangThaiDonHang tt ON tt.MaTrangThai = dh.MaTrangThai
    JOIN v_DonHang_ChiTiet v ON v.MaDonHang = dh.MaDonHang
    ORDER BY dh.MaDonHang
    """
)

col1, col2 = st.columns([2, 1])
chon_don = col1.selectbox(
    "Chọn đơn hàng cần xuất phiếu xác nhận",
    ds_don.to_dict("records"),
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

# R1.2: Truy van chi tiet don hang
ct = doc_sql(
    """
    SELECT v.MaDonHang, v.NgayDat,
           v.MaKH, v.TenKhachHang, kh.Email, kh.DiaChi AS DiaChiKH,
           kh.SoID, th.LoaiThe,
           GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ') AS DanhSachSDT,
           v.MaTour, v.TenTour, t.SoNgay, t.MoTa AS MoTaTour,
           tt_di.TenTinh  AS TinhXuatPhat,
           tt_den.TenTinh AS TinhDen,
           v.MaLichTrinh, v.NgayKhoiHanh, v.NgayKetThuc, v.SoDem,
           v.SoLuongKhach, v.GiaCoBan, v.TienTour,
           v.MaNhaNghi, v.TenNhaNghi, nn.DiaChi AS DiaChiNhaNghi,
           v.SoPhong, v.GiaPhongMoiDem, v.TienPhong,
           v.TongTien,
           v.MaTrangThai, v.TenTrangThai,
           v.NgayHuy, v.LyDoHuy, v.PhiPhatHuy,
           CASE
               WHEN v.MaTrangThai = 'HUY' THEN (v.TongTien - IFNULL(v.PhiPhatHuy, 0))
               ELSE NULL
           END AS SoTienHoanLai
    FROM v_DonHang_ChiTiet v
    JOIN KhachHang kh           ON kh.MaKH = v.MaKH
    LEFT JOIN TheThanhToan th   ON th.SoID = kh.SoID
    LEFT JOIN SDT_KhachHang sdt ON sdt.MaKH = kh.MaKH
    JOIN Tour t                 ON t.MaTour = v.MaTour
    JOIN TinhThanh tt_di        ON tt_di.MaTinh = t.MaTinhXuatPhat
    JOIN TinhThanh tt_den       ON tt_den.MaTinh = t.MaTinhDen
    LEFT JOIN NhaNghi nn        ON nn.MaNhaNghi = v.MaNhaNghi
    WHERE v.MaDonHang = %s
    GROUP BY v.MaDonHang, v.NgayDat,
             v.MaKH, v.TenKhachHang, kh.Email, kh.DiaChi,
             kh.SoID, th.LoaiThe,
             v.MaTour, v.TenTour, t.SoNgay, t.MoTa,
             tt_di.TenTinh, tt_den.TenTinh,
             v.MaLichTrinh, v.NgayKhoiHanh, v.NgayKetThuc, v.SoDem,
             v.SoLuongKhach, v.GiaCoBan, v.TienTour,
             v.MaNhaNghi, v.TenNhaNghi, nn.DiaChi,
             v.SoPhong, v.GiaPhongMoiDem, v.TienPhong,
             v.TongTien,
             v.MaTrangThai, v.TenTrangThai,
             v.NgayHuy, v.LyDoHuy, v.PhiPhatHuy
    """,
    (chon_don["MaDonHang"],),
).iloc[0]

# R1.3: Truy van danh sach chuyen xe trung chuyen cua don
ds_ctc = doc_sql(
    """
    SELECT ctc.SoThuTuChuyen,
           CASE ctc.SoThuTuChuyen
               WHEN 1 THEN 'Lượt đón khách'
               WHEN 2 THEN 'Lượt trả khách'
               ELSE CONCAT('Chuyến thứ ', ctc.SoThuTuChuyen)
           END AS TenLuot,
           ctc.DiemDon, ctc.DiemTra,
           x.BienSoXe, x.LoaiXe, x.SoChoNgoi,
           dv.TenDonVi, dv.SoDienThoai AS SDTDonVi
    FROM ChuyenTrungChuyen ctc
    JOIN Xe x           ON x.MaXe = ctc.MaXe
    JOIN DonViVanTai dv ON dv.MaDonVi = x.MaDonVi
    WHERE ctc.MaDonHang = %s
    ORDER BY ctc.SoThuTuChuyen
    """,
    (chon_don["MaDonHang"],),
)

# Tao khoi HTML cho muc 3: Nha nghi
if ct["MaNhaNghi"]:
    khoi_nha_nghi = (
        f"<table class='info-grid'>"
        f"<tr><td style='width:50%;'><strong>Nhà nghỉ / Khách sạn:</strong> "
        f"{escape(str(ct['TenNhaNghi']))} ({escape(str(ct['MaNhaNghi']))})</td>"
        f"<td style='width:50%;'><strong>Số lượng phòng:</strong> {int(ct['SoPhong'])} phòng "
        f"&times; {int(ct['SoDem'])} đêm ({dinh_dang_tien(ct['GiaPhongMoiDem'])}/đêm)</td></tr>"
        f"<tr><td colspan='2'><strong>Địa chỉ lưu trú:</strong> "
        f"{escape(str(ct['DiaChiNhaNghi']))}</td></tr>"
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
if not ds_ctc.empty:
    dong_html = []
    for _, r in ds_ctc.iterrows():
        dong_html.append(
            f"<tr>"
            f"<td class='text-center'>{int(r['SoThuTuChuyen'])}</td>"
            f"<td>{escape(str(r['TenLuot']))}</td>"
            f"<td>{escape(str(r['DiemDon']))}</td>"
            f"<td>{escape(str(r['DiemTra']))}</td>"
            f"<td class='text-center'>{escape(str(r['BienSoXe']))} ({escape(str(r['LoaiXe']))})</td>"
            f"<td>{escape(str(r['TenDonVi']))} ({escape(str(r['SDTDonVi']))})</td>"
            f"</tr>"
        )
    khoi_trung_chuyen = (
        "<table class='data-table'>"
        "<thead><tr>"
        "<th style='width:6%;'>STT</th>"
        "<th style='width:15%;'>Lượt di chuyển</th>"
        "<th style='width:24%;'>Điểm đón</th>"
        "<th style='width:24%;'>Điểm trả</th>"
        "<th style='width:15%;'>Xe phục vụ</th>"
        "<th style='width:16%;'>Đơn vị vận tải</th>"
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
if ct["MaTrangThai"] == "HUY":
    khoi_huy = (
        f"<table class='info-grid'>"
        f"<tr><td style='width:50%;'><strong>Thời điểm hủy đơn:</strong> {escape(str(ct['NgayHuy']))}</td>"
        f"<td style='width:50%;'><strong>Phí phạt hủy tour:</strong> "
        f"<strong>{dinh_dang_tien(ct['PhiPhatHuy'])}</strong></td></tr>"
        f"<tr><td><strong>Lý do hủy:</strong> {escape(str(ct['LyDoHuy']))}</td>"
        f"<td><strong>Số tiền hoàn lại cho khách:</strong> "
        f"<strong>{dinh_dang_tien(ct['SoTienHoanLai'])}</strong></td></tr>"
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
    "{{NGAY_IN}}": lay_hien_tai().strftime("%d/%m/%Y %H:%M"),
    "{{NGAY_DAT}}": escape(str(ct["NgayDat"])),
    "{{TEN_TRANG_THAI}}": escape(str(ct["TenTrangThai"])),
    "{{NGUOI_LAP}}": escape(nguoi_lap.strip()),
    "{{TEN_KHACH_HANG}}": escape(str(ct["TenKhachHang"])),
    "{{MA_KH}}": escape(str(ct["MaKH"])),
    "{{DANH_SACH_SDT}}": escape(str(ct["DanhSachSDT"] or "Chưa cập nhật")),
    "{{EMAIL_KH}}": escape(str(ct["Email"] or "Chưa cập nhật")),
    "{{LOAI_THE}}": escape(loai_the_str),
    "{{SO_ID_THE}}": escape(so_id_an),
    "{{DIA_CHI_KH}}": escape(str(ct["DiaChiKH"] or "Chưa cập nhật")),
    "{{TEN_TOUR}}": escape(str(ct["TenTour"])),
    "{{MA_TOUR}}": escape(str(ct["MaTour"])),
    "{{TINH_XUAT_PHAT}}": escape(str(ct["TinhXuatPhat"])),
    "{{TINH_DEN}}": escape(str(ct["TinhDen"])),
    "{{MA_LICH_TRINH}}": escape(str(ct["MaLichTrinh"])),
    "{{THOI_LUONG}}": f"{int(ct['SoNgay'])} ngày {int(ct['SoDem'])} đêm",
    "{{NGAY_KHOI_HANH}}": escape(str(ct["NgayKhoiHanh"])),
    "{{NGAY_KET_THUC}}": escape(str(ct["NgayKetThuc"])),
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
```

### 5.6. Hướng dẫn tự chạy 4 ca kiểm thử nghiệm thu màn hình R1 & In PDF (`TU4` & `TU5`)

| Ca kiểm thử | Thao tác thực hiện trên giao diện | Kết quả mong đợi (Pass Criteria) |
| :---: | :--- | :--- |
| **Ca 1 (Đơn đang hoạt động có đầy đủ nhà nghỉ & xe trung chuyển)** | Chọn đơn `DH007` (Khách `KH001` - Nguyễn Văn An). | 1. Hiển thị đủ 2 số điện thoại của `KH001`: `0901234567, 0987654321`.<br>2. Hiển thị thẻ `Visa (**** **** **** 1111)`.<br>3. Mục 3 hiển thị khách sạn `NN01`, `1 phòng x 2 đêm x 450.000 đ = 900.000 đ`.<br>4. Mục 4 hiển thị 2 chuyến xe trung chuyển (Lượt đón và Lượt trả).<br>5. Tổng tiền = **`6.250.000 đ`**. |
| **Ca 2 (Đơn đã hủy có phí phạt & tiền hoàn lại)** | Chọn đơn `DH008` (Khách `KH002` - Trần Thị Bình, trạng thái `Đã hủy tour`). | 1. Mục 5 hiển thị Tổng tiền = **`8.700.000 đ`** (`3 khách x 2.500.000 đ + 2 phòng x 2 đêm x 300.000 đ`).<br>2. Mục 6 hiển thị: Thời điểm hủy `2026-10-10 15:00:00`, Phí phạt hủy **`2.610.000 đ`** (30%), Số tiền hoàn lại cho khách **`6.090.000 đ`**. |
| **Ca 3 (Đơn không đặt nhà nghỉ và không có xe trung chuyển)** | Chọn đơn `DH013` (Khách `KH007` - Đặng Văn Giang). | Mục 3 hiển thị *"Khách hàng không đăng ký dịch vụ nhà nghỉ đi kèm (0 phòng)"*, Mục 4 hiển thị *"Không có chuyến xe trung chuyển đang hoạt động"*, Tiền phòng = `0 đ`. |
| **Ca 4 (Kiểm thử in PDF A4 Dọc 1 trang - `TU5`)** | Chọn đơn `DH007` (và sau đó thử với `DH008`), bấm nút màu xanh **In phiếu xác nhận (A4)** góc phải trên của phiếu. Trong hộp thoại Print của Microsoft Edge: Chọn `Destination: Save as PDF`, `Layout: Portrait`, `Paper size: A4`, `Margins: Default`, bỏ tích `Headers and footers`, tích chọn `Background graphics`. | Bản xem trước (Print Preview) của cả `DH007` và `DH008` đều nằm gọn gàng trong **đúng 1 trang A4 Dọc (1 of 1)**, nút "In phiếu xác nhận (A4)" tự động ẩn đi trên bản in. |

---

## 6. NHIỆM VỤ TU6 & TU7 (11/11 - 13/11): CHỤP 4 ẢNH MINH HỌA VÀ THU THẬP THÔNG TIN HÀNH CHÍNH

### 6.1. Nhiệm vụ TU6 (11/11 - 12/11): Chụp 4 ảnh giao diện chuẩn cho báo cáo Word

Trước khi chụp ảnh, bạn mở MySQL Workbench chạy lại file `database/1_QuanLyDatTour_v3.sql` để dữ liệu về trạng thái gốc, sau đó mở ứng dụng trên **Microsoft Edge** ở chế độ **Light Mode**, độ phóng đại `100%`, kích thước cửa sổ `1920 x 1080`:

1. **Ảnh 1 — `screenshots/Hinh06_F2_GiaoDien.png` (Giao diện hủy tour và tính phí phạt tự động trên `F2`):**
   - Vào trang `F2`, chọn đơn `DH010`, chọn trạng thái mới `Đã hủy tour (HUY)`.
   - Giữ Ngày hủy `2026-10-23`, Giờ hủy `08:00`, nhập Lý do hủy: `"Khách bận công tác đột xuất, xin hủy đơn"`.
   - Lúc này trên màn hình xuất hiện hộp màu vàng tính trước mức phạt **10%** (`1.600.000 đ`) và tiền hoàn lại (`14.400.000 đ`). Bạn bấm nút **Xác nhận hủy đơn hàng** để hiện thêm thông báo màu xanh thành công ở dưới, rồi nhấn `Win + Shift + S` chụp toàn bộ màn hình lưu thành `screenshots/Hinh06_F2_GiaoDien.png`.
2. **Ảnh 2 — `screenshots/Hinh07_F2_Loi.png` (Giao diện bắt lỗi nghiệp vụ trên `F2`):**
   - Chọn đơn `DH007` (Ngày đặt `2026-10-12 10:00:00`), chọn `Đã hủy tour (HUY)`.
   - Đổi Ngày hủy về `2026-10-10`, để trống ô **Lý do hủy tour (*)**, rồi bấm **Xác nhận hủy đơn hàng**.
   - Giao diện sẽ hiện 2 hộp thông báo lỗi màu đỏ (1 lỗi bỏ trống lý do hủy, 1 lỗi thời điểm hủy nhỏ hơn thời điểm đặt). Chụp màn hình lưu thành `screenshots/Hinh07_F2_Loi.png`.
3. **Ảnh 3 — `screenshots/Hinh10_R1_ManHinh.png` (Giao diện màn hình `R1 - Phiếu xác nhận đặt tour`):**
   - Vào trang `R1`, chọn đơn `DH007`, giữ tên nhân viên lập phiếu `"Nguyễn Quốc Khánh - Phòng Kinh doanh"`.
   - Chụp màn hình hiển thị cả khung chọn đơn hàng phía trên và phần nội dung phiếu xác nhận phía dưới, lưu thành `screenshots/Hinh10_R1_ManHinh.png`.
4. **Ảnh 4 — `screenshots/Hinh11_R1_PDF.png` (Bản in PDF 1 trang A4 của `R1`):**
   - Tại trang `R1` đang mở đơn `DH007` (hoặc `DH008`), bấm nút **In phiếu xác nhận (A4)**, lưu ra file `Phieu_DH007.pdf`.
   - Mở file `Phieu_DH007.pdf` bằng Microsoft Edge, thu phóng sao cho nhìn trọn vẹn cả trang giấy A4 trắng từ tiêu đề đến 2 chữ ký cuối trang, chụp lại và lưu thành `screenshots/Hinh11_R1_PDF.png`.
5. **Đẩy 4 ảnh lên Git:**
   ```powershell
   git checkout main
   git pull origin main
   git add screenshots/Hinh06_F2_GiaoDien.png screenshots/Hinh07_F2_Loi.png screenshots/Hinh10_R1_ManHinh.png screenshots/Hinh11_R1_PDF.png
   git commit -m "docs(screenshots): bo sung 4 anh chup man hinh F2 va R1"
   git push origin main
   ```

### 6.2. Nhiệm vụ TU7 (13/11): Rà soát thông tin hành chính của 4 thành viên gửi cho Thịnh

Danh sách Họ tên và Mã số sinh viên (MSSV) chính thức của 4 thành viên (đã điền sẵn vào Trang bìa và Bảng 2 của báo cáo Word):
- `Nguyễn Tất Đạt` — MSSV: `B24DCCN117` (Tỷ lệ đóng góp: `25%`).
- `Nguyễn Tiến Thịnh` — MSSV: `B24DCCN546` (Tỷ lệ đóng góp: `25%`).
- `Bùi Đức Tuân` — MSSV: `B24DCCN590` (Tỷ lệ đóng góp: `25%`).
- `Nguyễn Quốc Khánh` — MSSV: `B24DCCN311` (Tỷ lệ đóng góp: `25%`).
- Bạn bổ sung thêm Mã lớp tín chỉ và Họ tên giảng viên hướng dẫn (đúng học hàm/học vị: ThS. / TS. ...) gửi cho Thịnh điền nốt vào trang bìa.

---

## 7. NHIỆM VỤ TU8, TU9, TU10, TU11 (14/11 - 22/11): KIỂM THỬ CHÉO, LÀM SLIDE, ĐỌC SOÁT VÀ NỘP BÀI

### 7.1. Nhiệm vụ TU8 (14/11): Kiểm thử chéo màn hình `F3 - Đánh giá sau chuyến đi` của Thịnh

Vào ngày 14/11, bạn mở ứng dụng và kiểm thử màn hình `3_Danh_gia.py` của Thịnh theo 4 bước:
1. Chọn khách hàng `KH004` (Phạm Thị Dung) -> kiểm tra chỉ hiện chuyến `DH004` (tour Sa Pa đã hoàn thành nhưng chưa đánh giá).
2. Chọn 4 sao cho tour, 4 sao cho nhà nghỉ, nhập nhận xét rồi bấm gửi -> kiểm tra báo thành công và sang màn hình `S1` gõ `"sa pa"` thấy điểm trung bình đổi từ `5,0 (1 lượt)` sang `4,5 (2 lượt)`.
3. Chọn lại `KH004` trên `F3` -> kiểm tra đơn `DH004` không còn xuất hiện (chống đánh giá lại lần 2).
4. Chọn `KH001` -> kiểm tra báo không còn chuyến đi nào chờ đánh giá.

### 7.2. Nhiệm vụ TU9 (15/11 - 18/11): Thiết kế `Slide_Nhom.pptx` gồm đúng 8 trang

- **Quy tắc thiết kế Slide:** Cỡ chữ tối thiểu **20pt**, tối đa **5 gạch đầu dòng trên 1 slide**, nền sáng chữ đậm để chiếu máy chiếu trên lớp rõ nét.
- **Nội dung chi tiết của từng Slide:**

| Số Slide | Tiêu đề Slide | Nội dung hiển thị trên Slide | Người trình bày |
| :---: | :--- | :--- | :---: |
| **Slide 1** | **BÀI TẬP LỚN CƠ SỞ DỮ LIỆU: HỆ THỐNG QUẢN LÝ ĐẶT TOUR DU LỊCH** | - Tên học phần, tên giảng viên hướng dẫn.<br>- Danh sách 4 thành viên (`Nguyễn Tất Đạt - B24DCCN117`, `Nguyễn Tiến Thịnh - B24DCCN546`, `Bùi Đức Tuân - B24DCCN590`, `Nguyễn Quốc Khánh - B24DCCN311`) kèm vai trò. | Tuân (0:00 - 0:30) |
| **Slide 2** | **1. BÀI TOÁN NGHIỆP VỤ & QUY TẮC CỐT LÕI** | - Sơ đồ luồng 4 trạng thái: `DAT -> THANHTOAN -> HOANTHANH` và nhánh rẽ `HUY`.<br>- Công thức tính tổng tiền tự động: `TongTien = TienTour + TienPhong`.<br>- Bảng 5 mức phạt hủy tour (`0%`, `10%`, `30%`, `50%`, `100%`). | Tuân (0:30 - 1:30) |
| **Slide 3** | **2. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD KÝ HIỆU CHEN)** | - Chèn ảnh `Hinh01_ERD_Chen.png` độ phân giải cao.<br>- Hộp chú thích nổi bật: 11 thực thể (1 thực thể yếu `ChuyenTrungChuyen`), 12 mối kết hợp, thuộc tính đa trị `SDT`, thuộc tính dẫn xuất `TongTien`. | Đạt (1:30 - 4:30) |
| **Slide 4** | **3. LƯỢC ĐỒ QUAN HỆ & 56 RÀNG BUỘC TOÀN VẸN** | - Chèn ảnh `Hinh02_DataDiagram_Workbench.png`.<br>- Thống kê: **12 bảng quan hệ**, **13 khóa ngoại (`FK`)**, **27 `CHECK`**, **4 `UNIQUE`**, **2 `VIEW`**, **104 dòng dữ liệu mẫu**. | Thịnh (4:30 - 5:45) |
| **Slide 5** | **4. CHUẨN HÓA LƯỢC ĐỒ CƠ SỞ DỮ LIỆU ĐẠT CHUẨN 3NF** | - Bảng tổng hợp: 10/11 bảng gốc đạt ngay chuẩn 3NF.<br>- Điểm nhấn: Phát hiện phụ thuộc bắc cầu `MaKH -> SoID -> LoaiThe` tại bảng `KhachHang` (vi phạm 3NF) và tách bảng thứ 12 `TheThanhToan(SoID, LoaiThe)` để toàn bộ 12 bảng đạt chuẩn 3NF. | Thịnh (5:45 - 7:00) |
| **Slide 6** | **5. KIẾN TRÚC ỨNG DỤNG & QUẢN LÝ GIAO DỊCH (TRANSACTION)** | - Sơ đồ 3 tầng: Giao diện `Streamlit` -> Tầng kết nối `db.py` (Parameterized Queries + Transaction) -> `MySQL 8.0`.<br>- Cơ chế bảo vệ kép: Kiểm tra tại tầng giao diện + 56 ràng buộc khai báo tại MySQL.<br>- Minh họa giao dịch nguyên tử khi Đặt tour (`F1`) và Hủy tour (`F2`). | Khánh (7:00 - 8:30) |
| **Slide 7** | **6. DEMO TRỰC TIẾP 6 CHỨC NĂNG (`F1, F2, F3, S1, R1, R2`)** | - Liệt kê kịch bản Demo khép kín 6 màn hình trên dữ liệu thực tế.<br>- Mời giảng viên theo dõi màn hình ứng dụng trực tiếp. | Khánh điều phối Demo (8:30 - 11:30) |
| **Slide 8** | **7. TỔNG KẾT & PHẦN HỎI ĐÁP (Q&A)** | - Bảng đối chiếu 7/7 tiêu chí đánh giá của học phần đều hoàn thành 100%.<br>- Lời cảm ơn giảng viên và lắng nghe câu hỏi vấn đáp. | Cả nhóm (11:30 - 12:00) |

### 7.3. Nhiệm vụ TU10 (19/11 - 20/11): Đọc soát toàn bộ báo cáo `v0.9`

Khi Thịnh xuất bản nháp `v0.9` vào ngày 19/11, bạn đọc từ trang bìa đến trang cuối và kiểm tra:
- Không còn bất kỳ dòng chữ nào bị tô nền vàng (`Highlight`).
- Không có hình ảnh nào bị mất nửa trên hoặc tràn lề phải.
- Số thứ tự Hình 1 đến Hình 13 và các Bảng liền mạch, khớp với Mục lục.
- Tổng số trang báo cáo `<= 50 trang`.

### 7.4. Nhiệm vụ TU11 (Trước 21:00 ngày 22/11/2026): Nộp bài lên Google Drive

1. Nhận gói file hoàn chỉnh từ Khánh và Thịnh (gồm báo cáo `.pdf` + `.docx`, thư mục `database/`, thư mục `tour_app/`, sơ đồ `diagrams/`, `Slide_Nhom.pptx`, `README.md`).
2. Tải lên đúng thư mục Google Drive của lớp theo quy cách giảng viên đã trả lời ở nhiệm vụ `TU1`.
3. **Bước bắt buộc:** Mở một cửa sổ trình duyệt ẩn danh (`Ctrl + Shift + N`), truy cập vào đường link Google Drive vừa nộp, tải thử file `.pdf` và `.zip` xuống máy để chắc chắn 100% file không bị khóa quyền truy cập và không bị lỗi giải nén.
4. Chụp màn hình giao diện Google Drive hiển thị thời gian nộp bài (trước 21:00 ngày 22/11/2026) gửi vào nhóm chat.

---

## 8. KỊCH BẢN THUYẾT TRÌNH VÀ TRẢ LỜI VẤN ĐÁP DÀNH RIÊNG CHO TUÂN

### 8.1. Lời thoại thuyết trình của Tuân (Phút 0:00 - 1:30, Slide 1 & Slide 2)

> "Em chào thầy/cô ạ. Em là Tuân, xin phép đại diện nhóm mở đầu phần trình bày đề tài **Hệ thống Quản lý Đặt Tour Du lịch**.
> Nhóm em gồm 4 thành viên: Khánh phụ trách CSDL và kiến trúc hệ thống, Đạt phụ trách thiết kế ERD và chức năng đặt tour, Thịnh phụ trách chuẩn hóa lược đồ và báo cáo kỹ thuật, và em phụ trách chức năng quản lý đơn, phiếu xác nhận và tổng hợp bài nộp.
>
> Trên Slide 2 là bài toán nghiệp vụ cốt lõi của hệ thống:
> - Thứ nhất, mỗi đơn đặt tour đi qua quy trình 4 trạng thái chặt chẽ: từ `DAT` (*Đã đặt, chờ thanh toán*) chuyển sang `THANHTOAN` (*Đã thanh toán*), rồi sang `HOANTHANH` (*Hoàn thành chuyến đi*), hoặc rẽ nhánh sang `HUY` (*Đã hủy tour*).
> - Thứ hai, tổng tiền đơn hàng (`TongTien`) được tính tự động từ tiền tour cộng tiền phòng lưu trú theo số đêm thực tế của lịch trình.
> - Thứ ba, khi khách hàng hủy tour, hệ thống áp dụng tự động bảng 5 mức phí phạt: miễn phí `0%` nếu hủy trong vòng 24 giờ sau khi đặt và còn cách ngày khởi hành ít nhất 7 ngày; phạt `10%` nếu hủy trước từ 15 ngày trở lên; `30%` nếu trước 7 đến 14 ngày; `50%` nếu trước 3 đến 6 ngày; và `100%` nếu hủy sát ngày khởi hành dưới 3 ngày.
> Tiếp theo, em xin mời bạn Đạt trình bày chi tiết về sơ đồ thực thể liên kết ERD ạ."

### 8.2. Câu hỏi vấn đáp trọng tâm dành cho Tuân (Câu 9 và Câu 10)

#### Câu hỏi 9: "Hãy giải thích cách hệ thống tính phí phạt hủy tour trên màn hình F2. Nếu một đơn vừa đặt cách đây 10 tiếng đồng hồ nhưng chỉ còn 5 ngày nữa là tour khởi hành thì bị phạt bao nhiêu phần trăm?"

- **Cách trả lời chuẩn xác:**
  > "Thưa thầy/cô, công thức tính phí phạt hủy tour trong câu truy vấn `F2.4` dùng biểu thức `CASE ... WHEN` kiểm tra theo thứ tự ưu tiên từ trên xuống dưới.
  > Điều kiện ưu tiên số 1 để được miễn phí phạt (`0%`) đòi hỏi **đồng thời cả 2 vế (`AND`)**:
  > - Vế 1: `TIMESTAMPDIFF(HOUR, NgayDat, NgayHuy) < 24` (hủy trong vòng 24 giờ kể từ lúc đặt).
  > - Vế 2: `DATEDIFF(NgayKhoiHanh, DATE(NgayHuy)) >= 7` (tính đến ngày khởi hành vẫn còn ít nhất 7 ngày).
  >
  > Vì vậy, trong tình huống thầy/cô vừa nêu: dù khách hủy sau 10 tiếng (`< 24 giờ`), nhưng ngày khởi hành chỉ còn 5 ngày (`< 7 ngày`), nên điều kiện số 1 trả về `FALSE`. Hệ thống sẽ xét tiếp xuống các nhánh dưới và rơi vào nhánh `DATEDIFF >= 3` (từ 3 đến 6 ngày trước khởi hành), do đó đơn hàng này chịu mức phạt **50% tổng giá trị đơn hàng** ạ."

#### Câu hỏi 10: "Khi hủy một đơn đặt tour trên màn hình F2, những bảng nào trong CSDL bị thay đổi? Làm sao ngăn chặn trường hợp 2 nhân viên mở 2 máy tính cùng bấm hủy 1 đơn hàng dẫn đến hoàn trả số chỗ 2 lần?"

- **Cách trả lời chuẩn xác:**
  > "Thưa thầy/cô, khi hủy một đơn hàng trên `F2`, hệ thống thực thi một `Transaction` gồm **3 câu lệnh SQL** tác động lên **3 bảng**:
  > 1. Bảng `DonHang`: `UPDATE` chuyển `MaTrangThai = 'HUY'`, ghi nhận `NgayHuy`, `LyDoHuy` và `PhiPhatHuy`.
  > 2. Bảng `LichTrinh`: `UPDATE` giảm `SoChoDaDat = SoChoDaDat - SoLuongKhach` để hoàn trả lại chỗ trống cho lịch trình.
  > 3. Bảng `ChuyenTrungChuyen`: `DELETE` xóa các chuyến xe trung chuyển của đơn đó để giải phóng xe theo quy tắc nghiệp vụ `RB26`.
  >
  > Để chống lỗi 2 nhân viên bấm hủy cùng lúc (Race Condition), ở câu lệnh `UPDATE DonHang` đầu tiên, nhóm em đặt điều kiện khóa trạng thái ngay trong mệnh đề `WHERE`:
  > `WHERE MaDonHang = %s AND MaTrangThai IN ('DAT', 'THANHTOAN')`
  > kết hợp với cờ kiểm tra `phai_co_dong = True` (`cursor.rowcount > 0`) trong hàm `chay_giao_dich()`.
  > Khi nhân viên thứ nhất bấm hủy, MySQL khóa dòng đơn hàng đó và đổi `MaTrangThai` sang `'HUY'`. Ngay sau đó, câu lệnh `UPDATE DonHang` của nhân viên thứ hai chạy sẽ không tìm thấy dòng nào thỏa mãn `MaTrangThai IN ('DAT', 'THANHTOAN')` nữa nên `cursor.rowcount` bằng `0`. Hàm `chay_giao_dich()` lập tức thực hiện `conn.rollback()`, dừng toàn bộ giao dịch của người thứ hai và không chạy xuống câu lệnh hoàn trả chỗ cho `LichTrinh`. Nhờ vậy số chỗ không bao giờ bị hoàn trả 2 lần ạ."
