"""
运势API路由
提供每日运势、每月运势、周趋势等接口
"""

from datetime import date, datetime
from typing import Optional, Literal
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field
from ..divination.fortune import (
    calculate_daily_fortune,
    calculate_monthly_fortune,
    calculate_generic_daily_fortune,
    calculate_weekly_trend,
    generate_fortune_interpretation,
    get_day_master_personality,
    get_ten_god_detail,
    get_yongshen_career_advice,
    get_qiongtong_advice,
    get_seasonal_yongshen,
    DAY_MASTER_PERSONALITIES,
    TEN_GODS_DETAILED,
)
from ..divination.fortune.life_kline import (
    Gender,
    LIFE_KLINE_SYSTEM_INSTRUCTION,
    build_user_prompt,
    get_dayun_direction,
    generate_dayun_sequence,
)

router = APIRouter(prefix="/fortune", tags=["运势"])


class DailyFortuneRequest(BaseModel):
    """每日运势请求"""
    day_master: Optional[str] = Field(None, description="日主天干，如：甲、乙、丙等")
    date: Optional[str] = Field(None, description="日期，格式：YYYY-MM-DD，默认今天")


class MonthlyFortuneRequest(BaseModel):
    """每月运势请求"""
    day_master: str = Field(..., description="日主天干")
    year: int = Field(..., description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")


class WeeklyTrendRequest(BaseModel):
    """周趋势请求"""
    day_master: str = Field(..., description="日主天干")
    center_date: Optional[str] = Field(None, description="中心日期，默认今天")


class InterpretationRequest(BaseModel):
    """运势解读请求"""
    ten_god: str = Field(..., description="十神")
    overall: int = Field(..., ge=0, le=100)
    career: int = Field(..., ge=0, le=100)
    love: int = Field(..., ge=0, le=100)
    wealth: int = Field(..., ge=0, le=100)
    health: int = Field(..., ge=0, le=100)
    social: int = Field(..., ge=0, le=100)
    mode: Literal['colloquial', 'professional', 'technical'] = 'colloquial'


def parse_date(date_str: Optional[str]) -> date:
    """解析日期字符串"""
    if not date_str:
        return date.today()
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="日期格式错误，应为YYYY-MM-DD")


def validate_day_master(day_master: str) -> str:
    """验证日主天干"""
    valid_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    if day_master not in valid_stems:
        raise HTTPException(status_code=400, detail=f"无效的日主天干，应为：{', '.join(valid_stems)}")
    return day_master


@router.post("/daily")
async def get_daily_fortune(request: DailyFortuneRequest):
    """
    获取每日运势
    
    - 如果提供日主天干，返回个性化运势
    - 如果不提供，返回通用运势
    """
    target_date = parse_date(request.date)
    
    if request.day_master:
        day_master = validate_day_master(request.day_master)
        fortune = calculate_daily_fortune(day_master, target_date)
        return {
            "personalized": True,
            "date": fortune.date,
            "day_stem": fortune.day_stem,
            "day_branch": fortune.day_branch,
            "ten_god": fortune.ten_god,
            "scores": {
                "overall": fortune.overall,
                "career": fortune.career,
                "love": fortune.love,
                "wealth": fortune.wealth,
                "health": fortune.health,
                "social": fortune.social,
            },
            "advice": fortune.advice,
            "lucky_color": fortune.lucky_color,
            "lucky_direction": fortune.lucky_direction,
        }
    else:
        fortune = calculate_generic_daily_fortune(target_date)
        return {
            "personalized": False,
            **fortune
        }


@router.get("/daily")
async def get_daily_fortune_simple(
    day_master: Optional[str] = Query(None, description="日主天干"),
    date: Optional[str] = Query(None, description="日期YYYY-MM-DD")
):
    """GET方式获取每日运势"""
    request = DailyFortuneRequest(day_master=day_master, date=date)
    return await get_daily_fortune(request)


