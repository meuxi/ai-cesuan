"""
AI Provider 类型检测模块

支持智能识别国内外主流大模型服务商
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


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
