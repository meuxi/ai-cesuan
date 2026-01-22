import datetime
from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory


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
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("new_name_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位专业的起名大师。"
