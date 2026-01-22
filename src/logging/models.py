"""
操作日志数据模型
参考 zhanwen 项目的日志设计
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class LogLevel(Enum):
    """日志级别"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LogCategory(Enum):
    """日志分类"""
    DIVINATION = "divination"       # 占卜操作
    BAZI = "bazi"                   # 八字
    LIUYAO = "liuyao"               # 六爻
    TAROT = "tarot"                 # 塔罗
    QIMEN = "qimen"                 # 奇门遁甲
    DALIUREN = "daliuren"           # 大六壬
    XIAOLIU = "xiaoliu"             # 小六壬
    CHOUQIAN = "chouqian"           # 抽签
    ZHUGE = "zhuge"                 # 诸葛神算
    ZODIAC = "zodiac"               # 星座
    LIFE_KLINE = "life_kline"       # 人生K线
    RAG = "rag"                     # RAG知识库
    AI = "ai"                       # AI调用
    USER = "user"                   # 用户行为
    SYSTEM = "system"               # 系统操作
    API = "api"                     # API调用


@dataclass
class OperationLog:
    """操作日志"""
    id: str                                     # 日志ID
    timestamp: datetime                         # 时间戳
    level: LogLevel                             # 日志级别
    category: LogCategory                       # 日志分类
    action: str                                 # 操作动作
    user_id: Optional[str] = None               # 用户ID（可选）
    session_id: Optional[str] = None            # 会话ID
    ip_address: Optional[str] = None            # IP地址
    user_agent: Optional[str] = None            # 用户代理
    request_path: Optional[str] = None          # 请求路径
    request_method: Optional[str] = None        # 请求方法
    response_status: Optional[int] = None       # 响应状态码
    duration_ms: Optional[float] = None         # 耗时(毫秒)
    input_data: Optional[Dict[str, Any]] = None # 输入数据（脱敏）
    output_summary: Optional[str] = None        # 输出摘要
    error_message: Optional[str] = None         # 错误信息
    metadata: Dict[str, Any] = field(default_factory=dict)  # 元数据
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "level": self.level.value,
            "category": self.category.value,
            "action": self.action,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "request_path": self.request_path,
            "request_method": self.request_method,
            "response_status": self.response_status,
            "duration_ms": self.duration_ms,
            "input_data": self.input_data,
            "output_summary": self.output_summary,
            "error_message": self.error_message,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OperationLog":
        """从字典创建"""
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            level=LogLevel(data["level"]),
            category=LogCategory(data["category"]),
            action=data["action"],
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            ip_address=data.get("ip_address"),
            user_agent=data.get("user_agent"),
            request_path=data.get("request_path"),
            request_method=data.get("request_method"),
            response_status=data.get("response_status"),
            duration_ms=data.get("duration_ms"),
            input_data=data.get("input_data"),
            output_summary=data.get("output_summary"),
            error_message=data.get("error_message"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LogQuery:
    """日志查询条件"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    level: Optional[LogLevel] = None
    category: Optional[LogCategory] = None
    action: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    has_error: Optional[bool] = None
    limit: int = 100
    offset: int = 0


@dataclass
class LogStats:
    """日志统计"""
    total_count: int
    by_category: Dict[str, int]
    by_level: Dict[str, int]
    by_action: Dict[str, int]
    avg_duration_ms: float
    error_count: int
    error_rate: float
    time_range: Dict[str, str]
