# Kế hoạch và Hướng dẫn Thực thi Tổng hợp Bài tập lớn Cơ sở dữ liệu

- **Đề tài:** Hệ thống quản lý đặt tour du lịch các tỉnh thành tại miền Bắc
- **Học phần:** Cơ sở dữ liệu — Học viện Công nghệ Bưu chính Viễn thông (PTIT)
- **Thành viên nhóm:**
  1. Nguyễn Tất Đạt (`B24DCCN117`) — Phụ trách ERD, ánh xạ lược đồ quan hệ, màn hình `F1`
  2. Nguyễn Tiến Thịnh (`B24DCCN546`) — Phụ trách thực thể, ràng buộc toàn vẹn, chuẩn hóa 3NF, màn hình `F3`, biên tập báo cáo Word
  3. Bùi Đức Tuân (`B24DCCN590`) — Phụ trách yêu cầu dữ liệu, quy tắc nghiệp vụ, màn hình `F2`, phiếu xác nhận `R1`, Slide & nộp bài
  4. Nguyễn Quốc Khánh (`B24DCCN311`) — Phụ trách CSDL MySQL, Data Diagram, màn hình tìm kiếm `S1`, báo cáo doanh thu `R2`, quản lý GitHub
- **Hệ thống tài liệu hướng dẫn của dự án (Đã hợp nhất toàn bộ từ Bản 4 và Bản 5, không cần giữ file cũ):**
  1. `docs/Ke_hoach_Tong_hop_BTL_CSDL.md` (Tài liệu tổng quan này: lộ trình 6 cụm từ 05/11 đến 22/11/2026, ma trận phân công, quy trình Git và kịch bản bảo vệ 15 phút).
  2. `docs/Huong_dan_chi_tiet_Khanh.md` (Sổ tay cầm tay chỉ việc dành riêng cho **Khánh**: toàn bộ 4 file SQL 12 bảng, `db.py`, `app.py`, `S1`, `R2`, `DataDiagram`, chụp ảnh, đóng gói và điều phối Demo).
  3. `docs/Huong_dan_chi_tiet_Dat.md` (Sổ tay cầm tay chỉ việc dành riêng cho **Đạt**: hướng dẫn vẽ `ERD.drawio` 11 thực thể 12 mối kết hợp từng bước, code đầy đủ `F1`, kiểm thử máy sạch và câu hỏi vấn đáp ERD).
  4. `docs/Huong_dan_chi_tiet_Tuan.md` (Sổ tay cầm tay chỉ việc dành riêng cho **Tuân**: công thức nghiệp vụ, code đầy đủ `F2` & `R1`, thiết kế 8 trang Slide và quy trình nộp Google Drive).
  5. `docs/Huong_dan_chi_tiet_Thinh.md` (Sổ tay cầm tay chỉ việc dành riêng cho **Thịnh**: từ điển dữ liệu 12 bảng, 32 quy tắc toàn vẹn, chứng minh chuẩn hóa 3NF, code đầy đủ `F3` và quy trình biên tập báo cáo Word/PDF).

---

## Phần 1. Đối chiếu hai Bản Kế hoạch Nguồn và Các Quyết định Kỹ thuật Đã Chốt

### I. Bảng đối chiếu Bản 4 (Tài liệu 5 Quyển - 22/10) và Bản 5 (Kế hoạch hoàn thiện - 05/11)

| Hạng mục | Bản 4 (Tài liệu tổng hợp 5 Quyển - 22/10) | Bản 5 (Kế hoạch hoàn thiện - 05/11) | Quy tắc áp dụng chính thức cho nhóm |
| :--- | :--- | :--- | :--- |
| **Thiết kế CSDL (Quyết định D6)** | Đề xuất Phương án A: tách bảng `TheThanhToan(SoID, LoaiThe)` khỏi `KhachHang` | Chốt chính thức Phương án A | **11 thực thể ERD, 12 mối liên kết** -> **12 bảng đạt chuẩn 3NF, 13 khóa ngoại, 56 ràng buộc** (`12 PK`, `13 FK`, `27 CHECK`, `4 UNIQUE`), **2 view**, **104 dòng mẫu** |
| **Công nghệ & Thời gian Demo** | MySQL 8.0.16+, Python 3.11-3.13, `streamlit 1.66.0`, `mysql-connector-python 26.7.0`, `pandas 3.0.6`; `@HienTai = '2026-10-23 08:00:00'` | Giữ nguyên hoàn toàn | Giữ nguyên; trong `db.py` đặt `CHE_DO_DEMO = True` cố định mốc `23/10/2026 08:00:00` |
| **Mật khẩu MySQL trong `db.py`** | Ghi trực tiếp `"password": "matkhau_cua_ban"` trong `CAU_HINH` | Đọc qua biến môi trường `MYSQL_PASSWORD` | Không ghi mật khẩu vào code; đọc từ biến môi trường `MYSQL_PASSWORD` để đẩy lên GitHub an toàn |
| **Báo cáo R1 và R2** | Chỉ hiển thị dữ liệu đơn hàng / doanh thu và xuất HTML/PDF | Bổ sung ô nhập **Người lập**, dòng **Nơi nhận** và **Khối chữ ký** | Áp dụng Bản 5 để ăn trọn 1,0 điểm Tiêu chí 7 ("nêu rõ ai tạo, gửi ai"); bỏ trống tên người lập thì ẩn nút tải file |
| **Cấu trúc và Cách viết Báo cáo** | Viết từ đầu trên Google Docs, chia 6 chương (gộp chung F/S/R vào Chương 6) | Dùng file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` (42 trang, 9 chương + 1 phụ lục, tối đa 50 trang) | **Chỉ một mình Thịnh sửa trực tiếp file `.docx`**; Đạt, Tuân, Khánh rà soát và gửi file `docs/GopY_<Ten>.md` |
| **Số lượng ảnh chụp màn hình** | Chụp toàn bộ các ca nghiệm thu lưu vào `5_HinhAnh/` | Chốt đúng **13 hình chuẩn** (`Hinh01` đến `Hinh13`, trong đó Hình 5 gồm `5a`, `5b`) | Chụp đúng 13 hình theo kích thước quy định để chèn vào 13 khung chờ sẵn trong báo cáo Word (giữ tổng số trang <= 50) |
| **Lộ trình và Mã Task** | 10 cụm 3 ngày (23/10 - 21/11), mã `C1-D1`... `C10-TH1` | 6 cụm 3 ngày (05/11 - 22/11), mã `D1-D9`, `TH1-TH10`, `TU1-TU11`, `K1-K12` | Lịch thực thi chạy theo **6 cụm của Bản 5**; toàn bộ SQL, code và hướng dẫn từng bước đã được nhúng đầy đủ vào 4 file `docs/Huong_dan_chi_tiet_<Ten>.md` |
| **Nộp bài và Bảo vệ** | Nhóm tự tạo Drive gửi link cho giảng viên | Nộp vào thư mục Google Drive do giảng viên tạo trước **21:00 ngày 22/11/2026**; thuyết trình 15 phút ngày **23/11** hoặc **30/11/2026** | Chuẩn bị sẵn gói nộp chuẩn hóa; tập thuyết trình 2 lần với kịch bản 15 phút và có video demo dự phòng 6 phút |

---

## Phần 2. Mục tiêu (Goal), Tiêu chí Hoàn thành và Thang điểm 8 Tiêu chí

### I. Goal và Phạm vi
- **Goal:** Hoàn thành toàn bộ cơ sở dữ liệu (12 bảng), ứng dụng Streamlit (6 màn hình: `F1`, `F2`, `F3`, `S1`, `R1`, `R2`) và báo cáo Word/PDF (<= 50 trang, đủ 13 hình, không còn ô tô vàng Highlight) để nộp lên Google Drive của giảng viên trước **21:00 Chủ nhật ngày 22/11/2026** (sớm hơn 2 giờ so với hạn chót 23:00 ngày 22/11/2026), đạt đủ 8 tiêu chí chấm điểm (10/10 điểm) và bảo vệ trôi chảy trong 15 phút.
- **Phạm vi thực hiện (Must & Should):**
  - Cơ sở dữ liệu MySQL 8.0 gồm 4 tệp SQL chuẩn hóa 3NF.
  - Sơ đồ khái niệm `ERD.drawio` / `ERD.png` và sơ đồ vật lý `DataDiagram.mwb` / `DataDiagram.png`.
  - Ứng dụng `tour_app` gồm 3 Form nhập (`F1`, `F2`, `F3`), 1 Màn hình tìm kiếm (`S1`), 2 Báo cáo xuất PDF (`R1` khổ A4 dọc, `R2` khổ A4 ngang).
  - Báo cáo 9 chương + 1 phụ lục, Slide thuyết trình 8 trang, Video demo dự phòng 6 phút.
- **Phạm vi không thực hiện (Won't):**
  - Không làm chức năng đăng nhập, phân quyền, gửi email tự động, thanh toán trực tuyến.
  - Không dùng Stored Procedure, Function, Trigger trong MySQL (toàn bộ kiểm soát liên bảng xử lý bằng Transaction trong Python và đối soát bằng `4_KiemTra_RangBuoc.sql`).

### II. Bảng đối chiếu 8 Tiêu chí Chấm điểm với Chương Báo cáo và Người Phụ trách

| # | Tiêu chí chấm điểm của giảng viên | Điểm | Bằng chứng bắt buộc phải có trong báo cáo và sản phẩm | Vị trí trong Báo cáo Word | Người phụ trách | Người kiểm tra chéo |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | Mô tả tổng quan yêu cầu dữ liệu | **1,0** | Bài toán thực tế, phạm vi 15 tỉnh miền Bắc (sau sáp nhập 2025), người dùng, dữ liệu cần lưu, quy tắc tính tiền/hủy/trạng thái | Chương 1 (tr. 5-7) | Tuân | Thịnh |
| **2** | Vẽ và mô tả mô hình ERD | **2,5** | Bảng 11 thực thể & thuộc tính, bảng 12 mối liên kết, Hình 1 (`Hinh01_ERD.png`), bảng ký hiệu Chen (thực thể yếu, đa trị, dẫn xuất, phức hợp) | Chương 2 (tr. 8-10) | Đạt (2.3, Hình 1)<br>Thịnh (2.1)<br>Tuân (2.2) | Khánh |
| **3** | Mô hình quan hệ, mô tả bảng tương thích ERD | **2,0** | 4 quy tắc chuyển đổi, 12 lược đồ quan hệ, 12 bảng mô tả cột, 5 nhóm ràng buộc (RB01-RB32), Hình 2 (`Hinh02_DataDiagram.png`), bảng đối chiếu ERD - Data Diagram (12 bảng, 13 FK) | Chương 3 (tr. 11-16)<br>Chương 5 (tr. 20-22) | Đạt (3.1, 3.2)<br>Thịnh (3.3, 3.4)<br>Khánh (3.5, Ch.5) | Tuân |
| **4** | Kiểm tra và chuẩn hóa 3NF | **1,0** | Xét phụ thuộc hàm từng bảng, chỉ ra `KhachHang` vi phạm 3NF do `MaKH -> SoID -> LoaiThe`, tách bảng `TheThanhToan`, câu SQL `LEFT JOIN` chứng minh bảo toàn thông tin (8 dòng) | Chương 4 (tr. 17-19) | Thịnh | Đạt |
| **5** | Ít nhất 2 màn hình nhập, có demo kiểm tra tính đúng đắn | **1,0** | Đặc tả F1, F2, F3: giao diện, bảng trường, kiểm tra 2 lớp (Form + MySQL CHECK), câu lệnh SQL, bảng ca kiểm thử, ảnh chặn lỗi (`Hinh05a`, `Hinh05b`, `Hinh07`); demo trực tiếp nhập sai bị chặn | Chương 6 (tr. 23-30) | Đạt (F1 - 6.2)<br>Tuân (F2 - 6.3)<br>Thịnh (F3 - 6.4) | Khánh |
| **6** | 1 màn hình tìm kiếm | **0,5** | Đặc tả S1: 8 bộ lọc + nút lọc nhanh "Tour cao cấp", 1 câu SQL `SELECT` đa điều kiện `(@Loc IS NULL OR ...)`, 6 ca kiểm thử, `Hinh09_S1_CaoCap.png` | Chương 7 (tr. 31-33) | Khánh | Đạt |
| **7** | Ít nhất 2 báo cáo xem trên màn hình, xuất file thực tế, nêu rõ ai tạo, gửi ai | **1,0** | R1 (Nhân viên kinh doanh lập -> Khách hàng, PDF A4 dọc 1 trang) & R2 (Nhân viên kế toán lập -> Ban Giám đốc, PDF A4 ngang 1 trang); có ô nhập người lập, dòng nơi nhận và khối chữ ký (`Hinh10` - `Hinh13`) | Chương 8 (tr. 34-38) | Tuân (R1 - 8.1)<br>Khánh (R2 - 8.2) | Thịnh |
| **8** | Báo cáo đủ các mục trên, kèm câu lệnh SQL của mục 5, 6, 7 | **1,0** | Câu lệnh SQL đặt ngay tại mục của từng màn hình (6.2.2, 6.3.2, 6.4, 7.2, 8.1.3, 8.2.3); nộp kèm 4 tệp SQL đầy đủ; bảng đối chiếu tiêu chí ở Lời mở đầu | Toàn bộ báo cáo | Thịnh (biên tập) | Tuân |

---

## Phần 3. Nền tảng Làm việc, Cấu trúc Dự án và Quy trình Git/GitHub Chi tiết

### I. Nền tảng và Công cụ Làm việc theo Vai trò

| Hạng mục công việc | Nền tảng / Phần mềm sử dụng | Đầu vào cần mở | Đầu ra lưu tại đâu |
| :--- | :--- | :--- | :--- |
| **1. Vẽ sơ đồ ERD** | Web `app.diagrams.net` hoặc ứng dụng **draw.io Desktop** | Hướng dẫn tại `docs/Huong_dan_chi_tiet_Dat.md` (Mục 3) | `docs/diagrams/ERD.drawio`, `docs/diagrams/ERD.png` và `screenshots/Hinh01_ERD_Chen.png` |
| **2. Dựng CSDL & Data Diagram** | **MySQL Server 8.0.16+** và **MySQL Workbench 8.0** | Hướng dẫn tại `docs/Huong_dan_chi_tiet_Khanh.md` (Mục 3 & Mục 7) | 4 file trong `database/`, `docs/diagrams/DataDiagram.mwb`, `DataDiagram.png`, `screenshots/Hinh02_DataDiagram_Workbench.png`, `Hinh03_MinhChung_RangBuoc.png` |
| **3. Lập trình Ứng dụng (`tour_app/`)** | **VS Code** (hoặc PyCharm) + **Python 3.11-3.13** + Terminal **PowerShell** | Code và SQL đầy đủ trong 4 file `docs/Huong_dan_chi_tiet_<Ten>.md` | Các file `.py` trong `tour_app/pages/` và `.html` trong `tour_app/templates/` |
| **4. Rà soát & Biên tập Báo cáo** | **Microsoft Word** (dành cho Thịnh) và trình soạn thảo Markdown (dành cho Đạt, Tuân, Khánh) | `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` + hướng dẫn tại `docs/Huong_dan_chi_tiet_Thinh.md` | Góp ý lưu tại `docs/GopY_<Ten>.md`; bản báo cáo chính thức lưu tại `docs/report/` |
| **5. Quản lý Mã nguồn & Phối hợp** | **Git** và **GitHub Repository** (`BTL-quan-ly-dat-tour-csdl-PTIT`) | Nhánh `main` và các nhánh `feature/...` | Pull Request trên GitHub |

### II. Cấu trúc Thư mục và Phân quyền Sở hữu File (Tránh Xung đột Git)

```text
BTL-quan-ly-dat-tour-csdl-PTIT/
├── README.md                                           [Chỉ Khánh sửa]
├── .gitignore                                          [Chỉ Khánh sửa]
├── database/
│   ├── 1_QuanLyDatTour_v3.sql                          [Chỉ Khánh sửa]
│   ├── 2_QuanLyDatTour_v3_TruyVan.sql                  [Chỉ Khánh sửa]
│   ├── 3_QuanLyDatTour_v3_UngDung.sql                  [Chỉ Khánh sửa]
│   └── 4_KiemTra_RangBuoc.sql                          [Chỉ Khánh sửa]
├── docs/
│   ├── Ke_hoach_Tong_hop_BTL_CSDL.md                   [Kế hoạch tổng thể chung toàn nhóm]
│   ├── Huong_dan_chi_tiet_Khanh.md                     [Sổ tay hướng dẫn chi tiết của Khánh]
│   ├── Huong_dan_chi_tiet_Dat.md                       [Sổ tay hướng dẫn chi tiết của Đạt]
│   ├── Huong_dan_chi_tiet_Tuan.md                      [Sổ tay hướng dẫn chi tiết của Tuân]
│   ├── Huong_dan_chi_tiet_Thinh.md                     [Sổ tay hướng dẫn chi tiết của Thịnh]
│   ├── GopY_Dat.md / GopY_Tuan.md / GopY_Khanh.md      [Mỗi người tự tạo file góp ý của mình]
│   ├── diagrams/
│   │   ├── ERD.drawio, ERD.png                         [Chỉ Đạt sửa]
│   │   └── DataDiagram.mwb, DataDiagram.png            [Chỉ Khánh sửa]
│   └── report/
│       └── Bao_cao_BTL_CSDL_QuanLyDatTour.docx         [CHỈ THỊNH SỬA TRỰC TIẾP]
├── tour_app/
│   ├── app.py                                          [Chỉ Khánh sửa]
│   ├── db.py                                           [Chỉ Khánh sửa - ai cần thêm hàm thì nhắn Khánh]
│   ├── requirements.txt                                [Chỉ Khánh sửa]
│   ├── pages/
│   │   ├── 1_Dat_tour.py                               [Chỉ Đạt sửa - Nhánh feature/f1-dat-tour]
│   │   ├── 2_Quan_ly_don.py                            [Chỉ Tuân sửa - Nhánh feature/f2-quan-ly-don]
│   │   ├── 3_Danh_gia.py                               [Chỉ Thịnh sửa - Nhánh feature/f3-danh-gia]
│   │   ├── 4_Tim_kiem.py                               [Chỉ Khánh sửa - Nhánh feature/s1-tim-kiem]
│   │   ├── 5_Phieu_xac_nhan.py                         [Chỉ Tuân sửa - Nhánh feature/r1-phieu-xac-nhan]
│   │   └── 6_Bao_cao_doanh_thu.py                      [Chỉ Khánh sửa - Nhánh feature/r2-bao-cao-doanh-thu]
│   └── templates/
│       ├── phieu_xac_nhan.html                         [Chỉ Tuân sửa - Nhánh feature/r1-phieu-xac-nhan]
│       └── bao_cao_doanh_thu.html                      [Chỉ Khánh sửa - Nhánh feature/r2-bao-cao-doanh-thu]
└── screenshots/
    ├── Hinh01_ERD_Chen.png, Hinh04_F1_GiaoDien.png, Hinh05a_F1_Loi1.png, Hinh05b_F1_Loi2.png [Đạt thêm]
    ├── Hinh02_DataDiagram_Workbench.png, Hinh03_MinhChung_RangBuoc.png, Hinh09_S1_GiaoDien.png [Khánh thêm]
    ├── Hinh12_R2_ManHinh.png, Hinh13_R2_PDF.png                                              [Khánh thêm]
    ├── Hinh06_F2_GiaoDien.png, Hinh07_F2_Loi.png, Hinh10_R1_ManHinh.png, Hinh11_R1_PDF.png   [Tuân thêm]
    └── Hinh08_F3_GiaoDien.png                                                                [Thịnh thêm]
