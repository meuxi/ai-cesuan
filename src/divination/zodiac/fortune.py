"""
星座运势
提供每日、每周、每月星座运势
"""

from typing import Dict, Any, List
from datetime import date, datetime
import math


def _seeded_random(seed: int, offset: int = 0) -> float:
    """基于种子的伪随机函数"""
    x = math.sin(seed + offset) * 10000
    return x - math.floor(x)


def _get_fortune_score(seed: int, offset: int) -> int:
    """获取运势分数 (50-98)"""
    return int(_seeded_random(seed, offset) * 48) + 50


def get_daily_zodiac_fortune(zodiac: str, target_date: date = None) -> Dict[str, Any]:
    """
    获取每日星座运势
    
    Args:
        zodiac: 星座名称
        target_date: 目标日期，默认今天
        
    Returns:
        每日运势数据
    """
    if target_date is None:
        target_date = date.today()
    
    # 生成种子
    zodiac_seed = hash(zodiac) % 10000
    date_seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
    seed = zodiac_seed + date_seed
    
    # 计算各项运势
    overall = _get_fortune_score(seed, 1)
    love = _get_fortune_score(seed, 2)
    career = _get_fortune_score(seed, 3)
    wealth = _get_fortune_score(seed, 4)
    health = _get_fortune_score(seed, 5)
    
    # 幸运数字和颜色
    lucky_numbers = [
        int(_seeded_random(seed, 10) * 9) + 1,
        int(_seeded_random(seed, 11) * 9) + 1,
        int(_seeded_random(seed, 12) * 9) + 1,
    ]
    
    colors = ['红色', '橙色', '黄色', '绿色', '蓝色', '紫色', '粉色', '白色', '黑色', '金色']
    lucky_color = colors[int(_seeded_random(seed, 20) * len(colors))]
    
    # 生成建议
    advice = _generate_daily_advice(overall, love, career, wealth, health)
    
    return {
        'zodiac': zodiac,
        'date': target_date.strftime('%Y-%m-%d'),
        'scores': {
            'overall': overall,
            'love': love,
            'career': career,
            'wealth': wealth,
            'health': health,
        },
        'lucky_number': lucky_numbers,
        'lucky_color': lucky_color,
        'advice': advice,
    }


def _generate_daily_advice(overall: int, love: int, career: int, wealth: int, health: int) -> List[str]:
    """生成每日建议"""
    advice = []
    
    if overall >= 80:
        advice.append('整体运势极佳，今天是大展身手的好日子！')
    elif overall >= 60:
        advice.append('整体运势平稳，按部就班即可。')
    else:
        advice.append('今日运势稍弱，建议低调行事。')
    
    if love >= 75:
        advice.append('感情运旺盛，适合表达心意。')
    elif love < 55:
        advice.append('感情上需要多一些耐心和包容。')
    
    if career >= 75:
        advice.append('事业运强劲，把握机会展现实力。')
    elif career < 55:
        advice.append('工作上可能遇到小挑战，保持冷静。')
    
    if wealth >= 75:
        advice.append('财运亨通，可适当投资理财。')
    elif wealth < 55:
        advice.append('财务方面宜保守，避免大额消费。')
    
    if health < 60:
        advice.append('注意休息，避免过度劳累。')
    
    return advice[:4]


def get_weekly_zodiac_fortune(zodiac: str, year: int, week: int) -> Dict[str, Any]:
    """
    获取每周星座运势
    
    Args:
        zodiac: 星座名称
        year: 年份
        week: 周数 (1-53)
        
    Returns:
        每周运势数据
    """
    zodiac_seed = hash(zodiac) % 10000
    week_seed = year * 100 + week
    seed = zodiac_seed + week_seed
    
    # 计算各项运势
    overall = _get_fortune_score(seed, 1)
    love = _get_fortune_score(seed, 2)
    career = _get_fortune_score(seed, 3)
    wealth = _get_fortune_score(seed, 4)
    health = _get_fortune_score(seed, 5)
    
    # 本周关键日
    key_days = []
    for i in range(7):
        day_score = _get_fortune_score(seed + i * 100, 1)
        if day_score >= 80:
            key_days.append({'day': i + 1, 'type': 'lucky', 'desc': '吉日'})
        elif day_score < 55:
            key_days.append({'day': i + 1, 'type': 'caution', 'desc': '需谨慎'})
    
    # 生成周运总结
    summary = _generate_weekly_summary(overall, love, career, wealth)
    
    return {
        'zodiac': zodiac,
        'year': year,
        'week': week,
        'scores': {
            'overall': overall,
            'love': love,
            'career': career,
            'wealth': wealth,
            'health': health,
        },
        'key_days': key_days[:3],
        'summary': summary,
    }


