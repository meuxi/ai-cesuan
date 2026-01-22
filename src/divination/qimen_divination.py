"""奇门遁甲AI解读工厂"""
from src.models import DivinationBody
from src.prompts import get_prompt_manager
from .base import DivinationFactory


class QimenFactory(DivinationFactory):
    
    divination_type = "qimen"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        prompt = divination_body.prompt
        if not prompt:
            prompt = "请根据奇门盘进行分析"
        
        # 从模版库获取提示词
        manager = get_prompt_manager()
        template = manager.get_template("qimen_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通奇门遁甲的预测大师。"
