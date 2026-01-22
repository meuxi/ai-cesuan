@echo off
chcp 65001 >nul
echo ============================================
echo 启动后端服务
echo ============================================
cd /d %~dp0
call venv\Scripts\activate.bat
echo.
echo 后端服务启动中...
echo 后端地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.
python main.py
pause
