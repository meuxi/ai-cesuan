"""
塔罗牌阵配置
17种常用塔罗牌阵的完整定义

数据来源：全新AI占卜系统 前端/src/data/Tarot.ts
"""
from typing import List, TypedDict


class SpreadPosition(TypedDict):
    """牌阵位置定义"""
    index: int          # 位置索引
    name: str          # 位置名称
    meaning: str       # 位置含义


class TarotSpread(TypedDict):
    """塔罗牌阵定义"""
    id: str            # 牌阵ID
    name: str          # 牌阵名称
    name_en: str       # 英文名
    card_count: int    # 牌数
    category: str      # 分类
    description: str   # 描述
    positions: List[SpreadPosition]  # 位置列表


# 17种塔罗牌阵配置
TAROT_SPREADS: List[TarotSpread] = [
    # 1. 单卡占卜
    {
        'id': 'single',
        'name': '单卡占卜',
        'name_en': 'Single Card',
        'card_count': 1,
        'category': '基础',
        'description': '最简单的占卜方式，抽取一张牌来获得当下问题的直接答案或每日指引',
        'positions': [
            {'index': 0, 'name': '核心', 'meaning': '问题的核心答案或当日指引'},
        ],
    },
    # 2. 三张牌占卜法
    {
        'id': 'three_card',
        'name': '三张牌占卜法',
        'name_en': 'Three Card Spread',
        'card_count': 3,
        'category': '基础',
        'description': '经典的过去-现在-未来牌阵，揭示事件的发展脉络',
        'positions': [
            {'index': 0, 'name': '过去', 'meaning': '影响当前局面的过去因素'},
            {'index': 1, 'name': '现在', 'meaning': '当前的状态和处境'},
            {'index': 2, 'name': '未来', 'meaning': '如果保持现状，可能的发展方向'},
        ],
    },
    # 3. 时间流牌阵
    {
        'id': 'time_flow',
        'name': '时间流牌阵',
        'name_en': 'Time Flow Spread',
        'card_count': 3,
        'category': '时间',
        'description': '以时间维度解读问题，展现事件的演变过程',
        'positions': [
            {'index': 0, 'name': '起因', 'meaning': '事情的起因和根源'},
            {'index': 1, 'name': '经过', 'meaning': '目前正在经历的过程'},
            {'index': 2, 'name': '结果', 'meaning': '最终可能的结果'},
        ],
    },
    # 4. 圣三角牌阵
    {
        'id': 'holy_triangle',
        'name': '圣三角牌阵',
        'name_en': 'Holy Triangle Spread',
        'card_count': 3,
        'category': '决策',
        'description': '从身心灵三个层面分析问题',
        'positions': [
            {'index': 0, 'name': '身体/物质', 'meaning': '物质层面的状态和需求'},
            {'index': 1, 'name': '心理/情感', 'meaning': '情感和心理层面的状态'},
            {'index': 2, 'name': '灵性/精神', 'meaning': '精神层面的指引'},
        ],
    },
    # 5. 四元素牌阵
    {
        'id': 'four_elements',
        'name': '四元素牌阵',
        'name_en': 'Four Elements Spread',
        'card_count': 4,
        'category': '分析',
        'description': '从火(行动)、水(情感)、风(思想)、土(物质)四个元素分析问题',
        'positions': [
            {'index': 0, 'name': '火元素', 'meaning': '行动力、激情、动力'},
            {'index': 1, 'name': '水元素', 'meaning': '情感、直觉、感受'},
            {'index': 2, 'name': '风元素', 'meaning': '思想、沟通、计划'},
            {'index': 3, 'name': '土元素', 'meaning': '物质、实际、稳定'},
        ],
    },
    # 6. 恋人金字塔
    {
        'id': 'lover_pyramid',
        'name': '恋人金字塔',
        'name_en': 'Lover Pyramid Spread',
        'card_count': 4,
        'category': '爱情',
        'description': '分析双方在关系中的状态和互动',
        'positions': [
            {'index': 0, 'name': '你的状态', 'meaning': '你在这段关系中的状态'},
            {'index': 1, 'name': '对方状态', 'meaning': '对方在这段关系中的状态'},
            {'index': 2, 'name': '关系现状', 'meaning': '你们之间关系的现状'},
            {'index': 3, 'name': '发展建议', 'meaning': '关系发展的建议'},
        ],
    },
    # 7. 爱情大十字
    {
        'id': 'love_cross',
        'name': '爱情大十字',
        'name_en': 'Love Cross Spread',
        'card_count': 5,
        'category': '爱情',
        'description': '全面分析感情状况，包括过去、现在、障碍、建议和结果',
        'positions': [
            {'index': 0, 'name': '过去', 'meaning': '影响感情的过去因素'},
            {'index': 1, 'name': '现在', 'meaning': '当前感情状态'},
            {'index': 2, 'name': '障碍', 'meaning': '感情中的障碍和挑战'},
            {'index': 3, 'name': '建议', 'meaning': '处理感情的建议'},
            {'index': 4, 'name': '结果', 'meaning': '感情的可能结果'},
        ],
    },
    # 8. 寻找对象牌阵
    {
        'id': 'find_partner',
        'name': '寻找对象牌阵',
        'name_en': 'Finding Partner Spread',
        'card_count': 5,
        'category': '爱情',
        'description': '帮助单身者了解自己的感情状态和寻找对象的方向',
        'positions': [
            {'index': 0, 'name': '自我状态', 'meaning': '你当前的感情状态'},
            {'index': 1, 'name': '需要什么', 'meaning': '你在感情中需要什么'},
            {'index': 2, 'name': '障碍', 'meaning': '阻碍你找到对象的因素'},
            {'index': 3, 'name': '建议', 'meaning': '寻找对象的建议'},
            {'index': 4, 'name': '机遇', 'meaning': '可能的感情机遇'},
        ],
    },
    # 9. 爱情树牌阵
    {
        'id': 'love_tree',
        'name': '爱情树牌阵',
        'name_en': 'Love Tree Spread',
        'card_count': 5,
        'category': '爱情',
        'description': '像树一样展现爱情的根基、成长和果实',
        'positions': [
            {'index': 0, 'name': '根基', 'meaning': '感情的基础和根源'},
            {'index': 1, 'name': '树干', 'meaning': '感情的支柱和核心'},
            {'index': 2, 'name': '左枝', 'meaning': '你的付出和贡献'},
            {'index': 3, 'name': '右枝', 'meaning': '对方的付出和贡献'},
            {'index': 4, 'name': '果实', 'meaning': '感情的收获和结果'},
        ],
    },
    # 10. 吉普赛牌阵
    {
        'id': 'gypsy',
        'name': '吉普赛牌阵',
        'name_en': 'Gypsy Spread',
        'card_count': 5,
        'category': '综合',
        'description': '传统的吉普赛占卜法，全面分析问题',
        'positions': [
            {'index': 0, 'name': '问题核心', 'meaning': '问题的核心所在'},
            {'index': 1, 'name': '有利因素', 'meaning': '对你有利的因素'},
            {'index': 2, 'name': '不利因素', 'meaning': '对你不利的因素'},
            {'index': 3, 'name': '环境影响', 'meaning': '周围环境的影响'},
            {'index': 4, 'name': '最终结果', 'meaning': '事情的最终结果'},
        ],
    },
    # 11. 二选一牌阵
    {
        'id': 'choice',
        'name': '二选一牌阵',
        'name_en': 'Choice Spread',
        'card_count': 5,
        'category': '决策',
        'description': '帮助在两个选择之间做出决定',
        'positions': [
            {'index': 0, 'name': '当前状态', 'meaning': '你目前的处境'},
            {'index': 1, 'name': '选择A', 'meaning': '第一个选择的走向'},
            {'index': 2, 'name': '选择B', 'meaning': '第二个选择的走向'},
            {'index': 3, 'name': 'A的结果', 'meaning': '选择A的可能结果'},
            {'index': 4, 'name': 'B的结果', 'meaning': '选择B的可能结果'},
        ],
    },
    # 12. 财富之数
    {
        'id': 'wealth',
        'name': '财富之数',
        'name_en': 'Wealth Spread',
        'card_count': 5,
        'category': '事业财运',
        'description': '分析财运状况和理财建议',
        'positions': [
            {'index': 0, 'name': '财运现状', 'meaning': '当前的财务状况'},
            {'index': 1, 'name': '收入来源', 'meaning': '主要的收入来源'},
            {'index': 2, 'name': '支出问题', 'meaning': '需要注意的支出问题'},
            {'index': 3, 'name': '理财建议', 'meaning': '理财方面的建议'},
            {'index': 4, 'name': '财运展望', 'meaning': '未来的财运展望'},
        ],
    },
    # 13. 维纳斯牌阵
    {
        'id': 'venus',
        'name': '维纳斯牌阵',
        'name_en': 'Venus Spread',
        'card_count': 8,
        'category': '爱情',
        'description': '以爱神维纳斯命名，深入分析爱情的各个方面',
        'positions': [
            {'index': 0, 'name': '核心问题', 'meaning': '感情中的核心问题'},
            {'index': 1, 'name': '你的感受', 'meaning': '你的真实感受'},
            {'index': 2, 'name': '对方感受', 'meaning': '对方的真实感受'},
            {'index': 3, 'name': '关系优势', 'meaning': '关系中的优势'},
            {'index': 4, 'name': '关系劣势', 'meaning': '关系中的劣势'},
            {'index': 5, 'name': '外在影响', 'meaning': '外部因素的影响'},
            {'index': 6, 'name': '行动建议', 'meaning': '应该采取的行动'},
            {'index': 7, 'name': '最终结果', 'meaning': '感情的最终走向'},
        ],
    },
    # 14. 周运势牌阵
    {
        'id': 'weekly',
        'name': '周运势牌阵',
        'name_en': 'Weekly Spread',
        'card_count': 7,
        'category': '时间',
        'description': '预测一周七天的运势',
        'positions': [
            {'index': 0, 'name': '周一', 'meaning': '周一的运势和提醒'},
            {'index': 1, 'name': '周二', 'meaning': '周二的运势和提醒'},
            {'index': 2, 'name': '周三', 'meaning': '周三的运势和提醒'},
            {'index': 3, 'name': '周四', 'meaning': '周四的运势和提醒'},
            {'index': 4, 'name': '周五', 'meaning': '周五的运势和提醒'},
            {'index': 5, 'name': '周六', 'meaning': '周六的运势和提醒'},
            {'index': 6, 'name': '周日', 'meaning': '周日的运势和提醒'},
        ],
    },
    # 15. 六芒星牌阵
    {
        'id': 'hexagram',
        'name': '六芒星牌阵',
        'name_en': 'Hexagram Spread',
        'card_count': 7,
        'category': '综合',
        'description': '经典的六芒星牌阵，全面分析问题的各个层面',
        'positions': [
            {'index': 0, 'name': '过去', 'meaning': '过去的影响'},
            {'index': 1, 'name': '现在', 'meaning': '当前的状态'},
            {'index': 2, 'name': '未来', 'meaning': '未来的趋势'},
            {'index': 3, 'name': '环境', 'meaning': '周围环境的影响'},
            {'index': 4, 'name': '障碍', 'meaning': '面临的障碍'},
            {'index': 5, 'name': '建议', 'meaning': '行动建议'},
            {'index': 6, 'name': '结果', 'meaning': '最终结果'},
        ],
    },
    # 16. 情人复合牌阵
    {
        'id': 'reunion',
        'name': '情人复合牌阵',
        'name_en': 'Reunion Spread',
        'card_count': 9,
        'category': '爱情',
        'description': '分析与前任复合的可能性和建议',
        'positions': [
            {'index': 0, 'name': '分手原因', 'meaning': '导致分手的根本原因'},
            {'index': 1, 'name': '你的现状', 'meaning': '你目前的感情状态'},
            {'index': 2, 'name': '对方现状', 'meaning': '对方目前的感情状态'},
            {'index': 3, 'name': '你的想法', 'meaning': '你对复合的真实想法'},
            {'index': 4, 'name': '对方想法', 'meaning': '对方对复合的想法'},
            {'index': 5, 'name': '复合障碍', 'meaning': '复合面临的障碍'},
            {'index': 6, 'name': '复合优势', 'meaning': '复合的有利条件'},
            {'index': 7, 'name': '行动建议', 'meaning': '应该如何行动'},
            {'index': 8, 'name': '最终结果', 'meaning': '复合的可能性'},
        ],
    },
    # 17. 别人的爱
    {
        'id': 'others_love',
        'name': '别人的爱',
        'name_en': 'Others Love Spread',
        'card_count': 14,
        'category': '爱情',
        'description': '深入分析他人对你的感情，了解对方的真实想法',
        'positions': [
            {'index': 0, 'name': '对方对你的第一印象', 'meaning': '对方初见你时的印象'},
            {'index': 1, 'name': '对方现在怎么看你', 'meaning': '对方目前对你的看法'},
            {'index': 2, 'name': '对方喜欢你什么', 'meaning': '对方欣赏你的地方'},
            {'index': 3, 'name': '对方不喜欢你什么', 'meaning': '对方不欣赏你的地方'},
            {'index': 4, 'name': '对方的真实感受', 'meaning': '对方内心的真实感受'},
            {'index': 5, 'name': '对方的期望', 'meaning': '对方对你们关系的期望'},
            {'index': 6, 'name': '对方的担忧', 'meaning': '对方对你们关系的担忧'},
            {'index': 7, 'name': '你们的过去', 'meaning': '你们过去的互动如何影响现在'},
            {'index': 8, 'name': '当前的挑战', 'meaning': '你们目前面临的挑战'},
            {'index': 9, 'name': '外部影响', 'meaning': '外部因素对你们的影响'},
            {'index': 10, 'name': '对方的行动', 'meaning': '对方可能采取的行动'},
            {'index': 11, 'name': '你的行动建议', 'meaning': '你应该如何回应'},
            {'index': 12, 'name': '短期发展', 'meaning': '近期的发展趋势'},
            {'index': 13, 'name': '长期结果', 'meaning': '长远来看的结果'},
        ],
    },
]


