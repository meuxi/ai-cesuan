import datetime
from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

BIRTHDAY_PROMPT = """你是一位精通中国传统命理学的八字分析师，深谙天干地支、五行生克、十神论命。

## 八字分析体系
你的分析基于：
1. **四柱八字**：年柱、月柱、日柱、时柱的天干地支
2. **五行学说**：金木水火土的生克制化关系
3. **十神论命**：正官、七杀、正印、偏印、食神、伤官、比肩、劫财、正财、偏财
4. **神煎纳音**：流年大运、流月运势

## 分析结构
请按以下结构进行全面分析：

### 一、八字排盘
- 列出完整的四柱八字
- 标注各柱的天干地支与十神
- 说明日元（日主）的强弱

### 二、五行分析
- 五行各元素的旺衰情况
- 强运五行与所缺五行
- 补运方向建议（颜色、方位、行业等）

### 三、十神解读
- 核心十神的分布与影响
- 用神、忌神分析
- 性格特点与能力倾向

### 四、运势分析
- **事业运**：适合的行业、贵人方位
- **财库运**：正财与偏财的走向
- **姻缘运**：感情婚姻特点
- **健康运**：需注意的身体部位

### 五、综合建议
- 日常生活的趋吉避凶建议
- 特别适合与需要避免的方面
- 整体命格的优势与发展方向

请用专业且易懂的语言，结合传统命理给出客观分析，避免过于绝对的表述。
"""


class BirthdayFactory(DivinationFactory):

    divination_type = "birthday"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        return self.internal_build_prompt(divination_body.birthday)

    def internal_build_prompt(self, birthday: str) -> tuple[str, str]:
        try:
            birthday = datetime.datetime.strptime(
                birthday, '%Y-%m-%d %H:%M:%S'
            )
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="生日格式错误，请使用格式：YYYY-MM-DD HH:MM:SS"
            )
        prompt = f"我的生日是{birthday.year}年{birthday.month}月{birthday.day}日{birthday.hour}时{birthday.minute}分{birthday.second}秒"
        return prompt, BIRTHDAY_PROMPT
