"""Điểm khởi chạy FastAPI cho ứng dụng web Bắc Việt Travel."""

from __future__ import annotations

from pathlib import Path

import mysql.connector
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

try:
    from .dependencies import AppValidationError, ROOT_DIR, db, mysql_error_to_http
    from .routers import admin, auth, bookings, public
except ImportError:
    from dependencies import AppValidationError, ROOT_DIR, db, mysql_error_to_http
    from routers import admin, auth, bookings, public

FRONTEND_DIST_DIR = ROOT_DIR / "web_app" / "frontend" / "dist"

app = FastAPI(
    title="Bắc Việt Travel API",
    description="REST API đặt tour du lịch miền Bắc và quản trị vận hành Bắc Việt Travel.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.exception_handler(AppValidationError)
async def handle_app_validation_error(_request: Request, exc: AppValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "errors": exc.errors},
    )


@app.exception_handler(db.KhongCoDongNao)
async def handle_no_rows_error(_request: Request, exc: db.KhongCoDongNao) -> JSONResponse:
    http_exc = mysql_error_to_http(exc)
    return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})


@app.exception_handler(mysql.connector.Error)
async def handle_mysql_error(_request: Request, exc: mysql.connector.Error) -> JSONResponse:
    http_exc = mysql_error_to_http(exc)
    return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})


app.include_router(public.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(admin.router)


def _resolve_spa_file(full_path: str) -> Path | None:
    if not FRONTEND_DIST_DIR.is_dir():
        return None
    dist_root = FRONTEND_DIST_DIR.resolve()
    index_file = dist_root / "index.html"
    if not index_file.is_file():
        return None

    clean_rel = full_path.lstrip("/")
    if clean_rel:
        candidate = (dist_root / clean_rel).resolve()
        if candidate.is_relative_to(dist_root) and candidate.is_file():
            return candidate
    return index_file


@app.get("/", include_in_schema=False)
def serve_spa_root():
    target = _resolve_spa_file("")
    if target is not None:
        return FileResponse(target)
    return {"name": "Bắc Việt Travel API", "docs": "/docs"}


@app.get("/{full_path:path}", include_in_schema=False)
def serve_spa_catchall(full_path: str):
    if full_path == "api" or full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Không tìm thấy đường dẫn API.")
    target = _resolve_spa_file(full_path)
    if target is not None:
        return FileResponse(target)
    raise HTTPException(status_code=404, detail="Không tìm thấy tài nguyên yêu cầu.")
