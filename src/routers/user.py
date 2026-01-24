import jwt
import httpx
import datetime
import logging
import secrets
import hashlib
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from src.config import settings
from src.models import OauthBody, SettingsInfo, User
from src.user import get_user
from src.cache import CacheClientFactory

router = APIRouter()
_logger = logging.getLogger(__name__)

GITHUB_URL = "https://github.com/login/oauth/authorize?" \
    f"client_id={settings.github_client_id}" \
    "&scope=user:email"
# 安全改进：不在URL中暴露client_secret，改为POST请求体发送
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"

# OAuth State 配置
OAUTH_STATE_TTL = 600  # state 有效期 10 分钟
OAUTH_STATE_PREFIX = "oauth_state:"  # 缓存 key 前缀


def _get_cache_client():
    """获取缓存客户端"""
    return CacheClientFactory.get_client()


def _generate_oauth_state(redirect_url: str) -> str:
    """生成 OAuth state 参数（用于 CSRF 防护），使用缓存存储支持多实例部署"""
    # 生成随机 state
    state = secrets.token_urlsafe(32)
    state_hash = hashlib.sha256(state.encode()).hexdigest()
    cache_key = f"{OAUTH_STATE_PREFIX}{state_hash}"
    
    # 存储到缓存（自动过期）
    cache_client = _get_cache_client()
    cache_client.store_token(cache_key, redirect_url, OAUTH_STATE_TTL)
    
    return state


def _verify_oauth_state(state: str, redirect_url: str) -> bool:
    """验证 OAuth state 参数"""
    if not state:
        return False
    
    state_hash = hashlib.sha256(state.encode()).hexdigest()
    cache_key = f"{OAUTH_STATE_PREFIX}{state_hash}"
    
    cache_client = _get_cache_client()
    stored_redirect = cache_client.get_token(cache_key)
    
    if not stored_redirect:
        _logger.warning(f"[OAuth] state 不存在或已被使用: {state[:8]}...")
        return False
    
    # 使用后立即删除（一次性使用）
    cache_client.delete_token(cache_key)
    
    if stored_redirect != redirect_url:
        _logger.warning(f"[OAuth] redirect_url 不匹配: 期望 {stored_redirect}, 实际 {redirect_url}")
        return False
    
    return True


@router.get("/v1/settings", tags=["User"])
async def info(user: Optional[User] = Depends(get_user)):
    return SettingsInfo(
        login_type=user.login_type if user else "",
        user_name=user.user_name if user else "",
        ad_client=settings.ad_client,
        ad_slot=settings.ad_slot,
        rate_limit=settings.get_human_rate_limit(),
        user_rate_limit=settings.get_human_user_rate_limit(),
        enable_login=bool(settings.github_client_id),
        enable_rate_limit=settings.enable_rate_limit,
        default_api_base=settings.default_api_base,
        default_model=settings.default_model,
        purchase_url=settings.purchase_url
    )


@router.get("/v1/login", tags=["User"])
async def login(login_type: str, redirect_url: str):
    """
    获取 OAuth 登录 URL
    
    Returns:
        str: 带有 state 参数的 OAuth 授权 URL（用于 CSRF 防护）
    """
    if login_type == "github":
        # 生成 state 参数用于 CSRF 防护
        state = _generate_oauth_state(redirect_url)
        return f"{GITHUB_URL}&redirect_uri={redirect_url}&state={state}"
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Login type not supported"
    )


@router.post("/v1/oauth", tags=["User"])
async def oauth(oauth_body: OauthBody):
    """
    处理 OAuth 回调，验证 state 参数防止 CSRF 攻击
    
    Args:
        oauth_body: 包含 code、state、redirect_url 的请求体
    
    Returns:
        str: JWT token
    
    Raises:
        HTTPException: state 验证失败或登录类型不支持
    """
    if oauth_body.login_type == "github" and oauth_body.code:
        # 验证 state 参数（CSRF 防护）
        if oauth_body.state and oauth_body.redirect_url:
            if not _verify_oauth_state(oauth_body.state, oauth_body.redirect_url):
                _logger.warning(f"[OAuth] CSRF 检测：state 验证失败")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="OAuth state 验证失败，请重新登录"
                )
        else:
            # 兼容旧版本客户端（无 state 参数），记录警告
            _logger.warning("[OAuth] 请求未包含 state 参数，建议前端升级以支持 CSRF 防护")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 安全改进：使用POST请求体发送敏感信息，而非URL参数
                resp = await client.post(
                    GITHUB_TOKEN_URL,
                    data={
                        "client_id": settings.github_client_id,
                        "client_secret": settings.github_client_secret,
                        "code": oauth_body.code
                    },
                    headers={"Accept": "application/json"}
                )
                resp_data = resp.json()
                
                if "error" in resp_data:
                    _logger.error(f"[OAuth] GitHub token 获取失败: {resp_data}")
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"GitHub 授权失败: {resp_data.get('error_description', resp_data.get('error'))}"
                    )
                
                access_token = resp_data.get('access_token')
                if not access_token:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="GitHub 授权失败：未获取到 access_token"
                    )
                
                res = await client.get(
                    GITHUB_USER_URL,
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json"
                    }
                )
                user_data = res.json()
                
        except httpx.RequestError as e:
            _logger.error(f"[OAuth] 网络请求失败: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub 服务暂时不可用，请稍后重试"
            )
            
        user_name = user_data.get('login')
        if not user_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无法获取 GitHub 用户信息"
            )
        
        return jwt.encode(
            User(
                login_type=oauth_body.login_type,
                user_name=user_name,
                expire_at=(
                    datetime.datetime.now() +
                    datetime.timedelta(days=30)
                ).timestamp(),
            ).model_dump(),
            settings.jwt_secret, algorithm="HS256"
        )
    raise HTTPException(status_code=400, detail="Login type not supported")
