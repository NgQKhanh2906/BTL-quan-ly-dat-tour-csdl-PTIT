# GÓP Ý RÀ SOÁT BÁO CÁO - NGUYỄN QUỐC KHÁNH (B24DCCN311)

- **Ngày kiểm tra:** 17/11/2026
- **Phạm vi rà soát (Task K8):** Mục 3.5 (Data Diagram), Chương 5 (Cài đặt CSDL), Chương 7 (Màn hình tìm kiếm S1), Mục 8.2 (Báo cáo doanh thu R2), Phụ lục cài đặt trong `docs/report/Bao_cao_BTL_CSDL_QuanLyDatTour.docx`

---

## 1. Bảng đối chiếu chi tiết theo mục phụ trách

| Mục trong báo cáo | Nội dung đang ghi | Kết quả kiểm tra / Chỉnh sửa | Lý do / Đối chiếu nguồn thật |
| :--- | :--- | :--- | :--- |
| Mục 3.5 (Bảng 22) | 12 bảng, 13 đường nối khóa ngoại; `ChuyenTrungChuyen` là thực thể yếu; `SDT_KhachHang` từ thuộc tính đa trị | Khớp | Khớp hoàn toàn với `database/1_QuanLyDatTour_v3.sql` (12 base tables, 13 `FOREIGN KEY`). |
| Chương 5 (Bảng 25 - 27) | 4 tệp SQL, 56 ràng buộc (`12 PK + 13 FK + 4 UNIQUE + 27 CHECK`), 2 view, 104 dòng mẫu, 32 câu test dữ liệu sai | Khớp | Khớp với kết quả thực thi trực tiếp trên MySQL 8.0 (`QuanLyDatTour`: 104 dòng trên 12 bảng, `4_KiemTra_RangBuoc.sql` trả về rỗng `[]`). |
| Chương 7 (Bảng 33 - 34) | 8 bộ lọc tìm kiếm (`S1`), nút "Tour cao cấp (từ 10 triệu)" ra `LT08, LT09, LT12`; lọc Lào Cai `LT05` điểm `5,0`; báo lỗi khi `GiaDen < GiaTu` | Khớp (đã đồng bộ nút preset trong code) | Sau khi sửa `4_Tim_kiem.py` bind key `st.session_state` và callback `on_click`, bấm "Tour cao cấp" tự reset `gia_den` xung đột và "Đặt lại bộ lọc" reset sạch 8 tiêu chí. |
| Mục 8.2 (Bảng 36 - 37) | R2 kỳ `01/09/2026 - 31/12/2026`: Tổng `79.110.000 đ`, `10` đơn, `26` khách, `4` đơn hủy (`72.120.000 đ` dịch vụ + `6.990.000 đ` phạt); khổ in A4 ngang 1 trang | Khớp | Khớp 100% với `6_Bao_cao_doanh_thu.py`, `services.py` (`GROUP BY ... WITH ROLLUP`) và bản PDF A4 ngang 1 trang. |
| Phụ lục (cuối báo cáo) | Yêu cầu `python -m venv .venv`, `pip install -r tour_app\requirements.txt`, biến môi trường `MYSQL_PASSWORD`, chèn đường dẫn repo | Cần điền chỗ `[đường dẫn...]` và giữ tên thư mục chạy đúng `tour_app` | Đã điền link repository GitHub và mã học phần `INT1313` / Nhóm `14` vào báo cáo Word; lưu ý nếu thư mục chạy là `tour_app` cần cấu hình `MYSQL_PASSWORD` hoặc biến `DB_*` tương ứng trong `tour_app/db.py`. |

---

## 2. Kết luận rà soát (Task K8 & K9)

- **Kiểm tra chéo `F2` (`2_Quan_ly_don.py`) và `R1` (`5_Phieu_xac_nhan.py`) (Task K9):**
  - Đã kiểm thử lại `F2`: bổ sung checkbox `"Khách đã đồng ý mức phạt"`, kiểm tra `NgayHuy >= NgayDat` ở cả Python và SQL, transaction 3 bước nguyên tử hoàn trả chỗ và xóa `ChuyenTrungChuyen` hoạt động đúng.
  - Đã kiểm thử lại `R1`: sửa điều kiện `MaTrangThai == 'HUY'`, xử lý `LyDoHuy IS NULL` thành `"Không ghi nhận"`, sửa nhãn tiền mặt/chuyển khoản khi khách chưa có thẻ (`SoID IS NULL`), bổ sung `DiemTapTrung`, cột `ThoiGianDon`, escape HTML và xuất file HTML tải về in PDF A4 dọc đúng 1 trang (`DH007`, `DH008`).
- **Tồn đọng ngoài mã nguồn:** Cần người phụ trách điền nốt `[Họ tên giảng viên]` ở trang bìa và `[Tên giáo trình hoặc bài giảng...]` ở mục Tài liệu tham khảo trước khi cập nhật Mục lục và xuất PDF nộp bài.
