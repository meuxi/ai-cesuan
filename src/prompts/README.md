# 玄学AI提示词系统 v1.0

> 专业化、模块化、工程化的玄学AI提示词系统

---

## 📁 目录结构

```
src/prompts/
├── README.md                           # 本文档
├── PROMPT_DESIGN_SPECIFICATION.md      # 提示词设计规范与术语库（总纲）
├── USAGE_EXAMPLES.md                   # 使用示例文档（新增）
├── models.py                           # 数据模型定义
├── templates.py                        # 内置模板（Python版）
├── output_control.py                   # 输出控制模块
├── manager.py                          # 模板管理器
│
├── professional/                       # 专业化模板文档
│   ├── bazi_template.md               # 八字命理专业模板
│   ├── ziwei_template.md              # 紫微斗数专业模板
│   ├── liuyao_template.md             # 六爻预测专业模板
│   ├── xiaoliu_template.md            # 小六壬专业模板
│   ├── dream_template.md              # 周公解梦专业模板
│   ├── zodiac_template.md             # 星座运势专业模板
│   ├── tarot_template.md              # 塔罗牌专业模板
│   ├── qimen_template.md              # 奇门遁甲专业模板
│   ├── meihua_template.md             # 梅花易数专业模板
│   ├── daliuren_template.md           # 大六壬专业模板
│   ├── name_template.md               # 姓名测算专业模板
│   ├── chouqian_template.md           # 抽签解签专业模板
│   └── hehun_template.md              # 八字合婚专业模板
│
└── config/                             # TypeScript配置代码
    ├── index.ts                        # 导出索引
    └── promptConfig.ts                 # 核心配置文件
```

---

## 🚀 快速开始

### 安装与导入

```typescript
import { 
  DivinationType, 
  buildPrompt, 
  validateOutputFormat,
  PROMPT_TEMPLATES
} from '@/prompts/config';
```

### 基础使用

```typescript
// 1. 构建提示词
const { systemPrompt, userPrompt } = buildPrompt(DivinationType.BAZI, {
  gender: '男',
  birthDatetime: '1990年5月15日 14:30',
  yearPillar: '庚午',
  monthPillar: '辛巳',
  dayPillar: '甲子',
  hourPillar: '辛未',
  dayMaster: '甲木',
  strength: '偏弱',
  yongshen: '水木',
  xishen: '金',
  jishen: '火土',
  currentDayun: '壬申',
  userQuestion: '今年事业发展如何？'
});

// 2. 调用AI（以OpenAI为例）
const response = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userPrompt }
  ],
  stream: true
});

// 3. 验证输出格式
const validation = validateOutputFormat(fullResponse);
console.log('格式验证:', validation);
```

---

## 📋 支持的占卜类型

| 类型 | 枚举值 | 中文名 | 状态 |
|------|--------|--------|------|
| `BAZI` | bazi | 八字命理 | ✅ 完整 |
| `ZIWEI` | ziwei | 紫微斗数 | ✅ 完整 |
| `LIUYAO` | liuyao | 六爻预测 | ✅ 完整 |
| `XIAOLIU` | xiaoliu | 小六壬 | ✅ 完整 |
| `DREAM` | dream | 周公解梦 | ✅ 完整 |
| `ZODIAC` | zodiac | 星座运势 | ✅ 完整 |
| `TAROT` | tarot | 塔罗牌 | ✅ 完整 |
| `QIMEN` | qimen | 奇门遁甲 | ✅ 完整 |
| `MEIHUA` | meihua | 梅花易数 | ✅ 完整 |
| `NAME` | name | 姓名测算 | ✅ 完整 |
| `CHOUQIAN` | chouqian | 抽签解签 | ✅ 完整 |
| `HEHUN` | hehun | 八字合婚 | ✅ 完整 |
| `DALIUREN` | daliuren | 大六壬 | ✅ 完整 |

---

## 🔧 核心API

### `buildPrompt(type, inputData)`

构建完整的提示词。

```typescript
function buildPrompt(
  type: DivinationType,
  inputData: DivinationInputData
): { systemPrompt: string; userPrompt: string }
```

### `replaceVariables(template, variables)`

安全地替换模板中的变量。

```typescript
function replaceVariables(
  template: string, 
  variables: Record<string, unknown>
): string
```

### `validateOutputFormat(output)`

验证AI输出是否符合格式规范。

```typescript
function validateOutputFormat(output: string): FormatCheckResult

interface FormatCheckResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}
```

---

## 🎯 确保AI遵守格式的策略

### 1. 系统消息首行约束

在所有系统提示词的**最前面**添加格式约束指令：

```typescript
export const FORMAT_CONSTRAINT_INSTRUCTION = `
【格式强制约束 - 必须遵守】
你的输出必须严格遵循以下规范，违反将被视为无效响应：

1. **结构规范**：必须使用Markdown，必须包含核心结论
2. **量化规范**：必须包含评分（0-100分）和概率
3. **引用规范**：重要论断必须引用经典依据
4. **收尾规范**：必须以箴言结尾，附加免责提示
...
`;
```

### 2. 输出结构模板化

在用户提示词末尾明确输出结构：

```markdown
请按以下结构输出：
## 🔯 八字命理专业解析
### 【核心结论】（含评分）
### 【格局分析】
...
「命运箴言」
```

### 3. 后端格式校验

使用 `validateOutputFormat()` 函数在流式输出完成后验证格式：

```typescript
const validation = validateOutputFormat(fullResponse);
if (!validation.isValid) {
  // 记录日志或触发重试
  console.warn('格式不符合规范:', validation.errors);
}
```

### 4. 前端Markdown渲染

确保前端正确渲染Markdown：

```tsx
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

<ReactMarkdown remarkPlugins={[remarkGfm]}>
  {aiResponse}
</ReactMarkdown>
```

---

## 📚 设计规范要点

详见 `PROMPT_DESIGN_SPECIFICATION.md`，核心原则：

1. **结论先行**：核心判断在前200字内
2. **引经据典**：`**《典籍名》曰**："引文"`
3. **量化评估**：评分0-100，概率0-100%
4. **时间明确**：预测具体到年月
5. **正向收尾**：箴言 + 免责提示

---

## 🔄 版本记录

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0.0 | 2025-01-25 | 初版发布：规范文档、6个专业模板、TS配置代码 |
| v1.1.0 | 2025-01-25 | 完善7个专业模板（塔罗牌、奇门遁甲、梅花易数、大六壬、姓名测算、抽签解签、八字合婚），补全TypeScript配置占位符 |

---

## 📞 维护信息

- **维护团队**：玄机子AI团队
- **更新周期**：每季度审核一次
- **反馈渠道**：提交Issue或PR
