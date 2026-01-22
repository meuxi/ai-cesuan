"""
统一API响应格式
所有API统一返回 {code, data, message} 结构
"""
from typing import TypeVar, Generic, Optional, Any, Dict
from pydantic import BaseModel
from enum import IntEnum


class ResponseCode(IntEnum):
    """响应状态码"""
    SUCCESS = 0
    
    # 通用错误 1xxx
    UNKNOWN_ERROR = 1000
    INVALID_PARAMS = 1001
    RATE_LIMITED = 1002
    NOT_FOUND = 1003
    UNAUTHORIZED = 1004
    FORBIDDEN = 1005
    VALIDATION_ERROR = 1006
    REQUEST_TIMEOUT = 1007
    
    # 占卜业务错误 2xxx
    DIVINATION_FAILED = 2001
    AI_SERVICE_ERROR = 2002
    CALCULATION_ERROR = 2003
    TEMPLATE_NOT_FOUND = 2004
    INVALID_DATE = 2005
    INVALID_TIME = 2006
    INVALID_HEXAGRAM = 2007
    INVALID_BAZI = 2008
    INVALID_ZIWEI = 2009
    INVALID_QIMEN = 2010
    INVALID_TAROT = 2011
    INVALID_LIUYAO = 2012
    INVALID_PLUMFLOWER = 2013
    MASTER_NOT_FOUND = 2014
    
    # AI服务错误 25xx
    AI_PROVIDER_ERROR = 2500
    AI_TIMEOUT = 2501
    AI_RATE_LIMIT = 2502
    AI_INVALID_RESPONSE = 2503
    AI_CONTENT_FILTERED = 2504
    AI_MODEL_NOT_AVAILABLE = 2505
    
    # 外部服务错误 3xxx
    EXTERNAL_API_ERROR = 3001
    DATABASE_ERROR = 3002
    CACHE_ERROR = 3003
    FILE_ERROR = 3004


# 错误消息映射（中英文）
ERROR_MESSAGES: Dict[int, Dict[str, str]] = {
    ResponseCode.SUCCESS: {"zh": "成功", "en": "Success"},
    ResponseCode.UNKNOWN_ERROR: {"zh": "未知错误", "en": "Unknown error"},
    ResponseCode.INVALID_PARAMS: {"zh": "参数错误", "en": "Invalid parameters"},
    ResponseCode.RATE_LIMITED: {"zh": "请求过于频繁，请稍后重试", "en": "Rate limited, please try again later"},
    ResponseCode.NOT_FOUND: {"zh": "资源不存在", "en": "Resource not found"},
    ResponseCode.UNAUTHORIZED: {"zh": "未授权访问", "en": "Unauthorized"},
    ResponseCode.FORBIDDEN: {"zh": "禁止访问", "en": "Forbidden"},
    ResponseCode.VALIDATION_ERROR: {"zh": "数据验证失败", "en": "Validation failed"},
    ResponseCode.REQUEST_TIMEOUT: {"zh": "请求超时", "en": "Request timeout"},
    
    ResponseCode.DIVINATION_FAILED: {"zh": "占卜失败", "en": "Divination failed"},
    ResponseCode.AI_SERVICE_ERROR: {"zh": "AI服务异常", "en": "AI service error"},
    ResponseCode.CALCULATION_ERROR: {"zh": "计算错误", "en": "Calculation error"},
    ResponseCode.TEMPLATE_NOT_FOUND: {"zh": "提示词模板未找到", "en": "Prompt template not found"},
    ResponseCode.INVALID_DATE: {"zh": "日期格式错误", "en": "Invalid date format"},
    ResponseCode.INVALID_TIME: {"zh": "时间格式错误", "en": "Invalid time format"},
    ResponseCode.INVALID_HEXAGRAM: {"zh": "卦象数据无效", "en": "Invalid hexagram data"},
    ResponseCode.INVALID_BAZI: {"zh": "八字数据无效", "en": "Invalid BaZi data"},
    ResponseCode.INVALID_ZIWEI: {"zh": "紫微数据无效", "en": "Invalid Ziwei data"},
    ResponseCode.INVALID_QIMEN: {"zh": "奇门数据无效", "en": "Invalid Qimen data"},
    ResponseCode.INVALID_TAROT: {"zh": "塔罗数据无效", "en": "Invalid Tarot data"},
    ResponseCode.INVALID_LIUYAO: {"zh": "六爻数据无效", "en": "Invalid Liuyao data"},
    ResponseCode.INVALID_PLUMFLOWER: {"zh": "梅花易数数据无效", "en": "Invalid Plum Flower data"},
    ResponseCode.MASTER_NOT_FOUND: {"zh": "大师配置未找到", "en": "Master configuration not found"},
    
    ResponseCode.AI_PROVIDER_ERROR: {"zh": "AI提供商服务异常", "en": "AI provider error"},
    ResponseCode.AI_TIMEOUT: {"zh": "AI响应超时", "en": "AI response timeout"},
    ResponseCode.AI_RATE_LIMIT: {"zh": "AI服务调用频率超限", "en": "AI rate limit exceeded"},
    ResponseCode.AI_INVALID_RESPONSE: {"zh": "AI返回数据格式异常", "en": "Invalid AI response format"},
    ResponseCode.AI_CONTENT_FILTERED: {"zh": "内容被过滤", "en": "Content filtered"},
    ResponseCode.AI_MODEL_NOT_AVAILABLE: {"zh": "AI模型不可用", "en": "AI model not available"},
    
    ResponseCode.EXTERNAL_API_ERROR: {"zh": "外部服务调用失败", "en": "External API error"},
    ResponseCode.DATABASE_ERROR: {"zh": "数据库错误", "en": "Database error"},
    ResponseCode.CACHE_ERROR: {"zh": "缓存服务错误", "en": "Cache error"},
    ResponseCode.FILE_ERROR: {"zh": "文件操作错误", "en": "File operation error"},
}