```

### III. Hướng dẫn Git & GitHub Từng bước cho Tất cả Thành viên

#### Bước 1: Thiết lập lần đầu trên máy cá nhân (Mỗi thành viên làm 1 lần)
1. Mở **PowerShell** tại thư mục muốn lưu dự án, clone repository về máy:
   ```powershell
   git clone https://github.com/NgQKhanh2906/BTL-quan-ly-dat-tour-csdl-PTIT.git
   cd BTL-quan-ly-dat-tour-csdl-PTIT
   ```
2. Mở **MySQL Workbench 8.0**, mở file `database/1_QuanLyDatTour_v3.sql` và nhấn `Ctrl + Shift + Enter` để tạo CSDL `QuanLyDatTour` (12 bảng, 2 view, 104 dòng dữ liệu mẫu).
3. Tạo môi trường ảo Python và cài đặt thư viện trong PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r tour_app\requirements.txt
   ```
4. Thiết lập biến môi trường lưu mật khẩu `root` của MySQL trên máy cá nhân (tuyệt đối không sửa mật khẩu trực tiếp vào file `db.py`):
   ```powershell
   setx MYSQL_PASSWORD "mat_khau_mysql_cua_may_ban"
   ```
   *(Sau lệnh `setx`, đóng cửa sổ PowerShell hiện tại và mở lại cửa sổ PowerShell mới để biến môi trường có hiệu lực).*
5. Chạy thử ứng dụng để kiểm tra kết nối:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   cd tour_app
   streamlit run app.py
   ```
   Nếu trình duyệt mở `http://localhost:8501` và báo `"Đã kết nối cơ sở dữ liệu: 12 bảng"` là môi trường đã sẵn sàng.

#### Bước 2: Quy trình làm việc hàng ngày và Push Code lên GitHub
Mỗi khi bắt đầu làm một task code hoặc cập nhật hình ảnh/góp ý, thực hiện đúng 5 lệnh sau tại thư mục gốc của dự án:

1. **Lấy code mới nhất từ nhánh `main` về máy:**
   ```powershell
   git checkout main
   git pull origin main
   ```
2. **Chuyển sang nhánh tính năng của màn hình mình phụ trách** (nếu nhánh chưa có trên máy thì thêm cờ `-b`, nếu đã có thì bỏ `-b`):
   - **Đạt (F1):** `git checkout -b feature/f1-dat-tour`
   - **Tuân (F2):** `git checkout -b feature/f2-quan-ly-don`
   - **Tuân (R1):** `git checkout -b feature/r1-phieu-xac-nhan`
   - **Thịnh (F3):** `git checkout -b feature/f3-danh-gia`
   - **Khánh (S1):** `git checkout -b feature/s1-tim-kiem`
   - **Khánh (R2):** `git checkout -b feature/r2-bao-cao-doanh-thu`
   - Khi sửa lỗi sau kiểm thử chéo: `git checkout -b fix/ten-loi` (ví dụ: `git checkout -b fix/f1-kiem-tra-so-phong`)
3. **Viết code, chạy kiểm thử trên Streamlit và kiểm tra ràng buộc CSDL:**
   - Mở `database/1_QuanLyDatTour_v3.sql` chạy lại để reset dữ liệu gốc.
   - Chạy hết các ca kiểm thử của màn hình mình.
   - Mở `database/4_KiemTra_RangBuoc.sql` chạy trên Workbench: kết quả phải trả về **0 dòng** (rỗng).
4. **Kiểm tra các file đã thay đổi và Commit theo chuẩn Conventional Commits:**
   ```powershell
   git status
   git add <duong_dan_file_cua_minh>
   git commit -m "<loai>: <mo_ta_ngan_gon_khong_dau>"
   ```
   *Ví dụ cụ thể:*
   - Đạt: `git add tour_app/pages/1_Dat_tour.py` -> `git commit -m "feat: hoan thien form dat tour F1 va kiem tra 6 ca nghiem thu"`
   - Tuân: `git add tour_app/pages/5_Phieu_xac_nhan.py tour_app/templates/phieu_xac_nhan.html` -> `git commit -m "feat: them nhan vien lap phieu va khoi ky cho R1"`
   - Thịnh: `git add tour_app/pages/3_Danh_gia.py` -> `git commit -m "feat: hoan thien form danh gia sau chuyen di F3"`
   - Khánh: `git add tour_app/pages/6_Bao_cao_doanh_thu.py tour_app/templates/bao_cao_doanh_thu.html` -> `git commit -m "feat: them nguoi lap va noi nhan cho bao cao doanh thu"`
   *(Lưu ý: Không dùng `git add .` nếu trong máy có file nháp ngoài phạm vi nhiệm vụ; không ghi dòng Co-authored-by công cụ AI trong commit message).*
5. **Đẩy nhánh lên GitHub và tạo Pull Request:**
   ```powershell
   git push -u origin <ten_nhanh_cua_minh>
   ```
   Sau khi push, lên giao diện web GitHub của repo -> bấm **Compare & pull request** -> bấm **Create pull request** và nhắn vào nhóm để Khánh review, chạy thử và **Merge** vào nhánh `main`.

---

## Phần 4. Lộ trình Tổng thể theo Ngày (6 Cụm: 05/11 - 22/11/2026) và Lịch Họp Nhóm

### I. Lộ trình Thực thi Chi tiết theo Từng Đợt 3 Ngày

