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