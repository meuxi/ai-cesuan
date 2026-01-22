from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory


class Fate(DivinationFactory):

    divination_type = "fate"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        fate = divination_body.fate
        if not fate:
            raise HTTPException(status_code=400, detail="Fate is required")
        if len(fate.name1) > 40 or len(fate.name2) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")
        prompt = f'{fate.name1}, {fate.name2}'
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("fate_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位专业的姻缘分析师。"
