"""
合婚类型定义
"""
from typing import TypedDict


class HehunResult(TypedDict):
    """合婚结果"""
    male_year: int           # 男方年份
    female_year: int         # 女方年份
    male_ganzhi: str         # 男方干支
    female_ganzhi: str       # 女方干支
    male_gong: str           # 男方宫位
    female_gong: str         # 女方宫位
    male_wuxing: str         # 男方五行
    female_wuxing: str       # 女方五行
    relation: str            # 关系（生/克/比和等）
    score: int               # 配对分数