| Cụm | Thời gian | Mục tiêu trọng tâm của Cụm | Nhiệm vụ của ĐẠT | Nhiệm vụ của THỊNH | Nhiệm vụ của TUÂN | Nhiệm vụ của KHÁNH | Mốc kiểm soát cuối Cụm |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cụm 1** | **T5 05/11 - T7 07/11** | Chốt CSDL 12 bảng, khung `tour_app`, ERD bản cuối, nhận file báo cáo `.docx` | **05-06/11 (`D1`):** Sửa ERD thêm `TheThanhToan`, `ThanhToanBang`, xuất `Hinh01_ERD.png`.<br>**06/11 (`D2`):** Báo cáo tiến độ F1 tại họp H1. | **05/11 (`TH1`):** Nhận báo cáo `.docx`, lưu `v0.6`, cập nhật mục lục.<br>**06-07/11 (`TH2`):** Rà mục 2.1, 3.3, 3.4 khớp tệp SQL số 1, lập `docs/GopY_Thinh.md`. | **05-06/11 (`TU1`):** Nhắn hỏi giảng viên 4 ý về nộp bài & lịch bảo vệ.<br>**06-07/11 (`TU2`):** Rà Chương 1, mục 2.2, Chương 9, lập `docs/GopY_Tuan.md`. | **05/11 (`K1`):** Gửi báo cáo nháp cho Thịnh.<br>**05-06/11 (`K2`):** Hoàn thiện 4 tệp SQL (12 bảng), `db.py`, `app.py`.<br>**07/11 (`K3`):** Đẩy lên GitHub, hỗ trợ 3 bạn chạy trang chủ. | **Tối T6 06/11 (Họp H1):** Chốt hiện trạng từng màn hình.<br>**07/11:** 4 máy đều chạy được CSDL 12 bảng và trang chủ. |
| **Cụm 2** | **CN 08/11 - T3 10/11** | Hoàn thành code cả 6 màn hình (`F1`, `F2`, `F3`, `S1`, `R1`, `R2`) và `DataDiagram` | **08-10/11 (`D3`):** Code hoàn chỉnh `pages/1_Dat_tour.py`, vượt qua đủ 6 ca kiểm thử ở báo cáo (8 ca ở Quyển 5), tạo đơn `DH015` gửi Tuân. | **08-09/11 (`TH3`):** Code `pages/3_Danh_gia.py` vượt qua đủ 3 ca kiểm thử ở báo cáo (6 ca ở Quyển 5).<br>**10/11 (`TH4`):** Rà Chương 4 chuẩn hóa 3NF, chạy SQL ghép bảng. | **08-09/11 (`TU3`):** Code `pages/2_Quan_ly_don.py` đạt 5 ca kiểm thử.<br>**09-10/11 (`TU4`, `TU5`):** Thêm "Nhân viên lập phiếu" vào R1, kiểm tra in PDF `DH007`, `DH008` vừa 1 trang A4 dọc. | **08-09/11 (`K4`, `K5`):** Hoàn thiện `4_Tim_kiem.py` (6 ca) & `6_Bao_cao_doanh_thu.py` (thêm người lập, nơi nhận, khối ký; tổng cộng `79.110.000 đ`).<br>**10/11 (`K6`):** Reverse Engineer xuất `DataDiagram.mwb` & `Hinh02_DataDiagram.png`. | **Tối T3 10/11 (Họp H2):** Cả 6 màn hình chạy thông suốt và đạt các ca nghiệm thu. |
| **Cụm 3** | **T4 11/11 - T6 13/11** | Chụp đủ 13 hình chuẩn; hoàn tất rà soát SQL và nội dung báo cáo gửi Thịnh | **11/11 (`D4`):** Reset DB, chụp `Hinh04_F1_GiaoDien.png`, `Hinh05a_F1_Loi.png`, `Hinh05b_F1_Loi.png`.<br>**12-13/11 (`D5`):** Rà mục 2.3, 3.1, 3.2, 6.2 lập `docs/GopY_Dat.md` gửi Thịnh. | **11/11 (`TH5`):** Reset DB, chụp `Hinh08_F3_GiaoDien.png`, rà mục 6.4.<br>**12-13/11:** Kiểm tra định dạng 13 ảnh do các bạn gửi về. | **11/11 (`TU6`):** Reset DB, chụp `Hinh06`, `Hinh07`, `Hinh10`, `Hinh11`.<br>**12/11 (`TU6`):** Rà mục 6.3, 8.1 cập nhật `docs/GopY_Tuan.md`.<br>**13/11 (`TU7`):** Thu thập họ tên, MSSV, % đóng góp cả nhóm gửi Thịnh. | **11/11 (`K7`):** Chụp `Hinh03_LoiRangBuoc.png`, `Hinh09`, `Hinh12`, `Hinh13`; thử nghiệm sửa `LT07` kiểm tra `RB26`.<br>**12-13/11 (`K8`):** Rà mục 3.5, Ch.5, Ch.7, mục 8.2, Phụ lục lập `docs/GopY_Khanh.md`. | **23:00 T6 13/11:** Thịnh nhận đủ 13 hình trong `screenshots/` và đủ 4 file `GopY_<Ten>.md` + thông tin MSSV. |
| **Cụm 4** | **T7 14/11 - T2 16/11** | Kiểm thử chéo, sửa lỗi, chèn 13 hình vào báo cáo, làm Slide, **Đóng băng tính năng** | **14/11 (`D6`):** Kiểm thử chéo `S1`, `R2` của Khánh.<br>**15/11:** Sửa lỗi `F1` do Thịnh báo.<br>**16/11 (`D7`):** Đối chiếu tên bảng, cột giữa ERD, Data Diagram, báo cáo, code. | **14/11 (`TH6`):** Kiểm thử chéo `F1` của Đạt.<br>**15/11 (`TH7`):** Sửa lỗi `F3`; áp dụng toàn bộ góp ý vào báo cáo `v0.8`.<br>**16/11 (`TH8`):** Chèn 13 hình, điền hết ô vàng Highlight, lưu `v0.9` (<= 50 trang). | **14/11 (`TU8`):** Kiểm thử chéo `F3` của Thịnh.<br>**15/11:** Sửa lỗi `F2`, `R1` do Khánh báo.<br>**16/11 (`TU9`):** Làm slide thuyết trình 8 trang `Slide_Nhom.pptx`. | **14/11 (`K9`):** Kiểm thử chéo `F2`, `R1` của Tuân.<br>**15/11:** Sửa lỗi `S1`, `R2` do Đạt báo.<br>**16/11 (`K10`):** Merge toàn bộ PR vào `main`, hoàn thiện `README.md` bản cuối. | **Tối T2 16/11 (Họp H3):** **Đóng băng tính năng**; duyệt báo cáo `v0.9` đã chèn đủ 13 hình và hết ô vàng. |
| **Cụm 5** | **T3 17/11 - T5 19/11** | Kiểm thử máy sạch, đọc soát cuối, xuất Báo cáo `v1.0`, đóng gói bộ nộp, Tập bảo vệ lần 1 | **17/11 (`D8`):** Cài thử từ đầu trên máy sạch theo đúng Phụ lục báo cáo.<br>**18/11 (`D9`):** Xuất `ERD.drawio` và `ERD.png` độ phân giải cao.<br>**19/11:** Tập thuyết trình lần 1 (H4). | **17-18/11 (`TH9`):** Sửa theo đọc soát của Tuân, cập nhật mục lục tự động, xuất `v1.0` (`.docx` & `.pdf` có Bookmarks).<br>**19/11:** Tập thuyết trình lần 1 (H4). | **17-18/11 (`TU10`):** Đọc soát toàn bộ báo cáo `v0.9` (chính tả, số trang, SQL, chú thích hình/bảng).<br>**19/11:** Bấm giờ buổi tập thuyết trình lần 1 (H4). | **17-18/11 (`K11`):** Đóng gói thư mục nộp (`CSDL/`, `UngDung/tour_app.zip`, `ThietKe/`, `README.txt`); giải nén chạy thử.<br>**19/11 (`K12`):** Tập điều khiển demo lần 1 (H4). | **Tối T5 19/11 (Họp H4):** Có Báo cáo `v1.0` (`.docx`, `.pdf`) và gói nộp hoàn chỉnh; hoàn thành tập bảo vệ lần 1 (<= 13 phút). |
| **Cụm 6** | **T6 20/11 - CN 22/11** | Quay video demo dự phòng, Tập bảo vệ lần 2, Nộp bài lên Google Drive của giảng viên | **20-21/11:** Tập nhuần nhuyễn phần trình bày ERD và câu hỏi vấn đáp; chuẩn bị laptop dự phòng (đã cài ở `D8`). | **20-21/11 (`TH10`):** Sửa lỗi nhỏ cuối cùng (nếu có), xuất file PDF/DOCX đặt tên đúng quy định của giảng viên. | **21/11:** Tập bảo vệ lần 2 (H5).<br>**Trước 21:00 CN 22/11 (`TU11`):** Tải bộ file lên Google Drive của giảng viên, kiểm tra bằng tab ẩn danh, chụp ảnh xác nhận. | **20/11 (`K12`):** Quay video demo dự phòng 6 phút bằng Xbox Game Bar (`Win + Alt + R`).<br>**21/11:** Đặt bộ file nộp lên thư mục chung trước 20:00; tập bảo vệ lần 2 (H5). | **20:00 T7 21/11:** Đủ bộ file nộp.<br>**Trước 21:00 CN 22/11:** Hoàn tất nộp bài trên Drive giảng viên. |

### II. Lịch 5 Buổi Họp Nhóm và Bảng Phụ thuộc ("Ai cần gì từ ai")

#### 1. Lịch 5 buổi họp nhóm bắt buộc
- **Buổi H1 (Tối T6 06/11, 30 phút):** Mỗi người mở màn hình mình phụ trách chạy thử 1 ca đúng và 1 ca sai; chốt màn hình nào cần hỗ trợ trong Cụm 2.
- **Buổi H2 (Tối T3 10/11, 20 phút):** Nghiệm thu mốc "6 màn hình chạy được"; chốt phần trăm đóng góp của 4 thành viên.
- **Buổi H3 (Tối T2 16/11, 30 phút):** Đóng băng tính năng; duyệt báo cáo bản `v0.9` đã chèn 13 hình và điền hết ô vàng.
- **Buổi H4 (Tối T5 19/11, 60 phút):** Tập thuyết trình và demo lần 1 có bấm giờ (mục tiêu <= 13 phút, dành 2 phút hỏi đáp).
- **Buổi H5 (Tối T7 21/11, 60 phút):** Tập thuyết trình lần 2; kiểm tra toàn bộ bộ file nộp lần cuối trước khi Tuân tải lên Drive của giảng viên.

#### 2. Bảng phụ thuộc bàn giao giữa các thành viên

| Người nhận | Người giao | Sản phẩm bàn giao | Hạn chót bàn giao |
| :--- | :--- | :--- | :--- |
| Thịnh | Khánh | File báo cáo `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` | **05/11/2026** |
| Đạt, Thịnh, Tuân | Khánh | Tệp `database/1_QuanLyDatTour_v3.sql` bản chốt (12 bảng), `tour_app/db.py`, `tour_app/app.py` | **07/11/2026** |
| Khánh | Đạt | Sơ đồ `docs/diagrams/ERD.drawio` và `ERD.png` bản cuối (có `TheThanhToan`) để đối chiếu `DataDiagram` | **07/11/2026** |
| Tuân (`R1`) | Đạt (`F1`) | Đơn `DH015` tạo thành công từ màn hình `F1` để kiểm thử in phiếu xác nhận `R1` | **10/11/2026** |
| Thịnh | Đạt, Tuân, Khánh | Đủ 13 file ảnh trong `screenshots/` đặt tên đúng chuẩn và các file góp ý `docs/GopY_<Ten>.md` | **13/11/2026** |
| Thịnh | Tuân | Họ tên đầy đủ, MSSV và tỷ lệ % đóng góp của cả 4 thành viên (tổng 100%) | **13/11/2026** |
| Tuân | Thịnh, Khánh | Báo cáo bản `1.0` (`.docx`, `.pdf`) và bộ file đóng gói (`CSDL/`, `ThietKe/`, `UngDung/tour_app.zip`, `README.txt`) | **19/11/2026** |

---

## Phần 5. Nhiệm vụ Cụ thể Từng Thành viên (Chi tiết Từng Bước Làm, Nền tảng, Kiểm thử và Lệnh Push Code)

---

### I. NHIỆM VỤ CHI TIẾT CỦA KHÁNH (`K1` -> `K12`)

- **Vai trò:** Phụ trách Cơ sở dữ liệu (4 tệp SQL), Sơ đồ `DataDiagram`, Nền tảng ứng dụng (`db.py`, `app.py`, `requirements.txt`), Màn hình Tìm kiếm (`S1`), Báo cáo Doanh thu (`R2`), Quản lý GitHub Repository, Máy chạy Demo và Báo cáo mục 3.5, Chương 5, Chương 7, mục 8.2, Phụ lục.

