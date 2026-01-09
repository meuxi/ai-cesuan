import logging
import os
from typing import Tuple

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)


class Settings(BaseSettings):

    # project settings
    project_name: str = "ai-divination"

    # OpenAI API settings
    api_key: str = Field(default="", exclude=True)
    api_base: str = "https://api.openai.com/v1"
    model: str = "gpt-3.5-turbo"

    # github oauth login settings
    github_client_id: str = ""
    github_client_secret: str = Field(default="", exclude=True)
    jwt_secret: str = Field(default="secret", exclude=True)
    
    @field_validator('jwt_secret')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """验证JWT密钥安全性"""
        if v == 'secret' and os.getenv('VERCEL') == '1':
            _logger.warning("⚠️ 生产环境使用默认JWT密钥不安全，请配置jwt_secret环境变量")
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
    
    # 停止词列表：包含这些词的prompt将被拒绝
    stop_words: list = [
        "忽略", "ignore", "指令", "命令", "command", "help", "帮助", "之前",
        "幫助", "現在", "開始", "开始", "start", "restart", "重新开始", "重新開始",
        "遵守", "遵循", "遵从", "遵從"
    ]

    def get_human_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.rate_limit
        # convert to human readable format
        return f"{max_reqs}req/{time_window_seconds}seconds"

    def get_human_user_rate_limit(self) -> str:
        max_reqs, time_window_seconds = self.user_rate_limit
        # convert to human readable format
        return f"{max_reqs}req/{time_window_seconds}seconds"

    class Config:
        env_file = ".env"


settings = Settings()
