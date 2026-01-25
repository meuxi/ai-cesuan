import datetime
from typing import Dict, Any, Tuple
from src.models import DivinationBody
from src.exceptions import BirthdayFormatError
from .base import DivinationFactory


def _get_prompt_from_template(template_id: str = "birthday_divination") -> Tuple[str, str]:
    """
    从模版库获取八字分析提示词（延迟导入）
    
    Returns:
        (system_prompt, user_prompt_template) 元组
    """
    from src.prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template(template_id)
    if template:
        return template.system_prompt, template.user_prompt_template
    # 降级默认提示词
    return (
        "你是一位精通中国传统命理学的八字分析师。",
        "请分析以下八字信息：\n{birthday_info}"
    )


def _render_bazi_template(bazi_data: Dict[str, Any]) -> Tuple[str, str]:
    """
    渲染八字分析模板
    
    Args:
        bazi_data: 包含排盘数据的字典
    
    Returns:
        (user_prompt, system_prompt) 元组
    """
    from src.prompts import get_prompt_manager
    from src.prompts.output_control import enhance_prompt_with_length_control
    
    manager = get_prompt_manager()
    template = manager.get_template("birthday_divination")
    
    if template:
        # 使用模板渲染
        rendered = template.render({"birthday_info": _format_bazi_data(bazi_data)})
        # 增强提示词（添加输出框架）
        enhanced_user_prompt = enhance_prompt_with_length_control(
            rendered["user_prompt"],
            tool_name="birthday_divination"
        )
        return enhanced_user_prompt, rendered["system_prompt"]
    else:
        # 降级处理
        system_prompt, _ = _get_prompt_from_template()
        return _format_bazi_data(bazi_data), system_prompt


def _format_bazi_data(bazi_data: Dict[str, Any]) -> str:
    """格式化八字数据为提示词"""
    sizhu = bazi_data.get('sizhu', {})
    nayin = bazi_data.get('nayin', {})
    dizhi_cang = bazi_data.get('dizhi_cang', {})
    xunkong = bazi_data.get('xunkong', {})
    lunar_info = bazi_data.get('lunar_info', {})
    date_info = bazi_data.get('date_info', {})
    
    return f"""## 出生信息
- **公历**：{date_info.get('year', '')}年{date_info.get('month', '')}月{date_info.get('day', '')}日{date_info.get('hour', '')}时
- **农历**：{lunar_info.get('year_cn', '')} {lunar_info.get('month_cn', '')}{lunar_info.get('day_cn', '')}
- **生肖**：{lunar_info.get('zodiac', '')}

## 系统精确排盘结果

### 四柱八字
- **年柱**：{sizhu.get('year', '')} ({nayin.get('year', '')})
- **月柱**：{sizhu.get('month', '')} ({nayin.get('month', '')})
- **日柱**：{sizhu.get('day', '')} ({nayin.get('day', '')}) ← 日元
- **时柱**：{sizhu.get('hour', '')} ({nayin.get('hour', '')})

### 地支藏干
- **年支藏干**：{', '.join(dizhi_cang.get('year', []))}
- **月支藏干**：{', '.join(dizhi_cang.get('month', []))}
- **日支藏干**：{', '.join(dizhi_cang.get('day', []))}
- **时支藏干**：{', '.join(dizhi_cang.get('hour', []))}

### 旬空
- **年柱旬空**：{xunkong.get('year', '')}
- **月柱旬空**：{xunkong.get('month', '')}
- **日柱旬空**：{xunkong.get('day', '')}
- **时柱旬空**：{xunkong.get('hour', '')}"""


class BirthdayFactory(DivinationFactory):

    divination_type = "birthday"

    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        # 检查是否包含排盘数据（从前端传入）
        bazi_data = getattr(divination_body, 'bazi_data', None)
        
        if bazi_data:
            # 使用精确排盘数据
            return self.build_prompt_with_paipan(
                divination_body.birthday,
                divination_body.lunar_birthday,
                bazi_data
            )
        else:
            # 降级方案：让AI自己排盘（兼容旧版本）
            return self.internal_build_prompt(
                divination_body.birthday, 
                divination_body.lunar_birthday
            )

    def build_prompt_with_paipan(self, birthday: str, lunar_birthday: str, bazi_data: dict) -> Tuple[str, str]:
        """基于精确排盘数据构建提示词"""
        try:
            date = datetime.datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise BirthdayFormatError()
        
        # 添加日期信息到 bazi_data
        bazi_data['date_info'] = {
            'year': date.year,
            'month': date.month,
            'day': date.day,
            'hour': date.hour,
            'minute': date.minute
        }
        
        # 使用模板渲染函数
        return _render_bazi_template(bazi_data)

    def internal_build_prompt(self, birthday: str, lunar_birthday: str = None) -> Tuple[str, str]:
        """降级方案：让AI自己排盘（兼容旧版本）"""
        from src.prompts.output_control import enhance_prompt_with_length_control
        
        try:
            date = datetime.datetime.strptime(
                birthday, '%Y-%m-%d %H:%M:%S'
            )
        except ValueError:
            raise BirthdayFormatError()
        
        # 优先使用农历生日进行八字排盘
        if lunar_birthday:
            prompt = f"""我的农历生日是{lunar_birthday}
（公历：{date.year}年{date.month}月{date.day}日{date.hour}时{date.minute}分）

请根据农历生日进行八字排盘和命理分析。"""
        else:
            # 兼容旧版本：如果没有农历数据，使用公历并提示AI转换
            prompt = f"""我的公历生日是{date.year}年{date.month}月{date.day}日{date.hour}时{date.minute}分{date.second}秒

请先将公历转换为农历，然后进行八字排盘和命理分析。"""
        
        # 增强提示词（添加输出框架）
        enhanced_prompt = enhance_prompt_with_length_control(
            prompt,
            tool_name="birthday_divination"
        )
        
        system_prompt, _ = _get_prompt_from_template()
        return enhanced_prompt, system_prompt
