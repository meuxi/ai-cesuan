"""抽签路由 - 完整移植ASP源码的圣杯机制"""
import json
import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import random
from openai import AsyncOpenAI
from ..divination.chouqian.models import ChouqianResult, ChouqianRequest, ShengbeiResult
from ..divination.chouqian.service import chouqian_service
from ..config import settings
from ..common import safe_api_call, get_api_config_from_request, validate_api_config

_logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chouqian", tags=["抽签"])


class ShengbeiRequest(BaseModel):
    """圣杯请求"""
    qian_type: str = Field(..., min_length=1, max_length=50, description="签类型")
    qian_number: int = Field(..., ge=1, le=200, description="签号")
    current_count: int = Field(0, ge=0, le=3, description="当前已成功次数")


class ShengbeiResponse(BaseModel):
    """圣杯响应"""
    is_shengbei: bool      # True=圣杯, False=笑杯
    current_count: int     # 当前累计圣杯次数
    is_complete: bool      # 是否完成(3次圣杯)
    is_failed: bool        # 是否失败(掷出笑杯)
    message: str           # 提示信息
    can_view_result: bool  # 是否可以查看签文


class DrawWithShengbeiResponse(BaseModel):
    """抽签响应(含圣杯流程)"""
    qian_number: int       # 抽到的签号
    qian_type: str         # 签类型
    type_name: str         # 签类型名称
    message: str           # 提示信息
    need_shengbei: bool    # 是否需要掷圣杯


@router.get("/types", summary="获取签类型列表")
async def get_qian_types() -> Dict[str, dict]:
    """获取所有支持的签类型"""
    return chouqian_service.get_types()


@router.post("/draw", response_model=ChouqianResult, summary="抽签")
@safe_api_call("抽签")
async def draw_qian(request: ChouqianRequest):
    """
    抽签接口
    
    - **type**: 签类型 guanyin/guandi/lvzu/tianhou
    - **user_name**: 求签人姓名（可选）
    - **question**: 所问之事（可选）
    """
    return chouqian_service.draw(request.type)


@router.get("/detail/{qian_type}/{number}", response_model=ChouqianResult, summary="获取签文详情")
@safe_api_call("获取签文详情")
async def get_qian_detail(qian_type: str, number: int):
    """
    根据签号获取签文详情
    
    - **qian_type**: 签类型（guanyin）
    - **number**: 签号（1-100）
    """
    return chouqian_service.get_by_number(qian_type, number)


@router.get("/list/{qian_type}", response_model=List[ChouqianResult], summary="获取签文列表")
@safe_api_call("获取签文列表")
async def get_qian_list(qian_type: str):
    """
    获取所有签文列表
    
    - **qian_type**: 签类型（guanyin）
    """
    return chouqian_service.get_all(qian_type)