@router.post("/monthly")
async def get_monthly_fortune(request: MonthlyFortuneRequest):
    """获取每月运势"""
    day_master = validate_day_master(request.day_master)
    fortune = calculate_monthly_fortune(day_master, request.year, request.month)
    
    return {
        "year": fortune.year,
        "month": fortune.month,
        "month_stem": fortune.month_stem,
        "month_branch": fortune.month_branch,
        "ten_god": fortune.ten_god,
        "scores": {
            "overall": fortune.overall,
            "career": fortune.career,
            "love": fortune.love,
            "wealth": fortune.wealth,
            "health": fortune.health,
            "social": fortune.social,
        },
        "summary": fortune.summary,
        "key_dates": fortune.key_dates,
    }


@router.get("/monthly")
async def get_monthly_fortune_simple(
    day_master: str = Query(..., description="日主天干"),
    year: int = Query(..., description="年份"),
    month: int = Query(..., ge=1, le=12, description="月份")
):
    """GET方式获取每月运势"""
    request = MonthlyFortuneRequest(day_master=day_master, year=year, month=month)
    return await get_monthly_fortune(request)


@router.post("/weekly-trend")
async def get_weekly_trend(request: WeeklyTrendRequest):
    """获取周趋势数据（以指定日期为中心的7天）"""
    day_master = validate_day_master(request.day_master)
    center_date = parse_date(request.center_date)
    
    trend = calculate_weekly_trend(day_master, center_date)
    return {"trend": trend}


@router.get("/weekly-trend")
async def get_weekly_trend_simple(
    day_master: str = Query(..., description="日主天干"),
    center_date: Optional[str] = Query(None, description="中心日期")
):
    """GET方式获取周趋势"""
    request = WeeklyTrendRequest(day_master=day_master, center_date=center_date)
    return await get_weekly_trend(request)


@router.post("/interpret")
async def get_interpretation(request: InterpretationRequest):
    """获取运势解读文本"""
    scores = {
        'overall': request.overall,
        'career': request.career,
        'love': request.love,
        'wealth': request.wealth,
        'health': request.health,
        'social': request.social,
    }
    
    interpretation = generate_fortune_interpretation(
        request.ten_god,
        scores,
        request.mode
    )
    
    return {"interpretation": interpretation}


# ========== 命理文案库API ==========

@router.get("/bazi/day-master/{day_master}")
async def get_day_master_info(day_master: str):
    """获取日干心性解读"""
    day_master = validate_day_master(day_master)
    personality = get_day_master_personality(day_master)
    if not personality:
        raise HTTPException(status_code=404, detail="未找到该日主信息")
    return {"day_master": day_master, **personality}


@router.get("/bazi/day-masters")
async def list_day_masters():
    """获取所有日干心性列表"""
    return {"day_masters": DAY_MASTER_PERSONALITIES}


@router.get("/bazi/ten-god/{ten_god}")
async def get_ten_god_info(ten_god: str):
    """获取十神详解"""
    detail = get_ten_god_detail(ten_god)
    if not detail:
        raise HTTPException(status_code=404, detail="未找到该十神信息")
    return {"ten_god": ten_god, **detail}


@router.get("/bazi/ten-gods")
async def list_ten_gods():
    """获取所有十神详解列表"""
    return {"ten_gods": TEN_GODS_DETAILED}


@router.get("/bazi/yongshen-career/{element}")
async def get_yongshen_career(element: str):
    """获取喜用神事业建议"""
    valid_elements = ['木', '火', '土', '金', '水']
    if element not in valid_elements:
        raise HTTPException(status_code=400, detail=f"无效的五行，应为：{', '.join(valid_elements)}")
    advice = get_yongshen_career_advice(element)
    return {"element": element, "career_advice": advice}


@router.get("/bazi/qiongtong/{day_master}/{month}")
async def get_qiongtong_info(day_master: str, month: str):
    """获取穷通宝鉴调候建议"""
    day_master = validate_day_master(day_master)
    advice = get_qiongtong_advice(day_master, month)
    if not advice:
        return {"day_master": day_master, "month": month, "advice": "暂无该月令调候建议"}
    return {"day_master": day_master, "month": month, "advice": advice}


