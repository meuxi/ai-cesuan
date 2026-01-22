"""
奇门遁甲模块
采用分层架构设计，参考 mingpan 的服务结构

目录结构：
├── calculators/     # 计算器
│   ├── jushu.py     # 局数计算
│   ├── jiugong.py   # 九宫计算
│   └── sanqi.py     # 三奇六仪计算
├── analyzers/       # 分析器
│   ├── geju.py      # 格局分析
│   └── shensha.py   # 神煞分析
├── types.py         # 类型定义
├── service.py       # 服务入口
├── qimen.py         # 原有排盘类（向后兼容）
└── __init__.py      # 模块导出
"""

# 向后兼容：从原位置导入
from .qimen import QimenPaipan

# 新分层架构导入
from .service import QimenService, qimen_paipan
from .types import (
    PanStyle, PanType, GongInfo, GeJuInfo, 
    XunShouInfo, QimenPan, QimenResult
)

# 计算器
from .calculators.jushu import JuShuCalculator
from .calculators.jiugong import JiuGongCalculator
from .calculators.sanqi import SanQiLiuYiCalculator

# 分析器
from .analyzers.geju import GeJuAnalyzer
from .analyzers.shensha import ShenShaAnalyzer

# 用神系统
from .yongshen import (
    QimenYongShen,
    qimen_yongshen,
    get_shilei_list,
    analyze_yongshen,
    SHILEI_YONGSHEN_MAP,
    GONG_FANGWEI,
)

__all__ = [
    # 向后兼容
    'QimenPaipan',
    # 服务
    'QimenService',
    'qimen_paipan',
    # 类型
    'PanStyle', 'PanType', 'GongInfo', 'GeJuInfo',
    'XunShouInfo', 'QimenPan', 'QimenResult',
    # 计算器
    'JuShuCalculator',
    'JiuGongCalculator',
    'SanQiLiuYiCalculator',
    # 分析器
    'GeJuAnalyzer',
    'ShenShaAnalyzer',
    # 用神系统
    'QimenYongShen',
    'qimen_yongshen',
    'get_shilei_list',
    'analyze_yongshen',
    'SHILEI_YONGSHEN_MAP',
    'GONG_FANGWEI',
]
