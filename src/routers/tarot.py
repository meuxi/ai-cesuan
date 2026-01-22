"""
塔罗牌API路由
提供牌阵、牌义查询和智能解读接口
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..divination.tarot.cards import (
    get_all_major_arcana,
    get_card_by_code,
    get_spread_by_code,
    get_all_spreads,
    MAJOR_ARCANA,
    SPREADS,
    CardSuit
)
from ..divination.tarot.minor_arcana import (
    get_all_minor_arcana,
    get_cards_by_suit,
    get_minor_card_by_code,
    MINOR_ARCANA,
)

router = APIRouter(prefix="/tarot", tags=["塔罗牌"])


class CardResponse(BaseModel):
    """塔罗牌响应"""
    code: str
    name: str
    name_en: str
    number: int
    suit: str
    element: str
    keywords: List[str]
    upright_meaning: str
    reversed_meaning: str
    image_desc: str
    advice: str


class SpreadPositionResponse(BaseModel):
    """牌阵位置响应"""
    index: int
    name: str
    description: str


class SpreadResponse(BaseModel):
    """牌阵响应"""
    code: str
    name: str
    name_en: str
    positions: List[SpreadPositionResponse]
    description: str
    suitable_for: List[str]


class SpreadRecommendRequest(BaseModel):
    """牌阵推荐请求"""
    question_type: str = Field(..., description="问题类型：love/career/general/decision/daily")
    complexity: str = Field("medium", description="复杂度：simple/medium/complex")


def _card_to_response(card) -> CardResponse:
    """将TarotCard转换为CardResponse"""
    return CardResponse(
        code=card.code,
        name=card.name,
        name_en=card.name_en,
        number=card.number,
        suit=card.suit.value,
        element=card.element,
        keywords=card.keywords,
        upright_meaning=card.upright_meaning,
        reversed_meaning=card.reversed_meaning,
        image_desc=card.image_desc,
        advice=card.advice
    )


@router.get("/cards")
async def list_all_cards(include_minor: bool = False):
    """获取塔罗牌列表
    
    - **include_minor**: 是否包含小阿尔卡那（默认仅返回22张大阿尔卡那）
    """
    major_cards = get_all_major_arcana()
    
    if include_minor:
        minor_cards = get_all_minor_arcana()
        all_cards = major_cards + minor_cards
        return {
            "total": len(all_cards),
            "major_count": len(major_cards),
            "minor_count": len(minor_cards),
            "cards": [_card_to_response(c) for c in all_cards]
        }
    
    return {
        "total": len(major_cards),
        "cards": [_card_to_response(c) for c in major_cards]
    }


@router.get("/cards/minor")
async def list_minor_cards(suit: Optional[str] = None):
    """获取小阿尔卡那牌列表
    
    - **suit**: 按牌组筛选 (wands/cups/swords/pentacles)
    """
    if suit:
        suit_upper = suit.upper()
        try:
            card_suit = CardSuit(suit_upper)
            cards = get_cards_by_suit(card_suit)
            return {
                "suit": suit_upper,
                "suit_name": {"WANDS": "权杖", "CUPS": "圣杯", "SWORDS": "宝剑", "PENTACLES": "星币"}.get(suit_upper, suit),
                "total": len(cards),
                "cards": [_card_to_response(c) for c in cards]
            }
        except ValueError:
            raise HTTPException(status_code=400, detail=f"无效的牌组: {suit}，可选值: wands/cups/swords/pentacles")
    
    cards = get_all_minor_arcana()
    return {
        "total": len(cards),
        "suits": [
            {"code": "WANDS", "name": "权杖", "element": "火", "count": 14},
            {"code": "CUPS", "name": "圣杯", "element": "水", "count": 14},
            {"code": "SWORDS", "name": "宝剑", "element": "风", "count": 14},
            {"code": "PENTACLES", "name": "星币", "element": "土", "count": 14},
        ],
        "cards": [_card_to_response(c) for c in cards]
    }


@router.get("/cards/{code}")
async def get_card(code: str):
    """获取单张牌的详细信息（支持大/小阿尔卡那）"""
    code_upper = code.upper()
    
    # 先查大阿尔卡那
    card = get_card_by_code(code_upper)
    
    # 再查小阿尔卡那
    if not card:
        card = get_minor_card_by_code(code_upper)
    
    if not card:
        raise HTTPException(status_code=404, detail=f"未找到牌: {code}")
    
    return _card_to_response(card)


@router.get("/spreads")
async def list_all_spreads():
    """获取所有牌阵"""
    spreads = get_all_spreads()
    return {
        "total": len(spreads),
        "spreads": [
            SpreadResponse(
                code=s.code,
                name=s.name,
                name_en=s.name_en,
                positions=[
                    SpreadPositionResponse(
                        index=p.index,
                        name=p.name,
                        description=p.description
                    ) for p in s.positions
                ],
                description=s.description,
                suitable_for=s.suitable_for
            ) for s in spreads
        ]
    }


@router.get("/spreads/{code}")
async def get_spread(code: str):
    """获取单个牌阵详情"""
    spread = get_spread_by_code(code.lower())
    if not spread:
        raise HTTPException(status_code=404, detail=f"未找到牌阵: {code}")
    
    return SpreadResponse(
        code=spread.code,
        name=spread.name,
        name_en=spread.name_en,
        positions=[
            SpreadPositionResponse(
                index=p.index,
                name=p.name,
                description=p.description
            ) for p in spread.positions
        ],
        description=spread.description,
        suitable_for=spread.suitable_for
    )


@router.post("/spreads/recommend")
async def recommend_spread(request: SpreadRecommendRequest):
    """根据问题类型推荐牌阵"""
    question_type = request.question_type.lower()
    complexity = request.complexity.lower()
    
    # 推荐逻辑
    recommendations = []
    
    if question_type == "love":
        recommendations.append("love_cross")
        if complexity != "simple":
            recommendations.append("celtic_cross")
    elif question_type == "daily":
        recommendations.append("single_card")
        recommendations.append("three_card")
    elif question_type == "decision":
        recommendations.append("three_card")
        recommendations.append("horseshoe")
    else:  # general or career
        if complexity == "simple":
            recommendations.append("single_card")
            recommendations.append("three_card")
        elif complexity == "medium":
            recommendations.append("three_card")
            recommendations.append("horseshoe")
        else:
            recommendations.append("horseshoe")
            recommendations.append("celtic_cross")
    
    # 获取推荐牌阵详情
    result = []
    for code in recommendations:
        spread = get_spread_by_code(code)
        if spread:
            result.append({
                "code": spread.code,
                "name": spread.name,
                "card_count": len(spread.positions),
                "description": spread.description,
                "reason": get_recommendation_reason(code, question_type, complexity)
            })
    
    return {
        "question_type": question_type,
        "complexity": complexity,
        "recommendations": result
    }


def get_recommendation_reason(spread_code: str, question_type: str, complexity: str) -> str:
    """获取推荐理由"""
    reasons = {
        "single_card": "快速简洁，适合每日指引或简单问题",
        "three_card": "经典牌阵，展示过去-现在-未来的时间线",
        "love_cross": "专门针对感情问题设计，分析双方状态和关系发展",
        "horseshoe": "七张牌提供全面视角，包含建议和隐藏因素",
        "celtic_cross": "最全面的牌阵，深度剖析问题的各个层面",
    }
    return reasons.get(spread_code, "适合当前问题类型")


@router.get("/interpretation-guide")
async def get_interpretation_guide():
    """获取塔罗牌解读指南"""
    return {
        "upright_principles": [
            "能量正面、顺遂、显性表达",
            "代表事物的直接含义",
            "能量正常流动",
        ],
        "reversed_principles": [
            "能量受阻、延迟、隐性表达",
            "可能代表内在化的能量",
            "可能表示过度或不足",
            "需要结合具体牌意，不是简单的'坏牌'",
        ],
        "reading_steps": [
            "1. 了解问卜者的问题",
            "2. 选择合适的牌阵",
            "3. 洗牌并抽取牌",
            "4. 逐张解读每个位置的牌",
            "5. 分析牌与牌之间的关联",
            "6. 给出整体解读和建议",
        ],
        "elements_correspondence": {
            "火": "权杖牌组 - 行动、热情、创造力",
            "水": "圣杯牌组 - 情感、直觉、关系",
            "风": "宝剑牌组 - 思想、沟通、冲突",
            "土": "星币牌组 - 物质、实际、财务",
        },
        "structured_reading_flow": {
            "description": "结构化解读流程（参考tarot-ai-agent设计）",
            "steps": [
                {"step": 1, "name": "逐张解读", "desc": "对每张牌在其位置上的含义进行独立解读"},
                {"step": 2, "name": "牌面关系", "desc": "分析牌与牌之间的相生、相克、互补等关系"},
                {"step": 3, "name": "整体叙述", "desc": "综合所有信息给出流畅的整体解读"},
                {"step": 4, "name": "行动建议", "desc": "给出具体可行的行动建议和注意事项"},
            ]
        }
    }


class StructuredReadingRequest(BaseModel):
    """结构化解读请求"""
    question: str = Field(..., description="问卜问题")
    spread_code: str = Field(..., description="牌阵代码")
    drawn_cards: List[Dict[str, Any]] = Field(..., description="抽取的牌列表")


class DrawnCardInfo(BaseModel):
    """抽取的牌信息"""
    card_code: str
    is_upright: bool = True
    position_index: int


@router.post("/structured-reading/prompt")
async def get_structured_reading_prompt(request: StructuredReadingRequest):
    """
    获取结构化解读提示词
    
    返回构建好的提示词，供前端调用AI服务使用
    """
    from ..divination.tarot.interpreter import create_structured_reading_prompt
    
    # 获取牌阵信息
    spread = get_spread_by_code(request.spread_code)
    if not spread:
        raise HTTPException(status_code=404, detail=f"未找到牌阵: {request.spread_code}")
    
    # 构建牌面信息
    cards_info = []
    for card_data in request.drawn_cards:
        card_code = card_data.get("card_code", "")
        is_upright = card_data.get("is_upright", True)
        position_index = card_data.get("position_index", 0)
        
        # 获取牌信息
        card = get_card_by_code(card_code)
        if not card:
            card = get_minor_card_by_code(card_code)
        
        if not card:
            raise HTTPException(status_code=404, detail=f"未找到牌: {card_code}")
        
        # 获取位置信息
        if position_index < len(spread.positions):
            position = spread.positions[position_index]
            position_name = position.name
            position_meaning = position.description
        else:
            position_name = f"位置{position_index + 1}"
            position_meaning = ""
        
        cards_info.append({
            "card_code": card_code,
            "card_name": card.name,
            "is_upright": is_upright,
            "card_meaning": card.upright_meaning if is_upright else card.reversed_meaning,
            "position_name": position_name,
            "position_meaning": position_meaning,
        })
    
    # 生成提示词
    prompt = create_structured_reading_prompt(
        question=request.question,
        spread_name=spread.name,
        cards=cards_info
    )
    
    return {
        "prompt": prompt,
        "spread": {
            "code": spread.code,
            "name": spread.name,
            "card_count": len(spread.positions)
        },
        "cards": cards_info,
        "reading_structure": {
            "sections": ["逐张解读", "牌面关系分析", "整体叙述", "行动建议", "注意事项", "开运指引"]
        }
    }
