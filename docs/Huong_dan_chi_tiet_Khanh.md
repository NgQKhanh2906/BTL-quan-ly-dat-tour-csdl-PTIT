# Hướng dẫn Cầm tay Chỉ việc Chi tiết cho KHÁNH (Từ A đến Z)

- **Họ và tên:** Nguyễn Quốc Khánh (`B24DCCN311`)
- **Vai trò trong nhóm:** Phụ trách Cơ sở dữ liệu (4 tệp SQL), Sơ đồ vật lý (`DataDiagram.mwb`, `DataDiagram.png`), Khung ứng dụng dùng chung (`db.py`, `app.py`, `requirements.txt`), Màn hình Tìm kiếm (`S1` - `4_Tim_kiem.py`), Báo cáo Doanh thu (`R2` - `6_Bao_cao_doanh_thu.py` & `bao_cao_doanh_thu.html`), Quản lý GitHub Repository, Máy chạy Demo chính và Phụ lục báo cáo.
- **Mục tiêu của tài liệu này:** Bạn chỉ cần đọc duy nhất tài liệu này và làm lần lượt từ Bước 1 đến Bước cuối là hoàn thành 100% công việc của mình mà không cần mở lại bất kỳ tài liệu cũ nào. Mọi câu lệnh SQL, code Python, thao tác phím bấm trên MySQL Workbench, VS Code, PowerShell, Edge và lý do kỹ thuật đằng sau từng bước đều nằm trọn tại đây.

---

## Phần 1. Tổng quan Lịch làm việc của Khánh theo Ngày (K1 -> K12)

| Mã Task | Ngày thực hiện | Tên công việc | Nền tảng sử dụng | Sản phẩm đầu ra (File cụ thể) | Cách tự kiểm tra đã đạt |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **K1** | **05/11/2026** | Bàn giao báo cáo nháp `.docx` cho Thịnh | GitHub / Thư mục chung | `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` | Thịnh mở được trong Word và cập nhật được mục lục |
| **K2** | **05/11 - 06/11** | Tạo 4 tệp SQL (12 bảng) và khung ứng dụng (`db.py`, `app.py`, `requirements.txt`) | MySQL Workbench 8.0, VS Code, PowerShell | 4 file trong `database/`, 3 file trong `tour_app/` | Chạy tệp 1 có 12 bảng, 56 ràng buộc; chạy `streamlit run app.py` báo `"Đã kết nối cơ sở dữ liệu: 12 bảng"` |
| **K3** | **07/11/2026** | Đẩy tệp SQL số 1 và khung `tour_app` lên GitHub, hỗ trợ 3 bạn cài máy | PowerShell, GitHub | Nhánh `main` trên GitHub | Cả 4 máy trong nhóm mở được trang chủ tại `http://localhost:8501` |
| **K4** | **08/11 - 09/11** | Viết màn hình Tìm kiếm `S1` và Báo cáo doanh thu `R2` | VS Code, Streamlit | `tour_app/pages/4_Tim_kiem.py`, `6_Bao_cao_doanh_thu.py`, `templates/bao_cao_doanh_thu.html` | `S1` đạt 6 ca kiểm thử; `R2` kỳ `01/09 - 31/12/2026` có dòng `TỔNG CỘNG` = `79.110.000 đ` |
| **K5** | **09/11/2026** | Bổ sung Người lập, Nơi nhận, Khối ký cho báo cáo `R2` | VS Code, Microsoft Edge | Cập nhật `6_Bao_cao_doanh_thu.py` và `bao_cao_doanh_thu.html` | Để trống người lập thì ẩn nút tải; in ra PDF A4 ngang vừa khít 1 trang |
| **K6** | **10/11/2026** | Vẽ sơ đồ `DataDiagram` bằng Reverse Engineer | MySQL Workbench 8.0 | `docs/diagrams/DataDiagram.mwb`, `DataDiagram.png`, `screenshots/Hinh02_DataDiagram.png` | Sơ đồ có đúng 12 hộp bảng (không có view), 13 đường nối chân gà |
| **K7** | **11/11/2026** | Chụp Hình 3, 9, 12, 13 và thử nghiệm phát hiện lỗi `RB26` trên `LT07` | MySQL Workbench, Edge, Paint | `Hinh03_LoiRangBuoc.png`, `Hinh09_S1_CaoCap.png`, `Hinh12_R2_ManHinh.png`, `Hinh13_R2_PDF.png` | 4 ảnh rõ nét đặt trong `screenshots/`; tệp 4 bắt được lỗi `RB26 - LT07` |
| **K8** | **12/11 - 13/11** | Rà soát mục 3.5, Chương 5, Chương 7, mục 8.2, Phụ lục trong báo cáo Word | Microsoft Word (chế độ đọc), VS Code | `docs/GopY_Khanh.md` | Mọi câu SQL và số đếm trong báo cáo khớp 100% với tệp SQL và code thật |
| **K9** | **14/11/2026** | Kiểm thử chéo màn hình `F2` và `R1` của Tuân | Streamlit, MySQL Workbench | Danh sách lỗi gửi Tuân (nếu có) | Kiểm tra đủ 5 ca của `F2` và 3 điểm kiểm tra của `R1` |
| **K10** | **15/11 - 16/11** | Sửa lỗi `S1`/`R2` (nếu có), gộp (merge) code cả nhóm vào `main`, hoàn thiện `README.md` | PowerShell, GitHub | Nhánh `main` hoàn chỉnh (đóng băng tính năng tối 16/11) | Clone repo mới về máy bất kỳ đều chạy được ngay |
| **K11** | **17/11 - 19/11** | Đóng gói bộ file nộp (`CSDL/`, `ThietKe/`, `UngDung/tour_app.zip`, `README.txt`) | Windows Explorer, PowerShell | Bộ thư mục nộp chuẩn hóa | Giải nén `tour_app.zip` ra thư mục khác chạy được, không chứa `.venv` hay mật khẩu |
| **K12** | **20/11 - 22/11** | Chuẩn bị máy demo chính và quay Video demo dự phòng 6 phút | Xbox Game Bar (`Win + Alt + R`), Streamlit, Workbench | File video `.mp4` dài ~6 phút | Xem lại video thấy rõ chữ, chạy mượt cả 8 bước demo |

---

## Phần 2. Hướng dẫn Cầm tay Chỉ việc Từng Task (Tại sao làm vậy & Làm như thế nào)

---

### BƯỚC 1 (Task K2 - Phần A): Tạo 4 Tệp SQL Chuẩn 12 Bảng trên MySQL Workbench

#### 1. Tại sao phải chia thành 4 tệp SQL và tại sao có 12 bảng?
- **Lý do tách thành 12 bảng:** Thiết kế ban đầu có 11 bảng, trong đó bảng `KhachHang` chứa cả `SoID` (số thẻ thanh toán) và `LoaiThe` (Visa, MasterCard, ATM nội địa). Vì mỗi số thẻ thuộc đúng 1 loại thẻ (`SoID -> LoaiThe`), nên `LoaiThe` phụ thuộc bắc cầu vào khóa chính `MaKH` (`MaKH -> SoID -> LoaiThe`), làm vi phạm dạng chuẩn 3NF. Nhóm tách riêng bảng `TheThanhToan(SoID, LoaiThe)` (Phương án A) để cả **12 bảng đều đạt chuẩn 3NF và BCNF**.
- **Lý do chia đúng 4 tệp SQL đánh số 1 -> 4:**
  - Tệp `1_QuanLyDatTour_v3.sql`: Chứa lệnh xóa và tạo lại CSDL, 12 bảng, 56 ràng buộc, 2 view và 104 dòng dữ liệu mẫu. Bất cứ khi nào dữ liệu bị thay đổi sau khi thử nghiệm, chỉ cần mở tệp số 1 nhấn `Ctrl + Shift + Enter` là toàn bộ CSDL quay về trạng thái gốc trong 2 giây.
  - Tệp `2_QuanLyDatTour_v3_TruyVan.sql`: Chứa 13 câu truy vấn mẫu từ cơ bản đến nâng cao (JOIN, GROUP BY, HAVING, Subquery, Phép chia `NOT EXISTS` lồng nhau, Transaction) phục vụ Chương 5 báo cáo.
  - Tệp `3_QuanLyDatTour_v3_UngDung.sql`: Chứa toàn bộ câu lệnh SQL dùng trong 6 màn hình ứng dụng (dùng biến `@Ten` để chạy thử trực tiếp được trên Workbench).
  - Tệp `4_KiemTra_RangBuoc.sql`: Vì MySQL không cho phép `CHECK` tham chiếu sang bảng khác và nhóm không dùng Trigger, các ràng buộc liên bảng (`RB22` đến `RB32`) được kiểm tra bằng tệp này. Chạy tệp số 4 mà trả về **0 dòng (rỗng)** tức là dữ liệu hoàn toàn đúng.

#### 2. Thao tác tạo Tệp 1: `database/1_QuanLyDatTour_v3.sql`
1. Mở **VS Code** tại thư mục `D:\Khanh\CSDL`.
2. Tạo file mới tại đường dẫn `database/1_QuanLyDatTour_v3.sql` (lưu bảng mã `UTF-8`).
3. Dán toàn bộ nội dung SQL hoàn chỉnh dưới đây vào `database/1_QuanLyDatTour_v3.sql` rồi nhấn `Ctrl + S`:

