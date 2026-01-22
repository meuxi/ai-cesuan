"""
神煞数据大全
八字命理中的吉神凶煞定义与计算规则

数据来源：Y-AI-Fortune constants.py + 《子平基础概要》
"""
from typing import Dict, List, Optional, Union


# 十神定义
TEN_GODS = {
    '正印': {
        'meaning': '生我且阴阳异性',
        'family': '母亲',
        'effect': '主文书、学业、贵人',
        'positive': ['聪明好学', '有长辈缘', '文采出众'],
        'negative': ['依赖心强', '懒散', '不切实际'],
    },
    '偏印': {
        'meaning': '生我且阴阳同性',
        'family': '继母',
        'effect': '主艺术、偏业、特殊技能',
        'positive': ['艺术天赋', '特殊才能', '悟性高'],
        'negative': ['孤僻', '不合群', '想法怪异'],
    },
    '正官': {
        'meaning': '克我且阴阳异性',
        'family': '女命丈夫',
        'effect': '主官贵、名声、约束',
        'positive': ['正直守法', '有官运', '受人尊敬'],
        'negative': ['胆小怕事', '循规蹈矩', '不敢冒险'],
    },
    '七杀': {
        'meaning': '克我且阴阳同性',
        'family': '女命偏夫',
        'effect': '主权威、竞争、压力',
        'positive': ['有魄力', '敢于竞争', '适合武职'],
        'negative': ['性急冲动', '容易树敌', '压力大'],
    },
    '正财': {
        'meaning': '我克且阴阳异性',
        'family': '男命正妻',
        'effect': '主正财、辛勤致富',
        'positive': ['勤劳致富', '理财有道', '重视家庭'],
        'negative': ['保守', '斤斤计较', '缺乏冒险精神'],
    },
    '偏财': {
        'meaning': '我克且阴阳同性',
        'family': '父亲、偏妻',
        'effect': '主偏财、投机取利',
        'positive': ['人缘好', '意外之财', '慷慨大方'],
        'negative': ['好赌博', '不务正业', '花钱大手'],
    },
    '食神': {
        'meaning': '我生且阴阳异性',
        'family': '女儿',
        'effect': '主口才、艺术、餐饮',
        'positive': ['口才好', '懂享受', '有福气'],
        'negative': ['贪图享乐', '懒惰', '好逸恶劳'],
    },
    '伤官': {
        'meaning': '我生且阴阳同性',
        'family': '儿子',
        'effect': '主反叛、创新、艺术',
        'positive': ['才华横溢', '创新能力强', '敢于突破'],
        'negative': ['目中无人', '恃才傲物', '不服管教'],
    },
    '比肩': {
        'meaning': '同我且阴阳同性',
        'family': '兄弟',
        'effect': '主友情、合作、竞争',
        'positive': ['重友情', '独立自主', '能吃苦'],
        'negative': ['固执己见', '不听劝告', '好争斗'],
    },
    '劫财': {
        'meaning': '同我且阴阳异性',
        'family': '姐妹',
        'effect': '主争夺、投机、破财',
        'positive': ['胆大', '敢于冒险', '交际广'],
        'negative': ['破财', '争夺', '不稳定'],
    },
}


