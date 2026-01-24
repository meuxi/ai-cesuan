"""
操作日志 API 路由
提供日志查询和统计接口

安全说明：
- 所有日志接口需要管理员权限
- 通过 X-Admin-Token 请求头验证
"""

import os
import logging
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query, HTTPException, Header, Depends

from ..logging import (
    OperationLogService,
    get_log_service,
    LogLevel,
    LogCategory,
)
from ..logging.models import LogQuery

router = APIRouter(prefix="/logs", tags=["操作日志"])
_logger = logging.getLogger(__name__)

# 管理员 Token（从环境变量读取，生产环境必须配置）
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "")


async def verify_admin_token(x_admin_token: Optional[str] = Header(None)) -> bool:
    """
    验证管理员 Token
    
    安全说明：
    - 生产环境必须配置 ADMIN_TOKEN 环境变量
    - 未配置时拒绝所有请求
    """
    if not ADMIN_TOKEN:
        _logger.warning("[日志API] 未配置 ADMIN_TOKEN，拒绝访问")
        raise HTTPException(
            status_code=403,
            detail="日志接口未开放（未配置管理员令牌）"
        )
    
    # 使用常量时间比较防止时序攻击
    if not x_admin_token or not secrets.compare_digest(x_admin_token, ADMIN_TOKEN):
        _logger.warning("[日志API] 管理员令牌验证失败")
        raise HTTPException(
            status_code=403,
            detail="无权访问日志接口"
        )
    
    return True


@router.get("/")
async def list_logs(
    start_time: Optional[str] = Query(None, description="开始时间 (ISO格式)"),
    end_time: Optional[str] = Query(None, description="结束时间 (ISO格式)"),
    level: Optional[str] = Query(None, description="日志级别 (debug/info/warning/error)"),
    category: Optional[str] = Query(None, description="日志分类"),
    action: Optional[str] = Query(None, description="操作动作（模糊匹配）"),
    user_id: Optional[str] = Query(None, description="用户ID"),
    has_error: Optional[bool] = Query(None, description="是否有错误"),
    limit: int = Query(50, ge=1, le=500, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    _admin: bool = Depends(verify_admin_token),  # 需要管理员权限
) -> Dict[str, Any]:
    """
    查询操作日志
    """
    service = get_log_service()
    
    # 解析查询条件
    query = LogQuery(
        start_time=datetime.fromisoformat(start_time) if start_time else None,
        end_time=datetime.fromisoformat(end_time) if end_time else None,
        level=LogLevel(level) if level else None,
        category=LogCategory(category) if category else None,
        action=action,
        user_id=user_id,
        has_error=has_error,
        limit=limit,
        offset=offset,
    )
    
    logs = service.query(query)
    
    return {
        "total": len(logs),
        "offset": offset,
        "limit": limit,
        "logs": [log.to_dict() for log in logs],
    }


@router.get("/stats")
async def get_stats(
    start_time: Optional[str] = Query(None, description="开始时间 (ISO格式)"),
    end_time: Optional[str] = Query(None, description="结束时间 (ISO格式)"),
    category: Optional[str] = Query(None, description="限定分类"),
    _admin: bool = Depends(verify_admin_token),  # 需要管理员权限
) -> Dict[str, Any]:
    """
    获取日志统计
    """
    service = get_log_service()
    
    stats = service.get_stats(
        start_time=datetime.fromisoformat(start_time) if start_time else None,
        end_time=datetime.fromisoformat(end_time) if end_time else None,
        category=LogCategory(category) if category else None,
    )
    
    return {
        "total_count": stats.total_count,
        "by_category": stats.by_category,
        "by_level": stats.by_level,
        "by_action": stats.by_action,
        "avg_duration_ms": round(stats.avg_duration_ms, 2),
        "error_count": stats.error_count,
        "error_rate": round(stats.error_rate * 100, 2),
        "time_range": stats.time_range,
    }


@router.get("/stats/daily")
async def get_daily_stats(
    days: int = Query(7, ge=1, le=90, description="统计天数"),
    category: Optional[str] = Query(None, description="限定分类"),
    _admin: bool = Depends(verify_admin_token),  # 需要管理员权限
) -> Dict[str, Any]:
    """
    获取每日统计趋势
    """
    service = get_log_service()
    end_time = datetime.now()
    
    daily_stats = []
    for i in range(days):
        day_end = end_time - timedelta(days=i)
        day_start = day_end.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        stats = service.get_stats(
            start_time=day_start,
            end_time=day_end,
            category=LogCategory(category) if category else None,
        )
        
        daily_stats.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "total_count": stats.total_count,
            "error_count": stats.error_count,
            "avg_duration_ms": round(stats.avg_duration_ms, 2),
        })
    
    # 按日期正序排列
    daily_stats.reverse()
    
    return {
        "days": days,
        "category": category,
        "daily_stats": daily_stats,
    }


@router.get("/categories")
async def list_categories() -> Dict[str, Any]:
    """
    获取所有日志分类
    """
    return {
        "categories": [
            {"code": c.value, "name": _get_category_name(c)}
            for c in LogCategory
        ]
    }


@router.get("/levels")
async def list_levels() -> Dict[str, Any]:
    """
    获取所有日志级别
    """
    return {
        "levels": [
            {"code": l.value, "name": _get_level_name(l)}
            for l in LogLevel
        ]
    }


@router.post("/cleanup")
async def cleanup_old_logs(
    days_to_keep: int = Query(30, ge=7, le=365, description="保留天数"),
    _admin: bool = Depends(verify_admin_token),  # 需要管理员权限
) -> Dict[str, str]:
    """
    清理旧日志
    """
    service = get_log_service()
    service.cleanup_old_logs(days_to_keep)
    
    return {"message": f"已清理 {days_to_keep} 天前的日志"}


def _get_category_name(category: LogCategory) -> str:
    """获取分类中文名"""
    names = {
        LogCategory.DIVINATION: "占卜操作",
        LogCategory.BAZI: "八字",
        LogCategory.LIUYAO: "六爻",
        LogCategory.TAROT: "塔罗牌",
        LogCategory.QIMEN: "奇门遁甲",
        LogCategory.DALIUREN: "大六壬",
        LogCategory.XIAOLIU: "小六壬",
        LogCategory.CHOUQIAN: "抽签",
        LogCategory.ZHUGE: "诸葛神算",
        LogCategory.ZODIAC: "星座",
        LogCategory.LIFE_KLINE: "人生K线",
        LogCategory.RAG: "RAG知识库",
        LogCategory.AI: "AI调用",
        LogCategory.USER: "用户行为",
        LogCategory.SYSTEM: "系统操作",
        LogCategory.API: "API调用",
    }
    return names.get(category, category.value)


def _get_level_name(level: LogLevel) -> str:
    """获取级别中文名"""
    names = {
        LogLevel.DEBUG: "调试",
        LogLevel.INFO: "信息",
        LogLevel.WARNING: "警告",
        LogLevel.ERROR: "错误",
    }
    return names.get(level, level.value)
