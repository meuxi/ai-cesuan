import os
import uuid
import logging
from pathlib import Path

from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ========== 容错修复1：处理 src 模块导入失败 ==========
try:
    from src.limiter import get_real_ipaddr
    # 从统一入口导入所有路由
    from src.routers import (
        chatgpt_router,
        user_router,
        liuyao_router,
        bazi_router,
        chouqian_router,
        zhuge_router,
        qimen_router,
        daliuren_router,
        fortune_router,
        zodiac_router,
        tarot_router,
        prompts_router,
        life_kline_router,
        analytics_router,
        rag_router,
        logs_router,
        ziwei_router,
        hehun_router,
        plum_flower_router,
        monitoring_router,
    )
except ImportError as e:
    raise ImportError(f"Failed to import src modules: {e}. Check src module files exist.") from e

_logger = logging.getLogger(__name__)

# ========== 应用初始化 ==========
app = FastAPI(title="Chatgpt Divination API")

_logger.info(f"应用启动，环境 VERCEL={os.getenv('VERCEL')}")

# ========== 中间件1：请求ID生成（关联日志上下文） ==========
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id  # 透传给前端
    return response

# ========== CORS 配置修复2：安全的CORS策略 ==========
is_vercel = os.getenv("VERCEL") == "1"
is_development = os.getenv("ENVIRONMENT", "development") == "development"
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")

# 默认安全的允许源列表
DEFAULT_ALLOWED_ORIGINS = [
    "https://*.vercel.app",  # Vercel 预览部署
]

if is_development:
    # 开发环境：允许所有源，便于本地调试
    allowed_origins = ["*"]
    allow_credentials = False
    _logger.info("开发环境CORS设置为允许所有源（仅用于调试）")
elif is_vercel:
    # Vercel 生产环境：优先使用环境变量配置
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
    if allowed_origins:
        allow_credentials = True
        _logger.info(f"生产环境CORS允许的源: {allowed_origins}")
    else:
        # 未配置 ALLOWED_ORIGINS 时，使用严格的默认策略
        # 获取 Vercel 自动注入的域名
        vercel_url = os.getenv("VERCEL_URL", "")
        vercel_project_domain = os.getenv("VERCEL_PROJECT_PRODUCTION_URL", "")
        
        allowed_origins = []
        if vercel_url:
            allowed_origins.append(f"https://{vercel_url}")
        if vercel_project_domain:
            allowed_origins.append(f"https://{vercel_project_domain}")
        
        # 如果仍为空，使用通配符但记录警告
        if not allowed_origins:
            allowed_origins = ["*"]
            allow_credentials = False
            _logger.warning(
                "⚠️ 生产环境未配置 ALLOWED_ORIGINS，默认允许所有源。"
                "建议设置环境变量 ALLOWED_ORIGINS 限制跨域请求来源。"
            )
        else:
            allow_credentials = True
            _logger.info(f"Vercel环境自动检测CORS允许的源: {allowed_origins}")
