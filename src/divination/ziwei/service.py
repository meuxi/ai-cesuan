"""
紫微斗数服务入口
整合计算器和分析器，提供统一的紫微服务接口
"""
from typing import Dict, List
from lunar_python import Lunar, Solar

from .calculators.minggong import MingGongCalculator
from .calculators.xingxiu import XingXiuCalculator
from .analyzers.mingpan import MingPanAnalyzer


class ZiweiService:
    """紫微斗数服务类"""
    
    def __init__(self):
        """初始化服务"""
        self.minggong_calc = MingGongCalculator
        self.xingxiu_calc = XingXiuCalculator
        self.mingpan_analyzer = MingPanAnalyzer
    
    def paipan(self, year: int, month: int, day: int, hour: int,
               gender: str = '男', is_lunar: bool = False) -> Dict:
        """排盘
        
        Args:
            year, month, day, hour: 时间
            gender: 性别
            is_lunar: 是否农历
            
        Returns:
            完整的紫微命盘信息
        """
        # 1. 转换为农历（如需要）
        if not is_lunar:
            lunar_info = self._solar_to_lunar(year, month, day)
            lunar_year = lunar_info['year']
            lunar_month = lunar_info['month']
            lunar_day = lunar_info['day']
        else:
            lunar_year = year
            lunar_month = month
            lunar_day = day
        
        # 2. 获取时支
        shi_zhi = self._get_shi_zhi(hour)
        year_gan = self._get_year_gan(lunar_year)
        year_zhi = self._get_year_zhi(lunar_year)
        
        # 3. 计算命宫和身宫
        ming_gong = self.minggong_calc.calculate_ming_gong(lunar_month, shi_zhi)
        shen_gong = self.minggong_calc.calculate_shen_gong(lunar_month, shi_zhi)
        
        # 4. 安排十二宫
        gong_layout = self.minggong_calc.arrange_twelve_gong(ming_gong)
        
        # 5. 计算五行局
        wuxing_ju = self.xingxiu_calc.calculate_wuxing_ju(ming_gong, year_gan)
        
        # 6. 安星曜
        star_layout = self.xingxiu_calc.calculate_all_stars(
            wuxing_ju, lunar_day, lunar_month, shi_zhi, year_gan, year_zhi
        )
        
        # 7. 分析命盘
        # 组织宫位星曜
        gong_stars = self._organize_gong_stars(gong_layout, star_layout)
        analysis = self.mingpan_analyzer.analyze_full_pan(gong_stars)
        
        return {
            'datetime': f"{year}-{month:02d}-{day:02d} {hour:02d}:00",
            'gender': gender,
            'lunar_year': lunar_year,
            'lunar_month': lunar_month,
            'lunar_day': lunar_day,
            'shi_zhi': shi_zhi,
            'wuxing_ju': wuxing_ju,
            'ming_gong': ming_gong,
            'shen_gong': shen_gong,
            'gong_layout': gong_layout,
            'star_layout': star_layout,
            'analysis': analysis
        }
    
    def _solar_to_lunar(self, year: int, month: int, day: int) -> Dict:
        """公历转农历"""
        solar = Solar.fromYmd(year, month, day)
        lunar = solar.getLunar()
        return {
            'year': lunar.getYear(),
            'month': abs(lunar.getMonth()),
            'day': lunar.getDay(),
            'is_leap': lunar.getMonth() < 0,
            'year_ganzhi': lunar.getYearInGanZhi(),
            'month_cn': lunar.getMonthInChinese(),
            'day_cn': lunar.getDayInChinese()
        }
    
    def _get_shi_zhi(self, hour: int) -> str:
        """获取时支"""
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        idx = (hour + 1) // 2 % 12
        return dizhi[idx]
    
    def _get_year_gan(self, year: int) -> str:
        """获取年干"""
        tiangan = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
        return tiangan[(year - 4) % 10]
    
    def _get_year_zhi(self, year: int) -> str:
        """获取年支"""
        dizhi = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
        return dizhi[(year - 4) % 12]
    
    def _organize_gong_stars(self, gong_layout: Dict[str, str],
                             star_layout: Dict[str, str]) -> Dict[str, List[str]]:
        """组织宫位星曜"""
        gong_stars = {gong: [] for gong in gong_layout.keys()}
        
        # 反转：地支 -> 宫名
        zhi_to_gong = {v: k for k, v in gong_layout.items()}
        
        for star, zhi in star_layout.items():
            gong = zhi_to_gong.get(zhi)
            if gong and gong in gong_stars:
                gong_stars[gong].append(star)
        
        return gong_stars


# 便捷函数
def ziwei_paipan(year: int, month: int, day: int, hour: int,
                 gender: str = '男', is_lunar: bool = False) -> Dict:
    """快速排盘"""
    service = ZiweiService()
    return service.paipan(year, month, day, hour, gender, is_lunar)
