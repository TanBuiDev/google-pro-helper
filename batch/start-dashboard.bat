@echo off
chcp 65001 >nul
title Google Pro Helper - Bảng điều khiển
cd /d "%~dp0"
echo ==============================================================
echo   Đang khởi chạy bảng điều khiển Google Pro Helper...
echo   Địa chỉ: http://127.0.0.1:8765
echo ==============================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
