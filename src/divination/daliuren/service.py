"""
大六壬服务入口
整合计算器和分析器，提供统一的大六壬服务接口
"""
from typing import Dict, List
from datetime import datetime

from .calculators.tianpan import TianPanCalculator
from .calculators.sike import SiKeCalculator
from .calculators.sanchuan import SanChuanCalculator
from .analyzers.keti import KetiAnalyzer
from .analyzers.shenjiang import ShenJiangAnalyzer


class DaliurenService:
    """大六壬服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.tianpan_calc = TianPanCalculator
        self.sike_calc = SiKeCalculator
        self.sanchuan_calc = SanChuanCalculator
        self.keti_analyzer = KetiAnalyzer
        self.shenjiang_analyzer = ShenJiangAnalyzer
    
    def paipan(self, year: int, month: int, day: int, hour: int,
               minute: int = 0) -> Dict:
        """排盘
        
        Args:
            year, month, day, hour, minute: 时间
            
        Returns:
            完整的大六壬盘信息
        """
        # 1. 获取干支
        year_gz = self._get_year_ganzhi(year)
        month_gz = self._get_month_ganzhi(year, month)
        day_gz = self._get_day_ganzhi(year, month, day)
        hour_gz = self._get_hour_ganzhi(day_gz, hour)
        
        ri_gan = day_gz[0]
        ri_zhi = day_gz[1]
        shi_zhi = hour_gz[1]
        
        # 2. 获取月将
        yue_jiang = self.tianpan_calc.get_yue_jiang(month, day)
        
        # 3. 计算天地盘
        pan_info = self.tianpan_calc.calculate(yue_jiang, shi_zhi)
        di_pan = pan_info['di_pan']
        tian_pan = pan_info['tian_pan']
        
        # 4. 计算四课
        si_ke = self.sike_calc.calculate(ri_gan, ri_zhi, tian_pan)
        
        # 5. 计算三传
        san_chuan = self.sanchuan_calc.calculate(si_ke, tian_pan, ri_gan, ri_zhi)
        
        # 6. 计算十二天将
        tian_jiang = self.shenjiang_analyzer.calculate(ri_gan, shi_zhi)
        
        # 7. 分析课体
        keti = self.keti_analyzer.analyze(si_ke, san_chuan)
        
        # 8. 分析天将
        jiang_analysis = self.shenjiang_analyzer.analyze(tian_jiang, san_chuan)
        
        return {
            'datetime': f"{year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}",
            'year_gz': year_gz,
            'month_gz': month_gz,
            'day_gz': day_gz,
            'hour_gz': hour_gz,
            'yue_jiang': yue_jiang,
            'di_pan': di_pan,
            'tian_pan': tian_pan,
            'si_ke': si_ke,
            'san_chuan': san_chuan,
            'tian_jiang': tian_jiang,
            'analysis': {
                'keti': keti,
                'jiang': jiang_analysis
            }
        }
    
    def _get_year_ganzhi(self, year: int) -> str:
        """获取年干支"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        idx = (year - 4) % 60
        return tiangan[idx % 10] + dizhi[idx % 12]
    
    def _get_month_ganzhi(self, year: int, month: int) -> str:
        """获取月干支"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        year_gan_idx = (year - 4) % 10
        base_gan_idx = (year_gan_idx % 5) * 2 + 2
        gan_idx = (base_gan_idx + month - 1) % 10
        zhi_idx = (month + 1) % 12
        return tiangan[gan_idx] + dizhi[zhi_idx]
    
    def _get_day_ganzhi(self, year: int, month: int, day: int) -> str:
        """获取日干支"""
        from datetime import date
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        base_date = date(1900, 1, 31)
        target_date = date(year, month, day)
        diff = (target_date - base_date).days
        idx = diff % 60
        return tiangan[idx % 10] + dizhi[idx % 12]
    
    def _get_hour_ganzhi(self, day_gz: str, hour: int) -> str:
        """获取时干支"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        day_gan_idx = tiangan.index(day_gz[0]) if day_gz[0] in tiangan else 0
        shichen_idx = (hour + 1) // 2 % 12
        base_gan_idx = (day_gan_idx % 5) * 2
        gan_idx = (base_gan_idx + shichen_idx) % 10
        return tiangan[gan_idx] + dizhi[shichen_idx]


# 便捷函数
def daliuren_paipan(year: int, month: int, day: int, hour: int,
                    minute: int = 0) -> Dict:
    """快速排盘"""
    service = DaliurenService()
    return service.paipan(year, month, day, hour, minute)
