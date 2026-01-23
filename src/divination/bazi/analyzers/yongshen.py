# -*- coding: utf-8 -*-
"""
用神分析器 - 格局与调候综合判断
来源：mingpan项目 YongShenAnalyzer.ts
实现完整的用神（喜用神）分析系统
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

# 五行
FIVE_ELEMENTS = ['木', '火', '土', '金', '水']

# 五行相生关系（A生B）
ELEMENT_GENERATES = {
    '木': '火', '火': '土', '土': '金', '金': '水', '水': '木'
}

# 五行相克关系（A克B）
ELEMENT_CONTROLS = {
    '木': '土', '土': '水', '水': '火', '火': '金', '金': '木'
}

# 五行被生关系（A被B生）
ELEMENT_GENERATED_BY = {
    '木': '水', '火': '木', '土': '火', '金': '土', '水': '金'
}

# 五行被克关系（A被B克）
ELEMENT_CONTROLLED_BY = {
    '木': '金', '火': '水', '土': '木', '金': '火', '水': '土'
}

# 天干五行
STEM_ELEMENT = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}


@dataclass
class YongShenAnalysis:
    """用神分析结果"""
    yong_shen: List[str]  # 用神（最需要的五行）
    xi_shen: List[str]    # 喜神（次要有利的五行）
    ji_shen: List[str]    # 忌神（不利的五行）
    xian_shen: List[str]  # 闲神（中性的五行）
    explanation: str      # 分析说明
    method: str           # 分析方法（调候/格局/平衡）
    recommendations: Dict[str, Any] = field(default_factory=dict)


class YongShenAnalyzer:
    """用神分析器"""
    
    @classmethod
    def analyze(cls, bazi: Dict[str, Dict[str, str]], 
                strength_result: Dict[str, Any],
                pattern_result: Optional[Dict[str, Any]] = None,
                climate_result: Optional[Dict[str, Any]] = None) -> YongShenAnalysis:
        """
        综合分析用神
        
        优先级：
        1. 高优先级格局（从格、化气格）→ 按格局规则
        2. 调候急需（寒暑极端月份）→ 调候优先
        3. 普通格局 → 根据日主强弱判断
        """
        day_master = bazi['day']['stem']
        day_master_element = STEM_ELEMENT[day_master]
        
        # 检查格局优先级
        pattern_priority = 0
        pattern_type = '正格'
        if pattern_result:
            pattern_priority = pattern_result.get('priority', 0)
            pattern_type = pattern_result.get('type', '正格')
        
        # 1. 高优先级格局（从格、化气格等）
        if pattern_priority >= 8:
            return cls._analyze_by_pattern(
                day_master_element, pattern_result, strength_result
            )
        
        # 2. 检查是否需要调候优先
        if climate_result and climate_result.get('priority') == 'high':
            return cls._analyze_climate_first(
                day_master_element, climate_result, strength_result
            )
        
        # 3. 普通格局分析
        return cls._analyze_normal(
            bazi, day_master_element, strength_result, pattern_result, climate_result
        )
    
    @classmethod
    def _analyze_normal(cls, bazi: Dict, day_master_element: str,
                        strength_result: Dict, pattern_result: Optional[Dict],
                        climate_result: Optional[Dict]) -> YongShenAnalysis:
        """普通格局分析（根据日主强弱）"""
        strength = strength_result.get('strength', '中和')
        
        yong_shen = []
        xi_shen = []
        ji_shen = []
        xian_shen = []
        
        if strength in ['身弱', '衰极', '偏弱']:
            # 身弱：需要生扶
            # 用神：印星（生我）和比劫（同我）
            generating = ELEMENT_GENERATED_BY[day_master_element]
            yong_shen.append(generating)  # 印星
            yong_shen.append(day_master_element)  # 比劫
            
            # 喜神：生印星的元素
            xi_shen.append(ELEMENT_GENERATED_BY[generating])
            
            # 忌神：克泄耗
            ji_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀克我
            ji_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤泄我
            ji_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星耗我
            
            method = '扶抑法'
            explanation = f'日主{day_master_element}身弱，喜印星{generating}生扶，比劫{day_master_element}帮身'
            
        elif strength in ['身旺', '旺极', '偏强']:
            # 身旺：需要克泄耗
            # 用神：食伤（泄我）和官杀（克我）
            draining = ELEMENT_GENERATES[day_master_element]  # 食伤
            controlling = ELEMENT_CONTROLLED_BY[day_master_element]  # 官杀
            
            yong_shen.append(draining)
            yong_shen.append(controlling)
            
            # 喜神：财星（我克）
            xi_shen.append(ELEMENT_CONTROLS[day_master_element])
            
            # 忌神：印星和比劫
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星
            ji_shen.append(day_master_element)  # 比劫
            
            method = '扶抑法'
            explanation = f'日主{day_master_element}身旺，喜食伤{draining}泄秀，官杀{controlling}制身'
            
        else:
            # 中和：根据五行缺失判断
            element_counts = cls._count_elements(bazi)
            missing = [e for e in FIVE_ELEMENTS if element_counts.get(e, 0) == 0]
            excessive = [e for e in FIVE_ELEMENTS if element_counts.get(e, 0) > 3]
            
            # 用神：缺失的元素 + 制约过旺元素的元素
            yong_shen.extend(missing)
            for elem in excessive:
                controller = ELEMENT_CONTROLLED_BY[elem]
                if controller not in yong_shen:
                    yong_shen.append(controller)
            
            # 喜神：生用神的元素
            for elem in yong_shen:
                supporter = ELEMENT_GENERATED_BY[elem]
                if supporter not in yong_shen and supporter not in xi_shen:
                    xi_shen.append(supporter)
            
            # 忌神：过旺的元素
            ji_shen.extend(excessive)
            
            method = '平衡法'
            explanation = '日主中和，取五行平衡为要'
        
        # 闲神：剩余元素
        for elem in FIVE_ELEMENTS:
            if elem not in yong_shen and elem not in xi_shen and elem not in ji_shen:
                xian_shen.append(elem)
        
        # 考虑调候因素
        if climate_result and climate_result.get('god'):
            climate_god_elem = STEM_ELEMENT.get(climate_result['god'][0], '')
            if climate_god_elem and climate_god_elem not in yong_shen:
                explanation += f'；兼需{climate_god_elem}调候'
        
        return YongShenAnalysis(
            yong_shen=yong_shen,
            xi_shen=xi_shen,
            ji_shen=ji_shen,
            xian_shen=xian_shen,
            explanation=explanation,
            method=method,
            recommendations=cls._generate_recommendations(yong_shen, xi_shen, day_master_element)
        )
    
    @classmethod
    def _analyze_by_pattern(cls, day_master_element: str,
                            pattern_result: Dict, 
                            strength_result: Dict) -> YongShenAnalysis:
        """按格局规则分析用神"""
        pattern_type = pattern_result.get('type', '')
        yong_shen = []
        xi_shen = []
        ji_shen = []
        xian_shen = []
        
        if '从强' in pattern_type or '从旺' in pattern_type or '专旺' in pattern_type:
            # 从强格/专旺格：顺势而行
            yong_shen.append(day_master_element)  # 比劫
            yong_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星
            
            xi_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤泄秀
            
            ji_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀
            ji_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星
            
            explanation = f'{pattern_type}，宜顺不宜逆，喜印比生扶'
            
        elif '从弱' in pattern_type or '从势' in pattern_type:
            # 从弱格/从势格：顺从大势
            draining = ELEMENT_GENERATES[day_master_element]
            controlling = ELEMENT_CONTROLLED_BY[day_master_element]
            wealth = ELEMENT_CONTROLS[day_master_element]
            
            yong_shen.extend([draining, controlling, wealth])
            
            ji_shen.append(day_master_element)
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])
            
            explanation = f'{pattern_type}，弃命从势，喜财官食伤'
            
        elif '从财' in pattern_type:
            # 从财格
            wealth = ELEMENT_CONTROLS[day_master_element]
            yong_shen.append(wealth)
            yong_shen.append(ELEMENT_GENERATES[wealth])  # 财生官
            
            xi_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤生财
            
            ji_shen.append(day_master_element)
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])
            
            explanation = f'从财格，喜财星{wealth}，忌比劫夺财'
            
        elif '从官' in pattern_type:
            # 从官格
            official = ELEMENT_CONTROLLED_BY[day_master_element]
            yong_shen.append(official)
            yong_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财生官
            
            ji_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤克官
            ji_shen.append(day_master_element)
            
            explanation = f'从官格，喜官杀{official}，忌食伤克官'
            
        elif '从儿' in pattern_type:
            # 从儿格（从食伤）
            output = ELEMENT_GENERATES[day_master_element]
            yong_shen.append(output)
            yong_shen.append(ELEMENT_GENERATES[output])  # 食伤生财
            
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星克食伤
            ji_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀
            
            explanation = f'从儿格，喜食伤{output}生财，忌印枭夺食'
            
        elif '化' in pattern_type:
            # 化气格
            # 根据化气元素判断用神
            for elem in FIVE_ELEMENTS:
                if elem in pattern_type:
                    yong_shen.append(elem)
                    yong_shen.append(ELEMENT_GENERATED_BY[elem])
                    ji_shen.append(ELEMENT_CONTROLLED_BY[elem])
                    break
            
            explanation = f'{pattern_type}，真化需顺其势'
        
        elif '曲直' in pattern_type:
            # 曲直格（木局）
            yong_shen.extend(['木', '水'])
            xi_shen.append('火')  # 木生火泄秀
            ji_shen.append('金')  # 金克木
            explanation = '曲直格成立，喜木水生扶，忌金克'
            
        elif '炎上' in pattern_type:
            # 炎上格（火局）
            yong_shen.extend(['火', '木'])
            xi_shen.append('土')  # 火生土泄秀
            ji_shen.append('水')  # 水克火
            explanation = '炎上格成立，喜火木生扶，忌水克'
            
        elif '稼穡' in pattern_type:
            # 稼穡格（土局）
            yong_shen.extend(['土', '火'])
            xi_shen.append('金')  # 土生金泄秀
            ji_shen.append('木')  # 木克土
            explanation = '稼穡格成立，喜土火生扶，忌木克'
            
        elif '从革' in pattern_type:
            # 从革格（金局）
            yong_shen.extend(['金', '土'])
            xi_shen.append('水')  # 金生水泄秀
            ji_shen.append('火')  # 火克金
            explanation = '从革格成立，喜金土生扶，忌火克'
            
        elif '润下' in pattern_type:
            # 润下格（水局）
            yong_shen.extend(['水', '金'])
            xi_shen.append('木')  # 水生木泄秀
            ji_shen.append('土')  # 土克水
            explanation = '润下格成立，喜水金生扶，忌土克'
        
        elif '建禄' in pattern_type:
            # 建禄格
            # 身旺，喜泄耗
            yong_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤
            yong_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星
            xi_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀
            ji_shen.append(day_master_element)  # 比劫
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星
            explanation = '建禄格，日主有根，喜食伤生财，官杀制身'
            
        elif '羊刃' in pattern_type:
            # 羊刃格
            # 身强，喜官杀制刃
            yong_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀制刃
            yong_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星
            xi_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤
            ji_shen.append(day_master_element)  # 比劫
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星
            explanation = '羊刃格，身强刃旺，喜官杀制刃，财星泄刃'
        
        elif '正官' in pattern_type:
            # 正官格
            official = ELEMENT_CONTROLLED_BY[day_master_element]
            yong_shen.append(official)  # 正官为用
            xi_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星生官
            ji_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤克官
            explanation = f'正官格，喜官星{official}当权，财星生官，忌食伤克官'
            
        elif '七杀' in pattern_type:
            # 七杀格
            killer = ELEMENT_CONTROLLED_BY[day_master_element]
            yong_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤制杀
            xi_shen.append(killer)  # 七杀为用
            xi_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星化杀
            ji_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星生杀
            explanation = f'七杀格，喜食伤制杀，印星化杀，忌财星生杀'
            
        elif '正财' in pattern_type:
            # 正财格
            wealth = ELEMENT_CONTROLS[day_master_element]
            yong_shen.append(wealth)  # 正财为用
            xi_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤生财
            ji_shen.append(day_master_element)  # 比劫夺财
            explanation = f'正财格，喜财星{wealth}，食伤生财，忌比劫夺财'
            
        elif '偏财' in pattern_type:
            # 偏财格
            wealth = ELEMENT_CONTROLS[day_master_element]
            yong_shen.append(wealth)  # 偏财为用
            xi_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤生财
            ji_shen.append(day_master_element)  # 比劫夺财
            explanation = f'偏财格，喜财星{wealth}，食伤生财，忌比劫夺财'
            
        elif '正印' in pattern_type:
            # 正印格
            seal = ELEMENT_GENERATED_BY[day_master_element]
            yong_shen.append(seal)  # 正印为用
            yong_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀生印
            ji_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星克印
            explanation = f'正印格，喜印星{seal}，官杀生印，忌财星坏印'
            
        elif '偏印' in pattern_type:
            # 偏印格
            seal = ELEMENT_GENERATED_BY[day_master_element]
            yong_shen.append(seal)  # 偏印为用
            xi_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官杀生印
            xi_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星制偏印
            ji_shen.append(ELEMENT_GENERATES[day_master_element])  # 食伤被偏印所夺
            explanation = f'偏印格，喜印星{seal}，财星制偏印护食伤'
            
        elif '食神' in pattern_type:
            # 食神格
            output = ELEMENT_GENERATES[day_master_element]
            yong_shen.append(output)  # 食神为用
            xi_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星食伤生
            ji_shen.append(ELEMENT_GENERATED_BY[day_master_element])  # 印星夺食
            explanation = f'食神格，喜食神{output}生财，忌偏印夺食'
            
        elif '伤官' in pattern_type:
            # 伤官格
            output = ELEMENT_GENERATES[day_master_element]
            yong_shen.append(output)  # 伤官为用
            xi_shen.append(ELEMENT_CONTROLS[day_master_element])  # 财星
            ji_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])  # 官星被伤官所克
            explanation = f'伤官格，喜伤官{output}生财，忌官星'
        
        elif '五行俱全' in pattern_type:
            # 五行俱全格
            # 取五行平衡为要
            yong_shen.append(day_master_element)
            explanation = '五行俱全格，命中平衡，喜用需视具体强弱而定'
            
        elif '两神成象' in pattern_type:
            # 两神成象格
            # 顺势而行
            explanation = '两神成象格，专精特化，顺势而行'
            
        elif '天元一气' in pattern_type:
            # 天元一气格
            yong_shen.append(day_master_element)
            yong_shen.append(ELEMENT_GENERATED_BY[day_master_element])
            ji_shen.append(ELEMENT_CONTROLLED_BY[day_master_element])
            explanation = '天元一气格，天干纯一，顺势而行'
            
        else:
            # 其他格局走普通分析
            return cls._analyze_normal({}, day_master_element, strength_result, pattern_result, None)
        
        # 闲神
        for elem in FIVE_ELEMENTS:
            if elem not in yong_shen and elem not in xi_shen and elem not in ji_shen:
                xian_shen.append(elem)
        
        return YongShenAnalysis(
            yong_shen=yong_shen,
            xi_shen=xi_shen,
            ji_shen=ji_shen,
            xian_shen=xian_shen,
            explanation=explanation,
            method='格局法',
            recommendations=cls._generate_recommendations(yong_shen, xi_shen, day_master_element)
        )
    
    @classmethod
    def _analyze_climate_first(cls, day_master_element: str,
                               climate_result: Dict,
                               strength_result: Dict) -> YongShenAnalysis:
        """调候优先分析"""
        climate_god = climate_result.get('god', '')
        climate_reason = climate_result.get('reason', '')
        
        yong_shen = []
        xi_shen = []
        ji_shen = []
        xian_shen = []
        
        # 调候用神
        if climate_god:
            climate_elem = STEM_ELEMENT.get(climate_god[0], '')
            if climate_elem:
                yong_shen.append(climate_elem)
                # 生调候用神的元素为喜神
                xi_shen.append(ELEMENT_GENERATED_BY[climate_elem])
        
        # 再考虑日主强弱
        strength = strength_result.get('strength', '中和')
        if strength in ['身弱', '衰极', '偏弱']:
            helper = ELEMENT_GENERATED_BY[day_master_element]
            if helper not in yong_shen:
                xi_shen.append(helper)
            if day_master_element not in yong_shen:
                xi_shen.append(day_master_element)
        elif strength in ['身旺', '旺极', '偏强']:
            drainer = ELEMENT_GENERATES[day_master_element]
            if drainer not in yong_shen:
                xi_shen.append(drainer)
        
        # 忌神：克制调候用神的元素
        for elem in yong_shen:
            controller = ELEMENT_CONTROLLED_BY[elem]
            if controller not in ji_shen:
                ji_shen.append(controller)
        
        # 闲神
        for elem in FIVE_ELEMENTS:
            if elem not in yong_shen and elem not in xi_shen and elem not in ji_shen:
                xian_shen.append(elem)
        
        explanation = f'调候急需，{climate_reason}'
        
        return YongShenAnalysis(
            yong_shen=yong_shen,
            xi_shen=xi_shen,
            ji_shen=ji_shen,
            xian_shen=xian_shen,
            explanation=explanation,
            method='调候法',
            recommendations=cls._generate_recommendations(yong_shen, xi_shen, day_master_element)
        )
    
    @classmethod
    def _count_elements(cls, bazi: Dict) -> Dict[str, int]:
        """统计八字五行分布"""
        counts = {e: 0 for e in FIVE_ELEMENTS}
        
        for pillar in ['year', 'month', 'day', 'hour']:
            stem = bazi[pillar].get('stem', '')
            branch = bazi[pillar].get('branch', '')
            
            if stem in STEM_ELEMENT:
                counts[STEM_ELEMENT[stem]] += 1
            
            # 地支主气
            branch_elements = {
                '子': '水', '丑': '土', '寅': '木', '卯': '木',
                '辰': '土', '巳': '火', '午': '火', '未': '土',
                '申': '金', '酉': '金', '戌': '土', '亥': '水'
            }
            if branch in branch_elements:
                counts[branch_elements[branch]] += 1
        
        return counts
    
    @classmethod
    def _generate_recommendations(cls, yong_shen: List[str], 
                                   xi_shen: List[str],
                                   day_master_element: str) -> Dict[str, Any]:
        """生成用神建议"""
        # 五行对应颜色
        element_colors = {
            '木': ['绿色', '青色'],
            '火': ['红色', '紫色', '橙色'],
            '土': ['黄色', '咖啡色', '棕色'],
            '金': ['白色', '银色', '金色'],
            '水': ['黑色', '蓝色', '灰色']
        }
        
        # 五行对应方位
        element_directions = {
            '木': '东方',
            '火': '南方',
            '土': '中央',
            '金': '西方',
            '水': '北方'
        }
        
        # 五行对应行业
        element_careers = {
            '木': ['教育', '文化', '出版', '园艺', '服装', '家具', '中医'],
            '火': ['餐饮', '能源', '电子', '娱乐', '美容', '照明', '广告'],
            '土': ['房地产', '建筑', '农业', '矿业', '保险', '仓储', '陶瓷'],
            '金': ['金融', '银行', '五金', '机械', '汽车', '法律', '军警'],
            '水': ['贸易', '物流', '旅游', '水产', 'IT', '媒体', '咨询']
        }
        
        favorable_colors = []
        favorable_directions = []
        favorable_careers = []
        
        for elem in yong_shen + xi_shen:
            if elem in element_colors:
                favorable_colors.extend(element_colors[elem])
            if elem in element_directions:
                favorable_directions.append(element_directions[elem])
            if elem in element_careers:
                favorable_careers.extend(element_careers[elem])
        
        return {
            'colors': list(set(favorable_colors)),
            'directions': list(set(favorable_directions)),
            'careers': list(set(favorable_careers[:10])),
            'summary': f'宜用{",".join(yong_shen)}，喜{",".join(xi_shen)}'
        }
