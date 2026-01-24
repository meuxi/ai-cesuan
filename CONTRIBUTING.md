# 贡献指南

感谢您对本项目的关注！欢迎提交 Issue 和 Pull Request。

## 如何贡献

### 报告 Bug

1. 在 [Issues](../../issues) 中搜索是否已有相同问题
2. 如果没有，创建新 Issue，包含：
   - 问题描述
   - 复现步骤
   - 期望行为
   - 实际行为
   - 环境信息（浏览器、操作系统等）

### 功能建议

1. 在 [Issues](../../issues) 中创建 Feature Request
2. 描述您期望的功能及使用场景

### 提交代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发规范

### 代码风格

**前端 (TypeScript/React)**:
- 使用 ESLint + Prettier 格式化
- 组件使用函数式组件 + Hooks
- 文件命名：组件用 PascalCase，工具函数用 camelCase

**后端 (Python)**:
- 使用 flake8 检查
- 遵循 PEP 8 规范
- 类型注解

### 提交信息

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat(ziwei): add flying star analysis feature

Add palace stem click to show flying star targets
Support both click lock and hover preview modes
```

### 分支命名

- `feature/*` - 新功能
- `fix/*` - Bug 修复
- `docs/*` - 文档更新
- `refactor/*` - 重构

## 本地开发

### 环境准备

```bash
# 克隆项目
git clone https://github.com/meuxi/ai-cesuan.git
cd ai-divination

# 后端
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置 API Key

# 前端
cd frontend
pnpm install
cp .env.example .env
```

### 运行项目

```bash
# 后端（在项目根目录）
python main.py

# 前端（新终端，在 frontend 目录）
pnpm dev
```

### 测试

```bash
# 前端类型检查
cd frontend
pnpm type-check

# 前端代码检查
pnpm lint
```

## 项目结构

```
├── frontend/           # 前端代码
│   ├── src/
│   │   ├── components/ # UI 组件
│   │   ├── pages/      # 页面
│   │   ├── hooks/      # Hooks
│   │   ├── services/   # 服务
│   │   └── ...
│   └── ...
├── src/                # 后端代码
│   ├── divination/     # 占卜算法
│   ├── prompts/        # AI 提示词
│   ├── ai/             # AI 服务
│   └── ...
└── ...
```

## 添加新的占卜功能

1. **后端算法** (`src/divination/`)
   - 创建新的算法模块
   - 在 `__init__.py` 注册

2. **AI 提示词** (`src/prompts/`)
   - 添加专业的占卜提示词
   - 定义输出框架

3. **前端页面** (`frontend/src/pages/divination/`)
   - 创建页面组件
   - 实现用户交互

4. **路由配置** (`frontend/src/App.tsx`)
   - 添加页面路由

5. **功能配置** (`frontend/src/config/constants.ts`)
   - 在 `DIVINATION_OPTIONS` 添加配置

6. **国际化** (`frontend/src/i18n/`)
   - 添加中英文翻译

## 问题反馈

如有疑问，请在 [Discussions](../../discussions) 中讨论。

再次感谢您的贡献！
