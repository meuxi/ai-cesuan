"""
十神分析模块
参考 mingpan 的 TenGodsAnalyzer 实现
提供完整的十神计算、分析和解读功能
"""
from typing import Dict, List, Optional, Tuple
import json
import os


class TenGodsAnalyzer:
    """十神分析器"""
    
    # 十神名称
    TEN_GODS = [
        '比肩', '劫财', '食神', '伤官',
        '偏财', '正财', '七杀', '正官',
        '偏印', '正印'
    ]
    
    # 十神简称
    TEN_GODS_SHORT = [
        '比', '劫', '食', '伤',
        '偏财', '正财', '杀', '官',
        '枭', '印'
    ]
    
    # 十神属性
    TEN_GOD_ATTRIBUTES = {
        '比肩': {'nature': '中性', 'type': 'companion', 'element': 'same'},
        '劫财': {'nature': '凶', 'type': 'companion', 'element': 'same'},
        '食神': {'nature': '吉', 'type': 'output', 'element': 'generate'},
        '伤官': {'nature': '凶', 'type': 'output', 'element': 'generate'},
        '偏财': {'nature': '吉', 'type': 'wealth', 'element': 'control'},
        '正财': {'nature': '吉', 'type': 'wealth', 'element': 'control'},
        '七杀': {'nature': '凶', 'type': 'power', 'element': 'control'},
        '正官': {'nature': '吉', 'type': 'power', 'element': 'control'},
        '偏印': {'nature': '中性', 'type': 'resource', 'element': 'generate'},
        '正印': {'nature': '吉', 'type': 'resource', 'element': 'generate'}
    }
    
    # 十神含义
    TEN_GOD_MEANINGS = {
        '比肩': '代表兄弟姐妹、朋友、同事，性格独立、固执，善于竞争',
        '劫财': '代表竞争、夺取，性格冲动、好胜，易有破财之事',
        '食神': '代表才华、口福、子女，性格乐观、温和，善于表达',
        '伤官': '代表才华、技艺、创新，性格聪明、叛逆，易有官非',
        '偏财': '代表意外之财、父亲、偏妻，善于理财，机遇多',
        '正财': '代表正当收入、妻子、财富，勤劳踏实，理财稳健',
        '七杀': '代表压力、权威、小人，性格刚强、果断，易有灾祸',
        '正官': '代表事业、地位、丈夫，性格正直、守法，贵人运佳',
        '偏印': '代表继母、偏业、学术，性格孤僻、多疑，善于思考',
        '正印': '代表母亲、学历、贵人，性格仁慈、稳重，学业运佳'
    }
    
    # 位置权重（参考mingpan）
    POSITION_WEIGHTS = {
        'year': 1.0,    # 年柱
        'month': 1.5,   # 月柱最强
        'day': 0.8,     # 日柱（藏干）
        'hour': 1.2     # 时柱次强
    }
    
    # 十神权重
    TEN_GOD_WEIGHTS = {
        '正官': 1.2, '七杀': 1.1, '正财': 1.1, '偏财': 1.0,
        '正印': 1.1, '偏印': 1.0, '食神': 1.0, '伤官': 0.9,
        '比肩': 1.0, '劫财': 0.9
    }
    
    # 位置解读（参考mingpan的详细解读）
    POSITION_INTERPRETATIONS = {
        '比肩': {
            'year': '年柱比肩，兄弟姐妹缘份深，幼年有竞争',
            'month': '月柱比肩，朋友支持力强，青年独立奋斗',
            'day': '日柱比肩，自信独立，配偶性格强势',
            'hour': '时柱比肩，子女独立性强，晚年有助力'
        },
        '劫财': {
            'year': '年柱劫财，幼年竞争激烈，家境有波折',
            'month': '月柱劫财，青年奋斗求进，需防破财',
            'day': '日柱劫财，配偶性格急躁，婚姻需谨慎',
            'hour': '时柱劫财，晚年有斗志，子女争强好胜'
        },
        '食神': {
            'year': '年柱食神，童年快乐，祖上有福',
            'month': '月柱食神，青年有才华，贵人提携',
            'day': '日柱食神，感情丰富，生活品质好',
            'hour': '时柱食神，晚年享福，子女孝顺'
        },
        '伤官': {
            'year': '年柱伤官，幼年叛逆，与长辈有冲突',
            'month': '月柱伤官，青年创新，才华出众',
            'day': '日柱伤官，感情多变，配偶有才华',
            'hour': '时柱伤官，子女叛逆聪明，晚年需防官非'
        },
        '偏财': {
            'year': '年柱偏财，祖上有财，父亲能干',
            'month': '月柱偏财，青年发财机会多，善于经营',
            'day': '日柱偏财，配偶有助，异性缘佳',
            'hour': '时柱偏财，晚年富足，有意外之财'
        },
        '正财': {
            'year': '年柱正财，家境优渥，祖上勤俭',
            'month': '月柱正财，事业稳定，正财运佳',
            'day': '日柱正财，配偶贤淑，婚姻美满',
            'hour': '时柱正财，子女孝顺，晚年安康'
        },
        '七杀': {
            'year': '年柱七杀，幼年辛苦，祖上有威严',
            'month': '月柱七杀，青年压力大，事业有冲劲',
            'day': '日柱七杀，意志坚强，配偶性格刚强',
            'hour': '时柱七杀，晚年有权威，子女有魄力'
        },
        '正官': {
            'year': '年柱正官，家教严谨，祖上有地位',
            'month': '月柱正官，事业有成，青年得贵人',
            'day': '日柱正官，配偶正派，婚姻稳定',
            'hour': '时柱正官，子女有出息，晚年受尊重'
        },
        '偏印': {
            'year': '年柱偏印，祖上有学问，幼年多思考',
            'month': '月柱偏印，学习能力强，偏业有成',
            'day': '日柱偏印，思想独特，配偶有个性',
            'hour': '时柱偏印，晚年好学，子女聪慧'
        },
        '正印': {
            'year': '年柱正印，母慈子孝，幼年受宠',
            'month': '月柱正印，贵人相助，学业有成',
            'day': '日柱正印，配偶温柔，婚姻和谐',
            'hour': '时柱正印，晚年安康，子女贤孝'
        }
    }
    
    def __init__(self):
        """初始化，加载十神关系数据"""
        self.shishen_data = self._load_shishen_data()
    
    def _load_shishen_data(self) -> Dict:
        """加载十神关系数据"""
        data_path = os.path.join(
            os.path.dirname(__file__),
            'data/shishen.json'
        )
        
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # 如果文件不存在，返回默认数据
            return self._get_default_shishen_data()
    
    def _get_default_shishen_data(self) -> Dict:
        """获取默认十神关系数据"""
        # 简化的十神关系表
        return {
            '十神关系': {
                '甲': {'甲': '比肩', '乙': '劫财', '丙': '食神', '丁': '伤官',
                      '戊': '偏财', '己': '正财', '庚': '七杀', '辛': '正官',
                      '壬': '偏印', '癸': '正印'},
                '乙': {'甲': '劫财', '乙': '比肩', '丙': '伤官', '丁': '食神',
                      '戊': '正财', '己': '偏财', '庚': '正官', '辛': '七杀',
                      '壬': '正印', '癸': '偏印'},
                '丙': {'甲': '偏印', '乙': '正印', '丙': '比肩', '丁': '劫财',
                      '戊': '食神', '己': '伤官', '庚': '偏财', '辛': '正财',
                      '壬': '七杀', '癸': '正官'},
                '丁': {'甲': '正印', '乙': '偏印', '丙': '劫财', '丁': '比肩',
                      '戊': '伤官', '己': '食神', '庚': '正财', '辛': '偏财',
                      '壬': '正官', '癸': '七杀'},
                '戊': {'甲': '七杀', '乙': '正官', '丙': '偏印', '丁': '正印',
                      '戊': '比肩', '己': '劫财', '庚': '食神', '辛': '伤官',
                      '壬': '偏财', '癸': '正财'},
                '己': {'甲': '正官', '乙': '七杀', '丙': '正印', '丁': '偏印',
                      '戊': '劫财', '己': '比肩', '庚': '伤官', '辛': '食神',
                      '壬': '正财', '癸': '偏财'},
                '庚': {'甲': '偏财', '乙': '正财', '丙': '七杀', '丁': '正官',
                      '戊': '偏印', '己': '正印', '庚': '比肩', '辛': '劫财',
                      '壬': '食神', '癸': '伤官'},
                '辛': {'甲': '正财', '乙': '偏财', '丙': '正官', '丁': '七杀',
                      '戊': '正印', '己': '偏印', '庚': '劫财', '辛': '比肩',
                      '壬': '伤官', '癸': '食神'},
                '壬': {'甲': '食神', '乙': '伤官', '丙': '偏财', '丁': '正财',
                      '庚': '偏印', '辛': '正印', '壬': '比肩', '癸': '劫财',
                      '戊': '七杀', '己': '正官'},
                '癸': {'甲': '伤官', '乙': '食神', '丙': '正财', '丁': '偏财',
                      '庚': '正印', '辛': '偏印', '壬': '劫财', '癸': '比肩',
                      '戊': '正官', '己': '七杀'}
            }
        }
    
    def calculate_ten_god(self, day_master: str, target: str) -> str:
        """计算十神
        
        Args:
            day_master: 日元天干
            target: 目标天干
            
        Returns:
            十神名称
        """
        relations = self.shishen_data.get('十神关系', {})
        if day_master in relations:
            return relations[day_master].get(target, '比肩')
        return '比肩'
    
    def analyze_chart(self, bazi_chart: Dict, day_master_strength: str = '正格') -> Dict:
        """分析八字中的十神分布（增强版）
        
        Args:
            bazi_chart: 八字排盘结果，包含 sizhu 字段
            day_master_strength: 日主强弱（身旺/身弱/正格）
            
        Returns:
            完整的十神分析结果
        """
        sizhu = bazi_chart.get('sizhu', {})
        dizhi_cang = bazi_chart.get('dizhi_cang', {})
        
        # 日元（日柱天干）
        day_pillar = sizhu.get('day', '')
        if not day_pillar or len(day_pillar) < 2:
            return {'error': '无效的日柱数据'}
        
        day_master = day_pillar[0]  # 日元天干
        
        # 分析各柱
        pillars = {}
        distribution = {}
        ten_god_list = []  # 详细的十神列表
        
        for pillar_name in ['year', 'month', 'day', 'hour']:
            pillar = sizhu.get(pillar_name, '')
            if len(pillar) >= 2:
                stem = pillar[0]  # 天干
                branch = pillar[1]  # 地支
                
                # 计算天干十神
                stem_god = self.calculate_ten_god(day_master, stem)
                
                # 计算位置权重和力量
                pos_weight = self.POSITION_WEIGHTS.get(pillar_name, 1.0)
                god_weight = self.TEN_GOD_WEIGHTS.get(stem_god, 1.0)
                strength = pos_weight * god_weight
                
                # 获取位置解读
                interpretation = self._get_position_interpretation(stem_god, pillar_name)
                
                # 记录详细信息
                ten_god_list.append({
                    'name': stem_god,
                    'position': pillar_name,
                    'strength': round(strength, 2),
                    'interpretation': interpretation,
                    'is_hidden': False
                })
                
                # 计算地支藏干的十神
                branch_gods = []
                hidden_stems = dizhi_cang.get(pillar_name, [])
                for i, hidden_stem in enumerate(hidden_stems):
                    god = self.calculate_ten_god(day_master, hidden_stem)
                    # 藏干力量递减
                    hidden_power = 0.7 if i == 0 else (0.2 if i == 1 else 0.1)
                    hidden_strength = pos_weight * self.TEN_GOD_WEIGHTS.get(god, 1.0) * hidden_power
                    
                    branch_gods.append({
                        'stem': hidden_stem,
                        'god': god,
                        'strength': round(hidden_strength, 2)
                    })
                    
                    ten_god_list.append({
                        'name': f"{god}(藏)",
                        'position': pillar_name,
                        'strength': round(hidden_strength, 2),
                        'interpretation': self._get_position_interpretation(god, pillar_name),
                        'is_hidden': True
                    })
                
                pillars[pillar_name] = {
                    'stem': stem,
                    'stem_god': stem_god,
                    'stem_strength': round(strength, 2),
                    'branch': branch,
                    'branch_gods': branch_gods,
                    'interpretation': interpretation
                }
                
                # 统计分布
                distribution[stem_god] = distribution.get(stem_god, 0) + 1
                for bg in branch_gods:
                    god = bg['god']
                    distribution[god] = distribution.get(god, 0) + 1
        
        # 组合分析（新增）
        combinations = self._analyze_combinations(distribution)
        
        # 旺衰影响分析（新增）
        strength_analysis = self._analyze_strength_influence(distribution, day_master_strength)
        
        # 生成总结
        summary = self._generate_summary(distribution, combinations)
        
        # 生成建议
        suggestions = self._generate_suggestions(distribution, day_master, day_master_strength)
        
        return {
            'day_master': day_master,
            'day_master_strength': day_master_strength,
            'pillars': pillars,
            'ten_god_list': ten_god_list,
            'distribution': distribution,
            'combinations': combinations,
            'strength_analysis': strength_analysis,
            'summary': summary,
            'suggestions': suggestions
        }
    
    def _get_position_interpretation(self, god: str, position: str) -> str:
        """获取位置解读"""
        god_interpretations = self.POSITION_INTERPRETATIONS.get(god, {})
        return god_interpretations.get(position, f'{position}{god}')
    
    def _analyze_combinations(self, distribution: Dict[str, int]) -> List[Dict]:
        """分析十神组合（参考mingpan的analyzeCombinations）"""
        combinations = []
        
        # 官杀混杂
        if distribution.get('正官', 0) > 0 and distribution.get('七杀', 0) > 0:
            combinations.append({
                'pattern': '官杀混杂',
                'description': '正官与七杀同见，需要制化调和',
                'implications': [
                    '事业上可能有多重压力',
                    '性格可能有内在矛盾',
                    '需要印绶或食伤来调和'
                ]
            })
        
        # 财印相碍
        if (distribution.get('正财', 0) > 0 or distribution.get('偏财', 0) > 0) and \
           (distribution.get('正印', 0) > 0 or distribution.get('偏印', 0) > 0):
            combinations.append({
                'pattern': '财印相碍',
                'description': '财星与印绶同见，互有牵制',
                'implications': [
                    '学业与财运需要平衡',
                    '可能在求知与求财间犹豫',
                    '需要根据日主强弱取舍'
                ]
            })
        
        # 食伤生财
        if (distribution.get('食神', 0) > 0 or distribution.get('伤官', 0) > 0) and \
           (distribution.get('正财', 0) > 0 or distribution.get('偏财', 0) > 0):
            combinations.append({
                'pattern': '食伤生财',
                'description': '食伤生财，才华可以转化为财富',
                'implications': [
                    '适合创业或技术类工作',
                    '才华可以变现',
                    '财运来自于个人能力'
                ]
            })
        
        # 比劫过多
        total_companion = distribution.get('比肩', 0) + distribution.get('劫财', 0)
        if total_companion >= 3:
            combinations.append({
                'pattern': '比劫过多',
                'description': '比肩劫财过多，竞争激烈',
                'implications': [
                    '兄弟朋友多但关系复杂',
                    '财运需防破耗',
                    '独立发展可能更好'
                ]
            })
        
        # 印绶护身
        total_seal = distribution.get('正印', 0) + distribution.get('偏印', 0)
        if total_seal >= 2:
            combinations.append({
                'pattern': '印绶护身',
                'description': '印绶多见，贵人运强',
                'implications': [
                    '学业运势良好',
                    '有长辈或贵人相助',
                    '思想层次较高'
                ]
            })
        
        return combinations
    
    def _analyze_strength_influence(self, distribution: Dict[str, int], 
                                    day_master_strength: str) -> List[Dict]:
        """分析旺衰对十神的影响（参考mingpan的analyzeStrengthInfluence）"""
        analyses = []
        
        for god, count in distribution.items():
            if count == 0:
                continue
            
            attr = self.TEN_GOD_ATTRIBUTES.get(god, {})
            god_type = attr.get('type', '')
            
            influence = '中性'
            suggestion = '日主平衡，此神影响中性，顺其自然'
            
            if day_master_strength in ['身弱', '衰极']:
                # 弱日主喜印比
                if god_type in ['resource', 'companion']:
                    influence = '有利'
                    suggestion = '日主弱，此神有助，宜加强利用'
                elif god_type in ['power', 'output']:
                    influence = '不利'
                    suggestion = '日主弱，此神消耗，宜谨慎应对'
            elif day_master_strength in ['身旺', '旺极']:
                # 强日主喜食财官
                if god_type in ['output', 'wealth']:
                    influence = '有利'
                    suggestion = '日主强，此神泄秀，宜积极利用'
                elif god_type in ['resource', 'companion']:
                    influence = '不利'
                    suggestion = '日主强，此神加力，宜适度控制'
            
            analyses.append({
                'god': god,
                'count': count,
                'influence': influence,
                'suggestion': suggestion
            })
        
        return analyses
    
    def _generate_summary(self, distribution: Dict[str, int], 
                          combinations: List[Dict] = None) -> str:
        """生成十神分布总结（增强版）"""
        if not distribution:
            return '十神分布数据不足'
        
        # 找出最多的十神
        max_god = max(distribution.items(), key=lambda x: x[1])
        
        # 统计各类型
        type_counts = {
            'companion': 0,  # 比劫
            'output': 0,     # 食伤
            'wealth': 0,     # 财星
            'power': 0,      # 官杀
            'resource': 0    # 印绶
        }
        
        for god, count in distribution.items():
            attr = self.TEN_GOD_ATTRIBUTES.get(god, {})
            god_type = attr.get('type', '')
            if god_type in type_counts:
                type_counts[god_type] += count
        
        # 找出主导类型
        dominant_type = max(type_counts.items(), key=lambda x: x[1])
        type_names = {
            'companion': '比劫', 'output': '食伤', 'wealth': '财星',
            'power': '官杀', 'resource': '印绶'
        }
        
        # 统计吉凶
        auspicious = sum(count for god, count in distribution.items() 
                        if self.TEN_GOD_ATTRIBUTES.get(god, {}).get('nature') == '吉')
        inauspicious = sum(count for god, count in distribution.items() 
                          if self.TEN_GOD_ATTRIBUTES.get(god, {}).get('nature') == '凶')
        
        summary = f"命局中{max_god[0]}最多（{max_god[1]}个），"
        summary += f"{type_names.get(dominant_type[0], '未知')}类十神占主导。"
        summary += f"吉神{auspicious}个，凶神{inauspicious}个。"
        
        # 添加组合信息
        if combinations:
            patterns = [c['pattern'] for c in combinations]
            if patterns:
                summary += f" 特殊组合：{', '.join(patterns)}。"
        
        return summary
    
    def _generate_suggestions(self, distribution: Dict[str, int], 
                             day_master: str,
                             day_master_strength: str = '正格') -> List[str]:
        """生成建议（增强版，考虑日主强弱）"""
        suggestions = []
        
        # 根据日主强弱给出核心建议
        if day_master_strength in ['身弱', '衰极']:
            suggestions.append('加强印比之力，求得生扶')
            suggestions.append('避免过度消耗，保存实力')
        elif day_master_strength in ['身旺', '旺极']:
            suggestions.append('利用食伤财官，流通能量')
            suggestions.append('避免过度印比，保持平衡')
        
        # 根据十神分布给出建议
        if distribution.get('正官', 0) > 0 or distribution.get('七杀', 0) > 0:
            if distribution.get('正官', 0) > 0 and distribution.get('七杀', 0) > 0:
                suggestions.append('官杀混杂，需要印绶化杀或食神制杀')
            else:
                suggestions.append('命带官杀，适合从事管理、公职等工作')
        
        if distribution.get('正财', 0) > 0 or distribution.get('偏财', 0) > 0:
            suggestions.append('命带财星，善于理财，财运较佳')
        
        if distribution.get('食神', 0) > 0 or distribution.get('伤官', 0) > 0:
            suggestions.append('命带食伤，才华横溢，适合创作、技术类工作')
        
        if distribution.get('正印', 0) > 0 or distribution.get('偏印', 0) > 0:
            suggestions.append('命带印绶，学业运佳，贵人相助')
        
        if distribution.get('比肩', 0) > 2 or distribution.get('劫财', 0) > 2:
            suggestions.append('比劫过多，注意与人合作时的利益分配')
        
        # 通用建议
        suggestions.append('了解十神特性，顺势而为')
        suggestions.append('平衡五行能量，和谐发展')
        
        return suggestions[:5]  # 最多返回5条建议
    
    def get_ten_god_meaning(self, god_name: str) -> str:
        """获取十神含义"""
        return self.TEN_GOD_MEANINGS.get(god_name, '未知十神')
    
    def get_ten_god_attribute(self, god_name: str) -> Dict:
        """获取十神属性"""
        return self.TEN_GOD_ATTRIBUTES.get(god_name, {})


# 便捷函数
def analyze_ten_gods(bazi_chart: Dict) -> Dict:
    """快速分析八字十神
    
    Args:
        bazi_chart: 八字排盘结果
        
    Returns:
        十神分析结果
    """
    analyzer = TenGodsAnalyzer()
    return analyzer.analyze_chart(bazi_chart)
