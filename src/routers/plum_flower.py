"""
梅花易数 API 路由
支持数字起卦和时间起卦
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from src.divination.plum_flower_service import PlumFlowerService
from src.common.response import ApiResponse, ResponseCode, ok, fail

router = APIRouter(prefix="/api/plum-flower", tags=["梅花易数"])


class NumberInput(BaseModel):
    """数字起卦请求"""
    num1: int = Field(..., ge=0, le=9999, description="第一个数字")
    num2: int = Field(..., ge=0, le=9999, description="第二个数字")


class TimeInput(BaseModel):
    """时间起卦请求"""
    year: Optional[int] = Field(None, ge=1900, le=2100, description="年份")
    month: Optional[int] = Field(None, ge=1, le=12, description="月份")
    day: Optional[int] = Field(None, ge=1, le=31, description="日期")
    hour: Optional[int] = Field(None, ge=0, le=23, description="小时")
    use_true_solar_time: bool = Field(False, description="是否使用真太阳时")
    longitude: float = Field(116.4, ge=73, le=135, description="经度（用于真太阳时）")


@router.post("/by-number", summary="数字起卦")
async def calculate_by_number(request: Request, input: NumberInput):
    """
    使用两个数字进行起卦
    
    - num1: 用于计算上卦
    - num2: 用于计算下卦和动爻
    """
    request_id = getattr(request.state, 'request_id', None)
    try:
        result = PlumFlowerService.calculate_by_number(input.num1, input.num2)
        return ok(data=result, message="起卦成功")
    except Exception as e:
        return fail(code=ResponseCode.CALCULATION_ERROR, message=str(e))


@router.post("/by-time", summary="时间起卦")
async def calculate_by_time(request: Request, input: TimeInput):
    """
    使用时间进行起卦（不传参数则使用当前时间）
    
    - 可选择是否使用真太阳时
    - 真太阳时需要提供所在地经度
    """
    request_id = getattr(request.state, 'request_id', None)
    try:
        result = PlumFlowerService.calculate_by_time(
            year=input.year,
            month=input.month,
            day=input.day,
            hour=input.hour,
            use_true_solar_time=input.use_true_solar_time,
            longitude=input.longitude
        )
        return ok(data=result, message="起卦成功")
    except Exception as e:
        return fail(code=ResponseCode.CALCULATION_ERROR, message=str(e))


@router.get("/now", summary="即时起卦")
async def calculate_now(request: Request, use_true_solar_time: bool = False, longitude: float = 116.4):
    """
    使用当前时间立即起卦
    """
    request_id = getattr(request.state, 'request_id', None)
    try:
        result = PlumFlowerService.calculate_by_time(
            use_true_solar_time=use_true_solar_time,
            longitude=longitude
        )
        return ok(data=result, message="起卦成功")
    except Exception as e:
        return fail(code=ResponseCode.CALCULATION_ERROR, message=str(e))
