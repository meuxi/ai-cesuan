# 🚀 开发模式快速启动指南

本文档提供开发模式的快速启动步骤。

---

## 📋 前置要求

- **Python 3.8+**（推荐 3.10+）
- **Node.js 18+**（推荐 20+）
- **pnpm**（如果没有，会自动安装）

---

## 🎯 快速启动（自动脚本）

### Windows PowerShell

```powershell
# 在项目根目录执行
.\dev-start.ps1
```

### Windows 批处理

```cmd
# 在项目根目录执行
dev-start.bat
```

脚本会自动：
1. ✅ 检查 Python、Node.js、pnpm 环境
2. ✅ 创建 Python 虚拟环境（如果不存在）
3. ✅ 安装后端依赖
4. ✅ 安装前端依赖
5. ✅ 检查并创建 `.env` 文件
6. ✅ 可选择自动启动后端和前端服务

---

## 📝 手动启动步骤

### 1️⃣ 配置环境变量

创建 `.env` 文件（如果不存在）：

```bash
# Windows PowerShell
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

# Windows CMD
if not exist ".env" copy ".env.example" ".env"
```

**至少需要配置以下必填项：**

```env
# OpenAI API 密钥（必填）
api_key=sk-your-openai-api-key-here

# 可选：API 地址
api_base=https://api.openai.com/v1

# 可选：模型名称
model=gpt-3.5-turbo
```

### 2️⃣ 启动后端服务

打开**终端 1**（PowerShell 或 CMD）：

```powershell
# 进入项目根目录
cd C:\Users\UYU\Desktop\divination-main

# 激活虚拟环境
.\venv\Scripts\Activate.ps1    # PowerShell
# 或
venv\Scripts\activate.bat      # CMD

# 如果虚拟环境不存在，先创建
python -m venv venv

# 安装依赖（首次运行）
pip install -r requirements.txt

# 启动后端服务
python main.py
```

后端将在 **http://localhost:8000** 运行

### 3️⃣ 启动前端服务

打开**终端 2**（新的 PowerShell 或 CMD）：

```powershell
# 进入前端目录
cd C:\Users\UYU\Desktop\divination-main\frontend

# 安装依赖（首次运行）
pnpm install

# 启动前端开发服务器
pnpm dev
```

前端将在 **http://localhost:5173** 运行

---

## 🌐 访问应用

启动成功后，在浏览器中访问：

- **前端地址**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

---

## ⚙️ 开发模式配置说明

### Vite 代理配置

前端已配置代理，所有 `/api` 请求会自动转发到后端：

```typescript
// frontend/vite.config.ts
server: {
  proxy: {
    '/api': 'http://localhost:8000'
  }
}
```

### 环境变量

`.env` 文件配置说明：

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `api_key` | ✅ | - | OpenAI API 密钥 |
| `api_base` | ❌ | `https://api.openai.com/v1` | API 地址 |
| `model` | ❌ | `gpt-3.5-turbo` | 模型名称 |
| `jwt_secret` | ❌ | `secret` | JWT 密钥（开发环境可以使用默认值） |
| `enable_rate_limit` | ❌ | `true` | 是否启用速率限制 |

### 热重载

- **前端**: Vite 默认启用热模块替换（HMR），代码修改后自动刷新
- **后端**: 使用 `uvicorn` 的 `--reload` 参数可启用热重载（需要修改 `main.py`）

---

## 🐛 常见问题

### 1. Python 虚拟环境激活失败

**PowerShell 执行策略问题：**

```powershell
# 临时允许脚本执行
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后重新激活
.\venv\Scripts\Activate.ps1
```

### 2. pnpm 未安装

```bash
# 全局安装 pnpm
npm install -g pnpm
```

### 3. 端口被占用

如果 8000 或 5173 端口被占用：

**修改后端端口**（`main.py`）：
```python
uvicorn.run(app, host="0.0.0.0", port=8080)  # 改为 8080
```

**修改前端端口**（`frontend/vite.config.ts`）：
```typescript
server: {
  port: 3000,  // 改为 3000
  // ...
}
```

### 4. 依赖安装失败

**后端依赖：**
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**前端依赖：**
```bash
# 使用国内镜像源
pnpm config set registry https://registry.npmmirror.com
pnpm install
```

### 5. API Key 配置问题

- 确保 `.env` 文件在项目根目录
- 确保 `api_key` 格式正确（以 `sk-` 开头）
- 重启后端服务使环境变量生效

---

## 🔍 验证服务运行

### 检查后端服务

```bash
# 访问 API 文档
curl http://localhost:8000/docs

# 或浏览器访问
http://localhost:8000/docs
```

### 检查前端服务

```bash
# 访问前端页面
curl http://localhost:5173

# 或浏览器访问
http://localhost:5173
```

---

## 📚 开发提示

1. **前端代码修改**：保存后自动刷新，无需手动重启
2. **后端代码修改**：需要重启 `python main.py`
3. **查看日志**：后端日志会在终端输出
4. **调试模式**：可在浏览器开发者工具中查看网络请求和日志

---

## 🛑 停止服务

在各自的终端窗口中按 `Ctrl + C` 停止服务。

---

## 📖 更多信息

- 完整部署文档：查看 `README.md`
- 项目结构说明：查看 `README.md` 的项目结构部分
- API 文档：访问 http://localhost:8000/docs

---

**祝开发愉快！** 🎉
