"""
用户配额管理系统
支持多层级用户配额控制和使用量追踪
"""
import os
import atexit
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, date
import threading
import logging
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# 后台文件 IO 线程池（避免阻塞主线程）
_io_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="quota_io")

# 检测是否在Vercel环境（只读文件系统）
IS_VERCEL = os.getenv("VERCEL") == "1"

# 延迟导入 settings 避免循环引用
def _get_settings():
    from src.config import settings
    return settings


class QuotaTier(Enum):
    """用户等级"""
    FREE = "free"
    VIP = "vip"
    PREMIUM = "premium"
    UNLIMITED = "unlimited"


@dataclass
class TierQuotaConfig:
    """等级配额配置"""
    daily_calls: int           # 每日调用次数限制
    daily_tokens: int          # 每日token限制
    max_output_tokens: int     # 单次最大输出token
    allowed_models: list       # 允许使用的模型
    priority: int              # 请求优先级 (越高越优先)


def get_tier_configs() -> Dict[QuotaTier, TierQuotaConfig]:
    """
    动态获取等级配置（从环境变量读取）
    
    【用户体验优先模式】
    - 移除所有输出限制，所有等级统一使用最大配置
    - 专注于生成深度、专业的命理解析
    - 让AI充分发挥专业能力
    """
    settings = _get_settings()
    
    # 统一的无限制输出配置
    unlimited_output_tokens = 32000
    all_models = ["*"]  # 所有用户都可以使用所有模型
    
    return {
        QuotaTier.FREE: TierQuotaConfig(
            daily_calls=settings.quota_free_daily_calls,
            daily_tokens=settings.quota_free_daily_tokens,
            max_output_tokens=unlimited_output_tokens,  # 无限制输出
            allowed_models=all_models,
            priority=1
        ),
        QuotaTier.VIP: TierQuotaConfig(
            daily_calls=settings.quota_vip_daily_calls,
            daily_tokens=settings.quota_vip_daily_tokens,
            max_output_tokens=unlimited_output_tokens,  # 无限制输出
            allowed_models=all_models,
            priority=5
        ),
        QuotaTier.PREMIUM: TierQuotaConfig(
            daily_calls=settings.quota_premium_daily_calls,
            daily_tokens=settings.quota_premium_daily_tokens,
            max_output_tokens=unlimited_output_tokens,  # 无限制输出
            allowed_models=all_models,
            priority=10
        ),
        QuotaTier.UNLIMITED: TierQuotaConfig(
            daily_calls=-1,  # -1 表示无限制
            daily_tokens=-1,
            max_output_tokens=unlimited_output_tokens,  # 无限制输出
            allowed_models=all_models,
            priority=100
        )
    }


@dataclass
class UserUsage:
    """用户使用情况"""
    user_id: str
    date: str
    call_count: int = 0
    token_count: int = 0
    cost: float = 0.0
    last_call_time: Optional[str] = None


