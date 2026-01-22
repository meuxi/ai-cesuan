from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory


class DreamFactory(DivinationFactory):

    divination_type = "dream"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if len(divination_body.prompt) > 40:
            raise HTTPException(status_code=400, detail="Prompt too long")
        prompt = f"我的梦境是: {divination_body.prompt}"
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("dream_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通中国传统周公解梦的梦境分析师。"
