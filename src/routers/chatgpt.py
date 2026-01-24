import json
import os
import re
import time
import asyncio
from typing import Optional
from urllib.parse import urlparse
from fastapi.responses import StreamingResponse, JSONResponse
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
from src.ai import AIProviderManager, AIModelConfig, AIModel, get_ai_manager
from src.ai.models import PRESET_ROUTES, ModelStatus
from src.ai.provider import ChatMessage
from src.ai.degradation import degradation_manager, check_should_proceed
from src.ai.token_counter import estimate_tokens, estimate_cost
from src.quota import quota_manager
from src.monitoring import cost_monitor
from src.prompts.output_control import enhance_prompt_with_length_control, get_output_max_tokens
from src.i18n import Translator
from src.common.sse_response import SSEMessage, SSEErrorCode, SSE_HEADERS


# 预编译敏感字段集合（避免每次调用重新创建）
_SENSITIVE_KEYS_LOWER = {
    "api_key", "apikey", "api-key", "key", "secret", "password",
    "token", "access_token", "refresh_token", "jwt",
    "birthday", "bazi_data", "ziwei_data", "lunar_birthday",
    "expire_at", "cards",
}


def _sanitize_log_data(data: dict, sensitive_keys: set[str] = None) -> dict:
    """
    脱敏日志数据，隐藏敏感字段
    
    Args:
        data: 原始数据字典
        sensitive_keys: 需要脱敏的字段名集合
        
    Returns:
        脱敏后的数据字典
    """
    # 性能优化：非 DEBUG 级别时跳过脱敏处理，返回简化占位符
    if not _logger.isEnabledFor(logging.DEBUG):
        return {"_type": type(data).__name__, "_sanitized": True}
    
    if not isinstance(data, dict):
        return data
    
    # 使用预编译的敏感字段集合
    keys_to_check = sensitive_keys or _SENSITIVE_KEYS_LOWER
    
    result = {}
    for k, v in data.items():
        if k.lower() in keys_to_check:
            # 脱敏处理：只显示前4位和后4位（如果长度足够）
            if isinstance(v, str) and len(v) > 8:
                result[k] = f"{v[:4]}***{v[-4:]}"
            elif v is not None:
                result[k] = "***"
            else:
                result[k] = None
        elif isinstance(v, dict):
            result[k] = _sanitize_log_data(v, keys_to_check)
        elif isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            result[k] = f"[{len(v)} items]"  # 只显示数量
        else:
            result[k] = v
    
    return result

client = AsyncOpenAI(api_key=settings.api_key, base_url=settings.api_base)
router = APIRouter()
_logger = logging.getLogger(__name__)

# AI管理器已移至 src/ai/manager.py，通过 get_ai_manager 统一访问
# 保持向后兼容性：get_ai_manager 已从 src.ai 导入


