# -*- coding: utf-8 -*-
"""
地支关系分析器
来源：mingpan项目 RelationsAnalyzer.ts
分析八字中的天干合化、地支六合/六冲/三合/三会/刑/害/破
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# 位置索引（用于计算距离）
POSITION_INDEX = {'year': 0, 'month': 1, 'day': 2, 'hour': 3}
POSITION_NAMES = {'year': '年柱', 'month': '月柱', 'day': '日柱', 'hour': '时柱'}


@dataclass
class StemRelation:
    """天干关系"""
    stems: List[str]
    positions: List[str]
    relation_type: str
    element: str
    impact: str  # 正面/负面/中性
    strength: int
    description: str
    meaning: str = ''


@dataclass
class BranchRelation:
    """地支关系"""
    branches: List[str]
    positions: List[str]
    relation_type: str
    subtype: str = ''
    impact: str = '中性'
    strength: int = 5
    element: str = ''
    description: str = ''
    position_type: str = ''  # 相邻/隔位/遥隔
    spacing: int = 0


@dataclass
class RelationsResult:
    """关系分析结果"""
    # 天干关系
    stem_combinations: List[StemRelation] = field(default_factory=list)
    
    # 地支关系
    six_harmonies: List[BranchRelation] = field(default_factory=list)   # 六合
    six_conflicts: List[BranchRelation] = field(default_factory=list)   # 六冲
    six_harms: List[BranchRelation] = field(default_factory=list)       # 六害
    three_punishments: List[BranchRelation] = field(default_factory=list)  # 三刑
    three_harmonies: List[BranchRelation] = field(default_factory=list)    # 三合
    six_destructions: List[BranchRelation] = field(default_factory=list)   # 六破
    three_meetings: List[BranchRelation] = field(default_factory=list)     # 三会
    
    # 概览
    total_relations: int = 0
    positive_count: int = 0
    negative_count: int = 0
    harmony_score: int = 0
    dominant_pattern: str = ''


class RelationsAnalyzer:
    """地支关系分析器"""
    
    # 天干五合
    STEM_COMBINATIONS = [
        {'stems': ['甲', '己'], 'element': '土', 'strength': 8, 'description': '甲己合化土', 'meaning': '中正之合'},
        {'stems': ['乙', '庚'], 'element': '金', 'strength': 8, 'description': '乙庚合化金', 'meaning': '仁义之合'},
        {'stems': ['丙', '辛'], 'element': '水', 'strength': 7, 'description': '丙辛合化水', 'meaning': '威制之合'},
        {'stems': ['丁', '壬'], 'element': '木', 'strength': 6, 'description': '丁壬合化木', 'meaning': '淫匿之合'},
        {'stems': ['戊', '癸'], 'element': '火', 'strength': 6, 'description': '戊癸合化火', 'meaning': '无情之合'},
    ]
    
    # 地支六合
    SIX_HARMONIES = [
        {'branches': ['子', '丑'], 'element': '土', 'strength': 8, 'description': '子丑合化土'},
        {'branches': ['寅', '亥'], 'element': '木', 'strength': 9, 'description': '寅亥合化木'},
        {'branches': ['卯', '戌'], 'element': '火', 'strength': 7, 'description': '卯戌合化火'},
        {'branches': ['辰', '酉'], 'element': '金', 'strength': 8, 'description': '辰酉合化金'},
        {'branches': ['巳', '申'], 'element': '水', 'strength': 6, 'description': '巳申合化水'},
        {'branches': ['午', '未'], 'element': '火', 'strength': 9, 'description': '午未合化火'},
    ]
    
    # 地支六冲
    SIX_CONFLICTS = [
        {'branches': ['子', '午'], 'strength': 9, 'description': '子午冲（水火相冲）'},
        {'branches': ['丑', '未'], 'strength': 7, 'description': '丑未冲（土土相冲）'},
        {'branches': ['寅', '申'], 'strength': 8, 'description': '寅申冲（木金相冲）'},
        {'branches': ['卯', '酉'], 'strength': 9, 'description': '卯酉冲（木金相冲）'},
        {'branches': ['辰', '戌'], 'strength': 6, 'description': '辰戌冲（土土相冲）'},
        {'branches': ['巳', '亥'], 'strength': 8, 'description': '巳亥冲（火水相冲）'},
    ]
    
    # 地支六害
    SIX_HARMS = [
        {'branches': ['子', '未'], 'strength': 6, 'description': '子未害（六亲不和）'},
        {'branches': ['丑', '午'], 'strength': 5, 'description': '丑午害（官鬼相害）'},
        {'branches': ['寅', '巳'], 'strength': 5, 'description': '寅巳害（刑狱之害）'},
        {'branches': ['卯', '辰'], 'strength': 4, 'description': '卯辰害（欺凌之害）'},
        {'branches': ['申', '亥'], 'strength': 5, 'description': '申亥害（恩将仇报）'},
        {'branches': ['酉', '戌'], 'strength': 6, 'description': '酉戌害（嫉妒之害）'},
    ]
    
    # 地支六破
    SIX_DESTRUCTIONS = [
        {'branches': ['子', '酉'], 'strength': 4, 'description': '子酉破'},
        {'branches': ['丑', '辰'], 'strength': 3, 'description': '丑辰破'},
        {'branches': ['寅', '亥'], 'strength': 3, 'description': '寅亥破'},
        {'branches': ['卯', '午'], 'strength': 4, 'description': '卯午破'},
        {'branches': ['巳', '申'], 'strength': 3, 'description': '巳申破'},
        {'branches': ['未', '戌'], 'strength': 4, 'description': '未戌破'},
    ]
    
    # 地支三刑
    THREE_PUNISHMENTS = [
        {'branches': ['寅', '巳', '申'], 'subtype': '无恩之刑', 'strength': 8, 'description': '寅巳申三刑（无恩之刑）'},
        {'branches': ['丑', '戌', '未'], 'subtype': '持势之刑', 'strength': 7, 'description': '丑戌未三刑（持势之刑）'},
        {'branches': ['子', '卯'], 'subtype': '无礼之刑', 'strength': 6, 'description': '子卯刑（无礼之刑）'},
        {'branches': ['辰', '辰'], 'subtype': '自刑', 'strength': 5, 'description': '辰辰自刑'},
        {'branches': ['午', '午'], 'subtype': '自刑', 'strength': 5, 'description': '午午自刑'},
        {'branches': ['酉', '酉'], 'subtype': '自刑', 'strength': 5, 'description': '酉酉自刑'},
        {'branches': ['亥', '亥'], 'subtype': '自刑', 'strength': 5, 'description': '亥亥自刑'},
    ]
    
    # 地支三合
    THREE_HARMONIES = [
        {'branches': ['申', '子', '辰'], 'element': '水', 'strength': 9, 'description': '申子辰三合水局'},
        {'branches': ['亥', '卯', '未'], 'element': '木', 'strength': 9, 'description': '亥卯未三合木局'},
        {'branches': ['寅', '午', '戌'], 'element': '火', 'strength': 9, 'description': '寅午戌三合火局'},
        {'branches': ['巳', '酉', '丑'], 'element': '金', 'strength': 9, 'description': '巳酉丑三合金局'},
    ]
    
    # 地支三会
    THREE_MEETINGS = [
        {'branches': ['寅', '卯', '辰'], 'element': '木', 'strength': 10, 'description': '寅卯辰三会东方木'},
        {'branches': ['巳', '午', '未'], 'element': '火', 'strength': 10, 'description': '巳午未三会南方火'},
        {'branches': ['申', '酉', '戌'], 'element': '金', 'strength': 10, 'description': '申酉戌三会西方金'},
        {'branches': ['亥', '子', '丑'], 'element': '水', 'strength': 10, 'description': '亥子丑三会北方水'},
    ]
    
    @classmethod
    def analyze(cls, bazi: Dict[str, Dict[str, str]]) -> RelationsResult:
        """
        分析八字中的所有干支关系
        
        Args:
            bazi: {'year': {'stem': '甲', 'branch': '子'}, ...}
        """
        stems = [
            {'stem': bazi['year']['stem'], 'position': 'year'},
            {'stem': bazi['month']['stem'], 'position': 'month'},
            {'stem': bazi['day']['stem'], 'position': 'day'},
            {'stem': bazi['hour']['stem'], 'position': 'hour'},
        ]
        
        branches = [
            {'branch': bazi['year']['branch'], 'position': 'year'},
            {'branch': bazi['month']['branch'], 'position': 'month'},
            {'branch': bazi['day']['branch'], 'position': 'day'},
            {'branch': bazi['hour']['branch'], 'position': 'hour'},
        ]
        
        result = RelationsResult()
        
        # 天干关系
        result.stem_combinations = cls._find_stem_combinations(stems)
        
        # 地支关系
        result.six_harmonies = cls._find_six_harmonies(branches)
        result.six_conflicts = cls._find_six_conflicts(branches)
        result.six_harms = cls._find_six_harms(branches)
        result.three_punishments = cls._find_three_punishments(branches)
        result.three_harmonies = cls._find_three_harmonies(branches)
        result.six_destructions = cls._find_six_destructions(branches)
        result.three_meetings = cls._find_three_meetings(branches)
        
        # 计算概览
        cls._calculate_overview(result)
        
        return result
    
    @classmethod
    def _get_position_relation(cls, pos1: str, pos2: str) -> Tuple[str, int]:
        """计算位置关系类型和距离"""
        idx1 = POSITION_INDEX.get(pos1, 0)
        idx2 = POSITION_INDEX.get(pos2, 0)
        spacing = abs(idx1 - idx2)
        
        if spacing == 1:
            return '相邻', spacing
        elif spacing == 2:
            return '隔位', spacing
        else:
            return '遥隔', spacing
    
    @classmethod
    def _apply_position_modifier(cls, base_strength: int, position_type: str) -> int:
        """根据位置类型调整力量"""
        modifiers = {
            '相邻': 1.0,
            '隔位': 0.8,
            '遥隔': 0.6,
        }
        return round(base_strength * modifiers.get(position_type, 1.0))
    
    @classmethod
    def _find_stem_combinations(cls, stems: List[Dict]) -> List[StemRelation]:
        """查找天干五合"""
        combinations = []
        
        for combo in cls.STEM_COMBINATIONS:
            found1 = next((s for s in stems if s['stem'] == combo['stems'][0]), None)
            found2 = next((s for s in stems if s['stem'] == combo['stems'][1]), None)
            
            if found1 and found2:
                pos_type, spacing = cls._get_position_relation(found1['position'], found2['position'])
                strength = cls._apply_position_modifier(combo['strength'], pos_type)
                
                combinations.append(StemRelation(
                    stems=[found1['stem'], found2['stem']],
                    positions=[POSITION_NAMES[found1['position']], POSITION_NAMES[found2['position']]],
                    relation_type='五合',
                    element=combo['element'],
                    impact='正面',
                    strength=strength,
                    description=combo['description'],
                    meaning=combo['meaning']
                ))
        
        return combinations
    
    @classmethod
    def _find_six_harmonies(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支六合"""
        harmonies = []
        
        for harmony in cls.SIX_HARMONIES:
            found1 = next((b for b in branches if b['branch'] == harmony['branches'][0]), None)
            found2 = next((b for b in branches if b['branch'] == harmony['branches'][1]), None)
            
            if found1 and found2:
                pos_type, spacing = cls._get_position_relation(found1['position'], found2['position'])
                strength = cls._apply_position_modifier(harmony['strength'], pos_type)
                
                harmonies.append(BranchRelation(
                    branches=[found1['branch'], found2['branch']],
                    positions=[POSITION_NAMES[found1['position']], POSITION_NAMES[found2['position']]],
                    relation_type='六合',
                    impact='正面',
                    strength=strength,
                    element=harmony['element'],
                    description=harmony['description'],
                    position_type=pos_type,
                    spacing=spacing
                ))
        
        return harmonies
    
    @classmethod
    def _find_six_conflicts(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支六冲"""
        conflicts = []
        
        for conflict in cls.SIX_CONFLICTS:
            found1 = next((b for b in branches if b['branch'] == conflict['branches'][0]), None)
            found2 = next((b for b in branches if b['branch'] == conflict['branches'][1]), None)
            
            if found1 and found2:
                pos_type, spacing = cls._get_position_relation(found1['position'], found2['position'])
                strength = cls._apply_position_modifier(conflict['strength'], pos_type)
                
                conflicts.append(BranchRelation(
                    branches=[found1['branch'], found2['branch']],
                    positions=[POSITION_NAMES[found1['position']], POSITION_NAMES[found2['position']]],
                    relation_type='六冲',
                    impact='负面',
                    strength=strength,
                    description=conflict['description'],
                    position_type=pos_type,
                    spacing=spacing
                ))
        
        return conflicts
    
    @classmethod
    def _find_six_harms(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支六害"""
        harms = []
        
        for harm in cls.SIX_HARMS:
            found1 = next((b for b in branches if b['branch'] == harm['branches'][0]), None)
            found2 = next((b for b in branches if b['branch'] == harm['branches'][1]), None)
            
            if found1 and found2:
                pos_type, spacing = cls._get_position_relation(found1['position'], found2['position'])
                strength = cls._apply_position_modifier(harm['strength'], pos_type)
                
                harms.append(BranchRelation(
                    branches=[found1['branch'], found2['branch']],
                    positions=[POSITION_NAMES[found1['position']], POSITION_NAMES[found2['position']]],
                    relation_type='六害',
                    impact='负面',
                    strength=strength,
                    description=harm['description'],
                    position_type=pos_type,
                    spacing=spacing
                ))
        
        return harms
    
    @classmethod
    def _find_six_destructions(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支六破"""
        destructions = []
        
        for dest in cls.SIX_DESTRUCTIONS:
            found1 = next((b for b in branches if b['branch'] == dest['branches'][0]), None)
            found2 = next((b for b in branches if b['branch'] == dest['branches'][1]), None)
            
            if found1 and found2:
                pos_type, spacing = cls._get_position_relation(found1['position'], found2['position'])
                strength = cls._apply_position_modifier(dest['strength'], pos_type)
                
                destructions.append(BranchRelation(
                    branches=[found1['branch'], found2['branch']],
                    positions=[POSITION_NAMES[found1['position']], POSITION_NAMES[found2['position']]],
                    relation_type='六破',
                    impact='负面',
                    strength=strength,
                    description=dest['description'],
                    position_type=pos_type,
                    spacing=spacing
                ))
        
        return destructions
    
    @classmethod
    def _find_three_punishments(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支三刑"""
        punishments = []
        branch_list = [b['branch'] for b in branches]
        
        for punishment in cls.THREE_PUNISHMENTS:
            required = punishment['branches']
            
            # 自刑检查
            if len(required) == 2 and required[0] == required[1]:
                count = branch_list.count(required[0])
                if count >= 2:
                    positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] == required[0]]
                    punishments.append(BranchRelation(
                        branches=required,
                        positions=positions[:2],
                        relation_type='三刑',
                        subtype=punishment['subtype'],
                        impact='负面',
                        strength=punishment['strength'],
                        description=punishment['description']
                    ))
            # 三刑检查
            elif len(required) == 3:
                if all(b in branch_list for b in required):
                    positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] in required]
                    punishments.append(BranchRelation(
                        branches=required,
                        positions=positions,
                        relation_type='三刑',
                        subtype=punishment['subtype'],
                        impact='负面',
                        strength=punishment['strength'],
                        description=punishment['description']
                    ))
            # 二刑（子卯刑）
            elif len(required) == 2:
                if all(b in branch_list for b in required):
                    positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] in required]
                    punishments.append(BranchRelation(
                        branches=required,
                        positions=positions,
                        relation_type='三刑',
                        subtype=punishment['subtype'],
                        impact='负面',
                        strength=punishment['strength'],
                        description=punishment['description']
                    ))
        
        return punishments
    
    @classmethod
    def _find_three_harmonies(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支三合"""
        harmonies = []
        branch_list = [b['branch'] for b in branches]
        
        for harmony in cls.THREE_HARMONIES:
            required = harmony['branches']
            matched = [b for b in required if b in branch_list]
            
            # 完整三合
            if len(matched) == 3:
                positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] in required]
                harmonies.append(BranchRelation(
                    branches=required,
                    positions=positions,
                    relation_type='三合',
                    impact='正面',
                    strength=harmony['strength'],
                    element=harmony['element'],
                    description=harmony['description']
                ))
            # 半合（两个地支）
            elif len(matched) == 2:
                positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] in matched]
                harmonies.append(BranchRelation(
                    branches=matched,
                    positions=positions,
                    relation_type='半合',
                    impact='正面',
                    strength=harmony['strength'] - 3,
                    element=harmony['element'],
                    description=f'{matched[0]}{matched[1]}半合{harmony["element"]}局'
                ))
        
        return harmonies
    
    @classmethod
    def _find_three_meetings(cls, branches: List[Dict]) -> List[BranchRelation]:
        """查找地支三会"""
        meetings = []
        branch_list = [b['branch'] for b in branches]
        
        for meeting in cls.THREE_MEETINGS:
            required = meeting['branches']
            matched = [b for b in required if b in branch_list]
            
            if len(matched) == 3:
                positions = [POSITION_NAMES[b['position']] for b in branches if b['branch'] in required]
                meetings.append(BranchRelation(
                    branches=required,
                    positions=positions,
                    relation_type='三会',
                    impact='正面',
                    strength=meeting['strength'],
                    element=meeting['element'],
                    description=meeting['description']
                ))
        
        return meetings
    
    @classmethod
    def _calculate_overview(cls, result: RelationsResult) -> None:
        """计算概览统计"""
        all_relations = (
            result.stem_combinations +
            result.six_harmonies +
            result.six_conflicts +
            result.six_harms +
            result.three_punishments +
            result.three_harmonies +
            result.six_destructions +
            result.three_meetings
        )
        
        result.total_relations = len(all_relations)
        result.positive_count = sum(1 for r in all_relations if getattr(r, 'impact', '') == '正面')
        result.negative_count = sum(1 for r in all_relations if getattr(r, 'impact', '') == '负面')
        
        # 和谐度评分
        positive_score = sum(getattr(r, 'strength', 0) for r in all_relations if getattr(r, 'impact', '') == '正面')
        negative_score = sum(getattr(r, 'strength', 0) for r in all_relations if getattr(r, 'impact', '') == '负面')
        result.harmony_score = max(0, min(100, 50 + positive_score - negative_score))
        
        # 主导模式
        if result.positive_count > result.negative_count:
            result.dominant_pattern = '和合为主'
        elif result.negative_count > result.positive_count:
            result.dominant_pattern = '冲克较多'
        else:
            result.dominant_pattern = '中性平衡'
