"""
五行关系数据
参考方案中的五行相生相克关系设计
"""

from typing import Dict, Any, Tuple, List
from dataclasses import dataclass
from enum import Enum


class WuXing(Enum):
    """五行"""
    WOOD = "木"
    FIRE = "火"
    EARTH = "土"
    METAL = "金"
    WATER = "水"


class RelationType(Enum):
    """关系类型"""
    SHENG = "生"      # 相生
    KE = "克"         # 相克
    SAME = "同"       # 同类
    XIE = "泄"        # 被泄
    HAO = "耗"        # 被耗


@dataclass
class WuXingRelation:
    """五行关系"""
    source: WuXing
    target: WuXing
    relation_type: RelationType
    strength: int = 1
    description: str = ""


# 五行基础属性
WUXING_ATTRIBUTES = {
    WuXing.WOOD: {
        "name": "木",
        "direction": "东",
        "season": "春",
        "color": "绿色/青色",
        "number": [3, 8],
        "organ": "肝胆",
        "emotion": "怒",
        "taste": "酸",
        "planet": "木星",
        "animal": "龙",
        "characteristics": "生发、条达、舒展",
    },
    WuXing.FIRE: {
        "name": "火",
        "direction": "南",
        "season": "夏",
        "color": "红色/紫色",
        "number": [2, 7],
        "organ": "心小肠",
        "emotion": "喜",
        "taste": "苦",
        "planet": "火星",
        "animal": "凤",
        "characteristics": "炎上、热烈、向上",
    },
    WuXing.EARTH: {
        "name": "土",
        "direction": "中央",
        "season": "四季末",
        "color": "黄色/棕色",
        "number": [5, 10],
        "organ": "脾胃",
        "emotion": "思",
        "taste": "甘",
        "planet": "土星",
        "animal": "麒麟",
        "characteristics": "承载、化育、稳定",
    },
    WuXing.METAL: {
        "name": "金",
        "direction": "西",
        "season": "秋",
        "color": "白色/金色",
        "number": [4, 9],
        "organ": "肺大肠",
        "emotion": "悲",
        "taste": "辛",
        "planet": "金星",
        "animal": "虎",
        "characteristics": "收敛、肃杀、清洁",
    },
    WuXing.WATER: {
        "name": "水",
        "direction": "北",
        "season": "冬",
        "color": "黑色/蓝色",
        "number": [1, 6],
        "organ": "肾膀胱",
        "emotion": "恐",
        "taste": "咸",
        "planet": "水星",
        "animal": "龟蛇",
        "characteristics": "润下、寒凉、闭藏",
    },
}


# 五行相生关系
WUXING_SHENG_RELATIONS: List[WuXingRelation] = [
    WuXingRelation(WuXing.WOOD, WuXing.FIRE, RelationType.SHENG, 1, "木生火：木燃烧生火"),
    WuXingRelation(WuXing.FIRE, WuXing.EARTH, RelationType.SHENG, 1, "火生土：火燃尽成灰土"),
    WuXingRelation(WuXing.EARTH, WuXing.METAL, RelationType.SHENG, 1, "土生金：土中藏金矿"),
    WuXingRelation(WuXing.METAL, WuXing.WATER, RelationType.SHENG, 1, "金生水：金遇冷凝水"),
    WuXingRelation(WuXing.WATER, WuXing.WOOD, RelationType.SHENG, 1, "水生木：水滋养树木"),
]


# 五行相克关系
WUXING_KE_RELATIONS: List[WuXingRelation] = [
    WuXingRelation(WuXing.WOOD, WuXing.EARTH, RelationType.KE, 1, "木克土：木根破土"),
    WuXingRelation(WuXing.EARTH, WuXing.WATER, RelationType.KE, 1, "土克水：土能堵水"),
    WuXingRelation(WuXing.WATER, WuXing.FIRE, RelationType.KE, 1, "水克火：水能灭火"),
    WuXingRelation(WuXing.FIRE, WuXing.METAL, RelationType.KE, 1, "火克金：火能熔金"),
    WuXingRelation(WuXing.METAL, WuXing.WOOD, RelationType.KE, 1, "金克木：金能伐木"),
]


