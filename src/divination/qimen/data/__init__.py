"""
奇门遁甲/六壬数据模块

包含：
- xunkong: 六甲旬空数据
- sanchuan: 大六壬三传数据
"""
from .xunkong import (
    TIAN_GAN,
    DI_ZHI,
    JIA_ZI_60,
    XUN_KONG_TABLE,
    GAN_ZHI_XUN_KONG,
    get_xun_kong,
    get_xun_shou,
    is_kong,
    get_jia_zi_index,
    get_gan_zhi_by_index,
    DI_ZHI_CHONG,
    DI_ZHI_HE,
    DI_ZHI_SAN_HE,
    DI_ZHI_SAN_HUI,
)

from .sanchuan import (
    SHI_CHEN,
    SAN_CHUAN_TABLE,
    get_san_chuan,
    get_san_chuan_by_gan_zhi,
    format_san_chuan,
)

__all__ = [
    # 天干地支
    'TIAN_GAN',
    'DI_ZHI',
    'JIA_ZI_60',
    # 旬空
    'XUN_KONG_TABLE',
    'GAN_ZHI_XUN_KONG',
    'get_xun_kong',
    'get_xun_shou',
    'is_kong',
    'get_jia_zi_index',
    'get_gan_zhi_by_index',
    # 地支关系
    'DI_ZHI_CHONG',
    'DI_ZHI_HE',
    'DI_ZHI_SAN_HE',
    'DI_ZHI_SAN_HUI',
    # 三传
    'SHI_CHEN',
    'SAN_CHUAN_TABLE',
    'get_san_chuan',
    'get_san_chuan_by_gan_zhi',
    'format_san_chuan',
]
