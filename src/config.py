import logging
import os
import secrets
from typing import Tuple

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)

# 安全配置常量
MIN_JWT_SECRET_LENGTH = 32  # JWT 密钥最小长度
WEAK_JWT_SECRETS = {"secret", "password", "123456", "jwt_secret", ""}  # 弱密钥黑名单


class Settings(BaseSettings):

    # project settings
    project_name: str = "ai-divination"

    # OpenAI API settings (兼容所有OpenAI格式的API)
    api_key: str = Field(default="", exclude=True)
    api_base: str = "https://api.openai.com/v1"
    model: str = "gpt-3.5-turbo"
    
    # Gemini API settings (六爻专用，可选)
    gemini_api_key: str = Field(default="", exclude=True)
    gemini_model: str = "gemini-2.5-flash"
    
    # DashScope (阿里云百炼) API settings
    dashscope_api_key: str = Field(default="", exclude=True)
    dashscope_api_base: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscope_model: str = "qwen-plus"
    
    # DeepSeek API settings
    deepseek_api_key: str = Field(default="", exclude=True)
    deepseek_api_base: str = "https://api.deepseek.com/v1"
    deepseek_model: str = "deepseek-chat"
    
    # 智谱AI (Zhipu) API settings
    zhipu_api_key: str = Field(default="", exclude=True)
    zhipu_api_base: str = "https://open.bigmodel.cn/api/paas/v4"
    zhipu_model: str = "glm-4-air"
    
    # 硅基流动 SiliconFlow API settings
    siliconflow_api_key: str = Field(default="", exclude=True)
    siliconflow_api_base: str = "https://api.siliconflow.cn/v1"
    siliconflow_model: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"

    # github oauth login settings
    github_client_id: str = ""
    github_client_secret: str = Field(default="", exclude=True)
    jwt_secret: str = Field(default="", exclude=True)
    
    @field_validator('jwt_secret', mode='before')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """验证 JWT 密钥强度，生产环境强制使用强密钥"""
        is_production = os.getenv("VERCEL") == "1" or os.getenv("ENVIRONMENT") == "production"
        
        # 如果未设置或为弱密钥
        if not v or v.lower() in WEAK_JWT_SECRETS:
            if is_production:
                # 生产环境：必须配置强密钥
                raise ValueError(
                    f"安全错误：生产环境必须配置 JWT_SECRET 环境变量，"
                    f"且长度不少于 {MIN_JWT_SECRET_LENGTH} 个字符。"
                    f"可使用以下命令生成：python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            else:
                # 开发环境：自动生成随机密钥并警告
                generated_secret = secrets.token_urlsafe(32)
                _logger.warning(
                    f"[安全警告] JWT_SECRET 未配置或过于简单，已自动生成临时密钥。"
                    f"生产环境请务必配置强密钥！"
                )
                return generated_secret
        
        # 检查密钥长度
        if len(v) < MIN_JWT_SECRET_LENGTH:
            if is_production:
                raise ValueError(
                    f"安全错误：JWT_SECRET 长度不足，至少需要 {MIN_JWT_SECRET_LENGTH} 个字符。"
                )
            else:
                _logger.warning(
                    f"[安全警告] JWT_SECRET 长度不足 {MIN_JWT_SECRET_LENGTH} 字符，"
                    f"建议使用更强的密钥。"
                )
        
        return v
    
    @field_validator('cache_client_type', mode='after')
    @classmethod
    def validate_cache_client_type(cls, v: str) -> str:
        """验证缓存类型，生产环境警告使用内存缓存"""
        is_production = os.getenv("VERCEL") == "1" or os.getenv("ENVIRONMENT") == "production"
        valid_types = {"memory", "redis", "upstash_kv"}
        
        if v not in valid_types:
            raise ValueError(f"cache_client_type 必须是 {valid_types} 之一，实际值: {v}")
        
        if is_production and v == "memory":
            _logger.warning(
                "[水平扩展警告] 生产环境使用内存缓存 (cache_client_type=memory)，"
                "无法支持多实例部署。建议配置 Redis 或 Upstash KV。"
            )
        
        return v

    # google ads settings
    ad_client: str = ""
    ad_slot: str = ""

    # openai settings defaults
    default_api_base: str = "https://api.openai.com/v1"
    default_model: str = "gpt-3.5-turbo"
    purchase_url: str = ""

    # cache settings
    cache_client_type: str = "memory"
    redis_url: str = Field(default="", exclude=True, alias="KV_URL")
    upstash_api_url: str = Field(default="", alias="KV_REST_API_URL")
    upstash_api_token: str = Field(default="", exclude=True, alias="KV_REST_API_TOKEN")

    # rate limit settings
    enable_rate_limit: bool = True
    # rate limit xxx request per xx seconds
    rate_limit: Tuple[int, int] = (60, 60 * 60)
    user_rate_limit: Tuple[int, int] = (600, 60 * 60)
    # 禁止词汇配置（新增，解决报错）
    stop_words: list[str] = Field(default=[], description="占卜输入的禁止词汇列表，命中则拒绝请求")
    # quota settings (用户配额限制) - 0表示无限制
    quota_free_daily_calls: int = 0        # 免费用户每日调用次数上限
    quota_free_daily_tokens: int = 0       # 免费用户每日Token使用上限
    quota_vip_daily_calls: int = 0         # VIP用户每日调用次数上限
    quota_vip_daily_tokens: int = 0        # VIP用户每日Token使用上限
    quota_premium_daily_calls: int = 0     # 高级用户每日调用次数上限
    quota_premium_daily_tokens: int = 0    # 高级用户每日Token使用上限

    def get_human_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.rate_limit
        return f"{max_reqs}req/{time_window_seconds}seconds"

    def get_human_user_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.user_rate_limit
        return f"{max_reqs}req/{time_window_seconds}seconds"

    class Config:
        env_file = ".env"


settings = Settings()
