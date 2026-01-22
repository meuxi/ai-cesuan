# -*- coding: utf-8 -*-
"""
日主强弱分析器 - 360分量化算法
来源：mingpan项目 StrengthAnalyzer.ts
基于《八字旺衰量化算法研究》规范
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# ========== 常量定义 ==========

# 总能量池
TOTAL_ENERGY = 360
MONTH_BRANCH_ENERGY = 180  # 50%给月支
OTHER_POSITIONS_ENERGY = 180  # 50%给其他位置

# 各位置权重
POSITION_WEIGHTS = {
    'day_branch': 40,    # 日支
    'month_stem': 35,    # 月干
    'hour_stem': 30,     # 时干
    'hour_branch': 25,   # 时支
    'year_stem': 25,     # 年干
    'year_branch': 25    # 年支
}

# 天干五行映射
STEM_ELEMENT = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 地支藏干及其力量比例
HIDDEN_STEMS = {
    '子': [{'stem': '癸', 'power': 1.0}],
    '丑': [{'stem': '己', 'power': 0.6}, {'stem': '癸', 'power': 0.3}, {'stem': '辛', 'power': 0.1}],
    '寅': [{'stem': '甲', 'power': 0.6}, {'stem': '丙', 'power': 0.3}, {'stem': '戊', 'power': 0.1}],
    '卯': [{'stem': '乙', 'power': 1.0}],
    '辰': [{'stem': '戊', 'power': 0.6}, {'stem': '乙', 'power': 0.3}, {'stem': '癸', 'power': 0.1}],
    '巳': [{'stem': '丙', 'power': 0.6}, {'stem': '庚', 'power': 0.3}, {'stem': '戊', 'power': 0.1}],
    '午': [{'stem': '丁', 'power': 0.7}, {'stem': '己', 'power': 0.3}],
    '未': [{'stem': '己', 'power': 0.6}, {'stem': '丁', 'power': 0.3}, {'stem': '乙', 'power': 0.1}],
    '申': [{'stem': '庚', 'power': 0.6}, {'stem': '壬', 'power': 0.3}, {'stem': '戊', 'power': 0.1}],
    '酉': [{'stem': '辛', 'power': 1.0}],
    '戌': [{'stem': '戊', 'power': 0.6}, {'stem': '辛', 'power': 0.3}, {'stem': '丁', 'power': 0.1}],
    '亥': [{'stem': '壬', 'power': 0.7}, {'stem': '甲', 'power': 0.3}]
}

# 月支司令元素表（按节气日期分段）
MONTH_COMMANDING_ELEMENTS = {
    '寅': [{'element': '戊', 'days': 7}, {'element': '丙', 'days': 7}, {'element': '甲', 'days': 16}],
    '卯': [{'element': '甲', 'days': 10}, {'element': '乙', 'days': 20}],
    '辰': [{'element': '乙', 'days': 9}, {'element': '癸', 'days': 3}, {'element': '戊', 'days': 18}],
    '巳': [{'element': '戊', 'days': 5}, {'element': '庚', 'days': 9}, {'element': '丙', 'days': 16}],
    '午': [{'element': '丙', 'days': 10}, {'element': '己', 'days': 9}, {'element': '丁', 'days': 11}],
    '未': [{'element': '丁', 'days': 9}, {'element': '乙', 'days': 3}, {'element': '己', 'days': 18}],
    '申': [{'element': '己', 'days': 7}, {'element': '壬', 'days': 7}, {'element': '庚', 'days': 16}],
    '酉': [{'element': '庚', 'days': 10}, {'element': '辛', 'days': 20}],
    '戌': [{'element': '辛', 'days': 9}, {'element': '丁', 'days': 3}, {'element': '戊', 'days': 18}],
    '亥': [{'element': '戊', 'days': 7}, {'element': '甲', 'days': 7}, {'element': '壬', 'days': 16}],
    '子': [{'element': '壬', 'days': 10}, {'element': '癸', 'days': 20}],
    '丑': [{'element': '癸', 'days': 9}, {'element': '辛', 'days': 3}, {'element': '己', 'days': 18}]
}

# 距离衰减系数
DISTANCE_DECAY = {
    'adjacent': 1.0,    # 相邻
    'one_apart': 0.7,   # 隔位
    'two_apart': 0.5    # 遥隔
}


class DayMasterStrength(Enum):
    """日主强弱等级"""
    EXTREMELY_WEAK = '衰极'
    WEAK = '身弱'
    SLIGHTLY_WEAK = '偏弱'
    BALANCED = '中和'
    SLIGHTLY_STRONG = '偏强'
    STRONG = '身旺'
    EXTREMELY_STRONG = '旺极'


# 强弱分类阈值
STRENGTH_CATEGORIES = [
    {'min': -360, 'max': -150, 'strength': DayMasterStrength.EXTREMELY_WEAK},
    {'min': -149, 'max': -80, 'strength': DayMasterStrength.WEAK},
    {'min': -79, 'max': -30, 'strength': DayMasterStrength.SLIGHTLY_WEAK},
    {'min': -29, 'max': 29, 'strength': DayMasterStrength.BALANCED},
    {'min': 30, 'max': 79, 'strength': DayMasterStrength.SLIGHTLY_STRONG},
    {'min': 80, 'max': 149, 'strength': DayMasterStrength.STRONG},
    {'min': 150, 'max': 360, 'strength': DayMasterStrength.EXTREMELY_STRONG}
]


@dataclass
class ElementScores:
    """五行分数"""
    wood: float = 0.0
    fire: float = 0.0
    earth: float = 0.0
    metal: float = 0.0
    water: float = 0.0
    
    def __getitem__(self, key: str) -> float:
        return getattr(self, key, 0.0)
    
    def __setitem__(self, key: str, value: float):
        setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, float]:
        return {
            'wood': self.wood,
            'fire': self.fire,
            'earth': self.earth,
            'metal': self.metal,
            'water': self.water
        }


@dataclass
class StrengthAnalysisResult:
    """日主强弱分析结果"""
    strength: DayMasterStrength
    score: float
    percentage: int
    supporting_force: float
    opposing_force: float
    static_scores: Dict[str, float]
    dynamic_scores: Dict[str, float]
    month_commanding_element: str
    detailed_breakdown: List[Dict[str, Any]]
    analysis: str
    suggestions: List[str]


class StrengthAnalyzer:
    """日主强弱分析器 - 360分量化算法"""
    
    @classmethod
    def analyze(cls, bazi: Dict[str, Dict[str, str]], 
                birth_info: Optional[Dict] = None) -> StrengthAnalysisResult:
        """
        分析日主强弱
        
        Args:
            bazi: 八字信息 {'year': {'stem': '甲', 'branch': '子'}, ...}
            birth_info: 出生信息（可选，用于精确计算月令司令）
            
        Returns:
            StrengthAnalysisResult: 分析结果
        """
        day_master = bazi['day']['stem']
        day_master_element = STEM_ELEMENT.get(day_master, '土')
        
        detailed_breakdown = []
        
        # Step 1: 静态评分
        static_scores = cls._calculate_static_scores(bazi, birth_info, detailed_breakdown)
        
        # Step 2: 动态计算
        dynamic_scores, adjustments = cls._apply_dynamic_calculations(
            bazi, static_scores, detailed_breakdown
        )
        
        # Step 3: 计算最终分数
        supporting_force, opposing_force = cls._calculate_forces(
            day_master_element, dynamic_scores
        )
        final_score = supporting_force - opposing_force
        
        # 确定强弱类别
        strength = cls._categorize_strength(final_score)
        
        # 计算百分比
        total_force = supporting_force + opposing_force
        percentage = round((supporting_force / total_force) * 100) if total_force > 0 else 50
        
        # 获取月令司令
        month_commanding = cls._get_month_commanding_element(
            bazi['month']['branch'], birth_info
        )
        
        # 生成分析和建议
        analysis = cls._generate_analysis(strength, final_score, day_master_element)
        suggestions = cls._generate_suggestions(strength, day_master_element)
        
        return StrengthAnalysisResult(
            strength=strength,
            score=final_score,
            percentage=percentage,
            supporting_force=supporting_force,
            opposing_force=opposing_force,
            static_scores=static_scores.to_dict(),
            dynamic_scores=dynamic_scores.to_dict(),
            month_commanding_element=month_commanding,
            detailed_breakdown=detailed_breakdown,
            analysis=analysis,
            suggestions=suggestions
        )
    
    @classmethod
    def _calculate_static_scores(cls, bazi: Dict, birth_info: Optional[Dict],
                                  breakdown: List) -> ElementScores:
        """计算静态分数"""
        scores = ElementScores()
        
        month_branch = bazi['month']['branch']
        commanding_element = cls._get_month_commanding_element(month_branch, birth_info)
        commanding_key = cls._get_element_key(commanding_element)
        
        # 1. 月令司令元素得90分
        COMMANDING_SCORE = 90
        scores[commanding_key] += COMMANDING_SCORE
        breakdown.append({
            'item': f'月支{month_branch}司令{commanding_element}',
            'element': commanding_element,
            'base_score': COMMANDING_SCORE,
            'adjustment': '',
            'final_score': COMMANDING_SCORE
        })
        
        # 2. 剩余90分按月支藏干分配
        cls._distribute_hidden_stem_scores(
            month_branch, 90, '月支', scores, breakdown
        )
        
        # 3. 其他位置分配
        # 年干
        year_stem = bazi['year']['stem']
        year_stem_element = STEM_ELEMENT.get(year_stem, '土')
        year_stem_key = cls._get_element_key(year_stem_element)
        scores[year_stem_key] += POSITION_WEIGHTS['year_stem']
        breakdown.append({
            'item': f'年干{year_stem}',
            'element': year_stem_element,
            'base_score': POSITION_WEIGHTS['year_stem'],
            'adjustment': '',
            'final_score': POSITION_WEIGHTS['year_stem']
        })
        
        # 年支藏干
        cls._distribute_hidden_stem_scores(
            bazi['year']['branch'], POSITION_WEIGHTS['year_branch'], 
            '年支', scores, breakdown
        )
        
        # 月干
        month_stem = bazi['month']['stem']
        month_stem_element = STEM_ELEMENT.get(month_stem, '土')
        month_stem_key = cls._get_element_key(month_stem_element)
        scores[month_stem_key] += POSITION_WEIGHTS['month_stem']
        breakdown.append({
            'item': f'月干{month_stem}',
            'element': month_stem_element,
            'base_score': POSITION_WEIGHTS['month_stem'],
            'adjustment': '',
            'final_score': POSITION_WEIGHTS['month_stem']
        })
        
        # 日支藏干
        cls._distribute_hidden_stem_scores(
            bazi['day']['branch'], POSITION_WEIGHTS['day_branch'],
            '日支', scores, breakdown
        )
        
        # 时干
        hour_stem = bazi['hour']['stem']
        hour_stem_element = STEM_ELEMENT.get(hour_stem, '土')
        hour_stem_key = cls._get_element_key(hour_stem_element)
        scores[hour_stem_key] += POSITION_WEIGHTS['hour_stem']
        breakdown.append({
            'item': f'时干{hour_stem}',
            'element': hour_stem_element,
            'base_score': POSITION_WEIGHTS['hour_stem'],
            'adjustment': '',
            'final_score': POSITION_WEIGHTS['hour_stem']
        })
        
        # 时支藏干
        cls._distribute_hidden_stem_scores(
            bazi['hour']['branch'], POSITION_WEIGHTS['hour_branch'],
            '时支', scores, breakdown
        )
        
        return scores
    
    @classmethod
    def _distribute_hidden_stem_scores(cls, branch: str, total_score: float,
                                        position: str, scores: ElementScores,
                                        breakdown: List):
        """分配地支藏干分数"""
        hidden_stems = HIDDEN_STEMS.get(branch, [])
        for item in hidden_stems:
            stem = item['stem']
            power = item['power']
            element = STEM_ELEMENT.get(stem, '土')
            element_key = cls._get_element_key(element)
            score = round(total_score * power)
            scores[element_key] += score
            
            breakdown.append({
                'item': f'{position}{branch}藏{stem}',
                'element': element,
                'base_score': score,
                'adjustment': '',
                'final_score': score
            })
    
    @classmethod
    def _apply_dynamic_calculations(cls, bazi: Dict, static_scores: ElementScores,
                                     breakdown: List) -> Tuple[ElementScores, List]:
        """应用动态计算（三会、三合、六合、冲、刑、害）"""
        scores = ElementScores(
            wood=static_scores.wood,
            fire=static_scores.fire,
            earth=static_scores.earth,
            metal=static_scores.metal,
            water=static_scores.water
        )
        adjustments = []
        
        branches = [
            bazi['year']['branch'],
            bazi['month']['branch'],
            bazi['day']['branch'],
            bazi['hour']['branch']
        ]
        
        # 1. 检查三会局
        cls._check_three_meetings(branches, scores, adjustments)
        
        # 2. 检查三合局
        cls._check_three_harmonies(branches, scores, adjustments)
        
        # 3. 检查六合
        cls._check_six_combinations(branches, scores, adjustments)
        
        # 4. 检查相冲
        cls._check_clashes(branches, scores, adjustments)
        
        # 5. 检查相刑
        cls._check_punishments(branches, scores, adjustments)
        
        # 6. 检查相害
        cls._check_harms(branches, scores, adjustments)
        
        return scores, adjustments
    
    @classmethod
    def _check_three_meetings(cls, branches: List[str], scores: ElementScores,
                               adjustments: List):
        """检查三会局"""
        meetings = [
            {'branches': ['亥', '子', '丑'], 'element': 'water', 'name': '北方水局'},
            {'branches': ['寅', '卯', '辰'], 'element': 'wood', 'name': '东方木局'},
            {'branches': ['巳', '午', '未'], 'element': 'fire', 'name': '南方火局'},
            {'branches': ['申', '酉', '戌'], 'element': 'metal', 'name': '西方金局'}
        ]
        
        for meeting in meetings:
            found = [b for b in meeting['branches'] if b in branches]
            if len(found) == 3:
                # 三会成局，增加对应五行30%
                scores[meeting['element']] *= 1.3
                adjustments.append({
                    'type': '三会局',
                    'description': f"{meeting['name']}成功",
                    'score_change': scores[meeting['element']] * 0.3
                })
    
    @classmethod
    def _check_three_harmonies(cls, branches: List[str], scores: ElementScores,
                                adjustments: List):
        """检查三合局"""
        harmonies = [
            {'branches': ['申', '子', '辰'], 'element': 'water', 'name': '水局'},
            {'branches': ['亥', '卯', '未'], 'element': 'wood', 'name': '木局'},
            {'branches': ['寅', '午', '戌'], 'element': 'fire', 'name': '火局'},
            {'branches': ['巳', '酉', '丑'], 'element': 'metal', 'name': '金局'}
        ]
        
        for harmony in harmonies:
            found = [b for b in harmony['branches'] if b in branches]
            if len(found) == 3:
                # 三合成局，增加对应五行25%
                scores[harmony['element']] *= 1.25
                adjustments.append({
                    'type': '三合局',
                    'description': f"{harmony['name']}成功",
                    'score_change': scores[harmony['element']] * 0.25
                })
            elif len(found) == 2:
                # 半合，增加10%
                scores[harmony['element']] *= 1.1
                adjustments.append({
                    'type': '半合',
                    'description': f"{harmony['name']}半合",
                    'score_change': scores[harmony['element']] * 0.1
                })
    
    @classmethod
    def _check_six_combinations(cls, branches: List[str], scores: ElementScores,
                                 adjustments: List):
        """检查六合"""
        combinations = [
            {'pair': ['子', '丑'], 'result': 'earth'},
            {'pair': ['寅', '亥'], 'result': 'wood'},
            {'pair': ['卯', '戌'], 'result': 'fire'},
            {'pair': ['辰', '酉'], 'result': 'metal'},
            {'pair': ['巳', '申'], 'result': 'water'},
            {'pair': ['午', '未'], 'result': 'earth'}
        ]
        
        for combo in combinations:
            if combo['pair'][0] in branches and combo['pair'][1] in branches:
                # 六合成功，增加对应五行15%
                scores[combo['result']] *= 1.15
                adjustments.append({
                    'type': '六合',
                    'description': f"{combo['pair'][0]}{combo['pair'][1]}合化",
                    'score_change': scores[combo['result']] * 0.15
                })
    
    @classmethod
    def _check_clashes(cls, branches: List[str], scores: ElementScores,
                        adjustments: List):
        """检查相冲"""
        clashes = [
            ['子', '午'], ['丑', '未'], ['寅', '申'],
            ['卯', '酉'], ['辰', '戌'], ['巳', '亥']
        ]
        
        for clash in clashes:
            if clash[0] in branches and clash[1] in branches:
                # 相冲，双方藏干减力20%
                for branch in clash:
                    hidden = HIDDEN_STEMS.get(branch, [])
                    for item in hidden:
                        element = STEM_ELEMENT.get(item['stem'], '土')
                        key = cls._get_element_key(element)
                        reduction = scores[key] * 0.2 * item['power']
                        scores[key] -= reduction
                
                adjustments.append({
                    'type': '相冲',
                    'description': f"{clash[0]}{clash[1]}相冲",
                    'score_change': -20
                })
    
    @classmethod
    def _check_punishments(cls, branches: List[str], scores: ElementScores,
                            adjustments: List):
        """检查相刑"""
        # 自刑
        self_punishments = ['辰', '午', '酉', '亥']
        branch_counts = {}
        for b in branches:
            branch_counts[b] = branch_counts.get(b, 0) + 1
        
        for branch, count in branch_counts.items():
            if count >= 2 and branch in self_punishments:
                hidden = HIDDEN_STEMS.get(branch, [])
                for item in hidden:
                    element = STEM_ELEMENT.get(item['stem'], '土')
                    key = cls._get_element_key(element)
                    scores[key] *= 0.85
                adjustments.append({
                    'type': '自刑',
                    'description': f'{branch}{branch}自刑',
                    'score_change': -15
                })
        
        # 其他刑
        punishments = [
            ['子', '卯'],  # 无恩之刑
            ['寅', '巳'], ['巳', '申'], ['寅', '申'],  # 恃势之刑
            ['丑', '戌'], ['戌', '未'], ['丑', '未']   # 无礼之刑
        ]
        
        for punishment in punishments:
            if punishment[0] in branches and punishment[1] in branches:
                for branch in punishment:
                    hidden = HIDDEN_STEMS.get(branch, [])
                    for item in hidden:
                        element = STEM_ELEMENT.get(item['stem'], '土')
                        key = cls._get_element_key(element)
                        scores[key] *= 0.9
                adjustments.append({
                    'type': '相刑',
                    'description': f'{punishment[0]}{punishment[1]}相刑',
                    'score_change': -10
                })
    
    @classmethod
    def _check_harms(cls, branches: List[str], scores: ElementScores,
                      adjustments: List):
        """检查相害"""
        harms = [
            ['子', '未'], ['丑', '午'], ['寅', '巳'],
            ['卯', '辰'], ['申', '亥'], ['酉', '戌']
        ]
        
        for harm in harms:
            if harm[0] in branches and harm[1] in branches:
                for branch in harm:
                    hidden = HIDDEN_STEMS.get(branch, [])
                    for item in hidden:
                        element = STEM_ELEMENT.get(item['stem'], '土')
                        key = cls._get_element_key(element)
                        scores[key] *= 0.95
                adjustments.append({
                    'type': '相害',
                    'description': f'{harm[0]}{harm[1]}相害',
                    'score_change': -5
                })
    
    @classmethod
    def _calculate_forces(cls, day_element: str, 
                          scores: ElementScores) -> Tuple[float, float]:
        """计算我党和异党力量"""
        day_key = cls._get_element_key(day_element)
        generating_key = cls._get_element_key(cls._get_generating_element(day_element))
        
        # 我党：比劫(同类) + 印枭(生我者)
        supporting = scores[day_key] + scores[generating_key]
        
        # 异党：官杀(克我) + 食伤(我生) + 财才(我克)
        controlling_key = cls._get_element_key(cls._get_controlling_element(day_element))
        generated_key = cls._get_element_key(cls._get_generated_element(day_element))
        controlled_key = cls._get_element_key(cls._get_controlled_element(day_element))
        
        opposing = scores[controlling_key] + scores[generated_key] + scores[controlled_key]
        
        return supporting, opposing
    
    @classmethod
    def _categorize_strength(cls, score: float) -> DayMasterStrength:
        """根据分数确定强弱类别"""
        for category in STRENGTH_CATEGORIES:
            if category['min'] <= score <= category['max']:
                return category['strength']
        return DayMasterStrength.BALANCED
    
    @classmethod
    def _get_month_commanding_element(cls, month_branch: str, 
                                       birth_info: Optional[Dict]) -> str:
        """获取月令司令元素"""
        commanders = MONTH_COMMANDING_ELEMENTS.get(month_branch, [])
        if commanders:
            # 默认返回主气（最后一个通常天数最多）
            return commanders[-1]['element']
        
        # 回退：使用藏干主气
        hidden = HIDDEN_STEMS.get(month_branch, [])
        if hidden:
            return hidden[0]['stem']
        return '戊'
    
    @classmethod
    def _get_element_key(cls, element: str) -> str:
        """获取五行英文键名"""
        mapping = {
            '木': 'wood', '火': 'fire', '土': 'earth', '金': 'metal', '水': 'water',
            '甲': 'wood', '乙': 'wood', '丙': 'fire', '丁': 'fire',
            '戊': 'earth', '己': 'earth', '庚': 'metal', '辛': 'metal',
            '壬': 'water', '癸': 'water'
        }
        return mapping.get(element, 'earth')
    
    @classmethod
    def _get_generating_element(cls, element: str) -> str:
        """获取生我者"""
        mapping = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        return mapping.get(element, '土')
    
    @classmethod
    def _get_controlling_element(cls, element: str) -> str:
        """获取克我者"""
        mapping = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        return mapping.get(element, '木')
    
    @classmethod
    def _get_generated_element(cls, element: str) -> str:
        """获取我生者"""
        mapping = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        return mapping.get(element, '金')
    
    @classmethod
    def _get_controlled_element(cls, element: str) -> str:
        """获取我克者"""
        mapping = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
        return mapping.get(element, '水')
    
    @classmethod
    def _generate_analysis(cls, strength: DayMasterStrength, score: float,
                           day_element: str) -> str:
        """生成分析文本"""
        element_name = {'木': '木', '火': '火', '土': '土', '金': '金', '水': '水'}
        
        analyses = {
            DayMasterStrength.EXTREMELY_WEAK: f'{element_name.get(day_element)}日主衰极，八字严重失衡，需大补印比',
            DayMasterStrength.WEAK: f'{element_name.get(day_element)}日主偏弱，印比不足，宜补充生扶',
            DayMasterStrength.SLIGHTLY_WEAK: f'{element_name.get(day_element)}日主略弱，需适当扶持',
            DayMasterStrength.BALANCED: f'{element_name.get(day_element)}日主中和，五行较为平衡',
            DayMasterStrength.SLIGHTLY_STRONG: f'{element_name.get(day_element)}日主略旺，需适当泄耗',
            DayMasterStrength.STRONG: f'{element_name.get(day_element)}日主偏旺，食伤财官可用',
            DayMasterStrength.EXTREMELY_STRONG: f'{element_name.get(day_element)}日主旺极，需顺势而为或从格论'
        }
        
        return analyses.get(strength, '日主强弱待分析') + f'（分数：{score:.1f}）'
    
    @classmethod
    def _generate_suggestions(cls, strength: DayMasterStrength,
                              day_element: str) -> List[str]:
        """生成建议"""
        suggestions_map = {
            DayMasterStrength.EXTREMELY_WEAK: [
                '宜从弱格论命',
                '行运喜财官食伤',
                '忌讳印比运程'
            ],
            DayMasterStrength.WEAK: [
                '喜用印绶生扶',
                '比劫帮身有力',
                '忌财官过旺'
            ],
            DayMasterStrength.SLIGHTLY_WEAK: [
                '印比为喜用',
                '适当补充生扶',
                '财官适量可用'
            ],
            DayMasterStrength.BALANCED: [
                '五行较为平衡',
                '喜用需具体分析',
                '调候为主'
            ],
            DayMasterStrength.SLIGHTLY_STRONG: [
                '食伤生财为喜',
                '适当泄秀',
                '官杀可用'
            ],
            DayMasterStrength.STRONG: [
                '喜用食伤泄秀',
                '财星可用',
                '官杀制身有力'
            ],
            DayMasterStrength.EXTREMELY_STRONG: [
                '宜从旺格论命',
                '行运喜印比',
                '忌讳财官'
            ]
        }
        
        return suggestions_map.get(strength, ['需进一步分析'])