#### 1. Đợt 1 — Cụm 1 (05/11 - 07/11): Tasks `K1`, `K2`, `K3`
- **Nền tảng làm việc:** MySQL Workbench 8.0, VS Code, PowerShell, GitHub.
- **Các bước thực hiện cụ thể:**
  1. **Task `K1` (05/11):** Đưa file báo cáo `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` lên thư mục chung / GitHub để Thịnh nhận làm bản `v0.6`.
  2. **Task `K2` — Phần CSDL (05/11 - 06/11):** Mở MySQL Workbench, tạo đủ 4 tệp SQL trong thư mục `database/` theo đúng hướng dẫn và toàn bộ mã SQL tại `docs/Huong_dan_chi_tiet_Khanh.md` (Mục 3):
     - `database/1_QuanLyDatTour_v3.sql`: Tạo database `QuanLyDatTour` (`utf8mb4_0900_ai_ci`), 12 bảng theo thứ tự (`TinhThanh`, `TheThanhToan`, `KhachHang`, `SDT_KhachHang`, `Tour`, `LichTrinh`, `NhaNghi`, `DonViVanTai`, `Xe`, `TrangThaiDonHang`, `DonHang`, `ChuyenTrungChuyen`), 56 ràng buộc (`12 PK`, `13 FK`, `27 CHECK`, `4 UNIQUE`), 2 view (`v_DonHang_ChiTiet`, `v_LichTrungChuyen`) và chèn 104 dòng dữ liệu mẫu (gồm 5 dòng `TheThanhToan` và 99 dòng của 11 bảng còn lại).
     - `database/2_QuanLyDatTour_v3_TruyVan.sql`: Gồm 13 câu truy vấn minh họa tại Quyển 4 Phần 7.
     - `database/3_QuanLyDatTour_v3_UngDung.sql`: Gồm toàn bộ các khối SQL của F1, F2, F3, S1, R1, R2 tại Quyển 5.
     - `database/4_KiemTra_RangBuoc.sql`: Gồm khối truy vấn `UNION ALL` kiểm tra các ràng buộc liên bảng từ `RB22` đến `RB32` (trong đó `RB32` kiểm tra mọi thẻ trong `TheThanhToan` phải có khách sử dụng).
  3. **Task `K2` — Phần Khung Ứng dụng (06/11):** Tạo trong `tour_app/`:
     - `tour_app/requirements.txt`: Khai báo `streamlit==1.66.0`, `mysql-connector-python==26.7.0`, `pandas==3.0.6`.
     - `tour_app/db.py`: Chép mã nguồn từ Quyển 5 Phần 1 mục VI, sửa khóa `"password"` trong `CAU_HINH` thành `os.environ.get("MYSQL_PASSWORD", "")` (import `os` ở đầu file) để đọc mật khẩu từ biến môi trường; giữ `CHE_DO_DEMO = True` và `HIEN_TAI_DEMO = datetime(2026, 10, 23, 8, 0, 0)`.
     - `tour_app/app.py`: Trang chủ hiển thị tiêu đề hệ thống, kiểm tra kết nối MySQL và in thông báo `"Đã kết nối cơ sở dữ liệu: 12 bảng"`.
  4. **Task `K3` (07/11):** Đẩy 4 tệp SQL và khung `tour_app/` lên nhánh `main` của GitHub; nhắn Đạt, Thịnh, Tuân pull về và kiểm tra cả 3 máy đều mở được trang chủ.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git add database/ tour_app/app.py tour_app/db.py tour_app/requirements.txt README.md
  git commit -m "feat: khoi tao 4 tep SQL 12 bang va khung ung dung tour_app"
  git push origin main
  ```

#### 2. Đợt 2 — Cụm 2 (08/11 - 10/11): Tasks `K4`, `K5`, `K6`
- **Nền tảng làm việc:** VS Code, Streamlit, MySQL Workbench 8.0.
- **Các bước thực hiện cụ thể:**
  1. **Task `K4` — Màn hình Tìm kiếm S1 (08/11):**
     - Tạo nhánh `git checkout -b feature/s1-tim-kiem`.
     - Viết `tour_app/pages/4_Tim_kiem.py` theo Quyển 5 Phần 5: gồm 8 bộ lọc (Từ khóa tên tour, Tỉnh đến, Giá từ, Giá đến, Khởi hành từ ngày mặc định `23/10/2026`, Khởi hành đến ngày, Số khách mặc định `1`, Điểm đánh giá tối thiểu) và 1 nút bấm nhanh `"Tour cao cấp (từ 10 triệu)"`.
     - Chạy kiểm thử đủ 6 ca tại mục 7.3 báo cáo (Quyển 5 Phần 5 mục IV):
       - Ca 1 (Giá từ `10.000.000`): Ra 3 lịch trình `LT08` (`11.500.000 đ`), `LT09` (`10.800.000 đ`), `LT12` (`12.900.000 đ`).
       - Ca 2 (Từ khóa `"ha long"`, `2` khách): Ra `LT04` (điểm `4,5`, `2` lượt), `LT08`, `LT12`.
       - Ca 3 (Tỉnh đến `Lào Cai`, giá đến `4.000.000`, đến `31/12/2026`, `4` khách, điểm từ `4,5`): Ra `LT05` (điểm `5,0`).
       - Ca 4 (Giá từ `20.000.000`): Hiện thông báo không có lịch trình phù hợp.
       - Ca 5 (Giá từ `5.000.000`, giá đến `1.000.000`): Báo lỗi `"Giá đến phải lớn hơn hoặc bằng giá từ"`.
       - Ca 6 (Từ khóa `"du thuyen"`, đến `30/11/2026`, `11` khách): Báo không có kết quả (`LT08` chỉ còn 10 chỗ).
  2. **Task `K4` & `K5` — Báo cáo Doanh thu R2 có Người lập, Nơi nhận, Khối ký (09/11):**
     - Tạo nhánh `git checkout -b feature/r2-bao-cao-doanh_thu`.
     - Viết `tour_app/pages/6_Bao_cao_doanh_thu.py` và `tour_app/templates/bao_cao_doanh_thu.html` theo Quyển 5 Phần 7, sau đó áp dụng 5 điểm cập nhật của `K5`:
       - Khai báo hằng số `NOI_NHAN = "Ban Giám đốc công ty du lịch"`.
       - Thêm ô nhập `nguoi_lap = st.text_input("Người lập báo cáo", max_chars=100, placeholder="Họ tên nhân viên kế toán")` và `st.caption(f"Nơi nhận: {NOI_NHAN}")`.
       - Sau phần hiển thị bảng trên màn hình, kiểm tra: nếu `not nguoi_lap.strip()` thì hiện `st.warning("Nhập tên người lập báo cáo để tải và in báo cáo")` và gọi `st.stop()`.
       - Truyền `nguoi_lap=escape(nguoi_lap.strip())` và `noi_nhan=NOI_NHAN` vào hàm `mau.substitute(...)`.
       - Trong `tour_app/templates/bao_cao_doanh_thu.html`: chỉnh `body { font-size: 9pt; }`, `.chi-so { margin-bottom: 8px; }`, `.o { padding: 4px 8px; }`, `.ghi-chu { margin-top: 8px; font-size: 8.5pt; }`; thêm dòng `<div class="nguoi-lap">Người lập: $nguoi_lap | Nơi nhận: $noi_nhan</div>` dưới kỳ báo cáo và thêm khối `<div class="ky-ten">` gồm 2 cột ký `"Người lập báo cáo"` và `"Ban Giám đốc duyệt"` ngay trước `</body>`.
     - Kiểm thử 4 ca của `K5`:
       - Kỳ mặc định `01/09/2026` đến `31/12/2026`: 4 ô tổng hiện đúng `79.110.000 đ`, `10` đơn, `26` khách, `4` đơn hủy.
       - Để trống người lập: hiện cảnh báo vàng, không hiện nút tải.
       - Nhập `<b>Test</b>`: file HTML tải về hiển thị nguyên chuỗi `<b>Test</b>` (chống HTML injection).
       - Nhập tên thật, tải HTML, mở bằng Edge nhấn `Ctrl + P` in ra PDF khổ **A4 ngang (Landscape)**: vừa khít 1 trang, đủ người lập, nơi nhận và 2 ô ký.
  3. **Task `K6` — Tạo Sơ đồ Data Diagram (10/11):**
     - Mở MySQL Workbench -> chọn `Database > Reverse Engineer` (`Ctrl + R`) -> chọn schema `QuanLyDatTour` (chỉ tích chọn Tables, bỏ chọn Views).
     - Sắp xếp 12 bảng thành 4 cụm rõ ràng, không đè đường nối:
       - Cụm Khách hàng: `TinhThanh`, `TheThanhToan`, `KhachHang`, `SDT_KhachHang`.
       - Cụm Tour: `Tour`, `LichTrinh`.
       - Cụm Đối tác: `NhaNghi`, `DonViVanTai`, `Xe`.
       - Cụm Đơn hàng: `TrangThaiDonHang`, `DonHang`, `ChuyenTrungChuyen`.
     - Đếm đủ **12 hộp bảng, 13 đường nối khóa ngoại** (trong đó có 2 đường liền xác định nối vào `SDT_KhachHang` và `ChuyenTrungChuyen`).
     - Lưu file `docs/diagrams/DataDiagram.mwb`, xuất ảnh `docs/diagrams/DataDiagram.png` và chép 1 bản thành `screenshots/Hinh02_DataDiagram.png`.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout feature/s1-tim-kiem
  git add tour_app/pages/4_Tim_kiem.py
  git commit -m "feat: hoan thien man hinh tim kiem lich trinh S1"
  git push -u origin feature/s1-tim-kiem

  git checkout -b feature/r2-bao-cao-doanh-thu main
  git add tour_app/pages/6_Bao_cao_doanh_thu.py tour_app/templates/bao_cao_doanh_thu.html
  git commit -m "feat: them nguoi lap va noi nhan cho bao cao doanh thu"
  git push -u origin feature/r2-bao-cao-doanh-thu

  git checkout main
  git merge feature/s1-tim-kiem feature/r2-bao-cao-doanh-thu
  git add docs/diagrams/DataDiagram.mwb docs/diagrams/DataDiagram.png screenshots/Hinh02_DataDiagram.png
  git commit -m "docs: them DataDiagram 12 bang 13 khoa ngoai"
  git push origin main
  ```

