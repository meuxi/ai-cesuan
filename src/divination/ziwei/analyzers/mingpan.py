"""
命盘分析器
分析紫微斗数命盘
"""
from typing import Dict, List


class MingPanAnalyzer:
    """命盘分析类"""
    
    # 星曜吉凶属性
    XING_ATTR = {
        '紫微': {'nature': '吉', 'type': '帝星', 'meaning': '尊贵、领导力'},
        '天机': {'nature': '吉', 'type': '智星', 'meaning': '智慧、谋略'},
        '太阳': {'nature': '吉', 'type': '光明星', 'meaning': '光明、贵人'},
        '武曲': {'nature': '吉', 'type': '财星', 'meaning': '财富、果断'},
        '天同': {'nature': '吉', 'type': '福星', 'meaning': '福气、和善'},
        '廉贞': {'nature': '中', 'type': '囚星', 'meaning': '政治、官非'},
        '天府': {'nature': '吉', 'type': '财库星', 'meaning': '稳重、财库'},
        '太阴': {'nature': '吉', 'type': '财星', 'meaning': '财富、阴柔'},
        '贪狼': {'nature': '中', 'type': '桃花星', 'meaning': '欲望、才艺'},
        '巨门': {'nature': '凶', 'type': '暗星', 'meaning': '口舌、是非'},
        '天相': {'nature': '吉', 'type': '印星', 'meaning': '辅佐、印信'},
        '天梁': {'nature': '吉', 'type': '荫星', 'meaning': '化解、长寿'},
        '七杀': {'nature': '凶', 'type': '将星', 'meaning': '武勇、孤独'},
        '破军': {'nature': '凶', 'type': '耗星', 'meaning': '变动、破坏'},
        '左辅': {'nature': '吉', 'type': '辅星', 'meaning': '助力、贵人'},
        '右弼': {'nature': '吉', 'type': '辅星', 'meaning': '助力、贵人'},
        '文昌': {'nature': '吉', 'type': '科星', 'meaning': '文才、考试'},
        '文曲': {'nature': '吉', 'type': '科星', 'meaning': '艺术、才华'},
        '擎羊': {'nature': '凶', 'type': '煞星', 'meaning': '刑克、血光'},
        '陀罗': {'nature': '凶', 'type': '煞星', 'meaning': '拖延、纠缠'},
        '火星': {'nature': '凶', 'type': '煞星', 'meaning': '急躁、灾厄'},
        '铃星': {'nature': '凶', 'type': '煞星', 'meaning': '孤独、灾厄'}
    }
    
    @classmethod
    def analyze_gong(cls, gong_name: str, stars: List[str]) -> Dict:
        """分析单个宫位
        
        Args:
            gong_name: 宫名
            stars: 该宫位的星曜列表
            
        Returns:
            宫位分析结果
        """
        ji_count = 0
        xiong_count = 0
        star_details = []
        
        for star in stars:
            if star in cls.XING_ATTR:
                attr = cls.XING_ATTR[star]
                star_details.append({
                    'name': star,
                    'nature': attr['nature'],
                    'type': attr['type'],
                    'meaning': attr['meaning']
                })
                if attr['nature'] == '吉':
                    ji_count += 1
                elif attr['nature'] == '凶':
                    xiong_count += 1
        
        # 评估宫位
        if ji_count > xiong_count:
            evaluation = '吉'
        elif xiong_count > ji_count:
            evaluation = '凶'
        else:
            evaluation = '平'
        
        return {
            'gong_name': gong_name,
            'stars': star_details,
            'evaluation': evaluation,
            'summary': cls._generate_gong_summary(gong_name, star_details, evaluation)
        }
    
    @classmethod
    def _generate_gong_summary(cls, gong_name: str, stars: List[Dict], 
                               evaluation: str) -> str:
        """生成宫位总结"""
        if not stars:
            return f"{gong_name}无主星，需借对宫星曜论断"
        
        star_names = [s['name'] for s in stars]
        summary = f"{gong_name}有{'、'.join(star_names)}，"
        
        if evaluation == '吉':
            summary += "整体吉利，发展顺遂"
        elif evaluation == '凶':
            summary += "需注意化解，小心行事"
        else:
            summary += "平稳发展，宜守不宜攻"
        
        return summary
    
    @classmethod
    def analyze_full_pan(cls, gong_stars: Dict[str, List[str]]) -> Dict:
        """分析完整命盘
        
        Args:
            gong_stars: {宫名: [星曜列表]}
            
        Returns:
            完整分析结果
        """
        results = {}
        
        for gong_name, stars in gong_stars.items():
            results[gong_name] = cls.analyze_gong(gong_name, stars)
        
        # 生成总体评价
        overall = cls._generate_overall_summary(results)
        
        return {
            'gong_analysis': results,
            'overall': overall
        }
    
    @classmethod
    def _generate_overall_summary(cls, gong_analysis: Dict) -> str:
        """生成总体评价"""
        ming_gong = gong_analysis.get('命宫', {})
        cai_bo = gong_analysis.get('财帛宫', {})
        guan_lu = gong_analysis.get('官禄宫', {})
        
        parts = []
        
        if ming_gong:
            parts.append(f"命宫{ming_gong.get('evaluation', '平')}")
        if cai_bo:
            parts.append(f"财运{cai_bo.get('evaluation', '平')}")
        if guan_lu:
            parts.append(f"事业{guan_lu.get('evaluation', '平')}")
        
        return '，'.join(parts) if parts else '命盘待详细分析'
