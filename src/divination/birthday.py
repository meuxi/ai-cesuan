import datetime
from src.models import DivinationBody
from src.exceptions import BirthdayFormatError
from .base import DivinationFactory


def _get_birthday_system_prompt() -> str:
    """从模版库获取八字分析系统提示词（延迟导入）"""
    from src.prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template("birthday_divination")
    if template:
        return template.system_prompt
    return "你是一位精通中国传统命理学的八字分析师。"


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

    def build_prompt_with_paipan(self, birthday: str, lunar_birthday: str, bazi_data: dict) -> tuple[str, str]:
        """基于精确排盘数据构建提示词"""
        try:
            date = datetime.datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise BirthdayFormatError()
        
        # 提取排盘数据
        sizhu = bazi_data.get('sizhu', {})
        nayin = bazi_data.get('nayin', {})
        dizhi_cang = bazi_data.get('dizhi_cang', {})
        xunkong = bazi_data.get('xunkong', {})
        lunar_info = bazi_data.get('lunar_info', {})
        
        # 构建包含完整排盘数据的提示词
        prompt = f"""## 出生信息
- **公历**：{date.year}年{date.month}月{date.day}日{date.hour}时{date.minute}分
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
- **时柱旬空**：{xunkong.get('hour', '')}

---

## 你的任务
请基于以上精确的排盘数据：
1. **审查确认**：验证四柱干支、纳音的合理性
2. **计算十神**：以日元（{sizhu.get('day', '')[:1]}）为中心，计算各柱天干地支的十神
3. **分析五行**：统计五行强弱，确定日元旺衰
4. **判断用神**：根据日元旺衰和格局，确定用神忌神
5. **深度解读**：结合经典命理，给出事业、财运、感情、健康等全面分析
6. **实用建议**：提供趋吉避凶的具体建议

请用专业且易懂的语言进行分析。"""
        
        return prompt, _get_birthday_system_prompt()

    def internal_build_prompt(self, birthday: str, lunar_birthday: str = None) -> tuple[str, str]:
        """降级方案：让AI自己排盘（兼容旧版本）"""
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
        
        return prompt, _get_birthday_system_prompt()
