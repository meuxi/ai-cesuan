"""
塔罗牌数据模块
包含78张韦特塔罗牌的完整数据
参考 tarot-ai-agent 项目设计
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class CardSuit(Enum):
    """牌组类型"""
    MAJOR = "major"      # 大阿尔卡那
    WANDS = "wands"      # 权杖
    CUPS = "cups"        # 圣杯
    SWORDS = "swords"    # 宝剑
    PENTACLES = "pentacles"  # 星币


@dataclass
class TarotCard:
    """塔罗牌数据"""
    code: str                    # 牌代码
    name: str                    # 中文名
    name_en: str                 # 英文名
    number: int                  # 编号
    suit: CardSuit               # 牌组
    element: str                 # 元素
    keywords: List[str]          # 关键词
    upright_meaning: str         # 正位含义
    reversed_meaning: str        # 逆位含义
    image_desc: str              # 牌面描述
    advice: str                  # 建议


# 22张大阿尔卡那
MAJOR_ARCANA: List[TarotCard] = [
    TarotCard(
        code="FOOL",
        name="愚者",
        name_en="The Fool",
        number=0,
        suit=CardSuit.MAJOR,
        element="风",
        keywords=["新开始", "冒险", "天真", "自由", "可能性"],
        upright_meaning="新的旅程即将开始，怀着纯真的心态迈出第一步。代表无限可能、自由精神和对未知的勇敢探索。",
        reversed_meaning="鲁莽行事、缺乏计划、不负责任。可能正在逃避现实或做出轻率的决定。",
        image_desc="一位年轻人站在悬崖边，仰望天空，脚下是深渊，手持白玫瑰，身边有一只小狗。",
        advice="保持开放的心态，勇敢迈出第一步，但也要注意脚下的路。"
    ),
    TarotCard(
        code="MAGICIAN",
        name="魔术师",
        name_en="The Magician",
        number=1,
        suit=CardSuit.MAJOR,
        element="风",
        keywords=["创造力", "技能", "意志力", "专注", "行动"],
        upright_meaning="你拥有实现目标所需的一切资源和能力。现在是将想法付诸行动的最佳时机。",
        reversed_meaning="才能未能发挥、自我怀疑、操纵他人或被人操纵。需要重新评估自己的能力。",
        image_desc="魔术师一手指天，一手指地，桌上摆放着四元素的象征物。",
        advice="相信自己的能力，专注于目标，将资源整合起来付诸行动。"
    ),
    TarotCard(
        code="HIGH_PRIESTESS",
        name="女祭司",
        name_en="The High Priestess",
        number=2,
        suit=CardSuit.MAJOR,
        element="水",
        keywords=["直觉", "神秘", "潜意识", "智慧", "静默"],
        upright_meaning="倾听内心的声音，相信直觉。答案就在你的潜意识中，需要安静下来才能听到。",
        reversed_meaning="忽视直觉、秘密即将揭露、表面化。可能过于依赖理性而忽略内心感受。",
        image_desc="女祭司端坐于两根柱子之间，手持卷轴，脚下有新月。",
        advice="静下心来，倾听内在的智慧，不要急于做出决定。"
    ),
    TarotCard(
        code="EMPRESS",
        name="女皇",
        name_en="The Empress",
        number=3,
        suit=CardSuit.MAJOR,
        element="土",
        keywords=["丰饶", "创造", "母性", "美丽", "自然"],
        upright_meaning="丰收和创造的时期，生命力旺盛。代表母性的关怀、艺术创造力和物质富足。",
        reversed_meaning="创造力受阻、依赖他人、过度溺爱或被忽视。需要找回与自然的连接。",
        image_desc="女皇坐在舒适的宝座上，周围是茂盛的花园，象征丰饶。",
        advice="滋养你的创造力，关爱自己和他人，享受生活的美好。"
    ),
    TarotCard(
        code="EMPEROR",
        name="皇帝",
        name_en="The Emperor",
        number=4,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["权威", "结构", "稳定", "领导", "保护"],
        upright_meaning="建立秩序和结构的时候。代表权威、领导力和对生活的掌控。",
        reversed_meaning="专制、控制欲过强、缺乏纪律。可能是权威被滥用或结构崩塌。",
        image_desc="皇帝坐在石质宝座上，手持权杖，身后是险峻的山脉。",
        advice="建立清晰的规则和边界，承担起领导责任。"
    ),
    TarotCard(
        code="HIEROPHANT",
        name="教皇",
        name_en="The Hierophant",
        number=5,
        suit=CardSuit.MAJOR,
        element="土",
        keywords=["传统", "教育", "信仰", "指引", "仪式"],
        upright_meaning="寻求智慧的指引，学习传统知识。代表精神导师、教育和传统价值观。",
        reversed_meaning="挑战权威、打破常规、个人信仰冲突。可能需要走自己的路。",
        image_desc="教皇坐在两根柱子之间，祝福跪在面前的两个人。",
        advice="向有经验的人学习，但也要发展自己的信念体系。"
    ),
    TarotCard(
        code="LOVERS",
        name="恋人",
        name_en="The Lovers",
        number=6,
        suit=CardSuit.MAJOR,
        element="风",
        keywords=["爱情", "选择", "和谐", "价值观", "关系"],
        upright_meaning="重要的关系或选择。代表爱情、和谐的伴侣关系，以及价值观的统一。",
        reversed_meaning="关系不和谐、选择困难、价值观冲突。需要重新审视关系或决定。",
        image_desc="天使在上方祝福，一男一女站在伊甸园中。",
        advice="用心做出选择，确保它符合你的核心价值观。"
    ),
    TarotCard(
        code="CHARIOT",
        name="战车",
        name_en="The Chariot",
        number=7,
        suit=CardSuit.MAJOR,
        element="水",
        keywords=["胜利", "意志力", "决心", "控制", "前进"],
        upright_meaning="通过意志力和决心取得胜利。代表克服障碍、掌控局面、向目标前进。",
        reversed_meaning="失去方向、缺乏控制、挫折。需要重新找回动力和方向。",
        image_desc="战士驾驶战车，由一黑一白两只狮身人面像拉动。",
        advice="保持专注和决心，驾驭不同的力量向目标前进。"
    ),
    TarotCard(
        code="STRENGTH",
        name="力量",
        name_en="Strength",
        number=8,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["勇气", "耐心", "内在力量", "温柔", "自律"],
        upright_meaning="用温柔的方式展现力量。代表内在的勇气、耐心和对本能的掌控。",
        reversed_meaning="自我怀疑、缺乏自信、压抑情感。需要找回内在的力量。",
        image_desc="一位女性温柔地驯服一头狮子，头上有无限符号。",
        advice="相信自己的内在力量，用温和而坚定的方式面对挑战。"
    ),
    TarotCard(
        code="HERMIT",
        name="隐士",
        name_en="The Hermit",
        number=9,
        suit=CardSuit.MAJOR,
        element="土",
        keywords=["内省", "独处", "智慧", "寻求", "指引"],
        upright_meaning="需要独处和内省的时期。代表寻求内在智慧、精神追求和自我发现。",
        reversed_meaning="过度孤立、逃避社交、拒绝帮助。需要在独处和社交之间找到平衡。",
        image_desc="老隐士站在山顶，手持明灯和拐杖，照亮前路。",
        advice="花时间独处和反思，寻找内心的答案。"
    ),
    TarotCard(
        code="WHEEL_OF_FORTUNE",
        name="命运之轮",
        name_en="Wheel of Fortune",
        number=10,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["命运", "转折", "周期", "机遇", "变化"],
        upright_meaning="命运的转折点，好运即将到来。代表生命的循环、机遇和不可预测的变化。",
        reversed_meaning="厄运、抗拒变化、错失机会。需要适应变化而不是抗拒它。",
        image_desc="巨大的轮子转动，四角有四种神兽，代表固定星座。",
        advice="顺应命运的流动，把握机遇，接受生命的起伏。"
    ),
    TarotCard(
        code="JUSTICE",
        name="正义",
        name_en="Justice",
        number=11,
        suit=CardSuit.MAJOR,
        element="风",
        keywords=["公正", "真相", "因果", "平衡", "决断"],
        upright_meaning="公正的裁决，真相大白。代表因果报应、法律事务和道德责任。",
        reversed_meaning="不公正、逃避责任、偏见。需要面对真相，承担后果。",
        image_desc="正义女神坐在宝座上，一手持剑，一手持天平。",
        advice="诚实面对自己和他人，做出公正的决定。"
    ),
    TarotCard(
        code="HANGED_MAN",
        name="倒吊人",
        name_en="The Hanged Man",
        number=12,
        suit=CardSuit.MAJOR,
        element="水",
        keywords=["牺牲", "等待", "新视角", "放下", "顿悟"],
        upright_meaning="需要暂停和换个角度看问题。代表自愿的牺牲、等待时机和获得新视角。",
        reversed_meaning="无意义的牺牲、拖延、固执。需要行动而不是继续等待。",
        image_desc="一个人倒挂在树上，表情平静，头部发光。",
        advice="暂停脚步，换个角度看问题，有时放下才能获得。"
    ),
    TarotCard(
        code="DEATH",
        name="死神",
        name_en="Death",
        number=13,
        suit=CardSuit.MAJOR,
        element="水",
        keywords=["结束", "转变", "新生", "放手", "转型"],
        upright_meaning="一个阶段的结束，为新生腾出空间。代表深刻的转变、放下过去、迎接新生。",
        reversed_meaning="抗拒变化、停滞不前、无法放手。需要接受结束才能迎来新开始。",
        image_desc="骑着白马的死神，手持旗帜，太阳在远方升起。",
        advice="接受必要的结束，为新的开始做好准备。"
    ),
    TarotCard(
        code="TEMPERANCE",
        name="节制",
        name_en="Temperance",
        number=14,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["平衡", "调和", "耐心", "中庸", "愈合"],
        upright_meaning="寻找平衡和中庸之道。代表调和对立面、耐心等待和身心愈合。",
        reversed_meaning="失去平衡、过度、不和谐。需要重新找回生活的平衡。",
        image_desc="天使将水从一个杯子倒入另一个，一脚在水中，一脚在陆地。",
        advice="在各个方面寻找平衡，保持耐心和适度。"
    ),
    TarotCard(
        code="DEVIL",
        name="恶魔",
        name_en="The Devil",
        number=15,
        suit=CardSuit.MAJOR,
        element="土",
        keywords=["束缚", "诱惑", "阴影", "物质", "执念"],
        upright_meaning="被物质或欲望所束缚。代表需要面对的阴暗面、不健康的依赖和执念。",
        reversed_meaning="摆脱束缚、认清真相、重获自由。正在打破不健康的模式。",
        image_desc="恶魔坐在祭坛上，两个被锁链束缚的人站在下方。",
        advice="认识到什么在束缚你，你有能力打破这些锁链。"
    ),
    TarotCard(
        code="TOWER",
        name="高塔",
        name_en="The Tower",
        number=16,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["突变", "崩塌", "觉醒", "解放", "真相"],
        upright_meaning="突然的变化和崩塌，但也是必要的清理。代表打破虚假、突然的觉醒和解放。",
        reversed_meaning="逃避灾难、抗拒必要的改变、恐惧。需要面对而不是逃避。",
        image_desc="闪电击中高塔，人从塔中坠落，皇冠脱落。",
        advice="接受必要的崩塌，在废墟中重建更真实的生活。"
    ),
    TarotCard(
        code="STAR",
        name="星星",
        name_en="The Star",
        number=17,
        suit=CardSuit.MAJOR,
        element="风",
        keywords=["希望", "灵感", "宁静", "更新", "信心"],
        upright_meaning="希望和灵感的时期。代表内心的平静、精神的更新和对未来的信心。",
        reversed_meaning="失去希望、缺乏信心、脱节。需要重新找回内心的光芒。",
        image_desc="裸女跪在池边，将水倒入池中和大地，天上八颗星星闪耀。",
        advice="保持希望，相信宇宙的指引，你正走在正确的道路上。"
    ),
    TarotCard(
        code="MOON",
        name="月亮",
        name_en="The Moon",
        number=18,
        suit=CardSuit.MAJOR,
        element="水",
        keywords=["幻觉", "直觉", "恐惧", "潜意识", "神秘"],
        upright_meaning="事情不如表面看起来那样清晰。代表幻觉、恐惧、需要面对潜意识的时期。",
        reversed_meaning="走出迷雾、克服恐惧、真相浮现。迷惑正在消散。",
        image_desc="月亮照耀，狼和狗对月嚎叫，小龙虾从水中爬出。",
        advice="信任你的直觉，但也要小心不要被恐惧和幻觉所迷惑。"
    ),
    TarotCard(
        code="SUN",
        name="太阳",
        name_en="The Sun",
        number=19,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["成功", "快乐", "活力", "清晰", "乐观"],
        upright_meaning="光明和成功的时期。代表快乐、活力、清晰的理解和积极的结果。",
        reversed_meaning="暂时的阴霾、快乐被延迟、过度乐观。阳光终将穿透云层。",
        image_desc="太阳灿烂照耀，一个孩子骑在白马上，向日葵盛开。",
        advice="享受生命的美好，让你的光芒照耀他人。"
    ),
    TarotCard(
        code="JUDGEMENT",
        name="审判",
        name_en="Judgement",
        number=20,
        suit=CardSuit.MAJOR,
        element="火",
        keywords=["觉醒", "重生", "召唤", "评估", "解脱"],
        upright_meaning="灵魂的觉醒和召唤。代表重要的评估、内在的召唤和精神的重生。",
        reversed_meaning="自我怀疑、拒绝召唤、无法宽恕。需要回应内心的呼唤。",
        image_desc="天使吹响号角，死者从坟墓中复活，张开双臂迎接新生。",
        advice="回应你内心的召唤，放下过去，迎接新的使命。"
    ),
    TarotCard(
        code="WORLD",
        name="世界",
        name_en="The World",
        number=21,
        suit=CardSuit.MAJOR,
        element="土",
        keywords=["完成", "圆满", "成就", "整合", "旅程终点"],
        upright_meaning="一个周期的圆满完成。代表成就感、世界的整合和新旅程的开始。",
        reversed_meaning="未完成、延迟的成功、缺乏闭合。距离完成只差一步。",
        image_desc="女性被月桂花环环绕，四角有四神兽，手持权杖。",
        advice="庆祝你的成就，准备开始下一个更高层次的旅程。"
    ),
]


# 牌阵定义
@dataclass
class SpreadPosition:
    """牌阵位置"""
    index: int
    name: str
    description: str


@dataclass
class TarotSpread:
    """塔罗牌阵"""
    code: str
    name: str
    name_en: str
    positions: List[SpreadPosition]
    description: str
    suitable_for: List[str]


SPREADS: Dict[str, TarotSpread] = {
    "three_card": TarotSpread(
        code="three_card",
        name="三张牌阵",
        name_en="Three Card Spread",
        positions=[
            SpreadPosition(1, "过去", "过去的影响和经历"),
            SpreadPosition(2, "现在", "当前的状态和挑战"),
            SpreadPosition(3, "未来", "可能的发展和结果"),
        ],
        description="最经典的塔罗牌阵，适合简单直接的问题",
        suitable_for=["一般问题", "快速指引", "简单决策"]
    ),
    "celtic_cross": TarotSpread(
        code="celtic_cross",
        name="凯尔特十字",
        name_en="Celtic Cross",
        positions=[
            SpreadPosition(1, "现况", "当前的核心状态"),
            SpreadPosition(2, "障碍/支持", "面临的主要障碍或助力"),
            SpreadPosition(3, "目标", "意识层面的目标"),
            SpreadPosition(4, "根基", "潜意识的影响"),
            SpreadPosition(5, "过去", "近期过去的影响"),
            SpreadPosition(6, "未来", "近期未来的趋势"),
            SpreadPosition(7, "自我", "你在情境中的角色"),
            SpreadPosition(8, "环境", "外部环境的影响"),
            SpreadPosition(9, "希望/恐惧", "内心的期望或担忧"),
            SpreadPosition(10, "结果", "最终可能的结果"),
        ],
        description="最全面的塔罗牌阵，适合深度分析复杂问题",
        suitable_for=["复杂问题", "深度分析", "人生重大决策"]
    ),
    "horseshoe": TarotSpread(
        code="horseshoe",
        name="马蹄铁阵",
        name_en="Horseshoe Spread",
        positions=[
            SpreadPosition(1, "过去", "过去的影响"),
            SpreadPosition(2, "现在", "当前状态"),
            SpreadPosition(3, "隐藏因素", "未察觉的影响"),
            SpreadPosition(4, "障碍", "面临的挑战"),
            SpreadPosition(5, "周围环境", "外部影响"),
            SpreadPosition(6, "建议", "应采取的行动"),
            SpreadPosition(7, "结果", "可能的结果"),
        ],
        description="七张牌的中等复杂度牌阵",
        suitable_for=["中等复杂问题", "需要建议", "全面了解情况"]
    ),
    "love_cross": TarotSpread(
        code="love_cross",
        name="爱情十字阵",
        name_en="Love Cross",
        positions=[
            SpreadPosition(1, "你的状态", "你在关系中的状态"),
            SpreadPosition(2, "对方状态", "对方在关系中的状态"),
            SpreadPosition(3, "关系基础", "关系的根基"),
            SpreadPosition(4, "挑战", "关系面临的挑战"),
            SpreadPosition(5, "发展方向", "关系的发展趋势"),
        ],
        description="专门用于分析感情关系的牌阵",
        suitable_for=["感情问题", "关系分析", "爱情决策"]
    ),
    "single_card": TarotSpread(
        code="single_card",
        name="单牌抽取",
        name_en="Single Card",
        positions=[
            SpreadPosition(1, "指引", "当下的核心指引"),
        ],
        description="每日一牌或快速指引",
        suitable_for=["每日指引", "简单问题", "即时答案"]
    ),
}


def get_all_major_arcana() -> List[TarotCard]:
    """获取所有大阿尔卡那牌"""
    return MAJOR_ARCANA


def get_card_by_code(code: str) -> TarotCard | None:
    """根据代码获取牌"""
    for card in MAJOR_ARCANA:
        if card.code == code:
            return card
    return None


def get_spread_by_code(code: str) -> TarotSpread | None:
    """根据代码获取牌阵"""
    return SPREADS.get(code)


def get_all_spreads() -> List[TarotSpread]:
    """获取所有牌阵"""
    return list(SPREADS.values())
