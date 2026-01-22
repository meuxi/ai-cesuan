"""
六爻纳甲算法核心

包含完整的纳甲规则、八卦定义、64卦名、世应判断、六亲关系、伏神逻辑

数据来源：六爻起卦工具源码 utils/iching.ts
"""
from typing import Dict, List, Optional, Tuple, TypedDict
from enum import IntEnum


class LineType(IntEnum):
    """爻类型"""
    SHAO_YANG = 0   # 少阳 (静阳)
    SHAO_YIN = 1    # 少阴 (静阴)
    LAO_YANG = 2    # 老阳 (动阳->阴)
    LAO_YIN = 3     # 老阴 (动阴->阳)


class Trigram(TypedDict):
    """八卦定义"""
    name: str          # 英文名
    chinese_name: str  # 中文名
    nature: str        # 象征
    number: int        # 先天数
    element: str       # 五行
    binary: str        # 二进制表示


# 八卦定义
TRIGRAMS: Dict[int, Trigram] = {
    1: {'name': 'Heaven', 'chinese_name': '乾', 'nature': '天', 'number': 1, 'element': '金', 'binary': '111'},
    2: {'name': 'Lake', 'chinese_name': '兑', 'nature': '泽', 'number': 2, 'element': '金', 'binary': '011'},
    3: {'name': 'Fire', 'chinese_name': '离', 'nature': '火', 'number': 3, 'element': '火', 'binary': '101'},
    4: {'name': 'Thunder', 'chinese_name': '震', 'nature': '雷', 'number': 4, 'element': '木', 'binary': '001'},
    5: {'name': 'Wind', 'chinese_name': '巽', 'nature': '风', 'number': 5, 'element': '木', 'binary': '110'},
    6: {'name': 'Water', 'chinese_name': '坎', 'nature': '水', 'number': 6, 'element': '水', 'binary': '010'},
    7: {'name': 'Mountain', 'chinese_name': '艮', 'nature': '山', 'number': 7, 'element': '土', 'binary': '100'},
    8: {'name': 'Earth', 'chinese_name': '坤', 'nature': '地', 'number': 8, 'element': '土', 'binary': '000'},
}

# 天干
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 六神
SIX_BEASTS = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']

# 五种六亲关系
ALL_RELATIONS = ['父母', '兄弟', '官鬼', '妻财', '子孙']

# 地支五行对照
BRANCH_ELEMENTS: Dict[str, str] = {
    '子': '水', '亥': '水',
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '申': '金', '酉': '金',
    '辰': '土', '戌': '土', '丑': '土', '未': '土',
}

# 纳甲规则 (八卦 -> 内卦地支、外卦地支、内卦天干、外卦天干)
NA_JIA_RULES: Dict[int, Dict] = {
    1: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '甲', 'outer_stem': '壬'},  # 乾
    2: {'inner': ['巳', '卯', '丑'], 'outer': ['亥', '酉', '未'], 'inner_stem': '丁', 'outer_stem': '丁'},  # 兑
    3: {'inner': ['卯', '丑', '亥'], 'outer': ['酉', '未', '巳'], 'inner_stem': '己', 'outer_stem': '己'},  # 离
    4: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '庚', 'outer_stem': '庚'},  # 震
    5: {'inner': ['丑', '亥', '酉'], 'outer': ['未', '巳', '卯'], 'inner_stem': '辛', 'outer_stem': '辛'},  # 巽
    6: {'inner': ['寅', '辰', '午'], 'outer': ['申', '戌', '子'], 'inner_stem': '戊', 'outer_stem': '戊'},  # 坎
    7: {'inner': ['辰', '午', '申'], 'outer': ['戌', '子', '寅'], 'inner_stem': '丙', 'outer_stem': '丙'},  # 艮
    8: {'inner': ['未', '巳', '卯'], 'outer': ['丑', '亥', '酉'], 'inner_stem': '乙', 'outer_stem': '癸'},  # 坤
}

