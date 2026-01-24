"""
流式响应性能监控
用于追踪和分析流式 AI 响应的性能指标

关键指标：
- TTFB (Time To First Byte): 从请求发出到收到第一个数据块的时间
- TTFC (Time To First Character): 首字显示时间（等于 TTFB + 前端处理时间）
- Chunk Rate: 每秒接收的数据块数量
- Total Latency: 总延迟（从请求到完成）
- Error Rate: 流式请求失败率
"""

import time
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from collections import deque
from threading import Lock

logger = logging.getLogger(__name__)


@dataclass
class StreamMetricsSnapshot:
    """流式指标快照（单次请求）"""
    request_id: str
    model: str
    start_time: float
    first_chunk_time: Optional[float] = None
    end_time: Optional[float] = None
    chunk_count: int = 0
    total_bytes: int = 0
    success: bool = True
    error_message: Optional[str] = None
    user_id: Optional[str] = None
    tool_name: Optional[str] = None
    
    @property
    def ttfb_ms(self) -> Optional[float]:
        """Time To First Byte (毫秒)"""
        if self.first_chunk_time and self.start_time:
            return (self.first_chunk_time - self.start_time) * 1000
        return None
    
    @property
    def total_latency_ms(self) -> Optional[float]:
        """总延迟 (毫秒)"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time) * 1000
        return None
    
    @property
    def chunk_rate(self) -> Optional[float]:
        """数据块速率 (chunks/s)"""
        if self.end_time and self.first_chunk_time and self.chunk_count > 0:
            duration = self.end_time - self.first_chunk_time
            if duration > 0:
                return self.chunk_count / duration
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "request_id": self.request_id,
            "model": self.model,
            "ttfb_ms": self.ttfb_ms,
            "total_latency_ms": self.total_latency_ms,
            "chunk_count": self.chunk_count,
            "chunk_rate": self.chunk_rate,
            "total_bytes": self.total_bytes,
            "success": self.success,
            "error_message": self.error_message,
            "user_id": self.user_id,
            "tool_name": self.tool_name,
        }


class StreamMetricsCollector:
    """
    流式指标收集器
    线程安全，支持聚合统计
    """
    
    # 请求超时阈值（秒），超过此时间的请求会被清理
    REQUEST_TIMEOUT_SECONDS = 300  # 5分钟
    # 清理检查间隔（秒）
    CLEANUP_INTERVAL_SECONDS = 60
    
    def __init__(self, max_history: int = 1000):
        """
        初始化收集器
        
        Args:
            max_history: 保留的历史记录数量
        """
        self._history: deque[StreamMetricsSnapshot] = deque(maxlen=max_history)
        self._lock = Lock()
        self._active_requests: Dict[str, StreamMetricsSnapshot] = {}
        self._last_cleanup_time: float = time.time()
    
    def _cleanup_stale_requests(self) -> int:
        """
        清理超时的活跃请求（防止内存泄漏）
        
        Returns:
            清理的请求数量
        """
        current_time = time.time()
        
        # 检查是否需要执行清理
        if current_time - self._last_cleanup_time < self.CLEANUP_INTERVAL_SECONDS:
            return 0
        
        self._last_cleanup_time = current_time
        cleaned_count = 0
        
        # 找出超时的请求
        stale_ids = [
            req_id for req_id, snapshot in self._active_requests.items()
            if current_time - snapshot.start_time > self.REQUEST_TIMEOUT_SECONDS
        ]
        
        # 清理超时请求
        for req_id in stale_ids:
            snapshot = self._active_requests.pop(req_id, None)
            if snapshot:
                snapshot.end_time = current_time
                snapshot.success = False
                snapshot.error_message = "请求超时被清理"
                self._history.append(snapshot)
                cleaned_count += 1
                logger.warning(f"[StreamMetrics] 清理超时请求: {req_id}")
        
        if cleaned_count > 0:
            logger.info(f"[StreamMetrics] 已清理 {cleaned_count} 个超时请求")
        
        return cleaned_count
    
    def start_request(
        self, 
        request_id: str, 
        model: str,
        user_id: Optional[str] = None,
        tool_name: Optional[str] = None
    ) -> StreamMetricsSnapshot:
        """
        开始追踪一个新的流式请求
        
        Args:
            request_id: 请求唯一标识
            model: 使用的模型名称
            user_id: 用户ID
            tool_name: 工具名称
        
        Returns:
            StreamMetricsSnapshot: 指标快照对象
        """
        snapshot = StreamMetricsSnapshot(
            request_id=request_id,
            model=model,
            start_time=time.time(),
            user_id=user_id,
            tool_name=tool_name,
        )
        
        with self._lock:
            # 定期清理超时请求
            self._cleanup_stale_requests()
            self._active_requests[request_id] = snapshot
        
        logger.debug(f"[StreamMetrics] 开始追踪请求: {request_id}")
        return snapshot
    
    def record_first_chunk(self, request_id: str) -> None:
        """记录首个数据块的时间"""
        with self._lock:
            if request_id in self._active_requests:
                snapshot = self._active_requests[request_id]
                if snapshot.first_chunk_time is None:
                    snapshot.first_chunk_time = time.time()
                    logger.debug(f"[StreamMetrics] 首个数据块: {request_id}, TTFB={snapshot.ttfb_ms:.2f}ms")
    
    def record_chunk(self, request_id: str, chunk_bytes: int = 0) -> None:
        """记录一个数据块"""
        with self._lock:
            if request_id in self._active_requests:
                snapshot = self._active_requests[request_id]
                snapshot.chunk_count += 1
                snapshot.total_bytes += chunk_bytes
    
    def complete_request(
        self, 
        request_id: str, 
        success: bool = True,
        error_message: Optional[str] = None
    ) -> Optional[StreamMetricsSnapshot]:
        """
        完成请求追踪
        
        Args:
            request_id: 请求唯一标识
            success: 是否成功
            error_message: 错误消息（如果失败）
        
        Returns:
            完成的指标快照，如果请求不存在则返回 None
        """
        with self._lock:
            if request_id not in self._active_requests:
                return None
            
            snapshot = self._active_requests.pop(request_id)
            snapshot.end_time = time.time()
            snapshot.success = success
            snapshot.error_message = error_message
            
            self._history.append(snapshot)
        
        log_level = logging.INFO if success else logging.WARNING
        logger.log(
            log_level,
            f"[StreamMetrics] 请求完成: {request_id}, "
            f"TTFB={snapshot.ttfb_ms:.2f}ms, "
            f"总耗时={snapshot.total_latency_ms:.2f}ms, "
            f"chunks={snapshot.chunk_count}, "
            f"成功={success}"
        )
        
        return snapshot
    
    def get_statistics(self, window_seconds: float = 300.0) -> Dict[str, Any]:
        """
        获取指定时间窗口内的聚合统计
        
        Args:
            window_seconds: 时间窗口（秒），默认5分钟
        
        Returns:
            聚合统计数据
        """
        cutoff_time = time.time() - window_seconds
        
        with self._lock:
            recent = [
                s for s in self._history 
                if s.start_time >= cutoff_time
            ]
        
        if not recent:
            return {
                "window_seconds": window_seconds,
                "total_requests": 0,
                "success_rate": None,
                "avg_ttfb_ms": None,
                "avg_latency_ms": None,
                "avg_chunk_rate": None,
            }
        
        successful = [s for s in recent if s.success]
        ttfb_values = [s.ttfb_ms for s in successful if s.ttfb_ms is not None]
        latency_values = [s.total_latency_ms for s in successful if s.total_latency_ms is not None]
        chunk_rates = [s.chunk_rate for s in successful if s.chunk_rate is not None]
        
        return {
            "window_seconds": window_seconds,
            "total_requests": len(recent),
            "successful_requests": len(successful),
            "failed_requests": len(recent) - len(successful),
            "success_rate": len(successful) / len(recent) if recent else None,
            "avg_ttfb_ms": sum(ttfb_values) / len(ttfb_values) if ttfb_values else None,
            "min_ttfb_ms": min(ttfb_values) if ttfb_values else None,
            "max_ttfb_ms": max(ttfb_values) if ttfb_values else None,
            "avg_latency_ms": sum(latency_values) / len(latency_values) if latency_values else None,
            "min_latency_ms": min(latency_values) if latency_values else None,
            "max_latency_ms": max(latency_values) if latency_values else None,
            "avg_chunk_rate": sum(chunk_rates) / len(chunk_rates) if chunk_rates else None,
        }
    
    def get_recent_requests(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近的请求记录"""
        with self._lock:
            recent = list(self._history)[-limit:]
        return [s.to_dict() for s in reversed(recent)]


# 全局实例
stream_metrics = StreamMetricsCollector()


# 便捷函数
def start_stream_tracking(
    request_id: str,
    model: str,
    user_id: Optional[str] = None,
    tool_name: Optional[str] = None
) -> StreamMetricsSnapshot:
    """开始追踪流式请求"""
    return stream_metrics.start_request(request_id, model, user_id, tool_name)


def record_first_chunk(request_id: str) -> None:
    """记录首个数据块"""
    stream_metrics.record_first_chunk(request_id)


def record_chunk(request_id: str, chunk_bytes: int = 0) -> None:
    """记录数据块"""
    stream_metrics.record_chunk(request_id, chunk_bytes)


def complete_stream_tracking(
    request_id: str,
    success: bool = True,
    error_message: Optional[str] = None
) -> Optional[StreamMetricsSnapshot]:
    """完成流式请求追踪"""
    return stream_metrics.complete_request(request_id, success, error_message)


def get_stream_statistics(window_seconds: float = 300.0) -> Dict[str, Any]:
    """获取流式请求统计"""
    return stream_metrics.get_statistics(window_seconds)
