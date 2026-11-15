# Hệ thống quản lý đặt tour du lịch miền Bắc

Bài tập lớn môn Cơ sở dữ liệu, Học viện Công nghệ Bưu chính Viễn thông (PTIT).

Cơ sở dữ liệu quản lý tour, lịch khởi hành, đơn đặt tour của 15 tỉnh thành miền Bắc, có liên kết nhà nghỉ, homestay và đơn vị vận tải. Ứng dụng đi kèm gồm form nhập, màn hình tìm kiếm và báo cáo.

## Thành viên

| Họ và tên         | Mã sinh viên | Phụ trách                                                                  |
| ----------------- | ------------ | -------------------------------------------------------------------------- |
| Nguyễn Tất Đạt    | `B24DCCN117` | ERD, ánh xạ lược đồ, form đặt tour (F1)                                    |
| Nguyễn Tiến Thịnh | `B24DCCN546` | Thực thể, ràng buộc, chuẩn hóa 3NF, form đánh giá (F3), biên tập báo cáo   |
| Bùi Đức Tuân      | `B24DCCN590` | Yêu cầu dữ liệu, nghiệp vụ, form quản lý đơn (F2), phiếu xác nhận (R1)     |
| Nguyễn Quốc Khánh | `B24DCCN311` | Cài đặt database, Data Diagram, tìm kiếm (S1), báo cáo doanh thu (R2)      |

## Chức năng chính

- Quản lý tour, lịch khởi hành, số chỗ; không cho bán quá chỗ.
- Đặt tour kèm nơi nghỉ và tối đa 2 chuyến xe trung chuyển.
- Hủy đơn có tính tiền phạt, tiền hoàn theo ngày đặt, ngày hủy và ngày khởi hành.
- Đánh giá tour và nơi nghỉ sau chuyến đi.
- Tìm kiếm lịch trình theo từ khóa, tỉnh đến, khoảng giá, ngày, số chỗ, điểm đánh giá.
- Báo cáo phiếu xác nhận đặt tour và báo cáo doanh thu, đánh giá theo tour (có thông tin người lập, nơi nhận và khối ký xuất PDF).

## Công nghệ

| Thành phần             | Phiên bản      |
| ---------------------- | -------------- |
| MySQL Server           | 8.0.16 trở lên |
| MySQL Workbench        | 8.0            |
| Python                 | 3.11 đến 3.13  |
| streamlit              | 1.66.0         |
| mysql-connector-python | 26.7.0         |
| pandas                 | 3.0.6          |

## Cấu trúc thư mục

```text
BTL-quan-ly-dat-tour-csdl-PTIT/
├── README.md
├── .gitignore
├── database/
│   ├── 1_QuanLyDatTour_v3.sql
│   ├── 2_QuanLyDatTour_v3_TruyVan.sql
│   ├── 3_QuanLyDatTour_v3_UngDung.sql
│   └── 4_KiemTra_RangBuoc.sql
├── docs/
│   ├── Ke_hoach_Tong_hop_BTL_CSDL.md
│   ├── Huong_dan_chi_tiet_Khanh.md
│   ├── Huong_dan_chi_tiet_Dat.md
│   ├── Huong_dan_chi_tiet_Tuan.md
│   ├── Huong_dan_chi_tiet_Thinh.md
│   ├── diagrams/
│   │   ├── ERD.drawio
│   │   ├── ERD.png
│   │   ├── DataDiagram.mwb
│   │   └── DataDiagram.png
│   └── report/
│       └── Bao_cao_BTL_CSDL_QuanLyDatTour.docx
├── tour_app/
│   ├── app.py
│   ├── db.py
│   ├── requirements.txt
│   ├── pages/
│   │   ├── 1_Dat_tour.py
│   │   ├── 2_Quan_ly_don.py
│   │   ├── 3_Danh_gia.py
│   │   ├── 4_Tim_kiem.py
│   │   ├── 5_Phieu_xac_nhan.py
│   │   └── 6_Bao_cao_doanh_thu.py
│   └── templates/
│       ├── phieu_xac_nhan.html
│       └── bao_cao_doanh_thu.html
└── screenshots/
    ├── Hinh01_ERD.png
    ├── Hinh02_DataDiagram.png
    ├── Hinh03_LoiRangBuoc.png
    ├── Hinh04_F1_GiaoDien.png
    ├── Hinh05a_F1_Loi.png
    ├── Hinh05b_F1_Loi.png
    ├── Hinh06_F2_GiaoDien.png
    ├── Hinh07_F2_Loi.png
    ├── Hinh08_F3_GiaoDien.png
    ├── Hinh09_S1_CaoCap.png
    ├── Hinh10_R1_ManHinh.png
    ├── Hinh11_R1_PDF.png
    ├── Hinh12_R2_ManHinh.png
    └── Hinh13_R2_PDF.png
```

