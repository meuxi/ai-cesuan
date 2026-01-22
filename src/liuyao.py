"""
六爻算法模块 - 完整移植自源项目
包含：64卦名、纳甲法、六亲、世应、六神、变卦、伏神计算
"""
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import IntEnum
from datetime import datetime


class LineType(IntEnum):
    """爻类型"""
    SHAO_YANG = 0  # 少阳 (—) 静阳
    SHAO_YIN = 1   # 少阴 (--) 静阴
    LAO_YANG = 2   # 老阳 (— O) 动阳→阴
    LAO_YIN = 3    # 老阴 (-- X) 动阴→阳


@dataclass
class Trigram:
    """八卦"""
    name: str           # 英文名
    chinese_name: str   # 中文名
    nature: str         # 自然象
    number: int         # 卦数 1-8
    element: str        # 五行
    binary: str         # 二进制表示


@dataclass
class FuShenInfo:
    """伏神信息"""
    stem: str           # 天干
    branch: str         # 地支
    relation: str       # 六亲
    element: str        # 五行


@dataclass
class LineDetails:
    """爻详细信息"""
    index: int                      # 爻位 0-5
    line_type: LineType             # 爻类型
    is_moving: bool                 # 是否动爻
    stem: str                       # 天干
    branch: str                     # 地支
    element: str                    # 五行
    six_relation: str               # 六亲
    six_beast: str                  # 六神
    is_shi: bool                    # 是否世爻
    is_ying: bool                   # 是否应爻
    fu_shen: Optional[FuShenInfo] = None  # 伏神
    changed_type: Optional[LineType] = None      # 变爻类型
    changed_branch: Optional[str] = None         # 变爻地支
    changed_stem: Optional[str] = None           # 变爻天干
    changed_relation: Optional[str] = None       # 变爻六亲


@dataclass
class HexagramInfo:
    """卦象信息"""
    name: str                       # 卦名
    palace_name: str                # 宫名
    palace_element: str             # 宫五行
    lines: List[LineDetails]        # 六爻详情
    transformed_name: Optional[str] = None  # 变卦名


# ========== 常量定义 ==========

# 八卦定义
TRIGRAMS: Dict[int, Trigram] = {
    1: Trigram('Heaven', '乾', 'Sky', 1, '金', '111'),
    2: Trigram('Lake', '兑', 'Marsh', 2, '金', '011'),
    3: Trigram('Fire', '离', 'Fire', 3, '火', '101'),
    4: Trigram('Thunder', '震', 'Thunder', 4, '木', '001'),
    5: Trigram('Wind', '巽', 'Wind', 5, '木', '110'),
    6: Trigram('Water', '坎', 'Water', 6, '水', '010'),
    7: Trigram('Mountain', '艮', 'Mountain', 7, '土', '100'),
    8: Trigram('Earth', '坤', 'Earth', 8, '土', '000'),
}

# 天干
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 六神
SIX_BEASTS = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']

# 五亲
ALL_RELATIONS = ['父母', '兄弟', '官鬼', '妻财', '子孙']

# 地支五行映射
BRANCH_ELEMENTS: Dict[str, str] = {
    '子': '水', '亥': '水',
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '申': '金', '酉': '金',
    '辰': '土', '戌': '土', '丑': '土', '未': '土'
}

# 纳甲法规则 (卦数 -> 内卦地支、外卦地支、内卦天干、外卦天干)
NA_JIA_RULES: Dict[int, Dict] = {
    1: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '甲', 'outer_stem': '壬'},
    2: {'inner': ['巳', '卯', '丑'], 'outer': ['亥', '酉', '未'], 'inner_stem': '丁', 'outer_stem': '丁'},
    3: {'inner': ['卯', '丑', '亥'], 'outer': ['酉', '未', '巳'], 'inner_stem': '己', 'outer_stem': '己'},
    4: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '庚', 'outer_stem': '庚'},
    5: {'inner': ['丑', '亥', '酉'], 'outer': ['未', '巳', '卯'], 'inner_stem': '辛', 'outer_stem': '辛'},
    6: {'inner': ['寅', '辰', '午'], 'outer': ['申', '戌', '子'], 'inner_stem': '戊', 'outer_stem': '戊'},
    7: {'inner': ['辰', '午', '申'], 'outer': ['戌', '子', '寅'], 'inner_stem': '丙', 'outer_stem': '丙'},
    8: {'inner': ['未', '巳', '卯'], 'outer': ['丑', '亥', '酉'], 'inner_stem': '乙', 'outer_stem': '癸'},
}

