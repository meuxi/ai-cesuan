"""
API 通用工具函数

提供 API 密钥处理、请求验证等通用功能
"""

from typing import Optional
from fastapi import Request
from src.config import settings


def normalize_api_key(api_key: Optional[str]) -> str:
    """
    标准化 API 密钥格式
    
    - 去除首尾空格
    - 去除不可见字符（\xa0, \u200b 等）
    - 去除 "Bearer " 前缀
    
    Args:
        api_key: 原始 API 密钥
        
    Returns:
        清理后的 API 密钥，如果输入为空则返回空字符串
    """
    if not api_key:
        return ""
    
    cleaned = api_key.strip()
    # 去除常见的不可见字符
    cleaned = cleaned.replace('\xa0', '').replace('\u200b', '')
    # 去除 Bearer 前缀
    if cleaned.startswith("Bearer "):
        cleaned = cleaned[7:].strip()
    
    return cleaned


def get_api_config_from_request(request: Request) -> dict:
    """
    从请求中提取 API 配置
    
    优先使用请求头中的自定义配置，否则使用系统默认配置
    
    Args:
        request: FastAPI 请求对象
        
    Returns:
        包含 api_key, base_url, model 的配置字典
    """
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    
    api_key = normalize_api_key(custom_api_key or settings.api_key)
    base_url = custom_base_url or settings.api_base
    model = custom_api_model or settings.model
    
    return {
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
    }


def validate_api_config(config: dict) -> None:
    """
    验证 API 配置是否完整
    
    Args:
        config: API 配置字典
        
    Raises:
        ValueError: 如果配置不完整
    """
    if not config.get("api_key"):
        raise ValueError("请设置 API KEY")
    if not config.get("base_url"):
        raise ValueError("请设置 API BASE URL")
