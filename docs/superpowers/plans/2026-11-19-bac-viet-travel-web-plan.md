# Bắc Việt Travel Web Redesign Implementation Plan

> **For agentic workers:** Implement tasks cleanly according to assigned file ownership. Every worker must read the Spec (`docs/superpowers/specs/2026-11-19-bac-viet-travel-web-design.md`) and Design System Rules (`docs/superpowers/specs/2026-11-19-design-system-rules.md`). Do NOT run `git commit` or `git push`.

**Goal:** Build the full-stack `Bắc Việt Travel` web application (React + TypeScript + Vite + FastAPI) with distinct User and Admin portals, real local Northern Vietnam photography, smooth page transitions, and real A4 PDF export for both Revenue Report and Booking Confirmation, reusing 100% of `tour_app/db.py` and `tour_app/services.py` while leaving `database/` and `tour_app/` completely untouched.

**Architecture:** FastAPI backend (`web_app/backend/`) imports `tour_app/db.py` and `tour_app/services.py` directly, adds thin read-only query helpers (`queries.py`), stateless HMAC-SHA256 role tokens (`dependencies.py`), and headless Chrome/Edge A4 PDF rendering (`pdf_service.py`). React 19 + TypeScript + Vite + Tailwind frontend (`web_app/frontend/`) implements the airy cobalt travel User Portal (`/`, `/explore`, `/book`, `/my-bookings`) and dark-slate Admin Operations Dashboard (`/admin/login`, `/admin/dashboard`, `/admin/orders`, `/admin/confirmations`).

**Tech Stack:** Python 3.11 (`.venv`), FastAPI, Pydantic v2, Uvicorn, HTTPX, MySQL 8 (`QuanLyDatTour`), Node 25, React 19, TypeScript, Vite, Tailwind CSS v4, React Router v7, Framer Motion, Lucide React, Recharts, Chrome/Edge Headless PDF.

**Spec:** `docs/superpowers/specs/2026-11-19-bac-viet-travel-web-design.md` and `docs/superpowers/specs/2026-11-19-design-system-rules.md`.

## Global Constraints

1. **Zero modifications to `database/` or `tour_app/`:** All 12 MySQL tables, views, sample data, `tour_app/db.py`, `tour_app/services.py`, `tour_app/templates/*.html`, `tour_app/pages/*.py`, and `tour_app/tests/*` stay untouched.
2. **Zero function codes in UI:** Never display `F1.`, `F2.`, `F3.`, `S1.`, `R1.`, `R2.` anywhere in visible labels, titles, nav items, or tables.
3. **Zero AI-like technical captions:** Never show DB constraint explanations (`HOANTHANH`, `MaNhaNghi IS NULL`, `chk_DonHang_DanhGiaNhaNghi`, `RB22`, `RB23`), PTIT course labels, `"12 bảng"`, or raw system-clock banners on User screens.
4. **Zero emojis anywhere:** Use `lucide-react` icons exclusively (`strokeWidth={1.75}`); zero Unicode emoji in UI, docs, or comments.
5. **No invented statistics:** All numbers on Landing Page, Explore, and Admin Dashboard come live from MySQL `QuanLyDatTour`.
6. **PDF A4 exact 1-page output:** Revenue report exports `.pdf` A4 landscape (1 page); Confirmation voucher exports `.pdf` A4 portrait (1 page) with `BẮC VIỆT TRAVEL` branding applied at `web_app/backend/pdf_service.py`.
7. **Git safety:** Do not run `git commit` or `git push`.

## Review Focus

