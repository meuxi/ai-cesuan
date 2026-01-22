"""
六爻模块
采用分层架构设计

目录结构：
├── core/            # 核心计算
│   └── najia.py     # 纳甲计算
├── data/            # 数据文件
│   ├── eight_palaces.py   # 八宫数据
│   └── hexagram_texts.py  # 卦辞爻辞
├── advanced_analysis.py   # 高级分析
├── service.py       # 统一服务入口 ★
├── types.py         # 类型定义
└── __init__.py      # 模块导出
"""

# 从增强模块导入（兼容旧代码）
from ..liuyao_enhanced import (
    FushenCalculator,
    WangshuaiCalculator,
    JintuishenCalculator,
    LiuyaoEnhanced,
    enhance_liuyao_analysis
)

# 从高级分析模块导入
from .advanced_analysis import LiuyaoAdvancedAnalyzer, calculate_time_recommendations

# 从统一服务导入
from .service import (
    LiuyaoService,
    liuyao_service,
    calculate_hexagram,
    full_analysis,
    coin_cast,
    number_cast,
    time_cast,
)

__all__ = [
    # 统一服务（推荐使用）
    'LiuyaoService',
    'liuyao_service',
    'calculate_hexagram',
    'full_analysis',
    'coin_cast',
    'number_cast',
    'time_cast',
    
    # 高级分析
    'LiuyaoAdvancedAnalyzer',
    'calculate_time_recommendations',
    
    # 兼容旧接口
    'FushenCalculator',
    'WangshuaiCalculator',
    'JintuishenCalculator',
    'LiuyaoEnhanced',
    'enhance_liuyao_analysis',
]
