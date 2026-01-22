"""
塔罗牌小阿尔卡那数据
包含56张小阿尔卡那牌（权杖、圣杯、宝剑、星币各14张）
"""

from typing import List
from .cards import TarotCard, CardSuit


def _create_minor_cards(suit: CardSuit, suit_name: str, suit_en: str, element: str) -> List[TarotCard]:
    """创建某一牌组的所有牌"""
    
    # 数字牌含义模板
    NUMBER_MEANINGS = {
        1: {
            "keywords": ["新开始", "潜力", "机会"],
            "upright": "新的开始，原始能量，潜力无限",
            "reversed": "错失机会，延迟，缺乏方向",
        },
        2: {
            "keywords": ["平衡", "选择", "合作"],
            "upright": "平衡，伙伴关系，需要做出选择",
            "reversed": "失衡，冲突，优柔寡断",
        },
        3: {
            "keywords": ["成长", "创造", "团队"],
            "upright": "成长，创造力，团队合作",
            "reversed": "缺乏进展，创意受阻，不合作",
        },
        4: {
            "keywords": ["稳定", "基础", "休息"],
            "upright": "稳定，基础牢固，庆祝成果",
            "reversed": "不稳定，缺乏安全感，停滞",
        },
        5: {
            "keywords": ["冲突", "挑战", "变化"],
            "upright": "冲突，竞争，困难挑战",
            "reversed": "避免冲突，内在挣扎，和解",
        },
        6: {
            "keywords": ["和谐", "平衡", "给予"],
            "upright": "和谐，慷慨，平衡状态",
            "reversed": "不平等，自私，债务",
        },
        7: {
            "keywords": ["评估", "耐心", "坚持"],
            "upright": "评估进展，耐心等待，长期投资",
            "reversed": "缺乏耐心，回报延迟，挫败感",
        },
        8: {
            "keywords": ["行动", "速度", "掌控"],
            "upright": "快速行动，专注努力，接近目标",
            "reversed": "匆忙，混乱，缺乏方向",
        },
        9: {
            "keywords": ["接近完成", "自给自足", "成就"],
            "upright": "接近完成，独立自主，满足感",
            "reversed": "不完整，依赖他人，失落",
        },
        10: {
            "keywords": ["完成", "圆满", "过度"],
            "upright": "完成周期，圆满，达成目标",
            "reversed": "过度负担，无法完成，崩溃",
        },
    }
    
    # 宫廷牌含义
    COURT_MEANINGS = {
        "侍从": {
            "keywords": ["学习", "好奇", "消息"],
            "upright": "年轻的能量，学习新事物，带来消息",
            "reversed": "不成熟，缺乏经验，坏消息",
        },
        "骑士": {
            "keywords": ["行动", "追求", "冒险"],
            "upright": "积极行动，追求目标，充满热情",
            "reversed": "鲁莽，冲动，缺乏方向",
        },
        "王后": {
            "keywords": ["滋养", "直觉", "成熟"],
            "upright": "滋养能量，情感成熟，直觉敏锐",
            "reversed": "情绪化，依赖，内在不安",
        },
        "国王": {
            "keywords": ["掌控", "权威", "成就"],
            "upright": "掌控局面，领导能力，成功人士",
            "reversed": "专横，滥用权力，缺乏控制",
        },
    }
    
    # 牌组特定含义
    SUIT_THEMES = {
        CardSuit.WANDS: {
            "theme": "行动、创造、激情",
            "area": "事业、创意、冒险",
        },
        CardSuit.CUPS: {
            "theme": "情感、关系、直觉",
            "area": "感情、友情、内心",
        },
        CardSuit.SWORDS: {
            "theme": "思维、沟通、冲突",
            "area": "决策、真相、挑战",
        },
        CardSuit.PENTACLES: {
            "theme": "物质、财富、实际",
            "area": "金钱、工作、健康",
        },
    }
    
    cards = []
    theme = SUIT_THEMES[suit]
    
    # 数字牌 (Ace - 10)
    number_names = ["王牌", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    number_names_en = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    
    for i in range(1, 11):
        meaning = NUMBER_MEANINGS[i]
        cards.append(TarotCard(
            code=f"{suit.value.upper()}_{i:02d}",
            name=f"{suit_name}{number_names[i-1]}",
            name_en=f"{number_names_en[i-1]} of {suit_en}",
            number=i,
            suit=suit,
            element=element,
            keywords=meaning["keywords"] + [theme["theme"].split("、")[0]],
            upright_meaning=f"{meaning['upright']}。在{theme['area']}领域表现明显。",
            reversed_meaning=f"{meaning['reversed']}。{theme['area']}方面可能遇到阻碍。",
            image_desc=f"{suit_name}牌组第{i}张，象征{theme['theme']}中的{meaning['keywords'][0]}",
            advice=f"关注{theme['area']}领域的发展",
        ))
    
    # 宫廷牌 (侍从、骑士、王后、国王)
    court_names = ["侍从", "骑士", "王后", "国王"]
    court_names_en = ["Page", "Knight", "Queen", "King"]
    
    for i, (cn, en) in enumerate(zip(court_names, court_names_en)):
        meaning = COURT_MEANINGS[cn]
        cards.append(TarotCard(
            code=f"{suit.value.upper()}_{en.upper()}",
            name=f"{suit_name}{cn}",
            name_en=f"{en} of {suit_en}",
            number=11 + i,
            suit=suit,
            element=element,
            keywords=meaning["keywords"] + [theme["theme"].split("、")[0]],
            upright_meaning=f"{meaning['upright']}。代表在{theme['area']}领域的{cn}特质。",
            reversed_meaning=f"{meaning['reversed']}。在{theme['area']}方面需要注意。",
            image_desc=f"{suit_name}{cn}，象征{theme['theme']}中的{cn}角色",
            advice=f"发挥{cn}在{theme['area']}领域的特质",
        ))
    
    return cards


# 权杖牌组 (火元素 - 行动、创造、激情)
WANDS: List[TarotCard] = _create_minor_cards(CardSuit.WANDS, "权杖", "Wands", "火")

# 圣杯牌组 (水元素 - 情感、关系、直觉)
CUPS: List[TarotCard] = _create_minor_cards(CardSuit.CUPS, "圣杯", "Cups", "水")

# 宝剑牌组 (风元素 - 思维、沟通、冲突)
SWORDS: List[TarotCard] = _create_minor_cards(CardSuit.SWORDS, "宝剑", "Swords", "风")

# 星币牌组 (土元素 - 物质、财富、实际)
PENTACLES: List[TarotCard] = _create_minor_cards(CardSuit.PENTACLES, "星币", "Pentacles", "土")

# 所有小阿尔卡那
MINOR_ARCANA: List[TarotCard] = WANDS + CUPS + SWORDS + PENTACLES


def get_all_minor_arcana() -> List[TarotCard]:
    """获取所有小阿尔卡那牌"""
    return MINOR_ARCANA


def get_cards_by_suit(suit: CardSuit) -> List[TarotCard]:
    """按牌组获取牌"""
    suit_map = {
        CardSuit.WANDS: WANDS,
        CardSuit.CUPS: CUPS,
        CardSuit.SWORDS: SWORDS,
        CardSuit.PENTACLES: PENTACLES,
    }
    return suit_map.get(suit, [])


def get_minor_card_by_code(code: str) -> TarotCard | None:
    """根据代码获取小阿尔卡那牌"""
    for card in MINOR_ARCANA:
        if card.code == code:
            return card
    return None
