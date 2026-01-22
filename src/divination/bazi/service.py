"""
八字服务入口
整合计算器和分析器，提供统一的八字服务接口
参考 mingpan 的 BaziService.ts 实现

修复记录：
- 2026-01: 使用 lunar_python 正确处理节气交接，修复月柱计算不准问题
"""
from typing import Dict, Optional
from datetime import datetime
import logging

from lunar_python import Solar

from .calculators.ganzhi import GanZhi
from .calculators.nayin import NaYin
from .calculators.lunar import solar_to_lunar, lunar_to_solar
from .analyzers.shishen import TenGodsAnalyzer, analyze_ten_gods
from .analyzers.wuxing import WuXingAnalyzer

_logger = logging.getLogger(__name__)


class BaziService:
    """八字服务类
    
    使用 lunar_python 库计算四柱，正确处理节气交接问题：
    - 年柱以立春为界（不是农历新年）
    - 月柱以节气为界（立春、惊蛰、清明等）
    """
    
    def __init__(self):
        """初始化服务"""
        self.ganzhi = GanZhi
        self.nayin = NaYin
        self.ten_gods_analyzer = TenGodsAnalyzer()
        self.wuxing_analyzer = WuXingAnalyzer()
    
    def calculate(self, year: int, month: int, day: int, hour: int,
                  minute: int = 0, gender: str = '男') -> Dict:
        """计算八字
        
        使用 lunar_python 的 EightChar 类计算，正确处理：
        - 年柱：立春交节换年柱
        - 月柱：节气交节换月柱（立春、惊蛰、清明...）
        - 日柱：子时换日柱（23点后算下一天）
        - 时柱：根据日干推时干
        
        Args:
            year: 公历年
            month: 公历月
            day: 公历日
            hour: 时辰（0-23）
            minute: 分钟
            gender: 性别
            
        Returns:
            完整的八字信息
        """
        try:
            # 使用 lunar_python 精确计算四柱（自动处理节气交接）
            solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
            lunar = solar.getLunar()
            bazi = lunar.getEightChar()
            
            # 提取四柱干支
            year_gz = bazi.getYear()    # 年柱（立春交接）
            month_gz = bazi.getMonth()  # 月柱（节气交接）
            day_gz = bazi.getDay()      # 日柱
            hour_gz = bazi.getTime()    # 时柱
            
            # 组装四柱信息
            sizhu = {
                'year': year_gz,
                'month': month_gz,
                'day': day_gz,
                'hour': hour_gz
            }
            
            # 计算纳音
            nayin = {
                'year': self.nayin.get_nayin(year_gz),
                'month': self.nayin.get_nayin(month_gz),
                'day': self.nayin.get_nayin(day_gz),
                'hour': self.nayin.get_nayin(hour_gz)
            }
            
            # 日主信息
            day_master = day_gz[0]
            day_master_wuxing = GanZhi.WUXING_MAP.get(day_master, '未知')
            
            # 获取农历信息
            lunar_info = {
                'year': lunar.getYear(),
                'month': lunar.getMonth(),
                'day': lunar.getDay(),
                'is_leap': lunar.getMonth() < 0,
                'year_ganzhi': lunar.getYearInGanZhi(),
                'month_cn': lunar.getMonthInChinese(),
                'day_cn': lunar.getDayInChinese()
            }
            
            # 获取节气信息
            jieqi_info = self._get_jieqi_info(solar, bazi)
            
            return {
                'sizhu': sizhu,
                'nayin': nayin,
                'day_master': day_master,
                'day_master_wuxing': day_master_wuxing,
                'lunar_info': lunar_info,
                'jieqi_info': jieqi_info,
                'gender': gender
            }
            
        except Exception as e:
            _logger.error(f"八字计算失败，回退到简化算法: {e}")
            # 回退到原有简化算法
            return self._calculate_fallback(year, month, day, hour, minute, gender)
    
    def _get_jieqi_info(self, solar: Solar, bazi) -> Dict:
        """获取节气相关信息"""
        try:
            lunar = solar.getLunar()
            jie = lunar.getPrevJie()  # 上一个节
            qi = lunar.getPrevQi()    # 上一个气
            
            return {
                'prev_jie': jie.getName() if jie else None,
                'prev_qi': qi.getName() if qi else None,
                'month_jie': bazi.getMonthJie() if hasattr(bazi, 'getMonthJie') else None,
            }
        except Exception:
            return {}
    
    def _calculate_fallback(self, year: int, month: int, day: int, hour: int,
                           minute: int = 0, gender: str = '男') -> Dict:
        """简化计算（作为回退方案）"""
        lunar_info = solar_to_lunar(year, month, day)
        
        year_gz = self._calculate_year_pillar(lunar_info)
        month_gz = self._calculate_month_pillar(year_gz[0], lunar_info)
        day_gz = self._calculate_day_pillar(year, month, day)
        hour_gz = self._calculate_hour_pillar(day_gz[0], hour)
        
        sizhu = {
            'year': year_gz,
            'month': month_gz,
            'day': day_gz,
            'hour': hour_gz
        }
        
        nayin = {
            'year': self.nayin.get_nayin(year_gz),
            'month': self.nayin.get_nayin(month_gz),
            'day': self.nayin.get_nayin(day_gz),
            'hour': self.nayin.get_nayin(hour_gz)
        }
        
        day_master = day_gz[0]
        day_master_wuxing = GanZhi.WUXING_MAP.get(day_master, '未知')
        
        return {
            'sizhu': sizhu,
            'nayin': nayin,
            'day_master': day_master,
            'day_master_wuxing': day_master_wuxing,
            'lunar_info': lunar_info,
            'gender': gender,
            '_fallback': True  # 标记为回退计算
        }
    
    def analyze(self, bazi_chart: Dict, day_master_strength: str = '正格') -> Dict:
        """分析八字
        
        Args:
            bazi_chart: 八字信息
            day_master_strength: 日主旺衰
            
        Returns:
            分析结果
        """
        # 1. 十神分析
        ten_gods = self.ten_gods_analyzer.analyze_chart(bazi_chart, day_master_strength)
        
        # 2. 五行分析
        wuxing = self.wuxing_analyzer.analyze(bazi_chart.get('sizhu', {}))
        
        return {
            'ten_gods': ten_gods,
            'wuxing': wuxing
        }
    
    def full_analysis(self, year: int, month: int, day: int, hour: int,
                      minute: int = 0, gender: str = '男') -> Dict:
        """完整的八字计算和分析
        
        Args:
            year, month, day, hour, minute: 时间
            gender: 性别
            
        Returns:
            完整的八字和分析结果
        """
        # 计算八字
        bazi_chart = self.calculate(year, month, day, hour, minute, gender)
        
        # 分析八字
        analysis = self.analyze(bazi_chart)
        
        return {
            **bazi_chart,
            'analysis': analysis
        }
    
    def _calculate_year_pillar(self, lunar_info: Dict) -> str:
        """计算年柱"""
        lunar_year = lunar_info.get('year', 2000)
        # 简化计算：1984年为甲子年
        idx = (lunar_year - 4) % 60
        gan_idx = idx % 10
        zhi_idx = idx % 12
        return GanZhi.TIANGAN[gan_idx] + GanZhi.DIZHI[zhi_idx]
    
    def _calculate_month_pillar(self, year_gan: str, lunar_info: Dict) -> str:
        """计算月柱"""
        month = lunar_info.get('month', 1)
        year_gan_idx = GanZhi.TIANGAN.index(year_gan) if year_gan in GanZhi.TIANGAN else 0
        
        # 年上起月法
        base_gan_idx = (year_gan_idx % 5) * 2 + 2
        gan_idx = (base_gan_idx + month - 1) % 10
        zhi_idx = (month + 1) % 12  # 正月寅，二月卯...
        
        return GanZhi.TIANGAN[gan_idx] + GanZhi.DIZHI[zhi_idx]
    
    def _calculate_day_pillar(self, year: int, month: int, day: int) -> str:
        """计算日柱"""
        # 使用基准日期计算
        from datetime import date
        base_date = date(1900, 1, 31)  # 1900年1月31日是甲子日
        target_date = date(year, month, day)
        diff = (target_date - base_date).days
        
        idx = diff % 60
        gan_idx = idx % 10
        zhi_idx = idx % 12
        
        return GanZhi.TIANGAN[gan_idx] + GanZhi.DIZHI[zhi_idx]
    
    def _calculate_hour_pillar(self, day_gan: str, hour: int) -> str:
        """计算时柱"""
        day_gan_idx = GanZhi.TIANGAN.index(day_gan) if day_gan in GanZhi.TIANGAN else 0
        
        # 时辰索引（子时=0）
        shichen_idx = (hour + 1) // 2 % 12
        
        # 日上起时法
        base_gan_idx = (day_gan_idx % 5) * 2
        gan_idx = (base_gan_idx + shichen_idx) % 10
        
        return GanZhi.TIANGAN[gan_idx] + GanZhi.DIZHI[shichen_idx]


# 便捷函数
def bazi_calculate(year: int, month: int, day: int, hour: int,
                   minute: int = 0, gender: str = '男') -> Dict:
    """快速计算八字"""
    service = BaziService()
    return service.calculate(year, month, day, hour, minute, gender)


def bazi_full_analysis(year: int, month: int, day: int, hour: int,
                       minute: int = 0, gender: str = '男') -> Dict:
    """快速计算和分析八字"""
    service = BaziService()
    return service.full_analysis(year, month, day, hour, minute, gender)
