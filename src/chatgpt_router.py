import json
from typing import Optional
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

import logging

from fastapi import Depends, HTTPException, Request, status


from src.config import settings
from fastapi import APIRouter

from src.models import DivinationBody, User
from src.user import get_user
from src.limiter import get_real_ipaddr, check_rate_limit
from src.divination import DivinationFactory

client = AsyncOpenAI(api_key=settings.api_key, base_url=settings.api_base)
router = APIRouter()
_logger = logging.getLogger(__name__)
STOP_WORDS = [
    "忽略", "ignore", "指令", "命令", "command", "help", "帮助", "之前",
    "幫助", "現在", "開始", "开始", "start", "restart", "重新开始", "重新開始",
    "遵守", "遵循", "遵从", "遵從"
]


@router.post("/api/divination")
async def divination(
        request: Request,
        divination_body: DivinationBody,
        user: Optional[User] = Depends(get_user)
):

    real_ip = get_real_ipaddr(request)
    # rate limit when not login
    if settings.enable_rate_limit:
        if not user:
            max_reqs, time_window_seconds = settings.rate_limit
            check_rate_limit(f"{settings.project_name}:{real_ip}", time_window_seconds, max_reqs)
        else:
            max_reqs, time_window_seconds = settings.user_rate_limit
            check_rate_limit(
                f"{settings.project_name}:{user.login_type}:{user.user_name}", time_window_seconds, max_reqs
            )

    _logger.info(
        f"Request from {real_ip}, "
        f"user={json.dumps(user.model_dump(), ensure_ascii=False) if user else None}, "
        f"body={json.dumps(divination_body.model_dump(), ensure_ascii=False)}"
    )
    if any(w in divination_body.prompt.lower() for w in STOP_WORDS):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Prompt contains stop words"
        )
    divination_obj = DivinationFactory.get(divination_body.prompt_type)
    if not divination_obj:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No prompt type {divination_body.prompt_type} not supported"
        )
    prompt, system_prompt = divination_obj.build_prompt(divination_body)

    # custom api key, model and base url support
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    
    # 确定使用的 API 配置
    final_api_key = custom_api_key or settings.api_key
    final_base_url = custom_base_url or settings.api_base
    api_model = custom_api_model if custom_api_model else settings.model

    if not final_base_url or not final_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请设置 API KEY 和 API BASE URL"
        )
    
    # 清理API密钥：去除前后空格、不可见字符和Bearer前缀
    final_api_key = final_api_key.strip().replace('\xa0', '').replace('\u200b', '')
    if final_api_key.startswith("Bearer "):
        final_api_key = final_api_key[7:].strip()
    
    # 检测是否是智谱AI（用于特殊处理）
    is_zhipu = final_base_url and "bigmodel.cn" in final_base_url
    
    # 智谱AI兼容：智谱AI使用OpenAI兼容接口，直接使用AsyncOpenAI客户端即可
    # 智谱AI API密钥格式: xxxxx.xxxxx (SDK会自动添加 Bearer 前缀)
    # OpenAI API密钥格式: sk-xxxxx (SDK会自动添加 Bearer 前缀)
    api_client = AsyncOpenAI(
        api_key=final_api_key, 
        base_url=final_base_url,
        timeout=60.0,  # 增加超时时间
        max_retries=0  # 智谱AI并发限制严格，禁用自动重试
        )

    try:
        openai_stream = await api_client.chat.completions.create(
            model=api_model,
            max_tokens=1000,
            temperature=0.9,
            top_p=1,
            stream=True,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        error_msg = str(e)
        _logger.error(f"API error: {error_msg}")
        
        # 智谱AI并发限制友好提示
        if is_zhipu and ("1302" in error_msg or "并发" in error_msg):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="智谱AI并发请求过多，请稍后再试（建议间隔3-5秒）"
            )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"API调用失败: {error_msg}"
        )

    async def get_openai_generator():
        try:
            async for event in openai_stream:
                if event.choices and event.choices[0].delta and event.choices[0].delta.content:
                    current_response = event.choices[0].delta.content
                    yield f"data: {json.dumps(current_response)}\n\n"
        except Exception as e:
            _logger.error(f"Streaming error: {e}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(get_openai_generator(), media_type='text/event-stream')
