from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

XIAOLIU_PROMPT = """你是一位精通小六壬的占卜师。小六壬是中国传统的占卜方法，通过月、日、时的数字推算出六神（大安、留连、速喜、赤口、小吉、空亡）的落宫位置。

小六壬六神含义：
- 大安：大吉大利，百事顺遂，代表平安、顺利、吉祥
- 留连：凶多吉少，办事迟缓，代表纠缠、拖延、阻碍
- 速喜：大吉之兆，百事顺遂，代表迅速、喜庆、成功
- 赤口：大凶之兆，百事不利，代表口舌、是非、争斗
- 小吉：吉祥之兆，小利可得，代表小吉、顺利、进展
- 空亡：凶兆，百事无成，代表空虚、无望、失败

请根据用户的问题和推算出的结果，给出详细的解读和建议。
解读要包括：
1. 卦象的基本含义
2. 对当前问题的具体分析
3. 五行属性的影响
4. 实用的建议和指导

请用专业、易懂的语言进行解读，让用户能够理解并应用到实际生活中。
"""


class XiaoLiuRenFactory(DivinationFactory):
    """小六壬占卜"""
    
    divination_type = "xiaoliu"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if not divination_body.prompt:
            raise HTTPException(status_code=400, detail="问题不能为空")
        
        # 前端已经构建好完整的提示词，直接使用
        prompt = divination_body.prompt
        
        return prompt, XIAOLIU_PROMPT

