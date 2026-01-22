"""
黄历/日历数据封装

提供完整的黄历信息接口定义和辅助函数

数据来源：MingAI src/lib/calendar.ts
注意：实际日历计算需要配合 lunar-python 或类似库使用
"""
from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass
from datetime import date


class ShengXiao(TypedDict):
    """生肖信息"""
    year: str   # 年生肖
    month: str  # 月生肖
    day: str    # 日生肖


class GanZhi(TypedDict):
    """干支信息"""
    year: str   # 年柱
    month: str  # 月柱
    day: str    # 日柱
    time: str   # 时柱


class NaYin(TypedDict):
    """纳音信息"""
    year: str
    month: str
    day: str


class JieQiInfo(TypedDict):
    """节气信息"""
    name: str   # 节气名
    date: str   # 日期 YYYY-MM-DD
    time: str   # 时间 HH:mm:ss


class JieQi(TypedDict):
    """节气"""
    current: Optional[JieQiInfo]  # 当前节气
    next: Optional[JieQiInfo]     # 下一节气


class ChongSha(TypedDict):
    """冲煞信息"""
    chong: str  # 冲什么
    sha: str    # 煞方位


class ShenWei(TypedDict):
    """神位信息"""
    cai_shen: str      # 财神位
    xi_shen: str       # 喜神位
    fu_shen: str       # 福神位
    yang_gui_shen: str # 阳贵神


class Xiu(TypedDict):
    """二十八宿信息"""
    name: str   # 宿名
    gong: str   # 宫位
    luck: str   # 吉凶


class CalendarAlmanacData(TypedDict):
    """完整黄历数据结构"""
    # 基础日期信息
    solar_date: str           # 公历日期 YYYY-MM-DD
    solar_date_chinese: str   # 公历日期中文
    weekday: str              # 星期几
    lunar_date: str           # 农历日期
    lunar_month_day: str      # 农历月日
    
    # 生肖
    sheng_xiao: ShengXiao
    
    # 干支
    gan_zhi: GanZhi
    
    # 纳音
    na_yin: NaYin
    
    # 节气
    jie_qi: JieQi
    
    # 宜忌
    yi: List[str]             # 今日宜
    ji: List[str]             # 今日忌
    
    # 吉神凶煞
    ji_shen: List[str]        # 吉神宜趋
    xiong_sha: List[str]      # 凶神宜忌
    
    # 冲煞
    chong_sha: ChongSha
    
    # 空亡
    kong_wang: str
    
    # 胎神
    tai_shen: str
    
    # 值神（天神）
    zhi_shen: str
    
    # 神位
    shen_wei: ShenWei
    
    # 二十八宿
    xiu: Xiu
    
    # 月相
    yue_xiang: str
    
    # 六曜
    liu_yao: str
    
    # 九星
    jiu_xing: str
    
    # 物候
    wu_hou: str


# 黑道日值神
BLACK_DAY_ZHI_SHEN = ['天刑', '朱雀', '白虎', '天牢', '玄武', '勾陈']

# 黄道日值神
YELLOW_DAY_ZHI_SHEN = ['青龙', '明堂', '金匮', '天德', '玉堂', '司命']

# 星期中文名
WEEKDAY_NAMES = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']

# 农历月份中文
LUNAR_MONTH_NAMES = ['正', '二', '三', '四', '五', '六', '七', '八', '九', '十', '冬', '腊']

# 农历日期中文
LUNAR_DAY_NAMES = [
    '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
    '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十',
]

# 二十四节气
SOLAR_TERMS = [
    '小寒', '大寒', '立春', '雨水', '惊蛰', '春分',
    '清明', '谷雨', '立夏', '小满', '芒种', '夏至',
    '小暑', '大暑', '立秋', '处暑', '白露', '秋分',
    '寒露', '霜降', '立冬', '小雪', '大雪', '冬至',
]

# 十二生肖
ZODIAC_ANIMALS = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']

# 六曜
LIU_YAO = ['先胜', '友引', '先负', '佛灭', '大安', '赤口']

# 月相
MOON_PHASES = {
    1: '朔月', 2: '既朔', 3: '蛾眉新月', 7: '上弦月', 8: '上弦',
    15: '望月', 16: '既望', 22: '下弦月', 23: '下弦', 30: '晦月',
}


def is_black_day(zhi_shen: str) -> bool:
    """
    判断是否为黑道日
    
    Args:
        zhi_shen: 值神名称
        
    Returns:
        是否为黑道日
    """
    return any(b in zhi_shen for b in BLACK_DAY_ZHI_SHEN)


