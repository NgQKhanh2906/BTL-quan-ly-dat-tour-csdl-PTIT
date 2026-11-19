# Quy Tắc Design System (Design System Rules)

Tài liệu này phân tích hiện trạng giao diện trong mã nguồn hiện tại (`tour_app/`) và thiết lập bộ quy tắc Design System thống nhất cho ứng dụng Web mới (`web_app/`), phục vụ triển khai đồng bộ theo chủ đề thị giác đã phê duyệt và sẵn sàng tích hợp Figma MCP trong tương lai.

---

## 1. Hiện trạng Codebase (`tour_app/` — Trước khi nâng cấp)

- **UI Framework:** `Streamlit 1.66.0` (đa trang qua thư mục `tour_app/pages/*.py`).
- **Design Tokens:** Không tồn tại file token tập trung. Màu sắc và kiểu chữ dùng hoàn toàn mặc định của Streamlit, ngoại trừ CSS cục bộ nằm rời rạc bên trong 2 biểu mẫu in HTML (`tour_app/templates/phieu_xac_nhan.html` và `tour_app/templates/bao_cao_doanh_thu.html` dùng màu `#0b5ed7`, `#f0f4f8`, `#111`).
- **Component Library:** Không có thư viện component tái sử dụng; mỗi trang gọi trực tiếp widget Streamlit (`st.selectbox`, `st.number_input`, `st.metric`, `st.dataframe`, `st.caption`).
- **Asset & Icon System:** Chưa có thư mục ảnh ứng dụng hoặc bộ icon nhất quán.

---

## 2. Cấu trúc Design System cho Web App mới (`web_app/frontend/`)

### 2.1. Định nghĩa Token (Token Definitions)
Toàn bộ token thị giác được định nghĩa tập trung bằng CSS Custom Properties tại `web_app/frontend/src/styles/tokens.css` và ánh xạ vào cấu hình Tailwind CSS để dùng nhất quán across mọi component.

```css
/* web_app/frontend/src/styles/tokens.css */
:root {
  /* --- Color Palette: User Portal (Airy Cobalt Travel Theme) --- */
  --color-bg-canvas: #F7FAFF;
  --color-bg-surface: #FFFFFF;
  --color-bg-subtle: #EFF5FF;

  --color-brand-primary: #1D63ED;
  --color-brand-hover: #154EC2;
  --color-brand-soft: #DBEAFE;
  --color-brand-gradient-start: #1E5CE6;
  --color-brand-gradient-end: #0B3A99;

  --color-ink-primary: #0F172A;
  --color-ink-secondary: #475569;
  --color-ink-muted: #64748B;
  --color-border-subtle: #E2E8F0;
  --color-border-strong: #CBD5E1;

  /* --- Color Palette: Admin Portal (Slate Operations Theme) --- */
  --color-admin-sidebar: #0F172A;
  --color-admin-sidebar-hover: #1E293B;
  --color-admin-canvas: #F8FAFC;

  /* --- Semantic Status Colors --- */
  --color-status-booked-bg: #EFF6FF;
  --color-status-booked-fg: #1D4ED8;
  --color-status-paid-bg: #ECFDF5;
  --color-status-paid-fg: #047857;
  --color-status-done-bg: #F0FDF4;
  --color-status-done-fg: #15803D;
  --color-status-cancelled-bg: #FEF2F2;
  --color-status-cancelled-fg: #B91C1C;
  --color-rating-star: #F59E0B;

  /* --- Typography --- */
  --font-display: 'Spectral', Georgia, serif;
  --font-sans: 'Be Vietnam Pro', system-ui, -apple-system, sans-serif;

  /* --- Radius Scale --- */
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-xl: 28px;
  --radius-pill: 9999px;

  /* --- Elevation --- */
  --shadow-card: 0 4px 20px rgba(15, 23, 42, 0.05);
  --shadow-floating: 0 20px 50px rgba(15, 23, 42, 0.10);
  --shadow-glass: 0 12px 32px rgba(15, 23, 42, 0.14);

  /* --- Motion --- */
  --ease-out-expo: cubic-bezier(0.22, 1, 0.36, 1);
  --duration-fast: 150ms;
  --duration-base: 220ms;
  --duration-slow: 420ms;
}
```

### 2.2. Thư viện Component (Component Library)
Các component tái sử dụng nằm tại `web_app/frontend/src/components/`, phân theo 4 nhóm:
- `layout/`:
  - `UserLayout.tsx` (TopNavbar + Animated Page Container + Footer).
  - `AdminLayout.tsx` (Fixed Slate Sidebar + Workspace Header + Main Outlet).
- `common/`:
  - `Button.tsx` (Biến thể duy nhất: `primary`, `secondary`, `ghost`, `danger`; dạng pill cho CTA User Portal và bo `10px` cho Admin Operate controls).
  - `StatusBadge.tsx` (Ánh xạ đúng 4 trạng thái `DAT`, `THANHTOAN`, `HOANTHANH`, `HUY` sang token màu ngữ nghĩa).
  - `StarRating.tsx` (Chế độ hiển thị và chế độ tương tác chọn 1–5 sao).
  - `Modal.tsx` & `SlideOverDrawer.tsx` (Hỗ trợ Escape đóng, khóa cuộn nền, vùng focus rõ ràng).
  - `EmptyState.tsx` & `LoadingSkeleton.tsx` (Dùng skeleton thay cho spinner treo giữa trang).