```sql
DROP DATABASE IF EXISTS QuanLyDatTour;

CREATE DATABASE QuanLyDatTour
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE QuanLyDatTour;

-- 1. Bang TinhThanh (15 tinh thanh mien Bac)
CREATE TABLE TinhThanh (
    MaTinh  VARCHAR(5)  NOT NULL,
    TenTinh VARCHAR(50) NOT NULL,
    PRIMARY KEY (MaTinh),
    CONSTRAINT uq_TinhThanh_TenTinh UNIQUE (TenTinh)
);

-- 2. Bang TheThanhToan (Tach tu KhachHang de dat 3NF/BCNF)
CREATE TABLE TheThanhToan (
    SoID    VARCHAR(30) NOT NULL,
    LoaiThe VARCHAR(30) COLLATE utf8mb4_0900_as_cs NOT NULL,
    PRIMARY KEY (SoID),
    CONSTRAINT chk_TheThanhToan_SoID CHECK (SoID REGEXP '^[0-9]{12,19}$'),
    CONSTRAINT chk_TheThanhToan_LoaiThe CHECK (LoaiThe IN ('Visa', 'MasterCard', 'ATM nội địa'))
);

-- 3. Bang KhachHang
CREATE TABLE KhachHang (
    MaKH   VARCHAR(10)  NOT NULL,
    HoTen  VARCHAR(100) NOT NULL,
    Email  VARCHAR(100) NOT NULL,
    DiaChi VARCHAR(255) NULL,
    SoID   VARCHAR(30)  NULL,
    PRIMARY KEY (MaKH),
    CONSTRAINT uq_KhachHang_Email UNIQUE (Email),
    CONSTRAINT fk_KhachHang_TheThanhToan FOREIGN KEY (SoID)
        REFERENCES TheThanhToan (SoID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_KhachHang_Email CHECK (Email LIKE '%_@_%._%')
);

-- 4. Bang SDT_KhachHang (Thuoc tinh da tri SDT)
CREATE TABLE SDT_KhachHang (
    MaKH        VARCHAR(10) NOT NULL,
    SoDienThoai VARCHAR(10) NOT NULL,
    PRIMARY KEY (MaKH, SoDienThoai),
    CONSTRAINT fk_SDTKhachHang_KhachHang FOREIGN KEY (MaKH)
        REFERENCES KhachHang (MaKH)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT chk_SDTKhachHang_SoDienThoai CHECK (SoDienThoai REGEXP '^0[0-9]{9}$')
);

-- 5. Bang Tour
CREATE TABLE Tour (
    MaTour         VARCHAR(10)  NOT NULL,
    TenTour        VARCHAR(150) NOT NULL,
    MoTa           TEXT         NULL,
    MaTinhXuatPhat VARCHAR(5)   NOT NULL,
    MaTinhDen      VARCHAR(5)   NOT NULL,
    PRIMARY KEY (MaTour),
    CONSTRAINT fk_Tour_TinhXuatPhat FOREIGN KEY (MaTinhXuatPhat)
        REFERENCES TinhThanh (MaTinh)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_Tour_TinhDen FOREIGN KEY (MaTinhDen)
        REFERENCES TinhThanh (MaTinh)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- 6. Bang LichTrinh
CREATE TABLE LichTrinh (
    MaLichTrinh  VARCHAR(10)   NOT NULL,
    NgayXuatPhat DATETIME      NOT NULL,
    NgayKetThuc  DATETIME      NOT NULL,
    DiemTapTrung VARCHAR(255)  NOT NULL,
    DiemTraKhach VARCHAR(255)  NOT NULL,
    GiaCoBan     DECIMAL(12,0) NOT NULL,
    SoChoToiDa   INT           NOT NULL,
    SoChoDaDat   INT           NOT NULL DEFAULT 0,
    MaTour       VARCHAR(10)   NOT NULL,
    PRIMARY KEY (MaLichTrinh),
    CONSTRAINT fk_LichTrinh_Tour FOREIGN KEY (MaTour)
        REFERENCES Tour (MaTour)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_LichTrinh_NgayKetThuc CHECK (NgayKetThuc >= NgayXuatPhat),
    CONSTRAINT chk_LichTrinh_GiaCoBan CHECK (GiaCoBan > 0),
    CONSTRAINT chk_LichTrinh_SoChoToiDa CHECK (SoChoToiDa > 0),
    CONSTRAINT chk_LichTrinh_SoChoDaDat CHECK (SoChoDaDat BETWEEN 0 AND SoChoToiDa)
);

-- 7. Bang NhaNghi
CREATE TABLE NhaNghi (
    MaNhaNghi      VARCHAR(10)   NOT NULL,
    TenNhaNghi     VARCHAR(150)  NOT NULL,
    LoaiHinh       VARCHAR(20)   COLLATE utf8mb4_0900_as_cs NOT NULL,
    DiaChi         VARCHAR(255)  NOT NULL,
    SoDienThoai    VARCHAR(10)   NOT NULL,
    GiaPhongMoiDem DECIMAL(12,0) NOT NULL,
    MaTinh         VARCHAR(5)    NOT NULL,
    PRIMARY KEY (MaNhaNghi),
    CONSTRAINT fk_NhaNghi_TinhThanh FOREIGN KEY (MaTinh)
        REFERENCES TinhThanh (MaTinh)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_NhaNghi_LoaiHinh CHECK (LoaiHinh IN ('Nhà nghỉ', 'Homestay')),
    CONSTRAINT chk_NhaNghi_SoDienThoai CHECK (SoDienThoai REGEXP '^0[0-9]{9}$'),
    CONSTRAINT chk_NhaNghi_GiaPhong CHECK (GiaPhongMoiDem > 0)
);

-- 8. Bang DonViVanTai
CREATE TABLE DonViVanTai (
    MaDVVT      VARCHAR(10)  NOT NULL,
    TenDonVi    VARCHAR(150) NOT NULL,
    SoDienThoai VARCHAR(10)  NOT NULL,
    DiaChi      VARCHAR(255) NULL,
    PRIMARY KEY (MaDVVT),
    CONSTRAINT uq_DonViVanTai_SoDienThoai UNIQUE (SoDienThoai),
    CONSTRAINT chk_DonViVanTai_SoDienThoai CHECK (SoDienThoai REGEXP '^0[0-9]{9}$')
);

-- 9. Bang Xe
CREATE TABLE Xe (
    BienSo VARCHAR(12) NOT NULL,
    SoCho  INT         NOT NULL,
    MaDVVT VARCHAR(10) NOT NULL,
    PRIMARY KEY (BienSo),
    CONSTRAINT fk_Xe_DonViVanTai FOREIGN KEY (MaDVVT)
        REFERENCES DonViVanTai (MaDVVT)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_Xe_BienSo CHECK (BienSo REGEXP '^[0-9]{2}[A-Z][A-Z0-9]?-[0-9]{4,5}$'),
    CONSTRAINT chk_Xe_SoCho CHECK (SoCho BETWEEN 4 AND 45)
);

-- 10. Bang TrangThaiDonHang
CREATE TABLE TrangThaiDonHang (
    MaTrangThai  VARCHAR(10) NOT NULL,
    TenTrangThai VARCHAR(30) NOT NULL,
    ThuTu        INT         NOT NULL,
    PRIMARY KEY (MaTrangThai),
    CONSTRAINT uq_TrangThaiDonHang_Ten UNIQUE (TenTrangThai)
);

-- 11. Bang DonHang
CREATE TABLE DonHang (
    MaDonHang      VARCHAR(10)   NOT NULL,
    NgayDat        DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    SoLuongKhach   INT           NOT NULL,
    SoPhong        INT           NOT NULL DEFAULT 0,
    MaTrangThai    VARCHAR(10)   NOT NULL DEFAULT 'DAT',
    NgayHuy        DATETIME      NULL,
    LyDoHuy        VARCHAR(255)  NULL,
    DiemTour       TINYINT       NULL,
    NhanXetTour    VARCHAR(500)  NULL,
    DiemNhaNghi    TINYINT       NULL,
    NhanXetNhaNghi VARCHAR(500)  NULL,
    NgayDanhGia    DATETIME      NULL,
    MaKH           VARCHAR(10)   NOT NULL,
    MaLichTrinh    VARCHAR(10)   NOT NULL,
    MaNhaNghi      VARCHAR(10)   NULL,
    PRIMARY KEY (MaDonHang),
    CONSTRAINT fk_DonHang_KhachHang FOREIGN KEY (MaKH)
        REFERENCES KhachHang (MaKH)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_DonHang_LichTrinh FOREIGN KEY (MaLichTrinh)
        REFERENCES LichTrinh (MaLichTrinh)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_DonHang_NhaNghi FOREIGN KEY (MaNhaNghi)
        REFERENCES NhaNghi (MaNhaNghi)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT fk_DonHang_TrangThai FOREIGN KEY (MaTrangThai)
        REFERENCES TrangThaiDonHang (MaTrangThai)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CONSTRAINT chk_DonHang_SoLuongKhach CHECK (SoLuongKhach > 0),
    CONSTRAINT chk_DonHang_NhaNghi CHECK (
        (MaNhaNghi IS NULL AND SoPhong = 0)
        OR (MaNhaNghi IS NOT NULL AND SoPhong BETWEEN 1 AND SoLuongKhach)
    ),
    CONSTRAINT chk_DonHang_Huy CHECK (
        (MaTrangThai = 'HUY' AND NgayHuy IS NOT NULL)
        OR (MaTrangThai <> 'HUY' AND NgayHuy IS NULL)
    ),
    CONSTRAINT chk_DonHang_NgayHuy CHECK (NgayHuy >= NgayDat),
    CONSTRAINT chk_DonHang_LyDoHuy CHECK (LyDoHuy IS NULL OR NgayHuy IS NOT NULL),
    CONSTRAINT chk_DonHang_DiemTour CHECK (DiemTour BETWEEN 1 AND 5),
    CONSTRAINT chk_DonHang_DiemNhaNghi CHECK (DiemNhaNghi BETWEEN 1 AND 5),
    CONSTRAINT chk_DonHang_DanhGia CHECK (
        (DiemTour IS NULL AND DiemNhaNghi IS NULL) OR MaTrangThai = 'HOANTHANH'
    ),
    CONSTRAINT chk_DonHang_DanhGiaNhaNghi CHECK (DiemNhaNghi IS NULL OR MaNhaNghi IS NOT NULL),
    CONSTRAINT chk_DonHang_NhanXet CHECK (
        (NhanXetTour IS NULL OR DiemTour IS NOT NULL)
        AND (NhanXetNhaNghi IS NULL OR DiemNhaNghi IS NOT NULL)
    ),
    CONSTRAINT chk_DonHang_NgayDanhGia CHECK (
        (DiemTour IS NULL AND DiemNhaNghi IS NULL AND NgayDanhGia IS NULL)
        OR ((DiemTour IS NOT NULL OR DiemNhaNghi IS NOT NULL) AND NgayDanhGia IS NOT NULL)
    )
);

-- 12. Bang ChuyenTrungChuyen (Thuc the yeu)
CREATE TABLE ChuyenTrungChuyen (
    MaDonHang   VARCHAR(10)  NOT NULL,
    LoaiChuyen  VARCHAR(20)  NOT NULL,
    DiaChiDon   VARCHAR(255) NULL,
    ThoiGianDon DATETIME     NOT NULL,
    BienSoXe    VARCHAR(12)  NULL,
    PRIMARY KEY (MaDonHang, LoaiChuyen),
    CONSTRAINT fk_ChuyenTrungChuyen_DonHang FOREIGN KEY (MaDonHang)
        REFERENCES DonHang (MaDonHang)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_ChuyenTrungChuyen_Xe FOREIGN KEY (BienSoXe)
        REFERENCES Xe (BienSo)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT chk_ChuyenTrungChuyen_Loai CHECK (LoaiChuyen IN ('DON_TAI_NHA', 'VE_NOI_NGHI')),
    CONSTRAINT chk_ChuyenTrungChuyen_DiaChiDon CHECK (
        (LoaiChuyen = 'DON_TAI_NHA' AND DiaChiDon IS NOT NULL)
        OR (LoaiChuyen <> 'DON_TAI_NHA' AND DiaChiDon IS NULL)
    )
);

-- View 1: v_DonHang_ChiTiet
CREATE VIEW v_DonHang_ChiTiet AS
SELECT x.*,
       ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienPhat,
       x.TongTien - ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienHoan
FROM (
    SELECT d.MaDonHang,
           d.NgayDat,
           kh.MaKH,
           kh.HoTen,
           t.MaTour,
           t.TenTour,
           tden.TenTinh AS TinhDen,
           lt.MaLichTrinh,
           lt.NgayXuatPhat,
           lt.NgayKetThuc,
           DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS SoDem,
           d.SoLuongKhach,
           lt.GiaCoBan,
           nn.TenNhaNghi,
           d.SoPhong,
           nn.GiaPhongMoiDem,
           d.SoLuongKhach * lt.GiaCoBan AS TienTour,
           d.SoPhong * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TienPhong,
           d.SoLuongKhach * lt.GiaCoBan
           + d.SoPhong * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TongTien,
           d.MaTrangThai,
           tt.TenTrangThai,
           d.NgayHuy,
           d.LyDoHuy,
           DATEDIFF(lt.NgayXuatPhat, d.NgayHuy) AS SoNgayTruocKhoiHanh,
           CASE
               WHEN d.NgayHuy IS NULL THEN NULL
               WHEN TIMESTAMPDIFF(HOUR, d.NgayDat, d.NgayHuy) < 24
                    AND DATEDIFF(lt.NgayXuatPhat, d.NgayHuy) >= 7 THEN 0
               WHEN DATEDIFF(lt.NgayXuatPhat, d.NgayHuy) >= 15 THEN 10
               WHEN DATEDIFF(lt.NgayXuatPhat, d.NgayHuy) >= 7 THEN 30
               WHEN DATEDIFF(lt.NgayXuatPhat, d.NgayHuy) >= 3 THEN 50
               ELSE 100
           END AS TyLePhat,
           d.DiemTour,
           d.NhanXetTour,
           d.DiemNhaNghi,
           d.NhanXetNhaNghi,
           d.NgayDanhGia
    FROM DonHang d
    JOIN KhachHang kh ON kh.MaKH = d.MaKH
    JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
    JOIN Tour t ON t.MaTour = lt.MaTour
    JOIN TinhThanh tden ON tden.MaTinh = t.MaTinhDen
    JOIN TrangThaiDonHang tt ON tt.MaTrangThai = d.MaTrangThai
    LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
) AS x;

-- View 2: v_LichTrungChuyen
CREATE VIEW v_LichTrungChuyen AS
SELECT c.MaDonHang,
       c.LoaiChuyen,
       CASE c.LoaiChuyen
           WHEN 'DON_TAI_NHA' THEN 'Đón tại nhà'
           ELSE 'Về nơi nghỉ'
       END AS TenLoaiChuyen,
       c.ThoiGianDon,
       CASE c.LoaiChuyen
           WHEN 'DON_TAI_NHA' THEN c.DiaChiDon
           ELSE lt.DiemTraKhach
       END AS DiemDon,
       CASE c.LoaiChuyen
           WHEN 'DON_TAI_NHA' THEN lt.DiemTapTrung
           ELSE nn.DiaChi
       END AS DiemTra,
       d.SoLuongKhach,
       kh.HoTen AS TenKhach,
       c.BienSoXe,
       x.SoCho,
       dv.TenDonVi
FROM ChuyenTrungChuyen c
JOIN DonHang d ON d.MaDonHang = c.MaDonHang
JOIN KhachHang kh ON kh.MaKH = d.MaKH
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
LEFT JOIN Xe x ON x.BienSo = c.BienSoXe
LEFT JOIN DonViVanTai dv ON dv.MaDVVT = x.MaDVVT;

-- Du lieu mau (104 dong)
INSERT INTO TinhThanh (MaTinh, TenTinh) VALUES
('HN', 'Hà Nội'), ('HP', 'Hải Phòng'), ('QN', 'Quảng Ninh'),
('CB', 'Cao Bằng'), ('LS', 'Lạng Sơn'), ('LCH', 'Lai Châu'),
('DB', 'Điện Biên'), ('SL', 'Sơn La'), ('TQ', 'Tuyên Quang'),
('LC', 'Lào Cai'), ('TN', 'Thái Nguyên'), ('PT', 'Phú Thọ'),
('BN', 'Bắc Ninh'), ('HY', 'Hưng Yên'), ('NB', 'Ninh Bình');

INSERT INTO TrangThaiDonHang (MaTrangThai, TenTrangThai, ThuTu) VALUES
('DAT', 'Đã đặt tour', 1),
('THANHTOAN', 'Đã thanh toán', 2),
('HOANTHANH', 'Hoàn thành tour', 3),
('HUY', 'Đã hủy tour', 4);

INSERT INTO TheThanhToan (SoID, LoaiThe) VALUES
('4111111111111111', 'Visa'),
('5555555555554444', 'MasterCard'),
('9704000000000018', 'ATM nội địa'),
('4000000000000002', 'Visa'),
('4012888888881881', 'Visa');

INSERT INTO KhachHang (MaKH, HoTen, Email, DiaChi, SoID) VALUES
('KH001', 'Nguyễn Văn An',   'an.nguyen@gmail.com',   '12 Cầu Giấy, Hà Nội',                '4111111111111111'),
('KH002', 'Trần Thị Bình',   'binh.tran@gmail.com',   '45 Lê Lợi, Hải Phòng',               '5555555555554444'),
('KH003', 'Lê Hoàng Cường',  'cuong.le@yahoo.com',    '8 Trần Phú, Hà Đông, Hà Nội',        NULL),
('KH004', 'Phạm Thu Dung',   'dung.pham@outlook.com', '21 Bạch Đằng, Quảng Ninh',           '9704000000000018'),
('KH005', 'Hoàng Minh Đức',  'duc.hoang@gmail.com',   '5 Kim Mã, Ba Đình, Hà Nội',          '4000000000000002'),
('KH006', 'Vũ Thị Hà',       'ha.vu@gmail.com',       '3 Hùng Vương, Lào Cai',              NULL),
('KH007', 'Đặng Quốc Khải',  'khai.dang@gmail.com',   '77 Nguyễn Trãi, Thanh Xuân, Hà Nội', '4012888888881881'),
('KH008', 'Bùi Thanh Mai',   'mai.bui@gmail.com',     '19 Lạch Tray, Hải Phòng',            NULL);

INSERT INTO SDT_KhachHang (MaKH, SoDienThoai) VALUES
('KH001', '0912345678'), ('KH001', '0987654321'),
('KH002', '0901234567'), ('KH003', '0934567890'),
('KH004', '0978123456'), ('KH004', '0868123456'),
('KH005', '0359876543'), ('KH006', '0398765432'),
('KH007', '0965432109'), ('KH008', '0383456789');

INSERT INTO Tour (MaTour, TenTour, MoTa, MaTinhXuatPhat, MaTinhDen) VALUES
('T01', 'Hà Nội - Vịnh Hạ Long 2N1Đ',            'Du thuyền ngắm vịnh, hang Sửng Sốt, chèo kayak.',         'HN', 'QN'),
('T02', 'Hà Nội - Sa Pa - Fansipan 3N2Đ',        'Bản Cát Cát, cáp treo Fansipan, chợ Sa Pa.',              'HN', 'LC'),
('T03', 'Hà Nội - Tràng An - Bái Đính 1 ngày',   'Đi thuyền Tràng An, chùa Bái Đính.',                      'HN', 'NB'),
('T04', 'Hà Nội - Mộc Châu 2N1Đ',                'Đồi chè trái tim, thác Dải Yếm, rừng thông Bản Áng.',     'HN', 'SL'),
('T05', 'Hải Phòng - Cát Bà 2N1Đ',               'Vườn quốc gia Cát Bà, vịnh Lan Hạ.',                      'HP', 'HP'),
('T06', 'Hà Nội - Cao Bằng - Bản Giốc 3N2Đ',     'Thác Bản Giốc, động Ngườm Ngao, hồ Thang Hen.',           'HN', 'CB'),
('T07', 'Hạ Long du thuyền cao cấp 3N2Đ',        'Ngủ đêm trên du thuyền, vịnh Lan Hạ, làng chài Cửa Vạn.', 'HN', 'QN'),
('T08', 'Hành trình Tây Bắc - Điện Biên 6N5Đ',   'Mộc Châu, Sơn La, Điện Biên Phủ, Mường Thanh.',           'HN', 'DB'),
('T09', 'Hà Giang - Đồng Văn - Mã Pì Lèng 4N3Đ', 'Cột cờ Lũng Cú, đèo Mã Pì Lèng, sông Nho Quế.',           'HN', 'TQ');

INSERT INTO LichTrinh (MaLichTrinh, NgayXuatPhat, NgayKetThuc, DiemTapTrung, DiemTraKhach, GiaCoBan, SoChoToiDa, SoChoDaDat, MaTour) VALUES
('LT01', '2026-09-12 07:00:00', '2026-09-13 18:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Cảng tàu khách Tuần Châu, Quảng Ninh', 2900000, 25, 6, 'T01'),
('LT02', '2026-10-02 06:30:00', '2026-10-04 19:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Quảng trường Sa Pa, Lào Cai',           3500000, 25, 5, 'T02'),
('LT03', '2026-10-10 07:30:00', '2026-10-11 17:00:00', 'Bến xe Cầu Rào, Hải Phòng',          'Bến tàu Cát Bà, Hải Phòng',            1800000, 20, 2, 'T05'),
('LT04', '2026-10-24 07:00:00', '2026-10-25 18:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Cảng tàu khách Tuần Châu, Quảng Ninh', 2900000, 25, 2, 'T01'),
('LT05', '2026-11-14 06:30:00', '2026-11-16 19:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Quảng trường Sa Pa, Lào Cai',           3500000, 25, 4, 'T02'),
('LT06', '2026-11-21 07:30:00', '2026-11-21 19:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Bến thuyền Tràng An, Ninh Bình',        900000, 30, 3, 'T03'),
('LT07', '2026-12-05 07:00:00', '2026-12-06 18:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Trung tâm Mộc Châu, Sơn La',           2200000, 25, 0, 'T04'),
('LT08', '2026-11-20 08:00:00', '2026-11-22 16:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Cảng tàu khách Tuần Châu, Quảng Ninh', 11500000, 12, 2, 'T07'),
('LT09', '2026-12-10 06:00:00', '2026-12-15 20:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Trung tâm Điện Biên Phủ, Điện Biên',   10800000, 16, 2, 'T08'),
('LT10', '2026-11-26 20:00:00', '2026-11-29 20:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Thị trấn Đồng Văn, Tuyên Quang',        5900000, 20, 0, 'T09'),
('LT11', '2026-12-24 06:30:00', '2026-12-26 19:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Thác Bản Giốc, Cao Bằng',              4200000, 25, 0, 'T06'),
('LT12', '2026-12-31 08:00:00', '2027-01-02 16:00:00', 'Nhà hát Lớn, 1 Tràng Tiền, Hà Nội', 'Cảng tàu khách Tuần Châu, Quảng Ninh', 12900000, 12, 0, 'T07');

INSERT INTO NhaNghi (MaNhaNghi, TenNhaNghi, LoaiHinh, DiaChi, SoDienThoai, GiaPhongMoiDem, MaTinh) VALUES
('NN01', 'Homestay Vịnh Xanh',      'Homestay', '15 Hạ Long, Bãi Cháy, Quảng Ninh',    '0912000111', 450000, 'QN'),
('NN02', 'Nhà nghỉ Bãi Cháy Biển',  'Nhà nghỉ', '88 Hậu Cần, Bãi Cháy, Quảng Ninh',    '0912000222', 350000, 'QN'),
('NN03', 'Homestay Bản Mây',        'Homestay', 'Bản Cát Cát, Sa Pa, Lào Cai',         '0912000333', 400000, 'LC'),
('NN04', 'Nhà nghỉ Sương Sớm',      'Nhà nghỉ', '12 Cầu Mây, Sa Pa, Lào Cai',          '0912000444', 500000, 'LC'),
('NN05', 'Homestay Đồi Chè',        'Homestay', 'Tiểu khu 19/5, Mộc Châu, Sơn La',     '0912000555', 380000, 'SL'),
('NN06', 'Nhà nghỉ Biển Cát Bà',    'Nhà nghỉ', '210 Một Tháng Tư, Cát Bà, Hải Phòng', '0912000666', 420000, 'HP'),
('NN07', 'Homestay Thác Bạc',       'Homestay', 'Xã Đàm Thủy, Cao Bằng',               '0912000777', 350000, 'CB'),
('NN08', 'Homestay Cao Nguyên Đá',  'Homestay', '18 Phố Cổ, Đồng Văn, Tuyên Quang',    '0912000888', 420000, 'TQ'),
('NN09', 'Nhà nghỉ Hoa Ban',        'Nhà nghỉ', '45 Võ Nguyên Giáp, Điện Biên',        '0912000999', 400000, 'DB');

INSERT INTO DonViVanTai (MaDVVT, TenDonVi, SoDienThoai, DiaChi) VALUES
('VT01', 'Vận tải Sao Bắc',      '0904555111', '120 Giải Phóng, Hà Nội'),
('VT02', 'Xe đưa đón Biển Xanh', '0904555222', '30 Hạ Long, Quảng Ninh'),
('VT03', 'Vận tải Núi Rừng',     '0904555333', '5 Điện Biên Phủ, Lào Cai');

INSERT INTO Xe (BienSo, SoCho, MaDVVT) VALUES
('29B-12345', 16, 'VT01'),
('29A-67890', 7,  'VT01'),
('29A-11223', 4,  'VT01'),
('14B-24680', 16, 'VT02'),
('14A-13579', 7,  'VT02'),
('24B-55667', 16, 'VT03'),
('24A-88990', 7,  'VT03');

INSERT INTO DonHang (MaDonHang, NgayDat, SoLuongKhach, SoPhong, MaTrangThai, NgayHuy, LyDoHuy,
                     DiemTour, NhanXetTour, DiemNhaNghi, NhanXetNhaNghi, NgayDanhGia,
                     MaKH, MaLichTrinh, MaNhaNghi) VALUES
('DH001', '2026-08-20 10:00:00', 2, 1, 'HOANTHANH', NULL, NULL,
 5, 'Lịch trình hợp lý, hướng dẫn viên nhiệt tình.', 4, 'Phòng sạch, view vịnh đẹp.', '2026-09-15 20:00:00',
 'KH001', 'LT01', 'NN01'),
('DH002', '2026-08-25 15:30:00', 4, 2, 'HOANTHANH', NULL, NULL,
 4, 'Đồ ăn ngon, xe hơi chật.', 3, 'Phòng hơi ồn.', '2026-09-14 21:00:00',
 'KH002', 'LT01', 'NN02'),
('DH003', '2026-09-10 09:00:00', 2, 1, 'HOANTHANH', NULL, NULL,
 5, 'Fansipan tuyệt đẹp.', 5, 'Chủ nhà thân thiện.', '2026-10-05 19:00:00',
 'KH003', 'LT02', 'NN03'),
('DH004', '2026-09-15 11:00:00', 3, 2, 'HOANTHANH', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH004', 'LT02', 'NN04'),
('DH005', '2026-09-20 08:00:00', 2, 1, 'HOANTHANH', NULL, NULL,
 4, 'Biển đẹp, lịch hơi gấp.', 4, 'Gần biển, tiện đi lại.', '2026-10-12 10:00:00',
 'KH008', 'LT03', 'NN06'),
('DH006', '2026-09-25 14:00:00', 2, 0, 'HUY', '2026-10-08 09:00:00', 'Ốm, không đi được',
 NULL, NULL, NULL, NULL, NULL,
 'KH005', 'LT03', NULL),
('DH007', '2026-10-05 10:00:00', 2, 1, 'THANHTOAN', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH001', 'LT04', 'NN01'),
('DH008', '2026-10-06 16:00:00', 3, 0, 'HUY', '2026-10-15 20:00:00', 'Trùng lịch công tác',
 NULL, NULL, NULL, NULL, NULL,
 'KH007', 'LT04', NULL),
('DH009', '2026-09-25 09:00:00', 2, 1, 'HUY', '2026-10-01 10:00:00', 'Đổi kế hoạch gia đình',
 NULL, NULL, NULL, NULL, NULL,
 'KH006', 'LT05', 'NN03'),
('DH010', '2026-10-12 09:30:00', 4, 2, 'DAT', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH002', 'LT05', 'NN04'),
('DH011', '2026-10-15 09:00:00', 2, 0, 'HUY', '2026-10-15 20:00:00', 'Đặt nhầm ngày',
 NULL, NULL, NULL, NULL, NULL,
 'KH003', 'LT08', NULL),
('DH012', '2026-10-16 14:00:00', 2, 0, 'THANHTOAN', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH007', 'LT08', NULL),
('DH013', '2026-10-17 10:00:00', 3, 0, 'DAT', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH005', 'LT06', NULL),
('DH014', '2026-10-18 08:00:00', 2, 1, 'DAT', NULL, NULL,
 NULL, NULL, NULL, NULL, NULL,
 'KH004', 'LT09', 'NN09');

INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon, BienSoXe) VALUES
('DH001', 'DON_TAI_NHA', '12 Cầu Giấy, Hà Nội',         '2026-09-12 06:00:00', '29A-11223'),
('DH001', 'VE_NOI_NGHI', NULL,                          '2026-09-12 11:30:00', '14A-13579'),
('DH003', 'DON_TAI_NHA', '8 Trần Phú, Hà Đông, Hà Nội', '2026-10-02 05:30:00', '29A-11223'),
('DH003', 'VE_NOI_NGHI', NULL,                          '2026-10-02 13:00:00', '24A-88990'),
('DH007', 'DON_TAI_NHA', '12 Cầu Giấy, Hà Nội',         '2026-10-24 06:00:00', '29A-11223'),
('DH007', 'VE_NOI_NGHI', NULL,                          '2026-10-24 11:30:00', NULL),
('DH010', 'DON_TAI_NHA', '45 Lê Lợi, Hải Phòng',        '2026-11-14 04:00:00', NULL),
('DH014', 'DON_TAI_NHA', '21 Bạch Đằng, Quảng Ninh',    '2026-12-10 03:30:00', '14A-13579');
```