1. **Decimal / Datetime JSON serialization:** MySQL returns `decimal.Decimal` and `datetime.datetime`; every API response must convert VND/counts to `int`, ratings to `float | null`, and datetimes to ISO-8601 strings (`YYYY-MM-DDTHH:MM:SS`) so frontend formatting never hits `NaN` or type mismatches. (Pinned in Task 1 `test_api.py`.)
2. **Ownership & Auth boundary:** A customer token for `KH001` must receive `403` when requesting `KH004`'s orders, submitting a review for `DH004` (owned by `KH004`), or downloading PDF for `DH008` (owned by `KH007`), and unauthenticated requests to `/api/admin/*` must receive `401`. (Pinned in Task 1 `test_api.py`.)
3. **Guest booking auto-session & atomic rollback:** Creating a booking as a guest returns `customer_token` + `customer` so immediate PDF download succeeds with `200 application/pdf`; invalid bookings (duplicate email/phone, `SoPhong > SoLuongKhach`, missing pickup address) return `400` with Vietnamese messages and leave DB row counts unchanged. (Pinned in Task 1 `test_api.py`.)
4. **Day tour (`SoDem == 0`, e.g., `LT06`) & no-accommodation review edge cases:** Booking `LT06` hides accommodation & shuttle-to-accommodation controls and submits `ma_nha_nghi=null, so_phong=0`; reviewing an order without `MaNhaNghi` hides accommodation review inputs without printing DB constraint jargon. (Pinned in Task 1 & Task 3.)
5. **Real PDF binary integrity & XSS safety:** `POST /api/admin/reports/revenue/pdf` and `GET /api/orders/{ma_don}/confirmation/pdf` return `Content-Type: application/pdf`, start with `b"%PDF-"`, render exactly 1 A4 page, and escape HTML/script payloads in `nguoi_lap`. (Pinned in Task 1 `test_api.py`.)

---

## Shared Contracts & File Ownership Map

- **Subagent `image-generator` (Orchestrator-managed):** Produces 11 local PNG assets copied to `web_app/frontend/public/images/`:
  `hero-northern-vietnam.png`, `promo-cruise.png`, `tour-T01.png` .. `tour-T09.png`.
- **Worker `backend`:** Exclusively owns `web_app/backend/**`.
- **Worker `frontend-user`:** Exclusively owns `web_app/frontend/` root configs (`package.json`, `vite.config.ts`, `tsconfig*.json`, `index.html`), `src/main.tsx`, `src/App.tsx`, `src/styles/**`, `src/api/**`, `src/context/**`, `src/utils/**`, `src/constants/**`, `src/components/layout/**`, `src/components/common/**`, `src/components/user/**`, `src/pages/user/**`.
- **Worker `frontend-admin`:** Exclusively owns `web_app/frontend/src/components/admin/**` and `web_app/frontend/src/pages/admin/**`.
- **Worker `verifier`:** Read-only verification across backend tests, original `tour_app/tests`, `npm run build`, and live UI checks.

---

### Task 1: FastAPI Backend, Auth Tokens, Read Helpers, and PDF Service (`backend`)

**Files:**
- Create: `web_app/backend/requirements.txt` (`fastapi`, `pydantic`, `httpx`)
- Create: `web_app/backend/dependencies.py`
- Create: `web_app/backend/schemas.py`
- Create: `web_app/backend/queries.py`
- Create: `web_app/backend/pdf_service.py`
- Create: `web_app/backend/routers/__init__.py`
- Create: `web_app/backend/routers/public.py`
- Create: `web_app/backend/routers/auth.py`
- Create: `web_app/backend/routers/bookings.py`
- Create: `web_app/backend/routers/admin.py`
- Create: `web_app/backend/main.py`
- Test: `web_app/backend/tests/__init__.py`, `web_app/backend/tests/test_api.py`

**Interfaces (Produces — Exact REST JSON Contracts):**
- `GET /api/meta` -> `{ current_datetime: string, current_date: string, brand_name: "Bắc Việt Travel" }`
- `GET /api/landing` -> `{ stats: { total_provinces: number, total_tours: number, open_schedules: number, total_travelers_served: number, avg_rating: number | null, total_reviews: number }, featured_schedules: ScheduleSearchItem[] }`
- `GET /api/provinces` -> `ProvinceItem[]` (`{ ma_tinh: string, ten_tinh: string }`)
- `GET /api/schedules/search` (query: `tu_khoa`, `ma_tinh_den`, `gia_tu`, `gia_den`, `tu_ngay`, `den_ngay`, `so_khach`, `diem_toi_thieu`) -> `ScheduleSearchItem[]`:
  `{ ma_lich_trinh, ma_tour, ten_tour, mo_ta, noi_di, noi_den, ngay_xuat_phat, so_ngay, gia_co_ban, so_cho_con_lai, diem_tb, so_luot_danh_gia }`
