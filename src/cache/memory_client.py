import time
import logging
import threading
import cachetools

from fastapi import HTTPException

from typing import Optional

from .base import CacheClientBase


_logger = logging.getLogger(__name__)


def ttu_func(_key, value, now):
    _, expire_seconds = value
    return now + expire_seconds


class MemoryCacheClient(CacheClientBase):
    """
    内存缓存客户端
    
    线程安全说明：
    - 使用 _rate_limit_lock 保护速率限制的读-改-写操作
    - 使用 _token_lock 保护 token 缓存操作
    """

    _type = "memory"
    token_cache = cachetools.TLRUCache(
        maxsize=10000,  # 限制最大缓存数量，防止内存泄漏
        ttu=ttu_func,
        timer=time.time
    )
    # Fix memory leak: use TTLCache instead of defaultdict
    # TTL should be at least longer than the longest rate limit window (1 hour)
    request_limit_map = cachetools.TTLCache(
        maxsize=10000,
        ttl=3600 + 60,
        timer=time.time
    )
    
    # 线程锁：保护缓存操作的原子性
    _rate_limit_lock = threading.Lock()
    _token_lock = threading.Lock()

    @classmethod
    def store_token(cls, key: str, token: str, expire_seconds: int) -> None:
        try:
            with cls._token_lock:
                cls.token_cache[key] = (token, expire_seconds)
            return
        except Exception as e:
            _logger.error(f"Store token failed: {e}")
        raise HTTPException(
            status_code=400, detail="Store token failed"
        )

    @classmethod
    def get_token(cls, key: str) -> Optional[str]:
        try:
            with cls._token_lock:
                if key in cls.token_cache:
                    token, _ = cls.token_cache[key]
                    return token
            return None
        except Exception as e:
            _logger.error(f"Get token failed: {e}")
            return None

    @classmethod
    def delete_token(cls, key: str) -> bool:
        """删除指定 key"""
        try:
            with cls._token_lock:
                if key in cls.token_cache:
                    del cls.token_cache[key]
                    return True
            return False
        except Exception as e:
            _logger.error(f"Delete token failed: {e}")
            return False

    @classmethod
    def check_rate_limit(cls, key: str, time_window_seconds: int, max_requests: int) -> None:
        """
        检查速率限制（线程安全版本）
        
        使用锁保护整个读-改-写操作，确保原子性
        """
        cur_timestamp = int(time.time())
        try:
            with cls._rate_limit_lock:
                # get existing history or create new list
                if key not in cls.request_limit_map:
                    cls.request_limit_map[key] = []
                
                history = cls.request_limit_map[key]
                
                # 过滤过期记录
                cutoff = cur_timestamp - time_window_seconds
                history = [ts for ts in history if ts >= cutoff]
                
                # add current timestamp
                history.append(cur_timestamp)
                
                # update cache to refresh TTL
                cls.request_limit_map[key] = history
                
                req_count = len(history)
            
            # 在锁外检查并抛出异常
            if req_count > max_requests:
                raise HTTPException(
                    status_code=429, detail="Rate limit exceeded"
                )
            return
        except HTTPException:
            raise
        except Exception as e:
            _logger.error(f"Rate limit failed: {e}")
        raise HTTPException(
            status_code=400, detail="Rate limit failed"
        )
