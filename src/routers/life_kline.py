"""
人生K线图 API 路由
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from ..divination.life_kline import (
    LifeKLineAnalyzer,
    LifeKLineInput,
    Gender,
    calculate_dayun_direction,
)

router = APIRouter(prefix="/life-kline", tags=["人生K线图"])


class LifeKLineRequest(BaseModel):
    """人生K线图请求"""
    name: str = ""
    gender: str = "male"
    birth_year: int
    year_pillar: str
    month_pillar: str
    day_pillar: str
    hour_pillar: str
    start_age: int = 1
    first_dayun: str
    is_forward: Optional[bool] = None  # 可选，不提供则自动计算
    use_ai: bool = True  # 默认使用AI生成
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    model_name: Optional[str] = None


class LifeKLineResponse(BaseModel):
    """人生K线图响应"""
    chartData: List[Dict[str, Any]]
    analysis: Dict[str, Any]


@router.post("/generate", response_model=LifeKLineResponse)
async def generate_life_kline(request: LifeKLineRequest) -> Dict[str, Any]:
    """
    生成人生K线图
    
    **参数说明:**
    - **name**: 姓名（可选）
    - **gender**: 性别 (male/female)
    - **birth_year**: 出生年份（阳历）
    - **year_pillar**: 年柱，如"甲子"
    - **month_pillar**: 月柱
    - **day_pillar**: 日柱
    - **hour_pillar**: 时柱
    - **start_age**: 起运年龄（虚岁）
    - **first_dayun**: 第一步大运
    - **is_forward**: 大运是否顺行（可选，不提供则自动计算）
    - **use_ai**: 是否使用AI生成详细分析
    - **api_key**: AI API Key（use_ai=true时需要）
    - **api_base_url**: AI API Base URL（可选）
    - **model_name**: 模型名称（可选）
    
    **返回:**
    - chartData: 1-100岁的K线数据数组
    - analysis: 命理分析结果
    """
    try:
        # 解析性别
        gender = Gender.MALE if request.gender.lower() == "male" else Gender.FEMALE
        
        # 自动计算大运顺逆（如果未提供）
        is_forward = request.is_forward
        if is_forward is None:
            is_forward = calculate_dayun_direction(request.year_pillar, gender)
        
        # 构建输入
        input_data = LifeKLineInput(
            name=request.name,
            gender=gender,
            birth_year=request.birth_year,
            year_pillar=request.year_pillar,
            month_pillar=request.month_pillar,
            day_pillar=request.day_pillar,
            hour_pillar=request.hour_pillar,
            start_age=request.start_age,
            first_dayun=request.first_dayun,
            is_forward=is_forward,
        )
        
        # 创建分析器
        analyzer = LifeKLineAnalyzer()
        
        if request.use_ai:
            # 使用项目配置的AI服务生成
            from src.chatgpt_router import get_ai_manager as get_chatgpt_ai_manager
            
            # 获取已配置的AI管理器
            ai_manager = get_chatgpt_ai_manager()
            analyzer.ai_service = ai_manager
            result = await analyzer.generate_with_ai(input_data)
        else:
            # 使用基础算法生成
            result = analyzer.generate_basic_chart(input_data)
        
        return result.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成K线图失败: {str(e)}")


@router.post("/demo")
async def generate_demo_kline(request: LifeKLineRequest) -> Dict[str, Any]:
    """
    生成演示用K线图（不需要API Key）
    
    使用基础命理算法生成，适合演示和测试
    """
    try:
        gender = Gender.MALE if request.gender.lower() == "male" else Gender.FEMALE
        
        is_forward = request.is_forward
        if is_forward is None:
            is_forward = calculate_dayun_direction(request.year_pillar, gender)
        
        input_data = LifeKLineInput(
            name=request.name,
            gender=gender,
            birth_year=request.birth_year,
            year_pillar=request.year_pillar,
            month_pillar=request.month_pillar,
            day_pillar=request.day_pillar,
            hour_pillar=request.hour_pillar,
            start_age=request.start_age,
            first_dayun=request.first_dayun,
            is_forward=is_forward,
        )
        
        analyzer = LifeKLineAnalyzer()
        result = analyzer.generate_basic_chart(input_data)
        
        return result.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)}")


@router.get("/dayun-direction")
async def calculate_direction(
    year_pillar: str,
    gender: str
) -> Dict[str, Any]:
    """
    计算大运顺逆方向
    
    **参数:**
    - year_pillar: 年柱
    - gender: 性别 (male/female)
    
    **返回:**
    - is_forward: 是否顺行
    - direction: 方向描述
    """
    g = Gender.MALE if gender.lower() == "male" else Gender.FEMALE
    is_forward = calculate_dayun_direction(year_pillar, g)
    
    return {
        "is_forward": is_forward,
        "direction": "顺行" if is_forward else "逆行",
        "description": f"年柱{year_pillar}，{'男' if g == Gender.MALE else '女'}命，大运{'顺行' if is_forward else '逆行'}"
    }
