import logging
import os
import secrets
from typing import Tuple

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

_logger = logging.getLogger(__name__)

# 不安全的默认密钥列表
INSECURE_SECRETS = {'secret', 'password', '123456', 'admin', 'jwt_secret', 'changeme', ''}


class Settings(BaseSettings):
    # project settings
    project_name: str = "ai-divination"

    # OpenAI API settings
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
    # 移除alias确保环境变量名与Vercel配置一致
    jwt_secret: str = Field(default="secret", exclude=True)

    @field_validator('jwt_secret')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        """验证JWT密钥安全性
        
        安全要求：
        - 生产环境必须配置安全密钥
        - 密钥长度至少32字符
        - 不能使用常见不安全密钥
        """
        is_production = os.getenv('VERCEL') == '1' or os.getenv('ENV') == 'production'
        
        # 检查是否为不安全密钥
        is_insecure = v.lower() in INSECURE_SECRETS or len(v) < 16
        
        if is_production:
            if is_insecure:
                _logger.error("🚨 生产环境检测到不安全的JWT密钥！")
                _logger.error("   请配置 JWT_SECRET 环境变量，密钥至少需要32个字符")
                _logger.error("   推荐使用命令生成: python -c \"import secrets; print(secrets.token_hex(32))\"")
                # 生产环境使用不安全密钥时，自动生成一个临时密钥并发出严重警告
                # 这样应用仍能启动，但每次重启密钥都会变化（导致已有token失效）
                temp_secret = secrets.token_hex(32)
                _logger.warning(f"⚠️ 已自动生成临时密钥，应用重启后所有登录状态将失效！")
                return temp_secret
        elif is_insecure:
            _logger.warning("⚠️ 开发环境使用不安全的JWT密钥，生产部署前请务必更换！")
            _logger.info("   推荐使用命令生成: python -c \"import secrets; print(secrets.token_hex(32))\"")
        
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
    enable_rate_limit: bool = False  # 默认关闭，生产环境通过环境变量开启
    # rate limit xxx request per xx seconds
    rate_limit: Tuple[int, int] = (60, 60 * 60)
    user_rate_limit: Tuple[int, int] = (600, 60 * 60)

    # 停止词列表：包含这些词的prompt将被拒绝 (变量名已修正为英文)
    stop_words: list = [
        "忽略", "ignore", "指令", "命令", "command", "help", "帮助", "之前",
        "幫助", "現在", "開始", "开始", "start", "restart", "重新开始", "重新開始",
        "遵守", "遵循", "遵从", "遵從"
    ]

    def format_rate_limit(self, limit_pair: Tuple[int, int]) -> str:
        """将(次数, 秒数)格式化为易读的字符串。"""
        max_reqs, time_window_seconds = limit_pair
        return f"{max_reqs}req/{time_window_seconds}seconds"

    def get_human_rate_limit(self) -> str:
        """获取通用速率限制的人性化描述"""
        return self.format_rate_limit(self.rate_limit)

    def get_human_user_rate_limit(self) -> str:
        """获取用户速率限制的人性化描述"""
        return self.format_rate_limit(self.user_rate_limit)

    class Config:
        env_file = ".env"


# 添加配置加载异常捕获
try:
    settings = Settings()
except Exception as e:
    _logger.error(f"配置加载失败: {str(e)}", exc_info=True)
    raise RuntimeError(f"配置加载失败: {str(e)}") from e
