"""
路由模块统一入口

所有 API 路由从此模块导出，便于统一管理和版本控制。

路由前缀规范：
- /api/v1/xxx 或 /v1/api/xxx - 新版本 API（推荐）
- /api/xxx - 旧版本 API（兼容层，将逐步废弃）

注意：部分路由器自带 /api/ 前缀（如 bazi, qimen 等），
这些路由的 v1 版本使用 /v1/api/xxx 格式以避免重复。
"""

# 导入各功能模块路由
from .analytics import router as analytics_router
from .bazi import router as bazi_router
from .chatgpt import router as chatgpt_router
from .chouqian import router as chouqian_router
from .daliuren import router as daliuren_router
from .fortune import router as fortune_router
from .hehun import router as hehun_router
from .life_kline import router as life_kline_router
from .liuyao import router as liuyao_router
from .logs import router as logs_router
from .monitoring_router import router as monitoring_router
from .plum_flower import router as plum_flower_router
from .prompts import router as prompts_router
from .qimen import router as qimen_router
from .rag import router as rag_router
from .tarot import router as tarot_router
from .user import router as user_router
from .zhuge import router as zhuge_router
from .ziwei import router as ziwei_router
from .zodiac import router as zodiac_router


__all__ = [
    # 路由器
    'analytics_router',
    'chouqian_router',
    'daliuren_router',
    'fortune_router',
    'hehun_router',
    'life_kline_router',
    'logs_router',
    'monitoring_router',
    'plum_flower_router',
    'prompts_router',
    'qimen_router',
    'rag_router',
    'tarot_router',
    'zhuge_router',
    'ziwei_router',
    'zodiac_router',
    'chatgpt_router',
    'user_router',
    'liuyao_router',
    'bazi_router',
]
