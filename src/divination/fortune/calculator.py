"""
运势计算器
基于八字命理理论，通过日主与流日/流月的五行生克关系计算个性化运势

移植自 MingAI-master/src/lib/fortune.ts
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Dict, Any
import math

# 天干五行映射
STEM_ELEMENTS = {
    '甲': '木', '乙': '木',
    '丙': '火', '丁': '火',
    '戊': '土', '己': '土',
    '庚': '金', '辛': '金',
    '壬': '水', '癸': '水',
}

# 五行相生相克权重
ELEMENT_RELATION_SCORES = {
    'same': 75,       # 比和：平稳
    'produce': 85,    # 我生：付出但有回报
    'produced': 90,   # 生我：贵人运
    'control': 70,    # 我克：有压力但可掌控
    'controlled': 55, # 克我：有阻力
}

# 十神对应各类运势的加成
TEN_GOD_FORTUNE_BONUS = {
    '比肩': {'career': 5, 'love': 0, 'wealth': -5, 'health': 5, 'social': 10},
    '劫财': {'career': 0, 'love': -5, 'wealth': -10, 'health': 5, 'social': 5},
    '食神': {'career': 5, 'love': 10, 'wealth': 5, 'health': 10, 'social': 8},
    '伤官': {'career': -5, 'love': 5, 'wealth': 5, 'health': 0, 'social': -5},
    '偏财': {'career': 5, 'love': 5, 'wealth': 15, 'health': 0, 'social': 5},
    '正财': {'career': 5, 'love': 10, 'wealth': 10, 'health': 0, 'social': 5},
    '七杀': {'career': 10, 'love': -5, 'wealth': 5, 'health': -5, 'social': -3},
    '正官': {'career': 15, 'love': 5, 'wealth': 5, 'health': 0, 'social': 8},
    '偏印': {'career': 5, 'love': 0, 'wealth': -5, 'health': 5, 'social': 0},
    '正印': {'career': 10, 'love': 5, 'wealth': 0, 'health': 10, 'social': 5},
}

# 五行对应颜色
ELEMENT_COLORS = {
    '木': '绿色',
    '火': '红色',
    '土': '黄色',
    '金': '白色',
    '水': '黑色/蓝色',
}

# 五行对应方位
ELEMENT_DIRECTIONS = {
    '木': '东方',
    '火': '南方',
    '土': '中央',
    '金': '西方',
    '水': '北方',
}


@dataclass
class FortuneScores:
    """运势评分"""
    overall: int    # 综合运势 (0-100)
    career: int     # 事业运
    love: int       # 感情运
    wealth: int     # 财运
    health: int     # 健康运
    social: int     # 人际运


@dataclass
class DailyFortune(FortuneScores):
    """每日运势"""
    date: str
    day_stem: str
    day_branch: str
    ten_god: str           # 流日与日主形成的十神
    advice: List[str]      # 运势建议
    lucky_color: str       # 幸运色
    lucky_direction: str   # 吉方位


@dataclass
class MonthlyFortune(FortuneScores):
    """每月运势"""
    year: int
    month: int
    month_stem: str
    month_branch: str
    ten_god: str
    summary: str
    key_dates: List[Dict[str, Any]]


def get_stem_yin_yang(stem: str) -> str:
    """获取天干阴阳"""
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    return 'yang' if stem in yang_stems else 'yin'


def get_element_relation(from_el: str, to_el: str) -> str:
    """获取五行生克关系"""
    order = ['木', '火', '土', '金', '水']
    from_idx = order.index(from_el)
    to_idx = order.index(to_el)
    
    if from_el == to_el:
        return 'same'
    if (from_idx + 1) % 5 == to_idx:
        return 'produce'
    if (to_idx + 1) % 5 == from_idx:
        return 'produced'
    if (from_idx + 2) % 5 == to_idx:
        return 'control'
    return 'controlled'


def calculate_ten_god(day_stem: str, target_stem: str) -> str:
    """计算十神"""
    if day_stem == target_stem:
        return '比肩'
    
    day_element = STEM_ELEMENTS.get(day_stem, '木')
    target_element = STEM_ELEMENTS.get(target_stem, '木')
    day_yy = get_stem_yin_yang(day_stem)
    target_yy = get_stem_yin_yang(target_stem)
    same_yy = day_yy == target_yy
    
    relation = get_element_relation(day_element, target_element)
    
    ten_god_map = {
        'same': ('比肩', '劫财'),
        'produce': ('食神', '伤官'),
        'control': ('偏财', '正财'),
        'controlled': ('七杀', '正官'),
        'produced': ('偏印', '正印'),
    }
    
    return ten_god_map[relation][0 if same_yy else 1]


def clamp_score(score: float) -> int:
    """限制分数在合理范围内"""
    return max(30, min(98, round(score)))


def seeded_random(seed: int, offset: int = 0) -> float:
    """基于种子的伪随机函数"""
    x = math.sin(seed + offset) * 10000
    return x - math.floor(x)


def get_lucky_element(user_element: str) -> str:
    """获取幸运五行（生我者为吉）"""
    order = ['木', '火', '土', '金', '水']
    idx = order.index(user_element)
    return order[(idx + 4) % 5]


def generate_daily_advice(ten_god: str, overall: int, career: int, wealth: int, health: int) -> List[str]:
    """生成每日建议"""
    advice = []
    
    ten_god_advice = {
        '比肩': '今日适合与朋友合作，互帮互助',
        '劫财': '注意财务支出，避免借贷',
        '食神': '创意灵感丰富，适合发挥才华',
        '伤官': '思维活跃但需谨言慎行',
        '偏财': '有意外之财，可适当投资',
        '正财': '正财运佳，努力工作有回报',
        '七杀': '压力较大，但挑战中有机遇',
        '正官': '贵人运旺，适合拓展人脉',
        '偏印': '适合学习研究，提升自我',
        '正印': '长辈相助，学业事业顺遂',
    }
    
    advice.append(ten_god_advice.get(ten_god, '顺其自然，平常心对待'))
    
    if overall >= 80:
        advice.append('整体运势极佳，可大胆行动')
    elif overall < 60:
        advice.append('今日宜静不宜动，稳健为上')
    
    if career >= 80:
        advice.append('事业运强劲，把握晋升机会')
    elif career < 60:
        advice.append('职场需低调行事，避免冲突')
    
    if wealth < 60:
        advice.append('财运平平，不宜大额消费投资')
    
    if health < 60:
        advice.append('注意休息，避免过度劳累')
    
    return advice[:4]


def generate_monthly_summary(ten_god: str, overall: int) -> str:
    """生成月度总结"""
    ten_god_summary = {
        '比肩': '本月人际关系活跃，适合团队合作',
        '劫财': '本月财务需谨慎，防止意外支出',
        '食神': '本月创意运势佳，适合发展副业',
        '伤官': '本月思维活跃，但需注意言行',
        '偏财': '本月偏财运旺，可尝试投资',
        '正财': '本月正财稳定，努力有回报',
        '七杀': '本月挑战与机遇并存，需果断行动',
        '正官': '本月事业运强，贵人相助',
        '偏印': '本月适合学习进修，提升能力',
        '正印': '本月稳健发展，长辈贵人相助',
    }
    
    summary = ten_god_summary.get(ten_god, '本月运势平稳，顺其自然')
    
    if overall >= 80:
        summary += '。整体运势极佳，可积极把握机会。'
    elif overall >= 65:
        summary += '。运势良好，稳步前进即可。'
    else:
        summary += '。建议稳健行事，避免冒险。'
    
    return summary


def get_ganzhi_from_date(target_date: date) -> tuple:
    """从日期获取干支（简化实现，使用查表法）"""
    # 天干地支
    heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 使用1900年1月31日（甲辰日）作为基准
    base_date = date(1900, 1, 31)
    delta = (target_date - base_date).days
    
    stem_idx = delta % 10
    branch_idx = delta % 12
    
    return heavenly_stems[stem_idx], earthly_branches[branch_idx]


def calculate_daily_fortune(day_master: str, target_date: date) -> DailyFortune:
    """
    计算每日个性化运势
    
    Args:
        day_master: 用户八字日主天干
        target_date: 目标日期
    
    Returns:
        DailyFortune: 每日运势数据
    """
    day_stem, day_branch = get_ganzhi_from_date(target_date)
    
    # 计算流日与日主的十神关系
    ten_god = calculate_ten_god(day_master, day_stem)
    
    # 计算五行生克关系基础分
    day_element = STEM_ELEMENTS.get(day_stem, '木')
    user_element = STEM_ELEMENTS.get(day_master, '木')
    relation = get_element_relation(user_element, day_element)
    base_score = ELEMENT_RELATION_SCORES.get(relation, 75)
    
    # 获取十神加成
    god_bonus = TEN_GOD_FORTUNE_BONUS.get(ten_god, {})
    
    # 日期种子
    date_seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
    
    # 计算各项运势
    career = clamp_score(base_score + god_bonus.get('career', 0) + seeded_random(date_seed, 1) * 10 - 5)
    love = clamp_score(base_score + god_bonus.get('love', 0) + seeded_random(date_seed, 2) * 10 - 5)
    wealth = clamp_score(base_score + god_bonus.get('wealth', 0) + seeded_random(date_seed, 3) * 10 - 5)
    health = clamp_score(base_score + god_bonus.get('health', 0) + seeded_random(date_seed, 4) * 10 - 5)
    social = clamp_score(base_score + god_bonus.get('social', 0) + seeded_random(date_seed, 5) * 10 - 5)
    overall = clamp_score((career + love + wealth + health + social) / 5)
    
    # 生成运势建议
    advice = generate_daily_advice(ten_god, overall, career, wealth, health)
    
    # 幸运色和方位
    lucky_element = get_lucky_element(user_element)
    lucky_color = ELEMENT_COLORS.get(lucky_element, '白色')
    lucky_direction = ELEMENT_DIRECTIONS.get(lucky_element, '中央')
    
    return DailyFortune(
        date=target_date.strftime('%Y-%m-%d'),
        day_stem=day_stem,
        day_branch=day_branch,
        ten_god=ten_god,
        overall=overall,
        career=career,
        love=love,
        wealth=wealth,
        health=health,
        social=social,
        advice=advice,
        lucky_color=lucky_color,
        lucky_direction=lucky_direction,
    )


def calculate_monthly_fortune(day_master: str, year: int, month: int) -> MonthlyFortune:
    """计算每月个性化运势"""
    # 获取月中干支
    mid_date = date(year, month, 15)
    month_stem, month_branch = get_ganzhi_from_date(mid_date)
    
    # 计算流月与日主的十神关系
    ten_god = calculate_ten_god(day_master, month_stem)
    
    # 计算基础分
    month_element = STEM_ELEMENTS.get(month_stem, '木')
    user_element = STEM_ELEMENTS.get(day_master, '木')
    relation = get_element_relation(user_element, month_element)
    base_score = ELEMENT_RELATION_SCORES.get(relation, 75)
    
    # 获取十神加成
    god_bonus = TEN_GOD_FORTUNE_BONUS.get(ten_god, {})
    
    # 月度种子
    month_seed = year * 100 + month
    
    # 计算各项运势
    career = clamp_score(base_score + god_bonus.get('career', 0) + seeded_random(month_seed, 1) * 8 - 4)
    love = clamp_score(base_score + god_bonus.get('love', 0) + seeded_random(month_seed, 2) * 8 - 4)
    wealth = clamp_score(base_score + god_bonus.get('wealth', 0) + seeded_random(month_seed, 3) * 8 - 4)
    health = clamp_score(base_score + god_bonus.get('health', 0) + seeded_random(month_seed, 4) * 8 - 4)
    social = clamp_score(base_score + god_bonus.get('social', 0) + seeded_random(month_seed, 5) * 8 - 4)
    overall = clamp_score((career + love + wealth + health + social) / 5)
    
    # 生成月度总结
    summary = generate_monthly_summary(ten_god, overall)
    
    # 生成重要日期
    key_dates = generate_key_dates(day_master, year, month)
    
    return MonthlyFortune(
        year=year,
        month=month,
        month_stem=month_stem,
        month_branch=month_branch,
        ten_god=ten_god,
        overall=overall,
        career=career,
        love=love,
        wealth=wealth,
        health=health,
        social=social,
        summary=summary,
        key_dates=key_dates,
    )


def calculate_generic_daily_fortune(target_date: date) -> Dict[str, Any]:
    """计算通用运势（无八字时使用）"""
    seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
    
    def random_score(offset: int) -> int:
        x = math.sin(seed + offset) * 10000
        return int((x - math.floor(x)) * 40) + 55
    
    overall = random_score(1)
    career = random_score(2)
    love = random_score(3)
    wealth = random_score(4)
    health = random_score(5)
    social = random_score(6)
    
    advice = []
    if overall >= 75:
        advice.append('整体运势良好，适合开展新计划')
    else:
        advice.append('今日宜稳健行事，不宜冒进')
    
    if career >= 70:
        advice.append('工作上有贵人相助，把握机会')
    else:
        advice.append('职场上需多加耐心，避免冲突')
    
    if wealth >= 70:
        advice.append('财运亨通，可适当投资')
    else:
        advice.append('守财为主，避免大额消费')
    
    if health >= 70:
        advice.append('精力充沛，适合运动健身')
    else:
        advice.append('注意休息，避免过度劳累')
    
    return {
        'date': target_date.strftime('%Y-%m-%d'),
        'overall': overall,
        'career': career,
        'love': love,
        'wealth': wealth,
        'health': health,
        'social': social,
        'advice': advice,
    }


def calculate_weekly_trend(day_master: str, center_date: date) -> List[Dict[str, Any]]:
    """计算周趋势数据"""
    from datetime import timedelta
    
    result = []
    for offset in range(-3, 4):
        target_date = center_date + timedelta(days=offset)
        fortune = calculate_daily_fortune(day_master, target_date)
        
        result.append({
            'date': f"{target_date.month}/{target_date.day}",
            'full_date': fortune.date,
            'day_of_month': target_date.day,
            'scores': {
                'overall': fortune.overall,
                'career': fortune.career,
                'love': fortune.love,
                'wealth': fortune.wealth,
                'health': fortune.health,
                'social': fortune.social,
            }
        })
    
    return result


def generate_key_dates(day_master: str, year: int, month: int) -> List[Dict[str, Any]]:
    """生成月度关键日期"""
    import calendar
    
    key_dates = []
    days_in_month = calendar.monthrange(year, month)[1]
    
    # 计算所有天的运势
    daily_scores = []
    for day in range(1, days_in_month + 1):
        target_date = date(year, month, day)
        fortune = calculate_daily_fortune(day_master, target_date)
        daily_scores.append({
            'day': day,
            'overall': fortune.overall,
            'career': fortune.career,
            'wealth': fortune.wealth,
            'love': fortune.love,
            'health': fortune.health,
            'social': fortune.social,
        })
    
    # 识别吉日
    for score in daily_scores:
        if len(key_dates) >= 8:
            break
        
        if score['overall'] >= 85:
            key_dates.append({'date': score['day'], 'desc': '大吉日', 'type': 'lucky'})
        elif score['wealth'] >= 88:
            key_dates.append({'date': score['day'], 'desc': '财运日', 'type': 'lucky'})
        elif score['career'] >= 88:
            key_dates.append({'date': score['day'], 'desc': '事业吉日', 'type': 'lucky'})
        elif score['love'] >= 88:
            key_dates.append({'date': score['day'], 'desc': '桃花日', 'type': 'lucky'})
    
    # 识别转折日
    for i in range(1, len(daily_scores) - 1):
        if len(key_dates) >= 10:
            break
        
        prev_score = daily_scores[i - 1]
        curr = daily_scores[i]
        next_score = daily_scores[i + 1]
        
        # 运势急剧上升
        if prev_score['overall'] < 65 and curr['overall'] < 65 and next_score['overall'] >= 75:
            if not any(k['date'] == next_score['day'] for k in key_dates):
                key_dates.append({'date': next_score['day'], 'desc': '转运日', 'type': 'turning'})
        
        # 运势急剧下降
        if prev_score['overall'] >= 75 and curr['overall'] >= 75 and next_score['overall'] < 65:
            if not any(k['date'] == next_score['day'] for k in key_dates):
                key_dates.append({'date': next_score['day'], 'desc': '需谨慎', 'type': 'warning'})
    
    key_dates.sort(key=lambda x: x['date'])
    return key_dates[:8]
