"""
紫微斗数模块
采用分层架构设计，参考 mingpan 的服务结构

目录结构：
├── calculators/     # 计算器
│   ├── minggong.py  # 命宫计算
│   ├── xingxiu.py   # 星曜计算
│   └── sihua.py     # 四化/大运/流年计算
├── analyzers/       # 分析器
│   └── mingpan.py   # 命盘分析
├── data/            # 数据
│   └── stars.py     # 星曜数据库
├── types.py         # 类型定义
├── service.py       # 服务入口
└── __init__.py      # 模块导出
"""

# 向后兼容
from .ziwei import analyze_ziwei_stars, get_maxing, get_lushen, get_guiren

# 新分层架构导入
from .service import ZiweiService, ziwei_paipan
from .types import WuXingJu, GongInfo, StarInfo, ZiweiPan, ZiweiResult

# 计算器
from .calculators.minggong import MingGongCalculator
from .calculators.xingxiu import XingXiuCalculator
from .calculators.sihua import (
    SihuaCalculator,
    SihuaInfo,
    DayunCalculator as ZiweiDayunCalculator,
    LiunianCalculator as ZiweiLiunianCalculator,
    get_sihua,
    calculate_dayun as ziwei_calculate_dayun,
    calculate_liunian as ziwei_calculate_liunian,
)

# 分析器
from .analyzers.mingpan import MingPanAnalyzer

# 数据
from .data.stars import (
    MAIN_STARS,
    LUCKY_STARS,
    EVIL_STARS,
    SIHUA_STARS,
    TWELVE_PALACES,
    get_star_info,
    get_star_nature,
    get_palace_meaning,
    analyze_star_combination,
)

__all__ = [
    # 向后兼容
    'analyze_ziwei_stars', 'get_maxing', 'get_lushen', 'get_guiren',
    # 服务
    'ZiweiService',
    'ziwei_paipan',
    # 类型
    'WuXingJu', 'GongInfo', 'StarInfo', 'ZiweiPan', 'ZiweiResult',
    # 计算器
    'MingGongCalculator',
    'XingXiuCalculator',
    'SihuaCalculator',
    'SihuaInfo',
    'ZiweiDayunCalculator',
    'ZiweiLiunianCalculator',
    'get_sihua',
    'ziwei_calculate_dayun',
    'ziwei_calculate_liunian',
    # 分析器
    'MingPanAnalyzer',
    # 数据
    'MAIN_STARS',
    'LUCKY_STARS',
    'EVIL_STARS',
    'SIHUA_STARS',
    'TWELVE_PALACES',
    'get_star_info',
    'get_star_nature',
    'get_palace_meaning',
    'analyze_star_combination',
]
