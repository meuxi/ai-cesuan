"""
SSE (Server-Sent Events) 流式响应格式工具
统一前后端流式通信的数据格式

格式规范：
- 普通内容: data: "内容字符串"\n\n
- 错误消息: data: {"type":"error","code":"ERROR_CODE","message":"错误信息"}\n\n
- 结束标记: data: [DONE]\n\n
"""

import json
from typing import Optional, Dict, Any
from enum import Enum


class SSEErrorCode(str, Enum):
    """SSE 错误码"""
    STREAM_ERROR = "STREAM_ERROR"           # 流式传输错误
    TIMEOUT_ERROR = "TIMEOUT_ERROR"         # 超时错误
    PROVIDER_ERROR = "PROVIDER_ERROR"       # AI提供商错误
    RATE_LIMIT_ERROR = "RATE_LIMIT_ERROR"   # 频率限制错误
    AUTH_ERROR = "AUTH_ERROR"               # 认证错误
    CANCELLED = "CANCELLED"                 # 用户取消
    UNKNOWN_ERROR = "UNKNOWN_ERROR"         # 未知错误


class SSEMessage:
    """
    SSE 消息格式化工具
    
    使用示例:
        yield SSEMessage.data("这是一段内容")
        yield SSEMessage.error("发生错误", SSEErrorCode.STREAM_ERROR)
        yield SSEMessage.done()
    """
    
    @staticmethod
    def data(content: str) -> str:
        """
        普通数据消息
        
        Args:
            content: 内容字符串
            
        Returns:
            格式化的 SSE 数据行
        """
        return f"data: {json.dumps(content, ensure_ascii=False)}\n\n"
    
    @staticmethod
    def error(
        message: str, 
        code: SSEErrorCode = SSEErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        错误消息（统一格式）
        
        Args:
            message: 错误消息
            code: 错误码
            details: 额外的错误详情
            
        Returns:
            格式化的 SSE 错误数据行
        """
        error_obj: Dict[str, Any] = {
            "type": "error",
            "code": code.value if isinstance(code, SSEErrorCode) else code,
            "message": message,
        }
        if details:
            error_obj["details"] = details
        return f"data: {json.dumps(error_obj, ensure_ascii=False)}\n\n"
    
    @staticmethod
    def done() -> str:
        """
        结束标记
        
        Returns:
            SSE 结束标记
        """
        return "data: [DONE]\n\n"
    
    @staticmethod
    def event(event_name: str, data: Any) -> str:
        """
        自定义事件消息
        
        Args:
            event_name: 事件名称
            data: 事件数据
            
        Returns:
            格式化的 SSE 事件数据行
        """
        data_str = json.dumps(data, ensure_ascii=False) if not isinstance(data, str) else data
        return f"event: {event_name}\ndata: {data_str}\n\n"
    
    @staticmethod
    def reasoning(content: str) -> str:
        """
        推理内容（用于 DeepSeek R1 等支持推理过程的模型）
        
        Args:
            content: 推理内容
            
        Returns:
            格式化的 SSE 推理数据行
        """
        return f"data: {json.dumps({'type': 'reasoning', 'content': content}, ensure_ascii=False)}\n\n"
    
    @staticmethod
    def progress(current: int, total: int, message: str = "") -> str:
        """
        进度消息
        
        Args:
            current: 当前进度
            total: 总进度
            message: 进度说明
            
        Returns:
            格式化的 SSE 进度数据行
        """
        return f"data: {json.dumps({'type': 'progress', 'current': current, 'total': total, 'message': message}, ensure_ascii=False)}\n\n"


# 便捷函数
def sse_data(content: str) -> str:
    """普通数据消息的便捷函数"""
    return SSEMessage.data(content)


def sse_error(message: str, code: SSEErrorCode = SSEErrorCode.UNKNOWN_ERROR) -> str:
    """错误消息的便捷函数"""
    return SSEMessage.error(message, code)


def sse_done() -> str:
    """结束标记的便捷函数"""
    return SSEMessage.done()


# 常用响应头配置
SSE_HEADERS = {
    'Content-Type': 'text/event-stream; charset=utf-8',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Connection': 'keep-alive',
    'X-Accel-Buffering': 'no',  # 禁用 Nginx/Vercel 代理缓冲
}