def is_yellow_day(zhi_shen: str) -> bool:
    """
    判断是否为黄道日
    
    Args:
        zhi_shen: 值神名称
        
    Returns:
        是否为黄道日
    """
    return any(y in zhi_shen for y in YELLOW_DAY_ZHI_SHEN)


def get_zhi_shen_desc(zhi_shen: str) -> str:
    """
    获取值神的吉凶描述
    
    Args:
        zhi_shen: 值神名称
        
    Returns:
        带吉凶标注的值神描述
    """
    if is_black_day(zhi_shen):
        return f'{zhi_shen}(黑道日)'
    return f'{zhi_shen}(黄道日)'


def get_weekday_chinese(weekday_index: int) -> str:
    """
    获取星期中文名
    
    Args:
        weekday_index: 星期索引 (0=周日, 1=周一, ...)
        
    Returns:
        中文星期名
    """
    return WEEKDAY_NAMES[weekday_index % 7]


def get_lunar_month_name(month: int, is_leap: bool = False) -> str:
    """
    获取农历月份中文名
    
    Args:
        month: 月份 (1-12)
        is_leap: 是否闰月
        
    Returns:
        农历月份名
    """
    prefix = '闰' if is_leap else ''
    return f'{prefix}{LUNAR_MONTH_NAMES[month - 1]}月'


def get_lunar_day_name(day: int) -> str:
    """
    获取农历日期中文名
    
    Args:
        day: 日期 (1-30)
        
    Returns:
        农历日期名
    """
    if 1 <= day <= 30:
        return LUNAR_DAY_NAMES[day - 1]
    return str(day)


def get_zodiac_animal(year: int) -> str:
    """
    获取年份对应的生肖
    
    Args:
        year: 公历年份
        
    Returns:
        生肖名称
    """
    # 以1900年为鼠年基准
    index = (year - 1900) % 12
    return ZODIAC_ANIMALS[index]


def get_moon_phase(lunar_day: int) -> str:
    """
    获取月相名称
    
    Args:
        lunar_day: 农历日期 (1-30)
        
    Returns:
        月相名称
    """
    return MOON_PHASES.get(lunar_day, '')


def format_solar_date_chinese(d: date) -> str:
    """
    格式化公历日期为中文
    
    Args:
        d: 日期对象
        
    Returns:
        中文格式日期（如 "2026年1月17日"）
    """
    return f'{d.year}年{d.month}月{d.day}日'


def create_empty_almanac(d: date) -> CalendarAlmanacData:
    """
    创建空的黄历数据结构
    
    Args:
        d: 日期对象
        
    Returns:
        空的黄历数据结构
    """
    return {
        'solar_date': d.isoformat(),
        'solar_date_chinese': format_solar_date_chinese(d),
        'weekday': get_weekday_chinese(d.weekday() + 1),  # Python weekday() 0=周一
        'lunar_date': '',
        'lunar_month_day': '',
        'sheng_xiao': {'year': '', 'month': '', 'day': ''},
        'gan_zhi': {'year': '', 'month': '', 'day': '', 'time': ''},
        'na_yin': {'year': '', 'month': '', 'day': ''},
        'jie_qi': {'current': None, 'next': None},
        'yi': [],
        'ji': [],
        'ji_shen': [],
        'xiong_sha': [],
        'chong_sha': {'chong': '', 'sha': ''},
        'kong_wang': '',
        'tai_shen': '',
        'zhi_shen': '',
        'shen_wei': {'cai_shen': '', 'xi_shen': '', 'fu_shen': '', 'yang_gui_shen': ''},
        'xiu': {'name': '', 'gong': '', 'luck': ''},
        'yue_xiang': '',
        'liu_yao': '',
        'jiu_xing': '',
        'wu_hou': '',
    }


# 导出
__all__ = [
    'CalendarAlmanacData',
    'ShengXiao',
    'GanZhi',
    'NaYin',
    'JieQi',
    'JieQiInfo',
    'ChongSha',
    'ShenWei',
    'Xiu',
    'BLACK_DAY_ZHI_SHEN',
    'YELLOW_DAY_ZHI_SHEN',
    'WEEKDAY_NAMES',
    'LUNAR_MONTH_NAMES',
    'LUNAR_DAY_NAMES',
    'SOLAR_TERMS',
    'ZODIAC_ANIMALS',
    'LIU_YAO',
    'MOON_PHASES',
    'is_black_day',
    'is_yellow_day',
    'get_zhi_shen_desc',
    'get_weekday_chinese',
    'get_lunar_month_name',
    'get_lunar_day_name',
    'get_zodiac_animal',
    'get_moon_phase',
    'format_solar_date_chinese',
    'create_empty_almanac',
]
