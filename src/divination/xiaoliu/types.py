"""
小六壬类型定义
"""
from typing import TypedDict, Optional


class LiuGodInfo(TypedDict):
    """六神信息"""
    name: str               # 六神名称
    wuxing: str             # 五行
    fangwei: str            # 方位
    jixiong: str            # 吉凶
    tiangan: str            # 天干
    dizhi: str              # 地支
    renwu: str              # 人物
    shenti: str             # 身体
    hanyi: str              # 含义
    xiangjie: str           # 详解


class XiaoliuResult(TypedDict):
    """小六壬结果"""
    month: int              # 月份
    day: int                # 日期
    hour: int               # 时辰
    month_gong: int         # 月落宫
    day_gong: int           # 日落宫
    hour_gong: int          # 时落宫
    final_gong: int         # 最终落宫
    liu_god: str            # 六神名称
    liu_god_info: LiuGodInfo  # 六神详细信息
