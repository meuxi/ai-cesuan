"""
提示词模板系统
参考 zhanwen 项目的 prompt-template.service.ts 设计
支持版本控制、分类管理、变量替换、效果评分
"""

from .models import PromptTemplate, PromptCategory, PromptStatus
from .manager import PromptTemplateManager, get_prompt_manager
from .templates import BUILTIN_TEMPLATES

__all__ = [
    "PromptTemplate",
    "PromptCategory",
    "PromptStatus",
    "PromptTemplateManager",
    "get_prompt_manager",
    "BUILTIN_TEMPLATES",
]
