"""
星座配对
提供星座之间的配对分析
"""

from typing import Dict, Any, List, Tuple


# 元素相生相克
ELEMENT_COMPATIBILITY = {
    ('火', '火'): {'score': 75, 'desc': '同为火象，热情相投但容易冲突'},
    ('火', '土'): {'score': 60, 'desc': '火土相克，需要磨合适应'},
    ('火', '风'): {'score': 90, 'desc': '风助火势，相互促进'},
    ('火', '水'): {'score': 50, 'desc': '水火相克，差异较大'},
    ('土', '土'): {'score': 80, 'desc': '同为土象，稳定踏实'},
    ('土', '风'): {'score': 55, 'desc': '土风相异，观念不同'},
    ('土', '水'): {'score': 75, 'desc': '水润土肥，相互滋养'},
    ('风', '风'): {'score': 70, 'desc': '同为风象，思想共鸣但不够稳定'},
    ('风', '水'): {'score': 65, 'desc': '风水相济，有好有坏'},
    ('水', '水'): {'score': 85, 'desc': '同为水象，心灵相通'},
}

# 星座元素映射
ZODIAC_ELEMENT = {
    '白羊座': '火', '金牛座': '土', '双子座': '风', '巨蟹座': '水',
    '狮子座': '火', '处女座': '土', '天秤座': '风', '天蝎座': '水',
    '射手座': '火', '摩羯座': '土', '水瓶座': '风', '双鱼座': '水',
}

# 特殊配对（基于传统星座学）
SPECIAL_PAIRS: Dict[Tuple[str, str], Dict[str, Any]] = {
    ('白羊座', '狮子座'): {'score': 95, 'desc': '绝配！两个火象星座充满激情'},
    ('金牛座', '处女座'): {'score': 92, 'desc': '土象绝配，务实稳定'},
    ('双子座', '天秤座'): {'score': 90, 'desc': '风象绝配，心灵相通'},
    ('巨蟹座', '双鱼座'): {'score': 93, 'desc': '水象绝配，情感深厚'},
    ('狮子座', '射手座'): {'score': 91, 'desc': '火象绝配，热情奔放'},
    ('处女座', '摩羯座'): {'score': 88, 'desc': '土象绝配，事业伙伴'},
    ('天秤座', '水瓶座'): {'score': 89, 'desc': '风象绝配，思想共鸣'},
    ('天蝎座', '巨蟹座'): {'score': 94, 'desc': '水象绝配，深情专一'},
    ('白羊座', '天秤座'): {'score': 85, 'desc': '对宫星座，互补吸引'},
    ('金牛座', '天蝎座'): {'score': 82, 'desc': '对宫星座，深层吸引'},
    ('双子座', '射手座'): {'score': 80, 'desc': '对宫星座，自由灵魂'},
    ('巨蟹座', '摩羯座'): {'score': 78, 'desc': '对宫星座，家庭事业平衡'},
}


def get_zodiac_compatibility(zodiac1: str, zodiac2: str) -> Dict[str, Any]:
    """
    获取两个星座的配对分析
    
    Args:
        zodiac1: 第一个星座
        zodiac2: 第二个星座
        
    Returns:
        配对分析结果
    """
    # 获取元素
    element1 = ZODIAC_ELEMENT.get(zodiac1, '火')
    element2 = ZODIAC_ELEMENT.get(zodiac2, '火')
    
    # 检查特殊配对
    pair = (zodiac1, zodiac2)
    reverse_pair = (zodiac2, zodiac1)
    
    if pair in SPECIAL_PAIRS:
        special = SPECIAL_PAIRS[pair]
        base_score = special['score']
        special_desc = special['desc']
    elif reverse_pair in SPECIAL_PAIRS:
        special = SPECIAL_PAIRS[reverse_pair]
        base_score = special['score']
        special_desc = special['desc']
    else:
        special_desc = None
        # 使用元素配对
        element_pair = (element1, element2)
        reverse_element_pair = (element2, element1)
        
        if element_pair in ELEMENT_COMPATIBILITY:
            base_score = ELEMENT_COMPATIBILITY[element_pair]['score']
        elif reverse_element_pair in ELEMENT_COMPATIBILITY:
            base_score = ELEMENT_COMPATIBILITY[reverse_element_pair]['score']
        else:
            base_score = 70
    
    # 计算各维度配对
    love_score = _calculate_dimension_score(zodiac1, zodiac2, 'love', base_score)
    friendship_score = _calculate_dimension_score(zodiac1, zodiac2, 'friendship', base_score)
    work_score = _calculate_dimension_score(zodiac1, zodiac2, 'work', base_score)
    communication_score = _calculate_dimension_score(zodiac1, zodiac2, 'communication', base_score)
    
    # 生成配对分析
    analysis = _generate_compatibility_analysis(
        zodiac1, zodiac2, element1, element2, 
        base_score, love_score, work_score
    )
    
    # 配对建议
    advice = _generate_compatibility_advice(
        zodiac1, zodiac2, base_score, 
        love_score, communication_score
    )
    
    return {
        'zodiac1': zodiac1,
        'zodiac2': zodiac2,
        'element1': element1,
        'element2': element2,
        'overall_score': base_score,
        'scores': {
            'love': love_score,
            'friendship': friendship_score,
            'work': work_score,
            'communication': communication_score,
        },
        'special_note': special_desc,
        'analysis': analysis,
        'advice': advice,
        'rating': _get_rating(base_score),
    }