@router.post("/draw_start", response_model=DrawWithShengbeiResponse, summary="开始抽签(含圣杯流程)")
async def draw_start(request: ChouqianRequest):
    """
    开始抽签 - 完整实现源码中的抽签流程
    
    流程(从guanyin.asp等移植)：
    1. 随机产生签号
    2. 返回签号，提示用户需要掷圣杯
    3. 用户调用/shengbei接口掷圣杯
    4. 连续3次圣杯后调用/detail获取签文
    """
    try:
        types = chouqian_service.get_types()
        if request.type not in types:
            raise ValueError(f"不支持的签类型: {request.type}")
        
        type_info = types[request.type]
        count = type_info.get("count", 100)
        
        # 随机产生签号
        qian_number = random.randint(1, count)
        
        return DrawWithShengbeiResponse(
            qian_number=qian_number,
            qian_type=request.type,
            type_name=type_info["name"],
            message=f"您抽到了第{qian_number}签，请掷圣杯确认",
            need_shengbei=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/shengbei", response_model=ShengbeiResponse, summary="掷圣杯")
async def throw_shengbei(request: ShengbeiRequest):
    """
    掷圣杯 - 完整实现源码中的圣杯/笑杯机制
    
    规则(从guanyin.asp移植)：
    - 圣杯概率: 3/4 (75%)
    - 笑杯概率: 1/4 (25%)
    - 需连续掷出3次圣杯
    - 掷出笑杯则此签无效需重新抽签
    """
    # 1/4概率笑杯, 3/4概率圣杯
    result = random.randint(1, 4)
    is_shengbei = (result != 4)
    
    if is_shengbei:
        new_count = request.current_count + 1
        is_complete = (new_count >= 3)
        
        if is_complete:
            message = "恭喜！您连续掷出了三次圣杯，请查看签词！"
        else:
            message = f"圣杯！已掷出{new_count}次圣杯，还需{3-new_count}次"
        
        return ShengbeiResponse(
            is_shengbei=True,
            current_count=new_count,
            is_complete=is_complete,
            is_failed=False,
            message=message,
            can_view_result=is_complete
        )
    else:
        return ShengbeiResponse(
            is_shengbei=False,
            current_count=0,
            is_complete=False,
            is_failed=True,
            message="笑杯！此签不准，请重新抽签！",
            can_view_result=False
        )


class AIJieqianRequest(BaseModel):
    """AI解签请求"""
    qian_type: str = Field(..., min_length=1, max_length=50, description="签类型")
    qian_number: int = Field(..., ge=1, le=200, description="签号")
    user_name: str = Field("", max_length=50, description="求签人姓名")
    question: str = Field("", max_length=500, description="所问之事")


@router.post("/ai_jieqian", summary="AI解签")
async def ai_jieqian(request: Request, body: AIJieqianRequest):
    """
    AI智能解签 - 根据签文内容和用户问题提供个性化解读
    
    流式返回AI解签结果
    """
    try:
        # 获取签文详情
        qian_detail = chouqian_service.get_by_number(body.qian_type, body.qian_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    # 构建解签内容
    qian_info = f"【{qian_detail.type_name}第{qian_detail.number}签】\n"
    qian_info += f"签名：{qian_detail.title}\n"
    
    # 根据签类型添加特定字段
    if body.qian_type == "huangdaxian":
        if qian_detail.qianshu:
            qian_info += f"签属：{qian_detail.qianshu}\n"
        if qian_detail.name:
            qian_info += f"签等：{qian_detail.name}\n"
        if qian_detail.shi:
            qian_info += f"签诗：{qian_detail.shi}\n"
    
    qian_info += f"签文：{qian_detail.content}\n"
    
    # 用户信息
    user_info = ""
    if body.user_name:
        user_info += f"求签人：{body.user_name}\n"
    if body.question:
        user_info += f"所问之事：{body.question}\n"
    
    # 从模版库获取提示词
    from ..prompts import get_prompt_manager
    manager = get_prompt_manager()
    template = manager.get_template("chouqian_analysis")
    
    if template:
        system_prompt = template.system_prompt
    else:
        system_prompt = "你是一位精通中国传统文化的解签大师，擅长解读各类灵签。"

    user_prompt = f"{qian_info}\n{user_info}\n请为此签进行详细解读。"
    
    # 获取API配置（使用统一工具函数）
    api_config = get_api_config_from_request(request)
    try:
        validate_api_config(api_config)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    
    api_client = AsyncOpenAI(
        api_key=api_config["api_key"],
        base_url=api_config["base_url"],
        timeout=60.0,
        max_retries=0
    )
    
    try:
        openai_stream = await api_client.chat.completions.create(
            model=api_config["model"],
            max_tokens=32000,  # 用户体验优先：无限制输出
            temperature=0.8,
            stream=True,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    except Exception as e:
        _logger.error(f"AI解签API错误: {e}")
        raise HTTPException(status_code=500, detail="AI服务暂时不可用，请稍后重试")
    
    async def generate():
        try:
            async for event in openai_stream:
                if event.choices and event.choices[0].delta and event.choices[0].delta.content:
                    content = event.choices[0].delta.content
                    yield f"data: {json.dumps(content)}\n\n"
        except Exception as e:
            _logger.error(f"AI解签流式错误: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type='text/event-stream')
