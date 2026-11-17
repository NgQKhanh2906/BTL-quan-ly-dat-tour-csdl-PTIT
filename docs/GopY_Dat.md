# GÓP Ý RÀ SOÁT BÁO CÁO - NGUYỄN TẤT ĐẠT (B24DCCN117)

- **Ngày kiểm tra:** 17/11/2026
- **Phạm vi rà soát (Task D5 & D7):** Mục 2.3 (Sơ đồ ERD và Bảng ký hiệu), Mục 3.1 - 3.2 (Ánh xạ lược đồ quan hệ), Mục 6.2 (Form đặt tour `F1` và SQL) trong `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`, đối chiếu với `docs/diagrams/ERD.drawio` và `tour_app/pages/1_Dat_tour.py`

---

## 1. Đối chiếu tên thực thể, bảng, cột giữa ERD - Báo cáo - SQL - Code (Task D7)

| Vị trí | Đang ghi trước chỉnh sửa | Kết quả rà soát & Sửa chữa | Lý do |
| :--- | :--- | :--- | :--- |
| `docs/diagrams/ERD.drawio` (line 58) | `NoiDen` | Đã sửa thành `DenTai` | Khớp tên mối liên kết `DenTai` trong Mục 2.2 (Bảng 7) và `GopY_Tuan.md`. |
| `docs/diagrams/ERD.drawio` (line 103) | `TênTour` | Đã sửa thành `TenTour` | Đồng nhất chuẩn tên thuộc tính không dấu như `1_QuanLyDatTour_v3.sql` (`Tour.TenTour`) và Bảng 6. |
| `docs/diagrams/ERD.drawio` (line 196) | `LiDoHuy` | Đã sửa thành `LyDoHuy` | Đồng nhất với cột `DonHang.LyDoHuy` trong `1_QuanLyDatTour_v3.sql`, `services.py` và Báo cáo. |
| Báo cáo Mục 2.3 (Bảng 8) | Giải thích đầy đủ thực thể yếu (`ChuyenTrungChuyen`), liên kết xác định (`CoChuyen`), đa trị (`SDT`), dẫn xuất (`SoDem`, `TongTien`, `TienPhat`, `TienHoan`), phức hợp (`DanhGiaTour`, `DanhGiaNhaNghi`) | Khớp | Khớp 100% với file nguồn `docs/diagrams/ERD.drawio` và danh sách trong Chương 2; lưu ý cần mở lại `ERD.drawio` bằng draw.io Desktop để xuất lại ảnh `screenshots/Hinh01_ERD.png` sau 3 chỉnh sửa nhãn XML trên. |
| Báo cáo Mục 3.1 - 3.2 | 12 lược đồ quan hệ, 13 khóa ngoại | Khớp | Khớp từng tên bảng, khóa chính, khóa ngoại với `database/1_QuanLyDatTour_v3.sql`. |

---

## 2. Rà soát Mục 6.2 - Form đặt tour `F1` (Task D5)

| Mục | Đang ghi trong báo cáo | Cập nhật đề xuất / Thực trạng code | Lý do |
| :--- | :--- | :--- | :--- |
| Mục 6.2.1 (Bảng 28, dòng `Khách hàng`) | Chỉ mô tả `"Ô chọn, ví dụ KH001 - Nguyễn Văn An"` | Đã cập nhật Bảng 28: hỗ trợ 2 chế độ `"Khách hàng có sẵn"` (F1.1) và `"Khách hàng mới"` (nhập Họ tên, SĐT, Email, Địa chỉ, tự sinh `MaKH`, chặn trùng Email/SĐT) | Khớp với code thực tế trong `tour_app/pages/1_Dat_tour.py` và `tour_app/services.py` (`luu_dat_tour`) sau khi khắc phục lỗi ghi đè thông tin khách hàng. |
| Mục 6.2.2 (SQL lấy lịch trình) | Liệt kê 7 cột rút gọn (`MaLichTrinh`, `TenTour`, `NgayXuatPhat`, `SoDem`, `GiaCoBan`, `SoChoConLai`, `MaTinhDen`) | Hợp lệ (dạng minh họa cốt lõi); code thật lấy thêm `MaTour`, `NgayKetThuc`, `DiemTapTrung` để tính dự toán và kiểm tra giờ xe về nơi nghỉ | Không sai lệch nghiệp vụ; chỉ cần lưu ý trong giải thích cho người đọc. |
| Mục 6.2.3 (Bảng 29, Ca 1) | `"đón tại nhà 26/11 15:00, về nơi nghỉ 27/11 10:00"` -> tổng tiền `32.020.000 đ` | Đã ghi nhận giao diện `Hinh04_F1_GiaoDien.png` minh họa mặc định `26/11 18:00` (trước khởi hành `20:00`) và `27/11 00:00` vẫn cho tổng tiền `32.020.000 đ` | Tiền xe trung chuyển đã nằm trong giá tour nên tổng tiền khớp đúng `32.020.000 đ`. |
| Kiểm thử chéo `S1` & `R2` (Task D6) | 6 ca của `S1` và kỳ báo cáo `R2` (`01/09 - 31/12/2026` tổng `79.110.000 đ`) | Đạt | Đã xác nhận qua bộ unit/integration test `tour_app/tests/` và kiểm thử trực tiếp trên trình duyệt. |