def _calculate_dimension_score(zodiac1: str, zodiac2: str, dimension: str, base: int) -> int:
    """计算特定维度的配对分数"""
    # 基于两个星座名的hash值生成稳定的随机偏移
    import hashlib
    seed = hashlib.md5(f"{zodiac1}{zodiac2}{dimension}".encode()).hexdigest()
    offset = int(seed[:4], 16) % 20 - 10  # -10 到 +10 的偏移
    
    score = base + offset
    return max(40, min(98, score))


def _generate_compatibility_analysis(
    zodiac1: str, zodiac2: str,
    element1: str, element2: str,
    overall: int, love: int, work: int
) -> Dict[str, str]:
    """生成配对分析"""
    
    if element1 == element2:
        element_analysis = f'{zodiac1}与{zodiac2}同属{element1}象星座，有着相似的性格特质和处事方式，容易产生共鸣。'
    else:
        element_analysis = f'{zodiac1}({element1}象)与{zodiac2}({element2}象)属于不同元素，性格互补，需要相互理解。'
    
    if overall >= 85:
        overall_analysis = '这是一对非常般配的组合，彼此能够深入理解和支持对方。'
    elif overall >= 70:
        overall_analysis = '这对组合有着不错的默契，经营得当会是美好的缘分。'
    elif overall >= 55:
        overall_analysis = '这对组合需要双方付出更多努力来理解彼此的差异。'
    else:
        overall_analysis = '这对组合存在较大差异，需要很多磨合和包容。'
    
    return {
        'element': element_analysis,
        'overall': overall_analysis,
        'love': f'爱情指数{love}分，' + ('感情上容易擦出火花。' if love >= 75 else '需要更多耐心经营感情。'),
        'work': f'合作指数{work}分，' + ('工作上是很好的搭档。' if work >= 75 else '工作中需要磨合配合方式。'),
    }


def _generate_compatibility_advice(
    zodiac1: str, zodiac2: str,
    overall: int, love: int, communication: int
) -> List[str]:
    """生成配对建议"""
    advice = []
    
    if overall >= 80:
        advice.append('你们的配对非常和谐，珍惜这份缘分')
    elif overall < 60:
        advice.append('虽然存在差异，但爱可以跨越一切，关键在于理解和包容')
    
    if communication < 70:
        advice.append('多花时间进行深入的沟通交流')
    
    if love >= 80:
        advice.append('感情方面很有潜力，大胆表达你的心意')
    
    # 根据星座特性添加建议
    zodiac_advice = {
        '白羊座': '给予对方足够的空间和自由',
        '金牛座': '理解对方对稳定的需求',
        '双子座': '保持新鲜感和有趣的互动',
        '巨蟹座': '给予对方安全感和温暖',
        '狮子座': '欣赏和赞美对方的优点',
        '处女座': '接受对方的完美主义倾向',
        '天秤座': '共同创造和谐的氛围',
        '天蝎座': '建立深厚的信任基础',
        '射手座': '一起探索世界和新事物',
        '摩羯座': '支持对方的事业追求',
        '水瓶座': '尊重对方的独立性',
        '双鱼座': '理解对方的敏感和浪漫',
    }
    
    if zodiac2 in zodiac_advice:
        advice.append(zodiac_advice[zodiac2])
    
    return advice[:4]


def _get_rating(score: int) -> str:
    """获取配对评级"""
    if score >= 90:
        return '天作之合'
    elif score >= 80:
        return '非常般配'
    elif score >= 70:
        return '比较和谐'
    elif score >= 60:
        return '需要磨合'
    else:
        return '差异较大'
