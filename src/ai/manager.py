"""
AI管理器模块 - 提供全局共享的AI管理器实例
将AI管理逻辑从路由层抽离，避免路由间直接依赖
"""
import logging
from typing import Optional

from src.config import settings
from .models import AIModel, AIModelConfig, ModelStatus
from .failover import AIProviderManager

_logger = logging.getLogger(__name__)

# 全局AI管理器单例
_ai_manager: Optional[AIProviderManager] = None


def _init_ai_manager() -> AIProviderManager:
    """初始化AI管理器，使用环境变量配置的API密钥"""
    config = AIModelConfig()
    
    # 1. DashScope (阿里云百炼) - 优先使用
    if settings.dashscope_api_key:
        config.add_model(AIModel(
            name="DashScope-Qwen",
            provider="openai",
            api_key=settings.dashscope_api_key,
            base_url=settings.dashscope_api_base,
            is_primary=True,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.dashscope_model}
        ))
        _logger.info(f"[AI] 已配置DashScope: {settings.dashscope_model}")
    
    # 2. DeepSeek - 备用
    if settings.deepseek_api_key:
        config.add_model(AIModel(
            name="DeepSeek",
            provider="openai",
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.deepseek_model}
        ))
        _logger.info(f"[AI] 已配置DeepSeek: {settings.deepseek_model}")
    
    # 3. 智谱AI - 备用
    if settings.zhipu_api_key:
        config.add_model(AIModel(
            name="Zhipu-GLM",
            provider="openai",
            api_key=settings.zhipu_api_key,
            base_url=settings.zhipu_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.zhipu_model}
        ))
        _logger.info(f"[AI] 已配置智谱AI: {settings.zhipu_model}")
    
    # 4. 硅基流动 SiliconFlow - 备用
    if settings.siliconflow_api_key:
        config.add_model(AIModel(
            name="SiliconFlow",
            provider="openai",
            api_key=settings.siliconflow_api_key,
            base_url=settings.siliconflow_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.siliconflow_model}
        ))
        _logger.info(f"[AI] 已配置SiliconFlow: {settings.siliconflow_model}")
    
    # 5. OpenAI - 最后备用
    if settings.api_key:
        config.add_model(AIModel(
            name="OpenAI",
            provider="openai",
            api_key=settings.api_key,
            base_url=settings.api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.model}
        ))
        _logger.info(f"[AI] 已配置OpenAI: {settings.model}")
    
    return AIProviderManager(config)


def get_ai_manager() -> AIProviderManager:
    """
    获取全局AI管理器（懒加载单例）
    
    Returns:
        AIProviderManager: 全局共享的AI管理器实例
    """
    global _ai_manager
    if _ai_manager is None:
        _ai_manager = _init_ai_manager()
    return _ai_manager


def reset_ai_manager() -> None:
    """
    重置AI管理器（用于测试或配置更新后重新初始化）
    """
    global _ai_manager
    _ai_manager = None
    _logger.info("[AI] AI管理器已重置")