- `GET /api/schedules/open` -> `OpenScheduleItem[]`:
  `{ ma_lich_trinh, ma_tour, ten_tour, mo_ta, noi_di, ma_tinh_den, ten_tinh_den, diem_tap_trung, ngay_xuat_phat, ngay_ket_thuc, so_dem, gia_co_ban, so_cho_con_lai }`
- `GET /api/accommodations?ma_tinh_den=QN` -> `AccommodationItem[]`:
  `{ ma_nha_nghi, ten_nha_nghi, loai_hinh, dia_chi, gia_phong_moi_dem }`
- `GET /api/customers` -> `CustomerItem[]`:
  `{ ma_kh, ho_ten, email, dia_chi, so_dien_thoai }`
- `POST /api/customers/check-duplicate` body `{ email, so_dien_thoai }` -> `{ duplicate: boolean, customer: CustomerItem | null }`
- `POST /api/auth/customer-login` body `{ identifier: string }` -> `{ token: string, customer: CustomerItem }` (404 if not found)
- `POST /api/auth/admin-login` body `{ username: string, password: string, staff_name?: string }` -> `{ token: string, username: string, staff_name: string }` (401 if invalid; default `admin` / `admin123`, default staff_name `"Nguyễn Quốc Khánh"`)
- `POST /api/bookings/estimate` body `{ so_khach, gia_co_ban, so_phong, gia_phong_moi_dem, so_dem, co_nha_nghi }` -> `{ tien_tour, tien_phong, tong_tien }`
- `POST /api/bookings` body `{ la_khach_moi, ma_kh?, ho_ten?, so_dien_thoai?, email?, dia_chi?, ma_lich_trinh, so_khach, ma_nha_nghi?, so_phong, co_xe_don, dia_chi_don?, gio_don?, co_xe_ve, gio_ve_noi_nghi? }` -> `{ ma_don_hang, ma_kh, tong_tien, customer: CustomerItem, customer_token: string }` (400 with `{ detail: string, errors?: string[] }` on validation/duplicate failure)
- `GET /api/customers/{ma_kh}/orders` (Header `X-Customer-Token` or `X-Admin-Token`) -> `CustomerOrderItem[]`:
  `{ ma_don_hang, ma_tour, ten_tour, tinh_den, ma_lich_trinh, ngay_dat, ngay_xuat_phat, ngay_ket_thuc, so_luong_khach, ma_nha_nghi, ten_nha_nghi, so_phong, tien_tour, tien_phong, tong_tien, ma_trang_thai, ten_trang_thai, ngay_huy, ly_do_huy, ty_le_phat, tien_phat, tien_hoan, diem_tour, nhan_xet_tour, diem_nha_nghi, nhan_xet_nha_nghi, ngay_danh_gia, co_the_danh_gia }`
