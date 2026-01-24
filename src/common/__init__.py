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
from .sse_response import (
    SSEMessage,
    SSEErrorCode,
    SSE_HEADERS,
    sse_data,
    sse_error,
    sse_done,
)
from .error_handler import (
    handle_route_error,
    safe_api_call,
    format_error_response,
)
from .api_utils import (
    normalize_api_key,
    get_api_config_from_request,
    validate_api_config,
)

__all__ = [
    # API 响应
    'ApiResponse',
    'ResponseCode',
    'PagedData',
    'PagedResponse',
    'ok',
    'fail',
    # SSE 流式响应
    'SSEMessage',
    'SSEErrorCode',
    'SSE_HEADERS',
    'sse_data',
    'sse_error',
    'sse_done',
    # 错误处理
    'handle_route_error',
    'safe_api_call',
    'format_error_response',
    # API 工具
    'normalize_api_key',
    'get_api_config_from_request',
    'validate_api_config',
]
