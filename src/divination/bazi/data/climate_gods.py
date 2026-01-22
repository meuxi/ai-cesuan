# -*- coding: utf-8 -*-
"""
调候用神规则表
来源：Y-AI-Fortune项目 analysis_engine.py
基于《子平基础概要》调候理论
"""

from typing import Dict, Any, Optional, List

# 完整调候用神规则表（10天干×12地支）
CLIMATE_RULES: Dict[tuple, Dict[str, Any]] = {
    # ========== 甲木调候 ==========
    ('甲', '子'): {'god': '丁火', 'priority': 'high', 'reason': '子月寒水，甲木需丁火暖局解冻'},
    ('甲', '丑'): {'god': '丁火', 'priority': 'high', 'reason': '丑月严寒，甲木需丁火暖局'},
    ('甲', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺，甲木需丙火暖身'},
    ('甲', '卯'): {'god': '庚金', 'priority': 'medium', 'reason': '卯月木极旺，甲木需庚金雕琢成材'},
    ('甲', '辰'): {'god': '庚金', 'priority': 'medium', 'reason': '辰月木仍旺，需庚金栽培'},
    ('甲', '巳'): {'god': '癸水', 'priority': 'medium', 'reason': '巳月火旺，甲木需癸水滋润'},
    ('甲', '午'): {'god': '癸水', 'priority': 'high', 'reason': '午月炎夏，甲木需癸水润局解燥'},
    ('甲', '未'): {'god': '癸水', 'priority': 'high', 'reason': '未月燥土，甲木需癸水润局'},
    ('甲', '申'): {'god': '丁火', 'priority': 'medium', 'reason': '申月金旺，甲木需丁火制金'},
    ('甲', '酉'): {'god': '丁火', 'priority': 'high', 'reason': '酉月金极旺，甲木需丁火制金'},
    ('甲', '戌'): {'god': '庚金', 'priority': 'medium', 'reason': '戌月燥土，甲木需庚金雕琢'},
    ('甲', '亥'): {'god': '丁火', 'priority': 'high', 'reason': '亥月水旺寒，甲木需丁火暖局'},
    
    # ========== 乙木调候 ==========
    ('乙', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月严寒，乙木需丙火暖局'},
    ('乙', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月寒土，乙木需丙火解冻'},
    ('乙', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺，乙木需丙火暖身'},
    ('乙', '卯'): {'god': '癸水', 'priority': 'medium', 'reason': '卯月木极旺，乙木需癸水滋润'},
    ('乙', '辰'): {'god': '癸水', 'priority': 'medium', 'reason': '辰月木渐退，乙木需癸水滋养'},
    ('乙', '巳'): {'god': '癸水', 'priority': 'medium', 'reason': '巳月火旺，乙木需癸水润局'},
    ('乙', '午'): {'god': '癸水', 'priority': 'high', 'reason': '午月干燥，乙木需癸水滋润'},
    ('乙', '未'): {'god': '癸水', 'priority': 'high', 'reason': '未月燥热，乙木需癸水润土'},
    ('乙', '申'): {'god': '丙火', 'priority': 'medium', 'reason': '申月金旺，乙木需丙火制金'},
    ('乙', '酉'): {'god': '丙火', 'priority': 'high', 'reason': '酉月金极旺，乙木需丙火暖局'},
    ('乙', '戌'): {'god': '癸水', 'priority': 'medium', 'reason': '戌月燥土，乙木需癸水润土'},
    ('乙', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水旺，乙木需丙火暖局'},
    
    # ========== 丙火调候 ==========
    ('丙', '子'): {'god': '甲木', 'priority': 'high', 'reason': '子月严寒，丙火需甲木生扶暖局'},
    ('丙', '丑'): {'god': '甲木', 'priority': 'high', 'reason': '丑月寒土，丙火需甲木生火制寒'},
    ('丙', '寅'): {'god': '壬水', 'priority': 'medium', 'reason': '寅月木旺，丙火需壬水调节'},
    ('丙', '卯'): {'god': '壬水', 'priority': 'medium', 'reason': '卯月木旺，丙火需壬水调节'},
    ('丙', '辰'): {'god': '甲木', 'priority': 'medium', 'reason': '辰月土旺，丙火需甲木疏土生火'},
    ('丙', '巳'): {'god': '壬水', 'priority': 'high', 'reason': '巳月火旺，丙火需壬水调节过旺'},
    ('丙', '午'): {'god': '壬水', 'priority': 'high', 'reason': '午月炎夏，丙火需壬水调节炎热'},
    ('丙', '未'): {'god': '壬水', 'priority': 'medium', 'reason': '未月燥土，丙火需壬水润燥'},
    ('丙', '申'): {'god': '甲木', 'priority': 'medium', 'reason': '申月金旺，丙火需甲木生扶'},
    ('丙', '酉'): {'god': '甲木', 'priority': 'medium', 'reason': '酉月金旺，丙火需甲木生扶'},
    ('丙', '戌'): {'god': '甲木', 'priority': 'medium', 'reason': '戌月燥土，丙火需甲木疏土'},
    ('丙', '亥'): {'god': '甲木', 'priority': 'high', 'reason': '亥月水旺，丙火需甲木转化水生火'},
    
    # ========== 丁火调候 ==========
    ('丁', '子'): {'god': '甲木', 'priority': 'high', 'reason': '子月严寒，丁火需甲木生扶'},
    ('丁', '丑'): {'god': '甲木', 'priority': 'high', 'reason': '丑月寒土，丁火需甲木制寒生火'},
    ('丁', '寅'): {'god': '庚金', 'priority': 'medium', 'reason': '寅月甲木当令，丁火需庚金劈甲引丁'},
    ('丁', '卯'): {'god': '庚金', 'priority': 'medium', 'reason': '卯月乙木当令，丁火需庚金制木'},
    ('丁', '辰'): {'god': '甲木', 'priority': 'medium', 'reason': '辰月土旺，丁火需甲木疏土'},
    ('丁', '巳'): {'god': '甲木', 'priority': 'medium', 'reason': '巳月丙火当令，丁火需甲木继续生扶'},
    ('丁', '午'): {'god': '壬水', 'priority': 'high', 'reason': '午月炎夏，丁火需壬水调节'},
    ('丁', '未'): {'god': '甲木', 'priority': 'medium', 'reason': '未月燥土，丁火需甲木疏土'},
    ('丁', '申'): {'god': '甲木', 'priority': 'high', 'reason': '申月庚金当令，丁火需甲木制金生火'},
    ('丁', '酉'): {'god': '甲木', 'priority': 'high', 'reason': '酉月辛金当令，丁火需甲木制金生火'},
    ('丁', '戌'): {'god': '甲木', 'priority': 'medium', 'reason': '戌月燥土，丁火需甲木疏土'},
    ('丁', '亥'): {'god': '甲木', 'priority': 'high', 'reason': '亥月壬水当令，丁火需甲木化水生火'},
    
    # ========== 戊土调候 ==========
    ('戊', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月寒水，戊土需丙火暖局解冻'},
    ('戊', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月严寒，戊土需丙火暖局'},
    ('戊', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺克土，戊土需丙火通关'},
    ('戊', '卯'): {'god': '丙火', 'priority': 'medium', 'reason': '卯月木极旺，戊土需丙火化木生土'},
    ('戊', '辰'): {'god': '甲木', 'priority': 'medium', 'reason': '辰月土旺，戊土需甲木疏土'},
    ('戊', '巳'): {'god': '癸水', 'priority': 'medium', 'reason': '巳月火旺，戊土需癸水润土'},
    ('戊', '午'): {'god': '壬水', 'priority': 'high', 'reason': '午月炎热，戊土需壬水润燥'},
    ('戊', '未'): {'god': '癸水', 'priority': 'high', 'reason': '未月燥土，戊土需癸水滋润'},
    ('戊', '申'): {'god': '丙火', 'priority': 'medium', 'reason': '申月金旺泄土，戊土需丙火生扶'},
    ('戊', '酉'): {'god': '丙火', 'priority': 'medium', 'reason': '酉月金旺，戊土需丙火暖局'},
    ('戊', '戌'): {'god': '甲木', 'priority': 'medium', 'reason': '戌月土旺，戊土需甲木疏土'},
    ('戊', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水旺，戊土需丙火暖局'},
    
    # ========== 己土调候 ==========
    ('己', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月寒水，己土需丙火暖局'},
    ('己', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月严寒，己土需丙火暖局'},
    ('己', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺克土，己土需丙火通关'},
    ('己', '卯'): {'god': '丙火', 'priority': 'medium', 'reason': '卯月木极旺，己土需丙火化木'},
    ('己', '辰'): {'god': '癸水', 'priority': 'medium', 'reason': '辰月湿土，己土需癸水滋润'},
    ('己', '巳'): {'god': '癸水', 'priority': 'medium', 'reason': '巳月火旺，己土需癸水润土'},
    ('己', '午'): {'god': '癸水', 'priority': 'high', 'reason': '午月炎热，己土需癸水润燥'},
    ('己', '未'): {'god': '癸水', 'priority': 'high', 'reason': '未月燥土，己土需癸水滋润'},
    ('己', '申'): {'god': '丙火', 'priority': 'medium', 'reason': '申月金旺泄土，己土需丙火生扶'},
    ('己', '酉'): {'god': '丙火', 'priority': 'medium', 'reason': '酉月金旺，己土需丙火暖局'},
    ('己', '戌'): {'god': '癸水', 'priority': 'medium', 'reason': '戌月燥土，己土需癸水滋润'},
    ('己', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水旺，己土需丙火暖局'},
    
    # ========== 庚金调候 ==========
    ('庚', '子'): {'god': '丁火', 'priority': 'high', 'reason': '子月严寒，庚金需丁火暖局锻炼'},
    ('庚', '丑'): {'god': '丁火', 'priority': 'high', 'reason': '丑月寒土，庚金需丁火暖局'},
    ('庚', '寅'): {'god': '丁火', 'priority': 'medium', 'reason': '寅月木旺，庚金需丁火锻炼'},
    ('庚', '卯'): {'god': '丁火', 'priority': 'medium', 'reason': '卯月木极旺，庚金需丁火锻炼'},
    ('庚', '辰'): {'god': '甲木', 'priority': 'medium', 'reason': '辰月土旺，庚金需甲木疏土'},
    ('庚', '巳'): {'god': '壬水', 'priority': 'medium', 'reason': '巳月火旺，庚金需壬水护金'},
    ('庚', '午'): {'god': '壬水', 'priority': 'high', 'reason': '午月炎夏，庚金需壬水护金'},
    ('庚', '未'): {'god': '壬水', 'priority': 'high', 'reason': '未月燥热，庚金需壬水润金'},
    ('庚', '申'): {'god': '丁火', 'priority': 'medium', 'reason': '申月金旺，庚金需丁火锻炼成器'},
    ('庚', '酉'): {'god': '丁火', 'priority': 'high', 'reason': '酉月金极旺，庚金需丁火锻炼'},
    ('庚', '戌'): {'god': '甲木', 'priority': 'medium', 'reason': '戌月燥土，庚金需甲木疏土'},
    ('庚', '亥'): {'god': '丁火', 'priority': 'high', 'reason': '亥月水旺，庚金需丁火暖局'},
    
    # ========== 辛金调候 ==========
    ('辛', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月严寒，辛金需丙火暖局'},
    ('辛', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月寒土，辛金需丙火暖局'},
    ('辛', '寅'): {'god': '壬水', 'priority': 'medium', 'reason': '寅月木旺，辛金需壬水洗淘'},
    ('辛', '卯'): {'god': '壬水', 'priority': 'medium', 'reason': '卯月木极旺，辛金需壬水护金'},
    ('辛', '辰'): {'god': '壬水', 'priority': 'medium', 'reason': '辰月土旺，辛金需壬水洗淘'},
    ('辛', '巳'): {'god': '壬水', 'priority': 'high', 'reason': '巳月火旺，辛金需壬水护金'},
    ('辛', '午'): {'god': '壬水', 'priority': 'high', 'reason': '午月炎夏，辛金需壬水洗淘'},
    ('辛', '未'): {'god': '壬水', 'priority': 'high', 'reason': '未月燥热，辛金需壬水润金'},
    ('辛', '申'): {'god': '壬水', 'priority': 'medium', 'reason': '申月金旺，辛金需壬水洗淘'},
    ('辛', '酉'): {'god': '壬水', 'priority': 'medium', 'reason': '酉月金极旺，辛金需壬水泄秀'},
    ('辛', '戌'): {'god': '壬水', 'priority': 'medium', 'reason': '戌月燥土，辛金需壬水滋润'},
    ('辛', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水旺，辛金需丙火暖局'},
    
    # ========== 壬水调候 ==========
    ('壬', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月水旺，壬水需丙火暖局'},
    ('壬', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月严寒，壬水需丙火暖局'},
    ('壬', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺泄水，壬水需丙火暖局'},
    ('壬', '卯'): {'god': '丙火', 'priority': 'medium', 'reason': '卯月木极旺，壬水需丙火通关'},
    ('壬', '辰'): {'god': '甲木', 'priority': 'medium', 'reason': '辰月土旺克水，壬水需甲木疏土'},
    ('壬', '巳'): {'god': '庚金', 'priority': 'medium', 'reason': '巳月火旺，壬水需庚金生水'},
    ('壬', '午'): {'god': '庚金', 'priority': 'high', 'reason': '午月炎夏，壬水需庚金发水源'},
    ('壬', '未'): {'god': '庚金', 'priority': 'high', 'reason': '未月燥热，壬水需庚金生水'},
    ('壬', '申'): {'god': '戊土', 'priority': 'medium', 'reason': '申月金旺生水，壬水需戊土制水'},
    ('壬', '酉'): {'god': '戊土', 'priority': 'medium', 'reason': '酉月金极旺，壬水需戊土制水'},
    ('壬', '戌'): {'god': '甲木', 'priority': 'medium', 'reason': '戌月土旺克水，壬水需甲木疏土'},
    ('壬', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水极旺，壬水需丙火暖局'},
    
    # ========== 癸水调候 ==========
    ('癸', '子'): {'god': '丙火', 'priority': 'high', 'reason': '子月水旺，癸水需丙火暖局'},
    ('癸', '丑'): {'god': '丙火', 'priority': 'high', 'reason': '丑月严寒，癸水需丙火暖局'},
    ('癸', '寅'): {'god': '丙火', 'priority': 'medium', 'reason': '寅月木旺泄水，癸水需丙火暖局'},
    ('癸', '卯'): {'god': '丙火', 'priority': 'medium', 'reason': '卯月木极旺，癸水需丙火通关'},
    ('癸', '辰'): {'god': '辛金', 'priority': 'medium', 'reason': '辰月土旺克水，癸水需辛金生水'},
    ('癸', '巳'): {'god': '辛金', 'priority': 'medium', 'reason': '巳月火旺，癸水需辛金生水'},
    ('癸', '午'): {'god': '辛金', 'priority': 'high', 'reason': '午月炎夏，癸水需辛金发水源'},
    ('癸', '未'): {'god': '辛金', 'priority': 'high', 'reason': '未月燥热，癸水需辛金生水'},
    ('癸', '申'): {'god': '丁火', 'priority': 'medium', 'reason': '申月金旺生水，癸水需丁火暖局'},
    ('癸', '酉'): {'god': '丁火', 'priority': 'medium', 'reason': '酉月金极旺，癸水需丁火暖局'},
    ('癸', '戌'): {'god': '辛金', 'priority': 'medium', 'reason': '戌月土旺克水，癸水需辛金生水'},
    ('癸', '亥'): {'god': '丙火', 'priority': 'high', 'reason': '亥月水极旺，癸水需丙火暖局'},
}

# 天干五行映射
GAN_ELEMENT = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水'
}

# 季节月份映射
WINTER_MONTHS = ['子', '丑', '亥']  # 冬季
SUMMER_MONTHS = ['巳', '午', '未']  # 夏季
SPRING_MONTHS = ['寅', '卯', '辰']  # 春季
AUTUMN_MONTHS = ['申', '酉', '戌']  # 秋季


def get_climate_god(day_gan: str, month_zhi: str) -> Dict[str, Any]:
    """
    获取调候用神
    
    Args:
        day_gan: 日干（甲乙丙丁戊己庚辛壬癸）
        month_zhi: 月支（子丑寅卯辰巳午未申酉戌亥）
        
    Returns:
        调候用神信息，包含god/priority/reason
    """
    # 查找特定调候规则
    rule = CLIMATE_RULES.get((day_gan, month_zhi))
    if rule:
        return rule
    
    # 默认调候逻辑
    day_element = GAN_ELEMENT.get(day_gan, '')
    
    # 冬月用火，夏月用水的基本调候原则
    if month_zhi in WINTER_MONTHS:
        if day_element in ['金', '水']:
            return {'god': '丁火', 'priority': 'high', 'reason': f'冬月{day_element}寒，需火暖局'}
        else:
            return {'god': '丙火', 'priority': 'medium', 'reason': f'冬月需火调候'}
    elif month_zhi in SUMMER_MONTHS:
        if day_element in ['火', '土']:
            return {'god': '癸水', 'priority': 'high', 'reason': f'夏月{day_element}燥，需水润局'}
        else:
            return {'god': '壬水', 'priority': 'medium', 'reason': f'夏月需水调候'}
    else:
        return {'god': '中和', 'priority': 'low', 'reason': '春秋二季调候次要'}


def get_all_climate_rules() -> Dict[tuple, Dict[str, Any]]:
    """获取完整调候规则表"""
    return CLIMATE_RULES.copy()


def analyze_climate_needs(day_gan: str, month_zhi: str, 
                          existing_elements: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    分析调候需求
    
    Args:
        day_gan: 日干
        month_zhi: 月支
        existing_elements: 八字中已有的五行元素
        
    Returns:
        调候分析结果
    """
    climate_info = get_climate_god(day_gan, month_zhi)
    
    # 判断调候是否已得
    is_satisfied = False
    if existing_elements and climate_info['god'] != '中和':
        god_element = GAN_ELEMENT.get(climate_info['god'][0], '')
        is_satisfied = god_element in existing_elements
    
    return {
        'climate_god': climate_info['god'],
        'priority': climate_info['priority'],
        'reason': climate_info['reason'],
        'is_satisfied': is_satisfied,
        'season': _get_season(month_zhi),
        'need_description': _get_need_description(day_gan, month_zhi)
    }


def _get_season(month_zhi: str) -> str:
    """获取季节"""
    if month_zhi in WINTER_MONTHS:
        return '冬季'
    elif month_zhi in SUMMER_MONTHS:
        return '夏季'
    elif month_zhi in SPRING_MONTHS:
        return '春季'
    elif month_zhi in AUTUMN_MONTHS:
        return '秋季'
    return '未知'


def _get_need_description(day_gan: str, month_zhi: str) -> str:
    """获取调候需求描述"""
    season = _get_season(month_zhi)
    day_element = GAN_ELEMENT.get(day_gan, '')
    
    descriptions = {
        '冬季': f'{day_element}日主生于冬季，天寒地冻，需火暖局调候',
        '夏季': f'{day_element}日主生于夏季，天气炎热，需水润局调候',
        '春季': f'{day_element}日主生于春季，万物生发，调候需求较低',
        '秋季': f'{day_element}日主生于秋季，金气肃杀，调候需求较低'
    }
    return descriptions.get(season, f'{day_element}日主调候需求待分析')
