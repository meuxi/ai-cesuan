import re
import logging
from src.models import DivinationBody
from src.exceptions import EmptyPromptError
from src.divination.base import DivinationFactory

_logger = logging.getLogger(__name__)

# 六神详细数据
LIU_GODS = {
    1: "大安",
    2: "留连",
    3: "速喜",
    4: "赤口",
    5: "小吉",
    6: "空亡"
}

LIU_GOD_MEANINGS = {
    "大安": {
        "五行": "木",
        "方位": "东方",
        "吉凶": "大吉",
        "天干": "甲乙",
        "地支": "寅卯",
        "人物": "贵人、长辈",
        "身体": "肝胆、四肢",
        "含义": "平安顺遂、身心安泰、贵人相助、事业稳定",
        "详解": "大安为六神之首，主平安吉祥。凡事问大安，皆主顺遂。求财可得，求官有望，求婚成，求病愈。出行平安，寻人可见。"
    },
    "留连": {
        "五行": "木",
        "方位": "东南",
        "吉凶": "小凶",
        "天干": "丙丁",
        "地支": "巳午",
        "人物": "朋友、同辈",
        "身体": "心脏、血液",
        "含义": "事多纠缠、拖延阻碍、进退两难、暗昧不明",
        "详解": "留连主迟滞纠缠。凡事问留连，主有阻碍。求财难得，求官无望，求婚多阻，求病缠绵。出行有阻，寻人难见。宜守不宜进。"
    },
    "速喜": {
        "五行": "火",
        "方位": "南方",
        "吉凶": "大吉",
        "天干": "戊己",
        "地支": "辰戌丑未",
        "人物": "媒人、喜神",
        "身体": "脾胃、肌肉",
        "含义": "喜事临门、速战速决、心想事成、有意外之喜",
        "详解": "速喜主喜庆快速。凡事问速喜，主有喜事。求财速得，求官有喜，求婚成，求病速愈。出行大吉，寻人即见。宜速不宜迟。"
    },
    "赤口": {
        "五行": "金",
        "方位": "西方",
        "吉凶": "大凶",
        "天干": "庚辛",
        "地支": "申酉",
        "人物": "小人、官司",
        "身体": "肺部、呼吸",
        "含义": "口舌是非、争斗破财、需防小人、官非牢狱",
        "详解": "赤口主口舌是非。凡事问赤口，主有凶险。求财破败，求官有阻，求婚不成，求病加重。出行有灾，寻人不见。宜静不宜动，需防小人暗害。"
    },
    "小吉": {
        "五行": "水",
        "方位": "北方",
        "吉凶": "小吉",
        "天干": "壬癸",
        "地支": "亥子",
        "人物": "妇人、阴人",
        "身体": "肾脏、泌尿",
        "含义": "小有收获、稳中求进、适宜守成、有人相助",
        "详解": "小吉主小有所得。凡事问小吉，主吉中有阻。求财小得，求官有望，求婚可成，求病渐愈。出行小利，寻人可见。宜守正道，循序渐进。"
    },
    "空亡": {
        "五行": "土",
        "方位": "中央",
        "吉凶": "大凶",
        "天干": "戊己",
        "地支": "辰戌",
        "人物": "僧道、隐士",
        "身体": "脾胃、消化",
        "含义": "事落空虚、求之不得、宜静不宜动、诸事皆空",
        "详解": "空亡主虚空不实。凡事问空亡，主落空无成。求财不得，求官无望，求婚不成，求病难愈。出行无益，寻人不见。宜静守，不宜妄动。"
    }
}

