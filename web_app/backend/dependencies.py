"""Cấu hình đường dẫn tour_app, xác thực token HMAC-SHA256, xử lý lỗi MySQL và chuẩn hóa JSON."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import mysql.connector
from fastapi import Header, HTTPException

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parents[1]
TOUR_APP_DIR = ROOT_DIR / "tour_app"

if str(TOUR_APP_DIR) not in sys.path:
    sys.path.insert(0, str(TOUR_APP_DIR))

import db  # noqa: E402
import services  # noqa: E402

DEFAULT_SESSION_SECRET = "bac-viet-travel-local-session-secret-2026"
DEFAULT_TOKEN_TTL_SECONDS = 7 * 24 * 60 * 60


class AppValidationError(Exception):
    """Lỗi dữ liệu đầu vào kèm danh sách thông báo tiếng Việt chi tiết."""

    def __init__(self, detail: str, errors: list[str] | None = None, status_code: int = 400):
        super().__init__(detail)
        self.detail = detail
        self.errors = errors or [detail]
        self.status_code = status_code


def _session_secret() -> bytes:
    return os.environ.get("APP_SESSION_SECRET", DEFAULT_SESSION_SECRET).encode("utf-8")


def get_admin_credentials() -> tuple[str, str, str]:
    username = os.environ.get("ADMIN_USERNAME", "admin")
    password = os.environ.get("ADMIN_PASSWORD", "admin123")
    default_staff = os.environ.get("ADMIN_DEFAULT_STAFF_NAME", "Nguyễn Quốc Khánh")
    return username, password, default_staff


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64url_decode(encoded: str) -> bytes:
    padding = "=" * (-len(encoded) % 4)
    return base64.urlsafe_b64decode((encoded + padding).encode("ascii"))


def sign_token(payload: dict[str, Any], ttl_seconds: int = DEFAULT_TOKEN_TTL_SECONDS) -> str:
    """Ký token phiên không lưu trạng thái bằng HMAC-SHA256."""
    now = int(time.time())
    body = dict(payload)
    body.setdefault("iat", now)
    body.setdefault("exp", now + ttl_seconds)
    payload_bytes = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    payload_b64 = _b64url_encode(payload_bytes)
    sig = hmac.new(_session_secret(), payload_b64.encode("ascii"), hashlib.sha256).digest()
    return f"{payload_b64}.{_b64url_encode(sig)}"


def verify_token(token: str, expected_role: str | None = None) -> dict[str, Any]:
    """Xác minh chữ ký và thời hạn token phiên HMAC-SHA256."""
    if not token or "." not in token:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        )

    parts = token.strip().split(".")
    if len(parts) != 2:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        )

    payload_b64, sig_b64 = parts
    expected_sig = hmac.new(_session_secret(), payload_b64.encode("ascii"), hashlib.sha256).digest()
    try:
        actual_sig = _b64url_decode(sig_b64)
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        ) from exc

    if not hmac.compare_digest(actual_sig, expected_sig):
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        )

    try:
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    except Exception as exc:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        ) from exc

    if not isinstance(payload, dict):
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        )

    exp = payload.get("exp")
    if exp is not None and int(time.time()) > int(exp):
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại.",
        )

    if expected_role and payload.get("role") != expected_role:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không đúng vai trò yêu cầu.",
        )

    return payload


def sign_customer_token(ma_kh: str) -> str:
    return sign_token({"role": "user", "ma_kh": ma_kh})


def sign_admin_token(username: str, staff_name: str) -> str:
    return sign_token({"role": "admin", "username": username, "staff_name": staff_name})


def require_admin(
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> dict[str, Any]:
    if not x_admin_token:
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập tài khoản quản trị để thực hiện thao tác này.",
        )
    return verify_token(x_admin_token, expected_role="admin")


def require_customer(
    x_customer_token: str | None = Header(default=None, alias="X-Customer-Token"),
) -> dict[str, Any]:
    if not x_customer_token:
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập tài khoản khách hàng để tiếp tục.",
        )
    return verify_token(x_customer_token, expected_role="user")


def get_optional_auth(
    x_customer_token: str | None = Header(default=None, alias="X-Customer-Token"),
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> dict[str, dict[str, Any] | None]:
    admin: dict[str, Any] | None = None
    customer: dict[str, Any] | None = None
    first_error: HTTPException | None = None

    if x_admin_token:
        try:
            admin = verify_token(x_admin_token, expected_role="admin")
        except HTTPException as exc:
            first_error = first_error or exc

    if x_customer_token:
        try:
            customer = verify_token(x_customer_token, expected_role="user")
        except HTTPException as exc:
            first_error = first_error or exc

    if admin is None and customer is None and first_error is not None:
        raise first_error

    return {"admin": admin, "customer": customer}


def ensure_customer_or_admin(auth: dict[str, dict[str, Any] | None], ma_kh: str) -> None:
    """Cho phép quản trị viên hoặc chính chủ tài khoản khách hàng truy cập."""
    if auth["admin"] is not None:
        return
    if auth["customer"] is None:
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập để xem thông tin đơn hàng.",
        )
    if auth["customer"].get("ma_kh") != ma_kh:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền truy cập thông tin của khách hàng khác.",
        )


def mysql_error_to_http(exc: Exception) -> HTTPException:
    """Chuyển lỗi MySQL hoặc KhongCoDongNao sang HTTPException tiếng Việt rõ ràng."""
    message = db.thong_bao_loi(exc)
    if isinstance(exc, db.KhongCoDongNao):
        return HTTPException(status_code=409, detail=message)
    if isinstance(exc, mysql.connector.Error):
        if exc.errno == 1062:
            return HTTPException(status_code=409, detail=message)
        if exc.errno in (3819, 1406, 1452):
            return HTTPException(status_code=400, detail=message)
        if exc.errno == 1451:
            return HTTPException(status_code=409, detail=message)
        if exc.errno in (2002, 2003, 1045, 1049):
            return HTTPException(status_code=503, detail=message)
        return HTTPException(status_code=500, detail=message)
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    return HTTPException(status_code=500, detail=message)


def to_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    if isinstance(value, Decimal):
        return int(round(value))
    return int(value)


def to_opt_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, Decimal):
        return int(round(value))
    return int(value)


def to_opt_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)


def to_iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = datetime.fromisoformat(text)
            if len(text) == 10:
                return parsed.strftime("%Y-%m-%d")
            return parsed.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return text
    return str(value)


def parse_datetime_input(value: str | None) -> datetime | None:
    if value is None:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1]
    return datetime.fromisoformat(text).replace(tzinfo=None, microsecond=0)


def parse_date_input(value: str | date | None) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    text = value.strip()
    if not text:
        return None
    return date.fromisoformat(text[:10])


def sanitize_json(value: Any) -> Any:
    """Chuyển đệ quy Decimal sang int/float và datetime/date sang chuỗi ISO-8601."""
    if isinstance(value, dict):
        return {k: sanitize_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize_json(item) for item in value]
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    if isinstance(value, datetime):
        return value.replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


def clean_user_message(message: str) -> str:
    """Loại bỏ mã quy tắc kỹ thuật khỏi thông báo trả về cho người dùng cuối."""
    cleaned = message.replace(" (RB22)", "").replace("(RB22)", "")
    cleaned = cleaned.replace(" (RB23)", "").replace("(RB23)", "")
    return cleaned.strip()


__all__ = [
    "AppValidationError",
    "BACKEND_DIR",
    "ROOT_DIR",
    "TOUR_APP_DIR",
    "clean_user_message",
    "db",
    "ensure_customer_or_admin",
    "get_admin_credentials",
    "get_optional_auth",
    "mysql_error_to_http",
    "parse_date_input",
    "parse_datetime_input",
    "require_admin",
    "require_customer",
    "sanitize_json",
    "services",
    "sign_admin_token",
    "sign_customer_token",
    "sign_token",
    "to_int",
    "to_iso",
    "to_opt_float",
    "to_opt_int",
    "verify_token",
]
