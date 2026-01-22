"""
紫微斗数类型定义
"""
from typing import TypedDict, List, Optional, Dict
from enum import Enum


class WuXingJu(int, Enum):
    """五行局"""
    SHUI_ER = 2   # 水二局
    MU_SAN = 3    # 木三局
    JIN_SI = 4    # 金四局
    TU_WU = 5     # 土五局
    HUO_LIU = 6   # 火六局


class GongInfo(TypedDict):
    """宫位信息"""
    name: str              # 宫名
    dizhi: str             # 地支
    stars: List[str]       # 星曜列表
    evaluation: str        # 评价


class StarInfo(TypedDict):
    """星曜信息"""
    name: str              # 星名
    dizhi: str             # 所在地支
    nature: str            # 吉凶
    type: str              # 类型
    meaning: str           # 含义


class ZiweiPan(TypedDict):
    """紫微命盘信息"""
    # 基本信息
    datetime: str          # 时间
    gender: str            # 性别
    lunar_year: int        # 农历年
    lunar_month: int       # 农历月
    lunar_day: int         # 农历日
    shi_zhi: str           # 时支
    
    # 五行局
    wuxing_ju: int         # 五行局数
    
    # 宫位信息
    ming_gong: str         # 命宫地支
    shen_gong: str         # 身宫地支
    gong_layout: Dict[str, str]  # 十二宫布局
    
    # 星曜布局
    star_layout: Dict[str, str]  # {星名: 地支}


class ZiweiResult(TypedDict):
    """紫微斗数结果"""
    pan: ZiweiPan          # 命盘信息
    analysis: Dict         # 分析结果
    suggestions: List[str] # 建议
