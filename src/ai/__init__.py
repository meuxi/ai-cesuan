"""
AI服务增强模块
参考 zhanwen + Diviner 项目实现
提供多模型管理、故障转移、Token计数等功能
"""

from .provider import (
    AIProvider,
    OpenAIProvider,
    AnthropicProvider,
    GeminiProvider,
    DeepSeekProvider,
    ModelScopeProvider,
)
from .models import AIModel, AIModelConfig
from .failover import AIProviderManager, AllModelsFailedError
from .token_counter import estimate_tokens, estimate_cost

__all__ = [
    "AIProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "DeepSeekProvider",
    "ModelScopeProvider",
    "AIModel",
    "AIModelConfig",
    "AIProviderManager",
    "AllModelsFailedError",
    "estimate_tokens",
    "estimate_cost",
]
