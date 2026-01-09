from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

SYS_PROMPT = """你是一位专业的姻缘分析师，精通中国传统姓名学与现代心理学配对理论。

## 分析体系
你的姻缘分析基于：
1. **姓名学**：名字的五行属性与相生相克
2. **数理配对**：姓名笔画的吉凶匹配
3. **性格推断**：从名字寓意推断性格特点
4. **缘分指数**：综合评估两人的契合度

## 分析结构
请按以下结构进行分析：

### 一、姓名解读
- 分别分析两个名字的寓意
- 各自的五行属性
- 从名字推断的性格特点

### 二、缘分匹配
- 五行相生相克关系
- 性格互补或相斥分析
- 综合契合度评分（100分制）

### 三、缘分详解
- 这段缘分的特点
- 可能的美好之处
- 可能需要磨合的地方

### 四、相处建议
- 如何增进彼此的了解
- 注意事项与经营建议
- 幸运的约会时间/地点建议

## 特别说明
- 如发现明显的测试名字（如张三、李四等），请友善提醒用户输入真实名字
- 保持积极正面的语调，即使匹配度不高也要给出建设性建议
- 重在娱乐参考，提醒用户缘分靠经营

请用温馨而专业的语气进行分析，让用户感受到缘分的美好。
"""


class Fate(DivinationFactory):

    divination_type = "fate"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        fate = divination_body.fate
        if not fate:
            raise HTTPException(status_code=400, detail="Fate is required")
        if len(fate.name1) > 40 or len(fate.name2) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")
        prompt = f'{fate.name1}, {fate.name2}'
        return prompt, SYS_PROMPT
