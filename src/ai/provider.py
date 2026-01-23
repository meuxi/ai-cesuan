"""
AI Provider 抽象层
参考 zhanwen 项目的 ai-chat.service.ts 设计
支持 OpenAI、Anthropic、Gemini、DeepSeek、ModelScope 等多种 Provider
"""

import httpx
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

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
        """发送聊天请求"""
        pass
    
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
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
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


def detect_provider_from_url(base_url: str) -> Optional[str]:
    """
    智能识别Provider类型（根据URL）
    支持国内外主流大模型服务商
    """
    if not base_url:
        return None
    
    url_lower = base_url.lower()
    
    # Anthropic / Claude
    if "anthropic" in url_lower or "claude" in url_lower:
        return "anthropic"
    
    # Google Gemini
    if "generativelanguage.googleapis.com" in url_lower or "gemini" in url_lower:
        return "gemini"
    
    # DeepSeek
    if "deepseek" in url_lower:
        return "deepseek"
    
    # 硅基流动 SiliconFlow
    if "siliconflow" in url_lower or "silicon" in url_lower:
        return "openai"  # 硅基流动使用 OpenAI 兼容格式
    
    # 英伟达 NVIDIA NIM
    if "nvidia" in url_lower or "nim.ngc" in url_lower or "integrate.api.nvidia" in url_lower:
        return "openai"  # NVIDIA NIM 使用 OpenAI 兼容格式
    
    # 阿里云 DashScope / 百炼
    if "dashscope" in url_lower or "aliyun" in url_lower:
        return "openai"  # DashScope 使用 OpenAI 兼容格式
    
    # 智谱AI
    if "bigmodel.cn" in url_lower or "zhipu" in url_lower:
        return "openai"  # 智谱使用 OpenAI 兼容格式
    
    # ModelScope / 魔搭
    if "modelscope" in url_lower:
        return "modelscope"
    
    # Moonshot / 月之暗面 / Kimi
    if "moonshot" in url_lower or "kimi" in url_lower:
        return "openai"
    
    # 字节跳动 / 豆包 / 火山引擎
    if "volcengine" in url_lower or "bytedance" in url_lower or "doubao" in url_lower:
        return "openai"
    
    # 百度文心 / 千帆
    if "baidubce" in url_lower or "wenxin" in url_lower or "qianfan" in url_lower:
        return "openai"
    
    # 腾讯混元
    if "hunyuan" in url_lower or "tencent" in url_lower:
        return "openai"
    
    # 讯飞星火
    if "xfyun" in url_lower or "spark" in url_lower or "iflytek" in url_lower:
        return "openai"
    
    # MiniMax / 海螺AI
    if "minimax" in url_lower or "hailuo" in url_lower:
        return "openai"
    
    # 零一万物 / Yi
    if "lingyiwanwu" in url_lower or "01.ai" in url_lower:
        return "openai"
    
    # Groq
    if "groq" in url_lower:
        return "openai"
    
    # Together AI
    if "together" in url_lower:
        return "openai"
    
    # Fireworks AI
    if "fireworks" in url_lower:
        return "openai"
    
    # Perplexity
    if "perplexity" in url_lower:
        return "openai"
    
    # Mistral AI
    if "mistral" in url_lower:
        return "openai"
    
    # Cohere
    if "cohere" in url_lower:
        return "openai"
    
    # Azure OpenAI
    if "azure" in url_lower and "openai" in url_lower:
        return "openai"
    
    # OpenRouter
    if "openrouter" in url_lower:
        return "openai"
    
    # OpenAI 官方
    if "openai.com" in url_lower:
        return "openai"
    
    return None


def detect_provider_from_model(model_name: str) -> Optional[str]:
    """
    智能识别Provider类型（根据模型名称）
    支持国内外主流模型系列
    """
    if not model_name:
        return None
    
    model_lower = model_name.lower()
    
    # Anthropic Claude 系列
    if model_lower.startswith("claude"):
        return "anthropic"
    
    # Google Gemini 系列
    if model_lower.startswith("gemini") or model_lower.startswith("models/gemini"):
        return "gemini"
    
    # DeepSeek 系列
    if model_lower.startswith("deepseek"):
        return "deepseek"
    
    # 通义千问 Qwen (阿里)
    if model_lower.startswith("qwen"):
        return "openai"
    
    # 智谱 GLM / ChatGLM 系列
    if model_lower.startswith("glm") or model_lower.startswith("chatglm"):
        return "openai"
    
    # OpenAI GPT 系列
    if model_lower.startswith("gpt") or model_lower.startswith("o1") or model_lower.startswith("o3"):
        return "openai"
    
    # 百度 ERNIE 系列
    if model_lower.startswith("ernie"):
        return "openai"
    
    # 腾讯混元
    if model_lower.startswith("hunyuan"):
        return "openai"
    
    # 讯飞星火
    if model_lower.startswith("spark"):
        return "openai"
    
    # MiniMax
    if model_lower.startswith("abab"):
        return "openai"
    
    # 零一万物 Yi
    if model_lower.startswith("yi-"):
        return "openai"
    
    # Moonshot / Kimi
    if model_lower.startswith("moonshot"):
        return "openai"
    
    # 字节豆包
    if model_lower.startswith("doubao") or model_lower.startswith("skylark"):
        return "openai"
    
    # Mistral 系列
    if model_lower.startswith("mistral") or model_lower.startswith("mixtral"):
        return "openai"
    
    # Meta Llama 系列
    if model_lower.startswith("llama") or model_lower.startswith("meta-llama"):
        return "openai"
    
    # Cohere Command 系列
    if model_lower.startswith("command"):
        return "openai"
    
    # NVIDIA 模型
    if "nvidia" in model_lower or model_lower.startswith("nemotron"):
        return "openai"
    
    return None


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
