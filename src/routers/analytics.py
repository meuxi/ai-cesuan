"""
统计 API 路由
"""

from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..analytics import get_analytics_service, DivinationType

router = APIRouter(prefix="/analytics", tags=["用量统计"])


@router.get("/stats")
async def get_stats(
    period: str = Query("day", description="统计周期: day/week/month"),
    start_date: Optional[str] = Query(None, description="开始日期 (ISO格式)"),
    end_date: Optional[str] = Query(None, description="结束日期 (ISO格式)"),
) -> Dict[str, Any]:
    """
    获取使用统计
    
    返回指定周期内的各项统计指标
    """
    service = get_analytics_service()
    
    start = datetime.fromisoformat(start_date) if start_date else None
    end = datetime.fromisoformat(end_date) if end_date else None
    
    stats = service.get_stats(period=period, start_date=start, end_date=end)
    return stats.to_dict()


@router.get("/daily")
async def get_daily_stats(
    days: int = Query(7, ge=1, le=30, description="统计天数"),
) -> List[Dict[str, Any]]:
    """获取每日统计"""
    service = get_analytics_service()
    return service.get_daily_stats(days=days)


@router.get("/top-models")
async def get_top_models(
    limit: int = Query(5, ge=1, le=20, description="返回数量"),
) -> List[Dict[str, Any]]:
    """获取使用最多的模型"""
    service = get_analytics_service()
    return service.get_top_models(limit=limit)


@router.get("/records")
async def get_records(
    divination_type: Optional[str] = Query(None, description="占卜类型"),
    success_only: bool = Query(False, description="仅成功记录"),
    limit: int = Query(50, ge=1, le=500, description="返回数量"),
) -> List[Dict[str, Any]]:
    """获取使用记录"""
    service = get_analytics_service()
    
    dtype = None
    if divination_type:
        try:
            dtype = DivinationType(divination_type)
        except ValueError:
            pass
    
    records = service.get_records(
        divination_type=dtype,
        success_only=success_only,
        limit=limit,
    )
    
    return [r.to_dict() for r in records]


@router.get("/summary")
async def get_summary() -> Dict[str, Any]:
    """获取统计摘要"""
    service = get_analytics_service()
    
    day_stats = service.get_stats(period="day")
    week_stats = service.get_stats(period="week")
    month_stats = service.get_stats(period="month")
    top_models = service.get_top_models(limit=3)
    
    return {
        "today": {
            "requests": day_stats.total_requests,
            "tokens": day_stats.total_tokens,
            "cost": round(day_stats.total_cost, 4),
            "error_rate": round(day_stats.error_rate * 100, 2),
        },
        "this_week": {
            "requests": week_stats.total_requests,
            "tokens": week_stats.total_tokens,
            "cost": round(week_stats.total_cost, 4),
        },
        "this_month": {
            "requests": month_stats.total_requests,
            "tokens": month_stats.total_tokens,
            "cost": round(month_stats.total_cost, 4),
        },
        "top_models": top_models,
        "by_type": day_stats.by_type,
    }