@router.post("/divination")
async def divination(
        request: Request,
        divination_body: DivinationBody,
        user: Optional[User] = Depends(get_user)
):
    """
    AI占卜接口 - 返回AI生成的占卜结果
    
    Args:
        request: FastAPI请求对象，用于获取客户端IP和自定义API配置
        divination_body: 占卜请求体，包含prompt和prompt_type
        user: 可选的已登录用户信息
    
    Returns:
        - 自定义API模式: StreamingResponse (SSE流式响应)
        - 预设模式: JSONResponse (完整JSON，前端模拟打字机效果)
    
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

    # 性能优化：简化请求日志，减少 JSON 序列化开销
    _logger.info(f"Request: ip={real_ip}, type={divination_body.prompt_type}, len={len(divination_body.prompt)}")
    
    # 详细日志仅在 DEBUG 级别记录
    if _logger.isEnabledFor(logging.DEBUG):
        sanitized_user = _sanitize_log_data(user.model_dump()) if user else None
        sanitized_body = _sanitize_log_data(divination_body.model_dump())
        _logger.debug(f"Request detail: user={sanitized_user}, body={sanitized_body}")
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
    
    # 用户体验优先：固定最大输出，不设降级限制，确保报告完整
    output_mode = "detailed"
    max_tokens = 8000  # 约 4000 汉字，确保报告完整且不过长
    
    # 应用输出长度控制
    prompt = enhance_prompt_with_length_control(
        prompt, output_mode, divination_body.prompt_type
    )

    # ========== 安全增强：自定义API密钥处理 ==========
    custom_base_url = request.headers.get("x-api-url")
    custom_api_key = request.headers.get("x-api-key")
    custom_api_model = request.headers.get("x-api-model")
    
    # 判断是否使用自定义配置
    use_custom_api = custom_api_key and custom_api_key.strip()
    
    if use_custom_api:
        # 安全检查1：验证HTTPS协议（生产环境强制）
        is_production = os.getenv("VERCEL") == "1" or os.getenv("ENVIRONMENT") == "production"
        if is_production:
            # 多重检查请求是否通过HTTPS（防止头部伪造）
            forwarded_proto = request.headers.get("x-forwarded-proto", "").lower()
            # 额外检查：Cloudflare、AWS等CDN的协议头
            cf_visitor = request.headers.get("cf-visitor", "")
            is_https = (
                forwarded_proto == "https" or
                '"scheme":"https"' in cf_visitor or
                request.url.scheme == "https"
            )
            if not is_https:
                _logger.warning(f"拒绝非HTTPS请求传输自定义API密钥: {get_real_ipaddr(request)}")
                raise APIConfigError(message="安全错误：自定义API密钥仅支持HTTPS传输")
        
        # 安全检查2：API密钥格式验证
        final_api_key = custom_api_key.strip().replace('\xa0', '').replace('\u200b', '')
        if final_api_key.startswith("Bearer "):
            final_api_key = final_api_key[7:].strip()
        
        # 安全检查3：验证API密钥长度和格式
        if len(final_api_key) < 20:
            _logger.warning(f"API密钥格式无效（长度不足）: {get_real_ipaddr(request)}")
            raise APIConfigError(message="API密钥格式无效，请检查密钥是否完整")
        
        # 安全检查4：禁止可疑字符
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', final_api_key):
            _logger.warning(f"API密钥包含非法字符: {get_real_ipaddr(request)}")
            raise APIConfigError(message="API密钥包含无效字符")
        
        # 使用用户自定义的API配置
        final_base_url = custom_base_url or settings.api_base or "https://api.openai.com/v1"
        api_model = custom_api_model or settings.model or "gpt-3.5-turbo"
        
        # 安全检查5：验证API Base URL格式
        if final_base_url:
            parsed = urlparse(final_base_url)
            if parsed.scheme not in ("http", "https"):
                raise APIConfigError(message="API地址格式无效")
            # 生产环境强制HTTPS
            if is_production and parsed.scheme != "https":
                _logger.warning(f"生产环境拒绝非HTTPS的API地址: {final_base_url}")
                raise APIConfigError(message="生产环境仅支持HTTPS的API地址")
        
        is_zhipu = final_base_url and "bigmodel.cn" in final_base_url
        
        # 日志记录（不记录完整密钥）
        masked_key = f"{final_api_key[:8]}...{final_api_key[-4:]}" if len(final_api_key) > 12 else "***"
        _logger.info(f"使用自定义API配置: base={final_base_url}, model={api_model}, key={masked_key}")
        
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
        # 使用预设的免费模型线路（AI故障转移 + 流式输出）
        _logger.debug("使用预设AI模型线路（故障转移流式模式）")
        ai_manager = get_ai_manager()
        
        messages = [
            ChatMessage(role="system", content=system_prompt),
            ChatMessage(role="user", content=prompt)
        ]
        
        # 内存保护：最大输出长度限制（约 250KB）
        MAX_OUTPUT_LENGTH = 250000
        
        async def get_preset_stream_generator():
            """预设模型的流式生成器 - 使用统一的SSE响应格式"""
            # 优化：只统计输出长度，避免累积完整内容占用大量内存
            output_length = 0
            chunk_count = 0
            
            try:
                # 性能优化：禁用预检健康检查，减少 1-5 秒首字节延迟
                # 直接尝试主模型，失败后再故障转移到备用模型
                async for chunk in ai_manager.chat_stream_with_failover(
                    messages=messages,
                    temperature=0.9,
                    max_tokens=max_tokens,
                    pre_check=False,  # 禁用预检，避免额外的 API 调用
                ):
                    # 累计长度统计
                    chunk_len = len(chunk) if chunk else 0
                    output_length += chunk_len
                    chunk_count += 1
                    
                    # 内存保护：超出最大长度限制时停止
                    if output_length > MAX_OUTPUT_LENGTH:
                        _logger.warning(f"[流式响应] 输出超出限制 ({output_length}/{MAX_OUTPUT_LENGTH})，提前终止")
                        yield SSEMessage.data("\n\n[内容过长，已截断]")
                        break
                    
                    yield SSEMessage.data(chunk)
                
                # 发送结束标记
                yield SSEMessage.done()
                
                # 性能优化：使用后台任务记录监控，完全不阻塞响应
                async def _record_metrics():
                    try:
                        latency = time.time() - request_start_time
                        # 简化 token 估算，避免同步计算开销
                        input_tokens = len(system_prompt + prompt) // 4  # 粗略估算
                        output_tokens = output_length // 4
                        total_tokens = input_tokens + output_tokens
                        cost = estimate_cost(total_tokens, 0.002) if total_tokens > 0 else 0.0
                        
                        cost_monitor.record_call(
                            model="preset-stream",
                            input_tokens=input_tokens,
                            output_tokens=output_tokens,
                            cost=cost,
                            latency=latency,
                            success=True,
                            tool_name=divination_body.prompt_type,
                            user_id=user_id
                        )
                        quota_manager.consume_quota(user_id, total_tokens, cost)
                    except Exception as e:
                        _logger.warning(f"监控记录失败: {e}")
                
                # 创建后台任务，不等待完成
                asyncio.create_task(_record_metrics())
                    
            except asyncio.CancelledError:
                _logger.info("客户端断开连接，流式传输已取消")
                return
            except TimeoutError as e:
                _logger.error(f"Preset streaming timeout: {e}")
                yield SSEMessage.error(str(e), SSEErrorCode.TIMEOUT_ERROR)
                yield SSEMessage.done()
            except Exception as e:
                _logger.error(f"Preset streaming error: {e}")
                yield SSEMessage.error(str(e), SSEErrorCode.STREAM_ERROR)
                yield SSEMessage.done()
        
        # 返回流式响应（使用统一响应头）
        return StreamingResponse(
            get_preset_stream_generator(),
            media_type='text/event-stream',
            headers=SSE_HEADERS
        )

    async def get_openai_generator():
        """SSE 流式生成器 - 边收边发，实时输出（使用统一的SSE响应格式）"""
        try:
            async for event in openai_stream:
                # 检查是否结束（finish_reason 不为空表示生成完成）
                if event.choices and event.choices[0].finish_reason:
                    _logger.debug(f"Stream finished: {event.choices[0].finish_reason}")
                    yield SSEMessage.done()
                    break
                
                # 提取并发送内容
                if event.choices and event.choices[0].delta and event.choices[0].delta.content:
                    current_response = event.choices[0].delta.content
                    yield SSEMessage.data(current_response)
                    
        except asyncio.CancelledError:
            # 客户端主动断开连接（如用户取消请求）
            _logger.info("客户端断开连接，流式传输已取消")
            return
            
        except Exception as e:
            _logger.error(f"Streaming error: {e}")
            # 发送结构化错误信息（统一格式）
            yield SSEMessage.error(str(e), SSEErrorCode.STREAM_ERROR)
            yield SSEMessage.done()

    # 创建带完整响应头的 SSE 响应（使用统一响应头）
    return StreamingResponse(
        get_openai_generator(),
        media_type='text/event-stream',
        headers=SSE_HEADERS
    )
