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
    from fastapi.responses import Response
    from mangum import Mangum

    # 将 FastAPI 应用转换为 AWS Lambda handler
    handler = Mangum(app)
else:
    _logger.info(f"settings: {settings.model_dump_json(indent=2)}")

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
