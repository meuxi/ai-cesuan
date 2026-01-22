# AI 占卜 - ChatGPT Tarot Divination

基于 ChatGPT 的 AI 算命、占卜应用，支持多种占卜方式，提供流式输出体验和历史记录管理。

![demo](assets/demo.png)

## 功能列表

- [x] **塔罗牌占卜** - 通过塔罗牌探索内心，洞察未来可能性
- [x] **生辰八字** - 根据出生时间分析命理运势
- [x] **姓名五格** - 通过姓名笔画分析性格和命运
- [x] **周公解梦** - 解析梦境含义，探索潜意识
- [x] **起名取名** - 根据生辰八字和五行推荐吉祥名字
- [x] **梅花易数** - 传统易学占卜方法
- [x] **小六壬** - 简易掌诀占卜法
- [x] **姻缘占卜** - 分析感情运势和姻缘走向

**特色功能**：
- 🌊 流式输出 - AI 占卜结果以打字机效果实时呈现
- 📚 历史记录 - 每种占卜类型自动保存最近 10 条记录
- 📱 响应式设计 - 完美适配手机、平板、电脑
- 🌙 暗色模式 - 支持明暗主题切换
- 🎨 东方美学 - 朱砂红、青金石蓝配色 + 思源宋体
- 🛡️ 错误边界 - 防止应用崩溃
- 📤 结果导出 - 支持复制、分享、导出图片

---

## 🚀 快速开始

选择最适合你的部署方式：

