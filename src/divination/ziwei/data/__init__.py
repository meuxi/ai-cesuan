"""
紫微斗数数据模块
"""
from .stars import (
    StarCategory,
    StarNature,
    StarInfo,
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
    'StarCategory',
    'StarNature',
    'StarInfo',
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