else:
    # 其他生产环境：必须配置 ALLOWED_ORIGINS
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
    if not allowed_origins:
        _logger.error("❌ 生产环境必须配置 ALLOWED_ORIGINS 环境变量！")
        allowed_origins = []  # 拒绝所有跨域请求
        allow_credentials = False
    else:
        allow_credentials = True
        _logger.info(f"生产环境CORS允许的源: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 路由注册 ==========
# 
# API 版本说明：
# - /api/v1/xxx - 新版本 API（推荐使用）
# - /api/xxx - 旧版本兼容路径（将逐步废弃）
#
# 注意：部分路由器自带前缀，注册时需避免重复

# ========== API v1 路由（推荐） ==========
# 
# 注意：部分路由器自带 /api/ 前缀，这些路由器使用 /v1 前缀而非 /api/v1
# 以避免路径变成 /api/v1/api/xxx 的重复问题
#
# 核心功能
app.include_router(chatgpt_router, prefix="/api/v1", tags=["AI对话"])
app.include_router(user_router, prefix="/api/v1", tags=["用户"])

# 占卜模块 - 不带 /api 前缀的路由器
app.include_router(liuyao_router, prefix="/api/v1/liuyao", tags=["六爻"])
app.include_router(ziwei_router, prefix="/api/v1", tags=["紫微斗数"])  # 自带 /ziwei
app.include_router(tarot_router, prefix="/api/v1", tags=["塔罗牌"])  # 自带 /tarot
app.include_router(chouqian_router, prefix="/api/v1", tags=["抽签"])  # 自带 /chouqian
app.include_router(zhuge_router, prefix="/api/v1", tags=["诸葛神算"])  # 自带 /zhuge
app.include_router(hehun_router, prefix="/api/v1", tags=["合婚"])  # 自带 /hehun

# 占卜模块 - 自带 /api/ 前缀的路由器，使用 /v1 前缀避免重复
app.include_router(bazi_router, prefix="/v1")  # 自带 /api/bazi -> /v1/api/bazi
app.include_router(qimen_router, prefix="/v1")  # 自带 /api/qimen -> /v1/api/qimen
app.include_router(daliuren_router, prefix="/v1")  # 自带 /api/daliuren -> /v1/api/daliuren
app.include_router(plum_flower_router, prefix="/v1")  # 自带 /api/plum-flower -> /v1/api/plum-flower
app.include_router(zodiac_router, prefix="/v1")  # 自带 /api/zodiac -> /v1/api/zodiac

# 运势相关
app.include_router(fortune_router, prefix="/api/v1", tags=["运势"])  # 自带 /fortune
app.include_router(life_kline_router, prefix="/api/v1", tags=["人生K线图"])  # 自带 /life-kline

# 系统功能
app.include_router(prompts_router, prefix="/api/v1", tags=["提示词模板"])  # 自带 /prompts
app.include_router(analytics_router, prefix="/api/v1", tags=["用量统计"])  # 自带 /analytics
app.include_router(rag_router, prefix="/api/v1", tags=["RAG知识库"])  # 自带 /rag
app.include_router(logs_router, prefix="/api/v1", tags=["操作日志"])  # 自带 /logs
app.include_router(monitoring_router, prefix="/v1")  # 自带 /api/monitor -> /v1/api/monitor

# ========== 旧版本兼容层（保持向后兼容） ==========
# 这些路由保持原有路径，确保现有前端不受影响
app.include_router(chatgpt_router, prefix="/api", include_in_schema=False)
app.include_router(user_router, prefix="/api", include_in_schema=False)
app.include_router(liuyao_router, prefix="/api/liuyao", include_in_schema=False)
app.include_router(bazi_router, include_in_schema=False)  # 自带 /api/bazi
app.include_router(chouqian_router, prefix="/api", include_in_schema=False)
app.include_router(zhuge_router, prefix="/api", include_in_schema=False)
app.include_router(qimen_router, include_in_schema=False)  # 自带 /api/qimen
app.include_router(daliuren_router, include_in_schema=False)  # 自带 /api/daliuren
app.include_router(fortune_router, prefix="/api", include_in_schema=False)
app.include_router(zodiac_router, include_in_schema=False)  # 自带 /api/zodiac
app.include_router(tarot_router, prefix="/api", include_in_schema=False)
app.include_router(prompts_router, prefix="/api", include_in_schema=False)
app.include_router(life_kline_router, prefix="/api", include_in_schema=False)
app.include_router(analytics_router, prefix="/api", include_in_schema=False)
app.include_router(rag_router, prefix="/api", include_in_schema=False)
app.include_router(logs_router, prefix="/api", include_in_schema=False)
app.include_router(ziwei_router, prefix="/api", include_in_schema=False)
app.include_router(hehun_router, prefix="/api", include_in_schema=False)
app.include_router(plum_flower_router, include_in_schema=False)  # 自带 /api/plum-flower
app.include_router(monitoring_router, include_in_schema=False)  # 自带 /api/monitor

_logger.info("API路由已注册：v1版本路径 + 旧版本兼容层")

# ========== 静态前端文件服务修复3：绝对路径 + 容错 ==========
frontend_dist_path = Path(__file__).parent / "dist"  # 基于当前文件的绝对路径
if frontend_dist_path.is_dir():
    _logger.info(f"检测到前端目录 '{frontend_dist_path}'，启用静态文件服务")
    
    @app.get("/", include_in_schema=False)
    async def serve_index(request: Request):
        client_ip = get_real_ipaddr(request)
        _logger.debug(f"[Req-{request.state.request_id}] 根路径请求来自 IP: {client_ip}")
        return FileResponse(
            frontend_dist_path / "index.html",
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
        )
    
    app.mount("/", StaticFiles(directory=frontend_dist_path), name="static_frontend")
else:
    _logger.info(f"未找到前端目录 '{frontend_dist_path}'，仅提供API服务")
    
    @app.get("/", include_in_schema=False)
    async def root(request: Request):
        return {
            "message": "ChatGPT Divination API is running",
            "docs": "/docs",
            "request_id": request.state.request_id
        }

# ========== 健康检查端点 ==========
@app.get("/health", tags=["health"])
async def health_check(request: Request):
    """健康检查，用于部署和负载均衡器"""
    return {
        "status": "healthy",
        "request_id": request.state.request_id,
        "env": "vercel" if is_vercel else "local"
    }

# ========== 全局异常处理修复4：关联请求ID ==========
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", "unknown")
    client_ip = get_real_ipaddr(request)
    
    # 记录带请求上下文的错误日志
    _logger.error(
        f"[Req-{request_id}] [IP-{client_ip}] 未处理的异常: {type(exc).__name__}: {exc}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "request_id": request_id
        }
    )
    
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail, "request_id": request_id}
        )
    
    # 生产环境隐藏敏感信息
    error_content = {
        "error": "服务器内部错误，请稍后重试",
        "request_id": request_id  # 提供ID用于排查
    }
    if not is_vercel:
        error_content["debug"] = {
            "exception_type": type(exc).__name__,
            "exception_msg": str(exc)
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_content
    )

_logger.info("FastAPI应用初始化完成")
