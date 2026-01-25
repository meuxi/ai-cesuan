# 提示词系统使用指南

> 本文档提供提示词系统的完整使用示例

---

## 一、Python 端使用

### 1.1 基础使用 - 获取模板

```python
from src.prompts import get_prompt_manager, PromptCategory

# 获取全局管理器
manager = get_prompt_manager()

# 获取指定模板
template = manager.get_template("bazi_analysis")
if template:
    print(f"模板名称: {template.name}")
    print(f"系统提示词: {template.system_prompt}")
    print(f"用户提示词模板: {template.user_prompt_template}")
```

### 1.2 渲染模板 - 替换变量

```python
from src.prompts import get_prompt_manager

manager = get_prompt_manager()

# 准备变量
variables = {
    "gender": "男",
    "birth_datetime": "1990年5月15日 14:30",
    "year_pillar": "庚午",
    "month_pillar": "辛巳",
    "day_pillar": "甲子",
    "hour_pillar": "辛未",
    "day_master": "甲木",
    "strength": "偏弱",
    "yongshen": "水木",
    "xishen": "金",
    "jishen": "火土",
}

# 渲染模板
rendered = manager.render_template("bazi_analysis", variables)
print(f"系统提示词: {rendered['system_prompt']}")
print(f"用户提示词: {rendered['user_prompt']}")
```

### 1.3 结合输出控制

```python
from src.prompts import get_prompt_manager
from src.prompts.output_control import enhance_prompt_with_length_control, get_tool_framework

manager = get_prompt_manager()

# 获取模板
template = manager.get_template("bazi_analysis")

# 渲染模板
variables = {"gender": "男", "birth_datetime": "1990年5月15日", ...}
rendered = manager.render_template("bazi_analysis", variables)

# 增强提示词（添加输出框架和字数控制）
enhanced_user_prompt = enhance_prompt_with_length_control(
    rendered["user_prompt"], 
    mode="detailed",
    tool_name="bazi_analysis"
)

# 现在可以用于 AI 调用
system_prompt = rendered["system_prompt"]
user_prompt = enhanced_user_prompt
```

### 1.4 完整的占卜服务示例

```python
"""
示例：八字分析服务的完整实现
"""
from typing import Tuple, Dict, Any
from src.prompts import get_prompt_manager
from src.prompts.output_control import enhance_prompt_with_length_control


class BaziAnalysisService:
    """八字分析服务"""
    
    TEMPLATE_ID = "bazi_analysis"
    
    def __init__(self):
        self.manager = get_prompt_manager()
    
    def build_prompt(self, bazi_data: Dict[str, Any]) -> Tuple[str, str]:
        """
        构建八字分析提示词
        
        Args:
            bazi_data: 八字数据，包含 gender, birth_datetime, sizhu 等
        
        Returns:
            (user_prompt, system_prompt) 元组
        """
        # 准备变量
        variables = {
            "gender": bazi_data.get("gender", "男"),
            "birth_datetime": bazi_data.get("birth_datetime", ""),
            "year_pillar": bazi_data.get("sizhu", {}).get("year", ""),
            "month_pillar": bazi_data.get("sizhu", {}).get("month", ""),
            "day_pillar": bazi_data.get("sizhu", {}).get("day", ""),
            "hour_pillar": bazi_data.get("sizhu", {}).get("hour", ""),
            "day_master": bazi_data.get("day_master", ""),
            "strength": bazi_data.get("strength", ""),
            "yongshen": bazi_data.get("yongshen", ""),
            "xishen": bazi_data.get("xishen", ""),
            "jishen": bazi_data.get("jishen", ""),
        }
        
        # 获取模板并渲染
        template = self.manager.get_template(self.TEMPLATE_ID)
        if not template:
            raise ValueError(f"模板 {self.TEMPLATE_ID} 不存在")
        
        rendered = template.render(variables)
        
        # 增强用户提示词（添加输出框架）
        enhanced_user_prompt = enhance_prompt_with_length_control(
            rendered["user_prompt"],
            tool_name=self.TEMPLATE_ID
        )
        
        return enhanced_user_prompt, rendered["system_prompt"]
    
    async def analyze(self, bazi_data: Dict[str, Any], ai_client) -> str:
        """
        执行八字分析
        
        Args:
            bazi_data: 八字数据
            ai_client: AI 客户端
        
        Returns:
            AI 分析结果
        """
        user_prompt, system_prompt = self.build_prompt(bazi_data)
        
        # 调用 AI
        response = await ai_client.chat(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            stream=True
        )
        
        return response
```

