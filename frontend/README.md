# AI 智能占卜 - 前端

基于 React + TypeScript + Vite 构建的现代化占卜应用前端。

## 技术栈

- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式**: Tailwind CSS + shadcn/ui
- **路由**: React Router v6
- **状态管理**: Zustand
- **国际化**: i18next
- **HTTP**: Fetch API + Server-Sent Events

## 开发环境

### 前置要求

- Node.js 18+
- pnpm (推荐) 或 npm

### 安装依赖

```bash
pnpm install
```

### 开发模式

```bash
pnpm dev
```

访问 `http://localhost:5173`

### 生产构建

```bash
pnpm build
```

构建产物在 `dist/` 目录。

### 类型检查

```bash
pnpm type-check
```

### 代码检查

```bash
pnpm lint
```

## 目录结构

```
src/
├── components/          # 可复用组件
│   ├── ui/             # shadcn/ui 基础组件
│   ├── ziwei/          # 紫微斗数相关组件
│   ├── tarot/          # 塔罗牌相关组件
│   └── ...
├── pages/              # 页面组件
│   ├── divination/     # 占卜功能页面
│   └── ...
├── hooks/              # 自定义 Hooks
│   ├── useDivination.ts
│   ├── useIztro.ts
│   └── ...
├── services/           # API 服务
│   ├── ziwei/          # 紫微斗数计算服务
│   └── ...
├── config/             # 配置文件
│   └── constants.ts    # 常量定义
├── i18n/               # 国际化资源
│   ├── zh.json
│   └── en.json
├── store/              # 状态管理
├── utils/              # 工具函数
├── types/              # TypeScript 类型定义
├── layouts/            # 布局组件
├── App.tsx             # 应用入口
└── main.tsx            # 渲染入口
```

## 环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
# API 基础地址（可选，默认使用相对路径）
VITE_API_BASE=

# 是否为 Tauri 桌面应用
VITE_IS_TAURI=

# 网站统计（可选）
VITE_ANALYTICS_BAIDU=
VITE_ANALYTICS_CLARITY=
```

## 添加新页面

1. 在 `src/pages/divination/` 创建页面组件
2. 在 `src/App.tsx` 添加路由
3. 在 `src/config/constants.ts` 的 `DIVINATION_OPTIONS` 添加配置
4. 在 `src/i18n/` 添加翻译

## 组件开发

本项目使用 [shadcn/ui](https://ui.shadcn.com/) 组件库。

添加新组件：

```bash
npx shadcn-ui@latest add button
```

## 样式规范

- 使用 Tailwind CSS 类名
- 遵循 shadcn/ui 的设计规范
- 支持暗色模式 (`dark:` 前缀)
- 响应式设计 (`sm:`, `md:`, `lg:` 前缀)

## License

MIT License