class UserQuotaManager:
    """用户配额管理器"""
    
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
        
        # 用户使用数据存储 (内存 + 文件持久化)
        self._usage_data: Dict[str, UserUsage] = {}
        self._usage_lock = threading.Lock()
        
        # 用户等级映射
        self._user_tiers: Dict[str, QuotaTier] = {}
        
        # 数据持久化目录（Vercel环境下跳过文件存储）
        self._data_dir = None
        if not IS_VERCEL:
            self._data_dir = Path("data/quota")
            try:
                self._data_dir.mkdir(parents=True, exist_ok=True)
                # 加载持久化数据
                self._load_usage_data()
            except OSError as e:
                logger.warning(f"无法创建数据目录，将仅使用内存存储: {e}")
                self._data_dir = None
        else:
            logger.info("Vercel环境检测到，使用内存存储配额数据")
        
        self._initialized = True
        logger.info("UserQuotaManager initialized")
    
    def _get_usage_key(self, user_id: str) -> str:
        """获取用户使用数据的键（按日期）"""
        return f"{user_id}:{date.today().isoformat()}"
    
    def _load_usage_data(self):
        """加载今日使用数据"""
        if self._data_dir is None:
            return
        today_file = self._data_dir / f"usage_{date.today().isoformat()}.json"
        if today_file.exists():
            try:
                with open(today_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for key, usage_dict in data.items():
                    self._usage_data[key] = UserUsage(**usage_dict)
                logger.info(f"Loaded {len(self._usage_data)} usage records")
            except Exception as e:
                logger.error(f"Failed to load usage data: {e}")
    
    def _save_usage_data(self, async_save: bool = True):
        """
        保存使用数据
        
        Args:
            async_save: 是否异步保存（默认 True，使用后台线程避免阻塞）
        """
        if self._data_dir is None:
            return
        
        # 准备要保存的数据（在锁内完成）
        today_str = date.today().isoformat()
        today_file = self._data_dir / f"usage_{today_str}.json"
        
        data = {}
        with self._usage_lock:
            for key, usage in self._usage_data.items():
                if usage.date == today_str:
                    data[key] = {
                        "user_id": usage.user_id,
                        "date": usage.date,
                        "call_count": usage.call_count,
                        "token_count": usage.token_count,
                        "cost": usage.cost,
                        "last_call_time": usage.last_call_time
                    }
        
        def _do_save():
            """实际的文件写入操作"""
            try:
                with open(today_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Failed to save usage data: {e}")
        
        if async_save:
            # 异步保存：提交到后台线程池，不阻塞主线程
            _io_executor.submit(_do_save)
        else:
            # 同步保存：直接执行（用于程序退出时的强制保存）
            _do_save()
    
    def force_save(self):
        """强制同步保存（用于程序退出时）"""
        self._save_usage_data(async_save=False)
    
    def get_user_tier(self, user_id: str) -> QuotaTier:
        """获取用户等级"""
        return self._user_tiers.get(user_id, QuotaTier.FREE)
    
    def set_user_tier(self, user_id: str, tier: QuotaTier):
        """设置用户等级"""
        self._user_tiers[user_id] = tier
        logger.info(f"User {user_id} tier set to {tier.value}")
    
    def get_tier_config(self, tier: QuotaTier) -> TierQuotaConfig:
        """获取等级配置"""
        configs = get_tier_configs()
        return configs.get(tier, configs[QuotaTier.FREE])
    
    def get_user_usage(self, user_id: str) -> UserUsage:
        """获取用户今日使用情况"""
        key = self._get_usage_key(user_id)
        with self._usage_lock:
            if key not in self._usage_data:
                self._usage_data[key] = UserUsage(
                    user_id=user_id,
                    date=date.today().isoformat()
                )
            return self._usage_data[key]
    
    def check_quota(self, user_id: str) -> Dict[str, Any]:
        """
        检查用户配额
        返回: {"allowed": bool, "reason": str, "remaining": dict}
        """
        tier = self.get_user_tier(user_id)
        config = self.get_tier_config(tier)
        usage = self.get_user_usage(user_id)
        
        result = {
            "allowed": True,
            "reason": "",
            "tier": tier.value,
            "remaining": {
                "calls": config.daily_calls - usage.call_count if config.daily_calls > 0 else -1,
                "tokens": config.daily_tokens - usage.token_count if config.daily_tokens > 0 else -1
            }
        }
        
        # 无限制用户直接通过
        if tier == QuotaTier.UNLIMITED:
            return result
        
        # 检查调用次数
        if config.daily_calls > 0 and usage.call_count >= config.daily_calls:
            result["allowed"] = False
            result["reason"] = f"今日调用次数已达上限 ({config.daily_calls} 次)"
            return result
        
        # 检查token使用量
        if config.daily_tokens > 0 and usage.token_count >= config.daily_tokens:
            result["allowed"] = False
            result["reason"] = f"今日Token使用量已达上限 ({config.daily_tokens} tokens)"
            return result
        
        return result
    
    def consume_quota(self, user_id: str, tokens: int = 0, cost: float = 0.0) -> bool:
        """
        消费配额
        返回是否成功
        """
        # 先检查配额
        check_result = self.check_quota(user_id)
        if not check_result["allowed"]:
            return False
        
        key = self._get_usage_key(user_id)
        with self._usage_lock:
            if key not in self._usage_data:
                self._usage_data[key] = UserUsage(
                    user_id=user_id,
                    date=date.today().isoformat()
                )
            
            usage = self._usage_data[key]
            usage.call_count += 1
            usage.token_count += tokens
            usage.cost += cost
            usage.last_call_time = datetime.now().isoformat()
        
        # 异步保存
        self._save_usage_data()
        
        return True
    
    def get_max_output_tokens(self, user_id: str) -> int:
        """获取用户允许的最大输出token数"""
        tier = self.get_user_tier(user_id)
        config = self.get_tier_config(tier)
        return config.max_output_tokens
    
    def is_model_allowed(self, user_id: str, model: str) -> bool:
        """检查用户是否可以使用指定模型"""
        tier = self.get_user_tier(user_id)
        config = self.get_tier_config(tier)
        
        if "*" in config.allowed_models:
            return True
        
        return model in config.allowed_models
    
    def get_user_priority(self, user_id: str) -> int:
        """获取用户请求优先级"""
        tier = self.get_user_tier(user_id)
        config = self.get_tier_config(tier)
        return config.priority
    
    def get_usage_summary(self, user_id: str) -> Dict[str, Any]:
        """获取用户使用摘要"""
        tier = self.get_user_tier(user_id)
        config = self.get_tier_config(tier)
        usage = self.get_user_usage(user_id)
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "date": usage.date,
            "usage": {
                "calls": usage.call_count,
                "tokens": usage.token_count,
                "cost": round(usage.cost, 4)
            },
            "limits": {
                "daily_calls": config.daily_calls,
                "daily_tokens": config.daily_tokens,
                "max_output_tokens": config.max_output_tokens
            },
            "remaining": {
                "calls": max(0, config.daily_calls - usage.call_count) if config.daily_calls > 0 else -1,
                "tokens": max(0, config.daily_tokens - usage.token_count) if config.daily_tokens > 0 else -1
            },
            "last_call_time": usage.last_call_time
        }
    
    def cleanup_old_data(self, days_to_keep: int = 7):
        """清理过期数据"""
        if self._data_dir is None:
            return
        
        from datetime import timedelta
        
        cutoff_date = date.today() - timedelta(days=days_to_keep)
        
        for file in self._data_dir.glob("usage_*.json"):
            try:
                file_date_str = file.stem.replace("usage_", "")
                file_date = date.fromisoformat(file_date_str)
                if file_date < cutoff_date:
                    file.unlink()
                    logger.info(f"Cleaned up old usage file: {file.name}")
            except Exception as e:
                logger.warning(f"Failed to cleanup file {file}: {e}")


# 全局单例
quota_manager = UserQuotaManager()
