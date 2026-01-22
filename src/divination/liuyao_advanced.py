"""
六爻高级分析模块 - 空亡体系、旺衰五态、神系分析、三合六冲

参考来源：MingAI-master 六爻分析系统
功能清单：
1. 空亡体系（真空/动不空/冲空/临月建）
2. 旺衰五态（旺相休囚死）
3. 月建日辰作用判定
4. 十二长生阶段
5. 三合局/半合分析
6. 六冲卦判定
7. 原神/忌神/仇神体系
8. 动爻变化分析（化进/化退/回头生克/化空/化墓/伏吟/反吟）
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


# ============= 类型定义 =============

class WangShuai(Enum):
    """旺衰五态"""
    WANG = "旺"      # 当令最旺
    XIANG = "相"     # 次旺，受生
    XIU = "休"       # 休息，生他
    QIU = "囚"       # 受克无力
    SI = "死"        # 克他耗力


class KongWangState(Enum):
    """空亡状态"""
    NOT_KONG = "不空"           # 不在空亡地支
    KONG_STATIC = "真空"        # 静爻空亡（真空无力）
    KONG_CHANGING = "动空"      # 动爻空亡（动不为空）
    KONG_RI_CHONG = "冲空"      # 日辰冲空（冲空不空）
    KONG_YUE_JIAN = "临建"      # 临月建（临建不空）


class YaoAction(Enum):
    """月建日辰作用类型"""
    SHENG = "生"     # 生
    KE = "克"        # 克
    FU = "扶"        # 比和（扶）
    CHONG = "冲"     # 六冲
    HE = "合"        # 六合
    PO = "破"        # 相破
    NONE = "无"      # 无作用


class SpecialStatus(Enum):
    """爻的特殊状态"""
    NONE = "无"
    AN_DONG = "暗动"    # 静爻被日辰冲动
    RI_PO = "日破"      # 被日辰冲破


class HuaType(Enum):
    """动爻变化类型"""
    HUA_JIN = "化进"       # 变爻地支序数增加
    HUA_TUI = "化退"       # 变爻地支序数减少
    HUI_TOU_SHENG = "回头生"  # 变爻五行生本爻
    HUI_TOU_KE = "回头克"    # 变爻五行克本爻
    HUA_KONG = "化空"       # 变爻落入空亡
    HUA_MU = "化墓"         # 变爻为本爻的墓库
    FU_YIN = "伏吟"         # 变爻与本爻相同
    FAN_YIN = "反吟"        # 变爻与本爻六冲
    NONE = "无"


class ShiErChangSheng(Enum):
    """十二长生阶段"""
    CHANG_SHENG = "长生"
    MU_YU = "沐浴"
    GUAN_DAI = "冠带"
    LIN_GUAN = "临官"
    DI_WANG = "帝旺"
    SHUAI = "衰"
    BING = "病"
    SI = "死"
    MU = "墓"
    JUE = "绝"
    TAI = "胎"
    YANG = "养"


# ============= 数据表 =============

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 地支序数
DIZHI_INDEX: Dict[str, int] = {
    '子': 0, '丑': 1, '寅': 2, '卯': 3, '辰': 4, '巳': 5,
    '午': 6, '未': 7, '申': 8, '酉': 9, '戌': 10, '亥': 11
}

# 天干序数
TIANGAN_INDEX: Dict[str, int] = {
    '甲': 0, '乙': 1, '丙': 2, '丁': 3, '戊': 4,
    '己': 5, '庚': 6, '辛': 7, '壬': 8, '癸': 9
}

# 地支五行
DIZHI_WUXING: Dict[str, str] = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 天干五行
TIANGAN_WUXING: Dict[str, str] = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 五行生关系：A生B
WUXING_SHENG: Dict[str, str] = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
}

# 五行克关系：A克B
WUXING_KE: Dict[str, str] = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
}

# 旬空表（六甲旬对应的空亡地支）
XUN_KONG_TABLE: Dict[str, Tuple[str, str]] = {
    '甲子旬': ('戌', '亥'),
    '甲戌旬': ('申', '酉'),
    '甲申旬': ('午', '未'),
    '甲午旬': ('辰', '巳'),
    '甲辰旬': ('寅', '卯'),
    '甲寅旬': ('子', '丑'),
}

# 六冲表
LIU_CHONG: Dict[str, str] = {
    '子': '午', '丑': '未', '寅': '申', '卯': '酉', '辰': '戌', '巳': '亥',
    '午': '子', '未': '丑', '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳'
}

# 六合表及合化结果
LIU_HE: Dict[str, Dict[str, str]] = {
    '子': {'partner': '丑', 'result': '土'},
    '丑': {'partner': '子', 'result': '土'},
    '寅': {'partner': '亥', 'result': '木'},
    '亥': {'partner': '寅', 'result': '木'},
    '卯': {'partner': '戌', 'result': '火'},
    '戌': {'partner': '卯', 'result': '火'},
    '辰': {'partner': '酉', 'result': '金'},
    '酉': {'partner': '辰', 'result': '金'},
    '巳': {'partner': '申', 'result': '水'},
    '申': {'partner': '巳', 'result': '水'},
    '午': {'partner': '未', 'result': '火'},
    '未': {'partner': '午', 'result': '火'},
}

# 六害表
LIU_HAI: Dict[str, str] = {
    '子': '未', '丑': '午', '寅': '巳', '卯': '辰',
    '辰': '卯', '巳': '寅', '午': '丑', '未': '子',
    '申': '亥', '酉': '戌', '戌': '酉', '亥': '申'
}

# 相刑表
XIANG_XING: Dict[str, List[str]] = {
    '寅': ['巳', '申'],  # 寅巳申三刑
    '巳': ['寅', '申'],
    '申': ['寅', '巳'],
    '丑': ['戌', '未'],  # 丑戌未三刑
    '戌': ['丑', '未'],
    '未': ['丑', '戌'],
    '子': ['卯'],        # 子卯相刑
    '卯': ['子'],
    '辰': ['辰'],        # 自刑
    '午': ['午'],
    '酉': ['酉'],
    '亥': ['亥'],
}

# 相破表
XIANG_PO: Dict[str, str] = {
    '子': '酉', '酉': '子',
    '丑': '辰', '辰': '丑',
    '寅': '亥', '亥': '寅',
    '卯': '午', '午': '卯',
    '巳': '申', '申': '巳',
    '未': '戌', '戌': '未',
}

# 五行墓库表
WUXING_MU: Dict[str, str] = {
    '木': '未',  # 木墓在未
    '火': '戌',  # 火墓在戌
    '土': '戌',  # 土墓在戌
    '金': '丑',  # 金墓在丑
    '水': '辰',  # 水墓在辰
}

# 月令旺衰表
WANG_SHUAI_TABLE: Dict[str, Dict[str, WangShuai]] = {
    # 春季：木旺火相水休金囚土死
    '寅': {'木': WangShuai.WANG, '火': WangShuai.XIANG, '水': WangShuai.XIU, '金': WangShuai.QIU, '土': WangShuai.SI},
    '卯': {'木': WangShuai.WANG, '火': WangShuai.XIANG, '水': WangShuai.XIU, '金': WangShuai.QIU, '土': WangShuai.SI},
    '辰': {'土': WangShuai.WANG, '金': WangShuai.XIANG, '火': WangShuai.XIU, '木': WangShuai.QIU, '水': WangShuai.SI},
    # 夏季：火旺土相木休水囚金死
    '巳': {'火': WangShuai.WANG, '土': WangShuai.XIANG, '木': WangShuai.XIU, '水': WangShuai.QIU, '金': WangShuai.SI},
    '午': {'火': WangShuai.WANG, '土': WangShuai.XIANG, '木': WangShuai.XIU, '水': WangShuai.QIU, '金': WangShuai.SI},
    '未': {'土': WangShuai.WANG, '金': WangShuai.XIANG, '火': WangShuai.XIU, '木': WangShuai.QIU, '水': WangShuai.SI},
    # 秋季：金旺水相土休火囚木死
    '申': {'金': WangShuai.WANG, '水': WangShuai.XIANG, '土': WangShuai.XIU, '火': WangShuai.QIU, '木': WangShuai.SI},
    '酉': {'金': WangShuai.WANG, '水': WangShuai.XIANG, '土': WangShuai.XIU, '火': WangShuai.QIU, '木': WangShuai.SI},
    '戌': {'土': WangShuai.WANG, '金': WangShuai.XIANG, '火': WangShuai.XIU, '木': WangShuai.QIU, '水': WangShuai.SI},
    # 冬季：水旺木相金休土囚火死
    '亥': {'水': WangShuai.WANG, '木': WangShuai.XIANG, '金': WangShuai.XIU, '土': WangShuai.QIU, '火': WangShuai.SI},
    '子': {'水': WangShuai.WANG, '木': WangShuai.XIANG, '金': WangShuai.XIU, '土': WangShuai.QIU, '火': WangShuai.SI},
    '丑': {'土': WangShuai.WANG, '金': WangShuai.XIANG, '火': WangShuai.XIU, '木': WangShuai.QIU, '水': WangShuai.SI},
}

# 三合局表
SAN_HE_TABLE: List[Dict] = [
    {'branches': ['申', '子', '辰'], 'result': '水', 'name': '申子辰合水局'},
    {'branches': ['亥', '卯', '未'], 'result': '木', 'name': '亥卯未合木局'},
    {'branches': ['寅', '午', '戌'], 'result': '火', 'name': '寅午戌合火局'},
    {'branches': ['巳', '酉', '丑'], 'result': '金', 'name': '巳酉丑合金局'},
]

# 半合表
BAN_HE_TABLE: List[Dict] = [
    # 生方半合（长生+帝旺）
    {'branches': ['申', '子'], 'result': '水', 'type': 'sheng'},
    {'branches': ['亥', '卯'], 'result': '木', 'type': 'sheng'},
    {'branches': ['寅', '午'], 'result': '火', 'type': 'sheng'},
    {'branches': ['巳', '酉'], 'result': '金', 'type': 'sheng'},
    # 墓方半合（帝旺+墓）
    {'branches': ['子', '辰'], 'result': '水', 'type': 'mu'},
    {'branches': ['卯', '未'], 'result': '木', 'type': 'mu'},
    {'branches': ['午', '戌'], 'result': '火', 'type': 'mu'},
    {'branches': ['酉', '丑'], 'result': '金', 'type': 'mu'},
]

# 五行十二长生表
WUXING_CHANG_SHENG: Dict[str, Dict[str, ShiErChangSheng]] = {
    '木': {
        '亥': ShiErChangSheng.CHANG_SHENG, '子': ShiErChangSheng.MU_YU, 
        '丑': ShiErChangSheng.GUAN_DAI, '寅': ShiErChangSheng.LIN_GUAN,
        '卯': ShiErChangSheng.DI_WANG, '辰': ShiErChangSheng.SHUAI, 
        '巳': ShiErChangSheng.BING, '午': ShiErChangSheng.SI,
        '未': ShiErChangSheng.MU, '申': ShiErChangSheng.JUE, 
        '酉': ShiErChangSheng.TAI, '戌': ShiErChangSheng.YANG
    },
    '火': {
        '寅': ShiErChangSheng.CHANG_SHENG, '卯': ShiErChangSheng.MU_YU, 
        '辰': ShiErChangSheng.GUAN_DAI, '巳': ShiErChangSheng.LIN_GUAN,
        '午': ShiErChangSheng.DI_WANG, '未': ShiErChangSheng.SHUAI, 
        '申': ShiErChangSheng.BING, '酉': ShiErChangSheng.SI,
        '戌': ShiErChangSheng.MU, '亥': ShiErChangSheng.JUE, 
        '子': ShiErChangSheng.TAI, '丑': ShiErChangSheng.YANG
    },
    '土': {  # 土寄火
        '寅': ShiErChangSheng.CHANG_SHENG, '卯': ShiErChangSheng.MU_YU, 
        '辰': ShiErChangSheng.GUAN_DAI, '巳': ShiErChangSheng.LIN_GUAN,
        '午': ShiErChangSheng.DI_WANG, '未': ShiErChangSheng.SHUAI, 
        '申': ShiErChangSheng.BING, '酉': ShiErChangSheng.SI,
        '戌': ShiErChangSheng.MU, '亥': ShiErChangSheng.JUE, 
        '子': ShiErChangSheng.TAI, '丑': ShiErChangSheng.YANG
    },
    '金': {
        '巳': ShiErChangSheng.CHANG_SHENG, '午': ShiErChangSheng.MU_YU, 
        '未': ShiErChangSheng.GUAN_DAI, '申': ShiErChangSheng.LIN_GUAN,
        '酉': ShiErChangSheng.DI_WANG, '戌': ShiErChangSheng.SHUAI, 
        '亥': ShiErChangSheng.BING, '子': ShiErChangSheng.SI,
        '丑': ShiErChangSheng.MU, '寅': ShiErChangSheng.JUE, 
        '卯': ShiErChangSheng.TAI, '辰': ShiErChangSheng.YANG
    },
    '水': {
        '申': ShiErChangSheng.CHANG_SHENG, '酉': ShiErChangSheng.MU_YU, 
        '戌': ShiErChangSheng.GUAN_DAI, '亥': ShiErChangSheng.LIN_GUAN,
        '子': ShiErChangSheng.DI_WANG, '丑': ShiErChangSheng.SHUAI, 
        '寅': ShiErChangSheng.BING, '卯': ShiErChangSheng.SI,
        '辰': ShiErChangSheng.MU, '巳': ShiErChangSheng.JUE, 
        '午': ShiErChangSheng.TAI, '未': ShiErChangSheng.YANG
    }
}

# 十二长生强弱分类
CHANG_SHENG_STRENGTH: Dict[ShiErChangSheng, str] = {
    ShiErChangSheng.CHANG_SHENG: 'strong',
    ShiErChangSheng.MU_YU: 'medium',
    ShiErChangSheng.GUAN_DAI: 'strong',
    ShiErChangSheng.LIN_GUAN: 'strong',
    ShiErChangSheng.DI_WANG: 'strong',
    ShiErChangSheng.SHUAI: 'medium',
    ShiErChangSheng.BING: 'weak',
    ShiErChangSheng.SI: 'weak',
    ShiErChangSheng.MU: 'weak',
    ShiErChangSheng.JUE: 'weak',
    ShiErChangSheng.TAI: 'medium',
    ShiErChangSheng.YANG: 'medium'
}

# 十二长生描述
CHANG_SHENG_DESC: Dict[ShiErChangSheng, str] = {
    ShiErChangSheng.CHANG_SHENG: '如人初生，生机勃勃，有发展潜力',
    ShiErChangSheng.MU_YU: '如人沐浴，不稳定，易有波折',
    ShiErChangSheng.GUAN_DAI: '如人成年，渐入佳境，开始有成就',
    ShiErChangSheng.LIN_GUAN: '如人当官，权力渐盛，事业上升',
    ShiErChangSheng.DI_WANG: '如帝王之旺，鼎盛之极，最为有力',
    ShiErChangSheng.SHUAI: '盛极而衰，力量开始减弱',
    ShiErChangSheng.BING: '如人生病，力量衰弱，需要调养',
    ShiErChangSheng.SI: '气息将绝，力量极弱',
    ShiErChangSheng.MU: '入墓收藏，力量被封存',
    ShiErChangSheng.JUE: '气息已绝，最为无力',
    ShiErChangSheng.TAI: '如人受胎，开始孕育新生',
    ShiErChangSheng.YANG: '如人养育，等待时机出生'
}


# ============= 数据类 =============

@dataclass
class KongWangInfo:
    """旬空信息"""
    xun: str                        # 所属旬（甲子旬等）
    kong_dizhi: Tuple[str, str]     # 空亡地支


@dataclass
class YaoInfluence:
    """月建日辰影响"""
    month_action: YaoAction
    day_action: YaoAction
    description: str


@dataclass
class YaoStrength:
    """爻的综合强度"""
    wang_shuai: WangShuai           # 旺衰状态
    score: int                      # 0-100分
    factors: List[str]              # 影响因素
    is_strong: bool                 # 是否有力
    special_status: SpecialStatus  # 暗动/日破


@dataclass
class YaoChangeAnalysis:
    """动爻变化分析"""
    hua_type: HuaType
    original_zhi: str
    changed_zhi: str
    description: str


@dataclass
class ChangShengInfo:
    """十二长生信息"""
    stage: ShiErChangSheng
    strength: str  # strong/medium/weak
    description: str


@dataclass
class SanHeAnalysis:
    """三合局分析"""
    has_full_san_he: bool = False
    full_san_he: Optional[Dict] = None
    has_ban_he: bool = False
    ban_he: List[Dict] = field(default_factory=list)


@dataclass
class LiuChongGuaInfo:
    """六冲卦信息"""
    is_liu_chong_gua: bool
    description: Optional[str] = None


@dataclass
class ShenMember:
    """神系成员"""
    liu_qin: str            # 六亲
    wu_xing: str            # 五行
    positions: List[int]    # 爻位列表


@dataclass
class ShenSystem:
    """原神/忌神/仇神体系"""
    yuan_shen: Optional[ShenMember] = None   # 原神：生用神者
    ji_shen: Optional[ShenMember] = None     # 忌神：克用神者
    chou_shen: Optional[ShenMember] = None   # 仇神：克原神者


@dataclass
class ExtendedYaoInfo:
    """扩展爻信息"""
    index: int
    branch: str
    element: str
    liu_qin: str
    is_moving: bool
    kong_wang_state: KongWangState
    influence: YaoInfluence
    strength: YaoStrength
    change_analysis: Optional[YaoChangeAnalysis] = None
    chang_sheng: Optional[ChangShengInfo] = None


# ============= 核心计算函数 =============

def get_xun_from_day_ganzhi(day_gan: str, day_zhi: str) -> str:
    """根据日干支计算所属旬"""
    gan_index = TIANGAN_INDEX.get(day_gan, 0)
    zhi_index = DIZHI_INDEX.get(day_zhi, 0)
    # 计算旬首的地支索引
    xun_start_zhi_index = (zhi_index - gan_index + 12) % 12
    xun_names = {
        0: '甲子旬', 2: '甲寅旬', 4: '甲辰旬',
        6: '甲午旬', 8: '甲申旬', 10: '甲戌旬',
    }
    return xun_names.get(xun_start_zhi_index, '甲子旬')


def get_kong_wang(day_gan: str, day_zhi: str) -> KongWangInfo:
    """根据日柱获取旬空信息"""
    xun = get_xun_from_day_ganzhi(day_gan, day_zhi)
    return KongWangInfo(
        xun=xun,
        kong_dizhi=XUN_KONG_TABLE.get(xun, ('戌', '亥'))
    )


def check_yao_kong_wang(
    yao_zhi: str,
    kong_wang: KongWangInfo,
    month_zhi: str,
    day_zhi: str,
    is_changing: bool
) -> KongWangState:
    """检查爻的空亡状态"""
    # 不在空亡地支中，不空
    if yao_zhi not in kong_wang.kong_dizhi:
        return KongWangState.NOT_KONG
    
    # 动爻不为空（动不为空）
    if is_changing:
        return KongWangState.KONG_CHANGING
    
    # 日辰冲空则不空
    if LIU_CHONG.get(yao_zhi) == day_zhi:
        return KongWangState.KONG_RI_CHONG
    
    # 临月建不空
    if yao_zhi == month_zhi:
        return KongWangState.KONG_YUE_JIAN
    
    # 真空
    return KongWangState.KONG_STATIC


def get_zhi_action(source_zhi: str, target_zhi: str) -> YaoAction:
    """获取地支对爻的作用（月建或日辰对爻）"""
    # 六冲
    if LIU_CHONG.get(source_zhi) == target_zhi:
        return YaoAction.CHONG
    
    # 六合
    if LIU_HE.get(source_zhi, {}).get('partner') == target_zhi:
        return YaoAction.HE
    
    # 相破
    if XIANG_PO.get(source_zhi) == target_zhi:
        return YaoAction.PO
    
    source_wuxing = DIZHI_WUXING.get(source_zhi, '')
    target_wuxing = DIZHI_WUXING.get(target_zhi, '')
    
    # 比和（扶）
    if source_wuxing == target_wuxing:
        return YaoAction.FU
    
    # 生
    if WUXING_SHENG.get(source_wuxing) == target_wuxing:
        return YaoAction.SHENG
    
    # 克
    if WUXING_KE.get(source_wuxing) == target_wuxing:
        return YaoAction.KE
    
    return YaoAction.NONE


def calculate_yao_influence(
    yao_zhi: str,
    month_zhi: str,
    day_zhi: str
) -> YaoInfluence:
    """计算月建日辰对爻的影响"""
    month_action = get_zhi_action(month_zhi, yao_zhi)
    day_action = get_zhi_action(day_zhi, yao_zhi)
    
    descriptions = []
    if month_action != YaoAction.NONE:
        descriptions.append(f"月{month_action.value}")
    if day_action != YaoAction.NONE:
        descriptions.append(f"日{day_action.value}")
    
    return YaoInfluence(
        month_action=month_action,
        day_action=day_action,
        description="，".join(descriptions) if descriptions else "无特殊作用"
    )


def calculate_wang_shuai(yao_element: str, month_zhi: str) -> WangShuai:
    """计算爻的旺衰状态"""
    month_table = WANG_SHUAI_TABLE.get(month_zhi, {})
    return month_table.get(yao_element, WangShuai.XIU)


def check_special_status(
    yao_zhi: str,
    day_zhi: str,
    is_changing: bool,
    wang_shuai: WangShuai
) -> SpecialStatus:
    """检查爻的特殊状态（暗动/日破）"""
    # 动爻不判断暗动/日破
    if is_changing:
        return SpecialStatus.NONE
    
    # 日辰冲爻
    if LIU_CHONG.get(day_zhi) == yao_zhi:
        # 旺相之爻被冲为暗动
        if wang_shuai in [WangShuai.WANG, WangShuai.XIANG]:
            return SpecialStatus.AN_DONG
        # 休囚死之爻被冲为日破
        else:
            return SpecialStatus.RI_PO
    
    return SpecialStatus.NONE


def calculate_yao_strength(
    yao_element: str,
    yao_zhi: str,
    month_zhi: str,
    day_zhi: str,
    is_changing: bool,
    kong_wang_state: KongWangState,
    influence: YaoInfluence
) -> YaoStrength:
    """计算爻的综合强度"""
    wang_shuai = calculate_wang_shuai(yao_element, month_zhi)
    special_status = check_special_status(yao_zhi, day_zhi, is_changing, wang_shuai)
    
    # 基础分数（根据旺衰）
    base_scores = {
        WangShuai.WANG: 80,
        WangShuai.XIANG: 65,
        WangShuai.XIU: 50,
        WangShuai.QIU: 35,
        WangShuai.SI: 20
    }
    score = base_scores.get(wang_shuai, 50)
    factors = [f"月令{wang_shuai.value}"]
    
    # 日辰作用调整
    if influence.day_action == YaoAction.SHENG:
        score += 10
        factors.append("日生")
    elif influence.day_action == YaoAction.KE:
        score -= 10
        factors.append("日克")
    elif influence.day_action == YaoAction.FU:
        score += 5
        factors.append("日扶")
    elif influence.day_action == YaoAction.CHONG:
        if special_status == SpecialStatus.AN_DONG:
            score += 15
            factors.append("暗动有力")
        elif special_status == SpecialStatus.RI_PO:
            score -= 20
            factors.append("日破无力")
    
    # 月建作用调整
    if influence.month_action == YaoAction.SHENG:
        score += 8
        factors.append("月生")
    elif influence.month_action == YaoAction.KE:
        score -= 8
        factors.append("月克")
    
    # 空亡调整
    if kong_wang_state == KongWangState.KONG_STATIC:
        score -= 30
        factors.append("真空无力")
    elif kong_wang_state == KongWangState.KONG_CHANGING:
        factors.append("动空待实")
    
    # 动爻加分
    if is_changing:
        score += 10
        factors.append("动爻有力")
    
    # 限制分数范围
    score = max(0, min(100, score))
    
    return YaoStrength(
        wang_shuai=wang_shuai,
        score=score,
        factors=factors,
        is_strong=score >= 50,
        special_status=special_status
    )


def calculate_change_analysis(
    original_zhi: str,
    changed_zhi: str,
    original_element: str,
    changed_element: str,
    kong_wang: KongWangInfo
) -> YaoChangeAnalysis:
    """分析动爻变化类型"""
    original_index = DIZHI_INDEX.get(original_zhi, 0)
    changed_index = DIZHI_INDEX.get(changed_zhi, 0)
    
    # 伏吟（变爻与本爻相同）
    if original_zhi == changed_zhi:
        return YaoChangeAnalysis(
            hua_type=HuaType.FU_YIN,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="伏吟，事多反复，不易成就"
        )
    
    # 反吟（变爻与本爻六冲）
    if LIU_CHONG.get(original_zhi) == changed_zhi:
        return YaoChangeAnalysis(
            hua_type=HuaType.FAN_YIN,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="反吟，事情反复变化，难以稳定"
        )
    
    # 化空（变爻落入空亡）
    if changed_zhi in kong_wang.kong_dizhi:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUA_KONG,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="化空，事情落空，难有结果"
        )
    
    # 化墓（变爻为本爻的墓库）
    if WUXING_MU.get(original_element) == changed_zhi:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUA_MU,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="化墓，力量被封存，难以发挥"
        )
    
    # 回头生（变爻五行生本爻）
    if WUXING_SHENG.get(changed_element) == original_element:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUI_TOU_SHENG,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="回头生，变爻生助本爻，吉利"
        )
    
    # 回头克（变爻五行克本爻）
    if WUXING_KE.get(changed_element) == original_element:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUI_TOU_KE,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="回头克，变爻克制本爻，不利"
        )
    
    # 化进/化退（基于地支序数）
    diff = (changed_index - original_index + 12) % 12
    if 1 <= diff <= 5:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUA_JIN,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="化进，力量增强，事情向前发展"
        )
    elif 7 <= diff <= 11:
        return YaoChangeAnalysis(
            hua_type=HuaType.HUA_TUI,
            original_zhi=original_zhi,
            changed_zhi=changed_zhi,
            description="化退，力量减弱，事情退缩"
        )
    
    return YaoChangeAnalysis(
        hua_type=HuaType.NONE,
        original_zhi=original_zhi,
        changed_zhi=changed_zhi,
        description="无特殊变化"
    )


def calculate_chang_sheng(yao_element: str, day_zhi: str) -> ChangShengInfo:
    """计算爻的十二长生阶段"""
    element_table = WUXING_CHANG_SHENG.get(yao_element, {})
    stage = element_table.get(day_zhi, ShiErChangSheng.SHUAI)
    strength = CHANG_SHENG_STRENGTH.get(stage, 'medium')
    description = CHANG_SHENG_DESC.get(stage, '')
    
    return ChangShengInfo(
        stage=stage,
        strength=strength,
        description=description
    )


def analyze_san_he(branches: List[str]) -> SanHeAnalysis:
    """分析三合局"""
    result = SanHeAnalysis()
    branch_set = set(branches)
    
    # 检查完整三合
    for san_he in SAN_HE_TABLE:
        if set(san_he['branches']).issubset(branch_set):
            positions = [i for i, b in enumerate(branches) if b in san_he['branches']]
            result.has_full_san_he = True
            result.full_san_he = {
                'name': san_he['name'],
                'result': san_he['result'],
                'positions': positions
            }
            break
    
    # 检查半合
    for ban_he in BAN_HE_TABLE:
        if set(ban_he['branches']).issubset(branch_set):
            positions = [i for i, b in enumerate(branches) if b in ban_he['branches']]
            result.has_ban_he = True
            result.ban_he.append({
                'branches': ban_he['branches'],
                'result': ban_he['result'],
                'type': ban_he['type'],
                'positions': positions
            })
    
    return result


def check_liu_chong_gua(ben_gua_branches: List[str]) -> LiuChongGuaInfo:
    """检查是否为六冲卦"""
    # 六冲卦：六爻地支两两相冲
    chong_count = 0
    for i in range(3):
        if LIU_CHONG.get(ben_gua_branches[i]) == ben_gua_branches[i + 3]:
            chong_count += 1
    
    if chong_count >= 2:  # 至少2对六冲
        return LiuChongGuaInfo(
            is_liu_chong_gua=True,
            description="六冲卦，主事情散乱、变动、分离"
        )
    
    return LiuChongGuaInfo(is_liu_chong_gua=False)


def calculate_shen_system(
    yong_shen_element: str,
    yao_liu_qins: List[Dict[str, str]]
) -> ShenSystem:
    """计算原神/忌神/仇神体系"""
    # 原神：生用神五行者
    yuan_element = None
    for wx, sheng_wx in WUXING_SHENG.items():
        if sheng_wx == yong_shen_element:
            yuan_element = wx
            break
    
    # 忌神：克用神五行者
    ji_element = None
    for wx, ke_wx in WUXING_KE.items():
        if ke_wx == yong_shen_element:
            ji_element = wx
            break
    
    # 仇神：克原神五行者
    chou_element = None
    if yuan_element:
        for wx, ke_wx in WUXING_KE.items():
            if ke_wx == yuan_element:
                chou_element = wx
                break
    
    result = ShenSystem()
    
    # 找出各神在卦中的位置
    for i, yao in enumerate(yao_liu_qins):
        wx = yao.get('element', '')
        lq = yao.get('liu_qin', '')
        
        if yuan_element and wx == yuan_element:
            if result.yuan_shen is None:
                result.yuan_shen = ShenMember(liu_qin=lq, wu_xing=wx, positions=[])
            result.yuan_shen.positions.append(i)
        
        if ji_element and wx == ji_element:
            if result.ji_shen is None:
                result.ji_shen = ShenMember(liu_qin=lq, wu_xing=wx, positions=[])
            result.ji_shen.positions.append(i)
        
        if chou_element and wx == chou_element:
            if result.chou_shen is None:
                result.chou_shen = ShenMember(liu_qin=lq, wu_xing=wx, positions=[])
            result.chou_shen.positions.append(i)
    
    return result


# ============= 主分析函数 =============

class LiuyaoAdvancedAnalyzer:
    """六爻高级分析器"""
    
    def __init__(self, month_zhi: str, day_gan: str, day_zhi: str):
        """
        初始化分析器
        
        Args:
            month_zhi: 月支
            day_gan: 日干
            day_zhi: 日支
        """
        self.month_zhi = month_zhi
        self.day_gan = day_gan
        self.day_zhi = day_zhi
        self.kong_wang = get_kong_wang(day_gan, day_zhi)
    
    def analyze_yao(
        self,
        index: int,
        branch: str,
        element: str,
        liu_qin: str,
        is_moving: bool,
        changed_branch: Optional[str] = None,
        changed_element: Optional[str] = None
    ) -> ExtendedYaoInfo:
        """分析单个爻"""
        # 空亡状态
        kong_wang_state = check_yao_kong_wang(
            branch, self.kong_wang, self.month_zhi, self.day_zhi, is_moving
        )
        
        # 月建日辰影响
        influence = calculate_yao_influence(branch, self.month_zhi, self.day_zhi)
        
        # 综合强度
        strength = calculate_yao_strength(
            element, branch, self.month_zhi, self.day_zhi,
            is_moving, kong_wang_state, influence
        )
        
        # 动爻变化分析
        change_analysis = None
        if is_moving and changed_branch and changed_element:
            change_analysis = calculate_change_analysis(
                branch, changed_branch, element, changed_element, self.kong_wang
            )
        
        # 十二长生
        chang_sheng = calculate_chang_sheng(element, self.day_zhi)
        
        return ExtendedYaoInfo(
            index=index,
            branch=branch,
            element=element,
            liu_qin=liu_qin,
            is_moving=is_moving,
            kong_wang_state=kong_wang_state,
            influence=influence,
            strength=strength,
            change_analysis=change_analysis,
            chang_sheng=chang_sheng
        )
    
    def analyze_hexagram(
        self,
        yaos: List[Dict],
        yong_shen_element: Optional[str] = None
    ) -> Dict:
        """
        分析整个卦象
        
        Args:
            yaos: 六爻信息列表，每个包含 index, branch, element, liu_qin, is_moving, 
                  changed_branch(可选), changed_element(可选)
            yong_shen_element: 用神五行（可选）
        
        Returns:
            包含扩展分析的字典
        """
        # 分析每个爻
        extended_yaos = []
        branches = []
        
        for yao in yaos:
            extended = self.analyze_yao(
                index=yao.get('index', 0),
                branch=yao.get('branch', ''),
                element=yao.get('element', ''),
                liu_qin=yao.get('liu_qin', ''),
                is_moving=yao.get('is_moving', False),
                changed_branch=yao.get('changed_branch'),
                changed_element=yao.get('changed_element')
            )
            extended_yaos.append(extended)
            branches.append(yao.get('branch', ''))
        
        # 三合局分析
        san_he_analysis = analyze_san_he(branches)
        
        # 六冲卦判定
        liu_chong_info = check_liu_chong_gua(branches)
        
        # 神系分析
        shen_system = None
        if yong_shen_element:
            shen_system = calculate_shen_system(yong_shen_element, yaos)
        
        return {
            'kong_wang': {
                'xun': self.kong_wang.xun,
                'kong_dizhi': self.kong_wang.kong_dizhi
            },
            'extended_yaos': [self._extended_yao_to_dict(y) for y in extended_yaos],
            'san_he_analysis': {
                'has_full_san_he': san_he_analysis.has_full_san_he,
                'full_san_he': san_he_analysis.full_san_he,
                'has_ban_he': san_he_analysis.has_ban_he,
                'ban_he': san_he_analysis.ban_he
            },
            'liu_chong_gua': {
                'is_liu_chong_gua': liu_chong_info.is_liu_chong_gua,
                'description': liu_chong_info.description
            },
            'shen_system': self._shen_system_to_dict(shen_system) if shen_system else None
        }
    
    def _extended_yao_to_dict(self, yao: ExtendedYaoInfo) -> Dict:
        """转换扩展爻信息为字典"""
        result = {
            'index': yao.index,
            'branch': yao.branch,
            'element': yao.element,
            'liu_qin': yao.liu_qin,
            'is_moving': yao.is_moving,
            'kong_wang_state': yao.kong_wang_state.value,
            'influence': {
                'month_action': yao.influence.month_action.value,
                'day_action': yao.influence.day_action.value,
                'description': yao.influence.description
            },
            'strength': {
                'wang_shuai': yao.strength.wang_shuai.value,
                'score': yao.strength.score,
                'factors': yao.strength.factors,
                'is_strong': yao.strength.is_strong,
                'special_status': yao.strength.special_status.value
            },
            'chang_sheng': {
                'stage': yao.chang_sheng.stage.value if yao.chang_sheng else None,
                'strength': yao.chang_sheng.strength if yao.chang_sheng else None,
                'description': yao.chang_sheng.description if yao.chang_sheng else None
            } if yao.chang_sheng else None
        }
        
        if yao.change_analysis:
            result['change_analysis'] = {
                'hua_type': yao.change_analysis.hua_type.value,
                'original_zhi': yao.change_analysis.original_zhi,
                'changed_zhi': yao.change_analysis.changed_zhi,
                'description': yao.change_analysis.description
            }
        
        return result
    
    def _shen_system_to_dict(self, shen: ShenSystem) -> Dict:
        """转换神系为字典"""
        def member_to_dict(m: Optional[ShenMember]) -> Optional[Dict]:
            if m is None:
                return None
            return {
                'liu_qin': m.liu_qin,
                'wu_xing': m.wu_xing,
                'positions': m.positions
            }
        
        return {
            'yuan_shen': member_to_dict(shen.yuan_shen),
            'ji_shen': member_to_dict(shen.ji_shen),
            'chou_shen': member_to_dict(shen.chou_shen)
        }


# ============= 应期推断 =============

@dataclass
class TimeRecommendation:
    """应期推断"""
    type: str           # favorable/unfavorable/critical
    timeframe: str      # 特定日/月内/近期
    earthly_branch: Optional[str] = None
    description: str = ""


def calculate_time_recommendations(
    yong_shen_element: str,
    yong_shen_branch: str,
    moving_yaos: List[Dict]
) -> List[TimeRecommendation]:
    """
    计算应期推断
    
    应期原则：
    1. 用神所临地支为应期
    2. 生用神的五行旺时为有利时间
    3. 克用神的五行旺时为不利时间
    4. 动爻所临地支为关键变化时间
    5. 空亡填实之时
    6. 冲破之时
    """
    recommendations = []
    
    if yong_shen_branch:
        # 用神地支为应期
        recommendations.append(TimeRecommendation(
            type='favorable',
            timeframe='特定日',
            earthly_branch=yong_shen_branch,
            description=f"逢{yong_shen_branch}日/月为应期，事情易有进展"
        ))
    
    if yong_shen_element:
        # 生用神五行旺时有利
        sheng_element = None
        for wx, sheng_wx in WUXING_SHENG.items():
            if sheng_wx == yong_shen_element:
                sheng_element = wx
                break
        
        if sheng_element:
            # 找该五行旺的月份
            sheng_months = _get_wang_months(sheng_element)
            recommendations.append(TimeRecommendation(
                type='favorable',
                timeframe='月内',
                description=f"{sheng_element}旺之月（{sheng_months}）有利，可积极行动"
            ))
        
        # 克用神五行旺时不利
        ke_element = None
        for wx, ke_wx in WUXING_KE.items():
            if ke_wx == yong_shen_element:
                ke_element = wx
                break
        
        if ke_element:
            ke_months = _get_wang_months(ke_element)
            recommendations.append(TimeRecommendation(
                type='unfavorable',
                timeframe='近期',
                description=f"{ke_element}旺之月（{ke_months}）不利，宜谨慎"
            ))
    
    # 动爻应期
    if moving_yaos:
        for yao in moving_yaos:
            branch = yao.get('branch', '')
            if branch:
                recommendations.append(TimeRecommendation(
                    type='critical',
                    timeframe='特定日',
                    earthly_branch=branch,
                    description=f"动爻临{branch}，逢{branch}日/月可能有关键变化"
                ))
                break  # 只取第一个动爻
    
    return recommendations


def _get_wang_months(element: str) -> str:
    """获取五行旺的月份"""
    month_map = {
        '木': '寅卯月（农历正二月）',
        '火': '巳午月（农历四五月）',
        '土': '辰戌丑未月（四季月）',
        '金': '申酉月（农历七八月）',
        '水': '亥子月（农历十、十一月）'
    }
    return month_map.get(element, '')


def time_recommendations_to_dict(recs: List[TimeRecommendation]) -> List[Dict]:
    """转换应期推断为字典列表"""
    return [
        {
            'type': r.type,
            'timeframe': r.timeframe,
            'earthly_branch': r.earthly_branch,
            'description': r.description
        }
        for r in recs
    ]