# 64卦名 (上卦数 -> 下卦数 -> 卦名)
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


# ========== 辅助函数 ==========

def get_trigram_number(num: int) -> int:
    """获取卦数 (1-8)"""
    rem = num % 8
    return 8 if rem == 0 else rem


def get_moving_line_position(num: int) -> int:
    """获取动爻位置 (1-6)"""
    rem = num % 6
    return 6 if rem == 0 else rem


def determine_line(backs: int) -> LineType:
    """根据背面数量确定爻类型 (摇钱法)"""
    if backs == 1:
        return LineType.SHAO_YANG
    elif backs == 2:
        return LineType.SHAO_YIN
    elif backs == 3:
        return LineType.LAO_YANG
    else:  # backs == 0
        return LineType.LAO_YIN


def get_line_name(line_type: LineType) -> str:
    """获取爻名"""
    names = {
        LineType.SHAO_YANG: '少阳',
        LineType.SHAO_YIN: '少阴',
        LineType.LAO_YANG: '老阳',
        LineType.LAO_YIN: '老阴',
    }
    return names.get(line_type, '未知')


def to_binary(lines: List[LineType]) -> List[bool]:
    """将爻类型转换为二进制 (阳=True, 阴=False)"""
    return [line in (LineType.SHAO_YANG, LineType.LAO_YANG) for line in lines]


def get_trigram_index(l1: bool, l2: bool, l3: bool) -> int:
    """根据三爻获取卦数"""
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


def get_palace_and_shi_ying(lines: List[bool]) -> Dict:
    """获取宫位和世应位置"""
    target = lines.copy()
    
    def is_pure(l: List[bool]) -> bool:
        lower = get_trigram_index(l[0], l[1], l[2])
        upper = get_trigram_index(l[3], l[4], l[5])
        return lower == upper
    
    # 纯卦
    if is_pure(target):
        return {
            'palace_trigram': get_trigram_index(target[0], target[1], target[2]),
            'shi': 5,
            'ying': 2
        }
    
    # 一世卦
    target[0] = not target[0]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 0, 'ying': 3}
    
    # 二世卦
    target[1] = not target[1]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 1, 'ying': 4}
    
    # 三世卦
    target[2] = not target[2]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 2, 'ying': 5}
    
    # 四世卦
    target[3] = not target[3]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 3, 'ying': 0}
    
    # 五世卦
    target[4] = not target[4]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 4, 'ying': 1}
    
    # 游魂卦
    target[3] = not target[3]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 3, 'ying': 0}
    
    # 归魂卦
    target[0] = not target[0]
    target[1] = not target[1]
    target[2] = not target[2]
    if is_pure(target):
        return {'palace_trigram': get_trigram_index(target[0], target[1], target[2]), 'shi': 2, 'ying': 5}
    
    return {'palace_trigram': 1, 'shi': 0, 'ying': 0}


def get_relation(palace_element: str, line_element: str) -> str:
    """计算六亲关系"""
    relation_map = {
        '金': {'金': '兄弟', '木': '妻财', '水': '子孙', '火': '官鬼', '土': '父母'},
        '木': {'金': '官鬼', '木': '兄弟', '水': '父母', '火': '子孙', '土': '妻财'},
        '水': {'金': '父母', '木': '子孙', '水': '兄弟', '火': '妻财', '土': '官鬼'},
        '火': {'金': '妻财', '木': '父母', '水': '官鬼', '火': '兄弟', '土': '子孙'},
        '土': {'金': '子孙', '木': '官鬼', '水': '妻财', '火': '父母', '土': '兄弟'},
    }
    return relation_map.get(palace_element, {}).get(line_element, '兄弟')


