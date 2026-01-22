"""
统计数据模型
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DivinationType(Enum):
    """占卜类型"""
    BAZI = "bazi"
    LIUYAO = "liuyao"
    TAROT = "tarot"
    QIMEN = "qimen"
    DALIUREN = "daliuren"
    XIAOLIU = "xiaoliu"
    CHOUQIAN = "chouqian"
    LIFE_KLINE = "life_kline"
    OTHER = "other"


@dataclass
class UsageRecord:
    """使用记录"""
    id: str                                    # 记录ID
    timestamp: datetime                        # 时间戳
    divination_type: DivinationType            # 占卜类型
    model_name: str = ""                       # 使用的模型
    provider: str = ""                         # Provider
    tokens_used: int = 0                       # Token消耗
    cost: float = 0.0                          # 成本
    response_time_ms: int = 0                  # 响应时间
    success: bool = True                       # 是否成功
    error_message: str = ""                    # 错误信息
    user_id: Optional[str] = None              # 用户ID
    ip_address: Optional[str] = None           # IP地址
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "divination_type": self.divination_type.value,
            "model_name": self.model_name,
            "provider": self.provider,
            "tokens_used": self.tokens_used,
            "cost": self.cost,
            "response_time_ms": self.response_time_ms,
            "success": self.success,
            "error_message": self.error_message,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "metadata": self.metadata,
        }


@dataclass
class UsageStats:
    """使用统计"""
    period: str                                # 统计周期 (day/week/month)
    start_date: datetime                       # 开始日期
    end_date: datetime                         # 结束日期
    total_requests: int = 0                    # 总请求数
    successful_requests: int = 0               # 成功请求数
    failed_requests: int = 0                   # 失败请求数
    total_tokens: int = 0                      # 总Token消耗
    total_cost: float = 0.0                    # 总成本
    avg_response_time_ms: float = 0.0          # 平均响应时间
    by_type: Dict[str, int] = field(default_factory=dict)       # 按类型统计
    by_model: Dict[str, int] = field(default_factory=dict)      # 按模型统计
    by_provider: Dict[str, int] = field(default_factory=dict)   # 按Provider统计
    error_rate: float = 0.0                    # 错误率
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "total_tokens": self.total_tokens,
            "total_cost": round(self.total_cost, 4),
            "avg_response_time_ms": round(self.avg_response_time_ms, 2),
            "by_type": self.by_type,
            "by_model": self.by_model,
            "by_provider": self.by_provider,
            "error_rate": round(self.error_rate * 100, 2),
        }
