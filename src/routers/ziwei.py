"""
紫微斗数路由
提供紫微斗数排盘API
核心算法在后端执行（优先使用Node.js桥接调用原版iztro，回退到iztro-py）
支持全书派/中州派配置切换（参考py-iztro）
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
import logging

from src.divination.ziwei.iztro_bridge_service import hybrid_iztro_service
from src.divination.ziwei.ziwei_config import (
    ZiweiConfig, AlgorithmType, YearDivideType, AgeDivideType
)

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
    algorithm: Optional[str] = Field(
        default=None,
        description="派别: 'default'=全书派, 'zhongzhou'=中州派"
    )


class ZiweiConfigRequest(BaseModel):
    """紫微配置请求（参考py-iztro）"""
    mutagens: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="自定义四化表: {天干: [化禄星, 化权星, 化科星, 化忌星]}"
    )
    brightness: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="自定义星曜亮度: {星名: [子宫亮度, 丑宫亮度, ...]}"
    )
    year_divide: Optional[str] = Field(
        default="normal",
        description="年分割点: 'normal'=正月初一, 'exact'=立春"
    )
    age_divide: Optional[str] = Field(
        default="normal",
        description="小限分割点: 'normal'=只考虑年份, 'birthday'=以生日为分界"
    )
    algorithm: Optional[str] = Field(
        default="default",
        description="派别: 'default'=全书派, 'zhongzhou'=中州派"
    )


class ZiweiHoroscopeRequest(BaseModel):
    """运限查询请求"""
    birth_date: str = Field(description="出生日期 YYYY-MM-DD")
    birth_time_index: int = Field(ge=0, le=12, description="出生时辰索引 0-12")
    gender: str = Field(default="male", description="性别 male/female")
    target_date: Optional[str] = Field(default=None, description="目标日期 YYYY-MM-DD")
    target_time_index: Optional[int] = Field(default=None, ge=0, le=12, description="目标时辰 0-12")


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
            language=req.language or "zh-CN",
            algorithm=req.algorithm
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


@router.post("/config")
async def set_config(req: ZiweiConfigRequest):
    """设置紫微斗数全局配置（四化、亮度、派别等）
    
    参考 py-iztro 的 astro.config() 方法
    
    Args:
        req: 配置请求
        
    Returns:
        当前配置信息
    """
    try:
        config = ZiweiConfig(
            mutagens=req.mutagens,
            brightness=req.brightness,
            year_divide=YearDivideType(req.year_divide) if req.year_divide else YearDivideType.NORMAL,
            age_divide=AgeDivideType(req.age_divide) if req.age_divide else AgeDivideType.NORMAL,
            algorithm=AlgorithmType(req.algorithm) if req.algorithm else AlgorithmType.DEFAULT,
        )
        hybrid_iztro_service.config(config)
        
        return {
            "success": True,
            "message": "配置已更新",
            "config": {
                "algorithm": config.algorithm.value,
                "yearDivide": config.year_divide.value,
                "ageDivide": config.age_divide.value,
                "hasMutagens": bool(config.mutagens),
                "hasBrightness": bool(config.brightness),
            }
        }
    except Exception as e:
        logger.error(f"设置配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"设置配置失败: {str(e)}")


@router.get("/config")
async def get_config():
    """获取当前紫微斗数配置
    
    Returns:
        当前配置信息
    """
    try:
        config = hybrid_iztro_service.get_config()
        mutagen_table = config.get_mutagen_table()
        
        return {
            "algorithm": config.algorithm.value,
            "yearDivide": config.year_divide.value,
            "ageDivide": config.age_divide.value,
            "horoscopeDivide": config.horoscope_divide.value,
            "mutagens": mutagen_table,
        }
    except Exception as e:
        logger.error(f"获取配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取配置失败: {str(e)}")


@router.post("/config/reset")
async def reset_config():
    """重置紫微斗数配置为默认值
    
    Returns:
        重置结果
    """
    try:
        hybrid_iztro_service.reset_config()
        return {"success": True, "message": "配置已重置为默认值"}
    except Exception as e:
        logger.error(f"重置配置失败: {e}")
        raise HTTPException(status_code=500, detail=f"重置配置失败: {str(e)}")


@router.post("/horoscope")
async def get_horoscope(req: ZiweiHoroscopeRequest):
    """计算运限信息（大限/小限/流年/流月/流日/流时）
    
    参考 py-iztro 的 astrolabe.horoscope() 方法
    
    Args:
        req: 运限查询请求
        
    Returns:
        完整运限数据
    """
    try:
        result = hybrid_iztro_service.horoscope(
            birth_date=req.birth_date,
            birth_time_index=req.birth_time_index,
            gender=req.gender,
            target_date=req.target_date,
            target_time_index=req.target_time_index
        )
        return result
    except Exception as e:
        logger.error(f"运限计算失败: {e}")
        raise HTTPException(status_code=500, detail=f"运限计算失败: {str(e)}")