---

## 二、按分类获取最佳模板

```python
from src.prompts import get_prompt_manager, PromptCategory

manager = get_prompt_manager()

# 获取八字分类下效果最好的模板
best_bazi_template = manager.get_best(PromptCategory.BAZI)
if best_bazi_template:
    print(f"最佳八字模板: {best_bazi_template.name}")
    print(f"效果评分: {best_bazi_template.effectiveness_score}")

# 获取某分类下所有激活的模板
active_liuyao_templates = manager.get_active(PromptCategory.LIUYAO)
for t in active_liuyao_templates:
    print(f"- {t.name}: {t.effectiveness_score}分")
```

---

## 三、模板 ID 对照表

| 模板ID | 工具名称 | 分类 |
|--------|----------|------|
| `bazi_analysis` | 八字命理分析 | BAZI |
| `birthday_divination` | 生辰八字分析 | BAZI |
| `liuyao_analysis` | 六爻卦象解读 | LIUYAO |
| `tarot_reading` | 塔罗牌解读 | TAROT |
| `tarot_divination` | 塔罗牌占卜 | TAROT |
| `xiaoliu_analysis` | 小六壬解读 | XIAOLIU |
| `xiaoliu_divination` | 小六壬占卜 | XIAOLIU |
| `ziwei_divination` | 紫微斗数 | ZIWEI |
| `dream_divination` | 周公解梦 | DREAM |
| `name_divination` | 姓名测算 | NAME |
| `new_name_divination` | 起名服务 | NEW_NAME |
| `plum_flower_divination` | 梅花易数 | MEIHUA |
| `qimen_divination` | 奇门遁甲 | QIMEN |
| `daliuren_divination` | 大六壬 | DALIUREN |
| `hehun_divination` | 八字合婚 | HEHUN |
| `chouqian_analysis` | 抽签解读 | CHOUQIAN |
| `zhuge_divination` | 诸葛神算 | ZHUGE |
| `life_kline_analysis` | 人生K线图 | LIFE_KLINE |
| `daily_fortune` | 每日运势 | FORTUNE |
| `weekly_fortune` | 每周运势 | FORTUNE |
| `monthly_fortune` | 每月运势 | FORTUNE |
| `zodiac_fortune` | 星座运势 | ZODIAC |
| `fate_divination` | 缘分测算 | FATE |
| `palmistry_divination` | 手相分析 | GENERAL |

---

## 四、TypeScript 端使用（前端或Node.js）

### 4.1 导入和构建提示词

```typescript
import { 
  DivinationType, 
  buildPrompt, 
  validateOutputFormat,
  PROMPT_TEMPLATES 
} from '@/prompts/config';

// 构建八字分析提示词
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

console.log('系统提示词:', systemPrompt);
console.log('用户提示词:', userPrompt);
```

### 4.2 调用 OpenAI API

```typescript
import OpenAI from 'openai';
import { DivinationType, buildPrompt, validateOutputFormat } from '@/prompts/config';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function analyzeBazi(inputData: BaziInputData): Promise<string> {
  // 1. 构建提示词
  const { systemPrompt, userPrompt } = buildPrompt(DivinationType.BAZI, inputData);
  
  // 2. 调用 AI（流式输出）
  const stream = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ],
    stream: true
  });
  
  // 3. 收集响应
  let fullResponse = '';
  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || '';
    fullResponse += content;
    process.stdout.write(content); // 实时输出
  }
  
  // 4. 验证输出格式
  const validation = validateOutputFormat(fullResponse);
  if (!validation.isValid) {
    console.warn('格式警告:', validation.errors);
  }
  if (validation.warnings.length > 0) {
    console.warn('格式建议:', validation.warnings);
  }
  
  return fullResponse;
}
```

### 4.3 React 组件中使用

```tsx
import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { DivinationType, buildPrompt } from '@/prompts/config';

interface BaziAnalysisProps {
  inputData: BaziInputData;
}

export const BaziAnalysis: React.FC<BaziAnalysisProps> = ({ inputData }) => {
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleAnalyze = async () => {
    setLoading(true);
    setResponse('');
    
    const { systemPrompt, userPrompt } = buildPrompt(DivinationType.BAZI, inputData);
    
    // 调用后端 API 进行流式分析
    const eventSource = new EventSource(`/api/bazi/analyze?...`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setResponse(prev => prev + data.content);
    };
    
    eventSource.onerror = () => {
      eventSource.close();
      setLoading(false);
    };
  };
  
  return (
    <div>
      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? '分析中...' : '开始分析'}
      </button>
      
      {/* 使用 Markdown 渲染 AI 响应 */}
      <div className="markdown-body">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {response}
        </ReactMarkdown>
      </div>
    </div>
  );
};
```

