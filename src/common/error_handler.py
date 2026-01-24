"""
统一错误处理工具

提供统一的异常处理函数，简化路由中的错误处理代码
"""

import logging
from typing import Callable, TypeVar, Any
from functools import wraps

from fastapi import HTTPException, status

from src.exceptions import (
    DivinationException,
    InvalidInputError,
    APICallError,
    ServiceUnavailableError,
)

_logger = logging.getLogger(__name__)

T = TypeVar('T')


def handle_route_error(error: Exception, operation: str = "操作") -> None:
    """
    统一处理路由异常
    
    Args:
        error: 捕获的异常
        operation: 操作描述，用于日志和错误消息
    
    Raises:
        DivinationException: 已知的业务异常，直接重新抛出
        HTTPException: 对于未知异常，包装成友好的错误消息
    """
    # 已知的业务异常，直接抛出
    if isinstance(error, DivinationException):
        raise error
    
    # HTTPException 直接抛出
    if isinstance(error, HTTPException):
        raise error
    
    # ValueError 转换为输入错误
    if isinstance(error, ValueError):
        _logger.warning(f"{operation}参数错误: {error}")
        raise InvalidInputError(message=str(error))
    
    # 超时错误
    if isinstance(error, TimeoutError):
        _logger.error(f"{operation}超时: {error}")
        raise ServiceUnavailableError(message=f"{operation}超时，请稍后重试")
    
    # 未知错误，记录详细日志但返回友好消息
    _logger.error(f"{operation}失败: {type(error).__name__}: {error}", exc_info=True)
    raise APICallError(message=f"{operation}失败，请稍后重试")


def safe_api_call(operation: str = "操作"):
    """
    路由异常处理装饰器
    
    用法:
        @router.post("/example")
        @safe_api_call("获取数据")
        async def example_endpoint():
            ...
    
    Args:
        operation: 操作描述
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except DivinationException:
                raise
            except HTTPException:
                raise
            except Exception as e:
                handle_route_error(e, operation)
        return wrapper
    return decorator


def format_error_response(error: Exception) -> dict:
    """
    格式化错误响应（供全局异常处理器使用）
    
    Args:
        error: 异常对象
    
    Returns:
        格式化的错误响应字典
    """
    if isinstance(error, DivinationException):
        return {
            "success": False,
            "error": {
                "code": error.code,
                "message": error.message,
            }
        }
    
    if isinstance(error, HTTPException):
        return {
            "success": False,
            "error": {
                "code": "HTTP_ERROR",
                "message": error.detail if isinstance(error.detail, str) else str(error.detail),
            }
        }
    
    return {
        "success": False,
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "服务器内部错误，请稍后重试",
        }
    }
