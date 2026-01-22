"""
六爻类型定义
"""
from typing import TypedDict, List, Optional, Dict


class YaoInfo(TypedDict):
    """爻信息"""
    position: int           # 位置（1-6）
    branch: str             # 地支
    element: str            # 五行
    six_relation: str       # 六亲
    is_shi: bool            # 是否世爻
    is_ying: bool           # 是否应爻
    is_moving: bool         # 是否动爻
    monthly_strength: Optional[str]  # 月令旺衰
    daily_relation: Optional[str]    # 日辰关系
    fushen: Optional[Dict]           # 伏神
    jintui_shen: Optional[str]       # 进退神


class GuaInfo(TypedDict):
    """卦信息"""
    name: str               # 卦名
    palace_name: str        # 所属宫
    element: str            # 卦五行


class LiuyaoResult(TypedDict):
    """六爻结果"""
    ben_gua: GuaInfo        # 本卦
    bian_gua: Optional[GuaInfo]  # 变卦
    lines: List[YaoInfo]    # 六爻信息
    enhanced: bool          # 是否增强分析
    analysis_hints: List[str]  # 分析提示
