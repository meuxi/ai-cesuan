# -*- coding: utf-8 -*-
"""
格局分析器
来源：mingpan项目 PatternAnalyzer.ts
识别八字格局类型（正格、从格、特殊格局等）
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

# 天干五行映射
STEM_ELEMENT = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支五行映射
BRANCH_ELEMENT = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木',
    '辰': '土', '巳': '火', '午': '火', '未': '土',
    '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 五行生克关系
GENERATING = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
CONTROLLING = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
GENERATED_BY = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
CONTROLLED_BY = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}

# 天干合化
STEM_COMBINATIONS = {
    ('甲', '己'): '土', ('己', '甲'): '土',
    ('乙', '庚'): '金', ('庚', '乙'): '金',
    ('丙', '辛'): '水', ('辛', '丙'): '水',
    ('丁', '壬'): '木', ('壬', '丁'): '木',
    ('戊', '癸'): '火', ('癸', '戊'): '火'
}

# 化气格支持月支
TRANSFORMATION_SUPPORT = {
    '土': ['辰', '戌', '丑', '未'],
    '金': ['申', '酉', '戌'],
    '水': ['亥', '子', '丑'],
    '木': ['寅', '卯', '辰'],
    '火': ['巳', '午', '未']
}

# 专旺格条件
DOMINANT_PATTERNS = {
    '曲直格': {'element': '木', 'branches': ['寅', '卯', '辰']},
    '炎上格': {'element': '火', 'branches': ['巳', '午', '未']},
    '稼穡格': {'element': '土', 'branches': ['辰', '戌', '丑', '未']},
    '从革格': {'element': '金', 'branches': ['申', '酉', '戌']},
    '润下格': {'element': '水', 'branches': ['亥', '子', '丑']}
}

# 建禄月支对应
JIANLU_BRANCHES = {
    '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
    '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子'
}

# 羊刃月支对应
YANGREN_BRANCHES = {
    '甲': '卯', '乙': '寅', '丙': '午', '丁': '巳', '戊': '午',
    '己': '巳', '庚': '酉', '辛': '申', '壬': '子', '癸': '亥'
}


@dataclass
class PatternResult:
    """格局分析结果"""
    primary_pattern: Dict[str, Any]
    secondary_patterns: List[Dict[str, Any]]
    chart_structure: Dict[str, Any]
    special_features: List[Dict[str, Any]]
    recommendations: Dict[str, List[str]]


class PatternAnalyzer:
    """格局分析器"""
    
    @classmethod
    def analyze(cls, bazi: Dict[str, Dict[str, str]], 
                strength_score: float = 50) -> PatternResult:
        """
        分析八字格局
        
        Args:
            bazi: 八字信息 {'year': {'stem': '甲', 'branch': '子'}, ...}
            strength_score: 日主强弱分数（用于判断正格/从格）
            
        Returns:
            PatternResult: 格局分析结果
        """
        day_master = bazi['day']['stem']
        day_element = STEM_ELEMENT.get(day_master, '土')
        
        # 收集所有天干地支
        all_stems = [
            bazi['year']['stem'], bazi['month']['stem'],
            bazi['day']['stem'], bazi['hour']['stem']
        ]
        all_branches = [
            bazi['year']['branch'], bazi['month']['branch'],
            bazi['day']['branch'], bazi['hour']['branch']
        ]
        month_branch = bazi['month']['branch']
        
        patterns = []
        
        # 1. 检查化气格（最高优先级）
        transformation = cls._check_transformation_pattern(
            day_master, all_stems, month_branch
        )
        if transformation:
            patterns.append({**transformation, 'priority': 10})
        
        # 2. 检查从格
        follow_pattern = cls._check_follow_patterns(
            day_element, all_stems, all_branches, strength_score
        )
        if follow_pattern:
            patterns.append({**follow_pattern, 'priority': 9})
        
        # 3. 检查专旺格
        dominant = cls._check_dominant_pattern(day_element, all_branches)
        if dominant:
            patterns.append({**dominant, 'priority': 8})
        
        # 4. 检查传统格局（建禄格、羊刃格）
        traditional = cls._check_traditional_patterns(day_master, month_branch)
        if traditional:
            patterns.append({**traditional, 'priority': 7})
        
        # 5. 根据日主强弱判断正格
        strength_pattern = cls._get_strength_pattern(strength_score)
        patterns.append({**strength_pattern, 'priority': 5})
        
        # 选择最高优先级格局
        patterns.sort(key=lambda x: x['priority'], reverse=True)
        primary = patterns[0] if patterns else cls._get_default_pattern()
        
        # 次要格局
        secondary = cls._find_secondary_patterns(bazi)
        
        # 图表结构
        structure = cls._analyze_structure(bazi, primary, strength_score)
        
        # 特殊特征
        features = cls._identify_features(bazi, all_branches)
        
        # 建议
        recommendations = cls._generate_recommendations(primary, structure)
        
        return PatternResult(
            primary_pattern=primary,
            secondary_patterns=secondary,
            chart_structure=structure,
            special_features=features,
            recommendations=recommendations
        )
    
    @classmethod
    def _check_transformation_pattern(cls, day_master: str, 
                                        all_stems: List[str],
                                        month_branch: str) -> Optional[Dict]:
        """检查化气格"""
        other_stems = [s for s in all_stems if s != day_master]
        
        for stem in other_stems:
            combo = (day_master, stem)
            if combo in STEM_COMBINATIONS:
                result_element = STEM_COMBINATIONS[combo]
                support_branches = TRANSFORMATION_SUPPORT.get(result_element, [])
                
                if month_branch in support_branches:
                    return {
                        'type': '化气格',
                        'subtype': f'{day_master}{stem}化{result_element}',
                        'strength': 9,
                        'description': f'{day_master}{stem}相合，月支{month_branch}支持，化为{result_element}',
                        'characteristics': ['化气成功', '五行专一', '格局清纯']
                    }
        return None
    
    @classmethod
    def _check_follow_patterns(cls, day_element: str, all_stems: List[str],
                                all_branches: List[str], 
                                strength_score: float) -> Optional[Dict]:
        """检查从格"""
        # 统计五行
        element_counts = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
        
        for stem in all_stems:
            elem = STEM_ELEMENT.get(stem)
            if elem:
                element_counts[elem] += 1
        
        for branch in all_branches:
            elem = BRANCH_ELEMENT.get(branch)
            if elem:
                element_counts[elem] += 0.5
        
        # 日主极弱（分数<30）检查从格
        if strength_score < 30:
            # 找最旺的异类
            sorted_elems = sorted(
                [(k, v) for k, v in element_counts.items() if k != day_element],
                key=lambda x: x[1], reverse=True
            )
            
            if sorted_elems:
                dominant = sorted_elems[0][0]
                dominant_count = sorted_elems[0][1]
                
                if dominant_count >= 3:
                    # 判断从格类型
                    if dominant == GENERATING.get(day_element):
                        return {
                            'type': '从儿格',
                            'strength': 8,
                            'description': '日主极弱，顺从食伤',
                            'characteristics': ['顺从流通', '创意表达', '艺术天赋']
                        }
                    elif dominant == CONTROLLED_BY.get(day_element):
                        return {
                            'type': '从官格',
                            'strength': 8,
                            'description': '日主极弱，顺从官杀',
                            'characteristics': ['服从权威', '适合公职', '纪律严明']
                        }
                    else:
                        return {
                            'type': '从势格',
                            'strength': 7,
                            'description': '日主极弱，顺从强势五行',
                            'characteristics': ['灵活适应', '顺势而为', '借力发展']
                        }
        
        # 日主极旺（分数>150）检查从强格
        if strength_score > 150:
            same_count = element_counts.get(day_element, 0)
            gen_count = element_counts.get(GENERATED_BY.get(day_element), 0)
            
            if same_count + gen_count >= 5:
                return {
                    'type': '从旺格',
                    'strength': 8,
                    'description': '日主极旺，印比成群',
                    'characteristics': ['能量强大', '独立自主', '领导才能']
                }
        
        return None
    
    @classmethod
    def _check_dominant_pattern(cls, day_element: str,
                                 all_branches: List[str]) -> Optional[Dict]:
        """检查专旺格（曲直、炎上、稼穡、从革、润下）"""
        for pattern_name, config in DOMINANT_PATTERNS.items():
            if day_element != config['element']:
                continue
            
            matching = sum(1 for b in all_branches if b in config['branches'])
            if matching >= 3:
                descriptions = {
                    '曲直格': '木气纯粹，仁德双全',
                    '炎上格': '火势炎上，光明磊落',
                    '稼穡格': '土德深厚，忠信务实',
                    '从革格': '金气肃杀，果断坚毅',
                    '润下格': '水性润下，智慧灵动'
                }
                return {
                    'type': pattern_name,
                    'strength': 8,
                    'description': descriptions.get(pattern_name, '专旺成格'),
                    'characteristics': ['五行专一', '气势强劲', '个性鲜明']
                }
        return None
    
    @classmethod
    def _check_traditional_patterns(cls, day_master: str,
                                     month_branch: str) -> Optional[Dict]:
        """检查传统格局（建禄格、羊刃格）"""
        # 建禄格
        if JIANLU_BRANCHES.get(day_master) == month_branch:
            return {
                'type': '建禄格',
                'strength': 7,
                'description': '月支为日主之禄，自立自强',
                'characteristics': ['自力更生', '独立创业', '不靠祖业']
            }
        
        # 羊刃格
        if YANGREN_BRANCHES.get(day_master) == month_branch:
            return {
                'type': '羊刃格',
                'strength': 7,
                'description': '月支为日主羊刃，刚强果敢',
                'characteristics': ['性格刚烈', '竞争意识强', '适合军警']
            }
        
        return None
    
    @classmethod
    def _get_strength_pattern(cls, strength_score: float) -> Dict:
        """根据强弱分数获取正格"""
        if strength_score >= 80:
            return {
                'type': '身旺格',
                'strength': 7,
                'description': '日主强旺，精力充沛',
                'characteristics': ['精力充沛', '主动进取', '领导力强']
            }
        elif strength_score <= 20:
            return {
                'type': '身弱格',
                'strength': 7,
                'description': '日主偏弱，需要扶助',
                'characteristics': ['深思熟虑', '善于合作', '谨慎稳健']
            }
        else:
            return {
                'type': '正格',
                'strength': 5,
                'description': '五行较为平衡，中和之命',
                'characteristics': ['平衡稳定', '发展均衡', '适应力强']
            }
    
    @classmethod
    def _get_default_pattern(cls) -> Dict:
        """获取默认格局"""
        return {
            'type': '正格',
            'strength': 5,
            'description': '标准格局，五行较为平衡',
            'priority': 3,
            'characteristics': ['平衡稳定', '发展均衡']
        }
    
    @classmethod
    def _find_secondary_patterns(cls, bazi: Dict) -> List[Dict]:
        """查找次要格局"""
        patterns = []
        day_master = bazi['day']['stem']
        all_stems = [bazi[p]['stem'] for p in ['year', 'month', 'hour']]
        
        # 检查天乙贵人
        tianyi_map = {
            '甲': ['丑', '未'], '戊': ['丑', '未'],
            '乙': ['子', '申'], '己': ['子', '申'],
            '丙': ['亥', '酉'], '丁': ['亥', '酉'],
            '庚': ['午', '寅'], '辛': ['午', '寅'],
            '壬': ['巳', '卯'], '癸': ['巳', '卯']
        }
        
        tianyi_branches = tianyi_map.get(day_master, [])
        all_branches = [bazi[p]['branch'] for p in ['year', 'month', 'day', 'hour']]
        
        if any(b in tianyi_branches for b in all_branches):
            patterns.append({
                'type': '天乙贵人',
                'strength': 6,
                'description': '命带天乙贵人，遇难呈祥'
            })
        
        # 检查财星旺
        day_element = STEM_ELEMENT.get(day_master)
        wealth_element = CONTROLLING.get(day_element)
        wealth_count = sum(1 for s in all_stems if STEM_ELEMENT.get(s) == wealth_element)
        
        if wealth_count >= 2:
            patterns.append({
                'type': '财星格',
                'strength': 5,
                'description': '财星旺盛，利于求财'
            })
        
        return patterns
    
    @classmethod
    def _analyze_structure(cls, bazi: Dict, primary: Dict, 
                           strength_score: float) -> Dict:
        """分析图表结构"""
        day_element = STEM_ELEMENT.get(bazi['day']['stem'])
        pattern_type = primary.get('type', '正格')
        
        # 根据格局确定用神忌神
        useful_gods = []
        avoid_gods = []
        
        if '从' in pattern_type or pattern_type in ['曲直格', '炎上格', '稼穡格', '从革格', '润下格']:
            # 从格顺势
            useful_gods = [day_element, GENERATED_BY.get(day_element)]
            avoid_gods = [CONTROLLED_BY.get(day_element), CONTROLLING.get(day_element)]
        elif strength_score > 50:
            # 身旺喜泄耗
            useful_gods = [GENERATING.get(day_element), CONTROLLING.get(day_element)]
            avoid_gods = [GENERATED_BY.get(day_element), day_element]
        else:
            # 身弱喜生扶
            useful_gods = [GENERATED_BY.get(day_element), day_element]
            avoid_gods = [GENERATING.get(day_element), CONTROLLED_BY.get(day_element)]
        
        # 计算结构分数
        structure_score = 50
        if primary.get('strength', 0) >= 8:
            structure_score += 20
        if abs(strength_score - 50) < 20:
            structure_score += 15
        
        # 平衡类型
        if strength_score >= 80 or strength_score <= 20:
            balance_type = '极端'
        elif abs(strength_score - 50) > 20:
            balance_type = '不平衡'
        else:
            balance_type = '平衡'
        
        return {
            'day_master_type': '身旺' if strength_score > 50 else '身弱' if strength_score < 50 else '平衡',
            'useful_gods': [g for g in useful_gods if g],
            'avoid_gods': [g for g in avoid_gods if g],
            'structure_score': min(100, structure_score),
            'balance_type': balance_type
        }
    
    @classmethod
    def _identify_features(cls, bazi: Dict, all_branches: List[str]) -> List[Dict]:
        """识别特殊特征"""
        features = []
        
        # 检查三合
        three_harmonies = [
            (['申', '子', '辰'], '水'),
            (['亥', '卯', '未'], '木'),
            (['寅', '午', '戌'], '火'),
            (['巳', '酉', '丑'], '金')
        ]
        
        for branches, element in three_harmonies:
            if sum(1 for b in branches if b in all_branches) == 3:
                features.append({
                    'type': '三合局',
                    'description': f'{element}局三合成功',
                    'impact': '正面'
                })
        
        # 检查相冲
        conflicts = [('子', '午'), ('丑', '未'), ('寅', '申'),
                     ('卯', '酉'), ('辰', '戌'), ('巳', '亥')]
        conflict_count = sum(1 for c in conflicts 
                            if c[0] in all_branches and c[1] in all_branches)
        
        if conflict_count >= 2:
            features.append({
                'type': '多冲',
                'description': '命中多冲，易有动荡',
                'impact': '负面'
            })
        
        return features
    
    @classmethod
    def _generate_recommendations(cls, primary: Dict, 
                                   structure: Dict) -> Dict[str, List[str]]:
        """生成建议"""
        pattern_type = primary.get('type', '正格')
        
        career = []
        lifestyle = []
        
        # 根据格局类型给出建议
        if '从旺' in pattern_type or '从强' in pattern_type:
            career = ['适合领导职位', '独立创业', '管理经营']
            lifestyle = ['果断决策', '保持自信']
        elif '从儿' in pattern_type:
            career = ['创意产业', '艺术表演', '媒体传播']
            lifestyle = ['充分表达自我', '保持创新思维']
        elif '从财' in pattern_type:
            career = ['商业经营', '金融理财', '投资管理']
            lifestyle = ['讲求实际', '重视物质基础']
        elif '从官' in pattern_type:
            career = ['公职人员', '管理阶层', '法律相关']
            lifestyle = ['纪律严明', '组织有序']
        elif pattern_type == '曲直格':
            career = ['教育培训', '环保产业', '医疗健康']
            lifestyle = ['持续成长', '不断学习']
        elif pattern_type == '炎上格':
            career = ['娱乐表演', '科技产业', '能源产业']
            lifestyle = ['热情奔放', '充满活力']
        elif pattern_type == '稼穡格':
            career = ['房地产业', '农业发展', '咨询服务']
            lifestyle = ['稳定踏实', '养育关怀']
        elif pattern_type == '从革格':
            career = ['工程技术', '精密制造', '军事国防']
            lifestyle = ['结构严谨', '精益求精']
        elif pattern_type == '润下格':
            career = ['传播媒体', '物流运输', '研究开发']
            lifestyle = ['灵活变通', '智慧思考']
        elif pattern_type == '建禄格':
            career = ['自主创业', '专业技能', '自由职业']
            lifestyle = ['独立自主', '自力更生']
        elif pattern_type == '羊刃格':
            career = ['竞争激烈行业', '体育运动', '业务销售']
            lifestyle = ['积极主动', '喜欢竞争']
        elif pattern_type == '身旺格':
            career = ['领导管理', '积极开拓']
            lifestyle = ['充满活力', '主动出击']
        elif pattern_type == '身弱格':
            career = ['支援服务', '分析研究']
            lifestyle = ['深思熟虑', '谨慎小心']
        else:
            career = ['稳定职业', '传统行业']
            lifestyle = ['平衡生活', '中庸之道']
        
        return {
            'favorable_elements': structure.get('useful_gods', []),
            'unfavorable_elements': structure.get('avoid_gods', []),
            'career_suggestions': career,
            'lifestyle_suggestions': lifestyle
        }
