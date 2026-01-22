"""
78张韦特塔罗牌完整数据
包含22张大阿卡纳和56张小阿卡纳

数据来源：MingAI tarot.ts
"""
from typing import TypedDict, List, Literal, Optional
import random
from datetime import date


# 牌组类型
TarotSuit = Literal['major', 'wands', 'cups', 'swords', 'pentacles']

# 牌的方向
CardOrientation = Literal['upright', 'reversed']


class TarotCard(TypedDict):
    """塔罗牌定义"""
    id: int
    name: str              # 英文名
    name_chinese: str      # 中文名
    suit: TarotSuit        # 牌组
    number: int            # 编号
    image: str             # 图片路径
    keywords: List[str]    # 关键词
    upright_meaning: str   # 正位含义
    reversed_meaning: str  # 逆位含义
    element: Optional[str] # 对应元素
    zodiac: Optional[str]  # 对应星座


class DrawnCard(TypedDict):
    """抽牌结果"""
    card: TarotCard
    orientation: CardOrientation
    position: Optional[str]  # 在牌阵中的位置含义


class SpreadPosition(TypedDict):
    """牌阵位置"""
    name: str
    meaning: str


class TarotSpread(TypedDict):
    """牌阵定义"""
    id: str
    name: str
    description: str
    positions: List[SpreadPosition]
    card_count: int


