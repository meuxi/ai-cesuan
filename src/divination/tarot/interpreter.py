"""
塔罗牌结构化解读服务
参考 tarot-ai-agent 的解读流程：逐张解读 → 牌面关系 → 整体叙述 → 行动建议
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class CardPosition(Enum):
    """牌位朝向"""
    UPRIGHT = "upright"      # 正位
    REVERSED = "reversed"    # 逆位


@dataclass
class DrawnCard:
    """抽出的牌"""
    code: str                           # 牌代码
    name: str                           # 牌名
    position: CardPosition              # 正/逆位
    spread_position: int                # 牌阵位置索引
    spread_position_name: str           # 牌阵位置名称
    spread_position_meaning: str        # 牌阵位置含义


@dataclass
class CardInterpretation:
    """单张牌解读"""
    card: DrawnCard
    core_meaning: str                   # 核心含义
    position_context: str               # 结合位置的解读
    keywords: List[str]                 # 关键词
    energy_level: int = 5               # 能量等级 1-10


@dataclass
class CardRelation:
    """牌面关系"""
    card1_code: str
    card2_code: str
    relation_type: str                  # 相生/相克/互补/冲突/呼应
    description: str                    # 关系描述
    influence: str                      # 对问题的影响


@dataclass
class TarotReadingResult:
    """塔罗解读结果"""
    question: str                                           # 问卜问题
    question_type: str                                      # 问题类型
    spread_code: str                                        # 牌阵代码
    spread_name: str                                        # 牌阵名称
    drawn_cards: List[DrawnCard]                           # 抽出的牌
    card_interpretations: List[CardInterpretation]         # 逐张解读
    card_relations: List[CardRelation]                     # 牌面关系
    overall_narrative: str                                  # 整体叙述
    action_suggestions: List[str]                          # 行动建议
    cautions: List[str]                                    # 注意事项
    lucky_elements: Dict[str, str] = field(default_factory=dict)  # 开运元素
    summary_score: int = 5                                  # 总体评分 1-10


class TarotInterpreterPromptBuilder:
    """塔罗解读提示词构建器"""
    
    @staticmethod
    def build_system_prompt() -> str:
        """构建系统提示词"""
        return """你是一位专业的塔罗牌解读师，精通韦特塔罗牌78张牌的含义。
你的解读风格专业而温和，既能指出问题，也能给予希望和指引。

解读原则：
1. 正位代表能量顺畅流动、显性表达
2. 逆位代表能量受阻、隐性表达或过度/不足，不是简单的"坏牌"
3. 牌与牌之间存在关系，需要综合分析
4. 解读应结合问卜者的具体问题
5. 给出具体可行的建议，而非空泛的说教"""

    @staticmethod
    def build_card_interpretation_prompt(
        card: DrawnCard,
        question: str,
        card_info: Dict[str, Any]
    ) -> str:
        """构建单张牌解读提示词"""
        position_text = "正位" if card.position == CardPosition.UPRIGHT else "逆位"
        meaning = card_info.get("upright_meaning" if card.position == CardPosition.UPRIGHT else "reversed_meaning", "")
        
        return f"""请解读以下塔罗牌在特定位置的含义：

【问卜问题】{question}

【抽出的牌】
- 牌名：{card.name}（{position_text}）
- 牌阵位置：{card.spread_position_name}
- 位置含义：{card.spread_position_meaning}
- 牌义参考：{meaning}
- 关键词：{', '.join(card_info.get('keywords', []))}

请给出：
1. 核心含义（1-2句话）
2. 结合位置的具体解读（2-3句话）
3. 3个关键词
4. 能量等级（1-10分）

以JSON格式输出。"""

    @staticmethod
    def build_relation_analysis_prompt(
        cards: List[DrawnCard],
        card_infos: Dict[str, Dict[str, Any]],
        question: str
    ) -> str:
        """构建牌面关系分析提示词"""
        cards_desc = "\n".join([
            f"- {c.spread_position_name}: {c.name}（{'正位' if c.position == CardPosition.UPRIGHT else '逆位'}）"
            for c in cards
        ])
        
        return f"""请分析以下塔罗牌之间的关系：

【问卜问题】{question}

【牌面布局】
{cards_desc}

请分析牌与牌之间的关系（相生、相克、互补、冲突、呼应等），
每对重要关系给出：
1. 关系类型
2. 关系描述
3. 对问题的影响