#### 3. Thao tác tạo Tệp 2: `database/2_QuanLyDatTour_v3_TruyVan.sql`
Tạo file `database/2_QuanLyDatTour_v3_TruyVan.sql` trong VS Code và dán 13 câu truy vấn minh họa sau vào:

```sql
USE QuanLyDatTour;

-- Q1. Tim tour di Quang Ninh (go khong dau)
SELECT t.MaTour, t.TenTour, txp.TenTinh AS NoiXuatPhat, tden.TenTinh AS NoiDen
FROM Tour t
JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
JOIN TinhThanh tden ON tden.MaTinh = t.MaTinhDen
WHERE tden.TenTinh LIKE '%quang ninh%';

-- Q2. Lich trinh khoi hanh trong thang 11/2026
SELECT lt.MaLichTrinh, t.TenTour, lt.NgayXuatPhat, lt.GiaCoBan
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
WHERE lt.NgayXuatPhat >= '2026-11-01' AND lt.NgayXuatPhat < '2026-12-01'
ORDER BY lt.NgayXuatPhat;

-- Q3. Lich su dat tour cua khach KH001
SELECT d.MaDonHang, t.TenTour, lt.NgayXuatPhat, d.SoLuongKhach, nn.TenNhaNghi, tt.TenTrangThai
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
JOIN Tour t ON t.MaTour = lt.MaTour
JOIN TrangThaiDonHang tt ON tt.MaTrangThai = d.MaTrangThai
LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
WHERE d.MaKH = 'KH001'
ORDER BY lt.NgayXuatPhat;

-- Q4. Don da huy kem tien phat
SELECT MaDonHang, HoTen, NgayDat, NgayHuy, NgayXuatPhat, SoNgayTruocKhoiHanh,
       TongTien, TyLePhat, TienPhat, TienHoan
FROM v_DonHang_ChiTiet
WHERE MaTrangThai = 'HUY'
ORDER BY NgayHuy;

-- Q5. Thong ke don theo trang thai
SELECT tt.TenTrangThai, COUNT(d.MaDonHang) AS SoDon, COALESCE(SUM(d.SoLuongKhach), 0) AS SoKhach
FROM TrangThaiDonHang tt
LEFT JOIN DonHang d ON d.MaTrangThai = tt.MaTrangThai
GROUP BY tt.MaTrangThai, tt.TenTrangThai, tt.ThuTu
ORDER BY tt.ThuTu;

-- Q6. Doanh thu theo tour
SELECT t.MaTour, t.TenTour,
       COUNT(v.MaDonHang) AS SoDon,
       COALESCE(SUM(v.TongTien), 0) AS DoanhThu
FROM Tour t
LEFT JOIN v_DonHang_ChiTiet v ON v.MaTour = t.MaTour
                             AND v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH')
GROUP BY t.MaTour, t.TenTour
ORDER BY DoanhThu DESC;

-- Q7. Khach chi tieu tren 10 trieu
SELECT MaKH, HoTen, SUM(TongTien) AS TongChiTieu
FROM v_DonHang_ChiTiet
WHERE MaTrangThai IN ('THANHTOAN', 'HOANTHANH')
GROUP BY MaKH, HoTen
HAVING SUM(TongTien) > 10000000
ORDER BY TongChiTieu DESC;

-- Q8. Ty le lap day theo thang khoi hanh
SELECT DATE_FORMAT(lt.NgayXuatPhat, '%m/%Y') AS ThangKhoiHanh,
       COUNT(*) AS SoLichTrinh,
       SUM(lt.SoChoDaDat) AS TongChoDaDat,
       SUM(lt.SoChoToiDa) AS TongCho,
       ROUND(SUM(lt.SoChoDaDat) * 100 / SUM(lt.SoChoToiDa), 1) AS TyLeLapDay
FROM LichTrinh lt
GROUP BY DATE_FORMAT(lt.NgayXuatPhat, '%m/%Y')
ORDER BY MIN(lt.NgayXuatPhat);

-- Q9. Lich trinh gia cao nhat
SELECT lt.MaLichTrinh, t.TenTour, lt.NgayXuatPhat, lt.GiaCoBan
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
WHERE lt.GiaCoBan = (SELECT MAX(GiaCoBan) FROM LichTrinh);

-- Q10. Tour chua co don dat thanh cong
SELECT t.MaTour, t.TenTour
FROM Tour t
WHERE NOT EXISTS (
    SELECT 1
    FROM LichTrinh lt
    JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh
    WHERE lt.MaTour = t.MaTour
      AND d.MaTrangThai <> 'HUY'
);

-- Q11. Nha nghi co diem tu muc trung binh chung tro len
SELECT nn.MaNhaNghi, nn.TenNhaNghi, ROUND(AVG(d.DiemNhaNghi), 1) AS DiemTB
FROM NhaNghi nn
JOIN DonHang d ON d.MaNhaNghi = nn.MaNhaNghi
WHERE d.DiemNhaNghi IS NOT NULL
GROUP BY nn.MaNhaNghi, nn.TenNhaNghi
HAVING AVG(d.DiemNhaNghi) >= (
    SELECT AVG(DiemNhaNghi) FROM DonHang WHERE DiemNhaNghi IS NOT NULL
)
ORDER BY DiemTB DESC;

-- Q12. Khach da dung ca 2 loai chuyen trung chuyen (phep chia)
SELECT kh.MaKH, kh.HoTen
FROM KhachHang kh
WHERE NOT EXISTS (
    SELECT 1
    FROM (SELECT DISTINCT LoaiChuyen FROM ChuyenTrungChuyen) AS lc
    WHERE NOT EXISTS (
        SELECT 1
        FROM ChuyenTrungChuyen c
        JOIN DonHang d ON d.MaDonHang = c.MaDonHang
        WHERE d.MaKH = kh.MaKH
          AND c.LoaiChuyen = lc.LoaiChuyen
    )
);

-- Q13. Huy don trong transaction
START TRANSACTION;

UPDATE DonHang
SET MaTrangThai = 'HUY',
    NgayHuy = '2026-10-19 10:00:00',
    LyDoHuy = 'Bận việc gia đình'
WHERE MaDonHang = 'DH010';

UPDATE LichTrinh lt
JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh
SET lt.SoChoDaDat = lt.SoChoDaDat - d.SoLuongKhach
WHERE d.MaDonHang = 'DH010';

DELETE FROM ChuyenTrungChuyen
WHERE MaDonHang = 'DH010';

SELECT v.MaDonHang, v.TenTrangThai, v.TyLePhat, v.TienPhat, v.TienHoan, lt.SoChoDaDat,
       (SELECT COUNT(*) FROM ChuyenTrungChuyen c WHERE c.MaDonHang = v.MaDonHang) AS SoChuyen
FROM v_DonHang_ChiTiet v
JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
WHERE v.MaDonHang = 'DH010';

ROLLBACK;
```

