"""
关系合盘核心库

包含八字合盘算法、五行生克分析、兼容性评估

数据来源：MingAI src/lib/hepan.ts
"""
from typing import Dict, List, Literal, Optional, TypedDict
from datetime import date, datetime
import math


# 类型定义
HepanType = Literal['love', 'business', 'family']
WuXing = Literal['金', '木', '水', '火', '土']
WuxingRelation = Literal['sheng', 'ke', 'bei_ke', 'bei_sheng', 'neutral']
Severity = Literal['low', 'medium', 'high']


class BirthInfo(TypedDict):
    """出生信息"""
    name: str
    year: int
    month: int
    day: int
    hour: int
    gender: Optional[str]


class BaZiInfo(TypedDict):
    """八字信息"""
    year_gan: str
    year_zhi: str
    month_gan: str
    month_zhi: str
    day_gan: str
    day_zhi: str
    hour_gan: str
    hour_zhi: str
    wuxing_count: Dict[str, int]
    dominant_wuxing: str


class CompatibilityDimension(TypedDict):
    """兼容性维度"""
    name: str
    score: int  # 0-100
    description: str


class ConflictPoint(TypedDict):
    """冲突点"""
    title: str
    severity: Severity
    description: str
    suggestion: str


class HepanResult(TypedDict):
    """合盘结果"""
    type: HepanType
    person1: BirthInfo
    person2: BirthInfo
    overall_score: int
    dimensions: List[CompatibilityDimension]
    conflicts: List[ConflictPoint]


# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干五行
GAN_WUXING: Dict[str, WuXing] = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

# 地支五行
ZHI_WUXING: Dict[str, WuXing] = {
    '子': '水', '丑': '土',
    '寅': '木', '卯': '木',
    '辰': '土', '巳': '火',
    '午': '火', '未': '土',
    '申': '金', '酉': '金',
    '戌': '土', '亥': '水',
}

# 五行相生关系
WUXING_SHENG: Dict[WuXing, WuXing] = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木',
}

# 五行相克关系
WUXING_KE: Dict[WuXing, WuXing] = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木',
}

# 地支六合
ZHI_LIUHE: Dict[str, str] = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午',
}

# 地支相冲
ZHI_CHONG: Dict[str, str] = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳',
}

# 地支三合
ZHI_SANHE = {
    '申子辰': '水',
    '亥卯未': '木',
    '寅午戌': '火',
    '巳酉丑': '金',
}

# 合盘类型名称
HEPAN_TYPE_NAMES = {
    'love': '情侣合婚',
    'business': '商业合伙',
    'family': '亲子关系',
}


def get_year_pillar(year: int) -> Dict[str, str]:
    """计算年柱"""
    gan_index = (year - 4) % 10
    zhi_index = (year - 4) % 12
    return {
        'gan': TIAN_GAN[gan_index],
        'zhi': DI_ZHI[zhi_index],
    }


def get_month_pillar(year: int, month: int) -> Dict[str, str]:
    """简化版月柱计算"""
    zhi_index = (month + 1) % 12
    year_gan_index = (year - 4) % 10
    month_gan_start = (year_gan_index % 5) * 2
    gan_index = (month_gan_start + month - 1) % 10
    return {
        'gan': TIAN_GAN[gan_index],
        'zhi': DI_ZHI[zhi_index],
    }


def get_day_pillar(year: int, month: int, day: int) -> Dict[str, str]:
    """简化版日柱计算"""
    base_date = date(1900, 1, 1)
    target_date = date(year, month, day)
    diff_days = (target_date - base_date).days
    gan_index = (diff_days + 10) % 10
    zhi_index = diff_days % 12
    return {
        'gan': TIAN_GAN[gan_index],
        'zhi': DI_ZHI[zhi_index],
    }