def _generate_weekly_summary(overall: int, love: int, career: int, wealth: int) -> str:
    """生成周运总结"""
    parts = []
    
    if overall >= 75:
        parts.append('本周整体运势良好')
    elif overall >= 60:
        parts.append('本周运势平稳')
    else:
        parts.append('本周运势偏低')
    
    # 找出最强和最弱的领域
    scores = {'感情': love, '事业': career, '财运': wealth}
    best = max(scores, key=scores.get)
    worst = min(scores, key=scores.get)
    
    if scores[best] >= 70:
        parts.append(f'，{best}方面表现突出')
    
    if scores[worst] < 60:
        parts.append(f'，{worst}方面需要多加注意')
    
    parts.append('。')
    
    return ''.join(parts)


def get_monthly_zodiac_fortune(zodiac: str, year: int, month: int) -> Dict[str, Any]:
    """
    获取每月星座运势
    
    Args:
        zodiac: 星座名称
        year: 年份
        month: 月份 (1-12)
        
    Returns:
        每月运势数据
    """
    zodiac_seed = hash(zodiac) % 10000
    month_seed = year * 100 + month
    seed = zodiac_seed + month_seed
    
    # 计算各项运势
    overall = _get_fortune_score(seed, 1)
    love = _get_fortune_score(seed, 2)
    career = _get_fortune_score(seed, 3)
    wealth = _get_fortune_score(seed, 4)
    health = _get_fortune_score(seed, 5)
    
    # 本月关键日期
    import calendar
    days_in_month = calendar.monthrange(year, month)[1]
    key_dates = []
    
    for day in range(1, days_in_month + 1):
        day_seed = seed + day * 1000
        day_score = _get_fortune_score(day_seed, 1)
        if day_score >= 85:
            key_dates.append({'date': day, 'type': 'best', 'desc': '大吉日'})
        elif day_score >= 80:
            key_dates.append({'date': day, 'type': 'lucky', 'desc': '吉日'})
    
    # 生成月运分析
    analysis = _generate_monthly_analysis(zodiac, overall, love, career, wealth, health)
    
    return {
        'zodiac': zodiac,
        'year': year,
        'month': month,
        'scores': {
            'overall': overall,
            'love': love,
            'career': career,
            'wealth': wealth,
            'health': health,
        },
        'key_dates': key_dates[:5],
        'analysis': analysis,
    }


def _generate_monthly_analysis(
    zodiac: str, overall: int, love: int, 
    career: int, wealth: int, health: int
) -> Dict[str, str]:
    """生成月运分析"""
    return {
        'overall': f'{zodiac}本月整体运势{"旺盛" if overall >= 75 else "平稳" if overall >= 60 else "需要调整"}，把握时机积极行动。',
        'love': '感情方面' + ('桃花运旺，单身者有望遇到心仪对象。' if love >= 75 else '稳步发展，需要多一些耐心经营。' if love >= 60 else '可能遇到一些小波折，保持沟通很重要。'),
        'career': '事业方面' + ('有望取得突破，是展现实力的好时机。' if career >= 75 else '按部就班发展，注重积累。' if career >= 60 else '可能面临挑战，保持冷静应对。'),
        'wealth': '财运方面' + ('收入有望增加，可考虑投资理财。' if wealth >= 75 else '收支平衡，理性消费为宜。' if wealth >= 60 else '需要控制开支，避免冲动消费。'),
        'health': '健康方面' + ('精力充沛，适合增加运动量。' if health >= 70 else '需要注意休息，避免过度劳累。'),
    }