#### 4. Thao tác tạo Tệp 3: `database/3_QuanLyDatTour_v3_UngDung.sql`
Tạo file `database/3_QuanLyDatTour_v3_UngDung.sql` tổng hợp toàn bộ các câu lệnh SQL của F1, F2, F3, S1, R1, R2:

```sql
USE QuanLyDatTour;
SET @HienTai = '2026-10-23 08:00:00';

-- ==========================================
-- PHAN 1. F1 - FORM DAT TOUR (DAT)
-- ==========================================

-- F1.1: Danh sach khach hang
SELECT MaKH, CONCAT(MaKH, ' - ', HoTen) AS HienThi, DiaChi
FROM KhachHang
ORDER BY MaKH;

-- F1.2: Lich trinh chua khoi hanh, con cho
SELECT lt.MaLichTrinh,
       t.TenTour,
       lt.NgayXuatPhat,
       DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS SoDem,
       lt.GiaCoBan,
       lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
       t.MaTinhDen
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
WHERE lt.NgayXuatPhat > @HienTai
  AND lt.SoChoToiDa - lt.SoChoDaDat > 0
ORDER BY lt.NgayXuatPhat;

-- F1.3: Noi nghi o tinh diem den
SET @MaTinhDen = 'TQ';
SELECT MaNhaNghi, TenNhaNghi, LoaiHinh, GiaPhongMoiDem
FROM NhaNghi
WHERE MaTinh = @MaTinhDen
ORDER BY GiaPhongMoiDem;

-- F1.4: Sinh ma don moi
SELECT CONCAT('DH', LPAD(COALESCE(MAX(CAST(SUBSTRING(MaDonHang, 3) AS UNSIGNED)), 0) + 1, 3, '0')) AS MaDonHangMoi
FROM DonHang;

-- F1.5: Tong tien du kien
SET @MaDonHang = 'DH015';
SET @MaKH = 'KH006';
SET @MaLichTrinh = 'LT10';
SET @SoKhach = 5;
SET @MaNhaNghi = 'NN08';
SET @SoPhong = 2;
SET @DiaChiDon = '3 Hùng Vương, Lào Cai';
SET @GioDon = '2026-11-26 15:00:00';
SET @GioVeNoiNghi = '2026-11-27 10:00:00';

SELECT @SoKhach * lt.GiaCoBan AS TienTour,
       @SoPhong * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TienPhong,
       @SoKhach * lt.GiaCoBan
       + @SoPhong * COALESCE(nn.GiaPhongMoiDem, 0) * DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) AS TongTienDuKien
FROM LichTrinh lt
LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = @MaNhaNghi
WHERE lt.MaLichTrinh = @MaLichTrinh;

-- F1.6: Luu don, tru cho, them chuyen trong 1 transaction
START TRANSACTION;

INSERT INTO DonHang (MaDonHang, NgayDat, SoLuongKhach, SoPhong, MaKH, MaLichTrinh, MaNhaNghi)
VALUES (@MaDonHang, @HienTai, @SoKhach, @SoPhong, @MaKH, @MaLichTrinh, @MaNhaNghi);

UPDATE LichTrinh
SET SoChoDaDat = SoChoDaDat + @SoKhach
WHERE MaLichTrinh = @MaLichTrinh;

INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, DiaChiDon, ThoiGianDon)
VALUES (@MaDonHang, 'DON_TAI_NHA', @DiaChiDon, @GioDon);

INSERT INTO ChuyenTrungChuyen (MaDonHang, LoaiChuyen, ThoiGianDon)
VALUES (@MaDonHang, 'VE_NOI_NGHI', @GioVeNoiNghi);

SELECT v.MaDonHang, v.NgayDat, v.TongTien, v.TenTrangThai, lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai
FROM v_DonHang_ChiTiet v
JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
WHERE v.MaDonHang = @MaDonHang;

ROLLBACK;

-- ==========================================
-- PHAN 2. F2 - FORM QUAN LY DON (TUAN)
-- ==========================================

-- F2.1: Cac don co the cap nhat
SELECT MaDonHang, HoTen, TenTour, NgayXuatPhat, TenTrangThai
FROM v_DonHang_ChiTiet
WHERE MaTrangThai IN ('DAT', 'THANHTOAN')
ORDER BY NgayXuatPhat;

-- F2.2: Thong tin don
SET @MaDonHang = 'DH010';
SELECT MaDonHang, HoTen, TenTour, NgayXuatPhat, NgayKetThuc, SoLuongKhach, TongTien, TenTrangThai
FROM v_DonHang_ChiTiet
WHERE MaDonHang = @MaDonHang;

-- F2.3: Cac trang thai duoc phep chuyen
SELECT tt.MaTrangThai, tt.TenTrangThai
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
JOIN TrangThaiDonHang tt
  ON (d.MaTrangThai = 'DAT' AND tt.MaTrangThai = 'THANHTOAN')
  OR (d.MaTrangThai = 'THANHTOAN' AND tt.MaTrangThai = 'HOANTHANH' AND lt.NgayKetThuc < @HienTai)
  OR (d.MaTrangThai IN ('DAT', 'THANHTOAN') AND tt.MaTrangThai = 'HUY' AND lt.NgayXuatPhat > @HienTai)
WHERE d.MaDonHang = @MaDonHang
ORDER BY tt.ThuTu;

-- F2.4: Xem truoc tien phat
SET @NgayHuy = '2026-10-23 08:00:00';
SELECT x.MaDonHang,
       x.TongTien,
       x.SoNgayTruocKhoiHanh,
       x.TyLePhat,
       ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienPhat,
       x.TongTien - ROUND(x.TongTien * x.TyLePhat / 100, 0) AS TienHoan
FROM (
    SELECT v.MaDonHang,
           v.TongTien,
           DATEDIFF(v.NgayXuatPhat, @NgayHuy) AS SoNgayTruocKhoiHanh,
           CASE
               WHEN TIMESTAMPDIFF(HOUR, v.NgayDat, @NgayHuy) < 24
                    AND DATEDIFF(v.NgayXuatPhat, @NgayHuy) >= 7 THEN 0
               WHEN DATEDIFF(v.NgayXuatPhat, @NgayHuy) >= 15 THEN 10
               WHEN DATEDIFF(v.NgayXuatPhat, @NgayHuy) >= 7 THEN 30
               WHEN DATEDIFF(v.NgayXuatPhat, @NgayHuy) >= 3 THEN 50
               ELSE 100
           END AS TyLePhat
    FROM v_DonHang_ChiTiet v
    WHERE v.MaDonHang = @MaDonHang
) AS x;

-- F2.5: Luu huy don
SET @LyDoHuy = 'Bận việc gia đình';
START TRANSACTION;

UPDATE DonHang
SET MaTrangThai = 'HUY',
    NgayHuy = @NgayHuy,
    LyDoHuy = @LyDoHuy
WHERE MaDonHang = @MaDonHang AND MaTrangThai IN ('DAT', 'THANHTOAN');

UPDATE LichTrinh lt
JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh
SET lt.SoChoDaDat = lt.SoChoDaDat - d.SoLuongKhach
WHERE d.MaDonHang = @MaDonHang;

DELETE FROM ChuyenTrungChuyen
WHERE MaDonHang = @MaDonHang;

SELECT v.MaDonHang, v.TenTrangThai, v.TyLePhat, v.TienPhat, v.TienHoan, lt.SoChoDaDat,
       (SELECT COUNT(*) FROM ChuyenTrungChuyen c WHERE c.MaDonHang = v.MaDonHang) AS SoChuyen
FROM v_DonHang_ChiTiet v
JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
WHERE v.MaDonHang = @MaDonHang;

ROLLBACK;

-- F2.6: Chuyen sang thanh toan hoac hoan thanh
SET @MaDonHang = 'DH013';
SET @TrangThaiCu = 'DAT';
SET @TrangThaiMoi = 'THANHTOAN';

START TRANSACTION;

UPDATE DonHang
SET MaTrangThai = @TrangThaiMoi
WHERE MaDonHang = @MaDonHang AND MaTrangThai = @TrangThaiCu;

SELECT MaDonHang, TenTrangThai
FROM v_DonHang_ChiTiet
WHERE MaDonHang = @MaDonHang;

ROLLBACK;

-- ==========================================
-- PHAN 3. F3 - FORM DANH GIA (THINH)
-- ==========================================

-- F3.1: Chuyen di cho danh gia
SET @MaKH = 'KH004';
SELECT MaDonHang, TenTour, NgayXuatPhat, NgayKetThuc, TenNhaNghi
FROM v_DonHang_ChiTiet
WHERE MaKH = @MaKH AND MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL;

-- F3.2: Luu danh gia
SET @MaDonHang = 'DH004';
SET @DiemTour = 4;
SET @NhanXetTour = 'Cảnh đẹp, lịch trình vừa sức.';
SET @DiemNhaNghi = 4;
SET @NhanXetNhaNghi = 'Phòng ấm, sạch sẽ.';

START TRANSACTION;

UPDATE DonHang
SET DiemTour = @DiemTour,
    NhanXetTour = @NhanXetTour,
    DiemNhaNghi = @DiemNhaNghi,
    NhanXetNhaNghi = @NhanXetNhaNghi,
    NgayDanhGia = @HienTai
WHERE MaDonHang = @MaDonHang AND MaTrangThai = 'HOANTHANH' AND NgayDanhGia IS NULL;

SELECT MaDonHang, DiemTour, DiemNhaNghi, NgayDanhGia
FROM DonHang
WHERE MaDonHang = @MaDonHang;

ROLLBACK;

-- ==========================================
-- PHAN 4. S1 - MAN HINH TIM KIEM (KHANH)
-- ==========================================

-- S1.1: Danh sach tinh
SELECT MaTinh, TenTinh
FROM TinhThanh
ORDER BY TenTinh;

-- S1.2: Tim kiem lich trinh
SET @TuKhoa = NULL;
SET @MaTinhDen = NULL;
SET @GiaTu = 10000000;
SET @GiaDen = NULL;
SET @TuNgay = '2026-10-23';
SET @DenNgay = NULL;
SET @SoKhach = 1;
SET @DiemToiThieu = NULL;

SELECT lt.MaLichTrinh,
       t.TenTour,
       txp.TenTinh AS NoiDi,
       tden.TenTinh AS NoiDen,
       lt.NgayXuatPhat,
       DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) + 1 AS SoNgay,
       lt.GiaCoBan,
       lt.SoChoToiDa - lt.SoChoDaDat AS SoChoConLai,
       dg.DiemTB,
       COALESCE(dg.SoLuot, 0) AS SoLuotDanhGia
FROM LichTrinh lt
JOIN Tour t ON t.MaTour = lt.MaTour
JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
JOIN TinhThanh tden ON tden.MaTinh = t.MaTinhDen
LEFT JOIN (
    SELECT l.MaTour, ROUND(AVG(d.DiemTour), 1) AS DiemTB, COUNT(d.DiemTour) AS SoLuot
    FROM DonHang d
    JOIN LichTrinh l ON l.MaLichTrinh = d.MaLichTrinh
    WHERE d.DiemTour IS NOT NULL
    GROUP BY l.MaTour
) AS dg ON dg.MaTour = t.MaTour
WHERE (@TuKhoa IS NULL OR t.TenTour LIKE CONCAT('%', @TuKhoa, '%'))
  AND (@MaTinhDen IS NULL OR t.MaTinhDen = @MaTinhDen)
  AND (@GiaTu IS NULL OR lt.GiaCoBan >= @GiaTu)
  AND (@GiaDen IS NULL OR lt.GiaCoBan <= @GiaDen)
  AND lt.NgayXuatPhat >= @TuNgay
  AND (@DenNgay IS NULL OR lt.NgayXuatPhat < @DenNgay + INTERVAL 1 DAY)
  AND lt.SoChoToiDa - lt.SoChoDaDat >= @SoKhach
  AND (@DiemToiThieu IS NULL OR dg.DiemTB >= @DiemToiThieu)
ORDER BY lt.NgayXuatPhat, lt.GiaCoBan;

-- ==========================================
-- PHAN 5. R1 - PHIEU XAC NHAN (TUAN)
-- ==========================================

SET @MaDonHang = 'DH007';

-- R1.1: Thong tin chinh cua phieu
SELECT v.MaDonHang, v.NgayDat, v.TenTrangThai,
       v.HoTen, kh.Email,
       v.TenTour, txp.TenTinh AS TinhXuatPhat, v.TinhDen,
       v.NgayXuatPhat, v.NgayKetThuc, v.SoDem, lt.DiemTapTrung,
       v.SoLuongKhach, v.GiaCoBan, v.TienTour,
       v.TenNhaNghi, nn.LoaiHinh, nn.DiaChi AS DiaChiNhaNghi,
       v.SoPhong, v.GiaPhongMoiDem, v.TienPhong, v.TongTien,
       v.NgayHuy, v.LyDoHuy, v.TyLePhat, v.TienPhat, v.TienHoan
FROM v_DonHang_ChiTiet v
JOIN DonHang d ON d.MaDonHang = v.MaDonHang
JOIN KhachHang kh ON kh.MaKH = v.MaKH
JOIN LichTrinh lt ON lt.MaLichTrinh = v.MaLichTrinh
JOIN Tour t ON t.MaTour = v.MaTour
JOIN TinhThanh txp ON txp.MaTinh = t.MaTinhXuatPhat
LEFT JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
WHERE v.MaDonHang = @MaDonHang;

-- R1.2: Cac so dien thoai cua khach
SELECT GROUP_CONCAT(sdt.SoDienThoai ORDER BY sdt.SoDienThoai SEPARATOR ', ') AS SoDienThoai
FROM DonHang d
JOIN SDT_KhachHang sdt ON sdt.MaKH = d.MaKH
WHERE d.MaDonHang = @MaDonHang;

-- R1.3: Lich xe trung chuyen
SELECT TenLoaiChuyen, ThoiGianDon, DiemDon, DiemTra,
       COALESCE(BienSoXe, 'Chưa xếp xe') AS BienSoXe,
       COALESCE(TenDonVi, '') AS DonViVanTai
FROM v_LichTrungChuyen
WHERE MaDonHang = @MaDonHang
ORDER BY ThoiGianDon;

-- ==========================================
-- PHAN 6. R2 - BAO CAO DOANH THU (KHANH)
-- ==========================================

SET @TuNgay = '2026-09-01';
SET @DenNgay = '2026-12-31';

-- R2.1: Doanh thu theo tour
SELECT IF(GROUPING(t.MaTour), 'TỔNG CỘNG', t.MaTour) AS MaTour,
       IF(GROUPING(t.MaTour), '', t.TenTour) AS TenTour,
       COUNT(DISTINCT lt.MaLichTrinh) AS SoLichTrinh,
       COALESCE(SUM(v.MaTrangThai <> 'HUY'), 0) AS SoDon,
       COALESCE(SUM(CASE WHEN v.MaTrangThai <> 'HUY' THEN v.SoLuongKhach END), 0) AS SoKhach,
       COALESCE(SUM(v.MaTrangThai = 'HUY'), 0) AS SoDonHuy,
       COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0) AS DoanhThuDichVu,
       COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TienPhatHuy,
       COALESCE(SUM(CASE WHEN v.MaTrangThai IN ('THANHTOAN', 'HOANTHANH') THEN v.TongTien END), 0)
       + COALESCE(SUM(CASE WHEN v.MaTrangThai = 'HUY' THEN v.TienPhat END), 0) AS TongDoanhThu,
       ROUND(AVG(v.DiemTour), 1) AS DiemTourTB
FROM Tour t
JOIN LichTrinh lt ON lt.MaTour = t.MaTour
LEFT JOIN v_DonHang_ChiTiet v ON v.MaLichTrinh = lt.MaLichTrinh
WHERE lt.NgayXuatPhat >= @TuNgay AND lt.NgayXuatPhat < @DenNgay + INTERVAL 1 DAY
GROUP BY t.MaTour, t.TenTour WITH ROLLUP
HAVING GROUPING(t.TenTour) = 0 OR GROUPING(t.MaTour) = 1;

-- R2.2: Xep hang noi nghi
SELECT nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh,
       COUNT(d.DiemNhaNghi) AS SoLuotDanhGia,
       ROUND(AVG(d.DiemNhaNghi), 1) AS DiemTB
FROM NhaNghi nn
JOIN TinhThanh tt ON tt.MaTinh = nn.MaTinh
JOIN DonHang d ON d.MaNhaNghi = nn.MaNhaNghi
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.DiemNhaNghi IS NOT NULL
  AND lt.NgayXuatPhat >= @TuNgay AND lt.NgayXuatPhat < @DenNgay + INTERVAL 1 DAY
GROUP BY nn.MaNhaNghi, nn.TenNhaNghi, nn.LoaiHinh, tt.TenTinh
ORDER BY DiemTB DESC, SoLuotDanhGia DESC;
```

