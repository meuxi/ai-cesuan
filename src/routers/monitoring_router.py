"""
监控和管理API路由
提供系统状态、成本监控、配额管理等接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import logging

from src.monitoring import cost_monitor
from src.quota import quota_manager, QuotaTier
from src.ai.degradation import degradation_manager, DegradationLevel, SystemMetrics
from src.cache.prompt_cache import prompt_cache

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/monitor", tags=["监控管理"])


@router.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "degradation_level": degradation_manager.get_current_level().value
    }


@router.get("/cost/summary")
async def get_cost_summary():
    """获取成本监控摘要"""
    return cost_monitor.get_summary()


@router.get("/cost/models")
async def get_model_stats(hours: int = Query(default=24, ge=1, le=168)):
    """获取各模型使用统计"""
    return cost_monitor.get_model_stats(hours)


@router.get("/cost/tools")
async def get_tool_stats(hours: int = Query(default=24, ge=1, le=168)):
    """获取各工具使用统计"""
    return cost_monitor.get_tool_stats(hours)


@router.get("/quota/{user_id}")
async def get_user_quota(user_id: str):
    """获取用户配额使用情况"""
    return quota_manager.get_usage_summary(user_id)


@router.post("/quota/{user_id}/tier")
async def set_user_tier(user_id: str, tier: str):
    """设置用户等级"""
    try:
        tier_enum = QuotaTier(tier)
        quota_manager.set_user_tier(user_id, tier_enum)
        return {"success": True, "user_id": user_id, "tier": tier}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的等级: {tier}")


@router.get("/degradation/status")
async def get_degradation_status():
    """获取降级状态"""
    return degradation_manager.get_status()


@router.post("/degradation/override")
async def set_degradation_override(level: Optional[str] = None):
    """
    设置手动降级覆盖
    level为空则清除覆盖
    """
    if level is None:
        degradation_manager.set_manual_override(None)
        return {"success": True, "message": "已清除手动覆盖"}
    
    try:
        level_enum = DegradationLevel(level)
        degradation_manager.set_manual_override(level_enum)
        return {"success": True, "level": level}
    except ValueError:
        raise HTTPException(status_code=400, detail=f"无效的降级级别: {level}")


@router.post("/degradation/update")
async def update_degradation_metrics(
    hourly_cost: float = 0.0,
    error_rate: float = 0.0,
    latency_p95: float = 0.0
):
    """手动更新降级指标（用于测试或外部监控集成）"""
    metrics = SystemMetrics(
        hourly_cost=hourly_cost,
        error_rate=error_rate,
        latency_p95=latency_p95
    )
    degradation_manager.update_level(metrics)
    return {
        "success": True,
        "current_level": degradation_manager.get_current_level().value
    }


@router.get("/cache/stats")
async def get_cache_stats():
    """获取缓存统计"""
    return prompt_cache.get_stats()


@router.post("/cache/clear")
async def clear_cache():
    """清空所有缓存"""
    prompt_cache.clear_all()
    return {"success": True, "message": "缓存已清空"}


@router.post("/cleanup")
async def run_cleanup():
    """运行清理任务"""
    cost_monitor.cleanup_old_records(hours_to_keep=48)
    quota_manager.cleanup_old_data(days_to_keep=7)
    return {"success": True, "message": "清理完成"}


@router.get("/report/daily")
async def get_daily_report(date: Optional[str] = None):
    """获取或生成日报"""
    return cost_monitor.export_daily_report(date)