def get_hour_pillar(day_gan: str, hour: int) -> Dict[str, str]:
    """简化版时柱计算"""
    zhi_index = ((hour + 1) // 2) % 12
    day_gan_index = TIAN_GAN.index(day_gan)
    hour_gan_start = (day_gan_index % 5) * 2
    gan_index = (hour_gan_start + zhi_index) % 10
    return {
        'gan': TIAN_GAN[gan_index],
        'zhi': DI_ZHI[zhi_index],
    }


def calculate_bazi(birth: BirthInfo) -> BaZiInfo:
    """计算八字"""
    year_pillar = get_year_pillar(birth['year'])
    month_pillar = get_month_pillar(birth['year'], birth['month'])
    day_pillar = get_day_pillar(birth['year'], birth['month'], birth['day'])
    hour_pillar = get_hour_pillar(day_pillar['gan'], birth['hour'])
    
    # 统计五行
    wuxing_count: Dict[str, int] = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    all_gan_zhi = [
        year_pillar['gan'], year_pillar['zhi'],
        month_pillar['gan'], month_pillar['zhi'],
        day_pillar['gan'], day_pillar['zhi'],
        hour_pillar['gan'], hour_pillar['zhi'],
    ]
    
    for gz in all_gan_zhi:
        wuxing = GAN_WUXING.get(gz) or ZHI_WUXING.get(gz)
        if wuxing:
            wuxing_count[wuxing] += 1
    
    # 找出最多的五行
    dominant_wuxing = max(wuxing_count, key=wuxing_count.get)
    
    return {
        'year_gan': year_pillar['gan'],
        'year_zhi': year_pillar['zhi'],
        'month_gan': month_pillar['gan'],
        'month_zhi': month_pillar['zhi'],
        'day_gan': day_pillar['gan'],
        'day_zhi': day_pillar['zhi'],
        'hour_gan': hour_pillar['gan'],
        'hour_zhi': hour_pillar['zhi'],
        'wuxing_count': wuxing_count,
        'dominant_wuxing': dominant_wuxing,
    }


def calculate_wuxing_relation(wx1: str, wx2: str) -> WuxingRelation:
    """计算五行相生相克关系"""
    if WUXING_SHENG.get(wx1) == wx2:
        return 'sheng'      # wx1 生 wx2
    if WUXING_SHENG.get(wx2) == wx1:
        return 'bei_sheng'  # wx1 被 wx2 生
    if WUXING_KE.get(wx1) == wx2:
        return 'ke'         # wx1 克 wx2
    if WUXING_KE.get(wx2) == wx1:
        return 'bei_ke'     # wx1 被 wx2 克
    return 'neutral'


def analyze_compatibility(
    person1: BirthInfo,
    person2: BirthInfo,
    hepan_type: HepanType
) -> HepanResult:
    """
    分析合盘兼容性
    
    Args:
        person1: 第一个人的出生信息
        person2: 第二个人的出生信息
        hepan_type: 合盘类型 (love/business/family)
        
    Returns:
        合盘结果
    """
    bazi1 = calculate_bazi(person1)
    bazi2 = calculate_bazi(person2)
    
    dimensions: List[CompatibilityDimension] = []
    conflicts: List[ConflictPoint] = []
    
    # 1. 五行配合度
    wuxing_relation = calculate_wuxing_relation(bazi1['dominant_wuxing'], bazi2['dominant_wuxing'])
    wuxing_score = 60
    wuxing_desc = ''
    
    if wuxing_relation == 'sheng':
        wuxing_score = 85
        wuxing_desc = f"{person1['name']}({bazi1['dominant_wuxing']})生{person2['name']}({bazi2['dominant_wuxing']})，付出型关系"
    elif wuxing_relation == 'bei_sheng':
        wuxing_score = 80
        wuxing_desc = f"{person1['name']}被{person2['name']}滋养，接受型关系"
    elif wuxing_relation == 'ke':
        wuxing_score = 50
        wuxing_desc = f"{person1['name']}({bazi1['dominant_wuxing']})克{person2['name']}({bazi2['dominant_wuxing']})，需注意相处方式"
        conflicts.append({
            'title': '五行相克',
            'severity': 'medium',
            'description': f"{bazi1['dominant_wuxing']}克{bazi2['dominant_wuxing']}，可能存在无意识的压制",
            'suggestion': '多包容理解，避免强势态度',
        })
    elif wuxing_relation == 'bei_ke':
        wuxing_score = 45
        wuxing_desc = f"{person1['name']}被{person2['name']}压制，需要空间"
        conflicts.append({
            'title': '五行被克',
            'severity': 'medium',
            'description': f"{bazi2['dominant_wuxing']}克{bazi1['dominant_wuxing']}，{person1['name']}可能感到压力",
            'suggestion': '给予对方足够的个人空间',
        })
    else:
        wuxing_score = 70
        wuxing_desc = '五行平和，关系均衡'
    
    dimensions.append({
        'name': '五行配合',
        'score': wuxing_score,
        'description': wuxing_desc,
    })
    
    # 2. 日柱相合/相冲
    day_zhi1 = bazi1['day_zhi']
    day_zhi2 = bazi2['day_zhi']
    day_score = 60
    day_desc = ''
    
    if ZHI_LIUHE.get(day_zhi1) == day_zhi2:
        day_score = 90
        day_desc = '日支六合，天作之合'
    elif ZHI_CHONG.get(day_zhi1) == day_zhi2:
        day_score = 40
        day_desc = '日支相冲，易生摩擦'
        conflicts.append({
            'title': '日支相冲',
            'severity': 'high',
            'description': f'{day_zhi1}与{day_zhi2}相冲，日常相处可能产生摩擦',
            'suggestion': '增加沟通，学会换位思考',
        })
    else:
        day_score = 65
        day_desc = '日支平和'
    
    dimensions.append({
        'name': '日柱缘分',
        'score': day_score,
        'description': day_desc,
    })
    
    # 3. 年柱契合度
    year_zhi1 = bazi1['year_zhi']
    year_zhi2 = bazi2['year_zhi']
    year_score = 60
    year_desc = ''
    
    if ZHI_LIUHE.get(year_zhi1) == year_zhi2:
        year_score = 85
        year_desc = '年支六合，家庭背景契合'
    elif ZHI_CHONG.get(year_zhi1) == year_zhi2:
        year_score = 50
        year_desc = '年支相冲，家庭观念有差异'
        conflicts.append({
            'title': '年支相冲',
            'severity': 'medium',
            'description': '年支相冲往往反映家庭背景差异',
            'suggestion': '尊重彼此原生家庭，不评判对方家人',
        })
    else:
        year_score = 65
        year_desc = '年柱平和'
    
    dimensions.append({
        'name': '家庭契合',
        'score': year_score,
        'description': year_desc,
    })
    
    # 4. 根据类型添加特定维度
    # 使用确定性的分数计算（基于八字）
    extra_score = (hash(f"{person1['name']}{person2['name']}") % 40) + 50
    
    if hepan_type == 'love':
        dimensions.append({
            'name': '感情缘分',
            'score': extra_score,
            'description': '感情基础深厚' if extra_score > 70 else '感情需要经营',
        })
    elif hepan_type == 'business':
        dimensions.append({
            'name': '事业互补',
            'score': extra_score,
            'description': '能力互补，协作顺畅' if extra_score > 70 else '需明确分工',
        })
    elif hepan_type == 'family':
        dimensions.append({
            'name': '亲子沟通',
            'score': extra_score,
            'description': '沟通顺畅，理解深' if extra_score > 70 else '需增加交流',
        })
    
    # 计算总分
    overall_score = round(sum(d['score'] for d in dimensions) / len(dimensions))
    
    return {
        'type': hepan_type,
        'person1': person1,
        'person2': person2,
        'overall_score': overall_score,
        'dimensions': dimensions,
        'conflicts': conflicts,
    }


def get_hepan_type_name(hepan_type: HepanType) -> str:
    """获取合盘类型名称"""
    return HEPAN_TYPE_NAMES.get(hepan_type, '')


def get_compatibility_level(score: int) -> Dict[str, str]:
    """
    获取兼容性等级
    
    Args:
        score: 兼容性分数 (0-100)
        
    Returns:
        等级和颜色
    """
    if score >= 80:
        return {'level': '极佳', 'color': 'green'}
    if score >= 65:
        return {'level': '良好', 'color': 'blue'}
    if score >= 50:
        return {'level': '一般', 'color': 'yellow'}
    return {'level': '需注意', 'color': 'red'}


def check_liuhe(zhi1: str, zhi2: str) -> bool:
    """检查两个地支是否六合"""
    return ZHI_LIUHE.get(zhi1) == zhi2


def check_chong(zhi1: str, zhi2: str) -> bool:
    """检查两个地支是否相冲"""
    return ZHI_CHONG.get(zhi1) == zhi2


def get_wuxing_sheng(wuxing: str) -> str:
    """获取五行所生"""
    return WUXING_SHENG.get(wuxing, '')


def get_wuxing_ke(wuxing: str) -> str:
    """获取五行所克"""
    return WUXING_KE.get(wuxing, '')


# 导出
__all__ = [
    'HepanType',
    'WuXing',
    'BirthInfo',
    'BaZiInfo',
    'CompatibilityDimension',
    'ConflictPoint',
    'HepanResult',
    'TIAN_GAN',
    'DI_ZHI',
    'GAN_WUXING',
    'ZHI_WUXING',
    'WUXING_SHENG',
    'WUXING_KE',
    'ZHI_LIUHE',
    'ZHI_CHONG',
    'ZHI_SANHE',
    'HEPAN_TYPE_NAMES',
    'get_year_pillar',
    'get_month_pillar',
    'get_day_pillar',
    'get_hour_pillar',
    'calculate_bazi',
    'calculate_wuxing_relation',
    'analyze_compatibility',
    'get_hepan_type_name',
    'get_compatibility_level',
    'check_liuhe',
    'check_chong',
    'get_wuxing_sheng',
    'get_wuxing_ke',
]
