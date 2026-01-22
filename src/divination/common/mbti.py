"""
MBTI 性格测试核心库

包含16种人格类型定义、测试计算逻辑、维度描述

数据来源：MingAI src/lib/mbti.ts
"""
from typing import Dict, List, Optional, TypedDict
from enum import Enum


class Dimension(str, Enum):
    """MBTI 四个维度"""
    E = 'E'  # 外向
    I = 'I'  # 内向
    S = 'S'  # 实感
    N = 'N'  # 直觉
    T = 'T'  # 思考
    F = 'F'  # 情感
    J = 'J'  # 判断
    P = 'P'  # 知觉


# 16种人格类型
MBTI_TYPES = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP',
]


class PersonalityInfo(TypedDict):
    """人格基本信息"""
    name: str
    title: str
    emoji: str
    description: str


# 16种人格类型基本信息
PERSONALITY_BASICS: Dict[str, PersonalityInfo] = {
    'INTJ': {
        'name': 'INTJ',
        'title': '策略家',
        'emoji': '🧠',
        'description': '富有想象力和战略性的思想家，有着明确的计划',
    },
    'INTP': {
        'name': 'INTP',
        'title': '逻辑学家',
        'emoji': '🔬',
        'description': '创新型发明家，对知识有着永恒的渴望',
    },
    'ENTJ': {
        'name': 'ENTJ',
        'title': '指挥官',
        'emoji': '👔',
        'description': '大胆、富有想象力的领导者，总能找到或创造解决方案',
    },
    'ENTP': {
        'name': 'ENTP',
        'title': '辩论家',
        'emoji': '💡',
        'description': '聪明好奇的思想家，无法抵抗智力挑战',
    },
    'INFJ': {
        'name': 'INFJ',
        'title': '提倡者',
        'emoji': '🌟',
        'description': '安静而神秘的理想主义者，鼓舞人心',
    },
    'INFP': {
        'name': 'INFP',
        'title': '调停者',
        'emoji': '🌸',
        'description': '诗意、善良的利他主义者，总在寻求帮助他人',
    },
    'ENFJ': {
        'name': 'ENFJ',
        'title': '主人公',
        'emoji': '🎭',
        'description': '魅力四射的领导者，能够感染和激励听众',
    },
    'ENFP': {
        'name': 'ENFP',
        'title': '活动家',
        'emoji': '🎉',
        'description': '热情、创造性的自由精神，总能找到理由微笑',
    },
    'ISTJ': {
        'name': 'ISTJ',
        'title': '物流师',
        'emoji': '📋',
        'description': '实际且注重事实的人，可靠性不容置疑',
    },
    'ISFJ': {
        'name': 'ISFJ',
        'title': '守卫者',
        'emoji': '🛡️',
        'description': '非常专注和温暖的守护者，随时准备保护亲人',
    },
    'ESTJ': {
        'name': 'ESTJ',
        'title': '总经理',
        'emoji': '📊',
        'description': '卓越的管理者，在管理事务或人员方面无与伦比',
    },
    'ESFJ': {
        'name': 'ESFJ',
        'title': '执政官',
        'emoji': '👨‍👩‍👧‍👦',
        'description': '关心他人，社交且受欢迎，总是热心帮助',
    },
    'ISTP': {
        'name': 'ISTP',
        'title': '鉴赏家',
        'emoji': '🔧',
        'description': '勇敢而实际的实验者，掌握各种工具',
    },
    'ISFP': {
        'name': 'ISFP',
        'title': '探险家',
        'emoji': '🎨',
        'description': '灵活迷人的艺术家，随时准备探索和体验新事物',
    },
    'ESTP': {
        'name': 'ESTP',
        'title': '企业家',
        'emoji': '🚀',
        'description': '聪明、精力充沛的人，喜欢冒险',
    },
    'ESFP': {
        'name': 'ESFP',
        'title': '表演者',
        'emoji': '🎤',
        'description': '自发、精力充沛的表演者，生活永不无聊',
    },
}


# 维度描述
DIMENSION_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    'E': {'name': '外向', 'description': '从与他人互动中获取能量'},
    'I': {'name': '内向', 'description': '从独处和内省中获取能量'},
    'S': {'name': '实感', 'description': '关注实际和具体的信息'},
    'N': {'name': '直觉', 'description': '关注可能性和未来'},
    'T': {'name': '思考', 'description': '基于逻辑和客观分析做决定'},
    'F': {'name': '情感', 'description': '基于价值观和人际考量做决定'},
    'J': {'name': '判断', 'description': '喜欢有计划和有组织的生活'},
    'P': {'name': '知觉', 'description': '喜欢灵活和开放的生活方式'},
}


