"""
AI 故障转移逻辑
参考 zhanwen 的 analyzeDivination 函数设计
实现主备模型自动切换，支持同步和流式两种模式
"""

import asyncio
import httpx
import logging
import cachetools
from typing import List, Optional, Dict, Any, AsyncGenerator
from dataclasses import dataclass

from .provider import AIProvider, ChatMessage, ChatResponse, get_provider
from .models import AIModel, AIModelConfig, ModelStatus
from .token_counter import estimate_tokens, estimate_cost
from .http_client import http_client_manager

logger = logging.getLogger(__name__)

# 健康检查配置
HEALTH_CHECK_TIMEOUT = 5.0  # 健康检查超时时间（秒）
HEALTH_CHECK_CACHE_TTL = 300.0  # 健康检查缓存有效期（秒）- 从60秒延长到5分钟，减少重复检查

# Provider 缓存配置
PROVIDER_CACHE_MAX_SIZE = 50  # 最大缓存的 Provider 实例数
HEALTH_CACHE_MAX_SIZE = 100   # 最大缓存的健康检查结果数


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
    支持主备模型故障转移，流式预检健康机制
    
    缓存策略：
    - Provider 缓存：LRU 策略，限制最大数量防止内存泄漏
    - 健康检查缓存：TTL 策略，自动过期避免使用过时结果
    """
    
    def __init__(self, config: Optional[AIModelConfig] = None):
        self.config = config or AIModelConfig()
        # Provider 缓存：使用 LRUCache 限制大小，防止内存无限增长
        self._providers_cache: cachetools.LRUCache[str, AIProvider] = cachetools.LRUCache(
            maxsize=PROVIDER_CACHE_MAX_SIZE
        )
        # 健康检查缓存：使用 TTLCache 自动过期
        self._health_cache: cachetools.TTLCache[str, bool] = cachetools.TTLCache(
            maxsize=HEALTH_CACHE_MAX_SIZE,
            ttl=HEALTH_CHECK_CACHE_TTL
        )
    
    async def _health_check(self, model: AIModel, timeout: float = HEALTH_CHECK_TIMEOUT) -> bool:
        """
        快速健康检查：发送一个简单请求验证模型可用性
        
        Args:
            model: 要检查的模型
            timeout: 超时时间（秒）
        
        Returns:
            bool: 模型是否健康可用
        """
        cache_key = f"{model.provider}:{model.base_url}:{model.name}"
        
        # 检查缓存（TTLCache 会自动处理过期）
        if cache_key in self._health_cache:
            is_healthy = self._health_cache[cache_key]
            logger.debug(f"[AI] 使用缓存的健康检查结果: {model.name} = {is_healthy}")
            return is_healthy
        
        try:
            provider = self._get_provider_for_model(model)
            model_name = model.parameters.get("model", model.name)
            
            # 性能优化：复用连接池，避免每次创建新客户端
            client = http_client_manager.get_client(provider.base_url, timeout=timeout)
            response = await client.post(
                f"{provider.base_url}/chat/completions",
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": "hi"}],
                    "max_tokens": 1,
                    "stream": False,
                },
                headers=provider._build_headers()
            )
            is_healthy = response.status_code == 200
                
            # 更新缓存（TTLCache 会自动处理过期）
            self._health_cache[cache_key] = is_healthy
            logger.info(f"[AI] 健康检查完成: {model.name} = {'健康' if is_healthy else '不可用'}")
            return is_healthy
            
        except Exception as e:
            logger.warning(f"[AI] 模型 {model.name} 健康检查失败: {e}")
            # 缓存失败结果
            self._health_cache[cache_key] = False
            return False
    
    def _get_candidates(
        self,
        primary_model: Optional[AIModel] = None,
        backup_models: Optional[List[AIModel]] = None
    ) -> List[AIModel]:
        """获取候选模型列表"""
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
        return [m for m in candidates if m.status == ModelStatus.ACTIVE]
    
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
    
    async def chat_stream_with_failover(
        self,
        messages: List[ChatMessage],
        primary_model: Optional[AIModel] = None,
        backup_models: Optional[List[AIModel]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        pre_check: bool = True,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        带故障转移的流式 AI 调用（支持预检健康机制）
        
        Args:
            messages: 聊天消息列表
            primary_model: 主模型（可选，默认使用配置中的主模型）
            backup_models: 备用模型列表（可选）
            temperature: 温度参数
            max_tokens: 最大 Token 数
            pre_check: 是否在流式开始前进行健康检查（默认启用）
            **kwargs: 其他参数
        
        Yields:
            str: 内容片段
        
        Raises:
            AllModelsFailedError: 所有模型都失败时抛出
        
        Note:
            预检健康机制可以避免流式传输中途失败导致的数据不一致问题。
            当启用预检时，会先检查模型是否健康，选择第一个健康的模型进行流式调用。
        """
        # 获取候选模型列表
        active_candidates = self._get_candidates(primary_model, backup_models)
        
        if not active_candidates:
            raise AllModelsFailedError([{"error": "没有可用的AI模型配置"}])
        
        # 预检健康机制：在流式开始前检查模型可用性
        if pre_check and len(active_candidates) > 1:
            logger.info("[AI] 执行流式预检健康检查...")
            
            # 并发检查所有候选模型的健康状态
            health_tasks = [
                self._health_check(model) 
                for model in active_candidates
            ]
            health_results = await asyncio.gather(*health_tasks, return_exceptions=True)
            
            # 筛选出健康的模型
            healthy_candidates = [
                model for model, result in zip(active_candidates, health_results)
                if result is True
            ]
            
            if healthy_candidates:
                logger.info(f"[AI] 预检完成，{len(healthy_candidates)}/{len(active_candidates)} 个模型健康")
                # 优先使用健康的模型
                active_candidates = healthy_candidates + [
                    m for m in active_candidates if m not in healthy_candidates
                ]
            else:
                logger.warning("[AI] 所有模型预检失败，将按原顺序尝试")
        
        errors: List[Dict[str, Any]] = []
        
        for model in active_candidates:
            try:
                logger.info(f"[AI] 尝试流式调用模型: {model.name} (Provider: {model.provider})")
                
                provider = self._get_provider_for_model(model)
                model_name = model.parameters.get("model", model.name)
                
                # 尝试流式调用
                async for chunk in provider.chat_stream(
                    messages=messages,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    **kwargs
                ):
                    yield chunk
                
                # 成功完成，退出
                logger.info(f"[AI] 模型 {model.name} 流式调用成功")
                return
                
            except Exception as e:
                error_info = {
                    "model": model.name,
                    "provider": model.provider,
                    "error": str(e)
                }
                errors.append(error_info)
                logger.warning(f"[AI] 模型 {model.name} 流式调用失败: {e}, 尝试下一个")
                continue
        
        # 所有模型都失败
        logger.error(f"[AI] 所有模型流式调用均失败: {errors}")
        raise AllModelsFailedError(errors)
    
    def clear_health_cache(self):
        """清除健康检查缓存"""
        self._health_cache.clear()
        logger.info("[AI] 健康检查缓存已清除")
    
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
