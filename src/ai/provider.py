"""
AI Provider 抽象层
参考 zhanwen 项目的 ai-chat.service.ts 和 MingAI-master 项目设计
支持 OpenAI、Anthropic、Gemini、DeepSeek、ModelScope 等多种 Provider
支持同步和流式两种调用方式
"""

import json
import asyncio
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, AsyncGenerator

# 从拆分的模块导入
from .http_client import (
    HTTPClientManager,
    http_client_manager,
    DEFAULT_CHUNK_TIMEOUT,
)
from .provider_detection import (
    detect_provider_from_url,
    detect_provider_from_model,
)

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """聊天消息"""
    role: str  # system, user, assistant
    content: str


@dataclass
class ChatResponse:
    """聊天响应"""
    content: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    tokens_estimated: bool = False
    cost: Optional[float] = None
    response_time_ms: int = 0
    request_id: Optional[str] = None


class AIProvider(ABC):
    """AI Provider 抽象基类"""
    
    name: str = "base"
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, **kwargs):
        self.api_key = api_key.strip() if api_key else ""
        self.base_url = base_url.strip().rstrip("/") if base_url else self.default_base_url
        self.timeout = kwargs.get("timeout", 120)
        self.extra_config = kwargs
    
    @property
    @abstractmethod
    def default_base_url(self) -> str:
        """默认 API 地址"""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        """发送聊天请求（同步模式，等待完整响应）"""
        pass
    
    async def chat_stream(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        发送流式聊天请求（实时输出）
        
        默认实现：通过同步 chat 模拟流式（子类可覆盖实现真正的流式）
        
        Yields:
            str: 内容片段
        """
        response = await self.chat(messages, model, temperature, max_tokens, **kwargs)
        # 默认实现：将完整响应作为单个 chunk 返回
        yield response.content
    
    def _build_headers(self) -> Dict[str, str]:
        """构建请求头"""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }


class OpenAIProvider(AIProvider):
    """OpenAI Provider (兼容 OpenAI API 格式的服务)"""
    
    name = "openai"
    
    @property
    def default_base_url(self) -> str:
        return "https://api.openai.com/v1"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        import time
        start_time = time.time()
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "stream": False,
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        # 合并额外参数
        for key in ["top_p", "frequency_penalty", "presence_penalty"]:
            if key in kwargs:
                payload[key] = kwargs[key]
        
        # 使用连接池客户端
        client = http_client_manager.get_client(self.base_url, timeout=self.timeout)
        response = await client.post(url, json=payload, headers=self._build_headers())
        response.raise_for_status()
        data = response.json()
        
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 解析 Token 使用量
        usage = data.get("usage", {})
        tokens_used = usage.get("total_tokens") or (
            (usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)) or None
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            content=content,
            model=model,
            provider=self.name,
            tokens_used=tokens_used,
            tokens_estimated=tokens_used is None,
            response_time_ms=response_time_ms,
            request_id=data.get("id"),
        )
    
    async def chat_stream(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        chunk_timeout: Optional[float] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        OpenAI 流式聊天请求
        使用 SSE (Server-Sent Events) 协议实时返回内容
        
        Args:
            messages: 聊天消息列表
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大 Token 数
            chunk_timeout: 数据块间超时时间（秒），默认使用 DEFAULT_CHUNK_TIMEOUT
            **kwargs: 其他参数
        
        Yields:
            str: 内容片段
        
        Raises:
            TimeoutError: 数据块间超时
        """
        url = f"{self.base_url}/chat/completions"
        chunk_timeout = chunk_timeout or DEFAULT_CHUNK_TIMEOUT
        
        payload = {
            "model": model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature,
            "stream": True,  # 启用流式输出
        }
        
        if max_tokens:
            payload["max_tokens"] = max_tokens
        
        # 合并额外参数
        for key in ["top_p", "frequency_penalty", "presence_penalty"]:
            if key in kwargs:
                payload[key] = kwargs[key]
        
        # 使用连接池客户端（流式请求需要单独的上下文管理）
        client = http_client_manager.get_client(self.base_url, timeout=self.timeout)
        async with client.stream(
            "POST",
            url,
            json=payload,
            headers=self._build_headers()
        ) as response:
            response.raise_for_status()
            
            # 记录上次收到数据块的时间，用于超时检测
            last_chunk_time = asyncio.get_event_loop().time()
            
            async for line in response.aiter_lines():
                # 检查数据块间超时
                current_time = asyncio.get_event_loop().time()
                if current_time - last_chunk_time > chunk_timeout:
                    logger.warning(f"[AI] 流式响应超时：{chunk_timeout}秒内未收到有效数据")
                    raise TimeoutError(f"流式响应超时：{chunk_timeout}秒内未收到数据")
                
                # 跳过空行（但不更新超时计时器）
                if not line or not line.startswith("data: "):
                    continue
                
                # 收到有效数据，更新超时计时器
                last_chunk_time = current_time
                
                data_str = line[6:].strip()  # 移除 "data: " 前缀
                
                # 检查结束标记
                if data_str == "[DONE]":
                    break
                
                try:
                    data = json.loads(data_str)
                    
                    # 检查是否有内容
                    choices = data.get("choices", [])
                    if choices:
                        delta = choices[0].get("delta", {})
                        content = delta.get("content", "")
                        
                        # 支持 DeepSeek R1 的推理内容
                        reasoning_content = delta.get("reasoning_content", "")
                        
                        if reasoning_content:
                            # 可选：标记推理内容（前端可据此分离显示）
                            yield f"[REASONING]{reasoning_content}"
                        
                        if content:
                            yield content
                            
                except json.JSONDecodeError:
                    # 跳过无法解析的行
                    continue


class AnthropicProvider(AIProvider):
    """Anthropic (Claude) Provider"""
    
    name = "anthropic"
    
    @property
    def default_base_url(self) -> str:
        return "https://api.anthropic.com"
    
    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
        }
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        import time
        start_time = time.time()
        
        url = f"{self.base_url}/v1/messages"
        
        # 分离 system prompt
        system_prompt = ""
        user_messages = []
        for m in messages:
            if m.role == "system":
                system_prompt = m.content
            else:
                user_messages.append({"role": m.role, "content": m.content})
        
        payload = {
            "model": model,
            "messages": user_messages,
            "max_tokens": max_tokens or 32000,  # 用户体验优先：无限制输出
            "temperature": temperature,
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        # 使用连接池客户端
        client = http_client_manager.get_client(self.base_url, timeout=self.timeout)
        response = await client.post(url, json=payload, headers=self._build_headers())
        response.raise_for_status()
        data = response.json()
        
        # 提取内容
        content_blocks = data.get("content", [])
        content = ""
        if content_blocks:
            content = "".join(
                block.get("text", "") for block in content_blocks 
                if block.get("type") == "text"
            )
        
        # Token 使用量
        usage = data.get("usage", {})
        input_tokens = usage.get("input_tokens", 0)
        output_tokens = usage.get("output_tokens", 0)
        tokens_used = (input_tokens + output_tokens) if (input_tokens or output_tokens) else None
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            content=content,
            model=model,
            provider=self.name,
            tokens_used=tokens_used,
            tokens_estimated=tokens_used is None,
            response_time_ms=response_time_ms,
            request_id=data.get("id"),
        )


