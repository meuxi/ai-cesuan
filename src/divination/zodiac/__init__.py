"""
星座模块
包含十二星座查询、月亮星座、上升星座计算等功能
"""

from .calculator import (
    get_sun_sign,
    get_moon_sign,
    get_rising_sign,
    get_zodiac_info,
    get_all_zodiacs,
)
from .fortune import (
    get_daily_zodiac_fortune,
    get_weekly_zodiac_fortune,
    get_monthly_zodiac_fortune,
)
from .compatibility import (
    get_zodiac_compatibility,
)

__all__ = [
    'get_sun_sign',
    'get_moon_sign',
    'get_rising_sign',
    'get_zodiac_info',
    'get_all_zodiacs',
    'get_daily_zodiac_fortune',
    'get_weekly_zodiac_fortune',
    'get_monthly_zodiac_fortune',
    'get_zodiac_compatibility',
]