#### 3. Đợt 3 — Cụm 3 (11/11 - 13/11): Tasks `K7`, `K8`
- **Nền tảng làm việc:** MySQL Workbench 8.0, Trình duyệt Microsoft Edge (zoom 100%, rộng ~1400px), Paint, VS Code.
- **Các bước thực hiện cụ thể:**
  1. **Task `K7` — Chụp Hình 3, 9, 12, 13 và Thử nghiệm Tệp 4 (11/11):**
     - Chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc.
     - **Chụp `screenshots/Hinh03_LoiRangBuoc.png`:** Mở tab SQL mới trong Workbench, chạy lần lượt 4 câu lệnh cố tình vi phạm: (1) trùng khóa chính mã lỗi `1062`, (2) vi phạm `CHECK` mã lỗi `3819`, (3) thêm khóa ngoại không tồn tại mã lỗi `1452`, (4) xóa dòng cha đang được tham chiếu mã lỗi `1451`. Chụp vùng khung `Action Output` hiển thị 4 dòng báo lỗi màu đỏ.
     - **Kiểm tra phát hiện lỗi của Tệp 4 (mô tả ở cuối mục 5.5 báo cáo):** Chạy `UPDATE LichTrinh SET SoChoDaDat = 5 WHERE MaLichTrinh = 'LT07';` -> chạy `database/4_KiemTra_RangBuoc.sql` xác nhận trả về đúng 1 dòng `"RB26 Số chỗ đã đặt khớp với đơn - LT07"` -> chạy lại tệp 1 để khôi phục dữ liệu -> chạy lại tệp 4 xác nhận trả về rỗng.
     - **Chụp `screenshots/Hinh09_S1_CaoCap.png`:** Mở trang Tìm kiếm `S1`, bấm nút `"Tour cao cấp (từ 10 triệu)"`, chụp màn hình hiển thị 3 dòng `LT08`, `LT09`, `LT12`.
     - **Chụp `screenshots/Hinh12_R2_ManHinh.png`:** Mở trang Báo cáo doanh thu `R2` (kỳ `01/09/2026` - `31/12/2026`), nhập tên người lập, chụp giao diện trên màn hình.
     - **Chụp `screenshots/Hinh13_R2_PDF.png`:** Tải báo cáo R2, in ra PDF khổ A4 ngang, mở file PDF trên Microsoft Edge ở chế độ `"Fit to page"` (Vừa trang), chụp trọn trang PDF có dòng người lập, nơi nhận và 2 ô ký.
  2. **Task `K8` — Rà soát Báo cáo phần của Khánh (12/11 - 13/11):**
     - Đọc kỹ mục 3.5, Chương 5, Chương 7, mục 8.2 và Phụ lục trong `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`.
     - Đối chiếu số đếm ràng buộc (`12 PK`, `13 FK`, `27 CHECK`, `4 UNIQUE`), số dòng mẫu (`104`), các câu lệnh SQL và các bước cài đặt trong Phụ lục.
     - Ghi các điểm cần chỉnh sửa (nếu có) vào `docs/GopY_Khanh.md` theo bảng mẫu (`Trang | Mục | Đang ghi | Sửa thành | Lý do`).
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add screenshots/Hinh03_LoiRangBuoc.png screenshots/Hinh09_S1_CaoCap.png screenshots/Hinh12_R2_ManHinh.png screenshots/Hinh13_R2_PDF.png docs/GopY_Khanh.md
  git commit -m "docs: them hinh chup Hinh 3, 9, 12, 13 va gop y bao cao cua Khanh"
  git push origin main
  ```

#### 4. Đợt 4, 5, 6 — Cụm 4 đến Cụm 6 (14/11 - 22/11): Tasks `K9`, `K10`, `K11`, `K12`
- **Task `K9` (14/11 - Kiểm thử chéo F2 & R1 của Tuân):** Chạy lại tệp SQL số 1, kiểm tra đủ 5 ca của `F2` (mục 6.3.3 báo cáo) và 3 điểm nghiệm thu của `R1` (mục 8.1.3 báo cáo: `DH007`, `DH008`, bỏ trống tên người lập, in A4 dọc 1 trang). Ghi lỗi gửi Tuân.
- **Task `K10` (15/11 - 16/11):** Sửa lỗi `S1`, `R2` (nếu Đạt phát hiện khi kiểm thử chéo), merge toàn bộ nhánh của Đạt, Thịnh, Tuân vào `main`, rà lại `README.md` bản cuối để đóng băng tính năng vào tối 16/11.
- **Task `K11` (17/11 - 19/11 - Đóng gói bộ file nộp):** Tạo thư mục đóng gói chuẩn theo Phần 6 của tài liệu này (`CSDL/`, `ThietKe/`, `UngDung/tour_app.zip` không chứa `.venv` và `__pycache__`, `README.txt`). Giải nén thử `tour_app.zip` sang một thư mục độc lập và chạy kiểm tra.
- **Task `K12` (20/11 - 22/11 - Máy Demo & Video Dự phòng):** Chạy lại tệp SQL số 1, bật trình duyệt thu phóng `125%`, bật Xbox Game Bar (`Win + Alt + R`) quay video chạy trọn vẹn 8 bước demo trong 6 phút, lưu vào máy và tải lên Drive nhóm trước 20:00 ngày 21/11.

---

### II. NHIỆM VỤ CHI TIẾT CỦA ĐẠT (`D1` -> `D9`)

- **Vai trò:** Phụ trách Sơ đồ `ERD` (`ERD.drawio`, `ERD.png`), Ánh xạ lược đồ quan hệ, Màn hình Form đặt tour (`F1` - `tour_app/pages/1_Dat_tour.py`) và Báo cáo mục 2.3, 3.1, 3.2, 6.2.

#### 1. Đợt 1 — Cụm 1 (05/11 - 07/11): Tasks `D1`, `D2`
- **Nền tảng làm việc:** `app.diagrams.net` (draw.io), VS Code, Streamlit.
- **Các bước thực hiện cụ thể:**
  1. **Task `D1` — Hoàn thiện ERD Bản cuối 11 Thực thể, 12 Mối liên kết (05/11 - 06/11):**
     - Mở `ERD.drawio`, thực hiện theo đúng hướng dẫn chi tiết từng bước tại `docs/Huong_dan_chi_tiet_Dat.md` (Mục 3):
       - Giữ 10 thực thể cũ và **bổ sung thực thể mạnh thứ 11 là `TheThanhToan`** gồm 2 thuộc tính: `SoID` (khóa chính — chữ gạch chân liền) và `LoaiThe` (thuộc tính thường).
       - Xóa 2 elip `SoID` và `LoaiThe` khỏi thực thể `KhachHang`.
       - Thêm mối liên kết thứ 12 là hình thoi `ThanhToanBang` nối giữa `TheThanhToan` (bản số `1`, đường đôi — tham gia toàn phần) và `KhachHang` (bản số `N`, đường đơn — tham gia một phần).
     - Kiểm tra kỹ 4 ký hiệu đặc biệt (rất dễ mất điểm Tiêu chí 2 nếu vẽ sai):
       - `ChuyenTrungChuyen`: hình chữ nhật **viền đôi** (thực thể yếu), nối với `DonHang` qua hình thoi **viền đôi** `CoChuyen`; thuộc tính `LoaiChuyen` gạch chân **nét đứt** (khóa bộ phận).
       - `SDT` của `KhachHang`: elip **viền đôi** (thuộc tính đa trị).
       - `SoDem` (của `LichTrinh`), `TongTien`, `TienPhat`, `TienHoan` (của `DonHang`): 4 elip **nét đứt** (thuộc tính dẫn xuất).
       - `DanhGiaTour` (gồm 2 elip con `DiemTour`, `NhanXetTour`) và `DanhGiaNhaNghi` (gồm 2 elip con `DiemNhaNghi`, `NhanXetNhaNghi`): nối từ `DonHang` qua elip cha rồi mới tới elip con (thuộc tính phức hợp).
       - Tuyệt đối không vẽ các thuộc tính khóa ngoại (`MaKH`, `MaLichTrinh`, `MaTrangThai`...) lên sơ đồ ERD.
     - Lưu file `docs/diagrams/ERD.drawio`. Chọn `File > Export as > PNG`, đặt `Zoom = 200%`, `Border Width = 10`, bỏ tích `Transparent Background` (để nền trắng), lưu thành `docs/diagrams/ERD.png` và `screenshots/Hinh01_ERD.png`.
  2. **Task `D2` (Tối 06/11):** Mở màn hình `F1` trong buổi họp H1, chạy thử ít nhất Ca 1 và báo cáo các phần còn vướng.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add docs/diagrams/ERD.drawio docs/diagrams/ERD.png screenshots/Hinh01_ERD.png
  git commit -m "docs: cap nhat so do ERD 11 thuc the 12 moi lien ket theo D6"
  git push origin main
  ```

#### 2. Đợt 2 — Cụm 2 (08/11 - 10/11): Task `D3`
- **Nền tảng làm việc:** VS Code, Streamlit, MySQL Workbench 8.0.
- **Các bước thực hiện cụ thể:**
  1. Tạo và chuyển sang nhánh `feature/f1-dat-tour`:
     ```powershell
     git checkout main
     git pull origin main
     git checkout -b feature/f1-dat-tour
     ```
  2. Viết hoàn chỉnh file `tour_app/pages/1_Dat_tour.py` theo đúng đặc tả và mã nguồn đầy đủ tại `docs/Huong_dan_chi_tiet_Dat.md` (Mục 4):
     - Sử dụng các hàm `doc`, `ghi`, `hien_tai`, `thong_bao_loi`, `dinh_dang_tien`, `dinh_dang_ngay` từ `db.py`.
     - Đặt ô chọn **Lịch trình** và ô chọn **Nơi nghỉ** ở **bên ngoài** `st.form` để khi đổi lịch trình thì danh sách nơi nghỉ tự lọc theo `MaTinhDen` (SQL `F1.3`), ẩn nơi nghỉ nếu `SoDem == 0`, cập nhật giới hạn `SoChoConLai` và tính lại **Tổng tiền dự kiến** (SQL `F1.5`) ngay lập tức.
     - Khi bấm `"Xác nhận đặt tour"`: kiểm tra dữ liệu tầng form (số phòng từ 1 đến số khách; nếu tích đón tại nhà thì bắt buộc nhập địa chỉ đón tối đa 255 ký tự và giờ đón phải sau `hien_tai()` nhưng trước `NgayXuatPhat`; nếu tích xe về nơi nghỉ thì giờ đón nằm trong khoảng từ `NgayXuatPhat` đến `NgayKetThuc`).
     - Sinh mã đơn mới bằng SQL `F1.4` (`DH015`) và gọi `ghi()` thực thi trong **1 Transaction** (SQL `F1.6`): `INSERT INTO DonHang`, `UPDATE LichTrinh SET SoChoDaDat = SoChoDaDat + %(SoKhach)s`, và `INSERT INTO ChuyenTrungChuyen` (0, 1 hoặc 2 chuyến).
  3. **Chạy kiểm thử nghiệm thu `F1` (sau khi chạy lại tệp SQL số 1):**
     - **Ca 1:** Chọn `KH006`, lịch trình `LT10`, `5` khách, nơi nghỉ `NN08`, `2` phòng, tích đón tại nhà `26/11/2026 15:00` (địa chỉ mặc định `3 Hùng Vương, Lào Cai`), tích xe về nơi nghỉ `27/11/2026 10:00` -> Bấm lưu báo `"Đã tạo đơn DH015, tổng tiền 32.020.000 đ"`. Kiểm tra trong Workbench: `DonHang` có `DH015` (5 khách, 2 phòng), `LichTrinh` `LT10` còn `15` chỗ, `ChuyenTrungChuyen` có 2 dòng của `DH015`.
     - **Ca 2:** Chọn `LT06` (tour trong ngày, `SoDem = 0`) -> tự động ẩn phần chọn nơi nghỉ và chuyến về nơi nghỉ.
     - **Ca 3:** Nhập `2` khách nhưng chọn `3` phòng -> Form chặn và báo lỗi.
     - **Ca 4:** Tích đón tại nhà nhưng xóa trống ô địa chỉ đón -> Form chặn và báo lỗi.
     - **Ca 5:** Chọn giờ đón tại nhà sau giờ xuất phát -> Form chặn và báo lỗi.
     - **Ca 6 (Kiểm tra lớp CSDL chặn khi form bị lọt):** Tạm sửa `max_value` của ô Số khách trong code thành `50`, chọn `LT08` (chỉ còn 10 chỗ), nhập `11` khách rồi bấm lưu -> MySQL báo lỗi `3819` (`chk_LichTrinh_SoChoDaDat`), ứng dụng bắt lỗi qua `thong_bao_loi()` và hiện `"Lịch trình không còn đủ chỗ cho số khách này"`, không có đơn rác trong `DonHang`. Sau khi thử xong, trả lại `max_value` như cũ.
- **Lệnh Git thực hiện:**
  ```powershell
  git add tour_app/pages/1_Dat_tour.py
  git commit -m "feat: hoan thien form dat tour F1 va kiem tra 6 ca nghiem thu"
  git push -u origin feature/f1-dat-tour
  ```
  *(Lên GitHub tạo Pull Request vào `main` và báo Khánh merge).*

