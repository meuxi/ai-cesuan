"""八字排盘API路由"""
from fastapi import APIRouter
from src.bazi_models import BirthInfo, BaziResponse
from src.divination.bazi.paipan import BaziPaipan
from src.divination.bazi.lunar import solar_to_lunar
from src.common import safe_api_call
from src.cache import cached_divination

router = APIRouter(prefix="/api/bazi", tags=["八字"])

# 初始化排盘实例
paipan = BaziPaipan()


@router.post("/paipan", response_model=BaziResponse)
@safe_api_call("八字排盘")
@cached_divination("bazi", ["year", "month", "day", "hour", "minute", "gender", "use_true_solar"])
async def bazi_paipan(birth: BirthInfo):
    """八字排盘
    
    Args:
        birth: 出生信息
        
    Returns:
        排盘结果
    """
    # 排盘
    result = paipan.paipan(birth.dict(), birth.use_true_solar)
    
    # 农历信息
    lunar_info = solar_to_lunar(birth.year, birth.month, birth.day)
    result['lunar_info'] = lunar_info
    
    return result


@router.get("/test")
async def test_bazi():
    """测试接口"""
    birth = BirthInfo(
        year=1990, month=5, day=15, 
        hour=14, minute=30
    )
    return await bazi_paipan(birth)