# 64卦名对照表 (上卦 -> 下卦 -> 卦名)
HEXAGRAM_NAMES: Dict[int, Dict[int, str]] = {
    1: {1: '乾为天', 2: '天泽履', 3: '天火同人', 4: '天雷无妄', 5: '天风姤', 6: '天水讼', 7: '天山遁', 8: '天地否'},
    2: {1: '泽天夬', 2: '兑为泽', 3: '泽火革', 4: '泽雷随', 5: '泽风大过', 6: '泽水困', 7: '泽山咸', 8: '泽地萃'},
    3: {1: '火天大有', 2: '火泽睽', 3: '离为火', 4: '火雷噬嗑', 5: '火风鼎', 6: '火水未济', 7: '火山旅', 8: '火地晋'},
    4: {1: '雷天大壮', 2: '雷泽归妹', 3: '雷火丰', 4: '震为雷', 5: '雷风恒', 6: '雷水解', 7: '雷山小过', 8: '雷地豫'},
    5: {1: '风天小畜', 2: '风泽中孚', 3: '风火家人', 4: '风雷益', 5: '巽为风', 6: '风水涣', 7: '风山渐', 8: '风地观'},
    6: {1: '水天需', 2: '水泽节', 3: '水火既济', 4: '水雷屯', 5: '水风井', 6: '坎为水', 7: '水山蹇', 8: '水地比'},
    7: {1: '山天大畜', 2: '山泽损', 3: '山火贲', 4: '山雷颐', 5: '山风蛊', 6: '山水蒙', 7: '艮为山', 8: '山地剥'},
    8: {1: '地天泰', 2: '地泽临', 3: '地火明夷', 4: '地雷复', 5: '地风升', 6: '地水师', 7: '地山谦', 8: '坤为地'},
}


def get_trigram_number(num: int) -> int:
    """获取八卦数 (1-8)"""
    rem = num % 8
    return 8 if rem == 0 else rem


def get_moving_line_position(num: int) -> int:
    """获取动爻位置 (1-6)"""
    rem = num % 6
    return 6 if rem == 0 else rem


def determine_line(backs: int) -> LineType:
    """
    根据铜钱背面数确定爻类型
    
    Args:
        backs: 铜钱背面朝上的数量 (0-3)
        
    Returns:
        爻类型
    """
    if backs == 1:
        return LineType.SHAO_YANG
    elif backs == 2:
        return LineType.SHAO_YIN
    elif backs == 3:
        return LineType.LAO_YANG
    else:  # backs == 0
        return LineType.LAO_YIN


def get_line_name(line_type: LineType) -> str:
    """获取爻的中文名称"""
    names = {
        LineType.SHAO_YANG: '少阳',
        LineType.SHAO_YIN: '少阴',
        LineType.LAO_YANG: '老阳',
        LineType.LAO_YIN: '老阴',
    }
    return names.get(line_type, '未知')


def to_binary(lines: List[LineType]) -> List[bool]:
    """将爻列表转换为阴阳二进制 (True=阳, False=阴)"""
    return [l in (LineType.SHAO_YANG, LineType.LAO_YANG) for l in lines]


def get_trigram_index(l1: bool, l2: bool, l3: bool) -> int:
    """
    根据三个爻的阴阳获取八卦索引
    
    Args:
        l1, l2, l3: 初爻、二爻、三爻的阴阳 (True=阳)
        
    Returns:
        八卦索引 (1-8)
    """
    if l1 and l2 and l3:
        return 1  # 乾
    if l1 and l2 and not l3:
        return 2  # 兑
    if l1 and not l2 and l3:
        return 3  # 离
    if l1 and not l2 and not l3:
        return 4  # 震
    if not l1 and l2 and l3:
        return 5  # 巽
    if not l1 and l2 and not l3:
        return 6  # 坎
    if not l1 and not l2 and l3:
        return 7  # 艮
    if not l1 and not l2 and not l3:
        return 8  # 坤
    return 1


def get_palace_and_shi_ying(lines: List[bool]) -> Tuple[int, int, int]:
    """
    计算卦宫和世应位置
    
    Args:
        lines: 六爻阴阳列表
        
    Returns:
        (宫卦索引, 世爻位置, 应爻位置)
    """
    target = lines.copy()
    
    def is_pure(l: List[bool]) -> bool:
        lower = get_trigram_index(l[0], l[1], l[2])
        upper = get_trigram_index(l[3], l[4], l[5])
        return lower == upper
    
    # 本宫卦 (纯卦)
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 5, 2)
    
    # 一世卦
    target[0] = not target[0]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 0, 3)
    
    # 二世卦
    target[1] = not target[1]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 1, 4)
    
    # 三世卦
    target[2] = not target[2]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 2, 5)
    
    # 四世卦
    target[3] = not target[3]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 3, 0)
    
    # 五世卦
    target[4] = not target[4]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 4, 1)
    
    # 游魂卦
    target[3] = not target[3]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 3, 0)
    
    # 归魂卦
    target[0] = not target[0]
    target[1] = not target[1]
    target[2] = not target[2]
    if is_pure(target):
        return (get_trigram_index(target[0], target[1], target[2]), 2, 5)
    
    return (1, 0, 0)


