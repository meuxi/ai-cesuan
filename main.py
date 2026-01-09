import logging
import uvicorn
import sys
import os

from src.app import app
from src.config import settings

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    level=logging.INFO
)
_logger = logging.getLogger(__name__)

# Vercel 兼容性：在 Vercel 环境下使用 serverless 导出
if os.getenv("VERCEL") == "1":
    _logger.info("Running on Vercel platform")
    try:
        # 确保Mangum已安装
        import importlib.metadata  # 新增导入
        import mangum
        
        # 使用正确的方式获取Mangum版本
        mangum_version = importlib.metadata.version('mangum')
        _logger.info(f"Mangum version: {mangum_version}")
        
        handler = mangum.Mangum(app)
    except ImportError:
        _logger.error("Mangum package not found. Please install with: pip install mangum")
        raise
    except Exception as e:
        _logger.error(f"Error creating Mangum handler: {str(e)}", exc_info=True)
        raise
else:
    _logger.info(f"settings: {settings.model_dump_json(indent=2)}")

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