- `GET /api/customers/{ma_kh}/pending-reviews` (Header `X-Customer-Token` or `X-Admin-Token`) -> `PendingReviewItem[]`
- `POST /api/reviews` (Header `X-Customer-Token`) body `{ ma_don_hang, diem_tour, nhan_xet_tour?, co_danh_gia_nha_nghi, diem_nha_nghi?, nhan_xet_nha_nghi? }` -> `{ message, ma_don_hang, ngay_danh_gia }`
- `GET /api/orders/{ma_don}/confirmation/pdf?nguoi_lap=...` (Header `X-Customer-Token` owning `ma_don` OR `X-Admin-Token`) -> binary `application/pdf`
- `GET /api/admin/orders?trang_thai=...&tu_khoa=...` (Header `X-Admin-Token`) -> `{ counts: { ALL, DAT, THANHTOAN, HOANTHANH, HUY }, orders: AdminOrderSummary[] }`
- `GET /api/admin/orders/{ma_don}` (Header `X-Admin-Token`) -> `{ detail: AdminOrderDetail, valid_next_statuses: { ma_trang_thai, ten_trang_thai }[], phone_numbers: string, shuttles: ShuttleItem[] }`
- `POST /api/admin/orders/{ma_don}/cancel-preview` (Header `X-Admin-Token`) body `{ ngay_gio_huy: string }` -> `{ ma_don_hang, tong_tien, so_ngay_truoc_khoi_hanh, so_gio_sau_khi_dat, ty_le_phat, tien_phat, tien_hoan }`
- `POST /api/admin/orders/{ma_don}/cancel` (Header `X-Admin-Token`) body `{ ngay_gio_huy: string, ly_do_huy: string, da_dong_y_phat: boolean }` -> `{ message, ma_don_hang, tien_phat, tien_hoan, so_cho_hoan }`
- `PATCH /api/admin/orders/{ma_don}/status` (Header `X-Admin-Token`) body `{ trang_thai_moi: string }` -> `{ message, ma_don_hang, ma_trang_thai }`
- `GET /api/admin/orders/{ma_don}/confirmation/html?nguoi_lap=...` (Header `X-Admin-Token`) -> `{ html: string, ma_don_hang: string }`
- `GET /api/admin/reports/revenue?tu_ngay=YYYY-MM-DD&den_ngay=YYYY-MM-DD` (Header `X-Admin-Token`) -> `{ summary: { tong_doanh_thu, so_don, so_khach, so_don_huy }, tours: RevenueTourRow[], accommodations: AccommodationRankRow[], noi_nhan: string }`
- `POST /api/admin/reports/revenue/html` (Header `X-Admin-Token`) body `{ tu_ngay, den_ngay, nguoi_lap }` -> `{ html: string }`
- `POST /api/admin/reports/revenue/pdf` (Header `X-Admin-Token`) body `{ tu_ngay, den_ngay, nguoi_lap }` -> binary `application/pdf`

**Steps:**
- [ ] **Step 1:** Install `fastapi`, `pydantic`, `httpx` into `D:\Khanh\CSDL\.venv` and create `web_app/backend/requirements.txt`.
- [ ] **Step 2:** Implement `dependencies.py` (sys.path injection for `tour_app`, HMAC-SHA256 token sign/verify for `X-Customer-Token` & `X-Admin-Token`, MySQL error -> HTTPException translator, Decimal/datetime serializer), `schemas.py`, `queries.py`, and `pdf_service.py` (with `BẮC VIỆT TRAVEL` brand transform on confirmation HTML + Chrome/Edge headless PDF render).
- [ ] **Step 3:** Implement `routers/public.py`, `routers/auth.py`, `routers/bookings.py`, `routers/admin.py`, and `main.py` (CORS for `http://localhost:5173` and `http://127.0.0.1:5173`, plus automatic mounting of `web_app/frontend/dist` if built).
- [ ] **Step 4:** Write comprehensive `web_app/backend/tests/test_api.py` covering all endpoints, all 5 Review Focus items (serialization, 401/403 ownership, guest auto-session + rollback, day tour `LT06`, real 1-page A4 PDF binary + XSS escaping) using `tour_app/tests/helpers.py` cleanup so DB returns to pristine state.
- [ ] **Step 5:** Run `.\.venv\Scripts\python.exe -m unittest discover -s web_app\backend\tests -v` AND `.\.venv\Scripts\python.exe -m unittest discover -s tour_app\tests -v` — verify 100% PASS and zero constraint violations.

---

### Task 2: Local Northern Vietnam Photography Assets (11 Images)

**Files:**
- Create: `web_app/frontend/public/images/hero-northern-vietnam.png`
- Create: `web_app/frontend/public/images/promo-cruise.png`
- Create: `web_app/frontend/public/images/tour-T01.png` through `tour-T09.png`

