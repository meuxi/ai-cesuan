import json
import time
from typing import Optional
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

import logging

from fastapi import Depends, Request, status, HTTPException


from src.config import settings
from fastapi import APIRouter

from src.models import DivinationBody, User
from src.user import get_user
from src.limiter import get_real_ipaddr, check_rate_limit
from src.divination import DivinationFactory
from src.exceptions import (
    InvalidDivinationTypeError,
    StopWordDetectedError,
    APIConfigError,
    APICallError,
    ZhipuConcurrencyError,
)
from src.ai import AIProviderManager, AIModelConfig, AIModel
from src.ai.models import PRESET_ROUTES, ModelStatus
from src.ai.provider import ChatMessage
from src.ai.degradation import degradation_manager, check_should_proceed
from src.ai.token_counter import estimate_tokens, estimate_cost
from src.quota import quota_manager
from src.monitoring import cost_monitor
from src.prompts.output_control import enhance_prompt_with_length_control, get_output_max_tokens
from src.i18n import Translator

client = AsyncOpenAI(api_key=settings.api_key, base_url=settings.api_base)
router = APIRouter()
_logger = logging.getLogger(__name__)

# 初始化AI故障转移管理器（使用配置的API密钥）
def _init_ai_manager() -> AIProviderManager:
    """初始化AI管理器，使用环境变量配置的API密钥"""
    config = AIModelConfig()
    
    # 1. DashScope (阿里云百炼) - 优先使用
    if settings.dashscope_api_key:
        config.add_model(AIModel(
            name="DashScope-Qwen",
            provider="openai",  # OpenAI兼容格式
            api_key=settings.dashscope_api_key,
            base_url=settings.dashscope_api_base,
            is_primary=True,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.dashscope_model}
        ))
        _logger.info(f"[AI] 已配置DashScope: {settings.dashscope_model}")
    
    # 2. DeepSeek - 备用
    if settings.deepseek_api_key:
        config.add_model(AIModel(
            name="DeepSeek",
            provider="openai",
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.deepseek_model}
        ))
        _logger.info(f"[AI] 已配置DeepSeek: {settings.deepseek_model}")
    
    # 3. 智谱AI - 备用
    if settings.zhipu_api_key:
        config.add_model(AIModel(
            name="Zhipu-GLM",
            provider="openai",
            api_key=settings.zhipu_api_key,
            base_url=settings.zhipu_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.zhipu_model}
        ))
        _logger.info(f"[AI] 已配置智谱AI: {settings.zhipu_model}")
    
    # 4. 硅基流动 SiliconFlow - 备用
    if settings.siliconflow_api_key:
        config.add_model(AIModel(
            name="SiliconFlow",
            provider="openai",
            api_key=settings.siliconflow_api_key,
            base_url=settings.siliconflow_api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.siliconflow_model}
        ))
        _logger.info(f"[AI] 已配置SiliconFlow: {settings.siliconflow_model}")
    
    # 5. OpenAI - 最后备用（兼容所有OpenAI格式的API）
    if settings.api_key and settings.api_key != "sk-test-1234567890":
        config.add_model(AIModel(
            name="OpenAI",
            provider="openai",
            api_key=settings.api_key,
            base_url=settings.api_base,
            status=ModelStatus.ACTIVE,
            parameters={"model": settings.model}
        ))
        _logger.info(f"[AI] 已配置OpenAI: {settings.model}")
    
    return AIProviderManager(config)

_ai_manager: Optional[AIProviderManager] = None

def get_ai_manager() -> AIProviderManager:
    """获取全局AI管理器（懒加载）"""
    global _ai_manager
    if _ai_manager is None:
        _ai_manager = _init_ai_manager()
    return _ai_manager


