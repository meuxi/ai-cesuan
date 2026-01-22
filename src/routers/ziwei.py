"""
紫微斗数路由
提供紫微斗数排盘API
核心算法在后端执行（优先使用Node.js桥接调用原版iztro，回退到iztro-py）
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

from src.divination.ziwei.iztro_bridge_service import hybrid_iztro_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ziwei", tags=["紫微斗数"])


class ZiweiPaipanRequest(BaseModel):
    """紫微排盘请求"""
    year: int
    month: int
    day: int
    hour: int
    minute: Optional[int] = 0
    gender: str = "male"
    language: Optional[str] = "zh-CN"


@router.post("/paipan")
async def paipan(req: ZiweiPaipanRequest):
    """紫微斗数排盘（使用iztro-py后端计算）
    
    Args:
        req: 排盘请求，包含年月日时和性别
        
    Returns:
        完整的紫微命盘数据
    """
    try:
        result = hybrid_iztro_service.calculate(
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            minute=req.minute or 0,
            gender=req.gender,
            language=req.language or "zh-CN"
        )
        return result
    except Exception as e:
        logger.error(f"紫微排盘失败: {e}")
        raise HTTPException(status_code=500, detail=f"紫微排盘失败: {str(e)}")


@router.post("/paipan/enhanced")
async def paipan_enhanced(req: ZiweiPaipanRequest):
    """增强版紫微斗数排盘（与paipan相同，保持API兼容）
    
    Args:
        req: 排盘请求，包含年月日时和性别
        
    Returns:
        完整的紫微命盘数据（包含大限、流年、四化等）
    """
    return await paipan(req)