# 22张大阿卡纳
MAJOR_ARCANA: List[TarotCard] = [
    {
        'id': 0, 'name': 'The Fool', 'name_chinese': '愚人', 'suit': 'major', 'number': 0,
        'image': '/tarot_cards/thefool.jpeg',
        'keywords': ['新开始', '纯真', '冒险', '自由'],
        'upright_meaning': '代表新的开始、无限的可能性。保持开放的心态，勇敢地踏上未知的旅程。',
        'reversed_meaning': '可能意味着鲁莽、不负责任，或者对新事物的恐惧阻碍了你前进。',
        'element': '风', 'zodiac': '天王星'
    },
    {
        'id': 1, 'name': 'The Magician', 'name_chinese': '魔术师', 'suit': 'major', 'number': 1,
        'image': '/tarot_cards/themagician.jpeg',
        'keywords': ['意志力', '创造', '技巧', '资源'],
        'upright_meaning': '你拥有实现目标所需的一切资源和能力，现在是采取行动的时候。',
        'reversed_meaning': '警惕欺骗或被欺骗，可能存在潜力未被开发或资源使用不当的情况。',
        'element': '风', 'zodiac': '水星'
    },
    {
        'id': 2, 'name': 'The High Priestess', 'name_chinese': '女祭司', 'suit': 'major', 'number': 2,
        'image': '/tarot_cards/thehighpriestess.jpeg',
        'keywords': ['直觉', '神秘', '潜意识', '智慧'],
        'upright_meaning': '倾听你的直觉和内心的声音，答案可能就隐藏在潜意识中。',
        'reversed_meaning': '可能忽视了直觉的引导，或者被表面的事物所迷惑。',
        'element': '水', 'zodiac': '月亮'
    },
    {
        'id': 3, 'name': 'The Empress', 'name_chinese': '皇后', 'suit': 'major', 'number': 3,
        'image': '/tarot_cards/theempress.jpeg',
        'keywords': ['富饶', '母性', '自然', '创造力'],
        'upright_meaning': '象征丰收和繁荣，是创造力和养育能量的体现。',
        'reversed_meaning': '可能存在创造力受阻、过度依赖他人或自我忽视的情况。',
        'element': '土', 'zodiac': '金星'
    },
    {
        'id': 4, 'name': 'The Emperor', 'name_chinese': '皇帝', 'suit': 'major', 'number': 4,
        'image': '/tarot_cards/theemperor.jpeg',
        'keywords': ['权威', '结构', '控制', '父亲'],
        'upright_meaning': '代表稳定和秩序，鼓励你建立结构并承担领导责任。',
        'reversed_meaning': '警惕过度控制或权威的滥用，也可能暗示缺乏自律。',
        'element': '火', 'zodiac': '白羊座'
    },
    {
        'id': 5, 'name': 'The Hierophant', 'name_chinese': '教皇', 'suit': 'major', 'number': 5,
        'image': '/tarot_cards/thehierophant.jpeg',
        'keywords': ['传统', '信仰', '教育', '指导'],
        'upright_meaning': '代表传统价值观和精神指导，寻求导师或遵循既定的道路。',
        'reversed_meaning': '可能在挑战传统观念，或需要找到自己独特的精神道路。',
        'element': '土', 'zodiac': '金牛座'
    },
    {
        'id': 6, 'name': 'The Lovers', 'name_chinese': '恋人', 'suit': 'major', 'number': 6,
        'image': '/tarot_cards/TheLovers.jpg',
        'keywords': ['爱情', '选择', '和谐', '关系'],
        'upright_meaning': '代表和谐的关系和重要的选择，跟随内心做出决定。',
        'reversed_meaning': '可能面临关系中的不和谐，或在重要选择面前犹豫不决。',
        'element': '风', 'zodiac': '双子座'
    },
    {
        'id': 7, 'name': 'The Chariot', 'name_chinese': '战车', 'suit': 'major', 'number': 7,
        'image': '/tarot_cards/thechariot.jpeg',
        'keywords': ['意志力', '胜利', '决心', '控制'],
        'upright_meaning': '凭借坚定的意志力和决心，你将克服障碍取得胜利。',
        'reversed_meaning': '可能缺乏方向或自控力，需要重新调整你的目标。',
        'element': '水', 'zodiac': '巨蟹座'
    },
    {
        'id': 8, 'name': 'Strength', 'name_chinese': '力量', 'suit': 'major', 'number': 8,
        'image': '/tarot_cards/thestrength.jpeg',
        'keywords': ['勇气', '耐心', '内在力量', '慈悲'],
        'upright_meaning': '真正的力量来自内心，以耐心和慈悲面对挑战。',
        'reversed_meaning': '可能感到自我怀疑或缺乏信心，需要重新连接内在的力量。',
        'element': '火', 'zodiac': '狮子座'
    },
    {
        'id': 9, 'name': 'The Hermit', 'name_chinese': '隐士', 'suit': 'major', 'number': 9,
        'image': '/tarot_cards/thehermit.jpeg',
        'keywords': ['内省', '独处', '智慧', '引导'],
        'upright_meaning': '现在是内省和寻求内在智慧的时候，独处能带来启发。',
        'reversed_meaning': '可能过度孤立自己，或拒绝接受他人的指导。',
        'element': '土', 'zodiac': '处女座'
    },
    {
        'id': 10, 'name': 'Wheel of Fortune', 'name_chinese': '命运之轮', 'suit': 'major', 'number': 10,
        'image': '/tarot_cards/wheeloffortune.jpeg',
        'keywords': ['命运', '变化', '周期', '机遇'],
        'upright_meaning': '生活正在发生积极的变化，抓住命运带来的机遇。',
        'reversed_meaning': '可能经历不利的变化，记住这只是周期的一部分。',
        'element': '火', 'zodiac': '木星'
    },
    {
        'id': 11, 'name': 'Justice', 'name_chinese': '正义', 'suit': 'major', 'number': 11,
        'image': '/tarot_cards/justice.jpeg',
        'keywords': ['公正', '真相', '因果', '平衡'],
        'upright_meaning': '公正将会实现，你的行为会得到公平的回报。',
        'reversed_meaning': '可能存在不公正的情况，或需要面对自己逃避的真相。',
        'element': '风', 'zodiac': '天秤座'
    },
    {
        'id': 12, 'name': 'The Hanged Man', 'name_chinese': '倒吊人', 'suit': 'major', 'number': 12,
        'image': '/tarot_cards/thehangedman.jpeg',
        'keywords': ['暂停', '臣服', '新视角', '牺牲'],
        'upright_meaning': '暂时放下控制，换个角度看问题，可能需要做出一些牺牲。',
        'reversed_meaning': '可能在抗拒必要的改变，或做出了不必要的牺牲。',
        'element': '水', 'zodiac': '海王星'
    },
    {
        'id': 13, 'name': 'Death', 'name_chinese': '死神', 'suit': 'major', 'number': 13,
        'image': '/tarot_cards/death.jpeg',
        'keywords': ['结束', '转变', '重生', '放下'],
        'upright_meaning': '一个阶段的结束意味着新的开始，学会放下过去。',
        'reversed_meaning': '可能在抗拒必要的改变，害怕放手或前进。',
        'element': '水', 'zodiac': '天蝎座'
    },
    {
        'id': 14, 'name': 'Temperance', 'name_chinese': '节制', 'suit': 'major', 'number': 14,
        'image': '/tarot_cards/temperance.jpeg',
        'keywords': ['平衡', '耐心', '调和', '适度'],
        'upright_meaning': '保持耐心和平衡，找到生活中各方面的和谐。',
        'reversed_meaning': '可能存在不平衡或过度行为，需要恢复适度。',
        'element': '火', 'zodiac': '射手座'
    },
    {
        'id': 15, 'name': 'The Devil', 'name_chinese': '恶魔', 'suit': 'major', 'number': 15,
        'image': '/tarot_cards/thedevil.jpeg',
        'keywords': ['束缚', '诱惑', '物质', '阴影'],
        'upright_meaning': '意识到什么在束缚你，面对你的阴暗面和不良习惯。',
        'reversed_meaning': '正在打破束缚，从不良模式或关系中解脱出来。',
        'element': '土', 'zodiac': '摩羯座'
    },
    {
        'id': 16, 'name': 'The Tower', 'name_chinese': '高塔', 'suit': 'major', 'number': 16,
        'image': '/tarot_cards/thetower.jpeg',
        'keywords': ['突变', '崩塌', '觉醒', '解放'],
        'upright_meaning': '突然的变化可能令人不安，但这是破除虚假走向真实的必经之路。',
        'reversed_meaning': '可能在逃避必要的改变，或者变化正在内部发生。',
        'element': '火', 'zodiac': '火星'
    },
    {
        'id': 17, 'name': 'The Star', 'name_chinese': '星星', 'suit': 'major', 'number': 17,
        'image': '/tarot_cards/thestar.jpeg',
        'keywords': ['希望', '灵感', '宁静', '更新'],
        'upright_meaning': '经历困难后的平静和希望，相信宇宙的引导。',
        'reversed_meaning': '可能暂时失去希望或方向，需要重新找到信心。',
        'element': '风', 'zodiac': '水瓶座'
    },
    {
        'id': 18, 'name': 'The Moon', 'name_chinese': '月亮', 'suit': 'major', 'number': 18,
        'image': '/tarot_cards/themoon.jpeg',
        'keywords': ['幻觉', '恐惧', '潜意识', '直觉'],
        'upright_meaning': '面对恐惧和幻觉，相信你的直觉穿越迷雾。',
        'reversed_meaning': '幻觉正在消散，真相开始显现，恐惧减少。',
        'element': '水', 'zodiac': '双鱼座'
    },
    {
        'id': 19, 'name': 'The Sun', 'name_chinese': '太阳', 'suit': 'major', 'number': 19,
        'image': '/tarot_cards/thesun.jpeg',
        'keywords': ['喜悦', '成功', '生机', '光明'],
        'upright_meaning': '这是充满喜悦和成功的时期，享受生活的光明面。',
        'reversed_meaning': '喜悦可能被暂时遮蔽，但光明终将到来。',
        'element': '火', 'zodiac': '太阳'
    },
    {
        'id': 20, 'name': 'Judgement', 'name_chinese': '审判', 'suit': 'major', 'number': 20,
        'image': '/tarot_cards/judgement.jpeg',
        'keywords': ['觉醒', '重生', '召唤', '反思'],
        'upright_meaning': '听从内心更高的召唤，是自我评估和重生的时刻。',
        'reversed_meaning': '可能在逃避自我反思，或没有听到内心的召唤。',
        'element': '火', 'zodiac': '冥王星'
    },
    {
        'id': 21, 'name': 'The World', 'name_chinese': '世界', 'suit': 'major', 'number': 21,
        'image': '/tarot_cards/theworld.jpeg',
        'keywords': ['完成', '整合', '成就', '旅程'],
        'upright_meaning': '一个重要周期的完成，成就和圆满的时刻。',
        'reversed_meaning': '可能还有未完成的事项，或者在完成前需要更多努力。',
        'element': '土', 'zodiac': '土星'
    },
]

