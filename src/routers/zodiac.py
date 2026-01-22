"""
星座API路由
提供星座查询、运势、配对等接口
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

router = APIRouter(prefix="/api/zodiac", tags=["星座"])

# 导入星座模块
try:
    from src.divination.zodiac import (
        get_sun_sign,
        get_moon_sign,
        get_rising_sign,
        get_zodiac_info,
        get_all_zodiacs,
        get_daily_zodiac_fortune,
        get_weekly_zodiac_fortune,
        get_monthly_zodiac_fortune,
        get_zodiac_compatibility,
    )
    ZODIAC_AVAILABLE = True
except ImportError:
    ZODIAC_AVAILABLE = False


class SunSignRequest(BaseModel):
    """太阳星座查询请求"""
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")


class MoonSignRequest(BaseModel):
    """月亮星座查询请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(12, ge=0, le=23, description="小时")
    minute: int = Field(0, ge=0, le=59, description="分钟")


class RisingSignRequest(BaseModel):
    """上升星座查询请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(..., ge=0, le=23, description="小时")
    minute: int = Field(0, ge=0, le=59, description="分钟")
    latitude: float = Field(39.9, description="纬度，默认北京")


class CompatibilityRequest(BaseModel):
    """星座配对请求"""
    zodiac1: str = Field(..., description="第一个星座")
    zodiac2: str = Field(..., description="第二个星座")


VALID_ZODIACS = [
    '白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座',
    '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座'
]


def validate_zodiac(zodiac: str) -> str:
    """验证星座名称"""
    if zodiac not in VALID_ZODIACS:
        raise HTTPException(
            status_code=400,
            detail=f"无效的星座名称，应为：{', '.join(VALID_ZODIACS)}"
        )
    return zodiac


@router.get("/list")
async def list_zodiacs():
    """获取所有星座列表"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    return {"zodiacs": get_all_zodiacs()}


@router.get("/info/{zodiac}")
async def get_zodiac(zodiac: str):
    """获取星座详细信息"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac = validate_zodiac(zodiac)
    info = get_zodiac_info(zodiac)
    if not info:
        raise HTTPException(status_code=404, detail="星座信息未找到")
    return info


@router.post("/sun-sign")
async def calculate_sun_sign(request: SunSignRequest):
    """根据出生日期计算太阳星座"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    sign = get_sun_sign(request.month, request.day)
    info = get_zodiac_info(sign)
    return {
        "sign": sign,
        "info": info
    }


@router.get("/sun-sign")
async def calculate_sun_sign_get(
    month: int = Query(..., ge=1, le=12, description="月份"),
    day: int = Query(..., ge=1, le=31, description="日期")
):
    """GET方式计算太阳星座"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    sign = get_sun_sign(month, day)
    info = get_zodiac_info(sign)
    return {
        "sign": sign,
        "info": info
    }


@router.post("/moon-sign")
async def calculate_moon_sign(request: MoonSignRequest):
    """计算月亮星座"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    return get_moon_sign(
        request.year, request.month, request.day,
        request.hour, request.minute
    )


@router.post("/rising-sign")
async def calculate_rising_sign(request: RisingSignRequest):
    """计算上升星座"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    return get_rising_sign(
        request.year, request.month, request.day,
        request.hour, request.minute, request.latitude
    )


@router.get("/fortune/daily/{zodiac}")
async def get_daily_fortune(
    zodiac: str,
    date_str: Optional[str] = Query(None, description="日期YYYY-MM-DD，默认今天")
):
    """获取每日星座运势"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac = validate_zodiac(zodiac)
    
    target_date = None
    if date_str:
        try:
            from datetime import datetime
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")
    
    return get_daily_zodiac_fortune(zodiac, target_date)


@router.get("/fortune/weekly/{zodiac}")
async def get_weekly_fortune(
    zodiac: str,
    year: int = Query(..., description="年份"),
    week: int = Query(..., ge=1, le=53, description="周数")
):
    """获取每周星座运势"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac = validate_zodiac(zodiac)
    return get_weekly_zodiac_fortune(zodiac, year, week)


@router.get("/fortune/monthly/{zodiac}")
async def get_monthly_fortune(
    zodiac: str,
    year: int = Query(..., description="年份"),
    month: int = Query(..., ge=1, le=12, description="月份")
):
    """获取每月星座运势"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac = validate_zodiac(zodiac)
    return get_monthly_zodiac_fortune(zodiac, year, month)


@router.post("/compatibility")
async def get_compatibility(request: CompatibilityRequest):
    """获取星座配对分析"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac1 = validate_zodiac(request.zodiac1)
    zodiac2 = validate_zodiac(request.zodiac2)
    
    return get_zodiac_compatibility(zodiac1, zodiac2)


@router.get("/compatibility")
async def get_compatibility_get(
    zodiac1: str = Query(..., description="第一个星座"),
    zodiac2: str = Query(..., description="第二个星座")
):
    """GET方式获取星座配对分析"""
    if not ZODIAC_AVAILABLE:
        raise HTTPException(status_code=503, detail="星座模块不可用")
    
    zodiac1 = validate_zodiac(zodiac1)
    zodiac2 = validate_zodiac(zodiac2)
    
    return get_zodiac_compatibility(zodiac1, zodiac2)
