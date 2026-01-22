@echo off
REM ===========================================
REM AI 占卜应用 - 开发模式启动脚本 (批处理)
REM ===========================================
REM 
REM 使用方法：
REM dev-start.bat
REM
REM ===========================================

echo ============================================
echo AI 占卜应用 - 开发模式启动
echo ============================================
echo.

REM 检查 Python
echo [1/6] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
python --version
echo [OK] Python 已安装

REM 检查 Node.js
echo [2/6] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)
node --version
echo [OK] Node.js 已安装

REM 检查 pnpm
echo [3/6] 检查 pnpm...
pnpm --version >nul 2>&1
if errorlevel 1 (
    echo [警告] pnpm 未安装，正在安装...
    call npm install -g pnpm
)
pnpm --version
echo [OK] pnpm 已安装

REM 检查 .env 文件
echo [4/6] 检查环境变量配置...
if not exist ".env" (
    echo [警告] .env 文件不存在，正在从 .env.example 创建...
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo [OK] 已创建 .env 文件，请编辑并配置 API Key
        echo       至少需要配置: api_key=sk-your-api-key
    ) else (
        echo [错误] .env.example 文件不存在
    )
) else (
    echo [OK] .env 文件已存在
)

REM 设置后端虚拟环境
echo [5/6] 设置后端环境...
if not exist "venv" (
    echo   创建 Python 虚拟环境...
    python -m venv venv
)

echo   激活虚拟环境...
call venv\Scripts\activate.bat

echo   安装后端依赖...
pip install -r requirements.txt --quiet

echo [OK] 后端环境准备完成

REM 安装前端依赖
echo [6/6] 设置前端环境...
cd frontend
if not exist "node_modules" (
    echo   安装前端依赖...
    call pnpm install
) else (
    echo   node_modules 已存在，跳过安装
)
cd ..

echo [OK] 前端环境准备完成
echo.

echo ============================================
echo 环境准备完成！
echo ============================================
echo.
echo 接下来需要启动两个终端：
echo.
echo 【终端 1 - 后端服务】
echo   cd %CD%
echo   venv\Scripts\activate.bat
echo   python main.py
echo   后端将在 http://localhost:8000 运行
echo.
echo 【终端 2 - 前端服务】
echo   cd %CD%\frontend
echo   pnpm dev
echo   前端将在 http://localhost:5173 运行
echo.
echo ============================================
echo.

set /p response="是否自动启动后端和前端？(Y/N): "
if /i "%response%"=="Y" (
    echo.
    echo 正在启动服务...
    echo.
    
    REM 启动后端（在新窗口中）
    start "后端服务 - AI占卜" cmd /k "cd /d %CD% && venv\Scripts\activate.bat && python main.py"
    timeout /t 3 /nobreak >nul
    
    REM 启动前端（在新窗口中）
    start "前端服务 - AI占卜" cmd /k "cd /d %CD%\frontend && pnpm dev"
    
    echo.
    echo [OK] 服务已启动！
    echo   后端: http://localhost:8000
    echo   前端: http://localhost:5173
    echo.
    echo 提示：已打开两个新的命令窗口运行服务
)

pause