# 牌组中文名
SUIT_NAMES = {
    'major': '大阿卡纳',
    'wands': '权杖',
    'cups': '圣杯',
    'swords': '宝剑',
    'pentacles': '星币',
}

# 牌组五行
SUIT_ELEMENTS = {
    'wands': '火',
    'cups': '水',
    'swords': '风',
    'pentacles': '土',
}

# 数字中文名
NUMBER_CHINESE = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
COURT_CHINESE = ['侍从', '骑士', '王后', '国王']


def generate_minor_arcana() -> List[TarotCard]:
    """生成56张小阿卡纳"""
    suits = [
        {'suit': 'wands', 'element': '火', 'theme': '行动与创造力'},
        {'suit': 'cups', 'element': '水', 'theme': '情感与关系'},
        {'suit': 'swords', 'element': '风', 'theme': '思维与挑战'},
        {'suit': 'pentacles', 'element': '土', 'theme': '物质与实践'},
    ]
    
    numbers = [
        {'num': 1, 'name': 'Ace', 'keywords': ['新开始', '潜力', '机会']},
        {'num': 2, 'name': 'Two', 'keywords': ['平衡', '选择', '合作']},
        {'num': 3, 'name': 'Three', 'keywords': ['成长', '创造', '合作']},
        {'num': 4, 'name': 'Four', 'keywords': ['稳定', '基础', '休息']},
        {'num': 5, 'name': 'Five', 'keywords': ['冲突', '变化', '挑战']},
        {'num': 6, 'name': 'Six', 'keywords': ['和谐', '给予', '恢复']},
        {'num': 7, 'name': 'Seven', 'keywords': ['反思', '评估', '等待']},
        {'num': 8, 'name': 'Eight', 'keywords': ['行动', '速度', '进展']},
        {'num': 9, 'name': 'Nine', 'keywords': ['接近完成', '满足', '韧性']},
        {'num': 10, 'name': 'Ten', 'keywords': ['完成', '极端', '周期结束']},
        {'num': 11, 'name': 'Page', 'keywords': ['学习', '消息', '探索']},
        {'num': 12, 'name': 'Knight', 'keywords': ['行动', '冒险', '追求']},
        {'num': 13, 'name': 'Queen', 'keywords': ['掌握', '滋养', '直觉']},
        {'num': 14, 'name': 'King', 'keywords': ['权威', '控制', '成熟']},
    ]
    
    cards = []
    card_id = 22
    
    for suit_info in suits:
        suit = suit_info['suit']
        element = suit_info['element']
        theme = suit_info['theme']
        suit_name = SUIT_NAMES[suit]
        
        for num_info in numbers:
            num = num_info['num']
            name = num_info['name']
            keywords = num_info['keywords']
            
            # 英文名
            eng_name = f"{name} of {suit.capitalize()}"
            
            # 中文名
            if num <= 10:
                chinese_name = f"{suit_name}{NUMBER_CHINESE[num - 1]}"
            else:
                chinese_name = f"{suit_name}{COURT_CHINESE[num - 11]}"
            
            # 图片路径
            prefix = name.lower() + 'of'
            image = f"/tarot_cards/{prefix}{suit}.jpeg"
            
            cards.append({
                'id': card_id,
                'name': eng_name,
                'name_chinese': chinese_name,
                'suit': suit,
                'number': num,
                'image': image,
                'keywords': keywords + [theme],
                'upright_meaning': f'{chinese_name}正位：在{theme}领域的{"、".join(keywords)}能量。',
                'reversed_meaning': f'{chinese_name}逆位：{theme}领域可能面临阻碍或需要反思。',
                'element': element,
                'zodiac': None,
            })
            card_id += 1
    
    return cards


