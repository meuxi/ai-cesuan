"""
诸葛神算模块
基于三字笔画计算384爻签文
"""
from .zhuge import ZhugeService, zhuge_service
from .types import ZhugeInput, ZhugeResult

__all__ = [
    'ZhugeService',
    'zhuge_service',
    'ZhugeInput',
    'ZhugeResult',
]