# 神煞大全
SHEN_SHA = {
    # 贵人类
    '天乙贵人': {
        'meaning': '最重要的贵人星',
        'effect': '主贵人相助，遇难呈祥，有权威地位',
        'rule': {
            '甲': ['丑', '未'], '戊': ['丑', '未'],
            '乙': ['子', '申'], '己': ['子', '申'],
            '丙': ['亥', '酉'], '丁': ['亥', '酉'],
            '庚': ['午', '寅'], '辛': ['午', '寅'],
            '壬': ['巳', '卯'], '癸': ['巳', '卯'],
        },
        'type': '吉神',
    },
    '太极贵人': {
        'meaning': '聪明好学之星',
        'effect': '主聪明好学，喜神秘文化，有宗教缘分',
        'rule': {
            '甲': ['子', '午'], '乙': ['子', '午'],
            '丙': ['卯', '酉'], '丁': ['卯', '酉'],
            '戊': ['辰', '戌'], '己': ['辰', '戌'],
            '庚': ['丑', '未'], '辛': ['丑', '未'],
            '壬': ['寅', '申'], '癸': ['寅', '申'],
        },
        'type': '吉神',
    },
    '文昌贵人': {
        'meaning': '文学艺术之星',
        'effect': '主文学才华，利考试升学，聪明好学',
        'rule': {
            '甲': '巳', '乙': '午', '丙': '申', '丁': '酉', '戊': '申',
            '己': '酉', '庚': '亥', '辛': '子', '壬': '寅', '癸': '卯',
        },
        'type': '吉神',
    },
    '华盖': {
        'meaning': '艺术玄学之星',
        'effect': '主艺术天赋，喜神秘学术，有宗教倾向',
        'rule': {
            '申子辰': '辰', '亥卯未': '未',
            '寅午戌': '戌', '巳酉丑': '丑',
        },
        'type': '吉神',
    },
    '禄神': {
        'meaning': '财禄福星',
        'effect': '主财源稳定，福禄丰厚，衣食无忧',
        'rule': {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
            '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子',
        },
        'type': '吉神',
    },
    
    # 桃花类
    '桃花': {
        'meaning': '异性缘桃花星',
        'effect': '主异性缘佳，感情丰富，人缘好',
        'rule': {
            '申子辰': '酉', '亥卯未': '子',
            '寅午戌': '卯', '巳酉丑': '午',
        },
        'type': '中性',
    },
    '红鸾': {
        'meaning': '婚姻喜庆之星',
        'effect': '主婚姻喜庆，感情顺利，人缘佳',
        'rule': {
            '子': '卯', '丑': '寅', '寅': '丑', '卯': '子',
            '辰': '亥', '巳': '戌', '午': '酉', '未': '申',
            '申': '未', '酉': '午', '戌': '巳', '亥': '辰',
        },
        'type': '吉神',
    },
    
    # 权威类
    '将星': {
        'meaning': '领导统御之星',
        'effect': '主领导才能，有权威，能统御他人',
        'rule': {
            '寅午戌': '午', '申子辰': '子',
            '亥卯未': '卯', '巳酉丑': '酉',
        },
        'type': '吉神',
    },
    '驿马': {
        'meaning': '奔波变动之星',
        'effect': '主奔波劳碌，多变动，利外出发展',
        'rule': {
            '寅午戌': '申', '申子辰': '寅',
            '亥卯未': '巳', '巳酉丑': '亥',
        },
        'type': '中性',
    },
    
    # 凶煞类
    '羊刃': {
        'meaning': '刚强急躁之星',
        'effect': '主性格刚强，易冲动，有军警武职才能',
        'rule': {
            '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午',
            '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥',
        },
        'type': '凶煞',
    },
    '劫煞': {
        'meaning': '灾劫之星',
        'effect': '主意外灾祸，需防小人，谨慎行事',
        'rule': {
            '申子辰': '巳', '亥卯未': '申',
            '寅午戌': '亥', '巳酉丑': '寅',
        },
        'type': '凶煞',
    },
    '亡神': {
        'meaning': '耗散之星',
        'effect': '主精力耗散，易失财物，需防盗窃',
        'rule': {
            '申子辰': '亥', '亥卯未': '寅',
            '寅午戌': '巳', '巳酉丑': '申',
        },
        'type': '凶煞',
    },
    '孤辰': {
        'meaning': '孤独之星',
        'effect': '主孤独，不利婚姻，宜修行',
        'rule': {
            '亥子丑': '寅', '寅卯辰': '巳',
            '巳午未': '申', '申酉戌': '亥',
        },
        'type': '凶煞',
    },
    '寡宿': {
        'meaning': '寡居之星',
        'effect': '主寡居，婚姻不顺，宜修行',
        'rule': {
            '亥子丑': '戌', '寅卯辰': '丑',
            '巳午未': '辰', '申酉戌': '未',
        },
        'type': '凶煞',
    },
}


# 三合局
SAN_HE = {
    '申子辰': '水',
    '亥卯未': '木',
    '寅午戌': '火',
    '巳酉丑': '金',
}


def get_ten_god_info(god: str) -> Optional[Dict]:
    """获取十神详细信息"""
    return TEN_GODS.get(god)


def get_shensha_info(name: str) -> Optional[Dict]:
    """获取神煞详细信息"""
    return SHEN_SHA.get(name)


def check_tianyi_guiren(day_gan: str, branches: List[str]) -> List[str]:
    """
    检查天乙贵人
    
    Args:
        day_gan: 日干
        branches: 四柱地支列表
        
    Returns:
        包含天乙贵人的地支列表
    """
    rule = SHEN_SHA['天乙贵人']['rule'].get(day_gan, [])
    return [b for b in branches if b in rule]


def check_wenchange(day_gan: str, branches: List[str]) -> List[str]:
    """检查文昌贵人"""
    rule = SHEN_SHA['文昌贵人']['rule'].get(day_gan)
    if rule:
        return [b for b in branches if b == rule]
    return []


def check_lushen(day_gan: str, branches: List[str]) -> List[str]:
    """检查禄神"""
    rule = SHEN_SHA['禄神']['rule'].get(day_gan)
    if rule:
        return [b for b in branches if b == rule]
    return []


def get_sanhe_element(branch: str) -> Optional[str]:
    """获取地支所属三合局的五行"""
    for key, element in SAN_HE.items():
        if branch in key:
            return element
    return None


def check_taohua(year_zhi: str, branches: List[str]) -> List[str]:
    """检查桃花"""
    for key, taohua in SHEN_SHA['桃花']['rule'].items():
        if year_zhi in key:
            return [b for b in branches if b == taohua]
    return []


def check_yima(year_zhi: str, branches: List[str]) -> List[str]:
    """检查驿马"""
    for key, yima in SHEN_SHA['驿马']['rule'].items():
        if year_zhi in key:
            return [b for b in branches if b == yima]
    return []


# 导出
__all__ = [
    'TEN_GODS',
    'SHEN_SHA',
    'SAN_HE',
    'get_ten_god_info',
    'get_shensha_info',
    'check_tianyi_guiren',
    'check_wenchange',
    'check_lushen',
    'get_sanhe_element',
    'check_taohua',
    'check_yima',
]