# 完整的78张塔罗牌
TAROT_CARDS: List[TarotCard] = MAJOR_ARCANA + generate_minor_arcana()


# 常用牌阵
TAROT_SPREADS: List[TarotSpread] = [
    {
        'id': 'single',
        'name': '单牌',
        'description': '最简单的牌阵，抽一张牌获取当前情况的指引。',
        'positions': [{'name': '当前指引', 'meaning': '代表当前情况最需要关注的信息'}],
        'card_count': 1,
    },
    {
        'id': 'three-card',
        'name': '三牌阵',
        'description': '经典牌阵，展示过去、现在、未来的发展脉络。',
        'positions': [
            {'name': '过去', 'meaning': '影响当前情况的过去因素'},
            {'name': '现在', 'meaning': '当前情况的核心'},
            {'name': '未来', 'meaning': '可能的发展方向'},
        ],
        'card_count': 3,
    },
    {
        'id': 'love',
        'name': '爱情牌阵',
        'description': '专门解读感情问题的牌阵。',
        'positions': [
            {'name': '你的状态', 'meaning': '你在这段关系中的状态'},
            {'name': '对方状态', 'meaning': '对方在这段关系中的状态'},
            {'name': '关系现状', 'meaning': '两人关系的现状'},
            {'name': '建议', 'meaning': '改善关系的建议'},
        ],
        'card_count': 4,
    },
    {
        'id': 'celtic-cross',
        'name': '凯尔特十字',
        'description': '最经典全面的牌阵，深入分析复杂问题。',
        'positions': [
            {'name': '现状', 'meaning': '问题的核心'},
            {'name': '挑战', 'meaning': '面临的主要障碍'},
            {'name': '意识', 'meaning': '你意识到的方面'},
            {'name': '潜意识', 'meaning': '隐藏的影响因素'},
            {'name': '过去', 'meaning': '近期的影响'},
            {'name': '未来', 'meaning': '近期可能的发展'},
            {'name': '态度', 'meaning': '你对问题的态度'},
            {'name': '环境', 'meaning': '外部影响因素'},
            {'name': '希望与恐惧', 'meaning': '内心的期望与担忧'},
            {'name': '结果', 'meaning': '最可能的结果'},
        ],
        'card_count': 10,
    },
]