# 牌阵分类
SPREAD_CATEGORIES = {
    '基础': ['single', 'three_card'],
    '时间': ['time_flow', 'weekly'],
    '决策': ['holy_triangle', 'choice'],
    '分析': ['four_elements'],
    '爱情': ['lover_pyramid', 'love_cross', 'find_partner', 'love_tree', 'venus', 'reunion', 'others_love'],
    '综合': ['gypsy', 'hexagram'],
    '事业财运': ['wealth'],
}


def get_spread_by_id(spread_id: str) -> TarotSpread | None:
    """根据ID获取牌阵"""
    for spread in TAROT_SPREADS:
        if spread['id'] == spread_id:
            return spread
    return None


def get_spreads_by_category(category: str) -> List[TarotSpread]:
    """获取指定分类的所有牌阵"""
    ids = SPREAD_CATEGORIES.get(category, [])
    return [s for s in TAROT_SPREADS if s['id'] in ids]


def get_all_spread_names() -> List[str]:
    """获取所有牌阵名称"""
    return [s['name'] for s in TAROT_SPREADS]


# 导出
__all__ = [
    'TarotSpread',
    'SpreadPosition',
    'TAROT_SPREADS',
    'SPREAD_CATEGORIES',
    'get_spread_by_id',
    'get_spreads_by_category',
    'get_all_spread_names',
]