@router.post("/divination")
async def divination(
        request: Request,
        divination_body: DivinationBody,
        user: Optional[User] = Depends(get_user)
):
    """
    AI占卜接口 - 流式返回占卜结果
    
    Args:
        request: FastAPI请求对象，用于获取客户端IP和自定义API配置
        divination_body: 占卜请求体，包含prompt和prompt_type
        user: 可选的已登录用户信息
    
    Returns:
        StreamingResponse: SSE流式响应，逐步返回AI生成的占卜结果
    
    Raises:
        HTTPException 403: prompt包含停止词或缺少API配置
        HTTPException 400: 不支持的占卜类型
        HTTPException 429: 智谱AI并发限制
        HTTPException 500: API调用失败
    
    支持的自定义Header:
        x-api-key: 自定义API密钥
        x-api-url: 自定义API基础URL
        x-api-model: 自定义模型名称
    """
    real_ip = get_real_ipaddr(request)
    request_start_time = time.time()
    
    # 检查降级状态
    should_proceed, reject_reason = check_should_proceed()
    if not should_proceed:
        raise HTTPException(status_code=503, detail=reject_reason)
    
    # 获取用户ID
    user_id = f"{user.login_type}:{user.user_name}" if user else f"ip:{real_ip}"
    
    # 用户配额检查
    quota_check = quota_manager.check_quota(user_id)
    if not quota_check["allowed"]:
        raise HTTPException(status_code=429, detail=quota_check["reason"])
    
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
    if any(w in divination_body.prompt.lower() for w in settings.stop_words):
        raise StopWordDetectedError(message="输入包含禁止词汇，请重新输入")
    
    divination_obj = DivinationFactory.get(divination_body.prompt_type)
    if not divination_obj:
        raise InvalidDivinationTypeError(
            message=f"不支持的占卜类型: {divination_body.prompt_type}"
        )
    prompt, system_prompt = divination_obj.build_prompt(divination_body)
    
    # 多语言输出支持
    target_lang = divination_body.language or "zh"
    if target_lang and target_lang != "zh":
        translator = Translator()
        lang_prompt = translator.build_translation_prompt(target_lang)
        if lang_prompt:
            system_prompt = f"{system_prompt}\n\n{lang_prompt}"
            _logger.info(f"[多语言] 已启用{translator.get_language_name(target_lang)}输出")
    
    # 获取降级策略推荐的输出模式
    output_mode = degradation_manager.get_output_mode()
    max_tokens = min(
        degradation_manager.get_max_output_tokens(),
        quota_manager.get_max_output_tokens(user_id),
        get_output_max_tokens(output_mode, divination_body.prompt_type)
    )
    
    # 应用输出长度控制
    prompt = enhance_prompt_with_length_control(
        prompt, output_mode, divination_body.prompt_type
    )

    # custom api key, model and base url support
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    
    # 判断是否使用自定义配置
    use_custom_api = custom_api_key and custom_api_key.strip()
    
    if use_custom_api:
        # 使用用户自定义的API配置
        final_api_key = custom_api_key.strip().replace('\xa0', '').replace('\u200b', '')
        if final_api_key.startswith("Bearer "):
            final_api_key = final_api_key[7:].strip()
        final_base_url = custom_base_url or settings.api_base or "https://api.openai.com/v1"
        api_model = custom_api_model or settings.model or "gpt-3.5-turbo"
        
        is_zhipu = final_base_url and "bigmodel.cn" in final_base_url
        
        api_client = AsyncOpenAI(
            api_key=final_api_key, 
            base_url=final_base_url,
            timeout=60.0,
            max_retries=0
        )

        try:
            openai_stream = await api_client.chat.completions.create(
                model=api_model,
                max_tokens=max_tokens,
                temperature=0.9,
                top_p=1,
                stream=True,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            error_msg = str(e)
            _logger.error(f"Custom API error: {error_msg}")
            if is_zhipu and ("1302" in error_msg or "并发" in error_msg):
                raise ZhipuConcurrencyError()
            if "timeout" in error_msg.lower():
                raise APICallError(message="AI服务响应超时，请稍后重试")
            elif "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
                raise APIConfigError(message="API密钥无效，请检查配置")
            else:
                raise APICallError(message="AI服务暂时不可用，请稍后重试")
    else:
        # 使用预设的免费模型线路（AI故障转移）
        _logger.info("使用预设AI模型线路（故障转移模式）")
        ai_manager = get_ai_manager()
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt)
        ]
        
        try:
            result = await ai_manager.chat_with_failover(
                messages=messages,
                temperature=0.9,
                max_tokens=max_tokens,
            )
            _logger.info(f"使用模型: {result.model_used.name}, 尝试次数: {result.attempts}")
            
            # 记录成本监控
            latency = time.time() - request_start_time
            input_tokens = estimate_tokens(system_prompt + prompt)
            output_tokens = estimate_tokens(result.response.content)
            # 新增：确保 token 数不为空/0
total_tokens = input_tokens + output_tokens
# 修复空值问题：避免空值参与计算
cost = result.cost if (hasattr(result, 'cost') and result.cost is not None) else (
    estimate_cost(total_tokens, 0.002) if total_tokens > 0 else 0.0
)
            )
            
            cost_monitor.record_call(
                model=result.model_used.name,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                latency=latency,
                success=True,
                tool_name=divination_body.prompt_type,
                user_id=user_id
            )
            
            # 消费用户配额
            quota_manager.consume_quota(user_id, input_tokens + output_tokens, cost)
            
            # 非流式响应，模拟流式输出
            async def simulate_stream():
                content = result.response.content
                # 按字符分块输出，模拟流式效果
                chunk_size = 2
                for i in range(0, len(content), chunk_size):
                    chunk = content[i:i+chunk_size]
                    yield f"data: {json.dumps(chunk)}\n\n"
            
            return StreamingResponse(simulate_stream(), media_type='text/event-stream')
            
        except Exception as e:
            _logger.error(f"AI failover error: {e}")
            raise APICallError(message="AI服务暂时不可用，请稍后重试")

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