# 36种组合解读（6×6落宫组合）- 来源：小六壬排盘工具源码
LIU_GOD_COMBINATIONS = {
    "大安": {
        "basic": "大吉大利，百事顺遂。代表平安、顺利、吉祥。谋事可成，婚姻美满，出行平安，疾病不药而愈。",
        "combinations": {
            "大安": "双重吉利，万事如意",
            "留连": "先吉后阻，需耐心等待",
            "速喜": "速战速决，马到成功",
            "赤口": "吉中带凶，需谨慎行事",
            "小吉": "吉祥如意，小利可得",
            "空亡": "吉处藏凶，事有阻碍"
        }
    },
    "留连": {
        "basic": "凶多吉少，办事迟缓。代表纠缠、拖延、阻碍。谋事难成，婚姻有阻，出行不利，疾病缠绵。",
        "combinations": {
            "大安": "先阻后吉，终有好结果",
            "留连": "双重阻碍，难以成功",
            "速喜": "虽有阻碍，终会成功",
            "赤口": "凶上加凶，灾祸临头",
            "小吉": "困境中有机遇",
            "空亡": "完全受阻，宜守不宜进"
        }
    },
    "速喜": {
        "basic": "大吉之兆，百事顺遂。代表迅速、喜庆、成功。谋事速成，婚姻喜庆，出行顺利，疾病速愈。",
        "combinations": {
            "大安": "大吉大利，万事如意",
            "留连": "先吉后缓，不宜操之过急",
            "速喜": "双喜临门，运势亨通",
            "赤口": "先喜后忧，需防意外",
            "小吉": "喜庆连连，小利不断",
            "空亡": "喜中有忧，事有变数"
        }
    },
    "赤口": {
        "basic": "大凶之兆，百事不利。代表口舌、是非、争斗。谋事不成，婚姻不顺，出行有灾，疾病加重。",
        "combinations": {
            "大安": "凶中带吉，化险为夷",
            "留连": "凶上加凶，大祸临头",
            "速喜": "先凶后吉，转危为安",
            "赤口": "双重凶险，灾难重重",
            "小吉": "凶中有机，小吉可求",
            "空亡": "凶多吉少，宜守不宜进"
        }
    },
    "小吉": {
        "basic": "吉祥之兆，小利可得。代表小吉、顺利、进展。谋事小成，婚姻顺利，出行平安，疾病好转。",
        "combinations": {
            "大安": "大吉小吉，万事如意",
            "留连": "小有阻碍，终会成功",
            "速喜": "喜上加喜，运势亨通",
            "赤口": "小有不顺，需防口舌",
            "小吉": "双重小吉，步步顺利",
            "空亡": "吉中带凶，事有变数"
        }
    },
    "空亡": {
        "basic": "凶兆，百事无成。代表空虚、无望、失败。谋事不成，婚姻难成，出行不利，疾病难愈。",
        "combinations": {
            "大安": "凶中带吉，终有转机",
            "留连": "完全失败，不宜行动",
            "速喜": "先凶后吉，峰回路转",
            "赤口": "大凶之兆，灾祸临头",
            "小吉": "小吉化解，转危为安",
            "空亡": "双重空亡，一事无成"
        }
    }
}

# 时辰对照表
HOUR_TABLE = [
    {"index": 1, "chinese": "子", "time": "23:00-01:00"},
    {"index": 2, "chinese": "丑", "time": "01:00-03:00"},
    {"index": 3, "chinese": "寅", "time": "03:00-05:00"},
    {"index": 4, "chinese": "卯", "time": "05:00-07:00"},
    {"index": 5, "chinese": "辰", "time": "07:00-09:00"},
    {"index": 6, "chinese": "巳", "time": "09:00-11:00"},
    {"index": 7, "chinese": "午", "time": "11:00-13:00"},
    {"index": 8, "chinese": "未", "time": "13:00-15:00"},
    {"index": 9, "chinese": "申", "time": "15:00-17:00"},
    {"index": 10, "chinese": "酉", "time": "17:00-19:00"},
    {"index": 11, "chinese": "戌", "time": "19:00-21:00"},
    {"index": 12, "chinese": "亥", "time": "21:00-23:00"}
]


def get_hour_from_time(hour: int) -> int:
    """根据24小时制获取时辰序号（1-12）"""
    if hour >= 23 or hour < 1:
        return 1  # 子时
    if hour >= 1 and hour < 3:
        return 2  # 丑时
    if hour >= 3 and hour < 5:
        return 3  # 寅时
    if hour >= 5 and hour < 7:
        return 4  # 卯时
    if hour >= 7 and hour < 9:
        return 5  # 辰时
    if hour >= 9 and hour < 11:
        return 6  # 巳时
    if hour >= 11 and hour < 13:
        return 7  # 午时
    if hour >= 13 and hour < 15:
        return 8  # 未时
    if hour >= 15 and hour < 17:
        return 9  # 申时
    if hour >= 17 and hour < 19:
        return 10  # 酉时
    if hour >= 19 and hour < 21:
        return 11  # 戌时
    return 12  # 亥时


