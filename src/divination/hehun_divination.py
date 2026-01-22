"""八字合婚AI解读工厂"""
from src.models import DivinationBody
from src.prompts import get_prompt_manager
from .base import DivinationFactory


class HehunFactory(DivinationFactory):
    
    divination_type = "hehun"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        prompt = divination_body.prompt
        if not prompt:
            prompt = "请分析这对的婚姻配对"
        
        # 从模版库获取提示词
        manager = get_prompt_manager()
        template = manager.get_template("hehun_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通八字合婚的命理大师。"
