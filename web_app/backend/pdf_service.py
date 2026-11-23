"""Dịch vụ dựng HTML biểu mẫu đồng bộ thương hiệu và xuất PDF A4 thật qua Chrome/Edge headless."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from datetime import date, datetime
from pathlib import Path

from fastapi import HTTPException

try:
    from .dependencies import db, services
except ImportError:
    from dependencies import db, services

CONFIRMATION_BRAND_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    ("PTIT TOUR", "BẮC VIỆT TRAVEL"),
    ("PTIT Tour", "Bắc Việt Travel"),
    ("dieuhanh@ptittour.edu.vn", "lienhe@bacviettravel.vn"),
    (
        "Km10, Đường Nguyễn Trãi, Quận Hà Đông, Hà Nội",
        "Số 10 Nguyễn Trãi, Hà Đông, Hà Nội",
    ),
    (
        """        .header-table td {
            vertical-align: top;
            font-size: 9.8pt;
        }""",
        """        .header-table td {
            vertical-align: top;
            font-size: 9.6pt;
        }
        .header-quoc-hieu-cell {
            text-align: center;
        }
        .quoc-hieu {
            font-size: 12pt;
            font-weight: bold;
            line-height: 1.25;
            letter-spacing: 0.15px;
        }
        .tieu-ngu {
            font-size: 11.5pt;
            font-weight: bold;
            line-height: 1.25;
            margin-top: 1px;
        }
        .tieu-ngu span {
            display: inline-block;
            border-bottom: 1px solid #111;
            padding-bottom: 2px;
        }
        .ngay-in-phieu {
            font-size: 9.5pt;
            margin-top: 3px;
        }""",
    ),
    (
        """            <td style="width: 52%;">
                <strong>CÔNG TY DU LỊCH &amp; LỮ HÀNH BẮC VIỆT TRAVEL</strong><br>
                Địa chỉ: Số 10 Nguyễn Trãi, Hà Đông, Hà Nội<br>
                Hotline: 1900 1234 | Email: lienhe@bacviettravel.vn
            </td>
            <td style="width: 48%; text-align: right;">
                <strong>CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</strong><br>
                <span>Độc lập - Tự do - Hạnh phúc</span><br>
                <em>Ngày in phiếu:""",
        """            <td style="width: 46%;">
                <strong>CÔNG TY DU LỊCH &amp; LỮ HÀNH BẮC VIỆT TRAVEL</strong><br>
                Địa chỉ: Số 10 Nguyễn Trãi, Hà Đông, Hà Nội<br>
                Hotline: 1900 1234 | Email: lienhe@bacviettravel.vn
            </td>
            <td class="header-quoc-hieu-cell" style="width: 54%;">
                <div class="quoc-hieu">CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM</div>
                <div class="tieu-ngu"><span>Độc lập - Tự do - Hạnh phúc</span></div>
                <div class="ngay-in-phieu"><em>Ngày in phiếu:""",
    ),
    (
        """</em>
            </td>
        </tr>
    </table>""",
        """</em></div>
            </td>
        </tr>
    </table>""",
    ),
)


def apply_confirmation_branding(html_content: str) -> str:
    """Chuyển đổi nhận diện thương hiệu trên HTML phiếu xác nhận mà không sửa tour_app/templates/."""
    branded = html_content
    for old_text, new_text in CONFIRMATION_BRAND_REPLACEMENTS:
        branded = branded.replace(old_text, new_text)
    return branded


def build_confirmation_html(
    ma_don_hang: str,
    nguoi_lap: str,
    ngay_in: datetime | None = None,
) -> str:
    """Dựng chuỗi HTML phiếu xác nhận đặt tour (khổ A4 dọc) có thương hiệu Bắc Việt Travel."""
    ct = services.lay_chi_tiet_don_r1(ma_don_hang)
    if ct is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng.")
    ds_sdt = services.lay_sdt_khach_r1(ma_don_hang)
    ds_ctc = services.lay_lich_trung_chuyen_r1(ma_don_hang)
    raw_html = services.tao_html_phieu_xac_nhan(
        ct=ct,
        danh_sach_sdt=ds_sdt,
        ds_ctc=ds_ctc,
        nguoi_lap=nguoi_lap,
        ngay_in=ngay_in or db.hien_tai(),
    )
    return apply_confirmation_branding(raw_html)


def build_revenue_report_html(
    tu_ngay: date,
    den_ngay: date,
    nguoi_lap: str,
    ngay_xuat: datetime | None = None,
) -> str:
    """Dựng chuỗi HTML báo cáo doanh thu (khổ A4 ngang) từ services.tao_html_bao_cao_doanh_thu."""
    ds_tour = services.lay_doanh_thu_tour_r2(tu_ngay, den_ngay)
    ds_noi_nghi = services.lay_xep_hang_noi_nghi_r2(tu_ngay, den_ngay)
    return services.tao_html_bao_cao_doanh_thu(
        tu_ngay=tu_ngay,
        den_ngay=den_ngay,
        ds_tour=ds_tour,
        ds_noi_nghi=ds_noi_nghi,
        nguoi_lap=nguoi_lap,
        ngay_xuat=ngay_xuat or db.hien_tai(),
        noi_nhan=services.NOI_NHAN_R2,
    )


def find_headless_browser() -> str | None:
    """Tìm đường dẫn trình duyệt Chrome hoặc Microsoft Edge hỗ trợ xuất PDF headless."""
    candidates = [
        os.environ.get("PDF_BROWSER_PATH"),
        shutil.which("chrome"),
        shutil.which("msedge"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\Application\msedge.exe"),
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None


def render_html_to_pdf(html_content: str, timeout_seconds: int = 30) -> bytes:
    """Chuyển chuỗi HTML chuẩn in A4 sang dữ liệu nhị phân PDF thật (%PDF-)."""
    browser = find_headless_browser()
    if not browser:
        raise HTTPException(
            status_code=503,
            detail="Không tìm thấy trình duyệt Chrome hoặc Edge trên máy chủ để xuất tệp PDF.",
        )

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_dir:
        td = Path(tmp_dir)
        html_path = td / "document.html"
        pdf_path = td / "document.pdf"
        profile_dir = td / "profile"
        profile_dir.mkdir(exist_ok=True)

        html_path.write_text(html_content, encoding="utf-8")

        try:
            completed = subprocess.run(
                [
                    browser,
                    "--headless",
                    "--disable-gpu",
                    "--no-pdf-header-footer",
                    f"--user-data-dir={profile_dir}",
                    f"--print-to-pdf={pdf_path}",
                    html_path.as_uri(),
                ],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(
                status_code=503,
                detail="Quá thời gian xử lý khi tạo tệp PDF, vui lòng thử lại.",
            ) from exc
        except OSError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"Không thể khởi chạy trình duyệt xuất PDF: {exc}",
            ) from exc

        if completed.returncode != 0 or not pdf_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Không thể xuất tệp PDF từ biểu mẫu hiện tại.",
            )

        pdf_bytes = pdf_path.read_bytes()
        if not pdf_bytes.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=500,
                detail="Tệp PDF xuất ra không hợp lệ.",
            )
        return pdf_bytes
