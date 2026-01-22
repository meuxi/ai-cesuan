"""
紫微斗数星曜完整数据库
包含十四主星、六吉星、六煞星、四化星等详细信息

数据来源：mingpan项目 + 紫微斗数经典文献
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class StarCategory(Enum):
    """星曜类别"""
    MAIN = "主星"           # 十四主星
    LUCKY = "吉星"          # 六吉星
    EVIL = "煞星"           # 六煞星
    SIHUA = "四化"          # 四化星
    MINOR = "杂曜"          # 其他杂曜


class StarNature(Enum):
    """星曜性质"""
    AUSPICIOUS = "吉"
    INAUSPICIOUS = "凶"
    NEUTRAL = "中"


@dataclass
class StarInfo:
    """星曜信息"""
    name: str                    # 星名
    category: StarCategory       # 类别
    nature: StarNature           # 吉凶
    element: str                 # 五行
    yin_yang: str                # 阴阳
    meaning: str                 # 基本含义
    career: str                  # 事业特点
    personality: str             # 性格特点
    health: str                  # 健康注意
    relationship: str            # 感情特点
    brightness_levels: List[str] # 庙旺平落陷


# 十四主星详细数据
MAIN_STARS: Dict[str, StarInfo] = {
    '紫微': StarInfo(
        name='紫微',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='土',
        yin_yang='阴',
        meaning='帝星，尊贵之星，代表领导力和权威',
        career='适合管理、领导岗位，政界、大企业高层',
        personality='自尊心强，有领导才能，但有时显得高傲',
        health='注意脾胃、皮肤问题',
        relationship='对感情要求较高，配偶条件好',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '天机': StarInfo(
        name='天机',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='木',
        yin_yang='阴',
        meaning='智慧之星，代表谋略和变通',
        career='适合策划、顾问、技术研发等脑力工作',
        personality='聪明机智，善于思考，但有时优柔寡断',
        health='注意肝胆、神经系统',
        relationship='重视精神交流，感情细腻',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '太阳': StarInfo(
        name='太阳',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='火',
        yin_yang='阳',
        meaning='光明之星，代表博爱和付出',
        career='适合公职、教育、公益事业',
        personality='热情开朗，乐于助人，但有时过于操劳',
        health='注意心脏、眼睛问题',
        relationship='重感情，对家人照顾周到',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '武曲': StarInfo(
        name='武曲',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='金',
        yin_yang='阴',
        meaning='财星，代表财富和果断',
        career='适合金融、财务、军警等职业',
        personality='刚毅果断，重视效率，但有时显得冷漠',
        health='注意呼吸系统、肺部问题',
        relationship='感情上较为理性，重视物质基础',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '天同': StarInfo(
        name='天同',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='水',
        yin_yang='阳',
        meaning='福星，代表福气和享受',
        career='适合服务业、艺术、休闲娱乐相关',
        personality='温和善良，喜欢享受生活，但有时缺乏上进心',
        health='注意肾脏、泌尿系统',
        relationship='重视家庭和谐，感情温馨',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '廉贞': StarInfo(
        name='廉贞',
        category=StarCategory.MAIN,
        nature=StarNature.NEUTRAL,
        element='火',
        yin_yang='阴',
        meaning='囚星，代表桃花和政治',
        career='适合政治、法律、公关等职业',
        personality='聪明有魅力，但有时过于执着',
        health='注意心血管、神经问题',
        relationship='感情丰富，异性缘佳但需注意桃花',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '天府': StarInfo(
        name='天府',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='土',
        yin_yang='阳',
        meaning='财库星，代表稳重和积蓄',
        career='适合财务、银行、房产等稳定行业',
        personality='稳重保守，善于理财，有安全感需求',
        health='注意脾胃、消化系统',
        relationship='重视家庭稳定，感情忠诚',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '太阴': StarInfo(
        name='太阴',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='水',
        yin_yang='阴',
        meaning='财星，代表阴柔和细腻',
        career='适合财务、房产、夜间行业',
        personality='温柔细腻，有艺术气质，但有时多愁善感',
        health='注意肾脏、妇科（女性）问题',
        relationship='感情细腻，重视精神交流',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '贪狼': StarInfo(
        name='贪狼',
        category=StarCategory.MAIN,
        nature=StarNature.NEUTRAL,
        element='木',
        yin_yang='阳',
        meaning='桃花星，代表欲望和才艺',
        career='适合艺术、娱乐、公关、销售等',
        personality='多才多艺，善于交际，但有时欲望较强',
        health='注意肝脏、眼睛问题',
        relationship='异性缘佳，感情丰富多彩',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '巨门': StarInfo(
        name='巨门',
        category=StarCategory.MAIN,
        nature=StarNature.INAUSPICIOUS,
        element='水',
        yin_yang='阴',
        meaning='暗星，代表口才和是非',
        career='适合律师、教师、主播、销售等口才相关',
        personality='口才好，善于分析，但有时过于挑剔',
        health='注意口腔、咽喉问题',
        relationship='感情上需注意口舌之争',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '天相': StarInfo(
        name='天相',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='水',
        yin_yang='阳',
        meaning='印星，代表辅佐和协调',
        career='适合秘书、助理、协调管理等',
        personality='温和有礼，善于协调，但有时过于依赖他人',
        health='注意肾脏、泌尿系统',
        relationship='感情和谐，善于经营关系',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '天梁': StarInfo(
        name='天梁',
        category=StarCategory.MAIN,
        nature=StarNature.AUSPICIOUS,
        element='土',
        yin_yang='阳',
        meaning='荫星，代表化解和长寿',
        career='适合医疗、保险、慈善、教育等',
        personality='乐于助人，有包容心，但有时过于操心',
        health='注意脾胃，整体健康较好',
        relationship='感情稳定，有照顾他人的倾向',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '七杀': StarInfo(
        name='七杀',
        category=StarCategory.MAIN,
        nature=StarNature.INAUSPICIOUS,
        element='金',
        yin_yang='阴',
        meaning='将星，代表武勇和孤独',
        career='适合军警、运动员、创业等需要魄力的职业',
        personality='勇敢果断，有魄力，但有时过于刚硬',
        health='注意意外伤害、筋骨问题',
        relationship='感情上较为独立，需要空间',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
    '破军': StarInfo(
        name='破军',
        category=StarCategory.MAIN,
        nature=StarNature.INAUSPICIOUS,
        element='水',
        yin_yang='阴',
        meaning='耗星，代表变动和破坏',
        career='适合改革、创新、开拓类工作',
        personality='敢于冒险，追求变化，但有时过于冲动',
        health='注意意外、手术等问题',
        relationship='感情多变，需要刺激感',
        brightness_levels=['庙', '旺', '得', '平', '落', '陷']
    ),
}


# 六吉星
LUCKY_STARS: Dict[str, StarInfo] = {
    '左辅': StarInfo(
        name='左辅',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='土',
        yin_yang='阳',
        meaning='辅星，代表助力和贵人',
        career='有贵人相助，适合团队合作',
        personality='善于辅助他人，人缘好',
        health='整体健康较好',
        relationship='感情中有贵人牵线',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '右弼': StarInfo(
        name='右弼',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='水',
        yin_yang='阴',
        meaning='辅星，代表助力和贵人',
        career='有暗中相助之人，适合幕后工作',
        personality='温和有礼，善于协调',
        health='整体健康较好',
        relationship='感情顺利，有人暗中帮助',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '文昌': StarInfo(
        name='文昌',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='金',
        yin_yang='阳',
        meaning='科甲星，代表文才和考试',
        career='利考试、证照、文职工作',
        personality='聪明好学，文采出众',
        health='注意呼吸系统',
        relationship='重视精神层面的交流',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '文曲': StarInfo(
        name='文曲',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='水',
        yin_yang='阴',
        meaning='艺术星，代表才艺和口才',
        career='适合艺术、演艺、创作等',
        personality='多才多艺，有艺术气质',
        health='注意肾脏问题',
        relationship='感情浪漫，有艺术情调',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '天魁': StarInfo(
        name='天魁',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='火',
        yin_yang='阳',
        meaning='阳贵人星，代表男性贵人',
        career='事业有男性贵人相助',
        personality='正直有威严，受人尊敬',
        health='整体健康较好',
        relationship='有男性长辈或贵人帮助感情',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '天钺': StarInfo(
        name='天钺',
        category=StarCategory.LUCKY,
        nature=StarNature.AUSPICIOUS,
        element='火',
        yin_yang='阴',
        meaning='阴贵人星，代表女性贵人',
        career='事业有女性贵人相助',
        personality='温和有亲和力',
        health='整体健康较好',
        relationship='有女性长辈或贵人帮助感情',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
}


# 六煞星
EVIL_STARS: Dict[str, StarInfo] = {
    '擎羊': StarInfo(
        name='擎羊',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='金',
        yin_yang='阳',
        meaning='刑星，代表刑克和血光',
        career='适合外科医生、军警、屠宰等',
        personality='性格刚烈，容易冲动',
        health='注意意外伤害、手术',
        relationship='感情上容易有冲突',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '陀罗': StarInfo(
        name='陀罗',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='金',
        yin_yang='阴',
        meaning='拖延星，代表纠缠和拖延',
        career='做事容易拖延，需要耐心',
        personality='做事较慢，但有耐心',
        health='注意慢性病',
        relationship='感情上容易纠缠不清',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '火星': StarInfo(
        name='火星',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='火',
        yin_yang='阳',
        meaning='急躁星，代表急躁和灾厄',
        career='适合快节奏工作，但需控制脾气',
        personality='性格急躁，行动力强',
        health='注意发炎、烫伤等',
        relationship='感情上容易急躁',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '铃星': StarInfo(
        name='铃星',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='火',
        yin_yang='阴',
        meaning='孤独星，代表孤独和灾厄',
        career='适合独立工作，不喜团队',
        personality='性格孤僻，内心敏感',
        health='注意心脏、精神问题',
        relationship='感情上较为孤独',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '地空': StarInfo(
        name='地空',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='火',
        yin_yang='阳',
        meaning='空亡星，代表空虚和损失',
        career='不利投资，宜从事脑力工作',
        personality='想法独特，不切实际',
        health='注意精神问题',
        relationship='感情上容易空虚',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
    '地劫': StarInfo(
        name='地劫',
        category=StarCategory.EVIL,
        nature=StarNature.INAUSPICIOUS,
        element='火',
        yin_yang='阴',
        meaning='劫夺星，代表破财和意外',
        career='不利投资，宜稳定工作',
        personality='思想前卫，不拘常规',
        health='注意意外损失',
        relationship='感情上容易有波折',
        brightness_levels=['庙', '旺', '平', '陷']
    ),
}


# 四化星
SIHUA_STARS = {
    '化禄': {'nature': '吉', 'meaning': '财禄增加，顺利圆满'},
    '化权': {'nature': '吉', 'meaning': '权力掌控，能力展现'},
    '化科': {'nature': '吉', 'meaning': '名声荣誉，贵人相助'},
    '化忌': {'nature': '凶', 'meaning': '阻碍执著，需要化解'},
}


# 十二宫位名称和含义
TWELVE_PALACES = {
    '命宫': {'meaning': '代表自己，性格、外貌、一生格局'},
    '兄弟宫': {'meaning': '代表兄弟姐妹、朋友关系'},
    '夫妻宫': {'meaning': '代表婚姻、配偶、感情'},
    '子女宫': {'meaning': '代表子女、晚辈、性生活'},
    '财帛宫': {'meaning': '代表财运、理财能力'},
    '疾厄宫': {'meaning': '代表健康、疾病'},
    '迁移宫': {'meaning': '代表外出、贵人、社会关系'},
    '交友宫': {'meaning': '代表朋友、下属、社交'},
    '官禄宫': {'meaning': '代表事业、工作、社会地位'},
    '田宅宫': {'meaning': '代表房产、家庭环境'},
    '福德宫': {'meaning': '代表精神生活、兴趣爱好'},
    '父母宫': {'meaning': '代表父母、长辈、上司'},
}


# 便捷函数
def get_star_info(star_name: str) -> Optional[StarInfo]:
    """获取星曜信息"""
    all_stars = {**MAIN_STARS, **LUCKY_STARS, **EVIL_STARS}
    return all_stars.get(star_name)


def get_star_nature(star_name: str) -> str:
    """获取星曜吉凶"""
    info = get_star_info(star_name)
    if info:
        return info.nature.value
    return '未知'


def get_palace_meaning(palace_name: str) -> str:
    """获取宫位含义"""
    palace = TWELVE_PALACES.get(palace_name)
    return palace['meaning'] if palace else '未知宫位'


def analyze_star_combination(stars: List[str]) -> Dict:
    """分析星曜组合"""
    result = {
        'lucky_count': 0,
        'evil_count': 0,
        'main_stars': [],
        'lucky_stars': [],
        'evil_stars': [],
        'overall': '平'
    }
    
    for star in stars:
        if star in MAIN_STARS:
            result['main_stars'].append(star)
            if MAIN_STARS[star].nature == StarNature.AUSPICIOUS:
                result['lucky_count'] += 1
            elif MAIN_STARS[star].nature == StarNature.INAUSPICIOUS:
                result['evil_count'] += 1
        elif star in LUCKY_STARS:
            result['lucky_stars'].append(star)
            result['lucky_count'] += 1
        elif star in EVIL_STARS:
            result['evil_stars'].append(star)
            result['evil_count'] += 1
    
    if result['lucky_count'] > result['evil_count']:
        result['overall'] = '吉'
    elif result['evil_count'] > result['lucky_count']:
        result['overall'] = '凶'
    
    return result
