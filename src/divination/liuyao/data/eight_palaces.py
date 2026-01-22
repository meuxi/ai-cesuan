"""
八宫纳甲系统
用于六爻占卜的核心数据结构，包含六亲、世应计算等

数据来源：MingAI eight-palaces.ts
"""
from typing import TypedDict, List, Literal


# 五行类型
WuXing = Literal['金', '木', '水', '火', '土']

# 八宫名称
PalaceName = Literal['乾宫', '坎宫', '艮宫', '震宫', '巽宫', '离宫', '坤宫', '兑宫']

# 地支
DIZHI = ('子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥')

# 地支五行
DIZHI_WUXING: dict[str, WuXing] = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水',
}

# 天干
TIANGAN = ('甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸')

# 天干五行
TIANGAN_WUXING: dict[str, WuXing] = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火',
    '戊': '土', '己': '土', '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

# 五行相生
WUXING_SHENG = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
}

# 五行相克
WUXING_KE = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
}


class Palace(TypedDict):
    """八宫结构"""
    name: PalaceName           # 宫名
    element: WuXing            # 五行
    trigram: str               # 八卦代码
    hexagrams: List[str]       # 本宫8卦编码
    hexagram_names: List[str]  # 本宫8卦名称
    na_jia_yang: List[str]     # 阳爻纳甲 (1-6爻)
    na_jia_yin: List[str]      # 阴爻纳甲 (1-6爻)


# 八宫数据
# 每宫包含8个卦，按照：本卦→一世→二世→三世→四世→五世→游魂→归魂 顺序
EIGHT_PALACES: dict[PalaceName, Palace] = {
    '乾宫': {
        'name': '乾宫',
        'element': '金',
        'trigram': '111',
        'hexagrams': ['111111', '011111', '001111', '000111', '000011', '000001', '000101', '111101'],
        'hexagram_names': ['乾为天', '天风姤', '天山遯', '天地否', '风地观', '山地剥', '火地晋', '火天大有'],
        'na_jia_yang': ['子', '寅', '辰', '午', '申', '戌'],
        'na_jia_yin': ['丑', '亥', '酉', '未', '巳', '卯'],
    },
    '坎宫': {
        'name': '坎宫',
        'element': '水',
        'trigram': '010',
        'hexagrams': ['010010', '110010', '100010', '101010', '101110', '101100', '101000', '010000'],
        'hexagram_names': ['坎为水', '水泽节', '水雷屯', '水火既济', '泽火革', '雷火丰', '地火明夷', '地水师'],
        'na_jia_yang': ['寅', '辰', '午', '申', '戌', '子'],
        'na_jia_yin': ['卯', '丑', '亥', '酉', '未', '巳'],
    },
    '艮宫': {
        'name': '艮宫',
        'element': '土',
        'trigram': '001',
        'hexagrams': ['001001', '101001', '111001', '110001', '110101', '110111', '110011', '001011'],
        'hexagram_names': ['艮为山', '山火贲', '山天大畜', '山泽损', '火泽睽', '天泽履', '风泽中孚', '风山渐'],
        'na_jia_yang': ['辰', '午', '申', '戌', '子', '寅'],
        'na_jia_yin': ['巳', '卯', '丑', '亥', '酉', '未'],
    },
    '震宫': {
        'name': '震宫',
        'element': '木',
        'trigram': '100',
        'hexagrams': ['100100', '000100', '010100', '011100', '011000', '011010', '011110', '100110'],
        'hexagram_names': ['震为雷', '雷地豫', '雷水解', '雷风恒', '地风升', '水风井', '泽风大过', '泽雷随'],
        'na_jia_yang': ['子', '寅', '辰', '午', '申', '戌'],
        'na_jia_yin': ['未', '巳', '卯', '丑', '亥', '酉'],
    },
    '巽宫': {
        'name': '巽宫',
        'element': '木',
        'trigram': '011',
        'hexagrams': ['011011', '111011', '101011', '100011', '100111', '100101', '100001', '011001'],
        'hexagram_names': ['巽为风', '风天小畜', '风火家人', '风雷益', '天雷无妄', '火雷噬嗑', '山雷颐', '山风蛊'],
        'na_jia_yang': ['丑', '亥', '酉', '未', '巳', '卯'],
        'na_jia_yin': ['子', '寅', '辰', '午', '申', '戌'],
    },
    '离宫': {
        'name': '离宫',
        'element': '火',
        'trigram': '101',
        'hexagrams': ['101101', '001101', '011101', '010101', '010001', '010011', '010111', '101111'],
        'hexagram_names': ['离为火', '火山旅', '火风鼎', '火水未济', '山水蒙', '风水涣', '天水讼', '天火同人'],
        'na_jia_yang': ['卯', '丑', '亥', '酉', '未', '巳'],
        'na_jia_yin': ['寅', '辰', '午', '申', '戌', '子'],
    },
    '坤宫': {
        'name': '坤宫',
        'element': '土',
        'trigram': '000',
        'hexagrams': ['000000', '100000', '110000', '111000', '111100', '111110', '111010', '000010'],
        'hexagram_names': ['坤为地', '地雷复', '地泽临', '地天泰', '雷天大壮', '泽天夬', '水天需', '水地比'],
        'na_jia_yang': ['未', '巳', '卯', '丑', '亥', '酉'],
        'na_jia_yin': ['辰', '午', '申', '戌', '子', '寅'],
    },
    '兑宫': {
        'name': '兑宫',
        'element': '金',
        'trigram': '110',
        'hexagrams': ['110110', '010110', '000110', '001110', '001010', '001000', '001100', '110100'],
        'hexagram_names': ['兑为泽', '泽水困', '泽地萃', '泽山咸', '水山蹇', '地山谦', '雷山小过', '雷泽归妹'],
        'na_jia_yang': ['巳', '卯', '丑', '亥', '酉', '未'],
        'na_jia_yin': ['午', '申', '戌', '子', '寅', '辰'],
    },
}

