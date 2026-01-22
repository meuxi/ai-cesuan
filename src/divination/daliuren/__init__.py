"""
大六壬模块
采用分层架构设计，参考 mingpan 的服务结构

目录结构：
├── calculators/     # 计算器
│   ├── tianpan.py   # 天地盘计算
│   ├── sike.py      # 四课计算
│   └── sanchuan.py  # 三传计算
├── analyzers/       # 分析器
│   ├── keti.py      # 课体分析
│   └── shenjiang.py # 神将分析
├── types.py         # 类型定义
├── service.py       # 服务入口
└── __init__.py      # 模块导出
"""

# 向后兼容
from .daliuren import DaliurenPaipan

# 新分层架构导入
from .service import DaliurenService, daliuren_paipan
from .types import KeInfo, SanChuanInfo, TianJiangInfo, DaliurenPan, DaliurenResult

# 计算器
from .calculators.tianpan import TianPanCalculator
from .calculators.sike import SiKeCalculator
from .calculators.sanchuan import SanChuanCalculator

# 分析器
from .analyzers.keti import KetiAnalyzer
from .analyzers.shenjiang import ShenJiangAnalyzer

__all__ = [
    # 向后兼容
    'DaliurenPaipan',
    # 服务
    'DaliurenService',
    'daliuren_paipan',
    # 类型
    'KeInfo', 'SanChuanInfo', 'TianJiangInfo', 'DaliurenPan', 'DaliurenResult',
    # 计算器
    'TianPanCalculator',
    'SiKeCalculator',
    'SanChuanCalculator',
    # 分析器
    'KetiAnalyzer',
    'ShenJiangAnalyzer',
]
