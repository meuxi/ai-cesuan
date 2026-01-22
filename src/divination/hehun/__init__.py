"""
合婚模块
基于九宫五行分析男女婚配
"""
from .hehun import analyze_hehun, get_male_gong, get_female_gong, get_year_ganzhi
from .types import HehunResult

__all__ = [
    'analyze_hehun',
    'get_male_gong',
    'get_female_gong',
    'get_year_ganzhi',
    'HehunResult',
]
