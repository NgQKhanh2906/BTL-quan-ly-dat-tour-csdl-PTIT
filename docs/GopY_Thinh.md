# GÓP Ý RÀ SOÁT BÁO CÁO - NGUYỄN TIẾN THỊNH (B24DCCN546)

- **Ngày kiểm tra:** 17/11/2026
- **Phạm vi rà soát (Task TH2, TH5, TH7):** Mục 2.1 (Thực thể & thuộc tính), Mục 3.3 (Mô tả 12 bảng), Mục 3.4 (5 nhóm ràng buộc toàn vẹn), Chương 4 (Chuẩn hóa 3NF), Mục 6.4 (Form đánh giá `F3`), và rà soát chéo các tài liệu hướng dẫn trong `docs/`

---

## 1. Rà soát các mục báo cáo phụ trách

| Mục trong báo cáo | Đang ghi | Kết quả kiểm tra | Lý do / Đối chiếu |
| :--- | :--- | :--- | :--- |
| Mục 2.1 (Bảng 6) | 11 thực thể (`ChuyenTrungChuyen` là thực thể yếu, `SDT` đa trị, `DanhGiaTour` / `DanhGiaNhaNghi` phức hợp, 4 thuộc tính dẫn xuất) | Khớp | Đồng nhất hoàn toàn với `database/1_QuanLyDatTour_v3.sql` và `docs/diagrams/ERD.drawio`. |
| Mục 3.3 (Bảng 9 - 20) | Kiểu dữ liệu, `PK`, `FK`, `UQ`, `NULL/NOT NULL` của cả 12 bảng | Khớp | Khớp 100% từng cột và kiểu dữ liệu với tệp SQL số 1 (`DECIMAL(12,0)`, `TINYINT`, `VARCHAR`, `DATETIME`). |
| Mục 3.4 (Bảng 21) | 5 nhóm ràng buộc: miền giá trị, khóa/duy nhất, tham chiếu, `CHECK` nhiều cột trong 1 dòng, liên bảng qua ứng dụng + tệp SQL số 4 | Khớp | Tổng 56 ràng buộc khai báo (`12 PK + 13 FK + 27 CHECK + 4 UNIQUE`) và quy trình kiểm tra 2 lớp khớp với `db.py` + `4_KiemTra_RangBuoc.sql`. |
| Chương 4 (Chuẩn hóa 3NF) | Kiểm tra `1NF -> 2NF -> 3NF` từng bảng và chứng minh tách `TheThanhToan (SoID, LoaiThe)` khỏi `KhachHang` bằng `LEFT JOIN` ra 8 dòng | Khớp | Câu truy vấn ghép trong mục 4.4 chạy đúng và trả về đủ 8 khách hàng mẫu. |
| Mục 6.4 (Form `F3`) | `3_Danh_gia.py`: chọn đơn `HOANTHANH` chưa đánh giá (`NgayDanhGia IS NULL`), bắt buộc có điểm khi nhập nhận xét | Khớp (đã sửa lỗi crash trong code) | Đã khắc phục lỗi gọi sai tham số `ghi(...)` trong `3_Danh_gia.py`, thay định dạng ngày thô sang `dd/mm/yyyy hh:mm`, bổ sung flash message thành công và chụp lại `screenshots/Hinh08_F3_GiaoDien.png`. |

---

## 2. Phát hiện sai lệch trong tài liệu hướng dẫn nội bộ (`docs/Huong_dan_chi_tiet_*.md`)

Khi đối chiếu chéo với schema chuẩn `1_QuanLyDatTour_v3.sql` và code thực tế `tour_app/`, phát hiện một số chỗ viết theo phiên bản cũ trong hai tài liệu hướng dẫn (đã ghi chú đính chính để nhóm không nhầm lẫn khi làm Slide thuyết trình `Slide_Nhom.pptx`):

1. **Tên cột & hàm cũ trong `Huong_dan_chi_tiet_Thinh.md` và `Huong_dan_chi_tiet_Tuan.md`:**
   - Dùng `NgayKhoiHanh`, `PhiPhatHuy`, `SoThuTuChuyen` trong một số đoạn cũ -> schema chuẩn thực tế là `NgayXuatPhat`, `TyLePhat`/`TienPhat` (trong `v_DonHang_ChiTiet`), và `LoaiChuyen` (`'DON_TAI_NHA'` / `'VE_NOI_NGHI'`).
   - Gọi hàm `doc_sql`, `chay_giao_dich`, `lay_hien_tai` -> tên hàm thật trong `tour_app/db.py` là `doc`, `ghi`, `hien_tai`.
   - Ví dụ mã tour `T001` -> dữ liệu mẫu dùng `T01`..`T09`.
2. **Số lượng dữ liệu mẫu và số liệu tổng hợp ở bản cũ:**
   - Một số bảng tóm tắt cũ ghi 13 đơn hàng hoặc phân bổ từng bảng lệch với tổng `104` dòng -> số liệu thật đã kiểm chứng trực tiếp trên MySQL là **104 dòng**: `TinhThanh (15)`, `TheThanhToan (5)`, `KhachHang (8)`, `SDT_KhachHang (10)`, `Tour (9)`, `LichTrinh (12)`, `NhaNghi (9)`, `DonViVanTai (3)`, `Xe (7)`, `TrangThaiDonHang (4)`, `DonHang (14)`, `ChuyenTrungChuyen (8)`.
3. **Số tiêu chí chấm điểm trong Slide 8:**
   - Bản gợi ý trong `Huong_dan_chi_tiet_Thinh.md` ghi `"7/7 tiêu chí"` -> Bảng 1 của báo cáo có **8 tiêu chí** (tổng 10 điểm); khi dựng slide cần sửa thành `"8/8 tiêu chí"`.
