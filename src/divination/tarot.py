"""
塔罗牌占卜模块（兼容层）

注意：主要实现在 tarot/divination.py 中的 TarotDivination 类
此文件保留用于向后兼容，不再定义divination_type以避免冲突
"""
from src.models import DivinationBody
from src.exceptions import InvalidInputError


def get_tarot_system_prompt() -> str:
    """获取塔罗牌系统提示词"""
    from src.prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template("tarot_divination")
    if template:
        return template.system_prompt
    return "你是一位专业的塔罗牌占卜师。"


# TarotDivination 类已在 tarot/divination.py 中定义
# 此处不再重复定义，避免 divination_type='tarot' 冲突