# 世应位置表（按卦在宫中的位置）
# 本卦(0): 世6应3, 一世(1): 世1应4, 二世(2): 世2应5, 三世(3): 世3应6
# 四世(4): 世4应1, 五世(5): 世5应2, 游魂(6): 世4应1, 归魂(7): 世3应6
SHI_YING_TABLE = [
    (6, 3),  # 本卦
    (1, 4),  # 一世
    (2, 5),  # 二世
    (3, 6),  # 三世
    (4, 1),  # 四世
    (5, 2),  # 五世
    (4, 1),  # 游魂
    (3, 6),  # 归魂
]


def get_palace_by_hexagram(hexagram_code: str) -> tuple[Palace, int] | None:
    """
    根据卦码找到所属宫位和在宫中的位置
    
    Args:
        hexagram_code: 6位二进制卦码 (从下到上)
        
    Returns:
        (宫位信息, 在宫中的位置0-7) 或 None
    """
    for palace in EIGHT_PALACES.values():
        if hexagram_code in palace['hexagrams']:
            position = palace['hexagrams'].index(hexagram_code)
            return palace, position
    return None


def get_najia(palace: Palace, position: int, yao_type: int) -> str:
    """
    获取纳甲地支
    
    Args:
        palace: 宫位信息
        position: 爻位 (0-5, 对应初爻到上爻)
        yao_type: 爻类型 (1=阳爻, 0=阴爻)
        
    Returns:
        纳甲地支
    """
    if yao_type == 1:
        return palace['na_jia_yang'][position]
    else:
        return palace['na_jia_yin'][position]


def get_shi_ying_position(gua_position: int) -> tuple[int, int]:
    """
    获取世爻和应爻位置
    
    Args:
        gua_position: 卦在宫中的位置 (0-7)
        
    Returns:
        (世爻位置, 应爻位置) 1-6
    """
    return SHI_YING_TABLE[gua_position]


def get_liu_qin(day_element: WuXing, yao_element: WuXing) -> str:
    """
    根据日主五行和爻五行计算六亲
    
    Args:
        day_element: 日主五行
        yao_element: 爻五行
        
    Returns:
        六亲名称
    """
    if day_element == yao_element:
        return '兄弟'
    elif WUXING_SHENG.get(day_element) == yao_element:
        return '子孙'
    elif WUXING_KE.get(day_element) == yao_element:
        return '妻财'
    elif WUXING_SHENG.get(yao_element) == day_element:
        return '父母'
    elif WUXING_KE.get(yao_element) == day_element:
        return '官鬼'
    return '未知'


# 六神（六兽）
LIU_SHEN = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']

# 六神起始对应日干
LIU_SHEN_START = {
    '甲': 0, '乙': 0,  # 甲乙日起青龙
    '丙': 1, '丁': 1,  # 丙丁日起朱雀
    '戊': 2,           # 戊日起勾陈
    '己': 3,           # 己日起螣蛇
    '庚': 4, '辛': 4,  # 庚辛日起白虎
    '壬': 5, '癸': 5,  # 壬癸日起玄武
}


def get_liu_shen(day_gan: str, yao_position: int) -> str:
    """
    获取六神
    
    Args:
        day_gan: 日干
        yao_position: 爻位 (1-6)
        
    Returns:
        六神名称
    """
    start = LIU_SHEN_START.get(day_gan, 0)
    index = (start + yao_position - 1) % 6
    return LIU_SHEN[index]