def get_relation(palace_element: str, line_element: str) -> str:
    """
    计算六亲关系
    
    Args:
        palace_element: 卦宫五行
        line_element: 爻位五行
        
    Returns:
        六亲关系
    """
    relation_map = {
        '金': {'金': '兄弟', '木': '妻财', '水': '子孙', '火': '官鬼', '土': '父母'},
        '木': {'金': '官鬼', '木': '兄弟', '水': '父母', '火': '子孙', '土': '妻财'},
        '水': {'金': '父母', '木': '子孙', '水': '兄弟', '火': '妻财', '土': '官鬼'},
        '火': {'金': '妻财', '木': '父母', '水': '官鬼', '火': '兄弟', '土': '子孙'},
        '土': {'金': '子孙', '木': '官鬼', '水': '妻财', '火': '父母', '土': '兄弟'},
    }
    return relation_map.get(palace_element, {}).get(line_element, '兄弟')


def get_six_beasts_start(day_stem: str) -> int:
    """
    根据日干获取六神起始位置
    
    Args:
        day_stem: 日干
        
    Returns:
        起始六神索引 (0-5)
    """
    if day_stem in ['甲', '乙']:
        return 0  # 青龙
    if day_stem in ['丙', '丁']:
        return 1  # 朱雀
    if day_stem == '戊':
        return 2  # 勾陈
    if day_stem == '己':
        return 3  # 螣蛇
    if day_stem in ['庚', '辛']:
        return 4  # 白虎
    return 5  # 玄武


def get_hexagram_basic_info(upper_idx: int, lower_idx: int, palace_element: str) -> List[Dict]:
    """
    获取卦象基本信息 (六爻的地支、天干、五行、六亲)
    
    Args:
        upper_idx: 上卦索引
        lower_idx: 下卦索引
        palace_element: 卦宫五行
        
    Returns:
        六爻基本信息列表
    """
    lower_rule = NA_JIA_RULES[lower_idx]
    upper_rule = NA_JIA_RULES[upper_idx]
    
    all_branches = lower_rule['inner'] + upper_rule['outer']
    all_stems = [lower_rule['inner_stem']] * 3 + [upper_rule['outer_stem']] * 3
    
    result = []
    for i, branch in enumerate(all_branches):
        stem = all_stems[i]
        element = BRANCH_ELEMENTS[branch]
        relation = get_relation(palace_element, element)
        result.append({
            'branch': branch,
            'stem': stem,
            'element': element,
            'relation': relation,
        })
    
    return result


def get_hexagram_name(upper_idx: int, lower_idx: int) -> str:
    """获取卦名"""
    return HEXAGRAM_NAMES.get(upper_idx, {}).get(lower_idx, '未知卦')


def build_hexagram_from_trigrams(upper: int, lower: int, moving_line_pos: int) -> List[LineType]:
    """
    从上下卦和动爻位置构建六爻
    
    Args:
        upper: 上卦数 (1-8)
        lower: 下卦数 (1-8)
        moving_line_pos: 动爻位置 (1-6)
        
    Returns:
        六爻类型列表
    """
    trigram_lines = {
        1: [True, True, True],      # 乾 ☰
        2: [True, True, False],     # 兑 ☱
        3: [True, False, True],     # 离 ☲
        4: [True, False, False],    # 震 ☳
        5: [False, True, True],     # 巽 ☴
        6: [False, True, False],    # 坎 ☵
        7: [False, False, True],    # 艮 ☶
        8: [False, False, False],   # 坤 ☷
    }
    
    lower_lines = trigram_lines[lower]
    upper_lines = trigram_lines[upper]
    all_static_lines = lower_lines + upper_lines
    
    result = []
    for i, is_yang in enumerate(all_static_lines):
        line_pos = i + 1
        is_moving = line_pos == moving_line_pos
        if is_moving:
            result.append(LineType.LAO_YANG if is_yang else LineType.LAO_YIN)
        else:
            result.append(LineType.SHAO_YANG if is_yang else LineType.SHAO_YIN)
    
    return result


# 导出
__all__ = [
    'LineType',
    'Trigram',
    'TRIGRAMS',
    'HEAVENLY_STEMS',
    'SIX_BEASTS',
    'ALL_RELATIONS',
    'BRANCH_ELEMENTS',
    'NA_JIA_RULES',
    'HEXAGRAM_NAMES',
    'get_trigram_number',
    'get_moving_line_position',
    'determine_line',
    'get_line_name',
    'to_binary',
    'get_trigram_index',
    'get_palace_and_shi_ying',
    'get_relation',
    'get_six_beasts_start',
    'get_hexagram_basic_info',
    'get_hexagram_name',
    'build_hexagram_from_trigrams',
]