def get_error_message(code: int, lang: str = "zh") -> str:
    """获取错误消息"""
    msg = ERROR_MESSAGES.get(code, ERROR_MESSAGES[ResponseCode.UNKNOWN_ERROR])
    return msg.get(lang, msg.get("zh", "未知错误"))


T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一API响应格式
    
    Usage:
        return ApiResponse.success(data=result)
        return ApiResponse.error(code=ResponseCode.INVALID_PARAMS, message="参数错误")
    """
    code: int = ResponseCode.SUCCESS
    data: Optional[T] = None
    message: str = "success"
    request_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "data": {"key": "value"},
                "message": "success",
                "request_id": "abc-123"
            }
        }
    
    @classmethod
    def success(cls, data: Any = None, message: str = "success", request_id: str = None):
        """成功响应"""
        return cls(code=ResponseCode.SUCCESS, data=data, message=message, request_id=request_id)
    
    @classmethod
    def error(
        cls, 
        code: ResponseCode = ResponseCode.UNKNOWN_ERROR, 
        message: str = None,
        data: Any = None,
        request_id: str = None,
        lang: str = "zh"
    ):
        """错误响应"""
        if message is None:
            message = get_error_message(code, lang)
        return cls(code=code, data=data, message=message, request_id=request_id)
    
    @classmethod
    def from_exception(cls, e: Exception, request_id: str = None, code: ResponseCode = None):
        """从异常创建响应"""
        error_code = code or ResponseCode.UNKNOWN_ERROR
        return cls(
            code=error_code,
            message=str(e),
            request_id=request_id
        )
    
    @classmethod
    def ai_error(cls, message: str = None, request_id: str = None, lang: str = "zh"):
        """AI服务错误响应"""
        return cls.error(
            code=ResponseCode.AI_SERVICE_ERROR,
            message=message or get_error_message(ResponseCode.AI_SERVICE_ERROR, lang),
            request_id=request_id
        )
    
    @classmethod
    def validation_error(cls, message: str = None, data: Any = None, request_id: str = None):
        """参数验证错误响应"""
        return cls.error(
            code=ResponseCode.VALIDATION_ERROR,
            message=message or get_error_message(ResponseCode.VALIDATION_ERROR),
            data=data,
            request_id=request_id
        )


class PagedData(BaseModel, Generic[T]):
    """分页数据结构"""
    items: list[T]
    total: int
    page: int = 1
    page_size: int = 20
    has_more: bool = False
    
    @property
    def total_pages(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size


class PagedResponse(ApiResponse[PagedData[T]], Generic[T]):
    """分页响应"""
    pass


# 便捷函数
def ok(data: Any = None, message: str = "success") -> dict:
    """返回成功响应（字典形式，适用于直接返回）"""
    return {"code": 0, "data": data, "message": message}


def fail(code: int = 1000, message: str = None, data: Any = None, lang: str = "zh") -> dict:
    """返回失败响应（字典形式）"""
    if message is None:
        message = get_error_message(code, lang)
    return {"code": code, "data": data, "message": message}


# 占卜相关便捷函数
def divination_error(message: str = None, lang: str = "zh") -> dict:
    """占卜失败响应"""
    return fail(ResponseCode.DIVINATION_FAILED, message, lang=lang)


def calculation_error(message: str = None, lang: str = "zh") -> dict:
    """计算错误响应"""
    return fail(ResponseCode.CALCULATION_ERROR, message, lang=lang)


def ai_error(message: str = None, lang: str = "zh") -> dict:
    """AI服务错误响应"""
    return fail(ResponseCode.AI_SERVICE_ERROR, message, lang=lang)
