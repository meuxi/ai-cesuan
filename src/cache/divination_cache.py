"""
排盘结果缓存服务

为计算密集型的排盘操作提供缓存支持，避免重复计算。
支持紫微、奇门、八字、大六壬等排盘结果的缓存。
"""
import hashlib
import json
import logging
from typing import Optional, Any, Dict
from functools import wraps

from .cache_client_factory import CacheClientFactory

logger = logging.getLogger(__name__)

# 缓存 TTL 配置（秒）
CACHE_TTL = {
    "ziwei": 86400,      # 紫微命盘：24小时（命盘不变）
    "bazi": 86400,       # 八字排盘：24小时
    "qimen": 3600,       # 奇门排盘：1小时（时盘变化较快）
    "daliuren": 3600,    # 大六壬：1小时
    "plum_flower": 1800, # 梅花易数：30分钟
    "liuyao": 1800,      # 六爻：30分钟
    "default": 3600,     # 默认：1小时
}

# 缓存键前缀
CACHE_PREFIX = "divination:paipan:"


def generate_cache_key(divination_type: str, params: Dict[str, Any]) -> str:
    """
    生成缓存键
    
    Args:
        divination_type: 占卜类型（ziwei, qimen, bazi 等）
        params: 排盘参数字典或 Pydantic 模型
        
    Returns:
        缓存键字符串
    """
    # 如果是 Pydantic 模型，先转换为字典
    if hasattr(params, 'model_dump'):
        params = params.model_dump()
    elif hasattr(params, 'dict'):
        params = params.dict()
    
    # 过滤掉不影响结果的参数
    filtered_params = {k: v for k, v in sorted(params.items()) if v is not None}
    params_str = json.dumps(filtered_params, sort_keys=True, ensure_ascii=False, default=str)
    params_hash = hashlib.md5(params_str.encode()).hexdigest()[:16]
    return f"{CACHE_PREFIX}{divination_type}:{params_hash}"


def get_cached_result(divination_type: str, params: Dict[str, Any]) -> Optional[Dict]:
    """
    获取缓存的排盘结果
    
    Args:
        divination_type: 占卜类型
        params: 排盘参数（支持字典或 Pydantic 模型）
        
    Returns:
        缓存的结果字典，如果未命中返回 None
    """
    try:
        cache_key = generate_cache_key(divination_type, params)
        cache_client = CacheClientFactory.get_client()
        cached_value = cache_client.get_token(cache_key)
        
        if cached_value:
            logger.debug(f"缓存命中: {divination_type}")
            return json.loads(cached_value)
    except Exception as e:
        logger.warning(f"获取缓存失败: {e}")
    
    return None


def set_cached_result(divination_type: str, params: Dict[str, Any], result: Dict) -> bool:
    """
    缓存排盘结果
    
    Args:
        divination_type: 占卜类型
        params: 排盘参数（支持字典或 Pydantic 模型）
        result: 排盘结果
        
    Returns:
        是否成功缓存
    """
    try:
        cache_key = generate_cache_key(divination_type, params)
        cache_client = CacheClientFactory.get_client()
        ttl = CACHE_TTL.get(divination_type, CACHE_TTL["default"])
        
        # 确保结果可序列化
        if hasattr(result, 'model_dump'):
            result = result.model_dump()
        elif hasattr(result, 'dict'):
            result = result.dict()
        
        cache_client.store_token(cache_key, json.dumps(result, ensure_ascii=False, default=str), ttl)
        logger.debug(f"缓存设置成功: {divination_type}, TTL={ttl}s")
        return True
    except Exception as e:
        logger.warning(f"设置缓存失败: {e}")
        return False


def cached_divination(divination_type: str, param_keys: list = None):
    """
    排盘结果缓存装饰器
    
    Args:
        divination_type: 占卜类型
        param_keys: 用于生成缓存键的参数名列表，如果为 None 则使用所有参数
        
    Example:
        @cached_divination("ziwei", ["year", "month", "day", "hour", "gender"])
        async def paipan(req: ZiweiPaipanRequest):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 提取缓存参数
            cache_params = {}
            
            # 从 args 中提取（假设第一个参数是 request 对象）
            if args:
                request_obj = args[0]
                if hasattr(request_obj, '__dict__'):
                    # Pydantic model
                    if hasattr(request_obj, 'model_dump'):
                        all_params = request_obj.model_dump()
                    elif hasattr(request_obj, 'dict'):
                        all_params = request_obj.dict()
                    else:
                        all_params = vars(request_obj)
                    
                    if param_keys:
                        cache_params = {k: all_params.get(k) for k in param_keys}
                    else:
                        cache_params = all_params
            
            # 合并 kwargs
            cache_params.update(kwargs)
            
            # 尝试获取缓存
            cached = get_cached_result(divination_type, cache_params)
            if cached is not None:
                return cached
            
            # 执行原函数
            result = await func(*args, **kwargs)
            
            # 缓存结果（只缓存字典类型结果）
            if isinstance(result, dict):
                set_cached_result(divination_type, cache_params, result)
            elif hasattr(result, 'model_dump'):
                # Pydantic model
                set_cached_result(divination_type, cache_params, result.model_dump())
            elif hasattr(result, 'dict'):
                set_cached_result(divination_type, cache_params, result.dict())
            
            return result
        
        return wrapper
    return decorator


def invalidate_cache(divination_type: str, params: Dict[str, Any]) -> bool:
    """
    使特定排盘结果缓存失效
    
    Args:
        divination_type: 占卜类型
        params: 排盘参数
        
    Returns:
        是否成功
    """
    try:
        cache_key = generate_cache_key(divination_type, params)
        cache_client = CacheClientFactory.get_client()
        return cache_client.delete_token(cache_key)
    except Exception as e:
        logger.warning(f"缓存失效操作失败: {e}")
        return False