#### 3. Đợt 3 — Cụm 3 (11/11 - 13/11): Tasks `D4`, `D5`
- **Nền tảng làm việc:** Trình duyệt (zoom 100%, rộng ~1400px), Paint, VS Code.
- **Các bước thực hiện cụ thể:**
  1. **Task `D4` — Chụp Hình 4, Hình 5a, Hình 5b (11/11):**
     - Chạy lại `database/1_QuanLyDatTour_v3.sql` để dữ liệu về trạng thái gốc.
     - **`screenshots/Hinh04_F1_GiaoDien.png`:** Điền `KH006`, `LT10`, `5` khách, `NN08`, `2` phòng, tích 2 chuyến xe (chưa bấm nút Lưu), chụp giao diện lúc đang hiển thị tổng tiền dự kiến `32.020.000 đ`.
     - **`screenshots/Hinh05a_F1_Loi.png`:** Thực hiện Ca 3 (2 khách, 3 phòng) hoặc Ca 4 (tích đón tại nhà, để trống địa chỉ), chụp gọn vùng thông báo lỗi của form.
     - **`screenshots/Hinh05b_F1_Loi.png`:** Thực hiện Ca 6 (tạm mở `max_value=50`, đặt 11 khách cho `LT08`), chụp gọn vùng thông báo lỗi `"Lịch trình không còn đủ chỗ cho số khách này"`, sau đó khôi phục lại `max_value` trong code.
  2. **Task `D5` — Rà soát Báo cáo mục 2.3, 3.1, 3.2, 6.2 (12/11 - 13/11):**
     - Mở `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`, kiểm tra:
       - Mục 2.3: Bảng ký hiệu ERD.
       - Mục 3.1 & 3.2: 4 quy tắc chuyển ERD sang bảng và 12 lược đồ quan hệ (khóa chính gạch chân, khóa ngoại in nghiêng).
       - Mục 6.2: Bảng các trường của Form F1 và 2 khối câu lệnh SQL trong mục 6.2.2 phải khớp với code `tour_app/pages/1_Dat_tour.py`.
     - Ghi các điểm lệch (nếu có) vào `docs/GopY_Dat.md` theo mẫu (`Trang | Mục | Đang ghi | Sửa thành | Lý do`).
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add screenshots/Hinh04_F1_GiaoDien.png screenshots/Hinh05a_F1_Loi.png screenshots/Hinh05b_F1_Loi.png docs/GopY_Dat.md
  git commit -m "docs: them hinh chup F1 (Hinh 4, 5a, 5b) va gop y bao cao cua Dat"
  git push origin main
  ```

#### 4. Đợt 4, 5, 6 — Cụm 4 đến Cụm 6 (14/11 - 22/11): Tasks `D6`, `D7`, `D8`, `D9`
- **Task `D6` (14/11 - Kiểm thử chéo S1 & R2 của Khánh):** Chạy thử 6 ca của `S1` (mục 7.3) và kiểm tra `R2` (kỳ `01/09/2026 - 31/12/2026` ra tổng cộng `79.110.000 đ`, `10` đơn, `26` khách, `4` hủy; bỏ trống người lập không tải được file). Ghi lỗi gửi Khánh.
- **Task `D7` (15/11 - 16/11):** Sửa lỗi `F1` nếu Thịnh báo (trên nhánh `fix/f1-...`); đối chiếu toàn bộ tên bảng, tên cột giữa `ERD`, `DataDiagram`, Báo cáo và Code để đảm bảo đồng nhất 100%.
- **Task `D8` (17/11 - Kiểm thử cài đặt trên máy sạch):** Dùng một máy tính khác chưa từng cài dự án (hoặc môi trường sạch chỉ có MySQL 8.0 và Python), làm đúng từng bước trong mục `PHỤ LỤC. HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY` của báo cáo mà không hỏi Khánh. Ghi lại bất kỳ bước nào chưa rõ để Khánh cập nhật Phụ lục và `README.md`. Giữ máy này làm **Laptop dự phòng** mang đi hôm bảo vệ.
- **Task `D9` (18/11 - 21/11):** Kiểm tra độ nét của `ERD.png` khi phóng to 200%; tập thuyết trình phần ERD (phút `1:30 - 4:30`) và phần thuyết minh khi Khánh chạy demo `F1`.

---

### III. NHIỆM VỤ CHI TIẾT CỦA TUÂN (`TU1` -> `TU11`)

- **Vai trò:** Phụ trách Yêu cầu dữ liệu & Quy tắc nghiệp vụ (Chương 1, mục 2.2, Chương 9), Màn hình Quản lý & Hủy đơn (`F2` - `tour_app/pages/2_Quan_ly_don.py`), Báo cáo Phiếu xác nhận (`R1` - `tour_app/pages/5_Phieu_xac_nhan.py` & `tour_app/templates/phieu_xac_nhan.html`), Slide thuyết trình 8 trang, Liên lạc giảng viên và Nộp bài lên Google Drive.

#### 1. Đợt 1 — Cụm 1 (05/11 - 07/11): Tasks `TU1`, `TU2`
- **Nền tảng làm việc:** Kênh liên lạc lớp học, Microsoft Word (chế độ đọc), VS Code.
- **Các bước thực hiện cụ thể:**
  1. **Task `TU1` (05/11 - 06/11):** Nhắn tin hỏi giảng viên 4 nội dung:
     - Báo cáo nộp định dạng `.pdf`, `.docx` hay cả hai?
     - Mã nguồn và 4 tệp SQL đặt trong thư mục con trên Drive hay nén `.zip`?
     - Quy tắc đặt tên thư mục/file nộp (ví dụ: `NhomXX_QuanLyDatTour`)?
     - Nhóm thuyết trình vào ngày `23/11` hay `30/11/2026`, ca nào?
     *(Khi có câu trả lời và link Drive của giảng viên, báo ngay cho cả nhóm).*
  2. **Task `TU2` (06/11 - 07/11):** Mở `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`, đọc soát Chương 1 (tr. 5-7), mục 2.2 (bảng 12 mối liên kết) và Chương 9 (Kết luận):
     - Kiểm tra công thức tính tổng tiền, 5 mốc phạt hủy (`0%`, `10%`, `30%`, `50%`, `100%`), ví dụ tính phạt của `DH008` (30%, phạt `2.610.000 đ`, hoàn `6.090.000 đ`) và bảng kết quả view ở mục 5.3 (`DH011` 0%, `DH009` 10%, `DH008` 30%, `DH006` 100%).
     - Kiểm tra mục 2.2 đủ 12 mối liên kết (có `ThanhToanBang`) khớp với ERD của Đạt.
     - Tạo file `docs/GopY_Tuan.md` ghi lại các chỗ cần chỉnh sửa.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add docs/GopY_Tuan.md
  git commit -m "docs: cap nhat gop y Chuong 1, muc 2.2 va Chuong 9 cua Tuan"
  git push origin main
  ```

#### 2. Đợt 2 — Cụm 2 (08/11 - 10/11): Tasks `TU3`, `TU4`, `TU5`
- **Nền tảng làm việc:** VS Code, Streamlit, MySQL Workbench 8.0, Trình duyệt Microsoft Edge / Chrome.
- **Các bước thực hiện cụ thể:**
  1. **Task `TU3` — Hoàn thiện Màn hình Quản lý và Hủy đơn F2 (08/11 - 09/11):**
     - Tạo nhánh `git checkout -b feature/f2-quan-ly-don main`.
     - Viết `tour_app/pages/2_Quan_ly_don.py` theo đặc tả và mã nguồn đầy đủ tại `docs/Huong_dan_chi_tiet_Tuan.md` (Mục 4):
       - Ô chọn mã đơn chỉ lấy các đơn ở trạng thái `'DAT'` hoặc `'THANHTOAN'` (SQL `F2.1` — với dữ liệu mẫu ra 5 đơn: `DH007`, `DH010`, `DH012`, `DH013`, `DH014`).
       - Ô chọn trạng thái mới lấy từ SQL `F2.3` (chỉ hiện trạng thái hợp lệ theo thời gian `@HienTai`).
       - Khi chọn `"Đã hủy tour"`: hiện ô Ngày giờ hủy (mặc định `hien_tai()`), ô Lý do hủy (bắt buộc nhập, tối đa 255 ký tự), khung **Xem trước tiền phạt** (chạy SQL `F2.4` tự động tính số ngày trước khởi hành, tỷ lệ phạt, tiền phạt, tiền hoàn) và ô tích `"Khách đã đồng ý mức phạt"`.
       - Khi bấm lưu hủy đơn: gọi `ghi()` chạy 3 lệnh trong **1 Transaction** (SQL `F2.5`): `UPDATE DonHang` (có điều kiện `AND MaTrangThai IN ('DAT', 'THANHTOAN')`, `phai_co_dong=True`), `UPDATE LichTrinh` trả lại số chỗ (`phai_co_dong=True`), và `DELETE FROM ChuyenTrungChuyen` (`phai_co_dong=False`).
     - Chạy kiểm thử đủ 5 ca ở mục 6.3.3 báo cáo (7 ca ở Quyển 5):
       - Ca 1: Hủy `DH010` tại thời điểm mặc định `23/10/2026 08:00` -> Xem trước hiện đúng **22 ngày, phạt 10%, tiền phạt 1.600.000 đ, tiền hoàn 14.400.000 đ**. Sau khi lưu, kiểm tra Workbench thấy `LT05` còn `0` chỗ đã đặt và `DH010` không còn dòng nào trong `ChuyenTrungChuyen`.
       - Ca 2: Chuyển `DH013` sang `"Đã thanh toán"` -> Lưu thành công.
       - Ca 3: Chọn `DH012` -> Ô trạng thái mới chỉ hiện duy nhất `"Đã hủy tour"` (vì tour đi ngày 20/11, chưa kết thúc nên chưa thể chọn Hoàn thành).
       - Ca 4: Chọn hủy nhưng để trống Lý do hủy hoặc chưa tích ô xác nhận -> Form chặn và báo lỗi.
       - Ca 5: Nhập ngày hủy `10/10/2026` cho `DH010` (trước ngày đặt `12/10/2026`) -> Form chặn (nếu lọt xuống CSDL thì `chk_DonHang_NgayHuy` chặn với thông báo `"Ngày hủy phải sau ngày đặt"`).
     - Push nhánh `feature/f2-quan-ly-don` lên GitHub.
  2. **Task `TU4` & `TU5` — Hoàn thiện Báo cáo Phiếu xác nhận R1 có Nhân viên lập phiếu và Xuất PDF (09/11 - 10/11):**
     - Tạo nhánh `git checkout -b feature/r1-phieu-xac-nhan main`.
     - Viết `tour_app/pages/5_Phieu_xac_nhan.py` và `tour_app/templates/phieu_xac_nhan.html` theo Quyển 5 Phần 6 (dòng 3747 - 3834), sau đó bổ sung phần **Nhân viên lập phiếu** theo đúng yêu cầu Bản 5 (`TU4`):
       - Đầu file `5_Phieu_xac_nhan.py` thêm `from html import escape`.
       - Ngay dưới ô chọn mã đơn hàng, thêm:
         ```python
         nguoi_lap = st.text_input("Nhân viên lập phiếu", max_chars=100, placeholder="Họ tên nhân viên kinh doanh")
         st.caption("Người nhận: khách hàng đặt tour")
         ```
       - Sau phần hiển thị phiếu trên màn hình và trước nút `st.download_button`, thêm:
         ```python
         if not nguoi_lap.strip():
             st.warning("Nhập tên nhân viên lập phiếu để tải và in phiếu")
             st.stop()
         ```
       - Truyền `nhan_vien_lap=escape(nguoi_lap.strip())` vào hàm điền mẫu HTML.
       - Trong `tour_app/templates/phieu_xac_nhan.html`, cập nhật khối chữ ký cuối trang:
         ```html
         <div class="ky-ten">
         <div><b>Khách hàng</b><br>(Ký, ghi rõ họ tên)</div>
         <div><b>Nhân viên lập phiếu</b><br>(Ký, ghi rõ họ tên)<br><br>$nhan_vien_lap</div>
         </div>
         ```
         kèm CSS `.ky-ten { display: flex; justify-content: space-around; margin-top: 12px; text-align: center; }`.
     - Kiểm thử nghiệm thu `R1` (`TU5`):
       - Chọn `DH007`: tiền tour `5.800.000 đ`, tiền phòng `450.000 đ`, tổng `6.250.000 đ`; để trống tên nhân viên thì hiện cảnh báo và ẩn nút tải; nhập tên nhân viên thì tải được file.
       - Chọn `DH008`: hiển thị vùng Thông tin hủy gồm tỷ lệ phạt `30%`, tiền phạt `2.610.000 đ`, tiền hoàn `6.090.000 đ`.
       - Mở file HTML của `DH007` và `DH008` bằng trình duyệt Edge/Chrome -> nhấn `Ctrl + P` -> chọn `"Save as PDF"`, khổ **A4 dọc (Portrait)**, lề Mặc định, tích `"Background graphics"` -> xác nhận vừa khít **1 trang A4** và lưu thành `PhieuXacNhan_DH007.pdf`, `PhieuXacNhan_DH008.pdf`.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout feature/f2-quan-ly-don
  git add tour_app/pages/2_Quan_ly_don.py
  git commit -m "feat: hoan thien form quan ly va huy don F2"
  git push -u origin feature/f2-quan-ly-don

  git checkout feature/r1-phieu-xac-nhan
  git add tour_app/pages/5_Phieu_xac_nhan.py tour_app/templates/phieu_xac_nhan.html
  git commit -m "feat: hoan thien phieu xac nhan R1 co nhan vien lap phieu va khoi ky"
  git push -u origin feature/r1-phieu-xac-nhan
  ```
  *(Tạo 2 Pull Request trên GitHub và nhắn Khánh merge vào `main`).*

#### 3. Đợt 3 — Cụm 3 (11/11 - 13/11): Tasks `TU6`, `TU7`
- **Nền tảng làm việc:** Trình duyệt Edge (zoom 100%, rộng ~1400px), Paint, VS Code.
- **Các bước thực hiện cụ thể:**
  1. **Task `TU6` — Chụp Hình 6, 7, 10, 11 và Rà soát mục 6.3, 8.1 (11/11 - 12/11):**
     - Chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc.
     - **`screenshots/Hinh06_F2_GiaoDien.png`:** Mở F2, chọn `DH010`, chọn `"Đã hủy tour"`, nhập lý do hủy, chụp màn hình khi khung xem trước đang hiện `22 ngày, 10%, phạt 1.600.000 đ, hoàn 14.400.000 đ`.
     - **`screenshots/Hinh07_F2_Loi.png`:** Thực hiện Ca 4 (để trống lý do hủy) hoặc Ca 5 (chọn ngày hủy trước ngày đặt), chụp gọn vùng thông báo lỗi.
     - **`screenshots/Hinh10_R1_ManHinh.png`:** Mở R1, chọn đơn `DH007`, nhập tên nhân viên lập phiếu, chụp giao diện phiếu trên màn hình.
     - **`screenshots/Hinh11_R1_PDF.png`:** Mở file `PhieuXacNhan_DH008.pdf` (đơn đã hủy, có phần tiền phạt và chữ ký nhân viên lập phiếu) trên Edge ở chế độ `"Fit to page"`, chụp trọn trang PDF A4 dọc.
     - Rà soát mục 6.3 và 8.1 trong báo cáo Word xem bảng trường và các câu SQL đã khớp 100% với code `2_Quan_ly_don.py` và `5_Phieu_xac_nhan.py` chưa; bổ sung vào `docs/GopY_Tuan.md`.
  2. **Task `TU7` — Chốt thông tin thành viên và % đóng góp (13/11):**
     - Đối chiếu danh sách 4 thành viên (`Nguyễn Tất Đạt - B24DCCN117`, `Nguyễn Tiến Thịnh - B24DCCN546`, `Bùi Đức Tuân - B24DCCN590`, `Nguyễn Quốc Khánh - B24DCCN311`) cùng mức đóng góp (`25%` mỗi người, tổng `100%`) đã điền vào Trang bìa + Bảng 2 (trang 4).
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add screenshots/Hinh06_F2_GiaoDien.png screenshots/Hinh07_F2_Loi.png screenshots/Hinh10_R1_ManHinh.png screenshots/Hinh11_R1_PDF.png docs/GopY_Tuan.md
  git commit -m "docs: them hinh chup F2, R1 (Hinh 6, 7, 10, 11) va gop y cua Tuan"
  git push origin main
  ```

