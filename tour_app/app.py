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