| Thư mục        | Nội dung                                                                                                   |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| `database/`    | Script tạo database, truy vấn minh họa, SQL của ứng dụng, truy vấn kiểm tra ràng buộc. Chạy theo số thứ tự |
| `docs/`        | Kế hoạch thực hiện, ERD, Data Diagram, báo cáo Word/PDF                                                    |
| `tour_app/`    | Ứng dụng Streamlit: trang chủ, kết nối CSDL, 6 màn hình chức năng (`pages/`) và mẫu in HTML (`templates/`) |
| `screenshots/` | 13 hình chụp màn hình và sơ đồ dùng để chèn vào báo cáo                                                    |

## Cài đặt và chạy

1. Mở `database/1_QuanLyDatTour_v3.sql` trong MySQL Workbench và chạy toàn bộ script (`Ctrl + Shift + Enter`). Script tạo database `QuanLyDatTour` gồm 12 bảng, 2 view và dữ liệu mẫu.
2. Tạo môi trường ảo và cài thư viện Python tại thư mục gốc dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r tour_app\requirements.txt
```

3. Đặt mật khẩu tài khoản `root` của MySQL bằng biến môi trường `MYSQL_PASSWORD` (không ghi mật khẩu vào code), sau đó đóng và mở lại PowerShell:

```powershell
setx MYSQL_PASSWORD "mat_khau_cua_may"
```

4. Chạy ứng dụng:

```powershell
.\.venv\Scripts\Activate.ps1
cd tour_app
streamlit run app.py
```

- Trang chủ mở tại `http://localhost:8501` và báo: `"Đã kết nối cơ sở dữ liệu: 12 bảng"`.
- Chế độ demo: trong `db.py`, `CHE_DO_DEMO = True` cố định thời điểm hiện tại là `23/10/2026 08:00` để kết quả khớp dữ liệu mẫu.
- Muốn đưa dữ liệu về trạng thái ban đầu: chạy lại `database/1_QuanLyDatTour_v3.sql`.

## Tài liệu và Kiểm tra

- **Kế hoạch tổng hợp & Lộ trình thực thi toàn nhóm:** `docs/Ke_hoach_Tong_hop_BTL_CSDL.md`.
- **Sổ tay hướng dẫn chi tiết từng bước cho từng thành viên:**
  - Khánh: `docs/Huong_dan_chi_tiet_Khanh.md`.
  - Đạt: `docs/Huong_dan_chi_tiet_Dat.md`.
  - Tuân: `docs/Huong_dan_chi_tiet_Tuan.md`.
  - Thịnh: `docs/Huong_dan_chi_tiet_Thinh.md`.
- **Báo cáo tổng hợp (9 chương và Phụ lục):** `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`.
- **Kiểm tra dữ liệu sau khi thao tác:** chạy `database/4_KiemTra_RangBuoc.sql`, kết quả rỗng là dữ liệu đúng.

## Quy ước làm việc

- Nhánh chính `main` chỉ nhận code qua Pull Request.
- Nhánh theo màn hình: `feature/f1-dat-tour`, `feature/f2-quan-ly-don`, `feature/f3-danh-gia`, `feature/s1-tim-kiem`, `feature/r1-phieu-xac-nhan`, `feature/r2-bao-cao-doanh-thu`. Sửa lỗi: `fix/ten-loi`.
- Commit theo Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
