"""
八字（四柱）模块
采用分层架构设计，参考 mingpan 的服务结构

目录结构：
├── calculators/     # 计算器
│   ├── ganzhi.py    # 干支计算
│   ├── nayin.py     # 纳音计算
│   └── lunar.py     # 农历转换
├── analyzers/       # 分析器
│   ├── shishen.py   # 十神分析
│   └── wuxing.py    # 五行分析
├── data/            # 数据文件
├── types.py         # 类型定义
├── service.py       # 服务入口
└── __init__.py      # 模块导出
"""

# 向后兼容：从原位置导入
from .ganzhi import GanZhi
from .lunar import solar_to_lunar, lunar_to_solar
from .shishen import TenGodsAnalyzer, analyze_ten_gods
from .paipan import BaziPaipan

# 新分层架构导入
from .service import BaziService, bazi_calculate, bazi_full_analysis
from .types import (
    PillarType, WuXing, YinYang, TenGod,
    Pillar, HiddenStem, BaziChart,
    TenGodInfo, TenGodDistribution, TenGodAnalysis, WuXingAnalysis
)

__all__ = [
    # 计算器
    'GanZhi',
    'solar_to_lunar',
    'lunar_to_solar',
    # 分析器
    'TenGodsAnalyzer',
    'analyze_ten_gods',
    # 排盘
    'BaziPaipan',
    # 服务
    'BaziService',
    'bazi_calculate',
    'bazi_full_analysis',
    # 类型
    'PillarType', 'WuXing', 'YinYang', 'TenGod',
    'Pillar', 'HiddenStem', 'BaziChart',
    'TenGodInfo', 'TenGodDistribution', 'TenGodAnalysis', 'WuXingAnalysis',
]
