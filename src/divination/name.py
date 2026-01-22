from src.models import DivinationBody
from src.utils.stroke_counter import format_five_grids_prompt
from src.exceptions import NameLengthError
from .base import DivinationFactory


class NameFactory(DivinationFactory):

    divination_type = "name"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        name = divination_body.prompt.strip()
        if len(name) > 10 or len(name) < 2:
            raise NameLengthError()
        
        # 使用笔画计算工具生成五格信息
        five_grids_info = format_five_grids_prompt(name)
        
        prompt = f"""请分析以下姓名：

{five_grids_info}"""
        
        # 从模版库获取提示词（延迟导入）
        from src.prompts import get_prompt_manager
        manager = get_prompt_manager()
        template = manager.get_template("name_divination")
        if template:
            return prompt, template.system_prompt
        
        return prompt, "你是一位精通中国传统姓名学的分析师。"
