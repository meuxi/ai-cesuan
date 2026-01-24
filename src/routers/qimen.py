"""奇门遁甲API路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from src.common import safe_api_call
from src.cache import cached_divination

router = APIRouter(prefix="/api/qimen", tags=["奇门遁甲"])

# 导入用神模块
try:
    from src.divination.qimen.yongshen import (
        get_shilei_list,
        analyze_yongshen,
        qimen_yongshen,
        GONG_FANGWEI,
    )
    YONGSHEN_AVAILABLE = True
except ImportError:
    YONGSHEN_AVAILABLE = False


class QimenRequest(BaseModel):
    """奇门遁甲起盘请求"""
    year: int = Field(..., ge=1900, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    day: int = Field(..., ge=1, le=31, description="日期")
    hour: int = Field(..., ge=0, le=23, description="小时")
    minute: int = Field(0, ge=0, le=59, description="分钟")
    pan_type: str = Field("时盘", description="盘类型：时盘/日盘/月盘/年盘")
    pan_style: str = Field("转盘", description="盘式：转盘/飞盘")


class QimenResponse(BaseModel):
    """奇门遁甲排盘响应"""
    time_info: dict
    pan_info: dict
    jiugong: list
    summary: str


@router.post("/paipan", response_model=QimenResponse)
@safe_api_call("奇门排盘")
@cached_divination("qimen", ["year", "month", "day", "hour", "minute", "pan_type", "pan_style"])
async def qimen_paipan(request: QimenRequest):
    """奇门遁甲排盘
    
    支持四种盘类型：
    - 时盘：以时辰为基准起局（最常用）
    - 日盘：以日干支为基准起局
    - 月盘：以月干支为基准起局（月家奇门）
    - 年盘：以年干支为基准起局（年家奇门）
    
    支持两种盘式：
    - 转盘：天盘随值符转动
    - 飞盘：天盘按洛书飞布
    
    Args:
        request: 起盘参数
        
    Returns:
        排盘结果
    """
    from src.divination.qimen import QimenPaipan
    from src.divination.common.validators import validate_pan_type, validate_pan_style
    
    # 使用统一验证函数
    validate_pan_type(request.pan_type)
    validate_pan_style(request.pan_style)
    
    paipan = QimenPaipan()
    return paipan.paipan(
        request.year, 
        request.month, 
        request.day, 
        request.hour,
        request.minute,
        request.pan_type,
        request.pan_style
    )


@router.get("/test")
async def test_qimen():
    """测试奇门遁甲排盘"""
    now = datetime.now()
    
    try:
        from src.divination.qimen import QimenPaipan
        
        paipan = QimenPaipan()
        result = paipan.paipan(
            now.year, 
            now.month, 
            now.day, 
            now.hour
        )
        
        return {
            "status": "success",
            "message": "奇门遁甲排盘测试成功",
            "result": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"测试失败: {str(e)}"
        }


# ========== 用神系统API ==========

class YongShenRequest(BaseModel):
    """用神分析请求"""
    shi_lei: str = Field(..., description="事类：求财/婚姻/疾病/出行/诉讼/考试/工作/失物/置业/求官/孕产/寻人/合作/其他")
    yongshen_gong: int = Field(..., ge=1, le=9, description="用神落宫(1-9)")
    rigan_gong: int = Field(..., ge=1, le=9, description="日干落宫(1-9)")
    shigan_gong: int = Field(..., ge=1, le=9, description="时干落宫(1-9)")
    month: int = Field(..., ge=1, le=12, description="月份")
    rigan_wuxing: str = Field(..., description="日干五行：木/火/土/金/水")
    kongwang: Optional[List[int]] = Field(None, description="空亡宫位列表")


class ZhuKeRequest(BaseModel):
    """主客分析请求"""
    rigan_gong: int = Field(..., ge=1, le=9, description="日干落宫（我方）")
    shigan_gong: int = Field(..., ge=1, le=9, description="时干落宫（对方）")
    month: int = Field(..., ge=1, le=12, description="月份")
    rigan_wuxing: str = Field(..., description="日干五行")
    shigan_wuxing: str = Field(..., description="时干五行")


@router.get("/yongshen/shilei-list")
async def get_shilei_options():
    """获取所有事类选项"""
    if not YONGSHEN_AVAILABLE:
        raise HTTPException(status_code=503, detail="用神模块不可用")
    return {"shilei_list": get_shilei_list()}


@router.post("/yongshen/analyze")
@safe_api_call("用神分析")
async def analyze_yongshen_api(request: YongShenRequest):
    """
    分析用神状态
    
    根据事类选取用神，分析其落宫状态、旺相休囚死、与日干关系等
    """
    from src.exceptions import ServiceUnavailableError
    from src.divination.common.validators import validate_wuxing
    
    if not YONGSHEN_AVAILABLE:
        raise ServiceUnavailableError("用神模块不可用")
    
    validate_wuxing(request.rigan_wuxing)
    
    return analyze_yongshen(
        shi_lei=request.shi_lei,
        yongshen_gong=request.yongshen_gong,
        rigan_gong=request.rigan_gong,
        shigan_gong=request.shigan_gong,
        month=request.month,
        rigan_wuxing=request.rigan_wuxing,
        kongwang=request.kongwang,
    )


@router.post("/yongshen/zhuke")
@safe_api_call("主客分析")
async def analyze_zhuke_api(request: ZhuKeRequest):
    """
    主客分析
    
    用于合作、诉讼等涉及双方的事类，分析我方与对方的强弱对比
    """
    from src.exceptions import ServiceUnavailableError
    from src.divination.common.validators import validate_wuxing
    
    if not YONGSHEN_AVAILABLE:
        raise ServiceUnavailableError("用神模块不可用")
    
    validate_wuxing(request.rigan_wuxing)
    validate_wuxing(request.shigan_wuxing)
    
    return qimen_yongshen.analyze_zhuke(
        rigan_gong=request.rigan_gong,
        shigan_gong=request.shigan_gong,
        month=request.month,
        rigan_wuxing=request.rigan_wuxing,
        shigan_wuxing=request.shigan_wuxing,
    )


@router.get("/yongshen/fangwei")
async def get_fangwei_map():
    """获取宫位方位对照表"""
    if not YONGSHEN_AVAILABLE:
        raise HTTPException(status_code=503, detail="用神模块不可用")
    return {"fangwei_map": GONG_FANGWEI}
