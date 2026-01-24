"""
HTTP 客户端连接池管理器

解决问题：
- 每次请求创建新客户端的开销
- 连接无法复用，增加延迟

优化策略：
- 按 base_url 维护客户端实例
- 共享连接池配置
- 支持优雅关闭
"""

import asyncio
import atexit
import httpx
import logging
from typing import Dict, Optional, ClassVar

logger = logging.getLogger(__name__)

# 流式超时配置
DEFAULT_CHUNK_TIMEOUT = 30.0  # 数据块间默认超时时间（秒）

# HTTP 客户端连接池配置
HTTP_CLIENT_LIMITS = httpx.Limits(
    max_keepalive_connections=20,  # 最大保持连接数
    max_connections=100,           # 最大总连接数
    keepalive_expiry=30.0,         # 保持连接超时（秒）
)


class HTTPClientManager:
    """
    HTTP 客户端连接池管理器（单例模式）
    """
    _instance: ClassVar[Optional["HTTPClientManager"]] = None
    _clients: Dict[str, httpx.AsyncClient]
    _default_timeout: float
    
    def __new__(cls) -> "HTTPClientManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._clients = {}
            cls._instance._default_timeout = 120.0
            # 注册程序退出时的清理函数
            atexit.register(cls._instance._sync_cleanup)
        return cls._instance
    
    def get_client(
        self,
        base_url: str,
        timeout: Optional[float] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> httpx.AsyncClient:
        """
        获取或创建指定 base_url 的 HTTP 客户端
        
        Args:
            base_url: API 基础 URL
            timeout: 请求超时时间
            headers: 默认请求头
            
        Returns:
            httpx.AsyncClient 实例
        """
        # 使用 base_url 作为缓存键
        cache_key = base_url
        
        if cache_key not in self._clients:
            client = httpx.AsyncClient(
                timeout=timeout or self._default_timeout,
                limits=HTTP_CLIENT_LIMITS,
                headers=headers,
            )
            self._clients[cache_key] = client
            logger.debug(f"[HTTPClientManager] 创建新客户端: {base_url}")
        
        return self._clients[cache_key]
    
    async def close_all(self) -> None:
        """异步关闭所有客户端"""
        for url, client in self._clients.items():
            try:
                await client.aclose()
                logger.debug(f"[HTTPClientManager] 关闭客户端: {url}")
            except Exception as e:
                logger.warning(f"[HTTPClientManager] 关闭客户端失败: {url}, {e}")
        self._clients.clear()
    
    def _sync_cleanup(self) -> None:
        """同步清理（用于 atexit）"""
        # 在程序退出时尝试关闭客户端
        for client in self._clients.values():
            try:
                # 尝试获取事件循环
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(client.aclose())
                else:
                    loop.run_until_complete(client.aclose())
            except Exception:
                pass
        self._clients.clear()


# 全局客户端管理器实例
http_client_manager = HTTPClientManager()
