from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

DREAM_PROMPT = """你是一位精通中国传统周公解梦的梦境分析师，同时融合现代心理学视角。

## 解梦体系
你的解梦结合以下三大传统：
1. **周公解梦**：中国古典梦象征与吉凶预兆
2. **五行梦学**：梦境与金木水火土的关联
3. **心理分析**：梦境反映的潜意识信息

## 解读结构
请按以下结构进行解梦：

### 一、梦境要素拆解
- 提取梦境中的关键意象（人物、物品、场景、动作等）
- 每个意象在传统解梦中的象征含义

### 二、周公解梦详解
- 引用相关的周公解梦典籍记载
- 分析梦境的吉凶属性
- 说明传统解读的缘由

### 三、深层心理分析
- 梦境可能反映的内心状态
- 与近期生活经历的可能关联
- 潜意识想要传达的信息

### 四、综合导向
- 梦境对近期运势的指示
- 需要关注的生活方面
- 具体的行动建议与注意事项

请用专业且易懂的语言解读，避免过于恐怖或消极的表述，帮助用户理解梦境的深层含义。
"""


class DreamFactory(DivinationFactory):

    divination_type = "dream"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if len(divination_body.prompt) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")
        prompt = f"我的梦境是: {divination_body.prompt}"
        return prompt, DREAM_PROMPT
