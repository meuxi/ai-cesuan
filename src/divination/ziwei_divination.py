"""紫微斗数AI解读工厂"""
from src.models import DivinationBody
from .base import DivinationFactory


class ZiweiFactory(DivinationFactory):
    
    divination_type = "ziwei"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        prompt = divination_body.prompt
        if not prompt:
            prompt = "请根据我的紫微命盘进行分析"
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("ziwei_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通紫微斗数的命理大师。"
