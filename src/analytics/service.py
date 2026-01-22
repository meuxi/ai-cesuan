"""
统计服务
"""

import uuid
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict

from .models import UsageRecord, UsageStats, DivinationType

logger = logging.getLogger(__name__)


class AnalyticsService:
    """统计服务"""
    
    def __init__(self, max_records: int = 10000):
        """
        Args:
            max_records: 最大记录数（内存存储时的限制）
        """
        self._records: List[UsageRecord] = []
        self._max_records = max_records
    
    def record_usage(
        self,
        divination_type: DivinationType,
        model_name: str = "",
        provider: str = "",
        tokens_used: int = 0,
        cost: float = 0.0,
        response_time_ms: int = 0,
        success: bool = True,
        error_message: str = "",
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        **kwargs
    ) -> UsageRecord:
        """记录一次使用"""
        record = UsageRecord(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            divination_type=divination_type,
            model_name=model_name,
            provider=provider,
            tokens_used=tokens_used,
            cost=cost,
            response_time_ms=response_time_ms,
            success=success,
            error_message=error_message,
            user_id=user_id,
            ip_address=ip_address,
            metadata=kwargs,
        )
        
        self._records.append(record)
        
        # 限制记录数
        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records:]
        
        logger.debug(f"记录使用: {divination_type.value}, tokens={tokens_used}")
        return record
    
    def get_records(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        divination_type: Optional[DivinationType] = None,
        success_only: bool = False,
        limit: int = 100,
    ) -> List[UsageRecord]:
        """获取记录"""
        records = self._records
        
        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]
        
        if divination_type:
            records = [r for r in records if r.divination_type == divination_type]
        
        if success_only:
            records = [r for r in records if r.success]
        
        return records[-limit:]
    
    def get_stats(
        self,
        period: str = "day",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> UsageStats:
        """
        获取统计数据
        
        Args:
            period: 统计周期 (day/week/month)
            start_date: 开始日期
            end_date: 结束日期
        """
        now = datetime.now()
        
        if not end_date:
            end_date = now
        
        if not start_date:
            if period == "day":
                start_date = now - timedelta(days=1)
            elif period == "week":
                start_date = now - timedelta(weeks=1)
            elif period == "month":
                start_date = now - timedelta(days=30)
            else:
                start_date = now - timedelta(days=1)
        
        records = self.get_records(start_date=start_date, end_date=end_date, limit=10000)
        
        if not records:
            return UsageStats(
                period=period,
                start_date=start_date,
                end_date=end_date,
            )
        
        # 统计计算
        total = len(records)
        successful = sum(1 for r in records if r.success)
        failed = total - successful
        total_tokens = sum(r.tokens_used for r in records)
        total_cost = sum(r.cost for r in records)
        total_response_time = sum(r.response_time_ms for r in records)
        
        by_type: Dict[str, int] = defaultdict(int)
        by_model: Dict[str, int] = defaultdict(int)
        by_provider: Dict[str, int] = defaultdict(int)
        
        for r in records:
            by_type[r.divination_type.value] += 1
            if r.model_name:
                by_model[r.model_name] += 1
            if r.provider:
                by_provider[r.provider] += 1
        
        return UsageStats(
            period=period,
            start_date=start_date,
            end_date=end_date,
            total_requests=total,
            successful_requests=successful,
            failed_requests=failed,
            total_tokens=total_tokens,
            total_cost=total_cost,
            avg_response_time_ms=total_response_time / total if total > 0 else 0,
            by_type=dict(by_type),
            by_model=dict(by_model),
            by_provider=dict(by_provider),
            error_rate=failed / total if total > 0 else 0,
        )
    
    def get_daily_stats(self, days: int = 7) -> List[Dict[str, Any]]:
        """获取每日统计"""
        result = []
        now = datetime.now()
        
        for i in range(days):
            date = now - timedelta(days=i)
            start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            stats = self.get_stats(period="day", start_date=start, end_date=end)
            result.append({
                "date": start.strftime("%Y-%m-%d"),
                **stats.to_dict()
            })
        
        return result
    
    def get_top_models(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取使用最多的模型"""
        model_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "count": 0,
            "tokens": 0,
            "cost": 0,
        })
        
        for r in self._records:
            if r.model_name:
                model_stats[r.model_name]["count"] += 1
                model_stats[r.model_name]["tokens"] += r.tokens_used
                model_stats[r.model_name]["cost"] += r.cost
        
        sorted_models = sorted(
            model_stats.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:limit]
        
        return [
            {"model": name, **stats}
            for name, stats in sorted_models
        ]
    
    def clear_records(self):
        """清空记录"""
        self._records.clear()
        logger.info("已清空所有使用记录")


# 全局服务实例
_default_service: Optional[AnalyticsService] = None


def get_analytics_service() -> AnalyticsService:
    """获取全局统计服务"""
    global _default_service
    if _default_service is None:
        _default_service = AnalyticsService()
    return _default_service
