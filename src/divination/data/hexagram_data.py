"""
卦象数据库
参考 zhanwen 项目的 HexagramData 模型设计
包含小六壬六宫、六十四卦等完整数据
"""

from typing import Dict, Any, List
from dataclasses import dataclass, field


@dataclass
class HexagramInfo:
    """卦象信息"""
    name: str                          # 卦名
    element: str                       # 五行属性
    description: str                   # 描述
    interpretation: str                # 卦辞解读
    favorable_actions: List[str]       # 宜
    unfavorable_actions: List[str]     # 忌
    time_info: Dict[str, str]          # 时间信息
    direction_info: Dict[str, str]     # 方位信息
    resolution_methods: List[str]      # 化解方法
    six_god: str = ""                  # 六神
    luck_level: str = ""               # 吉凶等级


# 小六壬六宫数据
XIAOLIU_HEXAGRAMS: Dict[str, HexagramInfo] = {
    "大安": HexagramInfo(
        name="大安",
        element="木",
        description="身不动时，五行属木，颜色青色，方位东方",
        interpretation="大安事事昌，求财在坤方，失物去不远，宅舍保安康。行人身未动，病者主无妨，将军回田野，仔细更推详。",
        favorable_actions=["求财", "婚姻", "出行", "求官", "见贵", "谋事"],
        unfavorable_actions=["诉讼争斗"],
        time_info={"hour": "寅卯", "month": "春季", "day": "甲乙日"},
        direction_info={"favorable": "东方", "坤方": "西南方"},
        resolution_methods=["佩戴绿色饰品", "东方发展", "多亲近自然"],
        six_god="青龙",
        luck_level="大吉"
    ),
    "留连": HexagramInfo(
        name="留连",
        element="水",
        description="卒未归时，五行属水，颜色黑色，方位北方",
        interpretation="留连事难成，求谋日未明，官事只宜缓，去者未回程。失物南方见，急讨方心称，更须防口舌，人口且平平。",
        favorable_actions=["等待", "蓄势"],
        unfavorable_actions=["求财", "出行", "诉讼", "急事"],
        time_info={"hour": "亥子", "month": "冬季", "day": "壬癸日"},
        direction_info={"favorable": "北方", "失物": "南方"},
        resolution_methods=["耐心等待", "多喝水", "黑色衣物"],
        six_god="玄武",
        luck_level="小凶"
    ),
    "速喜": HexagramInfo(
        name="速喜",
        element="火",
        description="人便至时，五行属火，颜色红色，方位南方",
        interpretation="速喜喜来临，求财向南行，失物申未午，逢人路上寻。官事有福德，病者无祸侵，田宅六畜吉，行人有信音。",
        favorable_actions=["求财", "婚姻", "出行", "求官", "谋事", "考试"],
        unfavorable_actions=["安葬", "动土"],
        time_info={"hour": "巳午", "month": "夏季", "day": "丙丁日"},
        direction_info={"favorable": "南方", "失物": "西南方"},
        resolution_methods=["穿红色衣物", "南方发展", "多晒太阳"],
        six_god="朱雀",
        luck_level="大吉"
    ),
    "赤口": HexagramInfo(
        name="赤口",
        element="金",
        description="官事凶时，五行属金，颜色白色，方位西方",
        interpretation="赤口主口舌，官非切宜防，失物速速讨，行人有惊慌。六畜多作怪，病者出西方，更须防咀咒，诚恐染瘟皇。",
        favorable_actions=["求医", "祭祀"],
        unfavorable_actions=["诉讼", "口舌", "出行", "求财", "婚姻"],
        time_info={"hour": "申酉", "month": "秋季", "day": "庚辛日"},
        direction_info={"favorable": "西方", "凶方": "东方"},
        resolution_methods=["少言慎行", "佩戴金属饰品", "白色衣物"],
        six_god="白虎",
        luck_level="大凶"
    ),
    "小吉": HexagramInfo(
        name="小吉",
        element="水",
        description="人来喜时，五行属水，颜色黑色，方位北方",
        interpretation="小吉最吉昌，路上好商量，阴人来报喜，失物在坤方。行人即便至，交关甚是强，凡事皆和合，病者叩穹苍。",
        favorable_actions=["求财", "婚姻", "出行", "交易", "合作"],
        unfavorable_actions=["诉讼"],
        time_info={"hour": "亥子", "month": "冬季", "day": "壬癸日"},
        direction_info={"favorable": "北方", "失物": "西南方"},
        resolution_methods=["多与人合作", "黑蓝色衣物", "北方发展"],
        six_god="六合",
        luck_level="中吉"
    ),
    "空亡": HexagramInfo(
        name="空亡",
        element="土",
        description="音信稀时，五行属土，颜色黄色，方位中央",
        interpretation="空亡事不祥，阴人多乖张，求财无利益，行人有灾殃。失物寻不见，官事有刑伤，病人逢暗鬼，祈禳保安康。",
        favorable_actions=["祭祀", "祈福", "修身"],
        unfavorable_actions=["求财", "出行", "婚姻", "诉讼", "投资"],
        time_info={"hour": "辰戌丑未", "month": "四季月", "day": "戊己日"},
        direction_info={"favorable": "中央", "凶方": "四方皆凶"},
        resolution_methods=["静守待时", "多祈福", "黄色衣物"],
        six_god="勾陈",
        luck_level="大凶"
    ),
}


