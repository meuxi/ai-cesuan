"""紫微斗数AI解读工厂"""
import json
from src.models import DivinationBody
from .base import DivinationFactory


def _get_ziwei_system_prompt() -> str:
    """从模版库获取紫微斗数系统提示词（延迟导入）"""
    from src.prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template("ziwei_divination")
    if template:
        return template.system_prompt
    return "你是一位精通紫微斗数的命理大师。"


class ZiweiFactory(DivinationFactory):
    
    divination_type = "ziwei"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        # 检查是否包含排盘数据（从前端传入）
        ziwei_data = getattr(divination_body, 'ziwei_data', None)
        
        if ziwei_data:
            # 使用精确排盘数据
            return self.build_prompt_with_paipan(ziwei_data, divination_body.prompt)
        else:
            # 降级方案：简单提示词
            prompt = divination_body.prompt
            if not prompt:
                prompt = "请根据我的紫微命盘进行分析"
            return prompt, _get_ziwei_system_prompt()
    
    def build_prompt_with_paipan(self, ziwei_data: dict, user_question: str = None) -> tuple[str, str]:
        """基于精确排盘数据构建提示词"""
        
        # 提取基本信息
        basic_info = ziwei_data.get('basicInfo', {})
        palaces = ziwei_data.get('palaces', [])
        
        # 构建命盘信息
        prompt_parts = []
        
        # 基本信息
        prompt_parts.append("## 命盘基本信息")
        prompt_parts.append(f"- **阳历**：{basic_info.get('solarDate', '未知')}")
        prompt_parts.append(f"- **农历**：{basic_info.get('lunarDate', '未知')}")
        prompt_parts.append(f"- **性别**：{'男' if basic_info.get('gender') == 'male' else '女'}")
        prompt_parts.append(f"- **命主**：{basic_info.get('soul', '未知')}")
        prompt_parts.append(f"- **身主**：{basic_info.get('body', '未知')}")
        prompt_parts.append(f"- **五行局**：{basic_info.get('fiveElement', '未知')}")
        prompt_parts.append("")
        
        # 十二宫信息
        prompt_parts.append("## 十二宫详细信息")
        for palace in palaces:
            palace_name = palace.get('name', '未知宫')
            main_stars = palace.get('majorStars', [])
            minor_stars = palace.get('minorStars', [])
            adj_stars = palace.get('adjStars', [])
            
            # 主星
            main_star_names = [s.get('name', '') for s in main_stars if s.get('name')]
            # 辅星
            minor_star_names = [s.get('name', '') for s in minor_stars if s.get('name')]
            # 杂曜
            adj_star_names = [s.get('name', '') for s in adj_stars if s.get('name')]
            
            prompt_parts.append(f"### {palace_name}")
            if main_star_names:
                prompt_parts.append(f"- **主星**：{', '.join(main_star_names)}")
            if minor_star_names:
                prompt_parts.append(f"- **辅星**：{', '.join(minor_star_names)}")
            if adj_star_names:
                prompt_parts.append(f"- **杂曜**：{', '.join(adj_star_names)}")
            prompt_parts.append("")
        
        # 用户问题
        if user_question:
            prompt_parts.append("---")
            prompt_parts.append(f"## 用户问题")
            prompt_parts.append(user_question)
        
        prompt_parts.append("")
        prompt_parts.append("请基于以上精确的紫微斗数排盘数据，进行专业深入的命理分析。")
        
        prompt = "\n".join(prompt_parts)
        return prompt, _get_ziwei_system_prompt()
