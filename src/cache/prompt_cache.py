"""
提示词多级缓存系统
层级：内存(L1) → Redis(L2) → 文件(L3)

优化策略：
- TTL 随机抖动：防止缓存雪崩
- 空值缓存：防止缓存穿透
"""
import json
import hashlib
import logging
import random
from typing import Optional, Dict, Any, List
from pathlib import Path
from datetime import datetime, timedelta
import cachetools
import threading
import os

logger = logging.getLogger(__name__)

# 检测是否在Vercel环境（只读文件系统）
IS_VERCEL = os.getenv("VERCEL") == "1"

# 空值缓存标记（用于防止缓存穿透）
CACHE_NULL_VALUE = "__CACHE_NULL__"
# 空值缓存 TTL（较短，避免长时间缓存无效查询）
NULL_VALUE_TTL_SECONDS = 60


class PromptCacheConfig:
    """缓存配置"""
    # L1 内存缓存配置
    L1_MAX_SIZE = 100
    L1_TTL_SECONDS = 3600  # 1小时
    L1_TTL_JITTER = 0.1    # TTL 抖动比例 (±10%)
    
    # L2 Redis缓存配置
    L2_TTL_SECONDS = 86400  # 24小时
    L2_TTL_JITTER = 0.1    # TTL 抖动比例 (±10%)
    L2_PREFIX = "prompt:cache:"
    
    # L3 文件缓存配置
    L3_CACHE_DIR = "data/prompt_cache"
    L3_TTL_SECONDS = 604800  # 7天
    L3_TTL_JITTER = 0.05   # TTL 抖动比例 (±5%)
    
    # 高频工具列表（常驻内存）
    HIGH_FREQ_TOOLS = [
        "bazi_analysis", "tarot_reading", "xiaoliu_analysis",
        "life_kline_analysis", "dream_divination", "liuyao_analysis"
    ]
    
    @classmethod
    def get_ttl_with_jitter(cls, base_ttl: int, jitter_ratio: float) -> int:
        """
        获取带随机抖动的 TTL，防止缓存雪崩
        
        Args:
            base_ttl: 基础 TTL（秒）
            jitter_ratio: 抖动比例（如 0.1 表示 ±10%）
        
        Returns:
            带随机抖动的 TTL
        """
        jitter = int(base_ttl * jitter_ratio)
        return base_ttl + random.randint(-jitter, jitter)