#### 5. Thao tác tạo Tệp 4: `database/4_KiemTra_RangBuoc.sql`
Tạo file `database/4_KiemTra_RangBuoc.sql` trong VS Code và dán đoạn SQL kiểm tra `RB22` đến `RB32` dưới đây:

```sql
USE QuanLyDatTour;

SELECT 'RB22 Ngày đặt trước ngày xuất phát' AS RangBuoc, d.MaDonHang AS DoiTuong
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.NgayDat >= lt.NgayXuatPhat
UNION ALL
SELECT 'RB23 Ngày hủy trước ngày xuất phát', d.MaDonHang
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.NgayHuy >= lt.NgayXuatPhat
UNION ALL
SELECT 'RB24 Nơi nghỉ cùng tỉnh điểm đến', d.MaDonHang
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
JOIN Tour t ON t.MaTour = lt.MaTour
JOIN NhaNghi nn ON nn.MaNhaNghi = d.MaNhaNghi
WHERE nn.MaTinh <> t.MaTinhDen
UNION ALL
SELECT 'RB25 Tour trong ngày không đặt nơi nghỉ', d.MaDonHang
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.MaNhaNghi IS NOT NULL
  AND DATEDIFF(lt.NgayKetThuc, lt.NgayXuatPhat) = 0
UNION ALL
SELECT 'RB26 Số chỗ đã đặt khớp với đơn', lt.MaLichTrinh
FROM LichTrinh lt
LEFT JOIN DonHang d ON d.MaLichTrinh = lt.MaLichTrinh AND d.MaTrangThai <> 'HUY'
GROUP BY lt.MaLichTrinh, lt.SoChoDaDat
HAVING lt.SoChoDaDat <> COALESCE(SUM(d.SoLuongKhach), 0)
UNION ALL
SELECT 'RB27 Chuyến về nơi nghỉ cần đơn có nơi nghỉ', c.MaDonHang
FROM ChuyenTrungChuyen c
JOIN DonHang d ON d.MaDonHang = c.MaDonHang
WHERE c.LoaiChuyen = 'VE_NOI_NGHI' AND d.MaNhaNghi IS NULL
UNION ALL
SELECT 'RB28 Giờ đón hợp lệ', c.MaDonHang
FROM ChuyenTrungChuyen c
JOIN DonHang d ON d.MaDonHang = c.MaDonHang
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE (c.LoaiChuyen = 'DON_TAI_NHA' AND c.ThoiGianDon >= lt.NgayXuatPhat)
   OR (c.LoaiChuyen = 'VE_NOI_NGHI' AND (c.ThoiGianDon < lt.NgayXuatPhat OR c.ThoiGianDon > lt.NgayKetThuc))
UNION ALL
SELECT 'RB29 Xe đủ chỗ cho số khách', c.MaDonHang
FROM ChuyenTrungChuyen c
JOIN DonHang d ON d.MaDonHang = c.MaDonHang
JOIN Xe x ON x.BienSo = c.BienSoXe
WHERE x.SoCho < d.SoLuongKhach
UNION ALL
SELECT 'RB30 Không có chuyến cho đơn đã hủy', c.MaDonHang
FROM ChuyenTrungChuyen c
JOIN DonHang d ON d.MaDonHang = c.MaDonHang
WHERE d.MaTrangThai = 'HUY'
UNION ALL
SELECT 'RB31 Chỉ đánh giá sau khi tour kết thúc', d.MaDonHang
FROM DonHang d
JOIN LichTrinh lt ON lt.MaLichTrinh = d.MaLichTrinh
WHERE d.NgayDanhGia < lt.NgayKetThuc
UNION ALL
SELECT 'RB32 Thẻ thanh toán phải có khách sử dụng', th.SoID
FROM TheThanhToan th
WHERE NOT EXISTS (
    SELECT 1
    FROM KhachHang kh
    WHERE kh.SoID = th.SoID
);
```

