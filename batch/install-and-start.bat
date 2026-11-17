@echo off
chcp 65001 >nul
title Google Pro Helper - Cài đặt và khởi chạy
cd /d "%~dp0"
echo ==============================================================
echo   Đang kiểm tra và cài đặt thư viện Python...
echo ==============================================================
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.
echo ==============================================================
echo   Đang mở bảng điều khiển (http://127.0.0.1:8765)...
echo ==============================================================
start "" "http://127.0.0.1:8765"
python app.py
pause