def draw_cards(count: int = 1, allow_reversed: bool = True) -> List[DrawnCard]:
    """随机抽取塔罗牌"""
    shuffled = TAROT_CARDS.copy()
    random.shuffle(shuffled)
    drawn = shuffled[:count]
    
    return [
        {
            'card': card,
            'orientation': 'reversed' if allow_reversed and random.random() > 0.5 else 'upright',
            'position': None,
        }
        for card in drawn
    ]


def draw_for_spread(spread_id: str, allow_reversed: bool = True) -> dict | None:
    """根据牌阵抽牌"""
    spread = next((s for s in TAROT_SPREADS if s['id'] == spread_id), None)
    if not spread:
        return None
    
    drawn_cards = draw_cards(spread['card_count'], allow_reversed)
    
    # 添加位置信息
    for i, drawn in enumerate(drawn_cards):
        if i < len(spread['positions']):
            drawn['position'] = spread['positions'][i]['meaning']
    
    return {'spread': spread, 'cards': drawn_cards}


def get_daily_card(d: date = None) -> DrawnCard:
    """每日一牌（基于日期固定）"""
    if d is None:
        d = date.today()
    
    seed = d.year * 10000 + d.month * 100 + d.day
    card_index = seed % len(TAROT_CARDS)
    is_reversed = (seed % 7) > 3
    
    return {
        'card': TAROT_CARDS[card_index],
        'orientation': 'reversed' if is_reversed else 'upright',
        'position': None,
    }


def get_card_by_id(card_id: int) -> TarotCard | None:
    """通过ID获取卡片"""
    return next((c for c in TAROT_CARDS if c['id'] == card_id), None)
