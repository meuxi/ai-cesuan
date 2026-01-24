"""
占卜排盘统一响应模型

提供各类排盘结果的统一数据结构，确保前后端数据格式一致。
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============= 基础模型 =============

class TimeInfo(BaseModel):
    """时间信息"""
    year: int
    month: int
    day: int
    hour: int
    minute: int = 0
    ganzhi_year: Optional[str] = None
    ganzhi_month: Optional[str] = None
    ganzhi_day: Optional[str] = None
    ganzhi_hour: Optional[str] = None
    jieqi: Optional[str] = None


class GanZhi(BaseModel):
    """干支"""
    gan: str = Field(..., description="天干")
    zhi: str = Field(..., description="地支")
    wuxing: Optional[str] = Field(None, description="五行")


# ============= 紫微斗数响应 =============

class ZiweiStar(BaseModel):
    """紫微星曜"""
    name: str
    type: str  # major/minor/helper
    brightness: Optional[str] = None
    mutagen: Optional[str] = None  # 四化：禄权科忌


class ZiweiPalace(BaseModel):
    """紫微宫位"""
    index: int
    name: str
    heavenly_stem: str
    earthly_branch: str
    major_stars: List[ZiweiStar] = []
    minor_stars: List[ZiweiStar] = []
    helper_stars: List[ZiweiStar] = []


class ZiweiPaipanResponse(BaseModel):
    """紫微排盘响应"""
    birth_info: Dict[str, Any]
    soul_palace: str  # 命宫
    body_palace: str  # 身宫
    five_element: str  # 五行局
    palaces: List[ZiweiPalace]
    da_xian: Optional[List[Dict]] = None  # 大限


# ============= 奇门遁甲响应 =============

class QimenGong(BaseModel):
    """奇门九宫"""
    position: int  # 1-9
    direction: str  # 方位
    men: str  # 八门
    xing: str  # 九星
    shen: str  # 八神
    tianpan: str  # 天盘干
    dipan: str  # 地盘干
    palace_stars: List[str] = []


class QimenPaipanResponse(BaseModel):
    """奇门排盘响应"""
    time_info: TimeInfo
    pan_info: Dict[str, str]  # 局数、遁类等
    jiugong: List[QimenGong]
    zhifu: str  # 值符
    zhishi: str  # 值使
    summary: str


# ============= 大六壬响应 =============

class DaliurenSike(BaseModel):
    """大六壬四课"""
    position: int
    upper: str  # 上神
    lower: str  # 下神
    relation: Optional[str] = None


class DaliurenSanchuan(BaseModel):
    """大六壬三传"""
    position: str  # 初传/中传/末传
    branch: str  # 地支
    god: str  # 天将


class DaliurenPaipanResponse(BaseModel):
    """大六壬排盘响应"""
    time_info: TimeInfo
    tianpan: Dict[str, str]  # 天盘
    sike: List[DaliurenSike]
    sanchuan: List[DaliurenSanchuan]
    tianjiang: List[str]  # 天将
    summary: str


# ============= 八字响应 =============

class BaziPillar(BaseModel):
    """八字柱"""
    gan: str
    zhi: str
    gan_wuxing: str
    zhi_wuxing: str
    zhi_cang: List[str] = []  # 地支藏干


class BaziPaipanResponse(BaseModel):
    """八字排盘响应"""
    sizhu: Dict[str, str]  # 四柱：year/month/day/hour
    pillars: List[BaziPillar]
    day_master: str  # 日主
    day_master_wuxing: str
    lunar_info: Optional[Dict] = None
    wuxing_count: Optional[Dict[str, int]] = None  # 五行统计


# ============= 六爻响应 =============

class LiuyaoLine(BaseModel):
    """六爻爻位"""
    index: int  # 1-6
    type: str  # 阳/阴
    is_moving: bool
    branch: str  # 地支
    element: str  # 五行
    six_relation: str  # 六亲
    six_beast: Optional[str] = None  # 六神
    fu_shen: Optional[Dict] = None  # 伏神


class LiuyaoPaipanResponse(BaseModel):
    """六爻排盘响应"""
    hexagram_name: str  # 卦名
    palace_name: str  # 宫名
    palace_element: str  # 宫五行
    transformed_name: Optional[str] = None  # 变卦名
    lines: List[LiuyaoLine]
    shi_yao: int  # 世爻位置
    ying_yao: int  # 应爻位置


# ============= 梅花易数响应 =============

class MeihuaGua(BaseModel):
    """梅花卦象"""
    name: str
    nature: str  # 卦性
    element: str  # 五行
    number: int  # 先天数


class MeihuaPaipanResponse(BaseModel):
    """梅花易数排盘响应"""
    upper_gua: MeihuaGua  # 上卦/体卦
    lower_gua: MeihuaGua  # 下卦/用卦
    ben_gua: str  # 本卦名
    dong_yao: int  # 动爻
    bian_gua: Optional[str] = None  # 变卦名
    ti_yong: Dict[str, str]  # 体用关系
    time_info: Optional[TimeInfo] = None
