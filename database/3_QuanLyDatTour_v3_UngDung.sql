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