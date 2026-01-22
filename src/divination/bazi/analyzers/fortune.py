"""
运势计算模块
基于八字命理理论，通过日主与流日/流月的五行生克关系计算个性化运势

数据来源：MingAI fortune.ts
"""
from typing import TypedDict, List, Literal, Optional
from datetime import date
import math


# 类型定义
FiveElement = Literal['木', '火', '土', '金', '水']
HeavenlyStem = Literal['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']


class FortuneScores(TypedDict):
    """运势分数"""
    overall: int    # 综合运势 (0-100)
    career: int     # 事业运
    love: int       # 感情运
    wealth: int     # 财运
    health: int     # 健康运
    social: int     # 人际运


class DailyFortune(FortuneScores):
    """每日运势"""
    date: str
    day_stem: HeavenlyStem
    day_branch: str
    ten_god: str     # 流日与日主形成的十神
    advice: List[str]   # 运势建议
    lucky_color: str    # 幸运色
    lucky_direction: str  # 吉方位


class KeyDate(TypedDict):
    """关键日期"""
    date: int
    desc: str
    type: Optional[Literal['lucky', 'warning', 'turning']]


class MonthlyFortune(FortuneScores):
    """月度运势"""
    year: int
    month: int
    month_stem: HeavenlyStem
    month_branch: str
    ten_god: str
    summary: str
    key_dates: List[KeyDate]


