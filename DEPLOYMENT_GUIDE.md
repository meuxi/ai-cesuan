# 🚀 部署和测试指南

## 📋 前置要求

在开始之前，请确保已安装以下软件：

### 必需软件
- **Node.js** 16+ ([下载地址](https://nodejs.org/))
- **Python** 3.8+ ([下载地址](https://www.python.org/))
- **pnpm** ([安装指南](https://pnpm.io/installation))

### 安装 pnpm

**Windows (PowerShell)**
```powershell
# 使用 npm 安装
npm install -g pnpm

# 或使用独立脚本
iwr https://get.pnpm.io/install.ps1 -useb | iex
```

**Linux/Mac**
```bash
# 使用 npm 安装
npm install -g pnpm

# 或使用 curl
curl -fsSL https://get.pnpm.io/install.sh | sh -
```

---

## 🔧 本地开发部署

### 1. 安装依赖

```bash
# 进入前端目录
cd frontend

# 安装前端依赖（包含新增的 html2canvas）
pnpm install

# 返回项目根目录
cd ..

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，至少配置：
# api_key=sk-your-openai-api-key-here
```

### 3. 构建前端

```bash
cd frontend
pnpm build --emptyOutDir
cd ..

# 复制构建产物到 dist 目录
# Windows PowerShell:
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
Copy-Item -Recurse frontend/dist dist

# Linux/Mac:
rm -rf dist
cp -r frontend/dist dist
```

### 4. 运行应用

```bash
# 运行后端服务
python main.py

# 访问 http://localhost:8000
```

---

## 🧪 功能测试清单

### ✅ 基础功能测试

- [ ] **首页加载**
  - 打开 http://localhost:8000
  - 检查骨架屏是否正常显示
  - 检查卡片动画是否流畅
  - 检查东方美学配色是否正确

- [ ] **占卜功能**
  - 测试塔罗牌占卜
  - 测试生辰八字占卜
  - 测试姓名五格占卜
  - 测试周公解梦占卜
  - 测试起名取名占卜
  - 测试梅花易数占卜
  - 测试姻缘占卜

### ✅ 新增功能测试

- [ ] **错误边界**
  - 故意触发错误（如修改代码）
  - 检查错误提示是否友好
  - 检查刷新按钮是否有效

- [ ] **离线提示**
  - 断开网络连接
  - 检查顶部是否显示离线提示
  - 恢复网络连接
  - 检查提示是否自动消失

- [ ] **结果复制功能**
  - 完成一次占卜
  - 点击"复制结果"按钮
  - 检查是否成功复制到剪贴板
  - 检查 Toast 提示是否显示

- [ ] **结果分享功能**
  - 完成一次占卜
  - 点击"分享"按钮
  - **移动端**：检查是否调用原生分享
  - **桌面端**：检查是否复制链接

- [ ] **导出图片功能**
  - 完成一次占卜
  - 点击"导出图片"按钮
  - 检查是否生成长图
  - 检查图片质量和样式
  - 检查文件名是否包含占卜类型

### ✅ UI/UX 测试

- [ ] **字体显示**
  - 检查中文字体是否为思源宋体
  - 检查标题字体是否为马善政楷书
  - 检查字体加载是否正常

- [ ] **配色方案**
  - 测试明亮主题（水墨白）
  - 测试暗黑主题（夜空墨）
  - 检查主色（朱砂红）是否正确
  - 检查辅色（青金石蓝/青瓷绿）是否正确

- [ ] **动画效果**
  - 检查卡片悬停动画
  - 检查按钮点击反馈
  - 检查页面过渡动画
  - 检查加载动画

- [ ] **响应式布局**
  - 测试手机屏幕（< 768px）
  - 测试平板屏幕（768px - 1024px）
  - 测试桌面屏幕（> 1024px）
  - 检查所有元素是否正常显示

### ✅ 兼容性测试

- [ ] **浏览器测试**
  - Chrome/Edge（推荐）
  - Firefox
  - Safari
  - 移动端浏览器

- [ ] **功能降级测试**
  - 不支持 clipboard API 的浏览器
  - 不支持 navigator.share 的浏览器
  - 检查是否有友好的降级方案

---

## 🐛 常见问题

### Q1: pnpm 命令不存在
**A**: 请先安装 pnpm：`npm install -g pnpm`

### Q2: 字体加载失败
**A**: 检查网络连接，字体从 Google Fonts CDN 加载

### Q3: 导出图片失败
**A**: 检查浏览器是否支持 html2canvas，建议使用最新版 Chrome

### Q4: 占卜失败
**A**: 检查 .env 文件中的 api_key 是否正确配置

### Q5: 样式显示异常
**A**: 清除浏览器缓存，重新构建前端

---

## 📦 生产环境部署

### Vercel 部署（推荐）

1. Fork 项目到你的 GitHub
2. 在 Vercel 导入项目
3. 配置环境变量（至少配置 api_key）
4. 点击部署

### Docker 部署

```bash
# 构建镜像
docker build -t ai-divination .

# 运行容器
docker run -d -p 8000:8000 \
  -e api_key=sk-xxx \
  -e api_base=https://api.openai.com/v1 \
  ai-divination
```

---

## 🎯 性能优化建议

### 前端优化
- 启用 Gzip 压缩
- 配置 CDN 加速
- 使用浏览器缓存

### 后端优化
- 配置 Redis 缓存
- 启用速率限制
- 使用负载均衡

---

## 📞 获取帮助

如遇到问题，请：
1. 查看 [OPTIMIZATION_SUMMARY.md](./OPTIMIZATION_SUMMARY.md) 了解优化详情
2. 查看 [README.md](./README.md) 了解基础配置
3. 提交 GitHub Issue

---

**祝您使用愉快！** 🎉