---

### BƯỚC 2 (Task K2 - Phần B): Tạo Khung Ứng dụng (`requirements.txt`, `db.py`, `app.py`)

#### 1. Tạo file `tour_app/requirements.txt`
Mở VS Code, tạo file `tour_app/requirements.txt` với đúng 3 dòng sau:
```text
streamlit==1.66.0
mysql-connector-python==26.7.0
pandas==3.0.6
```

#### 2. Tạo file `tour_app/db.py`
- **Tại sao phải dùng `os.environ.get("MYSQL_PASSWORD", "")` và `CHE_DO_DEMO = True`?**
  - Dùng `os.environ.get("MYSQL_PASSWORD", "")` để mỗi thành viên trong nhóm tự đặt mật khẩu MySQL trên máy mình bằng lệnh `setx MYSQL_PASSWORD "..."` mà không bao giờ phải sửa file `db.py` hay làm lộ mật khẩu trên GitHub.
  - Dùng `CHE_DO_DEMO = True` cố định thời điểm hiện tại là `23/10/2026 08:00` để dù hôm thuyết trình là ngày 23/11 hay 30/11/2026, các lịch trình trong tháng 10 và 11 vẫn chưa khởi hành, giúp mọi kết quả tìm kiếm, đặt tour, hủy đơn khớp 100% với số liệu đã in trong báo cáo Word.

Tạo file `tour_app/db.py` và dán đoạn code chuẩn sau:

```python
import os
from datetime import datetime

import mysql.connector

CAU_HINH = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": "QuanLyDatTour",
    "charset": "utf8mb4",
    "collation": "utf8mb4_0900_ai_ci",
}

CHE_DO_DEMO = True
HIEN_TAI_DEMO = datetime(2026, 10, 23, 8, 0, 0)

THONG_BAO_CHECK = {
    "chk_LichTrinh_SoChoDaDat": "Lịch trình không còn đủ chỗ cho số khách này",
    "chk_DonHang_NhaNghi": "Số phòng phải từ 1 đến số khách",
    "chk_DonHang_NgayHuy": "Ngày hủy phải sau ngày đặt",
    "chk_DonHang_DiemTour": "Điểm đánh giá phải từ 1 đến 5",
    "chk_DonHang_DiemNhaNghi": "Điểm đánh giá phải từ 1 đến 5",
    "chk_DonHang_NhanXet": "Có nhận xét thì phải chấm điểm",
}

THONG_BAO_MA_LOI = {
    1045: "Sai tài khoản hoặc mật khẩu MySQL (kiểm tra biến môi trường MYSQL_PASSWORD)",
    1062: "Dữ liệu đã tồn tại",
    1452: "Dữ liệu được chọn không còn tồn tại, vui lòng tải lại trang",
    2002: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
    2003: "Không kết nối được cơ sở dữ liệu, kiểm tra MySQL đã chạy chưa",
}


class KhongCoDongNao(Exception):
    pass


def hien_tai():
    if CHE_DO_DEMO:
        return HIEN_TAI_DEMO
    return datetime.now().replace(microsecond=0)


def ket_noi():
    return mysql.connector.connect(**CAU_HINH)


def doc(sql, tham_so=None):
    cn = ket_noi()
    try:
        cur = cn.cursor(dictionary=True)
        cur.execute(sql, tham_so or {})
        return cur.fetchall()
    finally:
        cn.close()


def ghi(cac_lenh):
    cn = ket_noi()
    try:
        cn.start_transaction()
        cur = cn.cursor()
        for sql, tham_so, phai_co_dong in cac_lenh:
            cur.execute(sql, tham_so)
            if phai_co_dong and cur.rowcount == 0:
                raise KhongCoDongNao()
        cn.commit()
    except Exception:
        cn.rollback()
        raise
    finally:
        cn.close()


def thong_bao_loi(loi):
    if isinstance(loi, KhongCoDongNao):
        return "Đơn đã thay đổi hoặc không còn ở trạng thái phù hợp, vui lòng tải lại trang"
    if isinstance(loi, mysql.connector.Error):
        if loi.errno == 3819:
            for ten, cau in THONG_BAO_CHECK.items():
                if ten in loi.msg:
                    return cau
            return "Dữ liệu không hợp lệ: " + loi.msg
        return THONG_BAO_MA_LOI.get(loi.errno, "Lỗi cơ sở dữ liệu, mã " + str(loi.errno))
    return "Lỗi không xác định: " + str(loi)


def dinh_dang_tien(so):
    if so is None:
        return ""
    return f"{int(so):,}".replace(",", ".") + " đ"


def dinh_dang_ngay(gia_tri):
    if gia_tri is None:
        return ""
    return gia_tri.strftime("%d/%m/%Y %H:%M")
```

#### 3. Tạo file `tour_app/app.py`
Tạo file `tour_app/app.py` để làm Trang chủ kiểm tra kết nối 12 bảng:

