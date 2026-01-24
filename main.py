import logging
import os
import uvicorn

from src.app import app
from src.config import settings

logging.basicConfig(
    format="%(asctime)s: %(levelname)s: %(name)s: %(message)s",
    level=logging.INFO
)
_logger = logging.getLogger(__name__)

_logger.info(f"settings: {settings.model_dump_json(indent=2)}")


if __name__ == "__main__":
    # 生产环境建议: workers = CPU核心数 * 2 + 1
    # 开发环境使用单进程便于调试
    workers = int(os.getenv("UVICORN_WORKERS", 1))
    
    if workers > 1:
        # 多进程模式 (生产环境)
        uvicorn.run(
            "src.app:app",
            host="0.0.0.0",
            port=8000,
            workers=workers,
            log_level="info"
        )
    else:
        # 单进程模式 (开发环境，支持热重载)
        uvicorn.run(app, host="0.0.0.0", port=8000)
