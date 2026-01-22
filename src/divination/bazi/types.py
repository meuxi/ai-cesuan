"""
八字类型定义
参考 mingpan 的 types.ts 实现
"""
from typing import TypedDict, List, Optional, Dict
from enum import Enum


class PillarType(str, Enum):
    """柱位类型"""
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    HOUR = 'hour'


class WuXing(str, Enum):
    """五行"""
    MU = '木'
    HUO = '火'
    TU = '土'
    JIN = '金'
    SHUI = '水'


class YinYang(str, Enum):
    """阴阳"""
    YANG = '阳'
    YIN = '阴'


class TenGod(str, Enum):
    """十神"""
    BI_JIAN = '比肩'
    JIE_CAI = '劫财'
    SHI_SHEN = '食神'
    SHANG_GUAN = '伤官'
    PIAN_CAI = '偏财'
    ZHENG_CAI = '正财'
    QI_SHA = '七杀'
    ZHENG_GUAN = '正官'
    PIAN_YIN = '偏印'
    ZHENG_YIN = '正印'


class Pillar(TypedDict):
    """柱信息"""
    gan: str           # 天干
    zhi: str           # 地支
    gan_zhi: str       # 干支组合
    gan_wuxing: str    # 天干五行
    zhi_wuxing: str    # 地支五行
    nayin: str         # 纳音
    nayin_wuxing: str  # 纳音五行


class HiddenStem(TypedDict):
    """藏干信息"""
    stem: str          # 藏干
    power: float       # 力量（本气1.0，中气0.5，余气0.3）
    is_main: bool      # 是否本气


class BaziChart(TypedDict):
    """八字盘信息"""
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str           # 日主
    day_master_wuxing: str    # 日主五行
    day_master_yinyang: str   # 日主阴阳


class TenGodInfo(TypedDict):
    """十神信息"""
    name: str          # 十神名称
    position: str      # 位置
    strength: float    # 力量
    interpretation: str  # 解读


class TenGodDistribution(TypedDict):
    """十神分布"""
    bi_jian: int
    jie_cai: int
    shi_shen: int
    shang_guan: int
    pian_cai: int
    zheng_cai: int
    qi_sha: int
    zheng_guan: int
    pian_yin: int
    zheng_yin: int


class TenGodAnalysis(TypedDict):
    """十神分析结果"""
    distribution: Dict[str, int]      # 分布统计
    details: List[TenGodInfo]         # 详细信息
    combinations: List[Dict]          # 组合分析
    strength_analysis: Dict           # 旺衰分析
    summary: str                      # 总结
    suggestions: List[str]            # 建议


class WuXingAnalysis(TypedDict):
    """五行分析结果"""
    distribution: Dict[str, int]      # 分布统计
    dominant: Optional[str]           # 最旺五行
    weak: Optional[str]               # 最弱五行
    missing: List[str]                # 缺失五行
    balance: str                      # 平衡度评价
    suggestions: List[str]            # 建议