# Likert 量表权重映射 (1-7)
LIKERT_WEIGHTS = {
    1: {'a': 3, 'b': 0},  # 强烈同意A
    2: {'a': 2, 'b': 0},  # 同意A
    3: {'a': 1, 'b': 0},  # 略同意A
    4: {'a': 0, 'b': 0},  # 中立
    5: {'a': 0, 'b': 1},  # 略同意B
    6: {'a': 0, 'b': 2},  # 同意B
    7: {'a': 0, 'b': 3},  # 强烈同意B
}


class MBTIQuestion(TypedDict):
    """MBTI问题"""
    question: str
    choice_a: Dict[str, str]  # {'value': 'E', 'text': '...'}
    choice_b: Dict[str, str]


class TestAnswer(TypedDict):
    """测试答案"""
    question_index: int
    likert_value: int  # 1-7


class TestResult(TypedDict):
    """测试结果"""
    type: str
    scores: Dict[str, int]
    percentages: Dict[str, Dict[str, int]]


def get_personality_info(mbti_type: str) -> Optional[PersonalityInfo]:
    """获取人格类型基本信息"""
    return PERSONALITY_BASICS.get(mbti_type.upper())


def get_dimension_description(dimension: str) -> Optional[Dict[str, str]]:
    """获取维度描述"""
    return DIMENSION_DESCRIPTIONS.get(dimension.upper())


def calculate_result(questions: List[MBTIQuestion], answers: List[TestAnswer]) -> TestResult:
    """
    计算MBTI测试结果
    
    Args:
        questions: 问题列表
        answers: 答案列表（包含问题索引和Likert量表值1-7）
        
    Returns:
        测试结果，包含类型、分数和百分比
    """
    scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}
    
    for answer in answers:
        idx = answer['question_index']
        if idx >= len(questions):
            continue
            
        question = questions[idx]
        likert = answer['likert_value']
        
        if likert not in LIKERT_WEIGHTS:
            continue
            
        weights = LIKERT_WEIGHTS[likert]
        dim_a = question['choice_a']['value']
        dim_b = question['choice_b']['value']
        
        scores[dim_a] += weights['a']
        scores[dim_b] += weights['b']
    
    # 确定类型
    mbti_type = ''.join([
        'E' if scores['E'] >= scores['I'] else 'I',
        'S' if scores['S'] >= scores['N'] else 'N',
        'T' if scores['T'] >= scores['F'] else 'F',
        'J' if scores['J'] >= scores['P'] else 'P',
    ])
    
    # 计算百分比
    def calc_percent(a: int, b: int) -> Dict[str, int]:
        total = a + b
        if total == 0:
            return {'a': 50, 'b': 50}
        return {
            'a': round(a / total * 100),
            'b': round(b / total * 100),
        }
    
    ei = calc_percent(scores['E'], scores['I'])
    sn = calc_percent(scores['S'], scores['N'])
    tf = calc_percent(scores['T'], scores['F'])
    jp = calc_percent(scores['J'], scores['P'])
    
    return {
        'type': mbti_type,
        'scores': scores,
        'percentages': {
            'EI': {'E': ei['a'], 'I': ei['b']},
            'SN': {'S': sn['a'], 'N': sn['b']},
            'TF': {'T': tf['a'], 'F': tf['b']},
            'JP': {'J': jp['a'], 'P': jp['b']},
        },
    }


def is_valid_mbti_type(mbti_type: str) -> bool:
    """验证是否为有效的MBTI类型"""
    return mbti_type.upper() in MBTI_TYPES


def get_compatible_types(mbti_type: str) -> List[str]:
    """
    获取与指定类型相性较好的类型
    
    基于认知功能互补原则
    """
    compatibility_map = {
        'INTJ': ['ENFP', 'ENTP'],
        'INTP': ['ENTJ', 'ENFJ'],
        'ENTJ': ['INTP', 'INFP'],
        'ENTP': ['INTJ', 'INFJ'],
        'INFJ': ['ENTP', 'ENFP'],
        'INFP': ['ENTJ', 'ENFJ'],
        'ENFJ': ['INTP', 'INFP'],
        'ENFP': ['INTJ', 'INFJ'],
        'ISTJ': ['ESFP', 'ESTP'],
        'ISFJ': ['ESFP', 'ESTP'],
        'ESTJ': ['ISFP', 'ISTP'],
        'ESFJ': ['ISFP', 'ISTP'],
        'ISTP': ['ESFJ', 'ESTJ'],
        'ISFP': ['ESTJ', 'ESFJ'],
        'ESTP': ['ISFJ', 'ISTJ'],
        'ESFP': ['ISTJ', 'ISFJ'],
    }
    return compatibility_map.get(mbti_type.upper(), [])


# 导出
__all__ = [
    'Dimension',
    'MBTI_TYPES',
    'PERSONALITY_BASICS',
    'DIMENSION_DESCRIPTIONS',
    'LIKERT_WEIGHTS',
    'MBTIQuestion',
    'TestAnswer',
    'TestResult',
    'get_personality_info',
    'get_dimension_description',
    'calculate_result',
    'is_valid_mbti_type',
    'get_compatible_types',
]