class GeminiProvider(AIProvider):
    """Google Gemini Provider"""
    
    name = "gemini"
    
    @property
    def default_base_url(self) -> str:
        return "https://generativelanguage.googleapis.com/v1beta"
    
    def _build_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        import time
        start_time = time.time()
        
        url = f"{self.base_url}/models/{model}:generateContent"
        
        # Gemini 需要合并 system 和 user 消息
        combined_content = ""
        for m in messages:
            if m.role == "system":
                combined_content += m.content + "\n\n"
            else:
                combined_content += m.content
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": combined_content}]}],
        }
        
        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_tokens:
            generation_config["maxOutputTokens"] = max_tokens
        
        if generation_config:
            payload["generationConfig"] = generation_config
        
        # 使用连接池客户端
        client = http_client_manager.get_client(self.base_url, timeout=self.timeout)
        response = await client.post(url, json=payload, headers=self._build_headers())
        response.raise_for_status()
        data = response.json()
        
        # 提取内容
        content = ""
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            content = "".join(p.get("text", "") for p in parts)
        
        # Token 使用量
        usage = data.get("usageMetadata", {})
        tokens_used = usage.get("totalTokenCount")
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        return ChatResponse(
            content=content,
            model=model,
            provider=self.name,
            tokens_used=tokens_used,
            tokens_estimated=tokens_used is None,
            response_time_ms=response_time_ms,
        )


class DeepSeekProvider(OpenAIProvider):
    """DeepSeek Provider (OpenAI 兼容格式)"""
    
    name = "deepseek"
    
    @property
    def default_base_url(self) -> str:
        return "https://api.deepseek.com/v1"
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> ChatResponse:
        # DeepSeek max_tokens - 用户体验优先：提升到最大值
        if max_tokens is None:
            max_tokens = 32000
        max_tokens = max(1, min(max_tokens, 32000))
        
        return await super().chat(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )


class ModelScopeProvider(OpenAIProvider):
    """ModelScope Provider (阿里魔搭，OpenAI 兼容格式)"""
    
    name = "modelscope"
    
    @property
    def default_base_url(self) -> str:
        return "https://api-inference.modelscope.cn/v1"


# Provider 工厂
PROVIDER_CLASSES = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "deepseek": DeepSeekProvider,
    "modelscope": ModelScopeProvider,
}


def get_provider(provider_type: str, api_key: str, base_url: Optional[str] = None, **kwargs) -> AIProvider:
    """
    获取 Provider 实例
    支持智能识别：优先使用显式指定的类型，否则从URL/模型名自动推断
    """
    provider_type = provider_type.lower().strip() if provider_type else ""
    
    # 如果没有明确指定类型，尝试智能识别
    if not provider_type or provider_type == "auto":
        # 先从URL识别
        detected = detect_provider_from_url(base_url) if base_url else None
        
        # 再从模型名识别
        if not detected:
            model_name = kwargs.get("model") or kwargs.get("parameters", {}).get("model", "")
            detected = detect_provider_from_model(model_name)
        
        if detected:
            provider_type = detected
            logger.info(f"[AI] 自动识别Provider类型: {provider_type}")
        else:
            provider_type = "openai"  # 默认OpenAI兼容格式
    
    # 标准化 provider 类型
    if "claude" in provider_type or "anthropic" in provider_type:
        provider_type = "anthropic"
    elif "gemini" in provider_type or "google" in provider_type:
        provider_type = "gemini"
    elif "deepseek" in provider_type:
        provider_type = "deepseek"
    elif "modelscope" in provider_type or "dashscope" in provider_type:
        provider_type = "modelscope"
    elif provider_type not in PROVIDER_CLASSES:
        provider_type = "openai"  # 默认使用 OpenAI 兼容格式
    
    provider_class = PROVIDER_CLASSES[provider_type]
    return provider_class(api_key=api_key, base_url=base_url, **kwargs)