class MultiLevelPromptCache:
    """多级提示词缓存"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # L1: 内存缓存 (TTL Cache)
        self._l1_cache = cachetools.TTLCache(
            maxsize=PromptCacheConfig.L1_MAX_SIZE,
            ttl=PromptCacheConfig.L1_TTL_SECONDS
        )
        self._l1_lock = threading.Lock()
        
        # L2: Redis缓存 (延迟初始化)
        self._redis_client = None
        
        # L3: 文件缓存目录（Vercel环境下跳过）
        self._cache_dir = None
        if not IS_VERCEL:
            self._cache_dir = Path(PromptCacheConfig.L3_CACHE_DIR)
            try:
                self._cache_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.warning(f"无法创建缓存目录，将仅使用内存和Redis缓存: {e}")
                self._cache_dir = None
        else:
            logger.info("Vercel环境检测到，跳过文件缓存")
        
        # 统计信息
        self._stats = {
            "l1_hits": 0,
            "l1_misses": 0,
            "l2_hits": 0,
            "l2_misses": 0,
            "l3_hits": 0,
            "l3_misses": 0,
            "total_gets": 0,
            "total_sets": 0
        }
        self._stats_lock = threading.Lock()
        
        self._initialized = True
        logger.info("MultiLevelPromptCache initialized")
    
    def _get_redis_client(self):
        """延迟获取Redis客户端"""
        if self._redis_client is None:
            try:
                from .cache_client_factory import CacheClientFactory
                from src.config import settings
                if settings.cache_client_type == "redis":
                    from .redis_client import RedisCacheClient
                    self._redis_client = RedisCacheClient
            except Exception as e:
                logger.warning(f"Redis client not available: {e}")
        return self._redis_client
    
    @staticmethod
    def generate_cache_key(template_id: str, variables: Dict[str, Any]) -> str:
        """生成缓存键"""
        var_str = json.dumps(variables, sort_keys=True, ensure_ascii=False)
        content = f"{template_id}:{var_str}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _update_stats(self, stat_name: str):
        """更新统计信息"""
        with self._stats_lock:
            if stat_name in self._stats:
                self._stats[stat_name] += 1
    
    # ========== L1 内存缓存 ==========
    def _l1_get(self, key: str) -> Optional[str]:
        """从L1内存缓存获取"""
        with self._l1_lock:
            value = self._l1_cache.get(key)
            if value is not None:
                self._update_stats("l1_hits")
                return value
            self._update_stats("l1_misses")
            return None
    
    def _l1_set(self, key: str, value: str):
        """设置L1内存缓存"""
        with self._l1_lock:
            self._l1_cache[key] = value
    
    # ========== L2 Redis缓存 ==========
    def _l2_get(self, key: str) -> Optional[str]:
        """从L2 Redis缓存获取"""
        redis_client = self._get_redis_client()
        if redis_client is None:
            self._update_stats("l2_misses")
            return None
        
        try:
            redis_key = f"{PromptCacheConfig.L2_PREFIX}{key}"
            if hasattr(redis_client, 'redis_client') and redis_client.redis_client:
                value = redis_client.redis_client.get(redis_key)
                if value:
                    self._update_stats("l2_hits")
                    return value.decode() if isinstance(value, bytes) else value
        except Exception as e:
            logger.warning(f"L2 cache get error: {e}")
        
        self._update_stats("l2_misses")
        return None
    
    def _l2_set(self, key: str, value: str, ttl: int = None):
        """设置L2 Redis缓存（带 TTL 抖动防止雪崩）"""
        redis_client = self._get_redis_client()
        if redis_client is None:
            return
        
        try:
            redis_key = f"{PromptCacheConfig.L2_PREFIX}{key}"
            if hasattr(redis_client, 'redis_client') and redis_client.redis_client:
                # 使用带抖动的 TTL，防止缓存雪崩
                actual_ttl = ttl or PromptCacheConfig.get_ttl_with_jitter(
                    PromptCacheConfig.L2_TTL_SECONDS,
                    PromptCacheConfig.L2_TTL_JITTER
                )
                redis_client.redis_client.setex(
                    redis_key,
                    actual_ttl,
                    value
                )
        except Exception as e:
            logger.warning(f"L2 cache set error: {e}")
    
    # ========== L3 文件缓存 ==========
    def _l3_get(self, key: str) -> Optional[str]:
        """从L3文件缓存获取"""
        if self._cache_dir is None:
            self._update_stats("l3_misses")
            return None
        cache_file = self._cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            self._update_stats("l3_misses")
            return None
        
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 检查TTL
            created_at = datetime.fromisoformat(data.get("created_at", ""))
            if datetime.now() - created_at > timedelta(seconds=PromptCacheConfig.L3_TTL_SECONDS):
                cache_file.unlink()
                self._update_stats("l3_misses")
                return None
            
            self._update_stats("l3_hits")
            return data.get("content")
        except Exception as e:
            logger.warning(f"L3 cache get error: {e}")
            self._update_stats("l3_misses")
            return None
    
    def _l3_set(self, key: str, value: str):
        """设置L3文件缓存"""
        if self._cache_dir is None:
            return
        cache_file = self._cache_dir / f"{key}.json"
        
        try:
            data = {
                "content": value,
                "created_at": datetime.now().isoformat(),
                "key": key
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"L3 cache set error: {e}")
    
    # ========== 公开接口 ==========
    def get(self, template_id: str, variables: Dict[str, Any]) -> Optional[str]:
        """
        多级缓存获取
        查询顺序: L1 → L2 → L3
        命中低级缓存时会回填高级缓存
        
        注意：返回 None 表示缓存未命中，返回空字符串表示缓存的空值
        """
        key = self.generate_cache_key(template_id, variables)
        self._update_stats("total_gets")
        
        # L1查询
        value = self._l1_get(key)
        if value is not None:
            # 检查是否为空值标记（防止缓存穿透）
            if value == CACHE_NULL_VALUE:
                return ""  # 返回空字符串表示缓存的空值
            return value
        
        # L2查询
        value = self._l2_get(key)
        if value is not None:
            if value == CACHE_NULL_VALUE:
                self._l1_set(key, CACHE_NULL_VALUE)  # 回填L1
                return ""
            self._l1_set(key, value)  # 回填L1
            return value
        
        # L3查询
        value = self._l3_get(key)
        if value is not None:
            if value == CACHE_NULL_VALUE:
                self._l1_set(key, CACHE_NULL_VALUE)
                self._l2_set(key, CACHE_NULL_VALUE, ttl=NULL_VALUE_TTL_SECONDS)
                return ""
            self._l1_set(key, value)  # 回填L1
            self._l2_set(key, value)  # 回填L2
            return value
        
        return None
    
    def set_null(self, template_id: str, variables: Dict[str, Any]):
        """
        缓存空值（防止缓存穿透）
        
        当查询结果确实为空时调用，避免重复查询数据库/API
        空值缓存使用较短的 TTL
        """
        key = self.generate_cache_key(template_id, variables)
        self._l1_set(key, CACHE_NULL_VALUE)
        self._l2_set(key, CACHE_NULL_VALUE, ttl=NULL_VALUE_TTL_SECONDS)
    
    def set(self, template_id: str, variables: Dict[str, Any], content: str,
            levels: List[int] = None):
        """
        多级缓存设置
        levels: 指定要写入的缓存层级，默认全部写入
        """
        key = self.generate_cache_key(template_id, variables)
        self._update_stats("total_sets")
        
        if levels is None:
            levels = [1, 2, 3]
        
        if 1 in levels:
            self._l1_set(key, content)
        if 2 in levels:
            self._l2_set(key, content)
        if 3 in levels:
            self._l3_set(key, content)
    
    def invalidate(self, template_id: str, variables: Dict[str, Any] = None):
        """
        缓存失效
        如果不提供variables，则失效该模板的所有缓存
        """
        if variables is not None:
            key = self.generate_cache_key(template_id, variables)
            self._invalidate_key(key)
        else:
            # 失效该模板所有缓存（需要遍历）
            self._invalidate_template(template_id)
    
    def _invalidate_key(self, key: str):
        """失效特定键"""
        # L1
        with self._l1_lock:
            self._l1_cache.pop(key, None)
        
        # L2
        redis_client = self._get_redis_client()
        if redis_client and hasattr(redis_client, 'redis_client') and redis_client.redis_client:
            try:
                redis_client.redis_client.delete(f"{PromptCacheConfig.L2_PREFIX}{key}")
            except Exception:
                pass
        
        # L3
        if self._cache_dir is not None:
            cache_file = self._cache_dir / f"{key}.json"
            if cache_file.exists():
                cache_file.unlink()
    
    def _invalidate_template(self, template_id: str):
        """失效模板所有缓存（仅清理L3，因为L1/L2有TTL）"""
        if self._cache_dir is None:
            return
        for cache_file in self._cache_dir.glob("*.json"):
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # 可以在set时保存template_id便于筛选
                cache_file.unlink()
            except Exception:
                pass
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self._stats_lock:
            stats = self._stats.copy()
        
        # 计算命中率
        total_l1 = stats["l1_hits"] + stats["l1_misses"]
        total_l2 = stats["l2_hits"] + stats["l2_misses"]
        total_l3 = stats["l3_hits"] + stats["l3_misses"]
        
        stats["l1_hit_rate"] = stats["l1_hits"] / total_l1 if total_l1 > 0 else 0
        stats["l2_hit_rate"] = stats["l2_hits"] / total_l2 if total_l2 > 0 else 0
        stats["l3_hit_rate"] = stats["l3_hits"] / total_l3 if total_l3 > 0 else 0
        stats["l1_size"] = len(self._l1_cache)
        
        return stats
    
    def preload_high_freq_templates(self, template_manager):
        """预加载高频模板到L1缓存"""
        for tool_name in PromptCacheConfig.HIGH_FREQ_TOOLS:
            try:
                template = template_manager.get_template(tool_name)
                if template:
                    # 使用空变量预渲染基础模板
                    content = template_manager.render_template(tool_name, {})
                    self.set(tool_name, {}, content, levels=[1])
                    logger.debug(f"Preloaded template: {tool_name}")
            except Exception as e:
                logger.warning(f"Failed to preload template {tool_name}: {e}")
    
    def clear_all(self):
        """清空所有缓存"""
        # L1
        with self._l1_lock:
            self._l1_cache.clear()
        
        # L3
        if self._cache_dir is not None:
            for cache_file in self._cache_dir.glob("*.json"):
                try:
                    cache_file.unlink()
                except Exception:
                    pass
        
        logger.info("All caches cleared")


# 全局单例
prompt_cache = MultiLevelPromptCache()
