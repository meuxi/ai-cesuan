import logging
import uvicorn
import sys
import os

# ========== 容错修复1：处理 src 模块导入失败 ==========
try:
    from src.app import app as fastapi_app
    from src.config import settings
except ImportError as e:
    raise ImportError(f"Failed to import src modules: {e}. Check if src/app.py and src/config.py exist.") from e

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    level=logging.INFO
)
_logger = logging.getLogger(__name__)

application = fastapi_app

# ========== Vercel 兼容性逻辑 ==========
if os.getenv("VERCEL") == "1":
    _logger.info("Running on Vercel platform")
    try:
        # ========== 容错修复2：兼容 Python < 3.8 ==========
        if sys.version_info < (3, 8):
            import importlib_metadata as importlib_metadata
        else:
            import importlib.metadata as importlib_metadata
            
        import mangum
        
        mangum_version = importlib_metadata.version('mangum')
        _logger.info(f"Mangum version: {mangum_version}")
        
        application = mangum.Mangum(fastapi_app)
        _logger.info("Mangum handler created and set as application")
        
    except ImportError as e:
        _logger.error(f"Missing required packages: {e}. Install with: pip install mangum importlib-metadata")
        raise
    except Exception as e:
        _logger.error(f"Error creating Mangum handler: {str(e)}", exc_info=True)
        raise
else:
    # ========== 容错修复3：兼容 Pydantic v1/v2 ==========
    try:
        # Pydantic v2
        settings_json = settings.model_dump_json(indent=2)
    except AttributeError:
        # Pydantic v1 fallback
        from pydantic import json
        settings_json = json.pydantic_encoder(settings.dict(), indent=2)
    _logger.info(f"settings: {settings_json}")

# 本地开发服务器
if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8000)
