"""
奇门遁甲类型定义
参考 mingpan 的 types.ts 实现
"""
from typing import TypedDict, List, Optional, Dict
from enum import Enum


class PanStyle(str, Enum):
    """盘式类型"""
    SHI_PAN = '时盘'
    RI_PAN = '日盘'
    YUE_PAN = '月盘'
    NIAN_PAN = '年盘'


class PanType(str, Enum):
    """盘型"""
    ZHUAN_PAN = '转盘'
    FEI_PAN = '飞盘'


class GongInfo(TypedDict):
    """宫位信息"""
    gong: int              # 宫位（1-9）
    gong_name: str         # 宫名（坎一宫等）
    tian_gan: str          # 天盘天干
    di_gan: str            # 地盘天干
    men: str               # 八门
    xing: str              # 九星
    shen: str              # 八神
    wuxing: str            # 五行


class GeJuInfo(TypedDict):
    """格局信息"""
    name: str              # 格局名称
    gong: int              # 所在宫位
    type: str              # 类型（ji/xiong/zhong）
    meaning: str           # 含义


class XunShouInfo(TypedDict):
    """旬首信息"""
    xun_shou: str          # 旬首（甲子等）
    liu_yi: str            # 六仪（戊己庚辛壬癸）
    xun_kong: List[str]    # 旬空地支


class QimenPan(TypedDict):
    """奇门盘信息"""
    # 基本信息
    datetime: str          # 时间
    pan_style: str         # 盘式
    pan_type: str          # 盘型
    ju_shu: int            # 局数
    is_yang: bool          # 是否阳遁
    yuan: str              # 上中下元
    
    # 干支信息
    year_gz: str           # 年干支
    month_gz: str          # 月干支
    day_gz: str            # 日干支
    hour_gz: str           # 时干支
    
    # 旬首信息
    xun_shou: XunShouInfo
    
    # 值符值使
    zhi_fu: str            # 值符星
    zhi_shi: str           # 值使门
    zhi_fu_gong: int       # 值符落宫
    zhi_shi_gong: int      # 值使落宫
    
    # 九宫布局
    jiu_gong: List[GongInfo]
    
    # 格局分析
    ge_ju: Dict


class QimenResult(TypedDict):
    """奇门遁甲结果"""
    pan: QimenPan          # 盘信息
    analysis: Dict         # 分析结果
    suggestions: List[str] # 建议
