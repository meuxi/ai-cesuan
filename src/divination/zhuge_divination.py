"""诸葛神算AI解读工厂"""
from src.models import DivinationBody
from .base import DivinationFactory


class ZhugeFactory(DivinationFactory):
    
    divination_type = "zhuge"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        prompt = divination_body.prompt
        if not prompt:
            prompt = "请解读此签"
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("zhuge_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通诸葛神算的解签大师。"