def get_day_stem() -> str:
    """获取当日天干（简化算法）"""
    now = datetime.now()
    # 简化算法：基于公元元年1月1日为庚申日（天干索引6）
    # 计算从基准日期到现在的总天数
    base_date = datetime(2000, 1, 1)  # 2000年1月1日为戊午日
    base_stem_idx = 4  # 戊
    days_diff = (now - base_date).days
    idx = (base_stem_idx + days_diff) % 10
    return HEAVENLY_STEMS[idx]


def get_six_beasts_start(day_stem: str) -> int:
    """根据日干获取六神起始位置"""
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
    """获取卦象基本信息 (地支、天干、六亲)"""
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
            'relation': relation
        })
    
    return result


# ========== 核心计算函数 ==========

def calculate_hexagram(lines: List[LineType]) -> HexagramInfo:
    """计算完整卦象信息"""
    binary = to_binary(lines)
    lower_idx = get_trigram_index(binary[0], binary[1], binary[2])
    upper_idx = get_trigram_index(binary[3], binary[4], binary[5])
    
    name = HEXAGRAM_NAMES[upper_idx][lower_idx]
    palace_info = get_palace_and_shi_ying(binary)
    palace_trigram = palace_info['palace_trigram']
    shi = palace_info['shi']
    ying = palace_info['ying']
    
    palace_element = TRIGRAMS[palace_trigram].element
    palace_name = TRIGRAMS[palace_trigram].chinese_name + '宫'
    
    # 1. 计算本卦详情
    main_hex_info = get_hexagram_basic_info(upper_idx, lower_idx, palace_element)
    
    # 2. 计算六神
    start_beast = get_six_beasts_start(get_day_stem())
    
    # 3. 计算变卦
    has_moving = any(l in (LineType.LAO_YANG, LineType.LAO_YIN) for l in lines)
    transformed_details = []
    transformed_name = None
    
    if has_moving:
        transformed_binary = []
        for l in lines:
            if l == LineType.LAO_YANG:
                transformed_binary.append(False)  # 老阳变阴
            elif l == LineType.LAO_YIN:
                transformed_binary.append(True)   # 老阴变阳
            elif l == LineType.SHAO_YANG:
                transformed_binary.append(True)
            else:
                transformed_binary.append(False)
        
        t_lower = get_trigram_index(transformed_binary[0], transformed_binary[1], transformed_binary[2])
        t_upper = get_trigram_index(transformed_binary[3], transformed_binary[4], transformed_binary[5])
        
        transformed_details = get_hexagram_basic_info(t_upper, t_lower, palace_element)
        transformed_name = HEXAGRAM_NAMES[t_upper][t_lower]
    
    # 4. 计算伏神
    present_relations = set(info['relation'] for info in main_hex_info)
    missing_relations = [r for r in ALL_RELATIONS if r not in present_relations]
    fu_shen_map: Dict[int, FuShenInfo] = {}
    
    if missing_relations:
        # 生成本宫纯卦信息
        palace_hex_info = get_hexagram_basic_info(palace_trigram, palace_trigram, palace_element)
        
        for missing in missing_relations:
            for idx, info in enumerate(palace_hex_info):
                if info['relation'] == missing:
                    fu_shen_map[idx] = FuShenInfo(
                        stem=info['stem'],
                        branch=info['branch'],
                        relation=info['relation'],
                        element=info['element']
                    )
                    break
    
    # 5. 构建爻详情
    line_details = []
    for i, l in enumerate(lines):
        info = main_hex_info[i]
        
        changed_type = None
        changed_branch = None
        changed_stem = None
        changed_relation = None
        
        if has_moving and transformed_details:
            t_info = transformed_details[i]
            if l == LineType.LAO_YANG:
                changed_type = LineType.SHAO_YIN
            elif l == LineType.LAO_YIN:
                changed_type = LineType.SHAO_YANG
            changed_branch = t_info['branch']
            changed_stem = t_info['stem']
            changed_relation = t_info['relation']
        
        line_details.append(LineDetails(
            index=i,
            line_type=l,
            is_moving=l in (LineType.LAO_YANG, LineType.LAO_YIN),
            stem=info['stem'],
            branch=info['branch'],
            element=info['element'],
            six_relation=info['relation'],
            six_beast=SIX_BEASTS[(start_beast + i) % 6],
            is_shi=i == shi,
            is_ying=i == ying,
            fu_shen=fu_shen_map.get(i),
            changed_type=changed_type,
            changed_branch=changed_branch,
            changed_stem=changed_stem,
            changed_relation=changed_relation
        ))
    
    return HexagramInfo(
        name=name,
        palace_name=palace_name,
        palace_element=palace_element,
        lines=line_details,
        transformed_name=transformed_name
    )