def get_combination_interpretation(day_god: str, final_god: str) -> str:
    """获取日宫与时宫的组合解读"""
    if day_god in LIU_GOD_COMBINATIONS and final_god in LIU_GOD_COMBINATIONS[day_god]["combinations"]:
        return LIU_GOD_COMBINATIONS[day_god]["combinations"][final_god]
    return ""


def calculate_xiaoliu(month: int, day: int, hour: int) -> dict:
    """
    计算小六壬落宫
    
    六神循环顺序：大安(1)→留连(2)→速喜(3)→赤口(4)→小吉(5)→空亡(6)→大安(1)
    
    起卦方法（传统口诀）：
    1. 正月从大安起，二月从留连起，三月从速喜起...
    2. 月上定位后，初一从该宫起，初二下一宫...
    3. 日上定位后，子时从该宫起，丑时下一宫...
    
    计算公式：
    - 月份落宫 = ((month - 1) % 6) + 1
    - 日份落宫 = ((月份落宫 - 1 + day - 1) % 6) + 1
    - 时辰落宫 = ((日份落宫 - 1 + hour - 1) % 6) + 1
    
    Args:
        month: 农历月份 (1-12)
        day: 农历日期 (1-30)
        hour: 时辰序号 (1-12，子时为1)
        
    Returns:
        包含落宫信息的字典
    """
    # 月份落宫：正月从大安(1)起
    month_position = ((month - 1) % 6) + 1
    month_god = LIU_GODS[month_position]
    
    # 日份落宫：从月份落宫起，数日数
    day_position = ((month_position - 1 + day - 1) % 6) + 1
    day_god = LIU_GODS[day_position]
    
    # 时辰落宫：从日份落宫起，数时辰数
    hour_position = ((day_position - 1 + hour - 1) % 6) + 1
    final_god = LIU_GODS[hour_position]
    
    # 获取组合解读
    combination_interpretation = get_combination_interpretation(day_god, final_god)
    
    return {
        "month": month,
        "day": day,
        "hour": hour,
        "month_position": month_position,
        "month_god": month_god,
        "day_position": day_position,
        "day_god": day_god,
        "final_position": hour_position,
        "final_god": final_god,
        "meaning": LIU_GOD_MEANINGS.get(final_god, {}),
        "combination": combination_interpretation,
        "basic_interpretation": LIU_GOD_COMBINATIONS.get(final_god, {}).get("basic", "")
    }


def _get_xiaoliu_system_prompt() -> str:
    """从模版库获取小六壬系统提示词"""
    from src.prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template("xiaoliu_divination")
    if template:
        return template.system_prompt
    return "你是一位精通小六壬的占卜大师。"


class XiaoLiuRenFactory(DivinationFactory):
    """小六壬占卜"""
    
    divination_type = "xiaoliu"
    
    def build_prompt(self, divination_body: DivinationBody) -> tuple[str, str]:
        if not divination_body.prompt:
            raise EmptyPromptError()
        
        prompt = divination_body.prompt
        
        # 尝试从前端传来的prompt中解析月日时信息进行后端验证
        match = re.search(r"月(\d+)日(\d+)时(\d+)", prompt)
        if match:
            try:
                month = int(match.group(1))
                day = int(match.group(2))
                hour = int(match.group(3))
                
                # 后端计算验证
                result = calculate_xiaoliu(month, day, hour)
                god_info = result["meaning"]
                
                # 增强prompt，添加详细六神信息
                enhanced_info = f"""

【后端验证信息】
- 农历：{month}月{day}日 {hour}时
- 月上起宫：{result['month_god']}（第{result['month_position']}宫）
- 日上起宫：{result['day_god']}（第{result['day_position']}宫）
- 最终落宫：{result['final_god']}（第{result['final_position']}宫）
- 五行：{god_info.get('五行', '未知')}
- 方位：{god_info.get('方位', '未知')}
- 吉凶：{god_info.get('吉凶', '未知')}
- 天干：{god_info.get('天干', '未知')}
- 地支：{god_info.get('地支', '未知')}
- 人物：{god_info.get('人物', '未知')}
- 身体：{god_info.get('身体', '未知')}
- 核心含义：{god_info.get('含义', '未知')}
- 详解：{god_info.get('详解', '无')}"""
                
                prompt = prompt + enhanced_info
                
            except Exception as e:
                _logger.warning(f"小六壬后端验证失败: {e}")
        
        return prompt, _get_xiaoliu_system_prompt()