| 方式 | 适用场景 | 难度 | 推荐指数 |
|------|----------|------|----------|
| [方式一：Vercel 一键部署](#方式一vercel-一键部署推荐⭐) | 快速体验，无需服务器 | ⭐☆☆☆☆ | ⭐⭐⭐⭐⭐ |
| [方式二：EXE 安装包](#方式二exe-安装包windows-用户) | Windows 桌面用户 | ⭐☆☆☆☆ | ⭐⭐⭐⭐☆ |
| [方式三：Docker 部署](#方式三docker-部署) | 已有 Docker 环境 | ⭐⭐☆☆☆ | ⭐⭐⭐☆☆ |
| [方式四：本地运行（开发者）](#方式四本地运行开发者) | 开发调试、自定义修改 | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ |

---

## 📋 详细部署指南

### 方式一：Vercel 一键部署（推荐）⭐

最简单快捷的部署方式，无需服务器，完全免费。

1. 点击下方按钮开始部署：

   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fmeuxi%2Fai-cesuan&env=api_key,api_base&project-name=ai-cesuan&repository-name=ai-cesuan&demo-title=AI%20Divination&demo-description=AI%20Divination&demo-url=https%3A%2F%2Fcesuan.meuxi.com%2F)

2. 在部署时配置环境变量：
   - `api_key`：**必填**，你的 OpenAI API Key
   - `api_base`：可选，API 地址（默认为 OpenAI 官方地址）
   - `model`：可选，模型名称（默认 gpt-3.5-turbo）
   - `github_client_id`：可选，GitHub OAuth 客户端 ID
   - `github_client_secret`：可选，GitHub OAuth 客户端密钥
   - `jwt_secret`：可选，JWT 密钥（建议设置强密码）
   - `ad_client`：可选，Google AdSense 客户端 ID
   - `ad_slot`：可选，Google AdSense 广告位 ID

   > 💡 **提示**：更多环境变量配置请参考项目根目录的 `.env.example` 文件

3. 部署完成后，Vercel 会自动分配一个访问域名

4. 也可以绑定自己的域名

### 方式二：EXE 安装包（Windows 用户）

1. [点击下载 EXE 安装包](https://github.com/dreamhunter2333/chatgpt-tarot-divination/releases/tag/latest)
2. 安装并运行程序
3. 在设置中配置：
   - API BASE URL（OpenAI API 地址）
   - API KEY（你的 API 密钥）
4. 返回主页即可开始使用

### 方式三：Docker 部署

创建 `docker-compose.yml` 文件：

```yaml
services:
  chatgpt-tarot-divination:
    image: ghcr.io/dreamhunter2333/chatgpt-tarot-divination:latest
    container_name: chatgpt-tarot-divination
    restart: always
    ports:
      - 8000:8000
    environment:
      - api_key=sk-xxx                    # 必填：OpenAI API Key
      # - api_base=https://api.openai.com/v1  # 可选：API 地址
      # - model=gpt-3.5-turbo              # 可选：模型名称
      # - rate_limit=10/minute             # 可选：速率限制
      # - user_rate_limit=600/hour         # 可选：用户速率限制
      - github_client_id=xxx               # 可选：GitHub OAuth
      - github_client_secret=xxx           # 可选：GitHub OAuth
      - jwt_secret=secret                  # 可选：JWT 密钥
      - ad_client=ca-pub-xxx               # 可选：广告客户端
      - ad_slot=123                        # 可选：广告位
```

启动服务：

```bash
docker-compose up -d
```

访问 `http://localhost:8000` 即可使用。

### 方式四：本地运行（开发者）

**前置要求**：
- Node.js 16+（推荐 18+）
- Python 3.8+（推荐 3.10+）
- pnpm（快速安装：`npm install -g pnpm`）

#### 🛠️ 完整部署步骤

**1. 克隆项目**
```bash
git clone https://github.com/meuxi/ai-cesuan.git
cd ai-cesuan
```

**2. 配置环境变量**
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑 .env 文件，至少需要配置以下必填项：
# api_key=sk-your-openai-api-key-here
```

**3. 安装前端依赖**
```bash
cd frontend
pnpm install
```

**4. 构建前端**
```bash
# 生产环境构建
pnpm build --emptyOutDir
cd ..
```

**5. 部署前端文件**
```bash
# Linux/Mac
rm -r dist
cp -r frontend/dist/ dist

# Windows PowerShell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Copy-Item -Recurse frontend/dist dist
```

**6. 安装并运行后端**
```bash
# 创建虚拟环境（可选，推荐）
python3 -m venv ./venv

# 激活虚拟环境
# Linux/Mac:
source ./venv/bin/activate
# Windows:
.\venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python main.py
```

**7. 访问应用**
打开浏览器访问 `http://localhost:8000`

#### 🔧 开发模式（热重载）

如果需要修改代码，建议使用开发模式：

**终端1：运行前端开发服务器**
```bash
cd frontend
pnpm dev
```
前端将在 `http://localhost:5173` 运行（默认端口）

**终端2：运行后端API服务器**
```bash
# 确保在项目根目录
python main.py
```
后端将在 `http://localhost:8000` 运行

**配置前端代理**
修改 `frontend/vite.config.ts`，添加代理配置：
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

#### ⚙️ 环境变量说明

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `api_key` | ✅ | - | OpenAI API 密钥 |
| `api_base` | ❌ | `https://api.openai.com/v1` | OpenAI API 地址 |
| `model` | ❌ | `gpt-3.5-turbo` | 使用的模型名称 |
| `github_client_id` | ❌ | - | GitHub OAuth 客户端 ID |
| `github_client_secret` | ❌ | - | GitHub OAuth 客户端密钥 |
| `jwt_secret` | ❌ | `secret` | JWT 密钥（生产环境务必修改） |
| `enable_rate_limit` | ❌ | `true` | 是否启用速率限制 |
| `rate_limit` | ❌ | `60,3600` | 未登录用户速率限制（次数,秒） |
| `user_rate_limit` | ❌ | `600,3600` | 已登录用户速率限制（次数,秒） |
| `cache_client_type` | ❌ | `memory` | 缓存类型：memory 或 redis |
| `ad_client` | ❌ | - | Google AdSense 客户端 ID |
| `ad_slot` | ❌ | - | Google AdSense 广告位 ID |

> 📖 **详细配置说明**：请查看 `.env.example` 文件中的注释

---

## 🧪 测试指南

### 快速测试（无需 OpenAI API Key）

如果你想先测试界面和基本功能：

1. 在 `.env` 文件中设置一个虚拟的 `api_key`：
   ```
   api_key=sk-test-1234567890
   ```

2. 运行应用后，占卜功能会因 API Key 无效而失败，但可以：
   - 测试所有页面的加载和渲染
   - 测试响应式布局
   - 测试主题切换
   - 测试历史记录功能（本地存储）

3. 如果需要完整功能测试，请申请有效的 OpenAI API Key

### 单元测试

项目包含基本的测试框架：

```bash
# 运行 Python 测试
pytest

# 运行前端测试
cd frontend
pnpm test
```

---

## 🔍 常见问题

### 1. 如何获取 OpenAI API Key？
访问 [OpenAI Platform](https://platform.openai.com/api-keys) 创建 API Key。

### 2. 支持哪些 OpenAI 模型？
默认支持 gpt-3.5-turbo，也可配置为 gpt-4、gpt-4-turbo 等。

### 3. 如何修改端口？
修改 `main.py` 中的 `uvicorn.run` 参数：
```python
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### 4. 如何启用 Redis 缓存？
1. 安装并运行 Redis
2. 在 `.env` 中设置：
   ```
   cache_client_type=redis
   redis_url=redis://localhost:6379/0
   ```

### 5. 如何贡献代码？
欢迎提交 Pull Request！请确保：
- 代码符合现有风格
- 添加必要的测试
- 更新相关文档

---

## 📁 项目结构

```
divination-main/
├── frontend/              # React + Vite 前端
│   ├── src/
│   │   ├── components/    # 通用组件
│   │   ├── pages/        # 页面组件
│   │   ├── layouts/      # 布局组件
│   │   └── utils/        # 工具函数
│   └── package.json
├── src/                  # FastAPI 后端
│   ├── cache/           # 缓存实现
│   ├── divination/      # 占卜算法
│   ├── models.py        # 数据模型
│   └── app.py           # 主应用
├── requirements.txt     # Python 依赖
├── main.py             # 入口文件
├── Dockerfile          # Docker 配置
└── README.md           # 本文档
```

---

## 📄 相关文档

- [QUICK_START.md](./QUICK_START.md) - 快速开始指南
- [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - 详细部署指南
- [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) - 优化总结
- [AGENTS.md](./AGENTS.md) - AI 代理配置

---

## 🤝 贡献

欢迎任何形式的贡献！包括但不限于：
- 报告 Bug
- 提出新功能
- 改进文档
- 提交代码

请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)（如有）了解详情。

---

## 📜 许可证

MIT License © 2024 [Meuxi](https://github.com/meuxi)

---

## 🌟 致谢

- [OpenAI](https://openai.com) - 提供强大的 AI 能力
- [FastAPI](https://fastapi.tiangolo.com) - 高性能 Python Web 框架
- [React](https://reactjs.org) - 前端 UI 库
- [Vercel](https://vercel.com) - 优秀的部署平台

---

**提示**：本项目仅供娱乐和学习使用，占卜结果请勿过度依赖。保持理性，享受科技带来的乐趣！