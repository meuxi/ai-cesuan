"""
快速问题模板配置
用于各类占卜的常见问题预设

数据来源：zhouwenwang quickQuestions.ts
"""
from typing import List, Dict, Literal
import random


# 快速问题类型
QuestionType = Literal['liuyao', 'qimen', 'tarot', 'bazi', 'ziwei', 'palmistry', 'zhougong']


# 快速问题配置
QUICK_QUESTIONS: Dict[QuestionType, List[str]] = {
    'liuyao': [
        '今年运势怎么样？',
        '近期财运如何？',
        '什么时候能遇到真爱？',
        '与朋友的合作会顺利吗？',
        '我的事业会有突破吗？',
        '这次投资能赚钱吗？',
        '我和TA有缘分吗？',
        '家人身体健康吗？',
        '应该换工作吗？',
        '今年适合买房吗？',
        '孩子的学业如何？',
        '出国发展好吗？',
        '这件事能成功吗？',
        '最近的困难何时能过去？',
        '和对方谈判能成功吗？',
    ],
    'qimen': [
        '今年事业发展如何？',
        '近期财运怎么样？',
        '什么时候能遇到合适的人？',
        '当前决策是否正确？',
        '这个项目能成功吗？',
        '应该投资这个机会吗？',
        '搬家的时机合适吗？',
        '与合作伙伴关系如何？',
        '官司能打赢吗？',
        '出行是否顺利？',
        '求学之路如何？',
        '健康方面需要注意什么？',
        '失物能找回来吗？',
        '跳槽的时机对吗？',
        '今天适合签约吗？',
    ],
    'tarot': [
        '我和TA的关系会如何发展？',
        '近期我的感情运势如何？',
        '这份工作适合我吗？',
        '我应该做出改变吗？',
        '我们之间还有可能吗？',
        '我该如何处理目前的困境？',
        '对方是怎么看我的？',
        '未来三个月我的运势如何？',
        '我应该接受这个机会吗？',
        '什么在阻碍我前进？',
        '如何改善我的财务状况？',
        '我该如何找到内心的平静？',
    ],
    'bazi': [
        '我今年的整体运势如何？',
        '我的事业发展方向是什么？',
        '什么时候是我的桃花年？',
        '我适合做什么行业？',
        '我的财运何时会好转？',
        '我的婚姻运势如何？',
        '今年有贵人相助吗？',
        '我应该注意哪些健康问题？',
        '什么方位对我有利？',
        '我的子女运如何？',
    ],
    'ziwei': [
        '我的命宫主星是什么？',
        '我的事业宫显示什么信息？',
        '我的财帛宫情况如何？',
        '我的夫妻宫预示什么？',
        '我今年的流年运势如何？',
        '我的迁移宫对出行有何影响？',
        '我的福德宫显示什么？',
        '我的田宅宫对置产有何建议？',
    ],
    'palmistry': [
        '看看我的运势如何？',
        '我的事业线怎么样？',
        '感情线说明什么？',
        '财运好不好？',
        '健康方面有什么提示？',
        '我适合做什么工作？',
        '婚姻运势如何？',
        '有贵人相助吗？',
        '晚年生活怎么样？',
        '子女运势如何？',
        '我的性格特点是什么？',
        '需要注意哪些方面？',
    ],
    'zhougong': [
        '梦见蛇是什么意思？',
        '梦见死人说明什么？',
        '梦见水预示着什么？',
        '梦见考试失败怎么办？',
        '梦见飞翔代表什么？',
        '梦见迷路有何含义？',
        '梦见结婚是好事吗？',
        '梦见掉牙齿什么征兆？',
        '梦见老家的房子',
        '梦见已故的亲人',
        '梦见捡到钱财',
        '梦见被人追赶',
    ],
}


def get_random_questions(question_type: QuestionType, count: int = 3) -> List[str]:
    """
    从指定类型的问题列表中随机选择指定数量的问题
    
    Args:
        question_type: 占卜类型
        count: 选择数量，默认3个
        
    Returns:
        随机选择的问题数组
    """
    questions = QUICK_QUESTIONS.get(question_type, [])
    if not questions:
        return []
    
    if len(questions) <= count:
        return questions.copy()
    
    return random.sample(questions, count)


def get_all_questions(question_type: QuestionType) -> List[str]:
    """获取指定类型的所有问题"""
    return QUICK_QUESTIONS.get(question_type, []).copy()


def get_question_stats() -> Dict[str, int]:
    """获取所有类型的问题统计"""
    stats = {qtype: len(questions) for qtype, questions in QUICK_QUESTIONS.items()}
    stats['total'] = sum(stats.values())
    return stats


def add_custom_question(question_type: QuestionType, question: str) -> bool:
    """
    添加自定义问题
    
    Args:
        question_type: 占卜类型
        question: 问题内容
        
    Returns:
        是否添加成功
    """
    if question_type not in QUICK_QUESTIONS:
        return False
    
    if question not in QUICK_QUESTIONS[question_type]:
        QUICK_QUESTIONS[question_type].append(question)
        return True
    
    return False