#### 4. Đợt 4, 5, 6 — Cụm 4 đến Cụm 6 (14/11 - 22/11): Tasks `TU8`, `TU9`, `TU10`, `TU11`
- **Task `TU8` (14/11 - Kiểm thử chéo F3 của Thịnh):** Chạy lại tệp SQL số 1, kiểm tra đủ các ca của `F3` (mục 6.4 báo cáo), ghi lỗi gửi Thịnh.
- **Task `TU9` (15/11 - 16/11 - Làm Slide thuyết trình 8 trang):** Soạn `Slide_Nhom.pptx` (cỡ chữ tối thiểu 20pt, mỗi trang tối đa 5 dòng) gồm đúng 8 trang dùng cho 7 phút đầu trước khi demo:
  - Trang 1 (Tuân nói): Tên đề tài, nhóm, danh sách 4 thành viên.
  - Trang 2 (Tuân nói): Bài toán thực tế — 4 vấn đề khi quản lý thủ công (mục 1.1).
  - Trang 3 (Tuân nói): Phạm vi 15 tỉnh miền Bắc, người dùng, tổng quan 6 màn hình (mục 1.2 - 1.3).
  - Trang 4 (Đạt nói): Sơ đồ ERD (`Hinh01_ERD.png` tràn trang).
  - Trang 5 (Đạt nói): 4 điểm đặc biệt trên ERD (thực thể yếu, đa trị, dẫn xuất, phức hợp).
  - Trang 6 (Thịnh nói): 12 bảng, 56 ràng buộc và Sơ đồ Data Diagram (`Hinh02_DataDiagram.png`).
  - Trang 7 (Thịnh nói): Chuẩn hóa 3NF — `KhachHang` vi phạm 3NF (`SoID -> LoaiThe`), cách tách `TheThanhToan` để cả 12 bảng đạt chuẩn 3NF.
  - Trang 8 (Khánh nói): Lộ trình 8 bước demo trực tiếp trên ứng dụng và MySQL Workbench.
- **Task `TU10` (17/11 - 18/11):** Đọc soát toàn bộ báo cáo bản `v0.9` do Thịnh xuất (kiểm tra lỗi chính tả, số trang mục lục, chú thích bảng/hình, đối chiếu 8 tiêu chí chấm điểm).
- **Task `TU11` (Trước 21:00 CN 22/11 - Nộp bài lên Google Drive của giảng viên):**
  - Mở link Google Drive của giảng viên bằng email trường, tạo thư mục nhóm theo đúng quy tắc đặt tên của giảng viên, tải toàn bộ bộ file nộp lên.
  - Mở thử từng file `.pdf`, `.docx` trực tiếp trên Drive để kiểm tra không lỗi font.
  - Mở link bằng cửa sổ ẩn danh (`Ctrl + Shift + N`) để xác nhận quyền truy cập hợp lệ.
  - Chụp ảnh màn hình thư mục Drive kèm đồng hồ hệ thống gửi vào nhóm làm bằng chứng hoàn thành.

---

### IV. NHIỆM VỤ CHI TIẾT CỦA THỊNH (`TH1` -> `TH10`)

- **Vai trò:** Phụ trách Phân tích Thực thể (mục 2.1), Mô tả bảng & Ràng buộc toàn vẹn (mục 3.3, 3.4), Chuẩn hóa 3NF (Chương 4), Màn hình Đánh giá sau chuyến đi (`F3` - `tour_app/pages/3_Danh_gia.py`, mục 6.4) và là **Người duy nhất biên tập trực tiếp file Báo cáo Word** (`docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`).

#### 1. Đợt 1 — Cụm 1 (05/11 - 07/11): Tasks `TH1`, `TH2`
- **Nền tảng làm việc:** Microsoft Word, MySQL Workbench 8.0, VS Code.
- **Các bước thực hiện cụ thể:**
  1. **Task `TH1` (05/11):** Mở file `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` trong Microsoft Word. Khi hộp thoại hỏi `"Update the fields?"` xuất hiện, chọn **Yes** để mục lục tự động cập nhật số trang. Lưu bản làm việc với quy ước:
     - Giữ nguyên định dạng chuẩn đã thiết lập: khổ A4, lề trái 3 cm, lề trên/dưới/phải 2 cm, font Times New Roman cỡ 13, giãn dòng 1,4; dùng đúng Styles `Heading 1`, `Heading 2`, `Heading 3`.
  2. **Task `TH2` (06/11 - 07/11):** Mở `database/1_QuanLyDatTour_v3.sql` đặt cạnh báo cáo Word, rà soát kỹ:
     - Mục 2.1 (tr. 8): Bảng 11 thực thể và các thuộc tính phải khớp với ERD bản cuối của Đạt (đã tách `TheThanhToan`).
     - Mục 3.3 (tr. 12-15): Kiểm tra từng cột của cả 12 bảng (Tên cột, Kiểu dữ liệu, Khóa `PK`/`FK`/`UQ`, cột cho phép `NULL` có ghi `"có thể trống"`, điều kiện `CHECK` trong cột Ý nghĩa).
     - Mục 3.4 (tr. 15-16): Kiểm tra 5 nhóm ràng buộc toàn vẹn và các ví dụ minh họa.
     - Ghi các điểm tự rà soát vào `docs/GopY_Thinh.md`.

