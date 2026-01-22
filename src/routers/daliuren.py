"""大六壬API路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

router = APIRouter(prefix="/api/daliuren", tags=["大六壬"])


class DaliurenRequest(BaseModel):
    """大六壬起盘请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(..., ge=0, le=23, description="小时")
    minute: int = Field(0, ge=0, le=59, description="分钟")


class DaliurenResponse(BaseModel):
    """大六壬排盘响应"""
    time_info: dict
    tianpan: dict
    sike: list
    sanchuan: list
    tianjiang: list
    summary: str


@router.post("/paipan", response_model=DaliurenResponse)
async def daliuren_paipan(request: DaliurenRequest):
    """大六壬排盘
    
    Args:
        request: 起盘参数
        
    Returns:
        排盘结果
    """
    try:
        from src.divination.daliuren import DaliurenPaipan
        
        paipan = DaliurenPaipan()
        result = paipan.paipan(
            request.year, 
            request.month, 
            request.day, 
            request.hour,
            request.minute
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"排盘失败: {str(e)}")


@router.get("/test")
async def test_daliuren():
    """测试大六壬排盘"""
    now = datetime.now()
    
    try:
        from src.divination.daliuren import DaliurenPaipan
        
        paipan = DaliurenPaipan()
        result = paipan.paipan(
            now.year, 
            now.month, 
            now.day, 
            now.hour
        )
        
        return {
            "status": "success",
            "message": "大六壬排盘测试成功",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"测试失败: {str(e)}"
        }