def build_hexagram_from_trigrams(upper: int, lower: int, moving_line_pos: int) -> List[LineType]:
    """根据上下卦和动爻位置构建卦象 (数理卦/时空卦)"""
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
    for index, is_yang in enumerate(all_static_lines):
        line_pos = index + 1
        is_moving = line_pos == moving_line_pos
        if is_moving:
            result.append(LineType.LAO_YANG if is_yang else LineType.LAO_YIN)
        else:
            result.append(LineType.SHAO_YANG if is_yang else LineType.SHAO_YIN)
    
    return result


# ========== 起卦方法 ==========

def coin_cast_single() -> Tuple[LineType, int]:
    """
    摇钱法单次起卦 (模拟三枚铜钱)
    返回: (爻类型, 背面数量)
    """
    import random
    backs = sum(random.choice([0, 1]) for _ in range(3))
    return determine_line(backs), backs


def coin_cast_full() -> List[Tuple[LineType, int]]:
    """摇钱法完整起卦 (六次)"""
    return [coin_cast_single() for _ in range(6)]


def number_method(upper_num: int, lower_num: int, moving_num: int) -> List[LineType]:
    """
    数理起卦法
    upper_num: 上卦数字
    lower_num: 下卦数字
    moving_num: 动爻数字
    """
    upper = get_trigram_number(upper_num)
    lower = get_trigram_number(lower_num)
    moving = get_moving_line_position(moving_num)
    return build_hexagram_from_trigrams(upper, lower, moving)


def time_method() -> List[LineType]:
    """
    时空起卦法 (基于当前时间)
    上卦 = 时 + 分
    下卦 = 日 + 月
    动爻 = 上卦数 + 下卦数
    """
    now = datetime.now()
    hours = now.hour
    minutes = now.minute
    day = now.day
    month = now.month
    
    upper = get_trigram_number(hours + minutes)
    lower = get_trigram_number(day + month)
    moving = get_moving_line_position(upper + lower)
    
    return build_hexagram_from_trigrams(upper, lower, moving)


# ========== 数据转换 ==========

def hexagram_to_dict(hexagram: HexagramInfo) -> Dict:
    """将卦象信息转换为字典 (用于API响应)"""
    return {
        'name': hexagram.name,
        'palace_name': hexagram.palace_name,
        'palace_element': hexagram.palace_element,
        'transformed_name': hexagram.transformed_name,
        'lines': [
            {
                'index': line.index,
                'type': int(line.line_type),
                'type_name': get_line_name(line.line_type),
                'is_moving': line.is_moving,
                'stem': line.stem,
                'branch': line.branch,
                'element': line.element,
                'six_relation': line.six_relation,
                'six_beast': line.six_beast,
                'is_shi': line.is_shi,
                'is_ying': line.is_ying,
                'fu_shen': {
                    'stem': line.fu_shen.stem,
                    'branch': line.fu_shen.branch,
                    'relation': line.fu_shen.relation,
                    'element': line.fu_shen.element
                } if line.fu_shen else None,
                'changed_type': int(line.changed_type) if line.changed_type is not None else None,
                'changed_branch': line.changed_branch,
                'changed_stem': line.changed_stem,
                'changed_relation': line.changed_relation
            }
            for line in hexagram.lines
        ]
    }


def lines_to_visual(lines: List[LineType]) -> str:
    """将爻列表转换为可视化字符串 (用于AI解卦)"""
    result = []
    for i, l in enumerate(lines):
        result.append(f"爻{i + 1}: {get_line_name(l)}")
    return '\n'.join(result)
