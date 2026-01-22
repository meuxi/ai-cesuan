# ===========================================
# AI 占卜应用 - 开发模式启动脚本 (PowerShell)
# ===========================================
# 
# 此脚本会：
# 1. 检查 Python 和 Node.js 环境
# 2. 检查并创建虚拟环境
# 3. 安装依赖
# 4. 启动后端和前端开发服务器
#
# 使用方法：
# .\dev-start.ps1
#
# ===========================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "AI 占卜应用 - 开发模式启动" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "[1/6] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未找到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

# 检查 Node.js
Write-Host "[2/6] 检查 Node.js 环境..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未找到 Node.js，请先安装 Node.js 18+" -ForegroundColor Red
    exit 1
}

# 检查 pnpm
Write-Host "[3/6] 检查 pnpm..." -ForegroundColor Yellow
try {
    $pnpmVersion = pnpm --version 2>&1
    Write-Host "✓ pnpm: $pnpmVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠ pnpm 未安装，正在安装..." -ForegroundColor Yellow
    npm install -g pnpm
}

# 检查 .env 文件
Write-Host "[4/6] 检查环境变量配置..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "⚠ .env 文件不存在，正在从 .env.example 创建..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "✓ 已创建 .env 文件，请编辑并配置 API Key" -ForegroundColor Green
        Write-Host "  至少需要配置: api_key=sk-your-api-key" -ForegroundColor Yellow
    } else {
        Write-Host "✗ .env.example 文件不存在" -ForegroundColor Red
    }
} else {
    Write-Host "✓ .env 文件已存在" -ForegroundColor Green
}

# 设置后端虚拟环境
Write-Host "[5/6] 设置后端环境..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    Write-Host "  创建 Python 虚拟环境..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "  激活虚拟环境..." -ForegroundColor Gray
& ".\venv\Scripts\Activate.ps1"

Write-Host "  安装后端依赖..." -ForegroundColor Gray
pip install -r requirements.txt --quiet

Write-Host "✓ 后端环境准备完成" -ForegroundColor Green

# 安装前端依赖
Write-Host "[6/6] 设置前端环境..." -ForegroundColor Yellow
Set-Location frontend
if (-not (Test-Path "node_modules")) {
    Write-Host "  安装前端依赖..." -ForegroundColor Gray
    pnpm install
} else {
    Write-Host "  node_modules 已存在，跳过安装" -ForegroundColor Gray
}
Set-Location ..

Write-Host "✓ 前端环境准备完成" -ForegroundColor Green
Write-Host ""

# 提示用户
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "环境准备完成！" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "接下来需要启动两个终端：" -ForegroundColor Yellow
Write-Host ""
Write-Host "【终端 1 - 后端服务】" -ForegroundColor Cyan
Write-Host "  cd $PWD" -ForegroundColor Gray
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "  python main.py" -ForegroundColor Gray
Write-Host "  后端将在 http://localhost:8000 运行" -ForegroundColor Green
Write-Host ""
Write-Host "【终端 2 - 前端服务】" -ForegroundColor Cyan
Write-Host "  cd $PWD\frontend" -ForegroundColor Gray
Write-Host "  pnpm dev" -ForegroundColor Gray
Write-Host "  前端将在 http://localhost:5173 运行" -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 询问是否自动启动
$response = Read-Host "是否自动启动后端和前端？(Y/N)"
if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host ""
    Write-Host "正在启动服务..." -ForegroundColor Yellow
    Write-Host ""
    
    # 启动后端（在新窗口中）
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .\venv\Scripts\Activate.ps1; python main.py"
    Start-Sleep -Seconds 3
    
    # 启动前端（在新窗口中）
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; pnpm dev"
    
    Write-Host ""
    Write-Host "✓ 服务已启动！" -ForegroundColor Green
    Write-Host "  后端: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "  前端: http://localhost:5173" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "提示：已打开两个新的 PowerShell 窗口运行服务" -ForegroundColor Yellow
}