# 天干五行映射
STEM_ELEMENTS: dict[HeavenlyStem, FiveElement] = {
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
ELEMENT_COLORS: dict[FiveElement, str] = {
    '木': '绿色',
    '火': '红色',
    '土': '黄色',
    '金': '白色',
    '水': '黑色/蓝色',
}

# 五行对应方位
ELEMENT_DIRECTIONS: dict[FiveElement, str] = {
    '木': '东方',
    '火': '南方',
    '土': '中央',
    '金': '西方',
    '水': '北方',
}

# 五行相生顺序
WUXING_ORDER: list[FiveElement] = ['木', '火', '土', '金', '水']


def get_stem_yin_yang(stem: HeavenlyStem) -> Literal['yang', 'yin']:
    """获取天干阴阳"""
    yang_stems = ['甲', '丙', '戊', '庚', '壬']
    return 'yang' if stem in yang_stems else 'yin'


def get_element_relation(from_elem: FiveElement, to_elem: FiveElement) -> str:
    """获取五行生克关系"""
    from_idx = WUXING_ORDER.index(from_elem)
    to_idx = WUXING_ORDER.index(to_elem)
    
    if from_elem == to_elem:
        return 'same'
    if (from_idx + 1) % 5 == to_idx:
        return 'produce'
    if (to_idx + 1) % 5 == from_idx:
        return 'produced'
    if (from_idx + 2) % 5 == to_idx:
        return 'control'
    return 'controlled'


def calculate_ten_god(day_stem: HeavenlyStem, target_stem: HeavenlyStem) -> str:
    """计算十神"""
    if day_stem == target_stem:
        return '比肩'
    
    day_element = STEM_ELEMENTS[day_stem]
    target_element = STEM_ELEMENTS[target_stem]
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


def get_lucky_element(user_element: FiveElement) -> FiveElement:
    """获取幸运五行（生日主的五行）"""
    sheng_map = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
    return sheng_map[user_element]


def generate_daily_advice(ten_god: str, overall: int, career: int, wealth: int, health: int) -> List[str]:
    """生成每日运势建议"""
    advice = []
    
    # 根据十神给出建议
    ten_god_advice = {
        '比肩': '今日适合与朋友合作，团队协作会有好的效果。',
        '劫财': '今日要注意财务支出，不宜进行大额投资。',
        '食神': '今日灵感丰富，适合创作和表达。',
        '伤官': '今日思维敏捷但容易冲动，需要控制情绪。',
        '偏财': '今日有意外收获的机会，可以尝试新领域。',
        '正财': '今日工作稳定，适合处理财务事务。',
        '七杀': '今日压力较大，但也是突破的好时机。',
        '正官': '今日适合处理公务，有升职或获奖的机会。',
        '偏印': '今日适合学习新知识，独处思考。',
        '正印': '今日贵人运旺，可多向长辈请教。',
    }
    advice.append(ten_god_advice.get(ten_god, '保持平常心，顺势而为。'))
    
    # 根据综合运势
    if overall >= 85:
        advice.append('今日整体运势极佳，把握机会大胆行动。')
    elif overall >= 70:
        advice.append('今日运势良好，适合推进重要事项。')
    elif overall >= 55:
        advice.append('今日运势平稳，按部就班即可。')
    else:
        advice.append('今日宜低调行事，避免冲突。')
    
    # 根据各项运势
    if career >= 80:
        advice.append('事业运旺，适合谈判和签约。')
    if wealth >= 80:
        advice.append('财运佳，可考虑投资理财。')
    if health < 60:
        advice.append('注意休息，避免过度劳累。')
    
    return advice


def generate_monthly_summary(ten_god: str, overall: int) -> str:
    """生成月度总结"""
    ten_god_summary = {
        '比肩': '本月人际关系活跃，适合拓展社交圈。',
        '劫财': '本月注意理财，避免借贷和担保。',
        '食神': '本月创造力旺盛，艺术表演类活动顺利。',
        '伤官': '本月思维活跃但易生是非，言行需谨慎。',
        '偏财': '本月有偏财运，意外收获可期。',
        '正财': '本月正财稳定，工资奖金有保障。',
        '七杀': '本月压力与机遇并存，勇于挑战可突破。',
        '正官': '本月事业运佳，升职加薪有望。',
        '偏印': '本月适合学习进修，考试运不错。',
        '正印': '本月贵人相助，遇事可寻求帮助。',
    }
    
    base = ten_god_summary.get(ten_god, '本月运势平稳。')
    
    if overall >= 80:
        return base + '整体运势上佳，可积极进取。'
    elif overall >= 65:
        return base + '整体运势良好，按计划行事即可。'
    else:
        return base + '整体运势一般，宜守不宜攻。'


def calculate_daily_fortune(day_master: HeavenlyStem, target_date: date) -> DailyFortune:
    """
    计算每日个性化运势
    
    Args:
        day_master: 用户日主天干
        target_date: 目标日期
        
    Returns:
        每日运势
    """
    # 简化的日干支计算（实际应使用农历库）
    # 这里用简化算法示意
    day_index = (target_date.year * 365 + target_date.month * 30 + target_date.day) % 10
    day_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    day_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    day_stem = day_stems[day_index]
    day_branch = day_branches[(day_index * 2) % 12]
    
    # 计算十神
    ten_god = calculate_ten_god(day_master, day_stem)
    
    # 计算基础分
    day_element = STEM_ELEMENTS[day_stem]
    user_element = STEM_ELEMENTS[day_master]
    relation = get_element_relation(user_element, day_element)
    base_score = ELEMENT_RELATION_SCORES[relation]
    
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
    
    # 生成建议
    advice = generate_daily_advice(ten_god, overall, career, wealth, health)
    
    # 幸运色和方位
    lucky_element = get_lucky_element(user_element)
    lucky_color = ELEMENT_COLORS[lucky_element]
    lucky_direction = ELEMENT_DIRECTIONS[lucky_element]
    
    return {
        'date': target_date.strftime('%Y-%m-%d'),
        'day_stem': day_stem,
        'day_branch': day_branch,
        'ten_god': ten_god,
        'overall': overall,
        'career': career,
        'love': love,
        'wealth': wealth,
        'health': health,
        'social': social,
        'advice': advice,
        'lucky_color': lucky_color,
        'lucky_direction': lucky_direction,
    }


def calculate_generic_fortune(target_date: date) -> FortuneScores:
    """
    计算通用运势（无八字时使用）
    """
    seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
    
    def random_score(offset: int) -> int:
        x = math.sin(seed + offset) * 10000
        return int((x - math.floor(x)) * 40) + 55
    
    return {
        'overall': random_score(1),
        'career': random_score(2),
        'love': random_score(3),
        'wealth': random_score(4),
        'health': random_score(5),
        'social': random_score(6),
    }
