# GÓP Ý RÀ SOÁT BÁO CÁO - BÙI ĐỨC TUÂN (B24DCCN590)

- **Ngày kiểm tra:** 16/11/2026
- **Phạm vi rà soát:** Chương 1 (Mô tả bài toán), Mục 2.2 (12 mối kết hợp), Chương 9 (Kết luận)

---

## 1. Chương 1 – Mô tả bài toán (Trang 5 - 7)

### 1.1. Công thức tính tổng tiền (`TongTien`)

- [x] **Đã khớp:** `TienTour = SoLuongKhach * GiaCoBan` ✔
- [x] **Đã khớp:** `SoDem = DATEDIFF(NgayKetThuc, NgayKhoiHanh)` ✔
- [x] **Đã khớp:** `TienPhong = SoPhong * GiaPhongMoiDem * SoDem` (nếu `MaNhaNghi IS NULL` và `SoPhong = 0` thì `TienPhong = 0`) ✔
- [x] **Đã khớp:** `TongTien = TienTour + TienPhong` — thuộc tính dẫn xuất, tính qua View `v_DonHang_ChiTiet` ✔

### 1.2. Quy tắc chuyển trạng thái đơn hàng (4 trạng thái)

- [x] **Đã khớp:** Luồng đi xuôi: `DAT -> THANHTOAN -> HOANTHANH` ✔
- [x] **Đã khớp:** Luồng hủy: `DAT -> HUY` và `THANHTOAN -> HUY` ✔
- [x] **Đã khớp:** Trạng thái kết thúc: `HOANTHANH` và `HUY` không chuyển sang bất kỳ trạng thái nào khác ✔

### 1.3. Bảng 5 mức phạt hủy tour

| Thứ tự | Điều kiện | Mức phạt | Kết quả kiểm tra |
| :---: | :--- | :---: | :---: |
| 1 | Hủy < 24h kể từ lúc đặt **VÀ** còn ≥ 7 ngày trước khởi hành | 0% | ✔ Khớp |
| 2 | Còn ≥ 15 ngày trước khởi hành | 10% | ✔ Khớp |
| 3 | Còn 7 - 14 ngày trước khởi hành | 30% | ✔ Khớp |
| 4 | Còn 3 - 6 ngày trước khởi hành | 50% | ✔ Khớp |
| 5 | Còn < 3 ngày trước khởi hành | 100% | ✔ Khớp |

- [x] **Đã khớp:** Thứ tự ưu tiên xét `< 24h` trước rồi mới xét số ngày ✔
- [x] **Đã khớp:** Đơn hàng mẫu kiểm chứng: `DH011` (0%), `DH009` (10%), `DH008` (30%), `DH006` (100%) ✔

---

## 2. Mục 2.2 – 12 mối kết hợp trên sơ đồ ERD

| STT | Tên mối kết hợp | Thực thể tham gia | Bản số | Kết quả |
| :---: | :--- | :--- | :---: | :---: |
| 1 | `XuatPhatTu` | Tour — TinhThanh | N:1 | ✔ |
| 2 | `DenTai` | Tour — TinhThanh | N:1 | ✔ |
| 3 | `NamTai` | NhaNghi — TinhThanh | N:1 | ✔ |
| 4 | `CoLichTrinh` | Tour — LichTrinh | 1:N | ✔ |
| 5 | `ThanhToanBang` | KhachHang — TheThanhToan | N:1 | ✔ |
| 6 | `Dat` | KhachHang — DonHang | 1:N | ✔ |
| 7 | `ThuocLichTrinh` | LichTrinh — DonHang | 1:N | ✔ |
| 8 | `LuuTru` | NhaNghi — DonHang | 1:N | ✔ |
| 9 | `CoTrangThai` | TrangThaiDonHang — DonHang | 1:N | ✔ |
| 10 | `SoHuu` | DonViVanTai — Xe | 1:N | ✔ |
| 11 | `CoChuyen` | DonHang — ChuyenTrungChuyen | 1:N | ✔ |
| 12 | `PhucVu` | Xe — ChuyenTrungChuyen | 1:N | ✔ |

- [x] **Đã đủ 12/12 mối kết hợp** ✔
- [x] **Mối kết hợp số 12 `ThanhToanBang`** (giữa `KhachHang` và `TheThanhToan`) đã được mô tả ✔

---

## 3. Chương 9 – Kết luận

- [x] **Đã khớp:** 11 thực thể trên ERD (10 thực thể mạnh + 1 thực thể yếu `ChuyenTrungChuyen`) và 12 mối kết hợp ✔
- [x] **Đã khớp:** 12 bảng quan hệ trong MySQL, tất cả đạt chuẩn 3NF ✔
- [x] **Đã khớp:** 13 khóa ngoại (`FOREIGN KEY`) ✔
- [x] **Đã khớp:** 56 ràng buộc toàn vẹn khai báo (`12 PK + 13 FK + 27 CHECK + 4 UNIQUE`) ✔
- [x] **Đã khớp:** 2 khung nhìn (`VIEW`) ✔
- [x] **Đã khớp:** 104 dòng dữ liệu mẫu ✔

---

## 4. Kết luận rà soát

> **Không phát hiện sai sót nào** trong Chương 1, Mục 2.2 và Chương 9. Tất cả các công thức nghiệp vụ, mối kết hợp và con số tổng kết đều khớp chính xác với thiết kế CSDL đã chuẩn hóa 3NF và mã nguồn ứng dụng. Báo cáo đạt yêu cầu, không cần chỉnh sửa thêm.
