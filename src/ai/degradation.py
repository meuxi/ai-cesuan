"""
智能降级管理器
根据系统负载、成本和错误率动态调整服务策略
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import threading
import logging

logger = logging.getLogger(__name__)


class DegradationLevel(Enum):
    """降级级别"""
    NORMAL = "normal"        # 正常运行
    LIGHT = "light"          # 轻度降级
    MODERATE = "moderate"    # 中度降级
    SEVERE = "severe"        # 严重降级
    CRITICAL = "critical"    # 紧急降级


@dataclass
class DegradationPolicy:
    """降级策略配置"""
    level: DegradationLevel
    output_mode: str              # quick/standard/detailed
    max_output_tokens: int
    model_tier: str               # 使用的模型等级
    cache_only: bool              # 是否仅使用缓存
    reject_new_requests: bool     # 是否拒绝新请求
    description: str


# 预定义降级策略（用户体验优先：提升 max_output_tokens）
DEGRADATION_POLICIES: Dict[DegradationLevel, DegradationPolicy] = {
    DegradationLevel.NORMAL: DegradationPolicy(
        level=DegradationLevel.NORMAL,
        output_mode="detailed",
        max_output_tokens=16000,  # 用户体验优先：确保完整输出
        model_tier="premium",
        cache_only=False,
        reject_new_requests=False,
        description="正常运行，无降级"
    ),
    DegradationLevel.LIGHT: DegradationPolicy(
        level=DegradationLevel.LIGHT,
        output_mode="standard",
        max_output_tokens=12000,  # 用户体验优先：保证完整输出
        model_tier="standard",
        cache_only=False,
        reject_new_requests=False,
        description="轻度降级：减少输出token，使用标准模型"
    ),
    DegradationLevel.MODERATE: DegradationPolicy(
        level=DegradationLevel.MODERATE,
        output_mode="standard",
        max_output_tokens=8000,   # 用户体验优先：保证基本完整
        model_tier="economy",
        cache_only=False,
        reject_new_requests=False,
        description="中度降级：标准模式，经济模型"
    ),
    DegradationLevel.SEVERE: DegradationPolicy(
        level=DegradationLevel.SEVERE,
        output_mode="quick",
        max_output_tokens=4000,   # 严重降级时仍保证基本输出
        model_tier="economy",
        cache_only=True,
        reject_new_requests=False,
        description="严重降级：仅使用缓存，缓存未命中才请求AI"
    ),
    DegradationLevel.CRITICAL: DegradationPolicy(
        level=DegradationLevel.CRITICAL,
        output_mode="quick",
        max_output_tokens=2000,   # 紧急降级保留最小输出
        model_tier="economy",
        cache_only=True,
        reject_new_requests=True,
        description="紧急降级：拒绝新请求，仅返回缓存"
    )
}

# 模型等级映射
MODEL_TIERS: Dict[str, List[str]] = {
    "premium": ["gpt-4-turbo", "gpt-4", "claude-3-sonnet"],
    "standard": ["gpt-3.5-turbo", "claude-3-haiku", "deepseek-chat"],
    "economy": ["deepseek-chat", "gpt-3.5-turbo"]
}


@dataclass
class SystemMetrics:
    """系统指标"""
    hourly_cost: float = 0.0
    daily_cost: float = 0.0
    error_rate: float = 0.0
    latency_p95: float = 0.0
    active_requests: int = 0
    cache_hit_rate: float = 0.0


class DegradationManager:
    """智能降级管理器"""
    
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
        
        # 当前降级级别
        self._current_level = DegradationLevel.NORMAL
        self._level_lock = threading.Lock()
        
        # 降级阈值
        self._thresholds = {
            "hourly_cost_light": 8.0,      # 轻度降级阈值
            "hourly_cost_moderate": 15.0,  # 中度降级阈值
            "hourly_cost_severe": 25.0,    # 严重降级阈值
            "hourly_cost_critical": 40.0,  # 紧急降级阈值
            "error_rate_light": 0.05,
            "error_rate_moderate": 0.10,
            "error_rate_severe": 0.20,
            "error_rate_critical": 0.30,
            "latency_p95_light": 8.0,
            "latency_p95_moderate": 15.0,
            "latency_p95_severe": 25.0,
            "latency_p95_critical": 40.0
        }
        
        # 降级历史
        self._level_history: List[Dict[str, Any]] = []
        
        # 手动覆盖
        self._manual_override: Optional[DegradationLevel] = None
        
        self._initialized = True
        logger.info("DegradationManager initialized")
    
    def get_current_level(self) -> DegradationLevel:
        """获取当前降级级别"""
        with self._level_lock:
            if self._manual_override is not None:
                return self._manual_override
            return self._current_level
    
    def get_current_policy(self) -> DegradationPolicy:
        """获取当前降级策略"""
        level = self.get_current_level()
        return DEGRADATION_POLICIES[level]
    
    def evaluate_metrics(self, metrics: SystemMetrics) -> DegradationLevel:
        """
        评估系统指标并确定降级级别
        使用最高级别的降级需求
        """
        levels = []
        
        # 基于成本评估
        if metrics.hourly_cost >= self._thresholds["hourly_cost_critical"]:
            levels.append(DegradationLevel.CRITICAL)
        elif metrics.hourly_cost >= self._thresholds["hourly_cost_severe"]:
            levels.append(DegradationLevel.SEVERE)
        elif metrics.hourly_cost >= self._thresholds["hourly_cost_moderate"]:
            levels.append(DegradationLevel.MODERATE)
        elif metrics.hourly_cost >= self._thresholds["hourly_cost_light"]:
            levels.append(DegradationLevel.LIGHT)
        
        # 基于错误率评估
        if metrics.error_rate >= self._thresholds["error_rate_critical"]:
            levels.append(DegradationLevel.CRITICAL)
        elif metrics.error_rate >= self._thresholds["error_rate_severe"]:
            levels.append(DegradationLevel.SEVERE)
        elif metrics.error_rate >= self._thresholds["error_rate_moderate"]:
            levels.append(DegradationLevel.MODERATE)
        elif metrics.error_rate >= self._thresholds["error_rate_light"]:
            levels.append(DegradationLevel.LIGHT)
        
        # 基于延迟评估
        if metrics.latency_p95 >= self._thresholds["latency_p95_critical"]:
            levels.append(DegradationLevel.CRITICAL)
        elif metrics.latency_p95 >= self._thresholds["latency_p95_severe"]:
            levels.append(DegradationLevel.SEVERE)
        elif metrics.latency_p95 >= self._thresholds["latency_p95_moderate"]:
            levels.append(DegradationLevel.MODERATE)
        elif metrics.latency_p95 >= self._thresholds["latency_p95_light"]:
            levels.append(DegradationLevel.LIGHT)
        
        if not levels:
            return DegradationLevel.NORMAL
        
        # 返回最高级别
        level_order = [
            DegradationLevel.NORMAL,
            DegradationLevel.LIGHT,
            DegradationLevel.MODERATE,
            DegradationLevel.SEVERE,
            DegradationLevel.CRITICAL
        ]
        return max(levels, key=lambda x: level_order.index(x))
    
    def update_level(self, metrics: SystemMetrics):
        """更新降级级别"""
        new_level = self.evaluate_metrics(metrics)
        
        with self._level_lock:
            if new_level != self._current_level:
                old_level = self._current_level
                self._current_level = new_level
                
                # 记录历史
                self._level_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "from_level": old_level.value,
                    "to_level": new_level.value,
                    "metrics": {
                        "hourly_cost": metrics.hourly_cost,
                        "error_rate": metrics.error_rate,
                        "latency_p95": metrics.latency_p95
                    }
                })
                
                # 保留最近100条记录
                if len(self._level_history) > 100:
                    self._level_history = self._level_history[-100:]
                
                logger.warning(
                    f"Degradation level changed: {old_level.value} -> {new_level.value}"
                )
    
    def set_manual_override(self, level: Optional[DegradationLevel]):
        """设置手动覆盖级别"""
        with self._level_lock:
            self._manual_override = level
            if level:
                logger.info(f"Manual override set to: {level.value}")
            else:
                logger.info("Manual override cleared")
    
    def set_threshold(self, key: str, value: float):
        """设置降级阈值"""
        if key in self._thresholds:
            self._thresholds[key] = value
            logger.info(f"Threshold {key} set to {value}")
    
    def get_recommended_models(self) -> List[str]:
        """获取当前推荐使用的模型列表"""
        policy = self.get_current_policy()
        return MODEL_TIERS.get(policy.model_tier, MODEL_TIERS["economy"])
    
    def get_max_output_tokens(self) -> int:
        """获取当前允许的最大输出token数"""
        policy = self.get_current_policy()
        return policy.max_output_tokens
    
    def get_output_mode(self) -> str:
        """获取当前推荐的输出模式"""
        policy = self.get_current_policy()
        return policy.output_mode
    
    def should_use_cache_only(self) -> bool:
        """是否应该仅使用缓存"""
        policy = self.get_current_policy()
        return policy.cache_only
    
    def should_reject_request(self) -> bool:
        """是否应该拒绝新请求"""
        policy = self.get_current_policy()
        return policy.reject_new_requests
    
    def get_status(self) -> Dict[str, Any]:
        """获取降级状态"""
        policy = self.get_current_policy()
        return {
            "current_level": self.get_current_level().value,
            "manual_override": self._manual_override.value if self._manual_override else None,
            "policy": {
                "output_mode": policy.output_mode,
                "max_output_tokens": policy.max_output_tokens,
                "model_tier": policy.model_tier,
                "cache_only": policy.cache_only,
                "reject_new_requests": policy.reject_new_requests,
                "description": policy.description
            },
            "recommended_models": self.get_recommended_models(),
            "thresholds": self._thresholds.copy(),
            "recent_changes": self._level_history[-5:] if self._level_history else []
        }
    
    def apply_to_request(self, original_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        应用降级策略到请求参数
        """
        policy = self.get_current_policy()
        params = original_params.copy()
        
        # 限制max_tokens
        if "max_tokens" in params:
            params["max_tokens"] = min(params["max_tokens"], policy.max_output_tokens)
        else:
            params["max_tokens"] = policy.max_output_tokens
        
        # 添加输出模式标记
        params["_output_mode"] = policy.output_mode
        params["_degradation_level"] = policy.level.value
        params["_cache_only"] = policy.cache_only
        
        return params


# 全局单例
degradation_manager = DegradationManager()


def get_degradation_adjusted_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """便捷函数：获取降级调整后的参数"""
    return degradation_manager.apply_to_request(params)


def check_should_proceed() -> tuple[bool, str]:
    """
    便捷函数：检查是否应该继续处理请求
    返回: (should_proceed, reason)
    """
    if degradation_manager.should_reject_request():
        return False, "系统繁忙，暂时无法处理新请求，请稍后重试"
    return True, ""
