"""
小六壬模块
基于月日时计算六神落宫
"""
# 从同级目录的 xiaoliu.py 导入 XiaoLiuRenFactory
import sys
from pathlib import Path

# 导入同目录下的 xiaoliu.py 模块
_parent = Path(__file__).parent.parent
_xiaoliu_file = _parent / "xiaoliu.py"
if _xiaoliu_file.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("xiaoliu_factory", _xiaoliu_file)
    _xiaoliu_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_xiaoliu_module)
    XiaoLiuRenFactory = _xiaoliu_module.XiaoLiuRenFactory
    calculate_xiaoliu = _xiaoliu_module.calculate_xiaoliu
    LIU_GODS = _xiaoliu_module.LIU_GODS
    LIU_GOD_MEANINGS = _xiaoliu_module.LIU_GOD_MEANINGS
else:
    XiaoLiuRenFactory = None
    calculate_xiaoliu = None
    LIU_GODS = None
    LIU_GOD_MEANINGS = None

from .types import XiaoliuResult, LiuGodInfo

__all__ = [
    'XiaoLiuRenFactory',
    'calculate_xiaoliu',
    'LIU_GODS',
    'LIU_GOD_MEANINGS',
    'XiaoliuResult',
    'LiuGodInfo',
]
