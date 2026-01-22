@echo off
chcp 65001 >nul
echo ============================================
echo 启动前端服务
echo ============================================
cd /d %~dp0frontend
echo.
echo 前端服务启动中...
echo 前端地址: http://localhost:5173
echo.
echo 按 Ctrl+C 停止服务
echo.
call pnpm dev
pause
