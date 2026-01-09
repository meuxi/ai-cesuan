import logging
import uvicorn
import sys
import os

# 首先配置日志
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 定义全局变量
fastapi_app = None
settings = None
handler = None
application = None

# ========== 尝试导入应用模块 ==========
logger.info("开始导入应用模块...")

try:
    # 尝试从 src 模块导入
    from src.app import app as fastapi_app
    from src.config import settings
    logger.info("✓ 成功从 src 模块导入应用和配置")
except ImportError as e:
    logger.warning(f"从 src 模块导入失败: {e}")
    
    try:
        # 尝试从当前目录导入
        from app import app as fastapi_app
        from config import settings
        logger.info("✓ 成功从当前目录导入应用和配置")
    except ImportError as e2:
        logger.error(f"从当前目录导入也失败: {e2}")
        
        # 创建最小的 FastAPI 应用作为后备
        from fastapi import FastAPI
        fastapi_app = FastAPI(title="后备应用", version="1.0.0")
        
        @fastapi_app.get("/")
        async def root():
            return {"message": "应用正在运行（后备模式）"}
            
        @fastapi_app.get("/health")
        async def health():
            return {"status": "ok"}
        
        @fastapi_app.get("/api/health")
        async def api_health():
            return {"status": "API服务正常"}
        
        # 创建虚拟的 settings 对象
        class Settings:
            debug = True
            allowed_origins = []
            title = "后备配置"
        
        settings = Settings()
        logger.warning("⚠️ 创建了后备的 FastAPI 应用")

# ========== 确保 app 变量存在 ==========
if fastapi_app is None:
    from fastapi import FastAPI
    fastapi_app = FastAPI(title="默认应用", version="1.0.0")
    logger.error("应用导入完全失败，创建了默认应用")

# 设置基础变量
app = fastapi_app  # Vercel 需要的变量名

# ========== Vercel 环境处理 ==========
if os.getenv("VERCEL") == "1":
    logger.info("🚀 运行在 Vercel 平台")
    logger.info(f"Python 版本: {sys.version}")
    logger.info(f"当前目录: {os.getcwd()}")
    
    try:
        # 导入 mangum 适配器
        import mangum
        
        # 创建 Mangum handler - 这是 Vercel 需要的
        handler = mangum.Mangum(app, lifespan="auto")
        logger.info("✅ Mangum handler 已创建")
        
        # 设置 application 变量（向后兼容）
        application = handler
        
        logger.info(f"handler 类型: {type(handler)}")
        
    except ImportError as e:
        logger.error(f"❌ 缺少 mangum 包: {e}")
        logger.error("请添加 'mangum' 到 requirements.txt")
        
        # 如果没有 mangum，使用 FastAPI app 作为备选
        handler = app
        application = app
        logger.warning("⚠️ 使用 FastAPI app 作为 handler")
        
    except Exception as e:
        logger.error(f"❌ 创建 Mangum handler 时出错: {e}")
        handler = app
        application = app
        logger.warning("⚠️ 使用 FastAPI app 作为 handler（出错后备）")
        
else:
    # 本地开发环境
    logger.info("💻 运行在本地开发环境")
    
    # 设置变量
    handler = app
    application = app
    
    # 显示配置信息
    try:
        if hasattr(settings, 'model_dump_json'):
            settings_json = settings.model_dump_json(indent=2)
        elif hasattr(settings, 'dict'):
            settings_json = str(settings.dict())
        else:
            settings_json = str(settings)
        logger.info(f"应用配置: {settings_json}")
    except Exception as e:
        logger.warning(f"无法显示配置: {e}")

# ========== 最终导出确认 ==========
logger.info(f"✅ 导出变量 - app: {type(app).__name__}, handler: {type(handler).__name__}")

# ========== 本地开发服务器 ==========
if __name__ == "__main__":
    logger.info(f"启动本地开发服务器 (VERCEL={os.getenv('VERCEL', '0')})")
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        log_level="info",
        reload=os.getenv("VERCEL") != "1"  # 本地开发时启用热重载
    )
