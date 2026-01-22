"""
大六壬类型定义
"""
from typing import TypedDict, List, Optional, Dict
from enum import Enum


class KeInfo(TypedDict):
    """课信息"""
    name: str           # 课名（第一课等）
    shang: str          # 上神
    xia: str            # 下神


class SanChuanInfo(TypedDict):
    """三传信息"""
    chu_chuan: str      # 初传
    zhong_chuan: str    # 中传
    mo_chuan: str       # 末传
    type: str           # 三传类型
    interpretation: str # 解释


class TianJiangInfo(TypedDict):
    """天将信息"""
    position: str       # 位置
    dizhi: str          # 地支
    jiang: str          # 天将
    nature: str         # 吉凶
    meaning: str        # 含义


class DaliurenPan(TypedDict):
    """大六壬盘信息"""
    datetime: str       # 时间
    year_gz: str        # 年干支
    month_gz: str       # 月干支
    day_gz: str         # 日干支
    hour_gz: str        # 时干支
    yue_jiang: str      # 月将
    di_pan: Dict[int, str]   # 地盘
    tian_pan: Dict[int, str] # 天盘
    si_ke: List[KeInfo]      # 四课
    san_chuan: SanChuanInfo  # 三传
    tian_jiang: Dict[str, str]  # 天将布局


class DaliurenResult(TypedDict):
    """大六壬结果"""
    pan: DaliurenPan    # 盘信息
    analysis: Dict      # 分析结果
    suggestions: List[str]  # 建议