```python
import streamlit as st
from db import doc, dinh_dang_ngay, hien_tai, thong_bao_loi

st.set_page_config(page_title="Quản lý đặt tour miền Bắc", layout="wide")

st.title("Hệ thống quản lý đặt tour du lịch các tỉnh thành tại miền Bắc")
st.write("Bài tập lớn môn Cơ sở dữ liệu - Học viện Công nghệ Bưu chính Viễn thông (PTIT)")

try:
    ket_qua = doc(
        """
        SELECT COUNT(*) AS SoBang
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = 'QuanLyDatTour' AND TABLE_TYPE = 'BASE TABLE'
        """
    )
    so_bang = ket_qua[0]["SoBang"] if ket_qua else 0
    st.success(f"Đã kết nối cơ sở dữ liệu: {so_bang} bảng")
    st.caption(f"Thời điểm hệ thống hiện tại: {dinh_dang_ngay(hien_tai())}")
except Exception as loi:
    st.error(thong_bao_loi(loi))

st.markdown(
    """
### Chức năng hệ thống (chọn ở menu bên trái)
1. **Đặt tour (F1):** Tạo đơn đặt tour mới, chọn nơi nghỉ theo tỉnh đến và đăng ký tối đa 2 chuyến xe trung chuyển.
2. **Quản lý đơn (F2):** Cập nhật trạng thái đơn hàng, hủy đơn có xem trước tiền phạt và tiền hoàn.
3. **Đánh giá (F3):** Ghi nhận điểm và nhận xét đánh giá tour, nơi nghỉ sau khi chuyến đi hoàn thành.
4. **Tìm kiếm (S1):** Tra cứu lịch trình theo từ khóa, tỉnh đến, khoảng giá, ngày khởi hành, số chỗ, điểm đánh giá.
5. **Phiếu xác nhận (R1):** Xem và in phiếu xác nhận đặt tour (khổ A4 dọc).
6. **Báo cáo doanh thu (R2):** Tổng hợp doanh thu, số đơn hủy và điểm đánh giá theo tour (khổ A4 ngang).
"""
)
```

---

### BƯỚC 3 (Tasks K4 & K5): Viết Màn hình Tìm kiếm (`S1`) và Báo cáo Doanh thu (`R2`)

#### 1. Tạo màn hình Tìm kiếm `S1`: `tour_app/pages/4_Tim_kiem.py`
- **Tại sao câu lệnh SQL tìm kiếm lại viết `(@TuKhoa IS NULL OR t.TenTour LIKE ...)`?**
  - Khi người dùng bỏ trống một ô lọc trên giao diện, code Python truyền giá trị `None` (tương ứng `NULL` trong SQL). Khi đó biểu thức `@Loc IS NULL` có giá trị `TRUE`, khiến toàn bộ cụm `OR` luôn đúng và bộ lọc đó được bỏ qua. Nhờ vậy chỉ cần **duy nhất 1 câu SQL tĩnh có tham số** là xử lý được mọi tổ hợp của 8 bộ lọc mà không phải nối chuỗi `if/else` (tránh hoàn toàn lỗi SQL Injection).
- **Các bước làm:**
  1. Tạo nhánh `git checkout -b feature/s1-tim-kiem`.
  2. Tạo file `tour_app/pages/4_Tim_kiem.py` sử dụng câu lệnh `S1.1` và `S1.2` (đổi `@Ten` thành `%(Ten)s`).
  3. Thiết kế 8 bộ lọc theo đúng bảng đặc tả:
     - Ô 1: Từ khóa tên tour (`max_chars=100`, trống truyền `None`).
     - Ô 2: Tỉnh đến (`"Tất cả"` + 15 tỉnh từ `S1.1`, chọn `"Tất cả"` truyền `None`).
     - Ô 3 & Ô 4: Giá từ, Giá đến (bước nhảy `500.000`, kiểm tra nếu cả hai có nhập mà `GiaDen < GiaTu` thì báo lỗi `"Giá đến phải lớn hơn hoặc bằng giá từ"` và dừng).
     - Ô 5 & Ô 6: Khởi hành từ ngày (mặc định `hien_tai().date()` = `23/10/2026`), Khởi hành đến ngày (nếu `DenNgay < TuNgay` thì báo lỗi).
     - Ô 7: Số khách (mặc định `1`, tối thiểu `1`).
     - Ô 8: Điểm đánh giá tối thiểu (`"Tất cả"`, `3.0`, `4.0`, `4.5`).
     - Thêm nút bấm `"Tour cao cấp (từ 10 triệu)"`: khi bấm sẽ gán `GiaTu = 10000000` và chạy tìm kiếm ra 3 lịch trình `LT08`, `LT09`, `LT12`.

#### 2. Tạo Báo cáo Doanh thu `R2` kèm Người lập, Nơi nhận, Khối ký: `tour_app/pages/6_Bao_cao_doanh_thu.py` & `tour_app/templates/bao_cao_doanh_thu.html`
- **Tại sao phải thêm Người lập, Nơi nhận và Khối ký (Task `K5`)?**
  - Thang điểm của giảng viên ở Tiêu chí 7 (1,0 điểm) yêu cầu rõ: *"2 báo cáo xem trên màn hình, xuất file thực tế, nói rõ ai tạo, gửi ai"*. Nếu chỉ xuất bảng dữ liệu thuần túy sẽ bị trừ điểm chứng từ.
- **Các bước cập nhật trong `tour_app/pages/6_Bao_cao_doanh_thu.py`:**
  1. Tạo nhánh `git checkout -b feature/r2-bao-cao-doanh-thu main`.
  2. Đầu file đảm bảo có `from html import escape` và `from string import Template`.
  3. Đặt hằng số `NOI_NHAN = "Ban Giám đốc công ty du lịch"`.
  4. Dưới 2 ô chọn `Từ ngày` (mặc định `01/09/2026`) và `Đến ngày` (mặc định `31/12/2026`), thêm:
     ```python
     nguoi_lap = st.text_input("Người lập báo cáo", max_chars=100, placeholder="Họ tên nhân viên kế toán")
     st.caption(f"Nơi nhận: {NOI_NHAN}")
     ```
  5. Sau khi hiển thị 4 ô chỉ số tổng (`79.110.000 đ`, `10` đơn, `26` khách, `4` đơn hủy), Bảng A (Doanh thu theo tour dùng SQL `R2.1`) và Bảng B (Xếp hạng nơi nghỉ dùng SQL `R2.2`) trên màn hình, thêm đoạn kiểm tra trước khi tạo nút tải HTML:
     ```python
     if not nguoi_lap.strip():
         st.warning("Nhập tên người lập báo cáo để tải và in báo cáo")
         st.stop()

     html_bao_cao = tao_html(tu_ngay, den_ngay, dong_tour, dong_tong, dong_noi_nghi, nguoi_lap.strip())
     ```
  6. Trong hàm `tao_html(tu_ngay, den_ngay, dong_tour, dong_tong, dong_noi_nghi, nguoi_lap)`, truyền thêm 2 biến vào `mau.substitute(...)`:
     ```python
     nguoi_lap=escape(nguoi_lap),
     noi_nhan=NOI_NHAN,
     ```
- **Các bước cập nhật trong `tour_app/templates/bao_cao_doanh_thu.html`:**
  1. Thiết lập `@page { size: A4 landscape; margin: 12mm; }`, `body { font-family: Arial, sans-serif; font-size: 9pt; }`.
  2. Thêm CSS cho dòng người lập và khối ký:
     ```css
     .nguoi-lap { text-align: center; margin-bottom: 8px; }
     .ky-ten { display: flex; justify-content: space-around; margin-top: 6px; text-align: center; }
     ```
  3. Ngay dưới dòng `<div class="ky">Kỳ báo cáo ...</div>`, thêm:
     ```html
     <div class="nguoi-lap">Người lập: $nguoi_lap | Nơi nhận: $noi_nhan</div>
     ```
  4. Ngay trước thẻ đóng `</body>`, thêm khối chữ ký:
     ```html
     <div class="ky-ten">
     <div><b>Người lập báo cáo</b><br>(Ký, ghi rõ họ tên)<br><br>$nguoi_lap</div>
     <div><b>Ban Giám đốc duyệt</b><br>(Ký, ghi rõ họ tên)</div>
     </div>
     ```

---

### BƯỚC 4 (Task K6): Tạo Sơ đồ `DataDiagram` trên MySQL Workbench

1. Mở **MySQL Workbench 8.0**, kết nối vào Local instance, chạy lại `database/1_QuanLyDatTour_v3.sql` để chắc chắn CSDL có đủ 12 bảng.
2. Trên thanh menu trên cùng của Workbench, bấm `Database` -> chọn `Reverse Engineer...` (hoặc nhấn tổ hợp phím `Ctrl + R`).
3. Bấm `Next` -> nhập mật khẩu `root` -> bấm `Next` -> tích chọn vào ô `QuanLyDatTour` -> bấm `Next` -> bấm `Next`.
4. Tại màn hình **Select Objects to Reverse Engineer**:
   - **Tích chọn** `Import MySQL Table Objects` (12 objects).
   - **Bỏ tích** `Import MySQL View Objects` (để sơ đồ chỉ hiện 12 bảng, không hiện 2 view).
   - Bấm `Execute >` -> bấm `Next >` -> bấm `Finish`.
5. Trong cửa sổ sơ đồ EER Diagram vừa hiện ra, kéo sắp xếp 12 bảng thành 4 cụm gọn gàng, không để đường nối nào cắt ngang qua hộp bảng khác:
   - **Cụm 1 (Khách hàng):** `TinhThanh`, `TheThanhToan`, `KhachHang`, `SDT_KhachHang`.
   - **Cụm 2 (Tour):** `Tour`, `LichTrinh`.
   - **Cụm 3 (Đối tác):** `NhaNghi`, `DonViVanTai`, `Xe`.
   - **Cụm 4 (Đơn hàng):** `TrangThaiDonHang`, `DonHang`, `ChuyenTrungChuyen`.
6. Đếm kiểm tra: phải có đúng **12 hộp bảng** và **13 đường nối chân gà** (trong đó có 2 đường nét liền là quan hệ xác định nối vào `SDT_KhachHang` và `ChuyenTrungChuyen`, 11 đường nét đứt).
7. Bấm `File > Save Model As...` -> lưu vào `D:\Khanh\CSDL\docs\diagrams\DataDiagram.mwb`.
8. Bấm `File > Export > Export as PNG...` -> lưu thành `D:\Khanh\CSDL\docs\diagrams\DataDiagram.png` và copy thêm 1 bản đặt tên là `D:\Khanh\CSDL\screenshots\Hinh02_DataDiagram.png`.

---

### BƯỚC 5 (Task K7): Chụp 4 Hình (`Hinh03`, `Hinh09`, `Hinh12`, `Hinh13`) và Kiểm thử `RB26`

Trước khi chụp, mở Workbench chạy lại `database/1_QuanLyDatTour_v3.sql` để reset dữ liệu gốc.

#### 1. Chụp `screenshots/Hinh03_LoiRangBuoc.png` (4 mã lỗi trên Workbench)
1. Mở một tab Query mới trong MySQL Workbench (`Ctrl + T`), dán đúng 4 câu lệnh sai dưới đây vào:
   ```sql
   USE QuanLyDatTour;
   -- 1. Loi 1062: Trung khoa chinh
   INSERT INTO KhachHang (MaKH, HoTen, Email) VALUES ('KH001', 'Test Trùng Mã', 'test1@gmail.com');
   -- 2. Loi 3819: Vi pham CHECK (so cho da dat vuot so cho toi da)
   UPDATE LichTrinh SET SoChoDaDat = 13 WHERE MaLichTrinh = 'LT08';
   -- 3. Loi 1452: Vi pham khoa ngoai khi them (tinh TH khong co trong 15 tinh)
   INSERT INTO Tour (MaTour, TenTour, MaTinhXuatPhat, MaTinhDen) VALUES ('T10', 'Hà Nội - Sầm Sơn', 'HN', 'TH');
   -- 4. Loi 1451: Xoa dong cha dang duoc tham chieu
   DELETE FROM KhachHang WHERE MaKH = 'KH001';
   ```
