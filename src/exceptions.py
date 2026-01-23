"""
占卜业务统一异常模块

提供统一的错误码和异常类，便于前后端错误处理
"""

from fastapi import HTTPException, status


class DivinationException(HTTPException):
    """占卜业务异常基类"""
    
    code: str = "DIVINATION_ERROR"
    message: str = "占卜服务异常"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def __init__(self, message: str = None, code: str = None, status_code: int = None):
        self.code = code or self.code
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        
        super().__init__(
            status_code=self.status_code,
            detail={
                "code": self.code,
                "message": self.message
            }
        )


class InvalidDivinationTypeError(DivinationException):
    """不支持的占卜类型"""
    code = "INVALID_DIVINATION_TYPE"
    message = "不支持的占卜类型"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidInputError(DivinationException):
    """输入参数错误"""
    code = "INVALID_INPUT"
    message = "输入参数错误"
    status_code = status.HTTP_400_BAD_REQUEST


class StopWordDetectedError(DivinationException):
    """检测到停止词"""
    code = "STOP_WORD_DETECTED"
    message = "输入包含禁止词汇"
    status_code = status.HTTP_403_FORBIDDEN


class RateLimitExceededError(DivinationException):
    """请求频率限制"""
    code = "RATE_LIMIT_EXCEEDED"
    message = "请求过于频繁，请稍后再试"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class APIConfigError(DivinationException):
    """API配置错误"""
    code = "API_CONFIG_ERROR"
    message = "API配置错误，请检查设置"
    status_code = status.HTTP_403_FORBIDDEN


class APICallError(DivinationException):
    """API调用失败"""
    code = "API_CALL_ERROR"
    message = "AI服务调用失败"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ZhipuConcurrencyError(DivinationException):
    """智谱AI并发限制"""
    code = "ZHIPU_CONCURRENCY_ERROR"
    message = "智谱AI并发请求过多，请稍后再试（建议间隔3-5秒）"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class BirthdayFormatError(DivinationException):
    """生日格式错误"""
    code = "BIRTHDAY_FORMAT_ERROR"
    message = "生日格式错误，请使用格式：YYYY-MM-DD HH:MM:SS"
    status_code = status.HTTP_400_BAD_REQUEST


class NameLengthError(DivinationException):
    """姓名长度错误"""
    code = "NAME_LENGTH_ERROR"
    message = "姓名长度应为2-10个字"
    status_code = status.HTTP_400_BAD_REQUEST


class EmptyPromptError(DivinationException):
    """问题为空"""
    code = "EMPTY_PROMPT"
    message = "问题不能为空"
    status_code = status.HTTP_400_BAD_REQUEST


class TimeoutError(DivinationException):
    """API超时错误"""
    code = "API_TIMEOUT"
    message = "AI服务响应超时，请稍后重试"
    status_code = status.HTTP_504_GATEWAY_TIMEOUT


class AuthenticationError(DivinationException):
    """认证失败"""
    code = "AUTHENTICATION_ERROR"
    message = "认证失败，请检查API密钥"
    status_code = status.HTTP_401_UNAUTHORIZED


class DataValidationError(DivinationException):
    """数据验证失败"""
    code = "DATA_VALIDATION_ERROR"
    message = "数据验证失败"
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class ServiceUnavailableError(DivinationException):
    """服务不可用"""
    code = "SERVICE_UNAVAILABLE"
    message = "服务暂时不可用，请稍后重试"
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class QuotaExceededError(DivinationException):
    """配额超限"""
    code = "QUOTA_EXCEEDED"
    message = "今日使用次数已达上限"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


# 错误码映射表（供前端使用）
ERROR_CODES = {
    "DIVINATION_ERROR": "占卜服务异常",
    "INVALID_DIVINATION_TYPE": "不支持的占卜类型",
    "INVALID_INPUT": "输入参数错误",
    "STOP_WORD_DETECTED": "输入包含禁止词汇",
    "RATE_LIMIT_EXCEEDED": "请求过于频繁，请稍后再试",
    "API_CONFIG_ERROR": "API配置错误，请检查设置",
    "API_CALL_ERROR": "AI服务调用失败",
    "API_TIMEOUT": "AI服务响应超时",
    "AUTHENTICATION_ERROR": "认证失败",
    "DATA_VALIDATION_ERROR": "数据验证失败",
    "SERVICE_UNAVAILABLE": "服务暂时不可用",
    "QUOTA_EXCEEDED": "今日使用次数已达上限",
    "ZHIPU_CONCURRENCY_ERROR": "智谱AI并发请求过多，请稍后再试",
    "BIRTHDAY_FORMAT_ERROR": "生日格式错误",
    "NAME_LENGTH_ERROR": "姓名长度错误",
    "EMPTY_PROMPT": "问题不能为空",
}