# 五行关系速查表
WUXING_RELATIONS: Dict[Tuple[str, str], Dict[str, Any]] = {
    # 相生
    ("木", "火"): {"type": "生", "strength": 1, "description": "木生火"},
    ("火", "土"): {"type": "生", "strength": 1, "description": "火生土"},
    ("土", "金"): {"type": "生", "strength": 1, "description": "土生金"},
    ("金", "水"): {"type": "生", "strength": 1, "description": "金生水"},
    ("水", "木"): {"type": "生", "strength": 1, "description": "水生木"},
    # 相克
    ("木", "土"): {"type": "克", "strength": 1, "description": "木克土"},
    ("土", "水"): {"type": "克", "strength": 1, "description": "土克水"},
    ("水", "火"): {"type": "克", "strength": 1, "description": "水克火"},
    ("火", "金"): {"type": "克", "strength": 1, "description": "火克金"},
    ("金", "木"): {"type": "克", "strength": 1, "description": "金克木"},
    # 同类
    ("木", "木"): {"type": "同", "strength": 1, "description": "木木同类"},
    ("火", "火"): {"type": "同", "strength": 1, "description": "火火同类"},
    ("土", "土"): {"type": "同", "strength": 1, "description": "土土同类"},
    ("金", "金"): {"type": "同", "strength": 1, "description": "金金同类"},
    ("水", "水"): {"type": "同", "strength": 1, "description": "水水同类"},
    # 被生（泄）
    ("火", "木"): {"type": "泄", "strength": 1, "description": "木被火泄"},
    ("土", "火"): {"type": "泄", "strength": 1, "description": "火被土泄"},
    ("金", "土"): {"type": "泄", "strength": 1, "description": "土被金泄"},
    ("水", "金"): {"type": "泄", "strength": 1, "description": "金被水泄"},
    ("木", "水"): {"type": "泄", "strength": 1, "description": "水被木泄"},
    # 被克（耗）
    ("土", "木"): {"type": "耗", "strength": 1, "description": "土被木克"},
    ("水", "土"): {"type": "耗", "strength": 1, "description": "水被土克"},
    ("火", "水"): {"type": "耗", "strength": 1, "description": "火被水克"},
    ("金", "火"): {"type": "耗", "strength": 1, "description": "金被火克"},
    ("木", "金"): {"type": "耗", "strength": 1, "description": "木被金克"},
}


def get_relation(source: str, target: str) -> Dict[str, Any] | None:
    """获取两个五行之间的关系"""
    return WUXING_RELATIONS.get((source, target))


def get_sheng_element(element: str) -> str:
    """获取某五行所生的五行"""
    sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
    return sheng_map.get(element, "")


def get_ke_element(element: str) -> str:
    """获取某五行所克的五行"""
    ke_map = {"木": "土", "火": "金", "土": "水", "金": "木", "水": "火"}
    return ke_map.get(element, "")


def get_sheng_by(element: str) -> str:
    """获取生某五行的五行"""
    sheng_by_map = {"木": "水", "火": "木", "土": "火", "金": "土", "水": "金"}
    return sheng_by_map.get(element, "")


def get_ke_by(element: str) -> str:
    """获取克某五行的五行"""
    ke_by_map = {"木": "金", "火": "水", "土": "木", "金": "火", "水": "土"}
    return ke_by_map.get(element, "")


def get_wuxing_attributes(element: str) -> Dict[str, Any] | None:
    """获取五行属性"""
    for wx, attrs in WUXING_ATTRIBUTES.items():
        if wx.value == element:
            return attrs
    return None


def analyze_wuxing_balance(elements: Dict[str, int]) -> Dict[str, Any]:
    """
    分析五行平衡
    
    Args:
        elements: 五行数量统计 {"木": 2, "火": 1, ...}
    
    Returns:
        分析结果
    """
    total = sum(elements.values())
    if total == 0:
        return {"balanced": True, "strong": [], "weak": [], "missing": []}
    
    avg = total / 5
    
    strong = [e for e, count in elements.items() if count > avg * 1.5]
    weak = [e for e, count in elements.items() if 0 < count < avg * 0.5]
    missing = [e for e in ["木", "火", "土", "金", "水"] if elements.get(e, 0) == 0]
    
    return {
        "balanced": len(strong) == 0 and len(weak) == 0 and len(missing) == 0,
        "strong": strong,
        "weak": weak,
        "missing": missing,
        "distribution": elements,
        "advice": _generate_balance_advice(strong, weak, missing),
    }


def _generate_balance_advice(strong: List[str], weak: List[str], missing: List[str]) -> str:
    """生成五行平衡建议"""
    advice_parts = []
    
    if missing:
        for e in missing:
            attrs = get_wuxing_attributes(e)
            if attrs:
                advice_parts.append(f"缺{e}，可用{attrs['color']}补救，{attrs['direction']}方位有利")
    
    if strong:
        for e in strong:
            ke = get_ke_element(e)
            advice_parts.append(f"{e}旺，可用{ke}泄之")
    
    if weak:
        for e in weak:
            sheng_by = get_sheng_by(e)
            advice_parts.append(f"{e}弱，需用{sheng_by}生之")
    
    return "；".join(advice_parts) if advice_parts else "五行较为平衡"