---

## 五、输出框架对照表

| 工具 | 框架变量 | 说明 |
|------|----------|------|
| 八字分析 | `BAZI_FRAMEWORK` | 包含命盘、结论、五行、大运等 |
| 六爻预测 | `LIUYAO_FRAMEWORK` | 包含卦象、用神、应期等 |
| 塔罗牌 | `TAROT_FRAMEWORK` | 包含牌面、解读、建议等 |
| 紫微斗数 | `ZIWEI_FRAMEWORK` | 包含命盘、十二宫、大限等 |
| 小六壬 | `XIAOLIU_FRAMEWORK` | 包含三宫、五行、行动指南等 |
| 周公解梦 | `DREAM_FRAMEWORK` | 包含要素、解析、指引等 |
| 姓名测算 | `NAME_FRAMEWORK` | 包含五格、三才、建议等 |
| 梅花易数 | `MEIHUA_FRAMEWORK` | 包含体用、卦象、应期等 |
| 奇门遁甲 | `QIMEN_FRAMEWORK` | 包含盘局、格局、策略等 |
| 八字合婚 | `HEHUN_FRAMEWORK` | 包含双方信息、配合分析等 |
| 抽签解读 | `CHOUQIAN_FRAMEWORK` | 包含签文、解读、宜忌等 |
| 诸葛神算 | `ZHUGE_FRAMEWORK` | 包含签诗、解读、锦囊等 |

---

## 六、最佳实践

### 6.1 确保 AI 遵守格式的三重保障

1. **系统消息首行约束**：`FORMAT_CONSTRAINT_INSTRUCTION` 放在系统提示词最前面
2. **输出结构模板化**：用户提示词末尾明确输出结构
3. **后端格式校验**：使用 `validateOutputFormat()` 验证

### 6.2 处理变量缺失

```python
def safe_render(template_id: str, variables: dict) -> dict:
    """安全渲染模板，处理缺失变量"""
    manager = get_prompt_manager()
    template = manager.get_template(template_id)
    
    if not template:
        return {"system_prompt": "", "user_prompt": ""}
    
    # 为缺失变量提供默认值
    required_vars = template.variables
    for var in required_vars:
        if var not in variables:
            variables[var] = ""  # 或提供合理默认值
    
    return template.render(variables)
```

### 6.3 结合 RAG 增强

```python
from src.rag import RAGService

async def enhanced_analyze(template_id: str, variables: dict, question: str):
    """结合 RAG 增强的分析"""
    manager = get_prompt_manager()
    rag_service = RAGService()
    
    # 获取相关知识
    context = await rag_service.retrieve(question)
    
    # 将知识注入变量
    variables["rag_context"] = context
    
    # 渲染模板
    rendered = manager.render_template(template_id, variables)
    
    return rendered
```

---

## 七、故障排查

### 问题1：模板不存在

```python
template = manager.get_template("bazi_analysis")
if template is None:
    # 模板不存在，检查是否导入了内置模板
    from src.prompts.templates import BUILTIN_TEMPLATES
    print(f"内置模板数量: {len(BUILTIN_TEMPLATES)}")
    print(f"模板ID列表: {[t.id for t in BUILTIN_TEMPLATES]}")
```

### 问题2：变量替换失败

```python
# 检查模板需要的变量
template = manager.get_template("bazi_analysis")
print(f"需要的变量: {template.variables}")

# 检查你提供的变量
print(f"提供的变量: {list(variables.keys())}")

# 找出缺失的变量
missing = set(template.variables) - set(variables.keys())
print(f"缺失变量: {missing}")
```

### 问题3：AI 输出格式不正确

```python
from src.prompts.config import validateOutputFormat

result = validateOutputFormat(ai_response)
print(f"格式有效: {result['isValid']}")
print(f"错误: {result['errors']}")
print(f"警告: {result['warnings']}")
```

---

**文档版本**：v1.0  
**最后更新**：2025-01-25