@router.get("/bazi/seasonal-yongshen/{season}/{element}")
async def get_seasonal_yongshen_info(season: str, element: str):
    """获取四季用神参考"""
    valid_seasons = ['春', '夏', '秋', '冬']
    valid_elements = ['木', '火', '土', '金', '水']
    
    if season not in valid_seasons:
        raise HTTPException(status_code=400, detail=f"无效的季节，应为：{', '.join(valid_seasons)}")
    if element not in valid_elements:
        raise HTTPException(status_code=400, detail=f"无效的五行，应为：{', '.join(valid_elements)}")
    
    advice = get_seasonal_yongshen(season, element)
    return {"season": season, "element": element, "advice": advice}


# ========== 人生K线API ==========

class LifeKLineRequest(BaseModel):
    """人生K线请求"""
    name: Optional[str] = Field(None, description="姓名")
    gender: str = Field(..., description="性别：male或female")
    birth_year: int = Field(..., description="出生年份")
    year_pillar: str = Field(..., description="年柱")
    month_pillar: str = Field(..., description="月柱")
    day_pillar: str = Field(..., description="日柱")
    hour_pillar: str = Field(..., description="时柱")
    start_age: int = Field(..., ge=1, le=12, description="起运年龄（虚岁）")
    first_dayun: str = Field(..., description="第一步大运干支")


@router.post("/life-kline/prompt")
async def generate_life_kline_prompt(request: LifeKLineRequest):
    """
    生成人生K线AI提示词
    
    返回系统指令和用户提示词，可用于调用AI生成K线数据
    """
    try:
        gender = Gender.MALE if request.gender.lower() == "male" else Gender.FEMALE
    except:
        raise HTTPException(status_code=400, detail="性别应为male或female")
    
    # 验证四柱
    for pillar_name, pillar_value in [
        ("年柱", request.year_pillar),
        ("月柱", request.month_pillar),
        ("日柱", request.day_pillar),
        ("时柱", request.hour_pillar),
        ("第一步大运", request.first_dayun)
    ]:
        if len(pillar_value) != 2:
            raise HTTPException(status_code=400, detail=f"{pillar_name}应为2个字符的干支")
    
    # 计算大运方向
    is_forward = get_dayun_direction(gender, request.year_pillar)
    dayun_sequence = generate_dayun_sequence(request.first_dayun, is_forward, 10)
    
    # 生成提示词
    user_prompt = build_user_prompt(
        name=request.name,
        gender=gender,
        birth_year=request.birth_year,
        year_pillar=request.year_pillar,
        month_pillar=request.month_pillar,
        day_pillar=request.day_pillar,
        hour_pillar=request.hour_pillar,
        start_age=request.start_age,
        first_dayun=request.first_dayun
    )
    
    return {
        "system_instruction": LIFE_KLINE_SYSTEM_INSTRUCTION,
        "user_prompt": user_prompt,
        "dayun_direction": "顺行" if is_forward else "逆行",
        "dayun_sequence": dayun_sequence,
        "bazi": [
            request.year_pillar,
            request.month_pillar,
            request.day_pillar,
            request.hour_pillar
        ]
    }


@router.get("/life-kline/info")
async def get_life_kline_info():
    """获取人生K线功能说明"""
    return {
        "name": "人生K线",
        "description": "将八字命理运势以股票K线图形式可视化展示",
        "features": [
            "100年流年大运走势图",
            "每年运势评分（0-100）",
            "吉凶趋势可视化",
            "大运节点标记",
            "详细流年批断"
        ],
        "required_fields": {
            "name": "姓名（可选）",
            "gender": "性别（male/female）",
            "birth_year": "出生年份",
            "year_pillar": "年柱（如：甲子）",
            "month_pillar": "月柱",
            "day_pillar": "日柱",
            "hour_pillar": "时柱",
            "start_age": "起运年龄（1-12虚岁）",
            "first_dayun": "第一步大运干支"
        },
        "output_format": {
            "chartPoints": "K线数据点数组（age, year, ganZhi, daYun, open, close, high, low, score, reason）",
            "analysis": "命理分析（总评、事业、财运、婚姻、健康、六亲等维度及评分）"
        }
    }
