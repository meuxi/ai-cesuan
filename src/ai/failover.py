"""
AI 故障转移逻辑
参考 zhanwen 的 analyzeDivination 函数设计
实现主备模型自动切换
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from .provider import AIProvider, ChatMessage, ChatResponse, get_provider
from .models import AIModel, AIModelConfig, ModelStatus
from .token_counter import estimate_tokens, estimate_cost

logger = logging.getLogger(__name__)


class AllModelsFailedError(Exception):
    """所有模型均调用失败"""
    
    def __init__(self, errors: List[Dict[str, Any]]):
        self.errors = errors
        super().__init__(f"所有AI模型均调用失败: {errors}")


@dataclass
class FailoverResult:
    """故障转移调用结果"""
    response: ChatResponse
    model_used: AIModel
    attempts: int
    errors: List[Dict[str, Any]]


class AIProviderManager:
    """
    多 Provider 管理器
    支持主备模型故障转移
    """
    
    def __init__(self, config: Optional[AIModelConfig] = None):
        self.config = config or AIModelConfig()
        self._providers_cache: Dict[str, AIProvider] = {}
    
    def _get_provider_for_model(self, model: AIModel) -> AIProvider:
        """获取模型对应的 Provider 实例"""
        cache_key = f"{model.provider}:{model.base_url}:{model.api_key[:8] if model.api_key else ''}"
        
        if cache_key not in self._providers_cache:
            self._providers_cache[cache_key] = get_provider(
                provider_type=model.provider,
                api_key=model.api_key,
                base_url=model.base_url,
                **model.parameters
            )
        
        return self._providers_cache[cache_key]
    
    async def chat_with_failover(
        self,
        messages: List[ChatMessage],
        primary_model: Optional[AIModel] = None,
        backup_models: Optional[List[AIModel]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> FailoverResult:
        """
        带故障转移的 AI 调用
        
        Args:
            messages: 聊天消息列表
            primary_model: 主模型（可选，默认使用配置中的主模型）
            backup_models: 备用模型列表（可选）
            temperature: 温度参数
            max_tokens: 最大 Token 数
            **kwargs: 其他参数
        
        Returns:
            FailoverResult: 包含响应、使用的模型、尝试次数等信息
        
        Raises:
            AllModelsFailedError: 所有模型都失败时抛出
        """
        # 构建候选模型列表
        candidates: List[AIModel] = []
        
        if primary_model:
            candidates.append(primary_model)
        elif self.config.primary:
            candidates.append(self.config.primary)
        
        if backup_models:
            candidates.extend(backup_models)
        else:
            candidates.extend(self.config.backups)
        
        # 过滤出活跃的模型
        active_candidates = [
            m for m in candidates 
            if m.status == ModelStatus.ACTIVE
        ]
        
        if not active_candidates:
            raise AllModelsFailedError([{"error": "没有可用的AI模型配置"}])
        
        errors: List[Dict[str, Any]] = []
        attempts = 0
        
        for model in active_candidates:
            attempts += 1
            try:
                logger.info(f"[AI] 尝试调用模型: {model.name} (Provider: {model.provider})")
                
                provider = self._get_provider_for_model(model)
                
                # 获取实际模型名称
                model_name = model.parameters.get("model", model.name)
                
                response = await provider.chat(
                    messages=messages,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                )
                
                # 如果没有 token 信息，进行估算
                if response.tokens_used is None:
                    input_text = "\n".join(m.content for m in messages)
                    response.tokens_used = estimate_tokens(input_text) + estimate_tokens(response.content)
                    response.tokens_estimated = True
                
                # 计算成本
                if response.tokens_used and model.cost_per_1k_tokens > 0:
                    response.cost = estimate_cost(response.tokens_used, model.cost_per_1k_tokens)
                
                logger.info(f"[AI] 模型 {model.name} 调用成功, 耗时: {response.response_time_ms}ms")
                
                return FailoverResult(
                    response=response,
                    model_used=model,
                    attempts=attempts,
                    errors=errors
                )
                
            except Exception as e:
                error_info = {
                    "model": model.name,
                    "provider": model.provider,
                    "error": str(e)
                }
                errors.append(error_info)
                logger.warning(f"[AI] 模型 {model.name} 调用失败: {e}, 尝试下一个")
                continue
        
        # 所有模型都失败
        logger.error(f"[AI] 所有模型均调用失败: {errors}")
        raise AllModelsFailedError(errors)
    
    async def chat(
        self,
        messages: List[ChatMessage],
        **kwargs
    ) -> ChatResponse:
        """
        简化的聊天接口（自动使用故障转移）
        """
        result = await self.chat_with_failover(messages, **kwargs)
        return result.response
    
    def set_config(self, config: AIModelConfig):
        """设置配置"""
        self.config = config
        self._providers_cache.clear()
    
    def add_model(self, model: AIModel):
        """添加模型"""
        self.config.add_model(model)


# 全局管理器实例
_default_manager: Optional[AIProviderManager] = None


def get_ai_manager() -> AIProviderManager:
    """获取全局 AI 管理器"""
    global _default_manager
    if _default_manager is None:
        _default_manager = AIProviderManager()
    return _default_manager


def set_ai_manager(manager: AIProviderManager):
    """设置全局 AI 管理器"""
    global _default_manager
    _default_manager = manager


async def chat_with_ai(
    messages: List[Dict[str, str]],
    **kwargs
) -> ChatResponse:
    """
    便捷函数：使用全局管理器进行 AI 聊天
    
    Args:
        messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
        **kwargs: 其他参数
    
    Returns:
        ChatResponse
    """
    manager = get_ai_manager()
    chat_messages = [ChatMessage(role=m["role"], content=m["content"]) for m in messages]
    return await manager.chat(chat_messages, **kwargs)
