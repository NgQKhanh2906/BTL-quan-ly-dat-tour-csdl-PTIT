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

-- 2. Bang TheThanhToan (Tach tu KhachHang de dat 3NF)
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