# 六神数据
SIX_GODS = {
    "青龙": {
        "element": "木",
        "nature": "吉神",
        "meaning": "吉庆、喜事、贵人、文书",
        "favorable": ["求财", "升职", "婚姻", "出行"],
    },
    "朱雀": {
        "element": "火",
        "nature": "凶神",
        "meaning": "口舌、是非、文书、信息",
        "favorable": ["文书", "考试"],
        "unfavorable": ["官司", "口舌"],
    },
    "勾陈": {
        "element": "土",
        "nature": "凶神",
        "meaning": "田土、牢狱、勾连、拖延",
        "unfavorable": ["诉讼", "出行"],
    },
    "腾蛇": {
        "element": "土",
        "nature": "凶神",
        "meaning": "惊恐、怪异、虚惊、变化",
        "unfavorable": ["安神", "动土"],
    },
    "白虎": {
        "element": "金",
        "nature": "凶神",
        "meaning": "凶丧、血光、疾病、争斗",
        "unfavorable": ["婚姻", "求财", "出行"],
    },
    "玄武": {
        "element": "水",
        "nature": "凶神",
        "meaning": "盗贼、暧昧、小人、阴私",
        "unfavorable": ["求财", "合作"],
    },
    "六合": {
        "element": "木",
        "nature": "吉神",
        "meaning": "和合、婚姻、交易、合作",
        "favorable": ["婚姻", "交易", "合作"],
    },
}


# 六十四卦基础数据
SIXTY_FOUR_HEXAGRAMS = {
    "乾": {
        "name": "乾为天",
        "symbol": "䷀",
        "upper": "乾",
        "lower": "乾",
        "element": "金",
        "nature": "刚健",
        "judgment": "元亨利贞",
        "meaning": "乾卦象征天，具有刚健之德。元始、亨通、利益、贞正。",
    },
    "坤": {
        "name": "坤为地",
        "symbol": "䷁",
        "upper": "坤",
        "lower": "坤",
        "element": "土",
        "nature": "柔顺",
        "judgment": "元亨，利牝马之贞",
        "meaning": "坤卦象征地，具有柔顺之德。顺从、包容、承载万物。",
    },
    "屯": {
        "name": "水雷屯",
        "symbol": "䷂",
        "upper": "坎",
        "lower": "震",
        "element": "水",
        "nature": "艰难",
        "judgment": "元亨利贞，勿用有攸往，利建侯",
        "meaning": "屯卦象征草木初生，万事开头难，需要耐心和毅力。",
    },
    "蒙": {
        "name": "山水蒙",
        "symbol": "䷃",
        "upper": "艮",
        "lower": "坎",
        "element": "土",
        "nature": "蒙昧",
        "judgment": "亨。匪我求童蒙，童蒙求我",
        "meaning": "蒙卦象征启蒙教育，需要虚心学习，寻求智慧指引。",
    },
    "需": {
        "name": "水天需",
        "symbol": "䷄",
        "upper": "坎",
        "lower": "乾",
        "element": "水",
        "nature": "等待",
        "judgment": "有孚，光亨，贞吉，利涉大川",
        "meaning": "需卦象征等待，有诚信则光明亨通，时机未到需耐心等待。",
    },
    "讼": {
        "name": "天水讼",
        "symbol": "䷅",
        "upper": "乾",
        "lower": "坎",
        "element": "金",
        "nature": "争讼",
        "judgment": "有孚窒惕，中吉，终凶，利见大人",
        "meaning": "讼卦象征争讼，争执宜和解，见贵人可化解。",
    },
    "师": {
        "name": "地水师",
        "symbol": "䷆",
        "upper": "坤",
        "lower": "坎",
        "element": "土",
        "nature": "军旅",
        "judgment": "贞，丈人吉，无咎",
        "meaning": "师卦象征军队，需要有德行的领导者。",
    },
    "比": {
        "name": "水地比",
        "symbol": "䷇",
        "upper": "坎",
        "lower": "坤",
        "element": "水",
        "nature": "亲比",
        "judgment": "吉。原筮元永贞，无咎",
        "meaning": "比卦象征亲近，团结合作，互相扶持。",
    },
}


def get_xiaoliu_hexagram(name: str) -> HexagramInfo | None:
    """获取小六壬卦象信息"""
    return XIAOLIU_HEXAGRAMS.get(name)


def get_six_god(name: str) -> Dict[str, Any] | None:
    """获取六神信息"""
    return SIX_GODS.get(name)


def get_hexagram_by_name(name: str) -> Dict[str, Any] | None:
    """获取六十四卦信息"""
    return SIXTY_FOUR_HEXAGRAMS.get(name)


def get_all_xiaoliu() -> Dict[str, HexagramInfo]:
    """获取所有小六壬卦象"""
    return XIAOLIU_HEXAGRAMS
