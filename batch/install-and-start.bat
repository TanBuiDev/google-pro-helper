@echo off
chcp 65001 >nul
title Google Pro Helper - Cài đặt và khởi chạy
cd /d "%~dp0"
echo ==============================================================
echo   Đang kiểm tra và cài đặt thư viện Python...
echo ==============================================================
python -m pip install --index-url https://pypi.org/simple -r requirements.txt
if errorlevel 1 (
  echo Khong the cai dat thu vien. Kiem tra ket noi va thu lai.
  pause
  exit /b 1
)
echo.
echo ==============================================================
echo   Đang mở bảng điều khiển (http://127.0.0.1:8765)...
echo ==============================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