2. Đặt con trỏ chuột vào dòng `USE QuanLyDatTour;` nhấn `Ctrl + Enter`.
3. Xóa sạch khung `Action Output` ở dưới cùng (click chuột phải vào khung `Action Output` -> chọn `Clear`).
4. Đặt con trỏ vào từng câu trong 4 câu lệnh sai ở trên và nhấn `Ctrl + Enter` lần lượt 4 lần.
5. Khi khung `Action Output` hiện đủ 4 dòng dấu nhân màu đỏ chứa 4 mã lỗi `Error Code: 1062`, `Error Code: 3819`, `Error Code: 1452`, `Error Code: 1451`, nhấn `Win + Shift + S` quét chụp gọn khung `Action Output`, mở Paint nhấn `Ctrl + V` và lưu vào `D:\Khanh\CSDL\screenshots\Hinh03_LoiRangBuoc.png`.

#### 2. Thử nghiệm Tệp 4 phát hiện lỗi `RB26` (Khớp đoạn cuối mục 5.5 báo cáo)
1. Chạy câu lệnh cố ý làm lệch số chỗ của `LT07`:
   ```sql
   UPDATE LichTrinh SET SoChoDaDat = 5 WHERE MaLichTrinh = 'LT07';
   ```
2. Mở và chạy toàn bộ `database/4_KiemTra_RangBuoc.sql` -> Xác nhận kết quả trả về đúng 1 dòng: `RB26 Số chỗ đã đặt khớp với đơn | LT07`.
3. Chạy lại `database/1_QuanLyDatTour_v3.sql` để khôi phục dữ liệu đúng -> Chạy lại tệp 4 xác nhận trả về **0 dòng**.

#### 3. Chụp `Hinh09_S1_CaoCap.png`, `Hinh12_R2_ManHinh.png`, `Hinh13_R2_PDF.png`
1. Mở trình duyệt tại `http://localhost:8501`, để tỷ lệ thu phóng `100%`, chiều rộng cửa sổ khoảng `1400 px`.
2. **`screenshots/Hinh09_S1_CaoCap.png`:** Vào menu **Tìm kiếm**, bấm nút `"Tour cao cấp (từ 10 triệu)"`, chụp vùng giao diện có bộ lọc và bảng kết quả 3 dòng (`LT08`, `LT09`, `LT12`).
3. **`screenshots/Hinh12_R2_ManHinh.png`:** Vào menu **Báo cáo doanh thu**, để kỳ mặc định `01/09/2026` đến `31/12/2026`, nhập tên `"Nguyễn Quốc Khánh"` vào ô Người lập báo cáo, chụp giao diện trên màn hình (thấy rõ 4 ô chỉ số `79.110.000 đ`, `10`, `26`, `4` và bảng doanh thu).
4. **`screenshots/Hinh13_R2_PDF.png`:** Bấm nút tải file HTML báo cáo doanh thu, mở file vừa tải bằng Microsoft Edge -> nhấn `Ctrl + P` -> chọn Máy in `"Lưu dưới dạng PDF"` (`Save as PDF`), Khổ giấy `A4`, Hướng `Ngang` (`Landscape`), Lề `Mặc định`, tích `"Đồ họa nền"` -> Lưu thành PDF. Mở file PDF đó bằng Edge, chọn chế độ `"Vừa trang"` (`Fit to page`), dùng `Win + Shift + S` chụp trọn vẹn trang giấy A4 ngang (không chụp thanh công cụ trình duyệt) và lưu thành `screenshots/Hinh13_R2_PDF.png`.

---

### BƯỚC 6 (Tasks K8, K9, K10, K11, K12): Rà Báo cáo, Quản lý GitHub, Đóng gói và Chuẩn bị Demo

#### 1. Task `K8` (12/11 - 13/11): Rà soát báo cáo và lập `docs/GopY_Khanh.md`
- Mở `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx` (chỉ đọc, không sửa trực tiếp vào file Word vì Thịnh là người duy nhất sửa file Word).
- Kiểm tra:
  - Mục 3.5 (tr. 16): Bảng đối chiếu ERD và Data Diagram (11 thực thể, 12 mối liên kết, 12 bảng, 13 khóa ngoại).
  - Chương 5 (tr. 20-22): Số lượng ràng buộc (`12 PK`, `13 FK`, `27 CHECK`, `4 UNIQUE` = `56`), câu lệnh `CREATE TABLE LichTrinh`, số dòng mẫu (`104`), bảng kiểm thử chặn lỗi.
  - Chương 7 (tr. 31-33) và Mục 8.2 (tr. 36-38): Câu lệnh SQL và bảng kết quả của `S1`, `R2`.
  - Phụ lục (tr. 41-42): Các lệnh cài đặt trên PowerShell và đường dẫn repo GitHub.
- Nếu có điểm nào cần sửa cho khớp với code thực tế, tạo file `docs/GopY_Khanh.md` theo bảng: `| Trang | Mục | Đang ghi | Sửa thành | Lý do |`.

#### 2. Task `K10` (16/11): Quy trình Review và Merge Pull Request của 3 thành viên vào `main`
Khi Đạt, Thịnh, Tuân đẩy nhánh `feature/...` lên GitHub, bạn thực hiện kiểm tra và gộp nhánh trên PowerShell:
```powershell
git fetch origin
git checkout main
git pull origin main

# Gop nhanh cua Dat (F1)
git merge origin/feature/f1-dat-tour

# Gop nhanh cua Tuan (F2 va R1)
git merge origin/feature/f2-quan-ly-don
git merge origin/feature/r1-phieu-xac-nhan

# Gop nhanh cua Thinh (F3)
git merge origin/feature/f3-danh-gia

# Chay thu streamlit run app.py va 4_KiemTra_RangBuoc.sql, neu khong loi thi push len main:
git push origin main
```

#### 3. Task `K11` (17/11 - 19/11): Đóng gói Bộ File Nộp chuẩn hóa
Tạo một thư mục đóng gói bên ngoài (ví dụ `D:\Khanh\Nhom_QuanLyDatTour`) theo đúng cấu trúc:
- `README.txt`: Chép nội dung từ mục `PHỤ LỤC. HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY` của báo cáo Word (thêm tên đề tài và danh sách 4 thành viên ở đầu file).
- `CSDL/`: Chép đủ 4 file từ `database/` (`1_QuanLyDatTour_v3.sql` đến `4_KiemTra_RangBuoc.sql`).
- `ThietKe/`: Chép đủ 4 file từ `docs/diagrams/` (`ERD.drawio`, `ERD.png`, `DataDiagram.mwb`, `DataDiagram.png`).
- `UngDung/tour_app.zip`: Nén thư mục `tour_app/` (kiểm tra chắc chắn bên trong file `.zip` **không có** thư mục `__pycache__` hay `.venv`, chỉ có `app.py`, `db.py`, `requirements.txt`, `pages/`, `templates/`).

---

## Phần 3. Phần Thuyết trình và Câu hỏi Vấn đáp Bảo vệ của Khánh

### I. Nhiệm vụ trong 15 phút Bảo vệ
- **Từ phút `7:00` đến `13:00` (6 phút Demo):** Bạn là người trực tiếp điều khiển chuột và bàn phím cho cả 8 bước demo (xem bảng 8 bước tại cuối file `docs/Ke_hoach_Tong_hop_BTL_CSDL.md`). Bạn trực tiếp thuyết minh ở:
  - **Bước 1 (`S1` - 40 giây):** Bấm `"Tour cao cấp (từ 10 triệu)"`, giải thích kỹ thuật dùng 1 câu `SELECT` có tham số `(@Loc IS NULL OR ...)` xử lý mọi tổ hợp lọc, kết quả ra `LT08`, `LT09`, `LT12`.
  - **Bước 7 (`R2` - 50 giây):** Mở báo cáo doanh thu kỳ `01/09/2026 - 31/12/2026`, nhập tên người lập, mở file PDF A4 ngang, giải thích kỹ thuật `GROUP BY ... WITH ROLLUP` và hàm `GROUPING()` để tính dòng `TỔNG CỘNG` (`79.110.000 đ`).
  - **Bước 8 (Workbench - 20 giây):** Chuyển sang cửa sổ MySQL Workbench đã mở sẵn `database/4_KiemTra_RangBuoc.sql`, nhấn `Ctrl + Shift + Enter`, chỉ vào kết quả **0 dòng (rỗng)** để khẳng định sau mọi thao tác thêm/sửa/hủy trong buổi demo, toàn bộ ràng buộc liên bảng vẫn được đảm bảo tuyệt đối.

### II. 6 Câu hỏi Vấn đáp Trọng tâm Khánh Cần Thuộc Lòng

1. **Làm sao hệ thống chống bán vượt số chỗ của lịch trình?**
   - *Trả lời:* Bảng `LichTrinh` có ràng buộc `chk_LichTrinh_SoChoDaDat CHECK (SoChoDaDat BETWEEN 0 AND SoChoToiDa)`. Khi đặt tour ở màn hình F1, lệnh `INSERT INTO DonHang` và lệnh `UPDATE LichTrinh SET SoChoDaDat = SoChoDaDat + SoKhach` được chạy trong cùng 1 `Transaction` qua hàm `ghi()` của `db.py`. Nếu số khách làm `SoChoDaDat` vượt `SoChoToiDa`, MySQL lập tức báo lỗi `3819` và `ROLLBACK` toàn bộ giao dịch, không tạo ra đơn hàng rác.
2. **Các ràng buộc liên quan đến nhiều bảng (như nơi nghỉ phải cùng tỉnh điểm đến của tour) được kiểm tra như thế nào?**
   - *Trả lời:* Trong MySQL, `CHECK` chỉ kiểm tra được các cột trên cùng một dòng của một bảng. Nhóm bảo đảm các ràng buộc liên bảng (`RB22` đến `RB32`) bằng 2 cơ chế: (1) khi nhập liệu, form lọc dữ liệu đầu vào và thực thi trong `Transaction`; (2) đối soát hậu kiểm bằng tệp `4_KiemTra_RangBuoc.sql` sử dụng các câu `SELECT ... UNION ALL` tìm dòng vi phạm — kết quả rỗng chứng minh dữ liệu nhất quán.
3. **Vì sao nhóm không dùng Trigger hay Stored Procedure?**
   - *Trả lời:* Trọng tâm của học phần Cơ sở dữ liệu là thiết kế lược đồ đạt chuẩn 3NF/BCNF, cài đặt các ràng buộc khai báo (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`) và viết câu lệnh truy vấn SQL chuẩn. Việc đưa logic vào câu lệnh SQL có tham số và `Transaction` giúp luồng dữ liệu tường minh, dễ kiểm chứng; Trigger được nhóm đưa vào mục 9.3 (Hướng phát triển).
4. **Làm thế nào chỉ dùng 1 câu lệnh SQL trong màn hình tìm kiếm S1 mà xử lý được 8 bộ lọc tùy chọn?**
   - *Trả lời:* Mỗi điều kiện lọc trong mệnh đề `WHERE` được viết theo mẫu `(@ThamSo IS NULL OR cot = @ThamSo)`. Khi người dùng để trống bộ lọc nào trên giao diện, ứng dụng truyền giá trị `NULL` cho tham số đó; vế `@ThamSo IS NULL` nhận giá trị đúng nên điều kiện lọc đó tự động được bỏ qua.
5. **Ứng dụng chống lỗi bảo mật SQL Injection bằng cách nào?**
   - *Trả lời:* Trong toàn bộ ứng dụng, nhóm tuyệt đối không dùng phép cộng chuỗi hay `f-string` để ghép dữ liệu người dùng nhập vào câu lệnh SQL. Mọi giá trị đều được truyền qua cơ chế Parameterized Query (`%(TenThamSo)s`) của thư viện `mysql-connector-python`.
6. **Dòng `TỔNG CỘNG` ở cuối bảng Báo cáo doanh thu R2 được tính từ đâu?**
   - *Trả lời:* Dòng đó được tính trực tiếp trong MySQL bằng mệnh đề `GROUP BY t.MaTour, t.TenTour WITH ROLLUP` kết hợp với `HAVING GROUPING(t.TenTour) = 0 OR GROUPING(t.MaTour) = 1` để loại bỏ các dòng tổng phụ trung gian và dùng hàm `IF(GROUPING(t.MaTour), 'TỔNG CỘNG', t.MaTour)` để gắn nhãn.
