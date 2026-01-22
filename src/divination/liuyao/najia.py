# -*- coding: utf-8 -*-
"""
六爻纳甲算法
来源：六爻起卦工具源码 utils/iching.ts
包含八卦数据、纳甲规则、64卦名、六亲关系、六神等
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# 八卦数据（先天八卦序）
TRIGRAMS = {
    1: {'name': 'Heaven', 'chinese_name': '乾', 'nature': 'Sky', 'element': '金', 'binary': '111'},
    2: {'name': 'Lake', 'chinese_name': '兑', 'nature': 'Marsh', 'element': '金', 'binary': '011'},
    3: {'name': 'Fire', 'chinese_name': '离', 'nature': 'Fire', 'element': '火', 'binary': '101'},
    4: {'name': 'Thunder', 'chinese_name': '震', 'nature': 'Thunder', 'element': '木', 'binary': '001'},
    5: {'name': 'Wind', 'chinese_name': '巽', 'nature': 'Wind', 'element': '木', 'binary': '110'},
    6: {'name': 'Water', 'chinese_name': '坎', 'nature': 'Water', 'element': '水', 'binary': '010'},
    7: {'name': 'Mountain', 'chinese_name': '艮', 'nature': 'Mountain', 'element': '土', 'binary': '100'},
    8: {'name': 'Earth', 'chinese_name': '坤', 'nature': 'Earth', 'element': '土', 'binary': '000'},
}

# 天干
HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 六神
SIX_BEASTS = ['青龙', '朱雀', '勾陈', '螣蛇', '白虎', '玄武']

# 六亲
ALL_RELATIONS = ['父母', '兄弟', '官鬼', '妻财', '子孙']

# 地支五行
BRANCH_ELEMENTS = {
    '子': '水', '亥': '水',
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '申': '金', '酉': '金',
    '辰': '土', '戌': '土', '丑': '土', '未': '土'
}

# 纳甲规则（八卦对应的地支和天干）
NA_JIA_RULES = {
    1: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '甲', 'outer_stem': '壬'},  # 乾
    2: {'inner': ['巳', '卯', '丑'], 'outer': ['亥', '酉', '未'], 'inner_stem': '丁', 'outer_stem': '丁'},  # 兑
    3: {'inner': ['卯', '丑', '亥'], 'outer': ['酉', '未', '巳'], 'inner_stem': '己', 'outer_stem': '己'},  # 离
    4: {'inner': ['子', '寅', '辰'], 'outer': ['午', '申', '戌'], 'inner_stem': '庚', 'outer_stem': '庚'},  # 震
    5: {'inner': ['丑', '亥', '酉'], 'outer': ['未', '巳', '卯'], 'inner_stem': '辛', 'outer_stem': '辛'},  # 巽
    6: {'inner': ['寅', '辰', '午'], 'outer': ['申', '戌', '子'], 'inner_stem': '戊', 'outer_stem': '戊'},  # 坎
    7: {'inner': ['辰', '午', '申'], 'outer': ['戌', '子', '寅'], 'inner_stem': '丙', 'outer_stem': '丙'},  # 艮
    8: {'inner': ['未', '巳', '卯'], 'outer': ['丑', '亥', '酉'], 'inner_stem': '乙', 'outer_stem': '癸'},  # 坤
}

# 64卦名称
HEXAGRAM_NAMES = {
    1: {1: '乾为天', 2: '天泽履', 3: '天火同人', 4: '天雷无妄', 5: '天风姤', 6: '天水讼', 7: '天山遁', 8: '天地否'},
    2: {1: '泽天夬', 2: '兑为泽', 3: '泽火革', 4: '泽雷随', 5: '泽风大过', 6: '泽水困', 7: '泽山咸', 8: '泽地萃'},
    3: {1: '火天大有', 2: '火泽睽', 3: '离为火', 4: '火雷噬嗑', 5: '火风鼎', 6: '火水未济', 7: '火山旅', 8: '火地晋'},
    4: {1: '雷天大壮', 2: '雷泽归妹', 3: '雷火丰', 4: '震为雷', 5: '雷风恒', 6: '雷水解', 7: '雷山小过', 8: '雷地豫'},
    5: {1: '风天小畜', 2: '风泽中孚', 3: '风火家人', 4: '风雷益', 5: '巽为风', 6: '风水涣', 7: '风山渐', 8: '风地观'},
    6: {1: '水天需', 2: '水泽节', 3: '水火既济', 4: '水雷屯', 5: '水风井', 6: '坎为水', 7: '水山蹇', 8: '水地比'},
    7: {1: '山天大畜', 2: '山泽损', 3: '山火贲', 4: '山雷颐', 5: '山风蛊', 6: '山水蒙', 7: '艮为山', 8: '山地剥'},
    8: {1: '地天泰', 2: '地泽临', 3: '地火明夷', 4: '地雷复', 5: '地风升', 6: '地水师', 7: '地山谦', 8: '坤为地'},
}

# 六亲生克关系表
RELATION_MAP = {
    '金': {'金': '兄弟', '木': '妻财', '水': '子孙', '火': '官鬼', '土': '父母'},
    '木': {'金': '官鬼', '木': '兄弟', '水': '父母', '火': '子孙', '土': '妻财'},
    '水': {'金': '父母', '木': '子孙', '水': '兄弟', '火': '妻财', '土': '官鬼'},
    '火': {'金': '妻财', '木': '父母', '水': '官鬼', '火': '兄弟', '土': '子孙'},
    '土': {'金': '子孙', '木': '官鬼', '水': '妻财', '火': '父母', '土': '兄弟'},
}


@dataclass
class LineDetails:
    """爻的详细信息"""
    index: int
    line_type: int  # 0=少阳, 1=少阴, 2=老阳(动), 3=老阴(动)
    is_moving: bool
    branch: str
    stem: str
    element: str
    six_relation: str
    six_beast: str
    is_shi: bool
    is_ying: bool
    fu_shen: Optional[Dict] = None
    changed_branch: Optional[str] = None
    changed_relation: Optional[str] = None


@dataclass
class HexagramInfo:
    """卦象信息"""
    name: str
    palace_name: str
    palace_element: str
    lines: List[LineDetails]
    transformed_name: Optional[str] = None


class LiuYaoCalculator:
    """六爻计算器"""
    
    @classmethod
    def get_trigram_number(cls, num: int) -> int:
        """获取八卦序数"""
        rem = num % 8
        return 8 if rem == 0 else rem
    
    @classmethod
    def get_moving_line_position(cls, num: int) -> int:
        """获取动爻位置"""
        rem = num % 6
        return 6 if rem == 0 else rem
    
    @classmethod
    def determine_line(cls, backs: int) -> int:
        """根据铜钱背面数确定爻类型"""
        if backs == 1:
            return 0  # 少阳
        if backs == 2:
            return 1  # 少阴
        if backs == 3:
            return 2  # 老阳（动）
        return 3  # 老阴（动）
    
    @classmethod
    def get_line_name(cls, line_type: int) -> str:
        """获取爻名"""
        names = {0: '少阳', 1: '少阴', 2: '老阳', 3: '老阴'}
        return names.get(line_type, '未知')
    
    @classmethod
    def to_binary(cls, lines: List[int]) -> List[bool]:
        """转换为二进制（阳为True）"""
        return [l in (0, 2) for l in lines]
    
    @classmethod
    def get_trigram_index(cls, l1: bool, l2: bool, l3: bool) -> int:
        """根据三爻获取八卦序数"""
        mapping = {
            (True, True, True): 1,    # 乾
            (True, True, False): 2,   # 兑
            (True, False, True): 3,   # 离
            (True, False, False): 4,  # 震
            (False, True, True): 5,   # 巽
            (False, True, False): 6,  # 坎
            (False, False, True): 7,  # 艮
            (False, False, False): 8, # 坤
        }
        return mapping.get((l1, l2, l3), 1)
    
    @classmethod
    def get_palace_and_shi_ying(cls, lines: List[bool]) -> Dict[str, int]:
        """获取卦宫和世应位置"""
        target = lines.copy()
        
        def is_pure(l: List[bool]) -> bool:
            lower = cls.get_trigram_index(l[0], l[1], l[2])
            upper = cls.get_trigram_index(l[3], l[4], l[5])
            return lower == upper
        
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 5, 'ying': 2}
        
        target[0] = not target[0]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 0, 'ying': 3}
        
        target[1] = not target[1]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 1, 'ying': 4}
        
        target[2] = not target[2]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 2, 'ying': 5}
        
        target[3] = not target[3]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 3, 'ying': 0}
        
        target[4] = not target[4]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 4, 'ying': 1}
        
        # 游魂
        target[3] = not target[3]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 3, 'ying': 0}
        
        # 归魂
        target[0] = not target[0]
        target[1] = not target[1]
        target[2] = not target[2]
        if is_pure(target):
            return {'palace_trigram': cls.get_trigram_index(target[0], target[1], target[2]), 'shi': 2, 'ying': 5}
        
        return {'palace_trigram': 1, 'shi': 0, 'ying': 0}
    
    @classmethod
    def get_relation(cls, palace_element: str, line_element: str) -> str:
        """获取六亲关系"""
        return RELATION_MAP.get(palace_element, {}).get(line_element, '兄弟')
    
    @classmethod
    def get_day_stem(cls) -> str:
        """获取当日天干 - 基于基准日计算"""
        # 以1900年1月31日甲午日为基准（甲=0）
        base = datetime(1900, 1, 31)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        days_diff = (today - base).days
        return HEAVENLY_STEMS[days_diff % 10]
    
    @classmethod
    def get_six_beasts_start(cls, day_stem: str) -> int:
        """获取六神起始位置"""
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
    
    @classmethod
    def get_hexagram_basic_info(cls, upper_idx: int, lower_idx: int, 
                                 palace_element: str) -> List[Dict]:
        """获取卦象基础信息"""
        lower_rule = NA_JIA_RULES[lower_idx]
        upper_rule = NA_JIA_RULES[upper_idx]
        
        all_branches = lower_rule['inner'] + upper_rule['outer']
        all_stems = [lower_rule['inner_stem']] * 3 + [upper_rule['outer_stem']] * 3
        
        result = []
        for i, branch in enumerate(all_branches):
            stem = all_stems[i]
            element = BRANCH_ELEMENTS[branch]
            relation = cls.get_relation(palace_element, element)
            result.append({
                'branch': branch,
                'stem': stem,
                'element': element,
                'relation': relation
            })
        
        return result
    
    @classmethod
    def calculate_hexagram(cls, lines: List[int]) -> HexagramInfo:
        """
        计算卦象
        
        Args:
            lines: 六爻列表，从下到上 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
                   值: 0=少阳, 1=少阴, 2=老阳(动), 3=老阴(动)
        """
        binary = cls.to_binary(lines)
        lower_idx = cls.get_trigram_index(binary[0], binary[1], binary[2])
        upper_idx = cls.get_trigram_index(binary[3], binary[4], binary[5])
        
        name = HEXAGRAM_NAMES[upper_idx][lower_idx]
        palace_info = cls.get_palace_and_shi_ying(binary)
        palace_trigram = palace_info['palace_trigram']
        shi = palace_info['shi']
        ying = palace_info['ying']
        
        palace_element = TRIGRAMS[palace_trigram]['element']
        palace_name = TRIGRAMS[palace_trigram]['chinese_name'] + '宫'
        
        # 主卦信息
        main_hex_info = cls.get_hexagram_basic_info(upper_idx, lower_idx, palace_element)
        
        # 六神
        start_beast = cls.get_six_beasts_start(cls.get_day_stem())
        
        # 变卦计算
        has_moving = any(l in (2, 3) for l in lines)
        transformed_details = []
        transformed_name = None
        
        if has_moving:
            transformed_binary = []
            for l in lines:
                if l == 2:
                    transformed_binary.append(False)  # 老阳变阴
                elif l == 3:
                    transformed_binary.append(True)   # 老阴变阳
                elif l == 0:
                    transformed_binary.append(True)   # 少阳不变
                else:
                    transformed_binary.append(False)  # 少阴不变
            
            t_lower = cls.get_trigram_index(transformed_binary[0], transformed_binary[1], transformed_binary[2])
            t_upper = cls.get_trigram_index(transformed_binary[3], transformed_binary[4], transformed_binary[5])
            
            transformed_details = cls.get_hexagram_basic_info(t_upper, t_lower, palace_element)
            transformed_name = HEXAGRAM_NAMES[t_upper][t_lower]
        
        # 伏神计算
        present_relations = set(info['relation'] for info in main_hex_info)
        missing_relations = [r for r in ALL_RELATIONS if r not in present_relations]
        fu_shen_map = {}
        
        if missing_relations:
            palace_hex_info = cls.get_hexagram_basic_info(palace_trigram, palace_trigram, palace_element)
            
            for missing in missing_relations:
                for idx, info in enumerate(palace_hex_info):
                    if info['relation'] == missing:
                        fu_shen_map[idx] = {
                            'stem': info['stem'],
                            'branch': info['branch'],
                            'relation': info['relation'],
                            'element': info['element']
                        }
                        break
        
        # 构建爻详情
        line_details = []
        for i, l in enumerate(lines):
            info = main_hex_info[i]
            
            changed_branch = None
            changed_relation = None
            
            if has_moving and transformed_details:
                t_info = transformed_details[i]
                changed_branch = t_info['branch']
                changed_relation = t_info['relation']
            
            line_details.append(LineDetails(
                index=i,
                line_type=l,
                is_moving=l in (2, 3),
                branch=info['branch'],
                stem=info['stem'],
                element=info['element'],
                six_relation=info['relation'],
                six_beast=SIX_BEASTS[(start_beast + i) % 6],
                is_shi=i == shi,
                is_ying=i == ying,
                fu_shen=fu_shen_map.get(i),
                changed_branch=changed_branch,
                changed_relation=changed_relation
            ))
        
        return HexagramInfo(
            name=name,
            palace_name=palace_name,
            palace_element=palace_element,
            lines=line_details,
            transformed_name=transformed_name
        )
    
    @classmethod
    def build_hexagram_from_trigrams(cls, upper: int, lower: int, 
                                      moving_line_pos: int) -> List[int]:
        """根据上下卦和动爻位置构建六爻"""
        trigram_lines = {
            1: [True, True, True],      # 乾
            2: [True, True, False],     # 兑
            3: [True, False, True],     # 离
            4: [True, False, False],    # 震
            5: [False, True, True],     # 巽
            6: [False, True, False],    # 坎
            7: [False, False, True],    # 艮
            8: [False, False, False],   # 坤
        }
        
        lower_lines = trigram_lines[lower]
        upper_lines = trigram_lines[upper]
        all_static_lines = lower_lines + upper_lines
        
        result = []
        for i, is_yang in enumerate(all_static_lines):
            line_pos = i + 1
            is_moving = line_pos == moving_line_pos
            if is_moving:
                result.append(2 if is_yang else 3)
            else:
                result.append(0 if is_yang else 1)
        
        return result
    
    @classmethod
    def coin_toss_hexagram(cls, tosses: List[List[int]]) -> HexagramInfo:
        """
        铜钱起卦
        
        Args:
            tosses: 六次摇钱结果，每次三枚铜钱的背面数量
                    [[1,0,1], [0,1,1], ...] 或 [2, 2, 1, 3, 2, 1]
        """
        lines = []
        for toss in tosses:
            if isinstance(toss, list):
                backs = sum(toss)
            else:
                backs = toss
            lines.append(cls.determine_line(backs))
        
        return cls.calculate_hexagram(lines)


# 八宫数据（导出用）
EIGHT_PALACES = TRIGRAMS


def najia_calculate(lines: List[int]) -> Dict[str, Any]:
    """
    纳甲计算入口函数
    
    Args:
        lines: 六爻列表，从下到上 [初爻, 二爻, 三爻, 四爻, 五爻, 上爻]
               值: 0=少阳, 1=少阴, 2=老阳(动), 3=老阴(动)
    
    Returns:
        包含卦象完整信息的字典
    """
    hex_info = LiuYaoCalculator.calculate_hexagram(lines)
    
    # 转换为字典格式
    return {
        'name': hex_info.name,
        'palace_name': hex_info.palace_name,
        'palace_element': hex_info.palace_element,
        'transformed_name': hex_info.transformed_name,
        'lines': [
            {
                'index': line.index,
                'line_type': line.line_type,
                'is_moving': line.is_moving,
                'branch': line.branch,
                'stem': line.stem,
                'element': line.element,
                'six_relation': line.six_relation,
                'six_beast': line.six_beast,
                'is_shi': line.is_shi,
                'is_ying': line.is_ying,
                'fu_shen': line.fu_shen,
                'changed_branch': line.changed_branch,
                'changed_relation': line.changed_relation
            }
            for line in hex_info.lines
        ]
    }