以JSON数组格式输出，每个元素包含card1_code, card2_code, relation_type, description, influence字段。"""

    @staticmethod
    def build_overall_narrative_prompt(
        cards: List[DrawnCard],
        interpretations: List[CardInterpretation],
        relations: List[CardRelation],
        question: str,
        question_type: str
    ) -> str:
        """构建整体叙述提示词"""
        cards_summary = "\n".join([
            f"- {c.spread_position_name}: {c.name}（{'正位' if c.position == CardPosition.UPRIGHT else '逆位'}）- {interp.core_meaning}"
            for c, interp in zip(cards, interpretations)
        ])
        
        relations_summary = "\n".join([
            f"- {r.card1_code} 与 {r.card2_code}: {r.relation_type} - {r.description}"
            for r in relations
        ]) if relations else "无明显关系"
        
        return f"""请根据以下信息，给出完整的塔罗牌解读叙述：

【问卜问题】{question}
【问题类型】{question_type}

【各位置解读】
{cards_summary}

【牌面关系】
{relations_summary}

请给出：
1. 整体叙述（3-5段，流畅的叙事性文字）
2. 3-5条具体行动建议
3. 2-3条注意事项
4. 开运元素（颜色、数字、方位）
5. 总体评分（1-10分）

以JSON格式输出，包含overall_narrative, action_suggestions, cautions, lucky_elements, summary_score字段。"""


# 问题类型分类
QUESTION_TYPE_KEYWORDS = {
    "love": ["感情", "爱情", "恋爱", "婚姻", "伴侣", "对象", "暧昧", "分手", "复合", "桃花"],
    "career": ["工作", "事业", "职业", "升职", "跳槽", "面试", "创业", "项目", "同事", "老板"],
    "finance": ["财运", "金钱", "投资", "理财", "收入", "债务", "赚钱", "财富"],
    "health": ["健康", "身体", "疾病", "治疗", "康复", "运动"],
    "study": ["学习", "考试", "升学", "留学", "学业", "技能"],
    "decision": ["选择", "决定", "要不要", "该不该", "怎么办", "哪个"],
    "general": [],  # 默认类型
}


def classify_question(question: str) -> str:
    """根据问题内容分类"""
    for q_type, keywords in QUESTION_TYPE_KEYWORDS.items():
        if any(kw in question for kw in keywords):
            return q_type
    return "general"


# 牌面关系判断规则
ELEMENT_RELATIONS = {
    ("火", "火"): ("同元素", "能量叠加，强化特质"),
    ("水", "水"): ("同元素", "情感深化，直觉增强"),
    ("风", "风"): ("同元素", "思维活跃，沟通顺畅"),
    ("土", "土"): ("同元素", "稳固踏实，物质充实"),
    ("火", "风"): ("相生", "思想激发行动，创意蓬勃"),
    ("风", "火"): ("相生", "行动带动思考，突破局限"),
    ("水", "土"): ("相生", "情感滋养现实，感性与理性平衡"),
    ("土", "水"): ("相生", "现实基础支撑情感"),
    ("火", "水"): ("相克", "热情与情感可能冲突，需要平衡"),
    ("水", "火"): ("相克", "情感可能压制行动力"),
    ("风", "土"): ("相克", "理想与现实可能脱节"),
    ("土", "风"): ("相克", "过于务实可能限制思维"),
}


def analyze_element_relation(element1: str, element2: str) -> tuple:
    """分析两个元素之间的关系"""
    return ELEMENT_RELATIONS.get((element1, element2), ("中性", "各自发挥作用"))


# 结构化解读流程
class StructuredTarotInterpreter:
    """结构化塔罗解读器"""
    
    def __init__(self, ai_client=None):
        """
        初始化解读器
        
        Args:
            ai_client: AI客户端，需要有chat方法
        """
        self.ai_client = ai_client
        self.prompt_builder = TarotInterpreterPromptBuilder()
    
    def interpret(
        self,
        question: str,
        drawn_cards: List[DrawnCard],
        card_infos: Dict[str, Dict[str, Any]],
        spread_info: Dict[str, Any]
    ) -> TarotReadingResult:
        """
        执行结构化解读
        
        解读流程：
        1. 问题分类
        2. 逐张解读
        3. 牌面关系分析
        4. 整体叙述生成
        """
        # 1. 问题分类
        question_type = classify_question(question)
        
        # 2. 逐张解读
        card_interpretations = self._interpret_cards(
            drawn_cards, card_infos, question
        )
        
        # 3. 牌面关系分析
        card_relations = self._analyze_relations(
            drawn_cards, card_infos, question
        )
        
        # 4. 整体叙述生成
        overall_result = self._generate_overall(
            drawn_cards, card_interpretations, card_relations,
            question, question_type
        )
        
        return TarotReadingResult(
            question=question,
            question_type=question_type,
            spread_code=spread_info.get("code", ""),
            spread_name=spread_info.get("name", ""),
            drawn_cards=drawn_cards,
            card_interpretations=card_interpretations,
            card_relations=card_relations,
            overall_narrative=overall_result.get("overall_narrative", ""),
            action_suggestions=overall_result.get("action_suggestions", []),
            cautions=overall_result.get("cautions", []),
            lucky_elements=overall_result.get("lucky_elements", {}),
            summary_score=overall_result.get("summary_score", 5)
        )
    
    def _interpret_cards(
        self,
        cards: List[DrawnCard],
        card_infos: Dict[str, Dict[str, Any]],
        question: str
    ) -> List[CardInterpretation]:
        """逐张解读"""
        interpretations = []
        
        for card in cards:
            card_info = card_infos.get(card.code, {})
            
            # 基础解读（无AI时的回退方案）
            position_text = "正位" if card.position == CardPosition.UPRIGHT else "逆位"
            meaning_key = "upright_meaning" if card.position == CardPosition.UPRIGHT else "reversed_meaning"
            
            interpretation = CardInterpretation(
                card=card,
                core_meaning=card_info.get(meaning_key, f"{card.name}{position_text}"),
                position_context=f"在{card.spread_position_name}位置，{card_info.get(meaning_key, '')}",
                keywords=card_info.get("keywords", [])[:3],
                energy_level=7 if card.position == CardPosition.UPRIGHT else 5
            )
            
            interpretations.append(interpretation)
        
        return interpretations
    
    def _analyze_relations(
        self,
        cards: List[DrawnCard],
        card_infos: Dict[str, Dict[str, Any]],
        question: str
    ) -> List[CardRelation]:
        """分析牌面关系"""
        relations = []
        
        # 分析相邻牌的关系
        for i in range(len(cards) - 1):
            card1 = cards[i]
            card2 = cards[i + 1]
            
            info1 = card_infos.get(card1.code, {})
            info2 = card_infos.get(card2.code, {})
            
            element1 = info1.get("element", "")
            element2 = info2.get("element", "")
            
            if element1 and element2:
                rel_type, rel_desc = analyze_element_relation(element1, element2)
                
                relations.append(CardRelation(
                    card1_code=card1.code,
                    card2_code=card2.code,
                    relation_type=rel_type,
                    description=rel_desc,
                    influence=f"{card1.name}与{card2.name}的{rel_type}关系影响着问题的发展"
                ))
        
        return relations
    
    def _generate_overall(
        self,
        cards: List[DrawnCard],
        interpretations: List[CardInterpretation],
        relations: List[CardRelation],
        question: str,
        question_type: str
    ) -> Dict[str, Any]:
        """生成整体解读"""
        # 基础整体解读（无AI时的回退方案）
        cards_summary = "、".join([f"{c.name}({'正' if c.position == CardPosition.UPRIGHT else '逆'})" for c in cards])
        
        # 根据能量等级计算总分
        avg_energy = sum(i.energy_level for i in interpretations) / len(interpretations) if interpretations else 5
        
        return {
            "overall_narrative": f"针对您的问题「{question}」，抽取了{cards_summary}。综合来看，这组牌面显示了当前状况的多个层面。",
            "action_suggestions": [
                "保持开放的心态面对变化",
                "注意倾听内心的声音",
                "适时寻求他人的帮助和建议"
            ],
            "cautions": [
                "避免过于急躁做出决定",
                "注意情绪管理"
            ],
            "lucky_elements": {
                "颜色": "紫色",
                "数字": "7",
                "方位": "东方"
            },
            "summary_score": int(avg_energy)
        }


def create_structured_reading_prompt(
    question: str,
    spread_name: str,
    cards: List[Dict[str, Any]]
) -> str:
    """
    创建结构化解读的完整提示词
    
    用于前端或其他模块直接调用AI时使用
    """
    cards_desc = "\n".join([
        f"{i+1}. 【{c['position_name']}】{c['card_name']}（{'正位' if c['is_upright'] else '逆位'}）\n"
        f"   位置含义：{c['position_meaning']}\n"
        f"   牌义：{c['card_meaning']}"
        for i, c in enumerate(cards)
    ])
    
    return f"""# 塔罗牌解读请求

## 问卜信息
- **问题**：{question}
- **牌阵**：{spread_name}

## 抽取的牌
{cards_desc}

## 请按以下结构进行解读

### 一、逐张解读
对每张牌在其位置上的含义进行解读，包括：
- 核心含义（1-2句）
- 结合位置的具体解读（2-3句）

### 二、牌面关系分析
分析牌与牌之间的关系（相生、相克、互补、呼应等），
说明这些关系对问题的影响。

### 三、整体叙述
综合所有牌面信息，给出3-5段流畅的解读叙述，
要结合问卜者的具体问题进行分析。

### 四、行动建议
给出3-5条具体可行的建议。

### 五、注意事项
提醒2-3条需要注意的地方。

### 六、开运指引
- 幸运颜色：
- 幸运数字：
- 幸运方位：
- 总体评分：X/10

---
请以温和专业的语气进行解读，既要指出问题，也要给予希望和指引。
"""
