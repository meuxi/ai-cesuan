"""八字相关数据模型"""
from pydantic import BaseModel, Field
from typing import Optional, Dict


class BirthInfo(BaseModel):
    """出生信息"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(..., ge=0, le=23, description="小时")
    minute: int = Field(0, ge=0, le=59, description="分钟")
    longitude: Optional[float] = Field(None, description="经度")
    latitude: Optional[float] = Field(None, description="纬度")
    use_true_solar: bool = Field(False, description="是否使用真太阳时")


class BaziResponse(BaseModel):
    """八字排盘响应"""
    sizhu: Dict
    nayin: Dict
    xunkong: Dict
    dizhi_cang: Dict
    lunar_info: Optional[Dict] = None
