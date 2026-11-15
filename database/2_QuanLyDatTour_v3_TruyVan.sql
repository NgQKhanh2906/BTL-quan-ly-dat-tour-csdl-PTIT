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