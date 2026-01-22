"""
成本监控和告警系统
追踪AI调用成本，支持阈值告警
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from collections import defaultdict
import threading
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class AlertThreshold:
    """告警阈值配置"""
    hourly_cost: float = 10.0      # 每小时成本阈值（美元）
    daily_cost: float = 100.0      # 每日成本阈值
    single_call_cost: float = 1.0  # 单次调用成本阈值
    error_rate: float = 0.1        # 错误率阈值 (10%)
    latency_p95: float = 10.0      # P95延迟阈值（秒）


@dataclass
class CallRecord:
    """调用记录"""
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency: float  # 秒
    success: bool
    tool_name: str = ""
    user_id: str = ""


class CostMonitor:
    """成本监控器"""
    
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
        
        # 调用记录（按小时分桶）
        self._hourly_records: Dict[str, List[CallRecord]] = defaultdict(list)
        self._records_lock = threading.Lock()
        
        # 统计数据
        self._stats = {
            "total_calls": 0,
            "total_cost": 0.0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_errors": 0,
            "start_time": datetime.now().isoformat()
        }
        
        # 告警阈值
        self._thresholds = AlertThreshold()
        
        # 告警回调
        self._alert_callbacks: List[Callable] = []
        
        # 数据持久化
        self._data_dir = Path("data/monitoring")
        self._data_dir.mkdir(parents=True, exist_ok=True)
        
        self._initialized = True
        logger.info("CostMonitor initialized")
    
    def _get_hour_key(self, dt: datetime = None) -> str:
        """获取小时键"""
        if dt is None:
            dt = datetime.now()
        return dt.strftime("%Y-%m-%d-%H")
    
    def _get_day_key(self, dt: datetime = None) -> str:
        """获取日期键"""
        if dt is None:
            dt = datetime.now()
        return dt.strftime("%Y-%m-%d")
    
    def record_call(self, model: str, input_tokens: int, output_tokens: int,
                    cost: float, latency: float, success: bool,
                    tool_name: str = "", user_id: str = ""):
        """记录一次AI调用"""
        record = CallRecord(
            timestamp=datetime.now(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            latency=latency,
            success=success,
            tool_name=tool_name,
            user_id=user_id
        )
        
        hour_key = self._get_hour_key()
        
        with self._records_lock:
            self._hourly_records[hour_key].append(record)
            
            # 更新统计
            self._stats["total_calls"] += 1
            self._stats["total_cost"] += cost
            self._stats["total_input_tokens"] += input_tokens
            self._stats["total_output_tokens"] += output_tokens
            if not success:
                self._stats["total_errors"] += 1
        
        # 检查告警
        self._check_alerts(record)
    
    def _check_alerts(self, record: CallRecord):
        """检查是否需要触发告警"""
        alerts = []
        
        # 单次调用成本告警
        if record.cost > self._thresholds.single_call_cost:
            alerts.append({
                "type": "high_single_cost",
                "message": f"单次调用成本过高: ${record.cost:.4f}",
                "value": record.cost,
                "threshold": self._thresholds.single_call_cost
            })
        
        # 每小时成本告警
        hourly_cost = self.get_hourly_cost()
        if hourly_cost > self._thresholds.hourly_cost:
            alerts.append({
                "type": "high_hourly_cost",
                "message": f"每小时成本超标: ${hourly_cost:.2f}",
                "value": hourly_cost,
                "threshold": self._thresholds.hourly_cost
            })
        
        # 每日成本告警
        daily_cost = self.get_daily_cost()
        if daily_cost > self._thresholds.daily_cost:
            alerts.append({
                "type": "high_daily_cost",
                "message": f"每日成本超标: ${daily_cost:.2f}",
                "value": daily_cost,
                "threshold": self._thresholds.daily_cost
            })
        
        # 错误率告警
        error_rate = self.get_error_rate()
        if error_rate > self._thresholds.error_rate:
            alerts.append({
                "type": "high_error_rate",
                "message": f"错误率过高: {error_rate*100:.1f}%",
                "value": error_rate,
                "threshold": self._thresholds.error_rate
            })
        
        # 触发告警回调
        for alert in alerts:
            self._trigger_alert(alert)
    
    def _trigger_alert(self, alert: Dict[str, Any]):
        """触发告警"""
        logger.warning(f"ALERT: {alert['type']} - {alert['message']}")
        
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")
    
    def register_alert_callback(self, callback: Callable):
        """注册告警回调"""
        self._alert_callbacks.append(callback)
    
    def set_thresholds(self, **kwargs):
        """设置告警阈值"""
        for key, value in kwargs.items():
            if hasattr(self._thresholds, key):
                setattr(self._thresholds, key, value)
    
    def get_hourly_cost(self, hour_key: str = None) -> float:
        """获取指定小时的成本"""
        if hour_key is None:
            hour_key = self._get_hour_key()
        
        with self._records_lock:
            records = self._hourly_records.get(hour_key, [])
            return sum(r.cost for r in records)
    
    def get_daily_cost(self, day_key: str = None) -> float:
        """获取指定日期的成本"""
        if day_key is None:
            day_key = self._get_day_key()
        
        total = 0.0
        with self._records_lock:
            for hour_key, records in self._hourly_records.items():
                if hour_key.startswith(day_key):
                    total += sum(r.cost for r in records)
        return total
    
    def get_error_rate(self, hours: int = 1) -> float:
        """获取最近N小时的错误率"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        total = 0
        errors = 0
        
        with self._records_lock:
            for records in self._hourly_records.values():
                for r in records:
                    if r.timestamp >= cutoff:
                        total += 1
                        if not r.success:
                            errors += 1
        
        return errors / total if total > 0 else 0.0
    
    def get_latency_stats(self, hours: int = 1) -> Dict[str, float]:
        """获取延迟统计"""
        cutoff = datetime.now() - timedelta(hours=hours)
        latencies = []
        
        with self._records_lock:
            for records in self._hourly_records.values():
                for r in records:
                    if r.timestamp >= cutoff and r.success:
                        latencies.append(r.latency)
        
        if not latencies:
            return {"avg": 0, "p50": 0, "p95": 0, "p99": 0}
        
        latencies.sort()
        n = len(latencies)
        
        return {
            "avg": sum(latencies) / n,
            "p50": latencies[int(n * 0.5)],
            "p95": latencies[int(n * 0.95)] if n >= 20 else latencies[-1],
            "p99": latencies[int(n * 0.99)] if n >= 100 else latencies[-1]
        }
    
    def get_model_stats(self, hours: int = 24) -> Dict[str, Dict[str, Any]]:
        """获取各模型使用统计"""
        cutoff = datetime.now() - timedelta(hours=hours)
        model_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"calls": 0, "cost": 0.0, "tokens": 0, "errors": 0}
        )
        
        with self._records_lock:
            for records in self._hourly_records.values():
                for r in records:
                    if r.timestamp >= cutoff:
                        stats = model_stats[r.model]
                        stats["calls"] += 1
                        stats["cost"] += r.cost
                        stats["tokens"] += r.input_tokens + r.output_tokens
                        if not r.success:
                            stats["errors"] += 1
        
        return dict(model_stats)
    
    def get_tool_stats(self, hours: int = 24) -> Dict[str, Dict[str, Any]]:
        """获取各工具使用统计"""
        cutoff = datetime.now() - timedelta(hours=hours)
        tool_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"calls": 0, "cost": 0.0, "avg_latency": 0.0, "latencies": []}
        )
        
        with self._records_lock:
            for records in self._hourly_records.values():
                for r in records:
                    if r.timestamp >= cutoff and r.tool_name:
                        stats = tool_stats[r.tool_name]
                        stats["calls"] += 1
                        stats["cost"] += r.cost
                        stats["latencies"].append(r.latency)
        
        # 计算平均延迟
        for tool, stats in tool_stats.items():
            if stats["latencies"]:
                stats["avg_latency"] = sum(stats["latencies"]) / len(stats["latencies"])
            del stats["latencies"]
        
        return dict(tool_stats)
    
    def get_summary(self) -> Dict[str, Any]:
        """获取监控摘要"""
        return {
            "global": self._stats.copy(),
            "hourly_cost": self.get_hourly_cost(),
            "daily_cost": self.get_daily_cost(),
            "error_rate": self.get_error_rate(),
            "latency": self.get_latency_stats(),
            "thresholds": {
                "hourly_cost": self._thresholds.hourly_cost,
                "daily_cost": self._thresholds.daily_cost,
                "single_call_cost": self._thresholds.single_call_cost,
                "error_rate": self._thresholds.error_rate
            }
        }
    
    def cleanup_old_records(self, hours_to_keep: int = 48):
        """清理过期记录"""
        cutoff_key = self._get_hour_key(datetime.now() - timedelta(hours=hours_to_keep))
        
        with self._records_lock:
            keys_to_remove = [k for k in self._hourly_records.keys() if k < cutoff_key]
            for key in keys_to_remove:
                del self._hourly_records[key]
        
        logger.info(f"Cleaned up {len(keys_to_remove)} old hourly records")
    
    def export_daily_report(self, day_key: str = None) -> Dict[str, Any]:
        """导出日报"""
        if day_key is None:
            day_key = self._get_day_key()
        
        report = {
            "date": day_key,
            "generated_at": datetime.now().isoformat(),
            "cost": self.get_daily_cost(day_key),
            "models": self.get_model_stats(24),
            "tools": self.get_tool_stats(24),
            "latency": self.get_latency_stats(24),
            "error_rate": self.get_error_rate(24)
        }
        
        # 保存报告
        report_file = self._data_dir / f"report_{day_key}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        return report


# 全局单例
cost_monitor = CostMonitor()
