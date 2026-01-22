"""
星座计算器
提供太阳星座、月亮星座、上升星座的计算
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime, date
from dataclasses import dataclass
import math


@dataclass
class ZodiacInfo:
    """星座信息"""
    name: str           # 中文名
    english: str        # 英文名
    symbol: str         # 符号
    element: str        # 元素（火/土/风/水）
    quality: str        # 特质（本位/固定/变动）
    ruler: str          # 守护星
    date_range: str     # 日期范围
    traits: list        # 特质
    strengths: list     # 优点
    weaknesses: list    # 缺点


# 十二星座信息
ZODIAC_DATA: Dict[str, ZodiacInfo] = {
    '白羊座': ZodiacInfo(
        name='白羊座', english='Aries', symbol='♈',
        element='火', quality='本位', ruler='火星',
        date_range='3月21日-4月19日',
        traits=['热情', '勇敢', '直率', '冲动'],
        strengths=['勇气', '领导力', '行动力', '开拓精神'],
        weaknesses=['急躁', '自我', '缺乏耐心', '冲动行事']
    ),
    '金牛座': ZodiacInfo(
        name='金牛座', english='Taurus', symbol='♉',
        element='土', quality='固定', ruler='金星',
        date_range='4月20日-5月20日',
        traits=['稳重', '务实', '耐心', '固执'],
        strengths=['可靠', '耐心', '务实', '艺术感'],
        weaknesses=['固执', '占有欲强', '不够灵活', '贪图享受']
    ),
    '双子座': ZodiacInfo(
        name='双子座', english='Gemini', symbol='♊',
        element='风', quality='变动', ruler='水星',
        date_range='5月21日-6月20日',
        traits=['机智', '好奇', '善变', '健谈'],
        strengths=['聪明', '适应力强', '沟通能力强', '多才多艺'],
        weaknesses=['善变', '表面', '神经质', '缺乏专注']
    ),
    '巨蟹座': ZodiacInfo(
        name='巨蟹座', english='Cancer', symbol='♋',
        element='水', quality='本位', ruler='月亮',
        date_range='6月21日-7月22日',
        traits=['敏感', '顾家', '保护欲强', '情绪化'],
        strengths=['有爱心', '保护欲强', '直觉准', '忠诚'],
        weaknesses=['情绪化', '过度敏感', '多疑', '依赖性强']
    ),
    '狮子座': ZodiacInfo(
        name='狮子座', english='Leo', symbol='♌',
        element='火', quality='固定', ruler='太阳',
        date_range='7月23日-8月22日',
        traits=['自信', '大方', '戏剧化', '骄傲'],
        strengths=['领导力', '慷慨', '热情', '创造力'],
        weaknesses=['自负', '固执', '爱面子', '专制']
    ),
    '处女座': ZodiacInfo(
        name='处女座', english='Virgo', symbol='♍',
        element='土', quality='变动', ruler='水星',
        date_range='8月23日-9月22日',
        traits=['细心', '完美主义', '分析能力强', '挑剔'],
        strengths=['细致', '勤劳', '分析力强', '可靠'],
        weaknesses=['挑剔', '过度担忧', '苛刻', '保守']
    ),
    '天秤座': ZodiacInfo(
        name='天秤座', english='Libra', symbol='♎',
        element='风', quality='本位', ruler='金星',
        date_range='9月23日-10月22日',
        traits=['和谐', '公正', '优雅', '犹豫'],
        strengths=['外交能力', '公正', '有品味', '善于合作'],
        weaknesses=['犹豫不决', '逃避冲突', '依赖他人', '虚荣']
    ),
    '天蝎座': ZodiacInfo(
        name='天蝎座', english='Scorpio', symbol='♏',
        element='水', quality='固定', ruler='冥王星',
        date_range='10月23日-11月21日',
        traits=['神秘', '深沉', '洞察力强', '执着'],
        strengths=['意志力强', '洞察力', '忠诚', '热情'],
        weaknesses=['嫉妒', '多疑', '控制欲强', '报复心']
    ),
    '射手座': ZodiacInfo(
        name='射手座', english='Sagittarius', symbol='♐',
        element='火', quality='变动', ruler='木星',
        date_range='11月22日-12月21日',
        traits=['乐观', '自由', '坦率', '冒险'],
        strengths=['乐观', '诚实', '有远见', '热爱自由'],
        weaknesses=['冲动', '不负责任', '盲目乐观', '缺乏耐心']
    ),
    '摩羯座': ZodiacInfo(
        name='摩羯座', english='Capricorn', symbol='♑',
        element='土', quality='本位', ruler='土星',
        date_range='12月22日-1月19日',
        traits=['务实', '有野心', '严谨', '保守'],
        strengths=['责任心', '自律', '耐心', '野心'],
        weaknesses=['悲观', '固执', '不够灵活', '工作狂']
    ),
    '水瓶座': ZodiacInfo(
        name='水瓶座', english='Aquarius', symbol='♒',
        element='风', quality='固定', ruler='天王星',
        date_range='1月20日-2月18日',
        traits=['独立', '创新', '人道主义', '叛逆'],
        strengths=['独立', '创新', '人道主义', '理想主义'],
        weaknesses=['疏离', '固执', '不切实际', '情感淡漠']
    ),
    '双鱼座': ZodiacInfo(
        name='双鱼座', english='Pisces', symbol='♓',
        element='水', quality='变动', ruler='海王星',
        date_range='2月19日-3月20日',
        traits=['敏感', '富有同情心', '浪漫', '逃避现实'],
        strengths=['同理心', '直觉强', '艺术天赋', '无私'],
        weaknesses=['逃避现实', '过度敏感', '优柔寡断', '容易受伤']
    ),
}

# 星座日期范围（月, 日）
ZODIAC_DATE_RANGES = [
    ((1, 20), (2, 18), '水瓶座'),
    ((2, 19), (3, 20), '双鱼座'),
    ((3, 21), (4, 19), '白羊座'),
    ((4, 20), (5, 20), '金牛座'),
    ((5, 21), (6, 20), '双子座'),
    ((6, 21), (7, 22), '巨蟹座'),
    ((7, 23), (8, 22), '狮子座'),
    ((8, 23), (9, 22), '处女座'),
    ((9, 23), (10, 22), '天秤座'),
    ((10, 23), (11, 21), '天蝎座'),
    ((11, 22), (12, 21), '射手座'),
    ((12, 22), (1, 19), '摩羯座'),
]


def get_sun_sign(month: int, day: int) -> str:
    """
    根据出生月日获取太阳星座
    
    Args:
        month: 月份 (1-12)
        day: 日期 (1-31)
        
    Returns:
        星座名称
    """
    for start, end, sign in ZODIAC_DATE_RANGES:
        start_month, start_day = start
        end_month, end_day = end
        
        if start_month == end_month:
            if month == start_month and start_day <= day <= end_day:
                return sign
        elif start_month < end_month:
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day):
                return sign
        else:  # 跨年（摩羯座）
            if (month == start_month and day >= start_day) or \
               (month == end_month and day <= end_day):
                return sign
    
    return '摩羯座'  # 默认


def get_moon_sign(
    year: int, month: int, day: int, 
    hour: int = 12, minute: int = 0
) -> Dict[str, Any]:
    """
    计算月亮星座（简化算法）
    
    注：精确的月亮星座需要天文星历表，此处为简化算法
    
    Args:
        year: 年份
        month: 月份
        day: 日期
        hour: 小时
        minute: 分钟
        
    Returns:
        月亮星座信息
    """
    # 简化算法：基于出生日期的近似计算
    # 月亮约27.3天绑定一个周期
    base_date = datetime(2000, 1, 1, 12, 0)  # 基准日期
    birth_date = datetime(year, month, day, hour, minute)
    
    days_diff = (birth_date - base_date).total_seconds() / 86400
    
    # 月亮周期约27.3天
    moon_cycle = 27.321661
    
    # 计算月亮位置（0-360度）
    moon_position = (days_diff / moon_cycle * 360) % 360
    
    # 加上基准日期的月亮位置（约巨蟹座0度）
    moon_position = (moon_position + 90) % 360
    
    # 转换为星座（每个星座30度）
    zodiac_index = int(moon_position / 30)
    zodiac_names = [
        '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座',
        '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座'
    ]
    
    moon_sign = zodiac_names[zodiac_index]
    degree = moon_position % 30
    
    return {
        'sign': moon_sign,
        'degree': round(degree, 2),
        'info': ZODIAC_DATA.get(moon_sign),
        'note': '月亮星座影响你的情感模式和内心需求'
    }


def get_rising_sign(
    year: int, month: int, day: int,
    hour: int, minute: int = 0,
    latitude: float = 39.9  # 默认北京纬度
) -> Dict[str, Any]:
    """
    计算上升星座（简化算法）
    
    注：精确的上升星座需要出生地经纬度和星历表
    
    Args:
        year: 年份
        month: 月份
        day: 日期
        hour: 小时（24小时制）
        minute: 分钟
        latitude: 纬度
        
    Returns:
        上升星座信息
    """
    # 简化算法
    # 上升星座与出生时间、太阳位置相关
    
    # 获取太阳星座
    sun_sign = get_sun_sign(month, day)
    sun_index = list(ZODIAC_DATA.keys()).index(sun_sign)
    
    # 根据出生时间计算上升星座偏移
    # 大约每2小时上升一个星座
    hour_offset = ((hour + minute / 60) - 6) / 2  # 以6点为基准
    
    # 纬度修正（简化）
    lat_correction = (latitude - 45) / 90 * 0.5
    
    rising_index = int((sun_index + hour_offset + lat_correction) % 12)
    
    zodiac_names = list(ZODIAC_DATA.keys())
    rising_sign = zodiac_names[rising_index]
    
    return {
        'sign': rising_sign,
        'info': ZODIAC_DATA.get(rising_sign),
        'note': '上升星座代表你给他人的第一印象和外在表现',
        'calculation_note': '精确计算需要出生地经纬度'
    }


def get_zodiac_info(zodiac_name: str) -> Optional[Dict[str, Any]]:
    """获取星座详细信息"""
    info = ZODIAC_DATA.get(zodiac_name)
    if not info:
        return None
    
    return {
        'name': info.name,
        'english': info.english,
        'symbol': info.symbol,
        'element': info.element,
        'quality': info.quality,
        'ruler': info.ruler,
        'date_range': info.date_range,
        'traits': info.traits,
        'strengths': info.strengths,
        'weaknesses': info.weaknesses,
    }


def get_all_zodiacs() -> list:
    """获取所有星座信息"""
    return [get_zodiac_info(name) for name in ZODIAC_DATA.keys()]