**Steps:**
- [ ] **Step 1:** Generate 11 cohesive, vibrant, natural-light travel photography assets (no text, no watermark, no logos) via `image-generator` subagents matching each tour (`T01` Hạ Long kayak, `T02` Sa Pa Fansipan, `T03` Tràng An Ninh Bình, `T04` Mộc Châu tea hills, `T05` Cát Bà Lan Hạ, `T06` Bản Giốc waterfall, `T07` Hạ Long luxury cruise, `T08` Tây Bắc Điện Biên, `T09` Hà Giang Mã Pì Lèng + Nho Quế, plus Hero panoramic Hạ Long vista and Promo cruise scene).
- [ ] **Step 2:** Copy all 11 generated images to exact filenames inside `web_app/frontend/public/images/` and verify every file is non-empty.

---

### Task 3: Frontend Foundation, Design System, Shared Components & User Portal (`frontend-user`)

**Files:**
- Create: `web_app/frontend/package.json`, `vite.config.ts`, `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`, `index.html`
- Create: `web_app/frontend/src/styles/tokens.css`, `src/styles/globals.css`
- Create: `web_app/frontend/src/api/types.ts`, `src/api/client.ts`
- Create: `web_app/frontend/src/utils/format.ts`
- Create: `web_app/frontend/src/constants/tourImages.ts`
- Create: `web_app/frontend/src/context/AuthContext.tsx`
- Create: `web_app/frontend/src/components/common/BrandLogo.tsx`, `Button.tsx`, `StatusBadge.tsx`, `StarRating.tsx`, `Modal.tsx`, `SlideOverDrawer.tsx`, `EmptyState.tsx`, `LoadingSkeleton.tsx`
- Create: `web_app/frontend/src/components/layout/UserLayout.tsx`, `AdminLayout.tsx`, `CustomerLoginModal.tsx`
- Create: `web_app/frontend/src/components/user/HeroOrganicFrame.tsx`, `FloatingSearchBar.tsx`, `TourCard.tsx`, `BookingSummaryCard.tsx`
- Create: `web_app/frontend/src/pages/user/LandingPage.tsx`, `ExplorePage.tsx`, `BookingPage.tsx`, `MyBookingsPage.tsx`
- Create: `web_app/frontend/src/App.tsx`, `src/main.tsx`

**Interfaces (Produces for `frontend-admin`):**
- `src/api/types.ts`: Exports every TypeScript interface matching Task 1 JSON responses verbatim (`ProvinceItem`, `ScheduleSearchItem`, `OpenScheduleItem`, `AccommodationItem`, `CustomerItem`, `CustomerOrderItem`, `PendingReviewItem`, `AdminOrderSummary`, `AdminOrderDetail`, `ValidNextStatus`, `ShuttleItem`, `AdminOrderFullResponse`, `CancelPreviewResponse`, `RevenueTourRow`, `AccommodationRankRow`, `RevenueReportResponse`, `MetaResponse`, `LandingResponse`).
- `src/api/client.ts`: Exports `api` object with typed methods:
  - `getMeta()`, `getLanding()`, `getProvinces()`, `searchSchedules(params)`, `getOpenSchedules()`, `getAccommodations(maTinhDen)`, `getCustomers()`, `checkDuplicateCustomer(email, sdt)`
  - `customerLogin(identifier)`, `adminLogin(username, password, staffName?)`
  - `estimateBooking(payload)`, `createBooking(payload)`, `getCustomerOrders(maKh)`, `getPendingReviews(maKh)`, `submitReview(payload)`
  - `downloadConfirmationPdf(maDon, nguoiLap?)` -> triggers browser `.pdf` download (`Blob`)
  - `getAdminOrders(params)`, `getAdminOrderDetail(maDon)`, `previewCancelOrder(maDon, ngayGioHuy)`, `cancelOrder(maDon, payload)`, `updateOrderStatus(maDon, trangThaiMoi)`
  - `getConfirmationHtml(maDon, nguoiLap)`, `getRevenueReport(tuNgay, denNgay)`, `getRevenueHtml(tuNgay, denNgay, nguoiLap)`, `downloadRevenuePdf(tuNgay, denNgay, nguoiLap)` -> triggers browser `.pdf` download (`Blob`)
