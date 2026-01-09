# AI占卜系统 - 优化修复方案

> 生成时间：2026-01-09
> 分析范围：前端(React+Vite) + 后端(FastAPI)

---

## 一、P0-安全风险（需立即修复）

### 1.1 XSS风险 - dangerouslySetInnerHTML

| 项目 | 内容 |
|------|------|
| **文件** | `frontend/src/components/ResultDrawer.tsx:98` |
| **风险等级** | 🔴 高 |
| **问题描述** | 使用`dangerouslySetInnerHTML`渲染AI返回内容，可能被注入恶意脚本 |
| **修复方案** | 安装DOMPurify库，对HTML进行净化 |

```bash
# 安装依赖
cd frontend && pnpm add dompurify @types/dompurify
```

```tsx
// 修复代码
import DOMPurify from 'dompurify'

// 原代码
dangerouslySetInnerHTML={{ __html: result }}

// 修复后
dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(result) }}
```

---

### 1.2 JWT密钥默认值不安全

| 项目 | 内容 |
|------|------|
| **文件** | `src/config.py:23` |
| **风险等级** | 🔴 高 |
| **问题描述** | jwt_secret默认值为"secret"，易被暴力破解 |
| **修复方案** | 添加启动时检测，生产环境强制要求配置 |

```python
# 修复代码 - 在settings类中添加验证
from pydantic import validator

@validator('jwt_secret')
def validate_jwt_secret(cls, v):
    if v == 'secret' and os.getenv('VERCEL') == '1':
        raise ValueError('生产环境必须配置安全的JWT_SECRET')
    return v
```

---

### 1.3 CORS配置过于宽松

| 项目 | 内容 |
|------|------|
| **文件** | `src/app.py:17-23` |
| **风险等级** | 🟠 中 |
| **问题描述** | `allow_origins=["*"]`允许所有来源 |
| **修复方案** | 根据环境变量配置允许的域名 |

```python
# 修复代码
import os

# 根据环境配置CORS
if os.getenv("VERCEL") == "1":
    # 生产环境：限制允许的域名
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    if not allowed_origins or allowed_origins == [""]:
        allowed_origins = ["https://your-domain.vercel.app"]
else:
    # 开发环境：允许所有
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 二、P1-性能瓶颈（严重影响体验）

### 2.1 XiaoLiuRenPage组件过大

| 项目 | 内容 |
|------|------|
| **文件** | `frontend/src/pages/divination/XiaoLiuRenPage.tsx` |
| **问题描述** | 单文件1056行，包含数据+逻辑+UI，加载慢、难维护 |
| **优化方案** | 拆分为多个独立模块 |

**拆分结构：**

```
frontend/src/pages/divination/xiaoliu/
├── index.tsx              # 主页面（入口）
├── data/
│   └── interpretations.ts # 解读库数据
├── components/
│   ├── SixGrid.tsx        # 六宫格组件
│   ├── Interpretation.tsx # 卦象解读组件
│   ├── Steps.tsx          # 起课步骤组件
│   ├── CellModal.tsx      # 详情弹窗组件
│   └── AlertModal.tsx     # 提示弹窗组件
├── hooks/
│   └── useXiaoLiuRen.ts   # 计算逻辑Hook
└── types.ts               # 类型定义
```

---

### 2.2 内存缓存优化

| 项目 | 内容 |
|------|------|
| **文件** | `src/cache/memory_client.py` |
| **问题描述** | 纯内存缓存，服务重启数据丢失 |
| **优化方案** | 生产环境推荐使用Redis |

```python
# 已有maxsize限制，建议生产环境配置Redis
# .env 配置
cache_client_type=redis
KV_REST_API_URL=https://your-upstash-redis
KV_REST_API_TOKEN=your-token
```

---

## 三、P2-代码质量（近期优化）

### 3.1 TypeScript any类型

| 文件 | 位置 | 修复方案 |
|------|------|----------|
| App.tsx | Line 54 | 定义Error接口 |
| useDivination.ts | Line 104 | 定义params类型 |
| XiaoLiuRenPage.tsx | Line 138-139 | 添加lunar类型声明 |

```typescript
// 示例：为lunar-javascript添加类型声明
// frontend/src/types/lunar.d.ts
declare module 'lunar-javascript' {
  export class Solar {
    static fromYmdHms(y: number, m: number, d: number, h: number, mi: number, s: number): Solar
    getLunar(): Lunar
  }
  export class Lunar {
    getMonth(): number
    getDay(): number
    getYearGan(): string
    getYearZhi(): string
    // ...
  }
}
```

---

### 3.2 清理console.log

**受影响文件（17处）：**

- `utils/divinationHistory.ts` (5处)
- `hooks/index.ts` (2处)
- `hooks/useDivination.ts` (2处)
- `pages/Login.tsx` (2处)
- 其他6个文件各1处

**修复方案：**

```bash
# 方案1：手动清理
# 搜索并删除所有console.log

# 方案2：使用vite插件自动移除
# vite.config.ts
export default defineConfig({
  esbuild: {
    drop: process.env.NODE_ENV === 'production' ? ['console', 'debugger'] : []
  }
})
```

---

### 3.3 清理CSS空规则集

**文件：** `frontend/src/pages/divination/xiaoliu-ren.css`

**位置：** 710、775、777、791、1113行

**修复：** 删除空的CSS规则集

---

## 四、P3-最佳实践（长期改进）

### 4.1 添加单元测试

```bash
# 安装测试框架
cd frontend && pnpm add -D vitest @testing-library/react @testing-library/jest-dom

# 后端
pip install pytest pytest-asyncio httpx
```

**优先测试：**

1. 小六壬计算逻辑
2. API请求处理
3. 速率限制逻辑

---

### 4.2 错误边界细化

为每个占卜页面添加独立的错误边界，避免一个模块崩溃影响整体。

---

### 4.3 API响应格式统一

```python
# 统一响应格式
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    code: int = 200
```

---

## 五、执行优先级

| 优先级 | 任务 | 预计耗时 | 状态 |
|--------|------|----------|------|
| 1 | XSS修复（DOMPurify） | 10分钟 | ✅ 已完成 |
| 2 | CORS优化 | 15分钟 | ✅ 已完成 |
| 3 | JWT验证增强 | 10分钟 | ✅ 已完成 |
| 4 | CSS空规则清理 | 5分钟 | ✅ 已完成 |
| 5 | console.log清理配置 | 10分钟 | ✅ 已完成 |
| 6 | 组件拆分（可选） | 2小时 | ⚠️ 高风险，暂不执行 |

---

## 六、验证清单

修复完成后需验证：

- [ ] AI解读功能正常
- [ ] 弹窗居中显示
- [ ] 移动端适配正常
- [ ] 无事不起卦验证有效
- [ ] 生产构建无错误
