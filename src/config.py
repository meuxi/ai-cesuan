import logging
from typing import Tuple

from pydantic import Field
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)


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
    jwt_secret: str = Field(default="secret", exclude=True)

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

    # quota settings (用户配额限制)
    quota_free_daily_calls: int = 10        # 免费用户每日调用次数上限
    quota_free_daily_tokens: int = 20000    # 免费用户每日Token使用上限
    quota_vip_daily_calls: int = 50         # VIP用户每日调用次数上限
    quota_vip_daily_tokens: int = 100000    # VIP用户每日Token使用上限
    quota_premium_daily_calls: int = 200    # 高级用户每日调用次数上限
    quota_premium_daily_tokens: int = 500000  # 高级用户每日Token使用上限

    def get_human_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.rate_limit
        return f"{max_reqs}req/{time_window_seconds}seconds"

    def get_human_user_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.user_rate_limit
        return f"{max_reqs}req/{time_window_seconds}seconds"

    class Config:
        env_file = ".env"


settings = Settings()
