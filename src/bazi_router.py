"""八字排盘API路由"""
from fastapi import APIRouter, HTTPException
from .bazi_models import BirthInfo, BaziResponse
from .divination.bazi.paipan import BaziPaipan
from .divination.bazi.lunar import solar_to_lunar

router = APIRouter(prefix="/api/bazi", tags=["八字"])

# 初始化排盘实例
paipan = BaziPaipan()


@router.post("/paipan", response_model=BaziResponse)
async def bazi_paipan(birth: BirthInfo):
    """八字排盘
    
    Args:
        birth: 出生信息
        
    Returns:
        排盘结果
    """
    try:
        # 排盘
        result = paipan.paipan(birth.dict(), birth.use_true_solar)
        
        # 农历信息
        lunar_info = solar_to_lunar(birth.year, birth.month, birth.day)
        result['lunar_info'] = lunar_info
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/test")
async def test_bazi():
    """测试接口"""
    birth = BirthInfo(
        year=1990, month=5, day=15, 
        hour=14, minute=30
    )
    return await bazi_paipan(birth)
