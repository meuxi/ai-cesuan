"""
操作日志服务
提供日志记录、查询和统计功能
"""

import json
import uuid
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
from collections import defaultdict

from .models import OperationLog, LogLevel, LogCategory, LogQuery, LogStats

logger = logging.getLogger(__name__)


class OperationLogService:
    """操作日志服务"""
    
    def __init__(self, store_path: str = None):
        """
        初始化日志服务
        
        Args:
            store_path: 日志存储路径
        """
        self.store_path = Path(store_path) if store_path else Path("data/logs")
        self.store_path.mkdir(parents=True, exist_ok=True)
        self._logs_cache: List[OperationLog] = []
        self._max_cache_size = 1000
    
    def log(
        self,
        category: LogCategory,
        action: str,
        level: LogLevel = LogLevel.INFO,
        user_id: str = None,
        session_id: str = None,
        ip_address: str = None,
        user_agent: str = None,
        request_path: str = None,
        request_method: str = None,
        response_status: int = None,
        duration_ms: float = None,
        input_data: Dict[str, Any] = None,
        output_summary: str = None,
        error_message: str = None,
        metadata: Dict[str, Any] = None,
    ) -> OperationLog:
        """
        记录操作日志
        
        Args:
            category: 日志分类
            action: 操作动作
            level: 日志级别
            其他参数: 可选的日志详情
            
        Returns:
            创建的日志对象
        """
        log_entry = OperationLog(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            level=level,
            category=category,
            action=action,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            request_path=request_path,
            request_method=request_method,
            response_status=response_status,
            duration_ms=duration_ms,
            input_data=self._sanitize_input(input_data),
            output_summary=output_summary,
            error_message=error_message,
            metadata=metadata or {},
        )
        
        # 添加到缓存
        self._logs_cache.append(log_entry)
        
        # 缓存满时持久化
        if len(self._logs_cache) >= self._max_cache_size:
            self._flush_cache()
        
        # 同时输出到标准日志
        log_msg = f"[{category.value}] {action}"
        if error_message:
            logger.error(f"{log_msg} - Error: {error_message}")
        elif level == LogLevel.WARNING:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)
        
        return log_entry
    
    def log_divination(
        self,
        divination_type: str,
        action: str,
        input_data: Dict[str, Any] = None,
        output_summary: str = None,
        duration_ms: float = None,
        user_id: str = None,
        session_id: str = None,
        metadata: Dict[str, Any] = None,
    ) -> OperationLog:
        """
        记录占卜操作日志（便捷方法）
        """
        # 映射占卜类型到分类
        category_map = {
            "bazi": LogCategory.BAZI,
            "liuyao": LogCategory.LIUYAO,
            "tarot": LogCategory.TAROT,
            "qimen": LogCategory.QIMEN,
            "daliuren": LogCategory.DALIUREN,
            "xiaoliu": LogCategory.XIAOLIU,
            "chouqian": LogCategory.CHOUQIAN,
            "zhuge": LogCategory.ZHUGE,
            "zodiac": LogCategory.ZODIAC,
            "life_kline": LogCategory.LIFE_KLINE,
        }
        category = category_map.get(divination_type.lower(), LogCategory.DIVINATION)
        
        return self.log(
            category=category,
            action=action,
            level=LogLevel.INFO,
            user_id=user_id,
            session_id=session_id,
            input_data=input_data,
            output_summary=output_summary,
            duration_ms=duration_ms,
            metadata=metadata,
        )
    
    def log_ai_call(
        self,
        model_name: str,
        prompt_tokens: int = None,
        completion_tokens: int = None,
        duration_ms: float = None,
        success: bool = True,
        error_message: str = None,
        metadata: Dict[str, Any] = None,
    ) -> OperationLog:
        """
        记录AI调用日志（便捷方法）
        """
        meta = metadata or {}
        meta.update({
            "model_name": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": (prompt_tokens or 0) + (completion_tokens or 0),
        })
        
        return self.log(
            category=LogCategory.AI,
            action="ai_chat" if success else "ai_chat_failed",
            level=LogLevel.INFO if success else LogLevel.ERROR,
            duration_ms=duration_ms,
            error_message=error_message,
            metadata=meta,
        )
    
    def query(self, query: LogQuery) -> List[OperationLog]:
        """
        查询日志
        
        Args:
            query: 查询条件
            
        Returns:
            符合条件的日志列表
        """
        # 先刷新缓存
        self._flush_cache()
        
        # 加载日志文件
        all_logs = self._load_logs(query.start_time, query.end_time)
        
        # 应用过滤条件
        filtered = all_logs
        
        if query.level:
            filtered = [l for l in filtered if l.level == query.level]
        
        if query.category:
            filtered = [l for l in filtered if l.category == query.category]
        
        if query.action:
            filtered = [l for l in filtered if query.action in l.action]
        
        if query.user_id:
            filtered = [l for l in filtered if l.user_id == query.user_id]
        
        if query.session_id:
            filtered = [l for l in filtered if l.session_id == query.session_id]
        
        if query.has_error is not None:
            if query.has_error:
                filtered = [l for l in filtered if l.error_message]
            else:
                filtered = [l for l in filtered if not l.error_message]
        
        # 按时间倒序排列
        filtered.sort(key=lambda x: x.timestamp, reverse=True)
        
        # 分页
        return filtered[query.offset:query.offset + query.limit]
    
    def get_stats(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
        category: LogCategory = None,
    ) -> LogStats:
        """
        获取日志统计
        
        Args:
            start_time: 开始时间
            end_time: 结束时间
            category: 限定分类
            
        Returns:
            统计结果
        """
        # 默认统计最近7天
        if not end_time:
            end_time = datetime.now()
        if not start_time:
            start_time = end_time - timedelta(days=7)
        
        query = LogQuery(start_time=start_time, end_time=end_time, limit=10000)
        if category:
            query.category = category
        
        logs = self.query(query)
        
        if not logs:
            return LogStats(
                total_count=0,
                by_category={},
                by_level={},
                by_action={},
                avg_duration_ms=0,
                error_count=0,
                error_rate=0,
                time_range={"start": start_time.isoformat(), "end": end_time.isoformat()},
            )
        
        # 统计
        by_category = defaultdict(int)
        by_level = defaultdict(int)
        by_action = defaultdict(int)
        total_duration = 0
        duration_count = 0
        error_count = 0
        
        for log in logs:
            by_category[log.category.value] += 1
            by_level[log.level.value] += 1
            by_action[log.action] += 1
            
            if log.duration_ms:
                total_duration += log.duration_ms
                duration_count += 1
            
            if log.error_message:
                error_count += 1
        
        return LogStats(
            total_count=len(logs),
            by_category=dict(by_category),
            by_level=dict(by_level),
            by_action=dict(by_action),
            avg_duration_ms=total_duration / duration_count if duration_count > 0 else 0,
            error_count=error_count,
            error_rate=error_count / len(logs) if logs else 0,
            time_range={"start": start_time.isoformat(), "end": end_time.isoformat()},
        )
    
    def _sanitize_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """脱敏处理输入数据"""
        if not data:
            return None
        
        sanitized = {}
        sensitive_keys = {"api_key", "password", "token", "secret", "key"}
        
        for key, value in data.items():
            key_lower = key.lower()
            if any(s in key_lower for s in sensitive_keys):
                sanitized[key] = "***REDACTED***"
            elif isinstance(value, str) and len(value) > 200:
                sanitized[key] = value[:200] + "..."
            else:
                sanitized[key] = value
        
        return sanitized
    
    def _flush_cache(self):
        """将缓存写入文件"""
        if not self._logs_cache:
            return
        
        # 按日期分组
        logs_by_date = defaultdict(list)
        for log in self._logs_cache:
            date_str = log.timestamp.strftime("%Y-%m-%d")
            logs_by_date[date_str].append(log.to_dict())
        
        # 写入对应日期的文件
        for date_str, logs in logs_by_date.items():
            file_path = self.store_path / f"logs_{date_str}.jsonl"
            
            with open(file_path, "a", encoding="utf-8") as f:
                for log in logs:
                    f.write(json.dumps(log, ensure_ascii=False) + "\n")
        
        self._logs_cache.clear()
    
    def _load_logs(
        self,
        start_time: datetime = None,
        end_time: datetime = None,
    ) -> List[OperationLog]:
        """从文件加载日志"""
        logs = []
        
        # 确定要读取的日期范围
        if not end_time:
            end_time = datetime.now()
        if not start_time:
            start_time = end_time - timedelta(days=7)
        
        current = start_time.date()
        end_date = end_time.date()
        
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            file_path = self.store_path / f"logs_{date_str}.jsonl"
            
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                data = json.loads(line)
                                log = OperationLog.from_dict(data)
                                
                                # 时间范围过滤
                                if start_time and log.timestamp < start_time:
                                    continue
                                if end_time and log.timestamp > end_time:
                                    continue
                                
                                logs.append(log)
                except Exception as e:
                    logger.error(f"加载日志文件失败 {file_path}: {e}")
            
            current += timedelta(days=1)
        
        return logs
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """清理旧日志"""
        cutoff = datetime.now() - timedelta(days=days_to_keep)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
        
        for file_path in self.store_path.glob("logs_*.jsonl"):
            # 提取日期
            date_str = file_path.stem.replace("logs_", "")
            if date_str < cutoff_str:
                try:
                    file_path.unlink()
                    logger.info(f"已删除旧日志文件: {file_path}")
                except Exception as e:
                    logger.error(f"删除日志文件失败 {file_path}: {e}")


# 全局单例
_log_service: Optional[OperationLogService] = None


def get_log_service(store_path: str = None) -> OperationLogService:
    """获取日志服务单例"""
    global _log_service
    if _log_service is None:
        _log_service = OperationLogService(store_path)
    return _log_service
