import datetime
from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory

NEW_NAME_PROMPT = """你是一位专业的起名大师，精通中国传统姓名学、五行学说、并结合现代审美。

## 起名体系
你的起名基于：
1. **五格剖象**：确保天格、人格、地格、外格、总格均为吉数
2. **三才配置**：天、人、地三才五行相生或比和
3. **生辰八字**：根据八字五行补缺
4. **字音字义**：音韵和谐、寓意美好
5. **现代审美**：避免生僻字、谐音尴尬

## 起名结构
请按以下结构提供名字：

### 一、八字分析
- 根据生辰推算八字
- 分析五行强弱与喀用神
- 确定需要补助的五行

### 二、推荐名字（3-5个备选）
每个名字包含：
- 完整姓名（姓+名）
- 名字寓意解释
- 五格数理分析
- 三才配置说明
- 五行属性与补益效果

### 三、最佳推荐
- 标注最优选择及理由
- 该名字的详细分析

### 四、命名建议
- 名字使用注意事项
- 小名/昵称建议（如适用）

## 起名原则
- 姓氏在前，名字在后
- 避免与历史负面人物同名
- 音调和谐，朗朗上口
- 字形美观，书写顺畅

请结合用户提供的信息，给出专业且实用的命名建议。
"""


class NewNameFactory(DivinationFactory):

    divination_type = "new_name"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if (not divination_body.new_name or not all([
            divination_body.new_name.surname,
            divination_body.new_name.birthday,
            divination_body.new_name.sex,
        ]) or len(divination_body.new_name.new_name_prompt) > 20):
            raise HTTPException(status_code=400, detail="起名参数错误")

        try:
            birthday = datetime.datetime.strptime(
                divination_body.birthday, '%Y-%m-%d %H:%M:%S'
            )
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="生日格式错误，请使用格式：YYYY-MM-DD HH:MM:SS"
            )
        
        prompt = (
            f"姓氏是{divination_body.new_name.surname},"
            f"生日是{birthday.year}年{birthday.month}月{birthday.day}日{birthday.hour}时{birthday.minute}分{birthday.second}秒"
        )
        if divination_body.new_name.new_name_prompt:
            prompt += f",我的要求是: {divination_body.new_name.new_name_prompt}"
        return prompt, NEW_NAME_PROMPT
