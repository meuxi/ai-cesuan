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
    from src.chatgpt_router import router as chatgpt_router
    from src.user_router import router as user_router
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

# ========== CORS 配置修复2：解决 credentials 与 * 冲突 ==========
is_vercel = os.getenv("VERCEL") == "1"
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")

if is_vercel:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
    allow_credentials = bool(allowed_origins)  # 有具体源才允许凭证
    if not allowed_origins:
        allowed_origins = []
        _logger.warning("⚠️  生产环境未配置ALLOWED_ORIGINS，CORS限制所有跨域请求")
    else:
        _logger.info(f"生产环境CORS允许的源: {allowed_origins}")
else:
    allowed_origins = ["*"]
    allow_credentials = False  # 开发环境通配符时关闭凭证
    _logger.info("开发环境CORS设置为允许所有源（关闭凭证）")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 路由注册 ==========
app.include_router(chatgpt_router, prefix="/api")
app.include_router(user_router, prefix="/api")
_logger.info("API路由已注册")

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