#### 2. Đợt 2 — Cụm 2 (08/11 - 10/11): Tasks `TH3`, `TH4`
- **Nền tảng làm việc:** VS Code, Streamlit, MySQL Workbench 8.0.
- **Các bước thực hiện cụ thể:**
  1. **Task `TH3` — Hoàn thiện Màn hình Đánh giá F3 (08/11 - 09/11):**
     - Tạo nhánh `git checkout -b feature/f3-danh-gia main`.
     - Viết file `tour_app/pages/3_Danh_gia.py` theo đặc tả và mã nguồn đầy đủ tại `docs/Huong_dan_chi_tiet_Thinh.md` (Mục 4):
       - Ô 1 chọn Khách hàng (SQL `F1.1`).
       - Ô 2 chọn Chuyến đi chờ đánh giá của khách đó (SQL `F3.1`: lọc `MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL`). Nếu không có đơn nào thì thông báo `"Không có chuyến đi nào chờ đánh giá"`.
       - Ô 3 chọn Điểm tour (từ 1 đến 5, bắt buộc) và Ô 4 nhập Nhận xét tour (tối đa 500 ký tự, nếu để trống thì truyền `None`).
       - Ô 5 (Điểm nơi nghỉ, từ 1 đến 5) và Ô 6 (Nhận xét nơi nghỉ, tối đa 500 ký tự): **chỉ hiển thị khi đơn hàng có đặt nơi nghỉ** (`TenNhaNghi IS NOT NULL`). Nếu người dùng nhập Nhận xét nơi nghỉ thì bắt buộc phải chấm Điểm nơi nghỉ.
       - Khi bấm lưu: gọi `ghi()` chạy câu lệnh `UPDATE DonHang` (SQL `F3.2` với điều kiện `WHERE MaDonHang = %(MaDonHang)s AND MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL`, `phai_co_dong=True`), gán `NgayDanhGia = hien_tai()`.
     - Chạy kiểm thử nghiệm thu `F3`:
       - Ca 1: Chọn `KH004` -> hiện đơn `DH004` (có nơi nghỉ `Nhà nghỉ Sương Sớm`) -> chấm tour `4` điểm, nhận xét `"Cảnh đẹp, lịch trình vừa sức."`, chấm nơi nghỉ `4` điểm, nhận xét `"Phòng ấm, sạch sẽ."` -> Bấm lưu thành công (`NgayDanhGia = 23/10/2026 08:00`), `DH004` biến mất khỏi danh sách chờ; sang màn hình `S1` tìm `"sa pa"` thấy điểm trung bình tour đổi từ `5,0` (1 lượt) thành `4,5` (2 lượt).
       - Ca 2: Chọn `KH001` -> Báo `"Không có chuyến đi nào chờ đánh giá"` (`DH001` đã đánh giá, `DH007` chưa hoàn thành).
       - Ca 3: Nhập nhận xét nơi nghỉ nhưng không chấm điểm nơi nghỉ -> Form chặn và báo lỗi (nếu lọt xuống CSDL thì `chk_DonHang_NhanXet` chặn với thông báo `"Có nhận xét thì phải chấm điểm"`).
  2. **Task `TH4` — Rà soát Chương 4 Chuẩn hóa 3NF (10/11):**
     - Mở MySQL Workbench, chạy lại câu lệnh ghép bảng ở mục 4.4:
       ```sql
       SELECT kh.MaKH, kh.HoTen, kh.Email, kh.DiaChi, th.LoaiThe, kh.SoID
       FROM KhachHang kh
       LEFT JOIN TheThanhToan th ON th.SoID = kh.SoID
       ORDER BY kh.MaKH;
       ```
     - Xác nhận kết quả trả về đúng 8 dòng khách hàng như trước khi tách bảng. Kiểm tra bảng tổng hợp kiểm tra dạng chuẩn ở mục 4.3.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout feature/f3-danh-gia
  git add tour_app/pages/3_Danh_gia.py
  git commit -m "feat: hoan thien form danh gia sau chuyen di F3"
  git push -u origin feature/f3-danh-gia
  ```
  *(Tạo Pull Request trên GitHub và nhắn Khánh merge vào `main`).*

#### 3. Đợt 3 — Cụm 3 (11/11 - 13/11): Task `TH5`
- **Nền tảng làm việc:** Trình duyệt Edge (zoom 100%, rộng ~1400px), Paint, Microsoft Word.
- **Các bước thực hiện cụ thể:**
  - Chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc.
  - Mở trang Đánh giá `F3`, chọn `KH004`, đơn `DH004`, điền điểm và nhận xét như Ca 1 (trước khi bấm lưu), chụp màn hình lưu thành `screenshots/Hinh08_F3_GiaoDien.png`.
  - Rà soát mục 6.4 trong báo cáo Word cho khớp với code `tour_app/pages/3_Danh_gia.py`.
- **Lệnh Git thực hiện:**
  ```powershell
  git checkout main
  git pull origin main
  git add screenshots/Hinh08_F3_GiaoDien.png docs/GopY_Thinh.md
  git commit -m "docs: them Hinh 8 giao dien F3 va gop y cua Thinh"
  git push origin main
  ```

#### 4. Đợt 4, 5, 6 — Cụm 4 đến Cụm 6 (14/11 - 22/11): Tasks `TH6`, `TH7`, `TH8`, `TH9`, `TH10`
- **Task `TH6` (14/11 - Kiểm thử chéo F1 của Đạt):** Chạy lại tệp SQL số 1, kiểm tra đủ 6 ca của `F1` tại mục 6.2.3 báo cáo, gửi danh sách lỗi (nếu có) cho Đạt.
- **Task `TH7` (15/11 - Tổng hợp góp ý cả nhóm):** Mở các file `docs/GopY_Dat.md`, `docs/GopY_Tuan.md`, `docs/GopY_Khanh.md`, `docs/GopY_Thinh.md`, áp dụng toàn bộ chỉnh sửa vào `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`.
- **Task `TH8` (16/11 - Chèn 13 hình và Xóa toàn bộ ô vàng Highlight):**
  1. **Quy trình chèn từng hình vào 13 khung nét đứt trong Word (bắt buộc làm đúng để không bị cắt mất phần trên của ảnh):**
     - Nhấp chuột nhanh 3 lần vào dòng chữ tô vàng trong khung để bôi đen cả đoạn -> Nhấn `Shift + Mũi tên trái` 1 lần (để giữ lại dấu ngắt đoạn cuối khung) -> Nhấn `Delete`.
     - Nhấn `Ctrl + Q` (xóa định dạng khung viền nét đứt và khoảng cách dòng cố định) -> Nhấn `Ctrl + E` (căn giữa).
     - Chọn `Insert > Pictures > This Device` -> chèn đúng file ảnh trong `screenshots/` theo bảng ở Phần 6 mục I bên dưới.
     - Chọn ảnh vừa chèn: đặt `Layout Options = In Line with Text`; tại tab `Picture Format`, đặt `Width <= 16 cm` (riêng **Hình 5** chèn 2 ảnh `Hinh05a_F1_Loi.png` và `Hinh05b_F1_Loi.png` nằm ngang trên cùng một dòng, mỗi ảnh `Width = 7,8 cm`; **Hình 11** đặt `Height = 11 cm`).
     - Giữ nguyên dòng chú thích `"Hình n. ..."` bên dưới ảnh.
  2. **Quy trình tìm và điền hết các ô tô vàng Highlight:**
     - Nhấn `Ctrl + H` -> bấm `More >>` -> bấm `Format > Highlight` -> bấm `Find In > Main Document`.
     - Điền đầy đủ: Mã học phần, Tên giảng viên, Số nhóm, Họ tên và MSSV của Đạt, Thịnh, Tuân (ở Trang bìa và Bảng 2 phân công trang 4), mức đóng góp (%), giáo trình CSDL ở Tài liệu tham khảo và link GitHub/Drive ở Phụ lục.
     - Bôi đen vùng vừa điền -> chọn `Home > Text Highlight Color > No Color`.
     - Chạy tìm kiếm lại theo `Highlight`: kết quả phải báo **0 mục** (không còn bất kỳ ô vàng nào).
- **Task `TH9` & `TH10` (17/11 - 21/11 - Xuất bản `v1.0` và Bản nộp cuối):**
  - Áp dụng góp ý đọc soát của Tuân (`TU10`).
  - Nhấp chuột phải vào Mục lục đầu báo cáo -> chọn `Update Field > Update entire table > OK`. Kiểm tra tổng số trang ở thanh trạng thái Word **không vượt quá 50 trang**.
  - Lưu file `.docx` và chọn `File > Save As > PDF` (bấm `Options`, tích `"Create bookmarks using: Headings"`).
  - Commit file `.docx` và `.pdf` hoàn chỉnh lên nhánh `main` của GitHub và bàn giao cho Tuân nộp Drive.

---

## Phần 6. Quy chuẩn 13 Hình ảnh, Cấu trúc Gói Nộp Drive và Kịch bản Bảo vệ 15 Phút

### I. Bảng Đặc tả 13 Hình ảnh Chèn vào Báo cáo (Thư mục `screenshots/`)

Trước khi chụp bất kỳ hình nào, bắt buộc chạy lại `database/1_QuanLyDatTour_v3.sql` để dữ liệu về đúng trạng thái gốc tại mốc thời gian demo `23/10/2026 08:00`.

| Số hình | Tên file chuẩn trong `screenshots/` | Mục trong Báo cáo | Nội dung bắt buộc phải hiển thị trên ảnh | Kích thước trong Word | Người chụp |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Hình 1** | `Hinh01_ERD.png` | Mục 2.3 | Sơ đồ ERD 11 thực thể (có `TheThanhToan`), 12 mối liên kết, nền trắng, Zoom 200% | Rộng `16 cm` | Đạt |
| **Hình 2** | `Hinh02_DataDiagram.png` | Mục 3.5 | Sơ đồ Data Diagram 12 bảng xếp 4 cụm, 13 đường nối chân gà từ MySQL Workbench | Rộng `16 cm` | Khánh |
| **Hình 3** | `Hinh03_LoiRangBuoc.png` | Mục 5.5 | Khung `Action Output` của Workbench hiện đủ 4 dòng báo lỗi đỏ của 4 mã lỗi: `1062`, `3819`, `1452`, `1451` | Rộng `16 cm` | Khánh |
| **Hình 4** | `Hinh04_F1_GiaoDien.png` | Mục 6.2.1 | Form đặt tour F1: chọn `KH006`, `LT10`, `5` khách, `NN08`, `2` phòng, hiện tổng tiền dự kiến `32.020.000 đ` | Rộng `16 cm` | Đạt |
| **Hình 5** | `Hinh05a_F1_Loi.png`<br>`Hinh05b_F1_Loi.png` | Mục 6.2.3 | `5a`: Thông báo lỗi Ca 3 (2 khách, 3 phòng) hoặc Ca 4 (thiếu địa chỉ đón).<br>`5b`: Thông báo lỗi Ca 6 (`"Lịch trình không còn đủ chỗ cho số khách này"`) | Đặt cùng 1 dòng, mỗi ảnh rộng `7,8 cm` | Đạt |
| **Hình 6** | `Hinh06_F2_GiaoDien.png` | Mục 6.3.1 | Form F2 đang chọn hủy `DH010`: hiện xem trước `22` ngày, `10%`, phạt `1.600.000 đ`, hoàn `14.400.000 đ` | Rộng `16 cm` | Tuân |
| **Hình 7** | `Hinh07_F2_Loi.png` | Mục 6.3.3 | Thông báo lỗi Ca 4 (để trống lý do hủy) hoặc Ca 5 (ngày hủy trước ngày đặt) trên F2 | Rộng `16 cm` | Tuân |
| **Hình 8** | `Hinh08_F3_GiaoDien.png` | Mục 6.4 | Form đánh giá F3 đang chọn khách `KH004` và chuyến đi `DH004` (có cả phần đánh giá nơi nghỉ) | Rộng `16 cm` | Thịnh |
| **Hình 9** | `Hinh09_S1_CaoCap.png` | Mục 7.1 | Màn hình tìm kiếm S1 khi bấm `"Tour cao cấp (từ 10 triệu)"`: bảng kết quả hiện `LT08`, `LT09`, `LT12` | Rộng `16 cm` | Khánh |
| **Hình 10** | `Hinh10_R1_ManHinh.png` | Mục 8.1.2 | Giao diện màn hình R1 đang hiển thị phiếu xác nhận của đơn `DH007` (tổng `6.250.000 đ`) | Rộng `16 cm` | Tuân |
| **Hình 11** | `Hinh11_R1_PDF.png` | Mục 8.1.2 | Trang PDF khổ A4 dọc của đơn `DH008` (có vùng thông tin hủy 30%, tên nhân viên lập phiếu và 2 ô ký) | Cao `11 cm` | Tuân |
| **Hình 12** | `Hinh12_R2_ManHinh.png` | Mục 8.2.2 | Giao diện màn hình R2 kỳ `01/09/2026 - 31/12/2026` (4 ô chỉ số: `79.110.000 đ`, `10`, `26`, `4`) | Rộng `16 cm` | Khánh |
| **Hình 13** | `Hinh13_R2_PDF.png` | Mục 8.2.2 | Trang PDF khổ A4 ngang của R2 (vừa 1 trang, có dòng Người lập, Nơi nhận và 2 ô ký cuối trang) | Rộng `16 cm` | Khánh |

### II. Cấu trúc Bộ File Đóng gói Nộp lên Google Drive của Giảng viên

```text
Nhom<so_nhom>_QuanLyDatTour/
├── README.txt
├── BaoCao_Nhom<so_nhom>_QuanLyDatTour.pdf
├── BaoCao_Nhom<so_nhom>_QuanLyDatTour.docx
├── CSDL/
│   ├── 1_QuanLyDatTour_v3.sql
│   ├── 2_QuanLyDatTour_v3_TruyVan.sql
│   ├── 3_QuanLyDatTour_v3_UngDung.sql
│   └── 4_KiemTra_RangBuoc.sql
├── ThietKe/
│   ├── ERD.drawio
│   ├── ERD.png
│   ├── DataDiagram.mwb
│   └── DataDiagram.png
└── UngDung/
    └── tour_app.zip
```

### III. Kịch bản Thuyết trình và Demo Bảo vệ (15 Phút)

#### 1. Phân bổ thời gian 15 phút
- **Phút `0:00 - 1:30` (Tuân trình bày — Slide 1, 2, 3):** Giới thiệu nhóm, bài toán thực tế (4 vấn đề khi quản lý thủ công), phạm vi 15 tỉnh miền Bắc, các nhóm người dùng và quy tắc nghiệp vụ cốt lõi.
- **Phút `1:30 - 4:30` (Đạt trình bày — Slide 4, 5):** Trình bày sơ đồ ERD (11 thực thể, 12 mối liên kết) và giải thích 4 điểm thiết kế đặc biệt: thực thể yếu `ChuyenTrungChuyen`, thuộc tính đa trị `SDT`, thuộc tính dẫn xuất (`SoDem`, `TongTien`, `TienPhat`, `TienHoan`) và thuộc tính phức hợp (`DanhGiaTour`, `DanhGiaNhaNghi`).
- **Phút `4:30 - 7:00` (Thịnh trình bày — Slide 6, 7):** Trình bày ánh xạ sang 12 bảng quan hệ, 56 ràng buộc toàn vẹn, sơ đồ `DataDiagram` (12 bảng, 13 khóa ngoại) và quá trình phát hiện `KhachHang` vi phạm 3NF (`MaKH -> SoID -> LoaiThe`), cách tách bảng `TheThanhToan` để cả 12 bảng đạt chuẩn 3NF.
- **Phút `7:00 - 13:00` (Khánh điều khiển máy — Chủ màn hình thuyết minh theo 8 bước bên dưới):** Demo trực tiếp trên ứng dụng Streamlit và MySQL Workbench.
- **Phút `13:00 - 15:00` (Cả nhóm):** Trả lời câu hỏi vấn đáp của giảng viên (dựa trên bộ câu hỏi vấn đáp chuyên sâu tại mục cuối của từng file `docs/Huong_dan_chi_tiet_<Ten>.md`).

#### 2. Kịch bản 8 Bước Demo Trực tiếp (6 Phút)

| Bước | Thời lượng | Màn hình | Thao tác của Khánh trên máy | Người nói & Nội dung thuyết minh chính |
| :--- | :--- | :--- | :--- | :--- |
| **1** | `0:40` | `S1` (Tìm kiếm) | Bấm nút `"Tour cao cấp (từ 10 triệu)"` | **Khánh:** Dùng 1 câu `SELECT` có tham số `(@Loc IS NULL OR ...)` xử lý mọi tổ hợp lọc; kết quả ra `LT08`, `LT09`, `LT12`. |
| **2** | `1:00` | `F1` (Đặt tour) | Chọn `KH006`, `LT10`, `5` khách, `NN08`, `2` phòng, tích đón tại nhà & về nơi nghỉ -> Bấm Lưu tạo `DH015` | **Đạt:** Nơi nghỉ tự lọc theo tỉnh đến (`Tuyên Quang`); tổng tiền dự kiến `32.020.000 đ`; thêm đơn, trừ chỗ `LT10` (còn 15 chỗ) và thêm 2 chuyến xe chạy trong 1 `Transaction`. |
| **3** | `0:50` | `F1` (Kiểm tra chặn lỗi) | Nhập `2` khách nhưng chọn `3` phòng; nhập giờ đón sau giờ xuất phát | **Đạt:** Minh chứng Tiêu chí 5 (kiểm tra dữ liệu 2 lớp: Form chặn trước, nếu lọt xuống MySQL thì `CHECK` chặn và `ROLLBACK`). |
| **4** | `0:40` | `R1` (Phiếu xác nhận) | Chọn đơn `DH015` vừa tạo, nhập tên nhân viên lập phiếu, tải và mở PDF A4 dọc | **Tuân:** Chứng từ do Nhân viên kinh doanh lập gửi Khách hàng; file PDF 1 trang A4 có tên người lập và 2 ô ký. |
| **5** | `0:50` | `F2` (Quản lý & Hủy đơn) | Chọn `DH010`, chọn `"Đã hủy tour"`, xem trước phạt rồi bấm Lưu | **Tuân:** Tiền phạt tính tự động từ `NgayDat`, `NgayHuy`, `NgayXuatPhat` (còn 22 ngày -> phạt 10% = `1.600.000 đ`, hoàn `14.400.000 đ`); trả lại 4 chỗ cho `LT05` và xóa chuyến xe trong cùng `Transaction`. |
| **6** | `0:30` | `F3` (Đánh giá) | Chọn `KH004`, đánh giá đơn hoàn thành `DH004` | **Thịnh:** Minh họa thuộc tính phức hợp đánh giá tour và nơi nghỉ; chỉ đơn đã `HOANTHANH` và chưa đánh giá mới xuất hiện. |
| **7** | `0:50` | `R2` (Báo cáo doanh thu) | Kỳ `01/09/2026 - 31/12/2026`, nhập tên kế toán lập, mở PDF A4 ngang | **Khánh:** Dùng `GROUP BY ... WITH ROLLUP` tính dòng `TỔNG CỘNG`; Kế toán lập trình Ban Giám đốc duyệt, có khối ký trên PDF A4 ngang. |
| **8** | `0:20` | MySQL Workbench | Chạy toàn bộ `database/4_KiemTra_RangBuoc.sql` | **Khánh:** Kết quả trả về **0 dòng (rỗng)** — chứng minh sau toàn bộ thao tác thêm/sửa/hủy, dữ liệu trong 12 bảng hoàn toàn nhất quán và thỏa mãn mọi ràng buộc liên bảng (`RB22` - `RB32`). |