- `src/context/AuthContext.tsx`: Exports `AuthProvider` and `useAuth()` returning:
  `{ customer, customerToken, admin, adminToken, loginCustomer, setCustomerSession, logoutCustomer, loginAdmin, logoutAdmin, openCustomerLoginModal }`
- `src/utils/format.ts`: Exports `formatVnd(amount)`, `formatDateTime(iso)`, `formatDate(iso)`, `toSqlDateTimeInput(date, time)`.
- `src/components/common/*`: Exports `BrandLogo`, `Button`, `StatusBadge`, `StarRating`, `Modal`, `SlideOverDrawer`, `EmptyState`, `LoadingSkeleton`.
- `src/components/layout/AdminLayout.tsx`: Exports `AdminLayout` (sidebar nav for `/admin/dashboard`, `/admin/orders`, `/admin/confirmations`, auth guard redirecting unauthenticated users to `/admin/login`).
- `src/App.tsx`: Wires routes `/`, `/explore`, `/book`, `/my-bookings`, `/admin/login`, `/admin/dashboard`, `/admin/orders`, `/admin/confirmations` (importing default exports from `./pages/admin/AdminLoginPage`, `AdminDashboardPage`, `AdminOrdersPage`, `AdminConfirmationsPage`).

**Steps:**
- [ ] **Step 1:** Initialize Vite + React 19 + TypeScript + Tailwind CSS v4 project in `web_app/frontend/` and install `react-router-dom`, `framer-motion`, `lucide-react`, `recharts`, `tailwindcss`, `@tailwindcss/vite`. Configure Vite proxy `/api` -> `http://127.0.0.1:8000`.
- [ ] **Step 2:** Create `index.html` (Google Fonts `Spectral` + `Be Vietnam Pro`, Vietnamese title `Bắc Việt Travel — Du lịch miền Bắc`), `src/styles/tokens.css`, `src/styles/globals.css` (custom selection, focus-visible ring, tabular-nums utility, smooth transitions).
- [ ] **Step 3:** Create `src/api/types.ts`, `src/api/client.ts`, `src/utils/format.ts`, `src/constants/tourImages.ts`, `src/context/AuthContext.tsx`, and all `common/` + `layout/` components.
- [ ] **Step 4:** Build `LandingPage.tsx` faithful to reference Image 1 (editorial split Hero with `Spectral` display + italic cobalt emphasis, organic SVG curved mask hero photo, floating glassmorphism real-DB stats badge, floating pill search bar overlapping hero bottom, cobalt gradient Luxury Tour card + live DB metrics strip + 4-card Featured Destinations grid with photo hover zoom and star pills). Zero PTIT/12-table/demo-clock/F1..R2 text.
- [ ] **Step 5:** Build `ExplorePage.tsx` (8 filters + luxury/reset quick buttons + card/table view + direct `Đặt tour này` link), `BookingPage.tsx` (2-column layout with sticky cost estimator, guest/logged-in flow, day-tour `0 đêm` handling, accommodation filter, max 2 shuttle transfers, confirmation screen with instant PDF download), and `MyBookingsPage.tsx` (orders tab + interactive 5-star review tab with zero DB jargon).

---

### Task 4: Admin Portal Screens & Visualizations (`frontend-admin`)

**Files:**
- Create: `web_app/frontend/src/components/admin/KpiMetricCard.tsx`
- Create: `web_app/frontend/src/components/admin/RevenueChart.tsx`
- Create: `web_app/frontend/src/components/admin/OrderActionDrawer.tsx`
- Create: `web_app/frontend/src/components/admin/DocumentPreviewFrame.tsx`
- Create: `web_app/frontend/src/pages/admin/AdminLoginPage.tsx`
- Create: `web_app/frontend/src/pages/admin/AdminDashboardPage.tsx`
- Create: `web_app/frontend/src/pages/admin/AdminOrdersPage.tsx`
- Create: `web_app/frontend/src/pages/admin/AdminConfirmationsPage.tsx`

**Interfaces (Consumes from Task 3):**
- Uses exact exports from `src/api/client.ts`, `src/api/types.ts`, `src/context/AuthContext.tsx`, `src/utils/format.ts`, `src/components/common/*`.
- Produces default exports `AdminLoginPage`, `AdminDashboardPage`, `AdminOrdersPage`, `AdminConfirmationsPage` consumed by `src/App.tsx`.

