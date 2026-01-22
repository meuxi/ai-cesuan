# -*- coding: utf-8 -*-
"""
六爻高级分析模块
完整实现参考 MingAI liuyao.ts 的所有功能：
- 干支时间计算
- 旬空体系
- 月建日辰作用
- 旺衰判定
- 暗动/日破
- 动爻变化分析
- 六合/六冲/三合局
- 伏神系统
- 原神/忌神/仇神
- 十二长生
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# 地支列表
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干列表
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 五行类型
WUXING = ['金', '木', '水', '火', '土']

# 地支五行
DIZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 天干五行
TIANGAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
}

# 地支序数
DIZHI_INDEX = {zhi: i for i, zhi in enumerate(DIZHI)}

# 天干序数
TIANGAN_INDEX = {gan: i for i, gan in enumerate(TIANGAN)}

# 旬空表
XUN_KONG_TABLE = {
    '甲子旬': ('戌', '亥'),
    '甲戌旬': ('申', '酉'),
    '甲申旬': ('午', '未'),
    '甲午旬': ('辰', '巳'),
    '甲辰旬': ('寅', '卯'),
    '甲寅旬': ('子', '丑'),
}

# 六冲表
LIU_CHONG = {
    '子': '午', '丑': '未', '寅': '申', '卯': '酉', '辰': '戌', '巳': '亥',
    '午': '子', '未': '丑', '申': '寅', '酉': '卯', '戌': '辰', '亥': '巳',
}

# 六合表及合化结果
LIU_HE = {
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
LIU_HAI = {
    '子': '未', '丑': '午', '寅': '巳', '卯': '辰',
    '辰': '卯', '巳': '寅', '午': '丑', '未': '子',
    '申': '亥', '酉': '戌', '戌': '酉', '亥': '申',
}

# 相刑表
XIANG_XING = {
    '寅': ['巳', '申'], '巳': ['寅', '申'], '申': ['寅', '巳'],
    '丑': ['戌', '未'], '戌': ['丑', '未'], '未': ['丑', '戌'],
    '子': ['卯'], '卯': ['子'],
    '辰': ['辰'], '午': ['午'], '酉': ['酉'], '亥': ['亥'],
}

# 相破表
XIANG_PO = {
    '子': '酉', '酉': '子', '丑': '辰', '辰': '丑',
    '寅': '亥', '亥': '寅', '卯': '午', '午': '卯',
    '巳': '申', '申': '巳', '未': '戌', '戌': '未',
}

# 五行墓库表
WUXING_MU = {
    '木': '未', '火': '戌', '土': '戌', '金': '丑', '水': '辰',
}

# 五行生克
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
WUXING_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
WUXING_BEI_SHENG = {'火': '木', '土': '火', '金': '土', '水': '金', '木': '水'}
WUXING_BEI_KE = {'土': '木', '水': '土', '火': '水', '金': '火', '木': '金'}

# 三合局表
SAN_HE_TABLE = [
    {'branches': ('申', '子', '辰'), 'result': '水', 'name': '申子辰合水局'},
    {'branches': ('亥', '卯', '未'), 'result': '木', 'name': '亥卯未合木局'},
    {'branches': ('寅', '午', '戌'), 'result': '火', 'name': '寅午戌合火局'},
    {'branches': ('巳', '酉', '丑'), 'result': '金', 'name': '巳酉丑合金局'},
]

# 半合表
BAN_HE_TABLE = [
    {'branches': ('申', '子'), 'result': '水', 'type': 'sheng'},
    {'branches': ('亥', '卯'), 'result': '木', 'type': 'sheng'},
    {'branches': ('寅', '午'), 'result': '火', 'type': 'sheng'},
    {'branches': ('巳', '酉'), 'result': '金', 'type': 'sheng'},
    {'branches': ('子', '辰'), 'result': '水', 'type': 'mu'},
    {'branches': ('卯', '未'), 'result': '木', 'type': 'mu'},
    {'branches': ('午', '戌'), 'result': '火', 'type': 'mu'},
    {'branches': ('酉', '丑'), 'result': '金', 'type': 'mu'},
]

# 十二长生
CHANG_SHENG_ORDER = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

# 五行十二长生表
WUXING_CHANG_SHENG = {
    '木': {'亥': '长生', '子': '沐浴', '丑': '冠带', '寅': '临官', '卯': '帝旺', '辰': '衰',
           '巳': '病', '午': '死', '未': '墓', '申': '绝', '酉': '胎', '戌': '养'},
    '火': {'寅': '长生', '卯': '沐浴', '辰': '冠带', '巳': '临官', '午': '帝旺', '未': '衰',
           '申': '病', '酉': '死', '戌': '墓', '亥': '绝', '子': '胎', '丑': '养'},
    '土': {'寅': '长生', '卯': '沐浴', '辰': '冠带', '巳': '临官', '午': '帝旺', '未': '衰',
           '申': '病', '酉': '死', '戌': '墓', '亥': '绝', '子': '胎', '丑': '养'},
    '金': {'巳': '长生', '午': '沐浴', '未': '冠带', '申': '临官', '酉': '帝旺', '戌': '衰',
           '亥': '病', '子': '死', '丑': '墓', '寅': '绝', '卯': '胎', '辰': '养'},
    '水': {'申': '长生', '酉': '沐浴', '戌': '冠带', '亥': '临官', '子': '帝旺', '丑': '衰',
           '寅': '病', '卯': '死', '辰': '墓', '巳': '绝', '午': '胎', '未': '养'},
}

# 十二长生强弱
CHANG_SHENG_STRENGTH = {
    '长生': 'strong', '沐浴': 'medium', '冠带': 'strong', '临官': 'strong',
    '帝旺': 'strong', '衰': 'medium', '病': 'weak', '死': 'weak',
    '墓': 'weak', '绝': 'weak', '胎': 'medium', '养': 'medium',
}

# 月令旺衰表
WANG_SHUAI_TABLE = {
    '寅': {'木': '旺', '火': '相', '水': '休', '金': '囚', '土': '死'},
    '卯': {'木': '旺', '火': '相', '水': '休', '金': '囚', '土': '死'},
    '辰': {'土': '旺', '金': '相', '火': '休', '木': '囚', '水': '死'},
    '巳': {'火': '旺', '土': '相', '木': '休', '水': '囚', '金': '死'},
    '午': {'火': '旺', '土': '相', '木': '休', '水': '囚', '金': '死'},
    '未': {'土': '旺', '金': '相', '火': '休', '木': '囚', '水': '死'},
    '申': {'金': '旺', '水': '相', '土': '休', '火': '囚', '木': '死'},
    '酉': {'金': '旺', '水': '相', '土': '休', '火': '囚', '木': '死'},
    '戌': {'土': '旺', '金': '相', '火': '休', '木': '囚', '水': '死'},
    '亥': {'水': '旺', '木': '相', '金': '休', '土': '囚', '火': '死'},
    '子': {'水': '旺', '木': '相', '金': '休', '土': '囚', '火': '死'},
    '丑': {'土': '旺', '金': '相', '火': '休', '木': '囚', '水': '死'},
}


class WangShuai(Enum):
    """旺衰五态"""
    WANG = '旺'
    XIANG = '相'
    XIU = '休'
    QIU = '囚'
    SI = '死'


class YaoSpecialStatus(Enum):
    """爻的特殊状态"""
    NONE = '无'
    AN_DONG = '暗动'
    RI_PO = '日破'


class KongWangState(Enum):
    """空亡状态"""
    NOT_KONG = '不空'
    KONG_STATIC = '真空'
    KONG_CHANGING = '动空'
    KONG_RI_CHONG = '冲空'
    KONG_YUE_JIAN = '临建'


class HuaType(Enum):
    """动爻变化类型"""
    NONE = '无'
    HUA_JIN = '化进'
    HUA_TUI = '化退'
    HUI_TOU_SHENG = '回头生'
    HUI_TOU_KE = '回头克'
    HUA_KONG = '化空'
    HUA_MU = '化墓'
    FU_YIN = '伏吟'
    FAN_YIN = '反吟'


@dataclass
class GanZhi:
    """干支对"""
    gan: str
    zhi: str


@dataclass
class GanZhiTime:
    """完整干支时间"""
    year: GanZhi
    month: GanZhi
    day: GanZhi
    hour: GanZhi
    xun: str  # 日柱所属旬


@dataclass
class KongWang:
    """旬空信息"""
    xun: str
    kong_dizhi: Tuple[str, str]


@dataclass
class YaoInfluence:
    """月建日辰影响"""
    month_action: str
    day_action: str
    description: str


@dataclass
class YaoStrength:
    """爻的综合强度"""
    wang_shuai: str
    score: int
    factors: List[str]
    is_strong: bool
    special_status: str


@dataclass
class YaoChangeAnalysis:
    """动爻变化分析"""
    hua_type: str
    original_zhi: str
    changed_zhi: str
    description: str


@dataclass
class ChangShengInfo:
    """十二长生信息"""
    stage: str
    strength: str
    description: str


@dataclass
class FuShen:
    """伏神信息"""
    liu_qin: str
    wu_xing: str
    na_jia: str
    fei_shen_position: int
    fei_shen_liu_qin: str
    is_available: bool
    availability_reason: str


@dataclass
class ShenMember:
    """神系成员"""
    liu_qin: str
    wu_xing: str
    positions: List[int]


@dataclass
class ShenSystem:
    """原神/忌神/仇神体系"""
    yuan_shen: Optional[ShenMember]
    ji_shen: Optional[ShenMember]
    chou_shen: Optional[ShenMember]


@dataclass
class SanHeAnalysis:
    """三合局分析"""
    has_full_san_he: bool
    full_san_he: Optional[Dict]
    has_ban_he: bool
    ban_he: Optional[List[Dict]]


@dataclass
class LiuChongGuaInfo:
    """六冲卦信息"""
    is_liu_chong_gua: bool
    description: Optional[str]


def get_xun_from_day_ganzhi(day_gan: str, day_zhi: str) -> str:
    """根据日干支计算所属旬"""
    gan_index = TIANGAN_INDEX.get(day_gan, 0)
    zhi_index = DIZHI_INDEX.get(day_zhi, 0)
    xun_start_zhi_index = (zhi_index - gan_index + 12) % 12
    xun_names = {0: '甲子旬', 2: '甲寅旬', 4: '甲辰旬', 6: '甲午旬', 8: '甲申旬', 10: '甲戌旬'}
    return xun_names.get(xun_start_zhi_index, '甲子旬')


def calculate_ganzhi_time(date: datetime) -> GanZhiTime:
    """计算完整干支时间"""
    try:
        from lunar_python import Solar
        solar = Solar.fromYmdHms(date.year, date.month, date.day, date.hour, date.minute, 0)
        lunar = solar.getLunar()
        eight_char = lunar.getEightChar()
        
        day_gan = eight_char.getDayGan()
        day_zhi = eight_char.getDayZhi()
        
        return GanZhiTime(
            year=GanZhi(eight_char.getYearGan(), eight_char.getYearZhi()),
            month=GanZhi(eight_char.getMonthGan(), eight_char.getMonthZhi()),
            day=GanZhi(day_gan, day_zhi),
            hour=GanZhi(eight_char.getTimeGan(), eight_char.getTimeZhi()),
            xun=get_xun_from_day_ganzhi(day_gan, day_zhi)
        )
    except ImportError:
        # 简化计算（备用）
        base_date = datetime(1900, 1, 31)
        days_diff = (date - base_date).days
        gan_index = (days_diff + 10) % 10
        zhi_index = (days_diff + 12) % 12
        day_gan = TIANGAN[gan_index]
        day_zhi = DIZHI[zhi_index]
        
        return GanZhiTime(
            year=GanZhi('甲', '子'),
            month=GanZhi('甲', '寅'),
            day=GanZhi(day_gan, day_zhi),
            hour=GanZhi('甲', '子'),
            xun=get_xun_from_day_ganzhi(day_gan, day_zhi)
        )


def get_kong_wang(day_gan: str, day_zhi: str) -> KongWang:
    """获取旬空信息"""
    xun = get_xun_from_day_ganzhi(day_gan, day_zhi)
    return KongWang(xun=xun, kong_dizhi=XUN_KONG_TABLE.get(xun, ('戌', '亥')))


def check_yao_kong_wang(yao_zhi: str, kong_wang: KongWang, month_zhi: str, 
                        day_zhi: str, is_changing: bool) -> KongWangState:
    """检查爻的空亡状态"""
    if yao_zhi not in kong_wang.kong_dizhi:
        return KongWangState.NOT_KONG
    if is_changing:
        return KongWangState.KONG_CHANGING
    if LIU_CHONG.get(yao_zhi) == day_zhi:
        return KongWangState.KONG_RI_CHONG
    if yao_zhi == month_zhi:
        return KongWangState.KONG_YUE_JIAN
    return KongWangState.KONG_STATIC


def get_zhi_action(source_zhi: str, target_zhi: str) -> str:
    """获取地支对爻的作用"""
    if LIU_CHONG.get(source_zhi) == target_zhi:
        return '冲'
    if LIU_HE.get(source_zhi, {}).get('partner') == target_zhi:
        return '合'
    if XIANG_PO.get(source_zhi) == target_zhi:
        return '破'
    
    source_wuxing = DIZHI_WUXING.get(source_zhi, '土')
    target_wuxing = DIZHI_WUXING.get(target_zhi, '土')
    
    if source_wuxing == target_wuxing:
        return '扶'
    if WUXING_SHENG.get(source_wuxing) == target_wuxing:
        return '生'
    if WUXING_KE.get(source_wuxing) == target_wuxing:
        return '克'
    
    return '无'


def get_yao_influence(yao_zhi: str, month_zhi: str, day_zhi: str) -> YaoInfluence:
    """获取月建日辰对爻的综合影响"""
    month_action = get_zhi_action(month_zhi, yao_zhi)
    day_action = get_zhi_action(day_zhi, yao_zhi)
    
    parts = []
    if month_action != '无':
        parts.append(f'月{month_action}')
    if day_action != '无':
        parts.append(f'日{day_action}')
    
    return YaoInfluence(
        month_action=month_action,
        day_action=day_action,
        description='、'.join(parts) if parts else '无特殊作用'
    )


def calculate_yao_strength(yao_wuxing: str, month_zhi: str, day_zhi: str,
                          is_changing: bool, kong_wang_state: KongWangState,
                          influence: YaoInfluence) -> YaoStrength:
    """计算爻的综合强度（含暗动/日破判定）"""
    factors = []
    score = 50
    special_status = YaoSpecialStatus.NONE.value
    
    # 月令旺衰
    wang_shuai = WANG_SHUAI_TABLE.get(month_zhi, {}).get(yao_wuxing, '休')
    wang_shuai_scores = {'旺': 40, '相': 25, '休': 0, '囚': -15, '死': -25}
    score += wang_shuai_scores.get(wang_shuai, 0)
    factors.append(f'月令{wang_shuai}')
    
    is_wang_xiang = wang_shuai in ('旺', '相')
    
    # 日辰作用（关键：暗动与日破）
    if influence.day_action == '生':
        score += 15
        factors.append('日生')
    elif influence.day_action == '扶':
        score += 12
        factors.append('日扶')
    elif influence.day_action == '克':
        score -= 15
        factors.append('日克')
    elif influence.day_action == '冲':
        if is_changing:
            score -= 20
            factors.append('冲散')
        else:
            if is_wang_xiang:
                special_status = YaoSpecialStatus.AN_DONG.value
                score += 30
                factors.append('暗动')
            else:
                special_status = YaoSpecialStatus.RI_PO.value
                score = 0
                factors.append('日破')
    
    # 月建作用
    if special_status != YaoSpecialStatus.RI_PO.value:
        if influence.month_action == '生':
            score += 10
            factors.append('月生')
        elif influence.month_action == '扶':
            score += 8
            factors.append('月扶')
        elif influence.month_action == '克':
            score -= 10
            factors.append('月克')
        elif influence.month_action == '冲':
            score -= 8
            factors.append('月冲')
    
    # 空亡影响
    if special_status == YaoSpecialStatus.NONE.value and kong_wang_state == KongWangState.KONG_STATIC:
        score -= 25
        factors.append('空亡')
    
    # 动静状态
    if is_changing and special_status == YaoSpecialStatus.NONE.value:
        score += 5
        factors.append('动爻')
    
    score = max(0, min(100, score))
    
    return YaoStrength(
        wang_shuai=wang_shuai,
        score=score,
        factors=factors,
        is_strong=score >= 50,
        special_status=special_status
    )


def analyze_yao_change(original_zhi: str, changed_zhi: str, original_wuxing: str,
                       changed_wuxing: str, kong_wang: KongWang) -> YaoChangeAnalysis:
    """分析动爻变化"""
    # 伏吟
    if original_zhi == changed_zhi:
        return YaoChangeAnalysis(HuaType.FU_YIN.value, original_zhi, changed_zhi, '伏吟：变爻与本爻相同，事多反复')
    
    # 反吟
    if LIU_CHONG.get(original_zhi) == changed_zhi:
        return YaoChangeAnalysis(HuaType.FAN_YIN.value, original_zhi, changed_zhi, '反吟：变爻与本爻相冲，事情反复无常')
    
    # 化空
    if changed_zhi in kong_wang.kong_dizhi:
        return YaoChangeAnalysis(HuaType.HUA_KONG.value, original_zhi, changed_zhi, '化空：变爻落空，事难成就')
    
    # 化墓
    if WUXING_MU.get(original_wuxing) == changed_zhi:
        return YaoChangeAnalysis(HuaType.HUA_MU.value, original_zhi, changed_zhi, '化墓：变爻入墓，事情受阻')
    
    # 回头生
    if WUXING_SHENG.get(changed_wuxing) == original_wuxing:
        return YaoChangeAnalysis(HuaType.HUI_TOU_SHENG.value, original_zhi, changed_zhi, '回头生：变爻生本爻，吉利')
    
    # 回头克
    if WUXING_KE.get(changed_wuxing) == original_wuxing:
        return YaoChangeAnalysis(HuaType.HUI_TOU_KE.value, original_zhi, changed_zhi, '回头克：变爻克本爻，不利')
    
    # 化进/化退
    original_index = DIZHI_INDEX.get(original_zhi, 0)
    changed_index = DIZHI_INDEX.get(changed_zhi, 0)
    diff = (changed_index - original_index + 12) % 12
    
    if 0 < diff <= 6:
        return YaoChangeAnalysis(HuaType.HUA_JIN.value, original_zhi, changed_zhi, '化进：变爻进神，事情向好发展')
    elif diff > 6:
        return YaoChangeAnalysis(HuaType.HUA_TUI.value, original_zhi, changed_zhi, '化退：变爻退神，事情退步')
    
    return YaoChangeAnalysis(HuaType.NONE.value, original_zhi, changed_zhi, '')


def get_chang_sheng(wu_xing: str, di_zhi: str) -> ChangShengInfo:
    """获取十二长生状态"""
    stage = WUXING_CHANG_SHENG.get(wu_xing, {}).get(di_zhi, '养')
    strength = CHANG_SHENG_STRENGTH.get(stage, 'medium')
    
    descriptions = {
        '长生': '如人初生，生机勃勃，有发展潜力',
        '沐浴': '如人沐浴，不稳定，易有波折',
        '冠带': '如人成年，渐入佳境，开始有成就',
        '临官': '如人当官，权力渐盛，事业上升',
        '帝旺': '如帝王之旺，鼎盛之极，最为有力',
        '衰': '盛极而衰，力量开始减弱',
        '病': '如人生病，力量衰弱，需要调养',
        '死': '气息将绝，力量极弱',
        '墓': '入墓收藏，力量被封存',
        '绝': '气息已绝，最为无力',
        '胎': '如人受胎，开始孕育新生',
        '养': '如人养育，等待时机出生',
    }
    
    return ChangShengInfo(stage=stage, strength=strength, description=descriptions.get(stage, ''))


def analyze_san_he(yao_branches: List[str], month_zhi: Optional[str] = None,
                   day_zhi: Optional[str] = None) -> SanHeAnalysis:
    """分析三合局"""
    all_zhi = list(yao_branches)
    if month_zhi:
        all_zhi.append(month_zhi)
    if day_zhi:
        all_zhi.append(day_zhi)
    
    # 检查完整三合
    full_san_he = None
    for san_he in SAN_HE_TABLE:
        b1, b2, b3 = san_he['branches']
        if b1 in all_zhi and b2 in all_zhi and b3 in all_zhi:
            positions = [i + 1 for i, zhi in enumerate(yao_branches) if zhi in san_he['branches']]
            full_san_he = {
                'name': san_he['name'],
                'result': san_he['result'],
                'positions': positions
            }
            break
    
    # 检查半合
    ban_he_list = []
    for ban_he in BAN_HE_TABLE:
        b1, b2 = ban_he['branches']
        if b1 in all_zhi and b2 in all_zhi:
            positions = [i + 1 for i, zhi in enumerate(yao_branches) if zhi in (b1, b2)]
            if positions:
                ban_he_list.append({
                    'branches': list(ban_he['branches']),
                    'result': ban_he['result'],
                    'type': ban_he['type'],
                    'positions': positions
                })
    
    return SanHeAnalysis(
        has_full_san_he=full_san_he is not None,
        full_san_he=full_san_he,
        has_ban_he=len(ban_he_list) > 0,
        ban_he=ban_he_list if ban_he_list else None
    )


def check_liu_chong_gua(yao_branches: List[str]) -> LiuChongGuaInfo:
    """判断是否为六冲卦"""
    if len(yao_branches) != 6:
        return LiuChongGuaInfo(False, None)
    
    pair1_chong = LIU_CHONG.get(yao_branches[0]) == yao_branches[3]
    pair2_chong = LIU_CHONG.get(yao_branches[1]) == yao_branches[4]
    pair3_chong = LIU_CHONG.get(yao_branches[2]) == yao_branches[5]
    
    if pair1_chong and pair2_chong and pair3_chong:
        return LiuChongGuaInfo(True, '六冲卦：主事散、应期急、变动大')
    
    chong_count = sum([pair1_chong, pair2_chong, pair3_chong])
    if chong_count >= 2:
        return LiuChongGuaInfo(False, f'卦中有{chong_count}对爻相冲，事有变动')
    
    return LiuChongGuaInfo(False, None)


def calculate_liu_qin(yao_wuxing: str, gong_wuxing: str) -> str:
    """计算六亲"""
    if yao_wuxing == gong_wuxing:
        return '兄弟'
    if WUXING_SHENG.get(yao_wuxing) == gong_wuxing:
        return '父母'
    if WUXING_SHENG.get(gong_wuxing) == yao_wuxing:
        return '子孙'
    if WUXING_KE.get(gong_wuxing) == yao_wuxing:
        return '妻财'
    if WUXING_KE.get(yao_wuxing) == gong_wuxing:
        return '官鬼'
    return '兄弟'


def determine_yong_shen_type(question: str) -> str:
    """根据问事确定用神类型"""
    question_map = {
        '事业': '官鬼', '工作': '官鬼', '升职': '官鬼',
        '考试': '父母', '学业': '父母',
        '财运': '妻财', '投资': '妻财', '生意': '妻财',
        '感情': '妻财', '婚姻': '妻财', '恋爱': '妻财',
        '健康': '子孙', '疾病': '官鬼',
        '子女': '子孙', '父母': '父母', '兄弟': '兄弟',
        '出行': '子孙', '诉讼': '官鬼', '失物': '妻财',
    }
    
    for keyword, liu_qin in question_map.items():
        if keyword in question:
            return liu_qin
    
    return '妻财'


def calculate_shen_system(yong_shen_wuxing: str, gong_wuxing: str, 
                          yao_liu_qins: List[str]) -> ShenSystem:
    """计算原神/忌神/仇神体系"""
    # 原神：生用神者
    yuan_shen_wuxing = WUXING_BEI_SHENG.get(yong_shen_wuxing, '土')
    yuan_shen_liu_qin = calculate_liu_qin(yuan_shen_wuxing, gong_wuxing)
    
    # 忌神：克用神者
    ji_shen_wuxing = WUXING_BEI_KE.get(yong_shen_wuxing, '土')
    ji_shen_liu_qin = calculate_liu_qin(ji_shen_wuxing, gong_wuxing)
    
    # 仇神：克原神者
    chou_shen_wuxing = WUXING_BEI_KE.get(yuan_shen_wuxing, '土')
    chou_shen_liu_qin = calculate_liu_qin(chou_shen_wuxing, gong_wuxing)
    
    # 找位置
    def find_positions(liu_qin: str) -> List[int]:
        return [i + 1 for i, lq in enumerate(yao_liu_qins) if lq == liu_qin]
    
    return ShenSystem(
        yuan_shen=ShenMember(yuan_shen_liu_qin, yuan_shen_wuxing, find_positions(yuan_shen_liu_qin)),
        ji_shen=ShenMember(ji_shen_liu_qin, ji_shen_wuxing, find_positions(ji_shen_liu_qin)),
        chou_shen=ShenMember(chou_shen_liu_qin, chou_shen_wuxing, find_positions(chou_shen_liu_qin))
    )


def calculate_fu_shen(hexagram_data: Dict, yao_liu_qins: List[str], gong_wuxing: str,
                      kong_wang: KongWang, month_zhi: str, day_zhi: str) -> List[FuShen]:
    """
    计算伏神
    当用神不上卦时，从本宫首卦找伏神
    
    伏神可用性判断：
    1. 飞神克伏神 → 不可用
    2. 伏神空亡 → 暂不可用
    3. 飞神生伏神 → 可用
    4. 月日生扶伏神 → 可用
    """
    # 检查所有六亲是否都上卦
    all_liu_qins = ['父母', '兄弟', '官鬼', '妻财', '子孙']
    present_liu_qins = set(yao_liu_qins)
    missing_liu_qins = [lq for lq in all_liu_qins if lq not in present_liu_qins]
    
    if not missing_liu_qins:
        return []  # 所有六亲都上卦，不需要伏神
    
    # 八宫纳甲数据（本宫首卦的纳甲）
    # 这里使用简化版，实际应该从eight_palaces模块获取
    PALACE_NA_JIA = {
        '金': ['子', '寅', '辰', '午', '申', '戌'],  # 乾宫
        '木': ['子', '寅', '辰', '午', '申', '戌'],  # 震宫
        '水': ['寅', '辰', '午', '申', '戌', '子'],  # 坎宫
        '火': ['卯', '丑', '亥', '酉', '未', '巳'],  # 离宫
        '土': ['辰', '午', '申', '戌', '子', '寅'],  # 艮宫/坤宫
    }
    
    palace_na_jia = PALACE_NA_JIA.get(gong_wuxing, PALACE_NA_JIA['土'])
    lines = hexagram_data.get('lines', [])
    
    fu_shen_list = []
    
    for missing_lq in missing_liu_qins:
        # 在本宫首卦中找到该六亲对应的爻位
        for position in range(6):
            fu_shen_branch = palace_na_jia[position]
            fu_shen_wuxing = DIZHI_WUXING.get(fu_shen_branch, '土')
            fu_shen_liu_qin = calculate_liu_qin(fu_shen_wuxing, gong_wuxing)
            
            if fu_shen_liu_qin == missing_lq:
                # 找到伏神，获取飞神（当前卦该爻位的爻）
                fei_shen_line = lines[position] if position < len(lines) else None
                if not fei_shen_line:
                    continue
                
                fei_shen_branch = fei_shen_line.get('branch', '子')
                fei_shen_wuxing = DIZHI_WUXING.get(fei_shen_branch, '土')
                fei_shen_liu_qin = fei_shen_line.get('six_relation', '兄弟')
                
                # 判断伏神可用性
                is_available = True
                availability_reason = '伏神可用'
                
                # 飞神克伏神 → 不可用
                if WUXING_KE.get(fei_shen_wuxing) == fu_shen_wuxing:
                    is_available = False
                    availability_reason = '飞神克伏神，伏神不可用'
                # 伏神空亡 → 暂不可用
                elif fu_shen_branch in kong_wang.kong_dizhi:
                    is_available = False
                    availability_reason = '伏神空亡，暂不可用'
                # 飞神生伏神 → 可用
                elif WUXING_SHENG.get(fei_shen_wuxing) == fu_shen_wuxing:
                    is_available = True
                    availability_reason = '飞神生伏神，伏神可用'
                # 月日生扶伏神
                elif (WUXING_SHENG.get(DIZHI_WUXING.get(month_zhi, '土')) == fu_shen_wuxing or
                      WUXING_SHENG.get(DIZHI_WUXING.get(day_zhi, '土')) == fu_shen_wuxing):
                    is_available = True
                    availability_reason = '月日生扶伏神，伏神可用'
                # 日冲伏神可出
                elif LIU_CHONG.get(day_zhi) == fu_shen_branch:
                    is_available = True
                    availability_reason = '日冲伏神，伏神可出'
                
                fu_shen_list.append(FuShen(
                    liu_qin=missing_lq,
                    wu_xing=fu_shen_wuxing,
                    na_jia=fu_shen_branch,
                    fei_shen_position=position + 1,
                    fei_shen_liu_qin=fei_shen_liu_qin,
                    is_available=is_available,
                    availability_reason=availability_reason
                ))
                break  # 找到一个就够了
    
    return fu_shen_list


def perform_advanced_analysis(hexagram_data: Dict, question: str = "", 
                              date: Optional[datetime] = None) -> Dict[str, Any]:
    """
    执行完整的六爻高级分析
    
    Args:
        hexagram_data: 卦象数据（包含lines等）
        question: 问事内容
        date: 起卦时间
    
    Returns:
        完整的高级分析结果
    """
    if date is None:
        date = datetime.now()
    
    # 1. 计算干支时间
    ganzhi_time = calculate_ganzhi_time(date)
    month_zhi = ganzhi_time.month.zhi
    day_zhi = ganzhi_time.day.zhi
    
    # 2. 计算旬空
    kong_wang = get_kong_wang(ganzhi_time.day.gan, ganzhi_time.day.zhi)
    
    # 3. 获取宫位五行
    gong_wuxing = hexagram_data.get('palace_element', '土')
    
    # 4. 处理每一爻
    lines = hexagram_data.get('lines', [])
    extended_yaos = []
    yao_branches = []
    yao_liu_qins = []
    
    for line in lines:
        branch = line.get('branch', '子')
        yao_branches.append(branch)
        
        yao_wuxing = DIZHI_WUXING.get(branch, '土')
        is_changing = line.get('is_moving', False)
        
        # 空亡状态
        kong_wang_state = check_yao_kong_wang(branch, kong_wang, month_zhi, day_zhi, is_changing)
        
        # 月日影响
        influence = get_yao_influence(branch, month_zhi, day_zhi)
        
        # 综合强度
        strength = calculate_yao_strength(yao_wuxing, month_zhi, day_zhi, 
                                         is_changing, kong_wang_state, influence)
        
        # 十二长生
        chang_sheng = get_chang_sheng(yao_wuxing, month_zhi)
        
        # 动爻变化分析
        change_analysis = None
        if is_changing and line.get('changed_branch'):
            changed_branch = line['changed_branch']
            changed_wuxing = DIZHI_WUXING.get(changed_branch, '土')
            change_analysis = analyze_yao_change(branch, changed_branch, yao_wuxing, changed_wuxing, kong_wang)
        
        # 六亲
        liu_qin = line.get('six_relation', calculate_liu_qin(yao_wuxing, gong_wuxing))
        yao_liu_qins.append(liu_qin)
        
        extended_yaos.append({
            'position': line.get('index', 0) + 1,
            'branch': branch,
            'wu_xing': yao_wuxing,
            'liu_qin': liu_qin,
            'is_moving': is_changing,
            'kong_wang_state': kong_wang_state.value,
            'influence': {
                'month_action': influence.month_action,
                'day_action': influence.day_action,
                'description': influence.description
            },
            'strength': {
                'wang_shuai': strength.wang_shuai,
                'score': strength.score,
                'factors': strength.factors,
                'is_strong': strength.is_strong,
                'special_status': strength.special_status
            },
            'chang_sheng': {
                'stage': chang_sheng.stage,
                'strength': chang_sheng.strength,
                'description': chang_sheng.description
            },
            'change_analysis': {
                'hua_type': change_analysis.hua_type if change_analysis else None,
                'description': change_analysis.description if change_analysis else None
            } if change_analysis else None
        })
    
    # 5. 六冲卦判定
    liu_chong_gua = check_liu_chong_gua(yao_branches)
    
    # 6. 三合局分析
    san_he = analyze_san_he(yao_branches, month_zhi, day_zhi)
    
    # 7. 确定用神
    yong_shen_type = determine_yong_shen_type(question)
    yong_shen_positions = [i + 1 for i, lq in enumerate(yao_liu_qins) if lq == yong_shen_type]
    yong_shen_wuxing = '土'
    if yong_shen_positions:
        pos = yong_shen_positions[0] - 1
        if pos < len(extended_yaos):
            yong_shen_wuxing = extended_yaos[pos]['wu_xing']
    
    # 8. 神系分析
    shen_system = calculate_shen_system(yong_shen_wuxing, gong_wuxing, yao_liu_qins)
    
    # 9. 伏神计算（用神不上卦时）
    fu_shen_list = []
    if not yong_shen_positions:
        fu_shen_list = calculate_fu_shen(hexagram_data, yao_liu_qins, gong_wuxing, 
                                         kong_wang, month_zhi, day_zhi)
    
    return {
        'ganzhi_time': {
            'year': f"{ganzhi_time.year.gan}{ganzhi_time.year.zhi}",
            'month': f"{ganzhi_time.month.gan}{ganzhi_time.month.zhi}",
            'day': f"{ganzhi_time.day.gan}{ganzhi_time.day.zhi}",
            'hour': f"{ganzhi_time.hour.gan}{ganzhi_time.hour.zhi}",
            'xun': ganzhi_time.xun
        },
        'kong_wang': {
            'xun': kong_wang.xun,
            'kong_dizhi': list(kong_wang.kong_dizhi)
        },
        'extended_yaos': extended_yaos,
        'liu_chong_gua': {
            'is_liu_chong_gua': liu_chong_gua.is_liu_chong_gua,
            'description': liu_chong_gua.description
        },
        'san_he_analysis': {
            'has_full_san_he': san_he.has_full_san_he,
            'full_san_he': san_he.full_san_he,
            'has_ban_he': san_he.has_ban_he,
            'ban_he': san_he.ban_he
        },
        'yong_shen': {
            'type': yong_shen_type,
            'positions': yong_shen_positions,
            'wu_xing': yong_shen_wuxing
        },
        'shen_system': {
            'yuan_shen': {
                'liu_qin': shen_system.yuan_shen.liu_qin,
                'wu_xing': shen_system.yuan_shen.wu_xing,
                'positions': shen_system.yuan_shen.positions
            } if shen_system.yuan_shen else None,
            'ji_shen': {
                'liu_qin': shen_system.ji_shen.liu_qin,
                'wu_xing': shen_system.ji_shen.wu_xing,
                'positions': shen_system.ji_shen.positions
            } if shen_system.ji_shen else None,
            'chou_shen': {
                'liu_qin': shen_system.chou_shen.liu_qin,
                'wu_xing': shen_system.chou_shen.wu_xing,
                'positions': shen_system.chou_shen.positions
            } if shen_system.chou_shen else None
        },
        'fu_shen': [
            {
                'liu_qin': fs.liu_qin,
                'wu_xing': fs.wu_xing,
                'na_jia': fs.na_jia,
                'fei_shen_position': fs.fei_shen_position,
                'fei_shen_liu_qin': fs.fei_shen_liu_qin,
                'is_available': fs.is_available,
                'availability_reason': fs.availability_reason
            } for fs in fu_shen_list
        ] if fu_shen_list else None
    }


class LiuyaoAdvancedAnalyzer:
    """六爻高级分析器类"""
    
    def __init__(self, hexagram_data: Dict, question: str = "", date: Optional[datetime] = None):
        self.hexagram_data = hexagram_data
        self.question = question
        self.date = date or datetime.now()
        self._analysis_result = None
    
    def analyze(self) -> Dict[str, Any]:
        """执行完整分析"""
        if self._analysis_result is None:
            self._analysis_result = perform_advanced_analysis(
                self.hexagram_data, self.question, self.date
            )
        return self._analysis_result
    
    def get_ganzhi_time(self) -> Dict:
        """获取干支时间"""
        result = self.analyze()
        return result.get('ganzhi_time', {})
    
    def get_kong_wang(self) -> Dict:
        """获取旬空信息"""
        result = self.analyze()
        return result.get('kong_wang', {})
    
    def get_yong_shen(self) -> Dict:
        """获取用神信息"""
        result = self.analyze()
        return result.get('yong_shen', {})
    
    def get_shen_system(self) -> Dict:
        """获取神系信息"""
        result = self.analyze()
        return result.get('shen_system', {})
    
    def get_fu_shen(self) -> Optional[List[Dict]]:
        """获取伏神信息"""
        result = self.analyze()
        return result.get('fu_shen')
    
    def get_extended_yaos(self) -> List[Dict]:
        """获取扩展爻信息"""
        result = self.analyze()
        return result.get('extended_yaos', [])


def calculate_time_recommendations(hexagram_data: Dict, question: str = "") -> Dict[str, Any]:
    """
    计算时间建议（应期推算）
    
    Args:
        hexagram_data: 卦象数据
        question: 问事内容
    
    Returns:
        时间建议结果
    """
    analyzer = LiuyaoAdvancedAnalyzer(hexagram_data, question)
    result = analyzer.analyze()
    
    recommendations = []
    extended_yaos = result.get('extended_yaos', [])
    yong_shen = result.get('yong_shen', {})
    kong_wang = result.get('kong_wang', {})
    
    # 基于用神状态推算应期
    yong_shen_positions = yong_shen.get('positions', [])
    if yong_shen_positions:
        for pos in yong_shen_positions:
            if pos <= len(extended_yaos):
                yao = extended_yaos[pos - 1]
                strength = yao.get('strength', {})
                special_status = strength.get('special_status', '无')
                
                if special_status == '暗动':
                    recommendations.append({
                        'type': 'an_dong',
                        'description': f'用神暗动，事近成，应期在日冲之日'
                    })
                elif yao.get('kong_wang_state') == '真空':
                    kong_dizhi = kong_wang.get('kong_dizhi', [])
                    recommendations.append({
                        'type': 'kong_wang',
                        'description': f'用神空亡，出空之日应期，即逢{kong_dizhi}日'
                    })
                elif yao.get('is_moving'):
                    change = yao.get('change_analysis')
                    if change and change.get('hua_type'):
                        recommendations.append({
                            'type': 'moving',
                            'description': f'用神发动，{change.get("description", "")}'
                        })
    
    # 基于六冲卦推算
    liu_chong = result.get('liu_chong_gua', {})
    if liu_chong.get('is_liu_chong_gua'):
        recommendations.append({
            'type': 'liu_chong',
            'description': '六冲卦主散，应期较急，宜速不宜迟'
        })
    
    return {
        'recommendations': recommendations,
        'yong_shen': yong_shen,
        'kong_wang': kong_wang
    }
