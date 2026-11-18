# GÓP Ý RÀ SOÁT BÁO CÁO - BÙI ĐỨC TUÂN (B24DCCN590)

- **Ngày kiểm tra:** 17/11/2026 (cập nhật bổ sung Task TU6, TU7)
- **Phạm vi rà soát:** Chương 1 (Mô tả bài toán), Mục 2.2 (12 mối kết hợp), Mục 6.3 (Form cập nhật trạng thái & hủy đơn `F2`), Mục 8.1 (Phiếu xác nhận đặt tour `R1`), Chương 9 (Kết luận), Trang bìa & Bảng 2 phân công (Task TU7)

---

## 1. Chương 1 – Mô tả bài toán (Trang 5 - 7)

### 1.1. Công thức tính tổng tiền (`TongTien`)

- [x] **Đã khớp:** `TienTour = SoLuongKhach * GiaCoBan`
- [x] **Cần lưu ý tên cột:** Công thức trong ghi chú cũ từng viết `NgayKhoiHanh`, trên SQL và báo cáo chuẩn xác là `SoDem = DATEDIFF(NgayKetThuc, NgayXuatPhat)`
- [x] **Đã khớp:** `TienPhong = SoPhong * GiaPhongMoiDem * SoDem` (nếu `MaNhaNghi IS NULL` và `SoPhong = 0` thì `TienPhong = 0`)
- [x] **Đã khớp:** `TongTien = TienTour + TienPhong` — thuộc tính dẫn xuất, tính qua View `v_DonHang_ChiTiet`

### 1.2. Quy tắc chuyển trạng thái đơn hàng (4 trạng thái)

- [x] **Đã khớp:** Luồng đi xuôi: `DAT -> THANHTOAN -> HOANTHANH`
- [x] **Đã khớp:** Luồng hủy: `DAT -> HUY` và `THANHTOAN -> HUY`
- [x] **Đã khớp:** Trạng thái kết thúc: `HOANTHANH` và `HUY` không chuyển sang bất kỳ trạng thái nào khác

### 1.3. Bảng 5 mức phạt hủy tour

| Thứ tự | Điều kiện | Mức phạt | Kết quả kiểm tra |
| :---: | :--- | :---: | :--- |
| 1 | Hủy < 24h kể từ lúc đặt **VÀ** còn >= 7 ngày trước khởi hành | 0% | Khớp |
| 2 | Còn >= 15 ngày trước khởi hành | 10% | Khớp |
| 3 | Còn 7 - 14 ngày trước khởi hành | 30% | Khớp |
| 4 | Còn 3 - 6 ngày trước khởi hành | 50% | Khớp |
| 5 | Còn < 3 ngày trước khởi hành | 100% | Khớp |

- [x] **Đã khớp:** Thứ tự ưu tiên xét `< 24h` trước rồi mới xét số ngày
- [x] **Đã khớp:** Đơn hàng mẫu kiểm chứng: `DH011` (0%), `DH009` (10%), `DH008` (30%), `DH006` (100%)

---

## 2. Mục 2.2 – 12 mối kết hợp trên sơ đồ ERD

| STT | Tên mối kết hợp | Thực thể tham gia | Bản số | Kết quả |
| :---: | :--- | :--- | :---: | :--- |
| 1 | `XuatPhatTu` | `Tour` — `TinhThanh` | N:1 | Đạt |
| 2 | `DenTai` | `Tour` — `TinhThanh` | N:1 | Đạt |
| 3 | `NamTai` | `NhaNghi` — `TinhThanh` | N:1 | Đạt |
| 4 | `CoLichTrinh` | `Tour` — `LichTrinh` | 1:N | Đạt |
| 5 | `ThanhToanBang` | `KhachHang` — `TheThanhToan` | N:1 | Đạt |
| 6 | `Dat` | `KhachHang` — `DonHang` | 1:N | Đạt |
| 7 | `ThuocLichTrinh` | `LichTrinh` — `DonHang` | 1:N | Đạt |
| 8 | `LuuTru` | `NhaNghi` — `DonHang` | 1:N | Đạt |
| 9 | `CoTrangThai` | `TrangThaiDonHang` — `DonHang` | 1:N | Đạt |
| 10 | `SoHuu` | `DonViVanTai` — `Xe` | 1:N | Đạt |
| 11 | `CoChuyen` | `DonHang` — `ChuyenTrungChuyen` | 1:N | Đạt |
| 12 | `PhucVu` | `Xe` — `ChuyenTrungChuyen` | 1:N | Đạt |

- [x] **Đã đủ 12/12 mối kết hợp** (bao gồm `ThanhToanBang`).

---

## 3. Bổ sung rà soát Mục 6.3 (`F2`), Mục 8.1 (`R1`) và Thông tin thành viên (Task TU6, TU7)

| Mục trong báo cáo | Đang ghi | Kết quả rà soát & Cập nhật | Lý do / Đối chiếu nguồn thật |
| :--- | :--- | :--- | :--- |
| Trang bìa & Bảng 2 (Task TU7) | Danh sách 4 thành viên (`B24DCCN117`, `B24DCCN546`, `B24DCCN590`, `B24DCCN311`), mỗi người `25%` (`100%`) | Khớp | Khớp với bảng MSSV chính thức của Nhóm 14 (học phần `INT1313`). |
| Mục 6.3 (Bảng 30 - 31) | Form hủy đơn `F2` có xem trước tiền phạt, ô tích đồng ý mức phạt, kiểm tra ngày hủy >= ngày đặt; Bảng 31 Ca 5 minh họa `DH010` hủy ngày `10/10` | Cập nhật mô tả Ca 5 khớp với `Hinh07_F2_Loi.png` | `Hinh07_F2_Loi.png` minh họa trực quan lỗi gộp trên `DH007` (trống lý do, ngày `02/10/2026 < NgayDat 05/10/2026`, chưa tích đồng ý mức phạt); `2_Quan_ly_don.py` đã bổ sung đầy đủ kiểm tra `RB23` (`NgayHuy < NgayXuatPhat`) và try/except. |
| Mục 8.1 (Phiếu xác nhận `R1`) | Mô tả luồng người lập -> khách hàng, A4 dọc 1 trang; khối SQL 8.1.3 rút gọn | Đã nâng cấp `5_Phieu_xac_nhan.py` & template A4 khớp 100% | Đã sửa bug kiểm tra `MaTrangThai == 'HUY'`, `LyDoHuy IS NULL` -> `"Không ghi nhận"`, sửa nhãn tiền mặt/chuyển khoản khi `SoID IS NULL`, bổ sung `DiemTapTrung`, cột `ThoiGianDon` từ `v_LichTrungChuyen`, escape HTML và xuất vừa 1 trang A4 (`DH007`, `DH008`). |
| Chương 9 (Kết luận) | 11 thực thể, 12 mối liên kết, 12 bảng 3NF, 13 khóa ngoại, 56 ràng buộc, 2 view, 104 dòng mẫu | Khớp | Khớp chính xác với kết quả kiểm tra thực tế trên MySQL 8.0. |