**Steps:**
- [ ] **Step 1:** Implement `AdminLoginPage.tsx` (clean split card login for Operations Staff with demo fill button `admin` / `admin123`, staff name input, link back to Customer Landing Page).
- [ ] **Step 2:** Implement `KpiMetricCard.tsx`, `RevenueChart.tsx` (Recharts horizontal bar chart comparing `DoanhThuDichVu` and `TienPhatHuy` per tour, excluding `TỔNG CỘNG` ROLLUP row), `DocumentPreviewFrame.tsx`, and `AdminDashboardPage.tsx` (date filter default `2026-09-01`..`2026-12-31`, `Người lập báo cáo` input, 4 KPI cards, chart, Tour Revenue table with highlighted `TỔNG CỘNG` row, Accommodation Ranking table, `Xuất báo cáo PDF (A4 ngang)` button calling `api.downloadRevenuePdf`, and inline A4 print preview toggle).
- [ ] **Step 3:** Implement `OrderActionDrawer.tsx` and `AdminOrdersPage.tsx` (status filter pills with live counts, search bar, full order table, click-to-open slide-over drawer displaying customer/schedule/accommodation/shuttle/costs, forward status transition buttons, full cancellation section with live penalty preview via `api.previewCancelOrder`, mandatory consent checkbox, atomic `api.cancelOrder`, and direct PDF confirmation button).
- [ ] **Step 4:** Implement `AdminConfirmationsPage.tsx` (searchable order selector reading optional `?order=DHxxx` query param, `Nhân viên lập phiếu` input, live A4 portrait preview via `api.getConfirmationHtml`, `Tải phiếu xác nhận (PDF - A4 dọc)` button calling `api.downloadConfirmationPdf`, and browser print button).

---

### Task 5: End-to-End Integration, Build & Browser Visual Verification (`verifier`)

**Steps:**
- [ ] **Step 1:** Run `.\.venv\Scripts\python.exe -m unittest discover -s tour_app\tests -v` — verify 100% PASS (zero regressions in original app).
- [ ] **Step 2:** Run `.\.venv\Scripts\python.exe -m unittest discover -s web_app\backend\tests -v` — verify 100% PASS (API + Auth + real A4 PDF binary).
- [ ] **Step 3:** Run `npm run build` inside `web_app/frontend` — verify 0 TypeScript / Vite errors.
- [ ] **Step 4:** Static UI hygiene grep across `web_app/frontend/src/`: confirm ZERO occurrences of `F1.`, `F2.`, `F3.`, `S1.`, `R1.`, `R2.`, `HOANTHANH` in user-facing copy, `MaNhaNghi IS NULL`, `chk_DonHang`, `RB22`, `PTIT`, or emoji characters; confirm all 11 image files exist in `web_app/frontend/public/images/`.
- [ ] **Step 5:** Start FastAPI serving API + built SPA (or dev servers) and perform real browser verification across Desktop (1440px) and Mobile (390px) for User Portal (`/`, `/explore`, `/book`, `/my-bookings`) and Admin Portal (`/admin/login`, `/admin/dashboard`, `/admin/orders`, `/admin/confirmations`), verifying zero console errors, zero broken images, and live PDF downloads.

---

## Self-Review Checklist
- **Spec coverage:** Every requirement in `2026-11-19-bac-viet-travel-web-design.md` and `2026-11-19-design-system-rules.md` maps directly to Tasks 1–5 (User Landing Page + 3 User screens, Admin Login + 3 Admin screens, HMAC role separation without altering 12 MySQL tables, real A4 PDF export for Revenue & Confirmation, 11 local images, zero `F1..R2`/AI captions/emojis).
- **Type consistency:** All REST paths, query params, JSON keys, and TypeScript interfaces in Task 1 match Task 3 and Task 4 identically.
- **Collision check:** `backend`, `frontend-user`, `frontend-admin`, and `image-generator` operate on strictly disjoint file sets.