- `user/`:
  - `HeroOrganicFrame.tsx` (Khung cắt ảnh SVG clip-path bo cong + thẻ nổi Glassmorphism).
  - `FloatingSearchBar.tsx` (Thanh tìm kiếm dạng pill 4 trường + nút kính lúp tròn).
  - `TourCard.tsx` (Thẻ full-bleed bo `20px`, hiệu ứng zoom ảnh `1.04` khi hover, badge rating trắng, giá và nút hành động).
  - `BookingSummaryCard.tsx` (Thẻ dự toán chi phí dính `sticky` trên trang Đặt tour).
- `admin/`:
  - `KpiMetricCard.tsx` (Thẻ số liệu `tabular-nums` trên Dashboard).
  - `RevenueChart.tsx` (Biểu đồ cột ngang Recharts so sánh doanh thu dịch vụ và tiền phạt hủy).
  - `OrderActionDrawer.tsx` (Ngăn xem chi tiết, chuyển trạng thái và hủy đơn kèm bảng xem trước phạt).
  - `DocumentPreviewFrame.tsx` (Khung xem trước A4 dọc/ngang + nút tải PDF).

### 2.3. Frameworks & Libraries
- **Frontend Framework:** React 19 + TypeScript + Vite.
- **Routing:** `react-router-dom` v7.
- **Styling:** Tailwind CSS kết hợp biến CSS trong `tokens.css`.
- **Animation:** `framer-motion` (chỉ dùng cho chuyển cảnh route, hero entrance một lần khi tải trang và phản hồi tương tác có mục đích; tuân thủ `prefers-reduced-motion`).
- **Charts:** `recharts` (chỉ dùng trên màn hình Báo cáo doanh thu Admin).
- **Backend API:** FastAPI + Uvicorn (Python 3.11) kết nối trực tiếp MySQL qua `tour_app/db.py` và `tour_app/services.py`.

### 2.4. Quản lý Tài nguyên (Asset Management)
- Toàn bộ ảnh phong cảnh miền Bắc lưu cục bộ tại `web_app/frontend/public/images/` (định dạng `.png` / `.webp` tối ưu dung lượng, không dùng URL bên thứ ba dễ hỏng).
- Ánh xạ tập trung tại `web_app/frontend/src/constants/tourImages.ts` theo `MaTour` (`T01`..`T09`) kèm ảnh dự phòng mặc định.
- Mọi thẻ `<img>` đều dùng `object-cover`, có `alt` mô tả tiếng Việt rõ ràng và khai báo `loading="lazy"` cho các ảnh dưới đường gấp màn hình (trừ ảnh Hero dùng `loading="eager"`).

### 2.5. Hệ thống Icon (Icon System)
- Sử dụng duy nhất thư viện **`lucide-react`** (độ dày nét thống nhất `strokeWidth={1.75}` cho kích thước `16px`–`20px`).
- **Quy tắc cấm tuyệt đối:** Không sử dụng Unicode emoji làm icon ở bất kỳ vị trí nào (nút bấm, tiêu đề, badge, bảng dữ liệu hay thông báo).
- Logo thương hiệu (`Bắc Việt Travel`) và đường nét đứt trang trí ở Hero là inline SVG tối giản đặt trong `src/components/common/BrandLogo.tsx`.

### 2.6. Phương pháp Styling & Responsive
- **User Portal (Persuade & Discovery):** Container tối đa `1280px` (`max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`), hai mép nội dung trái–phải thẳng hàng. Hero full-width trên desktop `1440px`, tự chuyển sang bố cục xếp dọc (chữ trước, ảnh sau) ở `<= 1024px` và `390px`.
- **Admin Portal (Operate):** Sidebar cố định rộng `260px` trên desktop, tự gập thành drawer kéo trượt trên tablet/mobile (`< 1024px`). Bảng dữ liệu bọc trong container cuộn ngang mượt (`overflow-x-auto`) và căn phải toàn bộ cột tiền tệ với `font-variant-numeric: tabular-nums`.
- **Ngôn ngữ hiển thị (UX Copy):**
  - Tiếng Việt tự nhiên như một nền tảng đặt tour thương mại thực thụ.
  - Không có mã chức năng (`F1`, `F2`, `F3`, `S1`, `R1`, `R2`).
  - Không có các dòng ghi chú kỹ thuật giải thích ràng buộc CSDL hay trạng thái kết nối database trên giao diện.

### 2.7. Tổ chức Dự án (Project Structure)
- Phân tầng theo vai trò và miền nghiệp vụ:
  - `pages/user/*` chỉ chứa các màn hình cổng Khách hàng.
  - `pages/admin/*` chỉ chứa các màn hình cổng Quản trị.
  - `api/client.ts` tập trung toàn bộ HTTP fetch, đính kèm token phiên và chuẩn hóa thông báo lỗi tiếng Việt trả về từ Backend.
  - `utils/format.ts` tập trung định dạng tiền tệ (`32.020.000 đ`) và ngày giờ (`dd/MM/yyyy HH:mm`) khớp chuẩn với `tour_app/db.py`.
