from fastapi import HTTPException
from src.models import DivinationBody
from .base import DivinationFactory


class PlumFlowerFactory(DivinationFactory):

    divination_type = "plum_flower"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if not divination_body.plum_flower:
            raise HTTPException(status_code=400, detail="No plum_flower")
        prompt = f"我选择的数字是: {divination_body.plum_flower.num1} 和 {divination_body.plum_flower.num2}"
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("plum_flower_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通梅花易数的占卜大师。"
