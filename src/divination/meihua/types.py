"""
梅花易数类型定义
"""
from typing import TypedDict, Optional


class GuaInfo(TypedDict):
    """卦信息"""
    name: str               # 卦名
    number: int             # 卦数
    wuxing: str             # 五行
    xiang: str              # 卦象


class MeihuaResult(TypedDict):
    """梅花易数结果"""
    num1: int               # 第一个数
    num2: int               # 第二个数
    shang_gua: GuaInfo      # 上卦
    xia_gua: GuaInfo        # 下卦
    ben_gua: str            # 本卦
    hu_gua: str             # 互卦
    bian_gua: str           # 变卦
    dong_yao: int           # 动爻
