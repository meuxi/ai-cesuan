"""
通用模块
"""
from .response import (
    ApiResponse,
    ResponseCode,
    PagedData,
    PagedResponse,
    ok,
    fail,
)

__all__ = [
    'ApiResponse',
    'ResponseCode',
    'PagedData',
    'PagedResponse',
    'ok',
    'fail',
]
