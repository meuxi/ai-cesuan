@echo off
chcp 65001 >nul
echo ============================================
echo 启动后端服务 (生产模式)
echo ============================================
cd /d %~dp0
call venv\Scripts\activate.bat
echo.
echo 生产模式: 多进程 (4 workers)
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

set UVICORN_WORKERS=4
python main.py
pause
